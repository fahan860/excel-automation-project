# 📊 Excel Sales Automation

**A Python ETL pipeline that merges monthly Excel sales files, cleans them with explicit business rules and generates a formatted multi-sheet executive report — in one command.**

[![Live demo](https://img.shields.io/badge/Live%20demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://fahan-excel.streamlit.app)
[![Portfolio](https://img.shields.io/badge/Portfolio-Fatima%20Zahrae%20Ahannuk-0ea5e9)](https://fatima-zahrae-ahannuk.vercel.app/projects/excel)

## Try it
👉 **https://fahan-excel.streamlit.app** — run the pipeline on the sample files (or upload your own), inspect every cleaning step and download the generated report.
On the sample data: **1,389 raw rows → 1,254 clean rows**, 10 products, 75 countries.

## Problem
Consolidating monthly sales spreadsheets by hand is slow and error-prone:
- dates stored as text, datetime **or Excel serial numbers** in the same column,
- inconsistent product and category names (`laptop`, ` Laptop `, `LAPTOP`),
- missing quantities / prices and duplicate rows,
- the same report rebuilt manually every month.

## Pipeline
```text
data/*.xlsx ──► discover & merge ──► clean ──► compute revenue ──► output/clean_data.xlsx
                                                               └─► output/sales_report.xlsx
```
**Cleaning rules**: unified date parsing (text / datetime / Excel serial) · trimmed + normalised product and category names · missing prices and quantities imputed with the **per-product median** · duplicates removed · `total_price = quantity × price`.

**Report** (`sales_report.xlsx`): *Overview* KPIs · *Top Products* · *Revenue by Country* · *Revenue by Category* · *Clean Data*.

## Tech stack
Python · pandas · NumPy · openpyxl · XlsxWriter · Faker (sample data) · Streamlit (demo)

## Project structure
```text
data/                         # monthly input files (sample: Jan, Feb, Mar)
src/excel_automation/
├── io/excel_io.py            # file discovery and loading
├── data_processing/cleaning.py
├── reporting/report_generator.py
├── data_generation/          # realistic messy sample data (Faker)
├── pipeline.py               # orchestration
└── config.py                 # paths and settings
main.py                       # entry point
```

## Run locally
```bash
pip install -r requirements.txt
python src/generate_fake_data.py   # optional: regenerate messy sample files in data/
python main.py                     # → output/clean_data.xlsx + output/sales_report.xlsx
```
Drop next month's file into `data/` and run `python main.py` again.

## Author
**Fatima Zahrae Ahannuk** — Big Data & AI engineering student · [Portfolio](https://fatima-zahrae-ahannuk.vercel.app) · [LinkedIn](https://www.linkedin.com/in/fatima-zahrae-ahannuk-b936b1351/) · [GitHub](https://github.com/fahan860)
