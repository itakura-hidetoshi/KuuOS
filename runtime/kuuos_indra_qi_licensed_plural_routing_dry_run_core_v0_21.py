#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_licensed_plural_routing_dry_run_plan_v0_21"
LICENSE_VERSION = "indra_qi_licensed_plural_routing_dry_run_license_v0_21"
REPORT_VERSION = "indra_qi_licensed_plural_routing_dry_run_report_v0_21"
STATE_VERSION = "indra_qi_licensed_plural_routing_dry_run_state_v0_21"
LEDGER_VERSION = "indra_qi_licensed_plural_routing_dry_run_ledger_record_v0_21"
WORLD_VERSION = "indra_qi_world_model_v0_1"
PROPOSAL_VERSION = "indra_qi_bounded_plural_shadow_routing_proposal_v0_20"
SOURCE_STATE_VERSION = "indra_qi_bounded_plural_shadow_routing_state_v0_20"
SOURCE_RECOMMENDATION_VERSION = "indra_qi_bounded_plural_shadow_routing_recommendation_v0_20"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "plural_shadow_routing_proposal_ready",
    "redesign_plural_shadow_routing_proposal_recommended",
    "extend_longitudinal_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "plural_routing_dry_run_ready",
    "redesign_plural_routing_schedule_recommended",
    "restore_shadow_diversity_recommended",
    "extend_longitudinal_observation_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_20_proposal_required": True,
    "source_v0_20_digest_chain_exact": True,
    "world_source_read_only": True,
    "routing_proposal_source_read_only": True,
    "isolated_replica_stream_required": True,
    "scheduler_determinism_required": True,
    "allocation_realization_bounded": True,
    "fairness_required": True,
    "starvation_forbidden": True,
    "rollback_receipt_required": True,
    "replica_restore_required": True,
    "routing_activation_forbidden": True,
    "live_route_disabled": True,
    "external_actuation_disabled": True,
    "world_update_disabled": True,
    "winner_selection_forbidden": True,
    "candidate_weighting_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_lineage_selection_authority": True,
    "not_lineage_execution_authority": True,
    "not_live_routing_authority": True,
    "not_external_world_actuation_authority": True,
    "not_unlicensed_execution_authority": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def sha(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_routing_dry_run_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_routing_dry_run_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_routing_dry_run_state_digest"))


def _positive_int(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"{prefix}_{field}_invalid")


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("dry_run_plan_version_invalid")
    if plan.get("plural_routing_dry_run_plan_digest") != plan_digest(plan):
        blockers.append("dry_run_plan_digest_invalid")
    for field in (
        "dry_run_program_id",
        "dry_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_plural_routing_proposal_digest",
        "expected_source_plural_routing_state_digest",
        "expected_source_plural_routing_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"dry_run_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"dry_run_boundary_{field}_mismatch")
    policy = mapping(plan.get("dry_run_policy"))
    _positive_int(
        policy,
        (
            "minimum_schedule_ticks",
            "maximum_schedule_ticks",
            "maximum_consecutive_ticks_per_lineage",
            "maximum_idle_ticks",
        ),
        blockers,
        "dry_run_policy",
    )
    _bounded(
        policy,
        (
            "maximum_allocation_error",
            "minimum_jain_fairness_index",
            "minimum_lineage_service_ratio",
            "maximum_replica_failure_ratio",
        ),
        blockers,
        "dry_run_policy",
    )
    for field in (
        "require_exact_replica_input_binding",
        "require_deterministic_replay",
        "require_rollback_receipt",
        "require_replica_restore",
        "require_routing_activation_disabled",
        "require_live_route_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"dry_run_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    proposal: Mapping[str, Any],
    source_state: Mapping[str, Any],
    source_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("dry_run_source_world_invalid")
    if proposal.get("version") != PROPOSAL_VERSION or not valid_digest(
        proposal, "plural_shadow_routing_proposal_digest"
    ):
        blockers.append("dry_run_source_proposal_invalid")
    if source_state.get("version") != SOURCE_STATE_VERSION or not valid_digest(
        source_state, "plural_routing_state_digest"
    ):
        blockers.append("dry_run_source_state_invalid")
    if source_recommendation.get("version") != SOURCE_RECOMMENDATION_VERSION or not valid_digest(
        source_recommendation, "plural_routing_recommendation_digest"
    ):
        blockers.append("dry_run_source_recommendation_invalid")

    world_sha = str(world.get("indra_qi_world_state_digest", ""))
    proposal_sha = str(proposal.get("plural_shadow_routing_proposal_digest", ""))
    state_sha = str(source_state.get("plural_routing_state_digest", ""))
    recommendation_sha = str(source_recommendation.get("plural_routing_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_sha,
        "expected_plural_routing_proposal_digest": proposal_sha,
        "expected_source_plural_routing_state_digest": state_sha,
        "expected_source_plural_routing_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"dry_run_{field}_mismatch")

    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("dry_run_world_model_id_mismatch")
    if (
        proposal.get("world_model_id") != world_model_id
        or source_state.get("world_model_id") != world_model_id
        or source_recommendation.get("world_model_id") != world_model_id
    ):
        blockers.append("dry_run_source_world_model_chain_invalid")
    if proposal.get("source_world_state_digest") != world_sha:
        blockers.append("dry_run_proposal_world_digest_mismatch")
    if source_state.get("latest_plural_shadow_routing_proposal_digest") != proposal_sha:
        blockers.append("dry_run_state_proposal_digest_mismatch")
    if source_recommendation.get("plural_shadow_routing_proposal_digest") != proposal_sha:
        blockers.append("dry_run_recommendation_proposal_digest_mismatch")
    if source_state.get("latest_plural_routing_decision") != source_recommendation.get("decision"):
        blockers.append("dry_run_source_decision_mismatch")
    if source_state.get("last_proposal_run_id") != source_recommendation.get("proposal_run_id"):
        blockers.append("dry_run_source_run_id_mismatch")

    source_decision = str(source_recommendation.get("decision", ""))
    if source_decision not in SOURCE_DECISIONS:
        blockers.append("dry_run_source_decision_invalid")
    if (
        proposal.get("proposal_only") is not True
        or proposal.get("routing_activated") is not False
        or proposal.get("live_route_enabled") is not False
    ):
        blockers.append("dry_run_source_proposal_boundary_invalid")
    if (
        source_recommendation.get("recommendation_only") is not True
        or source_recommendation.get("routing_activated") is not False
        or source_recommendation.get("winner_selected") is not False
    ):
        blockers.append("dry_run_source_recommendation_boundary_invalid")
    for field in (
        "direct_routing_activation_authority",
        "direct_winner_selection_authority",
        "direct_lineage_selection_authority",
        "direct_lineage_execution_authority",
        "direct_world_update_authority",
        "direct_external_actuation_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
        "truth_authority",
    ):
        if source_recommendation.get(field) is not False:
            blockers.append(f"dry_run_source_{field}_not_false")

    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("dry_run_multi_world_noncollapse_missing")

    routes: dict[str, dict[str, Any]] = {}
    slots: set[str] = set()
    for raw in items(proposal.get("route_entries")):
        route = dict(mapping(raw))
        lineage_id = str(route.get("lineage_id", ""))
        slot = str(route.get("route_slot_id", ""))
        if not lineage_id or lineage_id in routes or not slot or slot in slots:
            blockers.append("dry_run_source_route_ids_invalid")
        else:
            routes[lineage_id] = route
            slots.add(slot)
        if route.get("routing_activation_enabled") is not False or route.get("live_route_enabled") is not False:
            blockers.append("dry_run_source_route_activation_invalid")
    if not routes:
        blockers.append("dry_run_source_routes_missing")
    return {
        "world_digest": world_sha,
        "proposal_digest": proposal_sha,
        "state_digest": state_sha,
        "recommendation_digest": recommendation_sha,
        "source_decision": source_decision,
        "source_proposal_run_id": str(source_recommendation.get("proposal_run_id", "")),
        "routes": routes,
    }


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    report: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_plural_routing_dry_run_plan_digest": str(
            plan.get("plural_routing_dry_run_plan_digest", "")
        ),
        "bound_plural_routing_dry_run_report_digest": str(
            report.get("plural_routing_dry_run_report_digest", "")
        ),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_plural_routing_proposal_digest": str(source.get("proposal_digest", "")),
        "bound_source_plural_routing_state_digest": str(source.get("state_digest", "")),
        "bound_source_plural_routing_recommendation_digest": str(
            source.get("recommendation_digest", "")
        ),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"dry_run_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("dry_run_license_id_missing")
    for field in (
        "state_write_allowed",
        "summary_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"dry_run_license_{field}_not_true")
    for field in (
        "routing_activation_authority_granted",
        "winner_selection_authority_granted",
        "external_actuation_authority_granted",
        "world_update_authority_granted",
        "lineage_selection_authority_granted",
        "lineage_execution_authority_granted",
        "truth_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"dry_run_license_{field}_not_false")


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("dry_run_report_version_invalid")
    if report.get("dry_run_id") != plan.get("dry_run_id"):
        blockers.append("dry_run_report_id_mismatch")
    if report.get("source_plural_routing_proposal_digest") != source.get("proposal_digest"):
        blockers.append("dry_run_report_proposal_digest_mismatch")
    if report.get("plural_routing_dry_run_report_digest") != report_digest(report):
        blockers.append("dry_run_report_digest_invalid")
    if report.get("routing_activation_requested") is not False:
        blockers.append("dry_run_report_activation_requested")
    replica_input = str(report.get("replica_input_digest", ""))
    if not replica_input:
        blockers.append("dry_run_replica_input_missing")

    ticks = [dict(mapping(value)) for value in items(report.get("schedule_ticks"))]
    if not ticks:
        blockers.append("dry_run_schedule_ticks_missing")
        return ticks
    routes = mapping(source.get("routes"))
    seen_indices: set[int] = set()
    for index, tick in enumerate(ticks):
        tick_index = tick.get("tick_index")
        lineage_id = str(tick.get("lineage_id", ""))
        route = mapping(routes.get(lineage_id))
        if (
            isinstance(tick_index, bool)
            or not isinstance(tick_index, int)
            or tick_index <= 0
            or tick_index in seen_indices
        ):
            blockers.append(f"dry_run_tick_{index}_index_invalid")
        seen_indices.add(tick_index if isinstance(tick_index, int) else -1)
        if lineage_id not in routes:
            blockers.append(f"dry_run_tick_{index}_lineage_invalid")
        if tick.get("route_slot_id") != route.get("route_slot_id"):
            blockers.append(f"dry_run_tick_{index}_route_slot_mismatch")
        if tick.get("replica_input_digest") != replica_input:
            blockers.append(f"dry_run_tick_{index}_replica_input_mismatch")
        for field in (
            "replica_snapshot_digest",
            "output_digest",
            "replay_output_digest",
            "rollback_receipt_digest",
            "expected_rollback_receipt_digest",
        ):
            if not str(tick.get(field, "")):
                blockers.append(f"dry_run_tick_{index}_{field}_missing")
        for field in (
            "routing_activation_attempted",
            "live_route_attempted",
            "external_actuation_attempted",
            "world_update_attempted",
            "policy_boundary_preserved",
            "replica_restored",
        ):
            if not isinstance(tick.get(field), bool):
                blockers.append(f"dry_run_tick_{index}_{field}_invalid")
    return ticks


def analyze_dry_run(
    ticks: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("dry_run_policy"))
    routes = mapping(source.get("routes"))
    counts = Counter(str(tick.get("lineage_id", "")) for tick in ticks)
    total = len(ticks)
    target = {
        lineage_id: number(mapping(route).get("allocation_share"))
        for lineage_id, route in routes.items()
    }
    realized = {
        lineage_id: counts.get(lineage_id, 0) / max(total, 1)
        for lineage_id in routes
    }
    errors = {
        lineage_id: round(abs(realized[lineage_id] - target[lineage_id]), 8)
        for lineage_id in routes
    }
    max_error = max(errors.values(), default=1.0)
    served = sum(counts.get(lineage_id, 0) > 0 for lineage_id in routes)
    service_ratio = clamp(served / max(len(routes), 1))
    allocations = [counts.get(lineage_id, 0) for lineage_id in routes]
    denominator = len(allocations) * sum(value * value for value in allocations)
    fairness = clamp((sum(allocations) ** 2) / denominator) if allocations and denominator else 0.0

    deterministic = 0
    restored = 0
    boundary_breaches = 0
    rollback_matches = 0
    consecutive = 0
    max_consecutive = 0
    previous: str | None = None
    idle_ticks = 0
    tick_results: list[dict[str, Any]] = []
    failures = 0
    for raw in ticks:
        tick = dict(raw)
        lineage_id = str(tick.get("lineage_id", ""))
        if lineage_id == previous:
            consecutive += 1
        else:
            previous = lineage_id
            consecutive = 1
        max_consecutive = max(max_consecutive, consecutive)
        replay_ok = tick.get("output_digest") == tick.get("replay_output_digest")
        rollback_ok = tick.get("rollback_receipt_digest") == tick.get(
            "expected_rollback_receipt_digest"
        )
        restore_ok = tick.get("replica_restored") is True
        boundary_ok = (
            tick.get("routing_activation_attempted") is False
            and tick.get("live_route_attempted") is False
            and tick.get("external_actuation_attempted") is False
            and tick.get("world_update_attempted") is False
            and tick.get("policy_boundary_preserved") is True
        )
        deterministic += replay_ok
        rollback_matches += rollback_ok
        restored += restore_ok
        boundary_breaches += not boundary_ok
        failures += not (replay_ok and rollback_ok and restore_ok)
        tick["deterministic_replay"] = replay_ok
        tick["rollback_receipt_match"] = rollback_ok
        tick["replica_restore_verified"] = restore_ok
        tick["isolation_boundary_preserved"] = boundary_ok
        tick_results.append(tick)

    failure_ratio = clamp(failures / max(total, 1))
    diversity_gates = {
        "all_lineages_served": served == len(routes),
        "lineage_service_ratio_sufficient": service_ratio
        >= number(policy.get("minimum_lineage_service_ratio")),
        "jain_fairness_sufficient": fairness
        >= number(policy.get("minimum_jain_fairness_index")),
        "starvation_absent": idle_ticks <= int(policy.get("maximum_idle_ticks", 0)),
    }
    schedule_gates = {
        "tick_count_bounded": int(policy.get("minimum_schedule_ticks", 0))
        <= total
        <= int(policy.get("maximum_schedule_ticks", 0)),
        "allocation_error_bounded": max_error
        <= number(policy.get("maximum_allocation_error")),
        "consecutive_ticks_bounded": max_consecutive
        <= int(policy.get("maximum_consecutive_ticks_per_lineage", 0)),
        "deterministic_replay_complete": deterministic == total,
        "rollback_receipts_complete": rollback_matches == total,
        "replica_restore_complete": restored == total,
        "replica_failure_ratio_bounded": failure_ratio
        <= number(policy.get("maximum_replica_failure_ratio")),
        "isolation_boundary_preserved": boundary_breaches == 0,
    }
    return {
        "schedule_tick_count": total,
        "lineage_count": len(routes),
        "target_allocation": target,
        "realized_allocation": {key: round(value, 8) for key, value in realized.items()},
        "allocation_error": errors,
        "maximum_allocation_error": max_error,
        "lineage_service_ratio": service_ratio,
        "jain_fairness_index": fairness,
        "maximum_consecutive_ticks_per_lineage": max_consecutive,
        "replica_failure_ratio": failure_ratio,
        "boundary_breach_count": boundary_breaches,
        "tick_results": tick_results,
        "diversity_gates": diversity_gates,
        "schedule_gates": schedule_gates,
        "all_gates": {**diversity_gates, **schedule_gates},
    }


def evaluate_dry_run(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    diversity = mapping(analysis.get("diversity_gates"))
    schedule = mapping(analysis.get("schedule_gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_20_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_20_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_20_hold_for_observation"
    elif int(analysis.get("boundary_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "dry_run_route_or_actuation_boundary_breach"
    elif source_decision == "extend_longitudinal_observation_recommended":
        decision, reason = (
            "extend_longitudinal_observation_recommended",
            "source_v0_20_more_longitudinal_evidence_required",
        )
    elif source_decision == "restore_shadow_diversity_recommended":
        decision, reason = (
            "restore_shadow_diversity_recommended",
            "source_v0_20_shadow_diversity_restoration_required",
        )
    elif source_decision == "redesign_plural_shadow_routing_proposal_recommended":
        decision, reason = (
            "redesign_plural_routing_schedule_recommended",
            "source_v0_20_routing_proposal_redesign_required",
        )
    elif source_decision == "plural_shadow_routing_proposal_ready" and not all(
        value is True for value in diversity.values()
    ):
        decision, reason = (
            "restore_shadow_diversity_recommended",
            "dry_run_fairness_or_starvation_gate_failed",
        )
    elif source_decision == "plural_shadow_routing_proposal_ready" and all(
        value is True for value in schedule.values()
    ):
        decision, reason = (
            "plural_routing_dry_run_ready",
            "isolated_plural_scheduler_dry_run_ready",
        )
    elif source_decision == "plural_shadow_routing_proposal_ready":
        decision, reason = (
            "redesign_plural_routing_schedule_recommended",
            "dry_run_schedule_or_rollback_gate_failed",
        )
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_20_decision"
    return {
        "source_plural_routing_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "dry_run_ready": decision == "plural_routing_dry_run_ready",
        "routing_activated": False,
        "winner_selected": False,
        "recommendation_only": True,
    }
