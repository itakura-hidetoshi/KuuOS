#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_information_geometric_qi_objective_kernel_v0_1 import (
    CANDIDATE_FIELD,
    STATUS_READY,
    build_information_geometric_qi_kernel,
    qi_condition_metric,
)


def _source_state() -> dict:
    return {
        "world_state_digest": "world-current",
        "plan_parameter_digest": "theta-current",
        "qi_process_tensor_digest": "qi-current",
        "history_digest": "history-read-only",
        "constraint_digest": "mission-resource-risk-verification",
        "authority_digest": "authority-current",
        "current_distribution": {"continue": 0.4, "hold": 0.3, "reroute": 0.3},
    }


def _paths() -> list[dict]:
    return [
        {
            "path_id": "path-continue",
            "candidate_id": "continue",
            "transition_action": 0.2,
            "mission_potential": 0.0,
            "risk_potential": 0.1,
            "resource_potential": 0.0,
            "authority_potential": 0.0,
            "verification_potential": 0.1,
            "wa_relational_potential": 0.1,
            "qi_potential": 0.0,
            "history_potential": 0.1,
            "admissible": True,
        },
        {
            "path_id": "path-reroute",
            "candidate_id": "reroute",
            "transition_action": 0.4,
            "mission_potential": 0.0,
            "risk_potential": 0.1,
            "resource_potential": 0.1,
            "authority_potential": 0.0,
            "verification_potential": 0.0,
            "wa_relational_potential": 0.1,
            "qi_potential": 0.0,
            "history_potential": 0.0,
            "admissible": True,
        },
        {
            "path_id": "path-hold",
            "candidate_id": "hold",
            "transition_action": 1.5,
            "mission_potential": 0.0,
            "risk_potential": 0.0,
            "resource_potential": 0.0,
            "authority_potential": 0.0,
            "verification_potential": 0.0,
            "wa_relational_potential": 0.0,
            "qi_potential": 0.0,
            "history_potential": 0.0,
            "admissible": True,
        },
        {
            "path_id": "path-forbidden",
            "candidate_id": "strengthen",
            "transition_action": 0.0,
            "mission_potential": 0.0,
            "risk_potential": 0.0,
            "resource_potential": 0.0,
            "authority_potential": 1.0,
            "verification_potential": 0.0,
            "wa_relational_potential": 0.0,
            "qi_potential": 0.0,
            "history_potential": 0.0,
            "admissible": True,
        },
    ]


def _build(**overrides):
    args = {
        "source_state": _source_state(),
        "paths": _paths(),
        "base_metric": {"switch": 1.0, "reroute": 1.0},
        "qi": {"recovery": 0.3, "stagnation": 0.4, "hysteresis": 0.2},
        "history": {"oscillation": 0.5},
        "target_region": {
            "mission_valid": True,
            "authority_valid": True,
            "resource_valid": True,
            "observable": True,
            "reversible_or_bounded": True,
            "wa_compatible": True,
        },
        "selected_candidate_id": "reroute",
        "dissent_evidence_digests": ("dissent-1",),
        "qi_temperature": 0.8,
        "hold_floor": 0.10,
        "reroute_evidence": True,
    }
    args.update(overrides)
    return build_information_geometric_qi_kernel(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.blockers == []
    assert result.path_distribution is not None
    assert result.objective_update is not None

    weights = result.path_distribution["normalized_path_weights"]
    masses = result.path_distribution["candidate_mass_map"]
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    assert abs(sum(masses.values()) - 1.0) < 1e-9
    assert weights["path-forbidden"] == 0.0
    assert masses["hold"] >= 0.10
    assert set(masses) == set(CANDIDATE_FIELD)

    update = result.objective_update
    assert update["selected_candidate_id"] == "reroute"
    assert "hold" in update["retained_candidate_ids"]
    assert update["future_only"] is True
    assert update["active_now"] is False
    assert update["execution_permission"] is False

    metric_without_evidence = qi_condition_metric(
        {"switch": 1.0, "reroute": 1.0},
        {"recovery": 0.3, "stagnation": 0.4, "hysteresis": 0.2},
        {"oscillation": 0.5},
        reroute_evidence=False,
    )
    metric_with_evidence = qi_condition_metric(
        {"switch": 1.0, "reroute": 1.0},
        {"recovery": 0.3, "stagnation": 0.4, "hysteresis": 0.2},
        {"oscillation": 0.5},
        reroute_evidence=True,
    )
    assert metric_without_evidence["switch"] >= 1.0
    assert metric_with_evidence["reroute"] < metric_without_evidence["reroute"]
    assert all(value >= 0.0 for value in metric_with_evidence.values())

    blocked_cases = [
        _build(source_state={}),
        _build(target_region={}),
        _build(qi_temperature=0.0),
        _build(hold_floor=1.0),
        _build(base_metric={"switch": -1.0}),
        _build(paths=[]),
        _build(selected_candidate_id="unknown"),
    ]
    tampered_paths = deepcopy(_paths())
    tampered_paths[0]["candidate_id"] = "outside-field"
    blocked_cases.append(_build(paths=tampered_paths))
    duplicate_paths = deepcopy(_paths())
    duplicate_paths[1]["path_id"] = duplicate_paths[0]["path_id"]
    blocked_cases.append(_build(paths=duplicate_paths))

    for blocked in blocked_cases:
        assert blocked.status != STATUS_READY
        assert blocked.blockers
        assert blocked.objective_update is None

    print("PASS: PlanOS Information-Geometric Qi Objective Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
