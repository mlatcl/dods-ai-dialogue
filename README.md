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
`_data/01_chunk/parameters.yml` and `_data/01_turns/parameters.yml`. Copy
`_data/corpus/documents.example.yml` to `_data/corpus/documents.yml` and fill
filenames from the private store. Put DOCX under `files/chatbot/` and
`files/workshops/`.

Do not commit `local.yml`, `_data/corpus/documents.yml`, or anything under
`files/` except the empty directory keepers.

## Stages

Run in directory order. Shared stores live in `_data/corpus/`.

1. `01_chunk` — catalog and segment units
2. `01_turns` — labelled workshop speaker turns (Access grain for 10)
3. `02_extract` — extract concern/benefit/condition phrases
4. `02_embed` — embed those phrases and pack the corpus
5. `03_vq` — vector quantisation (`n_vq: 40`)
6. `04_grain` — lenses on the codebook
7. `05_distance` — extra EMD / MDS (not in the paper; the paper uses JSD)
8. `06_compare` — document-weighted CBC, lens shares, JSD (Part A)
9. `07_grounds` — Part B basis coding
10. `08_questions` — chatbot question-type stress test
11. `09_validate` — word-list experience floor
12. `10_sequence` — stories-follow-stories
13. `11_multiverse` — analysis-choice product (page ready; not yet run)

Sidings (not in the paper): `siding_kind`, `siding_basis`, `siding_lens`.

Read `GAP.md` before treating 06 output as published Part A numbers.

## Edit on GitHub

`_config.yml` at the study root is a Jekyll-style site file. Referia
reads `ghub` from it and treats those keys as constants on every stage
(`github_edit_url`, `ghub_organization`, `ghub_repository`,
`ghub_branch`). The page header then shows Giki’s `[edit]` link to the
current markdown page on GitHub (`index.md`, `01_turns.md`, …). Analysis
knobs stay in `_data/<stage>/parameters.yml` and in
`_data/corpus/constants.yml`. `_config.yml` also sets `referia.urls: permalink`
so `/01_turns/` is `01_turns.md`, not a directory.

## Data layout
## GitHub Pages

