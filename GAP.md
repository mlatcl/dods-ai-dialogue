# Gap analysis: referia stages × Jess notebooks × paper

Study: `mlatcl/dods-ai-dialogue` (public configs). Live transcripts stay
in the private referia working copy.
Paper: `referia/2026-10-elicitation-dialogue-paper.docx` (“An elicitation fallacy?”)
Package: `mlatcl/ai-dialogue-formats` (notebooks are thin `Run` wrappers)

Independent reconstruction of the experiments in the paper, for Jess
to tweak via each stage’s `parameters.yml`. Each `_referia.md` quotes
the paper sentence it reconstructs.

Do not treat a completed 01–05 run as a reproduction of the published
numbers until the P0 items are closed.

## Roster facts (no quotes)

| Item | Count | Source |
|------|------:|--------|
| Recollective chatbot files | 2 | `files/chatbot/` |
| Chatbot Participant headings | 111 unique (87 autumn, 24 spring) | heading regex on the two Recollective dumps |
| Chatbot conversations with ≥4-word answers | **110** (`autumn_2025::{pid}` × 86 + `spring_2026::{pid}` × 24) | `01_chunk` after line-split + `min_unit_words: 4` |
| Units kept | **2013** (1003 chatbot, 1010 workshop) | matches paper D3 / `too_short` keep count |
| Workshop DOCX | 38 (17 autumn, 21 spring; 31 breakout, 7 carousel) | `files/workshops/` (`workshop_{round}_{session}_{f0N}.docx`) |
| Paper `[XXX]` chatbot transcripts | fill **110** conversations with analysable answers (111 headings; 112 was a heading-only guess) | D5 / `round::{participant_id}` |
| Paper `[XXX]` workshop transcripts | fill **38** | one file = one document |

## Coverage matrix

