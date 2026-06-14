#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_indra_qi_process_tensor_activation_core_v0_4 import (
    ALLOWED_FEEDBACK_KINDS,
    REQUIRED_BOUNDARY as ACTIVATION_BOUNDARY,
    activation_plan_digest,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import (
    REQUIRED_BOUNDARY as CYCLE_BOUNDARY,
    cycle_plan_digest,
)

PLAN_VERSION = "indra_qi_child_feedback_parent_cycle_plan_v0_10"
REQUIRED_BOUNDARY = {
    "child_feedback_handoff_not_truth": True,
    "child_feedback_copied_not_moved": True,
    "parent_feedback_stage_digest_exact": True,
    "parent_world_mutation_only_via_v0_4": True,
    "v0_4_activation_license_required": True,
    "v0_5_cycle_license_required": True,
    "v0_4_and_v0_5_transaction_compensated": True,
    "child_runtime_not_mutated": True,
    "child_v14_state_not_mutated": True,
    "parent_protected_structure_preserved": True,
    "runtime_observation_overlay_only": True,
    "next_cycle_seed_not_fact": True,
    "next_cycle_seed_not_direct_execution_authority": True,
    "runtime_local_external_state_only": True,
    "base_gauge_connection_not_mutated": True,
    "operator_algebra_unchanged": True,
    "causal_edge_not_gauge_connection": True,
    "qi_not_substance": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_external_world_actuation_authority": True,
    "not_direct_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def bridge_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "bridge_plan_digest"))


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("child_feedback_cycle_plan_version_invalid")
    if str(plan.get("bridge_plan_digest", "")) != bridge_plan_digest(plan):
        blockers.append("child_feedback_cycle_plan_digest_invalid")
    for field in (
        "bridge_id",
        "source_execution_id",
        "source_execution_record_digest",
        "source_execution_ledger_record_digest",
        "source_reentry_id",
        "source_reentry_record_digest",
        "source_parent_world_state_digest",
        "source_child_feedback_id",
        "source_child_feedback_packet_digest",
        "source_child_feedback_handoff_digest",
        "activation_id",
        "cycle_id",
        "expected_previous_cycle_state_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"child_feedback_cycle_plan_{field}_missing")
    approved = [str(value) for value in items(plan.get("approved_candidate_ids"))]
    if not approved or len(approved) != len(set(approved)):
        blockers.append("child_feedback_cycle_approved_candidate_ids_invalid")
    if plan.get("handoff_mode") != "child_feedback_to_parent_process_tensor_cycle":
        blockers.append("child_feedback_cycle_handoff_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"child_feedback_cycle_boundary_{field}_mismatch")

    process_policy = mapping(plan.get("process_tensor_policy"))
    for field in (
        "min_transition_continuity_score",
        "min_memory_continuity_score",
        "min_nonmarkov_link_density",
        "min_recoverability_branching_capacity",
        "max_observation_debt_pressure",
        "min_candidate_weight",
    ):
        raw = process_policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"child_feedback_cycle_process_policy_{field}_invalid")
    depth = process_policy.get("min_history_depth")
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 3:
        blockers.append("child_feedback_cycle_process_policy_min_history_depth_invalid")
    for field in (
        "require_process_tensor_visible",
        "require_transition_continuity_visible",
        "require_memory_continuity_visible",
        "require_nonmarkov_memory_visible",
        "require_recoverability_witness",
    ):
        if process_policy.get(field) is not True:
            blockers.append(f"child_feedback_cycle_process_policy_{field}_not_true")

    evolution = mapping(plan.get("evolution_policy"))
    for field in (
        "memory_retention",
        "intervention_residue_retention",
        "nonmarkov_retention",
        "recoverability_retention",
        "observation_debt_retention",
        "min_next_cycle_prior_weight",
        "max_next_cycle_observation_debt",
        "min_next_cycle_recoverability",
    ):
        raw = evolution.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"child_feedback_cycle_evolution_policy_{field}_invalid")
    maximum = evolution.get("max_channels")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
        blockers.append("child_feedback_cycle_evolution_policy_max_channels_invalid")


def build_activation_plan(
    *,
    plan: Mapping[str, Any],
    feedback_packet: Mapping[str, Any],
    feedback_handoff: Mapping[str, Any],
    parent_world_digest: str,
) -> dict[str, Any]:
    approved = {str(value) for value in items(plan.get("approved_candidate_ids"))}
    decisions: list[dict[str, Any]] = []
    for raw in items(feedback_packet.get("feedback_candidates")):
        candidate = mapping(raw)
        candidate_id = str(candidate.get("candidate_id", ""))
        is_approved = candidate_id in approved
        decisions.append(
            {
                "candidate_id": candidate_id,
                "decision": "approve" if is_approved else "reject",
                "reason": (
                    "approved by v0.10 child-to-parent Process Tensor handoff"
                    if is_approved
                    else "reviewed and retained without parent WORLD mutation"
                ),
            }
        )
    activation = {
        "version": "indra_qi_process_tensor_activation_plan_v0_4",
        "activation_id": str(plan.get("activation_id", "")),
        "source_feedback_id": str(feedback_packet.get("feedback_id", "")),
        "source_feedback_packet_digest": str(feedback_packet.get("feedback_packet_digest", "")),
        "source_approval_handoff_digest": str(feedback_handoff.get("approval_handoff_digest", "")),
        "source_indra_qi_world_state_digest": parent_world_digest,
        "mutation_scope": "runtime_observation_overlays_only",
        "apply_order": "feedback_packet_order",
        "rollback_required": True,
        "review_decisions": decisions,
        "process_tensor_policy": dict(mapping(plan.get("process_tensor_policy"))),
        "boundary": dict(ACTIVATION_BOUNDARY),
    }
    activation["activation_plan_digest"] = activation_plan_digest(activation)
    return activation


def build_cycle_plan(
    *,
    plan: Mapping[str, Any],
    activation_record: Mapping[str, Any],
    review: Mapping[str, Any],
    parent_world_digest: str,
) -> dict[str, Any]:
    cycle = {
        "version": "indra_qi_process_tensor_cycle_plan_v0_5",
        "cycle_id": str(plan.get("cycle_id", "")),
        "source_activation_id": str(activation_record.get("activation_id", "")),
        "source_activation_record_digest": str(activation_record.get("activation_record_digest", "")),
        "source_process_tensor_review_digest": str(review.get("process_tensor_review_digest", "")),
        "source_world_state_digest": parent_world_digest,
        "expected_previous_cycle_state_digest": str(
            plan.get("expected_previous_cycle_state_digest", "")
        ),
        "evolution_mode": "non_markov_overlay_assimilation",
        "evolution_policy": dict(mapping(plan.get("evolution_policy"))),
        "boundary": dict(CYCLE_BOUNDARY),
    }
    cycle["cycle_plan_digest"] = cycle_plan_digest(cycle)
    return cycle


def validate_activation_license_template(
    template: Mapping[str, Any], approved_count: int, blockers: list[str]
) -> None:
    if template.get("license_status") != "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_LICENSE_READY":
        blockers.append("child_feedback_cycle_nested_v0_4_license_not_ready")
    for flag in (
        "source_feedback_packet_read_allowed",
        "source_approval_handoff_read_allowed",
        "world_state_read_allowed",
        "activation_plan_validate_allowed",
        "process_tensor_review_write_allowed",
        "rollback_snapshot_write_allowed",
        "runtime_observation_overlay_write_allowed",
        "world_state_write_allowed",
        "post_write_verification_allowed",
        "activation_record_write_allowed",
        "mutation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "direct_world_model_mutation_allowed",
    ):
        if template.get(flag) is not True:
            blockers.append(f"child_feedback_cycle_nested_v0_4_{flag}_not_true")
    scopes = template.get("allowed_mutation_scopes", [])
    scope_set = {str(value) for value in scopes} if isinstance(scopes, list) else set()
    if scope_set != {"runtime_observation_overlays_only"}:
        blockers.append("child_feedback_cycle_nested_v0_4_mutation_scope_not_exact")
    kinds = template.get("allowed_feedback_kinds", [])
    kind_set = {str(value) for value in kinds} if isinstance(kinds, list) else set()
    if kind_set != ALLOWED_FEEDBACK_KINDS:
        blockers.append("child_feedback_cycle_nested_v0_4_feedback_kinds_not_exact")
    maximum = template.get("max_approved_candidates")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < approved_count:
        blockers.append("child_feedback_cycle_nested_v0_4_max_approved_candidates_insufficient")


def validate_cycle_license_template(template: Mapping[str, Any], blockers: list[str]) -> None:
    if template.get("license_status") != "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_LICENSE_READY":
        blockers.append("child_feedback_cycle_nested_v0_5_license_not_ready")
    for flag in (
        "world_state_read_allowed",
        "activation_record_read_allowed",
        "process_tensor_review_read_allowed",
        "feedback_packet_read_allowed",
        "mutation_ledger_read_allowed",
        "previous_cycle_state_read_allowed",
        "cycle_plan_validate_allowed",
        "cycle_state_write_allowed",
        "next_cycle_seed_write_allowed",
        "cycle_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if template.get(flag) is not True:
            blockers.append(f"child_feedback_cycle_nested_v0_5_{flag}_not_true")
