#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_reversible_shadow_admission_plan_v0_17"
LICENSE_VERSION = "indra_qi_reversible_shadow_admission_license_v0_17"
PROPOSAL_VERSION = "indra_qi_reversible_shadow_admission_proposal_v0_17"
STATE_VERSION = "indra_qi_reversible_shadow_admission_state_v0_17"
LEDGER_VERSION = "indra_qi_reversible_shadow_admission_ledger_record_v0_17"
WORLD_VERSION = "indra_qi_world_model_v0_1"
CANDIDATE_SET_VERSION = "indra_qi_multi_lineage_candidate_set_v0_15"
TRIAL_STATE_VERSION = "indra_qi_licensed_sandbox_lineage_trial_state_v0_16"
TRIAL_RECOMMENDATION_VERSION = "indra_qi_licensed_sandbox_lineage_trial_recommendation_v0_16"

SOURCE_DECISIONS = {
    "hold_for_observation",
    "sandbox_trial_set_ready",
    "redesign_sandbox_trials_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "reversible_shadow_admission_ready",
    "redesign_shadow_roster_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_15_candidate_set_required": True,
    "source_v0_16_trial_required": True,
    "source_digest_chain_exact": True,
    "world_source_read_only": True,
    "candidate_set_source_read_only": True,
    "sandbox_trial_source_read_only": True,
    "shadow_admission_only": True,
    "shadow_roster_bounded": True,
    "shadow_cycles_bounded": True,
    "shadow_observation_budget_bounded": True,
    "shadow_weight_dominance_bounded": True,
    "rollback_corridor_required": True,
    "sandbox_pass_required": True,
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
    output = dict(value)
    output.pop(field, None)
    return output


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "shadow_admission_plan_digest"))


def proposal_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "shadow_admission_proposal_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "shadow_admission_state_digest"))


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
        blockers.append("shadow_admission_plan_version_invalid")
    if plan.get("shadow_admission_plan_digest") != plan_digest(plan):
        blockers.append("shadow_admission_plan_digest_invalid")
    for field in (
        "shadow_program_id",
        "admission_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_candidate_set_digest",
        "expected_source_trial_state_digest",
        "expected_source_trial_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"shadow_admission_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"shadow_admission_boundary_{field}_mismatch")
    policy = mapping(plan.get("shadow_policy"))
    _positive_int(
        policy,
        (
            "minimum_shadow_lineages",
            "maximum_shadow_lineages",
            "maximum_shadow_cycles",
            "maximum_observation_budget_per_lineage",
            "maximum_total_observation_budget",
            "minimum_distinct_lineage_kinds",
            "minimum_recovery_lineages",
            "minimum_minority_lineages",
        ),
        blockers,
        "shadow_admission_policy",
    )
    low = policy.get("minimum_shadow_lineages")
    high = policy.get("maximum_shadow_lineages")
    if isinstance(low, int) and isinstance(high, int) and (low > high or high > 8):
        blockers.append("shadow_admission_lineage_count_bounds_invalid")
    _bounded(policy, ("maximum_single_shadow_weight",), blockers, "shadow_admission_policy")
    for field in (
        "require_all_admitted_lineages_sandbox_passed",
        "require_rollback_corridor_match",
        "require_shadow_baseline",
        "require_shadow_overlay",
        "require_live_route_disabled",
        "require_external_actuation_disabled",
        "require_world_update_disabled",
        "require_policy_boundary_preserved",
    ):
        if policy.get(field) is not True:
            blockers.append(f"shadow_admission_policy_{field}_not_true")


