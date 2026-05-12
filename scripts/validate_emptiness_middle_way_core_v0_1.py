#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "EMPTINESS_DEPENDENT_ORIGINATION_TWO_TRUTHS_MIDDLE_WAY_CORE_v0_1.md"
FIXTURES = ROOT / "specs" / "emptiness_middle_way_core_fixtures_v0_1.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def evaluate(case: dict) -> dict:
    if case.get("hides_harm"):
        status = "QUARANTINE"
    elif case.get("claims_self_essence"):
        status = "REJECT"
    elif case.get("collapses_two_truths"):
        status = "HOLD"
    elif case.get("denies_usefulness"):
        status = "REPAIR"
    elif case.get("hides_lineage"):
        status = "OBSERVE"
    else:
        status = "CANDIDATE"
    out = {"status": status}
    out.update({field: False for field in FALSE_FIELDS})
    return out


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing emptiness middle way core doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["No artifact", "Dependent origination", "Two truths", "Middle Way"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    if not FIXTURES.is_file():
        errors.append("missing emptiness middle way fixtures")
    else:
        data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        for case in data.get("fixtures", []):
            out = evaluate(case)
            if out["status"] != case.get("expected_status"):
                errors.append(f"{case.get('id')}: expected {case.get('expected_status')}, got {out['status']}")
            for field in FALSE_FIELDS:
                if out[field] is not False:
                    errors.append(f"{case.get('id')}: {field} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: Emptiness / Dependent Origination / Two Truths / Middle Way core validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
