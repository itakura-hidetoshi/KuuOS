#!/usr/bin/env python3
"""Validate the Physical Quantum Qi runtime manifest, release/finality/closure packets, and chain index v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "physical_quantum_qi_runtime_manifest_v0_1.json"
PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_runtime_release_packet_v0_1.json"
FINALITY_PATH = ROOT / "packets" / "physical_quantum_qi_runtime_finality_packet_v0_1.json"
CLOSURE_PATH = ROOT / "packets" / "physical_quantum_qi_runtime_release_closure_packet_v0_1.json"
CHAIN_INDEX_PATH = ROOT / "chain_indexes" / "physical_quantum_qi_runtime_chain_index_v0_1.json"

REQUIRED_MANIFEST_FILES = {
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_CONTRACT_v0_1.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_INDEX_v0_1.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_BASELINE_STATEMENT_v0_1.md",
    "specs/physical_quantum_qi_runtime_contract_v0_1.json",
    "examples/physical_quantum_qi_runtime_packet_v0_1.json",
    "validation_cases/physical_quantum_qi_runtime_validation_cases_v0_1.json",
    "scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py",
    "scripts/validate_physical_quantum_qi_runtime_release_packet_v0_1.py",
    "manifests/physical_quantum_qi_runtime_manifest_v0_1.json",
    "packets/physical_quantum_qi_runtime_release_packet_v0_1.json",
    "packets/physical_quantum_qi_runtime_finality_packet_v0_1.json",
    "packets/physical_quantum_qi_runtime_release_closure_packet_v0_1.json",
    "chain_indexes/physical_quantum_qi_runtime_chain_index_v0_1.json",
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

REQUIRED_CHAIN_PATHS = [
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_CONTRACT_v0_1.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_INDEX_v0_1.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_BASELINE_STATEMENT_v0_1.md",
    "specs/physical_quantum_qi_runtime_contract_v0_1.json",
    "examples/physical_quantum_qi_runtime_packet_v0_1.json",
    "validation_cases/physical_quantum_qi_runtime_validation_cases_v0_1.json",
    "scripts/validate_physical_quantum_qi_runtime_contract_v0_1.py",
    "manifests/physical_quantum_qi_runtime_manifest_v0_1.json",
    "packets/physical_quantum_qi_runtime_release_packet_v0_1.json",
    "scripts/validate_physical_quantum_qi_runtime_release_packet_v0_1.py",
    "packets/physical_quantum_qi_runtime_finality_packet_v0_1.json",
    "packets/physical_quantum_qi_runtime_release_closure_packet_v0_1.json",
    ".github/workflows/physical_quantum_qi_runtime_validation.yml",
]

REQUIRED_CLOSURE_FLAGS = {
    "runtime_contract_present",
    "baseline_statement_present",
    "machine_readable_spec_present",
    "example_packet_present",
    "validation_cases_present",
    "runtime_validator_present",
    "manifest_present",
    "release_packet_present",
    "finality_packet_present",
    "chain_index_present",
    "dedicated_ci_workflow_present",
    "all_governance_runner_includes_qi",
    "all_governance_workflow_tracks_release_dirs",
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


def validate_authority_false(boundaries: Dict[str, Any], prefix: str) -> List[str]:
    errors: List[str] = []
    for key in sorted(AUTHORITY_FALSE_FIELDS):
        if boundaries.get(key) is not False:
            errors.append(f"{prefix}.{key} must be false")
    return errors


def validate_release_packet(packet: Dict[str, Any], manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_runtime_release_packet_v0_1":
        errors.append("release packet_id mismatch")
    if packet.get("manifest") != "manifests/physical_quantum_qi_runtime_manifest_v0_1.json":
        errors.append("release packet manifest pointer mismatch")

    errors.extend(validate_authority_false(packet.get("declared_boundaries", {}), "declared_boundaries"))

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


def validate_finality_packet(finality: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if finality.get("packet_id") != "physical_quantum_qi_runtime_finality_packet_v0_1":
        errors.append("finality packet_id mismatch")
    if finality.get("root_release_packet") != "packets/physical_quantum_qi_runtime_release_packet_v0_1.json":
        errors.append("finality root_release_packet mismatch")
    if finality.get("manifest") != "manifests/physical_quantum_qi_runtime_manifest_v0_1.json":
        errors.append("finality manifest pointer mismatch")

    declaration = finality.get("finality_declaration", {})
    for key in [
        "additive_only",
        "tighten_only_default",
        "overwrite_forbidden",
        "destructive_replacement_forbidden",
        "same_root_required",
        "nonexecution_by_default",
    ]:
        if declaration.get(key) is not True:
            errors.append(f"finality_declaration.{key} must be true")

    locked = set(finality.get("locked_invariants", []))
    missing_locked = sorted(REQUIRED_INVARIANTS - locked)
    if missing_locked:
        errors.append("finality missing locked invariants: " + ", ".join(missing_locked))

    errors.extend(validate_authority_false(finality.get("authority_boundary", {}), "authority_boundary"))
    return errors


def validate_closure_packet(closure: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if closure.get("packet_id") != "physical_quantum_qi_runtime_release_closure_packet_v0_1":
        errors.append("closure packet_id mismatch")
    expected_refs = {
        "chain_index": "chain_indexes/physical_quantum_qi_runtime_chain_index_v0_1.json",
        "manifest": "manifests/physical_quantum_qi_runtime_manifest_v0_1.json",
        "release_packet": "packets/physical_quantum_qi_runtime_release_packet_v0_1.json",
        "finality_packet": "packets/physical_quantum_qi_runtime_finality_packet_v0_1.json",
    }
    for key, expected in expected_refs.items():
        if closure.get(key) != expected:
            errors.append(f"closure {key} pointer mismatch")

    requirements = closure.get("closure_requirements", {})
    for flag in sorted(REQUIRED_CLOSURE_FLAGS):
        if requirements.get(flag) is not True:
            errors.append(f"closure_requirements.{flag} must be true")

    closed = set(closure.get("closed_invariants", []))
    missing_closed = sorted(REQUIRED_INVARIANTS - closed)
    if missing_closed:
        errors.append("closure missing closed invariants: " + ", ".join(missing_closed))

    entrypoints = set(closure.get("required_validation_entrypoints", []))
    if "make physical-quantum-qi-runtime-checks" not in entrypoints:
        errors.append("closure missing Qi runtime validation entrypoint")
    if "make all-governance-checks" not in entrypoints:
        errors.append("closure missing all-governance validation entrypoint")

    errors.extend(validate_authority_false(closure.get("authority_boundary", {}), "authority_boundary"))
    statement = closure.get("closure_statement", "")
    for phrase in ["no proof", "ontology", "clinical", "execution", "belief commit", "memory overwrite", "world-root rewrite", "safety override"]:
        if phrase not in statement:
            errors.append(f"closure_statement missing phrase: {phrase}")
    return errors


def validate_chain_index(chain_index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if chain_index.get("chain_index_id") != "physical_quantum_qi_runtime_chain_index_v0_1":
        errors.append("chain_index_id mismatch")
    if chain_index.get("update_policy") != "additive_only":
        errors.append("chain index update_policy must be additive_only")
    if chain_index.get("overwrite_policy") != "forbidden":
        errors.append("chain index overwrite_policy must be forbidden")

    chain = chain_index.get("chain", [])
    paths = [entry.get("path") for entry in chain]
    for required in REQUIRED_CHAIN_PATHS:
        if required not in paths:
            errors.append(f"chain index missing path: {required}")
        elif not (ROOT / required).exists():
            errors.append(f"chain index references missing repository file: {required}")

    orders = [entry.get("order") for entry in chain]
    if orders != sorted(orders):
        errors.append("chain index orders must be sorted")
    if len(set(orders)) != len(orders):
        errors.append("chain index orders must be unique")

    statement = chain_index.get("non_authority_statement", "")
    for phrase in ["no proof", "execution", "belief commit", "memory overwrite", "world-root rewrite", "safety override"]:
        if phrase not in statement:
            errors.append(f"chain non_authority_statement missing phrase: {phrase}")
    return errors


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    packet = load_json(PACKET_PATH)
    finality = load_json(FINALITY_PATH)
    closure = load_json(CLOSURE_PATH)
    chain_index = load_json(CHAIN_INDEX_PATH)

    errors: List[str] = []
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_release_packet(packet, manifest))
    errors.extend(validate_finality_packet(finality))
    errors.extend(validate_closure_packet(closure))
    errors.extend(validate_chain_index(chain_index))

    if errors:
        print("Physical Quantum Qi runtime release/finality/closure/chain validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi runtime release/finality/closure/chain validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
