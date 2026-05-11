#!/usr/bin/env python3
"""
validate_invariant_pipeline_release_attestation_v0_1.py

Stdlib-only validator for the KuuOS Invariant Pipeline Release Attestation.
Fresh-build default: runs the attestation builder first.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_invariant_pipeline_release_attestation_v0_1.py"
ATTESTATION = ROOT / "specs" / "invariant_pipeline_release_attestation_v0_1.generated.json"
BUNDLE_MANIFEST = ROOT / "specs" / "invariant_pipeline_release_bundle_manifest_v0_1.generated.json"
AUDIT_LEDGER = ROOT / "specs" / "invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl"
WORM_RECEIPT = ROOT / "specs" / "invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json"
DOC_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_RELEASE_ATTESTATION_v0_1.md"
POLICY_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md"

FALSE_FIELDS = [
    "execution_authority_granted",
    "proof_authority_granted",
    "clinical_authority_granted",
    "truth_authority_granted",
    "teni_authority_granted",
]

REQUIRED_DOC_STRINGS = [
    "The release attestation is an integrity summary surface only.",
    "execution_authority_granted: false",
    "proof_authority_granted: false",
    "clinical_authority_granted: false",
    "truth_authority_granted: false",
    "teni_authority_granted: false",
]


def read_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_ledger_root(path: pathlib.Path) -> str:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise ValueError("audit ledger is empty")
    return json.loads(lines[-1])["entry_hash"]


def validate_doc() -> list[str]:
    errors: list[str] = []
    if not DOC_PATH.is_file():
        return [f"missing release attestation doc: {DOC_PATH.relative_to(ROOT)}"]
    text = DOC_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_DOC_STRINGS:
        if item not in text:
            errors.append(f"doc missing required string: {item}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(validate_doc())
    for path in [BUILDER, BUNDLE_MANIFEST, AUDIT_LEDGER, WORM_RECEIPT, POLICY_PATH]:
        if not path.exists() and path != BUNDLE_MANIFEST:
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    result = subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    attestation = read_json(ATTESTATION)
    bundle = read_json(BUNDLE_MANIFEST)
    worm = read_json(WORM_RECEIPT)
    audit_root = read_ledger_root(AUDIT_LEDGER)

    if attestation.get("authority_note") != "release_attestation_is_integrity_summary_not_authority":
        errors.append("authority_note mismatch")
    if attestation.get("bundle_root_hash") != bundle.get("bundle_root_hash"):
        errors.append("bundle_root_hash mismatch")
    if attestation.get("audit_hash_chain_root_hash") != audit_root:
        errors.append("audit_hash_chain_root_hash mismatch")
    if attestation.get("worm_receipt_source_ledger_root_hash") != worm.get("source_ledger_root_hash"):
        errors.append("worm_receipt_source_ledger_root_hash mismatch")
    if attestation.get("worm_receipt_source_ledger_root_hash") != attestation.get("audit_hash_chain_root_hash"):
        errors.append("worm receipt root must match audit hash-chain root")
    if attestation.get("generated_manifest_policy_path") != "docs/INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md":
        errors.append("generated_manifest_policy_path mismatch")

    flags = attestation.get("non_authority_flags", {})
    for field in FALSE_FIELDS:
        if flags.get(field) is not False:
            errors.append(f"non_authority_flags.{field} must be false")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Invariant Pipeline release attestation validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
