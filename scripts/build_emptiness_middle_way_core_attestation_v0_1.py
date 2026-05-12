#!/usr/bin/env python3
from __future__ import annotations

import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE_BUILDER = ROOT / "scripts" / "build_emptiness_middle_way_core_bundle_v0_1.py"
BUNDLE_MANIFEST = ROOT / "specs" / "emptiness_middle_way_core_bundle_v0_1.generated.json"
LEDGER = ROOT / "specs" / "emptiness_middle_way_core_audit_hash_chain_fixture_v0_1.jsonl"
WORM = ROOT / "specs" / "emptiness_middle_way_core_audit_worm_export_receipt_fixture_v0_1.json"
OUT = ROOT / "specs" / "emptiness_middle_way_core_attestation_v0_1.generated.json"


def read_json(path: pathlib.Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def ledger_root() -> str:
    lines = [x for x in LEDGER.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines:
        raise ValueError("empty core ledger")
    return json.loads(lines[-1])["entry_hash"]


def main() -> int:
    result = subprocess.run([sys.executable, str(BUNDLE_BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode
    bundle = read_json(BUNDLE_MANIFEST)
    worm = read_json(WORM)
    root = ledger_root()
    attestation = {
        "id": "emptiness_middle_way_core_attestation_v0_1",
        "version": "0.1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "bundle_manifest_path": "specs/emptiness_middle_way_core_bundle_v0_1.generated.json",
        "bundle_root_hash": bundle["bundle_root_hash"],
        "audit_hash_chain_path": "specs/emptiness_middle_way_core_audit_hash_chain_fixture_v0_1.jsonl",
        "audit_hash_chain_root_hash": root,
        "worm_receipt_path": "specs/emptiness_middle_way_core_audit_worm_export_receipt_fixture_v0_1.json",
        "worm_receipt_source_ledger_root_hash": worm["source_ledger_root_hash"],
        "authority_note": "integrity_summary_only",
        "execution_authority_granted": False,
        "proof_authority_granted": False,
        "truth_authority_granted": False,
        "essence_authority_granted": False,
        "teni_authority_granted": False
    }
    OUT.write_text(json.dumps(attestation, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {OUT.relative_to(ROOT)}")
    print(f"bundle_root_hash: {attestation['bundle_root_hash']}")
    print(f"audit_hash_chain_root_hash: {attestation['audit_hash_chain_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
