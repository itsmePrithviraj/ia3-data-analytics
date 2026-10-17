# The Screen-Time Blind Spot

**Estimated versus phone-recorded screen time among B.Tech students**

CES 2103 — IA3 Data Analytics Project. Status: topic selected; collection protocol prepared for discussion and pilot. No participant data have been collected or analyzed in this repository.

Build a reproducible Python analysis using a real, attributable dataset with more than 50 observations, explaining the concepts and code alongside the CES 2103 curriculum.

## Planning documents

- [Study design, variables and sampling](docs/STUDY_PROTOCOL.md)
- [Exact survey questions and invitation](docs/SURVEY_SCRIPT.md)
- [Prespecified analysis and report plan](docs/ANALYSIS_PLAN.md)
- [Assignment requirements and workflow](docs/PROJECT_PLAN.md)
- [Earlier dataset shortlist (historical)](docs/TOPIC_SHORTLIST.md)
- [Curriculum and Python learning map](docs/CURRICULUM_MAP.md)

## Current decision

Selected on 17 October 2026: compare B.Tech students' estimates of their average daily primary-phone screen time with participant-transcribed device records for the same seven completed days. Recruitment can include friends at multiple colleges; this is not limited to MIT Manipal.

Proposed target: 100 valid participant pairs, with at least 60 usable pairs for the intended project scale. One student contributes one observation. Primary test: two-sided paired t-test of mean recorded-minus-estimated minutes/day = 0, at alpha 0.05. The sample is a convenience/referral sample; it is not representative of all B.Tech students.

Next: discuss the draft, pilot with five volunteers across Android/iPhone where possible, revise and freeze the questions, then collect genuine responses. No live form has been created, and no invitations have been sent. Numerical results and the final report require those responses.

## Planned tools

Python, Jupyter, pandas, NumPy, Matplotlib/Seaborn and SciPy. Add statsmodels only if the selected analysis needs it. Dependencies and exact versions will be recorded when implementation starts.

Planned directories: `data/` for source metadata and data; `notebooks/` for explained analysis; `src/` for reusable code if needed; `outputs/` for figures and tables; `report/` for the final report.

The parent study folder is reference material only. Lecture files and the personal assignment screenshot are not included in this repository. Participant-level data stay local by default; GitHub stores methods, code and appropriately aggregated outputs.

Planning date: 17 October 2026. Deadline stated in the supplied assignment screenshot: **26 October 2026**. Confirm any later instructor updates before submission.
