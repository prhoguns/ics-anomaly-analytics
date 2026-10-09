"""Write small synthetic train1/test1 files to data/raw/ for CI.

Only the columns the build uses (time, the eight analysed sensors, attack labels), at one reading
per second like HAI 21.03. The test file has two attack episodes that push sensors off their
training range. It checks that every query runs; it says nothing about the real data.
"""
import csv
import gzip
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
SENSORS = {'P1_B2016': 1.6, 'P1_FT01': 176.0, 'P1_LIT01': 402.7, 'P2_CO_rpm': 54116.0,
           'P2_SIT01': 790.0, 'P3_PIT01': 2880.0, 'P4_ST_PT01': 10.0, 'P4_ST_TT01': 27000.0}
COLS = ['time', *SENSORS, 'attack', 'attack_P1', 'attack_P2', 'attack_P3']
EPISODES = [(900, 1200, 'P1'), (2500, 2700, 'P3')]  # (start s, end s, attacked process)

random.seed(11)
RAW.mkdir(parents=True, exist_ok=True)
for name, start, with_attacks in (('train1', datetime(2020, 7, 7, 15), False), ('test1', datetime(2020, 7, 9, 15), True)):
    with gzip.open(RAW / f'{name}.csv.gz', 'wt', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for s in range(4000):
            ep = next((p for a, b, p in EPISODES if with_attacks and a <= s < b), None)
            row = [(start + timedelta(seconds=s)).strftime('%Y-%m-%d %H:%M:%S')]
            for sensor, mean in SENSORS.items():
                value = random.gauss(mean, abs(mean) * 0.01)
                if ep and sensor.startswith(ep):
                    value += abs(mean) * 0.2  # the attacked process drifts well outside training
                row.append(round(value, 5))
            row += [int(ep is not None)] + [int(ep == p) for p in ('P1', 'P2', 'P3')]
            w.writerow(row)
print(f'fixture: train1/test1 in {RAW}')
