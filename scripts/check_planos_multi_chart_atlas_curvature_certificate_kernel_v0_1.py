#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import math

from runtime.kuuos_planos_multi_chart_atlas_curvature_certificate_kernel_v0_1 import (
    STATUS_READY,
    _connection_transform,
    _inverse_metric_transform,
    _metric_transform,
    _ricci_transform,
    _riemann_transform,
    _transform_vector,
    build_multi_chart_atlas_curvature_certificate,
    canonical_digest,
    compute_atlas_digest,
    compute_chart_bundle_digest,
    compute_transition_bundle_digest,
)


def zero_connection(coordinates: list[str]) -> dict:
    return {
        i: {j: {k: 0.0 for k in coordinates} for j in coordinates}
        for i in coordinates
    }


def zero_inverse_hessian(source: list[str], target: list[str]) -> dict:
    return {
        i: {a: {b: 0.0 for b in target} for a in target}
        for i in source
    }


def identity_metric(coordinates: list[str]) -> dict:
    return {
        i: {j: 1.0 if i == j else 0.0 for j in coordinates}
        for i in coordinates
    }


def base_riemann(coordinates: list[str], sectional_value: float = 0.1) -> dict:
    metric = identity_metric(coordinates)
    return {
        upper: {
            j: {
                k: {
                    l: sectional_value
                    * (
                        metric[upper][l] * metric[j][k]
                        - metric[upper][k] * metric[j][l]
                    )
                    for l in coordinates
                }
                for k in coordinates
            }
            for j in coordinates
        }
        for upper in coordinates
    }


def ricci_from_riemann(riemann: dict, coordinates: list[str]) -> dict:
    return {
        j: {
            l: sum(riemann[upper][j][upper][l] for upper in coordinates)
            for l in coordinates
        }
        for j in coordinates
    }


def holonomy_increment(
    riemann: dict,
    vector: dict,
    plane_u: dict,
    plane_v: dict,
    coordinates: list[str],
) -> dict:
    return {
        upper: sum(
            riemann[upper][j][k][l]
            * vector[j]
            * plane_u[k]
            * plane_v[l]
            for j in coordinates
            for k in coordinates
            for l in coordinates
        )
        for upper in coordinates
    }


def base_candidate_records(coordinates: list[str], riemann: dict) -> list[dict]:
    raw = [
        {
            "candidate_id": "continue",
            "plane_u": {coordinates[0]: 0.10, coordinates[1]: 0.0},
            "plane_v": {coordinates[0]: 0.0, coordinates[1]: 0.10},
            "holonomy_vector": {coordinates[0]: 0.20, coordinates[1]: -0.10},
            "source_candidate_digest": "candidate-continue-digest",
        },
        {
            "candidate_id": "reroute",
            "plane_u": {coordinates[0]: 0.08, coordinates[1]: 0.02},
            "plane_v": {coordinates[0]: -0.01, coordinates[1]: 0.09},
            "holonomy_vector": {coordinates[0]: -0.15, coordinates[1]: 0.12},
            "source_candidate_digest": "candidate-reroute-digest",
        },
    ]
    records = []
    for record in raw:
        records.append(
            {
                **record,
                "sectional_curvature": 0.1,
                "holonomy_increment": holonomy_increment(
                    riemann,
                    record["holonomy_vector"],
                    record["plane_u"],
                    record["plane_v"],
                    coordinates,
                ),
            }
        )
    return records


def transform_candidate_records(
    records: list[dict], jacobian: dict, source: list[str], target: list[str]
) -> list[dict]:
    return [
        {
            "candidate_id": record["candidate_id"],
            "plane_u": _transform_vector(jacobian, record["plane_u"], source, target),
            "plane_v": _transform_vector(jacobian, record["plane_v"], source, target),
            "holonomy_vector": _transform_vector(
                jacobian, record["holonomy_vector"], source, target
            ),
            "sectional_curvature": record["sectional_curvature"],
            "holonomy_increment": _transform_vector(
                jacobian, record["holonomy_increment"], source, target
            ),
            "source_candidate_digest": record["source_candidate_digest"],
        }
        for record in records
    ]


