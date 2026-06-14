#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping

PLAN_VERSION = "indra_qi_post_assimilation_causal_reentry_plan_v0_7"
REQUIRED_BOUNDARY = {
    "post_assimilation_reentry_not_truth": True,
    "new_world_digest_required": True,
    "debt_conditions_causal_projection": True,
    "recoverability_conditions_causal_projection": True,
    "effective_transport_conditions_causal_projection": True,
    "base_connection_not_causal_edge": True,
    "qi_projected_as_observable_not_substance": True,
    "non_markov_feedback_preserved": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "causal_world_internal_only": True,
    "not_external_world_actuation_authority": True,
    "not_operator_algebra_mutation_authority": True,
    "not_world_update_authority": True,
    "new_projection_license_required": True,
    "fail_closed_on_boundary_loss": True,
}


def mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def valid_digest(value: Mapping[str, Any], field: str) -> bool:
    embedded = str(value.get(field, ""))
    return bool(embedded) and embedded == sha(without(value, field))


def reentry_plan_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "reentry_plan_digest"))


def clamp(value: float) -> float:
    return round(max(0.0, min(1.0, value)), 8)


def number(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return default
    return float(value)


def safe_name(value: str, prefix: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_]", "_", value).strip("_").lower()
    if not normalized:
        normalized = "signal"
    if normalized[0].isdigit():
        normalized = f"n_{normalized}"
    return f"{prefix}_{normalized}"[:96]


def validate_plan(plan: Mapping[str, Any], blockers: list[str]) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("post_assimilation_reentry_plan_version_invalid")
    if str(plan.get("reentry_plan_digest", "")) != reentry_plan_digest(plan):
        blockers.append("post_assimilation_reentry_plan_digest_invalid")
    for field in (
        "reentry_id",
        "source_assimilation_id",
        "source_assimilation_record_digest",
        "source_post_assimilation_seed_packet_digest",
        "source_world_state_digest",
        "projection_id",
        "causal_world_id",
        "transaction_id",
        "derived_response_patch_id",
    ):
        if not str(plan.get(field, "")).strip():
            blockers.append(f"post_assimilation_reentry_{field}_missing")
    if plan.get("reentry_mode") != "new_world_digest_causal_projection":
        blockers.append("post_assimilation_reentry_mode_invalid")
    boundary = mapping(plan.get("boundary"))
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"post_assimilation_reentry_boundary_{field}_mismatch")
    policy = mapping(plan.get("projection_policy"))
    for field in (
        "debt_uncertainty_gain",
        "residue_uncertainty_gain",
        "minimum_uncertainty",
        "maximum_uncertainty",
        "mechanism_weight_floor",
        "mechanism_weight_ceiling",
        "mechanism_noise_debt_gain",
    ):
        raw = policy.get(field)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or not 0 <= float(raw) <= 1:
            blockers.append(f"post_assimilation_reentry_policy_{field}_invalid")
    if number(policy.get("minimum_uncertainty")) > number(policy.get("maximum_uncertainty"), 1.0):
        blockers.append("post_assimilation_reentry_uncertainty_range_invalid")
    count = policy.get("minimum_seed_count")
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        blockers.append("post_assimilation_reentry_minimum_seed_count_invalid")
    maximum = policy.get("max_projection_variables")
    if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 2:
        blockers.append("post_assimilation_reentry_max_projection_variables_invalid")


