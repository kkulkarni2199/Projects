import sqlite3
import pandas as pd
import os

# Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
TRANSFORMED_FILE = os.path.join(DATA_DIR, 'transformed_covid_data.csv')
DB_FILE = os.path.join(DATA_DIR, 'covid_vaccination.db')

# Load DataFrame
df = pd.read_csv(TRANSFORMED_FILE)

# Connect to SQLite DB (creates if not exists)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Drop and recreate the table to avoid column mismatch
cursor.execute("DROP TABLE IF EXISTS covid_vaccination")

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS covid_vaccination (
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
    )
""")

# Clear existing data
cursor.execute("DELETE FROM covid_vaccination")

# Insert data
df.to_sql('covid_vaccination', conn, if_exists='append', index=False)

# Finalize
conn.commit()
conn.close()

print(f"[INFO] Loaded transformed data into database at: {DB_FILE}")

