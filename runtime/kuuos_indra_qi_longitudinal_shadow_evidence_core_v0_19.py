#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_longitudinal_shadow_evidence_plan_v0_19"
LICENSE_VERSION = "indra_qi_longitudinal_shadow_evidence_license_v0_19"
REPORT_VERSION = "indra_qi_longitudinal_shadow_evidence_report_v0_19"
STATE_VERSION = "indra_qi_longitudinal_shadow_evidence_state_v0_19"
LEDGER_VERSION = "indra_qi_longitudinal_shadow_evidence_ledger_record_v0_19"
WORLD_VERSION = "indra_qi_world_model_v0_1"
COMPARISON_VERSION = "indra_qi_shadow_counterfactual_comparison_v0_18"
OBSERVATION_STATE_VERSION = "indra_qi_shadow_counterfactual_observation_state_v0_18"
OBSERVATION_RECOMMENDATION_VERSION = "indra_qi_shadow_counterfactual_observation_recommendation_v0_18"

BENEFIT_FIELDS = (
    "observation_debt_reduction",
    "recoverability_gain",
    "intervention_residue_reduction",
    "scar_pressure_reduction",
    "branch_energy_gain",
)
SOURCE_DECISIONS = {
    "hold_for_observation",
    "shadow_counterfactual_cycle_ready",
    "redesign_shadow_observation_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "longitudinal_shadow_evidence_ready",
    "extend_longitudinal_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_18_comparison_required": True,
    "source_v0_18_digest_chain_exact": True,
    "world_source_read_only": True,
    "counterfactual_source_read_only": True,
    "longitudinal_cycle_chain_required": True,
    "monotonic_cycle_index_required": True,
    "monotonic_epoch_required": True,
    "same_shadow_roster_required": True,
    "lineage_coverage_required": True,
    "persistent_frontier_plurality_required": True,
    "single_lineage_dominance_bounded": True,
    "single_lineage_only_streak_bounded": True,
    "sustained_benefit_required": True,
    "metric_volatility_bounded": True,
    "minority_persistence_preserved": True,
    "recovery_persistence_preserved": True,
    "winner_selection_forbidden": True,
    "live_route_disabled": True,
    "external_actuation_disabled": True,
    "world_update_disabled": True,
    "candidate_weighting_not_truth": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
    "not_lineage_selection_authority": True,
    "not_lineage_execution_authority": True,
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
    return sha(without(value, "longitudinal_evidence_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "longitudinal_evidence_report_digest"))


def cycle_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "cycle_evidence_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "longitudinal_evidence_state_digest"))


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
        blockers.append("longitudinal_plan_version_invalid")
    if plan.get("longitudinal_evidence_plan_digest") != plan_digest(plan):
        blockers.append("longitudinal_plan_digest_invalid")
    for field in (
        "evidence_program_id",
        "evidence_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_latest_comparison_digest",
        "expected_source_observation_state_digest",
        "expected_source_observation_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"longitudinal_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"longitudinal_boundary_{field}_mismatch")
    policy = mapping(plan.get("evidence_policy"))
    _positive_int(
        policy,
        (
            "minimum_evidence_cycles",
            "maximum_evidence_cycles",
            "minimum_persistent_frontier_lineages",
            "maximum_single_lineage_only_frontier_streak",
        ),
        blockers,
        "longitudinal_policy",
    )
    low = policy.get("minimum_evidence_cycles")
    high = policy.get("maximum_evidence_cycles")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 64):
        blockers.append("longitudinal_cycle_count_bounds_invalid")
    _bounded(
        policy,
        (
            "minimum_lineage_coverage_ratio",
            "minimum_persistent_frontier_ratio",
            "maximum_single_lineage_frontier_share",
            "minimum_sustained_benefit_ratio",
            "maximum_metric_volatility",
            "minimum_recovery_persistence_ratio",
            "minimum_minority_persistence_ratio",
        ),
        blockers,
        "longitudinal_policy",
    )
    for field in (
        "require_cycle_chain",
        "require_monotonic_cycle_index",
        "require_monotonic_epoch",
        "require_same_shadow_roster",
        "require_winner_selected_false",
        "require_live_route_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"longitudinal_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    comparison: Mapping[str, Any],
    observation_state: Mapping[str, Any],
    observation_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("longitudinal_source_world_invalid")
    if comparison.get("version") != COMPARISON_VERSION or not valid_digest(comparison, "counterfactual_comparison_digest"):
        blockers.append("longitudinal_source_comparison_invalid")
    if observation_state.get("version") != OBSERVATION_STATE_VERSION or not valid_digest(observation_state, "counterfactual_observation_state_digest"):
        blockers.append("longitudinal_source_observation_state_invalid")
    if observation_recommendation.get("version") != OBSERVATION_RECOMMENDATION_VERSION or not valid_digest(
        observation_recommendation, "counterfactual_observation_recommendation_digest"
    ):
        blockers.append("longitudinal_source_observation_recommendation_invalid")

    world_sha = str(world.get("indra_qi_world_state_digest", ""))
    comparison_sha = str(comparison.get("counterfactual_comparison_digest", ""))
    state_sha = str(observation_state.get("counterfactual_observation_state_digest", ""))
    recommendation_sha = str(observation_recommendation.get("counterfactual_observation_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_sha,
        "expected_latest_comparison_digest": comparison_sha,
        "expected_source_observation_state_digest": state_sha,
        "expected_source_observation_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"longitudinal_{field}_mismatch")
    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("longitudinal_world_model_id_mismatch")
    if comparison.get("world_model_id") != world_model_id or observation_state.get("world_model_id") != world_model_id or observation_recommendation.get("world_model_id") != world_model_id:
        blockers.append("longitudinal_source_world_model_chain_invalid")
    if comparison.get("source_world_state_digest") != world_sha:
        blockers.append("longitudinal_comparison_world_digest_mismatch")
    if observation_state.get("latest_counterfactual_comparison_digest") != comparison_sha:
        blockers.append("longitudinal_state_comparison_digest_mismatch")
    if observation_recommendation.get("counterfactual_comparison_digest") != comparison_sha:
        blockers.append("longitudinal_recommendation_comparison_digest_mismatch")
    if observation_state.get("latest_counterfactual_observation_decision") != observation_recommendation.get("decision"):
        blockers.append("longitudinal_source_decision_mismatch")
    if observation_state.get("last_observation_cycle_id") != observation_recommendation.get("observation_cycle_id"):
        blockers.append("longitudinal_source_cycle_id_mismatch")
    source_decision = str(observation_recommendation.get("decision", ""))
    if source_decision not in SOURCE_DECISIONS:
        blockers.append("longitudinal_source_decision_invalid")
    if observation_recommendation.get("recommendation_only") is not True or observation_recommendation.get("winner_selected") is not False:
        blockers.append("longitudinal_source_authority_boundary_invalid")
    for field in (
        "direct_live_route_authority",
        "direct_lineage_selection_authority",
        "direct_lineage_execution_authority",
        "direct_world_update_authority",
        "direct_external_actuation_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
        "truth_authority",
    ):
        if observation_recommendation.get(field) is not False:
            blockers.append(f"longitudinal_source_{field}_not_false")
    if comparison.get("winner_selected") is not False or comparison.get("pareto_frontier_not_winner_selection") is not True:
        blockers.append("longitudinal_comparison_winner_boundary_invalid")
    if comparison.get("live_route_enabled") is not False or comparison.get("external_actuation_enabled") is not False or comparison.get("world_update_enabled") is not False:
        blockers.append("longitudinal_comparison_route_boundary_invalid")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("longitudinal_multi_world_noncollapse_missing")
    return {
        "world_digest": world_sha,
        "latest_comparison_digest": comparison_sha,
        "observation_state_digest": state_sha,
        "observation_recommendation_digest": recommendation_sha,
        "source_decision": source_decision,
        "latest_cycle_id": str(observation_recommendation.get("observation_cycle_id", "")),
        "shadow_roster_digest": str(comparison.get("source_shadow_roster_digest", "")),
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
        "bound_longitudinal_evidence_plan_digest": str(plan.get("longitudinal_evidence_plan_digest", "")),
        "bound_longitudinal_evidence_report_digest": str(report.get("longitudinal_evidence_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_latest_comparison_digest": str(source.get("latest_comparison_digest", "")),
        "bound_source_observation_state_digest": str(source.get("observation_state_digest", "")),
        "bound_source_observation_recommendation_digest": str(source.get("observation_recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"longitudinal_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("longitudinal_license_id_missing")
    for field in (
        "state_write_allowed",
        "summary_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"longitudinal_license_{field}_not_true")
    for field in (
        "winner_selection_authority_granted",
        "live_route_authority_granted",
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
            blockers.append(f"longitudinal_license_{field}_not_false")


def _valid_vector(value: Mapping[str, Any]) -> bool:
    return all(
        not isinstance(value.get(field), bool)
        and isinstance(value.get(field), (int, float))
        and -1 <= float(value.get(field)) <= 1
        for field in BENEFIT_FIELDS
    )


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("longitudinal_report_version_invalid")
    if report.get("evidence_run_id") != plan.get("evidence_run_id"):
        blockers.append("longitudinal_report_run_id_mismatch")
    if report.get("latest_comparison_digest") != source.get("latest_comparison_digest"):
        blockers.append("longitudinal_report_latest_comparison_digest_mismatch")
    if report.get("source_observation_recommendation_digest") != source.get("observation_recommendation_digest"):
        blockers.append("longitudinal_report_recommendation_digest_mismatch")
    if report.get("longitudinal_evidence_report_digest") != report_digest(report):
        blockers.append("longitudinal_report_digest_invalid")
    raw_cycles = report.get("cycles")
    cycles = [dict(mapping(value)) for value in raw_cycles] if isinstance(raw_cycles, list) else []
    if not cycles:
        blockers.append("longitudinal_report_cycles_missing")
        return cycles
    policy = mapping(plan.get("evidence_policy"))
    low = int(policy.get("minimum_evidence_cycles", 0) or 0)
    high = int(policy.get("maximum_evidence_cycles", 0) or 0)
    if len(cycles) < low or len(cycles) > high:
        blockers.append("longitudinal_cycle_count_out_of_bounds")

    previous = "GENESIS"
    previous_epoch = -1
    seen_cycle_ids: set[str] = set()
    roster_digest = str(source.get("shadow_roster_digest", ""))
    latest_cycle_id = str(source.get("latest_cycle_id", ""))
    for index, cycle in enumerate(cycles):
        cycle_id = str(cycle.get("observation_cycle_id", ""))
        if not cycle_id or cycle_id in seen_cycle_ids:
            blockers.append(f"longitudinal_cycle_{index}_id_invalid")
        seen_cycle_ids.add(cycle_id)
        if cycle.get("cycle_index") != index + 1:
            blockers.append(f"longitudinal_cycle_{index}_index_invalid")
        epoch = cycle.get("epoch")
        if isinstance(epoch, bool) or not isinstance(epoch, int) or epoch <= previous_epoch:
            blockers.append(f"longitudinal_cycle_{index}_epoch_invalid")
        previous_epoch = int(epoch) if isinstance(epoch, int) and not isinstance(epoch, bool) else previous_epoch
        if cycle.get("prev_cycle_evidence_digest") != previous:
            blockers.append(f"longitudinal_cycle_{index}_chain_invalid")
        if cycle.get("cycle_evidence_digest") != cycle_digest(cycle):
            blockers.append(f"longitudinal_cycle_{index}_digest_invalid")
        previous = str(cycle.get("cycle_evidence_digest", ""))
        if cycle.get("source_shadow_roster_digest") != roster_digest:
            blockers.append(f"longitudinal_cycle_{index}_roster_digest_mismatch")
        for field in (
            "winner_selected",
            "live_route_attempted",
            "external_actuation_attempted",
            "world_update_attempted",
            "policy_boundary_preserved",
        ):
            if not isinstance(cycle.get(field), bool):
                blockers.append(f"longitudinal_cycle_{index}_{field}_invalid")
        frontier = [str(value) for value in items(cycle.get("pareto_frontier_lineage_ids")) if str(value)]
        observations = [dict(mapping(value)) for value in items(cycle.get("lineage_observations"))]
        if not frontier or not observations:
            blockers.append(f"longitudinal_cycle_{index}_evidence_missing")
        seen_lineages: set[str] = set()
        for obs_index, observation in enumerate(observations):
            lineage_id = str(observation.get("lineage_id", ""))
            if not lineage_id or lineage_id in seen_lineages:
                blockers.append(f"longitudinal_cycle_{index}_observation_{obs_index}_lineage_invalid")
            seen_lineages.add(lineage_id)
            if not str(observation.get("lineage_kind", "")):
                blockers.append(f"longitudinal_cycle_{index}_observation_{obs_index}_kind_missing")
            if not _valid_vector(mapping(observation.get("benefit_vector"))):
                blockers.append(f"longitudinal_cycle_{index}_observation_{obs_index}_vector_invalid")
            if observation.get("deterministic_replay") is not True:
                blockers.append(f"longitudinal_cycle_{index}_observation_{obs_index}_nondeterministic")
            if not str(observation.get("counterfactual_signature_digest", "")) or not str(observation.get("process_tensor_context_digest", "")) or not str(observation.get("non_markov_context_digest", "")):
                blockers.append(f"longitudinal_cycle_{index}_observation_{obs_index}_provenance_missing")
        if not set(frontier).issubset(seen_lineages):
            blockers.append(f"longitudinal_cycle_{index}_frontier_unknown_lineage")
    if cycles[-1].get("observation_cycle_id") != latest_cycle_id:
        blockers.append("longitudinal_latest_cycle_id_mismatch")
    if cycles[-1].get("source_comparison_digest") != source.get("latest_comparison_digest"):
        blockers.append("longitudinal_latest_comparison_digest_mismatch")
    return cycles


def _beneficial(vector: Mapping[str, Any]) -> bool:
    values = [number(vector.get(field), -1.0) for field in BENEFIT_FIELDS]
    return sum(values) > 0 and sum(value >= 0 for value in values) >= 3


def _max_streak(cycles: Sequence[Mapping[str, Any]]) -> int:
    best = 0
    current = 0
    current_lineage = ""
    for cycle in cycles:
        frontier = [str(value) for value in items(cycle.get("pareto_frontier_lineage_ids")) if str(value)]
        if len(frontier) == 1:
            lineage = frontier[0]
            if lineage == current_lineage:
                current += 1
            else:
                current_lineage = lineage
                current = 1
            best = max(best, current)
        else:
            current_lineage = ""
            current = 0
    return best


def analyze_longitudinal(cycles: Sequence[Mapping[str, Any]], plan: Mapping[str, Any]) -> dict[str, Any]:
    policy = mapping(plan.get("evidence_policy"))
    cycle_count = len(cycles)
    lineage_kinds: dict[str, str] = {}
    lineage_vectors: dict[str, list[dict[str, float]]] = defaultdict(list)
    frontier_counts: dict[str, int] = defaultdict(int)
    beneficial_counts: dict[str, int] = defaultdict(int)
    observation_counts: dict[str, int] = defaultdict(int)
    recovery_positive_cycles = 0
    minority_positive_cycles = 0
    boundary_breaches = 0
    total_frontier_memberships = 0

    for cycle in cycles:
        frontier = {str(value) for value in items(cycle.get("pareto_frontier_lineage_ids")) if str(value)}
        total_frontier_memberships += len(frontier)
        cycle_recovery_positive = False
        cycle_minority_positive = False
        if cycle.get("winner_selected") is not False or cycle.get("live_route_attempted") is not False or cycle.get("external_actuation_attempted") is not False or cycle.get("world_update_attempted") is not False or cycle.get("policy_boundary_preserved") is not True:
            boundary_breaches += 1
        for raw in items(cycle.get("lineage_observations")):
            observation = mapping(raw)
            lineage_id = str(observation.get("lineage_id", ""))
            kind = str(observation.get("lineage_kind", ""))
            vector = {field: number(mapping(observation.get("benefit_vector")).get(field)) for field in BENEFIT_FIELDS}
            lineage_kinds[lineage_id] = kind
            lineage_vectors[lineage_id].append(vector)
            observation_counts[lineage_id] += 1
            beneficial = _beneficial(vector)
            beneficial_counts[lineage_id] += beneficial
            frontier_counts[lineage_id] += lineage_id in frontier
            if kind == "recovery" and beneficial:
                cycle_recovery_positive = True
            if kind == "minority_preservation" and beneficial:
                cycle_minority_positive = True
        recovery_positive_cycles += cycle_recovery_positive
        minority_positive_cycles += cycle_minority_positive

    lineage_summaries: list[dict[str, Any]] = []
    maximum_volatility = 0.0
    persistent_lineages: list[str] = []
    total_observations = max(cycle_count, 1)
    for lineage_id in sorted(lineage_vectors):
        vectors = lineage_vectors[lineage_id]
        coverage_ratio = clamp(observation_counts[lineage_id] / total_observations)
        frontier_ratio = clamp(frontier_counts[lineage_id] / total_observations)
        beneficial_ratio = clamp(beneficial_counts[lineage_id] / total_observations)
        metric_volatility: dict[str, float] = {}
        metric_trend: dict[str, float] = {}
        for field in BENEFIT_FIELDS:
            values = [vector[field] for vector in vectors]
            volatility = max(values) - min(values) if values else 0.0
            metric_volatility[field] = round(volatility, 8)
            metric_trend[field] = round(values[-1] - values[0], 8) if values else 0.0
            maximum_volatility = max(maximum_volatility, volatility)
        if frontier_ratio >= number(policy.get("minimum_persistent_frontier_ratio")):
            persistent_lineages.append(lineage_id)
        lineage_summaries.append(
            {
                "lineage_id": lineage_id,
                "lineage_kind": lineage_kinds.get(lineage_id, ""),
                "coverage_ratio": coverage_ratio,
                "frontier_participation_ratio": frontier_ratio,
                "sustained_benefit_ratio": beneficial_ratio,
                "metric_volatility": metric_volatility,
                "metric_trend": metric_trend,
            }
        )

    lineage_count = len(lineage_vectors)
    minimum_coverage = min((summary["coverage_ratio"] for summary in lineage_summaries), default=0.0)
    aggregate_benefit_ratio = clamp(sum(beneficial_counts.values()) / max(cycle_count * lineage_count, 1))
    maximum_frontier_share = clamp(max(frontier_counts.values(), default=0) / max(total_frontier_memberships, 1))
    recovery_persistence = clamp(recovery_positive_cycles / max(cycle_count, 1))
    minority_persistence = clamp(minority_positive_cycles / max(cycle_count, 1))
    max_single_only_streak = _max_streak(cycles)
    collapse_gates = {
        "persistent_frontier_plurality_sufficient": len(persistent_lineages) >= int(policy.get("minimum_persistent_frontier_lineages", 0)),
        "single_lineage_frontier_share_bounded": maximum_frontier_share <= number(policy.get("maximum_single_lineage_frontier_share")),
        "single_lineage_only_frontier_streak_bounded": max_single_only_streak <= int(policy.get("maximum_single_lineage_only_frontier_streak", 0)),
    }
    evidence_gates = {
        "cycle_count_bounded": int(policy.get("minimum_evidence_cycles", 0)) <= cycle_count <= int(policy.get("maximum_evidence_cycles", 0)),
        "lineage_coverage_sufficient": minimum_coverage >= number(policy.get("minimum_lineage_coverage_ratio")),
        "sustained_benefit_sufficient": aggregate_benefit_ratio >= number(policy.get("minimum_sustained_benefit_ratio")),
        "metric_volatility_bounded": maximum_volatility <= number(policy.get("maximum_metric_volatility")),
        "recovery_persistence_sufficient": recovery_persistence >= number(policy.get("minimum_recovery_persistence_ratio")),
        "minority_persistence_sufficient": minority_persistence >= number(policy.get("minimum_minority_persistence_ratio")),
        "longitudinal_boundary_preserved": boundary_breaches == 0,
    }
    return {
        "cycle_count": cycle_count,
        "lineage_count": lineage_count,
        "lineage_summaries": lineage_summaries,
        "persistent_frontier_lineage_ids": persistent_lineages,
        "persistent_frontier_lineage_count": len(persistent_lineages),
        "minimum_lineage_coverage_ratio": minimum_coverage,
        "aggregate_sustained_benefit_ratio": aggregate_benefit_ratio,
        "maximum_metric_volatility": round(maximum_volatility, 8),
        "maximum_single_lineage_frontier_share": maximum_frontier_share,
        "maximum_single_lineage_only_frontier_streak": max_single_only_streak,
        "recovery_persistence_ratio": recovery_persistence,
        "minority_persistence_ratio": minority_persistence,
        "boundary_breach_count": boundary_breaches,
        "collapse_gates": collapse_gates,
        "evidence_gates": evidence_gates,
        "all_gates": {**collapse_gates, **evidence_gates},
    }


def evaluate_longitudinal(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    collapse_gates = mapping(analysis.get("collapse_gates"))
    evidence_gates = mapping(analysis.get("evidence_gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_18_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_18_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_18_hold_for_observation"
    elif int(analysis.get("boundary_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "longitudinal_route_or_actuation_boundary_breach"
    elif source_decision == "redesign_shadow_observation_recommended":
        decision, reason = "extend_longitudinal_observation_recommended", "source_v0_18_observation_redesign_required"
    elif source_decision == "shadow_counterfactual_cycle_ready" and not all(value is True for value in collapse_gates.values()):
        decision, reason = "restore_shadow_diversity_recommended", "longitudinal_single_lineage_collapse_pressure_detected"
    elif source_decision == "shadow_counterfactual_cycle_ready" and all(value is True for value in evidence_gates.values()):
        decision, reason = "longitudinal_shadow_evidence_ready", "persistent_improvement_without_collapse_observed"
    elif source_decision == "shadow_counterfactual_cycle_ready":
        decision, reason = "extend_longitudinal_observation_recommended", "longitudinal_evidence_stability_gates_incomplete"
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_18_decision"
    return {
        "source_counterfactual_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "longitudinal_evidence_ready": decision == "longitudinal_shadow_evidence_ready",
        "winner_selected": False,
        "recommendation_only": True,
    }
