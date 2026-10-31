---
layout: referia
permalink: /04_grain/
# =============================================================================
# Dialogue analysis — 04 subject grain (steps 8–9)
# =============================================================================
#
# Copy of examples/subject_grain_uq/_referia.md, retargeted at shared info/.
# Seed fit is CIP-0015 subject_grain_seed_fit (replaces build_records.py Assess).
# Split / Confirm / Undo / Reset / Name already exist (subject_grain_*).
#
# Merge is NOT wired (deferred step 13). See backlog
# 2026-10-21_subject-grain-merge-wiring. Do not add a Merge button here.
#
# Stores
# ------
#   parameters  04_grain/parameters.yml         (σ², EM, n_exemplars, lens_weight)
#   input       info/codebook.parquet (VQ centroids; CIP-001A)
#   output      info/scores.yml       (R, planes, labels, cluster_ids)
# No named cache: seed fit writes output. Skip-if-R-present also requires
# R rows == codebook m (leftover phrase-level scores do not skip).
# Knobs must not land in cache or scores; Save writes parameters.yml.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — subject grain (lenses)"
description: >
  Assess codebook geometry, then Address named lenses. Fit lenses on
  the VQ codebook (cluster centroids), then Propose split / Confirm /
  Undo / Reset / Name. Merge is not wired.
date: 2026-10-22

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: 04_grain
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: parquet
  index: Name
  filename: codebook.parquet
  directory: info

