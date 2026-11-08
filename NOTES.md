# Proyek: Analisis Harga Mobil Bekas

## Ringkasan
- Masalah: Tim Product butuh tahu rata-rata harga mobil bekas per merek & tahun.
- Data: daftar iklan mobil bekas (merek, tahun, harga, lokasi, kilometer).
- Output: tabel analytics_harga_per_merek (merek, tahun, rata_rata_harga, jumlah_iklan).

## Sumber Data
- URL: https://www.kaggle.com/datasets/manishkr1754/cardekho-used-car-data
- Diakses: 8 Nov 2026
- File lokal: data/raw/CAR DETAILS FROM CARDEKHO.csv
- Ukuran file: __ MB
- Baris: ____ | Kolom: 8   (verifikasi ulang via df.shape)
- Kolom: name (teks), year (angka), selling_price (angka), km_driven (angka),
  fuel (teks), seller_type (teks), transmission (teks), owner (teks)

## Masalah Data & Rencana Penanganan
| Masalah | Jumlah Baris | Rencana Penanganan |
|---|---|---|
| name = merek+model menyatu | 8.128 | Split kata pertama; mapping merek multi-kata |
| selling_price = 0 | __ | Hapus baris (tidak valid untuk rata-rata) |
| (tambahkan temuan lain) | __ | __ |

## Definisi Merek
- Merek = kata pertama pada kolom `name`.
- Merek multi-kata diperbaiki via mapping manual:
  - "Land" → "Land Rover"
  - (tambahkan sesuai hasil eksplorasi)

## Definisi Selesai (Definition of Done)
- Data mentah berhasil dimuat ke tabel PostgreSQL `raw_mobil`.
- Tabel analitik `analytics_harga_per_merek` berisi agregasi merek × tahun.
- DAG Airflow harian menjalankan extract → transform → load → analytics tanpa error.
- Query analitik bisa dijalankan dan hasilnya tampil di README (screenshot/teks).
- Jumlah baris raw_mobil = jumlah baris bersih di data/processed;
  selisih (baris dibuang karena harga = 0) tercatat di README.