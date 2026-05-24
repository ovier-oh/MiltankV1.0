# MiltankV1.0

Miltank is an interactive CLI tool for statistical and reliability analysis (2-parameter Weibull) using CSV data.

## Features

- Load CSV files and normalize column names by trimming spaces.
- Select a numeric column for exploratory analysis.
- Compute descriptive statistics.
- Run a Shapiro-Wilk normality test.
- Display a histogram and a normal Q-Q plot.
- Run Weibull analysis on uncensored data with bootstrap-based B-life confidence intervals.
- Run Weibull analysis on right-censored data (`event = 1` for failure, `event = 0` for censored).
- Accept time/event columns for censored analysis by either column name or column index.

## Project Structure

```text
.
├── main.py
├── requirements.txt
└── src/
    └── miltank/
        ├── __init__.py
        ├── cli.py
        ├── models.py
        ├── io/
        │   ├── __init__.py
        │   └── csv_loader.py
        ├── plots/
        │   ├── __init__.py
        │   ├── histogram.py
        │   └── qqplot.py
        ├── reliability/
        │   ├── __init__.py
        │   ├── data_prep.py
        │   └── weibull.py
        └── stats/
            ├── __init__.py
            └── descriptive.py
```

## Requirements

- Python 3.11+ recommended
- Dependencies listed in `requirements.txt`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The CLI will ask for:

1. CSV file path.
2. Numeric column index for descriptive analysis.
3. Whether to use right-censored analysis.
4. Confidence level (for example `0.60` or `0.90`; comma values like `0,90` are accepted in the uncensored branch).
5. If censored mode is selected, time and event columns (name or index).

## Right-Censored Data Format

For censored Weibull analysis, your CSV should include:

- A time column (operating time, cycles, etc.).
- An event column where:
  - `1` means failure.
  - `0` means right-censored/suspended.

## Local Validation

Minimal syntax check:

```bash
python -m py_compile main.py src/miltank/cli.py src/miltank/models.py src/miltank/io/csv_loader.py src/miltank/stats/descriptive.py src/miltank/reliability/data_prep.py src/miltank/reliability/weibull.py src/miltank/plots/histogram.py src/miltank/plots/qqplot.py
```

## Contribution Guide

To keep the codebase organized:

- Keep clear separation of responsibilities (`cli`, `io`, `stats`, `reliability`, `plots`).
- Avoid putting business logic in `main.py` or directly inside input/output blocks.
- Use type hints and clear naming.
- Add comments only for non-obvious logic.

Recommended workflow:

1. Create a branch from `main`.
2. Make focused, small changes.
3. Run local validation.
4. Open a PR with a clear problem/solution description.

Where to add new functions:

- Reliability data preparation -> `src/miltank/reliability/data_prep.py`
- File loading/parsing -> `src/miltank/io/`
- Generic statistical calculations -> `src/miltank/stats/`
- User interaction (`print`/`input`) -> `src/miltank/cli.py`

## Improvement Ideas

- Add automated tests with `pytest`.
- Export analysis outputs to CSV/JSON.
- Add non-interactive mode with CLI arguments.
- Improve input validation and exception handling.

## License

To be defined.
