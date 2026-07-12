#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_state_dependent_metric_jet_levi_civita_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_state_dependent_metric_jet_levi_civita_certificate,
    canonical_digest,
    compute_candidate_tangent_bundle_digest,
    compute_metric_jet_digest,
    compute_plan_coordinate_schema_digest,
    compute_state_context_digest,
)


def coordinates() -> list[str]:
    return ["goal", "reroute", "verification"]


def metric_matrix() -> dict:
    return {
        "goal": {"goal": 1.0925, "reroute": -0.0475, "verification": 0.0475},
        "reroute": {"goal": -0.0475, "reroute": 0.9025, "verification": 0.0675},
        "verification": {
            "goal": 0.0475,
            "reroute": 0.0675,
            "verification": 1.3325,
        },
    }


def invert_matrix(matrix: dict) -> dict:
    names = sorted(matrix)
    n = len(names)
    augmented = [
        [float(matrix[names[i]][names[j]]) for j in range(n)]
        + [1.0 if i == j else 0.0 for j in range(n)]
        for i in range(n)
    ]
    for pivot_index in range(n):
        pivot_row = max(
            range(pivot_index, n),
            key=lambda row: abs(augmented[row][pivot_index]),
        )
        augmented[pivot_index], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[pivot_index],
        )
        pivot = augmented[pivot_index][pivot_index]
        assert abs(pivot) > 1e-12
        augmented[pivot_index] = [value / pivot for value in augmented[pivot_index]]
        for row in range(n):
            if row == pivot_index:
                continue
            factor = augmented[row][pivot_index]
            augmented[row] = [
                augmented[row][column] - factor * augmented[pivot_index][column]
                for column in range(2 * n)
            ]
    return {
        names[i]: {
            names[j]: augmented[i][n + j]
            for j in range(n)
        }
        for i in range(n)
    }


def metric_derivatives() -> dict:
    return {
        "goal": {
            "goal": {"goal": 0.020, "reroute": 0.010, "verification": 0.000},
            "reroute": {"goal": 0.010, "reroute": -0.010, "verification": 0.005},
            "verification": {"goal": 0.000, "reroute": 0.005, "verification": 0.030},
        },
        "reroute": {
            "goal": {"goal": -0.010, "reroute": 0.000, "verification": 0.004},
            "reroute": {"goal": 0.000, "reroute": 0.015, "verification": -0.006},
            "verification": {"goal": 0.004, "reroute": -0.006, "verification": 0.010},
        },
        "verification": {
            "goal": {"goal": 0.005, "reroute": -0.003, "verification": 0.002},
            "reroute": {"goal": -0.003, "reroute": 0.004, "verification": 0.001},
            "verification": {"goal": 0.002, "reroute": 0.001, "verification": -0.008},
        },
    }


def plan_state_point() -> dict:
    return {"goal": 0.25, "reroute": -0.10, "verification": 0.40}


def candidate_tangents() -> list[dict]:
    return [
        {
            "candidate_id": "continue",
            "tangent_vector": {"goal": 0.20, "reroute": -0.10, "verification": 0.30},
            "transport_displacement": {
                "goal": 0.0005,
                "reroute": -0.0004,
                "verification": 0.0003,
            },
            "source_candidate_digest": "candidate-continue-v105",
        },
        {
            "candidate_id": "hold",
            "tangent_vector": {"goal": 0.0, "reroute": 0.0, "verification": 0.0},
            "transport_displacement": {
                "goal": 0.0002,
                "reroute": 0.0001,
                "verification": -0.0002,
            },
            "source_candidate_digest": "candidate-hold-v105",
        },
        {
            "candidate_id": "reroute",
            "tangent_vector": {"goal": -0.15, "reroute": 0.30, "verification": 0.10},
            "transport_displacement": {
                "goal": -0.0003,
                "reroute": 0.0005,
                "verification": 0.0002,
            },
            "source_candidate_digest": "candidate-reroute-v105",
        },
    ]


