---
# =============================================================================
# Dialogue analysis — 05 document distance (steps 10–12)
# =============================================================================
#
# CIP-0016: run_document_distance_analysis. Reads packed corpus + grain scores from
# shared ../info/. Writes P, EMD, MDS, tests, and Plotly specs to
# document_distance.yml. Click bindings write selected_doc to output.
# Knobs (group_field, min_mass, n_perm, seed) live in ./parameters.yml, not cache.
#
# Requires optional extra referia[distance] (pot) for EMD.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — lens share by format"
description: >
  Access of document × lens histograms `P`, then extra Assess geometry
  (EMD / MDS / tests). Not the paper's Address (that is JSD in
  06_compare). See ../GAP.md.
date: 2026-10-29

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: .
  filename: parameters.yml
  index: index
  select: dialogue-v1

# Packed corpus row (phrases, embeddings, doc_ids) from 02_embed.
input:
  type: parquet
  filename: records.parquet
  directory: ../info
  index: Name

# Grain catalogue — named store, not a sidecar. Joined on the corpus Name.
# Key is "data" (lynguine input type). referia forbids both "scores" and "output".
data:
  type: yaml
  filename: scores.yml
  directory: ../info
  index: Name

# Do not use a ``documents:`` store here. That key is reserved for
# generate-document actions (Create docx / Create yaml). Group labels
# already sit on the packed corpus row (``groups`` from 02_embed).