def multiply_matrix(
    left: dict,
    right: dict,
    rows: list[str],
    middle: list[str],
    columns: list[str],
) -> dict:
    return {
        row: {
            column: sum(left[row][k] * right[k][column] for k in middle)
            for column in columns
        }
        for row in rows
    }


def fixture() -> tuple[list[dict], list[dict]]:
    a = ["x", "y"]
    b = ["u", "v"]
    c = ["p", "q"]

    j_ab = {"u": {"x": 2.0, "y": 0.0}, "v": {"x": 0.0, "y": 0.5}}
    k_ab = {"x": {"u": 0.5, "v": 0.0}, "y": {"u": 0.0, "v": 2.0}}
    j_bc = {"p": {"u": 1.0, "v": 1.0}, "q": {"u": 0.0, "v": 1.0}}
    k_bc = {"u": {"p": 1.0, "q": -1.0}, "v": {"p": 0.0, "q": 1.0}}
    j_ac = multiply_matrix(j_bc, j_ab, c, b, a)
    k_ac = multiply_matrix(k_ab, k_bc, a, b, c)

    metric_a = identity_metric(a)
    inverse_a = identity_metric(a)
    connection_a = zero_connection(a)
    riemann_a = base_riemann(a)
    ricci_a = ricci_from_riemann(riemann_a, a)
    scalar_a = sum(inverse_a[i][j] * ricci_a[i][j] for i in a for j in a)
    records_a = base_candidate_records(a, riemann_a)

    def transformed_chart(
        *,
        chart_id: str,
        coordinates: list[str],
        jacobian: dict,
        inverse_jacobian: dict,
        boundary_margin: float,
        regularity_radius: float,
    ) -> dict:
        metric = _metric_transform(inverse_jacobian, metric_a, a, coordinates)
        inverse_metric = _inverse_metric_transform(
            jacobian, inverse_a, a, coordinates
        )
        connection = _connection_transform(
            jacobian,
            inverse_jacobian,
            zero_inverse_hessian(a, coordinates),
            connection_a,
            a,
            coordinates,
        )
        riemann = _riemann_transform(
            jacobian, inverse_jacobian, riemann_a, a, coordinates
        )
        ricci = _ricci_transform(inverse_jacobian, ricci_a, a, coordinates)
        return {
            "chart_id": chart_id,
            "coordinates": coordinates,
            "source_curvature_certificate_digest": f"planos-v1-07-curvature-{chart_id}",
            "metric_matrix": metric,
            "inverse_metric_matrix": inverse_metric,
            "christoffel_symbols": connection,
            "riemann_tensor": riemann,
            "ricci_tensor": ricci,
            "scalar_curvature": scalar_a,
            "candidate_records": transform_candidate_records(
                records_a, jacobian, a, coordinates
            ),
            "boundary_margin": boundary_margin,
            "regularity_radius": regularity_radius,
        }

    charts = [
        {
            "chart_id": "chart-a",
            "coordinates": a,
            "source_curvature_certificate_digest": "planos-v1-07-curvature-chart-a",
            "metric_matrix": metric_a,
            "inverse_metric_matrix": inverse_a,
            "christoffel_symbols": connection_a,
            "riemann_tensor": riemann_a,
            "ricci_tensor": ricci_a,
            "scalar_curvature": scalar_a,
            "candidate_records": records_a,
            "boundary_margin": 0.40,
            "regularity_radius": 0.50,
        },
        transformed_chart(
            chart_id="chart-b",
            coordinates=b,
            jacobian=j_ab,
            inverse_jacobian=k_ab,
            boundary_margin=0.35,
            regularity_radius=0.45,
        ),
        transformed_chart(
            chart_id="chart-c",
            coordinates=c,
            jacobian=j_ac,
            inverse_jacobian=k_ac,
            boundary_margin=0.30,
            regularity_radius=0.40,
        ),
    ]

    transitions = [
        {
            "source_chart_id": "chart-a",
            "target_chart_id": "chart-b",
            "jacobian": j_ab,
            "inverse_jacobian": k_ab,
            "inverse_hessian": zero_inverse_hessian(a, b),
            "overlap_margin": 0.30,
            "source_transition_digest": "transition-a-b-digest",
        },
        {
            "source_chart_id": "chart-b",
            "target_chart_id": "chart-c",
            "jacobian": j_bc,
            "inverse_jacobian": k_bc,
            "inverse_hessian": zero_inverse_hessian(b, c),
            "overlap_margin": 0.25,
            "source_transition_digest": "transition-b-c-digest",
        },
        {
            "source_chart_id": "chart-a",
            "target_chart_id": "chart-c",
            "jacobian": j_ac,
            "inverse_jacobian": k_ac,
            "inverse_hessian": zero_inverse_hessian(a, c),
            "overlap_margin": 0.20,
            "source_transition_digest": "transition-a-c-digest",
        },
    ]
    return charts, transitions


