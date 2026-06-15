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
from runtime.kuuos_adapter_portfolio_shadow_validation_v0_7 import (
    validate_bundle as validate_portfolio_bundle,
)
from runtime.kuuos_bounded_portfolio_experiment_validation_v0_8 import (
    validate_bundle as validate_experiment_bundle,
)
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    STATE_VERSION as EXPERIMENT_STATE_VERSION,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    BUNDLE_VERSION,
    LICENSE_VERSION,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    SECTION_VERSION,
    STATE_VERSION,
    as_list,
    clamp,
    integer,
    mapping,
    nonnegative,
    signed,
    valid_digest,
)


def validate_bundle(bundle: Mapping[str, Any], agent_id: str, blockers: list[str]) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("policy_bundle_version_invalid")
        return
    if not valid_digest(bundle, "policy_bundle_digest"):
        blockers.append("policy_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("policy_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("policy_bundle_generation_invalid")
    seen: set[str] = set()
    for raw in as_list(bundle.get("sections")):
        section = mapping(raw)
        context_key = str(section.get("context_key", ""))
        if section.get("version") != SECTION_VERSION:
            blockers.append("policy_section_version_invalid")
        if not valid_digest(section, "policy_section_digest"):
            blockers.append("policy_section_digest_invalid")
        if not context_key or context_key in seen:
            blockers.append("policy_section_context_missing_or_repeated")
        seen.add(context_key)
        for field in (
            "cycle_count",
            "experiment_count",
            "exploit_count",
            "reobserve_count",
            "compatible_resolution_count",
            "unresolved_after_live_count",
        ):
            if integer(section.get(field), -1) < 0:
                blockers.append(f"policy_section_{field}_invalid")
        if nonnegative(section.get("experiment_success_alpha"), -1.0) <= 0.0:
            blockers.append("policy_section_alpha_invalid")
        if nonnegative(section.get("experiment_success_beta"), -1.0) <= 0.0:
            blockers.append("policy_section_beta_invalid")
    processed = [
        str(item) for item in as_list(bundle.get("processed_child_effect_digests"))
    ]
    if len(processed) != len(set(processed)):
        blockers.append("policy_processed_effect_digest_repeated")


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
    policy_state: Mapping[str, Any],
    policy_bundle: Mapping[str, Any],
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
    agent_id = str(plan.get("agent_id", ""))
    validate_capability_bundle(capability_bundle, agent_id, blockers)
    validate_portfolio_bundle(source_portfolio_bundle, agent_id, blockers)
    validate_experiment_bundle(
        experiment_bundle,
        agent_id,
        str(source_portfolio_bundle.get("portfolio_bundle_digest", "")),
        blockers,
    )
    validate_bundle(policy_bundle, agent_id, blockers)
    if capability_state and (
        capability_state.get("version") != CAPABILITY_STATE_VERSION
        or not valid_digest(capability_state, "capability_state_digest")
    ):
        blockers.append("previous_capability_state_invalid")
    if experiment_state and (
        experiment_state.get("version") != EXPERIMENT_STATE_VERSION
        or not valid_digest(experiment_state, "experiment_state_digest")
    ):
        blockers.append("previous_experiment_state_invalid")
    if policy_state and (
        policy_state.get("version") != STATE_VERSION
        or not valid_digest(policy_state, "policy_state_digest")
    ):
        blockers.append("previous_policy_state_invalid")

    if plan.get("version") != PLAN_VERSION:
        blockers.append("policy_plan_version_invalid")
    if not valid_digest(plan, "policy_plan_digest"):
        blockers.append("policy_plan_digest_invalid")
    for field in ("policy_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"policy_plan_{field}_missing")
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
        "expected_previous_policy_state_digest": policy_state.get(
            "policy_state_digest", ""
        ),
        "expected_previous_policy_bundle_digest": policy_bundle.get(
            "policy_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"policy_plan_{field}_mismatch")
    for field, expected_value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected_value:
            blockers.append(f"policy_boundary_{field}_invalid")

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
        ("max_policy_outcomes", 1, 4096),
        ("max_policy_holonomy", 1, 4096),
        ("max_live_trials_total", 0, 100000),
        ("max_live_trials_per_adapter_context", 0, 1000),
        ("base_trial_cooldown_cycles", 0, 100000),
        ("hard_minimum_trial_cooldown_cycles", 0, 100000),
        ("maximum_cooldown_reduction_cycles", 0, 100000),
        ("minimum_policy_cycles_between_experiments", 0, 100000),
        ("minimum_policy_cycles_between_reobservations", 0, 100000),
    )
    for field, lower, upper in integer_bounds:
        value = integer(plan.get(field), -1)
        if not lower <= value <= upper:
            blockers.append(f"policy_plan_{field}_invalid")
    if integer(plan.get("hard_minimum_trial_cooldown_cycles"), 0) > integer(
        plan.get("base_trial_cooldown_cycles"), 0
    ):
        blockers.append("policy_hard_cooldown_exceeds_base")

    bounded_fields = (
        "learning_rate",
        "exploration_weight",
        "max_exploration_bonus",
        "curvature_penalty",
        "resolved_evidence_weight",
        "max_portfolio_adjustment",
        "shadow_model_weight",
        "shadow_learning_rate",
        "default_prediction_confidence",
        "uncertainty_weight",
        "unresolved_shadow_weight",
        "trial_novelty_weight",
        "opportunity_cost_weight",
        "base_minimum_information_gain",
        "hard_minimum_information_gain",
        "maximum_trial_risk",
        "minimum_trial_recoverability",
        "default_trial_risk",
        "default_trial_recoverability",
        "policy_information_gain_weight",
        "policy_posterior_weight",
        "policy_net_value_weight",
        "policy_pending_weight",
        "policy_recoverability_weight",
        "policy_cost_penalty_weight",
        "policy_risk_penalty_weight",
        "prior_experiment_value",
        "experiment_pressure_threshold",
        "reobserve_pending_weight",
        "reobserve_resolution_debt_weight",
        "reobserve_low_confidence_weight",
        "post_experiment_reobserve_bonus",
        "reobserve_pressure_threshold",
        "information_gain_threshold_adaptation_rate",
        "outcome_cost_weight",
        "outcome_risk_weight",
        "outcome_recoverability_weight",
    )
    for field in bounded_fields:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            blockers.append(f"policy_plan_{field}_invalid")
            continue
        if not 0.0 <= float(raw) <= 1.0:
            blockers.append(f"policy_plan_{field}_invalid")
    if clamp(plan.get("hard_minimum_information_gain")) > clamp(
        plan.get("base_minimum_information_gain")
    ):
        blockers.append("policy_hard_information_gain_floor_exceeds_base")
    if isinstance(plan.get("experiment_success_net_value_floor"), bool) or not isinstance(
        plan.get("experiment_success_net_value_floor"), (int, float)
    ):
        blockers.append("policy_experiment_success_net_value_floor_invalid")
    elif signed(plan.get("experiment_success_net_value_floor"), 2.0) != float(
        plan.get("experiment_success_net_value_floor")
    ):
        blockers.append("policy_experiment_success_net_value_floor_invalid")

    nonnegative_fields = (
        "reliability_prior_mass",
        "total_trial_budget",
        "maximum_trial_cost",
        "default_trial_cost",
        "posterior_confidence_mass",
    )
    for field in nonnegative_fields:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or float(raw) < 0.0:
            blockers.append(f"policy_plan_{field}_invalid")
    if nonnegative(plan.get("maximum_trial_cost")) > nonnegative(
        plan.get("total_trial_budget")
    ):
        blockers.append("policy_maximum_trial_cost_exceeds_total_budget")
    if nonnegative(plan.get("default_trial_cost")) > nonnegative(
        plan.get("maximum_trial_cost")
    ):
        blockers.append("policy_default_trial_cost_exceeds_maximum")
    if nonnegative(experiment_bundle.get("trial_budget_spent")) > nonnegative(
        plan.get("total_trial_budget")
    ):
        blockers.append("policy_existing_trial_spend_exceeds_budget")
    if not mapping(plan.get("shadow_action_utility")):
        blockers.append("policy_shadow_action_utility_missing")
    for action, value in mapping(plan.get("shadow_action_utility")).items():
        if not str(action) or clamp(value, -1.0) < 0.0:
            blockers.append("policy_shadow_action_utility_invalid")

    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("policy_license_version_invalid")
    license_expected = {
        "bound_policy_plan_digest": plan.get("policy_plan_digest", ""),
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
        "bound_previous_policy_bundle_digest": policy_bundle.get(
            "policy_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"policy_license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "capability_read_allowed",
        "portfolio_read_allowed",
        "experiment_read_allowed",
        "policy_read_allowed",
        "preview_allowed",
        "policy_decision_allowed",
        "one_child_experiment_cycle_allowed",
        "reobserve_routing_allowed",
        "policy_update_allowed",
        "policy_bundle_write_allowed",
        "policy_state_write_allowed",
        "decision_write_allowed",
        "outcome_write_allowed",
        "child_packet_write_allowed",
        "ledger_append_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "multiple_child_cycles_allowed",
        "v0_8_hard_gate_bypass_allowed",
        "unbudgeted_trial_allowed",
        "shadow_execution_allowed",
        "external_network_effect_allowed",
        "world_update_allowed",
        "memory_overwrite_allowed",
        "source_authority_transfer_allowed",
        "adapter_authority_inheritance_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))
