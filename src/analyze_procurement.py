import pandas as pd
from pathlib import Path


# --------------------------------
# DATEN EINLESEN
# --------------------------------

DATA_FILE = Path("data/processed/procurement_clean.csv")

df = pd.read_csv(
    DATA_FILE,
    parse_dates=["order_date"]
)

print("Datensätze:", len(df))


# --------------------------------
# KPI 1: EINKAUFSVOLUMEN
# --------------------------------

total_procurement_volume = df["total_cost"].sum()

print(
    f"\nGesamtes Einkaufsvolumen: "
    f"{total_procurement_volume:,.2f} €"
)


# --------------------------------
# KPI 2: REKLAMATIONSQUOTE
# --------------------------------

complaint_rate = (
    df["complaint"].eq("Ja").mean() * 100
)

print(
    f"Reklamationsquote: "
    f"{complaint_rate:.2f} %"
)


# --------------------------------
# KPI 3: PREISENTWICKLUNG
# --------------------------------

df["year_month"] = df["order_date"].dt.to_period("M")

monthly_prices = (
    df.groupby("year_month")["unit_price"]
    .mean()
    .reset_index()
)

monthly_prices["year_month"] = (
    monthly_prices["year_month"].astype(str)
)

print("\nDurchschnittliche Einkaufspreise pro Monat:")


print(monthly_prices)
# --------------------------------
# PREISENTWICKLUNG JE PRODUKT
# --------------------------------

product_price_trend = (
    df.groupby(["year_month", "product"])["unit_price"]
    .mean()
    .reset_index()
)

print("\nPreisentwicklung je Produkt:")
print(product_price_trend.head(20))


# --------------------------------
# LIEFERANTENANALYSE
# --------------------------------

supplier_analysis = (
    df.groupby("supplier")
    .agg(
        procurement_volume=("total_cost", "sum"),
        average_price=("unit_price", "mean"),
        average_delivery_days=("delivery_days", "mean"),
        complaints=("complaint", lambda x: (x == "Ja").sum()),
        orders=("order_id", "count")
    )
    .reset_index()
)

supplier_analysis["complaint_rate"] = (
    supplier_analysis["complaints"]
    / supplier_analysis["orders"]
    * 100
)

supplier_analysis = supplier_analysis.sort_values(
    "procurement_volume",
    ascending=False
)

print("\nLieferantenanalyse:")
print(supplier_analysis)