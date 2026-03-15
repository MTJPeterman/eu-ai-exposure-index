# EU AI Exposure Index

A reproducible research repo for estimating AI exposure across the European labour market using:

- Eurostat employment by occupation
- Eurostat earnings by occupation
- ESCO occupations, skills, and knowledge items
- task-level LLM exposure scoring

This repo is built to produce a Europe version of the popular US-style AI exposure chart, but with a methodology that is explicit, versioned, and reproducible.

## Current status

This repository already includes:

- an exact Eurostat employment layer for EU27 2024 from `lfsa_egai2d`
- a working 2-digit ISCO pipeline structure
- a scoring rubric and LLM prompt
- sample charts and workbook outputs
- a country-anchored and SES-anchored wage approach

What is still deliberately marked as pending:

- full direct pull of the 2022 Eurostat SES occupation earnings cube (`earn_ses22_49`) across all EU countries
- final row-by-row ISCO ↔ ESCO mapping at 2-digit coverage
- full task proxy generation and scoring for every occupation

## Repository structure

```text
.
├── README.md
├── methodology.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/
│   └── processed/
├── scoring/
│   ├── ai_scoring_prompt.txt
│   └── task_generation_prompt.txt
├── scripts/
│   ├── 01_pull_eurostat_employment.py
│   ├── 02_pull_eurostat_earnings.py
│   ├── 03_build_esco_crosswalk.py
│   ├── 04_generate_task_proxies.py
│   ├── 05_score_tasks.py
│   ├── 06_build_index.py
│   └── utils.py
├── output/
│   ├── eu_ai_exposure_index_v4_ses_anchored.xlsx
│   ├── charts/
│   │   └── eu_ai_exposure_index_v4_ses_anchored.png
│   └── sample_outputs.md
├── paper/
│   └── ai_exposure_eu_workforce.md
└── .github/
    └── workflows/
        └── validate.yml
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/01_pull_eurostat_employment.py
python scripts/02_pull_eurostat_earnings.py --inspect-only
python scripts/03_build_esco_crosswalk.py
python scripts/04_generate_task_proxies.py
python scripts/05_score_tasks.py
python scripts/06_build_index.py
```

## Core formula

For occupation `o`:

`Exposure_o = SUM(score_t * weight_t) / SUM(weight_t)`

Where:

- `t` = task proxy derived from ESCO
- `score_t` = AI exposure score from 0 to 10
- `weight_t` = essential task weight (default 2) or optional task weight (default 1)

Then:

`Exposed wage mass_o = employment_o * mean_annual_earnings_o * exposure_o / 10`

## Official data sources

- Eurostat employment by detailed occupation: `lfsa_egai2d`
- Eurostat Structure of Earnings Survey: `earn_ses22_49`
- ESCO occupations and skills API
- OpenAI paper: “GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models”

## What to publish from this repo

The three outputs that matter:

1. Top 20 most exposed EU occupations
2. Top 20 least exposed EU occupations
3. Exposed wage mass across the EU economy

## Recommended GitHub settings

- repository visibility: public
- enable Issues
- enable Discussions only if you want outside researchers to contribute mappings
- create a release tagged `v0.1-mvp` after first upload
- upload large raw files only if needed; otherwise keep raw pulls out of git and document the download path
