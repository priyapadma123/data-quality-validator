# validator/duplicate_checker.py

import pandas as pd
from config import VALIDATION_RULES

def check_duplicates(df: pd.DataFrame) -> list:
    errors = []

    if not VALIDATION_RULES["duplicate_check"]["enabled"]:
        return errors

    columns = VALIDATION_RULES["duplicate_check"]["columns"]

    for col in columns:
        if col not in df.columns:
            continue

        duplicated_mask = df.duplicated(subset=[col], keep=False)
        duplicate_rows = df[duplicated_mask]

        for idx, row in duplicate_rows.iterrows():
            errors.append({
                "Row": idx + 2,
                "CustomerID": row.get("CustomerID", "N/A"),
                "Column": col,
                "Issue": "Duplicate value",
                "Value": row[col]
            })

    return errors