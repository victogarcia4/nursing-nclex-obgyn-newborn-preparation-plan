# BUILD SPECIFICATION — Maternal/Newborn Teaching Resource Suite
## A model-agnostic execution plan for any LLM

**Owner:** Victor Sanchez, MSN, FNP-C, RN — guest faculty, Lone Star College–North Harris
**Courses covered:** RNSG 1523 Nursing I (Antepartum) · RNSG 2514 Nursing III (Complications of Pregnancy and Childbirth)
**Terminal goal:** a complete, exam-aligned resource suite that reliably moves cohort performance to **≥ 80% on Next Generation NCLEX (NGN)-style assessment** of these two units.
**Input artifacts (already exist — treat as canonical):**
- `RNSG1523_Antepartum_LessonPlan_Expanded_APA.md`
- `RNSG2514_Complications_LessonPlan_APA.md`

---

## 0. HOW TO USE THIS DOCUMENT

This is a **build spec, not a lesson plan.** It is written so that any capable LLM — with no memory of the prior conversation — can execute any single work order in it, in isolation, and produce an artifact that fits the rest of the suite.

**Rules for the executing model:**
1. Read the two canonical lesson plans first. They define scope, sequencing, terminology, and the reference list. **Do not introduce content outside them** without flagging it as an addition.
2. Execute **one work order at a time.** Do not batch. Each work order names its inputs, outputs, format, and acceptance criteria.
3. **Source policy is non-negotiable** (§2). If you cannot verify a clinical claim against an approved source, do not state it — flag it in a `## VERIFY` block at the end of the artifact.
4. **Never fabricate a citation, a DOI, a page number, a guideline number, or a statistic.** If uncertain, write `[VERIFY: <what to check> — <where>]` inline.
5. Output every artifact as a **standalone file** with the naming convention in §3. No conversational preamble inside the file.
6. If a work order's instructions conflict with the canonical lesson plans, **the lesson plans win** — and note the conflict.

**Honest framing of the goal.** No resource set can guarantee a score. What this suite can do is (a) align instruction to the actual NGN measurement model, (b) generate enough calibrated practice to make performance predictable, and (c) instrument the cohort so weak areas are found *before* the exam rather than after. The 80% target is operationalized in §7 as measurable proxies, not as a promise.

---

## 1. THE DELIVERABLE INVENTORY

Twelve artifact families. Build in the order given — later families consume earlier ones.

| # | Artifact family | Per course | Priority | Depends on |
|---|---|---|---|---|
| **A** | Exam blueprint & competency map | 1 | **P0** | Lesson plans |
| **B** | Terminology & abbreviation master deck (flashcard-ready) | 1 | P1 | Lesson plans §1 |
| **C** | Slide decks (4 sessions each) | 4 | **P0** | A |
| **D** | Faculty facilitation guide (talk track, timing, board work) | 4 | P1 | C |
| **E** | Student handouts / skeletal notes | 4 | P1 | C |
| **F** | NGN item bank (calibrated, tagged) | 1 large | **P0** | A |
| **G** | Unfolding case studies (multi-item NGN case sets) | 6–8 | **P0** | A, F |
| **H** | Exit tickets + daily formative checks | 4 | P1 | F |
| **I** | High-yield comparison tables & mnemonic sheets | 1 | P2 | B, C |
| **J** | Simulation / skills drill scripts | 3–4 | P2 | Lesson plans |
| **K** | Post-exam remediation deck (generated *after* item analysis) | 1 | **P0** | Real exam data |
| **L** | Student self-study pathway + spaced-repetition schedule | 1 | P2 | B, F, I |

**P0 = must exist before teaching.** P1 = should exist. P2 = value-add.

---

## 2. SOURCE POLICY (applies to every artifact)

**Approved sources only:**
- U.S. federal agencies: ACOG-adjacent federal bodies, CDC/MMWR, FDA, USPSTF, NIH/NICHD, AHRQ, USDA
- Professional society clinical guidance: ACOG (Practice Bulletins, Committee Opinions, Clinical Practice Guidelines, Obstetric Care Consensus), SMFM, AWHONN, AAP/AHA (NRP), The Menopause Society
- Peer-reviewed journal articles
- National Academies (NASEM/IOM) consensus reports
- Published nursing textbooks (department-adopted edition)
- NCSBN official publications for anything about NGN itself

