#!/usr/bin/env python3
from runtime.kuuos_planos_adaptive_qi_temperature_calibration_kernel_v0_1 import (
    STATUS_READY,
    build_adaptive_qi_temperature_calibration,
)


def source() -> dict:
    return {
        "minimum_positive_action_gap": 1.2,
        "minimal_action_candidate_count": 2,
        "nonminimal_candidate_count": 3,
        "epsilon_concentration_certified": True,
    }


def main() -> int:
    result = build_adaptive_qi_temperature_calibration(
        source_concentration_certificate=source(),
        current_temperature=0.25,
        minimum_temperature=0.05,
        maximum_temperature=1.0,
        target_epsilon=0.1,
        qi_state={
            "activation": 0.8,
            "stagnation": 0.5,
            "recovery": 0.2,
            "coherence": 0.6,
            "transition_readiness": 0.7,
            "hysteresis": 0.3,
        },
        history_state={"oscillation": 0.2},
    )
    assert result.status == STATUS_READY
    assert result.certificate is not None
    cert = result.certificate
    assert cert["minimum_temperature"] <= cert["calibrated_temperature"] <= cert["effective_temperature_ceiling"]
    assert cert["concentration_bound_preserved"] is True
    assert cert["future_only"] is True
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False
    assert cert["qi_grants_no_authority"] is True

    blocked = [
        build_adaptive_qi_temperature_calibration(
            source_concentration_certificate={}, current_temperature=0.2,
            minimum_temperature=0.05, maximum_temperature=1.0, target_epsilon=0.1,
            qi_state={}, history_state={}
        ),
        build_adaptive_qi_temperature_calibration(
            source_concentration_certificate=source(), current_temperature=0.2,
            minimum_temperature=1.1, maximum_temperature=1.0, target_epsilon=0.1,
            qi_state={}, history_state={}
        ),
        build_adaptive_qi_temperature_calibration(
            source_concentration_certificate={
                "minimum_positive_action_gap": 0.0,
                "minimal_action_candidate_count": 1,
                "nonminimal_candidate_count": 2,
            }, current_temperature=0.2, minimum_temperature=0.05,
            maximum_temperature=1.0, target_epsilon=0.1,
            qi_state={}, history_state={}
        ),
    ]
    assert all(item.status != STATUS_READY and item.blockers for item in blocked)
    print("PASS: PlanOS Adaptive Qi Temperature Calibration Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
