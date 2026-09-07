import pandas as pd
import numpy as np
from pathlib import Path
N_ROWS=50_000
np.random.seed(42)

categories_products = {
    "Obst & Gemüse": ["Äpfel", "Bananen", "Tomaten", "Kartoffeln", "Karotten"],
    "Milchprodukte": ["Milch", "Joghurt", "Käse", "Butter"],
    "Getreide": ["Reis", "Mehl", "Haferflocken", "Nudeln"],
    "Fleisch": ["Hähnchen", "Rindfleisch", "Putenfleisch"],
    "Tiefkühlprodukte": ["TK-Gemüse", "TK-Beeren", "TK-Pommes"]
}


suppliers = [
    "AgroFresh GmbH",
    "GreenFields GmbH",
    "NordFood GmbH",
    "BioHarvest GmbH",
    "FreshTrade GmbH",
    "EuroFoods GmbH",
    "LandGut GmbH",
    "FoodSupply GmbH"
]
base_prices = {
    "Äpfel": 1.40,
    "Bananen": 1.20,
    "Tomaten": 2.00,
    "Kartoffeln": 0.90,
    "Karotten": 1.10,
    "Milch": 0.95,
    "Joghurt": 0.70,
    "Käse": 5.50,
    "Butter": 2.20,
    "Reis": 1.80,
    "Mehl": 0.80,
    "Haferflocken": 1.30,
    "Nudeln": 1.10,
    "Hähnchen": 6.50,
    "Rindfleisch": 11.00,
    "Putenfleisch": 7.20,
    "TK-Gemüse": 2.50,
    "TK-Beeren": 4.50,
    "TK-Pommes": 2.00
}

supplier_profiles = {
    "AgroFresh GmbH": {
        "price_factor": 1.05,
        "complaint_rate": 0.02,
        "delivery_mean": 3
    },
    "GreenFields GmbH": {
        "price_factor": 0.96,
        "complaint_rate": 0.08,
        "delivery_mean": 6
    },
    "NordFood GmbH": {
        "price_factor": 1.00,
        "complaint_rate": 0.04,
        "delivery_mean": 4
    },
    "BioHarvest GmbH": {
        "price_factor": 1.10,
        "complaint_rate": 0.015,
        "delivery_mean": 3
    },
    "FreshTrade GmbH": {
        "price_factor": 0.98,
        "complaint_rate": 0.05,
        "delivery_mean": 5
    },
    "EuroFoods GmbH": {
        "price_factor": 1.02,
        "complaint_rate": 0.03,
        "delivery_mean": 4
    },
    "LandGut GmbH": {
        "price_factor": 0.94,
        "complaint_rate": 0.07,
        "delivery_mean": 7
    },
    "FoodSupply GmbH": {
        "price_factor": 1.04,
        "complaint_rate": 0.025,
        "delivery_mean": 3
    }
}

# Alle Produkte in eine einfache Liste umwandeln
all_products = [
    product
    for products in categories_products.values()
    for product in products
]
start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-07-31")

# Zufällige Bestelldaten erzeugen
date_range_days = (end_date - start_date).days

order_dates = start_date + pd.to_timedelta(
    np.random.randint(0, date_range_days + 1, N_ROWS),
    unit="D"
)

# Zufällige Lieferanten und Produkte auswählen
selected_suppliers = np.random.choice(suppliers, N_ROWS)
selected_products = np.random.choice(all_products, N_ROWS)

# Mengen erzeugen
quantities = np.random.randint(10, 1001, N_ROWS)


# Produkt -> Kategorie zuordnen
product_to_category = {
    product: category
    for category, products in categories_products.items()
    for product in products
}

categories = [product_to_category[p] for p in selected_products]

# Preise, Lieferzeiten und Reklamationen erzeugen
unit_prices = []
delivery_days = []
complaints = []

for product, supplier, order_date in zip(
    selected_products,
    selected_suppliers,
    order_dates
):
    profile = supplier_profiles[supplier]

    # Preisentwicklung über die Zeit
    years_since_start = (order_date - start_date).days / 365.25
    trend_factor = 1 + 0.04 * years_since_start

    # kleine zufällige Preisschwankung
    random_price_factor = np.random.normal(1.0, 0.04)

    price = (
        base_prices[product]
        * profile["price_factor"]
        * trend_factor
        * random_price_factor
    )

    unit_prices.append(round(max(price, 0.01), 2))

    # Lieferzeit
    delivery = np.random.normal(
        profile["delivery_mean"],
        1.5
    )

    delivery_days.append(max(1, int(round(delivery))))

    # Reklamation ja/nein
    complaint = np.random.random() < profile["complaint_rate"]
    complaints.append("Ja" if complaint else "Nein")

    # Gesamtkosten berechnen
total_costs = [
    round(quantity * price, 2)
    for quantity, price in zip(quantities, unit_prices)
]

# DataFrame erstellen
df = pd.DataFrame({
    "order_id": [f"PO-{i:06d}" for i in range(1, N_ROWS + 1)],
    "order_date": order_dates,
    "supplier": selected_suppliers,
    "product": selected_products,
    "category": categories,
    "quantity": quantities,
    "unit_price": unit_prices,
    "total_cost": total_costs,
    "delivery_days": delivery_days,
    "complaint": complaints
})

# Nach Datum sortieren
df = df.sort_values("order_date").reset_index(drop=True)

print(df.head())
print("\nAnzahl der Zeilen:", len(df))

# Speicherort festlegen
output_path = Path("data/raw/procurement_data.csv")

# Daten als CSV speichern
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\nCSV gespeichert unter: {output_path}")