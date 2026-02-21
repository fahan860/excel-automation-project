from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
CLEAN_PATH = OUTPUT_DIR / "clean_data.xlsx"
REPORT_PATH = OUTPUT_DIR / "sales_report.xlsx"

PRODUCT_CANONICAL = {
    "iphone14": ("iPhone 14", "Smartphones"),
    "galaxys23": ("Galaxy S23", "Smartphones"),
    "pixel8": ("Pixel 8", "Smartphones"),
    "airpodspro": ("AirPods Pro", "Accessories"),
    "ipadair": ("iPad Air", "Tablets"),
    "macbookair": ("MacBook Air", "Laptops"),
    "ps5": ("PlayStation 5", "Gaming"),
    "playstation5": ("PlayStation 5", "Gaming"),
    "nintendoswitch": ("Nintendo Switch", "Gaming"),
    "switch": ("Nintendo Switch", "Gaming"),
    "amazonecho": ("Amazon Echo", "Smart Home"),
    "echo": ("Amazon Echo", "Smart Home"),
    "kindlepaperwhite": ("Kindle Paperwhite", "E-Readers"),
    "kindle": ("Kindle Paperwhite", "E-Readers"),
}

RELEVANT_COLS = ["date", "product", "category", "quantity", "price", "country"]
