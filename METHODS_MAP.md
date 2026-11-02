# Methods map for Jess — paper methods × referia stages

**To:** Jess  
**From:** Neil / DODS reconstruction (`mlatcl/dods-ai-dialogue`)  
**Date:** 2026-11-02  
**Paper:** *An elicitation fallacy? Exploring the role of AI in public dialogue*

This note restates **your methods** as you analysed them, broken into the
sub-sections of the live reconstruction pipeline. It is a map for review
and tweaking (`parameters.yml` on each stage), not a second Methods
section for the paper and not a claim that this grain replaces your
canonical numbers.

How to read each block:

| Column | Meaning |
|--------|---------|
| **Your method** | What the paper / package run does |
| **This stage** | Where the reconstruction lives |
| **Estimator note** | Same idea, or deliberate analogue |
| **This grain (now)** | Current study output, if already run |
| **Your published figure** | Canonical paper / Jess-run number |

Published headlines stay labelled as **your run** unless you choose to
replace them. Clustering and lens grouping here are analogues (VQ +
MPPCA lenses), not a bit-for-bit replay of frozen k-means k=40.

Detail tables and gap status: [`GAP.md`](GAP.md). Stage knobs: each
page’s `_data/<stage>/parameters.yml`.

---

## 0. Roster and document grain

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Catalog chatbot + workshop files; round / session | `01_chunk` + `_data/corpus/documents.yml` | Same Access | 2 Recollective dumps; 38 workshop DOCX | Fill paper `[XXX]` from protocol |
| Chatbot: one conversation = one document; answer units with bot question as context | `01_chunk` (`docx_chatbot.v1`) | `doc_id` = `{round}::{participant_id}` | **110** conversations with ≥4-word answers (111 headings) | Chatbot transcript count in Data |
| Workshop: chunk at speaker labels; ~150-word units; facilitator tagged | `01_chunk` (`docx_workshop.v1`) | Facilitator names from `local.yml` | **38** documents | Workshop transcript count |
| Drop units shorter than 4 words | `min_unit_words: 4` | Same rule | **2013** units kept (1003 chatbot, 1010 workshop) | D3 / `too_short` keep count |

Document-equal weighting later (Part A/B) uses these `doc_id`s: 110
chatbot + 38 workshop.

---

## 1. Extracting concerns, benefits, and conditions

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Three-pass LLM extract; phrase with supporting quote | `02_extract` | Same Address; prompts in stage parameters | Pack extracted | Extracting CBC |
| Keep only verified quotes (`quote_support`); drop question / facilitator matches | `02_extract` (`quote_support_threshold: 0.8`) | Wired and applied on current pack | 27 unverified dropped in pack notes | Only verified points analysed |
| Format-conditional unit frame (bot asked / facilitator) | Partial | Workshop `text` carries tags; chatbot `text` is the answer; bot question not yet forced as “context only — extract nothing” | — | D2 / D3 |

---

## 2. Identifying themes (embeddings → topics → lenses)

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Embed phrases (`text-embedding-3-large`) | `02_embed` | Same | Packed corpus | Identifying themes |
| Shared k=40 clustering of phrases; freeze assignments; sensitivity k=25/60 | `03_vq` (`n_vq: 40`) | **Analogue:** vector quantisation of embeddings, not frozen k-means on your checkpoint | 64-cell codebook in current run notes | D4; robustness subsection |
| Group clusters into substantive lenses; blind labels; optional multi-run mapping | `04_grain` | Interactive Name; no three-run freeze | **5** named lenses on this grain | Your 11-lens map on k=40 |

**Not in the paper (extra geometry):** `05_distance` — EMD / MDS /
permutation tests on the same document–topic matrix `P`. The paper’s
similarity story uses JSD in Part A, not EMD.

---

## 3. Part A — do the formats elicit similar agendas?

**Question.** Did chatbot and workshop sessions draw out similar
distributions of concerns, benefits, conditions, and thematic lenses?

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Document-weighted CBC (concern / benefit / condition) mix; equal weight per document; workshop − chatbot; cluster bootstrap over documents | `06_compare` | Same estimator on **this** extract + grain | CBC ≈ 32.3 / 33.0 / 34.7 chatbot vs 32.5 / 32.1 / 35.4 workshop; no clear w−c gaps | ≈ 37.3 / 36.4 / 26.3 vs 36.7 / 36.2 / 27.1 |
| Document-weighted lens shares + bootstrap | `06_compare` | Same idea; **different catalogue** (5 lenses here vs 11 there) | Lens table in `part_a.yml` | Figure 1 / Table 1 lenses |
| Jensen–Shannon divergence on document-mean lens profiles (base 2); compare to format-label shuffle where reported | `06_compare` | Same estimator; coarser catalogue shrinks JSD | **JSD ≈ 0.0035** | **JSD = 0.006** |

**Paper story this block is for:** different dialogue modes produced
broadly similar substantive agendas.

Do not overwrite your published CBC / JSD with this grain without saying
so. Agreement of *direction* (similar agendas) is the reconstruction
claim; bit-identical Table 1 is not expected under P1.

---

## 4. Part B — what does each point rest on?

### 4.1 Coding the evidential basis

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Classify each extracted point into seven bases (personal experience, others’ experience, professional knowledge, principle, public example, project materials, unclear) | `07_grounds` (`llm_classify_grounds`) | Same Address; model default gpt-4.1-mini | `grounds.yml` filled (Classify all + Save done) | Table 2 coding scheme |

Coding unit = extract point. Sampling unit for shares = document.

