#!/usr/bin/env python3
"""Validate Qi Clinical Red Flag Consultation Governor v0.2L artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "specs" / "qi_clinical_red_flag_handover_governor_contract_v0_2L.json"
PACKET = ROOT / "examples" / "qi_clinical_red_flag_handover_governor_packet_v0_2L.json"
DOC = ROOT / "docs" / "QI_CLINICAL_RED_FLAG_HANDOVER_GOVERNOR_v0_2L.md"
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
    "governor_is_consultation_layer",
    "governor_is_visibility_layer",
    "doctor_to_ai_clinical_consultation_accepted",
    "licensed_physician_consultation_is_default_path",
    "handover_is_not_default",
    "handover_is_boundary_mode_only",
    "source_handoff_packet_required",
    "red_flag_visibility_required",
    "red_flag_suppression_forbidden",
    "red_flags_do_not_automatically_force_handover",
    "red_flags_trigger_consultation_deepening_first",
    "handover_required_only_on_boundary_violation_or_unresolvable_safety_gap",
    "clinician_review_context_presumed_when_requester_is_physician",
    "decisionos_safety_eval_required",
    "consultative_reasoning_allowed",
    "differential_discussion_allowed",
    "evidence_pointer_allowed",
    "safety_question_allowed",
    "patient_specific_action_forbidden",
    "unverified_triage_instruction_forbidden",
    "memoryos_append_only_record_required",
    "pii_minimization_required",
    "abstain_hold_reobserve_are_valid_outputs",
]

REQUIRED_FALSE = [
    "governor_is_triage",
    "governor_is_diagnosis",
    "governor_is_prescription",
    "governor_is_formula_selection",
    "governor_is_execution",
]

REQUIRED_FORBIDDEN = [
    "red_flag_visibility_to_automatic_handover",
    "red_flag_visibility_to_triage_instruction",
    "red_flag_visibility_to_diagnosis",
    "red_flag_visibility_to_prescription",
    "red_flag_visibility_to_formula_selection",
    "red_flag_visibility_to_execution",
    "physician_consultation_to_ai_clinical_authority",
    "consultative_reasoning_to_patient_specific_action",
    "consultation_deepening_to_treatment_recommendation_authority",
    "boundary_handover_required_to_patient_specific_action",
    "decisionos_safety_eval_to_safety_override",
    "governor_mode_to_clinical_authority",
    "severity_mode_to_truth_authority",
    "traditional_pattern_to_red_flag_certainty",
    "summary_to_source_replacement",
    "memory_receipt_to_truth_authority",
]

REQUIRED_INVARIANTS = [
    "same_root_required",
    "append_only_required",
    "additive_only_required",
    "tighten_only_default",
    "overwrite_forbidden",
    "doctor_to_ai_clinical_consultation_accepted",
    "licensed_physician_consultation_is_default_path",
    "handover_is_not_default",
    "handover_is_boundary_mode_only",
    "source_handoff_packet_required",
    "red_flag_visibility_required",
    "red_flag_suppression_forbidden",
    "red_flags_do_not_automatically_force_handover",
    "red_flags_trigger_consultation_deepening_first",
    "handover_required_only_on_boundary_violation_or_unresolvable_safety_gap",
    "decisionos_safety_eval_required",
    "consultative_reasoning_allowed",
    "differential_discussion_allowed",
    "evidence_pointer_allowed",
    "safety_question_allowed",
    "no_triage_authority",
    "no_patient_specific_action",
    "no_prescription",
    "no_diagnosis",
    "no_formula_selection",
    "no_execution",
    "severity_mode_non_authoritative",
    "abstain_is_valid_output",
    "hold_is_valid_output",
    "reobserve_is_valid_output",
    "memoryos_append_only_record_required",
    "pii_minimization_required",
]

REQUIRED_CONSULTATION_MODES = [
    "physician_ai_consultation_default",
    "consultation_deepening",
    "safety_questioning",
    "evidence_pointer_review",
    "differential_reasoning_review",
    "local_protocol_review_recommended",
    "boundary_handover_required",
    "blocked_execution_request",
]

REQUIRED_HANDOVER_TRIGGERS = [
    "requester_not_clinician_and_patient_specific_action_requested",
    "ai_execution_or_order_entry_requested",
    "prescription_authority_requested",
    "triage_authority_requested",
    "formula_selection_authority_requested",
    "missing_minimum_context_for_safe_consultation",
    "unresolvable_safety_gap_after_consultation_deepening",
    "institutional_or_legal_boundary_requires_human_only_review",
]

REQUIRED_DOC_PHRASES = [
    "Qi Clinical Red Flag Consultation Governor v0.2L",
    "doctor-to-AI clinical consultation",
    "Physician consultation is the default path",
    "should not cheaply convert clinical consultation into `handover_required`",
    "handover is not default",
    "boundary mode only",
    "red flags do not automatically force handover",
    "red flags trigger consultation deepening first",
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
        contract.get("contract_id") == "qi_clinical_red_flag_handover_governor_contract_v0_2L",
        "contract_id mismatch",
        errors,
    )
    require(contract.get("version") == "v0.2L", "version must be v0.2L", errors)
    require(contract.get("kind") == "QiClinicalRedFlagHandoverGovernorContract", "kind mismatch", errors)
    require(
        "qi_bensho_decisionos_clinician_handoff_contract_v0_2K" in contract.get("extends", []),
        "must extend v0.2K clinician handoff contract",
        errors,
    )

    definition = contract.get("definition", {})
    for key in REQUIRED_TRUE:
        require(definition.get(key) is True, f"definition.{key} must be true", errors)
    for key in REQUIRED_FALSE:
        require(definition.get(key) is False, f"definition.{key} must be false", errors)

    consultation_modes = set(contract.get("consultation_modes", []))
    for item in REQUIRED_CONSULTATION_MODES:
        require(item in consultation_modes, f"missing consultation mode: {item}", errors)

    handover_triggers = set(contract.get("handover_triggers", []))
    for item in REQUIRED_HANDOVER_TRIGGERS:
        require(item in handover_triggers, f"missing handover trigger: {item}", errors)

    forbidden = set(contract.get("forbidden_collapses", []))
    for item in REQUIRED_FORBIDDEN:
        require(item in forbidden, f"missing forbidden collapse: {item}", errors)

    invariants = set(contract.get("required_invariants", []))
    for item in REQUIRED_INVARIANTS:
        require(item in invariants, f"missing invariant: {item}", errors)

    allowed = set(contract.get("allowed_outputs", []))
    require("physician_ai_consultation_default" in allowed, "physician consultation default output required", errors)
    require("boundary_handover_required" in allowed, "boundary handover output required", errors)
    require("handover_required" not in allowed, "bare handover_required output must not be used", errors)

    surfaces = set(contract.get("allowed_surfaces", []))
    require(
        "PhysicianAIConsultation.consultative_reasoning_only" in surfaces,
        "physician AI consultation surface required",
        errors,
    )

    authority = contract.get("authority_boundary", {})
    for key in AUTHORITY_KEYS:
        require(authority.get(key) is False, f"authority_boundary.{key} must be false", errors)


def validate_packet(packet: dict[str, Any], errors: list[str]) -> None:
    require(
        packet.get("packet_id") == "qi_clinical_red_flag_handover_governor_packet_v0_2L",
        "packet_id mismatch",
        errors,
    )
    require(
        packet.get("contract_id") == "qi_clinical_red_flag_handover_governor_contract_v0_2L",
        "packet contract_id mismatch",
        errors,
    )
    require(packet.get("version") == "v0.2L", "packet version mismatch", errors)
    require(packet.get("surface_type") == "QiClinicalRedFlagConsultationGovernor", "surface_type mismatch", errors)

    ctx = packet.get("consultation_context", {})
    require(ctx.get("doctor_to_ai_clinical_consultation_accepted") is True, "doctor consultation must be accepted", errors)
    require(ctx.get("requester_role") == "licensed_physician", "requester role must be licensed_physician in default example", errors)
    require(ctx.get("physician_consultation_is_default_path") is True, "physician consultation default path required", errors)
    require(ctx.get("handover_is_default") is False, "handover must not be default", errors)
    require(ctx.get("handover_is_boundary_mode_only") is True, "handover must be boundary mode only", errors)
    for key in ["consultative_reasoning_allowed", "differential_discussion_allowed", "evidence_pointer_allowed", "safety_question_allowed"]:
        require(ctx.get(key) is True, f"consultation_context.{key} must be true", errors)

    visibility = packet.get("visibility_status", {})
    require(visibility.get("red_flag_visibility_required") is True, "red flag visibility required", errors)
    require(visibility.get("red_flag_suppression_allowed") is False, "red flag suppression must be false", errors)
    require(visibility.get("red_flag_hidden") is False, "red flag hidden must be false", errors)
    require(visibility.get("consultation_visibility") is True, "consultation visibility required", errors)

    severity = packet.get("severity_mode", {})
    require(severity.get("mode") == "consultation_deepening_required", "severity should deepen consultation first", errors)
    require(severity.get("automatic_handover") is False, "automatic handover must be false", errors)
    for key in ["authoritative", "diagnosis", "prescription", "formula_selection", "execution", "triage_instruction", "patient_specific_action"]:
        require(severity.get(key) is False, f"severity_mode.{key} must be false", errors)

    consultation = packet.get("consultation_decision", {})
    require(consultation.get("mode") == "physician_ai_consultation_default", "consultation decision must be default physician AI consultation", errors)
    require(consultation.get("red_flags_do_not_automatically_force_handover") is True, "red flags must not auto-handover", errors)
    require(consultation.get("red_flags_trigger_consultation_deepening_first") is True, "red flags must deepen consultation first", errors)
    require(consultation.get("consultation_deepening_required") is True, "consultation deepening required", errors)
    require(consultation.get("clinical_authority_granted") is False, "consultation must not grant clinical authority", errors)
    require(consultation.get("patient_specific_action_allowed") is False, "consultation must not allow patient-specific action", errors)

    handover = packet.get("boundary_handover_policy", {})
    require(handover.get("boundary_handover_required") is False, "default packet must not require boundary handover", errors)
    require(
        handover.get("handover_required_only_on_boundary_violation_or_unresolvable_safety_gap") is True,
        "handover must only occur on boundary violation or unresolvable safety gap",
        errors,
    )
    triggers = set(handover.get("allowed_triggers", []))
    for item in REQUIRED_HANDOVER_TRIGGERS:
        require(item in triggers, f"packet missing handover trigger: {item}", errors)
    require(handover.get("triggered") == [], "default physician consultation example must have no handover triggers", errors)

    decisionos = packet.get("decisionos_safety_eval_request", {})
    require(decisionos.get("required") is True, "DecisionOS safety eval request required", errors)
    require(decisionos.get("safety_override_allowed") is False, "DecisionOS safety override must be false", errors)
    require(decisionos.get("execution_release_allowed") is False, "DecisionOS execution release must be false", errors)
    require(decisionos.get("triage_authority_allowed") is False, "DecisionOS triage authority must be false", errors)
    require(decisionos.get("patient_specific_action_allowed") is False, "DecisionOS patient-specific action must be false", errors)

    red_flag = packet.get("red_flag_report", {})
    require(red_flag.get("required") is True, "red flag report required", errors)
    require(red_flag.get("flag_certainty_claimed") is False, "red flag certainty must not be claimed", errors)
    require(red_flag.get("traditional_pattern_certainty_claimed") is False, "traditional pattern certainty must not be claimed", errors)
    require(red_flag.get("direct_instruction_allowed") is False, "direct instruction must be false", errors)
    require(red_flag.get("consultation_deepening_first") is True, "consultation deepening first required", errors)

    barrier = packet.get("barrier_report", {})
    require(barrier.get("required") is True, "barrier report required", errors)
    require(barrier.get("barriers_hidden") is False, "barriers must not be hidden", errors)
    require(barrier.get("governor_blocks_execution") is True, "governor must block execution", errors)
    require(barrier.get("governor_blocks_consultation") is False, "governor must not block consultation", errors)

    allowed = packet.get("allowed_output", {})
    require(allowed.get("mode") == "physician_ai_consultation_default", "allowed output must keep consultation default", errors)
    for key in [
        "consultation_deepening_allowed",
        "safety_questioning_allowed",
        "evidence_pointer_review_allowed",
        "differential_reasoning_review_allowed",
        "local_protocol_review_recommended",
        "abstain_allowed",
        "hold_allowed",
        "reobserve_allowed",
    ]:
        require(allowed.get(key) is True, f"allowed_output.{key} must be true", errors)
    require(allowed.get("boundary_handover_required") is False, "boundary handover must be false in default example", errors)
    require(allowed.get("execution_allowed") is False, "execution must be false", errors)

    require(isinstance(packet.get("reobservation_plan"), list) and bool(packet["reobservation_plan"]), "reobservation_plan required", errors)
    require("deepen_physician_ai_consultation" in packet.get("reobservation_plan", []), "reobservation must deepen physician AI consultation", errors)

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

    surfaces = set(packet.get("allowed_next_surfaces", []))
    require(
        "PhysicianAIConsultation.consultative_reasoning_only" in surfaces,
        "packet must allow physician AI consultation surface",
        errors,
    )

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
    phrase = "scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py"
    require(phrase in text, f"full governance runner missing phrase: {phrase}", errors)


def main() -> int:
    errors: list[str] = []
    validate_contract(load_json(CONTRACT), errors)
    validate_packet(load_json(PACKET), errors)
    validate_doc(errors)
    validate_runner(errors)

    if errors:
        print("Qi Clinical Red Flag Consultation Governor v0.2L validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Clinical Red Flag Consultation Governor v0.2L validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
