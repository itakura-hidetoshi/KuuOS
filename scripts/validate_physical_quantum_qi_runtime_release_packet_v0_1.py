#!/usr/bin/env python3
"""Validate the Physical Quantum Qi runtime manifest and release packet v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "physical_quantum_qi_runtime_manifest_v0_1.json"
PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_runtime_release_packet_v0_1.json"

REQUIRED_MANIFEST_FILES = {
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_CONTRACT_v0_1.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_INDEX_v0_1.md",
    "specs/physical_quantum_qi_runtime_contract_v0_1.json",
    "examples/physical_quantum_qi_runtime_packet_v0_1.json",
    "validation_cases/physical_quantum_qi_runtime_validation_cases_v0_1.json",
    "scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py",
    ".github/workflows/physical_quantum_qi_runtime_validation.yml",
    ".github/workflows/all_governance_validation.yml",
    "Makefile",
    "scripts/run_all_governance_full_checks_v0_1.py",
}

REQUIRED_INVARIANTS = {
    "Qi is not K",
    "Qi is not a mystical substance",
    "claimed_type is not authoritative",
    "validated_type is computed from evidence",
    "mass_gap_33_20 is a stable floor, not a Qi source",
    "Qi grants no execution authority",
    "Qi grants no belief commit authority",
    "Qi grants no memory overwrite authority",
    "Qi grants no world-root rewrite authority",
    "Qi grants no safety override authority",
}

AUTHORITY_FALSE_FIELDS = {
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "belief_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "safety_override_authority",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_file_lists(files: Dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for value in files.values():
        if isinstance(value, list):
            out.update(str(item) for item in value)
    return out


def validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("manifest_id") != "physical_quantum_qi_runtime_manifest_v0_1":
        errors.append("manifest_id mismatch")
    if manifest.get("update_policy") != "additive_only":
        errors.append("manifest update_policy must be additive_only")
    if manifest.get("overwrite_policy") != "forbidden":
        errors.append("manifest overwrite_policy must be forbidden")

    files = flatten_file_lists(manifest.get("files", {}))
    missing_files = sorted(REQUIRED_MANIFEST_FILES - files)
    if missing_files:
        errors.append("manifest missing required file entries: " + ", ".join(missing_files))

    for relpath in files:
        if not (ROOT / relpath).exists():
            errors.append(f"manifest references missing repository file: {relpath}")

    invariants = set(manifest.get("invariants", []))
    missing_invariants = sorted(REQUIRED_INVARIANTS - invariants)
    if missing_invariants:
        errors.append("manifest missing invariants: " + ", ".join(missing_invariants))

    entrypoints = set(manifest.get("validation_entrypoints", []))
    if "make physical-quantum-qi-runtime-checks" not in entrypoints:
        errors.append("manifest missing Qi runtime make entrypoint")
    if "make all-governance-checks" not in entrypoints:
        errors.append("manifest missing all-governance make entrypoint")
    return errors


def validate_release_packet(packet: Dict[str, Any], manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_runtime_release_packet_v0_1":
        errors.append("release packet_id mismatch")
    if packet.get("manifest") != "manifests/physical_quantum_qi_runtime_manifest_v0_1.json":
        errors.append("release packet manifest pointer mismatch")

    boundaries = packet.get("declared_boundaries", {})
    for key in sorted(AUTHORITY_FALSE_FIELDS):
        if boundaries.get(key) is not False:
            errors.append(f"declared_boundaries.{key} must be false")

    claims = "\n".join(packet.get("core_claims", []))
    if "Qi is not K" not in claims:
        errors.append("release packet must state Qi is not K")
    if "33/20 mass gap" not in claims or "not a Qi source" not in claims:
        errors.append("release packet must preserve mass-gap-as-floor-not-source boundary")
    if "claimed_type" not in claims or "validated_type" not in claims:
        errors.append("release packet must preserve claimed/validated type separation")

    checks = set(packet.get("required_checks", []))
    if "make physical-quantum-qi-runtime-checks" not in checks:
        errors.append("release packet missing Qi runtime required check")
    if "make all-governance-checks" not in checks:
        errors.append("release packet missing all-governance required check")

    if manifest.get("manifest_id") != "physical_quantum_qi_runtime_manifest_v0_1":
        errors.append("release packet validation could not resolve expected manifest")
    return errors


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    packet = load_json(PACKET_PATH)

    errors: List[str] = []
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_release_packet(packet, manifest))

    if errors:
        print("Physical Quantum Qi runtime release packet validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi runtime release packet validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
