# Excel Sales Automation

Production-ready Python project for automating monthly Excel sales consolidation, data cleaning, and executive reporting.

## Problem
Manual processing of monthly sales spreadsheets is repetitive and error-prone:
- Mixed date formats (string, datetime, Excel serial)
- Inconsistent product naming
- Missing values and duplicate rows
- Time-consuming report preparation

## Solution
This project provides a deterministic, reusable pipeline that:
- Discovers Excel files in `data/`
- Merges and cleans records with standardized business rules
- Computes derived metrics (`total_price = quantity * price`)
- Produces clean data and a multi-sheet business report in `output/`

## Tech Stack
- Python 3.10+
- pandas, numpy
- openpyxl, xlsxwriter
- Faker (demo data generation)

## Architecture
```text
excel_automation_project/
├── data/                         # input monthly files
├── output/                       # generated artifacts
├── screenshots/                  # demo images for GitHub README
├── src/
│   ├── automate_excel.py         # backward-compatible wrapper
│   ├── generate_fake_data.py     # backward-compatible wrapper
│   ├── main.py                   # src-level entry point
│   └── excel_automation/
│       ├── config.py             # centralized settings and paths
│       ├── pipeline.py           # orchestration layer
│       ├── io/
│       │   └── excel_io.py       # file discovery and Excel loading
│       ├── data_processing/
│       │   └── cleaning.py       # cleaning and standardization logic
│       ├── reporting/
│       │   └── report_generator.py # report creation/formatting
│       ├── data_generation/
│       │   └── fake_data_generator.py # synthetic dataset generator
│       └── utils/
│           └── logger.py         # shared logging utility
├── main.py                       # repository entry point
├── requirements.txt
└── .gitignore
```

## Results
- Consolidated and cleaned dataset: `output/clean_data.xlsx`
- Executive report: `output/sales_report.xlsx` with:
  - Overview KPIs
  - Top Products
  - Revenue by Country
  - Revenue by Category
  - Clean Data snapshot

## Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Regenerate demo data:
   ```bash
   python src/generate_fake_data.py
   ```
3. Run automation (recommended):
   ```bash
   python main.py
   ```

Backward-compatible commands still work:
```bash
python src/automate_excel.py
python src/main.py
```

## Notes
- This is a data automation/analytics pipeline (not an ML model training project).
- Place new monthly source files into `data/` and rerun the pipeline.
