---
# =============================================================================
# Dialogue analysis — 02 extract, embed, pack (steps 4–6)
# =============================================================================
#
# CIP-0015 compute names: llm_extract_phrases, llm_embed_extraction_phrases.
# Explode / pack are lynguine CIP-0014 Access IO. Phrase extract is not
# optional: the studies embed extracted phrases, not raw paragraphs.
#
# Stores
# ------
#   constants     ../info/constants.yml      (frozen; uncompressed)
#   parameters    ./parameters.yml           (writable extract/embed knobs)
#   input         ../info/chunks.yml         (from 01_chunk; .yml.gz when bulky)
#   cache         ./_extract_cache.yml.gz    (payload + phrase text; nested
#                                            embedding keys are omitted on write)
#   join          ./_extract_phrases.parquet (unit_id + extraction_phrases;
#                                            07_grounds Access join — not
#                                            the yaml.gz, which is too slow)
#   output        ../info/phrases.yml        (phrase rows, no vectors)
#   pack          ../info/records.parquet    (phrases and embeddings)
#
# extraction_phrases is a declared cache column so populate/listing can
# write it; explode writes phrases.yml. Vectors stay in-memory for pack
# and land only in records.parquet. Pack is not a PopulateButton.
# LLMManager diskcache is cost-only. Gzip YAML is lynguine CIP-0015.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — extract phrases, embed, pack corpus"
description: >
  Nested Access / Address / Assess. LLM-extract short concern / benefit
  / condition phrases from each unit (paper-faithful prompt in
  ./parameters.yml), embed those phrases, then pack a one-row corpus
  store for grain. Serve this config on its own; 03_vq then 04_grain
  read the packed corpus.
date: 2026-10-29

display:
  layout: inline_list
  detail_field: extraction_phrases

constants:
  type: yaml
  directory: ../info
  filename: constants.yml
  index: index
  select: dialogue-v1

parameters:
  type: yaml
  directory: .
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: chunks.yml
  directory: ../info
  index: unit_id

cache:
  type: yaml
  filename: _extract_cache.yml.gz
  directory: .
  index: unit_id
  compress: gzip
  # Save also writes store_status (CIP-0017); v2 strict_columns would 503 on reload.
  strict_columns: false
  columns:
    - extraction_payload
    - extraction_phrases
    - store_status
  omit_nested_keys:
    extraction_phrases:
      - embedding

# Phrase table after explode of extraction_phrases (CIP-0014 explode reused).
output:
  type: yaml
  filename: phrases.yml
  directory: ../info
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