| Analysis step | Jess notebook / package | Referia now | Paper uses it? | Status |
|---------------|-------------------------|-------------|----------------|--------|
| Catalog files + round / session / facilitator | `access.load_corpus` | `01_chunk` + `info/documents.yml` | Data section | Ready |
| Chatbot: one unit per answer; bot question as context | `access.parse_chatbot` | `docx_chatbot.v1` now splits Recollective packed-newline turns; extras: `participant_id`, `context`, `extract_text` | D3 | Ready; context not yet concatenated into extract `text` |
| Workshop: ~150-word chunks, split at speaker labels; `[FACILITATOR]` context | `access` + `config/local.yaml` names | `docx_workshop.v1` + `facilitator_names` from gitignored `local.yml` / stage parameters | D3 | Ready |
| Drop units &lt; 4 words | `run_units` `too_short` (2013 kept, 120 dropped) | `min_unit_words: 4` on chatbot and workshop; **2013** units in `info/chunks.yml` | D3 | Ready |
| Assess diagnostics (no model) | `00_assess` | template deferred (chunk quality flags) | Methods (unitisation) | Missing |
| Three-pass extract + `phrase \|\| quote` | `01_extract` | `02_embed` prompt + parser | Extracting CBC | Prompt ready |
| `quote_support ≥ 0.8`; drop quotes from question / facilitator | `extract.py` | `llm_extract_phrases` scores quotes; `quote_support_threshold: 0.8` in `02_embed/parameters.yml` | D2; only verified points analysed | Ready (extracted; 27 unverified in pack) |
| Format-conditional unit frame (bot asked / `[FACILITATOR]`) | `prompts.unit_frame` | single `<<TEXT>>`; workshop `text` has tags; chatbot `text` is the answer only | D2 / D3 | Partial |
| Embed `text-embedding-3-large` | `02_cluster` | `02_embed` | Identifying themes | Ready |
| Shared k=40 k-means, frozen assignments, k=25/60 | `02_cluster` / `robust` | `03_vq` `n_vq: 40` (VQ + later MPPCA lenses, not frozen k-means) | D4; sensitivity subsection | Analogue, not identical |
| Blind cluster labels; 3 lens runs; optional researcher mapping | `02_cluster` | `04_grain` interactive Name | D4 | Partial (no 3-run freeze) |
| Document-weighted type/lens/cluster shares + cluster bootstrap | `03_part_a` `compare.py` | `06_compare` `run_format_share_compare` (05 is EMD on the same `P`) | Table 1, Figure 1, JSD 0.006 | Ready (current grain, not frozen k=40) |
| JSD on format topic mix | `stats` / `soft_lenses` | `06_compare` JSD base 2 | Results: JSD = 0.006 | Ready as analogue |
| Seven grounds codes | `04_part_b` `grounds.py` | `07_grounds` `llm_classify_grounds` | Table 2; 17.7% vs 4.1% experience | Ready to run (LLM) |
| Question-type stress test (0.3% experience questions) | `grounds.question_types` | `08_questions` regex | Results paragraph | Ready |
| Labelled workshop speaker turns | `access.Labels` / `build_turns` | `01_turns` `run_rebuild_speaker_turns` | Exploratory (grain for 10) | Ready (run Rebuild + Save) |
| Stories-follow-stories (labelled spring speaker turns) | `sequence.py` via `05_validation` | `10_sequence` on `turns.yml` + 07 codes | Exploratory analysis | Reconstructed (17 files / 2126 turns; story holds) |
| Word-list floor | `05_validation` | `09_validate` `run_wordlist_floor` | Validation of experience coding | Ready |
| Reconstruct extract `kind` (BoW CV) | not in `Run` | `siding_kind` `run_kind_reconstruction` | Consistency of CBC labels | Ready (siding) |
| Reconstruct Part B `basis` (BoW CV) | not in `Run` | `siding_basis` `run_basis_reconstruction` | Consistency of grounds codes | Ready (siding; needs Classify all) |
| Reconstruct hard grain lens (BoW CV) | not in `Run` | `siding_lens` `run_lens_reconstruction` | Are this grain's lenses lexical? | Ready (siding; argmax QR, not Name) |
| Own-words recode (format-blind; same / reworded / gpt-4.1) | `validate.py` | waits on a later coding pass (09 is word-list only) | D6 | Waiting |
| Blind hand-check sheets | `validation_playbook.md` | waits on human review | Human validation | Waiting |
| k=25/60 + 3 lens runs | `06_multiverse` / `robust` | refit `03_vq` → `04_grain` → `06_compare` | Stability of thematic analysis | Waiting (other stages) |
| Analysis-choice product (main-run codes) | `06_multiverse` | `11_multiverse` `run_analysis_multiverse` | Sensitivity across definitions / weights / exclusions | Page ready; **not yet run** (216 configs on main-run 07; not 1080 LLM jobs) |
| Qualitative chatbot-reflection coding | not in `Run` (manual in paper) | not a stage | “Experiences with the chatbot…” | Out of band |
| Fingerprinted checkpoints / replay | `llm.StageRunner` | LLM diskcache is cost-only | Reproducibility of canonical run | Different contract |

## P0 — paper numbers would be wrong

1. **Chatbot document grain.** Closed in config and in `info/chunks.yml`.
   `segment_dialogue_units` stamps `doc_id` as `{round}::{participant_id}`
   on chatbot units (110 conversations) and `filename` on workshops (38).
   Recollective participant numbers overlap across rounds, so bare
   `participant_id` is not unique. Extract coalesces the same grain.
2. **Verified quotes only.** Closed in extract compute, not yet run.
   `quote_support_threshold: 0.8` drops unverified quotes and quotes
   that match the bot question / facilitator but not `extract_text`.
   Do not claim CBC percentages until Extract all has been run.
