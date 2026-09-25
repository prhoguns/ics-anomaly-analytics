-- How does P4 pressure change during labeled attacks?
SELECT attack,COUNT(*) samples,ROUND(AVG(P4_ST_PT01),2) mean_value,ROUND(QUANTILE_CONT(P4_ST_PT01,0.05),2) p05,ROUND(QUANTILE_CONT(P4_ST_PT01,0.95),2) p95 FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
