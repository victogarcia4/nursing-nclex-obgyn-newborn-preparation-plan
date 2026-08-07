# INDEX — Maternal/Newborn Teaching Resource Suite

> **New to this project? Read [`HANDOFF.md`](HANDOFF.md) first** — it explains the goal, the
> generator-based workflow, verification commands, the Phase 0 blocker, and what to build next.

Build tracker for the critical-path artifacts (WO-A, WO-B, WO-F, WO-G, WO-I) across
**RNSG 1523 Nursing I (Antepartum)** and **RNSG 2514 Nursing III (Complications)**.

Canonical inputs (do not edit): `RNSG1523_Antepartum_LessonPlan_Expanded_APA.md`,
`RNSG2514_Complications_LessonPlan_APA.md`, `MaternalNewborn_BuildSpec_LLM_Executable.md`.

---

## Artifact status

| WO | Artifact | RNSG 1523 | RNSG 2514 |
|---|---|---|---|
| A | Blueprint & competency map | ✔ | ✔ |
| B | Terminology master deck (CSV + MD) | ✔ 121 cards | ✔ 125 cards |
| F | NGN item bank (JSON + MD mirror) | ✔ 61 items | ✔ 64 items |
| G | Unfolding case studies | ✔ (6/6) | ✔ (8/8) |
| I | High-yield sheets | ✔ | ✔ |
| H | Exit tickets + prior-knowledge polls | ✔ (added post-critical-path) | ✔ |
| — | Gate audit (`build/GATE_AUDIT_v1.md`) | ✔ 0 hard violations | |
| — | NotebookLM companion | ⏸ blocked — not authenticated (see below) | |

### NotebookLM companion — blocked on authentication
`get_health` returned `authenticated: false`, and the Google login is an interactive
browser step this session cannot perform. The study material is ready to load once you
authenticate. **To finish it yourself:**
1. In an interactive Claude Code session, run the NotebookLM `setup_auth` (logs into Google once; cookies persist).
2. Create one notebook per course in NotebookLM and share it; provide each share URL to `add_notebook`.
3. `add_source` these files per course as the student companion:
   - `build/<COURSE>/<COURSE>_Terms_v1.md`
   - `build/<COURSE>/<COURSE>_HighYield_v1.md`
   - `build/<COURSE>/<COURSE>_ItemBank_v1.md`
   - each `build/<COURSE>/<COURSE>_Case_*.md`
4. Students can then query the material and generate audio overviews.

**Deferred (out of scope this build):** WO-C slides, WO-D facilitation guides,
WO-E handouts, WO-J sim scripts, WO-K remediation (Phase 5 only), WO-L study paths,
and all Spanish versions. *(WO-H exit tickets were added after the critical path as the
§7 daily-accuracy instrument.)*

---

## Assumption register — Phase 0 has NOT been completed

No departmental blueprint, item-analysis criteria, textbook edition, or convention
decisions have been received from Dr. Sharma. Every choice below is tagged
`[ASSUMPTION: … — confirm with Dr. Sharma]` at each point of use so the revision
pass after alignment is mechanical. This table is the source of truth.

| # | Convention | Choice made | Rationale |
|---|---|---|---|
| A1 | GTPAL vs GPTAL | **GTPAL** | Used throughout RNSG1523 lesson plan §1.2 and §2B |
| A2 | ROM wording | **Prelabor** rupture of membranes | Mandated by RNSG2514 terminology-correction table §1.8 |
| A3 | Pregnancy drug labeling | **PLLR primary; legacy A/B/C/D/X taught as a crosswalk only** | RNSG1523 §4C / §1.7 treat letter categories as historical |
| A4 | Preeclampsia language | **with / without severe features** (never "mild/severe") | RNSG2514 §1.3, §1.8 |
| A5 | FGR vs IUGR | **FGR** in clinical language | RNSG2514 §1.7, §1.8 |
| A6 | Textbook edition | Lowdermilk 13th ed. / Silbert-Flagg 9th ed. **as cited** | Lesson-plan reference lists; swap to department edition |
| A7 | Item counts by topic | **Derived from lesson-plan session weight** | No departmental blueprint exists yet |
| A8 | Item provenance | **All items original** | Publisher-bank reuse is a licensing decision, not ours |
| A9 | Bloom taxonomy | **Revised Bloom (Remember→Create)** | Standard nursing-education usage |

---

## Currency flags carried into every artifact (restate, do not resolve)

- ACOG 2024 Clinical Practice Update supersedes parts of PB 190 (diabetes screening thresholds).
- ACOG 2025 intrapartum FHR guideline recommends **against routine maternal O₂** for Category II/III absent maternal hypoxia; supersedes PB 106/116; document-number discrepancy unresolved.
- 17-OHPC (Makena) withdrawn from U.S. market 2023.
- NRP edition currency (8th ed. cited; verify 9th).
- SMFM Consult Series #74 (cfDNA) layers onto PB 226.
- **Texas statute** (abortion, fetal remains disposition, minors' consent) — never stated from model knowledge; always `[VERIFY]`.

---

## Verification commands

```bash
python tools/validate_bank.py build/RNSG1523/RNSG1523_ItemBank_v1.json build/RNSG1523/RNSG1523_Blueprint_Unit_v1.md
python tools/validate_bank.py build/RNSG2514/RNSG2514_ItemBank_v1.json build/RNSG2514/RNSG2514_Blueprint_Unit_v1.md
python tools/gate_audit.py build/
```
