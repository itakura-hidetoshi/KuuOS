#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_zero_temperature_minimal_action_limit_kernel_v0_1 import (
    STATUS_READY,
    build_zero_temperature_minimal_action_limit,
)


def _source() -> dict:
    return {
        "receipt_digest": "kl-update-receipt",
        "boundary": {
            "future_only": True,
            "execution_permission": False,
        },
    }


def main() -> int:
    result = build_zero_temperature_minimal_action_limit(
        _source(),
        candidate_actions={"continue": 1.0, "hold": 0.5, "reroute": 0.5},
        temperature=0.05,
        selected_candidate_id="hold",
    )
    assert result.status == STATUS_READY
    assert result.blockers == []
    assert result.minimal_action == 0.5
    assert result.minimal_action_candidate_ids == ["hold", "reroute"]
    assert abs(sum(result.positive_temperature_distribution.values()) - 1.0) < 1e-9
    assert abs(sum(result.zero_temperature_limit_distribution.values()) - 1.0) < 1e-9
    assert result.zero_temperature_limit_distribution["continue"] == 0.0
    assert result.zero_temperature_limit_distribution["hold"] == 0.5
    assert result.boundary["authority_invariance_preserved"] is True
    assert result.boundary["future_only"] is True
    assert result.boundary["active_now"] is False
    assert result.boundary["execution_permission"] is False

    blocked = [
        build_zero_temperature_minimal_action_limit({}, candidate_actions={"hold": 0.0}),
        build_zero_temperature_minimal_action_limit(_source(), candidate_actions={}, temperature=0.1),
        build_zero_temperature_minimal_action_limit(_source(), candidate_actions={"hold": -1.0}),
        build_zero_temperature_minimal_action_limit(_source(), candidate_actions={"hold": 0.0}, temperature=0.0),
        build_zero_temperature_minimal_action_limit(
            _source(),
            candidate_actions={"hold": 0.0, "reroute": 1.0},
            selected_candidate_id="reroute",
        ),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers

    print("PASS: PlanOS v0.93 zero-temperature minimal-action limit kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
