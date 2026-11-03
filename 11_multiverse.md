---
layout: referia
permalink: /11_multiverse/
# =============================================================================
# Dialogue analysis — 11 analysis-choice product (CIP-001E / CIP-0023)
# =============================================================================
#
# Methodology of the 1080-config table on **main-run 07 codes**.
# Axes: experience definition × weighting × exclusion × quote threshold ×
# round. Not 1080 populate-all LLM jobs.
#
# CIP-0023: pipeline DAG + axis checkboxes. Phase 1 executes aggregate
# paper axes only; refit/llm ticks are shown on the graph but refused.
#
# Waiting: own-words coding variants (format-blind recode). k=25/60 is a
# refit of 03_vq → 04_grain → 06_compare, not this page.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — analysis-choice robustness"
description: >
  Address analysis-choice product. Paper reconstruction of the Bell et
  al. 2022 multiverse: experience gap across definition, weighting,
  exclusion, quote threshold, and round, on main-run 07 codes (216
  configs). Not 1080 LLM jobs.
date: 2026-10-30
seq: 110

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: _data/11_multiverse
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: constants.yml
  directory: _data/corpus
  index: index
  select: dialogue-v1

output:
  type: yaml
  filename: analysis_multiverse.yml
  directory: _data/corpus
  index: index
  strict_columns: false
  columns:
    - multiverse_summary
    - multiverse_md
    - n_configs
    - pipeline_dag
    - stage_params_md
    - store_status

