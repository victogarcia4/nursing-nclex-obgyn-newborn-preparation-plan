#!/usr/bin/env python3
"""gate_audit.py — sweep the build/ tree and enforce the mechanical quality gates.

Covers the parts of build-spec §6 gates 1-8 that a machine can judge:
  Gate 1  citation integrity   — bracketed-source-tag presence in clinical files
  Gate 3  terminology          — banned outdated terms
  Gate 7  safety review        — superseded practice taught as current; unflagged TX law
  Gate 8  cognitive load       — student-facing tables over 8 rows
Plus it harvests every [VERIFY] and [ASSUMPTION] flag into one register.

Usage:  python tools/gate_audit.py build/
Exit 0 if no hard violations. Stdlib only.
"""
import re
import sys
from pathlib import Path

# Gate 3 — outdated vocabulary (RNSG2514 §1.8). Word-boundary, case-insensitive.
# Each entry: (regex, human label). Allowed-context exceptions handled inline.
BANNED_TERMS = [
    (r"premature rupture of membranes", "premature ROM (use 'prelabor')"),
    (r"\bPIH\b", "PIH (use 'gestational hypertension')"),
    (r"\bnonreassuring\b", "nonreassuring (use 'Category II/III')"),
    (r"\btoxemia\b", "toxemia (use 'preeclampsia')"),
    (r"failure to progress", "failure to progress (use 'labor arrest')"),
    (r"habitual abort", "habitual aborter (use 'recurrent pregnancy loss')"),
    (r"mild preeclampsia|severe preeclampsia",
     "mild/severe preeclampsia (use 'with/without severe features')"),
]
# 'IUGR' is allowed only when paired with FGR (teaching the crosswalk).
IUGR = re.compile(r"\bIUGR\b")
IUGR_OK = re.compile(r"IUGR\s*/?\s*FGR|FGR\s*\(.*IUGR|IUGR.{0,30}\bFGR\b", re.I)

# Gate 7 — superseded practice stated as current (not merely named as superseded).
SUPERSEDED = [
    (re.compile(r"(routine|administer|apply|give).{0,30}oxygen.{0,40}"
                r"category\s*(ii|iii|2|3)", re.I),
     "routine O2 for Category II/III taught as current (ACOG 2025 reversal)"),
    (re.compile(r"17-?OHPC|makena", re.I),
     "17-OHPC/Makena mentioned — must be flagged as withdrawn 2023"),
]
# Gate 7 — Texas law must never be stated without a VERIFY flag on the same line.
TX_LAW = re.compile(r"texas.{0,60}(law|statute|abortion|consent|fetal remains|minor)", re.I)
VERIFY_INLINE = re.compile(r"\[VERIFY", re.I)

# A banned term / superseded practice is being TAUGHT AGAINST (not used as guidance) when
# it appears in quotation marks or on a line with a corrective cue. Those are not violations.
CORRECTION_CUE = re.compile(
    r"no longer|rather than|instead of|outdated|not recommended|against routine|"
    r"supersed|withdraw|\[verify|formerly|not ['\"]|say ['\"]|saying ['\"]|→", re.I)


def is_corrective(line, start, end):
    """True if the matched term is quoted or the line carries a correction cue."""
    before = line[max(0, start - 1):start]
    after = line[end:end + 1]
    if before in "'\"" and after in "'\".,":
        return True
    if before in "'\"" or after in "'\"":
        return True
    return bool(CORRECTION_CUE.search(line))


VERIFY_FLAG = re.compile(r"\[VERIFY:[^\]]*\]", re.I)
ASSUMPTION_FLAG = re.compile(r"\[ASSUMPTION:[^\]]*\]", re.I)
SOURCE_TAG = re.compile(r"\[(ACOG|CDC|FDA|USPSTF|NICHD|AAP|AHA|IOM|NASEM|SMFM|"
                        r"AWHONN|NCSBN|NRP|Lowdermilk|Silbert|QSEN)[^\]]*\]")

# Files that are student-facing COMPARISON tables for Gate 8 cognitive-load purposes.
# Terminology decks are excluded: a flashcard list is not a comparison table, and its
# cognitive load is bounded by the <=25-word back rule enforced in the deck builders.
STUDENT_FACING = ("HighYield", "Handout", "StudyPath", "ExitTickets")

# Terminology-teaching files MUST quote the outdated vocabulary to teach the corrections
# (build-spec WO-B "say this, not that"). Gate 3's banned-term scan is therefore skipped
# for them; the decks enforce current usage through their own say-this-not-that structure.
TERMINOLOGY_TEACHING = ("Terms",)


