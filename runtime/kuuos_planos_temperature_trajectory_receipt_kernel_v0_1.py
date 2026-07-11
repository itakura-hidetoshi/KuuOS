#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class TemperatureTrajectoryReceiptResult:
    status: str
    blockers: list[str]
    receipt: dict | None


def _digest(payload: dict) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def build_temperature_trajectory_receipt(
    *,
    source_rate_limit_receipt: dict,
    previous_temperature: float,
    bounded_temperature: float,
    target_temperature: float,
    disposition: str,
    cycle_ordinal: int,
    prior_trajectory_digest: str,
    reversal_count: int,
    oscillation_measure: float,
) -> TemperatureTrajectoryReceiptResult:
    blockers: list[str] = []
    valid_dispositions = {
        "hold_deadband",
        "increase_rate_limited",
        "decrease_rate_limited",
    }
    if not source_rate_limit_receipt:
        blockers.append("missing_source_rate_limit_receipt")
    for name, value in {
        "previous_temperature": previous_temperature,
        "bounded_temperature": bounded_temperature,
        "target_temperature": target_temperature,
        "oscillation_measure": oscillation_measure,
    }.items():
        if not math.isfinite(value) or value < 0.0:
            blockers.append(f"invalid_{name}")
    if disposition not in valid_dispositions:
        blockers.append("invalid_disposition")
    if cycle_ordinal < 0:
        blockers.append("invalid_cycle_ordinal")
    if reversal_count < 0:
        blockers.append("invalid_reversal_count")
    if not prior_trajectory_digest:
        blockers.append("missing_prior_trajectory_digest")
    delta = bounded_temperature - previous_temperature
    if disposition == "hold_deadband" and abs(delta) > 1e-12:
        blockers.append("hold_disposition_changed_temperature")
    if disposition == "increase_rate_limited" and delta < 0.0:
        blockers.append("increase_disposition_moved_down")
    if disposition == "decrease_rate_limited" and delta > 0.0:
        blockers.append("decrease_disposition_moved_up")
    if blockers:
        return TemperatureTrajectoryReceiptResult(STATUS_BLOCKED, blockers, None)
    direction = "hold" if abs(delta) <= 1e-12 else ("increase" if delta > 0 else "decrease")
    receipt = {
        "source_rate_limit_receipt_digest": _digest(source_rate_limit_receipt),
        "prior_trajectory_digest": prior_trajectory_digest,
        "cycle_ordinal": cycle_ordinal,
        "previous_temperature": previous_temperature,
        "target_temperature": target_temperature,
        "bounded_temperature": bounded_temperature,
        "temperature_delta": delta,
        "direction": direction,
        "disposition": disposition,
        "reversal_count": reversal_count,
        "oscillation_measure": oscillation_measure,
        "trajectory_append_count": 1,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    receipt["temperature_trajectory_receipt_digest"] = _digest(receipt)
    return TemperatureTrajectoryReceiptResult(STATUS_READY, [], receipt)
