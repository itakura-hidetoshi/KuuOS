#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    BUNDLE_VERSION as GAUGE_BUNDLE_VERSION,
    STATE_VERSION as GAUGE_STATE_VERSION,
    bundle_digest as gauge_bundle_digest,
    state_digest as gauge_state_digest,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    STATE_VERSION as REGRET_STATE_VERSION,
)
from runtime.kuuos_policy_regret_cadence_validation_v0_10 import (
    validate_bundle as validate_regret_bundle,
)
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    BUNDLE_VERSION,
    HORIZONS,
    LICENSE_VERSION,
    MODES,
    PLAN_VERSION,
    REQUIRED_BOUNDARY,
    SECTION_VERSION,
    STATE_VERSION,
    as_list,
    clamp,
    integer,
    mapping,
    nonnegative,
    valid_digest,
)


def validate_bundle(bundle: Mapping[str, Any], agent_id: str, blockers: list[str]) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("horizon_bundle_version_invalid")
        return
    if not valid_digest(bundle, "horizon_bundle_digest"):
        blockers.append("horizon_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("horizon_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("horizon_bundle_generation_invalid")
    seen: set[str] = set()
    for raw in as_list(bundle.get("sections")):
        section = mapping(raw)
        context_key = str(section.get("context_key", ""))
        if section.get("version") != SECTION_VERSION:
            blockers.append("horizon_section_version_invalid")
        if not valid_digest(section, "horizon_section_digest"):
            blockers.append("horizon_section_digest_invalid")
        if not context_key or context_key in seen:
            blockers.append("horizon_section_context_missing_or_repeated")
        seen.add(context_key)
        for horizon in HORIZONS:
            for mode in MODES:
                field = f"{horizon}_{mode}_credit"
                raw_value = section.get(field)
                if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)):
                    blockers.append(f"horizon_section_{field}_invalid")
                elif not 0.0 <= float(raw_value) <= 1.0:
                    blockers.append(f"horizon_section_{field}_invalid")
        for field in (
            "cycle_count",
            "short_cycle_count",
            "medium_cycle_count",
            "long_cycle_count",
            "delayed_compatible_evidence_count",
            "terminal_section_observation_count",
        ):
            if integer(section.get(field), -1) < 0:
                blockers.append(f"horizon_section_{field}_invalid")
    processed = [
        str(item)
        for item in as_list(bundle.get("processed_child_regret_outcome_digests"))
    ]
    if len(processed) != len(set(processed)):
        blockers.append("horizon_processed_regret_outcome_repeated")
    effects = [str(item) for item in as_list(bundle.get("processed_child_effect_digests"))]
    if len(effects) != len(set(effects)):
        blockers.append("horizon_processed_effect_repeated")


