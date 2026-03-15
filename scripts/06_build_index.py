from __future__ import annotations
from pathlib import Path
import pandas as pd

scores_file = Path("data/processed/task_scores.csv")
out_file = Path("data/processed/eu_ai_exposure_index.csv")

if not scores_file.exists():
    raise SystemExit("run 05_score_tasks.py first")

scores = pd.read_csv(scores_file)
if "score_0_10" not in scores.columns:
    raise SystemExit("task_scores.csv missing score_0_10")

scores["weight"] = scores["task_type"].map({"essential": 2, "optional": 1}).fillna(1)
scored = scores.dropna(subset=["score_0_10"]).copy()
if scored.empty:
    print("No scored tasks yet. Writing empty shell.")
    pd.DataFrame(columns=["isco_code", "occupation_name", "ai_exposure_score_0_10"]).to_csv(out_file, index=False)
else:
    grp = scored.groupby(["isco_code", "occupation_name"], as_index=False).apply(
        lambda g: pd.Series({"ai_exposure_score_0_10": (g["score_0_10"] * g["weight"]).sum() / g["weight"].sum()})
    ).reset_index(drop=True)
    grp.to_csv(out_file, index=False)
print(f"saved {out_file}")
