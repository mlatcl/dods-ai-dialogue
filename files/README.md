# Transcripts (not in git)

Put Recollective chatbot DOCX in `chatbot/` and workshop DOCX in
`workshops/`. Paths are relative to this directory; the glob is in
`info/constants.yml`.

Filename scheme (kebab-case inside a field, underscores between
fields, general → specific):

```
{format}_{round}_{session}.docx
{format}_{round}_{session}_{facilitator}.docx
```

- format: `chatbot` or `workshop`
- round: `autumn-2025` or `spring-2026`
- session: `recollective`, `breakout-1` … `breakout-5`, combined
  `breakout-3-4`, or zip carousel `carousel-c1` … `carousel-c7`
- facilitator: `f01` … `f06` on workshop files only

Examples: `chatbot_autumn-2025_recollective.docx`,
`workshop_autumn-2025_breakout-1_f01.docx`,
`workshop_spring-2026_carousel-c5_f06.docx`.

The name map for `f01`–`f06` lives in `local.yml` (copy
`local.example.yml`). Speaker-matching aliases go in
`facilitator_names` in that file and in the two stage
`parameters.yml` files. Do not put names in committed YAML.

The catalog `info/documents.yml` is gitignored. Start from
`info/documents.example.yml`. Original zip archives stay in
`files/originals/` and are not renamed.
