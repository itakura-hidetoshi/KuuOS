from __future__ import annotations

from math import gcd

from runtime.kuuos_planos_finite_p_wasserstein_persistence_transport_algebra_support_v0_1 import (
    integer_nth_root_bounds,
    optimal_p_wasserstein_transport,
)


def evaluate_barycenter_candidate(
    source_diagram_family: list[dict],
    candidate: dict,
    p_exponent: int,
    functional_denominator: int,
):
    source_powers: list[dict] = []
    numerator = 0
    for source in source_diagram_family:
        power, _, _ = optimal_p_wasserstein_transport(
            source["diagram_intervals"], candidate["diagram_intervals"], p_exponent
        )
        source_powers.append(
            {
                "source_id": source["source_id"],
                "transport_power_sum_twice_units": power,
            }
        )
        numerator += source["weight_numerator"] * power
    return {
        "candidate_id": candidate["candidate_id"],
        "functional_numerator_twice_power_units": numerator,
        "functional_denominator": functional_denominator,
        "source_transport_power_sums": source_powers,
    }


def candidate_functional_table(
    source_diagram_family: list[dict],
    barycenter_candidates: list[dict],
    p_exponent: int,
    functional_denominator: int,
):
    return [
        evaluate_barycenter_candidate(
            source_diagram_family,
            candidate,
            p_exponent,
            functional_denominator,
        )
        for candidate in sorted(
            barycenter_candidates, key=lambda item: item["candidate_id"]
        )
    ]


def finite_frechet_minimizers(candidate_functionals: list[dict]):
    if not candidate_functionals:
        raise ValueError("finite_candidate_functional_table_empty")
    minimum = min(
        item["functional_numerator_twice_power_units"]
        for item in candidate_functionals
    )
    minimizers = sorted(
        item["candidate_id"]
        for item in candidate_functionals
        if item["functional_numerator_twice_power_units"] == minimum
    )
    return minimum, minimizers, minimizers[0]


def consensus_source_transports(
    source_diagram_family: list[dict],
    representative_candidate: dict,
    p_exponent: int,
):
    output: list[dict] = []
    for source in source_diagram_family:
        total, maximum, matching = optimal_p_wasserstein_transport(
            source["diagram_intervals"],
            representative_candidate["diagram_intervals"],
            p_exponent,
        )
        root_floor, root_ceil = integer_nth_root_bounds(total, p_exponent)
        dimension_profile = [
            {
                "dimension": dimension,
                "power_sum_twice_units": sum(
                    item["cost_power"]
                    for item in matching
                    if item["dimension"] == dimension
                ),
            }
            for dimension in range(3)
        ]
        output.append(
            {
                "source_id": source["source_id"],
                "weight_numerator": source["weight_numerator"],
                "transport_power_sum_twice_units": total,
                "weighted_contribution_numerator": source["weight_numerator"]
                * total,
                "transport_maximum_cost_twice": maximum,
                "root_floor_twice": root_floor,
                "root_ceil_twice": root_ceil,
                "matching": matching,
                "dimension_power_profile": dimension_profile,
            }
        )
    return sorted(output, key=lambda item: item["source_id"])


def weighted_consensus_moment_profile(
    consensus_transports: list[dict],
    maximum_order: int,
    functional_denominator: int,
):
    return [
        {
            "order": order,
            "weighted_power_sum_numerator": sum(
                source["weight_numerator"]
                * sum(item["cost_twice"] ** order for item in source["matching"])
                for source in consensus_transports
            ),
            "functional_denominator": functional_denominator,
        }
        for order in range(1, maximum_order + 1)
    ]


def weighted_consensus_tail_profile(
    consensus_transports: list[dict],
    thresholds_twice: list[int],
    p_exponent: int,
    functional_denominator: int,
):
    output: list[dict] = []
    for threshold in thresholds_twice:
        weighted_count = sum(
            source["weight_numerator"]
            * sum(
                1
                for item in source["matching"]
                if item["cost_twice"] >= threshold
            )
            for source in consensus_transports
        )
        unweighted_count = sum(
            1
            for source in consensus_transports
            for item in source["matching"]
            if item["cost_twice"] >= threshold
        )
        output.append(
            {
                "threshold_twice": threshold,
                "weighted_count_numerator": weighted_count,
                "unweighted_count": unweighted_count,
                "p_power_lower_bound_numerator": weighted_count
                * threshold ** p_exponent,
                "functional_denominator": functional_denominator,
            }
        )
    return output


def reduced_fraction(numerator: int, denominator: int):
    if denominator <= 0:
        raise ValueError("functional_denominator_must_be_positive")
    common = gcd(numerator, denominator)
    return {"numerator": numerator // common, "denominator": denominator // common}


__all__ = [
    "candidate_functional_table",
    "consensus_source_transports",
    "evaluate_barycenter_candidate",
    "finite_frechet_minimizers",
    "integer_nth_root_bounds",
    "optimal_p_wasserstein_transport",
    "reduced_fraction",
    "weighted_consensus_moment_profile",
    "weighted_consensus_tail_profile",
]
