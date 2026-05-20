#!/usr/bin/env python3
"""Validate the public Physical Quantum Qi runtime contract v0.1."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "specs" / "physical_quantum_qi_runtime_contract_v0_1.json"
EXAMPLE_PATH = ROOT / "examples" / "physical_quantum_qi_runtime_packet_v0_1.json"
CASES_PATH = ROOT / "validation_cases" / "physical_quantum_qi_runtime_validation_cases_v0_1.json"
DOC_PATH = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_CONTRACT_v0_1.md"

CLASSIFIER_BOUNDARY = {
    "observe_only": True,
    "direct_execution_allowed": False,
    "authority_expansion": False,
    "standalone_diagnosis_authority": False,
    "standalone_treatment_authorization": False,
    "medical_act_authorization": False,
    "medical_modality_neutral": True,
    "qi_denied_by_boundary": False,
    "east_asian_medical_reasoning_denied": False,
    "biomedicine_privileged_by_wording": False,
    "professional_judgment_required": True,
    "patient_context_required": True,
}

SPEC_OUTPUT_BOUNDARY = {
    "observe_only": True,
    "direct_execution_allowed": False,
    "authority_expansion": False,
    "standalone_diagnosis_authority": False,
    "standalone_treatment_authorization": False,
    "medical_act_authorization": False,
}

SPEC_NEUTRAL_BOUNDARY = {
    "medical_modality_neutral": True,
    "qi_denied_by_boundary": False,
    "east_asian_medical_reasoning_denied": False,
    "biomedicine_privileged_by_wording": False,
    "professional_judgment_required": True,
    "patient_context_required": True,
}

DOC_MARKERS = [
    "Classification output boundary",
    "observe_only = true",
    "direct_execution_allowed = false",
    "authority_expansion = false",
    "standalone_diagnosis_authority = false",
    "standalone_treatment_authorization = false",
    "medical_act_authorization = false",
    "medical_modality_neutral = true",
    "qi_denied_by_boundary = false",
    "east_asian_medical_reasoning_denied = false",
    "biomedicine_privileged_by_wording = false",
]


@dataclass(frozen=True)
class QiRuntimeClassificationDecision:
    validated_type: str
    classification_reason: str
    observe_only: bool = True
    direct_execution_allowed: bool = False
    authority_expansion: bool = False
    standalone_diagnosis_authority: bool = False
    standalone_treatment_authorization: bool = False
    medical_act_authorization: bool = False
    medical_modality_neutral: bool = True
    qi_denied_by_boundary: bool = False
    east_asian_medical_reasoning_denied: bool = False
    biomedicine_privileged_by_wording: bool = False
    professional_judgment_required: bool = True
    patient_context_required: bool = True


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def evidence_pass(packet: Dict[str, Any], key: str) -> bool:
    return packet.get("evidence_status", {}).get(key) == "pass"


def all_evidence(packet: Dict[str, Any], keys: List[str]) -> bool:
    return all(evidence_pass(packet, key) for key in keys)


def authority_clear(packet: Dict[str, Any], authority_keys: List[str]) -> bool:
    authority = packet.get("authority", {})
    return all(authority.get(key) is False for key in authority_keys)


def has_fatal_error(packet: Dict[str, Any], fatal_flags: List[str]) -> bool:
    return bool(set(packet.get("fatal_flags", [])).intersection(fatal_flags)) or packet.get("mass_gap_floor", {}).get("not_source_of_qi") is False


def classify_decision(packet: Dict[str, Any], spec: Dict[str, Any]) -> QiRuntimeClassificationDecision:
    physical_keys = spec["physical_qi_required_evidence"]
    full_path_keys = spec["full_path_qi_additional_evidence"]
    fatal_flags = spec["fatal_reject_flags"]
    authority_keys = spec["authority_must_be_false"]

    if has_fatal_error(packet, fatal_flags):
        return QiRuntimeClassificationDecision("Reject", "fatal Qi runtime error")
    if not authority_clear(packet, authority_keys):
        return QiRuntimeClassificationDecision("Reject", "Qi packet attempted to grant forbidden authority")
    if not evidence_pass(packet, "delta_rel_in_K_perp"):
        if evidence_pass(packet, "K_non_reification"):
            return QiRuntimeClassificationDecision("NonQi", "K non-reification present but no K_perp dependent-origination difference")
        return QiRuntimeClassificationDecision("Reject", "no dependent-origination difference in K_perp")
    if not evidence_pass(packet, "string_mode_consistency") or not evidence_pass(packet, "brane_boundary_support"):
        return QiRuntimeClassificationDecision("PreQi", "missing string/brane organization")
    if not evidence_pass(packet, "gauge_connection_A_mu"):
        return QiRuntimeClassificationDecision("ProtoQi", "missing gauge connection")
    if not evidence_pass(packet, "curvature_F_munu") or not evidence_pass(packet, "Wilson_loop_residue"):
        return QiRuntimeClassificationDecision("TransportableQi", "missing curvature or holonomy residue")
    if not evidence_pass(packet, "current_J_Qi_mu"):
        return QiRuntimeClassificationDecision("CurvedQi", "missing Qi current coupling")
    if not evidence_pass(packet, "Ward_or_leak_identity"):
        return QiRuntimeClassificationDecision("CurrentQi", "missing Ward/leak identity")
    if not all_evidence(packet, physical_keys):
        return QiRuntimeClassificationDecision("CurrentQi", "missing PhysicalQi evidence bundle")
    if all_evidence(packet, full_path_keys):
        return QiRuntimeClassificationDecision("FullPathQi", "PhysicalQi evidence plus SK/FV history evidence present")
    return QiRuntimeClassificationDecision("PhysicalQi", "PhysicalQi evidence present; SK/FV history incomplete")


def classify(packet: Dict[str, Any], spec: Dict[str, Any]) -> Tuple[str, str]:
    decision = classify_decision(packet, spec)
    return decision.validated_type, decision.classification_reason


def expect_fields(label: str, data: Mapping[str, Any], expected: Mapping[str, Any]) -> List[str]:
    return [f"{label}.{k} must be {v!r}" for k, v in expected.items() if data.get(k) != v]


def validate_spec(spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if spec.get("schema_id") != "physical_quantum_qi_runtime_contract_v0_1":
        errors.append("schema_id must be physical_quantum_qi_runtime_contract_v0_1")
    if spec.get("update_policy") != "additive_only":
        errors.append("update_policy must be additive_only")
    if spec.get("overwrite_policy") != "forbidden":
        errors.append("overwrite_policy must be forbidden")
    if spec.get("mass_gap_floor", {}).get("not_source_of_qi") is not True:
        errors.append("mass_gap_floor.not_source_of_qi must be true")
    for required in ["physical_qi_required_evidence", "full_path_qi_additional_evidence", "authority_must_be_false"]:
        if not spec.get(required):
            errors.append(f"missing nonempty {required}")
    errors.extend(expect_fields("classification_output_boundary", spec.get("classification_output_boundary", {}), SPEC_OUTPUT_BOUNDARY))
    errors.extend(expect_fields("medical_modality_neutral_boundary", spec.get("medical_modality_neutral_boundary", {}), SPEC_NEUTRAL_BOUNDARY))
    return errors


def validate_docs() -> List[str]:
    if not DOC_PATH.exists():
        return ["runtime contract doc missing"]
    text = DOC_PATH.read_text(encoding="utf-8")
    return [f"runtime contract doc missing marker: {m}" for m in DOC_MARKERS if m not in text]


def validate_example(example: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    decision = classify_decision(example, spec)
    if decision.validated_type != "FullPathQi":
        errors.append(f"example should validate as FullPathQi, got {decision.validated_type}: {decision.classification_reason}")
    if example.get("validated_type") not in (None, decision.validated_type):
        errors.append("example validated_type must be null or match computed type")
    errors.extend(expect_fields("example decision", asdict(decision), CLASSIFIER_BOUNDARY))
    errors.extend(expect_fields("example expected_classification_boundary", example.get("expected_classification_boundary", {}), CLASSIFIER_BOUNDARY))
    return errors


def validate_cases(cases_doc: Dict[str, Any], spec: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend(expect_fields("runtime_boundary_expectations", cases_doc.get("runtime_boundary_expectations", {}), CLASSIFIER_BOUNDARY))
    for case in cases_doc.get("cases", []):
        name = case.get("name", "<unnamed>")
        packet = case.get("packet", {})
        expected = case.get("expected_validated_type")
        decision = classify_decision(packet, spec)
        if decision.validated_type != expected:
            errors.append(f"case {name}: expected {expected}, got {decision.validated_type}: {decision.classification_reason}")
        errors.extend(expect_fields(f"case {name}", asdict(decision), CLASSIFIER_BOUNDARY))
    return errors


def main() -> int:
    spec = load_json(SPEC_PATH)
    example = load_json(EXAMPLE_PATH)
    cases = load_json(CASES_PATH)

    errors: List[str] = []
    errors.extend(validate_spec(spec))
    errors.extend(validate_docs())
    errors.extend(validate_example(example, spec))
    errors.extend(validate_cases(cases, spec))

    if errors:
        print("Physical Quantum Qi runtime validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Physical Quantum Qi runtime validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())