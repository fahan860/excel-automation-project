from pathlib import Path
from typing import List, Optional

import pandas as pd


def generate_report(df: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_revenue = float(df["total_price"].sum())
    by_product_quantity = df.groupby("product")["quantity"].sum().sort_values(ascending=False)
    by_product_revenue = df.groupby("product")["total_price"].sum().sort_values(ascending=False)
    top5_products = by_product_quantity.head(5).to_frame(name="total_quantity").join(
        by_product_revenue.head(5).to_frame(name="total_revenue"), how="outer"
    )
    by_country = df.groupby("country")["total_price"].sum().sort_values(ascending=False).to_frame(name="revenue")
    by_category = df.groupby("category")["total_price"].sum().sort_values(ascending=False).to_frame(name="revenue")

    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        overview = pd.DataFrame(
            {
                "Metric": ["Total Revenue", "Rows (cleaned)", "Unique Products", "Countries"],
                "Value": [total_revenue, len(df), df["product"].nunique(), df["country"].nunique()],
            }
        )
        overview.to_excel(writer, index=False, sheet_name="Overview")
        top5_products.reset_index().to_excel(writer, index=False, sheet_name="Top Products")
        by_country.reset_index().to_excel(writer, index=False, sheet_name="Revenue by Country")
        by_category.reset_index().to_excel(writer, index=False, sheet_name="Revenue by Category")
        df.to_excel(writer, index=False, sheet_name="Clean Data")

        workbook = writer.book
        money_format = workbook.add_format({"num_format": "$#,##0", "align": "right"})
        header_format = workbook.add_format({"bold": True, "bg_color": "#DDEBF7"})
        normal_format = workbook.add_format({"text_wrap": False})

        def format_sheet(worksheet, local_df: pd.DataFrame, money_columns: Optional[List[str]] = None) -> None:
            for column_index, column_name in enumerate(local_df.columns):
                worksheet.write(0, column_index, column_name, header_format)
                width = max(12, min(30, int(local_df[column_name].astype(str).str.len().mean() + 6)))
                worksheet.set_column(column_index, column_index, width, normal_format)

            if money_columns:
                for column_index, column_name in enumerate(local_df.columns):
                    if column_name in money_columns:
                        worksheet.set_column(column_index, column_index, None, money_format)

        format_sheet(writer.sheets["Overview"], overview, money_columns=["Value"])
        format_sheet(writer.sheets["Top Products"], top5_products.reset_index(), money_columns=["total_revenue"])
        format_sheet(writer.sheets["Revenue by Country"], by_country.reset_index(), money_columns=["revenue"])
        format_sheet(writer.sheets["Revenue by Category"], by_category.reset_index(), money_columns=["revenue"])
        format_sheet(writer.sheets["Clean Data"], df, money_columns=["price", "total_price"])