3. **Part B is 07_grounds, not 04_grain.** Experience 17.7% vs 4.1%,
   principle 91.6% vs 68.9%, others’ experience 4.7% vs 1.5% come from
   basis coding. Classify all, then Save, then read `info/grounds.yml`.
   Until that run, do not quote those percentages from this study.

## P1 — same question, different estimator

- Paper clusters **phrases** with k-means k=40 then groups clusters into
  lenses. Referia VQ’s the embeddings (`n_vq: 40`) then fits MPPCA
  lenses on centroids. Topic labels can be named in `04_grain`; they
  will not match `cluster_assignments_k40.csv`.
- Paper reports **JSD** and document-weighted bootstrap CIs. `06_compare`
  now computes those on the current grain. `05_distance` remains **EMD /
  MDS / permutation tests** on `P`. The published 0.006 is Jess’s 11
  lenses; 06 will print a different figure.
- Chatbot extract prompt does not yet wrap the bot’s question as
  “context only — extract nothing from this”.
- Chatbot units shorter than 4 words are dropped (`min_unit_words: 4`).
  One autumn heading produced no kept answers, so conversation grain is
  110 rather than the heading-only 111 (or the draft placeholder 112).

## P2 — deferred on purpose

Own-words recode and hand-check sheets wait on a later coding pass /
human review. k=25/60 is a refit of 03 → 04 → 06. Qualitative
chatbot-reflection coding stays out of band. Canonical fingerprints
remain `dialogue_formats.Run(replay=True)` in the public package.

## Paper draft validity (writing, not pipeline)

Placeholders still in the Word file:

| Placeholder | Action |
|-------------|--------|
| `[XXX]` chatbot / workshop transcript counts | 112 conversations, 38 workshop files |
| `[INCENTIVES TO JOIN]`, `[CONDITIONS]` | recruitment incentive wording |
| Facilitators were briefed to `[WHAT]` | facilitator brief |
| `[CONSENT FOR ANALYSIS]` | fill from the study protocol; transcripts have no participant names |
| Human validation `[COMPLETE AFTER CODING.]` | wait for sheets; do not imply it is done |
| Appendix 1 `????` | empty |
| `[INSERT FIGURE/TABLE…]` | figures live in package `outputs/` (quotes; not in git) |

Draft prose: the Data section states the 4-word exclusion and the 2013-unit
count twice. Workshop unitisation is “paragraph breaks”; the code splits
at speaker labels then chunks to 150/260 words.

Headline numbers in the draft (JSD 0.006; CBC ~37/36/26 both formats;
experience 17.7 vs 4.1) are from the **canonical Jess run**, not from
this referia study. They stay valid only while that run (fingerprints +
checkpoints) is the source. A new referia extract will not reproduce
them bit-for-bit even after P0, because clustering and lens grouping
differ (P1).

## Suggested order of work

1. ~~Segment `01_chunk` (local, no API).~~ Done: 2013 units; 110 chatbot
   conversations + 38 workshops. Recollective transcripts are packed as
   one newline-separated paragraph per participant — `docx_chatbot.v1`
   now splits those lines (needs the lynguine checkout / venv copy).
2. ~~Coalesce pack `doc_id` (P0.1).~~ Done in `segment_dialogue_units`
   and extract coalesce.
3. ~~Add `quote_support` drop (P0.2).~~ Wired at `0.8`; not extracted.
4. ~~Extract / Embed / VQ / grain.~~ Done (64-cell codebook, 5 lenses).
5. Run `06_compare` (no API) for Part A analogue tables. Run `05_distance`
   if you want EMD geometry as well.
6. Run `07_grounds` Classify all + Save when you intend to spend API
   cost (~1888 calls; CIP-001D). Then 08 / 09. `siding_basis` stays
   empty until that run (`grounds.yml` is currently one Classify).
7. Optional: `siding_kind` / `siding_lens` after 02 / 04 Save (no API).
8. Canonical paper numbers stay on `Run(replay=True)` until you
   deliberately replace them with this grain.
