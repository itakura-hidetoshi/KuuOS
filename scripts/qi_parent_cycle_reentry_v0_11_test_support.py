#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_indra_qi_parent_cycle_reentry_core_v0_11 import (
    REQUIRED_BOUNDARY,
    loop_plan_digest,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import DYNAMIC_WORLD_FIELDS
from runtime.kuuos_runtime_daemon_qi_parent_cycle_reentry_v0_11 import (
    build_indra_qi_parent_cycle_assimilation_reentry_v0_11,
)
from scripts.check_indra_qi_process_tensor_world_assimilation_v0_6 import (
    read_json,
    records,
)
from scripts.qi_child_feedback_cycle_v0_10_test_support import (
    build_plan as build_v0_10_plan,
    prepare_v0_9_execution,
    run_bridge as run_v0_10,
)


def latest(path: pathlib.Path) -> dict[str, Any]:
    values = records(path)
    return values[-1] if values else {}


def prepare_v0_10_cycle(
    root: pathlib.Path,
    suffix: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    world, execution, _, feedback, feedback_handoff, execution_ledger = prepare_v0_9_execution(
        root, f"v0-11-{suffix}"
    )
    plan = build_v0_10_plan(
        root=root,
        world=world,
        execution=execution,
        execution_ledger=execution_ledger,
        feedback=feedback,
        handoff=feedback_handoff,
        suffix=f"v0-11-{suffix}",
    )
    result = run_v0_10(root, plan)
    assert result["status"] == "INDRA_QI_CHILD_FEEDBACK_PARENT_CYCLE_V0_10_READY", result
    parent_world = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
    handoff = read_json(root / "indra_qi_child_feedback_parent_cycle_handoff_v0_10.json")
    bridge_record = read_json(root / "indra_qi_child_feedback_parent_cycle_record_v0_10.json")
    bridge_ledger = latest(root / "indra_qi_child_feedback_parent_cycle_ledger_v0_10.jsonl")
    cycle = read_json(root / "indra_qi_process_tensor_cycle_state_v0_5.json")
    seed = read_json(root / "indra_qi_next_cycle_projection_seed_v0_5.json")
    return parent_world, handoff, bridge_record, bridge_ledger, cycle, seed


def build_plan(
    *,
    world: dict[str, Any],
    handoff: dict[str, Any],
    bridge_record: dict[str, Any],
    bridge_ledger: dict[str, Any],
    cycle: dict[str, Any],
    seed: dict[str, Any],
    suffix: str,
) -> dict[str, Any]:
    previous_dynamic = world.get("process_tensor_dynamic_world_state_digest") or "GENESIS"
    plan = {
        "version": "indra_qi_parent_cycle_assimilation_reentry_plan_v0_11",
        "loop_id": f"parent-cycle-assimilation-reentry-{suffix}",
        "source_v0_10_bridge_id": handoff["bridge_id"],
        "source_v0_10_handoff_packet_digest": handoff["handoff_packet_digest"],
        "source_v0_10_bridge_record_digest": bridge_record["bridge_record_digest"],
        "source_v0_10_ledger_record_digest": bridge_ledger["record_digest"],
        "source_parent_world_state_digest": world["indra_qi_world_state_digest"],
        "source_cycle_id": cycle["cycle_id"],
        "source_cycle_state_digest": cycle["process_tensor_cycle_state_digest"],
        "source_cycle_seed_packet_digest": seed["next_cycle_seed_packet_digest"],
        "assimilation_id": f"parent-cycle-world-assimilation-{suffix}",
        "expected_previous_dynamic_world_state_digest": previous_dynamic,
        "reentry_id": f"parent-cycle-causal-reentry-{suffix}",
        "projection_id": f"parent-cycle-causal-projection-{suffix}",
        "causal_world_id": f"parent-cycle-causal-world-{suffix}",
        "transaction_id": f"parent-cycle-causal-init-{suffix}",
        "derived_response_patch_id": "world-b",
        "derived_response_observable_id": f"world-b-parent-cycle-adaptive-response-{suffix}",
        "loop_mode": "parent_cycle_assimilation_then_causal_reentry",
        "assimilation_policy": {
            "world_memory_retention": 0.70,
            "world_residue_retention": 0.70,
            "world_nonmarkov_retention": 0.70,
            "world_recoverability_retention": 0.70,
            "world_debt_retention": 0.75,
            "tension_debt_gain": 0.45,
            "tension_residue_gain": 0.35,
            "tension_recovery_loss_gain": 0.20,
            "transport_resistance_gain": 0.65,
            "holonomy_residue_gain": 0.60,
            "seed_source_retention": 0.60,
            "min_post_assimilation_seed_weight": 0.35,
            "max_recoverability_branches": 8,
        },
        "projection_policy": {
            "minimum_seed_count": 2,
            "max_projection_variables": 16,
            "debt_uncertainty_gain": 0.65,
            "residue_uncertainty_gain": 0.35,
            "minimum_uncertainty": 0.01,
            "maximum_uncertainty": 0.95,
            "mechanism_weight_floor": 0.10,
            "mechanism_weight_ceiling": 0.95,
            "mechanism_noise_debt_gain": 0.50,
            "mechanism_bias": 0.05,
        },
        "boundary": dict(REQUIRED_BOUNDARY),
    }
    plan["loop_plan_digest"] = loop_plan_digest(plan)
    return plan


def assimilation_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_LICENSE_READY",
        "world_state_read_allowed": True,
        "cycle_state_read_allowed": True,
        "source_seed_read_allowed": True,
        "cycle_ledger_read_allowed": True,
        "assimilation_plan_validate_allowed": True,
        "rollback_snapshot_write_allowed": True,
        "dynamic_world_state_write_allowed": True,
        "world_state_write_allowed": True,
        "post_write_verification_allowed": True,
        "post_assimilation_seed_write_allowed": True,
        "assimilation_record_write_allowed": True,
        "assimilation_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_mutation_scopes": ["process_tensor_dynamic_world_state_only"],
        "allowed_dynamic_world_fields": [*DYNAMIC_WORLD_FIELDS, "process_tensor_world_state"],
    }
    value.update(overrides)
    return value


