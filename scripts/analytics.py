"""Analytics: bangun tabel analytics_harga_per_merek dari raw_mobil."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

SQL_DIR = Path("sql")
DDL_FILE = SQL_DIR / "analytics.sql"

DDL = '''
CREATE TABLE IF NOT EXISTS analytics_harga_per_merek (
    brand             TEXT NOT NULL,
    vehicle_age       INTEGER NOT NULL,
    rata_rata_harga   DOUBLE PRECISION NOT NULL,
    median_harga      DOUBLE PRECISION NOT NULL,
    jumlah_iklan      BIGINT NOT NULL,
    PRIMARY KEY (brand, vehicle_age)
)
'''

INSERT_SQL = '''
INSERT INTO analytics_harga_per_merek
SELECT brand,
       vehicle_age,
       AVG(selling_price) AS rata_rata_harga,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY selling_price) AS median_harga,
       COUNT(*) AS jumlah_iklan
FROM raw_mobil
GROUP BY brand, vehicle_age
'''


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
    engine = get_engine()

    with engine.begin() as conn:
        # 1. Pastikan tabel ada
        conn.execute(text(DDL))
        print("Table analytics_harga_per_merek siap")

        # 2. Kosongkan (idempoten)
        conn.execute(text("TRUNCATE analytics_harga_per_merek"))
        print("Truncated analytics_harga_per_merek")

        # 3. Insert hasil agregasi
        conn.execute(text(INSERT_SQL))
        print("Inserted hasil agregasi")

        # 4. Verifikasi: jumlah baris hasil == kombinasi unik (brand, vehicle_age)
        n_expected = conn.execute(
            text("SELECT COUNT(*) FROM (SELECT DISTINCT brand, vehicle_age FROM raw_mobil) t")
        ).scalar()
        n_actual = conn.execute(text("SELECT COUNT(*) FROM analytics_harga_per_merek")).scalar()

    print(f"Expected rows: {n_expected}")
    print(f"Actual rows  : {n_actual}")
    if n_actual != n_expected:
        raise AssertionError(f"Jumlah baris tidak cocok: {n_actual} != {n_expected}")

    print("OK: analytics selesai dan terverifikasi")


if __name__ == "__main__":
    main()
