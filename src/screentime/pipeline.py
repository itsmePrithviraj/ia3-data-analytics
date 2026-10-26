"""Load -> validate -> transform -> EDA -> paired inference -> export.

The same functions handle simulated and real CSV inputs. Source identity is
explicit and propagated to every artifact. No participant outcomes are imputed.
"""

import hashlib
import importlib.metadata
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from .simulate import DAY_COLUMNS, INPUT_COLUMNS

GUARDS = ["consent", "btech_enrolled", "first_response", "estimate_before_check", "record_scope_confirmed"]
METRICS = ["estimated_daily_minutes", "recorded_daily_minutes", "signed_error_minutes", "absolute_error_minutes"]


def parse_time(value):
    """Strict H:MM parsing; missing/invalid is NaN, never zero."""
    match = re.fullmatch(r"(\d{1,2}):([0-5]\d)", str(value).strip())
    if not match:
        return np.nan
    hours, minutes = map(int, match.groups())
    total = 60 * hours + minutes
    return float(total) if total <= 1440 else np.nan


def load_source(config_path):
    config_path = Path(config_path).resolve()
    config = json.loads(config_path.read_text())
    root = config_path.parent.parent
    kind = config.get("data_kind")
    if kind not in {"SIMULATED", "REAL"}:
        raise ValueError("config.data_kind must explicitly be SIMULATED or REAL.")
    alpha = config.get("alpha", 0.05)
    if not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between zero and one.")
    source = (root / config["input_csv"]).resolve()
    output = (root / config["output_dir"]).resolve()
    if output == source.parent or output in source.parents:
        raise ValueError("Keep output_dir separate from the source data directory.")
    if kind == "REAL" and "simulated" in source.parts:
        raise ValueError("A file in data/simulated cannot be used as REAL survey data.")
    if not source.exists():
        raise FileNotFoundError(f"No source file at {source}. Add the real export or use config/simulated.json.")
    raw = pd.read_csv(source, dtype=str, keep_default_na=False)
    if raw.empty:
        raise ValueError("The input contains no observations. A blank template is not a dataset.")
    # Inspect the provenance marker BEFORE applying optional form-header mapping.
    if "data_origin" in raw:
        markers = set(raw["data_origin"].str.strip().str.upper())
        if markers != {kind}:
            raise ValueError(f"Row provenance {markers} does not match declared {kind}; do not mix sources.")
    elif kind == "SIMULATED":
        raise ValueError("SIMULATED inputs must carry a data_origin=SIMULATED column.")
    mapping = config.get("column_map", {})
    missing_headers = set(mapping) - set(raw.columns)
    if missing_headers:
        raise ValueError(f"Mapped form headers not present: {sorted(missing_headers)}")
    raw = raw.rename(columns=mapping)
    if raw.columns.duplicated().any():
        raise ValueError("Column mapping produced duplicate field names.")
    missing = set(INPUT_COLUMNS) - set(raw.columns)
    if missing:
        raise ValueError(f"Required columns missing: {sorted(missing)}. See data/templates/survey_template.csv.")
    # Do not propagate unexpected fields such as Google Forms email addresses.
    raw = raw[INPUT_COLUMNS].copy()
    return config, source, output, raw


def prepare_data(raw, kind):
    """One row per student; validate and derive variables."""
    frame = raw.copy().reset_index(drop=True)
    frame.insert(0, "source_row", np.arange(2, len(frame) + 2))  # physical CSV row, including header
    prefix = "SIM" if kind == "SIMULATED" else "ST"
    frame.insert(0, "participant_id", [f"{prefix}{i:04d}" for i in range(1, len(frame) + 1)])
    frame.insert(0, "data_origin", kind)
    reasons = [[] for _ in range(len(frame))]
    for column in GUARDS:
        values = frame[column].astype(str).str.strip().str.lower()
        for i in np.flatnonzero(~values.eq("yes")):
            reasons[i].append(f"{column}_not_yes")
    dates = pd.to_datetime(frame["reference_end_date"], format="%Y-%m-%d", errors="coerce")
    strict = frame["reference_end_date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}")
    for i in np.flatnonzero(dates.isna() | ~strict):
        reasons[i].append("invalid_reference_end_date")
    frame["estimated_daily_minutes"] = frame["estimated_daily_time"].map(parse_time)
    for column in DAY_COLUMNS:
        frame[column.replace("_time", "_minutes")] = frame[column].map(parse_time)
    numeric_days = [c.replace("_time", "_minutes") for c in DAY_COLUMNS]
    for i in np.flatnonzero(frame["estimated_daily_minutes"].isna()):
        reasons[i].append("invalid_or_missing_estimate")
    for i in np.flatnonzero(frame[numeric_days].isna().any(axis=1)):
        reasons[i].append("invalid_or_missing_daily_record")
    # skipna=False prevents a six-day week from silently becoming a valid average.
    frame["recorded_daily_minutes"] = frame[numeric_days].mean(axis=1, skipna=False)
    frame["signed_error_minutes"] = frame["recorded_daily_minutes"] - frame["estimated_daily_minutes"]
    frame["absolute_error_minutes"] = frame["signed_error_minutes"].abs()
    frame["possible_duplicate"] = raw[INPUT_COLUMNS].duplicated(keep=False).to_numpy()
    # Identical measurements do not establish duplicate people; flag, do not delete.
    frame["included"] = [not reason for reason in reasons]
    frame["exclusion_reasons"] = [";".join(reason) for reason in reasons]
    frame["perception_group"] = "unavailable"
    valid = frame["included"]
    error = frame.loc[valid, "signed_error_minutes"]
    frame.loc[valid, "perception_group"] = np.select(
        [error > 30, error < -30], ["Underestimated >30 min", "Overestimated >30 min"],
        default="Within 30 min",
    )
    return frame, frame.loc[valid].copy().reset_index(drop=True)


