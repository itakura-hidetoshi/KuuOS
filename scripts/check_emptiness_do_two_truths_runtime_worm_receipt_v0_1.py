#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_emptiness_do_two_truths_runtime_worm_receipt_v0_1.py"
CHAIN = ROOT / "specs" / "emptiness_do_two_truths_runtime_audit_chain_v0_1.generated.jsonl"
RECEIPT = ROOT / "specs" / "emptiness_do_two_truths_runtime_worm_receipt_v0_1.generated.json"

FALSE_FIELDS = [
    "K_is_object_allowed",
    "K_direct_observation_allowed",
    "flat_graph_dependent_origination_allowed",
    "string_or_brane_identified_with_K_allowed",
    "gap_reifies_ultimate_truth_allowed",
    "observable_directly_measures_K_allowed",
    "paramartha_samvrti_collapse_allowed",
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
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
    if receipt.get("mass_gap_bridge_role") != "reference_only_non_collapse_barrier":
        errors.append("mass_gap_bridge_role mismatch")
    for field in FALSE_FIELDS:
        if receipt.get(field) is not False:
            errors.append(f"{field} must be false")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print(f"PASS: Integrated emptiness DO two truths WORM receipt checked root={root} entries={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
