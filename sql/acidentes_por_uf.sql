SELECT
    uf,
    COUNT(*) AS acidentes
FROM acidentes
GROUP BY uf
ORDER BY acidentes DESC;