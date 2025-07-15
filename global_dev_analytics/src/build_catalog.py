import os
import pandas as pd
import yaml
from datetime import datetime

PROCESSED_DIR = "data/processed"
CONFIG_PATH = "config/sources.yaml"
CATALOG_PATH = "data_catalog/catalog.yaml"

def get_config_dict():
    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)
    # Make a dict: name -> (url, desc)
    return {s['name']: {'source': s['url'], 'description': s['description']} for s in cfg['sources']}

def main():
    config_dict = get_config_dict()
    catalog = {"datasets": {}}
    for fname in os.listdir(PROCESSED_DIR):
        if not fname.endswith(".parquet"):
            continue
        ds_name = fname.replace(".parquet", "")
        path = os.path.join(PROCESSED_DIR, fname)
        df = pd.read_parquet(path)
        fields = []
        for col in df.columns:
            fields.append({
                "name": col,
                "dtype": str(df[col].dtype)
            })
        dataset_entry = {
            "source": config_dict.get(ds_name, {}).get("source", ""),
            "description": config_dict.get(ds_name, {}).get("description", ""),
            "fields": fields,
            "rows": int(df.shape[0]),
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        catalog["datasets"][ds_name] = dataset_entry

    # Save as YAML
    os.makedirs(os.path.dirname(CATALOG_PATH), exist_ok=True)
    with open(CATALOG_PATH, "w") as f:
        yaml.dump(catalog, f, sort_keys=False, allow_unicode=True)

    print(f"Catalog written to {CATALOG_PATH}")

if __name__ == "__main__":
    main()
