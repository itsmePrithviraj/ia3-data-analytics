"""Generate development data, never collected participant observations."""

import json
from pathlib import Path

import numpy as np
import pandas as pd

DAY_COLUMNS = [f"day_{i}_time" for i in range(1, 8)]
INPUT_COLUMNS = [
    "consent", "btech_enrolled", "first_response", "reference_end_date",
    "estimated_daily_time", *DAY_COLUMNS,
    "estimate_before_check", "record_scope_confirmed",
]


def as_time(minutes):
    """Represent integer minutes as H:MM; do not confuse 4:30 with 4.30 hours."""
    return f"{int(minutes) // 60}:{int(minutes) % 60:02d}"


def generate(n=120, seed=20261017, with_quality_cases=True):
    """Assumed distributions, deliberately not calibrated to student research."""
    if n < 10:
        raise ValueError("Use at least 10 rows for the simulation.")
    rng = np.random.default_rng(seed)
    # Positive, right-skewed person-level usage, with person-to-person variation.
    typical = np.clip(rng.lognormal(np.log(270), 0.43, n), 45, 850)
    rows = []
    for i, baseline in enumerate(typical):
        end = pd.Timestamp("2026-10-13") + pd.Timedelta(days=i % 5)
        daily = []
        for offset in range(7):
            # The form lists day 1 (oldest) through day 7 (reference end).
            date = end - pd.Timedelta(days=6-offset)
            weekend_multiplier = 1.10 if date.dayofweek >= 5 else 1.0
            value = baseline * weekend_multiplier * rng.lognormal(-0.23**2 / 2, 0.23)
            daily.append(int(np.clip(np.round(value), 0, 1200)))
        # Some overestimate and some underestimate. No seed or parameter search
        # is performed to obtain a preferred p-value.
        bias = rng.normal(20, 65)
        error = rng.normal(0, 25)
        estimate = int(np.clip(np.round((np.mean(daily) - bias + error) / 15) * 15, 0, 1440))
        rows.append({
            "data_origin": "SIMULATED", "consent": "Yes", "btech_enrolled": "Yes",
            "first_response": "Yes", "reference_end_date": end.date().isoformat(),
            "estimated_daily_time": as_time(estimate),
            **dict(zip(DAY_COLUMNS, map(as_time, daily))),
            "estimate_before_check": "Yes", "record_scope_confirmed": "Yes",
        })
    frame = pd.DataFrame(rows)
    if with_quality_cases:
        # Visible, documented test cases demonstrate cleaning without pretending
        # these rates or problems were observed in a survey.
        cases = {0: ("day_3_time", ""), 1: ("day_2_time", "24:15"),
                 2: ("estimate_before_check", "No"), 3: ("consent", "No"),
                 4: ("btech_enrolled", "No"), 5: ("first_response", "No"),
                 6: ("reference_end_date", "2026-02-30"),
                 7: ("record_scope_confirmed", "No")}
        for row, (column, value) in cases.items():
            frame.loc[row, column] = value
    return frame


def save_simulation(path, n=120, seed=20261017):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = generate(n, seed)
    frame.to_csv(path, index=False)
    metadata = {
        "data_origin": "SIMULATED", "seed": seed, "rows": n,
        "purpose": "Development and teaching only; no respondents were surveyed.",
        "reference_end_dates": "2026-10-13 through 2026-10-17 (fictional)",
        "day_order": "day_1 is six days before reference_end_date; day_7 is reference_end_date",
        "assumptions": {"median_baseline_minutes": 270, "baseline_log_sd": 0.43,
                        "weekend_multiplier": 1.10, "daily_log_sd": 0.23,
                        "mean_underestimation_minutes": 20, "bias_sd": 65,
                        "additional_estimate_noise_sd": 25, "estimate_rounding_minutes": 15},
        "quality_cases": "First eight rows each contain one deliberate exclusion case; see simulate.py.",
        "not_calibrated_to_real_data": True,
    }
    path.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    return frame
