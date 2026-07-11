#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_information_geometric_qi_objective_kernel_v0_1 import (
    build_information_geometric_qi_kernel,
)
from runtime.kuuos_planos_kl_regularized_objective_update_kernel_v0_92 import (
    STATUS_READY,
    build_kl_regularized_objective_update,
)
from scripts.check_planos_information_geometric_qi_objective_kernel_v0_1 import (
    _paths,
    _source_state,
)


def _source_kernel() -> dict:
    return build_information_geometric_qi_kernel(
        source_state=_source_state(),
        paths=_paths(),
        base_metric={"switch": 1.0, "reroute": 1.0},
        qi={"recovery": 0.3, "stagnation": 0.4, "hysteresis": 0.2},
        history={"oscillation": 0.5},
        target_region={
            "mission_valid": True,
            "authority_valid": True,
            "resource_valid": True,
            "observable": True,
            "reversible_or_bounded": True,
            "wa_compatible": True,
        },
        selected_candidate_id="reroute",
        dissent_evidence_digests=("dissent-1",),
        qi_temperature=0.8,
        hold_floor=0.10,
        reroute_evidence=True,
    ).to_dict()


def _build(**overrides):
    args = {
        "source_kernel": _source_kernel(),
        "prior_distribution": {"continue": 0.45, "reroute": 0.35, "hold": 0.20},
        "expected_action": {"continue": 0.60, "reroute": 0.35, "hold": 1.20},
        "admissible_candidate_ids": ["continue", "reroute", "hold"],
        "beta": 1.0,
        "entropy_weight": 0.25,
        "hold_floor": 0.10,
        "selected_candidate_id": "reroute",
    }
    args.update(overrides)
    return build_kl_regularized_objective_update(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.blockers == []
    assert result.next_distribution is not None
    assert abs(sum(result.next_distribution.values()) - 1.0) < 1e-9
    assert all(value > 0.0 for value in result.next_distribution.values())
    assert result.next_distribution["hold"] >= 0.10
    assert result.selected_candidate_id == "reroute"
    assert set(result.retained_candidate_ids) == {"continue", "hold"}
    assert result.boundary["history_read_only"] is True
    assert result.boundary["future_only"] is True
    assert result.boundary["active_now"] is False
    assert result.boundary["execution_permission"] is False

    exploratory = _build(entropy_weight=2.0)
    assert exploratory.status == STATUS_READY
    assert exploratory.next_distribution is not None
    assert exploratory.next_distribution["hold"] >= 0.10

    blocked_cases = [
        _build(source_kernel={}),
        _build(beta=-1.0),
        _build(entropy_weight=-0.1),
        _build(hold_floor=1.0),
        _build(admissible_candidate_ids=[]),
        _build(admissible_candidate_ids=["reroute", "reroute"]),
        _build(admissible_candidate_ids=["outside-field"]),
        _build(prior_distribution={"continue": 0.0, "reroute": 1.0, "hold": 0.0}),
        _build(expected_action={"continue": 0.6, "reroute": -0.1, "hold": 1.2}),
        _build(selected_candidate_id="strengthen"),
    ]
    for blocked in blocked_cases:
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.next_distribution is None

    print("PASS: PlanOS v0.92 KL-regularized objective update kernel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
