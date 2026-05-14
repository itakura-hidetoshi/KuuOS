#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_do_sheaf_gauge_runtime_audit_chain_v0_2.py"
CHAIN = ROOT / "specs" / "do_sheaf_gauge_runtime_audit_chain_v0_2.generated.jsonl"
OUT = ROOT / "specs" / "do_sheaf_gauge_runtime_worm_receipt_v0_2.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def chain_root_and_count() -> tuple[str, int]:
    rows = [x for x in CHAIN.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not rows:
        raise ValueError("empty sheaf gauge dependent origination audit chain")
    return json.loads(rows[-1])["entry_hash"], len(rows)


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    root, count = chain_root_and_count()
    receipt = {
        "id": "do_sheaf_gauge_runtime_worm_receipt_v0_2",
        "version": "0.2",
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_chain": "specs/do_sheaf_gauge_runtime_audit_chain_v0_2.generated.jsonl",
        "source_chain_root_hash": root,
        "exported_entry_count": count,
        "export_mode": "WORM",
        "retention_policy": "local_fixture_append_only",
        "object_lock_mode": "local_fixture",
        "authority_note": "do_sheaf_gauge_runtime_worm_receipt_is_record_surface_only",
        "implementation_not_proof": True,
        "graph_only_model_allowed": False,
        "site_cover_required": True,
        "gluing_required": True,
        "gauge_connection_required": True,
        "holonomy_record_required": True,
        "curvature_visibility_required": True,
        **FLAGS,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"root: {root}")
    print(f"entries: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
