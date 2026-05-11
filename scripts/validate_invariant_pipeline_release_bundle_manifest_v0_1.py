#!/usr/bin/env python3
"""
validate_invariant_pipeline_release_bundle_manifest_v0_1.py

Stdlib-only validator for the KuuOS Invariant Pipeline Release Bundle Manifest.

Fresh-build default: this validator runs the builder first so stale generated manifests
cannot pass or fail incorrectly after source files change.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "specs" / "invariant_pipeline_release_bundle_manifest_v0_1.generated.json"
BUILDER_PATH = ROOT / "scripts" / "build_invariant_pipeline_release_bundle_manifest_v0_1.py"

REQUIRED_FIXED_POINTS = [
    "release_bundle_manifest_is_integrity_surface_not_authority",
    "bundle_root_hash_proves_file_set_integrity_not_truth",
    "bundle_manifest_does_not_prove_teni_occurrence",
    "bundle_manifest_does_not_grant_execution_authority",
    "bundle_manifest_does_not_replace_worm_receipt",
]

REQUIRED_BUNDLE_FILES = [
    "docs/FORMAL_INVARIANT_SPINE_v0_1.md",
    "docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md",
    "docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md",
    "docs/INVARIANT_GATE_RUNTIME_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_v0_1.md",
    "docs/INVARIANT_GOVERNANCE_PIPELINE_AUDIT_EVENT_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_HASH_CHAIN_LEDGER_v0_1.md",
    "docs/INVARIANT_PIPELINE_AUDIT_WORM_EXPORT_RECEIPT_v0_1.md",
    "docs/INVARIANT_PIPELINE_RELEASE_BUNDLE_MANIFEST_v0_1.md",
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


def run_builder() -> int:
    print(f"INFO: running fresh builder: {BUILDER_PATH.relative_to(ROOT)}")
    return subprocess.run([sys.executable, str(BUILDER_PATH)], cwd=ROOT).returncode


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("authority_note") != "integrity_surface_not_authority":
        errors.append("authority_note must be integrity_surface_not_authority")

    fixed_points = set(manifest.get("fixed_points", []))
    for fp in REQUIRED_FIXED_POINTS:
        if fp not in fixed_points:
            errors.append(f"missing fixed point: {fp}")

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        return errors + ["manifest files must be a non-empty list"]

    listed_paths = {item.get("path") for item in files if isinstance(item, dict)}
    for required in REQUIRED_BUNDLE_FILES:
        if required not in listed_paths:
            errors.append(f"missing required bundle file in manifest: {required}")

    for item in files:
        rel = item.get("path")
        expected_sha = item.get("sha256")
        expected_size = item.get("size_bytes")
        if not isinstance(rel, str):
            errors.append("file entry missing path string")
            continue
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing bundle file: {rel}")
            continue
        actual_sha = sha256_file(path)
        if expected_sha != actual_sha:
            errors.append(f"sha256 mismatch for {rel}: expected {expected_sha}, got {actual_sha}")
        if expected_size != path.stat().st_size:
            errors.append(f"size mismatch for {rel}: expected {expected_size}, got {path.stat().st_size}")

    actual_root = compute_root(files)
    if manifest.get("bundle_root_hash") != actual_root:
        errors.append(f"bundle_root_hash mismatch: expected {actual_root}, got {manifest.get('bundle_root_hash')}")
    return errors


def main() -> int:
    builder_code = run_builder()
    if builder_code != 0:
        return builder_code

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: manifest JSON invalid: {exc}")
        return 1

    errors = validate_manifest(manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("PASS: Invariant Pipeline release bundle manifest validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
