---
layout: referia
permalink: /07_part_b/
# =============================================================================
# Dialogue analysis — 07 Part B shares (CIP-001E)
# =============================================================================
#
# Document-weighted basis mix and experience / professional gaps by format.
# Paper Table 2 analogue on the *current* grounds.yml from 07_grounds.
# Coding stays on 07; this stage only aggregates.
#
# Stores
# ------
#   parameters  _data/07_part_b/parameters.yml
#   input       _data/corpus/records.parquet  (one packed corpus row)
#   output      _data/corpus/part_b.yml
# Wrapper reads _data/corpus/grounds.yml (basis, format, doc_id).
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — Part B shares"
description: >
  Address Part B headlines. Document-weighted basis mix by format and
  the experience / professional gaps, with cluster-bootstrap intervals.
  Same estimator as the package 04_part_b tables on this study's
  grounds.yml — not a replay of Jess's 17.7 vs 4.1 extract grain.
date: 2026-11-02
seq: 75

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: _data/07_part_b
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: parquet
  filename: records.parquet
  directory: _data/corpus
  index: Name

output:
  type: yaml
  filename: part_b.yml
  directory: _data/corpus
  index: Name
  strict_columns: false
  columns:
    - basis_mix
    - experience_gap
    - basis_mix_md
    - experience_gap_md
    - n_docs
    - store_status

