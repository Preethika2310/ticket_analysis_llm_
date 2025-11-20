import pandas as pd
from typing import List, Dict

REQUIRED_COLUMNS = [
    "Assignment Group",
    "Service",
    "Service Offering",
    "Definition"
]

def load_catalog(excel_path: str) -> List[Dict]:
    df = pd.read_excel(excel_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Excel missing columns: {missing}. Found: {list(df.columns)}")

    # Normalize strings for robustness
    for col in REQUIRED_COLUMNS:
        df[col] = df[col].astype(str).fillna("").str.strip()

    # Convert to list of dicts
    records = df[REQUIRED_COLUMNS].to_dict(orient="records")
    return records
