-- Which plant subsystems carry labeled attack intervals?
SELECT 'P1' subsystem,SUM(attack_P1) attack_seconds FROM readings WHERE split='test' UNION ALL SELECT 'P2',SUM(attack_P2) FROM readings WHERE split='test' UNION ALL SELECT 'P3',SUM(attack_P3) FROM readings WHERE split='test';
