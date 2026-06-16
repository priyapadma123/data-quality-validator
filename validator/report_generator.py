# validator/report_generator.py

import pandas as pd
import os
from datetime import datetime
from config import EXPORT_FOLDER, REPORT_FOLDER

def generate_report(df: pd.DataFrame, all_errors: list, filename: str) -> dict:
    os.makedirs(REPORT_FOLDER, exist_ok=True)
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    total_rows = len(df)
    error_rows = list({e["Row"] for e in all_errors})
    total_errors = len(all_errors)
    clean_rows = total_rows - len(error_rows)
    pass_rate = round((clean_rows / total_rows) * 100, 2) if total_rows > 0 else 0

    # Group errors by validation type
    error_summary = {}
    for e in all_errors:
        issue = e["Issue"]
        error_summary[issue] = error_summary.get(issue, 0) + 1

    # Export error records to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_filename = f"error_records_{timestamp}.xlsx"
    export_path = os.path.join(EXPORT_FOLDER, export_filename)

    if all_errors:
        error_df = pd.DataFrame(all_errors)
        error_df.to_excel(export_path, index=False)
    else:
        export_path = None

    # Build HTML report
    report_filename = f"validation_report_{timestamp}.html"
    report_path = os.path.join(REPORT_FOLDER, report_filename)

    error_rows_html = ""
    for e in all_errors:
        error_rows_html += f"""
        <tr>
            <td>{e['Row']}</td>
            <td>{e['CustomerID']}</td>
            <td>{e['Column']}</td>
            <td>{e['Issue']}</td>
            <td>{e['Value'] if e['Value'] is not None else '<span class="null-val">NULL</span>'}</td>
        </tr>"""

    summary_rows_html = ""
    for issue, count in error_summary.items():
        summary_rows_html += f"""
        <tr>
            <td>{issue}</td>
            <td>{count}</td>
        </tr>"""

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; color: #333; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; margin-top: 40px; }}
        .summary-cards {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
        .card {{ background: white; padding: 20px 30px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); min-width: 150px; }}
        .card h3 {{ margin: 0 0 8px 0; font-size: 14px; color: #888; }}
        .card p {{ margin: 0; font-size: 28px; font-weight: bold; }}
        .pass {{ color: #27ae60; }}
        .fail {{ color: #e74c3c; }}
        .warn {{ color: #f39c12; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
        th {{ background: #2c3e50; color: white; padding: 12px 15px; text-align: left; }}
        td {{ padding: 10px 15px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f9f9f9; }}
        .null-val {{ color: #e74c3c; font-style: italic; }}
        .footer {{ margin-top: 40px; font-size: 12px; color: #aaa; }}
    </style>
</head>
<body>
    <h1>Data Quality Validation Report</h1>
    <p>File: <strong>{filename}</strong> &nbsp;|&nbsp; Generated: <strong>{datetime.now().strftime("%d %b %Y, %I:%M %p")}</strong></p>

    <div class="summary-cards">
        <div class="card">
            <h3>Total Rows</h3>
            <p>{total_rows}</p>
        </div>
        <div class="card">
            <h3>Clean Rows</h3>
            <p class="pass">{clean_rows}</p>
        </div>
        <div class="card">
            <h3>Error Rows</h3>
            <p class="fail">{len(error_rows)}</p>
        </div>
        <div class="card">
            <h3>Total Errors</h3>
            <p class="warn">{total_errors}</p>
        </div>
        <div class="card">
            <h3>Pass Rate</h3>
            <p class="{'pass' if pass_rate >= 80 else 'fail'}">{pass_rate}%</p>
        </div>
    </div>

    <h2>Error Summary by Type</h2>
    <table>
        <thead>
            <tr><th>Issue Type</th><th>Count</th></tr>
        </thead>
        <tbody>
            {summary_rows_html}
        </tbody>
    </table>

    <h2>Error Details</h2>
    <table>
        <thead>
            <tr><th>Row</th><th>CustomerID</th><th>Column</th><th>Issue</th><th>Value</th></tr>
        </thead>
        <tbody>
            {error_rows_html}
        </tbody>
    </table>

    <div class="footer">
        <p>Data Quality Validation Engine &mdash; Generated automatically</p>
    </div>
</body>
</html>"""

    with open(report_path, "w") as f:
        f.write(html)

    return {
        "total_rows": total_rows,
        "clean_rows": clean_rows,
        "error_rows": len(error_rows),
        "total_errors": total_errors,
        "pass_rate": pass_rate,
        "report_path": report_path,
        "export_path": export_path,
        "report_filename": report_filename,
        "export_filename": export_filename if all_errors else None,
        "error_summary": error_summary,
        "errors": all_errors
    }