from __future__ import annotations

from typing import Any

from runtime.kuuos_planos_finite_p_wasserstein_persistence_transport_schema_support_v0_1 import (
    canonical_digest,
    normalize_diagram_intervals,
    normalize_transport_matching_claims,
)


def _nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _positive_nat(value: Any) -> bool:
    return _nat(value) and value > 0


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _unique_text(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not _nonempty_text(value):
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def normalize_source_diagram_family(
    values: Any,
    maximum_coordinate_value: int,
    maximum_source_count: int,
    maximum_interval_count_per_diagram: int,
):
    if not isinstance(values, list) or not values:
        return ["source_diagram_family_empty"], []
    if len(values) > maximum_source_count:
        return ["maximum_source_count_exceeded"], []
    fields = {
        "source_id",
        "weight_numerator",
        "source_persistent_homology_certificate_digest",
        "source_bottleneck_stability_certificate_digest",
        "source_p_wasserstein_transport_certificate_digest",
        "diagram_intervals",
    }
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"source_diagram_schema_invalid_{index}")
            continue
        source_id = item["source_id"]
        ok, reason = _unique_text(
            source_id,
            seen,
            f"source_id_invalid_{index}",
            "duplicate_source_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        if not _positive_nat(item["weight_numerator"]):
            blockers.append(f"source_weight_numerator_invalid_{source_id}")
        for digest_field in (
            "source_persistent_homology_certificate_digest",
            "source_bottleneck_stability_certificate_digest",
            "source_p_wasserstein_transport_certificate_digest",
        ):
            if not _nonempty_text(item[digest_field]):
                blockers.append(f"{digest_field}_missing_{source_id}")
        interval_errors, intervals = normalize_diagram_intervals(
            item["diagram_intervals"], source_id, maximum_coordinate_value
        )
        blockers.extend(interval_errors)
        if len(intervals) > maximum_interval_count_per_diagram:
            blockers.append(f"maximum_interval_count_per_diagram_exceeded_{source_id}")
        output.append(
            {
                "source_id": source_id,
                "weight_numerator": item["weight_numerator"],
                "source_persistent_homology_certificate_digest": item[
                    "source_persistent_homology_certificate_digest"
                ],
                "source_bottleneck_stability_certificate_digest": item[
                    "source_bottleneck_stability_certificate_digest"
                ],
                "source_p_wasserstein_transport_certificate_digest": item[
                    "source_p_wasserstein_transport_certificate_digest"
                ],
                "diagram_intervals": intervals,
            }
        )
    return blockers, sorted(output, key=lambda item: item["source_id"])


def candidate_diagram_digest(candidate_id: str, diagram_intervals: list[dict]) -> str:
    return canonical_digest(
        {"candidate_id": candidate_id, "diagram_intervals": diagram_intervals}
    )


def normalize_barycenter_candidates(
    values: Any,
    maximum_coordinate_value: int,
    maximum_candidate_count: int,
    maximum_interval_count_per_diagram: int,
):
    if not isinstance(values, list) or not values:
        return ["barycenter_candidate_set_empty"], []
    if len(values) > maximum_candidate_count:
        return ["maximum_candidate_count_exceeded"], []
    fields = {"candidate_id", "candidate_diagram_digest", "diagram_intervals"}
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"barycenter_candidate_schema_invalid_{index}")
            continue
        candidate_id = item["candidate_id"]
        ok, reason = _unique_text(
            candidate_id,
            seen,
            f"candidate_id_invalid_{index}",
            "duplicate_candidate_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        if not _nonempty_text(item["candidate_diagram_digest"]):
            blockers.append(f"candidate_diagram_digest_missing_{candidate_id}")
        interval_errors, intervals = normalize_diagram_intervals(
            item["diagram_intervals"], candidate_id, maximum_coordinate_value
        )
        blockers.extend(interval_errors)
        if len(intervals) > maximum_interval_count_per_diagram:
            blockers.append(f"maximum_interval_count_per_diagram_exceeded_{candidate_id}")
        expected_digest = candidate_diagram_digest(candidate_id, intervals)
        if item["candidate_diagram_digest"] != expected_digest:
            blockers.append(f"candidate_diagram_digest_mismatch_{candidate_id}")
        output.append(
            {
                "candidate_id": candidate_id,
                "candidate_diagram_digest": item["candidate_diagram_digest"],
                "diagram_intervals": intervals,
            }
        )
    return blockers, sorted(output, key=lambda item: item["candidate_id"])


def normalize_candidate_functional_claims(values: Any):
    if not isinstance(values, list) or not values:
        return ["claimed_candidate_functionals_empty"], []
    fields = {
        "candidate_id",
        "functional_numerator_twice_power_units",
        "functional_denominator",
        "source_transport_power_sums",
    }
    source_fields = {"source_id", "transport_power_sum_twice_units"}
    blockers: list[str] = []
    output: list[dict] = []
    seen_candidates: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"candidate_functional_claim_schema_invalid_{index}")
            continue
        candidate_id = item["candidate_id"]
        ok, reason = _unique_text(
            candidate_id,
            seen_candidates,
            f"candidate_functional_id_invalid_{index}",
            "duplicate_candidate_functional_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        numerator = item["functional_numerator_twice_power_units"]
        denominator = item["functional_denominator"]
        if not _nat(numerator) or not _positive_nat(denominator):
            blockers.append(f"candidate_functional_numeric_invalid_{candidate_id}")
        source_values = item["source_transport_power_sums"]
        if not isinstance(source_values, list) or not source_values:
            blockers.append(f"candidate_source_transport_claims_empty_{candidate_id}")
            source_values = []
        source_output: list[dict] = []
        source_seen: set[str] = set()
        for source_index, source_item in enumerate(source_values):
            if not isinstance(source_item, dict) or set(source_item) != source_fields:
                blockers.append(
                    f"candidate_source_transport_claim_schema_invalid_{candidate_id}_{source_index}"
                )
                continue
            source_id = source_item["source_id"]
            ok, reason = _unique_text(
                source_id,
                source_seen,
                f"candidate_source_transport_source_id_invalid_{candidate_id}_{source_index}",
                f"duplicate_candidate_source_transport_source_id_{candidate_id}",
            )
            if not ok:
                blockers.append(reason)
                continue
            power = source_item["transport_power_sum_twice_units"]
            if not _nat(power):
                blockers.append(
                    f"candidate_source_transport_power_invalid_{candidate_id}_{source_id}"
                )
            source_output.append(
                {
                    "source_id": source_id,
                    "transport_power_sum_twice_units": power,
                }
            )
        output.append(
            {
                "candidate_id": candidate_id,
                "functional_numerator_twice_power_units": numerator,
                "functional_denominator": denominator,
                "source_transport_power_sums": sorted(
                    source_output, key=lambda value: value["source_id"]
                ),
            }
        )
    return blockers, sorted(output, key=lambda item: item["candidate_id"])


def normalize_consensus_source_claims(values: Any, p_exponent: int):
    if not isinstance(values, list) or not values:
        return ["claimed_consensus_source_transports_empty"], []
    fields = {
        "source_id",
        "weight_numerator",
        "transport_power_sum_twice_units",
        "weighted_contribution_numerator",
        "transport_maximum_cost_twice",
        "root_floor_twice",
        "root_ceil_twice",
        "matching",
        "dimension_power_profile",
    }
    dimension_fields = {"dimension", "power_sum_twice_units"}
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[str] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"consensus_source_claim_schema_invalid_{index}")
            continue
        source_id = item["source_id"]
        ok, reason = _unique_text(
            source_id,
            seen,
            f"consensus_source_id_invalid_{index}",
            "duplicate_consensus_source_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        for numeric_field in (
            "weight_numerator",
            "transport_power_sum_twice_units",
            "weighted_contribution_numerator",
            "transport_maximum_cost_twice",
            "root_floor_twice",
            "root_ceil_twice",
        ):
            value = item[numeric_field]
            valid = _positive_nat(value) if numeric_field == "weight_numerator" else _nat(value)
            if not valid:
                blockers.append(f"consensus_{numeric_field}_invalid_{source_id}")
        matching_errors, matching = normalize_transport_matching_claims(
            item["matching"], p_exponent
        )
        blockers.extend(matching_errors)
        dimension_values = item["dimension_power_profile"]
        if not isinstance(dimension_values, list):
            blockers.append(f"dimension_power_profile_invalid_{source_id}")
            dimension_values = []
        dimension_output: list[dict] = []
        dimension_seen: set[int] = set()
        for dimension_index, dimension_item in enumerate(dimension_values):
            if not isinstance(dimension_item, dict) or set(dimension_item) != dimension_fields:
                blockers.append(
                    f"dimension_power_claim_schema_invalid_{source_id}_{dimension_index}"
                )
                continue
            dimension = dimension_item["dimension"]
            power = dimension_item["power_sum_twice_units"]
            if not _nat(dimension) or dimension > 2 or not _nat(power):
                blockers.append(
                    f"dimension_power_claim_numeric_invalid_{source_id}_{dimension_index}"
                )
                continue
            if dimension in dimension_seen:
                blockers.append(f"duplicate_dimension_power_claim_{source_id}")
            dimension_seen.add(dimension)
            dimension_output.append(
                {"dimension": dimension, "power_sum_twice_units": power}
            )
        dimension_output.sort(key=lambda value: value["dimension"])
        if [value["dimension"] for value in dimension_output] != [0, 1, 2]:
            blockers.append(f"dimension_power_profile_must_cover_zero_through_two_{source_id}")
        output.append(
            {
                "source_id": source_id,
                "weight_numerator": item["weight_numerator"],
                "transport_power_sum_twice_units": item[
                    "transport_power_sum_twice_units"
                ],
                "weighted_contribution_numerator": item[
                    "weighted_contribution_numerator"
                ],
                "transport_maximum_cost_twice": item[
                    "transport_maximum_cost_twice"
                ],
                "root_floor_twice": item["root_floor_twice"],
                "root_ceil_twice": item["root_ceil_twice"],
                "matching": matching,
                "dimension_power_profile": dimension_output,
            }
        )
    return blockers, sorted(output, key=lambda item: item["source_id"])