def paired_analysis(clean, alpha=0.05):
    """A paired t-test is a one-sample t-test on within-person differences."""
    difference = clean["signed_error_minutes"].to_numpy(float)
    n = len(difference)
    result = {"n": n, "alpha": alpha, "difference": "recorded minus estimated, minutes/day",
              "alternative": "two-sided", "status": "insufficient_data", "warnings": []}
    if n < 60:
        result["warnings"].append("Fewer than the practical project target of 60 usable pairs; not a formal power rule.")
    if n == 0:
        return result
    result.update(mean_difference=float(np.mean(difference)), median_difference=float(np.median(difference)),
                  mean_absolute_error=float(np.mean(np.abs(difference))),
                  median_absolute_error=float(np.median(np.abs(difference))))
    if n < 2:
        return result
    sd = float(np.std(difference, ddof=1))
    result.update(sd_difference=sd, df=n - 1)
    if sd == 0:
        result["status"] = "zero_variance"
        result["warnings"].append("All differences are identical; an ordinary paired t-test is not reported.")
        return result
    se = sd / math.sqrt(n)
    manual_t = float(np.mean(difference) / se)
    manual_p = float(2 * stats.t.sf(abs(manual_t), df=n - 1))
    test = stats.ttest_rel(clean["recorded_daily_minutes"], clean["estimated_daily_minutes"],
                           alternative="two-sided", nan_policy="raise")
    if not (np.isclose(manual_t, test.statistic) and np.isclose(manual_p, test.pvalue, atol=1e-14)):
        raise AssertionError("Hand-formula and SciPy paired-test results disagree.")
    ci = stats.t.interval(1 - alpha, n - 1, loc=np.mean(difference), scale=se)
    q1, q3 = np.quantile(difference, [0.25, 0.75])
    iqr = q3 - q1
    flags = int(np.sum((difference < q1 - 1.5 * iqr) | (difference > q3 + 1.5 * iqr)))
    if flags:
        result["warnings"].append(f"{flags} differences outside Tukey fences: inspect, do not automatically remove.")
    result.update(status="computed_assumptions_need_review", standard_error=se, t_statistic=manual_t,
                  p_value=manual_p, ci_level=1-alpha, ci_low=float(ci[0]), ci_high=float(ci[1]),
                  cohens_dz=float(np.mean(difference) / sd), tukey_flag_count=flags,
                  decision="reject H0" if manual_p < alpha else "fail to reject H0")
    return result


def descriptive_table(clean, kind):
    table = clean[METRICS].describe().T.reset_index(names="variable")
    table.insert(0, "data_origin", kind)
    table.insert(2, "unit", "minutes/day")
    return table


def plot_figures(clean, output, kind):
    if clean.empty:
        return []
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="notebook", font_scale=1.05)
    plt.rcParams.update({"figure.dpi": 120, "savefig.dpi": 180, "axes.spines.top": False,
                         "axes.spines.right": False, "font.family": "DejaVu Sans"})
    label = "SIMULATED — demonstration only" if kind == "SIMULATED" else "REAL SURVEY — convenience sample"
    paths = []

    def save(fig, name):
        fig.text(0.5, 0.015, label, ha="center", fontsize=10, color="#9b3a20" if kind == "SIMULATED" else "#505050")
        fig.tight_layout(rect=(0, 0.055, 1, 0.96))
        for extension in ("png", "pdf"):
            path = output / f"{name}.{extension}"
            fig.savefig(path, bbox_inches="tight")
            paths.append(str(path))
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    sns.scatterplot(data=clean, x="estimated_daily_minutes", y="recorded_daily_minutes", ax=ax,
                    color="#245c82", alpha=0.7, s=45, edgecolor="white")
    limit = float(clean[["estimated_daily_minutes", "recorded_daily_minutes"]].max().max()) * 1.08
    limit = max(limit, 60)
    ax.plot([0, limit], [0, limit], "--", color="#a4492b", label="Perfect agreement")
    ax.set(xlim=(0, limit), ylim=(0, limit), xlabel="Estimated average (minutes/day)",
           ylabel="Phone-recorded average (minutes/day)", title="Do estimates match the phone records?")
    ax.legend(frameon=False)
    save(fig, "01_estimated_vs_recorded")

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    bins = min(20, max(5, int(np.sqrt(len(clean)))))
    sns.histplot(clean["signed_error_minutes"], bins=bins, ax=ax, color="#245c82", edgecolor="white")
    ax.axvline(0, color="#a4492b", linestyle="--", label="No estimation error")
    ax.set(xlabel="Recorded − estimated (minutes/day)", ylabel="Students",
           title="Direction and size of estimation error")
    ax.legend(frameon=False)
    save(fig, "02_signed_errors")

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    order = ["Overestimated >30 min", "Within 30 min", "Underestimated >30 min"]
    counts = clean["perception_group"].value_counts().reindex(order, fill_value=0)
    bars = ax.barh(order, counts / len(clean) * 100, color=["#977144", "#61866b", "#245c82"])
    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{count} ({count/len(clean):.1%})", va="center", fontsize=10)
    ax.set(xlim=(0, max(100, counts.max()/len(clean)*100 + 25)), xlabel="Share of included students (%)",
           title="How close were the estimates? (±30-minute convention)")
    ax.invert_yaxis()
    save(fig, "03_accuracy_groups")

    if len(clean) >= 3 and clean["signed_error_minutes"].std() > 0:
        fig, ax = plt.subplots(figsize=(6.4, 4.8))
        stats.probplot(clean["signed_error_minutes"], dist="norm", plot=ax)
        ax.set(title="Assumption check: distribution of paired differences",
               xlabel="Theoretical normal quantiles", ylabel="Observed differences (minutes/day)")
        save(fig, "04_difference_qq")
    return paths


