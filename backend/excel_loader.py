import pandas as pd
from typing import List, Dict

EXPECTED_HEADERS = {
    "assignment_group": "Assignment Group",
    "service": "Service",
    "service_offering": "Service Offering",
    "ticket_count": "Ticket Count",
    "ai_combination_definition": "Definition",
    "ai_routing_reason": "Routing Reason"
}

def load_catalog(excel_path: str) -> List[Dict]:
    df = pd.read_excel(excel_path)

    # Normalize column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Check required columns
    missing = [key for key in EXPECTED_HEADERS if key not in df.columns]
    if missing:
        raise ValueError(f"Excel missing required columns: {missing}")

    # Rename to standard keys
    df = df.rename(columns={k: EXPECTED_HEADERS[k] for k in EXPECTED_HEADERS})

    # Clean values
    for col in EXPECTED_HEADERS.values():
        df[col] = df[col].astype(str).fillna("").str.strip()

    return df[EXPECTED_HEADERS.values()].to_dict(orient="records")
