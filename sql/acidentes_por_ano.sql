SELECT
    YEAR(data_inversa) AS ano,
    COUNT(*) AS acidentes
FROM acidentes
GROUP BY ano
ORDER BY ano;