# Prespecified analysis — draft v0.1

No participant results exist. Freeze this plan after the pilot and before the main collection; log any later deviation without silently replacing the planned method.

## Primary estimand and hypotheses

For student i, let E_i be estimated average daily primary-phone screen time and R_i be the mean of seven participant-transcribed daily totals, both in minutes/day. Define d_i = R_i − E_i.

- Positive d: participant underestimated phone-recorded use.
- Negative d: participant overestimated phone-recorded use.
- Primary quantity: population mean signed difference, mu_d, interpreted cautiously for the convenience sample.
- H0: mu_d = 0; H1: mu_d != 0. Two-sided paired t-test, alpha = 0.05, chosen before outcomes are inspected.
- n is the number of usable student pairs, not the number of daily records.

Compute t = mean(d) / (sample_SD(d) / sqrt(n)); degrees of freedom = n − 1. Report mean difference, 95% t confidence interval, t, df, p and n. Use sample SD with denominator n−1. Optionally report paired standardized effect d_z = mean(d)/sample_SD(d), clearly labeled as an extension.

In Python, `scipy.stats.ttest_rel(recorded, estimated, alternative="two-sided", nan_policy="raise")` implements the test after alignment and validation. Check its result against the hand formula. The sign follows recorded minus estimated. See [SciPy documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html).

## Primary inclusion rules

Include non-pilot, consenting, currently enrolled B.Tech participants who have not already participated, submitted a valid estimate before the recorded report, answered No to checking the relevant report earlier that day, and provided seven valid daily totals for the correct window on their personally used unshared primary phone. They must confirm single-phone scope and transcription from the report. Review other reporting tools for comparability before inclusion; do not silently combine incomparable measures.

Match by participant ID, not row order. Parse timestamps with known timezone; check Part B follows Part A. Flag conflicting duplicate IDs, invalid dates and mismatches for resolution. Never automatically retain whichever duplicate gives the desired result. Preserve original submissions and document any verified transcription correction. Identical numerical usage values alone are not proof of duplicate people.

Do not impute missing estimates or daily usage outcomes for the primary test. Missing context such as college code does not invalidate otherwise complete pairs. Pre-exposed respondents are excluded from primary inference and counted separately; an explicitly labeled sensitivity summary may describe them without replacing the main result.

## Validation and preprocessing

1. Preserve raw exports and record checksum, questionnaire version and collection window.
2. Standardize field names, codes and categorical labels. Verify one-to-one pairing.
3. Convert every HH:MM value to integer minutes; validate 0–1,440 and dates.
4. Check completeness, device scope, eligibility and estimate ordering; retain an audit of every exclusion reason.
5. Calculate seven-day average, signed and absolute errors without rounding intermediate values.
6. Inspect unusual observations for entry errors; keep genuine extreme values. Do not remove them just because they affect significance.
7. Produce a participant flow table: received A, received B, matched pairs, exclusions by reason and final n (exclusion reasons can overlap; report totals without double-counting people).

## EDA outputs

- Sample profile: study years, reporting platforms and college-code coverage; undisclosed values remain explicit.
- Summary table for E, R, d and abs(d): n, mean, median, sample SD, quartiles and range.
- Histogram of signed errors with a zero line; inspect tails and asymmetry.
- Paired estimated/recorded plot or side-by-side boxplots, plus a scatterplot with the equality line R=E.
- Percentage underestimating by more than 30 minutes, within ±30 minutes, and overestimating by more than 30 minutes. This tolerance is chosen for descriptive convenience, not clinical relevance.
- Mean/median absolute error, because zero average bias can conceal large individual errors.

A high correlation can coexist with systematic underestimation; it is not proof of accuracy. Avoid presenting correlation between R and R−E as an independent discovery: those quantities share R algebraically. Optional checking-frequency or platform comparisons are exploratory and may have small or confounded groups.

## Assumptions and interpretation

The paired t-test treats different students' differences as appropriately independent and relies on approximate normality of the mean difference. Inspect the distribution of d, a Q–Q plot and influential values; the two original distributions need not separately be normal for the paired-difference argument. A Shapiro test alone does not select the analysis automatically. Shared colleges/friend groups and nonrandom recruitment limit inference, and adding colleges does not make the sample random.

If the differences are severely skewed or influential, report the limitation. A participant-level paired bootstrap confidence interval for the mean difference may be added as a predeclared sensitivity analysis, resampling complete student pairs. It does not repair nonrandom sampling or clustering. Do not swap to Wilcoxon and claim it tests the same population mean. If n is inadequate or SD(d)=0, do not report a misleading ordinary t-test; explain what the data support.

Reject H0 when the full two-sided p-value is below .05. Otherwise fail to reject: this does not prove estimates are accurate. Report confidence intervals and magnitude in minutes/day, including when the result is not statistically significant. Self-transcribed OS reports are a reference measure, not error-free ground truth. Differences across Android/iOS definitions, prior habitual checking and inconsistent transcription remain limitations.

## Planned implementation and delivery

Use a Jupyter notebook with pandas for import/join/validation; NumPy for transformations; Matplotlib/Seaborn for plots; SciPy for the paired test and interval. Explain the meaning of each operation alongside the relevant course concept. No implementation or dependency installation is claimed yet.

Final deliverables: reproducible notebook, source/cleaning documentation, selected figures/tables, and one 4–5 page team report. Suggested layout: (1) title/team/question/data; (2) methods and preprocessing; (3) EDA; (4) CDA and assumptions; (5) conclusions, limitations and references. Cite the team survey as the dataset source and the device documentation for measurement methods. The original IA3 brief has no requirement for an external dataset or ML model; primary data are not explicitly ruled out by the supplied screenshot.

Team number and members' names/registration numbers remain required for the final report. Statistical results and conclusions remain pending actual participant responses.
