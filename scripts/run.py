from pathlib import Path
import duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / 'data/analytics.duckdb'), read_only=True)
out = ROOT / 'results'
charts = ROOT / 'charts'
out.mkdir(exist_ok=True)
charts.mkdir(exist_ok=True)

def markdown(df):
    cols = [str(c) for c in df.columns]
    rows = [['' if v is None else str(round(v, 4) if isinstance(v, float) else v) for v in row]
            for row in df.itertuples(index=False, name=None)]
    return '| ' + ' | '.join(cols) + ' |\n| ' + ' | '.join(['---']*len(cols)) + ' |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)

for file in sorted((ROOT / 'sql').glob('*.sql')):
    sql = file.read_text()
    title = sql.splitlines()[0].removeprefix('-- ').strip()
    df = con.execute(sql).df()
    df.to_csv(out / f'{file.stem}.csv', index=False)
    (out / f'{file.stem}.md').write_text(f'# {title}\n\n{markdown(df.head(30))}')
    print(file.name, len(df), 'rows')

episodes = con.execute((ROOT / 'sql/02_attack_episodes.sql').read_text()).df()
fig, ax = plt.subplots(figsize=(10,4))
for _, row in episodes.iterrows():
    ax.axvspan(row['start_time'], row['end_time'], color='#dc2626', alpha=.45)
ax.set(title='Labeled attack intervals in test1', xlabel='Time', yticks=[])
fig.autofmt_xdate();fig.tight_layout();fig.savefig(charts/'attack_intervals.png',dpi=160);plt.close(fig)

tradeoff = con.execute((ROOT/'sql/09_threshold_tradeoff.sql').read_text()).df()
fig, ax = plt.subplots(figsize=(9,4.5))
ax.plot(tradeoff['threshold'], tradeoff['recall_pct'], marker='o',label='Attack seconds found')
ax.plot(tradeoff['threshold'], tradeoff['alert_precision_pct'],marker='s',label='Alert precision')
ax.set(title='Simple sensor deviation thresholds',xlabel='Maximum absolute z-score threshold',ylabel='Percent')
ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(charts/'threshold_tradeoff.png',dpi=160);plt.close(fig)
