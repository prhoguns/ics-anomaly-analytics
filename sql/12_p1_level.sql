-- How does P1 level change during labeled attacks?
SELECT attack,COUNT(*) samples,ROUND(AVG(P1_LIT01),2) mean_level,ROUND(QUANTILE_CONT(P1_LIT01,0.05),2) p05,ROUND(QUANTILE_CONT(P1_LIT01,0.95),2) p95 FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
