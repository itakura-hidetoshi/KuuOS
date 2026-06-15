#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping, Sequence

from runtime.kuuos_indra_qi_licensed_canary_observation_trial_base_v0_25 import *

def analyze_trial(
    trial_lanes: Sequence[Mapping[str, Any]],
    events: Sequence[Mapping[str, Any]],
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("trial_policy"))
    source_lanes = mapping(source.get("lanes"))
    trial_epoch = int(report.get("trial_epoch", 0) or 0)
    duration = int(report.get("duration_seconds", 0) or 0)
    trial_end = trial_epoch + duration
    total_fraction = sum(max(number(lane.get("trial_fraction")), 0.0) for lane in trial_lanes)
    maximum_lane_fraction = max((number(lane.get("trial_fraction")) for lane in trial_lanes), default=1.0)
    total_budget = sum(int(lane.get("event_budget", 0) or 0) for lane in trial_lanes)
    lane_count = len(trial_lanes)
    recovery_count = sum(str(lane.get("lineage_kind", "")) == "recovery" for lane in trial_lanes)
    minority_count = sum(str(lane.get("lineage_kind", "")) == "minority_preservation" for lane in trial_lanes)
    lane_counts = Counter(str(event.get("lane_id", "")) for event in events)
    trial_lane_ids = [str(lane.get("lane_id", "")) for lane in trial_lanes]
    target_total = max(total_fraction, 1e-12)
    target = {
        str(lane.get("lane_id", "")): number(lane.get("trial_fraction")) / target_total
        for lane in trial_lanes
    }
    realized = {lane_id: lane_counts.get(lane_id, 0) / max(len(events), 1) for lane_id in trial_lane_ids}
    allocation_errors = {
        lane_id: round(abs(realized.get(lane_id, 0.0) - target.get(lane_id, 0.0)), 8)
        for lane_id in trial_lane_ids
    }
    maximum_allocation_error = max(allocation_errors.values(), default=1.0)
    served = sum(lane_counts.get(lane_id, 0) > 0 for lane_id in trial_lane_ids)
    lane_service_ratio = clamp(served / max(lane_count, 1))
    service_ratios = [
        realized.get(lane_id, 0.0) / max(target.get(lane_id, 0.0), 1e-12)
        for lane_id in trial_lane_ids
    ]
    denominator = lane_count * sum(value * value for value in service_ratios)
    fairness = clamp((sum(service_ratios) ** 2) / denominator) if service_ratios and denominator else 0.0

    source_bounds_ok = True
    lane_budget_ok = True
    expiry_ok = trial_epoch >= int(source.get("proposal_epoch", 0))
    lane_boundary_breaches = 0
    enriched_lanes: list[dict[str, Any]] = []
    for raw in trial_lanes:
        lane = dict(raw)
        lane_id = str(lane.get("lane_id", ""))
        source_lane = mapping(source_lanes.get(lane_id))
        source_bounds_ok = source_bounds_ok and number(lane.get("trial_fraction"), 1.0) <= number(
            source_lane.get("canary_fraction")
        )
        lane_budget_ok = lane_budget_ok and int(lane.get("event_budget", 0) or 0) <= min(
            int(source_lane.get("event_budget", 0) or 0),
            int(policy.get("maximum_event_budget_per_lane", 0)),
        )
        expiry = int(lane.get("expiry_epoch", 0) or 0)
        expiry_ok = expiry_ok and trial_end <= expiry <= int(source_lane.get("expiry_epoch", 0) or 0)
        boundary_ok = (
            lane.get("observation_copy_enabled") is True
            and lane.get("automatic_revocation_enabled") is True
            and lane.get("live_canary_activation_enabled") is False
            and lane.get("live_response_influence_enabled") is False
            and lane.get("feedback_to_live_path_enabled") is False
            and lane.get("external_actuation_enabled") is False
            and lane.get("world_update_enabled") is False
            and lane.get("winner_selected") is False
            and lane.get("policy_boundary_preserved") is True
        )
        lane_boundary_breaches += not boundary_ok
        lane["source_lane_bound"] = bool(source_lane)
        lane["trial_end_epoch"] = trial_end
        lane["trial_boundary_preserved"] = boundary_ok
        enriched_lanes.append(lane)

    deterministic = redaction = rollback = revocation = restored = unchanged = delivered = 0
    event_boundary_breaches = 0
    maximum_latency = 0.0
    maximum_divergence = 0.0
    enriched_events: list[dict[str, Any]] = []
    for raw in events:
        event = dict(raw)
        replay_ok = event.get("trial_output_digest") == event.get("replay_output_digest")
        redaction_ok = event.get("redaction_receipt_digest") == event.get("expected_redaction_receipt_digest")
        rollback_ok = event.get("rollback_receipt_digest") == event.get("expected_rollback_receipt_digest")
        revocation_ok = event.get("revocation_receipt_digest") == event.get("expected_revocation_receipt_digest")
        restore_ok = event.get("replica_restored") is True
        live_ok = event.get("live_response_digest_before") == event.get("live_response_digest_after")
        delivery_ok = event.get("copy_delivered") is True and bool(event.get("copy_delivery_digest"))
        boundary_ok = (
            event.get("live_canary_activation_attempted") is False
            and event.get("feedback_to_live_path_attempted") is False
            and event.get("external_actuation_attempted") is False
            and event.get("world_update_attempted") is False
            and event.get("policy_boundary_preserved") is True
            and live_ok
        )
        deterministic += replay_ok
        redaction += redaction_ok
        rollback += rollback_ok
        revocation += revocation_ok and event.get("automatic_revocation_executed") is True
        restored += restore_ok
        unchanged += live_ok
        delivered += delivery_ok
        event_boundary_breaches += not boundary_ok
        maximum_latency = max(maximum_latency, number(event.get("latency_delta_ratio"), 1.0))
        maximum_divergence = max(maximum_divergence, number(event.get("output_divergence_score"), 1.0))
        event["deterministic_replay"] = replay_ok
        event["redaction_receipt_match"] = redaction_ok
        event["rollback_receipt_match"] = rollback_ok
        event["revocation_receipt_match"] = revocation_ok
        event["live_response_unchanged"] = live_ok
        event["trial_boundary_preserved"] = boundary_ok
        enriched_events.append(event)

    event_count = len(events)
    redaction_failure_ratio = clamp((event_count - redaction) / max(event_count, 1))
    live_influence_ratio = clamp((event_count - unchanged) / max(event_count, 1))
    delivery_failure_ratio = clamp((event_count - delivered) / max(event_count, 1))
    deterministic_ratio = clamp(deterministic / max(event_count, 1))
    rollback_ratio = clamp(rollback / max(event_count, 1))
    revocation_ratio = clamp(revocation / max(event_count, 1))
    restore_ratio = clamp(restored / max(event_count, 1))
    total_boundary_breaches = lane_boundary_breaches + event_boundary_breaches

    diversity_gates = {
        "minimum_plural_trial_lanes_present": lane_count >= int(policy.get("minimum_trial_lanes", 0)),
        "recovery_lane_preserved": recovery_count >= int(policy.get("minimum_recovery_lanes", 0)),
        "minority_lane_preserved": minority_count >= int(policy.get("minimum_minority_lanes", 0)),
        "all_trial_lanes_served": served == lane_count,
        "lane_service_ratio_sufficient": lane_service_ratio >= number(policy.get("minimum_lane_service_ratio")),
        "jain_fairness_sufficient": fairness >= number(policy.get("minimum_jain_fairness_index")),
        "allocation_error_bounded": maximum_allocation_error <= number(policy.get("maximum_allocation_error")),
    }
    trial_gates = {
        "maximum_trial_lane_count_bounded": lane_count <= int(policy.get("maximum_trial_lanes", 0)),
        "total_trial_fraction_bounded": total_fraction <= number(policy.get("maximum_total_trial_fraction")),
        "reported_total_trial_fraction_exact": abs(total_fraction - number(report.get("total_trial_fraction"))) <= 1e-8,
        "single_lane_fraction_bounded": maximum_lane_fraction <= number(policy.get("maximum_single_lane_fraction")),
        "source_lane_fraction_bounds_preserved": source_bounds_ok,
        "duration_bounded": duration <= int(policy.get("maximum_duration_seconds", 0)),
        "expiry_respected": expiry_ok,
        "total_event_budget_bounded": total_budget <= int(policy.get("maximum_event_budget", 0)),
        "per_lane_event_budget_bounded": lane_budget_ok,
        "event_count_within_budget": event_count <= total_budget,
        "latency_delta_bounded": maximum_latency <= number(policy.get("maximum_latency_delta_ratio")),
        "output_divergence_bounded": maximum_divergence <= number(policy.get("maximum_output_divergence_score")),
        "redaction_failure_ratio_bounded": redaction_failure_ratio <= number(
            policy.get("maximum_redaction_failure_ratio")
        ),
        "live_response_influence_absent": live_influence_ratio <= number(
            policy.get("maximum_live_response_influence_ratio")
        ),
        "copy_delivery_failure_ratio_bounded": delivery_failure_ratio <= number(
            policy.get("maximum_copy_delivery_failure_ratio")
        ),
        "rollback_receipts_complete": rollback_ratio >= number(policy.get("minimum_rollback_receipt_ratio")),
        "automatic_revocation_complete": revocation_ratio >= number(policy.get("minimum_revocation_ratio")),
        "replica_restore_complete": restore_ratio >= number(policy.get("minimum_replica_restore_ratio")),
        "deterministic_replay_complete": deterministic_ratio >= number(
            policy.get("minimum_deterministic_replay_ratio")
        ),
        "trial_boundary_preserved": total_boundary_breaches == 0,
    }
    return {
        "trial_lane_count": lane_count,
        "trial_event_count": event_count,
        "trial_lanes": enriched_lanes,
        "trial_events": enriched_events,
        "total_trial_fraction": round(total_fraction, 8),
        "maximum_single_lane_fraction": round(maximum_lane_fraction, 8),
        "total_event_budget": total_budget,
        "trial_duration_seconds": duration,
        "trial_end_epoch": trial_end,
        "target_allocation": target,
        "realized_allocation": {key: round(value, 8) for key, value in realized.items()},
        "allocation_error": allocation_errors,
        "maximum_allocation_error": maximum_allocation_error,
        "lane_service_ratio": lane_service_ratio,
        "jain_fairness_index": fairness,
        "maximum_latency_delta_ratio": round(maximum_latency, 8),
        "maximum_output_divergence_score": round(maximum_divergence, 8),
        "redaction_failure_ratio": redaction_failure_ratio,
        "live_response_influence_ratio": live_influence_ratio,
        "copy_delivery_failure_ratio": delivery_failure_ratio,
        "rollback_receipt_ratio": rollback_ratio,
        "automatic_revocation_ratio": revocation_ratio,
        "replica_restore_ratio": restore_ratio,
        "deterministic_replay_ratio": deterministic_ratio,
        "boundary_breach_count": total_boundary_breaches,
        "diversity_gates": diversity_gates,
        "trial_gates": trial_gates,
        "all_gates": {**diversity_gates, **trial_gates},
    }


