---
layout: referia
permalink: /08_questions/
# =============================================================================
# Dialogue analysis — 08 question-type stress test (CIP-001E)
# =============================================================================
#
# Regex on chatbot unit context. No model. Paper: ~0.3% of bot questions
# ask about experience, so the experience gap is not "the bot asked for
# stories."
# =============================================================================

referia_config_version: 2
title: "AI dialogue formats — chatbot question types"
description: >
  Assess bot questions, Address the Part B confound. Share of chatbot
  units whose preceding bot question matches each pattern (experience,
  example, why, safeguards, …). Local regex only.
date: 2026-10-29

display:
  layout: side_by_side

parameters:
  type: yaml
  directory: 08_questions
  filename: parameters.yml
  index: index
  select: dialogue-v1

input:
  type: parquet
  filename: records.parquet
  directory: info
  index: Name

output:
  type: yaml
  filename: question_types.yml
  directory: info
  index: Name
  strict_columns: false
  columns:
    - question_type_rows
    - question_type_md
    - n_chatbot_units
    - store_status

viewer:
  - liquid: |
      ## Access / Assess / Address

      Nested loop: Access chatbot context, Assess question-type
      coverage, Address the confound for Part B.

      **Access.** Data: preceding bot question on chatbot units
      (`chunks.yml` `context`, reached via the packed corpus row).
      Writes `info/question_types.yml` (counts and shares). Local
      regex only.

      **Assess.** The type table characterises what the bot asked
      (experience, example, why, safeguards, …). That coverage is
      usable without the experience-gap question.

      **Address.** Was the Part B experience gap because the bot asked
      for stories? Paper story: only 0.3% of chatbot questions asked
      directly for experience. Whether the *answer* was
      experience-grounded still needs `grounds.yml` from 07.

  - liquid: |
      ## Paper reconstruction

      Independent reconstruction of chatbot question typing. Tweaks:
      `parameters.yml`.

      > For chatbot interactions, we classified questions according to
      > the type of response they sought and compared the proportion of
      > experience-grounded contributions after different question
      > types.

      Paper story: “Only 0.3% of chatbot questions asked participants
      directly for their experiences. When the chatbot requested an
      example, the answer given was more likely to draw from
      experience (10.7% against 5.5% after other questions).”

  - liquid: |
      ## What this page is

      One corpus row. Regex over the **preceding bot question**
      (`chunks.yml` `context`) for chatbot units only: experience,
      example, why, safeguards, and the other patterns in
      `parameters.yml`. No model.

      **What you should see:** a count table and the share of bot
      questions that match each pattern. Jess's paragraph is that
      ~0.3% of bot questions ask about experience — so the Part B
      experience gap is not "the bot asked for stories." This stage
      reports how often the bot *asked*. Whether the *answer* was
      experience-grounded still needs `grounds.yml` from 07.

  - type: PopulateButton
    field: _run_questions
    args:
      description: Count question types
      target: question_type_md
      compute: &q_compute
        function: run_question_type_stress
        field:
          - question_type_rows
          - question_type_md
          - n_chatbot_units
        refresh: true

review:
  - type: precompute
    specifications:
      - function: named_store_status
        field: store_status
        refresh: true
      - function: run_question_type_stress
        field:
          - question_type_rows
          - question_type_md
          - n_chatbot_units
        refresh: true

  - type: Markdown
    field: question_type_md
    liquid: |
      {{ question_type_md }}
---

# AI dialogue formats — chatbot question types

Assess bot questions, Address the Part B confound. Share of chatbot units whose preceding bot question matches each pattern (experience, example, why, safeguards, …). Local regex only.

## Access / Assess / Address

Nested loop: Access chatbot context, Assess question-type
coverage, Address the confound for Part B.

**Access.** Data: preceding bot question on chatbot units
(`chunks.yml` `context`, reached via the packed corpus row).
Writes `info/question_types.yml` (counts and shares). Local
regex only.

**Assess.** The type table characterises what the bot asked
(experience, example, why, safeguards, …). That coverage is
usable without the experience-gap question.

**Address.** Was the Part B experience gap because the bot asked
for stories? Paper story: only 0.3% of chatbot questions asked
directly for experience. Whether the *answer* was
experience-grounded still needs `grounds.yml` from 07.

## Paper reconstruction

Independent reconstruction of chatbot question typing. Tweaks:
`parameters.yml`.

> For chatbot interactions, we classified questions according to
> the type of response they sought and compared the proportion of
> experience-grounded contributions after different question
> types.

Paper story: “Only 0.3% of chatbot questions asked participants
directly for their experiences. When the chatbot requested an
example, the answer given was more likely to draw from
experience (10.7% against 5.5% after other questions).”
