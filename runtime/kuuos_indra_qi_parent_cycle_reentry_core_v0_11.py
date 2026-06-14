#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from runtime.kuuos_indra_qi_post_assimilation_reentry_core_v0_7 import (
    REQUIRED_BOUNDARY as REENTRY_BOUNDARY,
    reentry_plan_digest,
)
from runtime.kuuos_indra_qi_world_assimilation_core_v0_6 import (
    DYNAMIC_WORLD_FIELDS,
    REQUIRED_BOUNDARY as ASSIMILATION_BOUNDARY,
    assimilation_plan_digest,
)

PLAN_VERSION = "indra_qi_parent_cycle_assimilation_reentry_plan_v0_11"
REQUIRED_BOUNDARY = {
    "source_v0_10_handoff_required": True,
    "source_cycle_and_seed_digest_exact": True,
    "parent_world_mutation_only_via_v0_6": True,
    "child_runtime_creation_only_via_v0_7": True,
    "v0_6_assimilation_license_required": True,
    "v0_7_reentry_license_required": True,
    "v0_6_and_v0_7_transaction_compensated": True,
    "existing_dynamic_world_history_preserved": True,
    "runtime_observation_overlay_history_preserved": True,
    "parent_protected_constitution_preserved": True,
    "child_runtime_internal_only": True,
    "new_child_runtime_required": True,
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


def loop_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "loop_plan_digest"))


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("parent_cycle_reentry_plan_version_invalid")
    if str(plan.get("loop_plan_digest", "")) != loop_plan_digest(plan):
        blockers.append("parent_cycle_reentry_plan_digest_invalid")
    for field in (
        "loop_id",
        "source_v0_10_bridge_id",
        "source_v0_10_handoff_packet_digest",
        "source_v0_10_bridge_record_digest",
        "source_v0_10_ledger_record_digest",
        "source_parent_world_state_digest",
        "source_cycle_id",
        "source_cycle_state_digest",
        "source_cycle_seed_packet_digest",
        "assimilation_id",
        "expected_previous_dynamic_world_state_digest",
        "reentry_id",
        "projection_id",
        "causal_world_id",
        "transaction_id",
        "derived_response_patch_id",
        "derived_response_observable_id",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"parent_cycle_reentry_plan_{field}_missing")
    if plan.get("loop_mode") != "parent_cycle_assimilation_then_causal_reentry":
        blockers.append("parent_cycle_reentry_loop_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"parent_cycle_reentry_boundary_{field}_mismatch")

    assimilation = mapping(plan.get("assimilation_policy"))
    for field in (
        "world_memory_retention",
        "world_residue_retention",
        "world_nonmarkov_retention",
        "world_recoverability_retention",
        "world_debt_retention",
        "tension_debt_gain",
        "tension_residue_gain",
        "tension_recovery_loss_gain",
        "transport_resistance_gain",
        "holonomy_residue_gain",
        "seed_source_retention",
        "min_post_assimilation_seed_weight",
    ):
        raw = assimilation.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"parent_cycle_reentry_assimilation_policy_{field}_invalid")
    maximum = assimilation.get("max_recoverability_branches")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum <= 0:
        blockers.append("parent_cycle_reentry_assimilation_policy_max_recoverability_branches_invalid")

    projection = mapping(plan.get("projection_policy"))
    for field in (
        "debt_uncertainty_gain",
        "residue_uncertainty_gain",
        "minimum_uncertainty",
        "maximum_uncertainty",
        "mechanism_weight_floor",
        "mechanism_weight_ceiling",
        "mechanism_noise_debt_gain",
        "mechanism_bias",
    ):
        raw = projection.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"parent_cycle_reentry_projection_policy_{field}_invalid")
    for field in ("minimum_seed_count", "max_projection_variables"):
        raw = projection.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"parent_cycle_reentry_projection_policy_{field}_invalid")
    minimum = projection.get("minimum_uncertainty")
    maximum_uncertainty = projection.get("maximum_uncertainty")
    if isinstance(minimum, (int, float)) and isinstance(maximum_uncertainty, (int, float)):
        if float(minimum) > float(maximum_uncertainty):
            blockers.append("parent_cycle_reentry_projection_uncertainty_range_invalid")
    floor = projection.get("mechanism_weight_floor")
    ceiling = projection.get("mechanism_weight_ceiling")
    if isinstance(floor, (int, float)) and isinstance(ceiling, (int, float)):
        if float(floor) > float(ceiling):
            blockers.append("parent_cycle_reentry_projection_mechanism_weight_range_invalid")


def build_assimilation_plan(
    *,
    plan: Mapping[str, Any],
    cycle_state: Mapping[str, Any],
    seed_packet: Mapping[str, Any],
    parent_world_digest: str,
    previous_dynamic_digest: str,
) -> dict[str, Any]:
    value = {
        "version": "indra_qi_process_tensor_world_assimilation_plan_v0_6",
        "assimilation_id": str(plan.get("assimilation_id", "")),
        "source_cycle_id": str(cycle_state.get("cycle_id", "")),
        "source_cycle_state_digest": str(cycle_state.get("process_tensor_cycle_state_digest", "")),
        "source_seed_packet_digest": str(seed_packet.get("next_cycle_seed_packet_digest", "")),
        "source_world_state_digest": parent_world_digest,
        "expected_previous_dynamic_world_state_digest": previous_dynamic_digest,
        "assimilation_mode": "debt_recovery_transport_world_update",
        "mutation_scope": "process_tensor_dynamic_world_state_only",
        "rollback_required": True,
        "assimilation_policy": dict(mapping(plan.get("assimilation_policy"))),
        "boundary": dict(ASSIMILATION_BOUNDARY),
    }
    value["assimilation_plan_digest"] = assimilation_plan_digest(value)
    return value


