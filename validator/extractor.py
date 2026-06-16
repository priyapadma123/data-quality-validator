# validator/extractor.py

import pandas as pd
import os

def extract(filepath: str) -> pd.DataFrame:
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(filepath, dtype=str)
    elif ext == ".xlsx":
        df = pd.read_excel(filepath, dtype=str)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    df.columns = df.columns.str.strip()
    df = df.where(pd.notnull(df), None)

    return df