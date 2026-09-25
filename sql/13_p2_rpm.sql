-- How does P2 turbine RPM change during labeled attacks?
SELECT attack,COUNT(*) samples,ROUND(AVG(P2_CO_rpm),2) mean_rpm,ROUND(QUANTILE_CONT(P2_CO_rpm,0.05),2) p05,ROUND(QUANTILE_CONT(P2_CO_rpm,0.95),2) p95 FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
