---
layout: referia
permalink: /07_grounds/
# =============================================================================
# Dialogue analysis — 07 Part B grounds (CIP-001E)
# =============================================================================
#
# One LLM JSON call per unit over that unit's extracted points. Explode to
# info/grounds.yml. Layout is inline_list (CIP-0020): first GET paints
# list_page_size rows, then Load more / scroll. Classify all still loops
# the full working set (CIP-0021 batches). Save even if HTMX fails.
#
# Stores
# ------
#   parameters  07_grounds/parameters.yml
#   input       info/chunks.yml
#   data        02_embed/_extract_phrases.parquet  (extraction_phrases)
#   cache       07_grounds/_grounds_cache.yml.gz
#   output      info/grounds.yml
# Access join on unit_id. row_args maps extraction_phrases → points.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — Part B grounds"
description: >
  Address Part B (Access join + explode). For each unit, classify what
  every extracted point rests on (experience, principle, professional
  knowledge, …). Headline experience 17.7% vs 4.1% comes from this
  stage, not from 04_grain.
date: 2026-10-29

display:
  layout: inline_list
  detail_field: grounds
  list_page_size: 50
  list_paging: append

parameters:
  type: yaml
  directory: 07_grounds
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: chunks.yml
  directory: info
  index: unit_id
  select_columns:
    - unit_id
    - extract_text
    - context
    - filename
    - group
    - format
    - round
    - session_type
    - participant_id
    - doc_id

# Projection of 02's unit-grained nest (CIP-0015). Do not join
# _extract_cache.yml.gz here — PyYAML safe_load of that file is ~11s
# (payloads + phrases). Phrase-grained phrases.yml is the VQ explode.
data:
  type: parquet
  filename: _extract_phrases.parquet
  directory: 02_embed
  index: unit_id
  select_columns:
    - unit_id
    - extraction_phrases

cache:
  type: yaml
  filename: _grounds_cache.yml.gz
  directory: 07_grounds
  index: unit_id
  compress: gzip
  strict_columns: false
  columns:
    - grounds_payload
    - grounds
    - store_status

