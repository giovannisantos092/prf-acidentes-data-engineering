SELECT
    causa_acidente,
    COUNT(*) AS total_acidentes
FROM acidentes
GROUP BY causa_acidente
ORDER BY total_acidentes DESC
LIMIT 10;