def build(**overrides):
    metric = overrides.pop("metric_matrix", metric_matrix())
    inverse = overrides.pop("inverse_metric_matrix", invert_matrix(metric_matrix()))
    derivatives = overrides.pop("metric_first_derivatives", metric_derivatives())
    point = overrides.pop("plan_state_point", plan_state_point())
    candidates = overrides.pop("candidate_tangents", candidate_tangents())
    qi_digest = overrides.pop("qi_state_digest", "qi-state-v106")
    history_digest = overrides.pop("history_state_digest", "history-window-v106")
    world_digest = overrides.pop("world_state_digest", "world-state-v14-rev7")
    names = sorted(metric) if isinstance(metric, dict) else []

    def safe(function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyError, TypeError, ValueError, ZeroDivisionError):
            return canonical_digest({"invalid": repr((args, kwargs))})

    args = {
        "source_native_coupled_metric_certificate_digest": "planos-v105-native-coupled-metric",
        "plan_coordinate_schema_digest": safe(compute_plan_coordinate_schema_digest, metric),
        "qi_state_digest": qi_digest,
        "history_state_digest": history_digest,
        "world_state_digest": world_digest,
        "state_context_digest": safe(
            compute_state_context_digest,
            plan_state_point=point,
            qi_state_digest=qi_digest,
            history_state_digest=history_digest,
            world_state_digest=world_digest,
        ),
        "plan_state_point": point,
        "metric_jet_digest": safe(
            compute_metric_jet_digest,
            metric_matrix=metric,
            inverse_metric_matrix=inverse,
            metric_first_derivatives=derivatives,
        ),
        "metric_matrix": metric,
        "inverse_metric_matrix": inverse,
        "metric_first_derivatives": derivatives,
        "candidate_tangent_bundle_digest": safe(
            compute_candidate_tangent_bundle_digest, candidates, names
        ),
        "candidate_tangents": candidates,
        "maximum_absolute_metric_derivative": 0.05,
        "maximum_absolute_christoffel": 0.10,
        "maximum_transport_displacement": 0.001,
        "maximum_first_order_norm_defect": 1e-7,
    }
    args.update(overrides)
    return build_state_dependent_metric_jet_levi_civita_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    certificate = result.certificate
    for name in (
        "state_dependent_metric_jet_present",
        "metric_symmetric",
        "metric_positive_definite",
        "inverse_metric_exact",
        "metric_derivative_symmetric",
        "levi_civita_connection_recomputed",
        "torsion_free",
        "metric_compatible",
        "connection_bounded",
        "parallel_transport_bounded",
        "first_order_metric_norm_preserved",
        "geodesic_acceleration_retained",
        "source_metric_not_mutated",
        "persistent_world_state_unchanged",
        "candidate_tangent_field_retained",
        "history_read_only",
        "qi_grants_no_authority",
        "world_projection_grants_no_authority",
        "connection_grants_no_authority",
        "future_only",
    ):
        assert certificate[name] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False
    assert certificate["computed_maximum_absolute_metric_derivative"] > 0.0
    assert certificate["computed_maximum_absolute_christoffel"] > 0.0
    assert certificate["maximum_metric_compatibility_residual"] < 1e-7
    assert certificate["maximum_observed_first_order_norm_defect"] < 1e-7

    for upper, by_j in certificate["christoffel_symbols"].items():
        for j, by_k in by_j.items():
            for k, value in by_k.items():
                assert abs(value - certificate["christoffel_symbols"][upper][k][j]) < 1e-9

    for record in certificate["candidate_transport_records"]:
        assert record["first_order_norm_defect"] <= 1e-7
        assert set(record["transported_tangent_vector"]) == set(coordinates())
        assert set(record["geodesic_acceleration"]) == set(coordinates())

    nonsymmetric_metric = metric_matrix()
    nonsymmetric_metric["goal"]["reroute"] += 0.1

    nonpositive_metric = metric_matrix()
    nonpositive_metric["goal"]["goal"] = -1.0

    bad_inverse = invert_matrix(metric_matrix())
    bad_inverse["goal"]["goal"] += 0.05

    asymmetric_derivative = metric_derivatives()
    asymmetric_derivative["goal"]["goal"]["reroute"] += 0.02

    zero_derivative = metric_derivatives()
    for derivative in zero_derivative.values():
        for row in derivative.values():
            for column in row:
                row[column] = 0.0

    bad_candidate_schema = candidate_tangents()
    bad_candidate_schema[0]["tangent_vector"].pop("goal")

    duplicate_candidate = candidate_tangents()
    duplicate_candidate[1]["candidate_id"] = duplicate_candidate[0]["candidate_id"]

    duplicate_source = candidate_tangents()
    duplicate_source[1]["source_candidate_digest"] = duplicate_source[0]["source_candidate_digest"]

    excessive_displacement = candidate_tangents()
    excessive_displacement[0]["transport_displacement"]["goal"] = 0.01

    blocked = [
        build(source_native_coupled_metric_certificate_digest=""),
        build(plan_coordinate_schema_digest="wrong"),
        build(qi_state_digest=""),
        build(history_state_digest=""),
        build(world_state_digest=""),
        build(state_context_digest="wrong"),
        build(metric_jet_digest="wrong"),
        build(candidate_tangent_bundle_digest="wrong"),
        build(maximum_absolute_metric_derivative=0.0),
        build(maximum_absolute_christoffel=0.0),
        build(maximum_transport_displacement=0.0),
        build(maximum_first_order_norm_defect=0.0),
        build(metric_matrix={}),
        build(metric_matrix=nonsymmetric_metric),
        build(metric_matrix=nonpositive_metric),
        build(inverse_metric_matrix=bad_inverse),
        build(metric_first_derivatives=asymmetric_derivative),
        build(metric_first_derivatives=zero_derivative),
        build(maximum_absolute_metric_derivative=0.01),
        build(maximum_absolute_christoffel=0.001),
        build(candidate_tangents=[]),
        build(candidate_tangents=bad_candidate_schema),
        build(candidate_tangents=duplicate_candidate),
        build(candidate_tangents=duplicate_source),
        build(candidate_tangents=excessive_displacement),
        build(maximum_first_order_norm_defect=1e-13),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    stale_candidates = candidate_tangents()
    stale_digest = compute_candidate_tangent_bundle_digest(
        stale_candidates, coordinates()
    )
    stale_candidates[0]["tangent_vector"]["goal"] += 0.1
    tampered = build(
        candidate_tangents=stale_candidates,
        candidate_tangent_bundle_digest=stale_digest,
    )
    assert tampered.status != STATUS_READY and tampered.certificate is None

    nonfinite = candidate_tangents()
    nonfinite[0]["transport_displacement"]["goal"] = float("nan")
    item = build(candidate_tangents=nonfinite)
    assert item.status != STATUS_READY and item.certificate is None

    print(
        "PASS: PlanOS State-Dependent Metric Jet and Levi-Civita Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