output:
  type: yaml
  filename: grounds.yml
  directory: info
  index: phrase_id
  strict_columns: false
  explode:
    field: grounds
    inherit:
      - unit_id
      - filename
      - group
      - format
      - round
      - session_type
      - participant_id
      - doc_id
  columns:
    - phrase_id
    - phrase
    - kind
    - quote
    - basis
    - unit_id
    - doc_id
    - format
    - round

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: Access the unit and its phrases, Address the
      grounding code, Access the exploded store.

      **Access.** Data: `info/chunks.yml` (units) joined on `unit_id`
      to `02_embed/_extract_phrases.parquet` (`extraction_phrases`).
      Classify writes `_grounds_cache.yml.gz`. Save explodes
      `info/grounds.yml` (one row per point: `phrase_id`, `basis`,
      `kind`, `format`, `doc_id`).

      **Assess.** Units with 0 points are not sent to the model
      (nothing to code). The chip's **complete** count is already
      classified or empty; **failed** is a compute error. That is
      coverage of the coding pass, not a characterisation of the
      transcripts.

      **Address.** What evidence does each extracted point rest on
      (seven bases)? Paper story: workshop contributions were more
      often grounded in personal experience (17.7% vs 4.1% chatbot);
      chatbot contributions were typically general principles (91.6%
      vs 68.9%).

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of evidential-grounding coding.
      Tweaks: `parameters.yml`.

      > To examine what evidence participants draw from when expressing
      > their views, we used gpt-4.1-mini to classify the ‘evidential
      > grounding’ of each extracted point. The model was given the
      > original transcript passage and extracted points, and asked to
      > assign each point to one of seven categories: personal
      > experience, others' experience, professional knowledge,
      > general principle, a public example, information from the
      > dialogue materials, or unclear.

      Paper story this coding is for: “Participants grounded their
      contributions differently in-person versus with chatbots.”
      Workshop experience 17.7% vs chatbot 4.1%; chatbot mostly
      general principles (91.6% vs 68.9% in workshops).

  - liquid: |
      ## Store status

      **Cache** `{% if store_status.cache.exists %}{{ store_status.cache.path }} · {{ store_status.cache.n_rows }} rows{% else %}absent — Classify writes _grounds_cache.yml.gz{% endif %}`

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }}{% else %}absent — Save explodes grounds.yml{% endif %}`

  - liquid: |
      ## What this page is

      You are looking at a **vertical list** of dialogue units (2013
      in the working set). The first paint is 50 rows; **Load more**
      appends the next page (CIP-0020). Points are the unit's
      `extraction_phrases` from 02's `_extract_phrases.parquet`, joined
      on `unit_id`. Expand a row to classify those points against seven
      bases:
      `personal_experience`, `others_experience`,
      `professional_knowledge`, `principle`, `public_example`,
      `project_materials`, `unclear`. Do not paste quotes into git.

      **Classify** greys once that unit has a payload, and when the
      unit has 0 points. Check **Refresh classification** on the row
      to run a filled unit again.       **Classify all** is rolling
      populate-all (CIP-0021): short batches, progress chip, Pause.
      The Classify all filtered box shows how many units are
      classified so far against the working set. The chip updates
      that count as batches finish. The chip fraction is units
      finished this pass. **Complete**
      means already classified or no points (nothing to send to the
      model). **Failed** is a compute error in the current batch.
      Remaining units still need Classify. **Refresh all** (Cache, at
      the top) overwrites every working unit that has points, including
      those already classified. **Save** even if HTMX says the request
      failed. Save explodes `grounds.yml` (one row per point). A
      one-row `grounds.yml` means a single Classify, not Classify all.

      Paper headline **experience 17.7% vs 4.1%** (chatbot vs workshop)
      is a document-weighted share of these codes. It does not come
      from 04_grain.

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true

  - type: Section
    title: Grounds parameters
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint">Model and prompt apply to every unit.
            <strong>Classify all</strong> uses these values.</p>
      - type: Dropdown
        field: grounds_model
        args:
          description: Model
          options: ["gpt-4.1-mini", "gpt-4o-mini", "stub"]
      - type: Textarea
        field: grounds_prompt
        args:
          description: Prompt (must include <<UNIT>> and <<POINTS>>)
          rows: 8

  - type: Section
    title: Cache
    args:
      collapse: false
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint"><strong>Refresh all</strong> re-classifies
            every working unit that has points, including ones already
            classified. The progress chip still labels a unit
            <em>complete</em> once this pass has written it (or when it
            has no points). <strong>Reload cache</strong> discards
            unsaved edits and re-reads the cache file from disk.</p>
      - type: PopulateButton
        field: _refresh_cache
        args:
          description: Refresh all
          skip_filled: false
          skip_empty: extraction_phrases
          target: grounds_payload
          compute: &grounds_compute
            function: llm_classify_grounds
            field:
              - grounds_payload
              - grounds
            refresh: true
            row_args:
              text: extract_text
              context: context
              points: extraction_phrases
              prompt_template: grounds_prompt
              model: grounds_model
              system_prompt: grounds_system
      - type: ReloadButton
        field: _reload
        args:
          description: Reload cache

  - type: PopulateButton
    field: _classify
    args:
      description: Classify
      all: true
      once: true
      refresh_if: refresh_classification
      skip_empty: extraction_phrases
      target: grounds_payload
      compute: *grounds_compute

  - type: Checkbox
    field: refresh_classification
    args:
      description: Refresh classification

  - type: Textarea
    field: notes
    args:
      description: Grounds notes
---

# AI dialogue formats — Part B grounds

Address Part B (Access join + explode). For each unit, classify what every extracted point rests on (experience, principle, professional knowledge, …). Headline experience 17.7% vs 4.1% comes from this stage, not from 04_grain.

## Access / Assess / Address

Nested loop: Access the unit and its phrases, Address the
grounding code, Access the exploded store.

**Access.** Data: `info/chunks.yml` (units) joined on `unit_id`
to `02_embed/_extract_phrases.parquet` (`extraction_phrases`).
Classify writes `_grounds_cache.yml.gz`. Save explodes
`info/grounds.yml` (one row per point: `phrase_id`, `basis`,
`kind`, `format`, `doc_id`).

**Assess.** Units with 0 points are not sent to the model
(nothing to code). The chip's **complete** count is already
classified or empty; **failed** is a compute error. That is
coverage of the coding pass, not a characterisation of the
transcripts.

**Address.** What evidence does each extracted point rest on
(seven bases)? Paper story: workshop contributions were more
often grounded in personal experience (17.7% vs 4.1% chatbot);
chatbot contributions were typically general principles (91.6%
vs 68.9%).

## Paper reconstruction

Independent reconstruction of evidential-grounding coding.
Tweaks: `parameters.yml`.

> To examine what evidence participants draw from when expressing
> their views, we used gpt-4.1-mini to classify the ‘evidential
> grounding’ of each extracted point. The model was given the
> original transcript passage and extracted points, and asked to
> assign each point to one of seven categories: personal
> experience, others' experience, professional knowledge,
> general principle, a public example, information from the
> dialogue materials, or unclear.

Paper story this coding is for: “Participants grounded their
contributions differently in-person versus with chatbots.”
Workshop experience 17.7% vs chatbot 4.1%; chatbot mostly
general principles (91.6% vs 68.9% in workshops).
