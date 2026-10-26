# Screen Time Analysis

A CES 2103 Data Analytics project comparing estimated daily smartphone use with the average of seven days of phone-recorded usage. It includes data cleaning, exploratory plots and a paired t-test to check the average difference.

The included dataset is simulated: 120 records, with 112 usable pairs after cleaning.

## Run

Use Python 3.12.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

On Windows, activate the environment with `.venv\Scripts\activate`.

Results and charts are saved in `outputs/simulated/`. For the calculations and explanations, open [the notebook](notebooks/01_screen_time_analysis.ipynb) in Jupyter or VS Code and select the project environment.

## Libraries

pandas and NumPy for data processing, Matplotlib and Seaborn for charts, and SciPy for the statistical test. Notebook support and pytest are also included in `requirements.txt`.

## Files

- `data/` — dataset and blank survey template
- `src/screentime/` — cleaning, analysis and data generation
- `config/` — input paths and analysis settings
- `tests/` — run with `python -m pytest`
- [Survey questions](docs/SURVEY_SCRIPT.md) and [real-data setup](docs/REAL_DATA_GUIDE.md)
- Report: [PDF](report/Team_03.pdf) | [Word](report/Team_03.docx)

Team 3: Prithviraj Gokule, Manish G S and Madhav Sunil.
