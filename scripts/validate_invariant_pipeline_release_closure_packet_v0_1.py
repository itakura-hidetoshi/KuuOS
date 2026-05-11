#!/usr/bin/env python3
"""
validate_invariant_pipeline_release_closure_packet_v0_1.py

Stdlib-only validator for the KuuOS Invariant Pipeline Release Closure Packet.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "INVARIANT_PIPELINE_RELEASE_CLOSURE_PACKET_v0_1.md"

REQUIRED_FILES = [
    "docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md",
    "docs/FORMAL_INVARIANT_SPINE_v0_1.md",
    "docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md",
    "docs/INVARIANT_GATE_RUNTIME_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_AUDIT_EVENT_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_MANIFEST_v0_1.md",
    "docs/INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_ATTESTATION_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_CLOSURE_PACKET_v0_1.md",
    "scripts/validate_invariant_governance_pipeline_v0_1.py",
    "scripts/validate_invariant_governance_pipeline_fixtures_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_event_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py",
    "scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py",
    "scripts/validate_invariant_pipeline_release_attestation_v0_1.py",
]

REQUIRED_DOC_STRINGS = [
    "Release closure is an operational closure surface only.",
    "It does not create execution, proof, domain, truth, or Ten'i authority.",
    "non-authority flags remain false",
]

VALIDATOR_COMMANDS = [
    "scripts/validate_invariant_governance_pipeline_v0_1.py",
    "scripts/validate_invariant_governance_pipeline_fixtures_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_event_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py",
    "scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py",
    "scripts/validate_invariant_pipeline_release_attestation_v0_1.py",
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required closure file: {rel}")

    if DOC_PATH.is_file():
        text = DOC_PATH.read_text(encoding="utf-8")
        for item in REQUIRED_DOC_STRINGS:
            if item not in text:
                errors.append(f"closure packet missing required string: {item}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    for rel in VALIDATOR_COMMANDS:
        print("\n>>> " + rel, flush=True)
        result = subprocess.run([sys.executable, rel], cwd=ROOT)
        if result.returncode != 0:
            print(f"FAIL: {rel} exited with {result.returncode}")
            return result.returncode

    print("PASS: Invariant Pipeline release closure packet validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
