#!/usr/bin/env python3
from runtime.kuuos_planos_temperature_hysteresis_rate_limit_kernel_v0_1 import (
    STATUS_READY,
    build_temperature_hysteresis_rate_limit,
)


def source() -> dict:
    return {
        "minimum_temperature": 0.05,
        "maximum_temperature": 1.0,
        "effective_temperature_ceiling": 0.6,
        "temperature_calibration_digest": "calibration-v0-95",
    }


def main() -> int:
    result = build_temperature_hysteresis_rate_limit(
        source_calibration=source(),
        current_temperature=0.4,
        target_temperature=0.8,
        deadband=0.02,
        max_up_step=0.1,
        max_down_step=0.15,
        oscillation=0.5,
        reversal_count=1,
    )
    assert result.status == STATUS_READY
    assert result.receipt is not None
    receipt = result.receipt
    assert 0.05 <= receipt["bounded_temperature"] <= 0.6
    assert receipt["rate_limit_preserved"]
    assert receipt["concentration_bound_preserved"]
    assert receipt["future_only"] and not receipt["active_now"]
    assert not receipt["execution_permission"]

    held = build_temperature_hysteresis_rate_limit(
        source_calibration=source(), current_temperature=0.4, target_temperature=0.41,
        deadband=0.02, max_up_step=0.1, max_down_step=0.1, oscillation=0.0, reversal_count=0,
    )
    assert held.receipt["bounded_temperature"] == 0.4
    assert held.receipt["disposition"] == "hold_deadband"

    blocked = [
        build_temperature_hysteresis_rate_limit(source_calibration={}, current_temperature=0.4, target_temperature=0.5, deadband=0.1, max_up_step=0.1, max_down_step=0.1, oscillation=0.0, reversal_count=0),
        build_temperature_hysteresis_rate_limit(source_calibration=source(), current_temperature=0.0, target_temperature=0.5, deadband=0.1, max_up_step=0.1, max_down_step=0.1, oscillation=0.0, reversal_count=0),
        build_temperature_hysteresis_rate_limit(source_calibration=source(), current_temperature=0.4, target_temperature=0.5, deadband=-0.1, max_up_step=0.1, max_down_step=0.1, oscillation=0.0, reversal_count=0),
    ]
    assert all(item.status != STATUS_READY and item.blockers for item in blocked)
    print("PASS: PlanOS Temperature Hysteresis and Rate-Limit Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
