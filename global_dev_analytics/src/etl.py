import os
import yaml
import requests
import zipfile
import io
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
CONFIG_PATH = "config/sources.yaml"

def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def load_config(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config["sources"]

def download_file(url, out_path):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download {url} ({response.status_code})")
    with open(out_path, "wb") as f:
        f.write(response.content)
    return out_path

def extract_main_csv_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_files = [name for name in zf.namelist()
                     if name.lower().endswith('.csv') and "metadata" not in name.lower()]
        if not csv_files:
            raise Exception("No data CSV (non-Metadata) found in ZIP!")
        # Use the first matching file
        main_csv = csv_files[0]
        print(f"Found data CSV: {main_csv}")
        with zf.open(main_csv) as f:
            df = pd.read_csv(f, skiprows=4)
        return df

def clean_df(df):
    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    df = df.dropna(axis=1, how="all")
    df = df.dropna(how="all")
    return df

def run_etl():
    ensure_dirs()
    sources = load_config(CONFIG_PATH)

    for src in sources:
        if not src.get("extract", True):
            print(f"[SKIP] {src['name']}")
            continue
        print(f"[INFO] Processing: {src['name']}")
        url = src["url"]
        is_zip = url.endswith('.zip') or 'downloadformat=csv' in url or 'zip' in url
        raw_path = os.path.join(RAW_DIR, f"{src['name']}.zip" if is_zip else f"{src['name']}.csv")
        try:
            print(f"[DOWNLOADING] {url}")
            download_file(url, raw_path)
        except Exception as e:
            print(f"[ERROR] Failed to download {src['name']}: {e}")
            continue

        try:
            if is_zip:
                # Extract main CSV from zip
                df = extract_main_csv_from_zip(raw_path)
            else:
                # For plain CSVs, try loading normally, with and without skiprows
                try:
                    df = pd.read_csv(raw_path, skiprows=4)
                except Exception:
                    df = pd.read_csv(raw_path)
            df = clean_df(df)
        except Exception as e:
            print(f"[ERROR] Failed to load/clean {src['name']}: {e}")
            continue

        out_parquet = os.path.join(PROCESSED_DIR, f"{src['name']}.parquet")
        try:
            df.to_parquet(out_parquet, index=False)
            print(f"[OK] Saved to {out_parquet} ({df.shape[0]} rows)")
        except Exception as e:
            print(f"[ERROR] Failed to save Parquet for {src['name']}: {e}")

if __name__ == "__main__":
    run_etl()
