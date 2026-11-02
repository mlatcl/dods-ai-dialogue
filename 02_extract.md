---
layout: referia
permalink: /02_extract/
# =============================================================================
# Dialogue analysis — 02 extract (Part A content)
# =============================================================================
#
# Extract is its own Address question: short concern / benefit / condition
# phrases with a supporting quote. It is not a cache, and it is not embed.
# CIP-0015 put extract+embed+pack on one page and parked the nest in
# cache: because populate-all flushes a same-index writable store. That
# mixed LLM diskcache (API cost) with the analysis product. The product
# is this page's output.
#
# Stores
# ------
#   constants     _data/corpus/constants.yml
#   parameters    _data/02_extract/parameters.yml
#   input         _data/corpus/chunks.yml
#   output        _data/corpus/extracts.parquet   (unit grain: payload + phrases)
# 07_grounds joins this parquet (not a yaml.gz). 02_embed reads it, embeds,
# explodes phrases.yml, and packs records.parquet.
# LLMManager diskcache is API-cost only.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — extract phrases"
description: >
  Address extract (+ Assess quote_support). LLM-extract short concern /
  benefit / condition phrases from each unit (paper-faithful prompt in
  _data/02_extract/parameters.yml). Output is _data/corpus/extracts.parquet, unit grain.
  Embed and pack are 02_embed.
date: 2026-10-29
seq: 20

display:
  layout: inline_list
  detail_field: extraction_phrases

constants:
  type: yaml
  directory: _data/corpus
  filename: constants.yml
  index: index
  select: dialogue-v1

parameters:
  type: yaml
  directory: _data/02_extract
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: chunks.yml
  directory: _data/corpus
  index: unit_id