def evaluate_trial(analysis: Mapping[str, Any], source_decision: str) -> tuple[str, str]:
    diversity = mapping(analysis.get("diversity_gates"))
    trial = mapping(analysis.get("trial_gates"))
    if source_decision in {"quarantine_recommended", "rollback_recommended", "hold_for_observation"}:
        return source_decision, f"source_v0_24_{source_decision}"
    if int(analysis.get("boundary_breach_count", 0)) > 0:
        return "quarantine_recommended", "canary_trial_live_intervention_boundary_breach"
    if source_decision == "extend_mirror_observation_recommended":
        return source_decision, "source_v0_24_more_mirror_evidence_required"
    if source_decision == "restore_shadow_diversity_recommended":
        return source_decision, "source_v0_24_shadow_diversity_restoration_required"
    if source_decision == "redesign_bounded_canary_observation_proposal_recommended":
        return "redesign_canary_observation_trial_recommended", "source_v0_24_canary_proposal_redesign_required"
    if source_decision == "bounded_canary_observation_proposal_ready" and not all(
        value is True for value in diversity.values()
    ):
        return "restore_shadow_diversity_recommended", "canary_trial_diversity_or_fairness_gate_failed"
    if source_decision == "bounded_canary_observation_proposal_ready" and all(
        value is True for value in trial.values()
    ):
        return "licensed_canary_observation_trial_ready", "bounded_isolated_revocable_canary_trial_ready"
    if source_decision == "bounded_canary_observation_proposal_ready":
        return "redesign_canary_observation_trial_recommended", "canary_trial_quality_or_recovery_gate_failed"
    return "quarantine_recommended", "unknown_source_v0_24_decision"
