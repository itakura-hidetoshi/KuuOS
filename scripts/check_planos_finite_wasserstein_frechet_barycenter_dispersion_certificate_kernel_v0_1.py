#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_planos_finite_wasserstein_frechet_barycenter_dispersion_certificate_kernel_v0_1 import (
    STATUS_READY,
    build_finite_wasserstein_frechet_barycenter_dispersion_certificate,
)
from runtime.kuuos_planos_finite_wasserstein_frechet_barycenter_dispersion_certificate_support_v0_1 import (
    candidate_diagram_digest,
    candidate_functional_table,
    compute_frechet_barycenter_dispersion_input_digest,
    consensus_source_transports,
    finite_frechet_minimizers,
    weighted_consensus_moment_profile,
    weighted_consensus_tail_profile,
)


def interval(
    interval_id: str,
    dimension: int,
    birth: int,
    death: int | None,
    birth_simplex_id: str,
    death_simplex_id: str,
) -> dict:
    return {
        "interval_id": interval_id,
        "dimension": dimension,
        "birth": birth,
        "death": death,
        "birth_simplex_id": birth_simplex_id,
        "death_simplex_id": death_simplex_id,
        "source_interval_digest": f"digest-{interval_id}",
    }


def diagram_left(prefix: str = "A") -> list[dict]:
    return [
        interval(f"{prefix}-H0-finite", 0, 0, 2, "vertex-B", "edge-AB"),
        interval(f"{prefix}-H0-infinite", 0, 0, None, "vertex-A", ""),
        interval(f"{prefix}-H1-main", 1, 2, 6, "edge-main", "triangle-main"),
    ]


def diagram_center(prefix: str = "M") -> list[dict]:
    return [
        interval(f"{prefix}-H0-finite", 0, 1, 3, "vertex-B", "edge-AB"),
        interval(f"{prefix}-H0-infinite", 0, 1, None, "vertex-A", ""),
        interval(f"{prefix}-H1-main", 1, 3, 7, "edge-main", "triangle-main"),
    ]


def diagram_center_extra(prefix: str = "B") -> list[dict]:
    return diagram_center(prefix) + [
        interval(f"{prefix}-H1-extra", 1, 4, 6, "edge-extra", "triangle-extra")
    ]


def diagram_right(prefix: str = "C") -> list[dict]:
    return [
        interval(f"{prefix}-H0-finite", 0, 2, 4, "vertex-B", "edge-AB"),
        interval(f"{prefix}-H0-infinite", 0, 2, None, "vertex-A", ""),
        interval(f"{prefix}-H1-main", 1, 4, 8, "edge-main", "triangle-main"),
    ]


def source_record(source_id: str, weight: int, diagram: list[dict]) -> dict:
    return {
        "source_id": source_id,
        "weight_numerator": weight,
        "source_persistent_homology_certificate_digest": f"planos-v1-17-{source_id}",
        "source_bottleneck_stability_certificate_digest": f"planos-v1-18-{source_id}",
        "source_p_wasserstein_transport_certificate_digest": f"planos-v1-19-{source_id}",
        "diagram_intervals": sorted(diagram, key=lambda item: item["interval_id"]),
    }


def source_family() -> list[dict]:
    return [
        source_record("source-A", 1, diagram_left("A")),
        source_record("source-B", 2, diagram_center_extra("B")),
        source_record("source-C", 1, diagram_right("C")),
    ]


def candidate_record(candidate_id: str, diagram: list[dict]) -> dict:
    return {
        "candidate_id": candidate_id,
        "candidate_diagram_digest": candidate_diagram_digest(candidate_id, diagram),
        "diagram_intervals": sorted(diagram, key=lambda item: item["interval_id"]),
    }


def candidate_set() -> list[dict]:
    return [
        candidate_record("candidate-center", diagram_center("M")),
        candidate_record("candidate-left", diagram_left("L")),
        candidate_record("candidate-right", diagram_right("R")),
    ]


