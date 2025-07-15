import os
import pandas as pd
from sqlalchemy import create_engine

PROCESSED_DIR = "data/processed"
DB_PATH = "db/global_dev.db"

def clean_column_names(df):
    df.columns = [
        col.strip().replace(" ", "_").replace("-", "_").lower()
        for col in df.columns
    ]
    return df

def main():
    # Ensure DB directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Connect to SQLite
    engine = create_engine(f"sqlite:///{DB_PATH}")

    parquet_files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith(".parquet")]
    print(f"Found {len(parquet_files)} Parquet files to load into DB.")

    for fname in parquet_files:
        table_name = fname.replace(".parquet", "")
        path = os.path.join(PROCESSED_DIR, fname)
        print(f"Loading {fname} -> table `{table_name}`...")
        df = pd.read_parquet(path)
        df = clean_column_names(df)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        print(f"  -> Loaded {df.shape[0]} rows, {df.shape[1]} columns.")

    print("\nAll Parquet files loaded into", DB_PATH)

if __name__ == "__main__":
    main()
