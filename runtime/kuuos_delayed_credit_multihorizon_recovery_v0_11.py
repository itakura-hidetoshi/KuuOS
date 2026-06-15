#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_event_adapter_federation_normalization_v0_5 import (
    validate_adapter_registry,
    validate_source_packets,
)
from runtime.kuuos_policy_regret_cadence_types_v0_10 import plan_digest as regret_plan_digest
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    DECISION_VERSION,
    decision_digest,
    integer,
    read_json,
    valid_digest,
)


def validate_pending(
    *, root_packet: Mapping[str, Any], registry: Mapping[str, Any],
    sources: list[Mapping[str, Any]], plan: Mapping[str, Any],
    license_packet: Mapping[str, Any], pending: Mapping[str, Any],
    source_batch: str, blockers: list[str],
) -> None:
    validate_adapter_registry(registry, blockers)
    validate_source_packets(
        sources,
        max_sources=integer(plan.get("max_sources_per_cycle"), 0),
        max_signals_per_source=integer(plan.get("max_signals_per_source"), 0),
        max_total_signals=integer(plan.get("max_total_signals"), 0),
        blockers=blockers,
    )
    if not valid_digest(plan, "horizon_plan_digest"):
        blockers.append("horizon_plan_digest_invalid")
    if pending.get("horizon_plan_digest") != plan.get("horizon_plan_digest"):
        blockers.append("pending_horizon_plan_digest_mismatch")
    if pending.get("source_batch_digest") != source_batch:
        blockers.append("pending_source_batch_digest_mismatch")
    if plan.get("expected_root_principles_digest") != root_packet.get("root_principles_digest", ""):
        blockers.append("pending_root_principles_digest_mismatch")
    if plan.get("expected_adapter_registry_digest") != registry.get("adapter_registry_digest", ""):
        blockers.append("pending_adapter_registry_digest_mismatch")
    for field, pending_field in (
        ("expected_previous_regret_state_digest", "previous_regret_state_digest"),
        ("expected_previous_regret_bundle_digest", "previous_regret_bundle_digest"),
        ("expected_previous_horizon_state_digest", "previous_horizon_state_digest"),
        ("expected_previous_horizon_bundle_digest", "previous_horizon_bundle_digest"),
    ):
        if plan.get(field, "") != pending.get(pending_field, ""):
            blockers.append(f"pending_{field}_mismatch")
    for field in (
        "one_child_regret_cycle_allowed", "horizon_credit_update_allowed",
        "cadence_adaptation_allowed", "horizon_bundle_write_allowed",
        "horizon_state_write_allowed", "decision_write_allowed",
        "outcome_write_allowed", "child_packet_write_allowed",
        "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    for field in (
        "multiple_child_regret_cycles_allowed", "effectless_credit_update_allowed",
        "counterfactual_outcome_promotion_allowed", "v0_10_authority_bypass_allowed",
        "v0_8_hard_gate_bypass_allowed", "unbudgeted_trial_allowed",
        "shadow_execution_allowed", "external_network_effect_allowed",
        "world_update_allowed", "memory_overwrite_allowed",
    ):
        if license_packet.get(field) is not False:
            blockers.append(field.replace("allowed", "not_denied"))


def load_recovery_packets(
    *, run_id: str, pending: Mapping[str, Any], paths: Mapping[str, Any],
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    decision = read_json(paths["decision"])
    child_plan = read_json(paths["child_plan"])
    child_license = read_json(paths["child_license"])
    if (
        decision.get("version") != DECISION_VERSION
        or decision.get("horizon_run_id") != run_id
        or decision.get("horizon_decision_digest") != decision_digest(decision)
        or decision.get("horizon_decision_digest") != pending.get("horizon_decision_digest")
    ):
        blockers.append("pending_horizon_decision_invalid")
    if (
        child_plan.get("regret_plan_digest") != regret_plan_digest(child_plan)
        or child_plan.get("regret_plan_digest") != pending.get("child_regret_plan_digest")
    ):
        blockers.append("pending_child_regret_plan_invalid")
    if child_license.get("bound_regret_plan_digest") != child_plan.get("regret_plan_digest"):
        blockers.append("pending_child_regret_license_invalid")
    return decision, child_plan, child_license
