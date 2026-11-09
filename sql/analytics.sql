-- Tabel analitik: rata-rata & median harga per merek per umur kendaraan
-- Dipakai oleh tim Business/Product untuk insight harga mobil bekas.

CREATE TABLE IF NOT EXISTS analytics_harga_per_merek (
    brand             TEXT NOT NULL,
    vehicle_age       INTEGER NOT NULL,
    rata_rata_harga   DOUBLE PRECISION NOT NULL,
    median_harga      DOUBLE PRECISION NOT NULL,
    jumlah_iklan      BIGINT NOT NULL,
    PRIMARY KEY (brand, vehicle_age)
);

-- Query agregasi (dijalankan oleh scripts/analytics.py):
-- TRUNCATE analytics_harga_per_merek;
-- INSERT INTO analytics_harga_per_merek
-- SELECT brand,
--        vehicle_age,
--        AVG(selling_price) AS rata_rata_harga,
--        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY selling_price) AS median_harga,
--        COUNT(*) AS jumlah_iklan
-- FROM raw_mobil
-- GROUP BY brand, vehicle_age;
