#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_bounded_plural_shadow_routing_plan_v0_20"
LICENSE_VERSION = "indra_qi_bounded_plural_shadow_routing_license_v0_20"
REPORT_VERSION = "indra_qi_bounded_plural_shadow_routing_report_v0_20"
STATE_VERSION = "indra_qi_bounded_plural_shadow_routing_state_v0_20"
LEDGER_VERSION = "indra_qi_bounded_plural_shadow_routing_ledger_record_v0_20"
WORLD_VERSION = "indra_qi_world_model_v0_1"
SUMMARY_VERSION = "indra_qi_longitudinal_shadow_evidence_summary_v0_19"
SOURCE_STATE_VERSION = "indra_qi_longitudinal_shadow_evidence_state_v0_19"
SOURCE_RECOMMENDATION_VERSION = "indra_qi_longitudinal_shadow_evidence_recommendation_v0_19"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "longitudinal_shadow_evidence_ready",
    "extend_longitudinal_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "plural_shadow_routing_proposal_ready",
    "redesign_plural_shadow_routing_proposal_recommended",
    "extend_longitudinal_observation_recommended",
    "restore_shadow_diversity_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_19_summary_required": True,
    "source_v0_19_digest_chain_exact": True,
    "world_source_read_only": True,
    "longitudinal_source_read_only": True,
    "proposal_only": True,
    "routing_activation_forbidden": True,
    "observation_traffic_bounded": True,
    "route_cycles_bounded": True,
    "route_observation_budget_bounded": True,
    "allocation_sum_exact": True,
    "single_lineage_allocation_bounded": True,
    "persistent_frontier_plurality_required": True,
    "recovery_lineage_preserved": True,
    "minority_lineage_preserved": True,
    "shadow_return_material_required": True,
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
    return sha(without(value, "plural_routing_plan_digest"))


