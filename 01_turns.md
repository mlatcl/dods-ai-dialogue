---
layout: referia
permalink: /01_turns/
# =============================================================================
# Dialogue analysis — 01 speaker turns (CIP-001E Access grain)
# =============================================================================
#
# Parallel to 01_chunk. Chunks stay ~150-word extract units. This page
# rebuilds labelled workshop *speaker turns* (Jess Labels) into
# info/turns.yml. 10_sequence reads that store; do not rerun 02–07.
# Markdown is coverage plus structure-only examples — no spoken text.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — labelled speaker turns"
description: >
  Access (+ Assess coverage). Rebuild labelled workshop speaker turns
  from DOCX (Speaker N / S2 / facilitator names, tab or colon,
  mid-paragraph split). Writes turns.yml for 10_sequence. Does not
  replace chunks.yml.
date: 2026-10-30

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: 01_turns
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: constants.yml
  directory: info
  index: index
  select: dialogue-v1

cache:
  type: yaml
  filename: _turns_cache.yml.gz
  directory: 01_turns
  index: index
  compress: gzip
  strict_columns: false
  columns:
    - turns
    - turns_md
    - n_turns
    - store_status

output:
  type: yaml
  filename: turns.yml
  directory: info
  index: turn_id
  strict_columns: false
  explode:
    field: turns
  columns:
    - turn_id
    - doc_id
    - turn_i
    - speaker
    - facilitator
    - round
    - format
    - filename
    - text

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: **Access** of labelled workshop speech, then
      **Assess** of which files actually have turns. The sequence
      question is Address on `10_sequence`.

      **Access.** Data: workshop DOCX that carry Speaker N / S2 /
      facilitator labels. Loaded as `info/turns.yml` (one row per
      speaker turn: `turn_id`, `doc_id`, `turn_i`, `speaker`,
      `facilitator`, `round`, `filename`, `text`). This does not
      replace `chunks.yml`.

      **Assess.** A file counts as labelled only if enough lines match
      the speaker pattern (`labelled_min_share`). Speaker 1 can be
      treated as facilitator. This reconstruction kept **17** labelled
      files and **2126** turns (paper: 16 transcripts, 2025 turns).
      After Rebuild, the right pane lists each workshop file
      (labelled / not / missing) and a few structure-only example
      turns (`speaker`, facilitator flag, word count). No spoken
      text.

      **Address.** None here. Whether stories follow stories is
      `10_sequence`.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the speaker-turn grain for the
      workshop sequence experiment. Tweaks: `parameters.yml`.

      > For this analysis, we focused on 16 transcripts from the second
      > workshop, where it was possible to identify 2025 ‘turns’ in
      > which interactions between speakers were clear.

      This Access stage rebuilds those turns (Labels: Speaker N / S2 /
      facilitator names). This reconstruction kept **17** labelled
      files and **2126** turns. `10_sequence` is the look-back on that
      store.

  - liquid: |
      ## Store status

      **Output** `{% if store_status.output.exists %}{{ store_status.output.path }} · {{ store_status.output.mtime }} · {{ store_status.output.size_human }}{% else %}absent — Rebuild + Save to write turns.yml{% endif %}`

  - liquid: |
      ## Labelled speaker turns

      Access grain beside `01_chunk`. Jess Labels: case-insensitive
      Speaker N / S2 / facilitator names; tab or colon; mid-paragraph
      split. All labelled workshop files (not only spring). 10_sequence
      filters the labelled round.

      This does **not** rerun extract, embed, VQ, or 07 Classify.
      After Rebuild: per-file labelled/not table, plus structure-only
      example turns. No spoken text.

      After Rebuild, **Save** so 10_sequence can read `turns.yml`.

  - type: Section
    title: Turn parameters
    entries:
      - type: HTML
        args:
          value: >
            <p class="chrome-hint">These knobs decide which workshop
            files count as labelled and whether Speaker 1 is a
            facilitator. <strong>Rebuild speaker turns</strong> uses
            the values on this row. Facilitator names stay in
            gitignored <code>local.yml</code> (copy into this
            parameters row locally if needed). Do not Save real names
            into git.</p>
      - type: BoundedFloatText
        field: labelled_min_share
        args:
          description: Min share of paragraphs with a speaker label
          min: 0
          max: 1
          step: 0.05
      - type: Checkbox
        field: treat_speaker_1_as_facilitator
        args:
          description: Treat Speaker 1 as facilitator
      - type: HTML
        liquid: |
          <p class="chrome-hint">{% if facilitator_names %}This row has {{ facilitator_names | size }} facilitator name(s) for Labels.{% else %}This row has no facilitator names. Rebuild will match Speaker N / S2 / Facilitator only.{% endif %}</p>

  - type: PopulateButton
    field: _run_turns
    args:
      description: Rebuild speaker turns
      target: turns_md
      compute:
        function: run_rebuild_speaker_turns
        field:
          - turns
          - turns_md
          - n_turns
        refresh: true
        args:
          files_root: files
        row_args:
          labelled_min_share: labelled_min_share
          treat_speaker_1_as_facilitator: treat_speaker_1_as_facilitator
          facilitator_names: facilitator_names

  - type: SaveButton
    field: _save
    args:
      description: Save turns.yml

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true

  - type: Markdown
    field: turns_md
    liquid: |
      {{ turns_md }}
---

# AI dialogue formats — labelled speaker turns

Access (+ Assess coverage). Rebuild labelled workshop speaker turns from DOCX (Speaker N / S2 / facilitator names, tab or colon, mid-paragraph split). Writes turns.yml for 10_sequence. Does not replace chunks.yml.

## Access / Assess / Address

Nested loop: **Access** of labelled workshop speech, then
**Assess** of which files actually have turns. The sequence
question is Address on `10_sequence`.

**Access.** Data: workshop DOCX that carry Speaker N / S2 /
facilitator labels. Loaded as `info/turns.yml` (one row per
speaker turn: `turn_id`, `doc_id`, `turn_i`, `speaker`,
`facilitator`, `round`, `filename`, `text`). This does not
replace `chunks.yml`.

**Assess.** A file counts as labelled only if enough lines match
the speaker pattern (`labelled_min_share`). Speaker 1 can be
treated as facilitator. This reconstruction kept **17** labelled
files and **2126** turns (paper: 16 transcripts, 2025 turns).
After Rebuild, the page lists each workshop file (labelled / not /
missing) and a few structure-only example turns (`speaker`,
facilitator flag, word count). No spoken text. The knobs are on
the form, not only in `parameters.yml`.

**Address.** None here. Whether stories follow stories is
`10_sequence`.

## Paper reconstruction

Independent reconstruction of the speaker-turn grain for the
workshop sequence experiment. Tweaks: `parameters.yml`.

> For this analysis, we focused on 16 transcripts from the second
> workshop, where it was possible to identify 2025 ‘turns’ in
> which interactions between speakers were clear.

This Access stage rebuilds those turns (Labels: Speaker N / S2 /
facilitator names). This reconstruction kept **17** labelled
files and **2126** turns. `10_sequence` is the look-back on that
store.
