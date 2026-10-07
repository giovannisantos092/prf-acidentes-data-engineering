SELECT
    tipo_acidente,
    COUNT(*) AS total_acidentes
FROM acidentes
GROUP BY tipo_acidente
ORDER BY total_acidentes DESC;