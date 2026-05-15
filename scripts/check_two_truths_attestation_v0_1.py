#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_two_truths_runtime_attestation_v0_1.py"
ATTEST = ROOT / "specs" / "two_truths_runtime_attestation_v0_1.generated.json"
BUNDLE = ROOT / "specs" / "two_truths_runtime_bundle_v0_1.generated.json"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"
WORM = ROOT / "specs" / "two_truths_runtime_worm_receipt_v0_1.generated.json"

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


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def chain_root() -> str:
    rows = [line for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty chain")
    return json.loads(rows[-1])["entry_hash"]


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    att = read_json(ATTEST)
    bundle = read_json(BUNDLE)
    worm = read_json(WORM)
    root = chain_root()
    errors: list[str] = []
    if att.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if att.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
        errors.append("mass_gap_bridge_role mismatch")
    if att.get("mass_gap_bridge_authority") != "forbidden":
        errors.append("mass_gap_bridge_authority must be forbidden")
    if att.get("bundle_root_hash") != bundle.get("bundle_root_hash"):
        errors.append("bundle root mismatch")
    if att.get("audit_chain_root_hash") != root:
        errors.append("audit chain root mismatch")
    if att.get("worm_receipt_source_chain_root_hash") != worm.get("source_chain_root_hash"):
        errors.append("worm root mismatch")
    if att.get("audit_chain_root_hash") != att.get("worm_receipt_source_chain_root_hash"):
        errors.append("audit and worm roots must match")
    for key in FALSE_KEYS:
        if att.get(key) is not False:
            errors.append(f"{key} must be false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("PASS: Two Truths runtime attestation checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
