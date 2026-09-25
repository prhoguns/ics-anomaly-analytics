-- How does P2_SIT01 change during labeled attacks?
SELECT attack,COUNT(*) samples,ROUND(AVG(P2_SIT01),2) mean_value,ROUND(QUANTILE_CONT(P2_SIT01,0.05),2) p05,ROUND(QUANTILE_CONT(P2_SIT01,0.95),2) p95 FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
