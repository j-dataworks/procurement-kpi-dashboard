import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# --------------------------------
# DATEN EINLESEN
# --------------------------------

DATA_FILE = Path("data/processed/procurement_clean.csv")

df = pd.read_csv(
    DATA_FILE,
    parse_dates=["order_date"]
)

print(f"Eingelesene Zeilen: {len(df)}")


# --------------------------------
# POSTGRESQL VERBINDUNG
# --------------------------------

DB_USER = "postgres"
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "procurement_analytics"

if not DB_PASSWORD:
    raise ValueError(
        "POSTGRES_PASSWORD ist nicht gesetzt."
    )

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(connection_url)


# --------------------------------
# DATEN IN POSTGRESQL LADEN
# --------------------------------

df.to_sql(
    "procurement",
    engine,
    if_exists="replace",
    index=False,
    method="multi",
    chunksize=1000
)

print(
    f"{len(df)} Zeilen erfolgreich "
    f"in PostgreSQL geladen."
)