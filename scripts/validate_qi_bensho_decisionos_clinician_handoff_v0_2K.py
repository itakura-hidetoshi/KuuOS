#!/usr/bin/env python3
"""Validate Qi Bensho DecisionOS Clinician Handoff v0.2K artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "specs" / "qi_bensho_decisionos_clinician_handoff_contract_v0_2K.json"
PACKET = ROOT / "examples" / "qi_bensho_decisionos_clinician_handoff_packet_v0_2K.json"
DOC = ROOT / "docs" / "QI_BENSHO_DECISIONOS_CLINICIAN_HANDOFF_v0_2K.md"
RUNNER = ROOT / "scripts" / "run_all_governance_full_checks_v0_1.py"

AUTHORITY_KEYS = [
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "clinical_authority",
    "diagnosis_authority",
    "prescription_authority",
    "formula_selection_authority",
    "treatment_recommendation_authority",
    "triage_authority",
    "patient_specific_action_authority",
    "proof_authority",
    "truth_authority",
    "ontology_authority",
    "safety_override_authority",
    "teni_authority",
]

REQUIRED_TRUE = [
    "handoff_is_candidate",
    "source_treatment_route_candidate_required",
    "source_qi_field_bundle_required",
    "source_bensho_readout_required",
    "decisionos_safety_eval_required",
    "clinician_review_required_for_clinical_use",
    "evidence_trace_required",
    "contradiction_report_required",
    "barrier_report_required",
    "stop_conditions_required",
    "red_flag_escalation_surface_required",
    "reobservation_plan_required",
    "memoryos_append_only_record_required",
    "patient_specific_action_forbidden",
    "pii_minimization_required",
]

REQUIRED_FALSE = [
    "handoff_is_execution",
    "handoff_is_prescription",
    "handoff_is_diagnosis",
    "handoff_is_formula_selection",
    "handoff_is_clinical_instruction",
]

REQUIRED_SECTIONS = [
    "source_refs",
    "route_candidate_summary",
    "non_authority_boundary",
    "contradiction_report",
    "barrier_report",
    "red_flag_escalation_surface",
    "reobservation_plan",
    "decisionos_safety_eval_request",
    "clinician_review_notice",
    "memoryos_append_only_receipt",
]

REQUIRED_FORBIDDEN = [
    "handoff_to_prescription",
    "handoff_to_diagnosis",
    "handoff_to_formula_selection",
    "handoff_to_clinical_instruction",
    "handoff_to_execution",
    "route_candidate_to_patient_specific_action",
    "decisionos_eval_to_safety_override",
    "clinician_handoff_to_clinical_authority",
    "red_flag_to_unverified_triage_instruction",
    "summary_to_source_replacement",
    "memory_receipt_to_truth_authority",
    "traditional_label_to_action_authority",
]

REQUIRED_INVARIANTS = [
    "same_root_required",
    "append_only_required",
    "additive_only_required",
    "tighten_only_default",
    "overwrite_forbidden",
    "source_treatment_route_candidate_required",
    "source_qi_field_bundle_required",
    "source_bensho_readout_required",
    "decisionos_safety_eval_required",
    "clinician_review_required_for_clinical_use",
    "non_authoritative_handoff_only",
    "no_patient_specific_action",
    "no_prescription",
    "no_diagnosis",
    "no_formula_selection",
    "no_execution",
    "contradiction_visibility_required",
    "barrier_visibility_required",
    "red_flag_visibility_required",
    "reobservation_is_valid_output",
    "abstention_is_valid_output",
    "memoryos_append_only_record_required",
    "pii_minimization_required",
]

REQUIRED_DOC_PHRASES = [
    "Qi Bensho DecisionOS Clinician Handoff v0.2K",
    "non-executing handoff layer",
    "DecisionOS safety-evaluation request",
    "clinician-review handoff packet",
    "does not diagnose",
    "does not prescribe",
    "does not select a formula",
    "does not execute",
    "does not replace clinician judgment",
    "Forbidden collapses",
]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_contract(contract: dict[str, Any], errors: list[str]) -> None:
    require(
        contract.get("contract_id") == "qi_bensho_decisionos_clinician_handoff_contract_v0_2K",
        "contract_id mismatch",
        errors,
    )
    require(contract.get("version") == "v0.2K", "version must be v0.2K", errors)
    require(contract.get("kind") == "QiBenshoDecisionOSClinicianHandoffContract", "kind mismatch", errors)
    require("qi_bensho_treatment_route_candidate_contract_v0_2J" in contract.get("extends", []), "must extend v0.2J route candidate", errors)

    definition = contract.get("definition", {})
    for key in REQUIRED_TRUE:
        require(definition.get(key) is True, f"definition.{key} must be true", errors)
    for key in REQUIRED_FALSE:
        require(definition.get(key) is False, f"definition.{key} must be false", errors)

    sections = set(contract.get("handoff_sections_required", []))
    for item in REQUIRED_SECTIONS:
        require(item in sections, f"missing handoff section: {item}", errors)

    forbidden = set(contract.get("forbidden_collapses", []))
    for item in REQUIRED_FORBIDDEN:
        require(item in forbidden, f"missing forbidden collapse: {item}", errors)

    invariants = set(contract.get("required_invariants", []))
    for item in REQUIRED_INVARIANTS:
        require(item in invariants, f"missing invariant: {item}", errors)

    authority = contract.get("authority_boundary", {})
    for key in AUTHORITY_KEYS:
        require(authority.get(key) is False, f"authority_boundary.{key} must be false", errors)


def validate_packet(packet: dict[str, Any], errors: list[str]) -> None:
    require(
        packet.get("packet_id") == "qi_bensho_decisionos_clinician_handoff_packet_v0_2K",
        "packet_id mismatch",
        errors,
    )
    require(
        packet.get("contract_id") == "qi_bensho_decisionos_clinician_handoff_contract_v0_2K",
        "packet contract_id mismatch",
        errors,
    )
    require(packet.get("version") == "v0.2K", "packet version mismatch", errors)
    require(packet.get("surface_type") == "QiBenshoDecisionOSClinicianHandoff", "surface_type mismatch", errors)

    require(bool(packet.get("source_treatment_route_candidate_ref")), "source_treatment_route_candidate_ref required", errors)
    require(bool(packet.get("source_qi_field_bundle_ref")), "source_qi_field_bundle_ref required", errors)
    require(bool(packet.get("source_bensho_readout_ref")), "source_bensho_readout_ref required", errors)

    route = packet.get("route_candidate_summary", {})
    require(route.get("non_authoritative") is True, "route summary must be non-authoritative", errors)
    require(route.get("prescription") is False, "route summary must not be prescription", errors)
    require(route.get("diagnosis") is False, "route summary must not be diagnosis", errors)
    require(route.get("formula_selection") is False, "route summary must not select formula", errors)
    require(route.get("execution") is False, "route summary must not execute", errors)
    require(route.get("patient_specific_action") is False, "route summary must not be patient-specific action", errors)

    boundary = packet.get("non_authority_boundary", {})
    for key in ["does_not_diagnose", "does_not_prescribe", "does_not_select_formula", "does_not_execute", "does_not_replace_clinician_judgment", "candidate_only"]:
        require(boundary.get(key) is True, f"non_authority_boundary.{key} must be true", errors)

    decisionos = packet.get("decisionos_safety_eval_request", {})
    require(decisionos.get("required") is True, "DecisionOS safety eval request required", errors)
    require(decisionos.get("safety_override_allowed") is False, "DecisionOS safety override must be false", errors)
    require(decisionos.get("execution_release_allowed") is False, "DecisionOS execution release must be false", errors)
    require(decisionos.get("patient_specific_action_allowed") is False, "DecisionOS patient-specific action must be false", errors)

    clinician = packet.get("clinician_review_notice", {})
    require(clinician.get("required_for_clinical_use") is True, "clinician review required for clinical use", errors)
    require(clinician.get("clinical_authority_granted") is False, "handoff must not grant clinical authority", errors)
    require(clinician.get("handoff_is_advisory_context_only") is True, "handoff must be advisory context only", errors)

    contradiction = packet.get("contradiction_report", {})
    require(contradiction.get("required") is True, "contradiction report required", errors)
    require(contradiction.get("contradiction_hidden") is False, "contradiction must not be hidden", errors)
    require(contradiction.get("direct_route_blocked_if_unresolved") is True, "unresolved contradiction must block direct route", errors)

    barrier = packet.get("barrier_report", {})
    require(barrier.get("required") is True, "barrier report required", errors)
    require(barrier.get("barriers_hidden") is False, "barriers must not be hidden", errors)
    require(barrier.get("handoff_blocks_execution") is True, "handoff must block execution", errors)

    red_flag = packet.get("red_flag_escalation_surface", {})
    require(red_flag.get("required") is True, "red flag surface required", errors)
    require(red_flag.get("red_flag_visibility_required") is True, "red flag visibility required", errors)
    require(red_flag.get("triage_authority") is False, "red flag surface must not grant triage authority", errors)
    require(red_flag.get("unverified_triage_instruction_allowed") is False, "unverified triage instruction must be false", errors)

    require(isinstance(packet.get("reobservation_plan"), list) and bool(packet["reobservation_plan"]), "reobservation_plan required", errors)

    memory = packet.get("memoryos_append_only_receipt", {})
    require(memory.get("required") is True, "MemoryOS receipt required", errors)
    require(memory.get("append_only") is True, "MemoryOS receipt must be append-only", errors)
    require(memory.get("overwrite_allowed") is False, "MemoryOS overwrite must be false", errors)
    require(memory.get("summary_replaces_source") is False, "summary must not replace source", errors)

    pii = packet.get("pii_minimization", {})
    require(pii.get("required") is True, "PII minimization required", errors)
    require(pii.get("patient_identifiers_required") is False, "patient identifiers must not be required", errors)
    require(pii.get("direct_identifier_storage_allowed") is False, "direct identifier storage must be false", errors)
    require(pii.get("minimum_necessary_context_only") is True, "minimum necessary context required", errors)

    authority = packet.get("authority_boundary", {})
    for key in AUTHORITY_KEYS:
        require(authority.get(key) is False, f"packet authority_boundary.{key} must be false", errors)


def validate_doc(errors: list[str]) -> None:
    if not DOC.exists():
        errors.append(f"missing doc: {DOC}")
        return
    text = DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES:
        require(phrase in text, f"doc missing phrase: {phrase}", errors)


def validate_runner(errors: list[str]) -> None:
    text = RUNNER.read_text(encoding="utf-8") if RUNNER.exists() else ""
    phrase = "scripts/validate_qi_bensho_decisionos_clinician_handoff_v0_2K.py"
    require(phrase in text, f"full governance runner missing phrase: {phrase}", errors)


def main() -> int:
    errors: list[str] = []
    validate_contract(load_json(CONTRACT), errors)
    validate_packet(load_json(PACKET), errors)
    validate_doc(errors)
    validate_runner(errors)

    if errors:
        print("Qi Bensho DecisionOS Clinician Handoff v0.2K validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Bensho DecisionOS Clinician Handoff v0.2K validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
