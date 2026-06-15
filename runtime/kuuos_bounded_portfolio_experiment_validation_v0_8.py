#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_adapter_capability_bundle_validation_v0_6 import (
    validate_bundle as validate_capability_bundle,
    validate_root,
)
from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    STATE_VERSION as CAPABILITY_STATE_VERSION,
)
from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    BUNDLE_VERSION as PORTFOLIO_BUNDLE_VERSION,
)
from runtime.kuuos_adapter_portfolio_shadow_validation_v0_7 import (
    validate_bundle as validate_portfolio_bundle,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_bounded_portfolio_experiment_model_v0_8 import portfolio_view
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    BUNDLE_VERSION,
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    as_list,
    clamp,
    integer,
    mapping,
    nonnegative,
    valid_digest,
)


def validate_bundle(
    bundle: Mapping[str, Any], agent_id: str, source_portfolio_digest: str, blockers: list[str]
) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("experiment_bundle_version_invalid")
        return
    if not valid_digest(bundle, "experiment_bundle_digest"):
        blockers.append("experiment_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("experiment_bundle_agent_mismatch")
    if bundle.get("source_portfolio_bundle_digest") != source_portfolio_digest:
        blockers.append("experiment_bundle_source_portfolio_digest_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("experiment_bundle_generation_invalid")
    view = portfolio_view(bundle)
    if bundle.get("working_portfolio_bundle_digest") != view.get("portfolio_bundle_digest"):
        blockers.append("working_portfolio_bundle_digest_invalid")
    trial_keys: set[tuple[str, str]] = set()
    for raw in as_list(bundle.get("trial_stats")):
        stat = mapping(raw)
        key = (
            str(stat.get("federation_adapter_id", "")),
            str(stat.get("context_key", "")),
        )
        if not all(key) or key in trial_keys:
            blockers.append("experiment_trial_stat_key_missing_or_repeated")
        trial_keys.add(key)
        if integer(stat.get("trial_count"), -1) < 0:
            blockers.append("experiment_trial_stat_count_invalid")
        if nonnegative(stat.get("cumulative_trial_cost"), -1.0) < 0.0:
            blockers.append("experiment_trial_stat_cost_invalid")
        if clamp(stat.get("mean_trial_utility"), -1.0) < 0.0:
            blockers.append("experiment_trial_stat_utility_invalid")
    processed = [
        str(item) for item in as_list(bundle.get("processed_experiment_effect_digests"))
    ]
    if len(processed) != len(set(processed)):
        blockers.append("processed_experiment_effect_digest_repeated")
    if integer(bundle.get("total_trial_count"), -1) < 0:
        blockers.append("experiment_total_trial_count_invalid")
    if integer(bundle.get("total_exploit_count"), -1) < 0:
        blockers.append("experiment_total_exploit_count_invalid")
    if nonnegative(bundle.get("trial_budget_spent"), -1.0) < 0.0:
        blockers.append("experiment_trial_budget_spent_invalid")


def validate_inputs(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    capability_state: Mapping[str, Any],
    capability_bundle: Mapping[str, Any],
    source_portfolio_bundle: Mapping[str, Any],
    experiment_state: Mapping[str, Any],
    experiment_bundle: Mapping[str, Any],
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
    validate_portfolio_bundle(
        source_portfolio_bundle, str(plan.get("agent_id", "")), blockers
    )
    validate_bundle(
        experiment_bundle,
        str(plan.get("agent_id", "")),
        str(source_portfolio_bundle.get("portfolio_bundle_digest", "")),
        blockers,
    )
    if capability_state and (
        capability_state.get("version") != CAPABILITY_STATE_VERSION
        or not valid_digest(capability_state, "capability_state_digest")
    ):
        blockers.append("previous_capability_state_invalid")
    if experiment_state and (
        experiment_state.get("version") != STATE_VERSION
        or not valid_digest(experiment_state, "experiment_state_digest")
    ):
        blockers.append("previous_experiment_state_invalid")

    if plan.get("version") != PLAN_VERSION:
        blockers.append("experiment_plan_version_invalid")
    if not valid_digest(plan, "experiment_plan_digest"):
        blockers.append("experiment_plan_digest_invalid")
    for field in ("experiment_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"experiment_plan_{field}_missing")
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
        "expected_source_portfolio_bundle_digest": source_portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
        "expected_previous_experiment_state_digest": experiment_state.get(
            "experiment_state_digest", ""
        ),
        "expected_previous_experiment_bundle_digest": experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"experiment_plan_{field}_mismatch")
    for field, expected_value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected_value:
            blockers.append(f"experiment_boundary_{field}_invalid")

    integer_bounds = (
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
        ("max_trial_records", 1, 4096),
        ("max_decision_holonomy", 1, 4096),
        ("max_live_trials_total", 0, 100000),
        ("max_live_trials_per_adapter_context", 0, 1000),
        ("trial_cooldown_cycles", 0, 100000),
    )
    for field, lower, upper in integer_bounds:
        value = integer(plan.get(field), -1)
        if not lower <= value <= upper:
            blockers.append(f"experiment_plan_{field}_invalid")

    bounded_fields = (
        ("learning_rate", 0.01, 1.0),
        ("exploration_weight", 0.0, 0.5),
        ("max_exploration_bonus", 0.0, 0.5),
        ("curvature_penalty", 0.0, 1.0),
        ("resolved_evidence_weight", 0.0, 1.0),
        ("max_portfolio_adjustment", 0.0, 0.25),
        ("shadow_model_weight", 0.0, 1.0),
        ("shadow_learning_rate", 0.01, 1.0),
        ("default_prediction_confidence", 0.0, 1.0),
        ("uncertainty_weight", 0.0, 1.0),
        ("unresolved_shadow_weight", 0.0, 1.0),
        ("trial_novelty_weight", 0.0, 1.0),
        ("opportunity_cost_weight", 0.0, 1.0),
        ("minimum_information_gain", 0.0, 1.0),
        ("maximum_trial_risk", 0.0, 1.0),
        ("minimum_trial_recoverability", 0.0, 1.0),
        ("default_trial_risk", 0.0, 1.0),
        ("default_trial_recoverability", 0.0, 1.0),
    )
    for field, lower, upper in bounded_fields:
        value = clamp(plan.get(field), -1.0)
        if not lower <= value <= upper:
            blockers.append(f"experiment_plan_{field}_invalid")

    nonnegative_fields = (
        "total_trial_budget",
        "maximum_trial_cost",
        "default_trial_cost",
        "reliability_prior_mass",
    )
    for field in nonnegative_fields:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or float(raw) < 0.0:
            blockers.append(f"experiment_plan_{field}_invalid")
    if nonnegative(plan.get("maximum_trial_cost")) > nonnegative(plan.get("total_trial_budget")):
        blockers.append("experiment_maximum_trial_cost_exceeds_total_budget")
    if nonnegative(plan.get("default_trial_cost")) > nonnegative(plan.get("maximum_trial_cost")):
        blockers.append("experiment_default_trial_cost_exceeds_maximum")
    if nonnegative(experiment_bundle.get("trial_budget_spent")) > nonnegative(
        plan.get("total_trial_budget")
    ):
        blockers.append("experiment_existing_budget_spent_exceeds_plan")
    for action, value in mapping(plan.get("shadow_action_utility")).items():
        if not str(action) or clamp(value, -1.0) < 0.0:
            blockers.append("experiment_shadow_action_utility_invalid")
    if not mapping(plan.get("shadow_action_utility")):
        blockers.append("experiment_shadow_action_utility_missing")

    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("experiment_license_version_invalid")
    license_expected = {
        "bound_experiment_plan_digest": plan.get("experiment_plan_digest", ""),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "bound_previous_capability_bundle_digest": capability_bundle.get(
            "capability_bundle_digest", ""
        ),
        "bound_source_portfolio_bundle_digest": source_portfolio_bundle.get(
            "portfolio_bundle_digest", ""
        ),
        "bound_previous_experiment_bundle_digest": experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"experiment_license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "capability_state_read_allowed",
        "capability_bundle_read_allowed",
        "portfolio_seed_read_allowed",
        "experiment_bundle_read_allowed",
        "information_gain_estimation_allowed",
        "experiment_decision_allowed",
        "licensed_live_trial_allowed",
        "baseline_exploitation_allowed",
        "one_live_capability_cycle_allowed",
        "shadow_projection_allowed",
        "shadow_resolution_allowed",
        "trial_budget_debit_allowed",
        "experiment_bundle_write_allowed",
        "experiment_state_write_allowed",
        "decision_write_allowed",
        "selection_write_allowed",
        "projection_write_allowed",
        "resolution_write_allowed",
        "trial_record_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "multiple_live_adapters_allowed",
        "unbudgeted_trial_allowed",
        "shadow_execution_allowed",
        "shadow_external_actuation_allowed",
        "shadow_world_update_allowed",
        "shadow_capability_connection_update_allowed",
        "source_authority_transfer_allowed",
        "adapter_authority_inheritance_allowed",
        "external_network_effect_allowed",
        "world_update_allowed",
        "memory_overwrite_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))
