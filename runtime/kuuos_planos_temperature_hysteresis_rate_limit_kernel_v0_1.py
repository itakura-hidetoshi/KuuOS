#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from json import dumps
from math import isfinite

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


def _digest(payload: dict) -> str:
    return sha256(dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _finite_nonnegative(value: float) -> bool:
    return isfinite(value) and value >= 0.0


@dataclass(frozen=True)
class TemperatureHysteresisResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def build_temperature_hysteresis_rate_limit(
    *,
    source_calibration: dict,
    current_temperature: float,
    target_temperature: float,
    deadband: float,
    max_up_step: float,
    max_down_step: float,
    oscillation: float,
    reversal_count: int,
) -> TemperatureHysteresisResult:
    blockers: list[str] = []
    if not source_calibration:
        blockers.append("missing_source_calibration")
    for name, value in {
        "current_temperature": current_temperature,
        "target_temperature": target_temperature,
        "deadband": deadband,
        "max_up_step": max_up_step,
        "max_down_step": max_down_step,
        "oscillation": oscillation,
    }.items():
        if not _finite_nonnegative(float(value)):
            blockers.append(f"invalid_{name}")
    if current_temperature <= 0 or target_temperature <= 0:
        blockers.append("nonpositive_temperature")
    if reversal_count < 0:
        blockers.append("invalid_reversal_count")

    minimum = float(source_calibration.get("minimum_temperature", 0.0))
    maximum = float(source_calibration.get("maximum_temperature", 0.0))
    concentration_ceiling = float(source_calibration.get("effective_temperature_ceiling", maximum))
    if not (0.0 < minimum <= maximum and concentration_ceiling > 0.0):
        blockers.append("invalid_source_bounds")
    effective_ceiling = min(maximum, concentration_ceiling)
    if minimum > effective_ceiling:
        blockers.append("empty_effective_interval")

    if blockers:
        return TemperatureHysteresisResult(STATUS_BLOCKED, blockers, None)

    effective_deadband = deadband * (1.0 + oscillation + reversal_count)
    effective_up = max_up_step / (1.0 + oscillation + reversal_count)
    effective_down = max_down_step / (1.0 + oscillation + reversal_count)
    delta = target_temperature - current_temperature

    if abs(delta) <= effective_deadband:
        proposed = current_temperature
        disposition = "hold_deadband"
    elif delta > 0:
        proposed = current_temperature + min(delta, effective_up)
        disposition = "increase_rate_limited"
    else:
        proposed = current_temperature - min(-delta, effective_down)
        disposition = "decrease_rate_limited"

    bounded = min(max(proposed, minimum), effective_ceiling)
    receipt = {
        "source_temperature_calibration_digest": source_calibration.get("temperature_calibration_digest", ""),
        "current_temperature": current_temperature,
        "target_temperature": target_temperature,
        "effective_deadband": effective_deadband,
        "effective_up_step": effective_up,
        "effective_down_step": effective_down,
        "proposed_temperature": proposed,
        "bounded_temperature": bounded,
        "minimum_temperature": minimum,
        "effective_temperature_ceiling": effective_ceiling,
        "disposition": disposition,
        "rate_limit_preserved": abs(bounded - current_temperature) <= max(effective_up, effective_down) + 1e-12,
        "concentration_bound_preserved": bounded <= effective_ceiling + 1e-12,
        "qi_grants_no_authority": True,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["temperature_hysteresis_rate_limit_digest"] = _digest(receipt)
    return TemperatureHysteresisResult(STATUS_READY, [], receipt)
