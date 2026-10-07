SELECT
    ano,
    COUNT(*) AS total_acidentes
FROM acidentes
GROUP BY ano
ORDER BY ano;