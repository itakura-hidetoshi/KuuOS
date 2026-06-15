#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_indra_qi_world_real_hilbert_l2_analytic_spine_base_v0_26 import *

def validate_report(
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
    blockers: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if report.get("version") != REPORT_VERSION:
        blockers.append("world_l2_report_version_invalid")
    if report.get("analysis_run_id") != plan.get("analysis_run_id"):
        blockers.append("world_l2_report_run_id_mismatch")
    if report.get("source_world_state_digest") != source.get("world_digest"):
        blockers.append("world_l2_report_source_digest_mismatch")
    if report.get("world_l2_embedding_report_digest") != report_digest(report):
        blockers.append("world_l2_report_digest_invalid")

    carrier = mapping(report.get("carrier"))
    if carrier.get("scalar_field") != "real":
        blockers.append("world_l2_scalar_field_not_real")
    if carrier.get("space_kind") != "ell2_countable_real":
        blockers.append("world_l2_space_kind_invalid")
    if carrier.get("index_set_kind") != "countable_feature_basis":
        blockers.append("world_l2_index_set_kind_invalid")
    if carrier.get("finite_support_runtime_witness") is not True:
        blockers.append("world_l2_finite_support_witness_missing")
    if carrier.get("complete_real_hilbert_space_declared") is not True:
        blockers.append("world_l2_complete_space_declaration_missing")

    representation = mapping(report.get("representation_map"))
    expected_representation = {
        "map_kind": "nonlinear_observation_embedding",
        "world_not_identified_with_hilbert_vector": True,
        "linear_required": False,
        "injective_required": False,
        "surjective_required": False,
        "multi_world_noncollapse_preserved": True,
        "two_truths_gap_preserved": True,
    }
    for field, expected in expected_representation.items():
        if representation.get(field) is not expected and representation.get(field) != expected:
            blockers.append(f"world_l2_representation_{field}_mismatch")
    if not str(representation.get("representation_digest", "")):
        blockers.append("world_l2_representation_digest_missing")

    operator = mapping(report.get("operator_template"))
    if operator.get("generator_kind") != "positive_diagonal_dense_core_template":
        blockers.append("world_l2_generator_kind_invalid")
    if operator.get("dense_core_declared") is not True:
        blockers.append("world_l2_dense_core_missing")
    if operator.get("symmetric_core_declared") is not True:
        blockers.append("world_l2_symmetric_core_missing")
    if operator.get("self_adjointness_status") != "not_asserted_by_runtime":
        blockers.append("world_l2_self_adjointness_runtime_claim_invalid")
    if operator.get("unbounded_operator_execution_enabled") is not False:
        blockers.append("world_l2_unbounded_operator_execution_enabled")

    coordinates = [dict(mapping(value)) for value in items(report.get("coordinates"))]
    projections = [dict(mapping(value)) for value in items(report.get("diagnostic_projections"))]
    if not coordinates:
        blockers.append("world_l2_coordinates_missing")
        return coordinates, projections

    basis_ids: set[str] = set()
    source_pairs: set[tuple[str, str]] = set()
    entities = mapping(source.get("entities"))
    for index, coordinate in enumerate(coordinates):
        basis_id = str(coordinate.get("basis_id", ""))
        source_kind = str(coordinate.get("source_kind", ""))
        source_id = str(coordinate.get("source_id", ""))
        pair = (source_kind, source_id)
        if not basis_id or basis_id in basis_ids:
            blockers.append(f"world_l2_coordinate_{index}_basis_id_invalid")
        if source_kind not in SOURCE_KIND_FIELDS:
            blockers.append(f"world_l2_coordinate_{index}_source_kind_invalid")
        elif source_id not in set(entities.get(source_kind, set())):
            blockers.append(f"world_l2_coordinate_{index}_source_id_unknown")
        if pair in source_pairs:
            blockers.append(f"world_l2_coordinate_{index}_source_pair_duplicate")
        if not finite_number(coordinate.get("coordinate")):
            blockers.append(f"world_l2_coordinate_{index}_value_nonfinite")
        if not finite_number(coordinate.get("weight")) or number(coordinate.get("weight")) <= 0:
            blockers.append(f"world_l2_coordinate_{index}_weight_not_positive")
        if not str(coordinate.get("semantic_role", "")):
            blockers.append(f"world_l2_coordinate_{index}_semantic_role_missing")
        basis_ids.add(basis_id)
        source_pairs.add(pair)

    projection_roles: set[str] = set()
    projection_ids: set[str] = set()
    for index, projection in enumerate(projections):
        projection_id = str(projection.get("projection_id", ""))
        role = str(projection.get("role", ""))
        selected = [str(value) for value in items(projection.get("basis_ids"))]
        if not projection_id or projection_id in projection_ids:
            blockers.append(f"world_l2_projection_{index}_id_invalid")
        if role not in REQUIRED_PROJECTION_ROLES:
            blockers.append(f"world_l2_projection_{index}_role_invalid")
        if not selected or any(value not in basis_ids for value in selected):
            blockers.append(f"world_l2_projection_{index}_basis_invalid")
        if projection.get("orthogonal_coordinate_projection") is not True:
            blockers.append(f"world_l2_projection_{index}_not_orthogonal_coordinate_projection")
        if not finite_number(projection.get("operator_norm_bound")) or not 0 <= number(
            projection.get("operator_norm_bound"), 2.0
        ) <= 1:
            blockers.append(f"world_l2_projection_{index}_not_contractive")
        projection_ids.add(projection_id)
        projection_roles.add(role)
    if projection_roles != REQUIRED_PROJECTION_ROLES:
        blockers.append("world_l2_required_projection_roles_missing")
    return coordinates, projections


def analyze_embedding(
    coordinates: Sequence[Mapping[str, Any]],
    projections: Sequence[Mapping[str, Any]],
    report: Mapping[str, Any],
    plan: Mapping[str, Any],
    source: Mapping[str, Any],
) -> dict[str, Any]:
    policy = mapping(plan.get("analytic_policy"))
    coordinate_values = {str(value.get("basis_id", "")): number(value.get("coordinate")) for value in coordinates}
    norm_squared = sum(value * value for value in coordinate_values.values())
    weighted_energy = sum(
        number(value.get("weight")) * number(value.get("coordinate")) ** 2 for value in coordinates
    )
    weights = [number(value.get("weight")) for value in coordinates]
    coercivity = min(weights, default=0.0)
    max_abs = max((abs(value) for value in coordinate_values.values()), default=0.0)
    tolerance = number(policy.get("numeric_tolerance"), 1e-9)

    declared = mapping(report.get("declared_observables"))
    declared_norm = number(declared.get("norm_squared"), math.nan)
    declared_energy = number(declared.get("weighted_energy"), math.nan)
    declared_coercivity = number(declared.get("coercivity_lower_bound"), math.nan)
    declared_match = (
        math.isfinite(declared_norm)
        and math.isfinite(declared_energy)
        and math.isfinite(declared_coercivity)
        and abs(declared_norm - norm_squared) <= tolerance
        and abs(declared_energy - weighted_energy) <= tolerance
        and abs(declared_coercivity - coercivity) <= tolerance
    )

    entities = mapping(source.get("entities"))
    expected_pairs = {
        (source_kind, source_id)
        for source_kind, identifiers in entities.items()
        for source_id in set(identifiers)
    }
    actual_pairs = {
        (str(value.get("source_kind", "")), str(value.get("source_id", "")))
        for value in coordinates
    }
    coverage_ratio = len(actual_pairs & expected_pairs) / max(len(expected_pairs), 1)
    missing_pairs = sorted(f"{kind}:{identifier}" for kind, identifier in expected_pairs - actual_pairs)

    projection_energy: dict[str, float] = {}
    for projection in projections:
        role = str(projection.get("role", ""))
        projection_energy[role] = round(
            sum(coordinate_values.get(str(basis_id), 0.0) ** 2 for basis_id in items(projection.get("basis_ids"))),
            12,
        )

    rayleigh_bound_verified = weighted_energy + tolerance >= coercivity * norm_squared
    finite_energy = math.isfinite(norm_squared) and math.isfinite(weighted_energy)
    coverage_gates = {
        "full_source_coverage": coverage_ratio == 1.0,
        "all_required_source_kinds_present": all(
            any(str(value.get("source_kind", "")) == source_kind for value in coordinates)
            for source_kind in SOURCE_KIND_FIELDS
        ),
        "required_projection_roles_present": {
            str(value.get("role", "")) for value in projections
        }
        == REQUIRED_PROJECTION_ROLES,
    }
    analytic_gates = {
        "coordinate_count_bounded": int(policy.get("minimum_coordinate_count", 0))
        <= len(coordinates)
        <= int(policy.get("maximum_coordinate_count", 0)),
        "absolute_coordinates_bounded": max_abs <= number(policy.get("maximum_absolute_coordinate")),
        "finite_energy": finite_energy,
        "norm_squared_bounded": norm_squared <= number(policy.get("maximum_norm_squared")),
        "weighted_energy_bounded": weighted_energy <= number(policy.get("maximum_weighted_energy")),
        "coercivity_positive_and_sufficient": coercivity
        >= number(policy.get("minimum_coercivity_lower_bound")),
        "rayleigh_lower_bound_verified": rayleigh_bound_verified,
        "declared_observables_match": declared_match,
        "projection_energies_finite": all(math.isfinite(value) for value in projection_energy.values()),
    }
    return {
        "coordinate_count": len(coordinates),
        "support_size": len(coordinates),
        "norm_squared": round(norm_squared, 12),
        "norm": round(math.sqrt(norm_squared), 12),
        "weighted_energy": round(weighted_energy, 12),
        "coercivity_lower_bound": round(coercivity, 12),
        "rayleigh_lower_bound_rhs": round(coercivity * norm_squared, 12),
        "rayleigh_lower_bound_verified": rayleigh_bound_verified,
        "maximum_absolute_coordinate": round(max_abs, 12),
        "source_coverage_ratio": round(coverage_ratio, 12),
        "missing_source_coordinates": missing_pairs,
        "projection_energy": projection_energy,
        "coverage_gates": coverage_gates,
        "analytic_gates": analytic_gates,
        "all_gates": {**coverage_gates, **analytic_gates},
    }


def evaluate_analysis(analysis: Mapping[str, Any], blockers: Sequence[str]) -> tuple[str, str]:
    if blockers:
        return "quarantine_recommended", "validation_or_integrity_boundary_failed"
    coverage = mapping(analysis.get("coverage_gates"))
    analytic = mapping(analysis.get("analytic_gates"))
    if not all(value is True for value in coverage.values()):
        return "restore_multi_world_coverage_recommended", "world_feature_or_projection_coverage_incomplete"
    if all(value is True for value in analytic.values()):
        return "world_l2_analytic_spine_ready", "finite_energy_real_l2_spine_with_rayleigh_lower_bound_ready"
    return "redesign_world_l2_embedding_recommended", "analytic_norm_energy_coercivity_or_observable_gate_failed"
