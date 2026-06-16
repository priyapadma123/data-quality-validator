# config.py

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"
EXPORT_FOLDER = "exports"

ALLOWED_EXTENSIONS = {"csv", "xlsx"}

COLUMNS = [
    "CustomerID",
    "Name",
    "Email",
    "Phone",
    "DOB",
    "Gender",
    "City",
    "State",
    "Pincode",
    "RegistrationDate"
]

VALIDATION_RULES = {
    "null_check": {
        "enabled": True,
        "columns": COLUMNS
    },
    "duplicate_check": {
        "enabled": True,
        "columns": ["CustomerID"]
    },
    "email_format": {
        "enabled": True,
        "columns": ["Email"],
        "pattern": r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    },
    "phone_format": {
        "enabled": True,
        "columns": ["Phone"],
        "pattern": r"^[6-9]\d{9}$"
    },
    "date_format": {
        "enabled": True,
        "columns": ["DOB", "RegistrationDate"],
        "format": "%Y-%m-%d"
    },
    "age_validity": {
        "enabled": True,
        "column": "DOB",
        "min_age": 18,
        "max_age": 100
    },
    "gender_values": {
        "enabled": True,
        "column": "Gender",
        "allowed": ["Male", "Female", "Other"]
    },
    "pincode_format": {
        "enabled": True,
        "columns": ["Pincode"],
        "pattern": r"^\d{6}$"
    },
    "future_date_check": {
        "enabled": True,
        "columns": ["RegistrationDate"]
    },
    "name_check": {
        "enabled": True,
        "columns": ["Name"],
        "pattern": r"^[A-Za-z\s]+$"
    }
}