output:
  type: yaml
  index: Name
  filename: scores.yml
  directory: info
  # Save writes *_modified / *_created; older scores.yml still has σ² knobs
  # that now live in 04_grain/parameters.yml. strict_columns would 503 on reload.
  strict_columns: false
  columns:
    - focus_topic
    - selected_phrase
    - topic_keys
    - topic_labels
    - topic_parent
    - topic_tree
    - responsibilities
    - uq_by_topic
    - uq_spec
    - pending_proposal
    - split_undo
    - notes
    - cluster_ids
    - vq_mass

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: Access the codebook, Assess its geometry with
      MPPCA splits, Address named lenses for Part A.

      **Access.** Data: `info/codebook.parquet` (VQ centroids from
      `03_vq`). Loaded as one grain row. Output is `info/scores.yml`
      (`R` responsibilities, planes, labels, `cluster_ids`).

      **Assess.** Seed fit is k=1. **Propose split** / Confirm / Undo
      / Reset explore how the codebook factors, without yet asking
      whether chatbot and workshop share themes. That exploration is
      reusable for any later lens reading.

      **Address.** **Name** and σ² soft assignment are the paper's
      cluster → thematic lens step, so `06_compare` can ask whether
      formats elicited similar distributions of issues. This page is
      MPPCA on the current codebook, not a replay of the frozen 10/11
      lenses.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of cluster → thematic lens grouping.
      Tweaks: `parameters.yml` (including σ²).

      > We used gpt-4.1-mini to generate a descriptive label for each
      > cluster, based on a sample of points from that cluster. The 40
      > clusters were then grouped into ten higher-level thematic
      > lenses using gpt-4.1-mini, using a soft assignment that allowed
      > each cluster to contribute to more than one lens. Relative
      > weights for each lens were controlled by the parameter σ².

      This page is MPPCA on the codebook (Name is the label step), not
      a replay of the frozen 10/11-lens map. Use **Name** so 06 tables
      are readable.

  - liquid: |
      ## Store status

      **Parameters** `{% if store_status.parameters.exists %}{{ store_status.parameters.path }}{% else %}absent — 04_grain/parameters.yml{% endif %}`

      **Input** `{% if store_status.input.exists %}{{ store_status.input.path }} · {{ store_status.input.size_human }}{% else %}absent — run 03_vq{% endif %}`

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}{% else %}absent — seed fit writes scores.yml{% endif %}`

  - liquid: |
      ## {{ Title | default: "Subject grain" }}

      Lenses on the **VQ codebook**, not the raw phrases. Each codebook
      cell is one geometric point (or a mass-weighted point — see Lens
      weights). The figure is the current focus topic in that geometry;
      click a point to pin a codebook phrase. Assess entry for MPPCA is
      **k=1**. **Propose split** grows the catalogue; **Confirm** seals
      or **Undo** restores. **Reset** returns to the single k=1 seed.
      **Name** writes labels. **Merge is not wired** (deferred step 13).

      This grain is the current MPPCA catalogue (recently **5 named
      topics** on **64 cells** unless you refit 03 at `n_vq: 40`). Do
      not treat these labels as the frozen `lens_of_cluster` map.

      <p><b>Topics:</b>
      {% for key in topic_keys %}{{ topic_labels[key] | default: key }}{% assign p = topic_parent[key] %}{% if p %}{% assign live_p = false %}{% for k2 in topic_keys %}{% if topic_labels[k2] == p %}{% assign live_p = true %}{% endif %}{% endfor %}{% if live_p %} ← {{ p }}{% endif %}{% endif %}{% unless forloop.last %}; {% endunless %}{% endfor %}
      </p>

      {% if pending_proposal and pending_proposal.kind == "split" %}
      <p class="status-ok"><b>Pending split:</b>
      {{ pending_proposal.parent }} → k={{ pending_proposal.k_before }}→{{ pending_proposal.k_after }},
      focus={{ pending_proposal.focus }}. Confirm or Undo.</p>
      {% endif %}

  - type: Dropdown
    field: focus_topic
    args:
      description: Focus topic
      options_field: topic_keys
      options_labels_field: topic_labels
      options: ["T0"]

  - type: PlotlyFigure
    field: uq_spec
    figure_source:
      map_field: uq_by_topic
      key_field: focus_topic
    "on":
      click_point:
        - set_field: selected_phrase
          from: customdata.phrase
    size:
      mode: container
      observe: true
      aspect_ratio: 4/3

  - type: Section
    title: MPPCA split
    visible_if:
      field: cluster_method
      equals: mppca
    entries:
      - type: PopulateButton
        field: _propose_split
        visible_if:
          field: pending_proposal
          not: true
        args:
          description: Propose split
          target: uq_spec
          compute:
            function: subject_grain_propose_split
            field:
              - uq_spec
              - uq_by_topic
              - topic_keys
              - responsibilities
              - focus_topic
              - topic_labels
              - topic_parent
              - topic_tree
              - pending_proposal
              - split_undo
            refresh: true
            row_args:
              embeddings: codebook_embeddings
              responsibilities: responsibilities
              phrases: codebook_phrases
              focus_topic: focus_topic
              sigma2: sigma2
              em_accept: em_accept
              topic_labels: topic_labels
              topic_parent: topic_parent
              label_model: label_model
              label_prompt: label_prompt
              n_exemplars: n_exemplars
              cluster_method: cluster_method

      - type: PopulateButton
        field: _confirm_split
        visible_if: pending_proposal
        args:
          description: Confirm split
          target: uq_spec
          compute:
            function: subject_grain_confirm_split
            field:
              - uq_spec
              - uq_by_topic
              - pending_proposal
              - split_undo
            refresh: true
            row_args:
              pending_proposal: pending_proposal

      - type: PopulateButton
        field: _undo_split
        visible_if: pending_proposal
        args:
          description: Undo split
          target: uq_spec
          compute:
            field:
              - uq_spec
              - uq_by_topic
              - topic_keys
              - responsibilities
              - focus_topic
              - topic_labels
              - topic_parent
              - topic_tree
              - pending_proposal
              - split_undo
            function: subject_grain_undo_split
            refresh: true
            row_args:
              split_undo: split_undo
              embeddings: codebook_embeddings
              phrases: codebook_phrases
              sigma2: sigma2

  - type: PopulateButton
    field: _fit_grain
    args:
      description: Fit grain (overwrites R)
      target: uq_spec
      compute:
        function: subject_grain_fit
        field:
          - responsibilities
          - uq_by_topic
          - uq_spec
          - topic_keys
          - topic_labels
          - topic_parent
          - topic_tree
          - focus_topic
        refresh: true
        row_args:
          embeddings: codebook_embeddings
          phrases: codebook_phrases
          cluster_method: cluster_method
          n_clusters: n_clusters
          sigma2: sigma2
          sigma2_mode: sigma2_mode
          em_accept: em_accept
          seed: seed
          kmeans_init: kmeans_init
          kmeans_n_init: kmeans_n_init
          kmeans_max_iter: kmeans_max_iter
          agglo_linkage: agglo_linkage
          agglo_metric: agglo_metric
          lens_weight: lens_weight
          vq_mass: vq_mass
        args:
          force_refit: true

  - type: PopulateButton
    field: _reset_grain
    args:
      description: Reset / refit
      target: uq_spec
      compute:
        function: subject_grain_reset
        field:
          - responsibilities
          - uq_by_topic
          - uq_spec
          - topic_keys
          - topic_labels
          - topic_parent
          - topic_tree
          - focus_topic
          - pending_proposal
          - split_undo
          - selected_phrase
        refresh: true
        row_args:
          embeddings: codebook_embeddings
          phrases: codebook_phrases
          cluster_method: cluster_method
          n_clusters: n_clusters
          sigma2: sigma2
          sigma2_mode: sigma2_mode
          em_accept: em_accept
          seed: seed
          kmeans_init: kmeans_init
          kmeans_n_init: kmeans_n_init
          kmeans_max_iter: kmeans_max_iter
          agglo_linkage: agglo_linkage
          agglo_metric: agglo_metric
          lens_weight: lens_weight
          vq_mass: vq_mass
        args:
          force_refit: true

review:
  # Step 7 — seed k=1 if scores are empty (CIP-0015). Field check, not a checkpoint.
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: subject_grain_fit
        field:
          - responsibilities
          - uq_by_topic
          - uq_spec
          - topic_keys
          - topic_labels
          - topic_parent
          - topic_tree
          - focus_topic
        refresh: true
        row_args:
          embeddings: codebook_embeddings
          phrases: codebook_phrases
          cluster_method: cluster_method
          n_clusters: n_clusters
          sigma2: sigma2
          sigma2_mode: sigma2_mode
          em_accept: em_accept
          seed: seed
          kmeans_init: kmeans_init
          kmeans_n_init: kmeans_n_init
          kmeans_max_iter: kmeans_max_iter
          agglo_linkage: agglo_linkage
          agglo_metric: agglo_metric
          lens_weight: lens_weight
          vq_mass: vq_mass
          responsibilities: responsibilities
          uq_by_topic: uq_by_topic
          uq_spec: uq_spec
          topic_keys: topic_keys
          topic_labels: topic_labels
          topic_parent: topic_parent
          topic_tree: topic_tree
          focus_topic: focus_topic
        args:
          k: 1
          force_refit: false
      - function: identity
        field: cluster_ids
        refresh: true
        row_args:
          input: cluster_ids
      - function: identity
        field: vq_mass
        refresh: true
        row_args:
          input: vq_mass
      - function: subject_grain_ensure_seed_names
        field:
          - topic_labels
          - topic_parent
          - topic_tree
        refresh: true
        row_args:
          phrases: codebook_phrases
          responsibilities: responsibilities
          focus_topic: focus_topic
          topic_labels: topic_labels
          topic_parent: topic_parent
          topic_keys: topic_keys
          label_prompt: label_prompt
          label_model: label_model
          n_exemplars: n_exemplars

  - type: Markdown
    field: selected_phrase
    liquid: |
      **Selected phrase**

      {{ selected_phrase }}

  - type: Section
    title: Lens weights
    entries:
      - type: Markdown
        liquid: |
          **Why two weights?** VQ already collapsed nearby phrases into
          cells. A lens can treat each cell as **one neighbourhood**
          (`uniform`, default) or pull toward **large cells** (`mass` =
          phrase count in the cell). Document histograms in 05 always
          recover phrase counts via `QR`, even when 04 used uniform.
          Agglomerative has no sample weights: mass + agglomerative
          errors. These knobs live in parameters.yml, not cache.
      - type: Dropdown
        field: lens_weight
        args:
          description: Lens geometry (uniform = each cluster one point; mass = weight by phrase count)
          options: ["uniform", "mass"]

  - type: Section
    title: Grain method
    entries:
      - type: Markdown
        liquid: |
          **Fit grain** overwrites responsibilities, labels, and figures.
          MPPCA seeds at k=1 then Propose. k-means and agglomerative use
          *Number of clusters*. Ward linkage requires Euclidean metric.
      - type: Dropdown
        field: cluster_method
        args:
          description: Grain method
          options: ["mppca", "kmeans", "agglomerative"]
      - type: BoundedIntText
        field: n_clusters
        args:
          description: Number of clusters (k-means / agglomerative; ignored by MPPCA seed)
          min: 1
          max: 40
      - type: Dropdown
        field: kmeans_init
        visible_if:
          field: cluster_method
          equals: kmeans
        args:
          description: k-means init
          options: ["k-means++", "random"]
      - type: BoundedIntText
        field: kmeans_n_init
        visible_if:
          field: cluster_method
          equals: kmeans
        args:
          description: k-means n_init
          min: 1
          max: 20
      - type: BoundedIntText
        field: kmeans_max_iter
        visible_if:
          field: cluster_method
          equals: kmeans
        args:
          description: k-means max iter
          min: 10
          max: 1000
      - type: Dropdown
        field: agglo_linkage
        visible_if:
          field: cluster_method
          equals: agglomerative
        args:
          description: Agglomerative linkage
          options: ["ward", "complete", "average", "single"]
      - type: Dropdown
        field: agglo_metric
        visible_if:
          field: cluster_method
          equals: agglomerative
        args:
          description: Agglomerative metric (ward requires euclidean)
          options: ["euclidean", "cosine"]

  - type: Section
    title: EM parameters
    visible_if:
      field: cluster_method
      equals: mppca
    entries:
      - type: Dropdown
        field: sigma2_mode
        args:
          description: σ² mode
          options: ["fixed", "profile"]
      - type: BoundedFloatText
        field: sigma2
        args:
          description: σ²
          min: 0.0001
          max: 2.0
          step: 0.01
      - type: BoundedIntText
        field: em_accept
        args:
          description: EM accept
          min: 1
          max: 50
      - type: BoundedIntText
        field: em_preview
        args:
          description: EM preview
          min: 0
          max: 50

  - type: Section
    title: LLM topic naming
    entries:
      - type: BoundedIntText
        field: n_exemplars
        args:
          description: Phrases used to name each topic
          min: 1
          max: 40
      - type: Textarea
        field: label_prompt
        args:
          description: Label prompt (must include <<PHRASES>>)
          rows: 6
      - type: Dropdown
        field: label_model
        args:
          description: Label model (stub = offline; Propose never calls an LLM)
          options: ["gpt-4.1-mini", "gpt-4o-mini", "stub"]

      - type: PopulateButton
        field: _name_focus_topic
        args:
          description: Name topics (focus + provisional)
          target: topic_labels
          compute:
            function: subject_grain_name_focus_topic
            field:
              - topic_labels
              - topic_parent
              - topic_tree
              - uq_spec
              - uq_by_topic
              - pending_proposal
            refresh: true
            row_args:
              phrases: codebook_phrases
              responsibilities: responsibilities
              focus_topic: focus_topic
              topic_labels: topic_labels
              topic_parent: topic_parent
              topic_keys: topic_keys
              label_prompt: label_prompt
              label_model: label_model
              n_exemplars: n_exemplars
              pending_proposal: pending_proposal
              uq_spec: uq_spec
              uq_by_topic: uq_by_topic

  - type: Markdown
    field: topic_tree
    liquid: |
      **Topics**

      {{ topic_tree }}

  - type: Textarea
    field: notes
    args:
      description: Assess notes
---

# AI dialogue formats — subject grain (lenses)

Assess codebook geometry, then Address named lenses. Fit lenses on the VQ codebook (cluster centroids), then Propose split / Confirm / Undo / Reset / Name. Merge is not wired.

## Access / Assess / Address

Nested loop: Access the codebook, Assess its geometry with
MPPCA splits, Address named lenses for Part A.

**Access.** Data: `info/codebook.parquet` (VQ centroids from
`03_vq`). Loaded as one grain row. Output is `info/scores.yml`
(`R` responsibilities, planes, labels, `cluster_ids`).

**Assess.** Seed fit is k=1. **Propose split** / Confirm / Undo
/ Reset explore how the codebook factors, without yet asking
whether chatbot and workshop share themes. That exploration is
reusable for any later lens reading.

**Address.** **Name** and σ² soft assignment are the paper's
cluster → thematic lens step, so `06_compare` can ask whether
formats elicited similar distributions of issues. This page is
MPPCA on the current codebook, not a replay of the frozen 10/11
lenses.

## Paper reconstruction

Independent reconstruction of cluster → thematic lens grouping.
Tweaks: `parameters.yml` (including σ²).

> We used gpt-4.1-mini to generate a descriptive label for each
> cluster, based on a sample of points from that cluster. The 40
> clusters were then grouped into ten higher-level thematic
> lenses using gpt-4.1-mini, using a soft assignment that allowed
> each cluster to contribute to more than one lens. Relative
> weights for each lens were controlled by the parameter σ².

This page is MPPCA on the codebook (Name is the label step), not
a replay of the frozen 10/11-lens map. Use **Name** so 06 tables
are readable.
