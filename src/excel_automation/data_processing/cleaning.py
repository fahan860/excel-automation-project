from datetime import datetime, timedelta
from typing import Tuple

import numpy as np
import pandas as pd

from excel_automation.config import PRODUCT_CANONICAL, RELEVANT_COLS


def parse_mixed_dates(series: pd.Series) -> pd.Series:
    def parse_one(value):
        if pd.isna(value):
            return pd.NaT
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            try:
                base = datetime(1899, 12, 30)
                return base + timedelta(days=int(value))
            except Exception:
                return pd.NaT
        if isinstance(value, (datetime, np.datetime64)):
            try:
                return pd.Timestamp(value)
            except Exception:
                return pd.NaT

        text = str(value).strip()
        for dayfirst in (False, True):
            try:
                return pd.to_datetime(text, errors="raise", dayfirst=dayfirst)
            except Exception:
                pass

        try:
            return pd.to_datetime(text, errors="coerce")
        except Exception:
            return pd.NaT

    return series.apply(parse_one)


def normalize_key(value: str) -> str:
    if value is None:
        return ""

    try:
        if isinstance(value, float) and np.isnan(value):
            return ""
    except Exception:
        pass

    try:
        normalized = str(value).lower().strip()
    except Exception:
        normalized = ""

    return "".join(character for character in normalized if character.isalnum())


def standardize_product_and_category(product: pd.Series, category: pd.Series) -> Tuple[pd.Series, pd.Series]:
    def map_one(name: str) -> Tuple[str, str]:
        key = normalize_key(name or "")
        if key in PRODUCT_CANONICAL:
            return PRODUCT_CANONICAL[key]

        for pattern, (canonical_name, canonical_category) in PRODUCT_CANONICAL.items():
            if pattern in key:
                return canonical_name, canonical_category

        try:
            if name is None or (isinstance(name, float) and np.isnan(name)):
                clean_name = ""
            else:
                clean_name = str(name)
        except Exception:
            clean_name = ""

        clean_name = " ".join(clean_name.strip().split())
        return clean_name.title(), None

    mapped = product.apply(map_one)
    standardized_product = mapped.apply(lambda item: item[0])
    mapped_category = mapped.apply(lambda item: item[1])

    final_category = []
    for index in range(len(category)):
        existing_category = category.iat[index]
        generated_category = mapped_category.iat[index]
        final_category.append(
            generated_category if generated_category is not None else (
                existing_category if pd.notna(existing_category) else "Unknown"
            )
        )

    return standardized_product, pd.Series(final_category, index=category.index)


def impute_numeric(series: pd.Series, by_group: pd.Series) -> pd.Series:
    frame = pd.DataFrame({"value": series, "group": by_group})
    medians = frame.groupby("group", dropna=False)["value"].median()
    overall_median = frame["value"].median()

    def fill_one(value, group):
        if pd.isna(value):
            group_median = medians.get(group, np.nan)
            return overall_median if pd.isna(group_median) else group_median
        return value

    return frame.apply(lambda row: fill_one(row["value"], row["group"]), axis=1)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    present_columns = [column for column in RELEVANT_COLS if column in df.columns]
    df = df[present_columns].copy()
    df.dropna(how="all", inplace=True)

    if "date" in df.columns:
        df["date"] = parse_mixed_dates(df["date"])

    product_series = df["product"] if "product" in df.columns else pd.Series([None] * len(df))
    category_series = df["category"] if "category" in df.columns else pd.Series([None] * len(df))
    standardized_product, standardized_category = standardize_product_and_category(product_series, category_series)
    df["product"] = standardized_product
    df["category"] = standardized_category

    if "product" in df.columns:
        df = df[df["product"].notna() & (df["product"].astype(str).str.len() > 0)]
    if "date" in df.columns:
        df = df[df["date"].notna()]

    if "quantity" in df.columns:
        df["quantity"] = impute_numeric(df["quantity"], df["product"])
        df["quantity"] = df["quantity"].round().astype(int)
        df["quantity"] = df["quantity"].clip(lower=0)
    else:
        df["quantity"] = 0

    if "price" in df.columns:
        df["price"] = impute_numeric(df["price"], df["product"])
        df["price"] = df["price"].astype(float).clip(lower=0.0)
    else:
        df["price"] = 0.0

    if "country" in df.columns:
        df["country"] = df["country"].fillna("Unknown")
    else:
        df["country"] = "Unknown"

    key_columns = ["date", "product", "quantity", "price", "country"]
    key_columns = [column for column in key_columns if column in df.columns]
    df = df.drop_duplicates(subset=key_columns)

    df["total_price"] = df["quantity"] * df["price"]
    df = df.sort_values(by=["date", "product"]).reset_index(drop=True)
    return df
