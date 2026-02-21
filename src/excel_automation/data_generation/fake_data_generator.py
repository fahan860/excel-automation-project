import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from faker import Faker
import numpy as np
import pandas as pd

from excel_automation.config import DATA_DIR

fake = Faker()
Faker.seed(1234)
random.seed(1234)
np.random.seed(1234)

PRODUCTS = [
    {"name": "iPhone 14", "category": "Smartphones", "price_min": 699, "price_max": 999},
    {"name": "Galaxy S23", "category": "Smartphones", "price_min": 649, "price_max": 949},
    {"name": "Pixel 8", "category": "Smartphones", "price_min": 599, "price_max": 899},
    {"name": "AirPods Pro", "category": "Accessories", "price_min": 199, "price_max": 299},
    {"name": "iPad Air", "category": "Tablets", "price_min": 499, "price_max": 899},
    {"name": "MacBook Air", "category": "Laptops", "price_min": 999, "price_max": 1699},
    {"name": "PlayStation 5", "category": "Gaming", "price_min": 399, "price_max": 599},
    {"name": "Nintendo Switch", "category": "Gaming", "price_min": 299, "price_max": 399},
    {"name": "Amazon Echo", "category": "Smart Home", "price_min": 79, "price_max": 149},
    {"name": "Kindle Paperwhite", "category": "E-Readers", "price_min": 129, "price_max": 189},
]

DATE_FORMATS: List[str] = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%b %d, %Y",
    None,
    "excel_serial",
]


def variant_names(base_name: str) -> List[str]:
    simple = base_name.lower().replace(" ", "")
    hyphen = base_name.replace(" ", "-")
    spaced = f" {base_name} "
    noisy = base_name.replace(" ", "  ")
    upper = base_name.upper()
    pro_suffix = base_name + (" Pro" if "iPhone" in base_name or "Galaxy" in base_name else "")
    alternate_brand = (
        base_name.replace("iPhone", "Apple iPhone")
        .replace("Galaxy", "Samsung Galaxy")
        .replace("Pixel", "Google Pixel")
    )
    return [base_name, simple, hyphen, spaced, noisy, upper, pro_suffix, alternate_brand]


def random_date_in_month(year: int, month: int) -> datetime:
    start = datetime(year, month, 1)
    end = start.replace(day=28) + timedelta(days=4)
    end = end - timedelta(days=end.day - 1)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, max(0, delta_days - 1)))


def format_date(dt: datetime):
    date_format = random.choice(DATE_FORMATS)
    if date_format is None:
        return dt
    if date_format == "excel_serial":
        base = datetime(1899, 12, 30)
        return (dt - base).days
    return dt.strftime(date_format)


def maybe_missing(value, prob: float = 0.05):
    return None if random.random() < prob else value


def build_month_df(year: int, month: int, n_rows: int = 400) -> pd.DataFrame:
    rows = []
    countries = [fake.country() for _ in range(30)]

    for _ in range(n_rows):
        product_meta = random.choice(PRODUCTS)
        product_name = random.choice(variant_names(product_meta["name"]))
        category = product_meta["category"]
        quantity = random.randint(1, 5)
        price = round(random.uniform(product_meta["price_min"], product_meta["price_max"]), 2)
        date_value = format_date(random_date_in_month(year, month))
        country = random.choice(countries)

        rows.append(
            {
                "date": maybe_missing(date_value, prob=0.03),
                "product": maybe_missing(product_name, prob=0.04),
                "category": maybe_missing(category, prob=0.03),
                "quantity": maybe_missing(quantity, prob=0.06),
                "price": maybe_missing(price, prob=0.05),
                "country": maybe_missing(country, prob=0.03),
            }
        )

    df = pd.DataFrame(rows)
    if len(df) > 0:
        duplicate_count = max(1, len(df) // 33)
        duplicated_rows = df.sample(duplicate_count, random_state=1234)
        df = pd.concat([df, duplicated_rows], ignore_index=True)

    return df.sample(frac=1.0, random_state=42).reset_index(drop=True)


def save_month(year: int, month: int, path: Path) -> None:
    month_df = build_month_df(year, month, n_rows=450)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        month_df.to_excel(writer, index=False, sheet_name="sales")


def generate_demo_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    files = [
        (2025, 1, DATA_DIR / "sales_jan.xlsx"),
        (2025, 2, DATA_DIR / "sales_feb.xlsx"),
        (2025, 3, DATA_DIR / "sales_mar.xlsx"),
    ]

    for year, month, file_path in files:
        print(f"Generating data for {year}-{month:02d} -> {file_path}")
        save_month(year, month, file_path)

    print("Done generating demo sales files.")
