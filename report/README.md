# Team 3 report

The current report is [Team_03.pdf](Team_03.pdf), with an editable [Team_03.docx](Team_03.docx). The expanded edition contains seven pages with left-aligned section headings, three figures, descriptive and statistical tables, two short Python excerpts, and a clickable GitHub link.

Members: Prithviraj Gokule (251090052818), Manish G S (251090052782), Madhav Sunil (251090051962). `Screen_Time_IA3_Report.docx` is an identical compatibility copy. Use the Team_03 files as the current report.

The assignment brief states **4–5 pages**. This edition extends to **seven pages at the user's explicit request**; it does not meet the original page-count limit. All required content sections remain present. The report uses 120 simulated input rows and 112 complete pairs; genuine survey collection remains pending.

## Rebuild the Word document

From the repository root, with the project environment active:

```sh
python -m pip install -r requirements.txt -r requirements-report.txt
python run.py --config config/simulated.json
python scripts/create_report_figures.py
python scripts/build_report.py
```

The report builder reads the saved statistics and creates both Word paths. It is specifically written for the current simulation study; changing the source requires reviewing the narrative, counts and conclusions as well as rerunning the analysis. It does not automatically produce a PDF. Export the updated DOCX through Word or LibreOffice, then inspect all pages and the repository hyperlink before replacing Team_03.pdf.

The tracked analysis implementation is in `src/screentime/`; report and figure builders are in `scripts/`. Internal figures and QA renders are under `report/work/`, excluded from Git.

## Verification

On 26 October 2026, all 26 project tests passed, and the report's numerical results were independently recomputed from the source CSV and matched the saved outputs. Both document formats were checked for team details, headings, figures, page count and the clickable repository URL. Every page of the final PDF was visually reviewed. See [REPORT_REVIEW.md](../docs/REPORT_REVIEW.md) for the requirement check and project explanation.