def run_pipeline(config_path):
    config, source, output, raw = load_source(config_path)
    kind = config["data_kind"]
    audited, clean = prepare_data(raw, kind)
    result = paired_analysis(clean, config.get("alpha", 0.05))
    result["data_origin"] = kind
    output.mkdir(parents=True, exist_ok=True)
    # Remove only known previous generated figure artifacts; never delete user files.
    for stem in ["01_estimated_vs_recorded", "02_signed_errors", "03_accuracy_groups", "04_difference_qq"]:
        for suffix in ["png", "pdf"]:
            (output / "figures" / f"{stem}.{suffix}").unlink(missing_ok=True)
    audited.to_csv(output / "audit.csv", index=False)
    clean.to_csv(output / "cleaned.csv", index=False)
    description = descriptive_table(clean, kind)
    description.to_csv(output / "descriptive_statistics.csv", index=False)
    counts = audited.loc[~audited["included"], "exclusion_reasons"].str.split(";").explode().value_counts()
    exclusions = counts.rename_axis("reason").reset_index(name="rows")
    exclusions.insert(0, "data_origin", kind)
    exclusions.to_csv(output / "exclusion_counts.csv", index=False)
    (output / "statistics.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    figures = plot_figures(clean, output / "figures", kind)
    manifest = {
        "data_origin": kind, "source_file": config["input_csv"],
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "submitted": len(raw), "included": len(clean), "excluded": len(raw)-len(clean),
        "possible_duplicate_rows": int(audited["possible_duplicate"].sum()),
        "config": config,
        "versions": {name: importlib.metadata.version(name) for name in ["numpy", "pandas", "scipy", "matplotlib", "seaborn"]},
        "scope": "Simulation demonstration, not student evidence" if kind == "SIMULATED" else "Volunteer B.Tech sample; no population representativeness established",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    lines = [f"# {kind}: screen-time analysis", "",
             "**SIMULATED DATA — no students were surveyed; numerical results demonstrate the workflow only.**" if kind == "SIMULATED" else
             "Participant-transcribed phone records from a convenience sample; assumptions and collection quality require review.", "",
             f"Submitted: {len(raw)}. Included: {len(clean)}. Excluded: {len(raw)-len(clean)}.",
             "Exclusion reason counts may overlap. IDs refer to rows of this frozen source file.", ""]
    if "mean_difference" in result:
        lines.extend([f"Mean recorded-minus-estimated difference: {result['mean_difference']:.2f} minutes/day.",
                      f"Mean absolute error: {result['mean_absolute_error']:.2f} minutes/day."])
    if "p_value" in result:
        lines.extend([f"Paired t({result['df']}) = {result['t_statistic']:.4f}; two-sided p = {result['p_value']:.6g}.",
                      f"{result['ci_level']:.0%} confidence interval: [{result['ci_low']:.2f}, {result['ci_high']:.2f}] minutes/day.",
                      f"Mechanical test decision: {result['decision']} at alpha={result['alpha']}. Review assumptions before interpretation."])
    else:
        lines.append(f"Test not reported: {result['status']}.")
    lines.extend(["", "Positive differences mean underestimation. Zero mean bias does not establish individual accuracy.",
                  "No causal, addiction, or academic-performance conclusion is supported.", "",
                  *[f"- {warning}" for warning in result["warnings"]]])
    (output / "RUN_SUMMARY.md").write_text("\n".join(lines) + "\n")
    return {"config": config, "raw": raw, "audited": audited, "clean": clean,
            "descriptive": description, "statistics": result, "manifest": manifest,
            "figures": figures, "output_dir": output}
