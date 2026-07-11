#!/usr/bin/env python3
from runtime.kuuos_planos_temperature_trajectory_receipt_kernel_v0_1 import (
    STATUS_READY,
    build_temperature_trajectory_receipt,
)


def _build(**overrides):
    args = {
        "source_rate_limit_receipt": {"digest": "source-v096"},
        "previous_temperature": 0.5,
        "bounded_temperature": 0.6,
        "target_temperature": 0.9,
        "disposition": "increase_rate_limited",
        "cycle_ordinal": 7,
        "prior_trajectory_digest": "trajectory-prior",
        "reversal_count": 1,
        "oscillation_measure": 0.2,
    }
    args.update(overrides)
    return build_temperature_trajectory_receipt(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.receipt is not None
    assert result.receipt["trajectory_append_count"] == 1
    assert result.receipt["direction"] == "increase"
    assert result.receipt["history_read_only"] is True
    assert result.receipt["qi_grants_no_authority"] is True
    assert result.receipt["future_only"] is True
    assert result.receipt["active_now"] is False
    assert result.receipt["execution_permission"] is False

    blocked = [
        _build(source_rate_limit_receipt={}),
        _build(previous_temperature=-1.0),
        _build(disposition="unknown"),
        _build(cycle_ordinal=-1),
        _build(prior_trajectory_digest=""),
        _build(reversal_count=-1),
        _build(disposition="hold_deadband", bounded_temperature=0.6),
        _build(disposition="increase_rate_limited", bounded_temperature=0.4),
        _build(disposition="decrease_rate_limited", bounded_temperature=0.6),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.receipt is None
    print("PASS: PlanOS Temperature Trajectory Receipt Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
