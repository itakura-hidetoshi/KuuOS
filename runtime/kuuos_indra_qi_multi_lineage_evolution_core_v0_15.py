#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_multi_lineage_evolution_plan_v0_15"
LICENSE_VERSION = "indra_qi_multi_lineage_evolution_license_v0_15"
PROPOSAL_VERSION = "indra_qi_multi_lineage_proposal_v0_15"
STATE_VERSION = "indra_qi_multi_lineage_evolution_state_v0_15"
LEDGER_VERSION = "indra_qi_multi_lineage_evolution_ledger_record_v0_15"
WORLD_VERSION = "indra_qi_world_model_v0_1"
ECOLOGY_STATE_VERSION = "indra_qi_world_qique_path_ecology_state_v0_14"
ECOLOGY_RECOMMENDATION_VERSION = "indra_qi_world_qique_path_ecology_recommendation_v0_14"

SOURCE_ECOLOGY_DECISIONS = {
    "hold_for_observation",
    "ecology_compatible_bounded_promotion",
    "reopen_branches_recommended",
    "focus_or_reobserve_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
DECISIONS = {
    "hold_for_observation",
    "diverse_bounded_evolution_ready",
    "branch_reopening_candidate_set_ready",
    "focus_reobserve_candidate_set_ready",
    "redesign_candidate_set_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
LINEAGE_KINDS = {
    "explore",
    "recovery",
    "minority_preservation",
    "focus",
    "reobserve",
    "hold",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_14_path_ecology_required": True,
    "source_v0_14_digest_chain_exact": True,
    "world_source_read_only": True,
    "path_ecology_source_read_only": True,
    "candidate_set_bounded": True,
    "candidate_lineage_weights_not_truth": True,
    "single_lineage_dominance_bounded": True,
    "minority_lineage_preserved": True,
    "recovery_lineage_preserved": True,
    "reobserve_lineage_required_when_indicated": True,
    "holonomy_scar_avoidance_visible": True,
    "multi_world_noncollapse_preserved": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
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
    return sha(without(value, "evolution_plan_digest"))


def proposal_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "lineage_proposal_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "multi_lineage_state_digest"))


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("multi_lineage_plan_version_invalid")
    if str(plan.get("evolution_plan_digest", "")) != plan_digest(plan):
        blockers.append("multi_lineage_plan_digest_invalid")
    for field in (
        "evolution_id",
        "evolution_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_source_path_ecology_state_digest",
        "expected_source_path_ecology_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"multi_lineage_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"multi_lineage_boundary_{field}_mismatch")

    policy = mapping(plan.get("evolution_policy"))
    for field in (
        "minimum_candidate_lineages",
        "maximum_candidate_lineages",
        "maximum_path_length",
        "minimum_recovery_lineages",
        "minimum_minority_lineages",
        "minimum_reobserve_lineages",
        "minimum_dominant_patch_egress_lineages",
    ):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
            blockers.append(f"multi_lineage_policy_{field}_invalid")
    low = policy.get("minimum_candidate_lineages")
    high = policy.get("maximum_candidate_lineages")
    if isinstance(low, int) and isinstance(high, int):
        if low < 1 or low > high or high > 16:
            blockers.append("multi_lineage_candidate_count_bounds_invalid")
    if isinstance(policy.get("maximum_path_length"), int) and not 1 <= int(policy["maximum_path_length"]) <= 32:
        blockers.append("multi_lineage_maximum_path_length_out_of_bounds")

    _bounded(
        policy,
        (
            "maximum_single_lineage_weight",
            "maximum_pairwise_connection_overlap",
            "minimum_lineage_diversity_score",
            "minimum_target_patch_diversity",
            "minimum_holonomy_scar_avoidance_ratio",
        ),
        blockers,
        "multi_lineage_policy",
    )


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    proposal: Mapping[str, Any],
    world_digest: str,
    ecology_state_digest: str,
    ecology_recommendation_digest: str,
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_evolution_plan_digest": str(plan.get("evolution_plan_digest", "")),
        "bound_lineage_proposal_digest": str(proposal.get("lineage_proposal_digest", "")),
        "bound_source_world_state_digest": world_digest,
        "bound_source_path_ecology_state_digest": ecology_state_digest,
        "bound_source_path_ecology_recommendation_digest": ecology_recommendation_digest,
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"multi_lineage_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("multi_lineage_license_id_missing")
    for field in (
        "state_write_allowed",
        "candidate_set_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"multi_lineage_license_{field}_not_true")
    for field in (
        "execution_authority_granted",
        "truth_authority_granted",
        "world_update_authority_granted",
        "lineage_selection_authority_granted",
        "lineage_execution_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"multi_lineage_license_{field}_not_false")


def validate_sources(
    world: Mapping[str, Any],
    ecology_state: Mapping[str, Any],
    ecology_recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION:
        blockers.append("multi_lineage_source_world_version_invalid")
    if not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("multi_lineage_source_world_digest_invalid")
    if ecology_state.get("version") != ECOLOGY_STATE_VERSION:
        blockers.append("multi_lineage_source_ecology_state_version_invalid")
    if not valid_digest(ecology_state, "path_ecology_state_digest"):
        blockers.append("multi_lineage_source_ecology_state_digest_invalid")
    if ecology_recommendation.get("version") != ECOLOGY_RECOMMENDATION_VERSION:
        blockers.append("multi_lineage_source_ecology_recommendation_version_invalid")
    if not valid_digest(ecology_recommendation, "path_ecology_recommendation_digest"):
        blockers.append("multi_lineage_source_ecology_recommendation_digest_invalid")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    ecology_state_digest = str(ecology_state.get("path_ecology_state_digest", ""))
    ecology_recommendation_digest = str(ecology_recommendation.get("path_ecology_recommendation_digest", ""))
    if plan.get("expected_source_world_state_digest") != world_digest:
        blockers.append("multi_lineage_expected_world_digest_mismatch")
    if plan.get("expected_source_path_ecology_state_digest") != ecology_state_digest:
        blockers.append("multi_lineage_expected_ecology_state_digest_mismatch")
    if plan.get("expected_source_path_ecology_recommendation_digest") != ecology_recommendation_digest:
        blockers.append("multi_lineage_expected_ecology_recommendation_digest_mismatch")
    if world.get("world_model_id") != plan.get("world_model_id"):
        blockers.append("multi_lineage_world_model_id_mismatch")
    if ecology_state.get("world_model_id") != world.get("world_model_id"):
        blockers.append("multi_lineage_ecology_state_world_model_id_mismatch")
    if ecology_recommendation.get("world_model_id") != world.get("world_model_id"):
        blockers.append("multi_lineage_ecology_recommendation_world_model_id_mismatch")
    if ecology_state.get("latest_path_ecology_decision") != ecology_recommendation.get("decision"):
        blockers.append("multi_lineage_ecology_decision_mismatch")
    if ecology_state.get("last_review_run_id") != ecology_recommendation.get("review_run_id"):
        blockers.append("multi_lineage_ecology_review_run_id_mismatch")
    if ecology_state.get("last_source_world_state_digest") != world_digest:
        blockers.append("multi_lineage_ecology_state_world_digest_mismatch")
    if ecology_recommendation.get("source_world_state_digest") != world_digest:
        blockers.append("multi_lineage_ecology_recommendation_world_digest_mismatch")

    source_decision = str(ecology_recommendation.get("decision", ""))
    if source_decision not in SOURCE_ECOLOGY_DECISIONS:
        blockers.append("multi_lineage_source_ecology_decision_invalid")
    if ecology_recommendation.get("recommendation_only") is not True:
        blockers.append("multi_lineage_source_ecology_recommendation_not_advisory")
    for field in (
        "direct_execution_authority",
        "direct_world_update_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
    ):
        if ecology_recommendation.get(field) is not False:
            blockers.append(f"multi_lineage_source_ecology_{field}_not_false")
    mandala = mapping(world.get("mandala_inclusion"))
    if (
        mandala.get("multi_world_noncollapse") is not True
        or mandala.get("single_ontology_forced") is not False
    ):
        blockers.append("multi_lineage_source_multi_world_noncollapse_missing")
    return {
        "world_digest": world_digest,
        "ecology_state_digest": ecology_state_digest,
        "ecology_recommendation_digest": ecology_recommendation_digest,
        "source_ecology_decision": source_decision,
        "source_ecology_review_run_id": str(ecology_recommendation.get("review_run_id", "")),
        "dominant_patch_id": str(mapping(ecology_recommendation.get("qique_observables")).get("dominant_patch_id", "")),
        "qique_regime": str(ecology_recommendation.get("qique_regime", "")),
    }


def _connection_maps(world: Mapping[str, Any]) -> tuple[set[str], dict[str, tuple[str, str]]]:
    connection_ids: set[str] = set()
    endpoints: dict[str, tuple[str, str]] = {}
    for raw in items(world.get("indra_connections")):
        connection = mapping(raw)
        connection_id = str(connection.get("connection_id", ""))
        if connection_id:
            connection_ids.add(connection_id)
            endpoints[connection_id] = (
                str(connection.get("source_patch", "")),
                str(connection.get("target_patch", "")),
            )
    return connection_ids, endpoints


def _dominant_scar_cycle(world: Mapping[str, Any]) -> set[str]:
    flow_weight: dict[str, float] = {}
    for raw in items(world.get("qi_flow_channels")):
        flow = mapping(raw)
        connection_id = str(flow.get("connection_id", ""))
        weight = 1.0
        for field in ("effective_weight", "candidate_weight", "flow_weight", "weight"):
            candidate = flow.get(field)
            if not isinstance(candidate, bool) and isinstance(candidate, (int, float)) and float(candidate) > 0:
                weight = float(candidate)
                break
        if connection_id:
            flow_weight[connection_id] = flow_weight.get(connection_id, 0.0) + weight
    best: set[str] = set()
    best_weight = -1.0
    for raw in items(world.get("holonomy_cycles")):
        cycle = mapping(raw)
        connections = {str(value) for value in items(cycle.get("connection_ids")) if str(value)}
        weight = sum(flow_weight.get(connection_id, 0.0) for connection_id in connections)
        if weight > best_weight:
            best = connections
            best_weight = weight
    return best


def validate_proposal(
    proposal: Mapping[str, Any],
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> list[dict[str, Any]]:
    if proposal.get("version") != PROPOSAL_VERSION:
        blockers.append("multi_lineage_proposal_version_invalid")
    if proposal.get("evolution_run_id") != plan.get("evolution_run_id"):
        blockers.append("multi_lineage_proposal_run_id_mismatch")
    if proposal.get("source_world_state_digest") != source.get("world_digest"):
        blockers.append("multi_lineage_proposal_world_digest_mismatch")
    if proposal.get("source_path_ecology_recommendation_digest") != source.get("ecology_recommendation_digest"):
        blockers.append("multi_lineage_proposal_ecology_recommendation_digest_mismatch")
    if proposal.get("lineage_proposal_digest") != proposal_digest(proposal):
        blockers.append("multi_lineage_proposal_digest_invalid")

    policy = mapping(plan.get("evolution_policy"))
    raw_lineages = proposal.get("candidate_lineages")
    lineages = [dict(mapping(value)) for value in raw_lineages] if isinstance(raw_lineages, list) else []
    minimum = int(policy.get("minimum_candidate_lineages", 0) or 0)
    maximum = int(policy.get("maximum_candidate_lineages", 0) or 0)
    if len(lineages) < minimum or len(lineages) > maximum:
        blockers.append("multi_lineage_candidate_count_out_of_bounds")

    patch_ids = {
        str(mapping(value).get("patch_id", ""))
        for value in items(world.get("local_world_patches"))
        if str(mapping(value).get("patch_id", ""))
    }
    connection_ids, endpoints = _connection_maps(world)
    maximum_path_length = int(policy.get("maximum_path_length", 0) or 0)
    seen: set[str] = set()
    for index, lineage in enumerate(lineages):
        lineage_id = str(lineage.get("lineage_id", ""))
        if not lineage_id or lineage_id in seen:
            blockers.append(f"multi_lineage_candidate_{index}_lineage_id_invalid")
        seen.add(lineage_id)
        if lineage.get("lineage_kind") not in LINEAGE_KINDS:
            blockers.append(f"multi_lineage_candidate_{index}_kind_invalid")
        source_patch = str(lineage.get("source_patch", ""))
        target_patch = str(lineage.get("target_patch", ""))
        if source_patch not in patch_ids or target_patch not in patch_ids:
            blockers.append(f"multi_lineage_candidate_{index}_patch_unknown")
        path = [str(value) for value in items(lineage.get("connection_ids"))]
        if not path or len(path) > maximum_path_length or any(value not in connection_ids for value in path):
            blockers.append(f"multi_lineage_candidate_{index}_path_invalid")
        elif endpoints.get(path[0], ("", ""))[0] != source_patch or endpoints.get(path[-1], ("", ""))[1] != target_patch:
            blockers.append(f"multi_lineage_candidate_{index}_path_endpoint_mismatch")
        else:
            for left, right in zip(path, path[1:]):
                if endpoints.get(left, ("", ""))[1] != endpoints.get(right, ("", ""))[0]:
                    blockers.append(f"multi_lineage_candidate_{index}_path_not_contiguous")
                    break
        weight = lineage.get("candidate_weight")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)) or float(weight) <= 0:
            blockers.append(f"multi_lineage_candidate_{index}_candidate_weight_invalid")
        for field in (
            "rollback_corridor_digest",
            "observation_projection_digest",
            "process_tensor_context_digest",
            "non_markov_context_digest",
        ):
            if not str(lineage.get(field, "")).strip():
                blockers.append(f"multi_lineage_candidate_{index}_{field}_missing")
        for field in (
            "preserves_minority_path",
            "recovery_path",
            "reobserve_path",
        ):
            if not isinstance(lineage.get(field), bool):
                blockers.append(f"multi_lineage_candidate_{index}_{field}_invalid")
    return lineages


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def analyze_candidate_set(
    lineages: Sequence[Mapping[str, Any]],
    plan: Mapping[str, Any],
    world: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("evolution_policy"))
    values = [dict(lineage) for lineage in lineages]
    raw_weights = [max(number(lineage.get("candidate_weight")), 0.0) for lineage in values]
    total_weight = sum(raw_weights)
    normalized = [round(value / total_weight, 8) if total_weight else 0.0 for value in raw_weights]
    for lineage, weight in zip(values, normalized):
        lineage["normalized_candidate_weight"] = weight

    target_patches = {str(lineage.get("target_patch", "")) for lineage in values if str(lineage.get("target_patch", ""))}
    patch_ids = {
        str(mapping(value).get("patch_id", ""))
        for value in items(world.get("local_world_patches"))
        if str(mapping(value).get("patch_id", ""))
    }
    target_diversity = clamp(len(target_patches) / max(len(patch_ids), 1))
    kinds = {str(lineage.get("lineage_kind", "")) for lineage in values if str(lineage.get("lineage_kind", ""))}
    kind_diversity = clamp(len(kinds) / max(min(len(values), len(LINEAGE_KINDS)), 1)) if values else 0.0

    path_sets = [{str(value) for value in items(lineage.get("connection_ids"))} for lineage in values]
    overlaps: list[float] = []
    for index, left in enumerate(path_sets):
        for right in path_sets[index + 1 :]:
            overlaps.append(_jaccard(left, right))
    maximum_overlap = clamp(max(overlaps)) if overlaps else 0.0
    average_overlap = clamp(sum(overlaps) / len(overlaps)) if overlaps else 0.0
    lineage_diversity = clamp(0.5 * (1.0 - average_overlap) + 0.3 * target_diversity + 0.2 * kind_diversity)

    dominant_patch = str(source.get("dominant_patch_id", ""))
    recovery_count = sum(lineage.get("recovery_path") is True for lineage in values)
    minority_count = sum(
        lineage.get("preserves_minority_path") is True
        and str(lineage.get("target_patch", "")) != dominant_patch
        for lineage in values
    )
    reobserve_count = sum(lineage.get("reobserve_path") is True for lineage in values)
    focus_count = sum(lineage.get("lineage_kind") == "focus" for lineage in values)
    dominant_egress_count = sum(
        str(lineage.get("source_patch", "")) == dominant_patch
        and str(lineage.get("target_patch", "")) != dominant_patch
        for lineage in values
    )

    scar_cycle = _dominant_scar_cycle(world)
    scar_avoiding_count = sum(
        not path_set or not path_set.issubset(scar_cycle) for path_set in path_sets
    )
    scar_avoidance_ratio = clamp(scar_avoiding_count / len(path_sets)) if path_sets else 0.0
    maximum_weight = clamp(max(normalized)) if normalized else 1.0

    gates = {
        "candidate_count_bounded": int(policy.get("minimum_candidate_lineages", 0)) <= len(values) <= int(policy.get("maximum_candidate_lineages", 0)),
        "single_lineage_dominance_bounded": maximum_weight <= number(policy.get("maximum_single_lineage_weight")),
        "pairwise_connection_overlap_bounded": maximum_overlap <= number(policy.get("maximum_pairwise_connection_overlap")),
        "lineage_diversity_sufficient": lineage_diversity >= number(policy.get("minimum_lineage_diversity_score")),
        "target_patch_diversity_sufficient": target_diversity >= number(policy.get("minimum_target_patch_diversity")),
        "recovery_lineage_sufficient": recovery_count >= int(policy.get("minimum_recovery_lineages", 0)),
        "minority_lineage_sufficient": minority_count >= int(policy.get("minimum_minority_lineages", 0)),
        "reobserve_lineage_sufficient": reobserve_count >= int(policy.get("minimum_reobserve_lineages", 0)),
        "dominant_patch_egress_sufficient": dominant_egress_count >= int(policy.get("minimum_dominant_patch_egress_lineages", 0)),
        "holonomy_scar_avoidance_sufficient": scar_avoidance_ratio >= number(policy.get("minimum_holonomy_scar_avoidance_ratio")),
    }
    return {
        "candidate_count": len(values),
        "candidate_lineages": values,
        "maximum_normalized_candidate_weight": maximum_weight,
        "distinct_target_patch_count": len(target_patches),
        "target_patch_diversity": target_diversity,
        "lineage_kind_diversity": kind_diversity,
        "maximum_pairwise_connection_overlap": maximum_overlap,
        "average_pairwise_connection_overlap": average_overlap,
        "lineage_diversity_score": lineage_diversity,
        "recovery_lineage_count": recovery_count,
        "minority_lineage_count": minority_count,
        "reobserve_lineage_count": reobserve_count,
        "focus_lineage_count": focus_count,
        "dominant_patch_egress_lineage_count": dominant_egress_count,
        "holonomy_scar_avoidance_ratio": scar_avoidance_ratio,
        "gates": gates,
    }


def evaluate_evolution(
    analysis: Mapping[str, Any],
    source_ecology_decision: str,
) -> dict[str, Any]:
    gates = mapping(analysis.get("gates"))
    common = (
        gates.get("candidate_count_bounded") is True
        and gates.get("single_lineage_dominance_bounded") is True
        and gates.get("pairwise_connection_overlap_bounded") is True
        and gates.get("lineage_diversity_sufficient") is True
        and gates.get("target_patch_diversity_sufficient") is True
        and gates.get("holonomy_scar_avoidance_sufficient") is True
    )
    if source_ecology_decision == "quarantine_recommended":
        decision, reason = "quarantine_recommended", "source_v0_14_quarantine_recommended"
    elif source_ecology_decision == "rollback_recommended":
        decision, reason = "rollback_recommended", "source_v0_14_rollback_recommended"
    elif source_ecology_decision == "hold_for_observation":
        decision, reason = "hold_for_observation", "source_v0_14_hold_for_observation"
    elif source_ecology_decision == "focus_or_reobserve_recommended":
        ready = (
            common
            and gates.get("reobserve_lineage_sufficient") is True
            and int(analysis.get("focus_lineage_count", 0)) >= 1
        )
        decision = "focus_reobserve_candidate_set_ready" if ready else "redesign_candidate_set_recommended"
        reason = "focus_and_reobserve_lineages_ready" if ready else "focus_reobserve_candidate_requirements_failed"
    elif source_ecology_decision == "reopen_branches_recommended":
        ready = (
            common
            and gates.get("recovery_lineage_sufficient") is True
            and gates.get("minority_lineage_sufficient") is True
            and gates.get("dominant_patch_egress_sufficient") is True
        )
        decision = "branch_reopening_candidate_set_ready" if ready else "redesign_candidate_set_recommended"
        reason = "diverse_recoverable_branch_reopening_ready" if ready else "branch_reopening_candidate_requirements_failed"
    elif source_ecology_decision == "ecology_compatible_bounded_promotion":
        ready = (
            common
            and gates.get("recovery_lineage_sufficient") is True
            and gates.get("minority_lineage_sufficient") is True
        )
        decision = "diverse_bounded_evolution_ready" if ready else "redesign_candidate_set_recommended"
        reason = "bounded_multi_lineage_evolution_ready" if ready else "diversity_preservation_requirements_failed"
    else:
        decision, reason = "quarantine_recommended", "unknown_source_ecology_decision"
    return {
        "source_ecology_decision": source_ecology_decision,
        "decision": decision,
        "decision_reasons": [reason],
        "candidate_set_ready": decision in {
            "diverse_bounded_evolution_ready",
            "branch_reopening_candidate_set_ready",
            "focus_reobserve_candidate_set_ready",
        },
        "recommendation_only": True,
    }
