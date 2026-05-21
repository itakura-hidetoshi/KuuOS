#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "specs" / "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json"

REQUIRED_TOP_LEVEL = {
    "manifest_id",
    "version",
    "status",
    "repository",
    "scope",
    "lineage",
    "authority_boundary",
    "files",
    "validators",
    "ci_targets",
    "invariants",
    "forbidden_authority_tokens",
}

REQUIRED_SPAN = [
    "v0.2J", "v0.2K", "v0.2L", "v0.2M", "v0.2N", "v0.2O", "v0.2P", "v0.2Q", "v0.2R",
]

REQUIRED_PATHS = [
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_PACKET_v0_2JR.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_POST_MERGE_RECEIPT_v0_2JR.md",
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py",
    "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py",
    "scripts/check_physical_quantum_qi_runtime_evolution_finality_packet_v0_2JR.py",
    "scripts/check_physical_quantum_qi_runtime_evolution_finality_post_merge_receipt_v0_2JR.py",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "Makefile",
    ".github/workflows/physical_quantum_qi_runtime_evolution_validation.yml",
]

REQUIRED_TARGETS = [
    "make physical-quantum-qi-runtime-evolution-checks",
    "make physical-quantum-qi-runtime-evolution-bundle-checks",
    "make physical-quantum-qi-runtime-evolution-finality-checks",
    "make physical-quantum-qi-runtime-evolution-finality-post-merge-receipt-checks",
]

REQUIRED_LINEAGE_FIELDS = [
    "ci_receipt_surface",
    "bundle_surface",
    "finality_surface",
    "finality_post_merge_receipt_surface",
]


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.is_file():
        errors.append(f"missing manifest: {MANIFEST.relative_to(ROOT)}")
        data = {}
    else:
        try:
            data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON: {exc}")
            data = {}

    for key in sorted(REQUIRED_TOP_LEVEL.difference(data)):
        errors.append(f"manifest missing key: {key}")

    if data.get("manifest_id") != "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR":
        errors.append("unexpected manifest_id")
    if data.get("version") != "v0.2J-R":
        errors.append("unexpected version")
    if data.get("status") != "FINALITY_POST_MERGE_RECEIPT_BUNDLE_MANIFEST_RECORDED":
        errors.append("unexpected status")
    if data.get("repository") != "itakura-hidetoshi/KuuOS":
        errors.append("unexpected repository")

    lineage = data.get("lineage", {})
    span = lineage.get("runtime_evolution_span", [])
    for item in REQUIRED_SPAN:
        if item not in span:
            errors.append(f"missing span: {item}")
    for key in REQUIRED_LINEAGE_FIELDS:
        if lineage.get(key) != "v0.2J-R":
            errors.append(f"unexpected lineage field: {key}")

    boundary = data.get("authority_boundary", {})
    for key in ["validation_only", "candidate_only_where_applicable", "append_only", "same_root_required", "non_authoritative"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary true check failed: {key}")
    for key, value in boundary.items():
        if key.endswith("_authority_granted") and value is not False:
            errors.append(f"boundary false check failed: {key}")

    files = data.get("files", [])
    validators = data.get("validators", [])
    targets = data.get("ci_targets", [])
    for path in REQUIRED_PATHS:
        if path not in files:
            errors.append(f"files missing: {path}")
        if not (ROOT / path).is_file():
            errors.append(f"path missing on disk: {path}")
    for path in REQUIRED_PATHS[4:9]:
        if path not in validators:
            errors.append(f"validators missing: {path}")
    for target in REQUIRED_TARGETS:
        if target not in targets:
            errors.append(f"ci_targets missing: {target}")

    if not isinstance(data.get("invariants", []), list):
        errors.append("invariants must be a list")
    if not isinstance(data.get("forbidden_authority_tokens", []), list):
        errors.append("forbidden_authority_tokens must be a list")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Physical Quantum Qi runtime evolution post-merge receipt bundle manifest v0.2J-R validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
