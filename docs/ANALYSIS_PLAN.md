# Prespecified analysis plan
Status: implemented and tested on disclosed simulation. Main survey data have not been collected. Freeze this plan before examining main-survey results.

## Primary question
Is mean phone-recorded daily use different from the mean self-estimated daily use for the same participants and seven completed dates?

Define d = recorded − estimated, in minutes/day.
- H0: population mean d = 0.
- H1: population mean d ≠ 0.
- Two-sided paired t-test; alpha = 0.05.
- Primary estimate: mean d and its 95% t confidence interval.
- One participant is the sampling unit. Do not treat the seven days as independent students.

## Import and validation
Read strings to preserve duration entries; map original survey headings to the 14 canonical fields. Ignore unexpected fields rather than propagating them into analysis. Keep the raw export local and unchanged. Save its SHA-256 fingerprint, configuration and software versions.

Require all five consent/eligibility/quality responses to be Yes; validate the date and all eight duration inputs. Convert H:MM to minutes. Assign IDs after import, before exclusions, to retain traceability. Retain the raw source row number.

The collector checks reference dates against the actual submission date; the software validates calendar syntax, not the truth of the reported period. It cannot verify unique people or correct transcription. Flag identical patterns for review without automatic deletion.

No mean imputation, silent unit guesses, arbitrary outlier deletion or synthetic supplementation. Document all exclusions. The simulation's eight deliberate bad cases exist to test these paths.

## EDA
1. Count submitted, included and excluded observations and reasons. Reason counts may overlap if one row fails multiple checks.
2. Describe estimate, recorded daily average, signed error and absolute error: n, mean, sample SD, quartiles and range.
3. Plot estimated versus recorded use with the equality line. Correlation is not agreement.
4. Plot signed errors and their zero reference.
5. Plot descriptive ±30-minute accuracy groups; the cutoff is our convention.
6. Inspect a Q–Q plot and extreme differences before interpreting a paired test.

## CDA calculation
For n usable pairs:
```text
d_bar = mean(d)
s_d = sample standard deviation of d (ddof=1)
SE = s_d / sqrt(n)
t = d_bar / SE
df = n - 1
p = 2 * upper_tail_t_probability(abs(t), df)
CI = d_bar ± t_critical(1-alpha/2, df) * SE
```
The notebook independently computes the formula and checks it against `scipy.stats.ttest_rel(recorded, estimated)`. The pipeline also reports d_z = d_bar / s_d as an effect-size extension; minutes/day are easier to interpret.

Independence between people and a sufficiently well-behaved distribution of differences matter. Check influential differences; normality of each original measurement separately is not the paired-test requirement. Friend-group sampling can violate independence and does not support population-wide claims.

The software computes a test with at least two pairs and nonzero difference SD, but that is a mathematical condition, not a recommendation for a two-person study. Below 60 it prints a project-scale warning, not a power verdict. Empty, one-pair and zero-variance cases produce an explicit status without a bogus finite p-value.

Do not silently swap tests after seeing results. If differences make the t procedure inappropriate, document the problem and agree a justified alternative with the course instructor. No bootstrap or alternative test is implemented or claimed here.

## Interpretation and report
Report n, mean difference, SD of differences, t, df, p, CI and practical magnitude; review assumptions before treating the automatic decision as a conclusion. Non-rejection does not prove estimates accurate. Large positive and negative individual errors can cancel; discuss mean absolute error.

All simulated exports carry a provenance label. Simulated significance reflects generation assumptions and random sampling, not evidence about students. The final report comes after source confirmation and assumption review.

References: [SciPy paired t-test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html), [NIST comparison of means](https://www.itl.nist.gov/div898/handbook/eda/section3/eda353.htm).
