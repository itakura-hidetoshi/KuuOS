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
from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    STATE_VERSION as EXPERIMENT_STATE_VERSION,
)
from runtime.kuuos_bounded_portfolio_experiment_validation_v0_8 import (
    validate_bundle as validate_experiment_bundle,
)
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    STATE_VERSION as POLICY_STATE_VERSION,
)
from runtime.kuuos_experiment_outcome_policy_validation_v0_9 import (
    validate_bundle as validate_policy_bundle,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
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
        blockers.append("regret_bundle_version_invalid")
        return
    if not valid_digest(bundle, "regret_bundle_digest"):
        blockers.append("regret_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("regret_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("regret_bundle_generation_invalid")
    seen: set[str] = set()
    for raw in as_list(bundle.get("sections")):
        section = mapping(raw)
        context_key = str(section.get("context_key", ""))
        if section.get("version") != SECTION_VERSION:
            blockers.append("regret_section_version_invalid")
        if not valid_digest(section, "regret_section_digest"):
            blockers.append("regret_section_digest_invalid")
        if not context_key or context_key in seen:
            blockers.append("regret_section_context_missing_or_repeated")
        seen.add(context_key)
        for field in (
            "cycle_count",
            "positive_regret_count",
            "zero_regret_count",
            "experiment_alternative_count",
            "reobserve_alternative_count",
            "exploit_alternative_count",
            "delayed_compatible_evidence_count",
            "pending_counterfactual_evidence_count",
        ):
            if integer(section.get(field), -1) < 0:
                blockers.append(f"regret_section_{field}_invalid")
        for field in (
            "experiment_regret_credit",
            "reobserve_regret_credit",
            "exploit_regret_credit",
            "last_best_alternative_confidence",
            "last_bounded_regret",
        ):
            raw_value = section.get(field)
            if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
                blockers.append(f"regret_section_{field}_invalid")
            elif not 0.0 <= float(raw_value) <= 1.0:
                blockers.append(f"regret_section_{field}_invalid")
    processed_outcomes = [
        str(item) for item in as_list(bundle.get("processed_policy_outcome_digests"))
    ]
    if len(processed_outcomes) != len(set(processed_outcomes)):
        blockers.append("regret_processed_policy_outcome_repeated")
    processed_resolutions = [
        str(item) for item in as_list(bundle.get("processed_delayed_resolution_ids"))
    ]
    if len(processed_resolutions) != len(set(processed_resolutions)):
        blockers.append("regret_processed_resolution_repeated")


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
    regret_state: Mapping[str, Any],
    regret_bundle: Mapping[str, Any],
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
    validate_policy_bundle(policy_bundle, agent_id, blockers)
    validate_bundle(regret_bundle, agent_id, blockers)

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
        policy_state.get("version") != POLICY_STATE_VERSION
        or not valid_digest(policy_state, "policy_state_digest")
    ):
        blockers.append("previous_policy_state_invalid")
    if regret_state and (
        regret_state.get("version") != STATE_VERSION
        or not valid_digest(regret_state, "regret_state_digest")
    ):
        blockers.append("previous_regret_state_invalid")

    if plan.get("version") != PLAN_VERSION:
        blockers.append("regret_plan_version_invalid")
    if not valid_digest(plan, "regret_plan_digest"):
        blockers.append("regret_plan_digest_invalid")
    for field in ("regret_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"regret_plan_{field}_missing")

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
        "expected_previous_regret_state_digest": regret_state.get(
            "regret_state_digest", ""
        ),
        "expected_previous_regret_bundle_digest": regret_bundle.get(
            "regret_bundle_digest", ""
        ),
    }
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"regret_plan_{field}_mismatch")

    for field, expected_value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected_value:
            blockers.append(f"regret_boundary_{field}_invalid")

    threshold_ranges = (
        (
            "minimum_experiment_pressure_threshold",
            "base_experiment_pressure_threshold",
            "maximum_experiment_pressure_threshold",
        ),
        (
            "minimum_reobserve_pressure_threshold",
            "base_reobserve_pressure_threshold",
            "maximum_reobserve_pressure_threshold",
        ),
    )
    for low_field, base_field, high_field in threshold_ranges:
        low = clamp(plan.get(low_field), -1.0)
        base = clamp(plan.get(base_field), -1.0)
        high = clamp(plan.get(high_field), -1.0)
        if min(low, base, high) < 0.0 or not low <= base <= high:
            blockers.append(f"regret_threshold_range_{base_field}_invalid")

    interval_ranges = (
        (
            "minimum_policy_cycles_between_experiments",
            "base_policy_cycles_between_experiments",
            "maximum_policy_cycles_between_experiments",
        ),
        (
            "minimum_policy_cycles_between_reobservations",
            "base_policy_cycles_between_reobservations",
            "maximum_policy_cycles_between_reobservations",
        ),
    )
    for low_field, base_field, high_field in interval_ranges:
        low = integer(plan.get(low_field), -1)
        base = integer(plan.get(base_field), -1)
        high = integer(plan.get(high_field), -1)
        if low < 0 or not low <= base <= high:
            blockers.append(f"regret_interval_range_{base_field}_invalid")

    bounded_fields = (
        "regret_threshold_gain",
        "exploit_resistance_gain",
        "minimum_counterfactual_confidence",
        "regret_tolerance",
        "maximum_regret_per_cycle",
        "regret_credit_decay",
        "regret_credit_learning_rate",
        "chosen_mode_credit_penalty",
        "prior_mode_confidence",
        "pending_shadow_discount",
        "delayed_compatible_weight",
        "prior_experiment_counterfactual_value",
        "prior_reobserve_counterfactual_value",
        "prior_exploit_counterfactual_value",
    )
    for field in bounded_fields:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            blockers.append(f"regret_plan_{field}_invalid")
        elif not 0.0 <= float(raw) <= 1.0:
            blockers.append(f"regret_plan_{field}_invalid")

    for field in (
        "regret_interval_gain_cycles",
        "exploit_interval_gain_cycles",
        "max_regret_outcomes",
        "max_regret_holonomy",
    ):
        if integer(plan.get(field), -1) < 0:
            blockers.append(f"regret_plan_{field}_invalid")
    if integer(plan.get("max_regret_outcomes"), 0) < 1:
        blockers.append("regret_plan_max_regret_outcomes_invalid")
    if integer(plan.get("max_regret_holonomy"), 0) < 1:
        blockers.append("regret_plan_max_regret_holonomy_invalid")
    if nonnegative(plan.get("counterfactual_credibility_mass"), -1.0) <= 0.0:
        blockers.append("regret_plan_counterfactual_credibility_mass_invalid")

    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("regret_license_version_invalid")
    license_expected = {
        "bound_regret_plan_digest": plan.get("regret_plan_digest", ""),
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
        "bound_previous_regret_bundle_digest": regret_bundle.get(
            "regret_bundle_digest", ""
        ),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"regret_license_{field}_mismatch")

    for field in (
        "source_read_allowed",
        "upstream_state_read_allowed",
        "counterfactual_estimation_allowed",
        "regret_update_allowed",
        "cadence_adaptation_allowed",
        "one_child_policy_cycle_allowed",
        "regret_bundle_write_allowed",
        "regret_state_write_allowed",
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
        "multiple_child_policy_cycles_allowed",
        "counterfactual_truth_promotion_allowed",
        "unexecuted_alternative_outcome_allowed",
        "v0_9_authority_bypass_allowed",
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
