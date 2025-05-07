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

## Structure
- `etl/` contains ETL scripts
- `data/` stores raw CSV files
- `requirements.txt` lists Python dependencies

### Run Extract
python etl/extract.py
python etl/transform.py
python etl/load.py

## Author
Kaustubh Kulkarni
