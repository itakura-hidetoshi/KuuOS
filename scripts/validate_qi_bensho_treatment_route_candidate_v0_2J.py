#!/usr/bin/env python3
"""Validate Qi Bensho Treatment Route Candidate v0.2J artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CONTRACT = ROOT / "specs" / "qi_bensho_treatment_route_candidate_contract_v0_2J.json"
PACKET = ROOT / "examples" / "qi_bensho_treatment_route_candidate_packet_v0_2J.json"
DOC = ROOT / "docs" / "QI_BENSHO_TREATMENT_ROUTE_CANDIDATE_v0_2J.md"

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
    "proof_authority",
    "truth_authority",
    "ontology_authority",
    "safety_override_authority",
    "teni_authority",
]

REQUIRED_TRUE = [
    "treatment_route_is_candidate",
    "source_qi_field_bundle_required",
    "source_bensho_readout_required",
    "recoverability_gate_required",
    "contradiction_gate_required",
    "barrier_conditions_required",
    "stop_conditions_required",
    "reobservation_plan_required",
    "route_family_non_authoritative",
    "route_requires_decisionos_safety_eval",
    "route_requires_memoryos_append_only_record",
]

REQUIRED_FALSE = [
    "treatment_route_is_execution",
    "treatment_route_is_prescription",
    "treatment_route_is_diagnosis",
    "treatment_route_is_formula_selection",
]

REQUIRED_FORBIDDEN = [
    "pattern_to_treatment_execution",
    "pattern_to_prescription",
    "route_to_formula_selection",
    "route_to_clinical_instruction",
    "route_to_truth_authority",
    "route_to_safety_override",
    "local_symptom_to_route_certainty",
    "recoverability_to_execution_permission",
    "smooth_route_to_commit_authority",
    "traditional_label_to_action_authority",
]

REQUIRED_INVARIANTS = [
    "same_root_required",
    "append_only_required",
    "additive_only_required",
    "tighten_only_default",
    "overwrite_forbidden",
    "source_qi_field_bundle_required",
    "source_bensho_readout_required",
    "route_family_non_authoritative",
    "recoverability_precedes_route_candidate",
    "contradiction_visibility_required",
    "barrier_conditions_required",
    "stop_conditions_required",
    "reobservation_is_valid_output",
    "abstention_is_valid_output",
    "decisionos_safety_eval_required",
    "clinical_authority_false",
    "prescription_authority_false",
]

REQUIRED_DOC_PHRASES = [
    "Qi Bensho Treatment Route Candidate v0.2J",
    "non-executing route layer",
    "bounded transport hypothesis",
    "does not diagnose",
    "does not prescribe",
    "does not execute",
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
        contract.get("contract_id") == "qi_bensho_treatment_route_candidate_contract_v0_2J",
        "contract_id mismatch",
        errors,
    )
    require(contract.get("version") == "v0.2J", "version must be v0.2J", errors)
    require(contract.get("kind") == "QiBenshoTreatmentRouteCandidateContract", "kind mismatch", errors)

    definition = contract.get("definition", {})
    for key in REQUIRED_TRUE:
        require(definition.get(key) is True, f"definition.{key} must be true", errors)
    for key in REQUIRED_FALSE:
        require(definition.get(key) is False, f"definition.{key} must be false", errors)

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
        packet.get("packet_id") == "qi_bensho_treatment_route_candidate_packet_v0_2J",
        "packet_id mismatch",
        errors,
    )
    require(
        packet.get("contract_id") == "qi_bensho_treatment_route_candidate_contract_v0_2J",
        "packet contract_id mismatch",
        errors,
    )
    require(packet.get("version") == "v0.2J", "packet version mismatch", errors)
    require(packet.get("surface_type") == "QiTreatmentRouteCandidate", "surface_type mismatch", errors)

    require(bool(packet.get("source_qi_field_bundle_ref")), "source_qi_field_bundle_ref required", errors)
    require(bool(packet.get("source_bensho_readout_ref")), "source_bensho_readout_ref required", errors)

    route_family = packet.get("route_family", {})
    require(route_family.get("authoritative") is False, "route_family must be non-authoritative", errors)
    require(route_family.get("prescription") is False, "route_family must not be prescription", errors)
    require(route_family.get("formula_selection") is False, "route_family must not select formula", errors)
    require(route_family.get("execution") is False, "route_family must not execute", errors)

    deformation = packet.get("intended_field_deformation", {})
    require(deformation.get("direct_action") is False, "field deformation must not be direct action", errors)
    require(deformation.get("requires_safety_eval") is True, "field deformation must require safety eval", errors)

    yin_yang = packet.get("yin_yang_balance_effect", {})
    require(yin_yang.get("symmetry_forcing_allowed") is False, "symmetry forcing must be false", errors)
    require(yin_yang.get("corridor_required") is True, "yin-yang corridor required", errors)

    leak = packet.get("leak_effect", {})
    require(leak.get("leak_must_remain_visible") is True, "leak must remain visible", errors)
    require(leak.get("leak_treated_as_noise") is False, "leak must not be treated as noise", errors)

    holonomy = packet.get("holonomy_effect", {})
    require(holonomy.get("holonomy_residue_must_remain_visible") is True, "holonomy residue must remain visible", errors)
    require(holonomy.get("local_global_gap_must_not_be_suppressed") is True, "local-global gap must not be suppressed", errors)

    memory_tail = packet.get("memory_tail_effect", {})
    require(memory_tail.get("non_markov_tail_preserved") is True, "non-Markov tail must be preserved", errors)
    require(memory_tail.get("summary_replacement_allowed") is False, "summary replacement must be false", errors)

    recoverability = packet.get("recoverability_gate", {})
    require(recoverability.get("required") is True, "recoverability gate required", errors)
    require(recoverability.get("execution_allowed") is False, "recoverability gate must not allow execution", errors)

    contradiction = packet.get("contradiction_gate", {})
    require(contradiction.get("required") is True, "contradiction gate required", errors)
    require(contradiction.get("direct_route_blocked") is True, "direct route must be blocked when contradiction remains", errors)

    require(isinstance(packet.get("barrier_conditions"), list) and bool(packet["barrier_conditions"]), "barrier_conditions required", errors)
    require(isinstance(packet.get("stop_conditions"), list) and bool(packet["stop_conditions"]), "stop_conditions required", errors)
    require(isinstance(packet.get("reobservation_plan"), list) and bool(packet["reobservation_plan"]), "reobservation_plan required", errors)

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


def main() -> int:
    errors: list[str] = []
    validate_contract(load_json(CONTRACT), errors)
    validate_packet(load_json(PACKET), errors)
    validate_doc(errors)

    if errors:
        print("Qi Bensho Treatment Route Candidate v0.2J validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Qi Bensho Treatment Route Candidate v0.2J validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
