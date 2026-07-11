#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-10
WORLD_KIND = "indra_qi_mandala_causal_projection"


@dataclass
class WorldConditionedPathProjectionPullbackMetricResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def finite(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=TOL)


def normalize_weights(entries: list[dict], key: str) -> list[dict]:
    return sorted(({key: str(e[key]), "weight": float(e["weight"])} for e in entries), key=lambda e: e[key])


def compute_plan_coordinate_schema_digest(entries: list[dict]) -> str:
    return canonical_digest([e["coordinate"] for e in normalize_weights(entries, "coordinate")])


def compute_conditioned_plan_metric_digest(entries: list[dict]) -> str:
    return canonical_digest(normalize_weights(entries, "coordinate"))


def compute_world_coordinate_schema_digest(entries: list[dict]) -> str:
    return canonical_digest([e["world_coordinate"] for e in normalize_weights(entries, "world_coordinate")])


def compute_world_metric_digest(entries: list[dict]) -> str:
    return canonical_digest(normalize_weights(entries, "world_coordinate"))


def compute_world_binding_digest(**fields: Any) -> str:
    return canonical_digest(fields)


def compute_candidate_world_projection_digest(candidate: dict) -> str:
    payload = dict(candidate)
    payload.pop("candidate_world_projection_digest", None)
    return canonical_digest(payload)


def validate_weights(entries: Any, key: str, prefix: str, positive: bool) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(entries, list) or not entries:
        return [f"empty_{prefix}_weights"], []
    normalized: list[dict] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {key, "weight"}:
            blockers.append(f"invalid_{prefix}_entry_{index}")
            continue
        coordinate, weight = entry[key], entry["weight"]
        if not isinstance(coordinate, str) or not coordinate.strip():
            blockers.append(f"invalid_{prefix}_coordinate_{index}")
            continue
        coordinate = coordinate.strip()
        if coordinate in seen:
            blockers.append(f"duplicate_{prefix}_coordinate")
        seen.add(coordinate)
        if not finite(weight):
            blockers.append(f"invalid_{prefix}_weight_{index}")
            continue
        weight = float(weight)
        if (positive and weight <= 0.0) or (not positive and weight < 0.0):
            blockers.append(f"invalid_{prefix}_weight_{index}")
        normalized.append({key: coordinate, "weight": weight})
    normalized.sort(key=lambda e: e[key])
    if not positive and normalized and not any(e["weight"] > 0.0 for e in normalized):
        blockers.append("world_metric_all_zero")
    return blockers, normalized


