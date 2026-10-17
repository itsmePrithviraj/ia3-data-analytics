# Assignment requirements and project workflow

## Requirements from the supplied screenshot

Source: the local WhatsApp screenshot supplied by the student, read on 17 October 2026. These are assignment requirements, not authorization to submit anything automatically.

- CES 2103 Data Analytics IA3 mini project, teams of 3–5 students.
- One report per team, 4–5 pages.
- Include project title, team names and registration numbers, dataset source and explanation, preprocessing, EDA, CDA with a relevant statistical test, findings and conclusions.
- Name the report using the team number, for example `Team_01.pdf`.
- Upload the project and report to the LMS on or before 26 October 2026.
- Five marks: dataset, preprocessing, EDA, CDA and report format, one mark each.
- Further peer evaluation and submission instructions are to be shared separately.

The screenshot does not specify a minimum number of rows. More than 40–50 observations is the student's additional requirement; aim for more than 50 usable paired observations after justified preprocessing.

## Agreed sequence

1. Understand the brief and map relevant course concepts — planning review completed.
2. Discuss topics with real sources — completed; screen-time perception selected on 17 October 2026, with B.Tech students across colleges in scope.
3. Prepare and pilot a primary-data survey — draft protocol and exact questions prepared. After collecting responses, preserve the original exports and record collection dates, questionnaire version and file checksums. Inspect actual rows, units, missingness and usable participant counts together.
4. Specify the primary question, H0/H1, significance level and planned test before examining its p-value. Separate any later exploratory tests from this planned comparison.
5. Implement explained preprocessing and EDA in a notebook. Preserve raw data, document row changes and justify exclusions.
6. Perform CDA with assumptions, statistic, degrees of freedom, p-value, effect size and an appropriate confidence interval. Explain conclusions in context.
7. Export selected plots and tables, produce the 4–5 page report, rerun from a fresh kernel, and check all reported values against saved outputs.

Team number and member details are needed when preparing the report; they do not block preparing the survey.

Suggested three-person division: one member owns survey piloting, collection and source documentation; one owns validation and EDA; one owns the paired-test explanation, assumptions and report integration. Each should review the others' work and understand the full notebook. This is a proposed allocation, not a claim that those contributions have already happened.

Selected-study details are in `STUDY_PROTOCOL.md`, `SURVEY_SCRIPT.md` and `ANALYSIS_PLAN.md`. The older dataset shortlist is retained as planning history. As of 18 October, the single-form design and Python workflow are implemented with 120 explicitly simulated development rows (112 usable). No real participant dataset or final empirical report exists yet. See the executed notebook for demonstration outputs and `REAL_DATA_GUIDE.md` for replacement instructions.

## Scope and interpretation

EDA describes distributions and explores patterns. CDA tests a stated hypothesis using an appropriate statistical procedure. One well-justified primary test meets the stated test requirement; extra methods should answer useful questions.

Preprocessing includes validation, type correction and documented decisions even when a publisher reports no missing values. Do not manufacture missingness, remove all outliers, or delete identical feature rows without establishing that they represent duplicated observations. Do not reduce a useful dataset to 50 rows simply to match a minimum.

Unknown population variance does not become known when n exceeds 30. Check independence and the sampling design before choosing a test. An observational association does not establish a causal effect. A non-significant result is a valid result and does not prove the null hypothesis.

Machine learning, a dashboard, deployment and association mining are optional extensions, not requirements visible in the brief.

## Suggested five-page allocation

| Page | Content |
|---|---|
| 1 | Title and team details, question, dataset provenance and variables |
| 2 | Preprocessing and compact descriptive statistics |
| 3 | EDA with 2–3 purposeful plots and interpretations |
| 4 | Primary hypothesis, test choice, assumptions and results |
| 5 | Findings, practical meaning, limitations, conclusion and references |

This is a proposed layout, not an instructor-mandated page breakdown. Keep the title on page 1 rather than spending an entire page on a cover.
