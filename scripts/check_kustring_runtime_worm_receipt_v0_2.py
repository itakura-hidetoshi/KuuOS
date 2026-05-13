#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "scripts" / "export_kustring_runtime_worm_receipt_v0_2.py"
CHAIN = ROOT / "specs" / "kustring_runtime_audit_chain_v0_2.generated.jsonl"
RECEIPT = ROOT / "specs" / "kustring_runtime_worm_receipt_v0_2.generated.json"
FLAGS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "essence_authority_granted",
    "teni_authority_granted",
]


def chain_root_and_count() -> tuple[str, int]:
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty chain")
    return json.loads(lines[-1])["entry_hash"], len(lines)


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
    for flag in FLAGS:
        if receipt.get(flag) is not False:
            errors.append(f"{flag} must be false")
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"PASS: KuString runtime WORM receipt checked root={root} entries={count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
