#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any, Mapping, Sequence

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
_TOLERANCE = 1e-12

_REQUIRED_QI_COMPONENTS = {
    "activation",
    "stagnation",
    "tension",
    "recovery",
    "coherence",
    "coupling",
    "transition_readiness",
    "hysteresis",
}
_VALID_DIRECTIONS = {"neutral", "switch", "reroute"}


@dataclass
class QiConditionedInformationMetricCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=_TOLERANCE)


def _normalized_metric_entries(base_metric_weights: Sequence[Mapping[str, Any]]) -> list[dict]:
    return sorted(
        (
            {
                "coordinate": str(entry["coordinate"]),
                "weight": float(entry["weight"]),
            }
            for entry in base_metric_weights
        ),
        key=lambda entry: entry["coordinate"],
    )


def compute_parameter_coordinate_schema_digest(
    base_metric_weights: Sequence[Mapping[str, Any]],
) -> str:
    coordinates = [
        entry["coordinate"] for entry in _normalized_metric_entries(base_metric_weights)
    ]
    return canonical_digest(coordinates)


def compute_base_metric_digest(
    base_metric_weights: Sequence[Mapping[str, Any]],
) -> str:
    return canonical_digest(_normalized_metric_entries(base_metric_weights))


def compute_conditioned_transition_action(
    conditioned_metric_weights: Mapping[str, float],
    parameter_delta: Mapping[str, float],
) -> float:
    if set(conditioned_metric_weights) != set(parameter_delta):
        raise ValueError("parameter_delta_coordinate_mismatch")
    total = 0.0
    for coordinate, weight in conditioned_metric_weights.items():
        delta = parameter_delta[coordinate]
        if (
            not _is_finite_number(weight)
            or float(weight) < 0.0
            or not _is_finite_number(delta)
        ):
            raise ValueError("invalid_quadratic_form_input")
        total += float(weight) * float(delta) ** 2
    return 0.5 * total


def _validate_base_metric_weights(
    base_metric_weights: Any,
    minimum_metric_weight: float,
    maximum_metric_weight: float,
) -> tuple[list[str], list[dict]]:
    blockers: list[str] = []
    if not isinstance(base_metric_weights, list) or not base_metric_weights:
        return ["empty_base_metric_weights"], []

    normalized: list[dict] = []
    seen_coordinates: set[str] = set()
    for index, entry in enumerate(base_metric_weights):
        if not isinstance(entry, dict):
            blockers.append(f"invalid_metric_entry_{index}")
            continue
        if set(entry) != {"coordinate", "weight"}:
            blockers.append(f"invalid_metric_entry_schema_{index}")
            continue
        coordinate = entry["coordinate"]
        weight = entry["weight"]
        if not isinstance(coordinate, str) or not coordinate.strip():
            blockers.append(f"invalid_metric_coordinate_{index}")
            continue
        coordinate = coordinate.strip()
        if coordinate in seen_coordinates:
            blockers.append("duplicate_metric_coordinate")
        seen_coordinates.add(coordinate)
        if not _is_finite_number(weight):
            blockers.append(f"invalid_metric_weight_{index}")
            continue
        numeric_weight = float(weight)
        if numeric_weight <= 0.0:
            blockers.append(f"nonpositive_metric_weight_{index}")
        if _is_finite_number(minimum_metric_weight) and numeric_weight < float(
            minimum_metric_weight
        ):
            blockers.append(f"metric_weight_below_floor_{index}")
        if _is_finite_number(maximum_metric_weight) and numeric_weight > float(
            maximum_metric_weight
        ):
            blockers.append(f"metric_weight_above_ceiling_{index}")
        normalized.append({"coordinate": coordinate, "weight": numeric_weight})
    normalized.sort(key=lambda item: item["coordinate"])
    return blockers, normalized


def _validate_qi_process_tensor(qi_process_tensor: Any) -> list[str]:
    if not isinstance(qi_process_tensor, dict):
        return ["invalid_qi_process_tensor"]
    blockers: list[str] = []
    missing = sorted(_REQUIRED_QI_COMPONENTS - set(qi_process_tensor))
    extra = sorted(set(qi_process_tensor) - _REQUIRED_QI_COMPONENTS)
    blockers.extend(f"missing_qi_component_{name}" for name in missing)
    blockers.extend(f"unknown_qi_component_{name}" for name in extra)
    for name in sorted(_REQUIRED_QI_COMPONENTS & set(qi_process_tensor)):
        value = qi_process_tensor[name]
        if not _is_finite_number(value) or not 0.0 <= float(value) <= 1.0:
            blockers.append(f"invalid_qi_component_{name}")
    return blockers


