-- What are normal operating ranges for selected sensors?
SELECT sensor,ROUND(mean_value,2) normal_mean,ROUND(sd_value,2) normal_sd,ROUND(p01,2) p01,ROUND(p99,2) p99 FROM baseline ORDER BY sensor;
