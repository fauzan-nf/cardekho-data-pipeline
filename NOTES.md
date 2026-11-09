## Sumber Data (REVISI — dataset aktual)
- URL: https://www.kaggle.com/datasets/manishkr1754/cardekho-used-car-data
- Diakses: 8 Nov 2026
- File lokal: data/raw/cardekho_dataset.csv
- Ukuran file: ~1.3 MB
- Baris: 15411 | Kolom: 14
- Kolom: Unnamed: 0 (int, sisa index), car_name (teks),
  brand (teks), model (teks), vehicle_age (int, tahun),
  km_driven (int), seller_type (teks), fuel_type (teks),
  transmission_type (teks), mileage (float), engine (int),
  max_power (float), seats (int), selling_price (int)

## Masalah Data & Rencana Penanganan (REVISI berbasis eksplorasi)
| Masalah | Jumlah Baris | Rencana Penanganan |
|---|---|---|
| `Unnamed: 0` = sisa index | 15411 | Drop kolom |
| `brand` case tidak konsisten (`ISUZU` vs `Isuzu`) | 2 | Normalisasi `.str.strip().str.title()` |
| `seats = 0` (tidak masuk akal secara domain) | 2 | **Dibiarkan** — keputusan: tidak mengubah dataset asli; filter di query analitik bila perlu |
| `selling_price = 0` | 0 | Tidak ada — tidak perlu treatment |
| Outlier `vehicle_age`, `mileage`, `engine`, `max_power` | 0 | Tidak ada — distribusi wajar |
| Missing values | 0 di semua kolom | Tidak perlu imputasi |

## Definisi Merek (REVISI)
- Merek = kolom `brand` (sudah tersedia, tidak perlu split).
- Normalisasi: `brand.str.strip().str.title()`.
- Verifikasi: setelah normalisasi, jumlah unique brand = 31 (dari 32, karena ISUZU → Isuzu).

## Keputusan `seats = 0`
- **Dibiarkan** (2 baris). Tidak menghapus baris dari dataset asli.
- Jika query analitik butuh kendaraan dengan kursi valid, gunakan `WHERE seats > 0` di query, bukan di tahap transform.

## Definisi Selesai
- Data mentah berhasil dimuat ke tabel PostgreSQL `raw_mobil`.
- Tabel analitik `analytics_harga_per_merek` berisi agregasi brand × vehicle_age.
- DAG Airflow harian menjalankan extract → transform → load → analytics tanpa error.
- Query analitik bisa dijalankan dan hasilnya tampil di README.
- Jumlah baris raw_mobil (15411) = jumlah baris di data/processed (15411);
  tidak ada baris dihapus pada tahap transform; normalisasi brand tidak mengubah jumlah baris.