# HANDOFF — Maternal/Newborn NGN Teaching-Resource Suite

**Read this first.** You are a fresh LLM continuing an in-progress project with no memory of the
prior session. This file is the single source of truth for *where things stand and what to do next*.
After reading it, read `INDEX.md` (status + assumption register) and `build/GATE_AUDIT_v1.md`
(the outstanding VERIFY questions).

---

## 1. What this project is

A course-aligned resource suite to move two nursing cohorts to **≥ 80% on the Next Generation
NCLEX (NGN)** for the Maternal/Newborn units:
- **RNSG 1523 Nursing I** — Antepartum (normal + screening)
- **RNSG 2514 Nursing III** — Complications (deterioration recognition + emergency response)

**Authoritative inputs (do not edit these):**
- `MaternalNewborn_BuildSpec_LLM_Executable.md` — the build spec. Defines 12 artifact families
  (work orders WO-A … WO-L), the item schema (§5.3), the item-writing rules (WO-F), the quality
  gates (§6), and the 80%-target instrumentation (§7). **It wins over any other instruction.**
- `RNSG1523_Antepartum_LessonPlan_Expanded_APA.md` and `RNSG2514_Complications_LessonPlan_APA.md`
  — canonical scope, sequencing, terminology, and the validated APA reference lists.

The owner is **Victor Sanchez** (guest faculty, Lone Star College–North Harris). The departmental
resource person is **Dr. Rajrani Sharma** (see the Phase 0 blocker, §6 below).

---

## 2. Current state (as of the last commit)

Built, validated, and committed — the **critical path (WO-A, B, F, G, I)** plus **WO-H**, for both
courses. Everything lives under `build/`. The gate audit passes with **0 hard violations**.

| WO | Artifact | 1523 | 2514 |
|---|---|---|---|
| A | Blueprint & competency map | ✔ | ✔ |
| B | Terminology deck (CSV + MD mirror) | ✔ 121 cards | ✔ 125 cards |
| F | NGN item bank (JSON + MD mirror) | ✔ 61 items | ✔ 64 items |
| G | Unfolding cases (6 scenes each) | ✔ 6 | ✔ 8 |
| I | High-yield sheets | ✔ | ✔ |
| H | Exit tickets + prior-knowledge polls | ✔ | ✔ |

Git: two commits on `master`, working tree clean. This is a **local repo with no remote** — do not
push anywhere; commit locally only, and only when the user asks.

---

## 3. THE CRITICAL MENTAL MODEL — content is generated, not hand-edited

Most artifacts are produced by **generator scripts in `tools/`**. The files in `build/` are OUTPUT.
**To change item-bank or terminology content, edit the generator and re-run it — never edit the
generated `.json`/`.csv`/mirror `.md` directly** (your edit would be overwritten on the next build).

| Generated artifact | Edit this generator | Re-run |
|---|---|---|
| `build/*/…_Terms_v1.csv` + `.md` | `tools/build_terms_1523.py`, `tools/build_terms_2514.py` | `python tools/build_terms_1523.py` |
| `build/*/…_ItemBank_v1.json` + shards + mirror | `tools/build_bank_1523.py`, `tools/build_bank_2514.py` | `python tools/build_bank_1523.py` |

**Hand-authored Markdown (edit directly):** the blueprints, all 14 `…_Case_*.md`, the high-yield
sheets, the exit tickets, `INDEX.md`, and the changelogs. `build/GATE_AUDIT_v1.md` is generated —
regenerate it, don't hand-edit (see §4).

The two validators are also in `tools/` and are the contract every artifact must satisfy:
- `tools/validate_bank.py` — enforces the §5.3 item schema + the mechanical item-writing rules.
- `tools/gate_audit.py` — enforces build-spec §6 gates 1, 3, 7, 8 across the tree, harvests all
  `[VERIFY]`/`[ASSUMPTION]` flags, and (with `--report`) writes `build/GATE_AUDIT_v1.md`.

Environment: **Windows, Python 3.11, stdlib only** (no third-party deps). Run commands from the
repo root `C:\Users\skint\Desktop\RNSG OG`.

