import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
INCOMING_DIR = Path("data/incoming")
PROCESSED_DIR = Path("data/processed")

csv_files = list(RAW_DIR.glob("*.csv")) + list(INCOMING_DIR.glob("*.csv"))

print(f"Gefundene CSV-Dateien: {len(csv_files)}")

for file in csv_files:
    print(file)


    dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    df["source_file"] = file.name
    dataframes.append(df)

if not dataframes:
    raise FileNotFoundError("Keine CSV-Dateien gefunden.")

df_all = pd.concat(dataframes, ignore_index=True)

print("\nGesamtzahl der eingelesenen Zeilen:", len(df_all))
print("\nSpalten:")
print(df_all.columns.tolist())

# -----------------------------
# DATA QUALITY CHECKS
# -----------------------------

print("\n--- DATA QUALITY CHECKS ---")

# Fehlende Werte
print("\nFehlende Werte:")
print(df_all.isnull().sum())

# Duplikate
duplicate_count = df_all.duplicated().sum()
print("\nAnzahl kompletter Duplikate:", duplicate_count)

# Datentypen
print("\nDatentypen:")
print(df_all.dtypes)

# Ungültige Werte prüfen
print("\nUngültige Mengen:", (df_all["quantity"] <= 0).sum())
print("Ungültige Preise:", (df_all["unit_price"] <= 0).sum())
print("Ungültige Gesamtkosten:", (df_all["total_cost"] <= 0).sum())
print("Ungültige Lieferzeiten:", (df_all["delivery_days"] <= 0).sum())

# Gültige Reklamationswerte prüfen
print("\nReklamationswerte:")
print(df_all["complaint"].value_counts(dropna=False))

# -----------------------------
# DATA CLEANING
# -----------------------------

# Datum in echten Datumsdatentyp umwandeln
df_all["order_date"] = pd.to_datetime(
    df_all["order_date"],
    errors="coerce"
)

# Textfelder bereinigen
text_columns = [
    "supplier",
    "product",
    "category",
    "complaint"
]

for column in text_columns:
    df_all[column] = df_all[column].str.strip()

# Duplikate entfernen
df_all = df_all.drop_duplicates()

print("\n--- NACH DER BEREINIGUNG ---")
print("Zeilen:", len(df_all))
print("Datentyp order_date:", df_all["order_date"].dtype)


# -----------------------------
# DATA VALIDATION
# -----------------------------

print("\n--- DATA VALIDATION ---")

validation_errors = []

# Pflichtfelder prüfen
required_columns = [
    "order_id",
    "order_date",
    "supplier",
    "product",
    "category",
    "quantity",
    "unit_price",
    "total_cost",
    "delivery_days",
    "complaint"
]

for column in required_columns:
    if df_all[column].isna().any():
        validation_errors.append(
            f"Fehlende Werte in: {column}"
        )

# Fachliche Regeln prüfen
if (df_all["quantity"] <= 0).any():
    validation_errors.append("Menge <= 0 gefunden")

if (df_all["unit_price"] <= 0).any():
    validation_errors.append("Preis <= 0 gefunden")

if (df_all["total_cost"] <= 0).any():
    validation_errors.append("Gesamtkosten <= 0 gefunden")

if (df_all["delivery_days"] <= 0).any():
    validation_errors.append("Ungültige Lieferzeit gefunden")

# Reklamation darf nur Ja oder Nein sein
valid_complaints = ["Ja", "Nein"]

if not df_all["complaint"].isin(valid_complaints).all():
    validation_errors.append(
        "Ungültiger Wert in complaint gefunden"
    )

# Ergebnis ausgeben
if validation_errors:
    print("Validierung FEHLGESCHLAGEN:")

    for error in validation_errors:
        print("-", error)

else:
    print("Validierung erfolgreich.")
    print("Die Daten erfüllen alle Qualitätsregeln.")


    # -----------------------------
# CLEAN DATA SPEICHERN
# -----------------------------

if not validation_errors:

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_file = PROCESSED_DIR / "procurement_clean.csv"

    df_all.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nBereinigte Daten gespeichert: {output_file}")
    print(f"Gespeicherte Zeilen: {len(df_all)}")

else:
    print("\nDatei wurde wegen Validierungsfehlern NICHT gespeichert.")

    


