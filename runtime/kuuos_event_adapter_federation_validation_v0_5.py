#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import ROOT_VERSION
from runtime.kuuos_event_adapter_federation_types_v0_5 import (
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    clamp,
    integer,
    mapping,
    valid_digest,
)


def validate_root(root_packet: Mapping[str, Any], blockers: list[str]) -> None:
    if root_packet.get("version") != ROOT_VERSION:
        blockers.append("root_principles_version_invalid")
    if not valid_digest(root_packet, "root_principles_digest"):
        blockers.append("root_principles_digest_invalid")
    if root_packet.get("protected") is not True:
        blockers.append("root_principles_not_protected")
    if root_packet.get("self_rewrite_allowed") is not False:
        blockers.append("root_principles_self_rewrite_not_denied")


def validate_plan(
    plan: Mapping[str, Any],
    *,
    source_batch: str,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    previous_state: Mapping[str, Any],
    blockers: list[str],
) -> tuple[int, int, int]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("federation_plan_version_invalid")
    if not valid_digest(plan, "federation_plan_digest"):
        blockers.append("federation_plan_digest_invalid")
    for field in ("federation_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    bindings = {
        "expected_source_batch_digest": source_batch,
        "expected_root_principles_digest": root_packet.get("root_principles_digest"),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest"),
        "expected_previous_federation_state_digest": previous_state.get(
            "federation_state_digest", ""
        ),
    }
    for field, expected in bindings.items():
        if plan.get(field, "") != expected:
            blockers.append(f"{field}_mismatch")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")

    max_sources = integer(plan.get("max_sources_per_cycle"), 0)
    max_signals_per_source = integer(plan.get("max_signals_per_source"), 0)
    max_total_signals = integer(plan.get("max_total_signals"), 0)
    if not 1 <= max_sources <= 32:
        blockers.append("max_sources_per_cycle_invalid")
    if not 1 <= max_signals_per_source <= 64:
        blockers.append("max_signals_per_source_invalid")
    if not 1 <= max_total_signals <= 256:
        blockers.append("max_total_signals_invalid")
    if max_total_signals < max_signals_per_source:
        blockers.append("total_signal_limit_below_per_source_limit")

    max_generated = integer(plan.get("max_generated_goals"), 0)
    max_selected = integer(plan.get("max_selected_goals"), 0)
    renewal_window = integer(plan.get("renewal_window_steps"), 0)
    max_sections = integer(plan.get("max_bundle_sections"), 0)
    max_new = integer(plan.get("max_new_sections_per_run"), 0)
    max_transports = integer(plan.get("max_transports_per_section"), 0)
    min_goal = clamp(plan.get("min_goal_score"), -1.0)
    min_scale = clamp(plan.get("min_action_scale"), -1.0)
    if not 1 <= max_generated <= 32:
        blockers.append("max_generated_goals_invalid")
    if not 1 <= max_selected <= min(max_generated, 8):
        blockers.append("max_selected_goals_invalid")
    if not 1 <= renewal_window <= 1000:
        blockers.append("renewal_window_steps_invalid")
    if not 2 <= max_sections <= 4096:
        blockers.append("max_bundle_sections_invalid")
    if not 1 <= max_new <= 32:
        blockers.append("max_new_sections_per_run_invalid")
    if not 1 <= max_transports <= 20:
        blockers.append("max_transports_per_section_invalid")
    if min_goal < 0.0:
        blockers.append("min_goal_score_invalid")
    if min_scale < 0.0 or min_scale > 0.25:
        blockers.append("min_action_scale_invalid")
    return max_sources, max_signals_per_source, max_total_signals


def validate_license(
    license_packet: Mapping[str, Any],
    *,
    plan: Mapping[str, Any],
    source_batch: str,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("federation_license_version_invalid")
    bindings = {
        "bound_plan_digest": plan.get("federation_plan_digest"),
        "bound_source_batch_digest": source_batch,
        "bound_root_principles_digest": root_packet.get("root_principles_digest"),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest"),
    }
    for field, expected in bindings.items():
        if license_packet.get(field) != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "source_normalization_allowed",
        "adapter_selection_allowed",
        "supervisor_cycle_allowed",
        "effect_evidence_write_allowed",
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