def build(**overrides):
    charts, transitions = fixture()
    charts = overrides.pop("charts", charts)
    transitions = overrides.pop("transitions", transitions)

    def safe(function, *args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyError, TypeError, ValueError, IndexError):
            return canonical_digest({"args": args, "kwargs": kwargs})

    chart_digest = overrides.pop(
        "chart_bundle_digest", safe(compute_chart_bundle_digest, charts)
    )
    transition_digest = overrides.pop(
        "transition_bundle_digest",
        safe(compute_transition_bundle_digest, charts, transitions),
    )
    source_digest = overrides.pop(
        "source_curvature_bundle_digest", "planos-v1-07-curvature-bundle"
    )
    args = {
        "source_curvature_bundle_digest": source_digest,
        "chart_bundle_digest": chart_digest,
        "transition_bundle_digest": transition_digest,
        "atlas_digest": safe(
            compute_atlas_digest,
            source_curvature_bundle_digest=source_digest,
            chart_bundle_digest=chart_digest,
            transition_bundle_digest=transition_digest,
        ),
        "charts": charts,
        "transitions": transitions,
        "minimum_absolute_jacobian_determinant": 0.20,
        "maximum_absolute_jacobian_component": 2.10,
        "maximum_absolute_inverse_jacobian_component": 2.10,
        "maximum_absolute_transition_hessian_component": 0.01,
        "minimum_chart_boundary_margin": 0.25,
        "minimum_overlap_margin": 0.15,
        "maximum_metric_transform_residual": 1e-9,
        "maximum_connection_transform_residual": 1e-9,
        "maximum_curvature_transform_residual": 1e-9,
        "maximum_scalar_invariance_residual": 1e-9,
        "maximum_sectional_invariance_residual": 1e-9,
        "maximum_holonomy_equivariance_residual": 1e-9,
        "maximum_cocycle_residual": 1e-9,
    }
    args.update(overrides)
    return build_multi_chart_atlas_curvature_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None, result.blockers
    certificate = result.certificate
    for field in (
        "atlas_present",
        "multiple_charts_present",
        "chart_dimensions_consistent",
        "transition_jacobians_invertible",
        "transition_inverse_exact",
        "transition_hessians_symmetric",
        "metric_transform_compatible",
        "inverse_metric_transform_compatible",
        "connection_transform_compatible",
        "riemann_transform_compatible",
        "ricci_transform_compatible",
        "scalar_curvature_invariant",
        "sectional_curvature_invariant",
        "holonomy_equivariant",
        "atlas_cocycle_satisfied",
        "chart_boundary_regular",
        "singular_transition_guard_present",
        "source_curvature_certificates_not_mutated",
        "persistent_world_state_unchanged",
        "candidate_plane_identity_retained",
        "history_read_only",
        "qi_grants_no_authority",
        "world_projection_grants_no_authority",
        "curvature_grants_no_authority",
        "atlas_grants_no_authority",
        "future_only",
    ):
        assert certificate[field] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False
    assert len(certificate["charts"]) == 3
    assert len(certificate["transitions"]) == 3
    assert certificate["cocycle_records"]
    assert abs(certificate["charts"][0]["scalar_curvature"] + 0.2) < 1e-10
    assert certificate["computed_minimum_absolute_jacobian_determinant"] >= 0.25
    for residual_name in (
        "maximum_observed_metric_transform_residual",
        "maximum_observed_inverse_metric_transform_residual",
        "maximum_observed_connection_transform_residual",
        "maximum_observed_riemann_transform_residual",
        "maximum_observed_ricci_transform_residual",
        "maximum_observed_scalar_invariance_residual",
        "maximum_observed_sectional_invariance_residual",
        "maximum_observed_holonomy_equivariance_residual",
        "maximum_observed_cocycle_residual",
    ):
        assert certificate[residual_name] < 1e-10

    charts, transitions = fixture()
    duplicate_chart = deepcopy(charts)
    duplicate_chart[1]["chart_id"] = duplicate_chart[0]["chart_id"]

    singular_transition = deepcopy(transitions)
    singular_transition[0]["jacobian"]["v"]["y"] = 0.0

    wrong_inverse = deepcopy(transitions)
    wrong_inverse[0]["inverse_jacobian"]["x"]["u"] = 0.6

    nonsymmetric_hessian = deepcopy(transitions)
    nonsymmetric_hessian[0]["inverse_hessian"]["x"]["u"]["v"] = 0.01

    metric_mismatch = deepcopy(charts)
    metric_mismatch[1]["metric_matrix"]["u"]["u"] += 0.01

    connection_mismatch = deepcopy(charts)
    connection_mismatch[1]["christoffel_symbols"]["u"]["u"]["u"] = 0.01

    riemann_mismatch = deepcopy(charts)
    riemann_mismatch[1]["riemann_tensor"]["u"]["v"]["u"]["v"] += 0.01

    scalar_mismatch = deepcopy(charts)
    scalar_mismatch[1]["scalar_curvature"] += 0.01

    sectional_mismatch = deepcopy(charts)
    sectional_mismatch[1]["candidate_records"][0]["sectional_curvature"] += 0.01

    holonomy_mismatch = deepcopy(charts)
    holonomy_mismatch[1]["candidate_records"][0]["holonomy_increment"]["u"] += 0.01

    cocycle_mismatch = deepcopy(transitions)
    cocycle_mismatch[2]["jacobian"]["p"]["x"] += 0.01
    cocycle_mismatch[2]["inverse_jacobian"]["x"]["p"] = 1.0 / cocycle_mismatch[2]["jacobian"]["p"]["x"]

    boundary_mismatch = deepcopy(charts)
    boundary_mismatch[2]["boundary_margin"] = 0.1

    nonfinite_chart = deepcopy(charts)
    nonfinite_chart[0]["metric_matrix"]["x"]["x"] = float("nan")

    missing_direct_transition = deepcopy(transitions[:2])

    blocked = [
        build(source_curvature_bundle_digest=""),
        build(chart_bundle_digest="wrong"),
        build(transition_bundle_digest="wrong"),
        build(atlas_digest="wrong"),
        build(charts=charts[:2]),
        build(charts=duplicate_chart),
        build(transitions=[]),
        build(transitions=singular_transition),
        build(transitions=wrong_inverse),
        build(transitions=nonsymmetric_hessian),
        build(charts=metric_mismatch),
        build(charts=connection_mismatch),
        build(charts=riemann_mismatch),
        build(charts=scalar_mismatch),
        build(charts=sectional_mismatch),
        build(charts=holonomy_mismatch),
        build(transitions=cocycle_mismatch),
        build(charts=boundary_mismatch),
        build(charts=nonfinite_chart),
        build(transitions=missing_direct_transition),
        build(minimum_absolute_jacobian_determinant=0.0),
        build(maximum_absolute_jacobian_component=1.0),
        build(maximum_absolute_inverse_jacobian_component=1.0),
        build(maximum_absolute_transition_hessian_component=0.0),
        build(minimum_chart_boundary_margin=0.45),
        build(minimum_overlap_margin=0.25),
        build(maximum_metric_transform_residual=1e-12, charts=metric_mismatch),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    tampered_charts = deepcopy(charts)
    stale_chart_digest = compute_chart_bundle_digest(tampered_charts)
    tampered_charts[0]["boundary_margin"] += 0.01
    item = build(charts=tampered_charts, chart_bundle_digest=stale_chart_digest)
    assert item.status != STATUS_READY and item.certificate is None

    tampered_transitions = deepcopy(transitions)
    stale_transition_digest = compute_transition_bundle_digest(charts, tampered_transitions)
    tampered_transitions[0]["overlap_margin"] += 0.01
    item = build(
        transitions=tampered_transitions,
        transition_bundle_digest=stale_transition_digest,
    )
    assert item.status != STATUS_READY and item.certificate is None

    print("PASS: PlanOS Multi-Chart Atlas Curvature Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
