#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "KUOS_EMPTINESS_VACUUM_NORMALIZATION_v0_1.md"
FIXTURES = ROOT / "specs" / "emptiness_vacuum_normalization_fixtures_v0_1.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def evaluate(case: dict) -> dict:
    if case.get("k_objectified"):
        status = "REJECT"
    elif case.get("gap_domain") != "K_perp":
        status = "REJECT"
    elif case.get("psi_star_domain") != "K_perp":
        status = "REJECT"
    elif case.get("k_kperp_collapsed"):
        status = "HOLD"
    elif case.get("direct_k_observed"):
        status = "HOLD"
    elif not case.get("h_world_k_zero"):
        status = "REPAIR"
    else:
        status = "CANDIDATE"
    out = {"status": status}
    out.update({field: False for field in FALSE_FIELDS})
    return out


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing emptiness vacuum normalization doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["H_world K = 0", "K is not an object", "m_gap = inf spectrum", "33/20"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    if not FIXTURES.is_file():
        errors.append("missing emptiness vacuum normalization fixtures")
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
    print("PASS: KuuOS Emptiness Vacuum Normalization validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
