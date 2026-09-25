-- How often do readings fall outside training 1st–99th percentiles?
SELECT sensor,split,attack,COUNT(*) readings,ROUND(100.0*AVG(outside_training_98pct::INT),2) outside_pct FROM scores GROUP BY 1,2,3 ORDER BY 1,2,3;
