"""Rebuild the teaching notebook; execute separately to verify a fresh kernel."""
from pathlib import Path
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
md = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell
nb.cells = [
    md("""# The Screen-Time Blind Spot
## CES 2103: a complete, explained Python workflow

**Default source: SIMULATED DEVELOPMENT DATA. No students were surveyed for these demonstration rows.**

One B.Tech student is one observation. Each student estimates average daily usage, then transcribes seven daily totals for the same primary phone and dates. IDs are assigned by the pipeline after export. No name, college, OS, study year or app list is requested.

This notebook teaches the calculations and runs the same reusable pipeline as `run.py`. To use collected responses later, supply the agreed CSV and change `CONFIG_PATH` to `config/real.json`. Run all cells from a fresh kernel. Do not mix generated and collected rows. The draft survey is in `docs/SURVEY_SCRIPT.md`."""),
    md("""## 1. Imports and source selection
`import ... as ...` gives a library a short name: `pd` for pandas tables, `np` for NumPy numerical operations. SciPy supplies statistical distributions/tests. `Path` handles file paths. The `src` package holds reusable, documented analysis functions.

**Curriculum:** L1–L4 — define the source, observation and variables before calculations."""),
    code("""from pathlib import Path
import sys
import numpy as np
import pandas as pd
from scipy import stats
from IPython.display import display, Markdown, Image

ROOT = Path.cwd().resolve()
while not (ROOT / 'src' / 'screentime').exists():
    if ROOT == ROOT.parent:
        raise RuntimeError('Open this notebook within the project folder.')
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / 'src'))
from screentime.pipeline import run_pipeline, parse_time

CONFIG_PATH = ROOT / 'config/simulated.json'  # Later: config/real.json
result = run_pipeline(CONFIG_PATH)
kind = result['config']['data_kind']
display(Markdown(f'**Active source: {kind}**'))
if kind == 'SIMULATED':
    display(Markdown('**Demonstration only — the outputs are not findings about real students.**'))
result['manifest']"""),
    md("""## 2. Inspect the source and understand a DataFrame
A DataFrame is a table: rows represent students and columns represent variables. `head()` shows its first rows; `shape` gives `(row_count, column_count)`. `df['column']` selects one Series. An ID is a label, not a numerical variable to average.

`estimated_daily_time` and `day_1_time` … `day_7_time` start as strings such as `4:30`. Date is a date; consent/quality checks are categories. **Curriculum:** L4 observations and variable types."""),
    code("""raw = result['raw']
print('Rows and columns:', raw.shape)
display(raw.head())
display(raw.dtypes)"""),
    md("""## 3. Validation and cleaning
**Curriculum:** L11–L13 — missing values, consistency and record identity.

The original CSV is unchanged. We assign IDs (`SIM0001` or `ST0001`) by source-row order and save the file checksum. IDs stay stable for that frozen export; do not sort/rewrite the raw file and expect the same assignment.

Time conversion is `60 × hours + minutes`: `4:30` means 270 minutes, not 4.30 decimal hours. An invalid or absent value becomes missing (`NaN`), not zero. We require seven valid daily totals, eligibility and quality confirmations. Identical response patterns are flagged for review, not automatically removed.

In the supplied simulation, eight deliberate bad rows exercise validation. These problems were invented for software testing, not observed in students."""),
    code("""print('4:30 ->', parse_time('4:30'), 'minutes')
print('Invalid 24:15 ->', parse_time('24:15'))
audit = result['audited']
clean = result['clean']
display(audit[['participant_id', 'included', 'exclusion_reasons', 'possible_duplicate']].head(12))
print(f'Submitted={len(audit)}, included={len(clean)}, excluded={len(audit)-len(clean)}')
if clean.empty:
    raise RuntimeError('No usable pairs. Review audit.csv before any inferential analysis.')"""),
    md("""## 4. Transformation and feature construction
**Curriculum:** L17 — unit conversion, aggregation and constructing variables.

`axis=1` means calculate across columns within each student's row. `skipna=False` ensures six available days are not silently treated as a complete week. `.abs()` removes a sign.

Let $E_i$ be estimated daily minutes and $R_i$ the mean of seven recorded daily totals. Define $d_i=R_i-E_i$. Positive means underestimation; negative means overestimation. Absolute error $|d_i|$ measures size regardless of direction. Seven daily values from one student do not create seven independent participants."""),
    code("""day_columns = [f'day_{i}_minutes' for i in range(1, 8)]
recorded_check = clean[day_columns].mean(axis=1, skipna=False)
difference_check = recorded_check - clean['estimated_daily_minutes']
assert np.allclose(recorded_check, clean['recorded_daily_minutes'])
assert np.allclose(difference_check, clean['signed_error_minutes'])
display(clean[['participant_id', 'estimated_daily_minutes', 'recorded_daily_minutes',
               'signed_error_minutes', 'absolute_error_minutes']].head())"""),
    md("""## 5. Descriptive statistics
**Curriculum:** L5 — mean, median, sample standard deviation, quartiles and range.

`describe()` summarises numerical columns. Its `std` uses sample standard deviation (denominator $n-1$). Mean signed error measures net bias; mean absolute error measures individual inaccuracy. For illustrative errors −60 and +60, mean bias is zero but mean absolute error is 60 minutes."""),
    code("""display(result['descriptive'].round(2))
display(clean['perception_group'].value_counts().rename('students').to_frame())"""),
    md("""## 6. EDA: agreement, error distribution and descriptive groups
**Curriculum:** L7–L10 — visual relationships and interpretation.

Above the equality line means recorded use exceeded the estimate. A high correlation does not imply agreement: estimates could track people perfectly while being consistently low. The ±30-minute group is our descriptive convention, not a clinically validated threshold. Use the same convention for all sources."""),
    code("""for filename in ['01_estimated_vs_recorded.png', '02_signed_errors.png', '03_accuracy_groups.png']:
    display(Image(filename=str(result['output_dir'] / 'figures' / filename), width=700))"""),
    md("""## 7. Confirmatory question and assumptions
**Curriculum:** L21 — hypotheses, alpha and two-sided inference.

$H_0:\\mu_d=0$ versus $H_1:\\mu_d\\ne0$, with $\\alpha=0.05$ chosen before analysing the main survey. This tests an average discrepancy, not whether every student's estimate is accurate. Do not change the tail after seeing the sign.

Different students should provide appropriately independent differences. Inspect their distribution and influential values. Normality of the two original columns separately is not the relevant paired-test condition. Convenience sampling, friend groups and self-transcription limit inference; a Q–Q plot cannot establish representativeness."""),
    code("""qq = result['output_dir'] / 'figures' / '04_difference_qq.png'
if qq.exists():
    display(Image(filename=str(qq), width=650))
else:
    print('Q–Q plot unavailable for an insufficient or constant set of differences.')
result['statistics']['warnings']"""),
    md("""## 8. Paired t-test: classroom formula and Python
**Curriculum:** L22 / T6 — paired measurements; L6 — confidence intervals.

$$t=\\frac{\\bar d}{s_d/\\sqrt{n}},\\qquad df=n-1.$$

The standard error uses the sample SD of the **differences**, not a pooled SD of two independent groups. `ddof=1` gives the sample SD. `stats.t.sf()` is the upper-tail probability; doubling it after taking `abs(t)` gives the two-sided p-value. `stats.t.ppf()` finds a critical value.

`ttest_rel(a,b)` uses related observations and computes a minus b. We place recorded values first to preserve our sign convention."""),
    code("""d = clean['signed_error_minutes'].to_numpy()
n = len(d)
if n >= 2 and np.std(d, ddof=1) > 0:
    mean_d = np.mean(d)
    sd_d = np.std(d, ddof=1)
    se = sd_d / np.sqrt(n)
    t_manual = mean_d / se
    p_manual = 2 * stats.t.sf(abs(t_manual), df=n-1)
    alpha = result['config']['alpha']
    critical = stats.t.ppf(1-alpha/2, df=n-1)
    ci_manual = (mean_d-critical*se, mean_d+critical*se)
    test = stats.ttest_rel(clean['recorded_daily_minutes'], clean['estimated_daily_minutes'],
                           alternative='two-sided', nan_policy='raise')
    assert np.isclose(test.statistic, t_manual)
    assert np.isclose(test.pvalue, p_manual)
    display(pd.DataFrame({'quantity': ['n', 'mean difference', 'SD of differences', 'SE', 't', 'df', 'p', 'CI low', 'CI high'],
                          'value': [n, mean_d, sd_d, se, t_manual, n-1, p_manual, *ci_manual]}))
else:
    print('An ordinary paired t-test cannot be computed for this dataset.')"""),
    md("""## 9. Interpret the active source honestly
Small p-values concern incompatibility with zero mean difference under the assumptions; they are not the probability the null is true. Non-rejection does not prove accuracy. Report effect magnitude and uncertainty, not just significance.

**For simulated data**, a small p-value reflects our generation assumptions and random draw. It says nothing about actual B.Tech students. No final empirical report should be based on these fictional observations without explicitly changing the project to a disclosed simulation study."""),
    code("""display(Markdown((result['output_dir'] / 'RUN_SUMMARY.md').read_text()))"""),
    md("""## 10. Replace the source later
1. Build the single form using `docs/SURVEY_SCRIPT.md`. Respondents do not enter IDs, college or OS.
2. Keep the original export. Place a canonical copy at `data/raw/screen_time_real.csv`, or map your original question headings in `config/real.json`.
3. Change only `CONFIG_PATH` above to `ROOT / 'config/real.json'`, restart the kernel and run all cells.
4. Inspect the new audit, plots and assumptions. Outputs go to `outputs/real/`; simulation outputs remain separate.
5. Never combine simulated rows with real responses to increase sample size. Real files and outputs are Git-ignored by default.

The source fingerprint and dependency versions are in `manifest.json`. The report will be prepared later using the actual data source, the IA3 page limit and the saved bitcrusher formatting handoff."""),
]
nb.metadata = {"kernelspec": {"display_name": "Python (screen-time project)", "language": "python", "name": "screentime"},
               "language_info": {"name": "python", "version": "3.12"}}
path = ROOT / "notebooks/01_screen_time_analysis.ipynb"
path.parent.mkdir(exist_ok=True)
nbf.write(nb, path)
print(path)
