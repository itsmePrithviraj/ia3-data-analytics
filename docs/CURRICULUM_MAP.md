# Curriculum and Python learning map
The parent Data Analytics folder is reference material only. This map uses its course plan, topic notes and corrections; no original study material was modified.

| Project step | Course connection | Python used and meaning |
|---|---|---|
| One person, two matched measurements | L4: observations, variables and scales | `df.head()`, `df.shape`, `df.dtypes`; IDs are labels |
| Validate dates, units, missingness and repeats | L11–L13 / T3: preprocessing | `pd.to_datetime()`, `isna()`, `duplicated()`; explicit row reasons |
| Average seven daily entries | L17: aggregation / attribute construction | `.mean(axis=1, skipna=False)`; across columns, require complete days |
| Signed and absolute error | L17: transformation | column subtraction, `.abs()` |
| Center and spread | L5: descriptive statistics | `.describe()`, `.mean()`, `.median()`, `.std(ddof=1)` |
| Agreement and error distribution | L7–L10: visual relationships | Seaborn scatterplot/histogram; Matplotlib equality line |
| Specify H0/H1, alpha and two-sided decision | L21: testing | prespecified config alpha; comparisons and conditional statements |
| Test the mean within-person difference | L22 / T6: paired samples | `stats.ttest_rel(recorded, estimated)` |
| Quantify uncertainty | L6 and L22: confidence intervals | `stats.t.interval()`; distinguish SD from SE |
| Diagnose assumptions | Practical extension to testing | `stats.probplot()`, Tukey flags; flags do not force exclusions |
| Reproducibility | Project practice | seed, config, source checksum, versions, reusable functions |

A paired design does not require a before/after intervention: estimate and recorded use refer to the same person and period. One form keeps the pair in a single row, so no cross-form join is needed.

## Library roles and syntax
- **pandas** handles tables: `df["column"]` selects a Series; `df[["a", "b"]]` selects two columns; a method such as `.mean()` calculates a result.
- **NumPy** supplies arrays and numerical operations, including seeded simulation and square roots. `np.random.default_rng(seed)` makes a reproducible random stream.
- **Matplotlib** controls figure axes, labels and exports. **Seaborn** makes statistical plots from table columns.
- **SciPy** supplies the t distribution and paired test. Arguments inside parentheses specify the choice: `alternative="two-sided"`.
- **Jupyter** places explanations, executable cells and outputs together.
- **pytest** checks validation and numerical behavior; it is a software tool, not a statistical test of the research hypothesis.

`axis=1` means across columns within a row. `ddof=1` uses n−1 for sample variance. `NaN` is missing, not zero. `Path` makes file paths portable. A function packages reusable logic; the notebook walks through the same formulas separately and checks agreement with the pipeline.

For example, 4:30 converts to 4×60+30 = 270 minutes. The difference uses recorded minus estimated; switching argument order flips t and the CI direction, though a two-sided p-value stays the same.

## Exact local source locators
Paths below are relative to the parent Data Analytics folder, outside this repository.
- `CES 2103_Data Analytics_Course Plan_2026.pdf`, physical p. 6; transcript `study-guide/sources/extracted/CP.md`.
- `LMS/L11-L13 - Copy.pdf`, pp. 2–18 for preprocessing; pp. 20–21 for association/causation cautions.
- `LMS/L21.pdf`, pp. 3–24 for hypothesis setup.
- **`LMS/L22 - Copy.pdf`, pp. 27–34 for paired differences.**
- `study-guide/notes/07_Z_T_TESTS.md`, section 8.
- `study-guide/COURSE_MAP.md` and `study-guide/sources/CORRECTIONS.md`.

Official lecture numbering is used; some lecturer filenames use shifted labels. Effect size, Q–Q diagnostics and provenance controls are useful extensions, not claims that every detail is explicitly required in the syllabus.

PCA, ANOVA, regression and Apriori are not needed to answer this question. More methods do not automatically improve a mini project. The notebook explains a compact, defensible analysis; it does not imply that the learner has already mastered it.