def build_reentry_plan(
    *,
    plan: Mapping[str, Any],
    assimilation_record: Mapping[str, Any],
    post_assimilation_seed: Mapping[str, Any],
    parent_world_digest: str,
) -> dict[str, Any]:
    value = {
        "version": "indra_qi_post_assimilation_causal_reentry_plan_v0_7",
        "reentry_id": str(plan.get("reentry_id", "")),
        "source_assimilation_id": str(assimilation_record.get("assimilation_id", "")),
        "source_assimilation_record_digest": str(
            assimilation_record.get("assimilation_record_digest", "")
        ),
        "source_post_assimilation_seed_packet_digest": str(
            post_assimilation_seed.get("post_assimilation_seed_packet_digest", "")
        ),
        "source_world_state_digest": parent_world_digest,
        "projection_id": str(plan.get("projection_id", "")),
        "causal_world_id": str(plan.get("causal_world_id", "")),
        "transaction_id": str(plan.get("transaction_id", "")),
        "derived_response_patch_id": str(plan.get("derived_response_patch_id", "")),
        "derived_response_observable_id": str(
            plan.get("derived_response_observable_id", "")
        ),
        "reentry_mode": "new_world_digest_causal_projection",
        "projection_policy": dict(mapping(plan.get("projection_policy"))),
        "boundary": dict(REENTRY_BOUNDARY),
    }
    value["reentry_plan_digest"] = reentry_plan_digest(value)
    return value


def validate_assimilation_license_template(
    template: Mapping[str, Any], blockers: list[str]
) -> None:
    if template.get("license_status") != "INDRA_QI_PROCESS_TENSOR_WORLD_ASSIMILATION_V0_6_LICENSE_READY":
        blockers.append("parent_cycle_reentry_nested_v0_6_license_not_ready")
    for flag in (
        "world_state_read_allowed",
        "cycle_state_read_allowed",
        "source_seed_read_allowed",
        "cycle_ledger_read_allowed",
        "assimilation_plan_validate_allowed",
        "rollback_snapshot_write_allowed",
        "dynamic_world_state_write_allowed",
        "world_state_write_allowed",
        "post_write_verification_allowed",
        "post_assimilation_seed_write_allowed",
        "assimilation_record_write_allowed",
        "assimilation_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "direct_world_model_mutation_allowed",
    ):
        if template.get(flag) is not True:
            blockers.append(f"parent_cycle_reentry_nested_v0_6_{flag}_not_true")
    scopes = template.get("allowed_mutation_scopes", [])
    scope_set = {str(value) for value in scopes} if isinstance(scopes, list) else set()
    if scope_set != {"process_tensor_dynamic_world_state_only"}:
        blockers.append("parent_cycle_reentry_nested_v0_6_mutation_scope_not_exact")
    fields = template.get("allowed_dynamic_world_fields", [])
    field_set = {str(value) for value in fields} if isinstance(fields, list) else set()
    expected = set(DYNAMIC_WORLD_FIELDS) | {"process_tensor_world_state"}
    if field_set != expected:
        blockers.append("parent_cycle_reentry_nested_v0_6_dynamic_fields_not_exact")


def validate_reentry_license_template(
    template: Mapping[str, Any], projection_limit: int, blockers: list[str]
) -> None:
    if template.get("license_status") != "INDRA_QI_POST_ASSIMILATION_CAUSAL_REENTRY_V0_7_LICENSE_READY":
        blockers.append("parent_cycle_reentry_nested_v0_7_license_not_ready")
    for flag in (
        "world_state_read_allowed",
        "assimilation_record_read_allowed",
        "post_assimilation_seed_read_allowed",
        "assimilation_ledger_read_allowed",
        "reentry_plan_validate_allowed",
        "child_runtime_create_allowed",
        "child_world_state_copy_allowed",
        "generated_projection_plan_write_allowed",
        "v0_2_projection_invoke_allowed",
        "reentry_record_write_allowed",
        "reentry_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if template.get(flag) is not True:
            blockers.append(f"parent_cycle_reentry_nested_v0_7_{flag}_not_true")
    projection = mapping(template.get("v0_2_projection_license_template"))
    if projection.get("license_status") != "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_LICENSE_READY":
        blockers.append("parent_cycle_reentry_nested_v0_2_license_not_ready")
    for flag in (
        "indra_qi_world_state_read_allowed",
        "projection_plan_validate_allowed",
        "projection_packet_write_allowed",
        "activation_record_write_allowed",
        "projection_ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
        "v14_initialize_invoke_allowed",
    ):
        if projection.get(flag) is not True:
            blockers.append(f"parent_cycle_reentry_nested_v0_2_{flag}_not_true")
    v14 = mapping(projection.get("v14_initialize_license_template"))
    if v14.get("license_status") != "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY":
        blockers.append("parent_cycle_reentry_nested_v14_license_not_ready")
    for flag in (
        "state_read_allowed",
        "event_ledger_append_allowed",
        "result_write_allowed",
        "audit_append_allowed",
        "initialize_allowed",
        "state_write_allowed",
        "direct_world_model_mutation_allowed",
    ):
        if v14.get(flag) is not True:
            blockers.append(f"parent_cycle_reentry_nested_v14_{flag}_not_true")
    kinds = v14.get("allowed_command_kinds", [])
    kind_set = {str(value) for value in kinds} if isinstance(kinds, list) else set()
    if kind_set != {"initialize"}:
        blockers.append("parent_cycle_reentry_nested_v14_command_kinds_not_exact")
    for field in ("max_variables", "max_mechanisms"):
        raw = v14.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < projection_limit:
            blockers.append(f"parent_cycle_reentry_nested_v14_{field}_insufficient")
