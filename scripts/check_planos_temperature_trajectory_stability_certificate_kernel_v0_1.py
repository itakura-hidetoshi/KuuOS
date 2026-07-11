#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_temperature_trajectory_stability_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_temperature_trajectory_stability_certificate,
    canonical_digest,
    compute_trajectory_window_digest,
)


def _record(
    *,
    prior_digest: str,
    ordinal: int,
    previous: float,
    bounded: float,
    target: float,
    disposition: str,
    reversal_count: int,
    oscillation_measure: float,
) -> dict:
    delta = bounded - previous
    direction = "hold" if abs(delta) <= 1e-12 else (
        "increase" if delta > 0.0 else "decrease"
    )
    record = {
        "source_rate_limit_receipt_digest": f"source-v096-{ordinal}",
        "prior_trajectory_digest": prior_digest,
        "cycle_ordinal": ordinal,
        "previous_temperature": previous,
        "target_temperature": target,
        "bounded_temperature": bounded,
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
    record["temperature_trajectory_receipt_digest"] = canonical_digest(record)
    return record


def _records() -> list[dict]:
    records: list[dict] = []
    prior = "trajectory-before-window"
    cases = [
        (7, 0.50, 0.60, 0.70, "increase_rate_limited", 0, 0.10),
        (8, 0.60, 0.65, 0.70, "increase_rate_limited", 0, 0.12),
        (9, 0.65, 0.65, 0.65, "hold_deadband", 0, 0.12),
        (10, 0.65, 0.64, 0.60, "decrease_rate_limited", 1, 0.20),
    ]
    for ordinal, previous, bounded, target, disposition, reversals, oscillation in cases:
        record = _record(
            prior_digest=prior,
            ordinal=ordinal,
            previous=previous,
            bounded=bounded,
            target=target,
            disposition=disposition,
            reversal_count=reversals,
            oscillation_measure=oscillation,
        )
        records.append(record)
        prior = record["temperature_trajectory_receipt_digest"]
    return records


def _build(records: list[dict] | None = None, **overrides):
    records = deepcopy(_records() if records is None else records)
    args = {
        "source_temperature_trajectory_receipt_digest": records[-1][
            "temperature_trajectory_receipt_digest"
        ] if records else "missing-final",
        "trajectory_window_digest": compute_trajectory_window_digest(records),
        "window_start_ordinal": 7,
        "window_end_ordinal": 10,
        "trajectory_records": records,
        "minimum_temperature": 0.1,
        "effective_temperature_ceiling": 1.0,
        "maximum_up_step": 0.1,
        "maximum_down_step": 0.1,
        "stability_thresholds": {
            "minimum_record_count": 3,
            "maximum_total_variation": 0.2,
            "maximum_absolute_net_drift": 0.2,
            "maximum_reversal_density": 0.4,
            "maximum_mean_absolute_step": 0.05,
            "maximum_oscillation_measure": 0.3,
        },
    }
    args.update(overrides)
    return build_temperature_trajectory_stability_certificate(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.certificate is not None
    certificate = result.certificate
    assert certificate["record_count"] == 4
    assert certificate["hold_count"] == 1
    assert certificate["increase_count"] == 2
    assert certificate["decrease_count"] == 1
    assert certificate["reversal_count"] == 1
    assert certificate["stability_disposition"] == "stable"
    assert certificate["rate_limit_preserved"] is True
    assert certificate["temperature_bounds_preserved"] is True
    assert certificate["concentration_ceiling_preserved"] is True
    assert certificate["ordinal_continuity_preserved"] is True
    assert certificate["digest_chain_preserved"] is True
    assert certificate["history_read_only"] is True
    assert certificate["qi_grants_no_authority"] is True
    assert certificate["future_only"] is True
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    records = _records()
    bad_ordinal = deepcopy(records)
    bad_ordinal[1]["cycle_ordinal"] = 9
    bad_chain = deepcopy(records)
    bad_chain[1]["prior_trajectory_digest"] = "wrong"
    bad_delta = deepcopy(records)
    bad_delta[0]["temperature_delta"] = 9.0
    bad_direction = deepcopy(records)
    bad_direction[0]["direction"] = "decrease"
    bad_temperature = deepcopy(records)
    bad_temperature[0]["previous_temperature"] = 0.0
    excessive_step = deepcopy(records)
    excessive_step[0]["bounded_temperature"] = 0.9
    duplicate = [deepcopy(records[0]), deepcopy(records[0])]

    blocked = [
        _build(source_temperature_trajectory_receipt_digest=""),
        _build(records=[], window_end_ordinal=6),
        _build(bad_ordinal),
        _build(bad_chain),
        _build(bad_delta),
        _build(bad_direction),
        _build(bad_temperature),
        _build(excessive_step),
        _build(records, trajectory_window_digest="wrong"),
        _build(records, source_temperature_trajectory_receipt_digest="wrong"),
        _build(duplicate, window_start_ordinal=7, window_end_ordinal=8),
        _build(records, window_end_ordinal=11),
        _build(records, effective_temperature_ceiling=0.55),
        _build(records, maximum_up_step=0.01),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print("PASS: PlanOS Temperature Trajectory Stability Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
