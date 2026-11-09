"""Transform: bersihkan dataset sesuai keputusan di NOTES.md."""
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/processed/extracted.parquet")
OUTPUT_FILE = Path("data/processed/transformed.parquet")

# Mapping untuk duplikasi case yang terdeteksi di check_brands.py
# Normalisasi .str.title() akan mengubah 'ISUZU' -> 'Isuzu', jadi sebenarnya
# tidak perlu mapping manual. Tapi kita simpan mapping eksplisit untuk audit
# dan untuk jaga-jaga kalau ada varian lain di masa depan.
BRAND_MAPPING = {
    "Isuzu": "Isuzu",   # 'ISUZU' -> title case -> 'Isuzu', sudah benar
}


def main() -> None:
    df = pd.read_parquet(INPUT_FILE)
    n_before = len(df)
    print(f"Rows before: {n_before}")

    # 1. Drop kolom sisa index
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])
        print("Dropped column: Unnamed: 0")

    # 2. Normalisasi brand: strip + title case
    df["brand"] = df["brand"].str.strip().str.title()
    print(f"Unique brand setelah normalisasi: {df['brand'].nunique()}")

    # 3. seats = 0 DIBIARKAN (keputusan: tidak mengubah dataset asli)
    n_seats_zero = int((df["seats"] == 0).sum())
    print(f"Baris seats=0 (dibiarkan): {n_seats_zero}")

    n_after = len(df)
    assert n_before == n_after, f"Jumlah baris berubah: {n_before} -> {n_after}"

    df.to_parquet(OUTPUT_FILE, index=False)
    print(f"Rows after : {n_after}")
    print(f"Tersimpan  : {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
