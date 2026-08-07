#!/usr/bin/env python3
"""validate_bank.py — mechanical acceptance checks for a WO-F NGN item bank.

Enforces the build-spec §5.3 JSON schema and the ten item-writing rules that can be
checked without human judgment. Rules 1 and 3 (stems present data, not conclusions;
every distractor is right in some other scenario) are partly heuristic here and must
still be spot-checked by hand — see the WARN output.

Usage:
    python tools/validate_bank.py <item_bank.json> <blueprint.md>

Exit code 0 = all hard checks pass. Non-zero = defects listed. Stdlib only.
"""
import json
import re
import sys

NINE_ITEM_TYPES = {
    "bowtie", "trend", "matrix_grid", "matrix_multiple_choice",
    "extended_multiple_response", "extended_drag_drop", "cloze_dropdown",
    "highlight", "standalone_mc", "sata",
}
# Spec §5.3 lists nine slots but names ten format tokens (standalone_mc AND sata).
# "All nine item types represented" is read as: at least nine distinct tokens present.

NCJMM_OPS = {
    "Recognize Cues", "Analyze Cues", "Prioritize Hypotheses",
    "Generate Solutions", "Take Actions", "Evaluate Outcomes",
}
CLIENT_NEEDS = {
    "Management of Care", "Safety and Infection Control",
    "Health Promotion and Maintenance", "Psychosocial Integrity",
    "Basic Care and Comfort", "Pharmacological and Parenteral Therapies",
    "Reduction of Risk Potential", "Physiological Adaptation",
}
DIFFICULTIES = {"easy", "moderate", "hard"}
REQUIRED_KEYS = {
    "id", "objective_id", "item_type", "ncjmm_operation", "client_needs",
    "bloom", "difficulty_target", "stem", "options", "key", "scoring",
    "rationale_correct", "rationale_distractors", "source", "keywords",
}
# Phrases in a stem that hand the student the conclusion (Rule 1 heuristic).
CONCLUSION_LEAK = re.compile(
    r"\b(the (client|patient) has|diagnos(is|ed) (of|with)|"
    r"known|confirmed|with severe features\b.{0,40}\bwhat should the nurse)\b",
    re.IGNORECASE,
)


def load_blueprint_ids(path):
    """Objective IDs look like 1523-D2-3. Harvest every one from the blueprint."""
    text = open(path, encoding="utf-8").read()
    return set(re.findall(r"\b\d{4}-D\d+-\d+\b", text))


def approx(part, whole, target, tol=0.12):
    return whole == 0 or abs(part / whole - target) <= tol


