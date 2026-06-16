# validator/null_checker.py

import pandas as pd
from config import VALIDATION_RULES

def check_nulls(df: pd.DataFrame) -> list:
    errors = []

    if not VALIDATION_RULES["null_check"]["enabled"]:
        return errors

    columns = VALIDATION_RULES["null_check"]["columns"]

    for col in columns:
        if col not in df.columns:
            continue
        null_rows = df[df[col].isnull() | (df[col].astype(str).str.strip() == "")]
        for idx, row in null_rows.iterrows():
            errors.append({
                "Row": idx + 2,
                "CustomerID": row.get("CustomerID", "N/A"),
                "Column": col,
                "Issue": "Null or empty value",
                "Value": None
            })

    return errors