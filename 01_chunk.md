---
layout: referia
permalink: /01_chunk/
# =============================================================================
# Dialogue analysis — 01 catalog, segment, explode (steps 1–3)
# =============================================================================
#
# Aspirational until lynguine CIP-0013 (document_segment, In Progress) and
# CIP-0014 (output.explode, file_catalog) land. Compute names are the spec.
#
# Stores
# ------
#   parameters    01_chunk/parameters.yml           (writable unitisation knobs)
#   input         info/documents.yml      (step 1; hand-written roster)
#   cache         01_chunk/_chunk_cache.yml.gz      (optional units list; deletable
#                                            once chunks.yml exists — segment
#                                            is local, not an LLM call)
#   output        info/chunks.yml         (.yml.gz when the corpus is large)
#
# No checkpoints/. Do not keep units in cache *and* full text in output as
# the long-term pair; gzip if you do persist both (lynguine CIP-0015).
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — catalog, segment, explode"
description: >
  Access (+ Assess grain). Catalog Recollective chatbot dumps and workshop
  DOCX, segment with docx_chatbot.v1 / docx_workshop.v1 (aspect
  dialogue_units), then explode to one chunk row per unit. Serve this
  config on its own; 02_embed reads info/chunks.yml.
date: 2026-10-29

display:
  layout: inline_list
  detail_field: units

parameters:
  type: yaml
  directory: 01_chunk
  filename: parameters.yml
  index: index
  select: dialogue-v1

# Step 1 — roster. Optional file_catalog (CIP-0014) can draft this from files.
input:
  type: yaml
  filename: documents.yml
  directory: info
  index: Name

# Step 2 — list-in-one-field on the document row (CIP-0013 contract).
cache:
  type: yaml
  filename: _chunk_cache.yml.gz
  directory: 01_chunk
  index: Name
  compress: gzip
  strict_columns: false
  columns:
    - units
    - store_status

