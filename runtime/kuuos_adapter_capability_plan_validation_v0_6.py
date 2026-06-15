#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    clamp,
    integer,
    mapping,
    valid_digest,
)


def validate_plan(
    plan: Mapping[str, Any],
    *,
    source_batch_digest: str,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    previous_state: Mapping[str, Any],
    previous_bundle: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("capability_plan_version_invalid")
    if not valid_digest(plan, "capability_plan_digest"):
        blockers.append("capability_plan_digest_invalid")
    for field in ("capability_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    bindings = {
        "expected_source_batch_digest": source_batch_digest,
        "expected_root_principles_digest": root_packet.get("root_principles_digest"),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest"),
        "expected_previous_capability_state_digest": previous_state.get(
            "capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": previous_bundle.get(
            "capability_bundle_digest", ""
        ),
    }
    for field, expected in bindings.items():
        if plan.get(field, "") != expected:
            blockers.append(f"{field}_mismatch")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")

    learning_rate = clamp(plan.get("learning_rate"), -1.0)
    exploration_weight = clamp(plan.get("exploration_weight"), -1.0)
    max_bonus = clamp(plan.get("max_exploration_bonus"), -1.0)
    curvature_penalty = clamp(plan.get("curvature_penalty"), -1.0)
    if not 0.01 <= learning_rate <= 1.0:
        blockers.append("learning_rate_invalid")
    if not 0.0 <= exploration_weight <= 0.5:
        blockers.append("exploration_weight_invalid")
    if not 0.0 <= max_bonus <= 0.5:
        blockers.append("max_exploration_bonus_invalid")
    if not 0.0 <= curvature_penalty <= 1.0:
        blockers.append("curvature_penalty_invalid")

    for field, lower, upper in (
        ("max_sources_per_cycle", 1, 32),
        ("max_signals_per_source", 1, 64),
        ("max_total_signals", 1, 256),
        ("max_generated_goals", 1, 32),
        ("max_selected_goals", 1, 8),
        ("renewal_window_steps", 1, 1000),
        ("max_bundle_sections", 2, 4096),
        ("max_new_sections_per_run", 1, 32),
        ("max_transports_per_section", 1, 20),
    ):
        value = integer(plan.get(field), 0)
        if not lower <= value <= upper:
            blockers.append(f"{field}_invalid")
    if integer(plan.get("max_selected_goals"), 0) > integer(
        plan.get("max_generated_goals"), 0
    ):
        blockers.append("max_selected_goals_exceeds_generated")
    if integer(plan.get("max_total_signals"), 0) < integer(
        plan.get("max_signals_per_source"), 0
    ):
        blockers.append("max_total_signals_below_per_source")
    min_goal = clamp(plan.get("min_goal_score"), -1.0)
    min_scale = clamp(plan.get("min_action_scale"), -1.0)
    if min_goal < 0.0:
        blockers.append("min_goal_score_invalid")
    if min_scale < 0.0 or min_scale > 0.25:
        blockers.append("min_action_scale_invalid")


def validate_license(
    license_packet: Mapping[str, Any],
    *,
    plan: Mapping[str, Any],
    source_batch_digest: str,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    previous_bundle: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("capability_license_version_invalid")
    bindings = {
        "bound_plan_digest": plan.get("capability_plan_digest"),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_packet.get("root_principles_digest"),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest"),
        "bound_previous_capability_bundle_digest": previous_bundle.get(
            "capability_bundle_digest", ""
        ),
    }
    for field, expected in bindings.items():
        if license_packet.get(field) != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "capability_bundle_read_allowed",
        "capability_selection_allowed",
        "federation_cycle_allowed",
        "effect_receipt_read_allowed",
        "capability_calibration_allowed",
        "bundle_write_allowed",
        "selection_write_allowed",
        "calibration_write_allowed",
        "state_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    if license_packet.get("external_network_effect_allowed") is not False:
        blockers.append("external_network_effect_not_denied")
    if license_packet.get("source_authority_transfer_allowed") is not False:
        blockers.append("source_authority_transfer_not_denied")
    if license_packet.get("adapter_authority_inheritance_allowed") is not False:
        blockers.append("adapter_authority_inheritance_not_denied")
