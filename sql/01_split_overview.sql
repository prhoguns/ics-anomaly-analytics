-- How much normal and attack data is in each split?
SELECT split, COUNT(*) sample_seconds, SUM(attack) attack_seconds, ROUND(100.0*AVG(attack),2) attack_pct FROM readings GROUP BY 1 ORDER BY 1;
