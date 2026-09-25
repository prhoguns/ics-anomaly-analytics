-- When is attack activity concentrated?
SELECT DATE_TRUNC('hour',time) hour_start,COUNT(*) samples,SUM(attack) attack_seconds,ROUND(100.0*AVG(attack),2) attack_pct FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
