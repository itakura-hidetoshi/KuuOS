#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from typing import Any

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
_TOLERANCE = 1e-12


@dataclass
class TemperatureTrajectoryStabilityCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def canonical_digest(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def compute_trajectory_window_digest(trajectory_records: list[dict]) -> str:
    return canonical_digest(trajectory_records)


def _is_finite_number(value: Any) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def _close(left: float, right: float) -> bool:
    return math.isclose(left, right, rel_tol=0.0, abs_tol=_TOLERANCE)


def _record_direction(delta: float) -> str:
    if _close(delta, 0.0):
        return "hold"
    return "increase" if delta > 0.0 else "decrease"


def _count_reversals(directions: list[str]) -> int:
    count = 0
    previous_non_hold: str | None = None
    for direction in directions:
        if direction == "hold":
            continue
        if previous_non_hold is not None and direction != previous_non_hold:
            count += 1
        previous_non_hold = direction
    return count


def _validate_thresholds(stability_thresholds: dict) -> list[str]:
    blockers: list[str] = []
    required = {
        "minimum_record_count",
        "maximum_total_variation",
        "maximum_absolute_net_drift",
        "maximum_reversal_density",
        "maximum_mean_absolute_step",
        "maximum_oscillation_measure",
    }
    if not isinstance(stability_thresholds, dict):
        return ["invalid_stability_thresholds"]
    missing = sorted(required - set(stability_thresholds))
    blockers.extend(f"missing_threshold_{name}" for name in missing)
    if missing:
        return blockers
    minimum_record_count = stability_thresholds["minimum_record_count"]
    if (
        not isinstance(minimum_record_count, int)
        or isinstance(minimum_record_count, bool)
        or minimum_record_count < 1
    ):
        blockers.append("invalid_threshold_minimum_record_count")
    for name in {
        "maximum_total_variation",
        "maximum_absolute_net_drift",
        "maximum_mean_absolute_step",
        "maximum_oscillation_measure",
    }:
        value = stability_thresholds[name]
        if not _is_finite_number(value) or float(value) < 0.0:
            blockers.append(f"invalid_threshold_{name}")
    reversal_density = stability_thresholds["maximum_reversal_density"]
    if (
        not _is_finite_number(reversal_density)
        or not 0.0 <= float(reversal_density) <= 1.0
    ):
        blockers.append("invalid_threshold_maximum_reversal_density")
    return blockers


def build_temperature_trajectory_stability_certificate(
    *,
    source_temperature_trajectory_receipt_digest: str,
    trajectory_window_digest: str,
    window_start_ordinal: int,
    window_end_ordinal: int,
    trajectory_records: list[dict],
    minimum_temperature: float,
    effective_temperature_ceiling: float,
    maximum_up_step: float,
    maximum_down_step: float,
    stability_thresholds: dict,
) -> TemperatureTrajectoryStabilityCertificateResult:
    blockers: list[str] = []
    if not source_temperature_trajectory_receipt_digest:
        blockers.append("missing_source_temperature_trajectory_receipt_digest")
    if not trajectory_window_digest:
        blockers.append("missing_trajectory_window_digest")
    if (
        not isinstance(window_start_ordinal, int)
        or isinstance(window_start_ordinal, bool)
        or window_start_ordinal < 0
    ):
        blockers.append("invalid_window_start_ordinal")
    if (
        not isinstance(window_end_ordinal, int)
        or isinstance(window_end_ordinal, bool)
        or window_end_ordinal < window_start_ordinal
    ):
        blockers.append("invalid_window_end_ordinal")
    if not isinstance(trajectory_records, list) or not trajectory_records:
        blockers.append("empty_trajectory_window")
    for name, value in {
        "minimum_temperature": minimum_temperature,
        "effective_temperature_ceiling": effective_temperature_ceiling,
        "maximum_up_step": maximum_up_step,
        "maximum_down_step": maximum_down_step,
    }.items():
        if not _is_finite_number(value):
            blockers.append(f"invalid_{name}")
    if _is_finite_number(minimum_temperature) and minimum_temperature <= 0.0:
        blockers.append("nonpositive_minimum_temperature")
    if (
        _is_finite_number(effective_temperature_ceiling)
        and _is_finite_number(minimum_temperature)
        and effective_temperature_ceiling < minimum_temperature
    ):
        blockers.append("temperature_ceiling_below_minimum")
    if _is_finite_number(maximum_up_step) and maximum_up_step < 0.0:
        blockers.append("negative_maximum_up_step")
    if _is_finite_number(maximum_down_step) and maximum_down_step < 0.0:
        blockers.append("negative_maximum_down_step")
    blockers.extend(_validate_thresholds(stability_thresholds))
    if blockers:
        return TemperatureTrajectoryStabilityCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    expected_record_count = window_end_ordinal - window_start_ordinal + 1
    if len(trajectory_records) != expected_record_count:
        blockers.append("record_count_window_length_mismatch")
    if trajectory_window_digest != compute_trajectory_window_digest(trajectory_records):
        blockers.append("trajectory_window_digest_mismatch")

    required_record_fields = {
        "prior_trajectory_digest",
        "cycle_ordinal",
        "previous_temperature",
        "target_temperature",
        "bounded_temperature",
        "temperature_delta",
        "direction",
        "disposition",
        "reversal_count",
        "oscillation_measure",
        "temperature_trajectory_receipt_digest",
    }
    valid_dispositions = {
        "hold_deadband": "hold",
        "increase_rate_limited": "increase",
        "decrease_rate_limited": "decrease",
    }
    seen_receipt_digests: set[str] = set()
    directions: list[str] = []
    deltas: list[float] = []
    oscillation_values: list[float] = []
    previous_record: dict | None = None

    for index, record in enumerate(trajectory_records):
        if not isinstance(record, dict):
            blockers.append(f"invalid_trajectory_record_{index}")
            continue
        missing_fields = sorted(required_record_fields - set(record))
        blockers.extend(
            f"missing_record_field_{index}_{field}" for field in missing_fields
        )
        if missing_fields:
            continue

        receipt_digest = record["temperature_trajectory_receipt_digest"]
        if not isinstance(receipt_digest, str) or not receipt_digest:
            blockers.append(f"invalid_record_digest_{index}")
        else:
            if receipt_digest in seen_receipt_digests:
                blockers.append("duplicate_trajectory_record")
            seen_receipt_digests.add(receipt_digest)
            record_payload = dict(record)
            del record_payload["temperature_trajectory_receipt_digest"]
            if canonical_digest(record_payload) != receipt_digest:
                blockers.append(f"record_digest_mismatch_{index}")

        ordinal = record["cycle_ordinal"]
        expected_ordinal = window_start_ordinal + index
        if (
            not isinstance(ordinal, int)
            or isinstance(ordinal, bool)
            or ordinal != expected_ordinal
        ):
            blockers.append("cycle_ordinal_not_contiguous")

        prior_digest = record["prior_trajectory_digest"]
        if not isinstance(prior_digest, str) or not prior_digest:
            blockers.append(f"missing_prior_trajectory_digest_{index}")
        if previous_record is not None:
            previous_digest = previous_record.get(
                "temperature_trajectory_receipt_digest"
            )
            if prior_digest != previous_digest:
                blockers.append("trajectory_digest_chain_mismatch")

        numeric_fields = {
            "previous_temperature": record["previous_temperature"],
            "target_temperature": record["target_temperature"],
            "bounded_temperature": record["bounded_temperature"],
            "temperature_delta": record["temperature_delta"],
            "oscillation_measure": record["oscillation_measure"],
        }
        numeric_valid = True
        for field, value in numeric_fields.items():
            if not _is_finite_number(value):
                blockers.append(f"invalid_record_{field}_{index}")
                numeric_valid = False
        reversal_count = record["reversal_count"]
        if (
            not isinstance(reversal_count, int)
            or isinstance(reversal_count, bool)
            or reversal_count < 0
        ):
            blockers.append(f"invalid_record_reversal_count_{index}")

        if numeric_valid:
            previous_temperature = float(record["previous_temperature"])
            target_temperature = float(record["target_temperature"])
            bounded_temperature = float(record["bounded_temperature"])
            recorded_delta = float(record["temperature_delta"])
            oscillation_measure = float(record["oscillation_measure"])
            for field, value in {
                "previous_temperature": previous_temperature,
                "target_temperature": target_temperature,
                "bounded_temperature": bounded_temperature,
            }.items():
                if value <= 0.0:
                    blockers.append(f"nonpositive_record_{field}_{index}")
                if value < minimum_temperature - _TOLERANCE:
                    blockers.append(f"minimum_temperature_violation_{index}")
                if value > effective_temperature_ceiling + _TOLERANCE:
                    blockers.append(f"temperature_ceiling_violation_{index}")
            if oscillation_measure < 0.0:
                blockers.append(f"negative_oscillation_measure_{index}")

            computed_delta = bounded_temperature - previous_temperature
            if not _close(recorded_delta, computed_delta):
                blockers.append("temperature_delta_identity_mismatch")
            computed_direction = _record_direction(computed_delta)
            if record["direction"] != computed_direction:
                blockers.append("direction_delta_mismatch")
            disposition = record["disposition"]
            if disposition not in valid_dispositions:
                blockers.append("invalid_record_disposition")
            elif valid_dispositions[disposition] != computed_direction:
                blockers.append("direction_disposition_mismatch")
            if computed_delta > maximum_up_step + _TOLERANCE:
                blockers.append("maximum_up_step_violation")
            if -computed_delta > maximum_down_step + _TOLERANCE:
                blockers.append("maximum_down_step_violation")
            if previous_record is not None:
                previous_bounded = previous_record.get("bounded_temperature")
                if _is_finite_number(previous_bounded) and not _close(
                    previous_temperature, float(previous_bounded)
                ):
                    blockers.append("temperature_trajectory_discontinuity")
            directions.append(computed_direction)
            deltas.append(computed_delta)
            oscillation_values.append(oscillation_measure)
        previous_record = record

    if trajectory_records and isinstance(trajectory_records[-1], dict):
        final_digest = trajectory_records[-1].get(
            "temperature_trajectory_receipt_digest"
        )
        if source_temperature_trajectory_receipt_digest != final_digest:
            blockers.append("source_trajectory_receipt_digest_mismatch")

    if blockers:
        return TemperatureTrajectoryStabilityCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    record_count = len(trajectory_records)
    hold_count = directions.count("hold")
    increase_count = directions.count("increase")
    decrease_count = directions.count("decrease")
    reversal_count = _count_reversals(directions)
    total_variation = sum(abs(delta) for delta in deltas)
    net_temperature_drift = (
        float(trajectory_records[-1]["bounded_temperature"])
        - float(trajectory_records[0]["previous_temperature"])
    )
    maximum_observed_step = max((abs(delta) for delta in deltas), default=0.0)
    mean_absolute_step = total_variation / record_count
    reversal_density = reversal_count / max(1, record_count - 1)
    oscillation_measure = max(oscillation_values, default=0.0)

    minimum_record_count = stability_thresholds["minimum_record_count"]
    if record_count < minimum_record_count:
        stability_disposition = "insufficient_evidence"
    elif (
        reversal_density > stability_thresholds["maximum_reversal_density"]
        or oscillation_measure
        > stability_thresholds["maximum_oscillation_measure"]
    ):
        stability_disposition = "oscillatory"
    elif abs(net_temperature_drift) > stability_thresholds[
        "maximum_absolute_net_drift"
    ]:
        stability_disposition = "drifting"
    elif (
        total_variation <= stability_thresholds["maximum_total_variation"]
        and mean_absolute_step
        <= stability_thresholds["maximum_mean_absolute_step"]
    ):
        stability_disposition = "stable"
    else:
        midpoint = max(1, record_count // 2)
        early_steps = [abs(delta) for delta in deltas[:midpoint]]
        late_steps = [abs(delta) for delta in deltas[midpoint:]]
        early_mean = sum(early_steps) / len(early_steps)
        late_mean = (
            sum(late_steps) / len(late_steps) if late_steps else early_mean
        )
        stability_disposition = (
            "damped" if late_mean <= early_mean + _TOLERANCE else "drifting"
        )

    certificate = {
        "source_trajectory_receipt_digest": source_temperature_trajectory_receipt_digest,
        "trajectory_window_digest": trajectory_window_digest,
        "window_start_ordinal": window_start_ordinal,
        "window_end_ordinal": window_end_ordinal,
        "record_count": record_count,
        "hold_count": hold_count,
        "increase_count": increase_count,
        "decrease_count": decrease_count,
        "reversal_count": reversal_count,
        "total_variation": total_variation,
        "net_temperature_drift": net_temperature_drift,
        "maximum_observed_step": maximum_observed_step,
        "mean_absolute_step": mean_absolute_step,
        "oscillation_measure": oscillation_measure,
        "rate_limit_preserved": True,
        "temperature_bounds_preserved": True,
        "concentration_ceiling_preserved": True,
        "ordinal_continuity_preserved": True,
        "digest_chain_preserved": True,
        "stability_disposition": stability_disposition,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["stability_certificate_digest"] = canonical_digest(certificate)
    return TemperatureTrajectoryStabilityCertificateResult(
        STATUS_READY, [], certificate
    )
