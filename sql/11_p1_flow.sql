-- How does P1 flow change during labeled attacks?
SELECT attack,COUNT(*) samples,ROUND(AVG(P1_FT01),2) mean_flow,ROUND(QUANTILE_CONT(P1_FT01,0.05),2) p05,ROUND(QUANTILE_CONT(P1_FT01,0.95),2) p95 FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
