#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_second_variation_morse_index_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_second_variation_morse_index_certificate,
    compute_second_variation_input_digest,
)


def identity_metric() -> dict:
    coordinates = ("x", "y", "z")
    return {
        i: {j: (1.0 if i == j else 0.0) for j in coordinates}
        for i in coordinates
    }


def curvature_tensor() -> dict:
    coordinates = ("x", "y", "z")
    tensor = {
        i: {
            j: {
                k: {l: 0.0 for l in coordinates}
                for k in coordinates
            }
            for j in coordinates
        }
        for i in coordinates
    }
    tensor["y"]["x"]["y"]["x"] = 0.2
    return tensor


def basis() -> list[dict]:
    zero = {"x": 0.0, "y": 0.0, "z": 0.0}
    return [
        {
            "basis_id": "negative-y",
            "source_candidate_id": "candidate-positive-curvature",
            "source_variation_digest": "variation-negative-y",
            "initial_endpoint_vector": dict(zero),
            "final_endpoint_vector": dict(zero),
        },
        {
            "basis_id": "null-x",
            "source_candidate_id": "candidate-tangent-reparametrization",
            "source_variation_digest": "variation-null-x",
            "initial_endpoint_vector": dict(zero),
            "final_endpoint_vector": dict(zero),
        },
        {
            "basis_id": "positive-z",
            "source_candidate_id": "candidate-flat-normal",
            "source_variation_digest": "variation-positive-z",
            "initial_endpoint_vector": dict(zero),
            "final_endpoint_vector": dict(zero),
        },
    ]


def samples() -> list[dict]:
    return [
        {
            "sample_id": "midpoint",
            "quadrature_weight": 1.0,
            "tangent": {"x": 1.0, "y": 0.0, "z": 0.0},
            "basis_data": {
                "negative-y": {
                    "variation_field": {"x": 0.0, "y": 1.0, "z": 0.0},
                    "covariant_derivative": {"x": 0.0, "y": 0.0, "z": 0.0},
                },
                "null-x": {
                    "variation_field": {"x": 1.0, "y": 0.0, "z": 0.0},
                    "covariant_derivative": {"x": 0.0, "y": 0.0, "z": 0.0},
                },
                "positive-z": {
                    "variation_field": {"x": 0.0, "y": 0.0, "z": 1.0},
                    "covariant_derivative": {"x": 0.0, "y": 0.0, "z": 1.0},
                },
            },
        }
    ]


def build(**overrides):
    metric = overrides.pop("metric_matrix", identity_metric())
    curvature = overrides.pop("riemann_tensor", curvature_tensor())
    variation_basis = overrides.pop("variation_basis", basis())
    quadrature_samples = overrides.pop("quadrature_samples", samples())
    digest = overrides.pop(
        "second_variation_input_digest",
        compute_second_variation_input_digest(
            metric=metric,
            curvature=curvature,
            variation_basis=variation_basis,
            quadrature_samples=quadrature_samples,
        ),
    )
    arguments = {
        "source_jacobi_certificate_digest": "planos-v1-09-jacobi-certificate",
        "second_variation_input_digest": digest,
        "metric_matrix": metric,
        "riemann_tensor": curvature,
        "variation_basis": variation_basis,
        "quadrature_samples": quadrature_samples,
        "endpoint_vanishing_tolerance": 1e-6,
        "minimum_tangent_norm": 0.5,
        "eigenvalue_zero_tolerance": 1e-8,
        "maximum_absolute_index_entry": 2.0,
        "maximum_absolute_eigenvalue": 2.0,
        "maximum_index_symmetry_residual": 1e-8,
        "maximum_spectral_invariant_residual": 1e-8,
    }
    arguments.update(overrides)
    return build_second_variation_morse_index_certificate(**arguments)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    certificate = result.certificate

    assert certificate["finite_basis_morse_index"] == 1
    assert certificate["finite_basis_nullity"] == 1
    assert certificate["finite_basis_positive_dimension"] == 1
    assert certificate["conjugate_multiplicity_candidate"] == 1
    assert certificate["index_form_matrix"]["negative-y"]["negative-y"] == -0.2
    assert certificate["index_form_matrix"]["null-x"]["null-x"] == 0.0
    assert certificate["index_form_matrix"]["positive-z"]["positive-z"] == 1.0
    assert certificate["negative_direction_witnesses_retained"] is True
    assert certificate["null_direction_witnesses_retained"] is True

    required_true = (
        "endpoint_fixed_variations_verified",
        "index_form_symmetric",
        "second_variation_retained",
        "finite_basis_morse_index_computed",
        "conjugate_multiplicity_candidate_local_only",
        "morse_index_finite_window_only",
        "candidate_identity_retained",
        "source_jacobi_certificate_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "curvature_grants_no_authority",
        "second_variation_grants_no_authority",
        "morse_index_grants_no_authority",
        "conjugate_multiplicity_grants_no_authority",
        "future_only",
    )
    for name in required_true:
        assert certificate[name] is True
    assert certificate["decision_selection_performed"] is False
    assert certificate["active_now"] is False
    assert certificate["execution_permission"] is False

    stale_digest = compute_second_variation_input_digest(
        metric=identity_metric(),
        curvature=curvature_tensor(),
        variation_basis=basis(),
        quadrature_samples=samples(),
    )
    tampered_samples = samples()
    tampered_samples[0]["basis_data"]["positive-z"]["covariant_derivative"]["z"] = 2.0

    duplicate_basis = basis()
    duplicate_basis[1]["basis_id"] = duplicate_basis[0]["basis_id"]

    duplicate_sample = samples() * 2

    bad_endpoint = basis()
    bad_endpoint[0]["final_endpoint_vector"]["y"] = 0.2

    bad_weight = samples()
    bad_weight[0]["quadrature_weight"] = 0.0

    small_tangent = samples()
    small_tangent[0]["tangent"] = {"x": 0.0, "y": 0.0, "z": 0.0}

    asymmetric_curvature = curvature_tensor()
    asymmetric_curvature["y"]["x"]["z"]["x"] = 0.3

    blocked = [
        build(source_jacobi_certificate_digest=""),
        build(second_variation_input_digest="wrong"),
        build(
            quadrature_samples=tampered_samples,
            second_variation_input_digest=stale_digest,
        ),
        build(variation_basis=duplicate_basis),
        build(quadrature_samples=duplicate_sample),
        build(variation_basis=bad_endpoint),
        build(quadrature_samples=bad_weight),
        build(quadrature_samples=small_tangent),
        build(riemann_tensor=asymmetric_curvature),
        build(maximum_absolute_index_entry=0.1),
        build(maximum_absolute_eigenvalue=0.1),
        build(eigenvalue_zero_tolerance=0.0),
    ]
    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print("PASS: PlanOS Second Variation and Morse Index Certificate Kernel v0.1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
