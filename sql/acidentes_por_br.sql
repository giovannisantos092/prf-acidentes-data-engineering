SELECT
    br,
    COUNT(*) AS acidentes
FROM acidentes
GROUP BY br
ORDER BY acidentes DESC;