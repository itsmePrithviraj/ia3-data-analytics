# Using survey responses

1. Export the form responses as CSV and keep the original file in `data/raw/`.
2. Use the columns in `data/templates/survey_template.csv`, or map the form's question headings in `config/real.json`.
3. Set `input_csv` to the export path. The default is `data/raw/screen_time_real.csv`.
4. Run:

```sh
python run.py --config config/real.json
```

For example, a header mapping looks like this:

```json
"column_map": {
  "Do you voluntarily agree to participate in this course project?": "consent",
  "What was yesterday's date?": "reference_end_date"
}
```

Map each required question to its matching template column. Durations must be H:MM, dates YYYY-MM-DD, and confirmations Yes/No/Not sure. A valid row requires Yes for all five confirmations and all seven daily readings.

The notebook has its own `CONFIG_PATH`; change it to `ROOT / 'config/real.json'`, restart the kernel and run all cells. Review the audit and charts in `outputs/real/`, then update the report with the new results.

Participant IDs are assigned by source-row order. Keep the original export unchanged so those IDs remain traceable. Do not combine simulated records with collected responses.

Real exports and generated outputs are ignored by Git. Clear notebook outputs before committing a run containing real participant data.
