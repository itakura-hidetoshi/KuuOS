from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_finite_p_wasserstein_persistence_transport_certificate_support_v0_1 import (
    canonical_digest,
    compute_p_wasserstein_transport_input_digest,
    cost_moment_profile,
    filtration_sup_norm,
    integer_nth_root_bounds,
    normalize_diagram_intervals,
    normalize_moment_claims,
    normalize_perturbation_records,
    normalize_tail_claims,
    normalize_tail_thresholds,
    normalize_transport_matching_claims,
    optimal_bottleneck_matching,
    optimal_p_wasserstein_transport,
    tail_profile,
    validate_interval_endpoint_bindings,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FinitePWassersteinPersistenceTransportCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def _nat(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def build_finite_p_wasserstein_persistence_transport_certificate(
    *,
    source_persistent_homology_certificate_digest_a: str,
    source_persistent_homology_certificate_digest_b: str,
    source_bottleneck_stability_certificate_digest: str,
    p_wasserstein_transport_input_digest: str,
    diagram_a_intervals: list[dict],
    diagram_b_intervals: list[dict],
    simplex_perturbation_records: list[dict],
    p_exponent: int,
    tail_thresholds_twice: list[int],
    claimed_optimal_transport_matching: list[dict],
    claimed_transport_power_sum_twice_units: int,
    claimed_wasserstein_root_floor_twice: int,
    claimed_wasserstein_root_ceil_twice: int,
    claimed_bottleneck_distance_twice: int,
    claimed_filtration_sup_norm: int,
    claimed_cost_moment_profile: list[dict],
    claimed_tail_profile: list[dict],
    maximum_p_exponent: int,
    maximum_coordinate_value: int,
    maximum_interval_count: int,
    maximum_simplex_record_count: int,
    maximum_tail_threshold_count: int,
) -> FinitePWassersteinPersistenceTransportCertificateResult:
    blockers: list[str] = []
    for name, value in {
        "source_persistent_homology_certificate_digest_a": source_persistent_homology_certificate_digest_a,
        "source_persistent_homology_certificate_digest_b": source_persistent_homology_certificate_digest_b,
        "source_bottleneck_stability_certificate_digest": source_bottleneck_stability_certificate_digest,
        "p_wasserstein_transport_input_digest": p_wasserstein_transport_input_digest,
    }.items():
        if not isinstance(value, str) or not value:
            blockers.append(f"{name}_missing")

    for name, value, positive in (
        ("maximum_p_exponent", maximum_p_exponent, True),
        ("maximum_coordinate_value", maximum_coordinate_value, False),
        ("maximum_interval_count", maximum_interval_count, True),
        ("maximum_simplex_record_count", maximum_simplex_record_count, True),
        ("maximum_tail_threshold_count", maximum_tail_threshold_count, True),
    ):
        invalid = (
            not isinstance(value, int)
            or isinstance(value, bool)
            or value < (1 if positive else 0)
        )
        if invalid:
            blockers.append(f"{name}_invalid")

    if (
        not isinstance(p_exponent, int)
        or isinstance(p_exponent, bool)
        or p_exponent <= 0
        or (
            isinstance(maximum_p_exponent, int)
            and maximum_p_exponent > 0
            and p_exponent > maximum_p_exponent
        )
    ):
        blockers.append("p_exponent_invalid_or_exceeds_bound")

    for name, value in {
        "claimed_transport_power_sum_twice_units": claimed_transport_power_sum_twice_units,
        "claimed_wasserstein_root_floor_twice": claimed_wasserstein_root_floor_twice,
        "claimed_wasserstein_root_ceil_twice": claimed_wasserstein_root_ceil_twice,
        "claimed_bottleneck_distance_twice": claimed_bottleneck_distance_twice,
        "claimed_filtration_sup_norm": claimed_filtration_sup_norm,
    }.items():
        if not _nat(value):
            blockers.append(f"{name}_invalid")

    coordinate_limit = (
        maximum_coordinate_value
        if isinstance(maximum_coordinate_value, int) and maximum_coordinate_value >= 0
        else 0
    )
    p_limit = p_exponent if isinstance(p_exponent, int) and p_exponent > 0 else 1
    errors_a, normalized_a = normalize_diagram_intervals(
        diagram_a_intervals, "a", coordinate_limit
    )
    errors_b, normalized_b = normalize_diagram_intervals(
        diagram_b_intervals, "b", coordinate_limit
    )
    perturbation_errors, normalized_perturbations = normalize_perturbation_records(
        simplex_perturbation_records, coordinate_limit
    )
    matching_errors, normalized_matching = normalize_transport_matching_claims(
        claimed_optimal_transport_matching, p_limit
    )
    moment_errors, normalized_moments = normalize_moment_claims(
        claimed_cost_moment_profile, p_limit
    )
    threshold_errors, normalized_thresholds = normalize_tail_thresholds(
        tail_thresholds_twice, 2 * coordinate_limit
    )
    tail_errors, normalized_tail = normalize_tail_claims(claimed_tail_profile)
    blockers.extend(
        errors_a
        + errors_b
        + perturbation_errors
        + matching_errors
        + moment_errors
        + threshold_errors
        + tail_errors
    )

    if isinstance(maximum_interval_count, int) and maximum_interval_count > 0:
        if len(normalized_a) + len(normalized_b) > maximum_interval_count:
            blockers.append("maximum_interval_count_exceeded")
    if (
        isinstance(maximum_simplex_record_count, int)
        and maximum_simplex_record_count > 0
        and len(normalized_perturbations) > maximum_simplex_record_count
    ):
        blockers.append("maximum_simplex_record_count_exceeded")
    if (
        isinstance(maximum_tail_threshold_count, int)
        and maximum_tail_threshold_count > 0
        and len(normalized_thresholds) > maximum_tail_threshold_count
    ):
        blockers.append("maximum_tail_threshold_count_exceeded")

    if normalized_moments and [item["order"] for item in normalized_moments] != list(
        range(1, p_limit + 1)
    ):
        blockers.append("cost_moment_orders_must_cover_one_through_p")
    if normalized_tail and [item["threshold_twice"] for item in normalized_tail] != normalized_thresholds:
        blockers.append("tail_claim_thresholds_mismatch")

    blockers.extend(
        validate_interval_endpoint_bindings(normalized_a, normalized_perturbations, "a")
    )
    blockers.extend(
        validate_interval_endpoint_bindings(normalized_b, normalized_perturbations, "b")
    )

    if blockers:
        return FinitePWassersteinPersistenceTransportCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    expected_digest = compute_p_wasserstein_transport_input_digest(
        diagram_a_intervals=normalized_a,
        diagram_b_intervals=normalized_b,
        simplex_perturbation_records=normalized_perturbations,
        p_exponent=p_exponent,
        tail_thresholds_twice=normalized_thresholds,
        claimed_optimal_transport_matching=normalized_matching,
        claimed_transport_power_sum_twice_units=claimed_transport_power_sum_twice_units,
        claimed_wasserstein_root_floor_twice=claimed_wasserstein_root_floor_twice,
        claimed_wasserstein_root_ceil_twice=claimed_wasserstein_root_ceil_twice,
        claimed_bottleneck_distance_twice=claimed_bottleneck_distance_twice,
        claimed_filtration_sup_norm=claimed_filtration_sup_norm,
        claimed_cost_moment_profile=normalized_moments,
        claimed_tail_profile=normalized_tail,
    )
    if p_wasserstein_transport_input_digest != expected_digest:
        blockers.append("p_wasserstein_transport_input_digest_mismatch")

    try:
        (
            computed_transport_power_sum,
            computed_transport_max_cost,
            computed_matching,
        ) = optimal_p_wasserstein_transport(normalized_a, normalized_b, p_exponent)
        computed_root_floor, computed_root_ceil = integer_nth_root_bounds(
            computed_transport_power_sum, p_exponent
        )
        computed_bottleneck, bottleneck_matching = optimal_bottleneck_matching(
            normalized_a, normalized_b
        )
        computed_sup_norm = filtration_sup_norm(normalized_perturbations)
        computed_moments = cost_moment_profile(computed_matching, p_exponent)
        computed_tail = tail_profile(
            computed_matching, normalized_thresholds, p_exponent
        )
    except (KeyError, ValueError, ZeroDivisionError) as exc:
        blockers.append(
            f"p_wasserstein_transport_computation_failed_{type(exc).__name__}_{exc}"
        )
        computed_transport_power_sum = 0
        computed_transport_max_cost = 0
        computed_matching = []
        computed_root_floor = 0
        computed_root_ceil = 0
        computed_bottleneck = 0
        bottleneck_matching = []
        computed_sup_norm = 0
        computed_moments = []
        computed_tail = []

    if computed_matching != normalized_matching:
        blockers.append("optimal_transport_matching_claim_mismatch")
    if computed_transport_power_sum != claimed_transport_power_sum_twice_units:
        blockers.append("transport_power_sum_claim_mismatch")
    if computed_root_floor != claimed_wasserstein_root_floor_twice:
        blockers.append("wasserstein_root_floor_claim_mismatch")
    if computed_root_ceil != claimed_wasserstein_root_ceil_twice:
        blockers.append("wasserstein_root_ceil_claim_mismatch")
    if computed_bottleneck != claimed_bottleneck_distance_twice:
        blockers.append("source_bottleneck_distance_claim_mismatch")
    if computed_sup_norm != claimed_filtration_sup_norm:
        blockers.append("filtration_sup_norm_claim_mismatch")
    if computed_moments != normalized_moments:
        blockers.append("cost_moment_profile_claim_mismatch")
    if computed_tail != normalized_tail:
        blockers.append("tail_profile_claim_mismatch")

    bottleneck_power = computed_bottleneck ** p_exponent
    bottleneck_cardinality_budget = len(bottleneck_matching) * bottleneck_power
    filtration_cardinality_budget = len(bottleneck_matching) * (
        (2 * computed_sup_norm) ** p_exponent
    )
    if computed_bottleneck > 2 * computed_sup_norm:
        blockers.append("source_finite_bottleneck_stability_inequality_failed")
    if bottleneck_power > computed_transport_power_sum:
        blockers.append("bottleneck_lower_bound_on_wasserstein_power_failed")
    if computed_transport_power_sum > bottleneck_cardinality_budget:
        blockers.append("finite_cardinality_bottleneck_upper_bound_failed")
    if computed_transport_power_sum > filtration_cardinality_budget:
        blockers.append("finite_perturbation_transport_budget_failed")
    if any(
        item["p_power_lower_bound"] > computed_transport_power_sum
        for item in computed_tail
    ):
        blockers.append("tail_markov_power_bound_failed")
    if not (
        computed_root_floor ** p_exponent
        <= computed_transport_power_sum
        <= computed_root_ceil ** p_exponent
    ):
        blockers.append("wasserstein_root_bracket_failed")

    if blockers:
        return FinitePWassersteinPersistenceTransportCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    diagonal_matches = [
        item for item in computed_matching if item["match_kind"] != "point_to_point"
    ]
    exact_root = computed_root_floor == computed_root_ceil
    certificate = {
        "kernel": "PlanOS Finite p-Wasserstein Persistence Transport Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.19",
        "diagram_metric": "p_Wasserstein_L_infinity_with_diagonal",
        "distance_encoding": "twice_exact_integer_power_sum",
        "p_exponent": p_exponent,
        "source_persistent_homology_certificate_digest_a": source_persistent_homology_certificate_digest_a,
        "source_persistent_homology_certificate_digest_b": source_persistent_homology_certificate_digest_b,
        "source_bottleneck_stability_certificate_digest": source_bottleneck_stability_certificate_digest,
        "p_wasserstein_transport_input_digest": p_wasserstein_transport_input_digest,
        "diagram_a_intervals": normalized_a,
        "diagram_b_intervals": normalized_b,
        "simplex_perturbation_records": normalized_perturbations,
        "optimal_transport_matching": computed_matching,
        "transport_power_sum_twice_units": computed_transport_power_sum,
        "transport_maximum_cost_twice": computed_transport_max_cost,
        "wasserstein_distance_twice_root_bounds": {
            "floor": computed_root_floor,
            "ceil": computed_root_ceil,
        },
        "wasserstein_distance_rational": (
            {"numerator": computed_root_floor, "denominator": 2}
            if exact_root
            else None
        ),
        "bottleneck_distance_twice": computed_bottleneck,
        "filtration_sup_norm": computed_sup_norm,
        "bottleneck_lower_bound_power_twice_units": bottleneck_power,
        "bottleneck_cardinality_upper_bound_power_twice_units": bottleneck_cardinality_budget,
        "filtration_cardinality_transport_budget_power_twice_units": filtration_cardinality_budget,
        "cost_moment_profile": computed_moments,
        "tail_profile": computed_tail,
        "transport_match_count": len(computed_matching),
        "point_to_point_match_count": len(computed_matching) - len(diagonal_matches),
        "diagonal_match_count": len(diagonal_matches),
        "bottleneck_matching_cardinality": len(bottleneck_matching),
        "maximum_p_exponent": maximum_p_exponent,
        "maximum_coordinate_value": maximum_coordinate_value,
        "maximum_interval_count": maximum_interval_count,
        "maximum_simplex_record_count": maximum_simplex_record_count,
        "maximum_tail_threshold_count": maximum_tail_threshold_count,
        "interval_endpoint_bindings_verified": True,
        "optimal_transport_matching_recomputed": True,
        "transport_power_sum_recomputed": True,
        "integer_root_bounds_recomputed": True,
        "bottleneck_distance_recomputed": True,
        "filtration_sup_norm_recomputed": True,
        "cost_moment_profile_recomputed": True,
        "tail_profile_recomputed": True,
        "tail_markov_power_bounds_verified": True,
        "bottleneck_to_wasserstein_power_bounds_verified": True,
        "finite_perturbation_transport_budget_verified": True,
        "infinite_intervals_never_matched_to_diagonal": True,
        "finite_diagram_pair_only": True,
        "bounded_p_exponent_only": True,
        "dimensions_above_two_not_compared": True,
        "irrational_wasserstein_roots_not_decimal_approximated": True,
        "source_filtration_to_barcode_relation_not_recomputed": True,
        "full_p_wasserstein_stability_theorem_not_claimed": True,
        "unbounded_diagram_transport_not_computed": True,
        "wasserstein_transport_does_not_rank_candidates": True,
        "tail_profile_does_not_rank_candidates": True,
        "moment_profile_does_not_rank_candidates": True,
        "candidate_identity_retained": True,
        "source_persistent_homology_certificate_a_not_mutated": True,
        "source_persistent_homology_certificate_b_not_mutated": True,
        "source_bottleneck_stability_certificate_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "decision_selection_performed": False,
        "history_read_only": True,
        "p_wasserstein_distance_grants_no_authority": True,
        "transport_matching_grants_no_authority": True,
        "tail_moment_evidence_grants_no_authority": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
    }
    certificate["p_wasserstein_transport_certificate_digest"] = canonical_digest(
        certificate
    )
    return FinitePWassersteinPersistenceTransportCertificateResult(
        STATUS_READY, [], certificate
    )
