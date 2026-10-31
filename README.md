# dods-ai-dialogue

A [DODS](https://github.com/mlatcl/dods) study: chatbot versus in-person
workshop as elicitation formats.

This repository encodes the data science analysis in *An elicitation fallacy? Exploring the
role of AI in public dialogue*. It uses the DODS approach to data analysis to enable the pipeline to be analysed and rerun easily. 

The paper focusses on two approaches to public dialogue, one driven by
on line chatbots, the otherthrough in person discussion. The aim of
the analysis is to understand whether formats elicited similar
distributions of issues and conditions. The analysis suggests
contributions grounded in personal experience were more frequent in
the workshop whereas chatbot contributions were typically grounded in
general principles. There is also some indication that
experience-grounded workshop contributions follow each other.

## What is public, what is not

This repo holds the analysis: configs, prompts, parameters, the gap map,
and placeholder catalog shape.

Transcripts, facilitator names, quotes, embeddings, LLM caches, and
derived stores that contain them are not stored, they would need to be
provided by a private working copy. Copy `local.example.yml` to
`local.yml` and paste the same name list into
`01_chunk/parameters.yml` and `01_turns/parameters.yml`. Copy
`info/documents.example.yml` to `info/documents.yml` and fill
filenames from the private store. Put DOCX under `files/chatbot/` and
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

## Install

This study is a directory of `_referia.md` stages (YAML frontmatter plus
a markdown body that describes what the stage does). The compute they call
lives in [referia](https://github.com/lawrennd/referia). Use GitHub
`main`, not the PyPI package: current `pip install referia` is 0.2.0 and
does not yet include the dialogue pipeline (segment, extract, VQ,
grounds, sequence, multiverse). Extract and grounds need the LLM stack
(`02_embed`, `07_grounds`, lens labels in `04_grain`).

Poetry from a clone (this is how referia ships the LLM group):

```bash
git clone https://github.com/lawrennd/referia.git
cd referia
poetry install --with llm
```

The same GitHub tree in a venv without Poetry. Referia’s LLM packages
are a Poetry group, not a pip extra, so install them in the same step:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "git+https://github.com/lawrennd/referia.git"
pip install langchain langchain-core langchain-openai langchain-anthropic \
  langchain-text-splitters openai anthropic tenacity diskcache python-dotenv
```

## API key

Extract and grounds call OpenAI (`gpt-4.1-mini` in this study). Referia
reads `OPENAI_API_KEY` from the process environment after loading a
`.env` file. It does not read lynguine credentials. Lynguine’s store
(`~/.lynguine/credentials/`, `LYNGUINE_CRED_*`, `${credential:KEY}` in
a flow) is for named sources such as Google Sheets, not for this LLM
path.

Create a `.env` with:

```
OPENAI_API_KEY=sk-...
```

Referia loads dotenv when the LLM module imports, in this order:

1. A `.env` found by walking up from the current working directory
   (put one in this study root if you `cd` here before `referia serve`,
   or in the referia clone if you `poetry run` from there).
2. Otherwise `~/.env`. Use that when the study sits on a network
   filesystem such as OneDrive: walking those trees can time out.

This repo gitignores `.env`. Do not put the key in `_referia.md` or
`parameters.yml`.

## Serve

This study is many configs, so use root-server mode (`--root`), not
single-config `--directory`. Default host is `127.0.0.1`, default port
`8000`.

```bash
git clone https://github.com/mlatcl/dods-ai-dialogue.git
cd dods-ai-dialogue
cp local.example.yml local.yml
cp info/documents.example.yml info/documents.yml
# fill local.yml, documents.yml, and files/ from the private store
referia serve --root . --host 127.0.0.1 --port 8000
```

If referia was installed with Poetry from the clone, run it from that
checkout:

```bash
poetry run referia serve --root /path/to/dods-ai-dialogue --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/`. Each stage is a subdirectory.

## Related

| Layer | Where |
|-------|--------|
| Approach | [mlatcl/dods](https://github.com/mlatcl/dods) |
| Tool | [lawrennd/referia](https://github.com/lawrennd/referia) |
| Paper package | [mlatcl/ai-dialogue-formats](https://github.com/mlatcl/ai-dialogue-formats) |
| This study | this repository |
