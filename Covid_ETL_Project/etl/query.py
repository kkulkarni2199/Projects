import sqlite3
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DB_FILE = os.path.join(DATA_DIR, 'covid_vaccination.db')

def run_query(query, params = None):
    conn = sqlite3.connect(DB_FILE)
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():

    while(True):

        print("\n[INFO] Connected to SQLite DB.")
        print("Choose an option:\n")
        print("1. Top 10 countries by people vaccinated")
        print("2. Total deaths by country (Top 10)")
        print("3. Average new cases per country")
        print("4. Run custom SQL query")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            query = """
                SELECT location, MAX(people_vaccinated) AS max_vaccinated
                FROM covid_vaccination
                GROUP BY location
                ORDER BY max_vaccinated DESC
                LIMIT 10
            """
            df = run_query(query)
            print(df)

        elif choice == '2':
            query = """
                SELECT location, MAX(total_deaths) AS deaths
                FROM covid_vaccination
                GROUP BY location
                ORDER BY deaths DESC
                LIMIT 10
            """
            df = run_query(query)
            print(df)

        elif choice == '3':
            query = """
                SELECT location, ROUND(AVG(new_cases)) as new_cases
                FROM covid_vaccination
                GROUP BY location
                ORDER BY new_cases DESC
                LIMIT 10
            """
            df = run_query(query)
            print(df)

        elif choice == '4':
            user_query = input("Enter your custom SQL query:\n")
            try:
                df = run_query(user_query)
                print(df)
            except Exception as e:
                print(f"[ERROR] Invalid query. Details: {e}")

        elif choice == '5':
            print("Exiting...")
            break

        else:
            print("[ERROR] Invalid choice. Try again.")

if __name__ == "__main__":
    main()