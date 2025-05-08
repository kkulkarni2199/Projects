import os
import subprocess

BASE_DIR = os.path.dirname(__file__)
etl_dir = os.path.join(BASE_DIR, 'etl')

def run_script(script_name):
    script_path = os.path.join(etl_dir, script_name)
    print(f"[INFO] Running {script_name}...")
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"[ERROR] {result.stderr}")

if __name__ == "__main__":
    run_script("extract.py")
    run_script("transform.py")
    run_script("load.py")
    print("[INFO] ETL process completed successfully.")