---

## 4. How to verify (run these after ANY change)

```bash
# 1. Item banks satisfy schema + rules (must exit 0)
python tools/validate_bank.py build/RNSG1523/RNSG1523_ItemBank_v1.json build/RNSG1523/RNSG1523_Blueprint_Unit_v1.md
python tools/validate_bank.py build/RNSG2514/RNSG2514_ItemBank_v1.json build/RNSG2514/RNSG2514_Blueprint_Unit_v1.md

# 2. Gate audit across the whole tree + regenerate the master report (must say PASSED)
python tools/gate_audit.py build/ --report
```

If you regenerate a bank, rebuild it first (`python tools/build_bank_2514.py`) then validate.
Hand-checks the validators cannot do (do these when you touch the relevant content):
- Recompute every **Naegele** date and **GTPAL** by hand (all currently correct).
- Confirm each case still has exactly 6 scenes mapping to the 6 NCJMM operations, in order.
- Confirm stems present **data, not the conclusion** (WO-F Rule 1).

### gate_audit.py behavior you must understand
The auditor has deliberate, documented exemptions so it doesn't false-positive on legitimate
teaching content. **Do not "fix" these by weakening content:**
- **Terminology decks** (`…_Terms_*`) are exempt from the banned-term scan — they *must* quote the
  outdated vocabulary to teach the "say this, not that" corrections.
- Banned terms / superseded practices are skipped **when quoted or on a line with a corrective cue**
  (`"not '…'"`, `"no longer"`, `"rather than"`, `"withdrawn"`, `→`, etc.). That is how a case can
  say *not "failure to progress"* without tripping the gate.
- The report file `GATE_AUDIT_v1.md` is excluded from its own scan.

If you add content that legitimately names an outdated term (to teach against it), phrase it with a
corrective cue or quotes so the auditor recognizes intent — that is the correct pattern, not a hack.

---

## 5. Non-negotiable rules for any new artifact (build-spec §2, §6)

1. **Approved sources only, APA 7th.** Reuse ONLY reference entries already in the two lesson plans'
   PART 5 reference lists. **Never invent** a DOI, page number, guideline number, or statistic. Every
   clinical claim carries a bracketed source tag, e.g. `[ACOG PB 222]`, `[CDC US MEC]`, `[Lowdermilk]`.
2. **Uncertainty → `[VERIFY: what to check — where]`** inline, collected in a `## VERIFY` section at
   the file's end. The auditor harvests these into `GATE_AUDIT_v1.md`.
