#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor

PLAN_VERSION = "indra_qi_process_tensor_activation_plan_v0_4"
ALLOWED_FEEDBACK_KINDS = {
    "local_patch_observation_candidate",
    "qi_flow_observable_candidate",
}
REQUIRED_BOUNDARY = {
    "qi_process_tensor_conditions_not_authority": True,
    "explicit_mutation_license_required": True,
    "runtime_observation_overlay_only": True,
    "source_feedback_candidate_not_truth": True,
    "source_indra_structure_preserved": True,
    "operator_algebra_unchanged": True,
    "gauge_connection_unchanged": True,
    "holonomy_preserved": True,
    "transport_residue_visible": True,
    "noncommutative_order_preserved": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "rollback_snapshot_required": True,
    "post_write_verification_required": True,
    "not_direct_execution_authority": True,
    "external_world_actuation_authority": False,
    "fail_closed_on_boundary_loss": True,
}
PROTECTED_STRUCTURE_FIELDS = (
    "core_statement",
    "causal_world_model_bridge",
    "local_world_patches",
    "indra_connections",
    "qi_flow_channels",
    "holonomy_cycles",
    "ku_string_correspondences",
    "extended_m_brane_surfaces",
    "mandala_inclusion",
    "two_truths_boundary",
    "governance_boundary",
)


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


def activation_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "activation_plan_digest"))


