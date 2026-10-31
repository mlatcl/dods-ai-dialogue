---
# =============================================================================
# Dialogue analysis — 06 Part A tables (CIP-001E)
# =============================================================================
#
# Document-weighted type mix, lens shares, bootstrap CIs, and JSD.
# Paper Table 1 / Figure 1 analogue on the *current* 04_grain catalogue.
# 05_distance is extra EMD geometry on the same P; do not treat EMD as JSD.
#
# Stores
# ------
#   parameters  ./parameters.yml
#   input       ../info/records.parquet
#   data        ../info/scores.yml
#   output      ../info/part_a.yml
# Wrapper also reads codebook.parquet (cluster_ids) and phrases.yml (kinds).
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — Part A shares and JSD"
description: >
  Address Part A. Document-weighted concern/benefit/condition mix and
  lens shares by format, with cluster-bootstrap intervals and
  Jensen–Shannon divergence. This is the paper's Part A estimator on
  the current grain, not a replay of Jess's frozen k=40 labels.
date: 2026-10-29

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: .
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: parquet
  filename: records.parquet
  directory: ../info
  index: Name

data:
  type: yaml
  filename: scores.yml
  directory: ../info
  index: Name

output:
  type: yaml
  filename: part_a.yml
  directory: ../info
  index: Name
  strict_columns: false
  columns:
    - type_mix
    - lens_mix
    - jsd
    - type_mix_md
    - lens_mix_md
    - jsd_md
    - n_docs
    - store_status

viewer:
  - liquid: |
      ## Access / Assess / Address

      This stage is **Address** of the Part A question. Access is a
      join of stores already assessed upstream.

      **Access.** Data: `info/records.parquet` (phrases, `doc_ids`,
      kinds) joined to `info/scores.yml` (lens responsibilities).
      Writes `info/part_a.yml` (type mix, lens mix, JSD).

      **Assess.** Documents with fewer phrases than **min mass** are
      dropped (too thin to be a histogram). Intervals resample
      documents; that is the estimator, not a quality pass on the
      raw files.

      **Address.** Did the two formats elicit similar distributions of
      issues and conditions? Document-equal CBC mix and lens shares,
      with JSD versus shuffled format labels. Paper story: broadly
      similar agendas (reported JSD 0.006; CBC 37.3/36.4/26.3 chatbot
      vs 36.7/36.2/27.1 workshop). This grain is 04's current lenses,
      not the frozen 11-lens map.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the Part A comparison. Tweaks:
      `parameters.yml`.

      > We compared the prevalence of themes between the two formats by
      > calculating the share of points assigned to each lens with each
      > document. Each document was given equal weight, with
      > differences calculated as workshop minus chatbot proportions.
      > We estimated 95% confidence intervals using 2,000 bootstrap
      > resamples of documents. To assess the overall similarity of the
      > thematic distributions, we calculated Jensen–Shannon divergence
      > and compared the observed value with a distribution obtained by
      > randomly reassigning format labels to documents.

      Paper story this table is for: “Different dialogue modes produced
      broadly similar substantive agendas.” Reported JSD = 0.006;
      concerns / benefits / conditions 37.3/36.4/26.3 chatbot vs
      36.7/36.2/27.1 workshop.

  - liquid: |
      ## Store status

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}{% else %}absent — Compute shares to write part_a.yml{% endif %}`

  - liquid: |
      ## Part A — what each format draws out

      Each **document** (chatbot conversation `round::{participant_id}`,
      or workshop filename) is a histogram. We average those histograms
      within format (D5). Intervals resample documents. **JSD** is base 2
      on the two mean lens profiles.

      This grain is 04's current lenses (five MPPCA topics on a 64-cell
      codebook unless you refit VQ at 40). Jess's published JSD 0.006 is
      on 11 k-means lenses. Do not overwrite that figure with this one
      without saying so.

      **What you should see** after Compute (or the page precompute):
      a JSD in bits, then two markdown tables — CBC type mix (~37/36/26
      on Jess's run; this grain was closer to even thirds) and lens mix
      by format with bootstrap intervals. One corpus row; Save writes
      `part_a.yml`. No extra API.

  - type: PopulateButton
    field: _run_compare
    args:
      description: Compute shares and JSD
      target: jsd_md
      compute: &compare_compute
        function: run_format_share_compare
        field:
          - type_mix
          - lens_mix
          - jsd
          - type_mix_md
          - lens_mix_md
          - jsd_md
          - n_docs
        refresh: true
        row_args:
          doc_ids: doc_ids
          groups: groups
          responsibilities: responsibilities
          topic_labels: topic_labels
          min_mass: min_mass
          n_boot: n_boot
          seed: seed
          min_gap: min_gap

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: run_format_share_compare
        field:
          - type_mix
          - lens_mix
          - jsd
          - type_mix_md
          - lens_mix_md
          - jsd_md
          - n_docs
        refresh: true
        row_args:
          doc_ids: doc_ids
          groups: groups
          responsibilities: responsibilities
          topic_labels: topic_labels
          min_mass: min_mass
          n_boot: n_boot
          seed: seed
          min_gap: min_gap

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
    field: jsd_md
    liquid: |
      {{ jsd_md }}

  - type: Markdown
    field: type_mix_md
    liquid: |
      **Type mix (document-weighted %)**

      {{ type_mix_md }}

  - type: Markdown
    field: lens_mix_md
    liquid: |
      **Lens mix (document-weighted %)**

      {{ lens_mix_md }}
---

# AI dialogue formats — Part A shares and JSD

Address Part A. Document-weighted concern/benefit/condition mix and lens shares by format, with cluster-bootstrap intervals and Jensen–Shannon divergence. This is the paper's Part A estimator on the current grain, not a replay of Jess's frozen k=40 labels.

## Access / Assess / Address

This stage is **Address** of the Part A question. Access is a
join of stores already assessed upstream.

**Access.** Data: `info/records.parquet` (phrases, `doc_ids`,
kinds) joined to `info/scores.yml` (lens responsibilities).
Writes `info/part_a.yml` (type mix, lens mix, JSD).

**Assess.** Documents with fewer phrases than **min mass** are
dropped (too thin to be a histogram). Intervals resample
documents; that is the estimator, not a quality pass on the
raw files.

**Address.** Did the two formats elicit similar distributions of
issues and conditions? Document-equal CBC mix and lens shares,
with JSD versus shuffled format labels. Paper story: broadly
similar agendas (reported JSD 0.006; CBC 37.3/36.4/26.3 chatbot
vs 36.7/36.2/27.1 workshop). This grain is 04's current lenses,
not the frozen 11-lens map.

## Paper reconstruction

Independent reconstruction of the Part A comparison. Tweaks:
`parameters.yml`.

> We compared the prevalence of themes between the two formats by
> calculating the share of points assigned to each lens with each
> document. Each document was given equal weight, with
> differences calculated as workshop minus chatbot proportions.
> We estimated 95% confidence intervals using 2,000 bootstrap
> resamples of documents. To assess the overall similarity of the
> thematic distributions, we calculated Jensen–Shannon divergence
> and compared the observed value with a distribution obtained by
> randomly reassigning format labels to documents.

Paper story this table is for: “Different dialogue modes produced
broadly similar substantive agendas.” Reported JSD = 0.006;
concerns / benefits / conditions 37.3/36.4/26.3 chatbot vs
36.7/36.2/27.1 workshop.
