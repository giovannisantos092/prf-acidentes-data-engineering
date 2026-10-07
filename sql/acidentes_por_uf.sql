SELECT
    uf,
    COUNT(*) AS total_acidentes
FROM acidentes
GROUP BY uf
ORDER BY total_acidentes DESC;