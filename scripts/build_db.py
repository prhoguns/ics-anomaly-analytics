from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / 'data/raw'
if not (raw/'train1.csv.gz').exists() or not (raw/'test1.csv.gz').exists():
    raise SystemExit('Run python scripts/download.py first.')
db = ROOT / 'data/analytics.duckdb'
con = duckdb.connect(str(db))
con.execute('CREATE OR REPLACE TABLE readings AS SELECT *, \'train\' AS split FROM read_csv_auto(?)', [str(raw/'train1.csv.gz')])
con.execute('INSERT INTO readings SELECT *, \'test\' AS split FROM read_csv_auto(?)', [str(raw/'test1.csv.gz')])
con.execute('''CREATE OR REPLACE TABLE sensor_values AS
 SELECT time, split, attack, attack_P1, attack_P2, attack_P3,
 sensor, reading FROM readings
 UNPIVOT (reading FOR sensor IN (P1_B2016,P1_FT01,P1_LIT01,P2_CO_rpm,
 P2_SIT01,P3_PIT01,P4_ST_PT01,P4_ST_TT01))''')
con.execute('''CREATE OR REPLACE TABLE baseline AS SELECT sensor,
 AVG(reading) mean_value, STDDEV_POP(reading) sd_value,
 QUANTILE_CONT(reading,0.01) p01, QUANTILE_CONT(reading,0.99) p99
 FROM sensor_values WHERE split='train' AND attack=0 GROUP BY sensor''')
con.execute('''CREATE OR REPLACE VIEW scores AS SELECT v.*,
 ABS(v.reading-b.mean_value)/NULLIF(b.sd_value,0) z_score,
 v.reading < b.p01 OR v.reading > b.p99 outside_training_98pct
 FROM sensor_values v JOIN baseline b USING(sensor)''')
print(con.execute("SELECT split,COUNT(*),SUM(attack) FROM readings GROUP BY 1 ORDER BY 1").fetchall())
assert con.execute("SELECT SUM(attack) FROM readings WHERE split='test'").fetchone()[0] > 0
con.close()
