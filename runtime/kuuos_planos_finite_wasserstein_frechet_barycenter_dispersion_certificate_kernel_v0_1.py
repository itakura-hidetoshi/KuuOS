from __future__ import annotations

from dataclasses import dataclass

from runtime.kuuos_planos_finite_wasserstein_frechet_barycenter_dispersion_certificate_support_v0_1 import (
    candidate_functional_table,
    canonical_digest,
    compute_frechet_barycenter_dispersion_input_digest,
    consensus_source_transports,
    finite_frechet_minimizers,
    normalize_barycenter_candidates,
    normalize_candidate_functional_claims,
    normalize_consensus_source_claims,
    normalize_consensus_tail_claims,
    normalize_source_diagram_family,
    normalize_tail_thresholds,
    normalize_weighted_moment_claims,
    reduced_fraction,
    weighted_consensus_moment_profile,
    weighted_consensus_tail_profile,
)

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"


@dataclass
class FiniteWassersteinFrechetBarycenterDispersionCertificateResult:
    status: str
    blockers: list[str]
    certificate: dict | None


def _nat(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _positive_nat(value) -> bool:
    return _nat(value) and value > 0


def _normalize_sorted_unique_texts(value, empty_blocker: str, invalid_blocker: str):
    if not isinstance(value, list) or not value:
        return [empty_blocker], []
    if any(not isinstance(item, str) or not item for item in value):
        return [invalid_blocker], []
    if value != sorted(set(value)):
        return [invalid_blocker], []
    return [], list(value)


def build_finite_wasserstein_frechet_barycenter_dispersion_certificate(
    *,
    frechet_barycenter_dispersion_input_digest: str,
    source_diagram_family: list[dict],
    barycenter_candidates: list[dict],
    p_exponent: int,
    functional_denominator: int,
    consensus_tail_thresholds_twice: list[int],
    claimed_candidate_functionals: list[dict],
    claimed_minimizer_candidate_ids: list[str],
    claimed_representative_candidate_id: str,
    claimed_consensus_source_transports: list[dict],
    claimed_dispersion_numerator_twice_power_units: int,
    claimed_maximum_source_transport_power_twice_units: int,
    claimed_maximum_source_ids: list[str],
    claimed_weighted_moment_profile: list[dict],
    claimed_consensus_tail_profile: list[dict],
    maximum_p_exponent: int,
    maximum_coordinate_value: int,
    maximum_source_count: int,
    maximum_candidate_count: int,
    maximum_interval_count_per_diagram: int,
    maximum_tail_threshold_count: int,
) -> FiniteWassersteinFrechetBarycenterDispersionCertificateResult:
    blockers: list[str] = []

    if (
        not isinstance(frechet_barycenter_dispersion_input_digest, str)
        or not frechet_barycenter_dispersion_input_digest
    ):
        blockers.append("frechet_barycenter_dispersion_input_digest_missing")

    for name, value, positive in (
        ("maximum_p_exponent", maximum_p_exponent, True),
        ("maximum_coordinate_value", maximum_coordinate_value, False),
        ("maximum_source_count", maximum_source_count, True),
        ("maximum_candidate_count", maximum_candidate_count, True),
        (
            "maximum_interval_count_per_diagram",
            maximum_interval_count_per_diagram,
            True,
        ),
        ("maximum_tail_threshold_count", maximum_tail_threshold_count, True),
    ):
        valid = _positive_nat(value) if positive else _nat(value)
        if not valid:
            blockers.append(f"{name}_invalid")

    if (
        not _positive_nat(p_exponent)
        or (
            _positive_nat(maximum_p_exponent)
            and p_exponent > maximum_p_exponent
        )
    ):
        blockers.append("p_exponent_invalid_or_exceeds_bound")
    if not _positive_nat(functional_denominator):
        blockers.append("functional_denominator_invalid")

    coordinate_limit = maximum_coordinate_value if _nat(maximum_coordinate_value) else 0
    source_limit = maximum_source_count if _positive_nat(maximum_source_count) else 1
    candidate_limit = maximum_candidate_count if _positive_nat(maximum_candidate_count) else 1
    interval_limit = (
        maximum_interval_count_per_diagram
        if _positive_nat(maximum_interval_count_per_diagram)
        else 1
    )
    p_limit = p_exponent if _positive_nat(p_exponent) else 1

    source_errors, normalized_sources = normalize_source_diagram_family(
        source_diagram_family,
        coordinate_limit,
        source_limit,
        interval_limit,
    )
    candidate_errors, normalized_candidates = normalize_barycenter_candidates(
        barycenter_candidates,
        coordinate_limit,
        candidate_limit,
        interval_limit,
    )
    functional_errors, normalized_functionals = normalize_candidate_functional_claims(
        claimed_candidate_functionals
    )
    minimizer_errors, normalized_minimizers = _normalize_sorted_unique_texts(
        claimed_minimizer_candidate_ids,
        "claimed_minimizer_candidate_ids_empty",
        "claimed_minimizer_candidate_ids_invalid",
    )
    consensus_errors, normalized_consensus = normalize_consensus_source_claims(
        claimed_consensus_source_transports, p_limit
    )
    maximum_source_errors, normalized_maximum_source_ids = _normalize_sorted_unique_texts(
        claimed_maximum_source_ids,
        "claimed_maximum_source_ids_empty",
        "claimed_maximum_source_ids_invalid",
    )
    moment_errors, normalized_moments = normalize_weighted_moment_claims(
        claimed_weighted_moment_profile, p_limit
    )
    threshold_errors, normalized_thresholds = normalize_tail_thresholds(
        consensus_tail_thresholds_twice, 2 * coordinate_limit
    )
    tail_errors, normalized_tail = normalize_consensus_tail_claims(
        claimed_consensus_tail_profile
    )
    blockers.extend(
        source_errors
        + candidate_errors
        + functional_errors
        + minimizer_errors
        + consensus_errors
        + maximum_source_errors
        + moment_errors
        + threshold_errors
        + tail_errors
    )

    if not isinstance(claimed_representative_candidate_id, str) or not claimed_representative_candidate_id:
        blockers.append("claimed_representative_candidate_id_missing")
    for name, value in (
        (
            "claimed_dispersion_numerator_twice_power_units",
            claimed_dispersion_numerator_twice_power_units,
        ),
        (
            "claimed_maximum_source_transport_power_twice_units",
            claimed_maximum_source_transport_power_twice_units,
        ),
    ):
        if not _nat(value):
            blockers.append(f"{name}_invalid")

    if (
        _positive_nat(maximum_tail_threshold_count)
        and len(normalized_thresholds) > maximum_tail_threshold_count
    ):
        blockers.append("maximum_tail_threshold_count_exceeded")

    source_ids = [item["source_id"] for item in normalized_sources]
    candidate_ids = [item["candidate_id"] for item in normalized_candidates]
    if _positive_nat(functional_denominator):
        if sum(item["weight_numerator"] for item in normalized_sources) != functional_denominator:
            blockers.append("source_weight_numerators_must_sum_to_functional_denominator")
    if [item["candidate_id"] for item in normalized_functionals] != candidate_ids:
        blockers.append("candidate_functional_ids_mismatch_candidate_set")
    for item in normalized_functionals:
        if item["functional_denominator"] != functional_denominator:
            blockers.append(f"candidate_functional_denominator_mismatch_{item['candidate_id']}")
        if [value["source_id"] for value in item["source_transport_power_sums"]] != source_ids:
            blockers.append(f"candidate_functional_source_ids_mismatch_{item['candidate_id']}")
    if [item["source_id"] for item in normalized_consensus] != source_ids:
        blockers.append("consensus_source_ids_mismatch_source_family")
    if [item["order"] for item in normalized_moments] != list(range(1, p_limit + 1)):
        blockers.append("weighted_moment_orders_must_cover_one_through_p")
    if any(
        item["functional_denominator"] != functional_denominator
        for item in normalized_moments
    ):
        blockers.append("weighted_moment_functional_denominator_mismatch")
    if [item["threshold_twice"] for item in normalized_tail] != normalized_thresholds:
        blockers.append("consensus_tail_claim_thresholds_mismatch")
    if any(
        item["functional_denominator"] != functional_denominator
        for item in normalized_tail
    ):
        blockers.append("consensus_tail_functional_denominator_mismatch")
    if any(item not in candidate_ids for item in normalized_minimizers):
        blockers.append("claimed_minimizer_not_in_candidate_set")
    if claimed_representative_candidate_id not in candidate_ids:
        blockers.append("claimed_representative_not_in_candidate_set")
    if any(item not in source_ids for item in normalized_maximum_source_ids):
        blockers.append("claimed_maximum_source_not_in_source_family")

    if blockers:
        return FiniteWassersteinFrechetBarycenterDispersionCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    expected_digest = compute_frechet_barycenter_dispersion_input_digest(
        source_diagram_family=normalized_sources,
        barycenter_candidates=normalized_candidates,
        p_exponent=p_exponent,
        functional_denominator=functional_denominator,
        consensus_tail_thresholds_twice=normalized_thresholds,
        claimed_candidate_functionals=normalized_functionals,
        claimed_minimizer_candidate_ids=normalized_minimizers,
        claimed_representative_candidate_id=claimed_representative_candidate_id,
        claimed_consensus_source_transports=normalized_consensus,
        claimed_dispersion_numerator_twice_power_units=claimed_dispersion_numerator_twice_power_units,
        claimed_maximum_source_transport_power_twice_units=claimed_maximum_source_transport_power_twice_units,
        claimed_maximum_source_ids=normalized_maximum_source_ids,
        claimed_weighted_moment_profile=normalized_moments,
        claimed_consensus_tail_profile=normalized_tail,
    )
    if frechet_barycenter_dispersion_input_digest != expected_digest:
        blockers.append("frechet_barycenter_dispersion_input_digest_mismatch")

    try:
        computed_functionals = candidate_functional_table(
            normalized_sources,
            normalized_candidates,
            p_exponent,
            functional_denominator,
        )
        (
            computed_dispersion,
            computed_minimizers,
            computed_representative,
        ) = finite_frechet_minimizers(computed_functionals)
        representative_candidate = next(
            item
            for item in normalized_candidates
            if item["candidate_id"] == computed_representative
        )
        computed_consensus = consensus_source_transports(
            normalized_sources, representative_candidate, p_exponent
        )
        computed_moments = weighted_consensus_moment_profile(
            computed_consensus, p_exponent, functional_denominator
        )
        computed_tail = weighted_consensus_tail_profile(
            computed_consensus,
            normalized_thresholds,
            p_exponent,
            functional_denominator,
        )
        computed_maximum_source_power = max(
            item["transport_power_sum_twice_units"] for item in computed_consensus
        )
        computed_maximum_source_ids = sorted(
            item["source_id"]
            for item in computed_consensus
            if item["transport_power_sum_twice_units"]
            == computed_maximum_source_power
        )
    except (KeyError, StopIteration, ValueError, ZeroDivisionError) as exc:
        blockers.append(
            f"frechet_barycenter_dispersion_computation_failed_{type(exc).__name__}_{exc}"
        )
        computed_functionals = []
        computed_dispersion = 0
        computed_minimizers = []
        computed_representative = ""
        representative_candidate = None
        computed_consensus = []
        computed_moments = []
        computed_tail = []
        computed_maximum_source_power = 0
        computed_maximum_source_ids = []

    if computed_functionals != normalized_functionals:
        blockers.append("candidate_functional_claim_mismatch")
    if computed_minimizers != normalized_minimizers:
        blockers.append("minimizer_tie_set_claim_mismatch")
    if computed_representative != claimed_representative_candidate_id:
        blockers.append("representative_candidate_claim_mismatch")
    if computed_consensus != normalized_consensus:
        blockers.append("consensus_source_transport_claim_mismatch")
    if computed_dispersion != claimed_dispersion_numerator_twice_power_units:
        blockers.append("dispersion_numerator_claim_mismatch")
    if (
        computed_maximum_source_power
        != claimed_maximum_source_transport_power_twice_units
    ):
        blockers.append("maximum_source_transport_power_claim_mismatch")
    if computed_maximum_source_ids != normalized_maximum_source_ids:
        blockers.append("maximum_source_ids_claim_mismatch")
    if computed_moments != normalized_moments:
        blockers.append("weighted_moment_profile_claim_mismatch")
    if computed_tail != normalized_tail:
        blockers.append("consensus_tail_profile_claim_mismatch")

    contribution_sum = sum(
        item["weighted_contribution_numerator"] for item in computed_consensus
    )
    if contribution_sum != computed_dispersion:
        blockers.append("source_contribution_sum_does_not_equal_dispersion")
    representative_functional = next(
        (
            item
            for item in computed_functionals
            if item["candidate_id"] == computed_representative
        ),
        None,
    )
    if representative_functional is None:
        blockers.append("representative_functional_missing")
    elif representative_functional["source_transport_power_sums"] != [
        {
            "source_id": item["source_id"],
            "transport_power_sum_twice_units": item[
                "transport_power_sum_twice_units"
            ],
        }
        for item in computed_consensus
    ]:
        blockers.append("representative_functional_consensus_power_mismatch")
    if computed_moments:
        if computed_moments[-1]["weighted_power_sum_numerator"] != computed_dispersion:
            blockers.append("p_moment_does_not_equal_dispersion")
    if any(
        item["p_power_lower_bound_numerator"] > computed_dispersion
        for item in computed_tail
    ):
        blockers.append("weighted_consensus_tail_power_bound_failed")
    if any(
        not (
            item["root_floor_twice"] ** p_exponent
            <= item["transport_power_sum_twice_units"]
            <= item["root_ceil_twice"] ** p_exponent
        )
        for item in computed_consensus
    ):
        blockers.append("source_transport_root_bracket_failed")
    if computed_dispersion == 0 and any(
        item["weighted_contribution_numerator"] != 0
        for item in computed_consensus
    ):
        blockers.append("zero_dispersion_source_contribution_implication_failed")

    if blockers:
        return FiniteWassersteinFrechetBarycenterDispersionCertificateResult(
            STATUS_BLOCKED, sorted(set(blockers)), None
        )

    certificate = {
        "kernel": "PlanOS Finite Wasserstein Frechet Barycenter and Dispersion Certificate Kernel",
        "kernel_version": "v0.1",
        "planos_version": "v1.20",
        "distance_model": "finite_p_Wasserstein_L_infinity_with_diagonal",
        "distance_encoding": "twice_exact_integer_power_sum",
        "weight_encoding": "positive_integer_numerators_with_common_denominator",
        "p_exponent": p_exponent,
        "functional_denominator": functional_denominator,
        "source_diagram_family": normalized_sources,
        "barycenter_candidates": normalized_candidates,
        "candidate_functionals": computed_functionals,
        "minimum_functional_numerator_twice_power_units": computed_dispersion,
        "minimum_functional_reduced": reduced_fraction(
            computed_dispersion, functional_denominator
        ),
        "minimizer_candidate_ids": computed_minimizers,
        "minimizer_count": len(computed_minimizers),
        "finite_candidate_minimizer_unique": len(computed_minimizers) == 1,
        "representative_candidate_id": computed_representative,
        "representative_candidate_diagram_digest": representative_candidate[
            "candidate_diagram_digest"
        ],
        "consensus_source_transports": computed_consensus,
        "dispersion_numerator_twice_power_units": computed_dispersion,
        "dispersion_denominator": functional_denominator,
        "dispersion_reduced": reduced_fraction(
            computed_dispersion, functional_denominator
        ),
        "maximum_source_transport_power_twice_units": computed_maximum_source_power,
        "maximum_source_ids": computed_maximum_source_ids,
        "weighted_moment_profile": computed_moments,
        "consensus_tail_profile": computed_tail,
        "consensus_tail_thresholds_twice": normalized_thresholds,
        "source_count": len(normalized_sources),
        "candidate_count": len(normalized_candidates),
        "consensus_matching_count": sum(
            len(item["matching"]) for item in computed_consensus
        ),
        "source_certificate_digests_bound": True,
        "candidate_diagram_digests_recomputed": True,
        "candidate_functionals_recomputed": True,
        "finite_minimizer_witness_recomputed": True,
        "minimizer_tie_set_recomputed": True,
        "lexical_representative_recomputed": True,
        "consensus_transports_recomputed": True,
        "source_contributions_sum_to_dispersion": True,
        "maximum_source_deviation_recomputed": True,
        "weighted_moment_profile_recomputed": True,
        "consensus_tail_profile_recomputed": True,
        "weighted_consensus_tail_bounds_verified": True,
        "zero_dispersion_implies_zero_source_contributions": True,
        "finite_diagram_family_only": True,
        "finite_candidate_barycenter_set_only": True,
        "bounded_positive_integer_p_only": True,
        "exact_rational_weights_only": True,
        "global_wasserstein_barycenter_not_claimed": True,
        "global_barycenter_existence_not_claimed": True,
        "global_barycenter_uniqueness_not_claimed": True,
        "finite_candidate_uniqueness_only_when_tie_set_singleton": True,
        "frechet_minimizer_does_not_rank_plans": True,
        "consensus_diagram_is_not_selected_plan": True,
        "low_dispersion_grants_no_activation_authorization": True,
        "high_dispersion_does_not_automatically_reject": True,
        "diagonal_consensus_grants_no_deletion_authority": True,
        "finite_diagram_family_is_not_planning_population": True,
        "source_v1_17_certificates_not_mutated": True,
        "source_v1_18_certificates_not_mutated": True,
        "source_v1_19_certificates_not_mutated": True,
        "persistent_world_state_unchanged": True,
        "candidate_selection_performed": False,
        "candidate_ranking_performed": False,
        "activation_performed": False,
        "history_read_only": True,
        "future_only": True,
        "active_now": False,
        "execution_permission": False,
        "maximum_p_exponent": maximum_p_exponent,
        "maximum_coordinate_value": maximum_coordinate_value,
        "maximum_source_count": maximum_source_count,
        "maximum_candidate_count": maximum_candidate_count,
        "maximum_interval_count_per_diagram": maximum_interval_count_per_diagram,
        "maximum_tail_threshold_count": maximum_tail_threshold_count,
        "frechet_barycenter_dispersion_input_digest": frechet_barycenter_dispersion_input_digest,
    }
    certificate["certificate_digest"] = canonical_digest(certificate)
    return FiniteWassersteinFrechetBarycenterDispersionCertificateResult(
        STATUS_READY, [], certificate
    )
