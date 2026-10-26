# The Screen-Time Blind Spot
**Estimated versus phone-recorded screen time among B.Tech students**

CES 2103 — IA3 Data Analytics. Python implementation and a seven-page simulated-data report are complete; genuine survey collection remains pending. Team 3 reports: [PDF](report/Team_03.pdf) and [Word](report/Team_03.docx).

**The included dataset is SIMULATED: 120 fictional responses, 112 usable pairs and 8 deliberate validation cases. No students were surveyed to produce it.** Generated rows must not be submitted as collected student evidence.

## Start here
- [Explained, executed notebook](notebooks/01_screen_time_analysis.ipynb)
- [Single-form questions](docs/SURVEY_SCRIPT.md)
- [Study design and variables](docs/STUDY_PROTOCOL.md)
- [Curriculum and Python syntax map](docs/CURRICULUM_MAP.md)
- [Replace the CSV with real responses](docs/REAL_DATA_GUIDE.md)
- [Demonstration outputs](outputs/simulated/RUN_SUMMARY.md)
- [Assignment requirements](docs/PROJECT_PLAN.md)

## Run the project
Tested with Python 3.12. Create a local environment:
```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py --config config/simulated.json
python -m pytest
```
The simulated CSV is already included. To regenerate the same seeded dataset:
```sh
python run.py --generate-simulated
```
For a notebook kernel:
```sh
python -m ipykernel install --prefix .venv --name screentime --display-name "Python (screen-time project)"
JUPYTER_PATH="$PWD/.venv/share/jupyter" python scripts/execute_notebook.py
```
Open the notebook in an editor with Jupyter support and select this environment to explore interactively. The execution script runs and saves all cells without needing a notebook server.

Once real responses exist:
```sh
python run.py --config config/real.json
```
Change the notebook's separate `CONFIG_PATH` to `config/real.json` when using it with real responses. Missing real input fails clearly; there is no automatic fallback to simulation.

## What the project asks
How closely do B.Tech students estimate their own average daily smartphone use? One student estimates first, then enters seven completed daily totals for the same primary phone. Both measurements belong to the same person and date window.

The primary analysis is a two-sided paired t-test of mean recorded-minus-estimated minutes/day = 0, with alpha 0.05. EDA examines agreement, error distribution and absolute error. A convenience sample cannot establish what all B.Tech students do.

A single form collects no name, participant ID, college, OS, study year or app list. The pipeline assigns IDs by source-row order after export. IDs are stable within a frozen source file, not across re-ordered exports. Keep the source export and its checksum.

## Structure
```text
config/             source path, provenance, column mapping, alpha
data/simulated/     fictional CSV and generation assumptions
data/templates/     empty canonical survey CSV
data/raw/           local real responses (ignored by Git)
src/screentime/     simulation, validation, EDA and paired inference
notebooks/          explained, executed analysis
scripts/            notebook creation and fresh-kernel execution
outputs/simulated/ labelled demonstration tables, figures and audit
outputs/real/      local real-data results (ignored by Git)
tests/              statistical and data-validation checks
docs/               protocol, form, curriculum and report handoff
report/             current Team 3 Word and PDF reports
```

Every run preserves source data and exports a row audit, cleaned table, descriptive statistics, exclusion counts, statistics JSON, figures, summary and provenance manifest. Missing daily totals are not replaced with invented values. Identical patterns are flagged for review, not automatically deleted.

Keep real participant records local. **A tracked notebook can contain real rows and plots after execution; clear its outputs before committing any real-data run.** The parent study folder is reference material and is not changed or uploaded.

Target 100 valid responses, with 60 as a practical project target minimum, not a power calculation or a requirement in the screenshot. Never top up real responses with generated rows. The current report explicitly uses simulation. Acceptance of a simulation-only dataset needs instructor confirmation; submission is due **26 October 2026** according to the supplied screenshot.

## Report edition and source files

The expanded report includes simple statistical interpretations, three figures, code excerpts and the repository link. Its seven pages were requested for readability; the assignment brief itself specifies 4–5 pages. See [report build instructions](report/README.md) for the tracked document and figure scripts. The analysis code, notebook, configurations and tests are included in this repository.