def validate_sources(
    world: Mapping[str, Any],
    candidate_set: Mapping[str, Any],
    trial_state: Mapping[str, Any],
    trial_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION or not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("shadow_admission_source_world_invalid")
    if candidate_set.get("version") != CANDIDATE_SET_VERSION or not valid_digest(candidate_set, "candidate_set_digest"):
        blockers.append("shadow_admission_source_candidate_set_invalid")
    if trial_state.get("version") != TRIAL_STATE_VERSION or not valid_digest(trial_state, "sandbox_trial_state_digest"):
        blockers.append("shadow_admission_source_trial_state_invalid")
    if trial_recommendation.get("version") != TRIAL_RECOMMENDATION_VERSION or not valid_digest(
        trial_recommendation, "sandbox_trial_recommendation_digest"
    ):
        blockers.append("shadow_admission_source_trial_recommendation_invalid")

    world_sha = str(world.get("indra_qi_world_state_digest", ""))
    candidate_sha = str(candidate_set.get("candidate_set_digest", ""))
    state_sha = str(trial_state.get("sandbox_trial_state_digest", ""))
    recommendation_sha = str(trial_recommendation.get("sandbox_trial_recommendation_digest", ""))
    expected = {
        "expected_source_world_state_digest": world_sha,
        "expected_candidate_set_digest": candidate_sha,
        "expected_source_trial_state_digest": state_sha,
        "expected_source_trial_recommendation_digest": recommendation_sha,
    }
    for field, value in expected.items():
        if plan.get(field) != value:
            blockers.append(f"shadow_admission_{field}_mismatch")
    world_model_id = str(world.get("world_model_id", ""))
    if plan.get("world_model_id") != world_model_id:
        blockers.append("shadow_admission_world_model_id_mismatch")
    if candidate_set.get("world_model_id") != world_model_id or trial_state.get("world_model_id") != world_model_id or trial_recommendation.get("world_model_id") != world_model_id:
        blockers.append("shadow_admission_source_world_model_chain_invalid")
    if candidate_set.get("source_world_state_digest") != world_sha:
        blockers.append("shadow_admission_candidate_world_digest_mismatch")
    if trial_state.get("last_source_candidate_set_digest") != candidate_sha:
        blockers.append("shadow_admission_trial_state_candidate_set_digest_mismatch")
    if trial_recommendation.get("source_candidate_set_digest") != candidate_sha:
        blockers.append("shadow_admission_trial_recommendation_candidate_set_digest_mismatch")
    if trial_state.get("latest_sandbox_trial_decision") != trial_recommendation.get("decision"):
        blockers.append("shadow_admission_trial_decision_mismatch")
    if trial_state.get("last_trial_run_id") != trial_recommendation.get("trial_run_id"):
        blockers.append("shadow_admission_trial_run_id_mismatch")
    source_decision = str(trial_recommendation.get("decision", ""))
    if source_decision not in SOURCE_DECISIONS:
        blockers.append("shadow_admission_source_decision_invalid")
    if trial_recommendation.get("recommendation_only") is not True:
        blockers.append("shadow_admission_source_recommendation_not_advisory")
    for field in (
        "direct_lineage_selection_authority",
        "direct_lineage_execution_authority",
        "direct_world_update_authority",
        "direct_external_actuation_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
        "truth_authority",
    ):
        if trial_recommendation.get(field) is not False:
            blockers.append(f"shadow_admission_source_{field}_not_false")
    if candidate_set.get("candidate_weighting_not_truth") is not True or candidate_set.get("candidate_set_not_selection") is not True:
        blockers.append("shadow_admission_candidate_authority_boundary_invalid")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("shadow_admission_multi_world_noncollapse_missing")

    lineages: dict[str, dict[str, Any]] = {}
    for raw in items(candidate_set.get("candidate_lineages")):
        lineage = dict(mapping(raw))
        lineage_id = str(lineage.get("lineage_id", ""))
        if not lineage_id or lineage_id in lineages:
            blockers.append("shadow_admission_candidate_lineage_ids_invalid")
        else:
            lineages[lineage_id] = lineage
    trial_results = items(mapping(trial_recommendation.get("trial_analysis")).get("trial_results"))
    passed_lineages = {
        str(mapping(value).get("lineage_id", ""))
        for value in trial_results
        if mapping(value).get("trial_passed") is True
    }
    return {
        "world_digest": world_sha,
        "candidate_set_digest": candidate_sha,
        "trial_state_digest": state_sha,
        "trial_recommendation_digest": recommendation_sha,
        "source_decision": source_decision,
        "source_trial_run_id": str(trial_recommendation.get("trial_run_id", "")),
        "lineages": lineages,
        "passed_lineages": passed_lineages,
    }


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    proposal: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_shadow_admission_plan_digest": str(plan.get("shadow_admission_plan_digest", "")),
        "bound_shadow_admission_proposal_digest": str(proposal.get("shadow_admission_proposal_digest", "")),
        "bound_source_world_state_digest": str(source.get("world_digest", "")),
        "bound_candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "bound_source_trial_state_digest": str(source.get("trial_state_digest", "")),
        "bound_source_trial_recommendation_digest": str(source.get("trial_recommendation_digest", "")),
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"shadow_admission_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("shadow_admission_license_id_missing")
    for field in (
        "state_write_allowed",
        "shadow_roster_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"shadow_admission_license_{field}_not_true")
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
            blockers.append(f"shadow_admission_license_{field}_not_false")


def validate_proposal(
    proposal: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if proposal.get("version") != PROPOSAL_VERSION:
        blockers.append("shadow_admission_proposal_version_invalid")
    if proposal.get("admission_run_id") != plan.get("admission_run_id"):
        blockers.append("shadow_admission_proposal_run_id_mismatch")
    if proposal.get("source_candidate_set_digest") != source.get("candidate_set_digest"):
        blockers.append("shadow_admission_proposal_candidate_set_digest_mismatch")
    if proposal.get("source_trial_recommendation_digest") != source.get("trial_recommendation_digest"):
        blockers.append("shadow_admission_proposal_trial_recommendation_digest_mismatch")
    if proposal.get("shadow_admission_proposal_digest") != proposal_digest(proposal):
        blockers.append("shadow_admission_proposal_digest_invalid")
    raw_entries = proposal.get("shadow_entries")
    entries = [dict(mapping(value)) for value in raw_entries] if isinstance(raw_entries, list) else []
    if not entries:
        blockers.append("shadow_admission_entries_missing")
        return entries
    policy = mapping(plan.get("shadow_policy"))
    low = int(policy.get("minimum_shadow_lineages", 0) or 0)
    high = int(policy.get("maximum_shadow_lineages", 0) or 0)
    if len(entries) < low or len(entries) > high:
        blockers.append("shadow_admission_entry_count_out_of_bounds")
    seen_slots: set[str] = set()
    seen_lineages: set[str] = set()
    lineages = mapping(source.get("lineages"))
    for index, entry in enumerate(entries):
        slot = str(entry.get("shadow_slot_id", ""))
        lineage_id = str(entry.get("lineage_id", ""))
        if not slot or slot in seen_slots:
            blockers.append(f"shadow_admission_entry_{index}_slot_invalid")
        if not lineage_id or lineage_id in seen_lineages or lineage_id not in lineages:
            blockers.append(f"shadow_admission_entry_{index}_lineage_invalid")
        seen_slots.add(slot)
        seen_lineages.add(lineage_id)
        cycles = entry.get("requested_shadow_cycles")
        budget = entry.get("observation_budget")
        weight = entry.get("shadow_weight")
        if isinstance(cycles, bool) or not isinstance(cycles, int) or cycles <= 0:
            blockers.append(f"shadow_admission_entry_{index}_cycles_invalid")
        if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
            blockers.append(f"shadow_admission_entry_{index}_budget_invalid")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or float(weight) <= 0:
            blockers.append(f"shadow_admission_entry_{index}_weight_invalid")
        for field in ("rollback_corridor_digest", "shadow_baseline_digest", "shadow_overlay_digest"):
            if not str(entry.get(field, "")):
                blockers.append(f"shadow_admission_entry_{index}_{field}_missing")
        for field in (
            "live_route_enabled",
            "external_actuation_enabled",
            "world_update_enabled",
            "policy_boundary_preserved",
        ):
            if not isinstance(entry.get(field), bool):
                blockers.append(f"shadow_admission_entry_{index}_{field}_invalid")
    return entries


def analyze_roster(
    entries: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("shadow_policy"))
    lineages = mapping(source.get("lineages"))
    passed = set(source.get("passed_lineages", set()))
    raw_weights = [max(number(entry.get("shadow_weight")), 0.0) for entry in entries]
    total_weight = sum(raw_weights)
    normalized = [round(value / total_weight, 8) if total_weight else 0.0 for value in raw_weights]
    enriched: list[dict[str, Any]] = []
    boundary_breaches = 0
    rollback_matches = 0
    sandbox_passed = 0
    recovery_count = 0
    minority_count = 0
    kinds: set[str] = set()
    total_budget = 0
    cycle_budget_ok = True
    per_lineage_budget_ok = True
    reversible = True
    for raw, weight in zip(entries, normalized):
        entry = dict(raw)
        lineage_id = str(entry.get("lineage_id", ""))
        lineage = mapping(lineages.get(lineage_id))
        kind = str(lineage.get("lineage_kind", ""))
        kinds.add(kind)
        recovery_count += lineage.get("recovery_path") is True or kind == "recovery"
        minority_count += lineage.get("preserves_minority_path") is True or kind == "minority_preservation"
        rollback_match = str(entry.get("rollback_corridor_digest", "")) == str(lineage.get("rollback_corridor_digest", ""))
        rollback_matches += rollback_match
        passed_trial = lineage_id in passed
        sandbox_passed += passed_trial
        cycles = int(entry.get("requested_shadow_cycles", 0) or 0)
        budget = int(entry.get("observation_budget", 0) or 0)
        total_budget += budget
        cycle_budget_ok = cycle_budget_ok and cycles <= int(policy.get("maximum_shadow_cycles", 0))
        per_lineage_budget_ok = per_lineage_budget_ok and budget <= int(policy.get("maximum_observation_budget_per_lineage", 0))
        isolation = (
            entry.get("live_route_enabled") is False
            and entry.get("external_actuation_enabled") is False
            and entry.get("world_update_enabled") is False
            and entry.get("policy_boundary_preserved") is True
        )
        if not isolation:
            boundary_breaches += 1
        reversible = reversible and rollback_match and bool(entry.get("shadow_baseline_digest")) and bool(entry.get("shadow_overlay_digest"))
        entry["lineage_kind"] = kind
        entry["normalized_shadow_weight"] = weight
        entry["sandbox_trial_passed"] = passed_trial
        entry["rollback_corridor_match"] = rollback_match
        entry["shadow_isolation_preserved"] = isolation
        enriched.append(entry)
    count = len(entries)
    maximum_weight = clamp(max(normalized)) if normalized else 1.0
    gates = {
        "shadow_count_bounded": int(policy.get("minimum_shadow_lineages", 0)) <= count <= int(policy.get("maximum_shadow_lineages", 0)),
        "shadow_cycles_bounded": cycle_budget_ok,
        "per_lineage_observation_budget_bounded": per_lineage_budget_ok,
        "total_observation_budget_bounded": total_budget <= int(policy.get("maximum_total_observation_budget", 0)),
        "single_shadow_weight_bounded": maximum_weight <= number(policy.get("maximum_single_shadow_weight"), 0.0),
        "lineage_kind_diversity_sufficient": len(kinds) >= int(policy.get("minimum_distinct_lineage_kinds", 0)),
        "recovery_lineage_sufficient": recovery_count >= int(policy.get("minimum_recovery_lineages", 0)),
        "minority_lineage_sufficient": minority_count >= int(policy.get("minimum_minority_lineages", 0)),
        "rollback_corridors_exact": rollback_matches == count,
        "all_admitted_lineages_sandbox_passed": sandbox_passed == count,
        "shadow_isolation_preserved": boundary_breaches == 0,
        "reversibility_material_complete": reversible,
    }
    return {
        "shadow_lineage_count": count,
        "shadow_entries": enriched,
        "total_observation_budget": total_budget,
        "maximum_normalized_shadow_weight": maximum_weight,
        "distinct_lineage_kind_count": len(kinds),
        "recovery_lineage_count": recovery_count,
        "minority_lineage_count": minority_count,
        "sandbox_passed_lineage_count": sandbox_passed,
        "rollback_corridor_match_count": rollback_matches,
        "shadow_boundary_breach_count": boundary_breaches,
        "gates": gates,
    }


def evaluate_admission(analysis: Mapping[str, Any], source_decision: str) -> dict[str, Any]:
    gates = mapping(analysis.get("gates"))
    if source_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_16_quarantine_recommended"
    elif source_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_16_rollback_recommended"
    elif source_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_16_hold_for_observation"
    elif int(analysis.get("shadow_boundary_breach_count", 0)) > 0:
        decision, reason = "quarantine_recommended", "shadow_live_route_or_actuation_boundary_breach"
    elif source_decision == "redesign_sandbox_trials_recommended":
        decision, reason = "redesign_shadow_roster_recommended", "source_v0_16_trial_redesign_required"
    elif source_decision == "sandbox_trial_set_ready" and all(value is True for value in gates.values()):
        decision, reason = "reversible_shadow_admission_ready", "bounded_reversible_shadow_roster_ready"
    elif source_decision == "sandbox_trial_set_ready":
        decision, reason = "redesign_shadow_roster_recommended", "shadow_admission_gates_failed"
    else:
        decision, reason = "quarantine_recommended", "unknown_source_v0_16_decision"
    return {
        "source_trial_decision": source_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "shadow_roster_ready": decision == "reversible_shadow_admission_ready",
        "recommendation_only": True,
    }
