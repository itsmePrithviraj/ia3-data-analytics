# Curriculum and Python learning map

Based on the parent folder's course map, official course-plan transcript, relevant topic notes, correction register and selected LMS transcripts. Original study files remain untouched. Official lecture numbering is used here; some lecturer filenames use shifted numbers.

| Project work | Course connection | Planned Python tools |
|---|---|---|
| Define observation, variable and measurement scale | L4 | DataFrame columns, `dtypes`, `head()` |
| Summarize center, spread and distributions | L5 | `describe()`, `mean()`, `median()`, sample `std()` |
| Explain uncertainty of an estimate | L6 / T2 | Confidence intervals; distinguish SD from SE |
| Plot relationships and group summaries | L7–L10 | Seaborn/Matplotlib, `groupby()`, `crosstab()`, correlation |
| Audit missingness, units, impossible values and duplicates | L11–L13 / T3 | `isna()`, `duplicated()`, type conversion and validation |
| Transform variables only when needed | L17–L20 / T5 | Derived columns, category labels, justified transformations |
| Define H0/H1, alpha and decision rule | L21 | Explicit notebook methods section before test results |
| Compare two independent means, if chosen | L22 / T6 | SciPy `ttest_ind(..., equal_var=False)` for Welch |
| Test categorical association, if chosen | L23 / T7; introduced in L13 | SciPy `chi2_contingency()` plus expected-count checks |

PCA (L14–L15), regression (L16), ANOVA (L23) and association mining are optional when the question actually needs them. We will not add techniques just to tick syllabus boxes.

## Local source locators

- Official lecture labels: `CES 2103_Data Analytics_Course Plan_2026.pdf`, physical page 6; existing transcript `study-guide/sources/extracted/CP.md`.
- Preprocessing: `LMS/L11-L13 - Copy.pdf`, pp. 2–18; nominal association and causation cautions, pp. 20–21.
- Hypothesis setup: `LMS/L21.pdf`, pp. 3–24.
- Mean comparisons: `LMS/L22 - Copy.pdf`, pp. 4–55; Welch material pp. 44, 49–54.
- Context and corrections: `study-guide/COURSE_MAP.md`, `study-guide/sources/CORRECTIONS.md`, and topic notes `01_PREPROCESSING_CLEANING.md`, `07_Z_T_TESTS.md`, `08_CHI_SQUARE_ANOVA.md`.

These paths are relative to the parent Data Analytics study folder, which is not part of the GitHub repository.

## How the implementation will be taught

For each step: explain the question and relevant course concept; introduce the library and syntax; run a small block; interpret the output; connect it to the report.

For example, we will explain that `df` names a table, `df["column"]` selects a column, a method such as `.mean()` computes a summary, and arguments specify choices. For a test, connect the software result to the classroom statistic and work through a small part manually.

Library roles: pandas for tables; NumPy for numerical operations; Matplotlib/Seaborn for plots; SciPy for statistical procedures; Jupyter for code, explanations and outputs together. Effect sizes and assumption diagnostics will be labeled as practical extensions where they go beyond the supplied teaching material.

Current learning status: project planning introduced; no claim of independent mastery or completed analysis.