viewer:
  - liquid: |
      ## Access / Assess / Address

      This stage is **Address** of the Part B share question. Coding
      stays on `07_grounds`; this page only aggregates.

      **Access.** Data: `_data/corpus/grounds.yml` — one row per
      extracted point with `basis`, `format`, `doc_id` (and ids),
      reached via the packed corpus row. Writes
      `_data/corpus/part_b.yml`.

      **Assess.** No new quality screen here. The codes are taken as
      given from 07. Bootstrap intervals are part of the *estimator*,
      not a check on classification quality. `min_gap` only flags
      “clear” differences after the CI is formed.

      **Address.** Were workshop points more often grounded in
      experience than chatbot points? Paper story: workshop experience
      17.7% vs chatbot 4.1% (document-weighted). This table is the same
      estimator on *this* study's extract grain — do not overwrite the
      published figure without saying so.

  - liquid: |
      ## Method

      **Where classification happens.** Not on this page. On
      `07_grounds`, `llm_classify_grounds` (gpt-4.1-mini by default)
      assigns each extracted point to exactly one of seven evidential
      bases: `personal_experience`, `others_experience`,
      `professional_knowledge`, `principle`, `public_example`,
      `project_materials`, `unclear`. Save on 07 explodes those labels
      into `grounds.yml`. This stage only *reads* those labels.

      **Unit of analysis.** The extract point is the coding unit; the
      **document** (`doc_id`) is the sampling unit. Long documents with
      many points do not dominate short ones.

      **Document-weighted share.** For each document, build a
      histogram over its points' basis codes and normalise to a
      composition (sums to 1). The format mean is the unweighted mean
      of those document compositions. Reported figures are percentages
      (×100). Empty / missing basis strings are dropped from the
      histogram.

      **Experience and professional measures.** From the same
      per-point labels we also build two binary compositions
      (overrides in `parameters.yml`):
      - **experience** — point in
        `personal_experience` ∪ `others_experience`;
      - **professional** — point equals `professional_knowledge`.
      Each document’s share is the fraction of its points in that
      set. Format means and gaps use the same document-average as B1.

      **Cluster bootstrap.** Resample **documents with replacement**
      within each format (`n_boot` replicates, default 2000; `seed`
      default 42). Each replicate recomputes the document-mean
      composition; the interval is the 2.5% / 97.5% percentiles of
      those replicate means. We do **not** resample individual
      points inside a document — that would understate dependence
      among points from the same speaker / session.

      **Workshop − chatbot (w−c).** With two formats, difference =
      workshop mean − chatbot mean (group names sorted
      alphabetically: chatbot, then workshop). The CI for the
      difference is the percentile interval of
      (workshop bootstrap mean − chatbot bootstrap mean) on paired
      replicate draws. A row is **clear** when that CI excludes zero
      *and* `|w−c| ≥ min_gap` (default 3 percentage points).

      **What this is not.** Not a re-classification of quotes. Not a
      phrase-level or token-level bootstrap. Not Jess’s frozen extract
      grain — rerunning 07 on a different extract changes the table
      even if the estimator is unchanged.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of Part B Table 2 / experience gap.
      Tweaks: `parameters.yml`. Coding is upstream on `07_grounds`.

      > We classified the basis of each extracted point (personal
      > experience, others’ experience, professional knowledge,
      > principle, …). Document-weighted shares by format, with
      > cluster-bootstrap intervals over documents.

      Paper headline this table is for: workshop experience 17.7% vs
      chatbot 4.1%. Run Classify all + Save on 07 first, then Compute
      here.

  - liquid: |
      ## Store status

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}{% else %}absent — Compute shares to write part_b.yml{% endif %}`

  - liquid: |
      ## Part B — what each point rests on

      B1 is the seven-way basis mix; the gap table collapses to
      experience vs professional as above. One corpus row; Save writes
      `part_b.yml`. No extra API.

  - type: PopulateButton
    field: _run_part_b
    args:
      description: Compute Part B shares
      target: experience_gap_md
      compute: &part_b_compute
        function: run_basis_share_compare
        field:
          - basis_mix
          - experience_gap
          - basis_mix_md
          - experience_gap_md
          - n_docs
        refresh: true
        row_args:
          n_boot: n_boot
          seed: seed
          min_gap: min_gap
          experience_bases: experience_bases
          professional_basis: professional_basis

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: run_basis_share_compare
        field:
          - basis_mix
          - experience_gap
          - basis_mix_md
          - experience_gap_md
          - n_docs
        refresh: true
        row_args:
          n_boot: n_boot
          seed: seed
          min_gap: min_gap
          experience_bases: experience_bases
          professional_basis: professional_basis

  - type: BoundedIntText
    field: n_boot
    args:
      description: Bootstrap replicates
      min: 50
      max: 5000

  - type: BoundedFloatText
    field: min_gap
    args:
      description: Clear-difference floor (percentage points)
      min: 0
      max: 20
      step: 0.5

  - type: Markdown
    field: experience_gap_md
    liquid: |
      ## Compare to Jess / paper Table 2

      The first table below is the headline: **this grain** vs
      **Jess 17.7 / 4.1**. Read that before the detail rows.

      {{ experience_gap_md }}

  - type: Markdown
    field: basis_mix_md
    liquid: |
      ## Basis mix (document-weighted %)

      Seven-way composition. Experience in the headline =
      `personal_experience` + `others_experience` shares here.

      {{ basis_mix_md }}
---

# AI dialogue formats — Part B shares

Address Part B headlines. Document-weighted basis mix by format and the experience / professional gaps, with cluster-bootstrap intervals. Same estimator as the package 04_part_b tables on this study's grounds.yml — not a replay of Jess's 17.7 vs 4.1 extract grain.

## Access / Assess / Address

This stage is **Address** of the Part B share question. Coding
stays on `07_grounds`; this page only aggregates.

**Access.** Data: `_data/corpus/grounds.yml` — one row per
extracted point with `basis`, `format`, `doc_id`, reached via the
packed corpus row. Writes `_data/corpus/part_b.yml`.

**Assess.** No new quality screen. Codes are taken from 07.
Bootstrap intervals are the estimator, not a check on
classification. `min_gap` only flags “clear” differences after the
CI is formed.

**Address.** Were workshop points more often grounded in
experience than chatbot points? Paper story: workshop experience
17.7% vs chatbot 4.1% (document-weighted). This table is the same
estimator on *this* study's extract grain — do not overwrite the
published figure without saying so.

## Method

**Where classification happens.** Not here. On `07_grounds`,
`llm_classify_grounds` assigns each extract point to one of seven
evidential bases. Save explodes `grounds.yml`. This stage only
reads those labels.

**Unit of analysis.** Point = coding unit; **document** (`doc_id`) =
sampling unit. Documents are equal weight.

**Document-weighted share.** Per document: histogram of basis codes
among its points, normalised to a composition. Format mean =
unweighted mean of those compositions (reported as %).

**Experience / professional.** Experience = personal + others
(configurable); professional = `professional_knowledge` alone.
Same document-average estimator as the seven-way mix.

**Cluster bootstrap.** Resample documents with replacement within
format (`n_boot`, `seed`). Percentile CI of document-mean shares.
Not a point-level bootstrap. Difference = workshop − chatbot;
**clear** when the difference CI excludes 0 and `|w−c| ≥ min_gap`.

## Paper reconstruction

Independent reconstruction of Part B Table 2 / experience gap.
Tweaks: `parameters.yml`. Coding is upstream on `07_grounds`.

> We classified the basis of each extracted point (personal
> experience, others’ experience, professional knowledge,
> principle, …). Document-weighted shares by format, with
> cluster-bootstrap intervals over documents.

Paper headline this table is for: workshop experience 17.7% vs
chatbot 4.1%. Run Classify all + Save on 07 first, then Compute
here.
