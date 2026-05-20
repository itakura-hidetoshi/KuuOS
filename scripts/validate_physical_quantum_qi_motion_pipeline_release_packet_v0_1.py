#!/usr/bin/env python3
"""Validate the Physical Quantum Qi motion pipeline release surface v0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests" / "physical_quantum_qi_motion_pipeline_manifest_v0_1.json"
RELEASE_PATH = ROOT / "packets" / "physical_quantum_qi_motion_pipeline_release_packet_v0_1.json"
FINALITY_PATH = ROOT / "packets" / "physical_quantum_qi_motion_pipeline_finality_packet_v0_1.json"
CLOSURE_PATH = ROOT / "packets" / "physical_quantum_qi_motion_pipeline_release_closure_packet_v0_1.json"
BASELINE_PATH = ROOT / "packets" / "physical_quantum_qi_motion_pipeline_validated_baseline_packet_v0_1.json"
CHAIN_INDEX_PATH = ROOT / "chain_indexes" / "physical_quantum_qi_motion_pipeline_chain_index_v0_1.json"
RUNNER_PATH = ROOT / "scripts" / "run_qi_motion_chain_checks_v0_1.py"
RUNTIME_VALIDATOR_PATH = ROOT / "scripts" / "validate_physical_quantum_qi_motion_pipeline_v0_1.py"

REQUIRED_FILES = [
    MANIFEST_PATH,
    RELEASE_PATH,
    FINALITY_PATH,
    CLOSURE_PATH,
    BASELINE_PATH,
    CHAIN_INDEX_PATH,
    RUNNER_PATH,
    RUNTIME_VALIDATOR_PATH,
]

REQUIRED_REPO_PATHS = {
    "docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md",
    "examples/physical_quantum_qi_motion_pipeline_minimal.py",
    "validation_cases/physical_quantum_qi_motion_pipeline_cases_v0_1.json",
    "scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py",
    "scripts/validate_physical_quantum_qi_motion_pipeline_release_packet_v0_1.py",
    "manifests/physical_quantum_qi_motion_pipeline_manifest_v0_1.json",
    "packets/physical_quantum_qi_motion_pipeline_release_packet_v0_1.json",
    "packets/physical_quantum_qi_motion_pipeline_finality_packet_v0_1.json",
    "packets/physical_quantum_qi_motion_pipeline_release_closure_packet_v0_1.json",
    "packets/physical_quantum_qi_motion_pipeline_validated_baseline_packet_v0_1.json",
    "chain_indexes/physical_quantum_qi_motion_pipeline_chain_index_v0_1.json",
    "scripts/run_qi_motion_chain_checks_v0_1.py",
}

LOCKED_INVARIANTS = {
    "Qi motion is licensed by evidence-bound validated_type, not claimed_type",
    "validated_type is the dynamics license source",
    "unlicensed dynamics terms are ignored",
    "FullPathQi is the history-bearing process-tensor-style motion level",
    "motion output is a bounded observe-only candidate",
    "motion output grants no execution authority",
    "motion output grants no diagnosis authority",
    "motion output grants no treatment authorization",
    "motion output grants no medical act authorization",
    "medical modality boundary is neutral",
    "Qi is not denied by boundary wording",
    "East Asian medical reasoning is not denied by boundary wording",
    "biomedicine is not privileged by wording",
    "professional judgment remains required",
    "patient context remains required",
}

AUTHORITY_FALSE_FIELDS = {
    "execution_authority",
    "belief_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "safety_override_authority",
    "direct_execution_allowed",
    "authority_expansion",
    "standalone_diagnosis_authority",
    "standalone_treatment_authorization",
    "medical_act_authorization",
}

NEUTRAL_TRUE_FIELDS = {
    "medical_modality_neutral",
    "professional_judgment_required",
    "patient_context_required",
}

NEUTRAL_FALSE_FIELDS = {
    "qi_denied_by_boundary",
    "east_asian_medical_reasoning_denied",
    "biomedicine_privileged_by_wording",
}

BASELINE_TRUE_COMMITMENTS = {
    "additive_only",
    "tighten_only_default",
    "overwrite_forbidden",
    "destructive_replacement_forbidden",
    "same_root_required",
    "nonexecution_by_default",
    "claimed_type_not_authoritative",
    "validated_type_evidence_bound",
    "validated_type_licenses_dynamics",
    "unlicensed_terms_ignored",
    "observe_only_motion_candidate",
    "medical_modality_neutral_boundary_preserved",
}

BASELINE_FALSE_CLAIMS = {
    "direct_execution_allowed",
    "authority_expansion",
    "standalone_diagnosis_authority",
    "standalone_treatment_authorization",
    "medical_act_authorization",
    "qi_denied_by_boundary",
    "east_asian_medical_reasoning_denied",
    "biomedicine_privileged_by_wording",
}


def fail(message: str) -> int:
    print(f"[physical-quantum-qi-motion-pipeline-release] FAIL: {message}", file=sys.stderr)
    return 1


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_manifest_files(manifest: Dict[str, Any]) -> Set[str]:
    files: Set[str] = set()
    for value in manifest.get("files", {}).values():
        if isinstance(value, list):
            files.update(str(item) for item in value)
    return files


def require_true(mapping: Dict[str, Any], keys: Iterable[str], prefix: str, errors: List[str]) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not True:
            errors.append(f"{prefix}.{key} must be true")


def require_false(mapping: Dict[str, Any], keys: Iterable[str], prefix: str, errors: List[str]) -> None:
    for key in sorted(keys):
        if mapping.get(key) is not False:
            errors.append(f"{prefix}.{key} must be false")


def validate_manifest(manifest: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if manifest.get("manifest_id") != "physical_quantum_qi_motion_pipeline_manifest_v0_1":
        errors.append("manifest_id mismatch")
    if manifest.get("update_policy") != "additive_only":
        errors.append("manifest.update_policy must be additive_only")
    if manifest.get("overwrite_policy") != "forbidden":
        errors.append("manifest.overwrite_policy must be forbidden")
    if manifest.get("same_root_required") is not True:
        errors.append("manifest.same_root_required must be true")

    files = flatten_manifest_files(manifest)
    missing = sorted(REQUIRED_REPO_PATHS - files - {"scripts/run_qi_motion_chain_checks_v0_1.py"})
    if missing:
        errors.append("manifest missing required file entries: " + ", ".join(missing))
    for relpath in files:
        if not (ROOT / relpath).exists():
            errors.append(f"manifest references missing repository file: {relpath}")

    invariants = set(manifest.get("invariants", []))
    missing_invariants = sorted(LOCKED_INVARIANTS - invariants)
    if missing_invariants:
        errors.append("manifest missing invariants: " + ", ".join(missing_invariants))
    return errors


def validate_release_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_motion_pipeline_release_packet_v0_1":
        errors.append("release packet_id mismatch")
    if packet.get("manifest") != "manifests/physical_quantum_qi_motion_pipeline_manifest_v0_1.json":
        errors.append("release manifest pointer mismatch")
    claims = "\n".join(packet.get("core_claims", []))
    for phrase in ["claimed_type", "validated_type", "dynamics_license_source", "observe-only", "does not deny Qi", "does not privilege biomedicine"]:
        if phrase not in claims:
            errors.append(f"release core_claims missing phrase: {phrase}")
    boundary = packet.get("declared_boundaries", {})
    require_false(boundary, AUTHORITY_FALSE_FIELDS, "declared_boundaries", errors)
    require_true(boundary, NEUTRAL_TRUE_FIELDS, "declared_boundaries", errors)
    require_false(boundary, NEUTRAL_FALSE_FIELDS, "declared_boundaries", errors)
    checks = set(packet.get("required_checks", []))
    for entrypoint in [
        "python3 scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py",
        "python3 scripts/validate_physical_quantum_qi_motion_pipeline_release_packet_v0_1.py",
        "python3 scripts/run_qi_motion_chain_checks_v0_1.py",
    ]:
        if entrypoint not in checks:
            errors.append(f"release required_checks missing: {entrypoint}")
    return errors


def validate_finality_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_motion_pipeline_finality_packet_v0_1":
        errors.append("finality packet_id mismatch")
    if packet.get("root_release_packet") != "packets/physical_quantum_qi_motion_pipeline_release_packet_v0_1.json":
        errors.append("finality root_release_packet mismatch")
    declaration = packet.get("finality_declaration", {})
    require_true(
        declaration,
        {
            "additive_only",
            "tighten_only_default",
            "overwrite_forbidden",
            "destructive_replacement_forbidden",
            "same_root_required",
            "nonexecution_by_default",
            "validated_type_license_required",
            "medical_modality_neutral_boundary_required",
        },
        "finality_declaration",
        errors,
    )
    locked = set(packet.get("locked_invariants", []))
    missing_locked = sorted(LOCKED_INVARIANTS - locked)
    if missing_locked:
        errors.append("finality missing locked invariants: " + ", ".join(missing_locked))
    require_false(packet.get("authority_boundary", {}), AUTHORITY_FALSE_FIELDS, "authority_boundary", errors)
    neutral = packet.get("medical_modality_neutral_boundary", {})
    require_true(neutral, NEUTRAL_TRUE_FIELDS, "medical_modality_neutral_boundary", errors)
    require_false(neutral, NEUTRAL_FALSE_FIELDS, "medical_modality_neutral_boundary", errors)
    return errors


def validate_closure_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_motion_pipeline_release_closure_packet_v0_1":
        errors.append("closure packet_id mismatch")
    expected_refs = {
        "chain_index": "chain_indexes/physical_quantum_qi_motion_pipeline_chain_index_v0_1.json",
        "manifest": "manifests/physical_quantum_qi_motion_pipeline_manifest_v0_1.json",
        "release_packet": "packets/physical_quantum_qi_motion_pipeline_release_packet_v0_1.json",
        "finality_packet": "packets/physical_quantum_qi_motion_pipeline_finality_packet_v0_1.json",
    }
    for key, expected in expected_refs.items():
        if packet.get(key) != expected:
            errors.append(f"closure {key} pointer mismatch")
    require_true(packet.get("closure_requirements", {}), packet.get("closure_requirements", {}).keys(), "closure_requirements", errors)
    closed = set(packet.get("closed_invariants", []))
    missing_closed = sorted(LOCKED_INVARIANTS - closed)
    if missing_closed:
        errors.append("closure missing closed invariants: " + ", ".join(missing_closed))
    require_false(packet.get("authority_boundary", {}), AUTHORITY_FALSE_FIELDS, "authority_boundary", errors)
    statement = packet.get("closure_statement", "")
    for phrase in ["no execution", "diagnosis", "treatment", "medical act", "belief commit", "memory overwrite", "world-root rewrite", "safety override"]:
        if phrase not in statement:
            errors.append(f"closure_statement missing phrase: {phrase}")
    return errors


def validate_baseline_packet(packet: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "physical_quantum_qi_motion_pipeline_validated_baseline_packet_v0_1":
        errors.append("baseline packet_id mismatch")
    require_true(packet.get("baseline_commitments", {}), BASELINE_TRUE_COMMITMENTS, "baseline_commitments", errors)
    require_false(packet.get("forbidden_baseline_claims", {}), BASELINE_FALSE_CLAIMS, "forbidden_baseline_claims", errors)
    basis = set(packet.get("validation_basis", []))
    for relpath in [
        "docs/PHYSICAL_QUANTUM_QI_MOTION_PIPELINE_v0_1.md",
        "examples/physical_quantum_qi_motion_pipeline_minimal.py",
        "validation_cases/physical_quantum_qi_motion_pipeline_cases_v0_1.json",
        "scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py",
        "scripts/validate_physical_quantum_qi_motion_pipeline_release_packet_v0_1.py",
    ]:
        if relpath not in basis:
            errors.append(f"baseline validation_basis missing: {relpath}")
    return errors


def validate_chain_index(chain: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if chain.get("chain_index_id") != "physical_quantum_qi_motion_pipeline_chain_index_v0_1":
        errors.append("chain_index_id mismatch")
    if chain.get("update_policy") != "additive_only":
        errors.append("chain update_policy must be additive_only")
    if chain.get("overwrite_policy") != "forbidden":
        errors.append("chain overwrite_policy must be forbidden")
    if chain.get("same_root_required") is not True:
        errors.append("chain same_root_required must be true")
    paths = [entry.get("path") for entry in chain.get("chain_order", [])]
    missing_paths = sorted(REQUIRED_REPO_PATHS - set(paths))
    if missing_paths:
        errors.append("chain_order missing paths: " + ", ".join(missing_paths))
    for relpath in paths:
        if relpath and not (ROOT / relpath).exists():
            errors.append(f"chain_order references missing repository file: {relpath}")
    invariants = chain.get("baseline_invariants", {})
    require_true(
        invariants,
        {
            "validated_type_licenses_dynamics_terms",
            "claimed_type_not_authoritative",
            "unlicensed_terms_ignored",
            "observe_only_motion_candidate",
            "medical_modality_neutral",
            "professional_judgment_required",
            "patient_context_required",
        },
        "baseline_invariants",
        errors,
    )
    require_false(
        invariants,
        {
            "direct_execution_allowed",
            "authority_expansion",
            "standalone_diagnosis_authority",
            "standalone_treatment_authorization",
            "medical_act_authorization",
            "qi_denied_by_boundary",
            "east_asian_medical_reasoning_denied",
            "biomedicine_privileged_by_wording",
        },
        "baseline_invariants",
        errors,
    )
    return errors


def validate_runner() -> List[str]:
    text = RUNNER_PATH.read_text(encoding="utf-8")
    required = [
        "physical-quantum-qi-motion-pipeline",
        "scripts/validate_physical_quantum_qi_motion_pipeline_v0_1.py",
        "physical-quantum-qi-motion-pipeline-release",
        "scripts/validate_physical_quantum_qi_motion_pipeline_release_packet_v0_1.py",
    ]
    return [f"runner missing marker: {marker}" for marker in required if marker not in text]


def main() -> int:
    for path in REQUIRED_FILES:
        if not path.exists():
            return fail(f"missing required file: {path.relative_to(ROOT)}")

    try:
        manifest = load_json(MANIFEST_PATH)
        release = load_json(RELEASE_PATH)
        finality = load_json(FINALITY_PATH)
        closure = load_json(CLOSURE_PATH)
        baseline = load_json(BASELINE_PATH)
        chain = load_json(CHAIN_INDEX_PATH)
    except Exception as exc:
        return fail(f"json load failed: {exc}")

    errors: List[str] = []
    errors.extend(validate_manifest(manifest))
    errors.extend(validate_release_packet(release))
    errors.extend(validate_finality_packet(finality))
    errors.extend(validate_closure_packet(closure))
    errors.extend(validate_baseline_packet(baseline))
    errors.extend(validate_chain_index(chain))
    errors.extend(validate_runner())

    if errors:
        for err in errors:
            print(f"[physical-quantum-qi-motion-pipeline-release] ERROR: {err}", file=sys.stderr)
        return 1

    print("[physical-quantum-qi-motion-pipeline-release] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
