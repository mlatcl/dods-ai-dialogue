---
layout: referia
permalink: /02_embed/
# =============================================================================
# Dialogue analysis — 02 embed and pack (theme space)
# =============================================================================
#
# Embed is a different Address question from extract. Input is the extract
# (_data/corpus/extracts.parquet). This page writes vectors onto those phrases and
# packs records.parquet. phrases.yml is the Access explode of the extract
# (text only). Compute: llm_embed_extraction_phrases.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — embed phrases, pack corpus"
description: >
  Address embeddings (+ Access explode and pack). Read the extract from
  _data/corpus/extracts.parquet, embed those phrases, explode _data/corpus/phrases.yml,
  pack _data/corpus/records.parquet for VQ. Extract is 02_extract.
date: 2026-10-29
seq: 25

display:
  layout: inline_list
  detail_field: extraction_phrases

parameters:
  type: yaml
  directory: _data/02_embed
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: parquet
  filename: extracts.parquet
  directory: _data/corpus
  index: unit_id

# Chunk identity for explode inherit and listing. Not the extract.
data:
  type: yaml
  filename: chunks.yml
  directory: _data/corpus
  index: unit_id
  select_columns:
    - unit_id
    - filename
    - group
    - format
    - round
    - session_type
    - participant_id
    - extract_text
    - doc_id

# Tall phrase table: Access reshape of 02_extract, not a new extract.
output:
  type: yaml
  filename: phrases.yml
  directory: _data/corpus
  index: phrase_id
  strict_columns: false
  explode:
    field: extraction_phrases
    inherit:
      - unit_id
      - filename
      - group
      - format
      - round
      - session_type
      - participant_id
      - extract_text
  columns:
    - phrase_id
    - phrase
    - kind
    - chunk_id
    - doc_id
    - quote
    - quote_support
    - verified
    - unit_id
    - filename
    - group
    - format
    - round
    - session_type
    - participant_id
    - extract_text
  omit_columns:
    - embedding

pack:
  type: parquet
  filename: records.parquet
  directory: _data/corpus
  index: Name
  pack:
    drop_incomplete: true
    columns:
      phrases: phrase
      embeddings: embedding
      doc_ids: doc_id
      source_files: filename
      groups: group
      kinds: kind
      unit_ids: unit_id
      phrase_ids: phrase_id
    index_value: corpus

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop on each unit: Access the extract, Address the
      embedding, Access the pack.

      **Access.** Data: `_data/corpus/extracts.parquet` from `02_extract` (nested
      `extraction_phrases`), joined to chunk identity from
      `_data/corpus/chunks.yml`. Save explodes `_data/corpus/phrases.yml` (one row per
      phrase, no vectors) and packs `_data/corpus/records.parquet` (phrases and
      embeddings).

      **Assess.** None here. Quote support was assessed on `02_extract`.
      VQ coverage is `03_vq`.

      **Address.** Embeddings (`text-embedding-3-large`) are the theme
      space for VQ. That is not the extract question.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the embedding step that follows
      extract. Tweaks: `parameters.yml`.

      > These extracted contributions were then converted into numerical
      > representations (embeddings) using OpenAI’s text-embedding-3-large
      > model, which captures semantic similarity between phrases.

  - liquid: |
      ## Store status

      **Input** `{% if store_status.input.exists %}{{ store_status.input.path }} · {{ store_status.input.n_rows }} rows{% else %}absent — run 02_extract Save.{% endif %}`

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }}{% else %}absent — Save explodes phrases.yml.{% endif %}`

      **Pack** `{% if store_status.pack.exists %}{{ store_status.pack.path }} · {{ store_status.pack.size_human }}{% else %}absent — Embed then Save writes records.parquet.{% endif %}`

      ## What this page is

      Each **row is one dialogue unit** already extracted on
      `02_extract`. **Embed** greys once that unit's phrases already
      have vectors. Check **Refresh embed** on the row to run a
      filled unit again. **Embed all** skips filled units.
      **Refresh all** overwrites every visible unit that has phrases,
      including those already embedded. **Save** explodes
      `phrases.yml` and packs `records.parquet`. Phrases without
      embeddings are omitted from the pack; Save without Embed still
      writes `phrases.yml` and keeps an existing pack.

      Pack `doc_id` is the conversation grain from `01_chunk`. Expand
      **Phrases** to read the text — do not paste quotes into git.

      LLM client diskcache is API-cost only.
      {% if store_status.llm_diskcache.exists %}
      **LLM diskcache** `{{ store_status.llm_diskcache.path }}` — {{ store_status.llm_diskcache.label }}
      {% endif %}

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true

  - type: Section
    title: Embed parameters
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Embed</strong> needs
            <code>_data/corpus/extracts.parquet</code> from 02_extract.
            <strong>Embed all</strong> writes vectors onto every visible
            unit that has phrases and is not yet embedded.</p>
      - type: Dropdown
        field: embed_model
        args:
          description: Embed model
          options:
            - text-embedding-3-large
            - text-embedding-3-small

  - type: Section
    title: Embed store
    args:
      collapse: false
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Refresh all</strong> re-embeds
            every visible unit that has phrases, including ones already
            embedded. <strong>Reload embed</strong> discards unsaved
            edits and re-reads the extract and packed stores.</p>
      - type: PopulateButton
        field: _refresh_embed
        args:
          description: Refresh all
          skip_filled: false
          skip_empty: extraction_phrases
          target: extraction_phrases
          filled_key: embedding
          compute: &embed_compute
            function: llm_embed_extraction_phrases
            field: extraction_phrases
            refresh: true
            row_args:
              extraction_phrases: extraction_phrases
              model: embed_model
              pca_dim: embed_pca_dim
      - type: ReloadButton
        field: _reload
        args:
          description: Reload embed

  - type: PopulateButton
    field: _embed
    args:
      description: Embed
      all: true
      once: true
      refresh_if: refresh_embed
      once_blocked: Already embedded. Check Refresh embed to run again.
      skip_empty: extraction_phrases
      filled_key: embedding
      target: extraction_phrases
      requires: extraction_phrases
      compute: *embed_compute

  - type: Checkbox
    field: refresh_embed
    args:
      description: Refresh embed

  - type: SaveButton

  - type: Textarea
    field: notes
    args:
      description: Embed notes
---

# AI dialogue formats — embed phrases, pack corpus

Address embeddings (+ Access explode and pack). Read the extract from _data/corpus/extracts.parquet, embed those phrases, explode _data/corpus/phrases.yml, pack _data/corpus/records.parquet for VQ. Extract is 02_extract.

## Access / Assess / Address

Nested loop on each unit: Access the extract, Address the
embedding, Access the pack.

**Access.** Data: `_data/corpus/extracts.parquet` from `02_extract` (nested
`extraction_phrases`), joined to chunk identity from
`_data/corpus/chunks.yml`. Save explodes `_data/corpus/phrases.yml` (one row per
phrase, no vectors) and packs `_data/corpus/records.parquet` (phrases and
embeddings).

**Assess.** None here. Quote support was assessed on `02_extract`.
VQ coverage is `03_vq`.

**Address.** Embeddings (`text-embedding-3-large`) are the theme
space for VQ. That is not the extract question.

## Paper reconstruction

Independent reconstruction of the embedding step that follows
extract. Tweaks: `parameters.yml`.

> These extracted contributions were then converted into numerical
> representations (embeddings) using OpenAI’s text-embedding-3-large
> model, which captures semantic similarity between phrases.