def build_qi_conditioned_information_metric_certificate(
    *,
    source_objective_kernel_digest: str,
    parameter_coordinate_schema_digest: str,
    base_metric_digest: str,
    base_metric_weights: list[dict],
    minimum_metric_weight: float,
    maximum_metric_weight: float,
    qi_process_tensor: dict,
    history_oscillation_measure: float,
    reroute_evidence_digest: str,
    reroute_evidence_present: bool,
    recovery_coefficient: float,
    stagnation_coefficient: float,
    hysteresis_coefficient: float,
    oscillation_coefficient: float,
    transition_direction_map: dict[str, str],
) -> QiConditionedInformationMetricCertificateResult:
    blockers: list[str] = []

    if not isinstance(source_objective_kernel_digest, str) or not source_objective_kernel_digest:
        blockers.append("missing_source_objective_kernel_digest")
    if (
        not isinstance(parameter_coordinate_schema_digest, str)
        or not parameter_coordinate_schema_digest
    ):
        blockers.append("missing_parameter_coordinate_schema_digest")
    if not isinstance(base_metric_digest, str) or not base_metric_digest:
        blockers.append("missing_base_metric_digest")
    if not isinstance(reroute_evidence_digest, str) or not reroute_evidence_digest:
        blockers.append("missing_reroute_evidence_digest")
    if not isinstance(reroute_evidence_present, bool):
        blockers.append("invalid_reroute_evidence_present")

    for name, value in {
        "minimum_metric_weight": minimum_metric_weight,
        "maximum_metric_weight": maximum_metric_weight,
        "history_oscillation_measure": history_oscillation_measure,
        "recovery_coefficient": recovery_coefficient,
        "stagnation_coefficient": stagnation_coefficient,
        "hysteresis_coefficient": hysteresis_coefficient,
        "oscillation_coefficient": oscillation_coefficient,
    }.items():
        if not _is_finite_number(value):
            blockers.append(f"invalid_{name}")

    if _is_finite_number(minimum_metric_weight) and minimum_metric_weight <= 0.0:
        blockers.append("nonpositive_minimum_metric_weight")
    if (
        _is_finite_number(maximum_metric_weight)
        and _is_finite_number(minimum_metric_weight)
        and maximum_metric_weight < minimum_metric_weight
    ):
        blockers.append("maximum_metric_weight_below_minimum")
    if (
        _is_finite_number(history_oscillation_measure)
        and not 0.0 <= history_oscillation_measure <= 1.0
    ):
        blockers.append("history_oscillation_measure_out_of_range")
    for name, value in {
        "recovery_coefficient": recovery_coefficient,
        "stagnation_coefficient": stagnation_coefficient,
        "hysteresis_coefficient": hysteresis_coefficient,
        "oscillation_coefficient": oscillation_coefficient,
    }.items():
        if _is_finite_number(value) and value < 0.0:
            blockers.append(f"negative_{name}")

    metric_blockers, normalized_metric = _validate_base_metric_weights(
        base_metric_weights,
        minimum_metric_weight,
        maximum_metric_weight,
    )
    blockers.extend(metric_blockers)
    blockers.extend(_validate_qi_process_tensor(qi_process_tensor))

    coordinates = [entry["coordinate"] for entry in normalized_metric]
    if not isinstance(transition_direction_map, dict):
        blockers.append("invalid_transition_direction_map")
    else:
        if set(transition_direction_map) != set(coordinates):
            blockers.append("transition_direction_coordinate_mismatch")
        for coordinate, direction in transition_direction_map.items():
            if not isinstance(coordinate, str) or not coordinate:
                blockers.append("invalid_transition_direction_coordinate")
            if direction not in _VALID_DIRECTIONS:
                blockers.append(f"invalid_transition_direction_{coordinate}")

    if not blockers:
        if parameter_coordinate_schema_digest != canonical_digest(coordinates):
            blockers.append("parameter_coordinate_schema_digest_mismatch")
        if base_metric_digest != canonical_digest(normalized_metric):
            blockers.append("base_metric_digest_mismatch")

    if blockers:
        return QiConditionedInformationMetricCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    qi = {name: float(qi_process_tensor[name]) for name in sorted(_REQUIRED_QI_COMPONENTS)}
    recovery_surcharge_value = recovery_coefficient * qi["recovery"]
    hysteresis_surcharge_value = hysteresis_coefficient * qi["hysteresis"]
    oscillation_surcharge_value = oscillation_coefficient * history_oscillation_measure
    reroute_discount_value = (
        stagnation_coefficient * qi["stagnation"]
        if reroute_evidence_present
        else 0.0
    )

    conditioned_metric_weights: dict[str, float] = {}
    recovery_switch_surcharge: dict[str, float] = {}
    hysteresis_switch_surcharge: dict[str, float] = {}
    oscillation_switch_surcharge: dict[str, float] = {}
    evidence_gated_reroute_discount: dict[str, float] = {}

    base_weight_map = {
        entry["coordinate"]: float(entry["weight"]) for entry in normalized_metric
    }
    for coordinate in coordinates:
        direction = transition_direction_map[coordinate]
        recovery_surcharge = recovery_surcharge_value if direction == "switch" else 0.0
        hysteresis_surcharge = hysteresis_surcharge_value if direction == "switch" else 0.0
        oscillation_surcharge = oscillation_surcharge_value if direction == "switch" else 0.0
        reroute_discount = reroute_discount_value if direction == "reroute" else 0.0
        raw_weight = (
            base_weight_map[coordinate]
            + recovery_surcharge
            + hysteresis_surcharge
            + oscillation_surcharge
            - reroute_discount
        )
        conditioned_weight = min(
            maximum_metric_weight,
            max(minimum_metric_weight, raw_weight),
        )
        conditioned_metric_weights[coordinate] = conditioned_weight
        recovery_switch_surcharge[coordinate] = recovery_surcharge
        hysteresis_switch_surcharge[coordinate] = hysteresis_surcharge
        oscillation_switch_surcharge[coordinate] = oscillation_surcharge
        evidence_gated_reroute_discount[coordinate] = reroute_discount

    metric_floor_preserved = all(
        weight + _TOLERANCE >= minimum_metric_weight
        for weight in conditioned_metric_weights.values()
    )
    metric_ceiling_preserved = all(
        weight <= maximum_metric_weight + _TOLERANCE
        for weight in conditioned_metric_weights.values()
    )
    metric_nonnegativity_preserved = all(
        weight >= -_TOLERANCE for weight in conditioned_metric_weights.values()
    )
    evidence_gate_preserved = (
        reroute_evidence_present
        or all(
            _close(discount, 0.0)
            for discount in evidence_gated_reroute_discount.values()
        )
    )
    recovery_protection_preserved = all(
        transition_direction_map[coordinate] != "switch"
        or conditioned_metric_weights[coordinate] + _TOLERANCE
        >= base_weight_map[coordinate]
        for coordinate in coordinates
    )
    hysteresis_resistance_preserved = recovery_protection_preserved
    oscillation_resistance_preserved = recovery_protection_preserved

    if not metric_nonnegativity_preserved:
        blockers.append("conditioned_metric_nonnegativity_violation")
    if not metric_floor_preserved:
        blockers.append("conditioned_metric_floor_violation")
    if not metric_ceiling_preserved:
        blockers.append("conditioned_metric_ceiling_violation")
    if not evidence_gate_preserved:
        blockers.append("reroute_evidence_gate_violation")
    if not recovery_protection_preserved:
        blockers.append("recovery_switch_protection_violation")
    if not hysteresis_resistance_preserved:
        blockers.append("hysteresis_switch_resistance_violation")
    if not oscillation_resistance_preserved:
        blockers.append("oscillation_switch_resistance_violation")
    if blockers:
        return QiConditionedInformationMetricCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    qi_process_tensor_digest = canonical_digest(qi)
    history_condition_digest = canonical_digest(
        {"history_oscillation_measure": history_oscillation_measure}
    )
    conditioned_metric_payload = {
        "source_objective_kernel_digest": source_objective_kernel_digest,
        "parameter_coordinate_schema_digest": parameter_coordinate_schema_digest,
        "base_metric_digest": base_metric_digest,
        "qi_process_tensor_digest": qi_process_tensor_digest,
        "history_condition_digest": history_condition_digest,
        "reroute_evidence_digest": reroute_evidence_digest,
        "reroute_evidence_present": reroute_evidence_present,
        "minimum_metric_weight": minimum_metric_weight,
        "maximum_metric_weight": maximum_metric_weight,
        "recovery_coefficient": recovery_coefficient,
        "stagnation_coefficient": stagnation_coefficient,
        "hysteresis_coefficient": hysteresis_coefficient,
        "oscillation_coefficient": oscillation_coefficient,
        "transition_direction_map": {
            coordinate: transition_direction_map[coordinate]
            for coordinate in coordinates
        },
        "conditioned_metric_weights": conditioned_metric_weights,
    }
    conditioned_metric_digest = canonical_digest(conditioned_metric_payload)

    certificate = {
        **conditioned_metric_payload,
        "qi_process_tensor": qi,
        "history_oscillation_measure": history_oscillation_measure,
        "recovery_switch_surcharge": recovery_switch_surcharge,
        "hysteresis_switch_surcharge": hysteresis_switch_surcharge,
        "oscillation_switch_surcharge": oscillation_switch_surcharge,
        "evidence_gated_reroute_discount": evidence_gated_reroute_discount,
        "minimum_conditioned_weight": min(conditioned_metric_weights.values()),
        "maximum_conditioned_weight": max(conditioned_metric_weights.values()),
        "metric_nonnegativity_preserved": metric_nonnegativity_preserved,
        "metric_floor_preserved": metric_floor_preserved,
        "metric_ceiling_preserved": metric_ceiling_preserved,
        "evidence_gate_preserved": evidence_gate_preserved,
        "recovery_protection_preserved": recovery_protection_preserved,
        "hysteresis_resistance_preserved": hysteresis_resistance_preserved,
        "oscillation_resistance_preserved": oscillation_resistance_preserved,
        "conditioned_metric_digest": conditioned_metric_digest,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["metric_certificate_digest"] = canonical_digest(certificate)
    return QiConditionedInformationMetricCertificateResult(
        STATUS_READY, [], certificate
    )