output:
  type: yaml
  filename: document_distance.yml
  directory: ../info
  index: Name
  columns:
    - P
    - topic_means
    - doc_mass
    - doc_ids_kept
    - ground_cost
    - emd_matrix
    - mds_coords
    - mds_explained
    - permanova
    - permdisp
    - axis_correlates
    - distance_tests_md
    - mds_spec
    - topic_document_heatmap_spec
    - emd_heatmap_spec
    - axis_correlate_bars_spec
    - chapter_lens_radar_spec
    - ground_cost_heatmap_spec
    - selected_doc
    - store_status
  strict_columns: false

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: Access document histograms, Assess extra geometry
      on `P`. The paper's Address of format similarity is `06_compare`.

      **Access.** Data: `info/records.parquet` (packed phrases) joined
      to `info/scores.yml` (grain). Each document becomes a histogram
      over current lenses (`P`, phrase-level `QR` summed and
      normalised). Thin documents (below **min mass**) are dropped.
      Writes `info/document_distance.yml`.

      **Assess.** EMD, classical MDS, PERMANOVA / PERMDISP, and the
      radar / heatmaps are extra geometry on the same `P`. They
      characterise how documents sit on the topic simplex. They are
      not Jensen–Shannon divergence.

      **Address.** Not an experiment in the paper. Do not hand this
      page back as the published comparison. The elicitation question
      on these shares is `06_compare`.

  - liquid: |
      ## Paper reconstruction

      This stage is **not** an experiment in the paper. The paper
      compares formats with Jensen–Shannon divergence on document-equal
      lens shares (`06_compare`). Tweaks still live in `parameters.yml`.

      > To assess the overall similarity of the thematic distributions,
      > we calculated Jensen–Shannon divergence and compared the
      > observed value with a distribution obtained by randomly
      > reassigning format labels to documents.

      EMD / MDS here is extra geometry on the same `P`. Do not hand
      this page back as the published comparison.

  - liquid: |
      ## Store status

      **Output** `{{ store_status.output.path }}`
      {% if store_status.output.exists %}
      in use · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}
      {% else %}
      absent — Compute histograms to write `document_distance.yml`.
      {% endif %}

  - liquid: |
      ## Lens share by format

      This stage asks which **lenses** from 04_grain are working in which
      **format** — chatbot conversations versus workshop transcripts.
      Each document is a histogram over the current lenses: we sum
      phrase-level membership (`QR` when 04 ran on a VQ codebook) and
      normalise so the shares sum to one (output column `P`). Documents
      with fewer phrases than **min mass** are dropped.

      The paper's Part A headline is document-weighted lens shares and
      Jensen–Shannon divergence on those shares, not EMD. Use this stage
      as a geometry on the same `P`; do not treat EMD as the published
      comparison (see `../GAP.md`).

      Pairwise distance is Earth Mover's Distance on those histograms.
      Classical
      [multidimensional scaling](https://en.wikipedia.org/wiki/Multidimensional_scaling)
      then draws a 2-D map whose Euclidean distances approximate EMD.
      Colour on the scatter is **format** (packed `group`). Click a
      point to pin that document.

      {% if selected_doc %}
      <p><b>Selected document:</b> {{ selected_doc }}</p>
      {% endif %}

      ## Earth Mover's Distance

      [Earth Mover's Distance](https://en.wikipedia.org/wiki/Earth_mover%27s_distance)
      (EMD) is the least work needed to reshape one pile of mass into
      another. Rubner, Tomasi, and Guibas used the earth-moving metaphor
      for comparing histograms; on a discrete ground space the same
      quantity is the
      [1-Wasserstein metric](https://en.wikipedia.org/wiki/Wasserstein_metric).

      Here each document is a pile whose bins are **topics**. Moving a
      unit of mass from topic *i* to topic *j* costs the
      [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity)
      between those topics' mean embeddings (one minus the cosine of
      L2-normalised means; the diagonal of that cost is zero). Two
      documents that put their mass on nearby topics are close even if
      they do not share the same leading topic. Two documents concentrated
      on distant topics are far. The implementation is POT `ot.emd2`.

      EMD is not Euclidean distance in embedding space, and it is not
      topic overlap counted as a set. It is transport cost on the topic
      simplex, with the topic-mean cosine as the ground metric.
    collapse:
      headings:
        - Earth Mover's Distance
      default: open

  - type: PopulateButton
    field: _run_distance
    args:
      description: Compute histograms, EMD, MDS, tests
      target: mds_spec
      compute:
        function: run_document_distance_analysis
        field:
          - P
          - topic_means
          - doc_mass
          - doc_ids_kept
          - ground_cost
          - emd_matrix
          - mds_coords
          - mds_explained
          - permanova
          - permdisp
          - axis_correlates
          - distance_tests_md
          - mds_spec
          - topic_document_heatmap_spec
          - emd_heatmap_spec
          - axis_correlate_bars_spec
          - chapter_lens_radar_spec
          - ground_cost_heatmap_spec
        refresh: true
        row_args:
          embeddings: embeddings
          doc_ids: doc_ids
          responsibilities: responsibilities
          topic_labels: topic_labels
          groups: groups
          group_field: group_field
          min_mass: min_mass
          n_perm: n_perm
          seed: seed
        args:
          n_components: 2

  - type: Section
    title: Lens share by format
    entries:
      - liquid: |
          Rows are documents (workshop filenames, or chatbot
          `round::{participant_id}` conversations). Columns are lenses
          from grain. Cell
          colour is that document's share of phrase mass on that lens (a
          row of `P`). A row concentrated on one column is a document
          dominated by one lens. A mixed row is a document whose phrases
          spread across lenses. Columns (lenses) are leaf-ordered by the
          same ground cost EMD uses: average-linkage clustering of
          topic-mean cosine distances, then Bar-Joseph so semantically
          nearby lenses sit next to each other. Rows are leaf-ordered by
          pairwise EMD under that cost. Both axes may then be reversed so
          high-mass cells tend toward the diagonal. Adjacent rows therefore
          mean small transport cost, not similar Pearson share profiles.

      - type: PlotlyFigure
        field: topic_document_heatmap_spec
        size:
          mode: container
          observe: true
          aspect_ratio: 16/9

  - type: Section
    title: Pairwise EMD
    entries:
      - liquid: |
          Cell *(i, j)* is the Earth Mover's Distance between those two
          documents. Blue is small distance (cheap to turn one histogram
          into the other); red is large. The diagonal is zero. Both axes
          use the Bar-Joseph leaf order of this same matrix, so the
          lowest-distance documents sit next to each other and the blue
          cells concentrate on the diagonal. That is the clustering.
          MDS below is a 2-D drawing of this matrix; the tests permute
          these distances.

      - type: PlotlyFigure
        field: emd_heatmap_spec
        size:
          mode: container
          observe: true
          aspect_ratio: 1

  - type: Section
    title: Pairwise ground cost
    entries:
      - liquid: |
          Cell *(i, j)* is the cosine distance between those two lenses'
          mean embeddings — the ground metric EMD uses when it moves mass
          from one lens to the other. Blue is small distance (cheap to move
          mass between those lenses); red is large. The diagonal is zero.
          Both axes use the Bar-Joseph leaf order of this same matrix, so
          the lowest-distance lenses sit next to each other and the blue
          cells concentrate on the diagonal. That is the clustering.

      - type: PlotlyFigure
        field: ground_cost_heatmap_spec
        size:
          mode: container
          observe: true
          aspect_ratio: 1

  - type: Section
    title: Radar
    entries:
      - liquid: |
          The same shares as the heatmap, one polar trace per document. A
          document that sits on one spoke is using one lens; a fuller
          polygon is using several.

      - type: PlotlyFigure
        field: chapter_lens_radar_spec
        size:
          mode: container
          observe: true
          aspect_ratio: 1

  - type: Section
    title: Document MDS
    entries:
      - liquid: |
          Each marker is one document that passed **min mass**. Axes MDS1
          and MDS2 are the leading coordinates of classical MDS (Torgerson /
          principal coordinates) of the EMD matrix — they are **not** lens
          axes. Nearby markers have small EMD; distant markers have large
          EMD. Colour is the selected group field (format). Click a marker
          to set `selected_doc`.

      - type: PlotlyFigure
        field: mds_spec
        "on":
          click_point:
            - set_field: selected_doc
              from: customdata.doc
        size:
          mode: container
          observe: true
          aspect_ratio: 4/3

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: run_document_distance_analysis
        field:
          - P
          - topic_means
          - doc_mass
          - doc_ids_kept
          - ground_cost
          - emd_matrix
          - mds_coords
          - mds_explained
          - permanova
          - permdisp
          - axis_correlates
          - distance_tests_md
          - mds_spec
          - topic_document_heatmap_spec
          - emd_heatmap_spec
          - axis_correlate_bars_spec
          - chapter_lens_radar_spec
          - ground_cost_heatmap_spec
        refresh: true
        row_args:
          embeddings: embeddings
          doc_ids: doc_ids
          responsibilities: responsibilities
          topic_labels: topic_labels
          groups: groups
          group_field: group_field
          min_mass: min_mass
          n_perm: n_perm
          seed: seed
        args:
          n_components: 2

  - type: Dropdown
    field: group_field
    args:
      description: Colour MDS by packed format (group)
      options:
        - group

  - type: BoundedIntText
    field: min_mass
    args:
      description: Min phrase mass per document
      min: 1
      max: 10000

  - type: BoundedIntText
    field: n_perm
    args:
      description: Permutation count
      min: 99
      max: 9999

  - type: BoundedIntText
    field: seed
    args:
      description: RNG seed
      min: 0
      max: 999999

  - type: Markdown
    field: distance_tests_md
    liquid: |
      **Permutation tests**

      [PERMANOVA](https://en.wikipedia.org/wiki/Permutational_analysis_of_variance)
      asks whether among-group EMD is larger than you get by shuffling
      group labels. Report the pseudo-F, R² (share of squared distance
      associated with groups), and a permutation p-value. A small p-value
      says group **location** differs in the EMD geometry.

      PERMDISP (Anderson, 2006; no dedicated Wikipedia page) asks whether
      groups differ in **spread**: mean distance to the group centroid in
      the MDS space of the same EMD matrix. If PERMANOVA is significant
      and PERMDISP is also, location and dispersion may be confounded —
      groups can look different because one is more scattered, not because
      its typical document sits elsewhere.

      {{ distance_tests_md }}

  - type: Markdown
    field: selected_doc
    liquid: |
      **Selected document**

      `{{ selected_doc }}`. Click a marker on the MDS scatter to pin a
      document, then read its row on the share heatmap, its cell on the
      pairwise EMD heatmap, the lens distances on the ground-cost
      heatmap, and its spoke on the radar.

  - type: HTML
    args:
      value: >
        <p class="chrome-hint"><strong>Axis correlates.</strong> Pearson
        correlation between each MDS coordinate and each topic's document
        shares. A large positive r means documents that load on that topic
        sit toward the positive end of that MDS axis. Use this to
        <em>read</em> the scatter; it is not a causal claim, and it is
        not a loading from a factor model of the phrases.</p>

  - type: PlotlyFigure
    field: axis_correlate_bars_spec
    size:
      mode: container
      observe: true
      aspect_ratio: 16/9
---

# AI dialogue formats — lens share by format

Access of document × lens histograms `P`, then extra Assess geometry (EMD / MDS / tests). Not the paper's Address (that is JSD in 06_compare). See ../GAP.md.

## Access / Assess / Address

Nested loop: Access document histograms, Assess extra geometry
on `P`. The paper's Address of format similarity is `06_compare`.

**Access.** Data: `info/records.parquet` (packed phrases) joined
to `info/scores.yml` (grain). Each document becomes a histogram
over current lenses (`P`, phrase-level `QR` summed and
normalised). Thin documents (below **min mass**) are dropped.
Writes `info/document_distance.yml`.

**Assess.** EMD, classical MDS, PERMANOVA / PERMDISP, and the
radar / heatmaps are extra geometry on the same `P`. They
characterise how documents sit on the topic simplex. They are
not Jensen–Shannon divergence.

**Address.** Not an experiment in the paper. Do not hand this
page back as the published comparison. The elicitation question
on these shares is `06_compare`.

## Paper reconstruction

This stage is **not** an experiment in the paper. The paper
compares formats with Jensen–Shannon divergence on document-equal
lens shares (`06_compare`). Tweaks still live in `parameters.yml`.

> To assess the overall similarity of the thematic distributions,
> we calculated Jensen–Shannon divergence and compared the
> observed value with a distribution obtained by randomly
> reassigning format labels to documents.

EMD / MDS here is extra geometry on the same `P`. Do not hand
this page back as the published comparison.
