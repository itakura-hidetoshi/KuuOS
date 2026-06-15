#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import validate_adapter_registry, validate_source_packets
from runtime.kuuos_delayed_credit_multihorizon_validation_v0_11 import validate_bundle as validate_horizon_bundle
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import BUNDLE_VERSION, LICENSE_VERSION, PLAN_VERSION, REQUIRED_BOUNDARY, SECTION_VERSION, STATE_VERSION, as_list, clamp, integer, mapping, valid_digest

def validate_bundle(bundle: Mapping[str, Any], agent_id: str, blockers: list[str]) -> None:
    if bundle.get("version") != BUNDLE_VERSION:
        blockers.append("arbitration_bundle_version_invalid")
        return
    if not valid_digest(bundle, "arbitration_bundle_digest"):
        blockers.append("arbitration_bundle_digest_invalid")
    if bundle.get("agent_id") != agent_id:
        blockers.append("arbitration_bundle_agent_mismatch")
    if integer(bundle.get("generation"), -1) < 0:
        blockers.append("arbitration_bundle_generation_invalid")
    seen: set[str] = set()
    for raw in as_list(bundle.get("sections")):
        section = mapping(raw)
        context_key = str(section.get("context_key", ""))
        if section.get("version") != SECTION_VERSION:
            blockers.append("arbitration_section_version_invalid")
        if not valid_digest(section, "arbitration_section_digest"):
            blockers.append("arbitration_section_digest_invalid")
        if not context_key or context_key in seen:
            blockers.append("arbitration_section_context_missing_or_repeated")
        seen.add(context_key)
        if integer(section.get("cycle_count"), -1) < 0:
            blockers.append("arbitration_section_cycle_count_invalid")
        for field in ("last_transported_short_weight", "last_transported_medium_weight", "last_transported_long_weight", "last_arbitration_curvature"):
            raw_value = section.get(field)
            if isinstance(raw_value, bool) or not isinstance(raw_value, (int, float)) or not 0.0 <= float(raw_value) <= 1.0:
                blockers.append(f"arbitration_section_{field}_invalid")

def validate_inputs(*, root_packet: Mapping[str, Any], registry: Mapping[str, Any], sources: list[Mapping[str, Any]], upstream: Mapping[str, Mapping[str, Any]], arbitration_state: Mapping[str, Any], arbitration_bundle: Mapping[str, Any], plan: Mapping[str, Any], license_packet: Mapping[str, Any], source_batch_digest: str, blockers: list[str]) -> None:
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    agent_id = str(plan.get("agent_id", ""))
    validate_horizon_bundle(upstream["horizon_bundle"], agent_id, blockers)
    validate_bundle(arbitration_bundle, agent_id, blockers)
    if arbitration_state and (arbitration_state.get("version") != STATE_VERSION or not valid_digest(arbitration_state, "arbitration_state_digest")):
        blockers.append("previous_arbitration_state_invalid")
    if plan.get("version") != PLAN_VERSION:
        blockers.append("arbitration_plan_version_invalid")
    if not valid_digest(plan, "arbitration_plan_digest"):
        blockers.append("arbitration_plan_digest_invalid")
    for field in ("arbitration_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"arbitration_plan_{field}_missing")
    digest_fields = {
        "expected_source_batch_digest": source_batch_digest,
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "expected_previous_arbitration_state_digest": arbitration_state.get("arbitration_state_digest", ""),
        "expected_previous_arbitration_bundle_digest": arbitration_bundle.get("arbitration_bundle_digest", ""),
    }
    source_fields = {
        "capability_state": "capability_state_digest",
        "capability_bundle": "capability_bundle_digest",
        "source_portfolio_bundle": "portfolio_bundle_digest",
        "experiment_state": "experiment_state_digest",
        "experiment_bundle": "experiment_bundle_digest",
        "policy_state": "policy_state_digest",
        "policy_bundle": "policy_bundle_digest",
        "regret_state": "regret_state_digest",
        "regret_bundle": "regret_bundle_digest",
        "horizon_state": "horizon_state_digest",
        "horizon_bundle": "horizon_bundle_digest",
        "gauge_state": "gauge_state_digest",
        "gauge_bundle": "gauge_bundle_digest",
    }
    for name, digest_field in source_fields.items():
        digest_fields[f"expected_{name}_digest"] = upstream[name].get(digest_field, "")
    for field, value in digest_fields.items():
        if plan.get(field, "") != value:
            blockers.append(f"arbitration_plan_{field}_mismatch")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"arbitration_boundary_{field}_invalid")
    bounded = (
        "base_short_horizon_weight", "base_medium_horizon_weight", "base_long_horizon_weight",
        "minimum_horizon_weight", "parallel_transport_gain", "curvature_temperature_gain",
        "short_curvature_response_gain", "medium_progress_response_gain",
        "medium_recovery_response_gain", "long_terminal_response_gain",
        "long_holonomy_response_gain", "outcome_memory_gain",
        "plural_conflict_curvature_threshold", "repair_outcome_threshold",
        "progressing_outcome_threshold", "stabilizing_terminal_threshold",
    )
    for field in bounded:
        raw = plan.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0.0 <= float(raw) <= 1.0:
            blockers.append(f"arbitration_plan_{field}_invalid")
    base_sum = sum(clamp(plan.get(field)) for field in ("base_short_horizon_weight", "base_medium_horizon_weight", "base_long_horizon_weight"))
    if base_sum <= 0.0:
        blockers.append("arbitration_base_weights_invalid")
    if clamp(plan.get("minimum_horizon_weight")) > 1.0 / 3.0:
        blockers.append("arbitration_minimum_horizon_weight_too_large")
    for field in ("max_arbitration_outcomes", "max_arbitration_holonomy"):
        if integer(plan.get(field), 0) <= 0:
            blockers.append(f"arbitration_plan_{field}_invalid")
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("arbitration_license_version_invalid")
    bindings = {
        "bound_arbitration_plan_digest": plan.get("arbitration_plan_digest", ""),
        "bound_source_batch_digest": source_batch_digest,
        "bound_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "bound_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "bound_previous_horizon_bundle_digest": upstream["horizon_bundle"].get("horizon_bundle_digest", ""),
        "bound_previous_arbitration_bundle_digest": arbitration_bundle.get("arbitration_bundle_digest", ""),
    }
    for field, value in bindings.items():
        if license_packet.get(field) != value:
            blockers.append(f"arbitration_license_{field}_mismatch")
    for field in ("source_read_allowed", "upstream_state_read_allowed", "gauge_arbitration_allowed", "parallel_transport_allowed", "one_child_horizon_cycle_allowed", "arbitration_bundle_write_allowed", "arbitration_state_write_allowed", "decision_write_allowed", "outcome_write_allowed", "child_packet_write_allowed", "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed"):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in ("multiple_child_horizon_cycles_allowed", "winner_take_all_collapse_allowed", "effectless_outcome_allowed", "v0_11_authority_bypass_allowed", "v0_8_hard_gate_bypass_allowed", "shadow_execution_allowed", "external_network_effect_allowed", "world_update_allowed", "memory_overwrite_allowed"):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))