The same markdown pages are a static site at
[mlatcl.github.io/dods-ai-dialogue](https://mlatcl.github.io/dods-ai-dialogue/).
That render is the page body (what each stage does), not the live
referia widgets. Personal stores are excluded from the build.

CI is GitHub’s Jekyll Pages workflow
(`.github/workflows/jekyll-gh-pages.yml`). Pushes to `main` run:

```bash
# equivalent of actions/jekyll-build-pages@v1
jekyll build --source ./ --destination ./_site --future
```

`baseurl` is `/dods-ai-dialogue`. Repo Settings → Pages is **GitHub
Actions**. Pull requests only build; they do not deploy.

Locally:

```bash
jekyll serve --baseurl /dods-ai-dialogue
```

Open `http://127.0.0.1:4000/dods-ai-dialogue/`. Do not commit `_site/`.

## Install

All writable analysis artefacts sit under `_data/`:

- `_data/corpus/` — shared stores (was `info/`): documents, chunks, phrases,
  extracts, codebook, Part A/B outputs, constants
- `_data/01_chunk/`, `_data/02_embed/`, … — per-stage `parameters.yml`, caches,
  and intermediate products

Stage *pages* stay at the repo root (`01_chunk.md`, …) for permalink URLs.
`_config.yml` excludes `_data` from the Pages build; only the small tracked
files under `_data/corpus/` (constants + documents example) ship publicly.

## GitHub Pages

The same markdown pages are a static site at
[mlatcl.github.io/dods-ai-dialogue](https://mlatcl.github.io/dods-ai-dialogue/).
That render is the page body (what each stage does), not the live
referia widgets. Personal stores are excluded from the build.

CI is GitHub’s Jekyll Pages workflow
(`.github/workflows/jekyll-gh-pages.yml`). Pushes to `main` run:

```bash
# equivalent of actions/jekyll-build-pages@v1
jekyll build --source ./ --destination ./_site --future
```

`baseurl` is `/dods-ai-dialogue`. Repo Settings → Pages must use
**GitHub Actions** as the source. Pull requests only build; they do
not deploy.

Locally:

```bash
jekyll serve --baseurl /dods-ai-dialogue
```

Open `http://127.0.0.1:4000/dods-ai-dialogue/`. Do not commit `_site/`.

## Setup

Clone this study under a parent directory (conventionally `mlatcl/`):

```bash
mkdir -p mlatcl
cd mlatcl
git clone git@github.com:mlatcl/dods-ai-dialogue.git
cd dods-ai-dialogue
```

HTTPS works the same way if you prefer
(`https://github.com/mlatcl/dods-ai-dialogue.git`).

Referia needs **Python 3.11 or higher**. Check before creating the venv:

```bash
python3 --version
```

That should print something like `Python 3.11.x` or `3.12.x`. If it is
3.10 or older, install a newer Python (for example via
[python.org](https://www.python.org/downloads/) or `brew install python@3.12`
on macOS) and use that interpreter for the steps below
(`python3.12 -m venv .venv`, …).

Create a virtualenv *in this study* and install
[referia](https://github.com/lawrennd/referia) from GitHub `main` (not
the PyPI package: current `pip install referia` is 0.2.0 and does not yet
include the dialogue pipeline or permalink-tree serving). Referia’s LLM
packages are a Poetry group upstream, not a pip extra, so install them
in the same step:

```bash
python3 -m venv .venv
source .venv/bin/activate
python --version   # confirm the venv is still 3.11+
pip install "git+https://github.com/lawrennd/referia.git"
pip install langchain langchain-core langchain-openai langchain-anthropic \
  langchain-text-splitters openai anthropic tenacity diskcache python-dotenv
```

You do not need a local clone of `lawrennd/referia` or `mlatcl/dods`.

Then wire the private working copy:

```bash
cp local.example.yml local.yml
cp _data/corpus/documents.example.yml _data/corpus/documents.yml
# fill local.yml (facilitator names), documents.yml, and files/ from the private store
```

## API key

Extract and grounds call OpenAI (`gpt-4.1-mini` in this study). Referia
reads `OPENAI_API_KEY` from the process environment after loading a
`.env` file. It does not read lynguine credentials. Lynguine’s store
(`~/.lynguine/credentials/`, `LYNGUINE_CRED_*`, `${credential:KEY}` in
a flow) is for named sources such as Google Sheets, not for this LLM
path.

Create a `.env` in this study root:

```
OPENAI_API_KEY=sk-...
```

Referia loads dotenv when the LLM module imports, in this order:

1. A `.env` found by walking up from the current working directory
   (the study root is the usual place when you `cd` here before
   `referia serve`).
2. Otherwise `~/.env`. Use that when the study sits on a network
   filesystem such as OneDrive: walking those trees can time out.

This repo gitignores `.env` and `.venv/`. Do not put the key in a stage
markdown page or in `parameters.yml`.

## Serve

This study is many configs, so use root-server mode (`--root`), not
single-config `--directory`. Default host is `127.0.0.1`, default port
`8000`. From the study root with the venv active:

```bash
source .venv/bin/activate
referia serve --root . --host 127.0.0.1 --port 8000
```

`_config.yml` already sets `referia.urls: permalink`. You can pass
`--urls permalink` to force that mode. Do not serve this study in path
mode: the pages are no longer `_referia.md` inside each stage folder.

Open `http://127.0.0.1:8000/`. Each stage is a filename at the study
root (`/01_turns/` is `01_turns.md`).

## Related

| Layer | Where |
|-------|--------|
| Approach | [mlatcl/dods](https://github.com/mlatcl/dods) |
| Tool | [lawrennd/referia](https://github.com/lawrennd/referia) |
| Paper package | [mlatcl/ai-dialogue-formats](https://github.com/mlatcl/ai-dialogue-formats) |
| This study | this repository |
