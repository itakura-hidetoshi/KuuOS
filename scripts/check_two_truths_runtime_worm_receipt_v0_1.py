#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_two_truths_runtime_worm_receipt_v0_1.py"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"
RECEIPT = ROOT / "specs" / "two_truths_runtime_worm_receipt_v0_1.generated.json"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]
FALSE_FIELDS = [
    "paramartha_objectification_allowed",
    "samvrti_denial_allowed",
    "ultimate_to_conventional_collapse_allowed",
    "conventional_to_ultimate_collapse_allowed",
]


def chain_root_and_count() -> tuple[str, int]:
    rows = [line for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty chain")
    return json.loads(rows[-1])["entry_hash"], len(rows)


def main() -> int:
    code = subprocess.run([sys.executable, str(EXPORTER)], cwd=ROOT).returncode
    if code != 0:
        return code
    errors: list[str] = []
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    root, count = chain_root_and_count()
    if receipt.get("source_chain_root_hash") != root:
        errors.append("source_chain_root_hash mismatch")
    if receipt.get("exported_entry_count") != count:
        errors.append("exported_entry_count mismatch")
    if receipt.get("export_mode") != "WORM":
        errors.append("export_mode must be WORM")
    if receipt.get("implementation_not_proof") is not True:
        errors.append("implementation_not_proof must be true")
    if receipt.get("mass_gap_bridge_authority") != "forbidden":
        errors.append("mass_gap_bridge_authority must be forbidden")
    if receipt.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
        errors.append("mass_gap_bridge_role mismatch")
    for field in FALSE_FIELDS:
        if receipt.get(field) is not False:
            errors.append(f"{field} must be false")
    for flag in FLAGS:
        if receipt.get(flag) is not False:
            errors.append(f"{flag} must be false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: Two Truths runtime WORM receipt checked root={root} entries={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
