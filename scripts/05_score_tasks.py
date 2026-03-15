from __future__ import annotations
from pathlib import Path
import pandas as pd

INFILE = Path("data/processed/task_proxies.csv")
OUT = Path("data/processed/task_scores.csv")

if not INFILE.exists():
    raise SystemExit("run 04_generate_task_proxies.py first")

df = pd.read_csv(INFILE)
# Placeholder scoring sheet for manual or API fill.
df["score_0_10"] = None
df["confidence"] = None
df["bottleneck_type"] = None
df["modality"] = None
df["rationale"] = None
df.to_csv(OUT, index=False)
print(f"saved {OUT}")