def main():
    if len(sys.argv) != 3:
        print("usage: validate_bank.py <item_bank.json> <blueprint.md>")
        return 2
    bank_path, blueprint_path = sys.argv[1], sys.argv[2]

    errors, warnings = [], []
    data = json.load(open(bank_path, encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    bp_ids = load_blueprint_ids(blueprint_path)

    n = len(items)
    if n < 60:
        errors.append(f"item count {n} < 60 (spec WO-F acceptance)")

    seen_types, seen_ops = set(), []
    diff_counts = {"easy": 0, "moderate": 0, "hard": 0}
    ids = set()

    for i, it in enumerate(items):
        tag = it.get("id", f"index[{i}]")
        missing = REQUIRED_KEYS - set(it)
        if missing:
            errors.append(f"{tag}: missing keys {sorted(missing)}")
            continue

        if it["id"] in ids:
            errors.append(f"{tag}: duplicate id")
        ids.add(it["id"])

        if it["objective_id"] not in bp_ids:
            errors.append(f"{tag}: objective_id {it['objective_id']} not in blueprint")
        if it["item_type"] not in NINE_ITEM_TYPES:
            errors.append(f"{tag}: bad item_type {it['item_type']!r}")
        else:
            seen_types.add(it["item_type"])
        if it["ncjmm_operation"] not in NCJMM_OPS:
            errors.append(f"{tag}: bad ncjmm_operation {it['ncjmm_operation']!r}")
        else:
            seen_ops.append(it["ncjmm_operation"])
        if it["client_needs"] not in CLIENT_NEEDS:
            errors.append(f"{tag}: bad client_needs {it['client_needs']!r}")
        if it["difficulty_target"] not in DIFFICULTIES:
            errors.append(f"{tag}: bad difficulty {it['difficulty_target']!r}")
        else:
            diff_counts[it["difficulty_target"]] += 1

        if not str(it.get("source", "")).strip():
            errors.append(f"{tag}: empty source (Rule 10)")
        if not it.get("rationale_correct", "").strip():
            errors.append(f"{tag}: empty rationale_correct (Rule 9)")

        # Rule 3: every distractor rationalized. Distractors = options not in key.
        rd = it.get("rationale_distractors", {})
        if not isinstance(rd, dict) or not rd:
            errors.append(f"{tag}: no rationale_distractors (Rule 3)")

        # Rule 4: no all-of-the-above / absolutes / negative stems.
        opt_text = " ".join(str(o) for o in it.get("options", [])).lower()
        if "all of the above" in opt_text:
            errors.append(f"{tag}: contains 'all of the above' (Rule 4)")
        if re.search(r"\b(always|never)\b", opt_text):
            warnings.append(f"{tag}: absolute term in options (Rule 4) — review")
        if re.search(r"\b(except|not|contraindicated).{0,3}\?", it["stem"].lower()):
            warnings.append(f"{tag}: possible negative stem (Rule 4) — review")

        # Rule 1 heuristic: stem hands over the conclusion.
        if CONCLUSION_LEAK.search(it["stem"]):
            warnings.append(f"{tag}: stem may state the conclusion (Rule 1) — review")

        # Rule 5: trend items need >= 3 time points.
        if it["item_type"] == "trend":
            blob = json.dumps(it.get("chart_data", {})) + json.dumps(it.get("options", []))
            tps = len(re.findall(r"\b([01]?\d|2[0-3]):[0-5]\d\b", blob)) \
                or len(re.findall(r"\bDay\s*\d+|\bhour\s*\d+|\bweek\s*\d+", blob, re.I))
            if tps < 3:
                errors.append(f"{tag}: trend item has < 3 time points (Rule 5)")

        # Rule 6: bowtie = 2 actions, 1 condition, 2 parameters, with surplus options.
        if it["item_type"] == "bowtie":
            key = it.get("key", [])
            if not (isinstance(key, dict)):
                warnings.append(f"{tag}: bowtie key should be a dict of "
                                f"actions/condition/parameters (Rule 6) — review")
            else:
                a = len(key.get("actions", []))
                c = len(key.get("condition", []) if isinstance(key.get("condition"), list)
                        else [key.get("condition")] if key.get("condition") else [])
                p = len(key.get("parameters", []))
                if (a, c, p) != (2, 1, 2):
                    errors.append(f"{tag}: bowtie key is {a} actions/{c} condition/"
                                  f"{p} parameters, need 2/1/2 (Rule 6)")

    # All nine item types represented.
    if len(seen_types) < 9:
        errors.append(f"only {len(seen_types)} item types present, need >= 9: "
                      f"missing {sorted(NINE_ITEM_TYPES - seen_types)}")
    # All six NCJMM operations present.
    if set(seen_ops) != NCJMM_OPS:
        errors.append(f"NCJMM ops missing: {sorted(NCJMM_OPS - set(seen_ops))}")

    # Rule 7: 30% easy / 40% moderate / 30% hard (± tolerance).
    if not approx(diff_counts["easy"], n, 0.30):
        warnings.append(f"easy share {diff_counts['easy']}/{n} off 30% target")
    if not approx(diff_counts["moderate"], n, 0.40):
        warnings.append(f"moderate share {diff_counts['moderate']}/{n} off 40% target")
    if not approx(diff_counts["hard"], n, 0.30):
        warnings.append(f"hard share {diff_counts['hard']}/{n} off 30% target")

    print(f"== {bank_path} ==")
    print(f"items={n}  types={len(seen_types)}/9  ops={len(set(seen_ops))}/6  "
          f"difficulty(e/m/h)={diff_counts['easy']}/{diff_counts['moderate']}/{diff_counts['hard']}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  FAIL  {e}")
    if errors:
        print(f"\nFAILED with {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"\nPASSED ({len(warnings)} warning(s) to review by hand).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