viewer:
  - liquid: |
      ## Access / Assess / Address

      This stage is **Address** of robustness. Access is the main-run
      07 store.

      **Access.** Data: `_data/corpus/grounds.yml` (main-run 07 codes) and the
      packed corpus fields those codes join. Writes
      `_data/corpus/analysis_multiverse.yml`. One coding source; 216 configs,
      not 1080 LLM jobs.

      **Assess.** None on the raw transcripts. Varying definition,
      weighting, exclusion, quote threshold, and round is the Address
      product, not a quality pass. Own-words recode (the missing axis
      to 1080) waits on another store.

      **Address.** Does the experience gap remain across analysis
      choices? Paper story: the finding remains across all multiverse
      configurations. Cluster-count 25/60 and extra lens runs are a
      03→04→06 refit, not this page.

  - liquid: |
      ## Pipeline (CIP-0023)

      Graph of the reconstruction as done (`_data/corpus/pipeline.yml`).
      Nodes are stages; edges are stores. Expand a stage via
      **focus_stage** to see declared parameters and cost classes
      (`aggregate` / `refit` / `llm` / `display`). Phase 1 **Run** only
      products the five paper **aggregate** axes below — ticking a
      whole refit/LLM stage is recorded on the graph for later, not
      executed here.

  - type: PlotlyFigure
    field: pipeline_dag
    size:
      mode: container
      observe: true
      aspect_ratio: 16/9

  - liquid: |
      ### Focused stage parameters

      {{ stage_params_md }}
    watch:
      - stage_params_md
      - focus_stage

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the analysis-choice product.
      Tweaks: `parameters.yml` axis checkboxes. **This is the remaining
      paper experiment that has not been run on this corpus.**

      > We used multiverse analysis (Bell et al., 2022) to test how
      > the findings changed under different analytical choices,
      > exploring 1080 different analytical specifications. These
      > varied the coding source, the definition of experience, the
      > weighting of contributions, exclusion rules, quote-matching
      > thresholds, and dialogue timing.

      Paper story: “This finding remains across all multiverse
      configurations.”

      This page is that product on **main-run 07 codes** (definition ×
      weighting × exclusion × threshold × round = 216 when all five
      axis boxes are on). The coding-source axis that takes 216 to
      1080 waits on a recode store. It is not 1080 LLM jobs.
      Cluster-count 25/60 and extra lens runs are a 03→04→06 refit,
      not this page.

  - liquid: |
      ## Multiverse results

      {% if multiverse_md %}
      {{ multiverse_md }}
      {% else %}
      No product yet. Tick axes, **Run analysis-choice product**, then **Save**.
      {% endif %}
    watch:
      - multiverse_md

  - liquid: |
      ## Store status

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}{% else %}absent — Run the product to write analysis_multiverse.yml{% endif %}`

  - liquid: |
      ## Analysis-choice product

      One corpus row. Same axes as the 1080-config table, with **one
      coding** (main-run 07). Canonical: personal+others, document-equal
      weights, no exclusion, quote_support ≥ 0.8, pooled rounds.
      Untick an axis to hold that dimension at its canonical level.

      **Waiting on another stage:** own-words coding variants. To vary
      codebook size (k=25/60) or lens grain, refit `03_vq` then
      `04_grain` then `06_compare` — that is a second reading of Part A,
      not 1080 configs (CIP-0023 Phase 2).

      No populate-all over configurations.

  - type: PopulateButton
    field: _run_multiverse
    args:
      description: Run analysis-choice product
      target: multiverse_md
      compute: &mv_compute
        function: run_analysis_multiverse
        field:
          - multiverse_summary
          - multiverse_md
          - n_configs
        refresh: true
        row_args:
          n_jsd_shuffles: n_jsd_shuffles
          seed: seed
          axis_definitions: axis_definitions
          axis_weightings: axis_weightings
          axis_exclusions: axis_exclusions
          axis_thresholds: axis_thresholds
          axis_rounds: axis_rounds

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: pipeline_dag_figure
        field: pipeline_dag
        refresh: true
      - function: pipeline_stage_params_md
        field: stage_params_md
        refresh: true
        row_args:
          focus_stage: focus_stage

  - type: Text
    field: focus_stage
    args:
      description: Focus stage id (e.g. 07_part_b, 03_vq, 11_multiverse)

  - type: Checkbox
    field: axis_definitions
    args:
      description: Vary experience definition (personal / +others / +professional)

  - type: Checkbox
    field: axis_weightings
    args:
      description: Vary weighting (document-equal vs point-equal)

  - type: Checkbox
    field: axis_exclusions
    args:
      description: Vary exclusion rules

  - type: Checkbox
    field: axis_thresholds
    args:
      description: Vary quote-support thresholds (0.8 / 0.9 / 0.95)

  - type: Checkbox
    field: axis_rounds
    args:
      description: Vary dialogue round (pooled / autumn / spring)

  - type: BoundedIntText
    field: n_jsd_shuffles
    args:
      description: Chance-level agenda JSD shuffles (0 to skip)
      min: 0
      max: 5000

  - type: BoundedIntText
    field: seed
    args:
      description: RNG seed
      min: 0
      max: 999999

  - type: Markdown
    field: multiverse_md
    liquid: |
      {{ multiverse_md }}

  - type: SaveButton
---

# AI dialogue formats — analysis-choice robustness

Address analysis-choice product. Paper reconstruction of the Bell et al. 2022 multiverse: experience gap across definition, weighting, exclusion, quote threshold, and round, on main-run 07 codes (216 configs). Not 1080 LLM jobs.

## Access / Assess / Address

This stage is **Address** of robustness. Access is the main-run
07 store.

**Access.** Data: `_data/corpus/grounds.yml` (main-run 07 codes) and the
packed corpus fields those codes join. Writes
`_data/corpus/analysis_multiverse.yml`. One coding source; 216 configs,
not 1080 LLM jobs.

**Assess.** None on the raw transcripts. Varying definition,
weighting, exclusion, quote threshold, and round is the Address
product, not a quality pass. Own-words recode (the missing axis
to 1080) waits on another store.

**Address.** Does the experience gap remain across analysis
choices? Paper story: the finding remains across all multiverse
configurations. Cluster-count 25/60 and extra lens runs are a
03→04→06 refit, not this page.

## Paper reconstruction

Independent reconstruction of the analysis-choice product.
Tweaks: `parameters.yml`. **This is the remaining paper
experiment that has not been run on this corpus.**

> We used multiverse analysis (Bell et al., 2022) to test how
> the findings changed under different analytical choices,
> exploring 1080 different analytical specifications. These
> varied the coding source, the definition of experience, the
> weighting of contributions, exclusion rules, quote-matching
> thresholds, and dialogue timing.

Paper story: “This finding remains across all multiverse
configurations.”

This page is that product on **main-run 07 codes** (definition ×
weighting × exclusion × threshold × round = 216). The coding-
source axis that takes 216 to 1080 waits on a recode store. It
is not 1080 LLM jobs. Cluster-count 25/60 and extra lens runs
are a 03→04→06 refit, not this page.
