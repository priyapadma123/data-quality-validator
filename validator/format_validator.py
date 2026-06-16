# validator/format_validator.py

import re
import pandas as pd
from datetime import date
from config import VALIDATION_RULES

def check_formats(df: pd.DataFrame) -> list:
    errors = []

    # Email format
    if VALIDATION_RULES["email_format"]["enabled"]:
        pattern = VALIDATION_RULES["email_format"]["pattern"]
        col = "Email"
        if col in df.columns:
            for idx, row in df.iterrows():
                val = row[col]
                if val and not re.match(pattern, str(val).strip()):
                    errors.append({
                        "Row": idx + 2,
                        "CustomerID": row.get("CustomerID", "N/A"),
                        "Column": col,
                        "Issue": "Invalid email format",
                        "Value": val
                    })

    # Phone format
    if VALIDATION_RULES["phone_format"]["enabled"]:
        pattern = VALIDATION_RULES["phone_format"]["pattern"]
        col = "Phone"
        if col in df.columns:
            for idx, row in df.iterrows():
                val = row[col]
                if val and not re.match(pattern, str(val).strip()):
                    errors.append({
                        "Row": idx + 2,
                        "CustomerID": row.get("CustomerID", "N/A"),
                        "Column": col,
                        "Issue": "Invalid phone format",
                        "Value": val
                    })

    # Date format
    if VALIDATION_RULES["date_format"]["enabled"]:
        fmt = VALIDATION_RULES["date_format"]["format"]
        for col in VALIDATION_RULES["date_format"]["columns"]:
            if col not in df.columns:
                continue
            for idx, row in df.iterrows():
                val = row[col]
                if val:
                    try:
                        pd.to_datetime(str(val).strip(), format=fmt)
                    except ValueError:
                        errors.append({
                            "Row": idx + 2,
                            "CustomerID": row.get("CustomerID", "N/A"),
                            "Column": col,
                            "Issue": "Invalid date format (expected YYYY-MM-DD)",
                            "Value": val
                        })

    # Age validity
    if VALIDATION_RULES["age_validity"]["enabled"]:
        col = VALIDATION_RULES["age_validity"]["column"]
        min_age = VALIDATION_RULES["age_validity"]["min_age"]
        max_age = VALIDATION_RULES["age_validity"]["max_age"]
        if col in df.columns:
            for idx, row in df.iterrows():
                val = row[col]
                if val:
                    try:
                        dob = pd.to_datetime(str(val).strip(), format="%Y-%m-%d")
                        today = date.today()
                        age = today.year - dob.year - (
                            (today.month, today.day) < (dob.month, dob.day)
                        )
                        if age < min_age or age > max_age:
                            errors.append({
                                "Row": idx + 2,
                                "CustomerID": row.get("CustomerID", "N/A"),
                                "Column": col,
                                "Issue": f"Age out of range (must be {min_age}–{max_age})",
                                "Value": val
                            })
                    except ValueError:
                        pass  # already caught in date format check

    # Gender values
    if VALIDATION_RULES["gender_values"]["enabled"]:
        col = VALIDATION_RULES["gender_values"]["column"]
        allowed = VALIDATION_RULES["gender_values"]["allowed"]
        if col in df.columns:
            for idx, row in df.iterrows():
                val = row[col]
                if val and str(val).strip() not in allowed:
                    errors.append({
                        "Row": idx + 2,
                        "CustomerID": row.get("CustomerID", "N/A"),
                        "Column": col,
                        "Issue": f"Invalid gender value (allowed: {', '.join(allowed)})",
                        "Value": val
                    })

    # Pincode format
    if VALIDATION_RULES["pincode_format"]["enabled"]:
        pattern = VALIDATION_RULES["pincode_format"]["pattern"]
        for col in VALIDATION_RULES["pincode_format"]["columns"]:
            if col not in df.columns:
                continue
            for idx, row in df.iterrows():
                val = row[col]
                if val and not re.match(pattern, str(val).strip()):
                    errors.append({
                        "Row": idx + 2,
                        "CustomerID": row.get("CustomerID", "N/A"),
                        "Column": col,
                        "Issue": "Invalid pincode (must be 6 digits)",
                        "Value": val
                    })

    # Future date check
    if VALIDATION_RULES["future_date_check"]["enabled"]:
        for col in VALIDATION_RULES["future_date_check"]["columns"]:
            if col not in df.columns:
                continue
            for idx, row in df.iterrows():
                val = row[col]
                if val:
                    try:
                        parsed = pd.to_datetime(str(val).strip(), format="%Y-%m-%d")
                        if parsed.date() > date.today():
                            errors.append({
                                "Row": idx + 2,
                                "CustomerID": row.get("CustomerID", "N/A"),
                                "Column": col,
                                "Issue": "Future date not allowed",
                                "Value": val
                            })
                    except ValueError:
                        pass  # already caught in date format check

    # Name check
    if VALIDATION_RULES["name_check"]["enabled"]:
        pattern = VALIDATION_RULES["name_check"]["pattern"]
        for col in VALIDATION_RULES["name_check"]["columns"]:
            if col not in df.columns:
                continue
            for idx, row in df.iterrows():
                val = row[col]
                if val and not re.match(pattern, str(val).strip()):
                    errors.append({
                        "Row": idx + 2,
                        "CustomerID": row.get("CustomerID", "N/A"),
                        "Column": col,
                        "Issue": "Name contains numbers or special characters",
                        "Value": val
                    })

    return errors