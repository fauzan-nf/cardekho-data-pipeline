-- =====================================================================
-- Query insight untuk tim Business & Product
-- Dijalankan terhadap tabel analytics_harga_per_merek dan raw_mobil
-- =====================================================================

-- Q1: Top 10 merek dengan rata-rata harga tertinggi (semua umur kendaraan)
-- Tujuan: mengidentifikasi segmen premium di pasar mobil bekas
SELECT brand,
       ROUND(AVG(rata_rata_harga)::numeric, 0) AS rata_rata_harga_merek,
       SUM(jumlah_iklan)                        AS total_iklan
FROM analytics_harga_per_merek
GROUP BY brand
ORDER BY rata_rata_harga_merek DESC
LIMIT 10;

-- Q2: Tren depresiasi harga berdasarkan kelompok umur kendaraan
-- Tujuan: melihat seberapa cepat harga turun seiring umur
SELECT CASE
           WHEN vehicle_age <= 3  THEN '0-3 tahun'
           WHEN vehicle_age <= 6  THEN '4-6 tahun'
           WHEN vehicle_age <= 10 THEN '7-10 tahun'
           ELSE '>10 tahun'
       END AS kelompok_umur,
       COUNT(*)                                AS jumlah_iklan,
       ROUND(AVG(selling_price)::numeric, 0)  AS rata_rata_harga,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY selling_price)::numeric, 0) AS median_harga
FROM raw_mobil
GROUP BY kelompok_umur
ORDER BY MIN(vehicle_age);

-- Q3: Distribusi iklan berdasarkan bahan bakar x transmisi
-- Tujuan: insight preferensi pasar untuk tim Product
SELECT fuel_type,
       transmission_type,
       COUNT(*) AS jumlah_iklan,
       ROUND(AVG(selling_price)::numeric, 0) AS rata_rata_harga
FROM raw_mobil
GROUP BY fuel_type, transmission_type
ORDER BY jumlah_iklan DESC;

-- Q4: Merek dengan median harga tertinggi di segmen mobil muda (umur 3-5 tahun)
-- Tujuan: insight untuk tim Business soal positioning merek di segmen populer
SELECT brand,
       ROUND(AVG(median_harga)::numeric, 0) AS median_harga_segmen_muda,
       SUM(jumlah_iklan)                    AS total_iklan
FROM analytics_harga_per_merek
WHERE vehicle_age BETWEEN 3 AND 5
GROUP BY brand
HAVING SUM(jumlah_iklan) >= 50
ORDER BY median_harga_segmen_muda DESC
LIMIT 10;