def reference_claims(
    sources: list[dict],
    candidates: list[dict],
    p_exponent: int,
    denominator: int,
    thresholds: list[int],
):
    functionals = candidate_functional_table(
        sources, candidates, p_exponent, denominator
    )
    dispersion, minimizers, representative = finite_frechet_minimizers(functionals)
    candidate = next(
        item for item in candidates if item["candidate_id"] == representative
    )
    consensus = consensus_source_transports(sources, candidate, p_exponent)
    moments = weighted_consensus_moment_profile(
        consensus, p_exponent, denominator
    )
    tail = weighted_consensus_tail_profile(
        consensus, thresholds, p_exponent, denominator
    )
    maximum_power = max(
        item["transport_power_sum_twice_units"] for item in consensus
    )
    maximum_ids = sorted(
        item["source_id"]
        for item in consensus
        if item["transport_power_sum_twice_units"] == maximum_power
    )
    return {
        "functionals": functionals,
        "dispersion": dispersion,
        "minimizers": minimizers,
        "representative": representative,
        "consensus": consensus,
        "moments": moments,
        "tail": tail,
        "maximum_power": maximum_power,
        "maximum_ids": maximum_ids,
    }


def build(**overrides):
    sources = sorted(
        overrides.pop("source_diagram_family", source_family()),
        key=lambda item: item["source_id"],
    )
    candidates = sorted(
        overrides.pop("barycenter_candidates", candidate_set()),
        key=lambda item: item["candidate_id"],
    )
    p_exponent = overrides.pop("p_exponent", 2)
    denominator = overrides.pop("functional_denominator", 4)
    thresholds = overrides.pop("consensus_tail_thresholds_twice", [1, 2, 3])
    reference_p = p_exponent if 1 <= p_exponent <= 4 else 2
    claims = reference_claims(
        sources, candidates, reference_p, denominator if denominator > 0 else 1, thresholds
    )
    functionals = overrides.pop("claimed_candidate_functionals", claims["functionals"])
    minimizers = overrides.pop("claimed_minimizer_candidate_ids", claims["minimizers"])
    representative = overrides.pop(
        "claimed_representative_candidate_id", claims["representative"]
    )
    consensus = overrides.pop(
        "claimed_consensus_source_transports", claims["consensus"]
    )
    dispersion = overrides.pop(
        "claimed_dispersion_numerator_twice_power_units", claims["dispersion"]
    )
    maximum_power = overrides.pop(
        "claimed_maximum_source_transport_power_twice_units", claims["maximum_power"]
    )
    maximum_ids = overrides.pop("claimed_maximum_source_ids", claims["maximum_ids"])
    moments = overrides.pop("claimed_weighted_moment_profile", claims["moments"])
    tail = overrides.pop("claimed_consensus_tail_profile", claims["tail"])
    digest = overrides.pop(
        "frechet_barycenter_dispersion_input_digest",
        compute_frechet_barycenter_dispersion_input_digest(
            source_diagram_family=sources,
            barycenter_candidates=candidates,
            p_exponent=p_exponent,
            functional_denominator=denominator,
            consensus_tail_thresholds_twice=thresholds,
            claimed_candidate_functionals=functionals,
            claimed_minimizer_candidate_ids=minimizers,
            claimed_representative_candidate_id=representative,
            claimed_consensus_source_transports=consensus,
            claimed_dispersion_numerator_twice_power_units=dispersion,
            claimed_maximum_source_transport_power_twice_units=maximum_power,
            claimed_maximum_source_ids=maximum_ids,
            claimed_weighted_moment_profile=moments,
            claimed_consensus_tail_profile=tail,
        ),
    )
    args = {
        "frechet_barycenter_dispersion_input_digest": digest,
        "source_diagram_family": sources,
        "barycenter_candidates": candidates,
        "p_exponent": p_exponent,
        "functional_denominator": denominator,
        "consensus_tail_thresholds_twice": thresholds,
        "claimed_candidate_functionals": functionals,
        "claimed_minimizer_candidate_ids": minimizers,
        "claimed_representative_candidate_id": representative,
        "claimed_consensus_source_transports": consensus,
        "claimed_dispersion_numerator_twice_power_units": dispersion,
        "claimed_maximum_source_transport_power_twice_units": maximum_power,
        "claimed_maximum_source_ids": maximum_ids,
        "claimed_weighted_moment_profile": moments,
        "claimed_consensus_tail_profile": tail,
        "maximum_p_exponent": 4,
        "maximum_coordinate_value": 10,
        "maximum_source_count": 8,
        "maximum_candidate_count": 8,
        "maximum_interval_count_per_diagram": 8,
        "maximum_tail_threshold_count": 5,
    }
    args.update(overrides)
    return build_finite_wasserstein_frechet_barycenter_dispersion_certificate(**args)


