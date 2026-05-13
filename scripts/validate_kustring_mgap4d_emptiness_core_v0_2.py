#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "KUSTRING_MGAP4D_EMPTINESS_CORE_v0_2.md"
FIXTURES = ROOT / "specs" / "kustring_mgap4d_emptiness_core_v0_2_fixtures.json"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def evaluate(case: dict) -> dict:
    if case.get("K_objectified"):
        status = "REJECT"
    elif case.get("gap_domain") != "K_perp":
        status = "REJECT"
    elif case.get("psi_star_domain") != "K_perp":
        status = "REJECT"
    elif not case.get("string_in_Kperp"):
        status = "REJECT"
    elif case.get("brane_is_substance"):
        status = "REJECT"
    elif case.get("K_Kperp_collapsed"):
        status = "HOLD"
    elif not case.get("psi_star_norm_one"):
        status = "HOLD"
    elif case.get("psi_star_eigenvalue") != "33/20":
        status = "HOLD"
    elif not case.get("centered_observable_used"):
        status = "HOLD"
    elif not case.get("spectral_weight_33_20_positive"):
        status = "OBSERVE"
    else:
        status = "CANDIDATE"
    out = {"status": status}
    out.update({field: False for field in FALSE_FIELDS})
    return out


def main() -> int:
    errors: list[str] = []
    if not DOC.is_file():
        errors.append("missing KuString MGAP4D Emptiness Core v0.2 doc")
    else:
        text = DOC.read_text(encoding="utf-8")
        for token in ["K -- delta_rel --> String/Brane", "StringMode", "Brane", "33/20", "A_circ"]:
            if token not in text:
                errors.append(f"doc missing: {token}")
    if not FIXTURES.is_file():
        errors.append("missing KuString MGAP4D Emptiness Core v0.2 fixtures")
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
    print("PASS: KuString MGAP4D Emptiness Core v0.2 validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
