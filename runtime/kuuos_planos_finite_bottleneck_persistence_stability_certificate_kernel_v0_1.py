from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_finite_bottleneck_persistence_stability_certificate_support_v0_1 import (
    canonical_digest,
    compute_bottleneck_stability_input_digest,
    filtration_sup_norm,
    normalize_diagram_intervals,
    normalize_matching_claims,
    normalize_perturbation_records,
    optimal_bottleneck_matching,
    validate_interval_endpoint_bindings,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FiniteBottleneckPersistenceStabilityCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def build_finite_bottleneck_persistence_stability_certificate(
    *,
    source_persistent_homology_certificate_digest_a: str,
    source_persistent_homology_certificate_digest_b: str,
    bottleneck_stability_input_digest: str,
    diagram_a_intervals: list[dict],
    diagram_b_intervals: list[dict],
    simplex_perturbation_records: list[dict],
    claimed_optimal_matching: list[dict],
    claimed_bottleneck_distance_twice: int,
    claimed_filtration_sup_norm: int,
    maximum_coordinate_value: int,
    maximum_interval_count: int,
    maximum_simplex_record_count: int,
) -> FiniteBottleneckPersistenceStabilityCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_persistent_homology_certificate_digest_a": source_persistent_homology_certificate_digest_a,
        "source_persistent_homology_certificate_digest_b": source_persistent_homology_certificate_digest_b,
        "bottleneck_stability_input_digest": bottleneck_stability_input_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    for name, value, positive in (
        ("maximum_coordinate_value", maximum_coordinate_value, False),
        ("maximum_interval_count", maximum_interval_count, True),
        ("maximum_simplex_record_count", maximum_simplex_record_count, True),
    ):
        invalid = (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < (1 if positive else 0)
        )
        if invalid:
            blockers.append(f"{name}_invalid")

    if (
        not isinstance(claimed_bottleneck_distance_twice, int)
        or isinstance(claimed_bottleneck_distance_twice, bool)
        or claimed_bottleneck_distance_twice < 0
    ):
        blockers.append("claimed_bottleneck_distance_twice_invalid")
    if (
        not isinstance(claimed_filtration_sup_norm, int)
        or isinstance(claimed_filtration_sup_norm, bool)
        or claimed_filtration_sup_norm < 0
    ):
        blockers.append("claimed_filtration_sup_norm_invalid")

    coordinate_limit = (
        maximum_coordinate_value
        if isinstance(maximum_coordinate_value, int) and maximum_coordinate_value >= 0
        else 0
    )
    errors_a, normalized_a = normalize_diagram_intervals(
        diagram_a_intervals, "a", coordinate_limit
    )
    errors_b, normalized_b = normalize_diagram_intervals(
        diagram_b_intervals, "b", coordinate_limit
    )
    perturbation_errors, normalized_perturbations = normalize_perturbation_records(
        simplex_perturbation_records, coordinate_limit
    )
    matching_errors, normalized_matching = normalize_matching_claims(
        claimed_optimal_matching
    )
    blockers.extend(errors_a + errors_b + perturbation_errors + matching_errors)

    if isinstance(maximum_interval_count, int) and maximum_interval_count > 0:
        if len(normalized_a) + len(normalized_b) > maximum_interval_count:
            blockers.append("maximum_interval_count_exceeded")
    if (
        isinstance(maximum_simplex_record_count, int)
        and maximum_simplex_record_count > 0
    ):
        if len(normalized_perturbations) > maximum_simplex_record_count:
            blockers.append("maximum_simplex_record_count_exceeded")

    blockers.extend(
        validate_interval_endpoint_bindings(normalized_a, normalized_perturbations, "a")
    )
    blockers.extend(
        validate_interval_endpoint_bindings(normalized_b, normalized_perturbations, "b")
    )

    if blockers:
        return FiniteBottleneckPersistenceStabilityCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    expected_digest = compute_bottleneck_stability_input_digest(
        diagram_a_intervals=normalized_a,
        diagram_b_intervals=normalized_b,
        simplex_perturbation_records=normalized_perturbations,
        claimed_optimal_matching=normalized_matching,
        claimed_bottleneck_distance_twice=claimed_bottleneck_distance_twice,
        claimed_filtration_sup_norm=claimed_filtration_sup_norm,
    )
    if bottleneck_stability_input_digest != expected_digest:
        blockers.append("bottleneck_stability_input_digest_mismatch")

    try:
        computed_distance_twice, computed_matching = optimal_bottleneck_matching(
            normalized_a, normalized_b
        )
        computed_sup_norm = filtration_sup_norm(normalized_perturbations)
    except (KeyError, ValueError) as exc:
        blockers.append(
            f"bottleneck_stability_computation_failed_{type(exc).__name__}_{exc}"
        )
        computed_distance_twice, computed_matching, computed_sup_norm = 0, [], 0

    if computed_matching != normalized_matching:
        blockers.append("optimal_matching_claim_mismatch")
    if computed_distance_twice != claimed_bottleneck_distance_twice:
        blockers.append("bottleneck_distance_claim_mismatch")
    if computed_sup_norm != claimed_filtration_sup_norm:
        blockers.append("filtration_sup_norm_claim_mismatch")
    if computed_distance_twice > 2 * computed_sup_norm:
        blockers.append("finite_stability_inequality_failed")

    if blockers:
        return FiniteBottleneckPersistenceStabilityCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    diagonal_matches = [
        item for item in computed_matching if item["match_kind"] != "point_to_point"
    ]
    certificate = {
        "kernel": "PlanOS Finite Bottleneck Persistence Stability Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.18",
        "diagram_metric": "L_infinity_with_diagonal",
        "distance_encoding": "twice_exact_integer",
        "source_persistent_homology_certificate_digest_a": source_persistent_homology_certificate_digest_a,
        "source_persistent_homology_certificate_digest_b": source_persistent_homology_certificate_digest_b,
        "bottleneck_stability_input_digest": bottleneck_stability_input_digest,
        "diagram_a_intervals": normalized_a,
        "diagram_b_intervals": normalized_b,
        "simplex_perturbation_records": normalized_perturbations,
        "optimal_matching": computed_matching,
        "bottleneck_distance_twice": computed_distance_twice,
        "bottleneck_distance_rational": {
            "numerator": computed_distance_twice,
            "denominator": 2,
        },
        "filtration_sup_norm": computed_sup_norm,
        "stability_budget_twice": 2 * computed_sup_norm,
        "stability_slack_twice": 2 * computed_sup_norm - computed_distance_twice,
        "point_to_point_match_count": len(computed_matching) - len(diagonal_matches),
        "diagonal_match_count": len(diagonal_matches),
        "maximum_coordinate_value": maximum_coordinate_value,
        "maximum_interval_count": maximum_interval_count,
        "maximum_simplex_record_count": maximum_simplex_record_count,
        "interval_endpoint_bindings_verified": True,
        "point_matching_recomputed": True,
        "diagonal_matching_recomputed": True,
        "infinite_intervals_never_matched_to_diagonal": True,
        "bottleneck_distance_recomputed": True,
        "filtration_sup_norm_recomputed": True,
        "finite_stability_inequality_verified": True,
        "finite_diagram_pair_only": True,
        "dimensions_above_two_not_compared": True,
        "source_filtration_to_barcode_relation_not_recomputed": True,
        "full_persistence_stability_theorem_not_claimed": True,
        "wasserstein_distance_not_computed": True,
        "interleaving_distance_not_computed": True,
        "zigzag_distance_not_computed": True,
        "persistence_distance_does_not_rank_candidates": True,
        "candidate_identity_retained": True,
        "source_persistent_homology_certificate_a_not_mutated": True,
        "source_persistent_homology_certificate_b_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "bottleneck_distance_grants_no_authority": True,
        "stability_witness_grants_no_authority": True,
        "diagonal_matching_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["bottleneck_stability_certificate_digest"] = canonical_digest(certificate)
    return FiniteBottleneckPersistenceStabilityCertificateResult(
        STATUS_READY, [], certificate
    )
