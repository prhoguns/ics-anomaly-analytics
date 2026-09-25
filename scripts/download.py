from pathlib import Path
from urllib.request import urlretrieve

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / 'data/raw'
raw.mkdir(parents=True, exist_ok=True)
for filename in ('train1.csv.gz', 'test1.csv.gz'):
    url = f'https://raw.githubusercontent.com/icsdataset/hai/master/hai-21.03/{filename}'
    target = raw / filename
    if not target.exists():
        urlretrieve(url, target)
    print(f'{target.name}: {target.stat().st_size:,} bytes')