3. **Texas statute** (abortion, fetal-remains disposition, minors' consent) is **NEVER stated from
   model knowledge — always a `[VERIFY]` flag.**
4. **Current terminology** (enforced by the auditor): *prelabor* (not premature) ROM · preeclampsia
   *with/without severe features* (not mild/severe) · *gestational hypertension* (not PIH) ·
   *Category II/III* (not nonreassuring) · *FGR* (not IUGR in clinical text) · *labor arrest* (not
   failure to progress).
5. **Currency flags** — restate, never silently resolve: ACOG 2024 diabetes-screening update over
   PB 190; **ACOG 2025 intrapartum FHR guideline recommends AGAINST routine maternal O₂ for Category
   II/III absent maternal hypoxia** (supersedes PB 106/116; document-number discrepancy unresolved);
   17-OHPC withdrawn from the U.S. market 2023; NRP edition currency; SMFM Consult Series #74 over PB 226.
6. End every artifact with a `## GATE REPORT` (pass/fail on the relevant gates, one line of evidence).
7. **File naming (§3):** `<COURSE>_<ARTIFACT>_<SCOPE>_v<N>.<ext>`. Increment `v<N>` on any content
   change; never overwrite a version that has been taught from. Log every change in
   `CHANGELOG_RNSG1523.md` / `CHANGELOG_RNSG2514.md`.

---

## 6. The big open blocker — Phase 0 is NOT done

No departmental blueprint, textbook edition, item-analysis criteria, or convention decisions have
been received from Dr. Sharma. Everything built so far runs on lesson-plan-derived **assumptions**,
each tagged `[ASSUMPTION: … — confirm with Dr. Sharma]` and collected in `INDEX.md`
(GTPAL vs GPTAL, prelabor ROM, PLLR-primary, all-original items, textbook edition, item weighting).

**The `[VERIFY]` register in `build/GATE_AUDIT_v1.md` is the content of the alignment email to
Dr. Sharma.** Resolving Phase 0 is the single highest-leverage action and turns the revision pass
into mechanical find-and-replace. If the user asks "what's most important," it is this.

Also blocked: the **NotebookLM** study companion — `get_health` returned `authenticated: false`;
it needs an interactive Google login the build session can't perform. Steps to finish are in
`INDEX.md`. It is additive; nothing depends on it.

---

## 7. What to build next (recommended order)

The user deliberately stopped after the critical path to "reassess before slides." Deferred work,
best order:

1. **WO-C slide decks** (8: 4 sessions × 2 courses) — now unblocked by the blueprints. Follow the
   session architecture in each lesson plan (hook → content → active learning → break → content →
   active learning → exit ticket). Spec WO-C: 35–45 content slides/session, claim-style titles,
   `> NOTES:` speaker notes, ≥ 2 comparison tables, ≥ 1 "first action" slide, bracketed source tags.
   Slides are Markdown with `---` breaks.
2. **WO-D facilitation guides** (8) and **WO-E handouts** (8) — both derive from the slides; build
   after C. (When these exist, backfill real slide numbers into the exit-ticket remediation pointers,
   which currently carry a `[VERIFY: slide numbers … deferred]` note.)
3. **WO-J sim scripts** (4) and **WO-L study path** (2).
4. **Spanish** versions of the student-facing set (E, H, I, L) — translate for clinical accuracy, not
   literalness; keep the English clinical term in parentheses on first use. A bilingual clinician must
   verify before student distribution.
5. **WO-K remediation** — Phase 5 ONLY. Requires real post-exam item analysis (p-values,
   point-biserial); do not attempt without that data. The item banks already hold an unused reserve
   pool for WO-K's fresh practice items.

To execute any single work order cold, copy its block from the build spec §5 plus the relevant
lesson plan into your context; the spec §8 has a handoff prompt template.

---

## 8. Honest framing to preserve (do not oversell)

- No resource set guarantees a score. The deliverable is **alignment + calibrated practice volume +
  early detection** (spec §0, §7).
- **Internal practice accuracy overestimates external NGN performance** — our items and our teaching
  share vocabulary. Do not declare success at 80% on internal items (spec §7 caveat 1).
- The biggest driver of NGN performance in these units is **worked cases with rationales read**, not
  lecture hours. If polishing slides ever competes with producing cases/practice, produce cases
  (spec §7 caveat 2).

---

## 9. File map

```
MaternalNewborn_BuildSpec_LLM_Executable.md   ← the spec (authoritative)
RNSG1523_…_LessonPlan_….md / RNSG2514_….md    ← canonical inputs
HANDOFF.md                                     ← this file
INDEX.md                                       ← status + assumption register (read 2nd)
CHANGELOG_RNSG1523.md / CHANGELOG_RNSG2514.md  ← version log (update on every change)
tools/
  validate_bank.py  gate_audit.py             ← validators (the contract)
  build_terms_1523.py  build_terms_2514.py    ← terminology generators
  build_bank_1523.py   build_bank_2514.py     ← item-bank generators
build/
  GATE_AUDIT_v1.md                             ← generated: gate status + VERIFY register
  RNSG1523/  RNSG2514/                         ← finished artifacts (§3 naming)
  _shards/                                      ← intermediate item-bank day-shards (not deliverables)
```

**Quick smoke test that everything still works:**
```bash
python tools/build_terms_1523.py && python tools/build_terms_2514.py \
 && python tools/build_bank_1523.py && python tools/build_bank_2514.py \
 && python tools/gate_audit.py build/ --report
```
Expect: builders report card/item counts, audit says `GATE AUDIT PASSED`.
