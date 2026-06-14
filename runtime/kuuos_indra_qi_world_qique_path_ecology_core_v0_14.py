#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

PLAN_VERSION = "indra_qi_world_qique_path_ecology_plan_v0_14"
LICENSE_VERSION = "indra_qi_world_qique_path_ecology_license_v0_14"
STATE_VERSION = "indra_qi_world_qique_path_ecology_state_v0_14"
LEDGER_VERSION = "indra_qi_world_qique_path_ecology_ledger_record_v0_14"
WORLD_VERSION = "indra_qi_world_model_v0_1"
GOVERNANCE_STATE_VERSION = "indra_qi_generational_governance_state_v0_13"
GOVERNANCE_RECOMMENDATION_VERSION = "indra_qi_generational_governance_recommendation_v0_13"

DECISIONS = {
    "hold_for_observation",
    "ecology_compatible_bounded_promotion",
    "reopen_branches_recommended",
    "focus_or_reobserve_recommended",
    "rollback_recommended",
    "quarantine_recommended",
}
SOURCE_GOVERNANCE_DECISIONS = {
    "hold_for_observation",
    "promote_bounded",
    "rollback_recommended",
    "quarantine_recommended",
}

REQUIRED_BOUNDARY = {
    "source_world_state_required": True,
    "source_world_state_digest_exact": True,
    "source_v0_13_governance_required": True,
    "source_v0_13_digest_chain_exact": True,
    "world_source_read_only": True,
    "governance_source_read_only": True,
    "qique_is_derived_diagnostic_field": True,
    "licensed_localization_not_automatic_failure": True,
    "multi_world_noncollapse_preserved": True,
    "path_diversity_required_for_promotion": True,
    "false_stability_blocks_promotion": True,
    "holonomy_scar_visible": True,
    "candidate_weighting_not_truth": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "recommendation_only": True,
    "not_truth_authority": True,
    "not_world_update_authority": True,
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
    return sha(without(value, "path_ecology_plan_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "path_ecology_state_digest"))


def _bounded(policy: Mapping[str, Any], fields: Sequence[str], blockers: list[str], prefix: str) -> None:
    for field in fields:
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"{prefix}_{field}_invalid")


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("world_qique_plan_version_invalid")
    if str(plan.get("path_ecology_plan_digest", "")) != plan_digest(plan):
        blockers.append("world_qique_plan_digest_invalid")
    for field in (
        "ecology_id",
        "review_run_id",
        "world_model_id",
        "expected_source_world_state_digest",
        "expected_source_governance_state_digest",
        "expected_source_governance_recommendation_digest",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"world_qique_plan_{field}_missing")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"world_qique_boundary_{field}_mismatch")
    policy = mapping(plan.get("ecology_policy"))
    _bounded(
        policy,
        (
            "minimum_patch_participation_ratio",
            "maximum_flow_concentration",
            "maximum_overdiffusion_score",
            "maximum_loop_mode_lock",
            "minimum_branch_energy",
            "maximum_scar_reentry_score",
            "minimum_multi_world_diversity",
            "maximum_false_stability_pressure",
            "quarantine_false_stability_pressure",
            "licensed_localization_relief",
        ),
        blockers,
        "world_qique_policy",
    )
    if number(policy.get("maximum_false_stability_pressure"), 1.0) >= number(
        policy.get("quarantine_false_stability_pressure"), 0.0
    ):
        blockers.append("world_qique_false_stability_threshold_order_invalid")
    licensed = policy.get("licensed_localization_patch_ids", [])
    if not isinstance(licensed, list) or any(not isinstance(value, str) or not value for value in licensed):
        blockers.append("world_qique_licensed_localization_patch_ids_invalid")
    weights = mapping(policy.get("false_stability_weights"))
    _bounded(
        weights,
        ("localization", "branch_loss", "loop_lock", "scar_reentry", "diversity_loss"),
        blockers,
        "world_qique_false_stability_weights",
    )
    if abs(sum(number(weights.get(field)) for field in weights) - 1.0) > 1e-8 or set(weights) != {
        "localization",
        "branch_loss",
        "loop_lock",
        "scar_reentry",
        "diversity_loss",
    }:
        blockers.append("world_qique_false_stability_weights_sum_invalid")


def validate_license(
    license_value: Mapping[str, Any],
    plan: Mapping[str, Any],
    world_digest: str,
    governance_state_digest: str,
    recommendation_digest: str,
    blockers: list[str],
) -> None:
    expected = {
        "version": LICENSE_VERSION,
        "bound_path_ecology_plan_digest": str(plan.get("path_ecology_plan_digest", "")),
        "bound_source_world_state_digest": world_digest,
        "bound_source_governance_state_digest": governance_state_digest,
        "bound_source_governance_recommendation_digest": recommendation_digest,
    }
    for field, value in expected.items():
        if license_value.get(field) != value:
            blockers.append(f"world_qique_license_{field}_mismatch")
    if not str(license_value.get("license_id", "")):
        blockers.append("world_qique_license_id_missing")
    for field in (
        "state_write_allowed",
        "ledger_append_allowed",
        "recommendation_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(field) is not True:
            blockers.append(f"world_qique_license_{field}_not_true")
    for field in (
        "execution_authority_granted",
        "truth_authority_granted",
        "world_update_authority_granted",
        "direct_promotion_authority_granted",
        "direct_rollback_authority_granted",
        "direct_quarantine_authority_granted",
    ):
        if license_value.get(field) is not False:
            blockers.append(f"world_qique_license_{field}_not_false")


def validate_sources(
    world: Mapping[str, Any],
    governance_state: Mapping[str, Any],
    recommendation: Mapping[str, Any],
    plan: Mapping[str, Any],
    blockers: list[str],
) -> dict[str, Any]:
    if world.get("version") != WORLD_VERSION:
        blockers.append("world_qique_source_world_version_invalid")
    if not valid_digest(world, "indra_qi_world_state_digest"):
        blockers.append("world_qique_source_world_digest_invalid")
    if governance_state.get("version") != GOVERNANCE_STATE_VERSION:
        blockers.append("world_qique_source_governance_state_version_invalid")
    if not valid_digest(governance_state, "governance_state_digest"):
        blockers.append("world_qique_source_governance_state_digest_invalid")
    if recommendation.get("version") != GOVERNANCE_RECOMMENDATION_VERSION:
        blockers.append("world_qique_source_recommendation_version_invalid")
    if not valid_digest(recommendation, "recommendation_digest"):
        blockers.append("world_qique_source_recommendation_digest_invalid")

    world_digest = str(world.get("indra_qi_world_state_digest", ""))
    governance_digest = str(governance_state.get("governance_state_digest", ""))
    recommendation_digest = str(recommendation.get("recommendation_digest", ""))
    if plan.get("expected_source_world_state_digest") != world_digest:
        blockers.append("world_qique_expected_world_digest_mismatch")
    if plan.get("expected_source_governance_state_digest") != governance_digest:
        blockers.append("world_qique_expected_governance_state_digest_mismatch")
    if plan.get("expected_source_governance_recommendation_digest") != recommendation_digest:
        blockers.append("world_qique_expected_recommendation_digest_mismatch")
    if world.get("world_model_id") != plan.get("world_model_id"):
        blockers.append("world_qique_world_model_id_mismatch")
    if governance_state.get("latest_governance_decision") != recommendation.get("decision"):
        blockers.append("world_qique_governance_decision_mismatch")
    if governance_state.get("last_review_run_id") != recommendation.get("review_run_id"):
        blockers.append("world_qique_governance_review_run_id_mismatch")
    source_decision = str(recommendation.get("decision", ""))
    if source_decision not in SOURCE_GOVERNANCE_DECISIONS:
        blockers.append("world_qique_source_governance_decision_invalid")
    if recommendation.get("recommendation_only") is not True:
        blockers.append("world_qique_source_recommendation_not_advisory")
    for field in (
        "direct_execution_authority",
        "direct_promotion_authority",
        "direct_rollback_authority",
        "direct_quarantine_authority",
    ):
        if recommendation.get(field) is not False:
            blockers.append(f"world_qique_source_recommendation_{field}_not_false")
    mandala = mapping(world.get("mandala_inclusion"))
    if mandala.get("multi_world_noncollapse") is not True or mandala.get("single_ontology_forced") is not False:
        blockers.append("world_qique_source_multi_world_noncollapse_missing")
    return {
        "world_digest": world_digest,
        "governance_state_digest": governance_digest,
        "recommendation_digest": recommendation_digest,
        "source_governance_decision": source_decision,
        "source_governance_review_run_id": str(recommendation.get("review_run_id", "")),
    }


def _flow_weight(flow: Mapping[str, Any]) -> float:
    for field in ("effective_weight", "candidate_weight", "flow_weight", "weight"):
        raw = flow.get(field)
        if not isinstance(raw, bool) and isinstance(raw, (int, float)) and float(raw) > 0:
            return float(raw)
    return 1.0


def _entropy_ratio(weights: list[float]) -> float:
    positive = [value for value in weights if value > 0]
    if len(positive) <= 1:
        return 0.0
    total = sum(positive)
    probabilities = [value / total for value in positive]
    entropy = -sum(value * math.log(value) for value in probabilities)
    return clamp(entropy / math.log(len(positive)))


def compute_observables(world: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    patches = [mapping(value) for value in items(world.get("local_world_patches"))]
    connections = [mapping(value) for value in items(world.get("indra_connections"))]
    flows = [mapping(value) for value in items(world.get("qi_flow_channels"))]
    cycles = [mapping(value) for value in items(world.get("holonomy_cycles"))]
    patch_ids = [str(value.get("patch_id", "")) for value in patches if str(value.get("patch_id", ""))]
    connection_ids = [str(value.get("connection_id", "")) for value in connections if str(value.get("connection_id", ""))]
    weights = [_flow_weight(flow) for flow in flows]
    total_flow = sum(weights)

    patch_weight = {patch_id: 0.0 for patch_id in patch_ids}
    connection_weight = {connection_id: 0.0 for connection_id in connection_ids}
    outgoing: dict[str, set[str]] = {patch_id: set() for patch_id in patch_ids}
    used_connections: set[str] = set()
    for flow, weight in zip(flows, weights):
        source = str(flow.get("source_patch", ""))
        target = str(flow.get("target_patch", ""))
        connection = str(flow.get("connection_id", ""))
        if source in patch_weight:
            patch_weight[source] += weight / 2.0
        if target in patch_weight:
            patch_weight[target] += weight / 2.0
        if connection in connection_weight:
            connection_weight[connection] += weight
            used_connections.add(connection)
        if source in outgoing and target in patch_weight and source != target:
            outgoing[source].add(target)

    patch_values = list(patch_weight.values())
    patch_total = sum(patch_values)
    patch_count = len(patch_values)
    sum_squares = sum(value * value for value in patch_values)
    participation = clamp((patch_total * patch_total) / (patch_count * sum_squares)) if patch_count and sum_squares else 0.0
    dominant_patch = max(patch_weight, key=patch_weight.get) if patch_weight else ""
    dominant_patch_share = clamp(patch_weight.get(dominant_patch, 0.0) / patch_total) if patch_total else 0.0
    flow_concentration = clamp(max(weights) / total_flow) if weights and total_flow else 1.0
    connection_utilization = clamp(len(used_connections) / len(connection_ids)) if connection_ids else 0.0
    overdiffusion = clamp(participation * (1.0 - connection_utilization))

    n = len(patch_ids)
    branch_topology = (
        clamp(sum(len(targets) / max(n - 1, 1) for targets in outgoing.values()) / n)
        if n
        else 0.0
    )
    branch_energy = clamp(0.5 * branch_topology + 0.5 * _entropy_ratio(weights))

    loop_lock = 0.0
    residue_cycles = 0
    for cycle in cycles:
        cycle_connections = {str(value) for value in items(cycle.get("connection_ids"))}
        locked_weight = sum(connection_weight.get(connection_id, 0.0) for connection_id in cycle_connections)
        if total_flow:
            loop_lock = max(loop_lock, locked_weight / total_flow)
        if str(cycle.get("transport_residue_digest", "")):
            residue_cycles += 1
    loop_lock = clamp(loop_lock)
    residue_ratio = clamp(residue_cycles / len(cycles)) if cycles else 0.0
    scar_reentry = clamp(loop_lock * residue_ratio)

    mandala = mapping(world.get("mandala_inclusion"))
    mandala_factor = 1.0 if (
        mandala.get("multi_world_noncollapse") is True
        and mandala.get("single_ontology_forced") is False
        and mandala.get("contradiction_visibility_preserved") is True
    ) else 0.0
    diversity = clamp(mandala_factor * (0.6 * participation + 0.4 * branch_energy))

    licensed_patch_ids = {str(value) for value in items(policy.get("licensed_localization_patch_ids"))}
    licensed_localization_active = dominant_patch in licensed_patch_ids and bool(dominant_patch)
    localization = clamp(max(flow_concentration, 1.0 - participation))
    relief = number(policy.get("licensed_localization_relief")) if licensed_localization_active else 0.0
    effective_localization = clamp(localization - relief)

    weights_policy = mapping(policy.get("false_stability_weights"))
    false_stability = clamp(
        effective_localization * number(weights_policy.get("localization"))
        + (1.0 - branch_energy) * number(weights_policy.get("branch_loss"))
        + loop_lock * number(weights_policy.get("loop_lock"))
        + scar_reentry * number(weights_policy.get("scar_reentry"))
        + (1.0 - diversity) * number(weights_policy.get("diversity_loss"))
    )
    return {
        "patch_count": len(patches),
        "connection_count": len(connections),
        "qi_flow_count": len(flows),
        "holonomy_cycle_count": len(cycles),
        "patch_participation_ratio": participation,
        "dominant_patch_id": dominant_patch,
        "dominant_patch_share": dominant_patch_share,
        "flow_concentration": flow_concentration,
        "connection_utilization": connection_utilization,
        "overdiffusion_score": overdiffusion,
        "branch_topology_score": branch_topology,
        "branch_energy": branch_energy,
        "loop_mode_lock": loop_lock,
        "scar_reentry_score": scar_reentry,
        "multi_world_diversity": diversity,
        "licensed_localization_active": licensed_localization_active,
        "effective_localization_score": effective_localization,
        "false_stability_pressure": false_stability,
    }


def evaluate_ecology(
    observables: Mapping[str, Any],
    policy: Mapping[str, Any],
    source_governance_decision: str,
) -> dict[str, Any]:
    licensed = observables.get("licensed_localization_active") is True
    gates = {
        "patch_participation_sufficient": licensed
        or number(observables.get("patch_participation_ratio"))
        >= number(policy.get("minimum_patch_participation_ratio")),
        "flow_concentration_bounded": licensed
        or number(observables.get("flow_concentration"), 1.0)
        <= number(policy.get("maximum_flow_concentration")),
        "overdiffusion_bounded": number(observables.get("overdiffusion_score"), 1.0)
        <= number(policy.get("maximum_overdiffusion_score")),
        "loop_mode_lock_bounded": number(observables.get("loop_mode_lock"), 1.0)
        <= number(policy.get("maximum_loop_mode_lock")),
        "branch_energy_sufficient": number(observables.get("branch_energy"))
        >= number(policy.get("minimum_branch_energy")),
        "scar_reentry_bounded": number(observables.get("scar_reentry_score"), 1.0)
        <= number(policy.get("maximum_scar_reentry_score")),
        "multi_world_diversity_sufficient": number(observables.get("multi_world_diversity"))
        >= number(policy.get("minimum_multi_world_diversity")),
        "false_stability_bounded": number(observables.get("false_stability_pressure"), 1.0)
        <= number(policy.get("maximum_false_stability_pressure")),
    }
    false_stability = number(observables.get("false_stability_pressure"), 1.0)
    if source_governance_decision == "quarantine_recommended":
        decision, regime, reason = "quarantine_recommended", "WORLD_QIQUE_GOVERNANCE_QUARANTINE", "source_v0_13_quarantine_recommended"
    elif source_governance_decision == "rollback_recommended":
        decision, regime, reason = "rollback_recommended", "WORLD_QIQUE_GOVERNANCE_ROLLBACK", "source_v0_13_rollback_recommended"
    elif source_governance_decision == "hold_for_observation":
        decision, regime, reason = "hold_for_observation", "WORLD_QIQUE_OBSERVATION_HOLD", "source_v0_13_hold_for_observation"
    elif false_stability >= number(policy.get("quarantine_false_stability_pressure"), 1.0):
        decision, regime, reason = "quarantine_recommended", "WORLD_QIQUE_FALSE_STABILITY_QUARANTINE", "false_stability_at_or_above_quarantine_threshold"
    elif not gates["overdiffusion_bounded"]:
        decision, regime, reason = "focus_or_reobserve_recommended", "WORLD_QIQUE_OVERDIFFUSION", "world_flow_overdiffused"
    elif not all(gates.values()):
        scar_locked = not gates["loop_mode_lock_bounded"] and not gates["scar_reentry_bounded"]
        regime = "WORLD_QIQUE_SCAR_LOCKED" if scar_locked else "WORLD_QIQUE_LOCALIZED_OR_BRANCH_POOR"
        reason = "holonomy_scar_lock_detected" if scar_locked else "path_ecology_gate_failed"
        decision = "reopen_branches_recommended"
    else:
        decision, regime, reason = "ecology_compatible_bounded_promotion", "WORLD_QIQUE_BALANCED_BOUNDED_FLOW", "v0_13_promotion_and_world_path_ecology_compatible"
    return {
        "source_governance_decision": source_governance_decision,
        "qique_regime": regime,
        "decision": decision,
        "decision_reasons": [reason],
        "promotion_ecology_compatible": decision == "ecology_compatible_bounded_promotion",
        "gates": gates,
    }
