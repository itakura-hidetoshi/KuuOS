#!/usr/bin/env python3
"""Physical Quantum Qi Process Tensor runtime v0.2F.

This runtime implements a non-authoritative Qi Process Tensor surface.

Canonical interpretation:
- Process Tensor = multi-time non-Markov temporal structure
- Qi = history-bearing relational/action flow on that temporal structure

The runtime does not simulate quantum mechanics.  It validates and projects a
machine-readable process-tensor packet into candidate surfaces for KuuOS modules.
It grants no proof, truth, ontology, clinical, execution, commit, memory
overwrite, world rewrite, or safety override authority.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Mapping, Sequence

REQUIRED_AUTHORITY_FALSE = [
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

REQUIRED_PROCESS_TENSOR_TRUE = [
    "process_tensor_declared",
    "multi_time_structure_declared",
    "operations_sequence_declared",
    "causal_order_declared",
    "non_markovian_by_definition",
    "history_state_not_replaced_by_snapshot",
    "intervention_history_declared",
    "observation_backaction_declared",
    "environment_memory_declared",
    "temporal_correlation_declared",
    "process_tensor_is_temporal_structure_not_qi_itself",
]

REQUIRED_QI_ON_PROCESS_TRUE = [
    "qi_as_history_bearing_relational_flow_declared",
    "qi_flow_on_process_tensor_declared",
    "qi_current_depends_on_operation_history",
    "qi_memory_kernel_depends_on_process_history",
    "qi_recoverability_depends_on_process_history",
    "qi_transport_depends_on_process_history",
    "qi_observation_changes_future_history",
    "qi_residue_visible_across_time",
]

REQUIRED_PATHOLOGY_TRUE = [
    "qi_stagnation_as_unresolved_memory_loop_declared",
    "qi_counterflow_as_runaway_feedback_declared",
    "qi_deficiency_as_capacity_recoverability_coherence_loss_declared",
    "runaway_feedback_guard_declared",
    "trapped_recurrence_guard_declared",
    "coherence_loss_guard_declared",
]

REQUIRED_INDRA_TRUE = [
    "indranet_as_spatial_dependent_origination_declared",
    "process_tensor_as_temporal_dependent_origination_declared",
    "qi_as_action_flow_across_spatial_and_temporal_engi_declared",
    "gauge_transport_link_declared",
    "holonomy_history_link_declared",
]

REQUIRED_SURFACES = {
    "BeliefOS.temporal_observation_candidate",
    "PlanOS.temporal_transport_candidate",
    "MemoryOS.process_history_record_candidate",
    "ReflectionOS.non_markov_residue_analysis_candidate",
    "DecisionOS.safety_evaluable_candidate",
}

FORBIDDEN_FLAGS = [
    "process_tensor_collapsed_to_markov_channel",
    "qi_identified_with_process_tensor_itself",
    "current_state_only_prediction_claimed",
    "operation_history_erased",
    "observation_backaction_erased",
    "environment_memory_erased",
    "temporal_correlation_erased",
    "stagnation_loop_hidden",
    "runaway_feedback_hidden",
    "coherence_loss_hidden",
]


@dataclass(frozen=True)
class QiProcessTensorResult:
    packet_id: str
    valid: bool
    errors: List[str]
    temporal_structure_status: str
    qi_flow_status: str
    non_markov_status: str
    pathology_status: str
    allowed_surfaces: List[str]
    authority_boundary: Dict[str, bool]
    candidate_payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _section(packet: Mapping[str, Any], name: str, errors: List[str]) -> Mapping[str, Any]:
    value = packet.get(name)
    if not isinstance(value, Mapping):
        errors.append(f"{name} must be an object")
        return {}
    return value


def _require_true(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not True:
            errors.append(f"{section_name}.{key} must be true")


def _require_false(section: Mapping[str, Any], section_name: str, keys: Sequence[str], errors: List[str]) -> None:
    for key in keys:
        if section.get(key) is not False:
            errors.append(f"{section_name}.{key} must be false")


def validate_qi_process_tensor_packet(packet: Mapping[str, Any]) -> List[str]:
    """Return validation errors for a Qi Process Tensor packet."""

    errors: List[str] = []
    if packet.get("packet_type") != "qi_process_tensor_packet":
        errors.append("packet_type must be qi_process_tensor_packet")
    if packet.get("version") != "v0.2F":
        errors.append("version must be v0.2F")

    process_tensor = _section(packet, "process_tensor", errors)
    qi_on_process = _section(packet, "qi_on_process_tensor", errors)
    pathologies = _section(packet, "qi_process_pathologies", errors)
    indra = _section(packet, "indranet_temporal_bridge", errors)
    forbidden = _section(packet, "forbidden_reductions", errors)
    authority = _section(packet, "authority_boundary", errors)

    _require_true(process_tensor, "process_tensor", REQUIRED_PROCESS_TENSOR_TRUE, errors)
    _require_true(qi_on_process, "qi_on_process_tensor", REQUIRED_QI_ON_PROCESS_TRUE, errors)
    _require_true(pathologies, "qi_process_pathologies", REQUIRED_PATHOLOGY_TRUE, errors)
    _require_true(indra, "indranet_temporal_bridge", REQUIRED_INDRA_TRUE, errors)
    _require_false(forbidden, "forbidden_reductions", FORBIDDEN_FLAGS, errors)
    _require_false(authority, "authority_boundary", REQUIRED_AUTHORITY_FALSE, errors)

    operations = process_tensor.get("operations")
    if not isinstance(operations, list) or len(operations) < 2:
        errors.append("process_tensor.operations must contain at least two time operations")
    else:
        for index, operation in enumerate(operations):
            if not isinstance(operation, Mapping):
                errors.append(f"process_tensor.operations[{index}] must be an object")
                continue
            for key in ["time", "operation_id", "operation_kind", "backaction_visible"]:
                if key not in operation:
                    errors.append(f"process_tensor.operations[{index}].{key} is required")
            if operation.get("backaction_visible") is not True:
                errors.append(f"process_tensor.operations[{index}].backaction_visible must be true")

    memory_links = process_tensor.get("memory_links")
    if not isinstance(memory_links, list) or not memory_links:
        errors.append("process_tensor.memory_links must be a nonempty list")
    else:
        for index, link in enumerate(memory_links):
            if not isinstance(link, Mapping):
                errors.append(f"process_tensor.memory_links[{index}] must be an object")
                continue
            if link.get("tail_residue_visible") is not True:
                errors.append(f"process_tensor.memory_links[{index}].tail_residue_visible must be true")

    surfaces = packet.get("allowed_surfaces")
    if not isinstance(surfaces, list):
        errors.append("allowed_surfaces must be a list")
    else:
        missing = sorted(REQUIRED_SURFACES - {str(surface) for surface in surfaces})
        for surface in missing:
            errors.append(f"allowed_surfaces missing {surface}")

    return errors


def build_qi_process_tensor_result(packet: Mapping[str, Any]) -> QiProcessTensorResult:
    """Validate and project a packet into a non-authoritative candidate result."""

    errors = validate_qi_process_tensor_packet(packet)
    valid = not errors
    surfaces = packet.get("allowed_surfaces", [])
    if not isinstance(surfaces, list):
        surfaces = []
    authority = packet.get("authority_boundary", {})
    if not isinstance(authority, Mapping):
        authority = {}

    candidate_payload = {
        "surface_type": "QiProcessTensorCandidate",
        "version": "v0.2F",
        "process_tensor_is_temporal_structure": True,
        "qi_is_flow_on_temporal_structure": True,
        "non_markov_primary": True,
        "markov_reduction_allowed": False,
        "current_state_only_prediction_allowed": False,
        "operation_history_required": True,
        "observation_backaction_visible": True,
        "tail_residue_visible": True,
        "authority_granted": False,
    }

    return QiProcessTensorResult(
        packet_id=str(packet.get("packet_id", "<missing>")),
        valid=valid,
        errors=errors,
        temporal_structure_status="valid_process_tensor_structure" if valid else "invalid_process_tensor_structure",
        qi_flow_status="valid_history_bearing_qi_flow" if valid else "invalid_qi_flow",
        non_markov_status="primary_non_markov" if valid else "non_markov_validation_failed",
        pathology_status="visible_stagnation_counterflow_deficiency_guards" if valid else "pathology_visibility_failed",
        allowed_surfaces=[str(surface) for surface in surfaces],
        authority_boundary={key: bool(authority.get(key)) for key in REQUIRED_AUTHORITY_FALSE},
        candidate_payload=candidate_payload,
    )


def build_qi_process_tensor_candidate(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Convenience dict wrapper for demos/tests."""

    return build_qi_process_tensor_result(packet).to_dict()
