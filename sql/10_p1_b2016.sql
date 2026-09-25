-- How does P1_B2016 shift between normal and attack test periods?
SELECT attack,COUNT(*) samples,ROUND(AVG(P1_B2016),3) mean_value,ROUND(STDDEV_POP(P1_B2016),3) sd_value,ROUND(MIN(P1_B2016),3) min_value,ROUND(MAX(P1_B2016),3) max_value FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