def v14_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "state_read_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_command_kinds": ["initialize"],
        "initialize_allowed": True,
        "state_write_allowed": True,
        "direct_world_model_mutation_allowed": True,
        "allowed_variables": [],
        "protected_variables": [],
        "max_variables": 16,
        "max_mechanisms": 16,
    }
    value.update(overrides)
    return value


def projection_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_LICENSE_READY",
        "indra_qi_world_state_read_allowed": True,
        "projection_plan_validate_allowed": True,
        "projection_packet_write_allowed": True,
        "activation_record_write_allowed": True,
        "projection_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v14_initialize_invoke_allowed": True,
        "v14_initialize_license_template": v14_template(),
    }
    value.update(overrides)
    return value


def reentry_template(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_LICENSE_READY",
        "world_state_read_allowed": True,
        "assimilation_record_read_allowed": True,
        "post_assimilation_seed_read_allowed": True,
        "assimilation_ledger_read_allowed": True,
        "reentry_plan_validate_allowed": True,
        "child_runtime_create_allowed": True,
        "child_world_state_copy_allowed": True,
        "generated_projection_plan_write_allowed": True,
        "v0_2_projection_invoke_allowed": True,
        "reentry_record_write_allowed": True,
        "reentry_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v0_2_projection_license_template": projection_template(),
    }
    value.update(overrides)
    return value


def loop_license(plan: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_PARENT_CYCLE_ASSIMILATION_REENTRY_V0_11_LICENSE_READY",
        "bound_loop_plan_digest": plan["loop_plan_digest"],
        "source_v0_10_read_allowed": True,
        "parent_world_read_allowed": True,
        "cycle_state_read_allowed": True,
        "transaction_snapshot_allowed": True,
        "transaction_restore_allowed": True,
        "child_runtime_remove_on_failure_allowed": True,
        "v0_6_assimilation_invoke_allowed": True,
        "v0_7_reentry_invoke_allowed": True,
        "loop_handoff_write_allowed": True,
        "loop_record_write_allowed": True,
        "loop_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v0_6_assimilation_license_template": assimilation_template(),
        "v0_7_reentry_license_template": reentry_template(),
    }
    value.update(overrides)
    return value


def run_loop(
    root: pathlib.Path,
    plan: dict[str, Any],
    license_value: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return build_indra_qi_parent_cycle_assimilation_reentry_v0_11(
        runtime_context={
            "runtime_root": str(root),
            "indra_qi_parent_cycle_assimilation_reentry_v0_11_enabled": True,
            "apply_indra_qi_parent_cycle_assimilation_reentry_v0_11": True,
        },
        loop_plan=plan,
        loop_license=license_value or loop_license(plan),
    ).to_dict()