def table_rows(md_text):
    """Yield (start_line, row_count) for each pipe-table with > 8 body rows."""
    lines = md_text.splitlines()
    i, out = 0, []
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) \
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            j = i + 2
            body = 0
            while j < len(lines) and lines[j].strip().startswith("|"):
                body += 1
                j += 1
            if body > 8:
                out.append((i + 1, body))
            i = j
        else:
            i += 1
    return out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "build")
    # Exclude the audit's own generated report so it does not scan/ double-count itself.
    files = [f for f in (sorted(root.rglob("*.md")) + sorted(root.rglob("*.csv")))
             if not f.name.startswith("GATE_AUDIT")]
    hard, soft = [], []
    verifies, assumptions = [], []

    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = f.as_posix()
        low = text.lower()

        is_terminology = any(k in f.name for k in TERMINOLOGY_TEACHING)
        lines = text.splitlines()
        if not is_terminology:
            for rx, label in BANNED_TERMS:
                for m in re.finditer(rx, low):
                    ln = low[:m.start()].count("\n") + 1
                    line = lines[ln - 1]
                    col = m.start() - (low.rfind("\n", 0, m.start()) + 1)
                    if is_corrective(line, col, col + (m.end() - m.start())):
                        continue
                    hard.append(f"[Gate3] {rel}:{ln}  banned term: {label}")
            for m in IUGR.finditer(text):
                seg = text[max(0, m.start() - 40):m.end() + 40]
                if not IUGR_OK.search(seg):
                    ln = text[:m.start()].count("\n") + 1
                    hard.append(f"[Gate3] {rel}:{ln}  'IUGR' without FGR crosswalk")

        for rx, label in SUPERSEDED:
            for m in rx.finditer(text):
                ln = text[:m.start()].count("\n") + 1
                line = lines[ln - 1]
                # Fine when the line teaches against it (withdrawn / superseded / no longer / quoted).
                col = m.start() - (text.rfind("\n", 0, m.start()) + 1)
                if is_corrective(line, col, col + (m.end() - m.start())):
                    continue
                hard.append(f"[Gate7] {rel}:{ln}  {label}")

        for m in TX_LAW.finditer(text):
            ln = text[:m.start()].count("\n") + 1
            line = text.splitlines()[ln - 1]
            if not VERIFY_INLINE.search(line):
                hard.append(f"[Gate7] {rel}:{ln}  Texas law stated without [VERIFY] flag")

        if f.suffix == ".md" and any(k in f.name for k in STUDENT_FACING):
            for ln, rows in table_rows(text):
                soft.append(f"[Gate8] {rel}:{ln}  student-facing table has {rows} rows (>8)")

        # Gate 1 heuristic: a clinical .md with zero source tags and zero VERIFY flags.
        if f.suffix == ".md" and any(k in f.name for k in
                                     ("ItemBank", "Case", "HighYield", "Blueprint")):
            if not SOURCE_TAG.search(text) and not VERIFY_FLAG.search(text):
                soft.append(f"[Gate1] {rel}  no source tags or VERIFY flags found")

        for m in VERIFY_FLAG.finditer(text):
            ln = text[:m.start()].count("\n") + 1
            verifies.append(f"{rel}:{ln}  {m.group(0)}")
        for m in ASSUMPTION_FLAG.finditer(text):
            ln = text[:m.start()].count("\n") + 1
            assumptions.append(f"{rel}:{ln}  {m.group(0)}")

    print(f"== gate audit: {root} ({len(files)} files) ==\n")
    print(f"VERIFY flags: {len(verifies)}   ASSUMPTION flags: {len(assumptions)}")
    print(f"hard violations: {len(hard)}   soft warnings: {len(soft)}\n")
    for h in hard:
        print("  " + h)
    for s in soft:
        print("  " + s)
    if "--report" in sys.argv:
        rpt = root / "GATE_AUDIT_v1.md"
        with open(rpt, "w", encoding="utf-8") as fh:
            fh.write("# Master Gate Audit & VERIFY Register\n")
            fh.write(f"Generated by `tools/gate_audit.py` over `{root}/` "
                     f"({len(files)} files scanned).\n\n")
            fh.write(f"- **Hard gate violations:** {len(hard)}\n")
            fh.write(f"- **Soft warnings:** {len(soft)}\n")
            fh.write(f"- **VERIFY flags:** {len(verifies)}  ·  "
                     f"**ASSUMPTION flags:** {len(assumptions)}\n\n")
            fh.write("Mechanical gates covered here: 1 (citation presence), 3 (terminology), "
                     "7 (superseded practice / unflagged Texas law), 8 (table size). Gates 2, 4, "
                     "5, 6 are asserted per-artifact in each file's own GATE REPORT and spot-checked "
                     "by hand (see the suite verification notes).\n\n")
            fh.write("## Hard violations\n\n")
            fh.write("None.\n\n" if not hard else "".join(f"- {h}\n" for h in hard) + "\n")
            fh.write("## Soft warnings (review, not blockers)\n\n")
            fh.write("None.\n\n" if not soft else "".join(f"- {s}\n" for s in soft) + "\n")
            fh.write("## VERIFY register — the question list for Dr. Sharma / local verification\n\n")
            fh.write("Every unresolved clinical, statutory, or convention question, collected from "
                     "all artifacts. This is the content of the alignment email.\n\n")
            for v in verifies:
                fh.write(f"- {v}\n")
            fh.write("\n## ASSUMPTION register — decisions made pending Phase 0\n\n")
            for a in assumptions:
                fh.write(f"- {a}\n")
            fh.write("\nSee `INDEX.md` for the rationale behind each assumption.\n")
        print(f"\nwrote {rpt}")

    if hard:
        print(f"\nGATE AUDIT FAILED: {len(hard)} hard violation(s).")
        return 1
    print("\nGATE AUDIT PASSED (soft warnings are review items, not blockers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
