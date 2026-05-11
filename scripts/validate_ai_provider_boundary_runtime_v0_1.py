#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "AI_PROVIDER_BOUNDARY_RUNTIME_v0_1.md"
FIXTURES = ROOT / "specs" / "ai_provider_boundary_fixtures_v0_1.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "memory_truth_granted",
    "decision_authority_granted",
    "teni_authority_granted",
]


def evaluate(case: dict) -> dict:
    if case.get("bypasses_governance"):
        status = "QUARANTINE"
    elif case.get("claims_authority"):
        status = "REJECT"
    elif case.get("hides_uncertainty"):
        status = "REPAIR"
    else:
        status = "CANDIDATE"
    out = {"status": status}
    out.update({field: False for field in FALSE_FIELDS})
    return out


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing AI provider boundary doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["AI provider output is raw candidate material", "execution_authority_granted: false"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    if not FIXTURES.is_file():
        errors.append("missing AI provider boundary fixtures")
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
    print("PASS: AI Provider Boundary Runtime validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