# Unit-grained extract. Same index as chunks so Extract stays on units
# after Save. Not a cache: this is the Part A content product.
output:
  type: parquet
  filename: extracts.parquet
  directory: _data/corpus
  index: unit_id
  strict_columns: false
  columns:
    - extraction_payload
    - extraction_phrases
    - store_status
  omit_nested_keys:
    extraction_phrases:
      - embedding

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop on each unit: Access the chunk, Address the extract,
      Assess the quote.

      **Access.** Data: `_data/corpus/chunks.yml` (one row per unit from
      `01_chunk`). Loaded as listing rows. Extract writes
      `_data/corpus/extracts.parquet` (one row per unit: payload and nested
      `extraction_phrases`). That parquet is the extract. 07 joins it.
      02_embed reads it. The tall `phrases.yml` table is an Access
      reshape on 02_embed Save, not a second extract.

      **Assess.** Fuzzy match of each supporting quote against the unit
      text (`quote_support` ≥ 0.8). Drop quotes taken from the bot
      question or a facilitator. Word bounds on the paraphrase. This
      is quality of the extract against source text, reusable for any
      later question on those phrases.

      **Address.** The extract prompt *is* the Part A content question:
      short concern, benefit, and condition phrases. Embeddings are a
      different question (`02_embed`).

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the three-pass extract. Tweaks:
      `parameters.yml`.

      > We extract contributions from each transcript unit using
      > gpt-4.1-mini, using three separate extraction passes to
      > identify: concerns about AI use, anticipated benefits, and
      > conditions or considerations attached to its acceptable use.
      > Each extracted point comprised a short paraphrase of the
      > original content and a supporting quote from the original
      > transcript. Extracted quotes were checked against the source
      > text using fuzzy matching, with points retained where the match
      > score met a threshold of 0.8.

  - liquid: |
      ## Store status

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · last write {{ store_status.output.mtime }} · {{ store_status.output.size_human }} · {{ store_status.output.n_rows }} rows{% else %}absent — Extract writes _data/corpus/extracts.parquet.{% endif %}`

      ## What this page is

      Each **row is one dialogue unit** from `01_chunk` (2013 after a
      good segment). **Extract** pulls short concern / benefit /
      condition phrases with a supporting quote. There is no Embed
      here. Expand **Phrases** on a row to read the text — do not paste
      quotes into git.

      Pack `doc_id` is stamped in `01_chunk`. Extract coalesces that
      grain and, when `quote_support_threshold` is 0.8, keeps only
      verified quotes and drops quotes taken from the bot question or
      facilitator.

      **Extract** greys once that unit has a payload. Check
      **Refresh extract** on the row to run a filled unit again.
      **Extract all** skips filled units. **Refresh all** overwrites
      every visible unit, including those already extracted.
      **Save** writes `_data/corpus/extracts.parquet`. **Reload extract**
      re-reads that file.
      LLM client diskcache is API-cost only, not this store.
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
    title: Extract parameters
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint">Kinds, model, word bounds, and prompt
            apply to every chunk. <strong>Extract all</strong> uses these
            values. This page does not embed.</p>
      - type: Text
        field: phrase_kinds
        args:
          description: Phrase kinds (comma-separated; not limited to benefit)
      - type: Dropdown
        field: extract_model
        args:
          description: Extract model
          options:
            - gpt-4o-mini
            - gpt-4o
            - gpt-4.1-mini
      - type: BoundedIntText
        field: extract_min_words
        args:
          description: Min words
          min: 1
          max: 40
      - type: BoundedIntText
        field: extract_max_words
        args:
          description: Max words
          min: 1
          max: 80
      - type: BoundedIntText
        field: extract_max_items
        args:
          description: Max phrases per kind
          min: 1
          max: 40
      - type: BoundedFloatText
        field: quote_support_threshold
        args:
          description: Keep quotes with support ≥ this (0 = keep all)
          min: 0
          max: 1
          step: 0.05
      - type: Textarea
        field: extract_prompt
        args:
          description: Extract prompt
          rows: 6

  - type: Section
    title: Extract store
    args:
      collapse: false
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Refresh all</strong> re-extracts
            every visible chunk, including ones already extracted.
            <strong>Reload extract</strong> discards unsaved edits and re-reads
            <code>_data/corpus/extracts.parquet</code>.</p>
      - type: PopulateButton
        field: _refresh_extract
        args:
          description: Refresh all
          skip_filled: false
          target: extraction_payload
          compute: &extract_compute
            function: llm_extract_phrases
            field:
              - extraction_payload
              - extraction_phrases
            refresh: true
            row_args:
              text: text
              chunk_id: unit_id
              doc_id: doc_id
              participant_id: participant_id
              round: round
              filename: filename
              format: format
              extract_text: extract_text
              context: context
              quote_support_threshold: quote_support_threshold
              prompt_template: extract_prompt
              model: extract_model
              min_words: extract_min_words
              max_words: extract_max_words
              max_items: extract_max_items
              kinds: phrase_kinds
              sentinel_concern: extract_sentinel_concern
              sentinel_benefit: extract_sentinel_benefit
              sentinel_condition: extract_sentinel_condition
      - type: ReloadButton
        field: _reload
        args:
          description: Reload extract

  - type: PopulateButton
    field: _extract
    args:
      description: Extract
      all: true
      once: true
      refresh_if: refresh_extract
      once_blocked: Already extracted. Check Refresh extract to run again.
      target: extraction_payload
      compute: *extract_compute

  - type: Checkbox
    field: refresh_extract
    args:
      description: Refresh extract

  - type: SaveButton

  - type: Textarea
    field: notes
    args:
      description: Extract notes
---

# AI dialogue formats — extract phrases

Address extract (+ Assess quote_support). LLM-extract short concern / benefit / condition phrases from each unit (paper-faithful prompt in _data/02_extract/parameters.yml). Output is _data/corpus/extracts.parquet, unit grain. Embed and pack are 02_embed.

## Access / Assess / Address

Nested loop on each unit: Access the chunk, Address the extract,
Assess the quote.

**Access.** Data: `_data/corpus/chunks.yml` (one row per unit from
`01_chunk`). Loaded as listing rows. Extract writes
`_data/corpus/extracts.parquet` (one row per unit: payload and nested
`extraction_phrases`). That parquet is the extract. 07 joins it.
02_embed reads it. The tall `phrases.yml` table is an Access
reshape on 02_embed Save, not a second extract.

**Assess.** Fuzzy match of each supporting quote against the unit
text (`quote_support` ≥ 0.8). Drop quotes taken from the bot
question or a facilitator. Word bounds on the paraphrase. This
is quality of the extract against source text, reusable for any
later question on those phrases.

**Address.** The extract prompt *is* the Part A content question:
short concern, benefit, and condition phrases. Embeddings are a
different question (`02_embed`).

## Paper reconstruction

Independent reconstruction of the three-pass extract. Tweaks:
`parameters.yml`.

> We extract contributions from each transcript unit using
> gpt-4.1-mini, using three separate extraction passes to
> identify: concerns about AI use, anticipated benefits, and
> conditions or considerations attached to its acceptable use.
> Each extracted point comprised a short paraphrase of the
> original content and a supporting quote from the original
> transcript. Extracted quotes were checked against the source
> text using fuzzy matching, with points retained where the match
> score met a threshold of 0.8.
