-- Which test seconds have the largest sensor deviation?
SELECT time,MAX(attack) attack,ROUND(MAX(z_score),2) max_abs_z,MAX_BY(sensor,z_score) leading_sensor FROM scores WHERE split='test' GROUP BY time ORDER BY max_abs_z DESC LIMIT 30;
