#!/usr/bin/env python3
"""
build_invariant_pipeline_release_attestation_v0_1.py

Stdlib-only builder for the KuuOS Invariant Pipeline Release Attestation.
"""

from __future__ import annotations

import datetime
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLE_BUILDER = ROOT / "scripts" / "build_invariant_pipeline_release_bundle_manifest_v0_1.py"
BUNDLE_MANIFEST = ROOT / "specs" / "invariant_pipeline_release_bundle_manifest_v0_1.generated.json"
AUDIT_LEDGER = ROOT / "specs" / "invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl"
WORM_RECEIPT = ROOT / "specs" / "invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json"
POLICY_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md"
OUTPUT_PATH = ROOT / "specs" / "invariant_pipeline_release_attestation_v0_1.generated.json"

FALSE_FLAGS = {
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "truth_authority_granted": False,
    "teni_authority_granted": False,
}


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_ledger_root(path: pathlib.Path) -> str:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("audit ledger is empty")
    last = json.loads(lines[-1])
    return last["entry_hash"]


def build_attestation() -> dict[str, Any]:
    result = subprocess.run([sys.executable, str(BUNDLE_BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        raise RuntimeError("bundle manifest builder failed")

    bundle = read_json(BUNDLE_MANIFEST)
    worm = read_json(WORM_RECEIPT)
    audit_root = read_ledger_root(AUDIT_LEDGER)

    return {
        "id": "invariant_pipeline_release_attestation_v0_1",
        "version": "0.1",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "bundle_manifest_path": "specs/invariant_pipeline_release_bundle_manifest_v0_1.generated.json",
        "bundle_root_hash": bundle["bundle_root_hash"],
        "audit_hash_chain_path": "specs/invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl",
        "audit_hash_chain_root_hash": audit_root,
        "worm_receipt_path": "specs/invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json",
        "worm_receipt_source_ledger_root_hash": worm["source_ledger_root_hash"],
        "generated_manifest_policy_path": "docs/INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md",
        "authority_note": "release_attestation_is_integrity_summary_not_authority",
        "non_authority_flags": FALSE_FLAGS,
    }


def main() -> int:
    attestation = build_attestation()
    OUTPUT_PATH.write_text(json.dumps(attestation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"bundle_root_hash: {attestation['bundle_root_hash']}")
    print(f"audit_hash_chain_root_hash: {attestation['audit_hash_chain_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
