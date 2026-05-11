#!/usr/bin/env python3
"""
build_invariant_pipeline_release_bundle_manifest_v0_1.py

Stdlib-only builder for the KuuOS Invariant Pipeline Release Bundle Manifest.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "specs" / "invariant_pipeline_release_bundle_manifest_v0_1.generated.json"

BUNDLE_FILES = [
    "docs/FORMAL_INVARIANT_SPINE_v0_1.md",
    "docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md",
    "docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md",
    "docs/INVARIANT_GATE_RUNTIME_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_AUDIT_EVENT_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_MANIFEST_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_ATTESTATION_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_CLOSURE_PACKET_v0_1.md",
    "docs/INVARIANT_PIPELINE_GENERATED_MANIFEST_POLICY_v0_1.md",
    "docs/INVARIANT_PIPELINE_NAVIGATION_ADDENDUM_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_CHECKLIST_ADDENDUM_v0_1.md",
    "docs/INVARIANT_PIPELINE_PR_CHECKLIST_ADDENDUM_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_NAVIGATION_ADDENDUM_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_CHECKLIST_ADDENDUM_v0_1.md",
    "formal/KUOS/CoreGovernance/Invariants.lean",
    "formal/KUOS/CoreGovernance/SuperRelativityBridge.lean",
    "examples/invariant_preservation_matrix_minimal.py",
    "examples/invariant_gate_minimal.py",
    "examples/invariant_governance_pipeline_minimal.py",
    "specs/invariant_preservation_matrix_fixtures_v0_1.json",
    "specs/invariant_gate_fixtures_v0_1.json",
    "specs/invariant_governance_pipeline_fixtures_v0_1.json",
    "specs/invariant_pipeline_audit_hash_chain_fixture_v0_1.jsonl",
    "specs/invariant_pipeline_audit_worm_export_receipt_fixture_v0_1.json",
    "scripts/validate_formal_invariant_spine_v0_1.py",
    "scripts/validate_super_relativity_invariant_bridge_v0_1.py",
    "scripts/validate_invariant_preservation_matrix_v0_1.py",
    "scripts/validate_invariant_preservation_matrix_fixtures_v0_1.py",
    "scripts/validate_invariant_gate_fixtures_v0_1.py",
    "scripts/validate_invariant_governance_pipeline_v0_1.py",
    "scripts/validate_invariant_governance_pipeline_fixtures_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_event_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_hash_chain_v0_1.py",
    "scripts/validate_invariant_pipeline_audit_worm_export_receipt_v0_1.py",
    "scripts/build_invariant_pipeline_release_bundle_manifest_v0_1.py",
    "scripts/validate_invariant_pipeline_release_bundle_manifest_v0_1.py",
    "scripts/build_invariant_pipeline_release_attestation_v0_1.py",
    "scripts/validate_invariant_pipeline_release_attestation_v0_1.py",
    "scripts/validate_invariant_pipeline_release_closure_packet_v0_1.py",
]

FIXED_POINTS = [
    "release_bundle_manifest_is_integrity_surface_not_authority",
    "bundle_root_hash_proves_file_set_integrity_not_truth",
    "bundle_manifest_does_not_prove_teni_occurrence",
    "bundle_manifest_does_not_grant_execution_authority",
    "bundle_manifest_does_not_replace_worm_receipt",
]


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_root(files: list[dict[str, Any]]) -> str:
    ordered = sorted(files, key=lambda x: x["path"])
    payload = "".join(item["path"] + item["sha256"] for item in ordered)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_manifest() -> dict[str, Any]:
    file_entries: list[dict[str, Any]] = []
    for rel in BUNDLE_FILES:
        path = ROOT / rel
        if not path.is_file():
            raise FileNotFoundError(rel)
        file_entries.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })

    return {
        "id": "invariant_pipeline_release_bundle_manifest_v0_1",
        "version": "0.1",
        "date": "2026-05-11",
        "author": "Hidetoshi Itakura / 板倉英俊",
        "authority_note": "integrity_surface_not_authority",
        "fixed_points": FIXED_POINTS,
        "files": sorted(file_entries, key=lambda x: x["path"]),
        "bundle_root_hash": compute_root(file_entries),
    }


def main() -> int:
    manifest = build_manifest()
    OUTPUT_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE: {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"bundle_root_hash: {manifest['bundle_root_hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
