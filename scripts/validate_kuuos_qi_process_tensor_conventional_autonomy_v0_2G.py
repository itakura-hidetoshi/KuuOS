#!/usr/bin/env python3
"""Validate KuuOS Qi Process Tensor Conventional Autonomy packet v0.2G.

This validator fixes Qi Process Tensor as the conventional-truth temporal
substrate for safe autonomous AI. It rejects ultimate-truth reification,
state-snapshot replacement, reward-loop replacement of recoverability gates,
DecisionOS gate skipping, hidden residue/backaction/environment memory, and any
authority expansion.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "examples" / "kuuos_qi_process_tensor_conventional_autonomy_packet_v0_2G.json"

REQUIRED_TWO_TRUTHS_TRUE = [
    "qi_process_tensor_as_conventional_truth_temporal_substrate",
    "qi_process_tensor_not_ultimate_truth",
    "qi_process_tensor_not_fixed_ontology",
    "qi_process_tensor_not_proof_authority",
    "qi_process_tensor_not_self_grounding_substance",
    "ultimate_side_non_reification_preserved",
    "conventional_side_process_with_history_declared",
]

REQUIRED_SUBSTRATE_TRUE = [
    "C_world_as_process_with_history_declared",
    "T_Qi_process_tensor_declared",
    "operations_A_k_declared",
    "non_markov_memory_M_t_declared",
    "residue_bundle_R_t_declared",
    "boundary_authority_state_B_t_declared",
    "lineage_trace_Trace_t_declared",
    "state_snapshot_replacement_forbidden",
]

REQUIRED_LOOP_TRUE = [
    "observe_declared",
    "remember_declared",
    "reflect_declared",
    "plan_declared",
    "gate_declared",
    "propose_or_intervene_if_licensed_declared",
    "update_process_history_declared",
    "loop_is_candidate_generation_not_ungated_execution",
    "execution_requires_gate_license",
]

REQUIRED_ALLOWED_AUTONOMY_TRUE = [
    "history_aware_observation",
    "memory_preserving_update",
    "residue_aware_reflection",
    "recoverability_aware_planning",
    "candidate_generation",
    "safety_evaluable_proposal_formation",
]

REQUIRED_FORBIDDEN_AUTONOMY_TRUE = [
    "ungated_execution",
    "self_granted_authority",
    "direct_commit",
    "belief_root_commit",
    "memory_overwrite",
    "world_root_rewrite",
    "truth_authority",
    "clinical_authority",
    "safety_override",
]

REQUIRED_DIAGNOSTICS_TRUE = [
    "qi_stagnation_as_unresolved_memory_loop_declared",
    "qi_counterflow_as_runaway_feedback_declared",
    "qi_deficiency_as_capacity_recoverability_coherence_loss_declared",
    "diagnostics_are_control_diagnostics_not_metaphor_only",
    "pathology_visibility_required",
]

REQUIRED_GATES_TRUE = [
    "DecisionOS_safety_gate_required",
    "CBF_gate_required",
    "PAC_Bayes_uncertainty_gate_required",
    "recoverability_margin_gate_required",
    "residue_visibility_gate_required",
    "authority_boundary_gate_required",
    "handover_gate_when_required",
    "no_gate_may_be_skipped_by_qi_flow_claim",
    "no_gate_may_be_skipped_by_process_tensor_support_claim",
    "no_gate_may_be_skipped_by_historical_coherence_claim",
]

FORBIDDEN_COLLAPSES_FALSE = [
    "conventional_truth_substrate_claimed_as_ultimate_truth",
    "process_tensor_reified_as_fixed_ontology",
    "qi_process_tensor_grants_execution_authority",
    "state_snapshot_replaces_process_history",
    "reward_loop_replaces_recoverability_gate",
    "agent_loop_skips_decision_gate",
    "observation_backaction_erased",
    "environment_memory_erased",
    "temporal_correlation_erased",
    "residue_hidden",
    "reflection_result_claimed_as_truth",
    "memory_candidate_claimed_as_source_history",
    "plan_candidate_claimed_as_execution_license",
]

AUTHORITY_FALSE_FIELDS = [
    "execution_authority",
    "commit_authority",
    "belief_root_commit_authority",
    "memory_overwrite_authority",
    "world_root_rewrite_authority",
    "proof_authority",
    "ontology_authority",
    "truth_authority",
    "clinical_authority",
    "safety_override_authority",
]

REQUIRED_MODULE_MAPPING = {
    "BeliefOS": "temporal_observation_candidate",
    "MemoryOS": "process_history_record_candidate",
    "ReflectionOS": "non_markov_residue_pathology_analysis_candidate",
    "PlanOS": "temporal_transport_or_intervention_candidate",
    "DecisionOS": "safety_evaluable_candidate_and_gate_decision",
    "Qi_Process_Tensor": "temporal_history_update_surface",
}

REQUIRED_ALLOWED_SURFACES = {
    "BeliefOS.temporal_observation_candidate",
    "MemoryOS.process_history_record_candidate",
    "ReflectionOS.non_markov_residue_pathology_analysis_candidate",
    "PlanOS.temporal_transport_or_intervention_candidate",
    "DecisionOS.safety_evaluable_candidate",
    "QiProcessTensor.temporal_history_update_surface",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def require_object(packet: Mapping[str, Any], key: str, errors: List[str]) -> Mapping[str, Any]:
    value = packet.get(key)
    if not isinstance(value, Mapping):
        errors.append(f"{key} must be an object")
        return {}
    return value


def require_true(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not True:
            errors.append(f"{section_name}.{key} must be true")


def require_false(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not False:
            errors.append(f"{section_name}.{key} must be false")


def validate_shape(packet: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    if packet.get("packet_id") != "kuuos_qi_process_tensor_conventional_autonomy_packet_v0_2G":
        errors.append("packet_id mismatch")
    if packet.get("packet_type") != "qi_process_tensor_conventional_autonomy_packet":
        errors.append("packet_type must be qi_process_tensor_conventional_autonomy_packet")
    if packet.get("version") != "v0.2G":
        errors.append("version must be v0.2G")
    if packet.get("root_design") != "docs/KUUOS_QI_PROCESS_TENSOR_CONVENTIONAL_AUTONOMY_v0_2G.md":
        errors.append("root_design pointer mismatch")
    if packet.get("root_process_tensor") != "examples/physical_quantum_qi_process_tensor_packet_v0_2F.json":
        errors.append("root_process_tensor pointer mismatch")
    return errors


def validate_packet(packet: Mapping[str, Any]) -> List[str]:
    errors: List[str] = []
    errors.extend(validate_shape(packet))

    two_truths = require_object(packet, "two_truths_placement", errors)
    substrate = require_object(packet, "conventional_temporal_substrate", errors)
    loop = require_object(packet, "autonomous_loop", errors)
    mapping = require_object(packet, "module_mapping", errors)
    allowed_autonomy = require_object(packet, "allowed_autonomy", errors)
    forbidden_autonomy = require_object(packet, "forbidden_autonomy", errors)
    diagnostics = require_object(packet, "diagnostics", errors)
    gates = require_object(packet, "safety_gates", errors)
    collapses = require_object(packet, "forbidden_collapses", errors)
    authority = require_object(packet, "authority_boundary", errors)

    require_true(two_truths, "two_truths_placement", REQUIRED_TWO_TRUTHS_TRUE, errors)
    require_true(substrate, "conventional_temporal_substrate", REQUIRED_SUBSTRATE_TRUE, errors)
    require_true(loop, "autonomous_loop", REQUIRED_LOOP_TRUE, errors)
    require_true(allowed_autonomy, "allowed_autonomy", REQUIRED_ALLOWED_AUTONOMY_TRUE, errors)
    require_true(forbidden_autonomy, "forbidden_autonomy", REQUIRED_FORBIDDEN_AUTONOMY_TRUE, errors)
    require_true(diagnostics, "diagnostics", REQUIRED_DIAGNOSTICS_TRUE, errors)
    require_true(gates, "safety_gates", REQUIRED_GATES_TRUE, errors)
    require_false(collapses, "forbidden_collapses", FORBIDDEN_COLLAPSES_FALSE, errors)
    require_false(authority, "authority_boundary", AUTHORITY_FALSE_FIELDS, errors)

    for key, expected in REQUIRED_MODULE_MAPPING.items():
        if mapping.get(key) != expected:
            errors.append(f"module_mapping.{key} must be {expected}")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_ALLOWED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    packet = load_json(path)
    errors = validate_packet(packet)
    if errors:
        print("KuuOS Qi Process Tensor Conventional Autonomy v0.2G validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("KuuOS Qi Process Tensor Conventional Autonomy v0.2G validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
