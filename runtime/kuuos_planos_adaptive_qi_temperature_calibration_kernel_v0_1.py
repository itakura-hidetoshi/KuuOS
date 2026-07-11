#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from math import isfinite, log

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


def _digest(value: object) -> str:
    return sha256(dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass
class CalibrationResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def build_adaptive_qi_temperature_calibration(
    *,
    source_concentration_certificate: dict,
    current_temperature: float,
    minimum_temperature: float,
    maximum_temperature: float,
    target_epsilon: float,
    qi_state: dict,
    history_state: dict,
    require_concentration_certificate: bool = True,
) -> CalibrationResult:
    blockers: list[str] = []
    if not source_concentration_certificate:
        blockers.append("missing_source_concentration_certificate")
    if not all(isfinite(x) and x > 0 for x in (current_temperature, minimum_temperature, maximum_temperature)):
        blockers.append("temperature_bounds_must_be_positive_finite")
    if minimum_temperature > maximum_temperature:
        blockers.append("minimum_temperature_exceeds_maximum_temperature")
    if not isfinite(target_epsilon) or not 0 < target_epsilon < 1:
        blockers.append("target_epsilon_must_be_between_zero_and_one")

    gap = float(source_concentration_certificate.get("minimum_positive_action_gap", 0.0))
    minimizer_count = int(source_concentration_certificate.get("minimal_action_candidate_count", 0))
    nonminimal_count = int(source_concentration_certificate.get("nonminimal_candidate_count", 0))
    if gap < 0 or not isfinite(gap):
        blockers.append("invalid_action_gap")
    if minimizer_count <= 0 or nonminimal_count < 0:
        blockers.append("invalid_support_counts")

    for key in ("activation", "stagnation", "recovery", "coherence", "transition_readiness", "hysteresis"):
        value = float(qi_state.get(key, 0.0))
        if not isfinite(value) or value < 0:
            blockers.append(f"invalid_qi_{key}")
    oscillation = float(history_state.get("oscillation", 0.0))
    if not isfinite(oscillation) or oscillation < 0:
        blockers.append("invalid_history_oscillation")

    if blockers:
        return CalibrationResult(STATUS_BLOCKED, blockers, None)

    if nonminimal_count == 0:
        concentration_ceiling = maximum_temperature
    elif gap == 0:
        concentration_ceiling = 0.0
    else:
        ratio = nonminimal_count / (minimizer_count * target_epsilon)
        concentration_ceiling = maximum_temperature if ratio <= 1 else gap / log(ratio)

    exploration = (
        float(qi_state.get("activation", 0.0))
        + float(qi_state.get("stagnation", 0.0))
        + float(qi_state.get("transition_readiness", 0.0))
    ) / 3.0
    stabilization = (
        float(qi_state.get("recovery", 0.0))
        + float(qi_state.get("coherence", 0.0))
        + float(qi_state.get("hysteresis", 0.0))
        + oscillation
    ) / 4.0
    raw_multiplier = max(0.25, 1.0 + 0.25 * exploration - 0.25 * stabilization)
    raw_temperature = current_temperature * raw_multiplier

    effective_maximum = maximum_temperature
    if require_concentration_certificate:
        effective_maximum = min(effective_maximum, concentration_ceiling)
    if effective_maximum < minimum_temperature:
        return CalibrationResult(STATUS_BLOCKED, ["no_temperature_satisfies_requested_concentration"], None)

    calibrated_temperature = min(max(raw_temperature, minimum_temperature), effective_maximum)
    certificate = {
        "source_concentration_certificate_digest": _digest(source_concentration_certificate),
        "current_temperature": current_temperature,
        "raw_temperature": raw_temperature,
        "calibrated_temperature": calibrated_temperature,
        "minimum_temperature": minimum_temperature,
        "maximum_temperature": maximum_temperature,
        "concentration_temperature_ceiling": concentration_ceiling,
        "effective_temperature_ceiling": effective_maximum,
        "target_epsilon": target_epsilon,
        "exploration_signal": exploration,
        "stabilization_signal": stabilization,
        "require_concentration_certificate": require_concentration_certificate,
        "concentration_bound_preserved": (not require_concentration_certificate) or calibrated_temperature <= concentration_ceiling,
        "qi_grants_no_authority": True,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["temperature_calibration_digest"] = _digest(certificate)
    return CalibrationResult(STATUS_READY, [], certificate)
