from __future__ import annotations
import argparse
import json
from pathlib import Path
from utils import fetch_eurostat

OUT_JSON = Path("data/raw/earn_ses22_49_2022_inspect.json")

parser = argparse.ArgumentParser()
parser.add_argument("--inspect-only", action="store_true", help="Pull broad cube metadata first")
args = parser.parse_args()

params = {"lang": "EN", "time": "2022"}
payload = fetch_eurostat("earn_ses22_49", params)
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(payload, indent=2))
print(f"saved {OUT_JSON}")
print("Next step: inspect dimensions and total codes before narrowing filters.")
