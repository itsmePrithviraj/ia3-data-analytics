# Replace simulation with real survey responses
## 1. Keep the source
Export the single form as CSV. Preserve the original, unchanged, under `data/raw/`; it is Git-ignored. Do not upload email addresses or participant-level exports to GitHub. Do not collect identifiers merely to assign IDs.

A header-only template is provided at `data/templates/survey_template.csv`. It is not a collected dataset. The default real path is `data/raw/screen_time_real.csv`, which is deliberately absent until collection.

## 2. Match headings and values
Use the canonical headers in the template, or edit `config/real.json` to point at your unchanged original export and map its question titles:
```json
"column_map": {
  "Do you voluntarily agree to participate in this course project?": "consent",
  "What was yesterday's date?": "reference_end_date"
}
```
Map every differently named required field. Mapping direction is original heading → canonical heading. Missing required fields and duplicate mapped headings fail clearly. Extra columns such as a form timestamp are not propagated to the analysis table.

Use Yes / No / Not sure, dates YYYY-MM-DD, and duration strings H:MM. Do not allow a spreadsheet editor to turn durations into dates, decimal hours or clock timestamps. If an export uses other conventions, preserve it and make a documented conversion copy; do not guess silently.

## 3. Run
```sh
source .venv/bin/activate
python run.py --config config/real.json
```
In the notebook separately change:
```python
CONFIG_PATH = ROOT / "config/real.json"
```
Restart the kernel and run all cells. Real input does not exist yet; the command should fail until you supply it.

The source path, mode and output directory come from config. Real outputs go to `outputs/real/`, separately from the demonstration. Known SIMULATED markers are rejected in REAL mode. These safeguards cannot verify truth: do not strip simulation labels and rename a generated file as real.

## 4. Inspect before drawing conclusions
Review `audit.csv` and excluded rows, verify source dates against the submission dates, review flagged duplicates without assuming they are the same person, and inspect the figures and assumptions. Confirm included count and missingness. Keep a short collection log with form version, recruitment approach, dates and pilot handling.

IDs are assigned in source-row order before exclusions. The source hash identifies that exact export. Keep it frozen; sorting or replacing rows can change which person has a given ID. IDs are not respondent-entered or portable identity keys.

The eight deliberate bad rows are specific to the simulation. A real dataset may have none or different issues. Never manufacture missingness in actual responses to make preprocessing look substantial.

## 5. Protect the distinction
Never mix simulated rows into collected responses to reach a target. A non-significant real result is acceptable and informative. Keep simulation outputs clearly labelled if retained as development examples.

Real CSVs and output folders are ignored by Git, but **notebook outputs are embedded in the notebook file**. Clear real-data notebook outputs before committing, or save that executed copy locally under `outputs/real/`. Review staged files before pushing. Missing values and excluded participants must remain disclosed in the report.

The final 4–5 page report should identify the true dataset source, included n, exclusions, limitations and findings from the selected source. This implementation does not create or submit the final report.
