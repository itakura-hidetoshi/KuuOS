from __future__ import annotations

from typing import Any

from runtime.kuuos_planos_finite_bottleneck_persistence_stability_schema_support_v0_1 import (
    canonical_digest,
    normalize_diagram_intervals,
    normalize_perturbation_records,
)


def _nat(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _positive_nat(value: Any) -> bool:
    return _nat(value) and value > 0


def _unique_text(value: Any, seen: set[str], invalid: str, duplicate: str):
    if not isinstance(value, str) or not value:
        return False, invalid
    if value in seen:
        return False, duplicate
    seen.add(value)
    return True, ""


def normalize_transport_matching_claims(values: Any, p_exponent: int):
    if not isinstance(values, list) or not values:
        return ["claimed_optimal_transport_matching_empty"], []
    fields = {
        "match_id",
        "dimension",
        "match_kind",
        "left_interval_id",
        "right_interval_id",
        "cost_twice",
        "cost_power",
    }
    allowed = {"point_to_point", "left_to_diagonal", "diagonal_to_right"}
    blockers, out, ids = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"transport_matching_claim_schema_invalid_{index}")
            continue
        match_id = item["match_id"]
        ok, reason = _unique_text(
            match_id,
            ids,
            f"transport_matching_claim_id_invalid_{index}",
            "duplicate_transport_matching_claim_id",
        )
        if not ok:
            blockers.append(reason)
            continue
        dimension = item["dimension"]
        kind = item["match_kind"]
        left = item["left_interval_id"]
        right = item["right_interval_id"]
        cost = item["cost_twice"]
        cost_power = item["cost_power"]
        if (
            not _nat(dimension)
            or dimension > 2
            or kind not in allowed
            or not _nat(cost)
            or not _nat(cost_power)
        ):
            blockers.append(f"transport_matching_claim_numeric_or_kind_invalid_{match_id}")
            continue
        if not isinstance(left, str) or not isinstance(right, str):
            blockers.append(f"transport_matching_claim_interval_ids_invalid_{match_id}")
            continue
        valid_binding = (
            (kind == "point_to_point" and bool(left) and bool(right))
            or (kind == "left_to_diagonal" and bool(left) and not right)
            or (kind == "diagonal_to_right" and not left and bool(right))
        )
        if not valid_binding:
            blockers.append(f"transport_matching_claim_binding_invalid_{match_id}")
            continue
        if _positive_nat(p_exponent) and cost_power != cost ** p_exponent:
            blockers.append(f"transport_matching_claim_cost_power_mismatch_{match_id}")
            continue
        out.append(dict(item))
    return blockers, sorted(out, key=lambda item: item["match_id"])


def normalize_moment_claims(values: Any, maximum_order: int):
    if not isinstance(values, list) or not values:
        return ["claimed_cost_moment_profile_empty"], []
    fields = {"order", "power_sum_twice_units"}
    blockers, out, seen = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"cost_moment_claim_schema_invalid_{index}")
            continue
        order = item["order"]
        value = item["power_sum_twice_units"]
        if not _positive_nat(order) or order > maximum_order or not _nat(value):
            blockers.append(f"cost_moment_claim_numeric_invalid_{index}")
            continue
        if order in seen:
            blockers.append("duplicate_cost_moment_order")
        seen.add(order)
        out.append({"order": order, "power_sum_twice_units": value})
    return blockers, sorted(out, key=lambda item: item["order"])


def normalize_tail_thresholds(values: Any, maximum_threshold_twice: int):
    if (
        not isinstance(values, list)
        or not values
        or any(not _positive_nat(value) or value > maximum_threshold_twice for value in values)
        or values != sorted(set(values))
    ):
        return ["tail_thresholds_twice_invalid"], []
    return [], list(values)


def normalize_tail_claims(values: Any):
    if not isinstance(values, list) or not values:
        return ["claimed_tail_profile_empty"], []
    fields = {
        "threshold_twice",
        "count_at_or_above",
        "p_power_lower_bound",
    }
    blockers, out, seen = [], [], set()
    for index, item in enumerate(values):
        if not isinstance(item, dict) or set(item) != fields:
            blockers.append(f"tail_claim_schema_invalid_{index}")
            continue
        threshold = item["threshold_twice"]
        count = item["count_at_or_above"]
        lower = item["p_power_lower_bound"]
        if not _positive_nat(threshold) or not _nat(count) or not _nat(lower):
            blockers.append(f"tail_claim_numeric_invalid_{index}")
            continue
        if threshold in seen:
            blockers.append("duplicate_tail_threshold")
        seen.add(threshold)
        out.append(
            {
                "threshold_twice": threshold,
                "count_at_or_above": count,
                "p_power_lower_bound": lower,
            }
        )
    return blockers, sorted(out, key=lambda item: item["threshold_twice"])


def compute_p_wasserstein_transport_input_digest(**payload):
    return canonical_digest(payload)
