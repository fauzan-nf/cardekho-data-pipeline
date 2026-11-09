"""Load: muat transformed.parquet ke tabel raw_mobil di PostgreSQL."""
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

INPUT_FILE = Path("data/processed/transformed.parquet")
TABLE_NAME = "raw_mobil"


def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
    )
    return create_engine(url)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"File input tidak ditemukan: {INPUT_FILE}")

    df = pd.read_parquet(INPUT_FILE)
    n_input = len(df)
    print(f"Input      : {INPUT_FILE}")
    print(f"Rows       : {n_input}")
    print(f"Columns    : {list(df.columns)}")

    engine = get_engine()

    # Truncate lalu insert ulang (idempoten: aman dijalankan berkali-kali)
    with engine.begin() as conn:
        # Cek tabel sudah ada atau belum; kalau belum, pandas to_sql akan membuatnya
        exists = conn.execute(
            text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :t)"),
            {"t": TABLE_NAME},
        ).scalar()

        if exists:
            conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME}"))
            print(f"Truncated  : {TABLE_NAME}")
        else:
            print(f"Table {TABLE_NAME} belum ada, akan dibuat oleh pandas")

    # Load ke database
    df.to_sql(TABLE_NAME, engine, if_exists="append", index=False, method="multi", chunksize=1000)
    print(f"Inserted   : {n_input} rows into {TABLE_NAME}")

    # Verifikasi jumlah baris di database
    with engine.connect() as conn:
        n_db = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}")).scalar()

    print(f"Rows in DB : {n_db}")
    if n_db != n_input:
        raise AssertionError(f"Jumlah baris DB ({n_db}) != input ({n_input})")

    print("OK: load selesai dan terverifikasi")


if __name__ == "__main__":
    main()