def report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_routing_report_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plural_routing_state_digest"))


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
        blockers.append("plural_routing_plan_version_invalid")
    if plan.get("plural_routing_plan_digest") != plan_digest(plan):
        blockers.append("plural_routing_plan_digest_invalid")
    for field in (
        "routing_program_id",
        "proposal_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_longitudinal_summary_digest",
        "expected_source_longitudinal_state_digest",
        "expected_source_longitudinal_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"plural_routing_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"plural_routing_boundary_{field}_mismatch")

    policy = mapping(plan.get("routing_policy"))
    _positive_int(
        policy,
        (
            "minimum_routed_lineages",
            "maximum_routed_lineages",
            "minimum_recovery_lineages",
            "minimum_minority_lineages",
            "maximum_route_cycles",
            "maximum_observation_budget_per_lineage",
            "maximum_total_observation_budget",
        ),
        blockers,
        "plural_routing_policy",
    )
    low = policy.get("minimum_routed_lineages")
    high = policy.get("maximum_routed_lineages")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 8):
        blockers.append("plural_routing_lineage_count_bounds_invalid")
    _bounded(
        policy,
        (
            "minimum_route_share",
            "maximum_single_route_share",
            "maximum_total_observation_traffic_fraction",
            "minimum_persistent_frontier_coverage_ratio",
            "minimum_sustained_benefit_ratio",
        ),
        blockers,
        "plural_routing_policy",
    )
    if number(policy.get("minimum_route_share")) > number(policy.get("maximum_single_route_share")):
        blockers.append("plural_routing_share_bounds_invalid")
    for field in (
        "require_persistent_frontier_only",
        "require_recovery_lineage",
        "require_minority_lineage",
        "require_shadow_return_material",
        "require_proposal_only",
        "require_live_route_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"plural_routing_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    summary: Mapping[str, Any],
    source_state: Mapping[str, Any],
    source_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("plural_routing_source_world_invalid")
    if summary.get("version") != SUMMARY_VERSION or not valid_digest(summary, "longitudinal_evidence_summary_digest"):
        blockers.append("plural_routing_source_summary_invalid")
    if source_state.get("version") != SOURCE_STATE_VERSION or not valid_digest(source_state, "longitudinal_evidence_state_digest"):
        blockers.append("plural_routing_source_state_invalid")
    if source_recommendation.get("version") != SOURCE_RECOMMENDATION_VERSION or not valid_digest(
        source_recommendation, "longitudinal_evidence_recommendation_digest"
    ):
        blockers.append("plural_routing_source_recommendation_invalid")

    world_sha = str(world.get("indra_qi_world_state_digest", ""))
    summary_sha = str(summary.get("longitudinal_evidence_summary_digest", ""))
    state_sha = str(source_state.get("longitudinal_evidence_state_digest", ""))
    recommendation_sha = str(source_recommendation.get("longitudinal_evidence_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_sha,
        "expected_longitudinal_summary_digest": summary_sha,
        "expected_source_longitudinal_state_digest": state_sha,
        "expected_source_longitudinal_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"plural_routing_{field}_mismatch")

    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("plural_routing_world_model_id_mismatch")
    if (
        summary.get("world_model_id") != world_model_id
        or source_state.get("world_model_id") != world_model_id
        or source_recommendation.get("world_model_id") != world_model_id
    ):
        blockers.append("plural_routing_source_world_model_chain_invalid")
    if summary.get("source_world_state_digest") != world_sha:
        blockers.append("plural_routing_summary_world_digest_mismatch")
    if source_state.get("latest_longitudinal_evidence_summary_digest") != summary_sha:
        blockers.append("plural_routing_state_summary_digest_mismatch")
    if source_recommendation.get("longitudinal_evidence_summary_digest") != summary_sha:
        blockers.append("plural_routing_recommendation_summary_digest_mismatch")
    if source_state.get("latest_longitudinal_evidence_decision") != source_recommendation.get("decision"):
        blockers.append("plural_routing_source_decision_mismatch")
    if source_state.get("last_evidence_run_id") != source_recommendation.get("evidence_run_id"):
        blockers.append("plural_routing_source_run_id_mismatch")

    source_decision = str(source_recommendation.get("decision", ""))
    if source_decision not in SOURCE_DECISIONS:
        blockers.append("plural_routing_source_decision_invalid")
    if (
        source_recommendation.get("recommendation_only") is not True
        or source_recommendation.get("winner_selected") is not False
        or summary.get("winner_selected") is not False
    ):
        blockers.append("plural_routing_source_authority_boundary_invalid")
    for field in (
        "direct_winner_selection_authority",
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
        if source_recommendation.get(field) is not False:
            blockers.append(f"plural_routing_source_{field}_not_false")

    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("plural_routing_multi_world_noncollapse_missing")

    analysis = mapping(summary.get("longitudinal_analysis"))
    persistent_ids = {str(value) for value in items(analysis.get("persistent_frontier_lineage_ids")) if str(value)}
    lineage_summaries: dict[str, dict[str, Any]] = {}
    for raw in items(analysis.get("lineage_summaries")):
        lineage = dict(mapping(raw))
        lineage_id = str(lineage.get("lineage_id", ""))
        if not lineage_id or lineage_id in lineage_summaries:
            blockers.append("plural_routing_source_lineage_ids_invalid")
        else:
            lineage_summaries[lineage_id] = lineage
    if not persistent_ids or not persistent_ids.issubset(lineage_summaries):
        blockers.append("plural_routing_persistent_frontier_invalid")
    return {
        "world_digest": world_sha,
        "summary_digest": summary_sha,
        "state_digest": state_sha,
        "recommendation_digest": recommendation_sha,
        "source_decision": source_decision,
        "source_evidence_run_id": str(source_recommendation.get("evidence_run_id", "")),
        "persistent_lineage_ids": persistent_ids,
        "lineage_summaries": lineage_summaries,
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
        "bound_plural_routing_plan_digest": str(plan.get("plural_routing_plan_digest", "")),
        "bound_plural_routing_report_digest": str(report.get("plural_routing_report_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_longitudinal_summary_digest": str(source.get("summary_digest", "")),
        "bound_source_longitudinal_state_digest": str(source.get("state_digest", "")),
        "bound_source_longitudinal_recommendation_digest": str(source.get("recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"plural_routing_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("plural_routing_license_id_missing")
    for field in (
        "state_write_allowed",
        "proposal_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"plural_routing_license_{field}_not_true")
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
            blockers.append(f"plural_routing_license_{field}_not_false")


def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("plural_routing_report_version_invalid")
    if report.get("proposal_run_id") != plan.get("proposal_run_id"):
        blockers.append("plural_routing_report_run_id_mismatch")
    if report.get("source_longitudinal_summary_digest") != source.get("summary_digest"):
        blockers.append("plural_routing_report_summary_digest_mismatch")
    if report.get("source_longitudinal_recommendation_digest") != source.get("recommendation_digest"):
        blockers.append("plural_routing_report_recommendation_digest_mismatch")
    if report.get("proposal_only") is not True:
        blockers.append("plural_routing_report_not_proposal_only")
    if report.get("routing_activation_requested") is not False:
        blockers.append("plural_routing_report_activation_requested")
    if report.get("plural_routing_report_digest") != report_digest(report):
        blockers.append("plural_routing_report_digest_invalid")

    fraction = report.get("total_observation_traffic_fraction")
    if isinstance(fraction, bool) or not isinstance(fraction, (int, float)) or not 0 < float(fraction) <= 1:
        blockers.append("plural_routing_total_traffic_fraction_invalid")

    raw_entries = report.get("route_entries")
    entries = [dict(mapping(value)) for value in raw_entries] if isinstance(raw_entries, list) else []
    if not entries:
        blockers.append("plural_routing_entries_missing")
        return entries

    seen_slots: set[str] = set()
    seen_lineages: set[str] = set()
    lineage_summaries = mapping(source.get("lineage_summaries"))
    for index, entry in enumerate(entries):
        slot = str(entry.get("route_slot_id", ""))
        lineage_id = str(entry.get("lineage_id", ""))
        if not slot or slot in seen_slots:
            blockers.append(f"plural_routing_entry_{index}_slot_invalid")
        if not lineage_id or lineage_id in seen_lineages or lineage_id not in lineage_summaries:
            blockers.append(f"plural_routing_entry_{index}_lineage_invalid")
        seen_slots.add(slot)
        seen_lineages.add(lineage_id)

        share = entry.get("allocation_share")
        cycles = entry.get("requested_route_cycles")
        budget = entry.get("observation_budget")
        if isinstance(share, bool) or not isinstance(share, (int, float)) or not 0 < float(share) <= 1:
            blockers.append(f"plural_routing_entry_{index}_share_invalid")
        if isinstance(cycles, bool) or not isinstance(cycles, int) or cycles <= 0:
            blockers.append(f"plural_routing_entry_{index}_cycles_invalid")
        if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
            blockers.append(f"plural_routing_entry_{index}_budget_invalid")
        for field in ("shadow_return_token_digest", "route_overlay_digest", "observation_scope_digest"):
            if not str(entry.get(field, "")):
                blockers.append(f"plural_routing_entry_{index}_{field}_missing")
        for field in (
            "routing_activation_enabled",
            "live_route_enabled",
            "external_actuation_enabled",
            "world_update_enabled",
            "policy_boundary_preserved",
        ):
            if not isinstance(entry.get(field), bool):
                blockers.append(f"plural_routing_entry_{index}_{field}_invalid")
    return entries


def analyze_proposal(
    entries: Sequence[Mapping[str, Any]],
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("routing_policy"))
    lineage_summaries = mapping(source.get("lineage_summaries"))
    persistent = set(source.get("persistent_lineage_ids", set()))
    enriched: list[dict[str, Any]] = []
    total_share = sum(max(number(entry.get("allocation_share")), 0.0) for entry in entries)
    max_share = max((number(entry.get("allocation_share")) for entry in entries), default=1.0)
    min_share = min((number(entry.get("allocation_share")) for entry in entries), default=0.0)
    total_budget = 0
    recovery_count = 0
    minority_count = 0
    persistent_count = 0
    sustained_count = 0
    boundary_breaches = 0
    cycle_bounds = True
    budget_bounds = True

    for raw in entries:
        entry = dict(raw)
        lineage_id = str(entry.get("lineage_id", ""))
        summary = mapping(lineage_summaries.get(lineage_id))
        kind = str(summary.get("lineage_kind", ""))
        persistent_member = lineage_id in persistent
        persistent_count += persistent_member
        recovery_count += kind == "recovery"
        minority_count += kind == "minority_preservation"
        sustained = number(summary.get("sustained_benefit_ratio")) >= number(policy.get("minimum_sustained_benefit_ratio"))
        sustained_count += sustained
        cycles = int(entry.get("requested_route_cycles", 0) or 0)
        budget = int(entry.get("observation_budget", 0) or 0)
        total_budget += budget
        cycle_bounds = cycle_bounds and cycles <= int(policy.get("maximum_route_cycles", 0))
        budget_bounds = budget_bounds and budget <= int(policy.get("maximum_observation_budget_per_lineage", 0))
        boundary_ok = (
            entry.get("routing_activation_enabled") is False
            and entry.get("live_route_enabled") is False
            and entry.get("external_actuation_enabled") is False
            and entry.get("world_update_enabled") is False
            and entry.get("policy_boundary_preserved") is True
        )
        boundary_breaches += not boundary_ok
        entry["lineage_kind"] = kind
        entry["persistent_frontier_member"] = persistent_member
        entry["sustained_benefit_qualified"] = sustained
        entry["proposal_boundary_preserved"] = boundary_ok
        enriched.append(entry)

    count = len(entries)
    persistent_coverage_ratio = clamp(persistent_count / max(count, 1))
    diversity_gates = {
        "minimum_plural_lineages_present": count >= int(policy.get("minimum_routed_lineages", 0)),
        "single_lineage_allocation_bounded": max_share <= number(policy.get("maximum_single_route_share")),
        "recovery_lineage_preserved": recovery_count >= int(policy.get("minimum_recovery_lineages", 0)),
        "minority_lineage_preserved": minority_count >= int(policy.get("minimum_minority_lineages", 0)),
        "persistent_frontier_coverage_sufficient": persistent_coverage_ratio >= number(
            policy.get("minimum_persistent_frontier_coverage_ratio")
        ),
    }
    proposal_gates = {
        "maximum_lineage_count_bounded": count <= int(policy.get("maximum_routed_lineages", 0)),
        "allocation_sum_exact": abs(total_share - 1.0) <= 1e-8,
        "minimum_route_share_preserved": min_share >= number(policy.get("minimum_route_share")),
        "route_cycles_bounded": cycle_bounds,
        "per_lineage_observation_budget_bounded": budget_bounds,
        "total_observation_budget_bounded": total_budget <= int(policy.get("maximum_total_observation_budget", 0)),
        "total_observation_traffic_bounded": number(report.get("total_observation_traffic_fraction"))
        <= number(policy.get("maximum_total_observation_traffic_fraction")),
        "all_routed_lineages_persistent": persistent_count == count,
        "all_routed_lineages_sustained": sustained_count == count,
        "proposal_boundary_preserved": boundary_breaches == 0,
        "routing_activation_not_requested": report.get("routing_activation_requested") is False,
        "proposal_only": report.get("proposal_only") is True,
    }
    return {
        "route_lineage_count": count,
        "route_entries": enriched,
        "allocation_sum": round(total_share, 8),
        "maximum_route_share": round(max_share, 8),
        "minimum_route_share": round(min_share, 8),
        "total_observation_traffic_fraction": number(report.get("total_observation_traffic_fraction")),
        "total_observation_budget": total_budget,
        "persistent_frontier_coverage_ratio": persistent_coverage_ratio,
        "recovery_lineage_count": recovery_count,
        "minority_lineage_count": minority_count,
        "sustained_lineage_count": sustained_count,
        "boundary_breach_count": boundary_breaches,
        "diversity_gates": diversity_gates,
        "proposal_gates": proposal_gates,
        "all_gates": {**diversity_gates, **proposal_gates},
    }


def evaluate_proposal(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    diversity_gates = mapping(analysis.get("diversity_gates"))
    proposal_gates = mapping(analysis.get("proposal_gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_19_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_19_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_19_hold_for_observation"
    elif int(analysis.get("boundary_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "routing_activation_or_actuation_boundary_breach"
    elif source_decision == "extend_longitudinal_observation_recommended":
        decision, reason = "extend_longitudinal_observation_recommended", "source_v0_19_more_longitudinal_evidence_required"
    elif source_decision == "restore_shadow_diversity_recommended":
        decision, reason = "restore_shadow_diversity_recommended", "source_v0_19_shadow_diversity_restoration_required"
    elif source_decision == "longitudinal_shadow_evidence_ready" and not all(
        value is True for value in diversity_gates.values()
    ):
        decision, reason = "restore_shadow_diversity_recommended", "plural_routing_diversity_gates_failed"
    elif source_decision == "longitudinal_shadow_evidence_ready" and all(
        value is True for value in proposal_gates.values()
    ):
        decision, reason = "plural_shadow_routing_proposal_ready", "bounded_plural_observation_routing_proposal_ready"
    elif source_decision == "longitudinal_shadow_evidence_ready":
        decision, reason = (
            "redesign_plural_shadow_routing_proposal_recommended",
            "plural_routing_budget_or_integrity_gates_failed",
        )
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_19_decision"
    return {
        "source_longitudinal_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "proposal_ready": decision == "plural_shadow_routing_proposal_ready",
        "routing_activated": False,
        "winner_selected": False,
        "recommendation_only": True,
    }