**Prohibited:** UpToDate as a primary student citation, commercial NCLEX-prep publishers, Wikipedia, Studocu/Course Hero/Quizlet, nursing blogs, YouTube channels, any secondary site restating guideline content, and AI-generated summaries of any of the above.

**Citation format:** APA 7th edition. Reuse the exact reference entries already validated in the two lesson plans — do not re-derive them.

**Currency flags to carry into every artifact** (these are known-unstable; restate the flag rather than silently picking a side):
- ACOG 2024 Clinical Practice Update supersedes parts of PB 190 (diabetes screening thresholds)
- ACOG 2025 intrapartum FHR guideline: **recommends against routine maternal oxygen** for Category II/III absent maternal hypoxia; supersedes PB 106/116; document-number discrepancy unresolved
- 17-OHPC (Makena) withdrawn from U.S. market 2023
- NRP edition currency
- SMFM Consult Series #74 (cfDNA) layered onto PB 226
- Texas statute on abortion, fetal remains disposition, and minors' consent — **never state Texas law from model knowledge; always flag for local verification**

---

## 3. FILE NAMING & FORMAT CONVENTIONS

```
<COURSE>_<ARTIFACT>_<SCOPE>_v<N>.<ext>
```
Examples:
- `RNSG1523_Blueprint_Unit_v1.md`
- `RNSG1523_Slides_Day2_v1.md`
- `RNSG2514_ItemBank_Hemorrhage_v1.json`
- `RNSG2514_Case_CordProlapse_v1.md`

**Formats:**
- Blueprints, guides, handouts, cases → **Markdown**
- Item banks → **JSON** (schema in §5.3) **plus** a human-readable Markdown mirror
- Slides → Markdown with `---` slide breaks (convertible to PPTX/Gamma/Canva downstream)
- Flashcards → CSV (`front,back,tag,difficulty`) for Anki/Quizlet import

**Bilingual note:** all student-facing artifacts (E, H, I, L) should be producible in **English and Spanish**. Generate English first; Spanish is a separate work order, translated for *clinical accuracy*, not literalness. Clinical terms keep the English term in parentheses on first use.

---

## 4. PHASED EXECUTION ROADMAP

### Phase 0 — Alignment (human work, blocks everything)
Cannot be done by an LLM. Obtain from Dr. Sharma before generating P0 artifacts:
- Departmental PowerPoints and curriculum grid
- **Exam blueprint** (item counts by topic and cognitive level)
- Item-analysis criteria (p-value ranges, point-biserial thresholds)
- Required textbook and **edition**
- Convention decisions: GTPAL vs GPTAL · PROM as "premature" vs "prelabor" · legacy pregnancy letter categories vs PLLR
- Whether test-bank items must be original or drawn from a publisher bank

**Until Phase 0 completes, LLM work should proceed on artifacts A, B, F, G, I — which are blueprint-shaped but not blueprint-dependent — and be revised after.**

### Phase 1 — Foundation (Artifacts A, B)
### Phase 2 — Instruction (C, D, E)
### Phase 3 — Assessment (F, G, H)
### Phase 4 — Reinforcement (I, J, L)
### Phase 5 — Response (K, post-exam only)

---

## 5. WORK ORDERS

Each work order is self-contained. Copy the whole block into a fresh LLM session along with the relevant lesson plan.

---

### WO-A · Exam Blueprint & Competency Map

**Input:** the course's lesson plan.
**Output:** `<COURSE>_Blueprint_Unit_v1.md`

**Instructions to the model:**
Build a table with one row per teachable objective. Columns:

| Objective ID | Session | Topic | Curriculum thread(s) | NCJMM operation | Bloom level | NCLEX Client Needs category | Target item count | Source citation |

