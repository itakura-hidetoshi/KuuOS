#!/usr/bin/env python3
"""Validate the Physical Quantum Qi deepening manifest, release/finality packets, and chain index v0.2."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "physical_quantum_qi_deepening_manifest_v0_2.json"
RELEASE_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_release_packet_v0_2.json"
FINALITY_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_finality_packet_v0_2.json"
CHAIN_INDEX_PATH = ROOT / "chain_indexes" / "physical_quantum_qi_deepening_chain_index_v0_2.json"

REQUIRED_MODULES = {
    "SK_FV_path_integral",
    "Ward_leak_identity",
    "DPI_recoverability",
    "IndraNet_gauge_transport",
    "KuString_Qi_emergence_bridge",
}

REQUIRED_FILES = {
    "specs/physical_quantum_qi_deepening_contract_v0_2.json",
    "examples/physical_quantum_qi_deepening_packet_v0_2.json",
    "validation_cases/physical_quantum_qi_deepening_validation_cases_v0_2.json",
    "scripts/validate_physical_quantum_qi_deepening_v0_2.py",
    "scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
    "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
    "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
    "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
    "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
    ".github/workflows/physical_quantum_qi_deepening_validation.yml",
    ".github/workflows/all_governance_validation.yml",
    "Makefile",
    "scripts/run_all_governance_full_checks_v0_1.py",
}

REQUIRED_INVARIANTS = {
    "FullPathQi requires SK/FV history evidence",
    "PhysicalQi requires Ward/leak accounting",
    "Recovery claims require positive delta_rec",
    "IndraNet Qi transport requires gauge connection and holonomy accounting",
    "Qi emerges from delta_rel through string/brane/gauge/current structure and never directly from K",
    "MGAP4D 33/20 remains a stable floor, not a Qi source",
    "No v0.2 module grants execution authority",
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
    "specs/physical_quantum_qi_deepening_contract_v0_2.json",
    "examples/physical_quantum_qi_deepening_packet_v0_2.json",
    "validation_cases/physical_quantum_qi_deepening_validation_cases_v0_2.json",
    "scripts/validate_physical_quantum_qi_deepening_v0_2.py",
    "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
    "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
    "scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
    "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
    ".github/workflows/physical_quantum_qi_deepening_validation.yml",
]


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_file_lists(files: Dict[str, Any]) -> set[str]:
    out: set[str] = set()
    for value in files.values():
        if isinstance(value, list):
            out.update(str(item) for item in value)
    return out


def validate_authority_false(boundaries: Dict[str, Any], prefix: str) -> List[str]:
    errors: List[str] = []
    for key in sorted(AUTHORITY_FALSE_FIELDS):
        if boundaries.get(key) is not False:
            errors.append(f"{prefix}.{key} must be false")
    return errors


def validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("manifest_id") != "physical_quantum_qi_deepening_manifest_v0_2":
        errors.append("manifest_id mismatch")
    if manifest.get("root") != "physical_quantum_qi_runtime_baseline_established_final_packet_v0_1":
        errors.append("manifest root must point to v0.1 baseline established final packet")
    if manifest.get("update_policy") != "additive_only":
        errors.append("manifest update_policy must be additive_only")
    if manifest.get("overwrite_policy") != "forbidden":
        errors.append("manifest overwrite_policy must be forbidden")

    modules = set(manifest.get("deepening_modules", []))
    missing_modules = sorted(REQUIRED_MODULES - modules)
    if missing_modules:
        errors.append("manifest missing deepening modules: " + ", ".join(missing_modules))

    files = flatten_file_lists(manifest.get("files", {}))
    missing_files = sorted(REQUIRED_FILES - files)
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
    for required in [
        "make physical-quantum-qi-deepening-checks",
        "python3 scripts/validate_physical_quantum_qi_deepening_v0_2.py",
        "python3 scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
        "make all-governance-checks",
    ]:
        if required not in entrypoints:
            errors.append(f"manifest missing validation entrypoint: {required}")
    return errors


def validate_release_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_deepening_release_packet_v0_2":
        errors.append("release packet_id mismatch")
    if packet.get("manifest") != "manifests/physical_quantum_qi_deepening_manifest_v0_2.json":
        errors.append("release packet manifest pointer mismatch")
    if packet.get("root_baseline") != "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json":
        errors.append("release packet root_baseline pointer mismatch")

    claims = "\n".join(packet.get("core_claims", []))
    required_phrases = [
        "FullPathQi requires SK/FV history evidence",
        "PhysicalQi requires Ward/leak accounting",
        "positive delta_rec",
        "IndraNet Qi transport requires gauge connection",
        "Qi never emerges directly from K",
        "33/20 remains a stable floor, not a Qi source",
        "No v0.2 deepening module grants execution authority",
    ]
    for phrase in required_phrases:
        if phrase not in claims:
            errors.append(f"release packet core_claims missing phrase: {phrase}")

    errors.extend(validate_authority_false(packet.get("declared_boundaries", {}), "declared_boundaries"))

    checks = set(packet.get("required_checks", []))
    if "make physical-quantum-qi-deepening-checks" not in checks:
        errors.append("release packet missing deepening required check")
    if "make all-governance-checks" not in checks:
        errors.append("release packet missing all-governance required check")
    return errors


def validate_finality_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_deepening_finality_packet_v0_2":
        errors.append("finality packet_id mismatch")
    if packet.get("root_release_packet") != "packets/physical_quantum_qi_deepening_release_packet_v0_2.json":
        errors.append("finality root_release_packet mismatch")
    if packet.get("manifest") != "manifests/physical_quantum_qi_deepening_manifest_v0_2.json":
        errors.append("finality manifest pointer mismatch")
    if packet.get("root_baseline") != "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json":
        errors.append("finality root_baseline pointer mismatch")

    declaration = packet.get("finality_declaration", {})
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

    locked_modules = set(packet.get("locked_modules", []))
    missing_modules = sorted(REQUIRED_MODULES - locked_modules)
    if missing_modules:
        errors.append("finality missing locked modules: " + ", ".join(missing_modules))

    locked = set(packet.get("locked_invariants", []))
    missing_locked = sorted(REQUIRED_INVARIANTS - locked)
    if missing_locked:
        errors.append("finality missing locked invariants: " + ", ".join(missing_locked))

    errors.extend(validate_authority_false(packet.get("authority_boundary", {}), "authority_boundary"))
    return errors


def validate_chain_index(chain_index: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if chain_index.get("chain_index_id") != "physical_quantum_qi_deepening_chain_index_v0_2":
        errors.append("chain_index_id mismatch")
    if chain_index.get("root_baseline") != "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json":
        errors.append("chain root_baseline pointer mismatch")
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
    release_packet = load_json(RELEASE_PACKET_PATH)
    finality_packet = load_json(FINALITY_PACKET_PATH)
    chain_index = load_json(CHAIN_INDEX_PATH)

    errors: List[str] = []
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_release_packet(release_packet))
    errors.extend(validate_finality_packet(finality_packet))
    errors.extend(validate_chain_index(chain_index))

    if errors:
        print("Physical Quantum Qi deepening release/finality/chain validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi deepening release/finality/chain validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
