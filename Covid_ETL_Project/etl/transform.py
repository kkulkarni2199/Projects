import pandas as pd
import os
from glob import glob

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
TRANSFORMED_DATA_PATH = os.path.join('data', 'transformed_covid_data.csv')

def get_latest_raw_file() -> str:
    pattern = os.path.join(DATA_DIR, "covid_vaccination_raw_*.csv")
    csv_files = glob(pattern)
    if not csv_files:
        raise FileNotFoundError("No raw COVID data files found in 'data/' folder.")
    latest_file = max(csv_files, key=os.path.getctime)  # get the most recent
    return latest_file


# Countries to focus on
COUNTRIES = ['India', 'United States', 'United Kingdom', 'Germany', 'Brazil', 'China']

def load_raw_data(path: str)-> pd.DataFrame:
    return pd.read_csv(path)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Filter for selected countries
    df = df[df['location'].isin(COUNTRIES)]

    # Select columns of interest
    columns = [
        'iso_code', 'location', 'date', 'total_cases', 'new_cases',
        'total_deaths', 'new_deaths', 'people_vaccinated',
        'people_fully_vaccinated', 'total_tests'
    ]

    df = df[columns]

    # Handle missing values
    df.fillna(0, inplace=True)

    df['date'] = pd.to_datetime(df['date'])

    return df

def save_transformed_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False)
    print(f"Transformed data saved to {path}")

if __name__ == '__main__':
    latest_file = get_latest_raw_file()
    raw_df = load_raw_data(latest_file)
    cleaned_df = transform_data(raw_df)
    save_transformed_data(cleaned_df, TRANSFORMED_DATA_PATH)