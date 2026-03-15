from __future__ import annotations
import requests
import pandas as pd
from pathlib import Path

EUROSTAT_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
ESCO_BASE = "https://ec.europa.eu/esco/api"


def fetch_eurostat(dataset_code: str, params: dict, timeout: int = 90) -> dict:
    url = f"{EUROSTAT_BASE}/{dataset_code}"
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()


def save_json(payload: dict, path: str | Path) -> None:
    Path(path).write_text(pd.io.json.dumps(payload, indent=2))


def ensure_parent(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
