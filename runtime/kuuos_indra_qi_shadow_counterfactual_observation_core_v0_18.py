#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_shadow_counterfactual_observation_plan_v0_18"
LICENSE_VERSION = "indra_qi_shadow_counterfactual_observation_license_v0_18"
REPORT_VERSION = "indra_qi_shadow_counterfactual_observation_report_v0_18"
STATE_VERSION = "indra_qi_shadow_counterfactual_observation_state_v0_18"
LEDGER_VERSION = "indra_qi_shadow_counterfactual_observation_ledger_record_v0_18"
WORLD_VERSION = "indra_qi_world_model_v0_1"
ROSTER_VERSION = "indra_qi_reversible_shadow_roster_v0_17"
ADMISSION_STATE_VERSION = "indra_qi_reversible_shadow_admission_state_v0_17"
ADMISSION_RECOMMENDATION_VERSION = "indra_qi_reversible_shadow_admission_recommendation_v0_17"

METRICS = (
    "observation_debt",
    "recoverability_reserve",
    "intervention_residue",
    "scar_pressure",
    "branch_energy",
)
SOURCE_DECISIONS = {
    "hold_for_observation",
    "reversible_shadow_admission_ready",
    "redesign_shadow_roster_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "shadow_counterfactual_cycle_ready",
    "redesign_shadow_observation_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_17_shadow_roster_required": True,
    "source_v0_17_digest_chain_exact": True,
    "world_source_read_only": True,
    "shadow_source_read_only": True,
    "shared_observation_input_required": True,
    "shadow_baseline_binding_required": True,
    "shadow_overlay_binding_required": True,
    "deterministic_replay_required": True,
    "counterfactual_metrics_bounded": True,
    "pareto_frontier_not_winner_selection": True,
    "minority_projection_preserved": True,
    "recovery_projection_preserved": True,
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
    return sha(without(value, "counterfactual_observation_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "counterfactual_observation_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "counterfactual_observation_state_digest"))


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def _positive_int(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw <= 0:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("counterfactual_plan_version_invalid")
    if plan.get("counterfactual_observation_plan_digest") != plan_digest(plan):
        blockers.append("counterfactual_plan_digest_invalid")
    for field in (
        "observation_program_id",
        "observation_cycle_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_shadow_roster_digest",
        "expected_source_admission_state_digest",
        "expected_source_admission_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"counterfactual_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"counterfactual_boundary_{field}_mismatch")
    policy = mapping(plan.get("observation_policy"))
    _positive_int(
        policy,
        (
            "minimum_projection_lineages",
            "maximum_projection_lineages",
            "minimum_pareto_frontier_lineages",
            "minimum_distinct_counterfactual_signatures",
            "minimum_recovery_projections",
            "minimum_minority_projections",
        ),
        blockers,
        "counterfactual_policy",
    )
    low = policy.get("minimum_projection_lineages")
    high = policy.get("maximum_projection_lineages")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 8):
        blockers.append("counterfactual_projection_count_bounds_invalid")
    _bounded(
        policy,
        (
            "minimum_projection_coverage_ratio",
            "minimum_deterministic_replay_ratio",
            "maximum_adverse_metric_shift",
        ),
        blockers,
        "counterfactual_policy",
    )
    for field in (
        "require_shared_observation_input",
        "require_shadow_baseline_binding",
        "require_shadow_overlay_binding",
        "require_live_route_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"counterfactual_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    roster: Mapping[str, Any],
    admission_state: Mapping[str, Any],
    admission_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("counterfactual_source_world_invalid")
    if roster.get("version") != ROSTER_VERSION or not valid_digest(roster, "shadow_roster_digest"):
        blockers.append("counterfactual_source_roster_invalid")
    if admission_state.get("version") != ADMISSION_STATE_VERSION or not valid_digest(admission_state, "shadow_admission_state_digest"):
        blockers.append("counterfactual_source_admission_state_invalid")
    if admission_recommendation.get("version") != ADMISSION_RECOMMENDATION_VERSION or not valid_digest(
        admission_recommendation, "shadow_admission_recommendation_digest"
    ):
        blockers.append("counterfactual_source_admission_recommendation_invalid")

    world_sha = str(world.get("indra_qi_world_state_digest", ""))
    roster_sha = str(roster.get("shadow_roster_digest", ""))
    state_sha = str(admission_state.get("shadow_admission_state_digest", ""))
    recommendation_sha = str(admission_recommendation.get("shadow_admission_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_sha,
        "expected_shadow_roster_digest": roster_sha,
        "expected_source_admission_state_digest": state_sha,
        "expected_source_admission_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"counterfactual_{field}_mismatch")
    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("counterfactual_world_model_id_mismatch")
    if roster.get("world_model_id") != world_model_id or admission_state.get("world_model_id") != world_model_id or admission_recommendation.get("world_model_id") != world_model_id:
        blockers.append("counterfactual_source_world_model_chain_invalid")
    if roster.get("source_world_state_digest") != world_sha:
        blockers.append("counterfactual_roster_world_digest_mismatch")
    if admission_state.get("latest_shadow_roster_digest") != roster_sha:
        blockers.append("counterfactual_state_roster_digest_mismatch")
    if admission_recommendation.get("shadow_roster_digest") != roster_sha:
        blockers.append("counterfactual_recommendation_roster_digest_mismatch")
    if admission_state.get("latest_shadow_admission_decision") != admission_recommendation.get("decision"):
        blockers.append("counterfactual_source_decision_mismatch")
    if admission_state.get("last_admission_run_id") != admission_recommendation.get("admission_run_id"):
        blockers.append("counterfactual_source_run_id_mismatch")
    decision = str(admission_recommendation.get("decision", ""))
    if decision not in SOURCE_DECISIONS:
        blockers.append("counterfactual_source_decision_invalid")
    if admission_recommendation.get("recommendation_only") is not True:
        blockers.append("counterfactual_source_recommendation_not_advisory")
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
        if admission_recommendation.get(field) is not False:
            blockers.append(f"counterfactual_source_{field}_not_false")
    if roster.get("shadow_only") is not True or roster.get("live_route_enabled") is not False or roster.get("external_actuation_enabled") is not False or roster.get("world_update_enabled") is not False:
        blockers.append("counterfactual_roster_shadow_boundary_invalid")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("counterfactual_multi_world_noncollapse_missing")

    entries: dict[str, dict[str, Any]] = {}
    slots: set[str] = set()
    for raw in items(roster.get("shadow_entries")):
        entry = dict(mapping(raw))
        lineage_id = str(entry.get("lineage_id", ""))
        slot = str(entry.get("shadow_slot_id", ""))
        if not lineage_id or lineage_id in entries or not slot or slot in slots:
            blockers.append("counterfactual_shadow_entry_ids_invalid")
        else:
            entries[lineage_id] = entry
            slots.add(slot)
        if entry.get("sandbox_trial_passed") is not True or entry.get("rollback_corridor_match") is not True or entry.get("shadow_isolation_preserved") is not True:
            blockers.append("counterfactual_shadow_entry_not_admissible")
    if not entries:
        blockers.append("counterfactual_shadow_entries_missing")
    return {
        "world_digest": world_sha,
        "roster_digest": roster_sha,
        "admission_state_digest": state_sha,
        "admission_recommendation_digest": recommendation_sha,
        "source_decision": decision,
        "source_admission_run_id": str(admission_recommendation.get("admission_run_id", "")),
        "entries": entries,
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
        "bound_counterfactual_observation_plan_digest": str(plan.get("counterfactual_observation_plan_digest", "")),
        "bound_counterfactual_observation_report_digest": str(report.get("counterfactual_observation_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_shadow_roster_digest": str(source.get("roster_digest", "")),
        "bound_source_admission_state_digest": str(source.get("admission_state_digest", "")),
        "bound_source_admission_recommendation_digest": str(source.get("admission_recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"counterfactual_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("counterfactual_license_id_missing")
    for field in (
        "state_write_allowed",
        "comparison_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"counterfactual_license_{field}_not_true")
    for field in (
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
            blockers.append(f"counterfactual_license_{field}_not_false")


def _valid_metrics(value: Mapping[str, Any]) -> bool:
    return all(
        not isinstance(value.get(field), bool)
        and isinstance(value.get(field), (int, float))
        and 0 <= float(value.get(field)) <= 1
        for field in METRICS
    )


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("counterfactual_report_version_invalid")
    if report.get("observation_cycle_id") != plan.get("observation_cycle_id"):
        blockers.append("counterfactual_report_cycle_id_mismatch")
    if report.get("source_shadow_roster_digest") != source.get("roster_digest"):
        blockers.append("counterfactual_report_roster_digest_mismatch")
    if not str(report.get("shared_observation_input_digest", "")):
        blockers.append("counterfactual_report_shared_input_missing")
    if report.get("counterfactual_observation_report_digest") != report_digest(report):
        blockers.append("counterfactual_report_digest_invalid")
    raw_projections = report.get("projections")
    projections = [dict(mapping(value)) for value in raw_projections] if isinstance(raw_projections, list) else []
    if not projections:
        blockers.append("counterfactual_report_projections_missing")
        return projections
    entries = mapping(source.get("entries"))
    shared_input = str(report.get("shared_observation_input_digest", ""))
    seen_projection_ids: set[str] = set()
    seen_lineages: set[str] = set()
    for index, projection in enumerate(projections):
        projection_id = str(projection.get("projection_id", ""))
        lineage_id = str(projection.get("lineage_id", ""))
        entry = mapping(entries.get(lineage_id))
        if not projection_id or projection_id in seen_projection_ids:
            blockers.append(f"counterfactual_projection_{index}_projection_id_invalid")
        if not lineage_id or lineage_id in seen_lineages or lineage_id not in entries:
            blockers.append(f"counterfactual_projection_{index}_lineage_invalid")
        seen_projection_ids.add(projection_id)
        seen_lineages.add(lineage_id)
        if projection.get("shadow_slot_id") != entry.get("shadow_slot_id"):
            blockers.append(f"counterfactual_projection_{index}_shadow_slot_mismatch")
        if projection.get("observation_input_digest") != shared_input:
            blockers.append(f"counterfactual_projection_{index}_observation_input_mismatch")
        if projection.get("shadow_baseline_digest") != entry.get("shadow_baseline_digest"):
            blockers.append(f"counterfactual_projection_{index}_baseline_mismatch")
        if projection.get("shadow_overlay_digest") != entry.get("shadow_overlay_digest"):
            blockers.append(f"counterfactual_projection_{index}_overlay_mismatch")
        for field in (
            "output_digest",
            "replay_output_digest",
            "counterfactual_signature_digest",
            "process_tensor_context_digest",
            "non_markov_context_digest",
        ):
            if not str(projection.get(field, "")):
                blockers.append(f"counterfactual_projection_{index}_{field}_missing")
        if not _valid_metrics(mapping(projection.get("baseline_metrics"))) or not _valid_metrics(mapping(projection.get("projected_metrics"))):
            blockers.append(f"counterfactual_projection_{index}_metrics_invalid")
        cycle_index = projection.get("shadow_cycle_index")
        budget_used = projection.get("observation_budget_used")
        if isinstance(cycle_index, bool) or not isinstance(cycle_index, int) or cycle_index <= 0 or cycle_index > int(entry.get("requested_shadow_cycles", 0)):
            blockers.append(f"counterfactual_projection_{index}_cycle_index_invalid")
        if isinstance(budget_used, bool) or not isinstance(budget_used, int) or budget_used <= 0 or budget_used > int(entry.get("observation_budget", 0)):
            blockers.append(f"counterfactual_projection_{index}_budget_invalid")
        for field in (
            "live_route_attempted",
            "external_actuation_attempted",
            "world_update_attempted",
            "policy_boundary_preserved",
        ):
            if not isinstance(projection.get(field), bool):
                blockers.append(f"counterfactual_projection_{index}_{field}_invalid")
    return projections


def _benefit_vector(projection: Mapping[str, Any]) -> dict[str, float]:
    baseline = mapping(projection.get("baseline_metrics"))
    projected = mapping(projection.get("projected_metrics"))
    return {
        "observation_debt_reduction": round(number(baseline.get("observation_debt")) - number(projected.get("observation_debt")), 8),
        "recoverability_gain": round(number(projected.get("recoverability_reserve")) - number(baseline.get("recoverability_reserve")), 8),
        "intervention_residue_reduction": round(number(baseline.get("intervention_residue")) - number(projected.get("intervention_residue")), 8),
        "scar_pressure_reduction": round(number(baseline.get("scar_pressure")) - number(projected.get("scar_pressure")), 8),
        "branch_energy_gain": round(number(projected.get("branch_energy")) - number(baseline.get("branch_energy")), 8),
    }


def _dominates(left: Mapping[str, float], right: Mapping[str, float]) -> bool:
    keys = tuple(left.keys())
    return all(left[key] >= right[key] for key in keys) and any(left[key] > right[key] for key in keys)


def analyze_projections(
    projections: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("observation_policy"))
    entries = mapping(source.get("entries"))
    enriched: list[dict[str, Any]] = []
    covered: set[str] = set()
    deterministic_count = 0
    boundary_breaches = 0
    signatures: set[str] = set()
    recovery_count = 0
    minority_count = 0
    maximum_adverse_shift = 0.0
    vectors: dict[str, dict[str, float]] = {}
    for raw in projections:
        projection = dict(raw)
        lineage_id = str(projection.get("lineage_id", ""))
        entry = mapping(entries.get(lineage_id))
        covered.add(lineage_id)
        deterministic = projection.get("output_digest") == projection.get("replay_output_digest")
        deterministic_count += deterministic
        isolation = (
            projection.get("live_route_attempted") is False
            and projection.get("external_actuation_attempted") is False
            and projection.get("world_update_attempted") is False
            and projection.get("policy_boundary_preserved") is True
        )
        boundary_breaches += not isolation
        signature = str(projection.get("counterfactual_signature_digest", ""))
        if signature:
            signatures.add(signature)
        kind = str(entry.get("lineage_kind", ""))
        recovery_count += kind == "recovery"
        minority_count += kind == "minority_preservation"
        vector = _benefit_vector(projection)
        vectors[lineage_id] = vector
        adverse = max(0.0, *(-value for value in vector.values()))
        maximum_adverse_shift = max(maximum_adverse_shift, adverse)
        projection["lineage_kind"] = kind
        projection["deterministic_replay"] = deterministic
        projection["shadow_isolation_preserved"] = isolation
        projection["counterfactual_benefit_vector"] = vector
        projection["maximum_adverse_metric_shift"] = round(adverse, 8)
        enriched.append(projection)

    frontier: list[str] = []
    for lineage_id, vector in vectors.items():
        if not any(other_id != lineage_id and _dominates(other, vector) for other_id, other in vectors.items()):
            frontier.append(lineage_id)
    frontier.sort()
    denominator = max(len(entries), 1)
    projection_count = len(projections)
    coverage_ratio = clamp(len(covered) / denominator)
    deterministic_ratio = clamp(deterministic_count / projection_count) if projection_count else 0.0
    gates = {
        "projection_count_bounded": int(policy.get("minimum_projection_lineages", 0)) <= projection_count <= int(policy.get("maximum_projection_lineages", 0)),
        "projection_coverage_sufficient": coverage_ratio >= number(policy.get("minimum_projection_coverage_ratio")),
        "deterministic_replay_sufficient": deterministic_ratio >= number(policy.get("minimum_deterministic_replay_ratio")),
        "counterfactual_signatures_distinct": len(signatures) >= int(policy.get("minimum_distinct_counterfactual_signatures", 0)),
        "pareto_frontier_sufficient": len(frontier) >= int(policy.get("minimum_pareto_frontier_lineages", 0)),
        "recovery_projection_preserved": recovery_count >= int(policy.get("minimum_recovery_projections", 0)),
        "minority_projection_preserved": minority_count >= int(policy.get("minimum_minority_projections", 0)),
        "adverse_metric_shift_bounded": maximum_adverse_shift <= number(policy.get("maximum_adverse_metric_shift")),
        "shadow_isolation_preserved": boundary_breaches == 0,
    }
    return {
        "shadow_lineage_count": len(entries),
        "projection_count": projection_count,
        "covered_lineage_count": len(covered),
        "projection_coverage_ratio": coverage_ratio,
        "deterministic_projection_count": deterministic_count,
        "deterministic_replay_ratio": deterministic_ratio,
        "distinct_counterfactual_signature_count": len(signatures),
        "pareto_frontier_lineage_ids": frontier,
        "pareto_frontier_lineage_count": len(frontier),
        "recovery_projection_count": recovery_count,
        "minority_projection_count": minority_count,
        "maximum_adverse_metric_shift": round(maximum_adverse_shift, 8),
        "shadow_boundary_breach_count": boundary_breaches,
        "projections": enriched,
        "gates": gates,
    }


def evaluate_cycle(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    gates = mapping(analysis.get("gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_17_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_17_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_17_hold_for_observation"
    elif int(analysis.get("shadow_boundary_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "shadow_projection_live_route_or_actuation_boundary_breach"
    elif source_decision == "redesign_shadow_roster_recommended":
        decision, reason = "redesign_shadow_observation_recommended", "source_v0_17_shadow_roster_redesign_required"
    elif source_decision == "reversible_shadow_admission_ready" and all(value is True for value in gates.values()):
        decision, reason = "shadow_counterfactual_cycle_ready", "shared_input_counterfactual_comparison_ready"
    elif source_decision == "reversible_shadow_admission_ready":
        decision, reason = "redesign_shadow_observation_recommended", "counterfactual_observation_gates_failed"
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_17_decision"
    return {
        "source_shadow_admission_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "counterfactual_cycle_ready": decision == "shadow_counterfactual_cycle_ready",
        "winner_selected": False,
        "recommendation_only": True,
    }
