# EU AI Exposure Index — Execution Pack

This pack is a reproducible blueprint for building a Eurostat-based AI Exposure Index for Europe.

## Objective

Build an occupation-level exposure index using:

- Eurostat employment by occupation
- Eurostat earnings by occupation
- ESCO occupations, skills, and knowledge items
- LLM-based task exposure scoring

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

1. Eurostat employment by detailed occupation (ISCO-08 two digit level), dataset `lfsa_egai2d`
2. Eurostat mean annual earnings by sex, occupation and economic activity (2022), dataset `earn_ses22_49`
3. ESCO occupation and skills APIs
4. OpenAI paper "GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models"

## Recommended version 1 scope

- Geography: EU27_2020
- Occupation level: ISCO-08 2-digit
- Earnings: total, all sexes, all economic activities where available
- Scoring model: current frontier LLM
- Scoring repetitions: 3 runs per task proxy, use median

## Workflow

### Step 1 — Pull Eurostat employment
Use `lfsa_egai2d` and filter for:
- geo = EU27_2020
- sex = T
- unit = THS_PER or suitable headcount unit
- age = Y15-74 or TOTAL, depending on coverage
- time = latest available year

Output:
- `isco_code`
- `occupation_name`
- `employment_eu`

### Step 2 — Pull Eurostat earnings
Use `earn_ses22_49` and filter for:
- geo = EU27_2020 where available, otherwise country-level rollup
- sex = T
- indic = mean annual earnings
- economic activity = B-S_X_O or total if available
- occupation = ISCO categories aligned to step 1
- time = 2022

Output:
- `isco_code`
- `mean_annual_earnings_eur`

### Step 3 — Build ISCO ↔ ESCO crosswalk
Map each Eurostat ISCO occupation to one or more ESCO occupation IDs.

Rules:
- one-to-many mapping allowed
- record confidence
- note ambiguous mappings explicitly

Output:
- `isco_code`
- `occupation_name`
- `esco_uri`
- `esco_label`
- `mapping_confidence`
- `mapping_notes`

### Step 4 — Extract ESCO work content
For each ESCO occupation, pull:
- essential skills
- optional skills
- knowledge items
- description

Output raw tables:
- `ESCO_Occupations`
- `ESCO_Skills`

### Step 5 — Convert ESCO items into task proxies
Turn each skill or knowledge item into concrete work statements.

Examples:
- "prepare financial reports"
- "reconcile accounting records"
- "explain treatment plans to patients"
- "repair electrical wiring on site"

Target:
- 20 to 60 task proxies per occupation where possible

### Step 6 — Score each task proxy
Use a strict 0–10 exposure rubric.

#### Exposure rubric
- 0–1: essentially not feasible for current LLMs without physical execution or embodied perception
- 2–4: limited assistance on documentation, lookup, summarization, scheduling, or admin
- 5–7: substantial acceleration of meaningful parts of the task
- 8–10: primarily language-based, screen-based, codified, analytical, or software-mediated work

Also return:
- confidence
- bottleneck type
- modality
- rationale

### Step 7 — Aggregate to occupation score
Default weights:
- essential task proxy = 2
- optional task proxy = 1

Use median score if each task is scored multiple times.

### Step 8 — Merge employment and earnings
Create final occupation table with:
- employment
- earnings
- exposure score
- wage mass
- exposed wage mass

### Step 9 — Produce outputs
Recommended outputs:
- Top 20 most exposed occupations
- Top 20 least exposed occupations
- Average exposure across EU jobs
- Share of jobs scoring 7+
- Wage mass in high exposure occupations

## Validation

Minimum validation:
1. Human spot-check top 30 and bottom 30 occupations
2. Compare directional ranking against US exposure studies
3. Review all occupations with low mapping confidence manually

## Limitations

- ESCO is a competence framework, not a direct task-frequency database like O*NET
- Eurostat ↔ ESCO mapping is the weakest link
- Exposure is technical feasibility, not legal adoption or employment displacement
- Earnings dataset may require country aggregation if EU total is not consistently available

## Deliverables in this pack

- `eu_ai_exposure_index_template.xlsx`
- `eu_ai_exposure_pipeline_stub.py`
- `eu_ai_exposure_scoring_prompt.txt`
- `eu_ai_exposure_methodology.md`



## GitHub release note

This repository is meant to keep the method transparent and reproducible. Version outputs in `output/` are examples and should not be treated as the final paper-grade estimate until the direct SES occupation earnings cube is fully integrated.