### 4.2 Document-weighted shares and the experience gap

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Per document: histogram of basis codes among its points; format mean = mean of those compositions; experience = personal + others; cluster bootstrap over documents; workshop − chatbot | `07_part_b` (`run_basis_share_compare`) | Same estimator on current `grounds.yml` | **Experience: workshop 22.9% vs chatbot 5.7%** (w−c 17.2; 95% CI 13.6–21.2) | **17.7% vs 4.1%** (w−c 13.6) |
| Professional knowledge share (same weighting) | `07_part_b` | Same | Workshop 3.1% vs chatbot 0.3% (not “clear” at min_gap 3) | Table 2 professional row |
| Full seven-way basis mix | `07_part_b` | B1 table | In compute / (Save writes `part_b.yml`) | Table 2 |

**Paper story this block is for:** workshop contributions more often
grounded in experience; chatbot contributions typically in general
principles.

Same *direction* as your headline; levels differ on this extract grain.
Persist `part_b.yml` via Compute + Save on `/07_part_b/` if the file is
still absent from `_data/corpus/`.

### 4.3 Was the gap because the bot asked for stories?

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Classify chatbot *questions* by type of response sought; share that ask directly for experience | `08_questions` (regex on preceding bot question) | Local patterns; no model | **0.3%** of chatbot units | **~0.3%** |
| Experience rate after “example” questions vs other questions | Partially in paper prose | This stage reports how often the bot *asked*; answer grounding still from 07 | Example questions 11.3% of units | 10.7% vs 5.5% after example vs other (your results paragraph) |

**Paper story:** the experience gap is not explained by the bot asking
for stories.

### 4.4 Transparent floor on experience language

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Word list of explicit personal / others’ experience markers in supporting quotes | `09_validate` (`run_wordlist_floor`) | Floor only; misses coded experience without those words | Word-list hits: workshop **4.1%** vs chatbot **1.0%** of points; LLM experience codes 7.1% overall | Validation subsection |
| Format-blind own-words recode of a sample (~300) | — | **Not this page** | Waiting | D6 |
| Blind hand-check sheets | — | Human review | Waiting | Human validation |

### 4.5 Stories follow stories (workshop sequence)

| Your method | This stage | Estimator note | This grain (now) | Your published figure |
|-------------|------------|----------------|------------------|------------------------|
| Labelled spring workshop speaker turns; place experience-grounded points; look-back L = 1…5 vs within-transcript shuffle | `01_turns` (Access) + `10_sequence` (Address) | Main-run 07 codes; no quote text stored | **17** files, **2126** turns; observed > shuffled (story holds); within-topic blank until topic ids on points | 16 transcripts, 2025 turns; “some indication” stories follow stories |

---

## 5. Sidings (not in the paper)

Off the main line. Consistency checks on *this* coding, not experiments
to hand back as yours.

| Check | Stage | What it asks | This grain (now) |
|-------|-------|--------------|------------------|
| Recover extract CBC kind from text (BoW CV) | `siding_kind` | Are kind labels lexical? | Artefact `kind_check.yml` present |
| Recover Part B experience vs rest from quote + phrase | `siding_basis` | Are experience codes recoverable linearly? | Balanced accuracy **0.789** vs chance 0.5 (`basis_check.yml`) |
| Recover hard grain lens (argmax QR) | `siding_lens` | Are lenses lexical on this grain? | Artefact `lens_check.yml` present |

---

## 6. Sensitivity / multiverse (page ready; not the focus here)

| Your method | This stage | Status |
|-------------|------------|--------|
| k=25/60 and multi-run lens stability | Refit `03_vq` → `04_grain` → `06_compare` | Waiting |
| Analysis-choice product over definitions / weights / exclusions | `11_multiverse` | Page ready; **not yet run** |

---

## 7. What this reconstruction is *not*

- Not a replay of fingerprinted `Run(replay=True)` checkpoints.
- Not bit-identical Table 1 / Table 2 (different clustering + lens
  catalogue; different extract grain even when the estimator matches).
- Not complete human validation (own-words recode and hand-check sheets
  still waiting).
- Not qualitative “experiences with the chatbot” coding (out of band in
  the paper).

---

## 8. One-page number card (for side-by-side reading)

| Claim | Your published figure | This grain (now) |
|-------|----------------------:|-----------------:|
| Units kept (≥4 words) | 2013 | 2013 |
| Chatbot documents | (fill Data) | 110 |
| Workshop documents | 38 | 38 |
| Part A JSD (lens profiles) | 0.006 | 0.0035 |
| Part A CBC chatbot (C/B/Co) | 37.3 / 36.4 / 26.3 | 32.3 / 33.0 / 34.7 |
| Part A CBC workshop (C/B/Co) | 36.7 / 36.2 / 27.1 | 32.5 / 32.1 / 35.4 |
| Part B experience workshop vs chatbot | 17.7 vs 4.1 | 22.9 vs 5.7 |
| Bot questions asking for experience | ~0.3% | 0.3% |
| Stories-follow-stories | holds (your prose) | holds (gap vs shuffle) |

---

## 9. Suggested reading order for you

1. This file (map).
2. Live stages in seq order, especially `06_compare`, `07_part_b`,
   `08_questions`, `09_validate`, `10_sequence`.
3. `GAP.md` for status and deliberate differences (P1).
4. Sidings only if you want lexical consistency diagnostics.

Tweaks that change a table belong in that stage’s `parameters.yml`, then
re-Compute / Save — not in a one-off notebook cell.
