"""Check statistical arithmetic and input boundaries, not only happy-path output."""
import json

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from screentime.pipeline import load_source, paired_analysis, parse_time, prepare_data, run_pipeline
from screentime.simulate import INPUT_COLUMNS, generate


@pytest.mark.parametrize("value,expected", [("0:00", 0), ("4:30", 270), ("24:00", 1440), (" 2:07 ", 127)])
def test_time_conversion(value, expected):
    assert parse_time(value) == expected


@pytest.mark.parametrize("value", ["", "4.30", "2:60", "24:01", "25:00", "-1:00", "3:5", "nan", None])
def test_bad_times_are_missing_not_zero(value):
    assert np.isnan(parse_time(value))


def test_missing_day_does_not_silently_average_six_days():
    raw = generate(with_quality_cases=False)[INPUT_COLUMNS].iloc[:2].copy()
    raw.loc[0, "day_3_time"] = ""
    audit, clean = prepare_data(raw, "SIMULATED")
    assert np.isnan(audit.loc[0, "recorded_daily_minutes"])
    assert len(clean) == 1
    assert "daily_record" in audit.loc[0, "exclusion_reasons"]


def test_deliberate_quality_cases_and_reproducibility():
    raw = generate()
    pd.testing.assert_frame_equal(raw, generate())
    audit, clean = prepare_data(raw[INPUT_COLUMNS], "SIMULATED")
    assert len(audit) == 120 and len(clean) == 112
    assert audit["participant_id"].is_unique
    assert audit.iloc[:8]["included"].sum() == 0
    assert audit.iloc[8:]["included"].all()


def test_identical_measurements_are_flagged_but_not_deleted():
    row = generate(with_quality_cases=False)[INPUT_COLUMNS].iloc[[0]]
    audit, clean = prepare_data(pd.concat([row, row], ignore_index=True), "SIMULATED")
    assert audit["possible_duplicate"].all()
    assert len(clean) == 2


def test_simulated_days_follow_form_calendar_order(monkeypatch):
    # Remove random variation to isolate calendar alignment. For the first
    # period (Oct 7–13), only day 4 (Saturday) and day 5 (Sunday) are weekends.
    class FixedRandom:
        def lognormal(self, mean, sigma, size=None):
            return np.full(size, 270.) if size is not None else 1.

        def normal(self, mean, sigma):
            return 0.

    monkeypatch.setattr(np.random, "default_rng", lambda seed: FixedRandom())
    row = generate(with_quality_cases=False).iloc[0]
    assert row["reference_end_date"] == "2026-10-13"
    assert [parse_time(row[f"day_{i}_time"]) for i in range(1, 8)] == [270, 270, 270, 297, 297, 270, 270]


def test_known_paired_example_and_confidence_interval():
    # Teaching differences from the course note: 2, 3, 1, 4, 0.
    d = np.array([2., 3., 1., 4., 0.])
    clean = pd.DataFrame({"recorded_daily_minutes": 100+d, "estimated_daily_minutes": 100.,
                          "signed_error_minutes": d})
    result = paired_analysis(clean)
    assert result["df"] == 4
    assert result["mean_difference"] == 2
    assert result["t_statistic"] == pytest.approx(2.8284271247461903)
    assert result["p_value"] == pytest.approx(0.04742065558431962)
    expected_margin = stats.t.ppf(.975, 4) * np.sqrt(.5)
    assert result["ci_low"] == pytest.approx(2 - expected_margin)
    assert result["ci_high"] == pytest.approx(2 + expected_margin)


def test_canceling_errors_are_not_called_accurate():
    d = np.array([-60., 60., -60., 60.])
    frame = pd.DataFrame({"recorded_daily_minutes": 100+d, "estimated_daily_minutes": 100.,
                          "signed_error_minutes": d})
    result = paired_analysis(frame)
    assert result["mean_difference"] == 0
    assert result["mean_absolute_error"] == 60
    assert result["p_value"] == 1


def test_degenerate_samples_do_not_emit_infinite_statistics():
    for d in [[], [2.], [2., 2., 2.]]:
        frame = pd.DataFrame({"signed_error_minutes": d})
        result = paired_analysis(frame)
        assert "p_value" not in result
        json.dumps(result, allow_nan=False)


def write_fixture(tmp_path, frame, kind):
    (tmp_path / "config").mkdir(exist_ok=True)
    source = tmp_path / "input.csv"
    frame.to_csv(source, index=False)
    config = tmp_path / "config" / "test.json"
    config.write_text(json.dumps({"data_kind": kind, "input_csv": "input.csv", "output_dir": "outputs", "alpha": .05}))
    return config


def test_simulation_cannot_accidentally_run_as_real(tmp_path):
    config = write_fixture(tmp_path, generate(), "REAL")
    with pytest.raises(ValueError, match="provenance"):
        load_source(config)


def test_mixed_provenance_rejected(tmp_path):
    frame = generate()
    frame.loc[2, "data_origin"] = "REAL"
    with pytest.raises(ValueError, match="provenance"):
        load_source(write_fixture(tmp_path, frame, "SIMULATED"))


def test_blank_template_fails_clearly(tmp_path):
    config = write_fixture(tmp_path, pd.DataFrame(columns=INPUT_COLUMNS), "REAL")
    with pytest.raises(ValueError, match="no observations"):
        load_source(config)


def test_form_column_mapping_and_id_assignment(tmp_path):
    # A fake export is used only in this temporary unit test, never as research data.
    frame = generate(with_quality_cases=False)[INPUT_COLUMNS].iloc[:3].rename(columns={"consent": "Do you agree?"})
    frame["Email Address"] = "unused@example.test"
    config = write_fixture(tmp_path, frame, "REAL")
    settings = json.loads(config.read_text())
    settings["column_map"] = {"Do you agree?": "consent"}
    config.write_text(json.dumps(settings))
    _, _, _, imported = load_source(config)
    assert "Email Address" not in imported
    audit, clean = prepare_data(imported, "REAL")
    assert audit["participant_id"].tolist() == ["ST0001", "ST0002", "ST0003"]
    assert len(clean) == 3


def test_all_excluded_run_exports_honest_empty_results(tmp_path):
    frame = generate().iloc[:8]
    result = run_pipeline(write_fixture(tmp_path, frame, "SIMULATED"))
    assert result["manifest"]["included"] == 0
    assert result["statistics"]["status"] == "insufficient_data"
    assert result["figures"] == []
    assert "SIMULATED" in (result["output_dir"] / "RUN_SUMMARY.md").read_text()


def test_changing_source_changes_results(tmp_path):
    frame = generate(with_quality_cases=False).iloc[:12]
    config = write_fixture(tmp_path, frame, "SIMULATED")
    first = run_pipeline(config)
    frame["estimated_daily_time"] = "0:00"
    frame.to_csv(tmp_path / "input.csv", index=False)
    second = run_pipeline(config)
    assert first["manifest"]["sha256"] != second["manifest"]["sha256"]
    assert first["statistics"]["mean_difference"] != second["statistics"]["mean_difference"]
