"""Extract: baca CSV mentah, validasi, simpan ke Parquet."""
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
CSV_FILE = RAW_DIR / "cardekho_dataset.csv"
OUTPUT_FILE = PROCESSED_DIR / "extracted.parquet"

EXPECTED_ROWS = 8128
EXPECTED_COLS = 8


def main() -> None:
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV tidak ditemukan: {CSV_FILE}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(CSV_FILE)

    print(f"File       : {CSV_FILE}")
    print(f"Shape      : {df.shape}")
    print(f"Kolom      : {list(df.columns)}")
    print(f"Tipe data  :\n{df.dtypes}")

    n_rows, n_cols = df.shape
    if n_rows != EXPECTED_ROWS:
        print(f"WARNING: jumlah baris {n_rows} != ekspektasi {EXPECTED_ROWS}")
    if n_cols != EXPECTED_COLS:
        print(f"WARNING: jumlah kolom {n_cols} != ekspektasi {EXPECTED_COLS}")

    print(f"Missing values per kolom:\n{df.isna().sum()}")

    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"Tersimpan  : {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
