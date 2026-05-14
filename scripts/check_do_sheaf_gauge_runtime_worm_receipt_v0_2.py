#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_do_sheaf_gauge_runtime_worm_receipt_v0_2.py"
CHAIN = ROOT / "specs" / "do_sheaf_gauge_runtime_audit_chain_v0_2.generated.jsonl"
RECEIPT = ROOT / "specs" / "do_sheaf_gauge_runtime_worm_receipt_v0_2.generated.json"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]
TRUE_FIELDS = [
    "site_cover_required",
    "gluing_required",
    "gauge_connection_required",
    "holonomy_record_required",
    "curvature_visibility_required",
]


def chain_root_and_count() -> tuple[str, int]:
    rows = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
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
    if receipt.get("graph_only_model_allowed") is not False:
        errors.append("graph_only_model_allowed must be false")
    for field in TRUE_FIELDS:
        if receipt.get(field) is not True:
            errors.append(f"{field} must be true")
    for flag in FLAGS:
        if receipt.get(flag) is not False:
            errors.append(f"{flag} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: DO sheaf gauge WORM receipt checked root={root} entries={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
