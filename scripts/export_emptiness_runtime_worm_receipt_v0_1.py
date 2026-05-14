#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAIN_BUILDER = ROOT / "scripts" / "build_emptiness_runtime_audit_chain_v0_1.py"
CHAIN = ROOT / "specs" / "emptiness_runtime_audit_chain_v0_1.generated.jsonl"
OUT = ROOT / "specs" / "emptiness_runtime_worm_receipt_v0_1.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def chain_root_and_count() -> tuple[str, int]:
    lines = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty emptiness runtime audit chain")
    return json.loads(lines[-1])["entry_hash"], len(lines)


def main() -> int:
    code = subprocess.run([sys.executable, str(CHAIN_BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    root, count = chain_root_and_count()
    receipt = {
        "id": "emptiness_runtime_worm_receipt_v0_1",
        "version": "0.1",
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_chain": "specs/emptiness_runtime_audit_chain_v0_1.generated.jsonl",
        "source_chain_root_hash": root,
        "exported_entry_count": count,
        "export_mode": "WORM",
        "retention_policy": "local_fixture_append_only",
        "object_lock_mode": "local_fixture",
        "authority_note": "emptiness_runtime_worm_receipt_is_record_surface_only",
        "implementation_not_proof": True,
        **FLAGS,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"root: {root}")
    print(f"entries: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