# Step 3 — tall chunk table. Explode is Access IO, not an in-memory frame.
output:
  type: yaml
  filename: chunks.yml
  directory: info
  index: unit_id
  # Inherit + document_segment extras sit on the exploded YAML; v2 default
  # strict_columns would 503 this config on reload.
  strict_columns: false
  explode:
    field: units
    inherit:
      - Name
      - filename
      - reader
      - strategy
      - year
      - technology
      - format
      - group
      - round
      - session_type
      - facilitator
  columns:
    - unit_id
    - text
    - chunk_index
    - word_count
    - chunking_method
    - doc_id
    - Name
    - filename
    - reader
    - strategy
    - year
    - technology
    - format
    - group
    - round
    - session_type
    - facilitator
    - participant_id
    - extract_text
    - context
    - n_fac_lines
    - segment_strategy
    - aspect
    - was_truncated
    - source_path
    - segmentation
    - text_layer
    - recogniser_score
    - recogniser_rationale

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: **Access** of the files, then a short **Assess** of
      grain and coverage. This page does not Address the elicitation
      question.

      **Access.** Data: Recollective chatbot DOCX and workshop DOCX
      under `files/`, rostered in `info/documents.yml` (one row per
      file). Each file is segmented into a `units` list on that row,
      then exploded to `info/chunks.yml` (one row per unit: `unit_id`,
      `text`, `word_count`, `format`, `doc_id`, `participant_id`, …).

      **Assess.** Units shorter than four words are dropped (too little
      text for any later question). Two Recollective dumps pack many
      conversations into two files; chatbot `doc_id` is stamped
      `{round}::{participant_id}` so later document-equal weights do
      not treat two dumps as two documents. A good run is **2013**
      units (1003 chatbot, 1010 workshop) from **110** conversations
      and **38** workshop transcripts.

      **Address.** None. Segmentation is how the corpus is unitised,
      not whether formats elicit similar issues.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction. Tweaks: `parameters.yml`.

      > Online and in-person interactions were captured in [XXX]
      > chatbot transcripts and [XXX] workshop transcripts. Before
      > analysis, chatbot transcripts were divided into individual
      > participant responses and workshop transcripts were split into
      > passages at paragraph breaks (typically 150 words; no more than
      > 260 words). Units with fewer than four words were excluded,
      > leaving 2013 units for analysis.

      This stage fills those `[XXX]`: **110** chatbot conversations and
      **38** workshop transcripts, then the 2013 units.

  - liquid: |
      ## Store status

      **Cache** `{% if store_status.cache.exists %}{{ store_status.cache.path }} · {{ store_status.cache.mtime }} · {{ store_status.cache.size_human }}{% else %}absent (optional; Segment writes units here){% endif %}`

      ## What this page is

      Each **row is one source file** from `info/documents.yml` — two
      Recollective chatbot dumps plus 38 workshop DOCX (40 files).
      **Segment** splits a file into dialogue units; **Segment all** does
      the filtered set. Aspect must be `dialogue_units` (chatbot/workshop
      strategies do not emit `body_chunks`). Expand **Units** to read
      paragraph text. Save writes the cache and exploded `chunks.yml`.
      Once that output exists you may delete the cache.

      After a good run you should see **2013 units** (1003 chatbot, 1010
      workshop). Chatbot Recollective dumps pack many conversations into
      two files. `segment_dialogue_units` stamps `doc_id` as
      `{round}::{participant_id}` on chatbot units and `filename` on
      workshops so later stages weight **110 conversations + 38
      transcripts**, not the two dump files (see `GAP.md`).

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true

  - type: PopulateButton
    field: _segment
    args:
      description: Segment
      target: units
      compute:
        function: segment_dialogue_units
        field: units
        refresh: true
        row_args:
          path: filename
          reader: reader
          strategy: strategy
          min_chunk_words: min_chunk_words
          on_sparse_text: on_sparse_text
          workshop_chunk_words: workshop_chunk_words
          workshop_max_words: workshop_max_words
          min_unit_words: min_unit_words
          round: round
          filename: filename
          format: format
          facilitator_names: facilitator_names
        args:
          aspect: dialogue_units
          root: files

  - type: Dropdown
    field: strategy
    args:
      description: Segment strategy
      options:
        - docx_workshop.v1
        - docx_chatbot.v1
        - auto
        - pub_dialogue.v1

  - type: Textarea
    field: notes
    args:
      description: Catalog notes
---

# AI dialogue formats — catalog, segment, explode

Access (+ Assess grain). Catalog Recollective chatbot dumps and workshop DOCX, segment with docx_chatbot.v1 / docx_workshop.v1 (aspect dialogue_units), then explode to one chunk row per unit. Serve this config on its own; 02_embed reads info/chunks.yml.

## Access / Assess / Address

Nested loop: **Access** of the files, then a short **Assess** of
grain and coverage. This page does not Address the elicitation
question.

**Access.** Data: Recollective chatbot DOCX and workshop DOCX
under `files/`, rostered in `info/documents.yml` (one row per
file). Each file is segmented into a `units` list on that row,
then exploded to `info/chunks.yml` (one row per unit: `unit_id`,
`text`, `word_count`, `format`, `doc_id`, `participant_id`, …).

**Assess.** Units shorter than four words are dropped (too little
text for any later question). Two Recollective dumps pack many
conversations into two files; chatbot `doc_id` is stamped
`{round}::{participant_id}` so later document-equal weights do
not treat two dumps as two documents. A good run is **2013**
units (1003 chatbot, 1010 workshop) from **110** conversations
and **38** workshop transcripts.

**Address.** None. Segmentation is how the corpus is unitised,
not whether formats elicit similar issues.

## Paper reconstruction

Independent reconstruction. Tweaks: `parameters.yml`.

> Online and in-person interactions were captured in [XXX]
> chatbot transcripts and [XXX] workshop transcripts. Before
> analysis, chatbot transcripts were divided into individual
> participant responses and workshop transcripts were split into
> passages at paragraph breaks (typically 150 words; no more than
> 260 words). Units with fewer than four words were excluded,
> leaving 2013 units for analysis.

This stage fills those `[XXX]`: **110** chatbot conversations and
**38** workshop transcripts, then the 2013 units.
