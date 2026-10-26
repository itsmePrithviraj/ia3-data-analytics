# Team 3 report review and project explanation

Reviewed on 26 October 2026 against the assignment wording supplied by the user. This is a content and implementation review, not a guarantee of marks or instructor acceptance.

## Requirement check

| Requirement | Evidence in the seven-page report |
|---|---|
| Project title | Page 1 identifies estimated and recorded smartphone screen time among B.Tech students |
| Team of 3–5 with names and registration numbers | Page 1 has Team 3 and all three supplied members |
| Dataset source and explanation | Page 1 names the simulated CSV, generator, seed, row counts, measurement pairing and assumptions; page 2 defines variables |
| Preprocessing | Page 2 explains time conversion, checks, eight exclusions, missingness, duplicate flags and derived columns |
| EDA | Pages 3–4 include descriptive statistics, a scatterplot, an error histogram, a normal Q–Q plot and written interpretations |
| CDA with a relevant statistical test | Page 5 states hypotheses, alpha, paired design, calculation, t, degrees of freedom, p, CI, effect size, decision and assumptions; page 6 shows the code |
| Findings and conclusions | Page 7 distinguishes net bias from individual error and explains limitations |
| 4–5 pages | Not met: expanded to seven pages at the user’s explicit request; every page was visually checked |
| Team-based filename | Team_03.docx and Team_03.pdf |
| One report per team and LMS submission | Files prepared; no LMS submission performed. Deadline in supplied brief: 26 October 2026 |

## What is still unresolved

No real participant CSV is present. The report is complete as a disclosed simulation analysis. The assignment text does not explicitly prohibit simulated data, but it does not explicitly approve it either. Confirm whether this meets the instructor's dataset criterion. Genuine survey evidence and conclusions about real students are not yet available.

The generator assumes a tendency to underestimate, so the significant simulated result partly reflects its design. It is not an independent discovery about B.Tech students. Do not relabel the simulated CSV as real or combine generated rows with survey responses.

The GitHub repository was verified as public on 26 October 2026, and the report includes a clickable URL. Submit the required project files with the report through the LMS, following any later instructions. The brief does not require a separate abstract, contents page, machine-learning model or individual contribution section. Peer evaluation instructions remain separate; do not invent contributions.

## How the project works

1. The configuration chooses an input CSV and explicitly declares SIMULATED or REAL mode. The current source is data/simulated/screen_time_simulated.csv.
2. One row represents one participant, containing an estimate and seven daily totals for the same phone and completed dates. Seven days are not seven independent participants.
3. pandas reads the table as strings. The program assigns participant IDs, checks confirmations/dates/durations and converts H:MM to minutes. It preserves the original file and saves an audit.
4. All seven valid daily totals are averaged. Signed error = recorded average minus estimate. Absolute error = the magnitude of that difference.
5. EDA uses summaries and plots to describe the 112 included pairs. NumPy supports numerical calculations; Matplotlib/Seaborn create figures.
6. SciPy performs a two-sided paired t-test of zero mean difference, checked against the manual formula. Matching is within the same person, so an independent-samples test would not fit the design.
7. The program exports the cleaned data, exclusions, figures, statistical results and provenance manifest. The notebook explains the same workflow. A changed source requires rerunning the analysis and updating the report separately.

## Explain the main calculations

For an illustrative student who estimates 4 hours/day and has a recorded daily average of 5 hours, the difference is 300 − 240 = +60 minutes/day. Positive means underestimation; negative means overestimation.

In the current simulation, mean signed error is +22.48 minutes/day and mean absolute error is 59.42 minutes/day. The first measures net bias; the second measures average error size. Errors of +60 and −60 would cancel to zero mean bias while still having 60-minute mean absolute error.

For the test, H0 is mean difference = 0 and H1 is mean difference ≠ 0, with alpha 0.05. The sample SD of differences is 72.17 minutes. SE = SD / sqrt(112) = 6.82 minutes, and t = mean difference / SE = 3.297 with 111 degrees of freedom. The two-sided p-value is 0.00131, below 0.05. Under the assumptions, the simulated analysis rejects zero mean difference.

The 95% CI for mean difference is 8.97–36.00 minutes/day. It concerns uncertainty in the mean, not the range containing most individual errors. The test addresses average bias, not whether every student's estimate is accurate. Independence, distribution shape and the sampling process still matter.

## Verification and learning continuity

All 26 existing project tests pass. The report's displayed mean differences, means, p-value, CI and sample size agree with the saved outputs. The final PDF has seven pages and includes all three names and registration numbers. Report figures were regenerated from the saved cleaned data. Two explained code excerpts match the analysis implementation. The final PDF includes a working repository hyperlink.

This explanation introduces the workflow; no independent student understanding has been assessed. Resume teaching with one CSV row, its seven-day average and signed error, then progress to the EDA charts and paired-test formula. Parent study materials remain unchanged, as requested for this project.
