-- Are timestamps, labels, or selected sensor values missing?
SELECT split,COUNT(*) samples,COUNT(*)-COUNT(DISTINCT time) duplicate_timestamps,COUNT(*) FILTER (WHERE attack IS NULL) missing_labels,COUNT(*) FILTER (WHERE P1_FT01 IS NULL OR P2_CO_rpm IS NULL OR P3_PIT01 IS NULL OR P4_ST_PT01 IS NULL) missing_selected_sensor_values FROM readings GROUP BY 1 ORDER BY 1;
