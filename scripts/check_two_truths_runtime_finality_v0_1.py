#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLOSURE_CHECKER = ROOT / "scripts" / "check_two_truths_runtime_closure_v0_1.py"
DOC = ROOT / "docs" / "TWO_TRUTHS_RUNTIME_FINALITY_PACKET_v0_1.md"
ATTEST = ROOT / "specs" / "two_truths_runtime_attestation_v0_1.generated.json"

REQUIRED = [
    "docs/TWO_TRUTHS_RUNTIME_CLOSURE_PACKET_v0_1.md",
    "docs/TWO_TRUTHS_RUNTIME_FINALITY_PACKET_v0_1.md",
    "specs/two_truths_runtime_attestation_v0_1.generated.json",
    "specs/two_truths_runtime_bundle_v0_1.generated.json",
    "specs/two_truths_runtime_worm_receipt_v0_1.generated.json",
    "scripts/check_two_truths_runtime_closure_v0_1.py",
]

FALSE_KEYS = [
    "paramartha_objectification_allowed",
    "samvrti_denial_allowed",
    "ultimate_to_conventional_collapse_allowed",
    "conventional_to_ultimate_collapse_allowed",
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def main() -> int:
    code = subprocess.run([sys.executable, str(CLOSURE_CHECKER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing: {rel}")
    text = DOC.read_text(encoding="utf-8") if DOC.is_file() else ""
    for token in [
        "implementation finality only",
        "Paramartha direct objectification is forbidden",
        "Samvrti denial is forbidden",
        "Ultimate-to-conventional collapse is forbidden",
        "Conventional-to-ultimate collapse is forbidden",
        "reference-only non-collapse barrier",
        "not proof, truth, essence authority, Ten'i authority, clinical authority, or execution authority",
    ]:
        if token not in text:
            errors.append(f"finality doc missing: {token}")
    att = json.loads(ATTEST.read_text(encoding="utf-8")) if ATTEST.is_file() else {}
    if att.get("mass_gap_bridge_authority") != "forbidden":
        errors.append("mass_gap_bridge_authority must be forbidden")
    if att.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
        errors.append("mass_gap_bridge_role mismatch")
    for key in FALSE_KEYS:
        if att.get(key) is not False:
            errors.append(f"attestation {key} must be false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Two Truths runtime finality checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
