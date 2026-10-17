# Study protocol — version 0.2, 18 October 2026
## Question and scope
**The Screen-Time Blind Spot:** how accurately do B.Tech students estimate their average daily primary-smartphone screen time?

Recruit friends across B.Tech colleges. This is a voluntary convenience/referral sample, not a representative sample of India or MIT Manipal. One participant contributes one row and a matched estimate/recorded pair. Seven days from that person are repeated measurements used to compute one daily average, not seven independent observations.

The original two-form proposal has been replaced by **one form**. No names, college codes, OS, year, age, gender, grades, app lists or respondent-entered participant IDs are needed for this question. Phone OS was possible context for measurement differences; it is not necessary for the primary paired comparison. Android/iPhone instructions remain as help text.

## Minimal input schema
Use these canonical column names in the CSV, or map full form question headings to them.

| Field | Type / permitted values | Purpose |
|---|---|---|
| consent | Yes / No | Voluntary participation |
| btech_enrolled | Yes / No | Population eligibility |
| first_response | Yes / No | Discourage repeated participation, including a pilot |
| reference_end_date | YYYY-MM-DD | Yesterday; fixes the seven completed dates |
| estimated_daily_time | H:MM, 0:00–24:00 | Estimate before opening the report |
| day_1_time … day_7_time | H:MM, 0:00–24:00 or blank | Seven device-recorded totals, oldest to newest |
| estimate_before_check | Yes / No / Not sure | Estimate entered before checking and not revised |
| record_scope_confirmed | Yes / No / Not sure | Correct dates, one primary phone, complete records |

There are 14 input columns. Collection systems may add a timestamp; it is not an analysis variable. Do not collect email addresses. In the simulated CSV only, an extra `data_origin` column labels every row SIMULATED.

## Date and measurement rules
If yesterday is 2026-10-17, day 1 is 2026-10-11 and day 7 is 2026-10-17. All seven days must be completed. Ask about this exact period before the estimate. Use the same personally used primary smartphone throughout, include all use counted by its report, and exclude combined-device totals. Do not use a partial current-week dashboard average.

Each person supplies their own date window. Phone totals are transcribed by the participant, not independently verified; do not call them perfectly objective measures. Avoid screenshots because they can expose personal information. Device reporting conventions may differ; OS is intentionally uncollected, so this cannot be adjusted for.

One form cannot reliably lock an earlier answer. Sections and an explicit confirmation reduce retrospective changes but cannot prove order or eliminate recall effects.

## Sampling and collection
1. Pilot with five volunteers to check wording, date navigation and duration entry. Keep pilot data separate and exclude pilot participants from the main sample.
2. Revise and freeze the form before main collection. Record the version and collection dates.
3. Aim for 100 valid pairs; 60 is a practical minimum target for this project, not a formal power analysis.
4. Proposed collection stop: 23 October 2026, 21:00 IST, or 100 valid pairs, whichever occurs first. If the timetable changes before collection, document it. Never stop or extend collection based on a p-value.
5. One response per person. No identifying code is requested. This limits reliable deduplication and verification of college coverage.
6. Retain the original export. Assign `ST0001`, `ST0002`, etc. in source order after import; use `SIM` IDs for simulation. Freeze the export to preserve this assignment.

## Inclusion and cleaning
Include rows only when all five consent/eligibility/quality fields are Yes, the date is valid, and the estimate plus all seven daily durations are present and valid. The software accepts durations up to 24:00 and rejects larger or malformed entries. A missing day is not zero and is not imputed. Keep excluded rows with reasons in the audit.

The importer checks date format, but the collector must also verify the date window against the submission date and the collection log. It cannot verify whether a respondent actually opened the correct report. Plausible extreme values are reviewed, not silently trimmed.

Identical full response patterns are flags, not proof of duplicate people. Do not delete them without a documented basis. No personal identifying fields are used to resolve duplicates.

## Outcomes and inference
Recorded daily minutes = sum of the seven valid daily totals / 7.
Signed error = recorded minus estimated; positive means underestimation.
Absolute error = magnitude of the signed error.

Primary hypothesis: population mean signed error is zero versus nonzero; two-sided paired t-test, alpha 0.05. Report mean difference and 95% CI in minutes/day and review the distribution of differences. A mean near zero can hide large individual errors that cancel.

For a descriptive chart only: more than +30 minutes = Underestimated; less than −30 = Overestimated; otherwise Within 30 minutes. This is a project convention, not a validated accuracy or health threshold.

## Simulation and provenance
The included 120 rows are generated with a fixed seed, varied daily use and noisy, rounded estimates. Eight deliberate invalid rows exercise preprocessing. Generation parameters are assumptions, not estimates from a published dataset or real students. The generator does not search for a desired p-value.

Simulation is for building, learning and checking the workflow. Preserve its labels in tables, charts and summaries. Replace the input with genuine responses later; never mix synthetic and real people. If only simulation is available at submission, disclose it and confirm that a simulation study satisfies the instructor's dataset requirement.

## Participation wording
Participation is voluntary; a respondent can stop before submitting. No name or contact details are requested by the form. Explain that without an identifying response code the team may be unable to find an individual's row to withdraw it after submission. Share aggregate analysis in the course report and keep individual exports local.
