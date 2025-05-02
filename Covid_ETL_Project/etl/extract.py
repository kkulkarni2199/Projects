import requests
import pandas as pd
from datetime import datetime

def fetch_covid_data(url: str) -> pd.DataFrame:
    """
    Fetch COVID-19 data from the given URL and return it as a DataFrame.
    
    Args:
        url (str): The URL to fetch the data from.
    
    Returns:
        pd.DataFrame: The COVID-19 data as a DataFrame.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data_json = response.json()
        records = []
        for country_code, country_data in data_json.items():
            if isinstance(country_data, dict) and 'data' in country_data:
                for entry in country_data['data']:
                    entry['iso_code'] = country_code
                    entry['location'] = country_data.get('location', '')
                    records.append(entry)
        df = pd.DataFrame(records)
        return df
    else:
        raise Exception(f"Failed to fetch data. Status Code: {response.status_code}")
    
def save_data(df: pd.DataFrame, filename: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/{filename}_{timestamp}.csv"
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    URL = "https://covid.ourworldindata.org/data/owid-covid-data.json"
    data_df = fetch_covid_data(URL)
    save_data(data_df, "covid_vaccination_raw")
