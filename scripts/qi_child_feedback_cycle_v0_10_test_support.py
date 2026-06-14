#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_child_feedback_cycle_core_v0_10 import (
    REQUIRED_BOUNDARY,
    bridge_plan_digest,
)
from runtime.kuuos_indra_qi_process_tensor_cycle_core_v0_5 import cycle_state_digest
from runtime.kuuos_runtime_daemon_qi_child_feedback_parent_cycle_v0_10 import (
    build_indra_qi_child_feedback_parent_cycle_v0_10,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
)
from scripts.qi_action_v0_9_test_support import (
    build_execution_plan,
    prepare_envelope,
    run_execution,
)


def prepare_v0_9_execution(
    root: pathlib.Path,
    suffix: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    pathlib.Path,
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    world, reentry, child, causal, source = prepare_envelope(
        root, f"parent-cycle-{suffix}", "bounded"
    )
    execution_plan = build_execution_plan(
        world=world,
        reentry=reentry,
        causal=causal,
        envelope=source["envelope"],
        activation=source["activation"],
        kind="bounded_intervention_candidate",
        suffix=f"parent-cycle-{suffix}",
    )
    execution_result = run_execution(root, execution_plan, causal)
    assert execution_result[
        "status"
    ] == "INDRA_QI_APPROVED_RECOVERY_ACTION_EXECUTION_V0_9_READY", execution_result
    execution = read_json(
        root / "indra_qi_approved_recovery_action_execution_record_v0_9.json"
    )
    execution_ledger = records(
        root / "indra_qi_approved_recovery_action_execution_ledger_v0_9.jsonl"
    )[-1]
    child_feedback = read_json(
        child / "indra_qi_causal_feedback_candidate_packet_v0_3.json"
    )
    child_handoff = read_json(
        child / "indra_qi_causal_feedback_approval_handoff_v0_3.json"
    )
    parent_world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    return (
        parent_world,
        execution,
        child,
        child_feedback,
        child_handoff,
        execution_ledger,
    )


def approved_candidate_ids(feedback: dict[str, Any]) -> list[str]:
    candidates = feedback["feedback_candidates"]
    local = [
        value["candidate_id"]
        for value in candidates
        if value["feedback_kind"] == "local_patch_observation_candidate"
    ]
    flow = [
        value["candidate_id"]
        for value in candidates
        if value["feedback_kind"] == "qi_flow_observable_candidate"
    ]
    assert local and flow, feedback
    return [local[0], flow[0]]


def build_plan(
    *,
    root: pathlib.Path,
    world: dict[str, Any],
    execution: dict[str, Any],
    execution_ledger: dict[str, Any],
    feedback: dict[str, Any],
    handoff: dict[str, Any],
    suffix: str,
) -> dict[str, Any]:
    reentry = read_json(root / "indra_qi_post_assimilation_causal_reentry_record_v0_7.json")
    previous = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    previous_digest = (
        previous["process_tensor_cycle_state_digest"] if previous else "GENESIS"
    )
    if previous:
        assert cycle_state_digest(previous) == previous_digest
    plan = {
        "version": "indra_qi_child_feedback_parent_cycle_plan_v0_10",
        "bridge_id": f"child-feedback-parent-cycle-{suffix}",
        "source_execution_id": execution["execution_id"],
        "source_execution_record_digest": execution["execution_record_digest"],
        "source_execution_ledger_record_digest": execution_ledger["record_digest"],
        "source_reentry_id": reentry["reentry_id"],
        "source_reentry_record_digest": reentry["reentry_record_digest"],
        "source_parent_world_state_digest": world["indra_qi_world_state_digest"],
        "source_child_feedback_id": feedback["feedback_id"],
        "source_child_feedback_packet_digest": feedback["feedback_packet_digest"],
        "source_child_feedback_handoff_digest": handoff["approval_handoff_digest"],
        "activation_id": f"parent-process-tensor-activation-{suffix}",
        "cycle_id": f"parent-process-tensor-cycle-{suffix}",
        "expected_previous_cycle_state_digest": previous_digest,
        "approved_candidate_ids": approved_candidate_ids(feedback),
        "handoff_mode": "child_feedback_to_parent_process_tensor_cycle",
        "process_tensor_policy": {
            "min_history_depth": 3,
            "min_transition_continuity_score": 0.75,
            "min_memory_continuity_score": 0.75,
            "min_nonmarkov_link_density": 0.5,
            "min_recoverability_branching_capacity": 0.75,
            "max_observation_debt_pressure": 0.1,
            "min_candidate_weight": 0.5,
            "require_process_tensor_visible": True,
            "require_transition_continuity_visible": True,
            "require_memory_continuity_visible": True,
            "require_nonmarkov_memory_visible": True,
            "require_recoverability_witness": True,
        },
        "evolution_policy": {
            "memory_retention": 0.75,
            "intervention_residue_retention": 0.70,
            "nonmarkov_retention": 0.75,
            "recoverability_retention": 0.70,
            "observation_debt_retention": 0.80,
            "min_next_cycle_prior_weight": 0.50,
            "max_next_cycle_observation_debt": 0.20,
            "min_next_cycle_recoverability": 0.25,
            "max_channels": 16,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    plan["bridge_plan_digest"] = bridge_plan_digest(plan)
    return plan


def activation_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_ACTIVATION_V0_4_LICENSE_READY",
        "source_feedback_packet_read_allowed": True,
        "source_approval_handoff_read_allowed": True,
        "world_state_read_allowed": True,
        "activation_plan_validate_allowed": True,
        "process_tensor_review_write_allowed": True,
        "rollback_snapshot_write_allowed": True,
        "runtime_observation_overlay_write_allowed": True,
        "world_state_write_allowed": True,
        "post_write_verification_allowed": True,
        "activation_record_write_allowed": True,
        "mutation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_mutation_scopes": ["runtime_observation_overlays_only"],
        "allowed_feedback_kinds": [
            "local_patch_observation_candidate",
            "qi_flow_observable_candidate",
        ],
        "max_approved_candidates": 3,
    }
    value.update(overrides)
    return value


def cycle_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_CYCLE_V0_5_LICENSE_READY",
        "world_state_read_allowed": True,
        "activation_record_read_allowed": True,
        "process_tensor_review_read_allowed": True,
        "feedback_packet_read_allowed": True,
        "mutation_ledger_read_allowed": True,
        "previous_cycle_state_read_allowed": True,
        "cycle_plan_validate_allowed": True,
        "cycle_state_write_allowed": True,
        "next_cycle_seed_write_allowed": True,
        "cycle_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def bridge_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_LICENSE_READY",
        "bound_bridge_plan_digest": plan["bridge_plan_digest"],
        "source_execution_lineage_read_allowed": True,
        "source_reentry_read_allowed": True,
        "child_feedback_read_allowed": True,
        "parent_world_read_allowed": True,
        "parent_feedback_stage_write_allowed": True,
        "transaction_snapshot_allowed": True,
        "transaction_restore_allowed": True,
        "v0_4_activation_invoke_allowed": True,
        "v0_5_cycle_invoke_allowed": True,
        "handoff_packet_write_allowed": True,
        "bridge_record_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v0_4_activation_license_template": activation_template(),
        "v0_5_cycle_license_template": cycle_template(),
    }
    value.update(overrides)
    return value


def run_bridge(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_child_feedback_parent_cycle_v0_10(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_child_feedback_parent_cycle_v0_10_enabled": True,
            "apply_indra_qi_child_feedback_parent_cycle_v0_10": True,
        },
        bridge_plan=plan,
        bridge_license=license_value or bridge_license(plan),
    ).to_dict()