# Lynguine CIP-0014 array-pack: tall phrase output → one corpus row.
# Not a PopulateButton and not referia compute.
pack:
  type: parquet
  filename: records.parquet
  directory: ../info
  index: Name
  pack:
    # Extract and embed are separate steps; Save after extract must not abort.
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

      Nested loop on each unit: Access the chunk, Address the extract,
      Assess the quote, Address the embedding, Access the pack.

      **Access.** Data: `info/chunks.yml` (one row per unit from
      `01_chunk`). After extract, explode `extraction_phrases` to
      `info/phrases.yml` (one row per phrase, no vectors). Pack
      `info/records.parquet` (one corpus row: phrases, embeddings,
      `doc_ids`, kinds). Join copy for 07: `_extract_phrases.parquet`.

      **Assess.** Fuzzy match of each supporting quote against the unit
      text (`quote_support` ≥ 0.8). Drop quotes taken from the bot
      question or a facilitator. Word bounds on the paraphrase. This
      is quality of the extract against source text, reusable for any
      later question on those phrases.

      **Address.** The extract prompt *is* the Part A content question:
      short concern, benefit, and condition phrases. Embeddings
      (`text-embedding-3-large`) are the theme space for VQ. Neither
      step is question-agnostic.

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

      Embeddings here are `text-embedding-3-large`, as in the next
      paper sentence (themes).

  # Aspirational until referia CIP-0017 / lynguine store_stat.
  - liquid: |
      ## Store status

      **Cache** `{{ store_status.cache.path }}`
      {% if store_status.cache.exists %}
      in use · last write {{ store_status.cache.mtime }} · {{ store_status.cache.size_human }} · {{ store_status.cache.codec | default: "uncompressed" }}
      · {{ store_status.cache.n_rows }} rows · columns: {{ store_status.cache.columns | join: ", " }}
      {% else %}
      absent — Extract writes `_extract_cache.yml.gz`.
      {% endif %}

      ## What this page is

      Each **row is one dialogue unit** from `01_chunk` (2013 after a
      good segment). **Extract** pulls short concern / benefit /
      condition phrases with a supporting quote; **Embed** puts vectors
      on those phrases; **Save** explodes `phrases.yml` and packs
      `records.parquet`. After extract+embed you should see on the order
      of **11k phrases** (workshop-heavy). Expand **Phrases** on a row
      to read the text — do not paste quotes into git.

      Pack `doc_id` is the conversation grain stamped in `01_chunk`
      (`{round}::{participant_id}` for chatbot, `filename` for workshops).
      Extract also coalesces that grain and, when
      `quote_support_threshold` is 0.8, keeps only verified quotes and
      drops quotes taken from the bot question or facilitator.

      Phrase kinds and models are parameters (not limited to benefit).
      Edit them in **Extract parameters**, then **Refresh cache** or
      **Extract all**. **Embed all** writes vectors onto those phrases
      in memory. Expand **Phrases** on a row to read the text. Save writes
      parameters, cache (payload + phrase text, not vectors), exploded
      `phrases.yml` (text only), and packed `records.parquet` (vectors).
      Phrases without embeddings are omitted from the pack; Save after
      extract alone keeps an existing pack.
      **Reload cache** re-reads `_extract_cache.yml.gz` from disk.

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
            values.</p>
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
    title: Embed parameters
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Embed</strong> is available after
            extract has written phrases for that chunk.
            <strong>Embed all</strong> waits until every filtered row has
            been extracted.</p>
      - type: Dropdown
        field: embed_model
        args:
          description: Embed model
          options:
            - text-embedding-3-large
            - text-embedding-3-small

  - type: Section
    title: Cache
    args:
      collapse: false
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Refresh cache</strong> re-extracts
            every visible chunk with the extract parameters.
            <strong>Reload cache</strong> discards unsaved edits and re-reads
            the cache file from disk.</p>
      - type: PopulateButton
        field: _refresh_cache
        args:
          description: Refresh cache
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
          description: Reload cache

  - type: PopulateButton
    field: _extract
    args:
      description: Extract
      target: extraction_payload
      compute: *extract_compute

  - type: PopulateButton
    field: _embed
    args:
      description: Embed
      target: extraction_phrases
      requires: extraction_phrases
      compute:
        function: llm_embed_extraction_phrases
        field: extraction_phrases
        refresh: true
        row_args:
          extraction_phrases: extraction_phrases
          model: embed_model
          pca_dim: embed_pca_dim

  - type: Textarea
    field: notes
    args:
      description: Extract / embed notes
---

# AI dialogue formats — extract phrases, embed, pack corpus

Nested Access / Address / Assess. LLM-extract short concern / benefit / condition phrases from each unit (paper-faithful prompt in ./parameters.yml), embed those phrases, then pack a one-row corpus store for grain. Serve this config on its own; 03_vq then 04_grain read the packed corpus.

## Access / Assess / Address

Nested loop on each unit: Access the chunk, Address the extract,
Assess the quote, Address the embedding, Access the pack.

**Access.** Data: `info/chunks.yml` (one row per unit from
`01_chunk`). After extract, explode `extraction_phrases` to
`info/phrases.yml` (one row per phrase, no vectors). Pack
`info/records.parquet` (one corpus row: phrases, embeddings,
`doc_ids`, kinds). Join copy for 07: `_extract_phrases.parquet`.

**Assess.** Fuzzy match of each supporting quote against the unit
text (`quote_support` ≥ 0.8). Drop quotes taken from the bot
question or a facilitator. Word bounds on the paraphrase. This
is quality of the extract against source text, reusable for any
later question on those phrases.

**Address.** The extract prompt *is* the Part A content question:
short concern, benefit, and condition phrases. Embeddings
(`text-embedding-3-large`) are the theme space for VQ. Neither
step is question-agnostic.

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

Embeddings here are `text-embedding-3-large`, as in the next
paper sentence (themes).
