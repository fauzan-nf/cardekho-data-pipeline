# cardekho-data-pipeline

End-to-end ETL pipeline untuk analisis harga mobil bekas, dibangun dengan
Python, PostgreSQL, dan Apache Airflow. Mengubah data mentah iklan mobil
menjadi tabel analitik yang siap pakai untuk tim Business & Product.

## Arsitektur
CSV mentah (data/raw/)
│
▼ extract.py
Parquet mentah (data/processed/extracted.parquet)
│
▼ transform.py
Parquet bersih (data/processed/transformed.parquet)
│
▼ load.py
PostgreSQL: tabel raw_mobil (15.411 baris)
│
▼ analytics.py
PostgreSQL: tabel analytics_harga_per_merek
│
▼ queries.sql
Insight untuk Business & Product


## Dataset

- **Sumber**: [Cardekho Used Car Data](https://www.kaggle.com/datasets/manishkr1754/cardekho-used-car-data) (Kaggle)
- **Baris**: 15.411
- **Kolom**: 14 (setelah transformasi: 13 — kolom `Unnamed: 0` dibuang)
- **Periode**: data iklan mobil bekas di India

## Cara Menjalankan

```bash
# 1. Clone & setup
git clone https://github.com/fauzan-nf/cardekho-data-pipeline.git
cd cardekho-data-pipeline
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Siapkan .env dari template
copy .env.example .env
# edit .env dengan kredensial PostgreSQL lokal

# 3. Jalankan PostgreSQL via Docker
docker compose up -d

# 4. Jalankan pipeline
python scripts/extract.py
python -m scripts.transform
python scripts/load.py
python scripts/analytics.py

# 5. Lihat insight
docker exec -it cardekho-postgres psql -U postgres -d cardekho \ -c "SELECT * FROM analytics_harga_per_merek LIMIT 10;"

Top 10 merek dengan rata-rata harga tertinggi
    brand     | rata_rata_harga_merek | total_iklan 
--------------+-----------------------+-------------
 Ferrari      |              39500000 |           1
 Rolls-Royce  |              24200000 |           1
 Bentley      |               8975000 |           3
 Maserati     |               6100000 |           2
 Lexus        |               5744583 |          10
 Mercedes-AMG |               5100000 |           1
 Porsche      |               4745885 |          21
 Land Rover   |               3909049 |          51
 Volvo        |               3643033 |          20
 Jaguar       |               2746817 |          59
(10 rows)

Tren depresiasi harga berdasarkan umur kendaraan
kelompok_umur | jumlah_iklan | rata_rata_harga | median_harga 
---------------+--------------+-----------------+--------------
 0-3 tahun     |         3297 |         1044655 |       755000
 4-6 tahun     |         6293 |          838516 |       620000
 7-10 tahun    |         4457 |          621149 |       450000
 >10 tahun     |         1364 |          332559 |       250000
(4 rows)

Takeaway: harga rata-rata turun dari Rp ... (0-3 tahun) menjadi Rp ... (>10 tahun),
menunjukkan depresiasi ...% per kelompok umur.

Distribusi iklan berdasarkan bahan bakar × transmisi
     brand     | median_harga_segmen_muda | total_iklan 
---------------+--------------------------+-------------
 Mercedes-Benz |                  4107500 |          83
 BMW           |                  3333333 |         143
 Toyota        |                  1765833 |         293
 Skoda         |                  1002500 |         100
 Mahindra      |                   926500 |         390
 Honda         |                   737500 |         590
 Ford          |                   716667 |         310
 Volkswagen    |                   708333 |         154
 Hyundai       |                   664167 |        1147
 Maruti        |                   603333 |        2247
(10 rows)

Merek dengan median harga tertinggi di segmen mobil muda (3-5 tahun)
 brand | vehicle_age |  rata_rata_harga   | median_harga | jumlah_iklan 
-------+-------------+--------------------+--------------+--------------
 Audi  |           1 |            5700000 |      5700000 |            2
 Audi  |           2 |            5422500 |      5422500 |            2
 Audi  |           3 |            3609000 |      3490000 |            5
 Audi  |           4 |            3133750 |      2950000 |           12
 Audi  |           5 |  2610285.714285714 |      2675000 |           21
 Audi  |           6 | 2635642.8571428573 |      2412500 |           14
 Audi  |           7 | 1748794.1176470588 |      1750500 |           34
 Audi  |           8 | 1637540.5405405406 |      1495000 |           37
 Audi  |           9 | 1438621.6216216215 |      1345000 |           37
 Audi  |          10 | 1216105.2631578948 |      1100000 |           19
(10 rows)

## Struktur Project
cardekho-data-pipeline/
├── dags/                  # DAG Airflow (menyusul)
├── scripts/
│   ├── extract.py         # baca CSV → Parquet
│   ├── transform.py       # bersihkan & normalisasi
│   ├── load.py            # Parquet → PostgreSQL raw_mobil
│   ├── analytics.py       # raw_mobil → analytics_harga_per_merek
│   ├── brands.py          # daftar merek kanonik + normalisasi
│   └── test_connection.py # uji koneksi PostgreSQL
├── sql/
│   ├── analytics.sql      # DDL tabel analitik
│   └── queries.sql        # query insight
├── data/
│   ├── raw/               # CSV mentah (gitignored)
│   └── processed/         # Parquet hasil proses (gitignored)
├── docker-compose.yml     # PostgreSQL
├── requirements.txt
├── NOTES.md               # keputusan desain & catatan eksplorasi
└── README.md


## Failure Handling

Pipeline diuji dengan skenario kegagalan untuk memastikan monitoring & recovery bekerja:

### Skenario: file CSV hilang (typo nama file)

1. `scripts/extract.py` diubah agar mencari `cardekho_dataset_TYPO.csv`.
2. DAG di-trigger manual → task `extract` gagal (merah), task lain tidak jalan.
3. Log task `extract` menunjukkan: ![alt text](log_task_failed.png)
4. Nama file dikembalikan ke `cardekho_dataset.csv`.
5. DAG di-trigger ulang → semua 4 task hijau. ![alt text](trigger_ulang.png)

Pelajaran: dengan `>>` dependency, kegagalan di `extract` otomatis mencegah `transform`, `load`, dan `analytics` berjalan — data warehouse tidak tercemar data parsial. `retries=1` memberi kesempatan kedua sebelum task dinyatakan gagal.