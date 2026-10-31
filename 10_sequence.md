---
layout: referia
permalink: /10_sequence/
# =============================================================================
# Dialogue analysis — 10 stories-follow-stories (CIP-001E)
# =============================================================================
#
# Methodology, not published counts. Grain is labelled spring workshop
# *speaker turns* from 01_turns (turns.yml), with 07 grounds placed by quote.
# Within-transcript shuffle; optional within-topic when a topic id exists.
# Own-words recode is a later column — this page is main-run 07 codes.
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — stories follow stories"
description: >
  Address stories-follow-stories (Access turns + 07 codes). Among
  labelled workshop speaker turns: if a previous different
  non-facilitator turn carried an experience-grounded point, does this
  speaker's point also rest on experience? Compared to a
  within-transcript shuffle. Main-run 07 codes. No quote text is stored.
date: 2026-10-30

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: 10_sequence
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: yaml
  filename: constants.yml
  directory: info
  index: index
  select: dialogue-v1

output:
  type: yaml
  filename: sequence.yml
  directory: info
  index: index
  strict_columns: false
  columns:
    - sequence_rows
    - sequence_md
    - n_sequence_turns
    - store_status

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: Access speaker turns and 07 codes, Assess coverage
      of labelled files, Address the look-back.

      **Access.** Data: `info/turns.yml` from `01_turns` (one row per
      labelled workshop speaker turn). 07 points are placed onto turns
      by quote substring. Writes `info/sequence.yml` (look-back rates,
      no quote text). This page does not rebuild DOCX.

      **Assess.** How many labelled files and turns have a 07 point to
      place. This reconstruction: **17** files, **2126** turns (paper:
      16 transcripts, 2025 turns). Within-topic is blank until points
      carry a VQ/grain id.

      **Address.** Are participants more likely to draw from experience
      after another participant has done the same? Observed P(this
      turn is a story | a different non-facilitator's story in the
      previous L turns) versus a within-transcript shuffle that keeps
      each speaker's story rate. L = 1, 2, 3, 5. Paper story: some
      indication that experience-grounded contributions follow each
      other.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of the workshop look-back. Tweaks:
      `parameters.yml`.

      > For workshop interactions, we examined whether participants
      > were more likely to draw from experience after another
      > participant had done the same. For this analysis, we focused
      > on 16 transcripts from the second workshop, where it was
      > possible to identify 2025 ‘turns’ in which interactions
      > between speakers were clear. For each turn, we examined
      > whether another participant had contributed an
      > experience-grounded point within the preceding one to five
      > turns.

      Paper story: “Our sequence analysis provides some indication of
      this, as that experience-grounded contributions tended to follow
      each other.”

  - liquid: |
      ## Look-back results

      {% if sequence_md %}
      {{ sequence_md }}
      {% else %}
      No look-back table yet. Run **look-back shuffle**, then **Save**.
      {% endif %}
    watch:
      - sequence_md

  - liquid: |
      ## Stories follow stories

      One corpus row. **Speaker turns** from `01_turns` (`turns.yml`),
      not 01_chunk units. This page places 07 points by quote substring
      and runs the look-back shuffle. It does not rebuild DOCX.

      Own-words recode (format-blind second code column) is not on this
      page. Within-topic is blank until points carry a VQ/grain id —
      the shuffle does not wait on that.

      Observed: P(this turn is a story | one of the previous L turns by a
      *different* non-facilitator was a story). Shuffle keeps each
      speaker's story rate. Look-backs L = 1, 2, 3, 5.

      No populate-all over turns. No quote text in the output.

  - type: PopulateButton
    field: _run_sequence
    args:
      description: Run look-back shuffle
      target: sequence_md
      skip_filled: false
      compute: &seq_compute
        function: run_stories_follow_stories
        field:
          - sequence_rows
          - sequence_md
          - n_sequence_turns
        refresh: true
        row_args:
          lookbacks: lookbacks
          n_shuffles: n_shuffles
          seed: seed
          labelled_round: labelled_round
          cross_unit_only: cross_unit_only

  - type: SaveButton
    field: _save
    args:
      description: Save sequence.yml

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true

  - type: Markdown
    field: sequence_md
    liquid: |
      {{ sequence_md }}
---

# AI dialogue formats — stories follow stories

Address stories-follow-stories (Access turns + 07 codes). Among labelled workshop speaker turns: if a previous different non-facilitator turn carried an experience-grounded point, does this speaker's point also rest on experience? Compared to a within-transcript shuffle. Main-run 07 codes. No quote text is stored.

## Access / Assess / Address

Nested loop: Access speaker turns and 07 codes, Assess coverage
of labelled files, Address the look-back.

**Access.** Data: `info/turns.yml` from `01_turns` (one row per
labelled workshop speaker turn). 07 points are placed onto turns
by quote substring. Writes `info/sequence.yml` (look-back rates,
no quote text). This page does not rebuild DOCX.

**Assess.** How many labelled files and turns have a 07 point to
place. This reconstruction: **17** files, **2126** turns (paper:
16 transcripts, 2025 turns). Within-topic is blank until points
carry a VQ/grain id.

**Address.** Are participants more likely to draw from experience
after another participant has done the same? Observed P(this
turn is a story | a different non-facilitator's story in the
previous L turns) versus a within-transcript shuffle that keeps
each speaker's story rate. L = 1, 2, 3, 5. Paper story: some
indication that experience-grounded contributions follow each
other.

## Paper reconstruction

Independent reconstruction of the workshop look-back. Tweaks:
`parameters.yml`.

> For workshop interactions, we examined whether participants
> were more likely to draw from experience after another
> participant had done the same. For this analysis, we focused
> on 16 transcripts from the second workshop, where it was
> possible to identify 2025 ‘turns’ in which interactions
> between speakers were clear. For each turn, we examined
> whether another participant had contributed an
> experience-grounded point within the preceding one to five
> turns.

Paper story: “Our sequence analysis provides some indication of
this, as that experience-grounded contributions tended to follow
each other.”
