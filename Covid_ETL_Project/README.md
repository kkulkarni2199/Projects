# COVID ETL Pipeline Project

This project demonstrates an end-to-end ETL (Extract, Transform, Load) data pipeline using Python and SQL on COVID-19 vaccination data.

## Steps Implemented
- Step 1: Data extraction using requests and pandas:
    - Fetches COVID-19 vaccination and case data from the OWID API.
    - Saves output as: `covid_vaccination_raw_{timestamp}.csv` in the `data/` folder.
- Step 2: Data transformation:
    - Automatically loads the latest raw CSV.
    - Filters for selected countries: *India, US, UK, Germany, Brazil*.
    - Drops irrelevant columns and fills missing values with zero.
    - Saves cleaned data to: `transformed_covid_data.csv`.
- Step 3: Load into SQLite/PostgreSQL:
    - Connects to (or creates) a SQLite database named `covid_vaccination.db` in the `data/` directory.
    - Drops the existing table (`covid_vaccination`) to avoid schema mismatch.
    - Creates a new table with the following explicit schema:

  ```sql
  CREATE TABLE covid_vaccination (
      iso_code TEXT,
      location TEXT,
      date TEXT,
      total_cases REAL,
      new_cases REAL,
      total_deaths REAL,
      new_deaths REAL,
      people_vaccinated REAL,
      people_fully_vaccinated REAL,
      total_tests REAL
  );
- Step 4: Automation:

The entire ETL pipeline is automated using a `run_etl.py` controller script and Windows Task Scheduler.

Automation Flow:
- `run_etl.py` sequentially runs: `extract.py` → `transform.py` → `load.py`
- A batch file (`run_etl.bat`) is created to execute the pipeline
- Windows Task Scheduler is used to run this batch file on a defined schedule (e.g., daily)

To run manually:
```bash
python run_etl.py
```

- Step 5 : Query & Explore

The `query.py` module allows for interactive querying of the SQLite database.

Features:
- Top 10 countries by people vaccinated
- Total deaths by country
- Average new COVID-19 cases
- Support for custom SQL queries

How to Run:
```bash
python etl/query.py
```

## Structure
- `etl/` contains ETL scripts
- `data/` stores raw CSV files
- `requirements.txt` lists Python dependencies

### Running ETL scripts
python etl/extract.py
python etl/transform.py
python etl/load.py

## Author
Kaustubh Kulkarni
