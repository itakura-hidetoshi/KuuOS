#!/usr/bin/env python3
"""Validate the Physical Quantum Qi deepening v0.2 release chain.

This validator intentionally checks both governance packets and equation/runtime
content.  Physical Quantum Qi v0.2 is not valid unless the equation document,
machine-readable equation packet, phase runtime, OS bridge runtime, runtime
bridge tests, phase demo, and Qi OS handoff surface are present in the
manifest/chain and on disk.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

MANIFEST_PATH = ROOT / "manifests" / "physical_quantum_qi_deepening_manifest_v0_2.json"
CHAIN_INDEX_PATH = ROOT / "chain_indexes" / "physical_quantum_qi_deepening_chain_index_v0_2.json"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_deepening_validation_cases_v0_2.json"
RELEASE_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_release_packet_v0_2.json"
FINALITY_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_finality_packet_v0_2.json"
CLOSURE_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_release_closure_packet_v0_2.json"
VALIDATED_BASELINE_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_validated_baseline_packet_v0_2.json"
BASELINE_ESTABLISHED_FINAL_PACKET_PATH = ROOT / "packets" / "physical_quantum_qi_deepening_baseline_established_final_packet_v0_2.json"

REQUIRED_MODULES = {
    "SK_FV_path_integral",
    "Ward_leak_identity",
    "DPI_recoverability",
    "IndraNet_gauge_transport",
    "KuString_Qi_emergence_bridge",
    "Qi_OS_handoff",
    "Qi_OS_bridge_packet",
}

REQUIRED_FILES = {
    "docs/PHYSICAL_QUANTUM_QI_EQUATIONS_v0_2.md",
    "specs/physical_quantum_qi_deepening_contract_v0_2.json",
    "examples/physical_quantum_qi_deepening_packet_v0_2.json",
    "examples/physical_quantum_qi_equation_packet_v0_2.json",
    "examples/run_physical_quantum_qi_phase_demo_v0_2.py",
    "src/physical_quantum_qi_phase_runtime_v0_2.py",
    "src/physical_quantum_qi_os_bridge_v0_2.py",
    "tests/test_physical_quantum_qi_phase_runtime_v0_2.py",
    "tests/test_physical_quantum_qi_os_bridge_v0_2.py",
    "validation_cases/physical_quantum_qi_deepening_validation_cases_v0_2.json",
    "scripts/validate_physical_quantum_qi_equations_v0_2.py",
    "scripts/validate_physical_quantum_qi_equation_packet_v0_2.py",
    "scripts/validate_physical_quantum_qi_deepening_v0_2.py",
    "scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
    "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
    "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
    "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
    "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
    "packets/physical_quantum_qi_deepening_release_closure_packet_v0_2.json",
    "packets/physical_quantum_qi_deepening_validated_baseline_packet_v0_2.json",
    "packets/physical_quantum_qi_deepening_baseline_established_final_packet_v0_2.json",
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
    "Qi phase classification is a routing surface, not an authority grant",
    "FullPathQi is MemoryOS-recordable and ReflectionOS-analyzable but not executable",
    "No v0.2 module grants execution authority",
    "Equation-level content is required for v0.2 deepening",
    "Machine-readable equation packet must expose required equation keys",
    "Equation packet must classify as FullPathQi through the phase runtime demo",
    "Equation packet must expose Qi_OS_handoff",
    "Declared Qi_OS_handoff must match runtime-computed handoff",
    "Qi_OS_bridge_packet must expose candidate-only OS payloads",
    "Qi_OS_bridge_packet must keep all authority fields false",
    "Baseline established final packet must declare authority_boundary_complete",
}

REQUIRED_CASE_NAMES = {
    "baseline_authority_boundary_complete_pass",
    "baseline_authority_boundary_incomplete_fails",
}

REQUIRED_ENTRYPOINTS = {
    "make physical-quantum-qi-deepening-checks",
    "python3 scripts/validate_physical_quantum_qi_equations_v0_2.py",
    "python3 scripts/validate_physical_quantum_qi_equation_packet_v0_2.py",
    "python3 tests/test_physical_quantum_qi_phase_runtime_v0_2.py",
    "python3 tests/test_physical_quantum_qi_os_bridge_v0_2.py",
    "python3 examples/run_physical_quantum_qi_phase_demo_v0_2.py",
    "python3 scripts/validate_physical_quantum_qi_deepening_v0_2.py",
    "python3 scripts/validate_physical_quantum_qi_deepening_release_packet_v0_2.py",
    "make all-governance-checks",
}

AUTHORITY_FALSE_FIELDS = {
    "proof_authority",
    "ontology_authority",
    "clinical_authority",
    "execution_authority",
    "commit_authority",
    "belief_commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "truth_authority",
    "safety_override_authority",
}

PACKET_REFS = {
    "release": {
        "path": RELEASE_PACKET_PATH,
        "packet_id": "physical_quantum_qi_deepening_release_packet_v0_2",
        "refs": {
            "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
            "root_baseline": "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json",
        },
        "authority_key": "declared_boundaries",
    },
    "finality": {
        "path": FINALITY_PACKET_PATH,
        "packet_id": "physical_quantum_qi_deepening_finality_packet_v0_2",
        "refs": {
            "root_release_packet": "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
            "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
            "root_baseline": "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json",
        },
        "authority_key": "authority_boundary",
    },
    "closure": {
        "path": CLOSURE_PACKET_PATH,
        "packet_id": "physical_quantum_qi_deepening_release_closure_packet_v0_2",
        "refs": {
            "root_baseline": "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json",
            "chain_index": "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
            "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
            "release_packet": "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
            "finality_packet": "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
        },
        "authority_key": "authority_boundary",
    },
    "validated_baseline": {
        "path": VALIDATED_BASELINE_PACKET_PATH,
        "packet_id": "physical_quantum_qi_deepening_validated_baseline_packet_v0_2",
        "refs": {
            "root_baseline": "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json",
            "chain_index": "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
            "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
            "release_packet": "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
            "finality_packet": "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
            "release_closure_packet": "packets/physical_quantum_qi_deepening_release_closure_packet_v0_2.json",
        },
        "authority_key": "authority_boundary",
    },
    "baseline_established_final": {
        "path": BASELINE_ESTABLISHED_FINAL_PACKET_PATH,
        "packet_id": "physical_quantum_qi_deepening_baseline_established_final_packet_v0_2",
        "refs": {
            "root_v0_1_baseline": "packets/physical_quantum_qi_runtime_baseline_established_final_packet_v0_1.json",
            "validated_baseline_packet": "packets/physical_quantum_qi_deepening_validated_baseline_packet_v0_2.json",
            "release_closure_packet": "packets/physical_quantum_qi_deepening_release_closure_packet_v0_2.json",
            "finality_packet": "packets/physical_quantum_qi_deepening_finality_packet_v0_2.json",
            "release_packet": "packets/physical_quantum_qi_deepening_release_packet_v0_2.json",
            "chain_index": "chain_indexes/physical_quantum_qi_deepening_chain_index_v0_2.json",
            "manifest": "manifests/physical_quantum_qi_deepening_manifest_v0_2.json",
        },
        "authority_key": "authority_boundary",
    },
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


def missing_items(required: Iterable[str], actual: Iterable[str]) -> List[str]:
    return sorted(set(required) - set(actual))


def validate_authority_false(packet: Dict[str, Any], authority_key: str, label: str) -> List[str]:
    authority = packet.get(authority_key, {})
    return [
        f"{label}.{authority_key}.{key} must be false"
        for key in sorted(AUTHORITY_FALSE_FIELDS)
        if authority.get(key) is not False
    ]


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

    errors.extend([f"manifest missing deepening module: {x}" for x in missing_items(REQUIRED_MODULES, manifest.get("deepening_modules", []))])

    files = flatten_file_lists(manifest.get("files", {}))
    errors.extend([f"manifest missing required file entry: {x}" for x in missing_items(REQUIRED_FILES, files)])
    for relpath in sorted(files):
        if not (ROOT / relpath).exists():
            errors.append(f"manifest references missing repository file: {relpath}")

    errors.extend([f"manifest missing invariant: {x}" for x in missing_items(REQUIRED_INVARIANTS, manifest.get("invariants", []))])
    errors.extend([f"manifest missing validation entrypoint: {x}" for x in missing_items(REQUIRED_ENTRYPOINTS, manifest.get("validation_entrypoints", []))])
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
    errors.extend([f"chain index missing path: {x}" for x in missing_items(REQUIRED_FILES - {"Makefile", "scripts/run_all_governance_full_checks_v0_1.py", ".github/workflows/all_governance_validation.yml"}, paths)])
    for relpath in sorted(set(paths)):
        if relpath and not (ROOT / relpath).exists():
            errors.append(f"chain index references missing repository file: {relpath}")

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


def validate_packet(label: str, spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    packet = load_json(spec["path"])
    if packet.get("packet_id") != spec["packet_id"]:
        errors.append(f"{label} packet_id mismatch")
    for key, expected in spec["refs"].items():
        if packet.get(key) != expected:
            errors.append(f"{label} {key} pointer mismatch")
    errors.extend(validate_authority_false(packet, spec["authority_key"], label))
    if label == "baseline_established_final":
        declaration = packet.get("baseline_established_final_declaration", {})
        if declaration.get("authority_boundary_complete") is not True:
            errors.append("baseline_established_final.baseline_established_final_declaration.authority_boundary_complete must be true")
    return errors


def validate_required_case_names(cases_doc: Dict[str, Any]) -> List[str]:
    names = {case.get("name") for case in cases_doc.get("cases", [])}
    return [f"validation cases missing required case: {x}" for x in missing_items(REQUIRED_CASE_NAMES, names)]


def validate_demo_packet_classification() -> List[str]:
    try:
        src = ROOT / "src"
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))
        from physical_quantum_qi_phase_runtime_v0_2 import classify_qi_phase, state_from_packet  # type: ignore
        from physical_quantum_qi_os_bridge_v0_2 import build_qi_os_bridge_packet, bridge_packet_to_dict, validate_qi_os_bridge_packet  # type: ignore
        from physical_quantum_qi_phase_runtime_v0_2 import qi_phase_handoff  # type: ignore

        packet = load_json(ROOT / "examples" / "physical_quantum_qi_equation_packet_v0_2.json")
        result = classify_qi_phase(state_from_packet(packet))
        if result.phase.value != "FullPathQi":
            return [f"phase demo packet must classify as FullPathQi, got {result.phase.value}"]
        handoff = qi_phase_handoff(result)
        bridge = bridge_packet_to_dict(build_qi_os_bridge_packet(handoff))
        bridge_errors = validate_qi_os_bridge_packet(bridge)
        if bridge_errors:
            return ["Qi OS bridge packet validation failed: " + "; ".join(bridge_errors)]
        return []
    except Exception as exc:  # pragma: no cover - CI diagnostic path
        return [f"phase demo packet classification raised {type(exc).__name__}: {exc}"]


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    chain_index = load_json(CHAIN_INDEX_PATH)
    cases_doc = load_json(CASES_PATH)

    errors: List[str] = []
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_chain_index(chain_index))
    errors.extend(validate_required_case_names(cases_doc))
    for label, spec in PACKET_REFS.items():
        errors.extend(validate_packet(label, spec))
    errors.extend(validate_demo_packet_classification())

    if errors:
        print("Physical Quantum Qi deepening release/finality/closure/baseline/final/chain validation failed:")
        print(f"diagnostic.root={ROOT}")
        print(f"diagnostic.chain_index={CHAIN_INDEX_PATH}")
        print("diagnostic.chain_paths=")
        for entry in chain_index.get("chain", []):
            print(f"  - {entry.get('order')}: {entry.get('role')} -> {entry.get('path')}")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi deepening release/finality/closure/baseline/final/chain validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
