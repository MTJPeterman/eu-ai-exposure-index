from __future__ import annotations
from pathlib import Path
import pandas as pd

OUT = Path("data/processed/isco_esco_crosswalk.csv")

# Seed file. Replace with actual mapped rows.
seed = [
    {"isco_code": "11", "occupation_name": "Chief executives, senior officials and legislators", "esco_uri": "", "esco_label": "", "mapping_confidence": "pending", "mapping_notes": "add manual mapping"},
    {"isco_code": "21", "occupation_name": "Science and engineering professionals", "esco_uri": "", "esco_label": "", "mapping_confidence": "pending", "mapping_notes": "add manual mapping"},
]

df = pd.DataFrame(seed)
OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"saved {OUT}")
