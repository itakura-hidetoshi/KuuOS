#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_bundle_validation_v0_6 import (
    validate_bundle as validate_capability_bundle,
    validate_root,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import STATE_VERSION as CAPABILITY_STATE_VERSION
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    BUNDLE_VERSION,
    LICENSE_VERSION,
    PLAN_VERSION,
    PROJECTION_VERSION,
    REQUIRED_BOUNDARY,
    SECTION_VERSION,
    STATE_VERSION,
    as_list,
    clamp,
    integer,
    mapping,
    signed,
    valid_digest,
)


def validate_bundle(bundle: Mapping[str, Any], agent_id: str, blockers: list[str]) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("portfolio_bundle_version_invalid")
        return
    if not valid_digest(bundle, "portfolio_bundle_digest"):
        blockers.append("portfolio_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("portfolio_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("portfolio_bundle_generation_invalid")
    keys: set[tuple[str, str]] = set()
    for raw in as_list(bundle.get("sections")):
        section = mapping(raw)
        if section.get("version") != SECTION_VERSION:
            blockers.append("portfolio_section_version_invalid")
        if not valid_digest(section, "portfolio_section_digest"):
            blockers.append("portfolio_section_digest_invalid")
        key = (
            str(section.get("federation_adapter_id", "")),
            str(section.get("context_key", "")),
        )
        if not all(key) or key in keys:
            blockers.append("portfolio_section_key_missing_or_repeated")
        keys.add(key)
        if integer(section.get("resolved_shadow_count"), -1) < 0:
            blockers.append("portfolio_resolved_shadow_count_invalid")
        if integer(section.get("live_count"), -1) < 0:
            blockers.append("portfolio_live_count_invalid")
        if signed(section.get("shadow_bias"), 2.0) > 1.0:
            blockers.append("portfolio_shadow_bias_invalid")
        if clamp(section.get("reliability"), -1.0) < 0.0:
            blockers.append("portfolio_reliability_invalid")
    prediction_ids: set[str] = set()
    for raw in as_list(bundle.get("pending_predictions")):
        prediction = mapping(raw)
        if prediction.get("version") != PROJECTION_VERSION:
            blockers.append("pending_shadow_projection_version_invalid")
        if not valid_digest(prediction, "shadow_projection_digest"):
            blockers.append("pending_shadow_projection_digest_invalid")
        prediction_id = str(prediction.get("prediction_id", ""))
        if not prediction_id or prediction_id in prediction_ids:
            blockers.append("pending_shadow_prediction_id_missing_or_repeated")
        prediction_ids.add(prediction_id)
        if prediction.get("status") != "pending":
            blockers.append("pending_shadow_prediction_status_invalid")
        if prediction.get("shadow_non_actuating") is not True:
            blockers.append("pending_shadow_prediction_not_non_actuating")
        if prediction.get("shadow_prediction_not_truth") is not True:
            blockers.append("pending_shadow_prediction_truth_boundary_missing")
        if prediction.get("shadow_prediction_not_capability_evidence") is not True:
            blockers.append("pending_shadow_capability_boundary_missing")
    processed = [str(item) for item in as_list(bundle.get("processed_live_effect_digests"))]
    if len(processed) != len(set(processed)):
        blockers.append("processed_live_effect_digest_repeated")


def validate_inputs(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    capability_state: Mapping[str, Any],
    capability_bundle: Mapping[str, Any],
    portfolio_state: Mapping[str, Any],
    portfolio_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    source_batch_digest: str,
    blockers: list[str],
) -> None:
    validate_root(root_packet, blockers)
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    validate_capability_bundle(
        capability_bundle, str(plan.get("agent_id", "")), blockers
    )
    validate_bundle(portfolio_bundle, str(plan.get("agent_id", "")), blockers)
    if capability_state and (
        capability_state.get("version") != CAPABILITY_STATE_VERSION
        or not valid_digest(capability_state, "capability_state_digest")
    ):
        blockers.append("previous_capability_state_invalid")
    if portfolio_state and (
        portfolio_state.get("version") != STATE_VERSION
        or not valid_digest(portfolio_state, "portfolio_state_digest")
    ):
        blockers.append("previous_portfolio_state_invalid")

    if plan.get("version") != PLAN_VERSION:
        blockers.append("portfolio_plan_version_invalid")
    if not valid_digest(plan, "portfolio_plan_digest"):
        blockers.append("portfolio_plan_digest_invalid")
    for field in ("portfolio_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"portfolio_plan_{field}_missing")
    expected = {
        "expected_source_batch_digest": source_batch_digest,
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "expected_previous_capability_state_digest": capability_state.get(
            "capability_state_digest", ""
        ),
        "expected_previous_capability_bundle_digest": capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "expected_previous_portfolio_state_digest": portfolio_state.get(
            "portfolio_state_digest", ""
        ),
        "expected_previous_portfolio_bundle_digest": portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"portfolio_plan_{field}_mismatch")
    for field, value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not value:
            blockers.append(f"portfolio_boundary_{field}_invalid")

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
        ("max_shadow_candidates", 1, 32),
        ("max_pending_predictions", 1, 4096),
        ("max_resolved_predictions", 1, 4096),
        ("max_portfolio_holonomy", 1, 4096),
    ):
        value = integer(plan.get(field), 0)
        if not lower <= value <= upper:
            blockers.append(f"portfolio_plan_{field}_invalid")
    for field, lower, upper in (
        ("learning_rate", 0.01, 1.0),
        ("exploration_weight", 0.0, 0.5),
        ("max_exploration_bonus", 0.0, 0.5),
        ("curvature_penalty", 0.0, 1.0),
        ("resolved_evidence_weight", 0.0, 1.0),
        ("max_portfolio_adjustment", 0.0, 0.25),
        ("shadow_model_weight", 0.0, 1.0),
        ("shadow_learning_rate", 0.01, 1.0),
        ("default_prediction_confidence", 0.0, 1.0),
    ):
        value = clamp(plan.get(field), -1.0)
        if not lower <= value <= upper:
            blockers.append(f"portfolio_plan_{field}_invalid")
    prior_mass = plan.get("reliability_prior_mass")
    if isinstance(prior_mass, bool) or not isinstance(prior_mass, (int, float)) or not 0.1 <= float(prior_mass) <= 100.0:
        blockers.append("portfolio_plan_reliability_prior_mass_invalid")
    for action, value in mapping(plan.get("shadow_action_utility")).items():
        if not str(action) or clamp(value, -1.0) < 0.0:
            blockers.append("portfolio_shadow_action_utility_invalid")
    if not mapping(plan.get("shadow_action_utility")):
        blockers.append("portfolio_shadow_action_utility_missing")

    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("portfolio_license_version_invalid")
    license_expected = {
        "bound_portfolio_plan_digest": plan.get("portfolio_plan_digest", ""),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "bound_previous_capability_bundle_digest": capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "bound_previous_portfolio_bundle_digest": portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"portfolio_license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "capability_state_read_allowed",
        "capability_bundle_read_allowed",
        "portfolio_bundle_read_allowed",
        "portfolio_selection_allowed",
        "one_live_capability_cycle_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "portfolio_bundle_write_allowed",
        "portfolio_state_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "shadow_execution_allowed",
        "shadow_external_actuation_allowed",
        "shadow_world_update_allowed",
        "shadow_capability_connection_update_allowed",
        "source_authority_transfer_allowed",
        "adapter_authority_inheritance_allowed",
        "external_network_effect_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))
