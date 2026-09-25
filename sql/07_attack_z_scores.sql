-- Which sensors diverge most during labeled attacks?
SELECT sensor,attack,COUNT(*) readings,ROUND(AVG(z_score),2) mean_abs_z,ROUND(QUANTILE_CONT(z_score,0.95),2) p95_abs_z FROM scores WHERE split='test' GROUP BY 1,2 ORDER BY 1,2;
