#!/usr/bin/env python3
from copy import deepcopy

from runtime.kuuos_planos_qi_conditioned_information_metric_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_qi_conditioned_information_metric_certificate,
    compute_base_metric_digest,
    compute_conditioned_transition_action,
    compute_parameter_coordinate_schema_digest,
)


def _metric_entries():
    return [
        {"coordinate": "goal", "weight": 1.0},
        {"coordinate": "switch", "weight": 1.2},
        {"coordinate": "reroute", "weight": 0.9},
        {"coordinate": "verification", "weight": 1.1},
    ]


def _build(**overrides):
    metric_entries = overrides.pop("base_metric_weights", _metric_entries())
    args = {
        "source_objective_kernel_digest": "source-v091-objective-kernel",
        "parameter_coordinate_schema_digest": (
            compute_parameter_coordinate_schema_digest(metric_entries)
        ),
        "base_metric_digest": compute_base_metric_digest(metric_entries),
        "base_metric_weights": metric_entries,
        "minimum_metric_weight": 0.25,
        "maximum_metric_weight": 3.0,
        "qi_process_tensor": {
            "activation": 0.5,
            "stagnation": 0.8,
            "tension": 0.4,
            "recovery": 0.7,
            "coherence": 0.8,
            "coupling": 0.6,
            "transition_readiness": 0.5,
            "hysteresis": 0.3,
        },
        "history_oscillation_measure": 0.4,
        "reroute_evidence_digest": "reroute-evidence-v1",
        "reroute_evidence_present": True,
        "recovery_coefficient": 0.5,
        "stagnation_coefficient": 0.4,
        "hysteresis_coefficient": 0.3,
        "oscillation_coefficient": 0.2,
        "transition_direction_map": {
            "goal": "neutral",
            "switch": "switch",
            "reroute": "reroute",
            "verification": "neutral",
        },
    }
    args.update(overrides)
    return build_qi_conditioned_information_metric_certificate(**args)


def main() -> int:
    result = _build()
    assert result.status == STATUS_READY
    assert result.certificate is not None
    certificate = result.certificate
    weights = certificate["conditioned_metric_weights"]

    assert weights["switch"] > 1.2
    assert weights["reroute"] < 0.9
    assert weights["goal"] == 1.0
    assert certificate["metric_nonnegativity_preserved"] is True
    assert certificate["metric_floor_preserved"] is True
    assert certificate["metric_ceiling_preserved"] is True
    assert certificate["evidence_gate_preserved"] is True
    assert certificate["recovery_protection_preserved"] is True
    assert certificate["hysteresis_resistance_preserved"] is True
    assert certificate["oscillation_resistance_preserved"] is True
    assert certificate["history_read_only"] is True
    assert certificate["qi_grants_no_authority"] is True
    assert certificate["future_only"] is True
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    action = compute_conditioned_transition_action(
        weights,
        {
            "goal": 0.1,
            "switch": -0.2,
            "reroute": 0.3,
            "verification": 0.0,
        },
    )
    assert action >= 0.0

    no_evidence = _build(reroute_evidence_present=False)
    assert no_evidence.status == STATUS_READY
    assert no_evidence.certificate is not None
    assert (
        no_evidence.certificate["evidence_gated_reroute_discount"]["reroute"]
        == 0.0
    )
    assert (
        no_evidence.certificate["conditioned_metric_weights"]["reroute"]
        == 0.9
    )

    floor_clipped = _build(
        stagnation_coefficient=10.0,
        minimum_metric_weight=0.25,
    )
    assert floor_clipped.status == STATUS_READY
    assert floor_clipped.certificate is not None
    assert (
        floor_clipped.certificate["conditioned_metric_weights"]["reroute"]
        == 0.25
    )

    duplicate_entries = _metric_entries() + [
        {"coordinate": "switch", "weight": 1.3}
    ]
    invalid_direction_map = deepcopy(
        {
            "goal": "neutral",
            "switch": "switch",
            "reroute": "reroute",
            "verification": "neutral",
        }
    )
    invalid_direction_map["switch"] = "unknown"

    blocked = [
        _build(source_objective_kernel_digest=""),
        _build(parameter_coordinate_schema_digest="wrong"),
        _build(base_metric_digest="wrong"),
        _build(base_metric_weights=duplicate_entries),
        _build(
            base_metric_weights=[
                {"coordinate": "goal", "weight": -1.0},
            ],
            transition_direction_map={"goal": "neutral"},
        ),
        _build(minimum_metric_weight=0.0),
        _build(maximum_metric_weight=0.1),
        _build(history_oscillation_measure=1.1),
        _build(recovery_coefficient=-0.1),
        _build(
            qi_process_tensor={
                "activation": 1.1,
                "stagnation": 0.8,
                "tension": 0.4,
                "recovery": 0.7,
                "coherence": 0.8,
                "coupling": 0.6,
                "transition_readiness": 0.5,
                "hysteresis": 0.3,
            }
        ),
        _build(reroute_evidence_digest=""),
        _build(
            transition_direction_map={
                "goal": "neutral",
                "switch": "switch",
                "reroute": "reroute",
            }
        ),
        _build(transition_direction_map=invalid_direction_map),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    try:
        compute_conditioned_transition_action(
            {"goal": 1.0},
            {"other": 0.2},
        )
    except ValueError:
        pass
    else:
        raise AssertionError("coordinate mismatch must fail closed")

    print(
        "PASS: PlanOS Qi-Conditioned Information Metric "
        "Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