def protected_structure_digest(state: Mapping[str, Any]) -> str:
    return sha({field: deepcopy(state.get(field)) for field in PROTECTED_STRUCTURE_FIELDS})


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("process_tensor_activation_plan_version_invalid")
    if str(plan.get("activation_plan_digest", "")) != activation_plan_digest(plan):
        blockers.append("process_tensor_activation_plan_digest_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"process_tensor_activation_boundary_{field}_mismatch")
    if plan.get("mutation_scope") != "runtime_observation_overlays_only":
        blockers.append("process_tensor_activation_mutation_scope_invalid")
    if plan.get("apply_order") != "feedback_packet_order":
        blockers.append("process_tensor_activation_apply_order_invalid")
    if plan.get("rollback_required") is not True:
        blockers.append("process_tensor_activation_rollback_required_not_true")
    policy = mapping(plan.get("process_tensor_policy"))
    numeric_ranges = {
        "min_transition_continuity_score": (0.0, 1.0),
        "min_memory_continuity_score": (0.0, 1.0),
        "min_nonmarkov_link_density": (0.0, 1.0),
        "min_recoverability_branching_capacity": (0.0, 1.0),
        "max_observation_debt_pressure": (0.0, 1.0),
        "min_candidate_weight": (0.0, 1.0),
    }
    for field, (minimum, maximum) in numeric_ranges.items():
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not minimum <= float(raw) <= maximum:
            blockers.append(f"process_tensor_policy_{field}_invalid")
    depth = policy.get("min_history_depth")
    if isinstance(depth, bool) or not isinstance(depth, int) or depth < 3:
        blockers.append("process_tensor_policy_min_history_depth_invalid")
    for field in (
        "require_process_tensor_visible",
        "require_transition_continuity_visible",
        "require_memory_continuity_visible",
        "require_nonmarkov_memory_visible",
        "require_recoverability_witness",
    ):
        if policy.get(field) is not True:
            blockers.append(f"process_tensor_policy_{field}_not_true")


def validate_review_decisions(
    plan: Mapping[str, Any], candidates: list[Mapping[str, Any]], blockers: list[str]
) -> dict[str, Mapping[str, Any]]:
    raw_decisions = items(plan.get("review_decisions"))
    decisions: dict[str, Mapping[str, Any]] = {}
    for raw in raw_decisions:
        decision = mapping(raw)
        candidate_id = str(decision.get("candidate_id", ""))
        if not candidate_id or candidate_id in decisions:
            blockers.append("process_tensor_review_candidate_id_invalid_or_duplicate")
            continue
        if decision.get("decision") not in {"approve", "reject"}:
            blockers.append(f"process_tensor_review_{candidate_id}_decision_invalid")
        if not str(decision.get("reason", "")).strip():
            blockers.append(f"process_tensor_review_{candidate_id}_reason_missing")
        decisions[candidate_id] = decision
    candidate_ids = [str(candidate.get("candidate_id", "")) for candidate in candidates]
    if set(decisions) != set(candidate_ids):
        blockers.append("process_tensor_review_decision_set_mismatch")
    if len(candidate_ids) != len(set(candidate_ids)):
        blockers.append("source_feedback_candidate_id_duplicate")
    return decisions


def _history_item(
    *,
    stage: str,
    digest: str,
    nonmarkov: bool,
    recoverable: bool,
    debt_unresolved: bool,
) -> dict[str, Any]:
    return {
        "stage": stage,
        "stage_digest": digest,
        "transition_visible": True,
        "memory_link_visible": True,
        "nonmarkov_link_visible": nonmarkov,
        "process_observation": stage,
        "process_action": "review_and_transport",
        "recovery_witness_present": recoverable,
        "observation_debt_unresolved": debt_unresolved,
    }


def process_history(
    *,
    feedback_packet: Mapping[str, Any],
    candidate: Mapping[str, Any],
    decision: Mapping[str, Any],
    prior_overlays: list[Mapping[str, Any]],
    rollback_required: bool,
) -> list[dict[str, Any]]:
    history = [
        _history_item(
            stage="local_causal_projection",
            digest=str(feedback_packet.get("source_projection_id", "")),
            nonmarkov=False,
            recoverable=True,
            debt_unresolved=False,
        ),
        _history_item(
            stage=str(feedback_packet.get("source_causal_event_kind", "causal_event")),
            digest=str(feedback_packet.get("source_causal_event_digest", "")),
            nonmarkov=True,
            recoverable=True,
            debt_unresolved=False,
        ),
    ]
    for overlay in prior_overlays[-3:]:
        history.append(
            _history_item(
                stage="prior_indra_qi_observation_overlay",
                digest=str(overlay.get("overlay_digest", "")),
                nonmarkov=True,
                recoverable=True,
                debt_unresolved=False,
            )
        )
    history.append(
        _history_item(
            stage="feedback_candidate_review",
            digest=str(mapping(candidate.get("candidate_payload")).get("feedback_evidence_digest", "")),
            nonmarkov=True,
            recoverable=rollback_required,
            debt_unresolved=decision.get("decision") not in {"approve", "reject"},
        )
    )
    return history


def assess_candidate(
    *,
    feedback_packet: Mapping[str, Any],
    candidate: Mapping[str, Any],
    decision: Mapping[str, Any],
    prior_overlays: list[Mapping[str, Any]],
    plan: Mapping[str, Any],
) -> dict[str, Any]:
    history = process_history(
        feedback_packet=feedback_packet,
        candidate=candidate,
        decision=decision,
        prior_overlays=prior_overlays,
        rollback_required=plan.get("rollback_required") is True,
    )
    raw = {
        "cycle_id": f"process-tensor-{candidate.get('candidate_id', '')}",
        "process_history": history,
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
    }
    receipt = evaluate_qi_process_tensor(raw).to_dict()
    history_depth = len(history)
    transition_count = sum(1 for item in history if item.get("transition_visible") is True)
    memory_count = sum(1 for item in history if item.get("memory_link_visible") is True)
    nonmarkov_count = sum(1 for item in history if item.get("nonmarkov_link_visible") is True)
    recovery_count = sum(1 for item in history if item.get("recovery_witness_present") is True)
    debt_count = sum(1 for item in history if item.get("observation_debt_unresolved") is True)
    denominator = max(history_depth, 1)
    assessment = {
        "candidate_id": str(candidate.get("candidate_id", "")),
        "history_depth": history_depth,
        "transition_continuity_score": round(transition_count / denominator, 8),
        "memory_continuity_score": round(memory_count / denominator, 8),
        "nonmarkov_link_density": round(nonmarkov_count / denominator, 8),
        "recoverability_branching_capacity": round(recovery_count / denominator, 8),
        "observation_debt_pressure": round(debt_count / denominator, 8),
        "qi_process_tensor_receipt": receipt,
        "process_history_digest": sha(history),
        "process_history": history,
        "boundary": {
            "history_bearing_process_tensor": True,
            "non_markov_context_required": True,
            "multi_time_window_required": True,
            "memory_kernel_visible": True,
            "recoverability_visible": True,
            "observation_debt_visible": True,
            "process_tensor_conditions_not_authority": True,
        },
    }
    assessment["assessment_digest"] = sha(assessment)
    return assessment


def assessment_blockers(
    *,
    candidate: Mapping[str, Any],
    decision: Mapping[str, Any],
    assessment: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    candidate_id = str(candidate.get("candidate_id", ""))
    receipt = mapping(assessment.get("qi_process_tensor_receipt"))
    if decision.get("decision") != "approve":
        return blockers
    checks = {
        "process_tensor_visible": receipt.get("process_tensor_visible") is True,
        "transition_continuity_visible": receipt.get("transition_continuity_visible") is True,
        "memory_continuity_visible": receipt.get("memory_continuity_visible") is True,
        "nonmarkov_memory_visible": receipt.get("nonmarkov_memory_visible") is True,
    }
    for field, ok in checks.items():
        if policy.get(f"require_{field}") is True and not ok:
            blockers.append(f"candidate_{candidate_id}_{field}_missing")
    thresholds = {
        "history_depth": ("min_history_depth", ">="),
        "transition_continuity_score": ("min_transition_continuity_score", ">="),
        "memory_continuity_score": ("min_memory_continuity_score", ">="),
        "nonmarkov_link_density": ("min_nonmarkov_link_density", ">="),
        "recoverability_branching_capacity": ("min_recoverability_branching_capacity", ">="),
        "observation_debt_pressure": ("max_observation_debt_pressure", "<="),
    }
    for metric, (policy_field, direction) in thresholds.items():
        value = float(assessment.get(metric, 0.0))
        threshold = float(policy.get(policy_field, 0.0))
        if (direction == ">=" and value < threshold) or (direction == "<=" and value > threshold):
            blockers.append(f"candidate_{candidate_id}_{metric}_outside_policy")
    weight = candidate.get("candidate_weight")
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        blockers.append(f"candidate_{candidate_id}_weight_invalid")
    elif float(weight) < float(policy.get("min_candidate_weight", 0.0)):
        blockers.append(f"candidate_{candidate_id}_weight_below_policy")
    if policy.get("require_recoverability_witness") is True and float(
        assessment.get("recoverability_branching_capacity", 0.0)
    ) <= 0:
        blockers.append(f"candidate_{candidate_id}_recoverability_witness_missing")
    return blockers


def build_overlay(
    *,
    activation_id: str,
    sequence: int,
    candidate: Mapping[str, Any],
    assessment: Mapping[str, Any],
    feedback_packet_digest: str,
    previous_overlay_digest: str,
) -> dict[str, Any]:
    payload = mapping(candidate.get("candidate_payload"))
    overlay = {
        "overlay_id": f"{activation_id}-overlay-{sequence}",
        "activation_id": activation_id,
        "sequence": sequence,
        "feedback_kind": str(candidate.get("feedback_kind", "")),
        "target": deepcopy(dict(mapping(candidate.get("target")))),
        "observed_value": payload.get("proposed_observable_value"),
        "observed_uncertainty": payload.get("proposed_uncertainty"),
        "candidate_weight": candidate.get("candidate_weight"),
        "source_candidate_id": str(candidate.get("candidate_id", "")),
        "source_feedback_packet_digest": feedback_packet_digest,
        "process_tensor_assessment_digest": str(assessment.get("assessment_digest", "")),
        "process_history_digest": str(assessment.get("process_history_digest", "")),
        "previous_overlay_digest": previous_overlay_digest,
        "surface_kind": "runtime_conventional_observation_overlay",
        "boundary": {
            "direct_world_state_mutation": True,
            "runtime_observation_overlay_only": True,
            "operator_algebra_unchanged": True,
            "gauge_connection_unchanged": True,
            "holonomy_preserved": True,
            "external_world_not_actuated": True,
            "rollback_snapshot_available": True,
        },
    }
    overlay["overlay_digest"] = sha(overlay)
    return overlay
