#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
TOL = 1e-10


@dataclass
class NativeCoupledInformationMetricCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(value: Any) -> str:
    return sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def finite(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=TOL)


def _normalize_base_metric_weights(
    entries: Sequence[Mapping[str, Any]],
) -> list[dict]:
    return sorted(
        (
            {
                "coordinate": str(entry["coordinate"]),
                "weight": float(entry["weight"]),
            }
            for entry in entries
        ),
        key=lambda entry: entry["coordinate"],
    )


def _normalize_coupling_factor_rows(
    rows: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> list[dict]:
    return sorted(
        (
            {
                "factor_id": str(row["factor_id"]),
                "coefficients": {
                    coordinate: float(row["coefficients"][coordinate])
                    for coordinate in coordinates
                },
                "provenance_digest": str(row["provenance_digest"]),
            }
            for row in rows
        ),
        key=lambda row: row["factor_id"],
    )


def _normalize_candidate_deltas(
    candidates: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> list[dict]:
    return sorted(
        (
            {
                "candidate_id": str(candidate["candidate_id"]),
                "parameter_delta": {
                    coordinate: float(candidate["parameter_delta"][coordinate])
                    for coordinate in coordinates
                },
                "source_candidate_digest": str(candidate["source_candidate_digest"]),
            }
            for candidate in candidates
        ),
        key=lambda candidate: candidate["candidate_id"],
    )


def compute_plan_coordinate_schema_digest(
    base_metric_weights: Sequence[Mapping[str, Any]],
) -> str:
    coordinates = [
        entry["coordinate"]
        for entry in _normalize_base_metric_weights(base_metric_weights)
    ]
    return canonical_digest(coordinates)


def compute_base_diagonal_metric_digest(
    base_metric_weights: Sequence[Mapping[str, Any]],
) -> str:
    return canonical_digest(_normalize_base_metric_weights(base_metric_weights))


def compute_coupling_factor_digest(
    coupling_factor_rows: Sequence[Mapping[str, Any]],
    coordinates: Sequence[str],
) -> str:
    return canonical_digest(
        _normalize_coupling_factor_rows(coupling_factor_rows, coordinates)
    )


def compute_candidate_delta_bundle_digest(
    candidate_deltas: Sequence[Mapping[str, Any]], coordinates: Sequence[str]
) -> str:
    return canonical_digest(_normalize_candidate_deltas(candidate_deltas, coordinates))


def _validate_base_metric_weights(
    entries: Any,
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(entries, list) or not entries:
        return ["empty_base_metric_weights"], []

    normalized: list[dict] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"coordinate", "weight"}:
            blockers.append(f"invalid_base_metric_entry_{index}")
            continue
        coordinate = entry["coordinate"]
        weight = entry["weight"]
        if not isinstance(coordinate, str) or not coordinate.strip():
            blockers.append(f"invalid_base_metric_coordinate_{index}")
            continue
        coordinate = coordinate.strip()
        if coordinate in seen:
            blockers.append("duplicate_base_metric_coordinate")
        seen.add(coordinate)
        if not finite(weight):
            blockers.append(f"invalid_base_metric_weight_{index}")
            continue
        numeric = float(weight)
        if numeric <= 0.0:
            blockers.append(f"nonpositive_base_metric_weight_{index}")
        normalized.append({"coordinate": coordinate, "weight": numeric})
    normalized.sort(key=lambda entry: entry["coordinate"])
    return blockers, normalized


def _validate_coupling_rows(
    rows: Any, coordinates: Sequence[str]
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(rows, list) or not rows:
        return ["empty_coupling_factor_rows"], []

    coordinate_set = set(coordinates)
    normalized: list[dict] = []
    seen_factor_ids: set[str] = set()
    seen_provenance: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {
            "factor_id",
            "coefficients",
            "provenance_digest",
        }:
            blockers.append(f"invalid_coupling_factor_row_{index}")
            continue
        factor_id = row["factor_id"]
        provenance = row["provenance_digest"]
        coefficients = row["coefficients"]
        if not isinstance(factor_id, str) or not factor_id.strip():
            blockers.append(f"invalid_coupling_factor_id_{index}")
            continue
        factor_id = factor_id.strip()
        if factor_id in seen_factor_ids:
            blockers.append("duplicate_coupling_factor_id")
        seen_factor_ids.add(factor_id)
        if not isinstance(provenance, str) or not provenance:
            blockers.append(f"missing_coupling_provenance_digest_{index}")
        elif provenance in seen_provenance:
            blockers.append("duplicate_coupling_provenance_digest")
        else:
            seen_provenance.add(provenance)
        if not isinstance(coefficients, dict) or set(coefficients) != coordinate_set:
            blockers.append(f"coupling_coordinate_mismatch_{index}")
            continue
        if any(not finite(coefficients[coordinate]) for coordinate in coordinates):
            blockers.append(f"invalid_coupling_coefficient_{index}")
            continue
        normalized.append(
            {
                "factor_id": factor_id,
                "coefficients": {
                    coordinate: float(coefficients[coordinate])
                    for coordinate in coordinates
                },
                "provenance_digest": provenance,
            }
        )
    normalized.sort(key=lambda row: row["factor_id"])
    if normalized and all(
        close(coefficient, 0.0)
        for row in normalized
        for coefficient in row["coefficients"].values()
    ):
        blockers.append("coupling_factor_all_zero")
    return blockers, normalized


def _validate_candidate_deltas(
    candidates: Any, coordinates: Sequence[str]
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(candidates, list) or not candidates:
        return ["empty_candidate_deltas"], []

    coordinate_set = set(coordinates)
    normalized: list[dict] = []
    seen_ids: set[str] = set()
    seen_source_digests: set[str] = set()
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict) or set(candidate) != {
            "candidate_id",
            "parameter_delta",
            "source_candidate_digest",
        }:
            blockers.append(f"invalid_candidate_delta_entry_{index}")
            continue
        candidate_id = candidate["candidate_id"]
        source_digest = candidate["source_candidate_digest"]
        delta = candidate["parameter_delta"]
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            blockers.append(f"invalid_candidate_id_{index}")
            continue
        candidate_id = candidate_id.strip()
        if candidate_id in seen_ids:
            blockers.append("duplicate_candidate_id")
        seen_ids.add(candidate_id)
        if not isinstance(source_digest, str) or not source_digest:
            blockers.append(f"missing_source_candidate_digest_{index}")
        elif source_digest in seen_source_digests:
            blockers.append("duplicate_source_candidate_digest")
        else:
            seen_source_digests.add(source_digest)
        if not isinstance(delta, dict) or set(delta) != coordinate_set:
            blockers.append(f"candidate_delta_coordinate_mismatch_{index}")
            continue
        if any(not finite(delta[coordinate]) for coordinate in coordinates):
            blockers.append(f"invalid_candidate_delta_{index}")
            continue
        normalized.append(
            {
                "candidate_id": candidate_id,
                "parameter_delta": {
                    coordinate: float(delta[coordinate]) for coordinate in coordinates
                },
                "source_candidate_digest": source_digest,
            }
        )
    normalized.sort(key=lambda candidate: candidate["candidate_id"])
    return blockers, normalized


def _interaction_disposition(contribution: float) -> str:
    if contribution < -TOL:
        return "synergy"
    if contribution > TOL:
        return "tradeoff"
    return "neutral"


def build_native_coupled_information_metric_certificate(
    *,
    source_qi_conditioned_metric_certificate_digest: str,
    source_world_conditioned_metric_certificate_digest: str,
    plan_coordinate_schema_digest: str,
    base_diagonal_metric_digest: str,
    base_metric_weights: list[dict],
    coupling_factor_digest: str,
    coupling_factor_rows: list[dict],
    candidate_delta_bundle_digest: str,
    candidate_deltas: list[dict],
    minimum_metric_eigenvalue_bound: float,
    maximum_metric_eigenvalue_bound: float,
) -> NativeCoupledInformationMetricCertificateResult:
    blockers: list[str] = []

    for name, value in {
        "source_qi_conditioned_metric_certificate_digest": (
            source_qi_conditioned_metric_certificate_digest
        ),
        "source_world_conditioned_metric_certificate_digest": (
            source_world_conditioned_metric_certificate_digest
        ),
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "base_diagonal_metric_digest": base_diagonal_metric_digest,
        "coupling_factor_digest": coupling_factor_digest,
        "candidate_delta_bundle_digest": candidate_delta_bundle_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"missing_{name}")

    for name, value in {
        "minimum_metric_eigenvalue_bound": minimum_metric_eigenvalue_bound,
        "maximum_metric_eigenvalue_bound": maximum_metric_eigenvalue_bound,
    }.items():
        if not finite(value):
            blockers.append(f"invalid_{name}")
    if finite(minimum_metric_eigenvalue_bound) and float(
        minimum_metric_eigenvalue_bound
    ) <= 0.0:
        blockers.append("nonpositive_minimum_metric_eigenvalue_bound")
    if (
        finite(minimum_metric_eigenvalue_bound)
        and finite(maximum_metric_eigenvalue_bound)
        and float(maximum_metric_eigenvalue_bound)
        < float(minimum_metric_eigenvalue_bound)
    ):
        blockers.append("maximum_metric_eigenvalue_bound_below_minimum")

    metric_errors, normalized_metric = _validate_base_metric_weights(
        base_metric_weights
    )
    blockers.extend(metric_errors)
    coordinates = [entry["coordinate"] for entry in normalized_metric]

    coupling_errors, normalized_rows = _validate_coupling_rows(
        coupling_factor_rows, coordinates
    )
    blockers.extend(coupling_errors)
    candidate_errors, normalized_candidates = _validate_candidate_deltas(
        candidate_deltas, coordinates
    )
    blockers.extend(candidate_errors)

    if not blockers:
        if plan_coordinate_schema_digest != canonical_digest(coordinates):
            blockers.append("plan_coordinate_schema_digest_mismatch")
        if base_diagonal_metric_digest != canonical_digest(normalized_metric):
            blockers.append("base_diagonal_metric_digest_mismatch")
        if coupling_factor_digest != canonical_digest(normalized_rows):
            blockers.append("coupling_factor_digest_mismatch")
        if candidate_delta_bundle_digest != canonical_digest(normalized_candidates):
            blockers.append("candidate_delta_bundle_digest_mismatch")

    if blockers:
        return NativeCoupledInformationMetricCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    weights = {
        entry["coordinate"]: float(entry["weight"]) for entry in normalized_metric
    }
    factor_rows = {
        row["factor_id"]: row["coefficients"] for row in normalized_rows
    }

    gram_metric = {
        i: {
            j: sum(
                factor_rows[factor_id][i] * factor_rows[factor_id][j]
                for factor_id in factor_rows
            )
            for j in coordinates
        }
        for i in coordinates
    }
    coupled_metric = {
        i: {
            j: (weights[i] if i == j else 0.0) + gram_metric[i][j]
            for j in coordinates
        }
        for i in coordinates
    }

    metric_symmetric = all(
        close(coupled_metric[i][j], coupled_metric[j][i])
        for i in coordinates
        for j in coordinates
    )
    off_diagonal_entries = [
        coupled_metric[i][j]
        for left_index, i in enumerate(coordinates)
        for j in coordinates[left_index + 1 :]
    ]
    non_diagonal_coupling_present = any(
        not close(value, 0.0) for value in off_diagonal_entries
    )
    if not metric_symmetric:
        blockers.append("coupled_metric_symmetry_violation")
    if not non_diagonal_coupling_present:
        blockers.append("non_diagonal_coupling_missing")

    minimum_diagonal_weight = min(weights.values())
    maximum_diagonal_weight = max(weights.values())
    frobenius_norm_squared = sum(
        coefficient * coefficient
        for row in factor_rows.values()
        for coefficient in row.values()
    )
    computed_lower_bound = minimum_diagonal_weight
    computed_upper_bound = maximum_diagonal_weight + frobenius_norm_squared
    metric_floor_preserved = (
        computed_lower_bound + TOL >= float(minimum_metric_eigenvalue_bound)
    )
    metric_ceiling_preserved = (
        computed_upper_bound <= float(maximum_metric_eigenvalue_bound) + TOL
    )
    if not metric_floor_preserved:
        blockers.append("metric_floor_bound_violation")
    if not metric_ceiling_preserved:
        blockers.append("metric_ceiling_bound_violation")

    candidate_action_map: dict[str, float] = {}
    candidate_base_diagonal_action_map: dict[str, float] = {}
    candidate_gram_coupling_action_map: dict[str, float] = {}
    candidate_diagonal_component_action_map: dict[str, float] = {}
    candidate_pairwise_interaction_action_map: dict[str, float] = {}
    candidate_pairwise_interaction_map: dict[str, list[dict]] = {}

    for candidate in normalized_candidates:
        candidate_id = candidate["candidate_id"]
        delta = candidate["parameter_delta"]
        base_action = 0.5 * sum(
            weights[i] * delta[i] * delta[i] for i in coordinates
        )
        row_actions = {
            factor_id: sum(
                coefficients[i] * delta[i] for i in coordinates
            )
            for factor_id, coefficients in factor_rows.items()
        }
        gram_action = 0.5 * sum(value * value for value in row_actions.values())
        total_action = base_action + gram_action
        matrix_action = 0.5 * sum(
            delta[i] * coupled_metric[i][j] * delta[j]
            for i in coordinates
            for j in coordinates
        )
        diagonal_component = 0.5 * sum(
            coupled_metric[i][i] * delta[i] * delta[i] for i in coordinates
        )
        pairwise_records: list[dict] = []
        pairwise_total = 0.0
        for left_index, i in enumerate(coordinates):
            for j in coordinates[left_index + 1 :]:
                contribution = coupled_metric[i][j] * delta[i] * delta[j]
                pairwise_total += contribution
                pairwise_records.append(
                    {
                        "coordinate_i": i,
                        "coordinate_j": j,
                        "metric_entry": coupled_metric[i][j],
                        "delta_i": delta[i],
                        "delta_j": delta[j],
                        "interaction_contribution": contribution,
                        "interaction_disposition": _interaction_disposition(
                            contribution
                        ),
                    }
                )
        if not close(total_action, matrix_action):
            blockers.append(f"candidate_matrix_action_identity_violation_{candidate_id}")
        if not close(total_action, diagonal_component + pairwise_total):
            blockers.append(
                f"candidate_pairwise_action_decomposition_violation_{candidate_id}"
            )
        if min(base_action, gram_action, total_action) < -TOL:
            blockers.append(f"candidate_negative_coupled_action_{candidate_id}")
        candidate_action_map[candidate_id] = total_action
        candidate_base_diagonal_action_map[candidate_id] = base_action
        candidate_gram_coupling_action_map[candidate_id] = gram_action
        candidate_diagonal_component_action_map[candidate_id] = diagonal_component
        candidate_pairwise_interaction_action_map[candidate_id] = pairwise_total
        candidate_pairwise_interaction_map[candidate_id] = pairwise_records

    if blockers:
        return NativeCoupledInformationMetricCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    metric_payload = {
        "source_qi_conditioned_metric_certificate_digest": (
            source_qi_conditioned_metric_certificate_digest
        ),
        "source_world_conditioned_metric_certificate_digest": (
            source_world_conditioned_metric_certificate_digest
        ),
        "plan_coordinate_schema_digest": plan_coordinate_schema_digest,
        "base_diagonal_metric_digest": base_diagonal_metric_digest,
        "coupling_factor_digest": coupling_factor_digest,
        "candidate_delta_bundle_digest": candidate_delta_bundle_digest,
        "minimum_metric_eigenvalue_bound": float(
            minimum_metric_eigenvalue_bound
        ),
        "maximum_metric_eigenvalue_bound": float(
            maximum_metric_eigenvalue_bound
        ),
        "coupled_metric": coupled_metric,
    }
    coupled_metric_digest = canonical_digest(metric_payload)

    certificate = {
        "kernel": "PlanOS Native Coupled Information Metric Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.05",
        **metric_payload,
        "base_metric_weights": normalized_metric,
        "coupling_factor_rows": normalized_rows,
        "candidate_deltas": normalized_candidates,
        "gram_metric": gram_metric,
        "minimum_diagonal_weight": minimum_diagonal_weight,
        "maximum_diagonal_weight": maximum_diagonal_weight,
        "coupling_factor_frobenius_norm_squared": frobenius_norm_squared,
        "computed_metric_lower_bound": computed_lower_bound,
        "computed_metric_upper_bound": computed_upper_bound,
        "condition_number_upper_bound": (
            computed_upper_bound / computed_lower_bound
        ),
        "candidate_action_map": candidate_action_map,
        "candidate_base_diagonal_action_map": (
            candidate_base_diagonal_action_map
        ),
        "candidate_gram_coupling_action_map": (
            candidate_gram_coupling_action_map
        ),
        "candidate_diagonal_component_action_map": (
            candidate_diagonal_component_action_map
        ),
        "candidate_pairwise_interaction_action_map": (
            candidate_pairwise_interaction_action_map
        ),
        "candidate_pairwise_interaction_map": candidate_pairwise_interaction_map,
        "metric_symmetric": metric_symmetric,
        "metric_positive_definite": True,
        "metric_floor_preserved": metric_floor_preserved,
        "metric_ceiling_preserved": metric_ceiling_preserved,
        "non_diagonal_coupling_present": non_diagonal_coupling_present,
        "diagonal_metric_recoverable_as_zero_coupling": True,
        "pairwise_interactions_retained": True,
        "interaction_sign_direction_aware": True,
        "world_pullback_composition_preserves_positive_definiteness": True,
        "source_metric_not_mutated": True,
        "candidate_field_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "world_projection_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
        "coupled_metric_digest": coupled_metric_digest,
    }
    certificate["metric_certificate_digest"] = canonical_digest(certificate)
    return NativeCoupledInformationMetricCertificateResult(
        STATUS_READY, [], certificate
    )
