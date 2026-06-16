# app.py

import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from validator.extractor import extract
from validator.null_checker import check_nulls
from validator.duplicate_checker import check_duplicates
from validator.format_validator import check_formats
from validator.report_generator import generate_report

app = Flask(__name__)
app.secret_key = "dqv_secret_key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected.")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type. Only CSV and Excel files are allowed.")
            return redirect(request.url)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Run pipeline
        df = extract(filepath)

        null_errors = check_nulls(df)
        duplicate_errors = check_duplicates(df)
        format_errors = check_formats(df)

        all_errors = null_errors + duplicate_errors + format_errors

        result = generate_report(df, all_errors, file.filename)
        result["filename"] = file.filename

        return render_template("report.html", result=result)

    return render_template("index.html")


@app.route("/download/report/<filename>")
def download_report(filename):
    path = os.path.join("reports", filename)
    return send_file(path, as_attachment=True)


@app.route("/download/export/<filename>")
def download_export(filename):
    path = os.path.join("exports", filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)