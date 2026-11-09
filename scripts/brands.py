"""Daftar merek resmi + helper normalisasi brand."""

# 31 merek final, ejaan yang benar sesuai data asli
BRAND_CANONICAL = {
    "Audi",
    "BMW",
    "Bentley",
    "Datsun",
    "Ferrari",
    "Force",
    "Ford",
    "Honda",
    "Hyundai",
    "Isuzu",
    "Jaguar",
    "Jeep",
    "Kia",
    "Land Rover",
    "Lexus",
    "MG",
    "Mahindra",
    "Maruti",
    "Maserati",
    "Mercedes-AMG",
    "Mercedes-Benz",
    "Mini",
    "Nissan",
    "Porsche",
    "Renault",
    "Rolls-Royce",
    "Skoda",
    "Tata",
    "Toyota",
    "Volkswagen",
    "Volvo",
}

# Mapping dari lowercase -> ejaan kanonik
_BRAND_LOWER_TO_CANONICAL = {b.lower(): b for b in BRAND_CANONICAL}


def normalize_brand(series):
    """Normalisasi kolom brand ke ejaan kanonik.

    - strip spasi
    - lowercase untuk pencocokan
    - map ke ejaan kanonik
    - jika tidak dikenal, kembalikan nilai asli (dengan warning terpisah)
    """
    stripped = series.str.strip()
    lowered = stripped.str.lower()
    result = lowered.map(_BRAND_LOWER_TO_CANONICAL)
    unknown = stripped[result.isna()].unique()
    if len(unknown) > 0:
        raise ValueError(f"Brand tidak dikenal (perlu ditambah ke BRAND_CANONICAL): {unknown}")
    return result
