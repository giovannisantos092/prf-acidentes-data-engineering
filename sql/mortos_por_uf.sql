SELECT
    uf,
    SUM(mortos) AS total_mortos
FROM acidentes
GROUP BY uf
ORDER BY total_mortos DESC;