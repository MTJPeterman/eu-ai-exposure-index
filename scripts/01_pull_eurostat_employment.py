from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from utils import fetch_eurostat

OUT_JSON = Path("data/raw/lfsa_egai2d_eu27_2024.json")
OUT_CSV = Path("data/processed/eurostat_employment_eu27_2024.csv")

params = {
    "lang": "EN",
    "geo": "EU27_2020",
    "sex": "T",
    "time": "2024",
    "unit": "THS_PER",
}

payload = fetch_eurostat("lfsa_egai2d", params)
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(payload, indent=2))

# Eurostat JSON-stat cubes need custom parsing. This script stores the raw pull and a minimal flat view.
values = payload.get("value", {})
rows = [{"obs_key": k, "value": v} for k, v in values.items()]
df = pd.DataFrame(rows)
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)
print(f"saved {OUT_JSON}")
print(f"saved {OUT_CSV}")
