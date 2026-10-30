# dods-ai-dialogue

A [DODS](https://github.com/mlatcl/dods) study: chatbot versus in-person
workshop as elicitation formats.

This repository is the independent reconstruction, in chained referia
stages, of the experiments in *An elicitation fallacy? Exploring the
role of AI in public dialogue*. It is for the domain researcher to
tweak. Each stage’s `_referia.yml` quotes the paper sentence it
reconstructs. If reconstructed numbers support the paper’s story, we
stop.

The paper’s story: the two formats elicited similar distributions of
issues and conditions; contributions grounded in personal experience
were more frequent in the workshop; chatbot contributions were typically
grounded in general principles; there is some indication that
experience-grounded workshop contributions follow each other.

## What is public, what is not

This repo holds the analysis: configs, prompts, parameters, the gap map,
and placeholder catalog shape.

Transcripts, facilitator names, quotes, embeddings, LLM caches, and
derived stores that contain them stay out of git. Serve those from a
private working copy. Copy `local.example.yml` to `local.yml` and paste the same name
list into `01_chunk/parameters.yml` and `01_turns/parameters.yml`. Copy
`info/documents.example.yml` to `info/documents.yml` and fill filenames
from the private store. Put DOCX under `files/chatbot/` and
`files/workshops/`.

Do not commit `local.yml`, `info/documents.yml`, or anything under
`files/` except the empty directory keepers.

## Stages

Run in directory order. Shared stores live in `info/`.

1. `01_chunk` — catalog and segment units
2. `01_turns` — labelled workshop speaker turns (Access grain for 10)
3. `02_embed` — extract concern/benefit/condition phrases, embed, pack
4. `03_vq` — vector quantisation (`n_vq: 40`)
5. `04_grain` — lenses on the codebook
6. `05_distance` — extra EMD / MDS (not in the paper; the paper uses JSD)
7. `06_compare` — document-weighted CBC, lens shares, JSD (Part A)
8. `07_grounds` — Part B basis coding
9. `08_questions` — chatbot question-type stress test
10. `09_validate` — word-list experience floor
11. `10_sequence` — stories-follow-stories
12. `11_multiverse` — analysis-choice product (page ready; not yet run)

Sidings (not in the paper): `siding_kind`, `siding_basis`, `siding_lens`.

Read `GAP.md` before treating 06 output as published Part A numbers.

## Serve

```bash
# from a private working copy that has files/ and filled local names
referia serve --root /path/to/this/study --port 8003
```

The live reconstruction currently sits under the private referia root,
not this clone. This clone is the public analysis package.

## Related

| Layer | Where |
|-------|--------|
| Approach | [mlatcl/dods](https://github.com/mlatcl/dods) |
| Tool | [lawrennd/referia](https://github.com/lawrennd/referia) |
| Paper package | [mlatcl/ai-dialogue-formats](https://github.com/mlatcl/ai-dialogue-formats) |
| This study | this repository |
