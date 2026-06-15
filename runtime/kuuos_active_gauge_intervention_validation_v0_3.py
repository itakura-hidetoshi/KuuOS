#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    ACTION_VERSION as GAUGE_ACTION_VERSION,
    BUNDLE_VERSION as GAUGE_BUNDLE_VERSION,
    STATE_VERSION as GAUGE_STATE_VERSION,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    ADAPTER_PROFILE_VERSION,
    DEFAULT_ROUTING,
    LICENSE_VERSION,
    LOCAL_ACTIONS,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    as_list,
    clamp,
    contains_graph_keys,
    integer,
    mapping,
    valid_digest,
)


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> tuple[int, int, int, float]:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("intervention_plan_version_invalid")
    if not valid_digest(plan, "intervention_plan_digest"):
        blockers.append("intervention_plan_digest_invalid")
    for field in ("intervention_run_id", "gauge_reentry_run_id", "agent_id", "adapter_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    if plan.get("auto_reenter_gauge") is not True:
        blockers.append("auto_reenter_gauge_not_true")
    max_sections = integer(plan.get("reentry_max_bundle_sections"), 256)
    max_new = integer(plan.get("reentry_max_new_sections_per_run"), 8)
    max_transports = integer(plan.get("reentry_max_transports_per_section"), 4)
    min_scale = clamp(plan.get("reentry_min_action_scale"), -1.0)
    if not 2 <= max_sections <= 4096:
        blockers.append("reentry_max_bundle_sections_invalid")
    if not 1 <= max_new <= 32:
        blockers.append("reentry_max_new_sections_per_run_invalid")
    if not 1 <= max_transports <= 20:
        blockers.append("reentry_max_transports_per_section_invalid")
    if min_scale < 0.0 or min_scale > 0.25:
        blockers.append("reentry_min_action_scale_invalid")
    return max_sections, max_new, max_transports, min_scale


def validate_profile(profile: Mapping[str, Any], plan: Mapping[str, Any], blockers: list[str]) -> None:
    if profile.get("version") != ADAPTER_PROFILE_VERSION:
        blockers.append("adapter_profile_version_invalid")
    if not valid_digest(profile, "adapter_profile_digest"):
        blockers.append("adapter_profile_digest_invalid")
    if profile.get("adapter_id") != plan.get("adapter_id"):
        blockers.append("adapter_profile_id_mismatch")
    if profile.get("backend") != "qi_local_execution_adapter_v0_2":
        blockers.append("adapter_backend_unsupported")
    supported = {str(item) for item in as_list(profile.get("supported_domain_actions"))}
    if not supported or not supported.issubset(LOCAL_ACTIONS):
        blockers.append("adapter_supported_domain_actions_invalid")
    if profile.get("result_to_curvature_mapping") != "deterministic_local_effect_v0_3":
        blockers.append("adapter_effect_mapping_invalid")


def validate_upstream(
    gauge_state: Mapping[str, Any],
    bundle: Mapping[str, Any],
    action: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if gauge_state.get("version") != GAUGE_STATE_VERSION or not valid_digest(gauge_state, "gauge_state_digest"):
        blockers.append("source_gauge_state_invalid")
    if bundle.get("version") != GAUGE_BUNDLE_VERSION or not valid_digest(bundle, "gauge_bundle_digest"):
        blockers.append("source_gauge_bundle_invalid")
    if action.get("version") != GAUGE_ACTION_VERSION or not valid_digest(action, "covariant_action_digest"):
        blockers.append("source_covariant_action_invalid")
    if action.get("action_ready") is not True:
        blockers.append("source_covariant_action_not_ready")
    if contains_graph_keys(bundle) or contains_graph_keys(action):
        blockers.append("graph_semantics_present")
    for field, expected in {
        "expected_gauge_state_digest": gauge_state.get("gauge_state_digest"),
        "expected_gauge_bundle_digest": bundle.get("gauge_bundle_digest"),
        "expected_covariant_action_digest": action.get("covariant_action_digest"),
    }.items():
        if plan.get(field) != expected:
            blockers.append(f"{field}_mismatch")
    if gauge_state.get("gauge_bundle_digest") != bundle.get("gauge_bundle_digest"):
        blockers.append("gauge_state_bundle_digest_mismatch")
    if gauge_state.get("covariant_action_digest") != action.get("covariant_action_digest"):
        blockers.append("gauge_state_action_digest_mismatch")
    # An outstanding action is deliberately byte-stable while unrelated Telos
    # sections extend the bundle. Therefore its source_bundle_digest may name the
    # earlier dispatch bundle. Exact authority is carried by the action digest plus
    # the current bundle's active action and section bindings below.
    if bundle.get("active_action_id") != action.get("action_id"):
        blockers.append("bundle_active_action_id_mismatch")
    if bundle.get("active_section_id") != action.get("section_id"):
        blockers.append("bundle_active_section_id_mismatch")
    agent = plan.get("agent_id")
    if gauge_state.get("agent_id") != agent or bundle.get("agent_id") != agent:
        blockers.append("agent_binding_mismatch")


def validate_license(
    license_packet: Mapping[str, Any],
    plan: Mapping[str, Any],
    profile: Mapping[str, Any],
    gauge_state: Mapping[str, Any],
    bundle: Mapping[str, Any],
    action: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("intervention_license_version_invalid")
    for field, expected in {
        "bound_plan_digest": plan.get("intervention_plan_digest"),
        "bound_adapter_profile_digest": profile.get("adapter_profile_digest"),
        "bound_gauge_state_digest": gauge_state.get("gauge_state_digest"),
        "bound_gauge_bundle_digest": bundle.get("gauge_bundle_digest"),
        "bound_covariant_action_digest": action.get("covariant_action_digest"),
    }.items():
        if license_packet.get(field) != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "route_action_allowed", "domain_intervention_allowed", "local_adapter_execution_allowed",
        "effect_receipt_write_allowed", "gauge_reentry_allowed", "next_action_continue_allowed",
        "state_write_allowed", "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))


def route_action(
    action: Mapping[str, Any],
    plan: Mapping[str, Any],
    profile: Mapping[str, Any],
    context: Mapping[str, Any],
    blockers: list[str],
) -> str:
    routing = dict(DEFAULT_ROUTING)
    routing.update({str(k): str(v) for k, v in mapping(plan.get("routing_table")).items()})
    routed = routing.get(str(action.get("covariant_step_kind", "")), "")
    if routed not in LOCAL_ACTIONS:
        blockers.append("covariant_step_route_missing_or_invalid")
        return ""
    if routed not in {str(item) for item in as_list(profile.get("supported_domain_actions"))}:
        blockers.append("routed_action_not_supported_by_adapter")
    if routed not in {str(item) for item in as_list(context.get("allowed_domain_actions"))}:
        blockers.append("routed_action_not_allowed_in_runtime_context")
    return routed