def dynamic_state_map(world_state: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for field in ("local_patch_dynamic_states", "qi_flow_effective_states"):
        for raw in items(world_state.get(field)):
            state = mapping(raw)
            key = str(state.get("target_key", ""))
            if key:
                result[key] = state
    return result


def project_variable(
    *, seed: Mapping[str, Any], dynamic_state: Mapping[str, Any], policy: Mapping[str, Any]
) -> tuple[str, dict[str, Any]]:
    target = dict(mapping(seed.get("target")))
    is_flow = bool(str(target.get("flow_id", "")))
    observable_id = str(target.get("observable_id", "signal"))
    name = safe_name(observable_id, "flow" if is_flow else "patch")
    debt = clamp(number(dynamic_state.get("observation_debt")))
    residue = clamp(number(dynamic_state.get("intervention_residue")))
    uncertainty = clamp(
        number(policy.get("debt_uncertainty_gain"), 0.65) * debt
        + number(policy.get("residue_uncertainty_gain"), 0.35) * residue
    )
    uncertainty = max(
        number(policy.get("minimum_uncertainty"), 0.01),
        min(number(policy.get("maximum_uncertainty"), 0.95), uncertainty),
    )
    if is_flow:
        value = clamp(number(dynamic_state.get("effective_transport_coefficient")))
        binding = {
            "binding_kind": "qi_flow_observable_projection",
            "flow_id": str(target.get("flow_id", "")),
            "observable_id": observable_id,
            "source_digest": str(target.get("source_digest", "")),
            "qi_itself": False,
            "projection_not_flow_identity": True,
        }
    else:
        value = clamp(number(dynamic_state.get("effective_response_capacity")))
        binding = {
            "binding_kind": "local_patch_observable",
            "patch_id": str(target.get("patch_id", "")),
            "observable_id": observable_id,
            "source_digest": str(target.get("source_digest", "")),
        }
    return name, {
        "value": value,
        "uncertainty": round(uncertainty, 8),
        "status": "observed",
        "unit": "normalized",
        "source_binding": binding,
        "world_conditioning": {
            "source_post_assimilation_seed_entry_digest": str(seed.get("seed_entry_digest", "")),
            "source_dynamic_state_entry_digest": str(dynamic_state.get("dynamic_state_entry_digest", "")),
            "assimilated_prior_weight": seed.get("assimilated_prior_weight"),
            "observation_debt": debt,
            "recoverability_reserve": dynamic_state.get("recoverability_reserve"),
            "intervention_residue": residue,
            "relational_tension": dynamic_state.get("relational_tension"),
            "effective_capacity": value,
        },
    }


def mechanism_weight(seed: Mapping[str, Any], policy: Mapping[str, Any]) -> float:
    raw = number(seed.get("assimilated_prior_weight"))
    floor = number(policy.get("mechanism_weight_floor"), 0.10)
    ceiling = number(policy.get("mechanism_weight_ceiling"), 0.95)
    return round(max(floor, min(ceiling, raw)), 8)


def build_projection_plan(
    *,
    reentry_plan: Mapping[str, Any],
    world_state: Mapping[str, Any],
    seed_packet: Mapping[str, Any],
    blockers: list[str],
) -> tuple[dict[str, Any], dict[str, str]]:
    policy = mapping(reentry_plan.get("projection_policy"))
    seeds = [mapping(value) for value in items(seed_packet.get("seed_entries"))]
    minimum = int(policy.get("minimum_seed_count", 1) or 1)
    maximum = int(policy.get("max_projection_variables", 16) or 16)
    if len(seeds) < minimum:
        blockers.append("post_assimilation_reentry_seed_count_below_minimum")
    if len(seeds) + 1 > maximum:
        blockers.append("post_assimilation_reentry_projection_variable_limit_exceeded")

    dynamic = dynamic_state_map(world_state)
    variables: dict[str, dict[str, Any]] = {}
    source_names: dict[str, str] = {}
    weights: dict[str, float] = {}
    flow_count = 0
    uncertainties: list[float] = []
    for index, seed in enumerate(seeds):
        if not valid_digest(seed, "seed_entry_digest"):
            blockers.append(f"post_assimilation_reentry_seed_{index}_digest_invalid")
        key = str(seed.get("target_key", ""))
        state = dynamic.get(key, {})
        if not state:
            blockers.append(f"post_assimilation_reentry_seed_{index}_dynamic_state_missing")
            continue
        if str(seed.get("source_dynamic_state_entry_digest", "")) != str(
            state.get("dynamic_state_entry_digest", "")
        ):
            blockers.append(f"post_assimilation_reentry_seed_{index}_dynamic_digest_mismatch")
        name, variable = project_variable(seed=seed, dynamic_state=state, policy=policy)
        if name in variables:
            name = f"{name}_{index + 1}"
        variables[name] = variable
        source_names[key] = name
        weights[name] = mechanism_weight(seed, policy)
        uncertainties.append(number(variable.get("uncertainty")))
        if mapping(variable.get("source_binding")).get("binding_kind") == "qi_flow_observable_projection":
            flow_count += 1
    if flow_count <= 0:
        blockers.append("post_assimilation_reentry_qi_flow_seed_missing")

    patch_id = str(reentry_plan.get("derived_response_patch_id", ""))
    patch = next(
        (
            mapping(value)
            for value in items(world_state.get("local_world_patches"))
            if str(mapping(value).get("patch_id", "")) == patch_id
        ),
        {},
    )
    if not patch:
        blockers.append("post_assimilation_reentry_derived_patch_unknown")
    derived_name = "world_adaptive_response"
    variables[derived_name] = {
        "value": 0.0,
        "uncertainty": round(sum(uncertainties) / len(uncertainties), 8) if uncertainties else 1.0,
        "status": "derived",
        "unit": "normalized",
        "source_binding": {
            "binding_kind": "local_patch_observable",
            "patch_id": patch_id,
            "observable_id": str(reentry_plan.get("derived_response_observable_id", "world-adaptive-response")),
            "source_digest": str(patch.get("change_generator_digest", "")),
        },
        "world_conditioning": {
            "derived_from_post_assimilation_variables": list(weights),
            "source_world_dynamic_revision": world_state.get("world_dynamic_revision"),
        },
    }
    mechanisms = {
        derived_name: {
            "type": "affine",
            "parents": list(weights),
            "weights": weights,
            "bias": number(policy.get("mechanism_bias"), 0.0),
            "noise": clamp(
                number(policy.get("mechanism_noise_debt_gain"), 0.50)
                * (sum(uncertainties) / len(uncertainties) if uncertainties else 1.0)
            ),
        }
    }
    annotations = {
        f"{parent}->{derived_name}": {
            "edge_kind": "local_causal_projection_only",
            "not_indra_connection": True,
            "not_gauge_equivalence_claim": True,
            "not_qi_flow_identity": True,
        }
        for parent in weights
    }
    projection_plan = {
        "version": "indra_qi_causal_projection_plan_v0_2",
        "projection_id": str(reentry_plan.get("projection_id", "")),
        "source_world_model_id": str(world_state.get("world_model_id", "")),
        "source_indra_qi_world_state_digest": str(world_state.get("indra_qi_world_state_digest", "")),
        "causal_world_id": str(reentry_plan.get("causal_world_id", "")),
        "transaction_id": str(reentry_plan.get("transaction_id", "")),
        "variables": variables,
        "mechanisms": mechanisms,
        "edge_annotations": annotations,
        "boundary": {
            "projection_only_from_indra_substrate": True,
            "qi_projected_as_observable_not_substance": True,
            "causal_dag_not_complete_world_ontology": True,
            "causal_edge_not_gauge_connection": True,
            "source_indra_state_not_mutated": True,
            "not_external_world_actuation_authority": True,
            "not_operator_algebra_mutation_authority": True,
            "candidate_weighting_not_truth": True,
            "non_markov_feedback_preserved": True,
            "fail_closed_on_boundary_loss": True,
        },
    }
    return projection_plan, source_names
