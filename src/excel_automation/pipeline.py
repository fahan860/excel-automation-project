import sys

import pandas as pd

from excel_automation.config import CLEAN_PATH, DATA_DIR, OUTPUT_DIR, REPORT_PATH
from excel_automation.data_processing.cleaning import clean_dataframe
from excel_automation.io.excel_io import find_excel_files, read_excel_file
from excel_automation.reporting.report_generator import generate_report
from excel_automation.utils.logger import log


def run_automation() -> None:
    log("Starting Excel sales automation...")
    if not DATA_DIR.is_dir():
        log(f"Data folder not found: {DATA_DIR}")
        sys.exit(1)

    files = find_excel_files(DATA_DIR)
    if not files:
        log("No Excel files found in data/. If needed, run: python src/generate_fake_data.py")
        sys.exit(1)

    log(f"Found {len(files)} file(s):")
    for file_path in files:
        log(f" - {file_path.name}")

    frames = []
    for file_path in files:
        try:
            log(f"Loading {file_path.name}...")
            frames.append(read_excel_file(file_path))
        except Exception as exc:
            log(f"Warning: failed to read {file_path}: {exc}")

    if not frames:
        log("No readable Excel files. Exiting.")
        sys.exit(1)

    merged = pd.concat(frames, ignore_index=True)
    log(f"Merged rows: {len(merged)}")

    log("Cleaning data (dates, products, missing values, duplicates)...")
    cleaned = clean_dataframe(merged)
    log(f"Cleaned rows: {len(cleaned)} (removed {len(merged) - len(cleaned)} problematic rows/dupes)")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    log(f"Saving cleaned dataset -> {CLEAN_PATH}")
    try:
        with pd.ExcelWriter(CLEAN_PATH, engine="openpyxl") as writer:
            cleaned.to_excel(writer, index=False, sheet_name="Clean Data")
    except PermissionError:
        log(f"ERROR: Cannot write to {CLEAN_PATH}")
        log("The file may be open in Excel or another program. Please close it and try again.")
        sys.exit(1)

    log(f"Generating business report -> {REPORT_PATH}")
    try:
        generate_report(cleaned, REPORT_PATH)
    except PermissionError:
        log(f"ERROR: Cannot write to {REPORT_PATH}")
        log("The file may be open in Excel or another program. Please close it and try again.")
        sys.exit(1)

    log("All done. Deliverables:")
    log(f" - Clean data: {CLEAN_PATH}")
    log(f" - Sales report: {REPORT_PATH}")
