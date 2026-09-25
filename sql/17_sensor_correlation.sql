-- Do selected subsystem signals move together in normal and attack periods?
SELECT attack,COUNT(*) samples,ROUND(CORR(P1_FT01,P1_LIT01),3) p1_flow_level_corr,ROUND(CORR(P2_CO_rpm,P2_SIT01),3) p2_rpm_sensor_corr,ROUND(CORR(P4_ST_PT01,P4_ST_TT01),3) p4_pressure_temp_corr FROM readings WHERE split='test' GROUP BY 1 ORDER BY 1;