Rules:
- Objective IDs: `<COURSE>-D<day>-<n>` (e.g., `1523-D2-3`)
- **NCJMM operations** (use exactly these six): Recognize Cues · Analyze Cues · Prioritize Hypotheses · Generate Solutions · Take Actions · Evaluate Outcomes
- **Client Needs categories** (2023 NCLEX-RN Test Plan): Management of Care · Safety and Infection Control · Health Promotion and Maintenance · Psychosocial Integrity · Basic Care and Comfort · Pharmacological and Parenteral Therapies · Reduction of Risk Potential · Physiological Adaptation
- Weight item counts toward **Take Actions and Prioritize Hypotheses for RNSG 2514**, and toward **Recognize Cues and Generate Solutions for RNSG 1523** — this mirrors the two units' clinical character.
- End with a **coverage audit**: any objective with zero planned items, any thread appearing fewer than 3 times, any NCJMM operation under-represented.

**Acceptance criteria:** every topic in the lesson plan appears ≥ once; all six NCJMM operations appear; total target item count between 60–90 per course.

---

### WO-B · Terminology Master Deck

**Input:** lesson plan §1 (abbreviation glossary) + §1.8 (terminology corrections, Nursing III only).
**Output:** `<COURSE>_Terms_v1.csv` + `<COURSE>_Terms_v1.md`

**Instructions:**
- One card per term. `front` = abbreviation or term; `back` = full term + one-clause clinical significance; `tag` = domain from the glossary section; `difficulty` = 1–3.
- Add a second card type for **discrimination pairs** (PROM vs PPROM, previa vs abruption, FGR symmetric vs asymmetric, Category I/II/III, gHTN vs preeclampsia): front = "Distinguish X from Y"; back = the single most decisive differentiator, not a paragraph.
- Add **mnemonic cards**: ACHES, PATCH, GTPAL, VEAL CHOP, 4 Ts, 5 Ps, HELPERR — front = mnemonic, back = expansion + when it fires.
- Include a **"say this, not that"** card set from the Nursing III terminology-correction table.

**Acceptance:** ≥ 120 cards per course; no card longer than 25 words on the back.

---

### WO-C · Slide Deck (one work order per session — 8 total)

**Input:** the session's section of the lesson plan + `<COURSE>_Blueprint_Unit_v1.md`
**Output:** `<COURSE>_Slides_Day<N>_v1.md`

**Instructions:**
Follow the session architecture already in the lesson plan (hook → content 1 → AL1 → break → content 2 → AL2 → exit ticket). Slide budget for 140 minutes: **35–45 content slides maximum.**

Per slide:
- One idea. Title is a **claim**, not a label ("Proteinuria is not required to diagnose preeclampsia" beats "Preeclampsia Diagnosis").
- ≤ 6 lines of text. Tables allowed and encouraged — this content is comparison-heavy.
- Speaker-notes block under each slide (`> NOTES:`) with the talk track, the question to ask the room, and the common student error to preempt.
- Every clinical claim carries a bracketed source tag: `[ACOG PB 222]`, `[CDC US MEC 2024]`.

