SELECT
    classificacao_acidente,
    COUNT(*) AS acidentes
FROM acidentes
GROUP BY classificacao_acidente
ORDER BY acidentes DESC;