def main() -> int:
    result = build()
    assert result.status == STATUS_READY and result.certificate is not None
    cert = result.certificate
    assert cert["planos_version"] == "v1.20"
    assert cert["candidate_functionals"] == [
        {
            "candidate_id": "candidate-center",
            "functional_numerator_twice_power_units": 32,
            "functional_denominator": 4,
            "source_transport_power_sums": [
                {"source_id": "source-A", "transport_power_sum_twice_units": 12},
                {"source_id": "source-B", "transport_power_sum_twice_units": 4},
                {"source_id": "source-C", "transport_power_sum_twice_units": 12},
            ],
        },
        {
            "candidate_id": "candidate-left",
            "functional_numerator_twice_power_units": 72,
            "functional_denominator": 4,
            "source_transport_power_sums": [
                {"source_id": "source-A", "transport_power_sum_twice_units": 0},
                {"source_id": "source-B", "transport_power_sum_twice_units": 16},
                {"source_id": "source-C", "transport_power_sum_twice_units": 40},
            ],
        },
        {
            "candidate_id": "candidate-right",
            "functional_numerator_twice_power_units": 72,
            "functional_denominator": 4,
            "source_transport_power_sums": [
                {"source_id": "source-A", "transport_power_sum_twice_units": 40},
                {"source_id": "source-B", "transport_power_sum_twice_units": 16},
                {"source_id": "source-C", "transport_power_sum_twice_units": 0},
            ],
        },
    ]
    assert cert["minimum_functional_numerator_twice_power_units"] == 32
    assert cert["minimum_functional_reduced"] == {"numerator": 8, "denominator": 1}
    assert cert["minimizer_candidate_ids"] == ["candidate-center"]
    assert cert["minimizer_count"] == 1
    assert cert["finite_candidate_minimizer_unique"] is True
    assert cert["representative_candidate_id"] == "candidate-center"
    assert cert["dispersion_numerator_twice_power_units"] == 32
    assert cert["dispersion_denominator"] == 4
    assert cert["maximum_source_transport_power_twice_units"] == 12
    assert cert["maximum_source_ids"] == ["source-A", "source-C"]
    assert cert["weighted_moment_profile"] == [
        {
            "order": 1,
            "weighted_power_sum_numerator": 16,
            "functional_denominator": 4,
        },
        {
            "order": 2,
            "weighted_power_sum_numerator": 32,
            "functional_denominator": 4,
        },
    ]
    assert cert["consensus_tail_profile"] == [
        {
            "threshold_twice": 1,
            "weighted_count_numerator": 8,
            "unweighted_count": 7,
            "p_power_lower_bound_numerator": 8,
            "functional_denominator": 4,
        },
        {
            "threshold_twice": 2,
            "weighted_count_numerator": 8,
            "unweighted_count": 7,
            "p_power_lower_bound_numerator": 32,
            "functional_denominator": 4,
        },
        {
            "threshold_twice": 3,
            "weighted_count_numerator": 0,
            "unweighted_count": 0,
            "p_power_lower_bound_numerator": 0,
            "functional_denominator": 4,
        },
    ]
    assert cert["consensus_matching_count"] == 10
    source_b = next(
        item
        for item in cert["consensus_source_transports"]
        if item["source_id"] == "source-B"
    )
    assert source_b["weighted_contribution_numerator"] == 8
    assert sum(
        1 for item in source_b["matching"] if item["match_kind"] != "point_to_point"
    ) == 1

    for name in (
        "source_certificate_digests_bound",
        "candidate_diagram_digests_recomputed",
        "candidate_functionals_recomputed",
        "finite_minimizer_witness_recomputed",
        "minimizer_tie_set_recomputed",
        "lexical_representative_recomputed",
        "consensus_transports_recomputed",
        "source_contributions_sum_to_dispersion",
        "maximum_source_deviation_recomputed",
        "weighted_moment_profile_recomputed",
        "consensus_tail_profile_recomputed",
        "weighted_consensus_tail_bounds_verified",
        "zero_dispersion_implies_zero_source_contributions",
        "finite_diagram_family_only",
        "finite_candidate_barycenter_set_only",
        "bounded_positive_integer_p_only",
        "exact_rational_weights_only",
        "global_wasserstein_barycenter_not_claimed",
        "global_barycenter_existence_not_claimed",
        "global_barycenter_uniqueness_not_claimed",
        "finite_candidate_uniqueness_only_when_tie_set_singleton",
        "frechet_minimizer_does_not_rank_plans",
        "consensus_diagram_is_not_selected_plan",
        "low_dispersion_grants_no_activation_authorization",
        "high_dispersion_does_not_automatically_reject",
        "diagonal_consensus_grants_no_deletion_authority",
        "finite_diagram_family_is_not_planning_population",
        "source_v1_17_certificates_not_mutated",
        "source_v1_18_certificates_not_mutated",
        "source_v1_19_certificates_not_mutated",
        "persistent_world_state_unchanged",
        "history_read_only",
        "future_only",
    ):
        assert cert[name] is True
    assert cert["candidate_selection_performed"] is False
    assert cert["candidate_ranking_performed"] is False
    assert cert["activation_performed"] is False
    assert cert["active_now"] is False
    assert cert["execution_permission"] is False

    tie_candidates = candidate_set() + [
        candidate_record("candidate-center-z", diagram_center("Z"))
    ]
    tie = build(barycenter_candidates=tie_candidates)
    assert tie.status == STATUS_READY and tie.certificate is not None
    assert tie.certificate["minimizer_candidate_ids"] == [
        "candidate-center",
        "candidate-center-z",
    ]
    assert tie.certificate["minimizer_count"] == 2
    assert tie.certificate["finite_candidate_minimizer_unique"] is False
    assert tie.certificate["representative_candidate_id"] == "candidate-center"

    blocked = [
        build(frechet_barycenter_dispersion_input_digest="stale"),
        build(p_exponent=0),
        build(p_exponent=5),
        build(functional_denominator=5),
        build(claimed_dispersion_numerator_twice_power_units=31),
        build(claimed_representative_candidate_id="candidate-left"),
        build(claimed_maximum_source_ids=["source-A"]),
        build(consensus_tail_thresholds_twice=[2, 1]),
        build(maximum_source_count=2),
        build(maximum_candidate_count=2),
        build(maximum_interval_count_per_diagram=2),
        build(maximum_tail_threshold_count=2),
    ]

    missing_digest_sources = source_family()
    missing_digest_sources[0]["source_p_wasserstein_transport_certificate_digest"] = ""
    blocked.append(build(source_diagram_family=missing_digest_sources))

    bad_candidate_digest = candidate_set()
    bad_candidate_digest[0]["candidate_diagram_digest"] = "tampered"
    blocked.append(build(barycenter_candidates=bad_candidate_digest))

    duplicate_candidate = candidate_set()
    duplicate_candidate[1]["candidate_id"] = duplicate_candidate[0]["candidate_id"]
    blocked.append(build(barycenter_candidates=duplicate_candidate))

    wrong_functionals = deepcopy(
        reference_claims(source_family(), candidate_set(), 2, 4, [1, 2, 3])[
            "functionals"
        ]
    )
    wrong_functionals[0]["functional_numerator_twice_power_units"] = 31
    blocked.append(build(claimed_candidate_functionals=wrong_functionals))

    wrong_moments = deepcopy(
        reference_claims(source_family(), candidate_set(), 2, 4, [1, 2, 3])[
            "moments"
        ]
    )
    wrong_moments[-1]["weighted_power_sum_numerator"] = 31
    blocked.append(build(claimed_weighted_moment_profile=wrong_moments))

    wrong_tail = deepcopy(
        reference_claims(source_family(), candidate_set(), 2, 4, [1, 2, 3])[
            "tail"
        ]
    )
    wrong_tail[1]["weighted_count_numerator"] = 7
    blocked.append(build(claimed_consensus_tail_profile=wrong_tail))

    for item in blocked:
        assert item.status != STATUS_READY
        assert item.blockers
        assert item.certificate is None

    print(
        "PASS: PlanOS Finite Wasserstein Frechet Barycenter and Dispersion Certificate Kernel v0.1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