Mandatory slide types to include in every deck:
1. **Objectives** slide (from blueprint, verbatim)
2. **Thread map** slide showing which curriculum threads this session hits
3. At least two **comparison tables**
4. At least one **"first action"** slide (a scenario, four options, the answer, and *why the other three fail*)
5. **Exit ticket** slide
6. **Sources** slide (APA, from the lesson plan's reference list)

**Acceptance:** slide count in range; every content slide has notes; no uncited clinical claim.

---

### WO-D · Faculty Facilitation Guide

**Input:** the matching slide deck.
**Output:** `<COURSE>_FacGuide_Day<N>_v1.md`

**Instructions:** Produce a minute-by-minute run sheet: cumulative clock, slide range, activity, materials needed, and a **"if you're running 15 minutes behind, cut this"** column. Add a *Predicted Student Misconceptions* section (≥ 6 per session) with the correction script. Add board-work diagrams to draw live (described in words). Add three cold-call questions per content block.

---

### WO-E · Student Handout / Skeletal Notes

**Input:** the matching slide deck.
**Output:** `<COURSE>_Handout_Day<N>_v1.md`

**Instructions:** Guided notes with strategic blanks — students write the **discriminating detail**, never the connective tissue. Include all comparison tables with 30–40% of cells blank. Include the day's mnemonics with expansions blanked. End with the exit ticket and a "before next session" checklist. Two-page maximum per session.

---

### WO-F · NGN Item Bank

**Input:** blueprint + lesson plan.
**Output:** `<COURSE>_ItemBank_v1.json` + Markdown mirror

**This is the highest-leverage artifact. Build it most carefully.**

**5.3 — Required JSON schema per item:**
```json
{
  "id": "1523-D3-012",
  "objective_id": "1523-D3-2",
  "item_type": "bowtie|trend|matrix_grid|matrix_multiple_choice|extended_multiple_response|extended_drag_drop|cloze_dropdown|highlight|standalone_mc|sata",
  "ncjmm_operation": "Recognize Cues",
  "client_needs": "Reduction of Risk Potential",
  "bloom": "Analyze",
  "difficulty_target": "easy|moderate|hard",
  "stem": "...",
  "chart_data": { "vital_signs": "...", "labs": "...", "nurses_notes": "..." },
  "options": [...],
  "key": [...],
  "scoring": "0/1|+/-|rationale",
  "rationale_correct": "...",
  "rationale_distractors": { "B": "why this is wrong and what it would be right for" },
  "source": "ACOG PB 222 (2020)",
  "keywords": ["preeclampsia", "severe features"]
}
```

**Item-writing rules — enforce all of them:**
1. **Stems must present data, not conclusions.** Give the assessment findings and let the student conclude. Never write "The client has preeclampsia with severe features. What should the nurse do?" — that removes the measured skill.
2. Use a **realistic chart format**: nurses' notes, vital signs flowsheet, lab results with reference ranges, provider orders. NGN items are chart-driven.
3. **Every distractor must be plausible to an under-prepared student** and must be a correct action *in some other scenario*. State that scenario in `rationale_distractors`.
4. **No "all of the above," no negatively-worded stems, no absolutes** ("always," "never") in options.
5. **Trend items** must include ≥ 3 time points and require noticing change, not reading a single value.
6. **Bowtie items** need exactly: 2 actions to take, 1 condition, 2 parameters to monitor — with more options than slots.
7. Distribution target per course: 40% moderate, 30% easy, 30% hard.
8. Distribution by NCJMM operation must match the blueprint's weighting.
9. **Rationales are the product.** A student learns from the rationale, not the item. Write each correct rationale in 2–4 sentences ending with the transferable principle.
10. Include the **source citation** on every item.

**Priority topics for over-sampling** (these predict exam failure):
- *Nursing I:* GTPAL calculation · Naegele's rule · presumptive/probable/positive · screening vs diagnostic timing · Rh(D) immune globulin triggers · warning signs vs normal discomforts · legacy categories vs PLLR
- *Nursing III:* magnesium toxicity sequence · previa vs abruption · uterotonic contraindications · cord prolapse action ordering · FHR category management (including the oxygen reversal) · preeclampsia without proteinuria · tachysystole response · antenatal corticosteroid windows

**Acceptance:** ≥ 60 items per course; all nine item types represented; every item traces to an objective ID; no item without a distractor rationale.

---

### WO-G · Unfolding Case Studies

**Output:** `<COURSE>_Case_<Topic>_v1.md`, 6–8 per course.

**Instructions:** Each case = **6 linked items**, one per NCJMM operation, in order, following a single patient across a deteriorating timeline. This is the exact NGN case-study format.

Structure:
- **Scene 1** (Recognize Cues): initial presentation, chart data, highlight/matrix item
- **Scene 2** (Analyze Cues): new data 2–4 hours later, matrix or drag-drop
- **Scene 3** (Prioritize Hypotheses): cloze/dropdown
- **Scene 4** (Generate Solutions): extended multiple response
- **Scene 5** (Take Actions): drag-and-drop ordering or SATA
- **Scene 6** (Evaluate Outcomes): trend item across the whole encounter

Required cases:
- *Nursing I:* prenatal visit with rising BP · Rh-negative client across pregnancy · adolescent contraception counseling · abnormal quad screen counseling · GDM diagnosis and teaching · warning-sign triage call
- *Nursing III:* PPH after vaginal birth · preeclampsia → HELLP progression · PPROM at 30 weeks · cord prolapse · uterine rupture during TOLAC · IUFD and bereavement · GDM in labor + neonatal hypoglycemia · dystocia and failed induction

**Add a debrief section** to each case: the three decision points where students most commonly go wrong, and what the correct reasoning was.

**Acceptance:** each case has exactly 6 scenes mapping to the 6 operations; the patient's data is internally consistent across scenes (check dates, gestational age, lab trends).

---

### WO-H · Exit Tickets & Daily Formative Checks

**Output:** `<COURSE>_ExitTickets_v1.md`

Per session: the lesson plan's stated exit ticket, expanded to **5 items** (3 recall, 2 application), with an answer key and a **remediation pointer** (which slide, which source) per item. Add a 3-question pre-session "prior knowledge" poll for each day.

---

### WO-I · High-Yield Sheets

**Output:** `<COURSE>_HighYield_v1.md`

One page per theme, table-dominant, no prose paragraphs:
- *Nursing I:* contraception method comparison · screening/diagnostic timeline (gestational age axis) · discomfort vs warning sign · pregnancy medication categories + PLLR crosswalk · GTPAL worked examples · lab values in pregnancy vs non-pregnant reference ranges
- *Nursing III:* previa vs abruption · the 4 Ts · uterotonic drug card (dose, route, contraindication) · magnesium sulfate card · FHR category → action algorithm · VEAL CHOP · tocolytic comparison · emergency action sequences (cord prolapse, shoulder dystocia, uterine rupture, PPH)

Each sheet ends with **"the three things most likely to be tested."**

---

### WO-J · Simulation / Drill Scripts

**Output:** `<COURSE>_Sim_<Scenario>_v1.md`

For: PPH escalation · magnesium safety check · cord prolapse · SBAR to provider.
Include: learning objectives, setup, role assignments, timeline of programmed changes, expected actions checklist, **and a debrief guide structured on the Lasater Clinical Judgment Rubric dimensions** (noticing, interpreting, responding, reflecting).

---

### WO-K · Post-Exam Remediation Deck (Phase 5 — after real data exists)

**Input:** departmental item analysis (p-values, point-biserial), plus aggregated exit-ticket errors.
**Output:** `<COURSE>_Remediation_v1.md`

**Instructions:**
- Rank items by **lowest p-value** and by **point-biserial below the department's threshold** (low discrimination = the item may be flawed, not the students).
- For each high-miss concept: one slide re-teaching the concept from a *different angle than the original lecture* (if it was taught as a table, re-teach as an algorithm; if as an algorithm, re-teach as a case).
- Add 2 fresh practice items per high-miss concept, drawn from the item bank's unused pool.
- Add a **faculty note** distinguishing *student knowledge gaps* from *item construction problems* — do not remediate students for a bad distractor.

---

### WO-L · Student Self-Study Pathway

**Output:** `<COURSE>_StudyPath_v1.md`

A dated schedule across the three weeks: what to read before each session, which flashcard deck to run when, spaced-repetition intervals (day 1, 3, 7, 14), which case study to attempt after which session, and a self-assessment checkpoint before the exam with a "if you score under X, do Y" branch.

---

## 6. QUALITY GATES

Run these checks on every artifact before it is considered done. An LLM can self-run all of them.

**Gate 1 — Citation integrity.** Every clinical claim has a source tag. Every source tag resolves to an entry in the lesson plan's reference list. No invented DOIs, page numbers, or guideline numbers. All `[VERIFY]` flags are collected at the end of the file.

**Gate 2 — Blueprint traceability.** Every item, slide, and case traces to an objective ID. No orphan content. No objective with zero coverage.

**Gate 3 — Terminology consistency.** Current terms used throughout (prelabor not premature ROM; preeclampsia with severe features not severe preeclampsia; FGR not IUGR in clinical language; Category II/III not "nonreassuring"). Abbreviations expanded on first use in every artifact independently.

**Gate 4 — NGN fidelity.** Item types match NCSBN formats. Stems present data, not conclusions. Distractors are plausible and individually rationalized. Case studies have six scenes mapping to six operations.

**Gate 5 — Thread coverage.** All seven curriculum threads appear across each course's artifact set. Run a count; report it.

**Gate 6 — Internal consistency.** Within a case or a deck: gestational ages, dates, lab trends, and patient details do not contradict. Check arithmetic on every EDC calculation, every GTPAL, every dosage.

**Gate 7 — Safety review.** No artifact teaches a superseded practice as current (oxygen for Category II/III; 17-OHPC as available; letter categories as the current FDA system). No artifact states Texas law without a verification flag.

**Gate 8 — Cognitive load.** Slide counts within budget. Handouts within page limits. No table over 8 rows in student-facing material without being split.

---

## 7. THE 80% TARGET — OPERATIONALIZED

The score is a lagging indicator. Instrument these leading indicators instead:

| Metric | Target | How measured | When |
|---|---|---|---|
| Exit-ticket accuracy, daily | ≥ 75% by session 3 | Exit tickets (WO-H) | Each session |
| Item-bank practice accuracy | ≥ 80% on second attempt | Self-study pathway | Weeks 1–3 |
| Case-study completion | ≥ 70% of cohort attempts ≥ 4 cases | Self-report / LMS | Before exam |
| Terminology deck mastery | ≥ 90% on discrimination pairs | Flashcard app stats | Before exam |
| Blueprint coverage | 100% of objectives with ≥ 1 practice item | Gate 2 audit | Before session 1 |
| Predicted-high-miss pre-check | ≥ 70% on the over-sampled topics (WO-F) | Practice quiz, day 4 | Session 4 |

**Escalation rule:** if exit-ticket accuracy on any objective falls below 60%, that objective is added to session 4's wrap-up **and** to the remediation deck regardless of what the exam shows.

**Two honest caveats to keep in the document:**
1. Practice-item accuracy on *your own* items overestimates NCLEX performance, because your items and your teaching share a vocabulary. Treat 80% on internal items as roughly equivalent to a lower external score; do not declare victory at 80% internal.
2. The single largest driver of NGN performance in these units is **volume of worked cases with rationales read**, not lecture hours. If a trade-off appears between polishing slides and producing cases, produce cases.

---

## 8. HANDOFF PROMPT TEMPLATE

Paste this at the top of any fresh LLM session:

> You are producing one artifact in a nursing-education resource suite for Lone Star College–North Harris. I am attaching the canonical lesson plan and this build specification.
>
> **Execute only work order `<WO-ID>`.** Do not produce other artifacts. Do not summarize the lesson plan back to me.
>
> Follow the source policy in §2 exactly: approved sources only, APA 7th edition, and never fabricate a citation, DOI, page number, guideline number, or statistic. Where you are uncertain, write `[VERIFY: what to check — where]` inline and collect all flags in a `## VERIFY` section at the end.
>
> Before returning the artifact, run quality gates 1–8 from §6 and append a short `## GATE REPORT` stating pass/fail for each with one line of evidence.
>
> Output the artifact as a single file named per §3, with no conversational preamble inside the file.

---

## 9. BUILD ORDER (recommended sequence)

```
Phase 0  →  Human: obtain blueprint, textbook edition, convention decisions from Dr. Sharma
Phase 1  →  WO-A ×2, WO-B ×2
Phase 3a →  WO-F ×2          [start item bank early; it is the long pole]
Phase 2  →  WO-C ×8, WO-D ×8, WO-E ×8
Phase 3b →  WO-G ×14, WO-H ×2
Phase 4  →  WO-I ×2, WO-J ×4, WO-L ×2
Phase 4b →  Spanish versions of E, H, I, L
Phase 5  →  WO-K ×2          [after each exam only]
```

**Critical path:** WO-A → WO-F → WO-G. If time is short, build those three families for both courses and treat everything else as optional. A student with a blueprint-aligned item bank and fourteen worked cases will outperform a student with beautiful slides and no practice.

---

## 10. VERSIONING & MAINTENANCE

- Increment `v<N>` on any content change; never overwrite a version that has been taught from.
- Maintain a single `CHANGELOG.md` per course recording: date, artifact, what changed, why, and which source drove the change.
- **Annual review trigger points:** ACOG publishes new Practice Bulletins and Clinical Practice Guidelines continuously. Before each semester, re-verify the currency flags in §2 and search ACOG's clinical guidance index for successors to every cited document.
- After each cohort, fold the item analysis back into WO-F: retire items with poor point-biserial, and promote the previously-unused pool.