def normalize_weighted_moment_claims(values: Any, maximum_order: int):
    if not isinstance(values, list) or not values:
        return ["claimed_weighted_moment_profile_empty"], []
    fields = {"order", "weighted_power_sum_numerator", "functional_denominator"}
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[int] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"weighted_moment_claim_schema_invalid_{index}")
            continue
        order = item["order"]
        numerator = item["weighted_power_sum_numerator"]
        denominator = item["functional_denominator"]
        if (
            not _positive_nat(order)
            or order > maximum_order
            or not _nat(numerator)
            or not _positive_nat(denominator)
        ):
            blockers.append(f"weighted_moment_claim_numeric_invalid_{index}")
            continue
        if order in seen:
            blockers.append("duplicate_weighted_moment_order")
        seen.add(order)
        output.append(
            {
                "order": order,
                "weighted_power_sum_numerator": numerator,
                "functional_denominator": denominator,
            }
        )
    return blockers, sorted(output, key=lambda item: item["order"])


def normalize_tail_thresholds(values: Any, maximum_threshold_twice: int):
    if (
        not isinstance(values, list)
        or not values
        or any(not _positive_nat(value) or value > maximum_threshold_twice for value in values)
        or values != sorted(set(values))
    ):
        return ["consensus_tail_thresholds_twice_invalid"], []
    return [], list(values)


def normalize_consensus_tail_claims(values: Any):
    if not isinstance(values, list) or not values:
        return ["claimed_consensus_tail_profile_empty"], []
    fields = {
        "threshold_twice",
        "weighted_count_numerator",
        "unweighted_count",
        "p_power_lower_bound_numerator",
        "functional_denominator",
    }
    blockers: list[str] = []
    output: list[dict] = []
    seen: set[int] = set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"consensus_tail_claim_schema_invalid_{index}")
            continue
        threshold = item["threshold_twice"]
        if (
            not _positive_nat(threshold)
            or not _nat(item["weighted_count_numerator"])
            or not _nat(item["unweighted_count"])
            or not _nat(item["p_power_lower_bound_numerator"])
            or not _positive_nat(item["functional_denominator"])
        ):
            blockers.append(f"consensus_tail_claim_numeric_invalid_{index}")
            continue
        if threshold in seen:
            blockers.append("duplicate_consensus_tail_threshold")
        seen.add(threshold)
        output.append(dict(item))
    return blockers, sorted(output, key=lambda item: item["threshold_twice"])


def compute_frechet_barycenter_dispersion_input_digest(**payload):
    return canonical_digest(payload)
