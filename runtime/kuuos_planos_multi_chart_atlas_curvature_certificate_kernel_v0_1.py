#!/usr/bin/env python3
from __future__ import annotations

from runtime.kuuos_planos_atlas_cocycle_checks_v0_1 import evaluate_atlas_cocycles
from runtime.kuuos_planos_atlas_common_v0_1 import (
    STATUS_BLOCKED,
    STATUS_READY,
    TOL,
    MultiChartAtlasCurvatureCertificateResult,
    canonical_digest,
    compute_atlas_digest,
    compute_chart_bundle_digest,
    compute_transition_bundle_digest,
    finite,
)
from runtime.kuuos_planos_atlas_geometry_v0_1 import (
    _connection_transform,
    _inverse_metric_transform,
    _metric_transform,
    _ricci_transform,
    _riemann_transform,
    _transform_vector,
)
from runtime.kuuos_planos_atlas_transition_checks_v0_1 import (
    evaluate_atlas_transitions,
)
from runtime.kuuos_planos_atlas_validation_v0_1 import (
    _validate_charts,
    _validate_transitions,
)


def build_multi_chart_atlas_curvature_certificate(
    *,
    source_curvature_bundle_digest: str,
    chart_bundle_digest: str,
    transition_bundle_digest: str,
    atlas_digest: str,
    charts: list[dict],
    transitions: list[dict],
    minimum_absolute_jacobian_determinant: float,
    maximum_absolute_jacobian_component: float,
    maximum_absolute_inverse_jacobian_component: float,
    maximum_absolute_transition_hessian_component: float,
    minimum_chart_boundary_margin: float,
    minimum_overlap_margin: float,
    maximum_metric_transform_residual: float,
    maximum_connection_transform_residual: float,
    maximum_curvature_transform_residual: float,
    maximum_scalar_invariance_residual: float,
    maximum_sectional_invariance_residual: float,
    maximum_holonomy_equivariance_residual: float,
    maximum_cocycle_residual: float,
) -> MultiChartAtlasCurvatureCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_curvature_bundle_digest": source_curvature_bundle_digest,
        "chart_bundle_digest": chart_bundle_digest,
        "transition_bundle_digest": transition_bundle_digest,
        "atlas_digest": atlas_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")
    numeric_bounds = {
        "minimum_absolute_jacobian_determinant": minimum_absolute_jacobian_determinant,
        "maximum_absolute_jacobian_component": maximum_absolute_jacobian_component,
        "maximum_absolute_inverse_jacobian_component": maximum_absolute_inverse_jacobian_component,
        "maximum_absolute_transition_hessian_component": maximum_absolute_transition_hessian_component,
        "minimum_chart_boundary_margin": minimum_chart_boundary_margin,
        "minimum_overlap_margin": minimum_overlap_margin,
        "maximum_metric_transform_residual": maximum_metric_transform_residual,
        "maximum_connection_transform_residual": maximum_connection_transform_residual,
        "maximum_curvature_transform_residual": maximum_curvature_transform_residual,
        "maximum_scalar_invariance_residual": maximum_scalar_invariance_residual,
        "maximum_sectional_invariance_residual": maximum_sectional_invariance_residual,
        "maximum_holonomy_equivariance_residual": maximum_holonomy_equivariance_residual,
        "maximum_cocycle_residual": maximum_cocycle_residual,
    }
    for name, value in numeric_bounds.items():
        if not finite(value) or float(value) <= 0.0:
            blockers.append(f"{name}_invalid")

    chart_errors, normalized_charts = _validate_charts(charts)
    blockers.extend(chart_errors)
    chart_by_id = {chart["chart_id"]: chart for chart in normalized_charts}
    transition_errors, normalized_transitions = _validate_transitions(
        transitions, chart_by_id
    )
    blockers.extend(transition_errors)
    if blockers:
        return MultiChartAtlasCurvatureCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    if chart_bundle_digest != compute_chart_bundle_digest(normalized_charts):
        blockers.append("chart_bundle_digest_mismatch")
    if transition_bundle_digest != compute_transition_bundle_digest(
        normalized_charts, normalized_transitions
    ):
        blockers.append("transition_bundle_digest_mismatch")
    expected_atlas_digest = compute_atlas_digest(
        source_curvature_bundle_digest=source_curvature_bundle_digest,
        chart_bundle_digest=chart_bundle_digest,
        transition_bundle_digest=transition_bundle_digest,
    )
    if atlas_digest != expected_atlas_digest:
        blockers.append("atlas_digest_mismatch")
    if any(
        chart["boundary_margin"] < minimum_chart_boundary_margin - TOL
        or chart["regularity_radius"] < minimum_chart_boundary_margin - TOL
        for chart in normalized_charts
    ):
        blockers.append("chart_boundary_margin_below_minimum")

    transition_blockers, transition_records, observed, transition_by_pair = (
        evaluate_atlas_transitions(
            normalized_charts=normalized_charts,
            normalized_transitions=normalized_transitions,
            minimum_absolute_jacobian_determinant=minimum_absolute_jacobian_determinant,
            maximum_absolute_jacobian_component=maximum_absolute_jacobian_component,
            maximum_absolute_inverse_jacobian_component=maximum_absolute_inverse_jacobian_component,
            maximum_absolute_transition_hessian_component=maximum_absolute_transition_hessian_component,
            minimum_overlap_margin=minimum_overlap_margin,
            maximum_metric_transform_residual=maximum_metric_transform_residual,
            maximum_connection_transform_residual=maximum_connection_transform_residual,
            maximum_curvature_transform_residual=maximum_curvature_transform_residual,
            maximum_scalar_invariance_residual=maximum_scalar_invariance_residual,
            maximum_sectional_invariance_residual=maximum_sectional_invariance_residual,
            maximum_holonomy_equivariance_residual=maximum_holonomy_equivariance_residual,
        )
    )
    blockers.extend(transition_blockers)
    cocycle_blockers, cocycle_records, maximum_observed_cocycle_residual = (
        evaluate_atlas_cocycles(
            normalized_charts=normalized_charts,
            transition_by_pair=transition_by_pair,
            maximum_cocycle_residual=maximum_cocycle_residual,
        )
    )
    blockers.extend(cocycle_blockers)
    if blockers:
        return MultiChartAtlasCurvatureCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": "PlanOS Multi-Chart Atlas Curvature Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.08",
        "source_curvature_bundle_digest": source_curvature_bundle_digest,
        "chart_bundle_digest": chart_bundle_digest,
        "transition_bundle_digest": transition_bundle_digest,
        "atlas_digest": atlas_digest,
        "charts": normalized_charts,
        "transitions": normalized_transitions,
        "transition_records": transition_records,
        "cocycle_records": cocycle_records,
        **{name: float(value) for name, value in numeric_bounds.items()},
        "computed_minimum_absolute_jacobian_determinant": observed[
            "minimum_absolute_jacobian_determinant"
        ],
        "computed_maximum_absolute_jacobian_component": observed[
            "maximum_absolute_jacobian_component"
        ],
        "computed_maximum_absolute_inverse_jacobian_component": observed[
            "maximum_absolute_inverse_jacobian_component"
        ],
        "computed_maximum_absolute_transition_hessian_component": observed[
            "maximum_absolute_transition_hessian_component"
        ],
        "computed_minimum_overlap_margin": observed["minimum_overlap_margin"],
        "maximum_observed_metric_transform_residual": observed[
            "maximum_metric_transform_residual"
        ],
        "maximum_observed_inverse_metric_transform_residual": observed[
            "maximum_inverse_metric_transform_residual"
        ],
        "maximum_observed_connection_transform_residual": observed[
            "maximum_connection_transform_residual"
        ],
        "maximum_observed_riemann_transform_residual": observed[
            "maximum_riemann_transform_residual"
        ],
        "maximum_observed_ricci_transform_residual": observed[
            "maximum_ricci_transform_residual"
        ],
        "maximum_observed_scalar_invariance_residual": observed[
            "maximum_scalar_invariance_residual"
        ],
        "maximum_observed_sectional_invariance_residual": observed[
            "maximum_sectional_invariance_residual"
        ],
        "maximum_observed_holonomy_equivariance_residual": observed[
            "maximum_holonomy_equivariance_residual"
        ],
        "maximum_observed_cocycle_residual": maximum_observed_cocycle_residual,
        "atlas_present": True,
        "multiple_charts_present": True,
        "chart_dimensions_consistent": True,
        "transition_jacobians_invertible": True,
        "transition_inverse_exact": True,
        "transition_hessians_symmetric": True,
        "metric_transform_compatible": True,
        "inverse_metric_transform_compatible": True,
        "connection_transform_compatible": True,
        "riemann_transform_compatible": True,
        "ricci_transform_compatible": True,
        "scalar_curvature_invariant": True,
        "sectional_curvature_invariant": True,
        "holonomy_equivariant": True,
        "atlas_cocycle_satisfied": True,
        "chart_boundary_regular": True,
        "singular_transition_guard_present": True,
        "source_curvature_certificates_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "candidate_plane_identity_retained": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "qi_grants_no_authority": True,
        "world_projection_grants_no_authority": True,
        "curvature_grants_no_authority": True,
        "atlas_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["atlas_curvature_certificate_digest"] = canonical_digest(certificate)
    return MultiChartAtlasCurvatureCertificateResult(STATUS_READY, [], certificate)
