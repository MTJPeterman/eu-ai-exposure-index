from __future__ import annotations
from pathlib import Path
import pandas as pd

INFILE = Path("data/processed/isco_esco_crosswalk.csv")
OUT = Path("data/processed/task_proxies.csv")

if not INFILE.exists():
    raise SystemExit("run 03_build_esco_crosswalk.py first")

crosswalk = pd.read_csv(INFILE)
rows = []
for _, r in crosswalk.iterrows():
    rows.append({
        "isco_code": r["isco_code"],
        "occupation_name": r["occupation_name"],
        "task_proxy": "TODO generate from ESCO skills",
        "task_type": "essential",
        "source_item": "TODO",
    })

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"saved {OUT}")
