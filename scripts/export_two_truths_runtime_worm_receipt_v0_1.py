#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_two_truths_runtime_audit_chain_v0_1.py"
CHAIN = ROOT / "specs" / "two_truths_runtime_audit_chain_v0_1.generated.jsonl"
OUT = ROOT / "specs" / "two_truths_runtime_worm_receipt_v0_1.generated.json"

FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "truth_authority_granted": False,
    "essence_authority_granted": False,
    "teni_authority_granted": False,
}


def chain_root_and_count() -> tuple[str, int]:
    rows = [line for line in CHAIN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        raise ValueError("empty two truths runtime audit chain")
    return json.loads(rows[-1])["entry_hash"], len(rows)


def main() -> int:
    code = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT).returncode
    if code != 0:
        return code
    root, count = chain_root_and_count()
    receipt = {
        "id": "two_truths_runtime_worm_receipt_v0_1",
        "version": "0.1",
        "exported_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_chain": "specs/two_truths_runtime_audit_chain_v0_1.generated.jsonl",
        "source_chain_root_hash": root,
        "exported_entry_count": count,
        "export_mode": "WORM",
        "retention_policy": "local_fixture_append_only",
        "object_lock_mode": "local_fixture",
        "adapter": "examples/two_truths_mass_gap_runtime_adapter_minimal.py",
        "authority_note": "two_truths_runtime_worm_receipt_is_record_surface_only",
        "implementation_not_proof": True,
        "paramartha_objectification_allowed": False,
        "samvrti_denial_allowed": False,
        "ultimate_to_conventional_collapse_allowed": False,
        "conventional_to_ultimate_collapse_allowed": False,
        "mass_gap_bridge_authority": "forbidden",
        "mass_gap_bridge_role": "reference_only_non_collapse_barrier",
        **FLAGS,
    }
    OUT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"root: {root}")
    print(f"entries: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
