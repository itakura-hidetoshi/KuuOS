#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "specs" / "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json"

REQUIRED_TOP_LEVEL = [
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
]

REQUIRED_FILES = [
    "docs/QI_BENSHO_TREATMENT_ROUTE_CANDIDATE_v0_2J.md",
    "docs/QI_BENSHO_DECISIONOS_CLINICIAN_HANDOFF_v0_2K.md",
    "docs/QI_CLINICAL_RED_FLAG_HANDOVER_GOVERNOR_v0_2L.md",
    "docs/QI_CLINICAL_RED_FLAG_CONSULTATION_GOVERNOR_FINALITY_PACKET_v0_2L.md",
    "docs/PHYSICAL_QUANTUM_QI_OBSERVATION_KERNEL_v0_2M.md",
    "docs/PHYSICAL_QUANTUM_QI_STATE_TRANSITION_KERNEL_v0_2N.md",
    "docs/PHYSICAL_QUANTUM_QI_TRANSITION_TRAJECTORY_LEDGER_v0_2O.md",
    "docs/PHYSICAL_QUANTUM_QI_TRAJECTORY_PHASE_TRANSITION_DETECTOR_v0_2P.md",
    "docs/PHYSICAL_QUANTUM_QI_PHASE_TRANSITION_RESPONSE_GOVERNOR_v0_2Q.md",
    "docs/PHYSICAL_QUANTUM_QI_RESPONSE_FEEDBACK_LOOP_v0_2R.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md",
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py",
    "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "Makefile",
    ".github/workflows/physical_quantum_qi_runtime_evolution_validation.yml",
]

REQUIRED_FALSE_BOUNDARIES = [
    "clinical_authority_granted",
    "diagnosis_authority_granted",
    "prescription_authority_granted",
    "formula_selection_authority_granted",
    "treatment_recommendation_authority_granted",
    "triage_authority_granted",
    "patient_specific_action_authority_granted",
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "memory_overwrite_authority_granted",
    "governance_bypass_authority_granted",
]

REQUIRED_TRUE_BOUNDARIES = [
    "validation_only",
    "candidate_only_where_applicable",
    "append_only",
    "same_root_required",
    "non_authoritative",
]

REQUIRED_INVARIANTS = [
    "runtime evolution checks are validation-only",
    "CI green is integration evidence, not theorem truth",
    "CI green is integration evidence, not clinical authority",
    "observation and state-transition kernels remain non-authoritative readout surfaces",
    "transition ledgers remain append-only trace surfaces",
    "phase transition detection remains signal classification, not direct action",
    "response governance remains bounded by consultation and non-sovereignty",
    "response feedback remains non-overwriting and non-escalatory",
    "bundle manifest records traceability and does not create execution authority",
]


def load_manifest() -> tuple[dict, list[str]]:
    if not MANIFEST.is_file():
        return {}, [f"missing manifest: {MANIFEST.relative_to(ROOT)}"]
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return {}, [f"invalid JSON in {MANIFEST.relative_to(ROOT)}: {exc}"]


def main() -> int:
    manifest, errors = load_manifest()
    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    for key in REQUIRED_TOP_LEVEL:
        if key not in manifest:
            errors.append(f"manifest missing top-level key: {key}")

    if manifest.get("manifest_id") != "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR":
        errors.append("unexpected manifest_id")
    if manifest.get("version") != "v0.2J-R":
        errors.append("unexpected version")
    if manifest.get("status") != "BUNDLE_MANIFEST_RECORDED":
        errors.append("unexpected status")
    if manifest.get("repository") != "itakura-hidetoshi/KuuOS":
        errors.append("unexpected repository")

    lineage = manifest.get("lineage", {})
    span = lineage.get("runtime_evolution_span", [])
    for expected in ["v0.2J", "v0.2K", "v0.2L", "v0.2M", "v0.2N", "v0.2O", "v0.2P", "v0.2Q", "v0.2R"]:
        if expected not in span:
            errors.append(f"lineage missing runtime span: {expected}")
    if lineage.get("ci_receipt_surface") != "v0.2J-R":
        errors.append("lineage ci_receipt_surface must be v0.2J-R")

    boundary = manifest.get("authority_boundary", {})
    for key in REQUIRED_TRUE_BOUNDARIES:
        if boundary.get(key) is not True:
            errors.append(f"authority_boundary.{key} must be true")
    for key in REQUIRED_FALSE_BOUNDARIES:
        if boundary.get(key) is not False:
            errors.append(f"authority_boundary.{key} must be false")

    files = manifest.get("files", [])
    if not isinstance(files, list):
        errors.append("files must be a list")
        files = []
    for path in REQUIRED_FILES:
        if path not in files:
            errors.append(f"manifest files missing required path: {path}")
    for path in files:
        candidate = ROOT / path
        if not candidate.is_file():
            errors.append(f"manifest path does not exist: {path}")

    validators = manifest.get("validators", [])
    for validator in [
        "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py",
        "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py",
        "scripts/run_all_governance_full_checks_v0_1.py",
    ]:
        if validator not in validators:
            errors.append(f"validators missing: {validator}")

    ci_targets = manifest.get("ci_targets", [])
    for target in [
        "make physical-quantum-qi-runtime-evolution-checks",
        "make physical-quantum-qi-runtime-evolution-bundle-checks",
        "python3 scripts/run_all_governance_full_checks_v0_1.py",
    ]:
        if target not in ci_targets:
            errors.append(f"ci_targets missing: {target}")

    invariants = manifest.get("invariants", [])
    for invariant in REQUIRED_INVARIANTS:
        if invariant not in invariants:
            errors.append(f"invariants missing: {invariant}")

    forbidden_tokens = manifest.get("forbidden_authority_tokens", [])
    if not isinstance(forbidden_tokens, list):
        errors.append("forbidden_authority_tokens must be a list")
        forbidden_tokens = []
    for token in forbidden_tokens:
        if not isinstance(token, str):
            errors.append("forbidden_authority_tokens must contain strings only")
            continue
        if token.endswith(": true"):
            boundary_key = token.removesuffix(": true")
            if boundary.get(boundary_key) is True:
                errors.append(f"forbidden authority boundary is true: {boundary_key}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Physical Quantum Qi runtime evolution bundle manifest v0.2J-R validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