def build_world_conditioned_path_projection_pullback_metric_certificate(
    *,
    source_qi_conditioned_metric_certificate_digest: str,
    world_model_kind: str,
    world_model_state_digest: str,
    world_model_revision: int,
    world_lineage_digest: str,
    world_patch_id: str,
    world_patch_projection_digest: str,
    observation_operator_digest: str,
    causal_graph_digest: str,
    causal_variable_schema_digest: str,
    causal_state_digest: str,
    uncertainty_state_digest: str,
    active_interventions_digest: str,
    process_tensor_context_digest: str,
    history_window_digest: str,
    holonomy_context_digest: str,
    transport_residue_digest: str,
    world_binding_digest: str,
    plan_coordinate_schema_digest: str,
    conditioned_plan_metric_digest: str,
    conditioned_plan_metric_weights: list[dict],
    world_coordinate_schema_digest: str,
    world_metric_digest: str,
    world_metric_weights: list[dict],
    pullback_weight: float,
    candidate_projections: list[dict],
) -> WorldConditionedPathProjectionPullbackMetricResult:
    blockers: list[str] = []
    binding_fields = {
        "world_model_kind": world_model_kind,
        "world_model_state_digest": world_model_state_digest,
        "world_model_revision": world_model_revision,
        "world_lineage_digest": world_lineage_digest,
        "world_patch_id": world_patch_id,
        "world_patch_projection_digest": world_patch_projection_digest,
        "observation_operator_digest": observation_operator_digest,
        "causal_graph_digest": causal_graph_digest,
        "causal_variable_schema_digest": causal_variable_schema_digest,
        "causal_state_digest": causal_state_digest,
        "uncertainty_state_digest": uncertainty_state_digest,
        "active_interventions_digest": active_interventions_digest,
        "process_tensor_context_digest": process_tensor_context_digest,
        "history_window_digest": history_window_digest,
        "holonomy_context_digest": holonomy_context_digest,
        "transport_residue_digest": transport_residue_digest,
    }
    text_fields = {
        "source_qi_conditioned_metric_certificate_digest": source_qi_conditioned_metric_certificate_digest,
        "world_binding_digest": world_binding_digest,
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "conditioned_plan_metric_digest": conditioned_plan_metric_digest,
        "world_coordinate_schema_digest": world_coordinate_schema_digest,
        "world_metric_digest": world_metric_digest,
        **{k: v for k, v in binding_fields.items() if k != "world_model_revision"},
    }
    blockers.extend(f"missing_{name}" for name, value in text_fields.items() if not isinstance(value, str) or not value)
    if world_model_kind != WORLD_KIND:
        blockers.append("invalid_world_model_kind")
    if not isinstance(world_model_revision, int) or isinstance(world_model_revision, bool) or world_model_revision < 0:
        blockers.append("invalid_world_model_revision")
    if not finite(pullback_weight) or float(pullback_weight) < 0.0:
        blockers.append("invalid_pullback_weight")

    plan_errors, plan_entries = validate_weights(conditioned_plan_metric_weights, "coordinate", "plan_metric", True)
    world_errors, world_entries = validate_weights(world_metric_weights, "world_coordinate", "world_metric", False)
    blockers.extend(plan_errors + world_errors)
    plan_coordinates = [e["coordinate"] for e in plan_entries]
    world_coordinates = [e["world_coordinate"] for e in world_entries]

    if not blockers:
        if world_binding_digest != compute_world_binding_digest(**binding_fields):
            blockers.append("world_binding_digest_mismatch")
        if plan_coordinate_schema_digest != canonical_digest(plan_coordinates):
            blockers.append("plan_coordinate_schema_digest_mismatch")
        if conditioned_plan_metric_digest != canonical_digest(plan_entries):
            blockers.append("conditioned_plan_metric_digest_mismatch")
        if world_coordinate_schema_digest != canonical_digest(world_coordinates):
            blockers.append("world_coordinate_schema_digest_mismatch")
        if world_metric_digest != canonical_digest(world_entries):
            blockers.append("world_metric_digest_mismatch")
    if not isinstance(candidate_projections, list) or not candidate_projections:
        blockers.append("empty_candidate_projections")
    if blockers:
        return WorldConditionedPathProjectionPullbackMetricResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    plan_set, world_set = set(plan_coordinates), set(world_coordinates)
    plan_weights = {e["coordinate"]: e["weight"] for e in plan_entries}
    world_weights = {e["world_coordinate"]: e["weight"] for e in world_entries}
    seen_ids: set[str] = set()
    seen_digests: set[str] = set()
    outputs: dict[str, dict] = {}
    required = {
        "candidate_id", "parameter_delta", "world_jacobian", "projected_world_delta",
        "persistent_world_state_digest_before", "persistent_world_state_digest_after",
        "projection_not_fact", "world_prediction_not_truth", "world_mutation_requested",
        "candidate_world_projection_digest",
    }

    for index, candidate in enumerate(candidate_projections):
        if not isinstance(candidate, dict) or set(candidate) != required:
            blockers.append(f"invalid_candidate_schema_{index}")
            continue
        candidate_id = candidate["candidate_id"]
        digest = candidate["candidate_world_projection_digest"]
        if not isinstance(candidate_id, str) or not candidate_id:
            blockers.append(f"invalid_candidate_id_{index}")
            continue
        if candidate_id in seen_ids:
            blockers.append("duplicate_candidate_id")
        seen_ids.add(candidate_id)
        if not isinstance(digest, str) or not digest:
            blockers.append(f"missing_candidate_projection_digest_{index}")
        elif digest in seen_digests:
            blockers.append("duplicate_candidate_projection_digest")
        else:
            seen_digests.add(digest)
        if digest != compute_candidate_world_projection_digest(candidate):
            blockers.append(f"candidate_projection_digest_mismatch_{index}")

        delta, jacobian, world_delta = candidate["parameter_delta"], candidate["world_jacobian"], candidate["projected_world_delta"]
        if not isinstance(delta, dict) or set(delta) != plan_set:
            blockers.append(f"candidate_plan_coordinate_mismatch_{index}")
            continue
        if not isinstance(jacobian, dict) or set(jacobian) != world_set:
            blockers.append(f"candidate_jacobian_world_coordinate_mismatch_{index}")
            continue
        if not isinstance(world_delta, dict) or set(world_delta) != world_set:
            blockers.append(f"candidate_world_coordinate_mismatch_{index}")
            continue
        if any(not finite(delta[c]) for c in plan_coordinates):
            blockers.append(f"invalid_candidate_plan_delta_{index}")
            continue
        valid_jacobian = all(isinstance(jacobian[a], dict) and set(jacobian[a]) == plan_set and all(finite(jacobian[a][c]) for c in plan_coordinates) for a in world_coordinates)
        if not valid_jacobian or any(not finite(world_delta[a]) for a in world_coordinates):
            blockers.append(f"invalid_candidate_jacobian_or_world_delta_{index}")
            continue
        if candidate["persistent_world_state_digest_before"] != world_model_state_digest:
            blockers.append(f"candidate_source_world_state_mismatch_{index}")
        if candidate["persistent_world_state_digest_after"] != world_model_state_digest:
            blockers.append(f"candidate_persistent_world_state_changed_{index}")
        if candidate["projection_not_fact"] is not True:
            blockers.append(f"candidate_projection_fact_boundary_lost_{index}")
        if candidate["world_prediction_not_truth"] is not True:
            blockers.append(f"candidate_prediction_truth_boundary_lost_{index}")
        if candidate["world_mutation_requested"] is not False:
            blockers.append(f"candidate_world_mutation_requested_{index}")

        numeric_delta = {c: float(delta[c]) for c in plan_coordinates}
        numeric_world_delta = {a: float(world_delta[a]) for a in world_coordinates}
        numeric_jacobian = {a: {c: float(jacobian[a][c]) for c in plan_coordinates} for a in world_coordinates}
        for a in world_coordinates:
            expected = sum(numeric_jacobian[a][c] * numeric_delta[c] for c in plan_coordinates)
            if not close(expected, numeric_world_delta[a]):
                blockers.append(f"candidate_projected_world_delta_mismatch_{index}_{a}")

        pullback = {
            i: {j: sum(world_weights[a] * numeric_jacobian[a][i] * numeric_jacobian[a][j] for a in world_coordinates) for j in plan_coordinates}
            for i in plan_coordinates
        }
        combined = {
            i: {j: (plan_weights[i] if i == j else 0.0) + float(pullback_weight) * pullback[i][j] for j in plan_coordinates}
            for i in plan_coordinates
        }
        plan_action = 0.5 * sum(plan_weights[c] * numeric_delta[c] ** 2 for c in plan_coordinates)
        world_action = 0.5 * sum(world_weights[a] * numeric_world_delta[a] ** 2 for a in world_coordinates)
        combined_action = plan_action + float(pullback_weight) * world_action
        matrix_action = 0.5 * sum(numeric_delta[i] * combined[i][j] * numeric_delta[j] for i in plan_coordinates for j in plan_coordinates)
        if not close(combined_action, matrix_action):
            blockers.append(f"combined_action_matrix_identity_violation_{index}")
        if min(plan_action, world_action, combined_action) < -TOL:
            blockers.append(f"negative_transition_action_{index}")
        outputs[candidate_id] = {
            "projection_digest": digest,
            "world_delta": numeric_world_delta,
            "pullback_metric": pullback,
            "combined_metric": combined,
            "plan_action": plan_action,
            "world_action": world_action,
            "combined_action": combined_action,
        }

    if blockers:
        return WorldConditionedPathProjectionPullbackMetricResult(STATUS_BLOCKED, sorted(set(blockers)), None)

    certificate = {
        "kernel": "PlanOS WORLD-Conditioned Path Projection Pullback Metric Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.00",
        "source_qi_conditioned_metric_certificate_digest": source_qi_conditioned_metric_certificate_digest,
        **binding_fields,
        "world_binding_digest": world_binding_digest,
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "conditioned_plan_metric_digest": conditioned_plan_metric_digest,
        "world_coordinate_schema_digest": world_coordinate_schema_digest,
        "world_metric_digest": world_metric_digest,
        "pullback_weight": float(pullback_weight),
        "candidate_world_projection_digests": {k: v["projection_digest"] for k, v in outputs.items()},
        "candidate_world_delta_map": {k: v["world_delta"] for k, v in outputs.items()},
        "candidate_pullback_metric_map": {k: v["pullback_metric"] for k, v in outputs.items()},
        "candidate_combined_metric_map": {k: v["combined_metric"] for k, v in outputs.items()},
        "plan_transition_action_map": {k: v["plan_action"] for k, v in outputs.items()},
        "world_transition_action_map": {k: v["world_action"] for k, v in outputs.items()},
        "combined_transition_action_map": {k: v["combined_action"] for k, v in outputs.items()},
        "world_pullback_metric_nonnegative": True,
        "combined_qi_world_metric_nonnegative": True,
        "plan_coordinate_dimension_preserved": True,
        "source_world_state_digest_preserved": True,
        "persistent_world_state_unchanged": True,
        "counterfactual_projection_not_fact": True,
        "world_model_prediction_not_truth": True,
        "world_mutation_not_granted": True,
        "holonomy_context_preserved": True,
        "transport_residue_visible": True,
        "candidate_field_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["pullback_metric_digest"] = canonical_digest({"world_binding_digest": world_binding_digest, "outputs": outputs})
    certificate["world_conditioned_metric_certificate_digest"] = canonical_digest(certificate)
    return WorldConditionedPathProjectionPullbackMetricResult(STATUS_READY, [], certificate)