def validate_inputs(
    *,
    root_packet: Mapping[str, Any],
    registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]],
    upstream: Mapping[str, Mapping[str, Any]],
    gauge_state: Mapping[str, Any],
    gauge_bundle: Mapping[str, Any],
    regret_state: Mapping[str, Any],
    regret_bundle: Mapping[str, Any],
    horizon_state: Mapping[str, Any],
    horizon_bundle: Mapping[str, Any],
    plan: Mapping[str, Any],
    license_packet: Mapping[str, Any],
    source_batch_digest: str,
    blockers: list[str],
) -> None:
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    agent_id = str(plan.get("agent_id", ""))
    validate_regret_bundle(regret_bundle, agent_id, blockers)
    validate_bundle(horizon_bundle, agent_id, blockers)

    if regret_state and (
        regret_state.get("version") != REGRET_STATE_VERSION
        or not valid_digest(regret_state, "regret_state_digest")
    ):
        blockers.append("previous_regret_state_invalid")
    if horizon_state and (
        horizon_state.get("version") != STATE_VERSION
        or not valid_digest(horizon_state, "horizon_state_digest")
    ):
        blockers.append("previous_horizon_state_invalid")
    if gauge_bundle and (
        gauge_bundle.get("version") != GAUGE_BUNDLE_VERSION
        or gauge_bundle.get("gauge_bundle_digest") != gauge_bundle_digest(gauge_bundle)
    ):
        blockers.append("gauge_bundle_invalid")
    if gauge_state and (
        gauge_state.get("version") != GAUGE_STATE_VERSION
        or gauge_state.get("gauge_state_digest") != gauge_state_digest(gauge_state)
    ):
        blockers.append("gauge_state_invalid")

    if plan.get("version") != PLAN_VERSION:
        blockers.append("horizon_plan_version_invalid")
    if not valid_digest(plan, "horizon_plan_digest"):
        blockers.append("horizon_plan_digest_invalid")
    for field in ("horizon_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"horizon_plan_{field}_missing")

    expected = {
        "expected_source_batch_digest": source_batch_digest,
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "expected_previous_regret_state_digest": regret_state.get("regret_state_digest", ""),
        "expected_previous_regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "expected_previous_horizon_state_digest": horizon_state.get("horizon_state_digest", ""),
        "expected_previous_horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "expected_gauge_state_digest": gauge_state.get("gauge_state_digest", ""),
        "expected_gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
    }
    for name, packet in upstream.items():
        digest_field = {
            "capability_state": "capability_state_digest",
            "capability_bundle": "capability_bundle_digest",
            "source_portfolio_bundle": "portfolio_bundle_digest",
            "experiment_state": "experiment_state_digest",
            "experiment_bundle": "experiment_bundle_digest",
            "policy_state": "policy_state_digest",
            "policy_bundle": "policy_bundle_digest",
        }[name]
        expected[f"expected_{name}_digest"] = packet.get(digest_field, "")
    for field, value in expected.items():
        if plan.get(field, "") != value:
            blockers.append(f"horizon_plan_{field}_mismatch")

    for field, expected_value in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected_value:
            blockers.append(f"horizon_boundary_{field}_invalid")

    weights = [clamp(plan.get(f"{horizon}_horizon_weight"), -1.0) for horizon in HORIZONS]
    if min(weights) < 0.0 or sum(weights) <= 0.0:
        blockers.append("horizon_weights_invalid")
    for horizon in HORIZONS:
        for field in (
            f"{horizon}_credit_decay",
            f"{horizon}_value_learning_rate" if horizon == "short" else "",
        ):
            if not field:
                continue
            raw = plan.get(field)
            if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0.0 <= float(raw) <= 1.0:
                blockers.append(f"horizon_plan_{field}_invalid")

    bounded_fields = (
        "horizon_threshold_gain",
        "horizon_exploit_resistance_gain",
        "short_regret_learning_rate",
        "medium_progress_learning_rate",
        "medium_recovery_learning_rate",
        "medium_delayed_learning_rate",
        "long_progress_learning_rate",
        "long_terminal_learning_rate",
        "long_recovery_learning_rate",
        "long_delayed_learning_rate",
        "progress_delta_weight",
        "observed_benefit_weight",
        "terminal_ratio_weight",
        "effect_confidence_weight",
        "observed_harm_weight",
        "recoverability_deficit_weight",
        "curvature_cost_weight",
        "repair_continuation_cost",
    )
    for field in bounded_fields:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0.0 <= float(raw) <= 1.0:
            blockers.append(f"horizon_plan_{field}_invalid")

    if integer(plan.get("long_horizon_activation_cycles"), 0) < 1:
        blockers.append("horizon_plan_long_horizon_activation_cycles_invalid")
    for field in (
        "horizon_interval_gain_cycles",
        "horizon_exploit_interval_gain_cycles",
        "max_horizon_outcomes",
        "max_horizon_holonomy",
    ):
        if integer(plan.get(field), -1) < 0:
            blockers.append(f"horizon_plan_{field}_invalid")
    if nonnegative(plan.get("delayed_evidence_scale"), -1.0) <= 0.0:
        blockers.append("horizon_plan_delayed_evidence_scale_invalid")
    if nonnegative(plan.get("long_holonomy_scale"), -1.0) <= 0.0:
        blockers.append("horizon_plan_long_holonomy_scale_invalid")

    threshold_ranges = (
        ("minimum_experiment_pressure_threshold", "base_experiment_pressure_threshold", "maximum_experiment_pressure_threshold"),
        ("minimum_reobserve_pressure_threshold", "base_reobserve_pressure_threshold", "maximum_reobserve_pressure_threshold"),
    )
    for low_field, base_field, high_field in threshold_ranges:
        low = clamp(plan.get(low_field), -1.0)
        base = clamp(plan.get(base_field), -1.0)
        high = clamp(plan.get(high_field), -1.0)
        if min(low, base, high) < 0.0 or not low <= base <= high:
            blockers.append(f"horizon_threshold_range_{base_field}_invalid")
    interval_ranges = (
        ("minimum_policy_cycles_between_experiments", "base_policy_cycles_between_experiments", "maximum_policy_cycles_between_experiments"),
        ("minimum_policy_cycles_between_reobservations", "base_policy_cycles_between_reobservations", "maximum_policy_cycles_between_reobservations"),
    )
    for low_field, base_field, high_field in interval_ranges:
        low = integer(plan.get(low_field), -1)
        base = integer(plan.get(base_field), -1)
        high = integer(plan.get(high_field), -1)
        if low < 0 or not low <= base <= high:
            blockers.append(f"horizon_interval_range_{base_field}_invalid")

    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("horizon_license_version_invalid")
    license_expected = {
        "bound_horizon_plan_digest": plan.get("horizon_plan_digest", ""),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "bound_previous_regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "bound_previous_horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
    }
    for field, value in license_expected.items():
        if license_packet.get(field) != value:
            blockers.append(f"horizon_license_{field}_mismatch")
    for field in (
        "source_read_allowed",
        "upstream_state_read_allowed",
        "gauge_evidence_read_allowed",
        "horizon_credit_update_allowed",
        "cadence_adaptation_allowed",
        "one_child_regret_cycle_allowed",
        "horizon_bundle_write_allowed",
        "horizon_state_write_allowed",
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
        "multiple_child_regret_cycles_allowed",
        "effectless_credit_update_allowed",
        "counterfactual_outcome_promotion_allowed",
        "v0_10_authority_bypass_allowed",
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
