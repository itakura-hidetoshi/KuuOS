from __future__ import annotations

from functools import lru_cache

from runtime.kuuos_planos_finite_bottleneck_persistence_stability_algebra_support_v0_1 import (
    filtration_sup_norm,
    interval_diagonal_cost_twice,
    interval_point_cost_twice,
    optimal_bottleneck_matching,
    validate_interval_endpoint_bindings,
)

_KIND_RANK = {
    "point_to_point": 0,
    "left_to_diagonal": 1,
    "diagonal_to_right": 2,
}


def _action_key(actions):
    return tuple(
        (_KIND_RANK[kind], left_id, right_id, cost)
        for kind, left_id, right_id, cost in actions
    )


def _optimal_dimension_transport(left_intervals, right_intervals, p_exponent: int):
    left = tuple(sorted(left_intervals, key=lambda item: item["interval_id"]))
    right = tuple(sorted(right_intervals, key=lambda item: item["interval_id"]))
    left_count = len(left)

    @lru_cache(maxsize=None)
    def solve(left_index: int, used_right_mask: int):
        if left_index == left_count:
            actions = []
            total_power = 0
            maximum_cost = 0
            for right_index, interval in enumerate(right):
                if (used_right_mask >> right_index) & 1:
                    continue
                cost = interval_diagonal_cost_twice(interval)
                if cost is None:
                    return None
                actions.append(("diagonal_to_right", "", interval["interval_id"], cost))
                total_power += cost ** p_exponent
                maximum_cost = max(maximum_cost, cost)
            return total_power, maximum_cost, tuple(actions)

        current = left[left_index]
        candidates = []
        for right_index, target in enumerate(right):
            if (used_right_mask >> right_index) & 1:
                continue
            cost = interval_point_cost_twice(current, target)
            if cost is None:
                continue
            tail = solve(left_index + 1, used_right_mask | (1 << right_index))
            if tail is None:
                continue
            actions = (
                (
                    "point_to_point",
                    current["interval_id"],
                    target["interval_id"],
                    cost,
                ),
            ) + tail[2]
            candidates.append(
                (
                    cost ** p_exponent + tail[0],
                    max(cost, tail[1]),
                    actions,
                )
            )

        diagonal_cost = interval_diagonal_cost_twice(current)
        if diagonal_cost is not None:
            tail = solve(left_index + 1, used_right_mask)
            if tail is not None:
                actions = (
                    (
                        "left_to_diagonal",
                        current["interval_id"],
                        "",
                        diagonal_cost,
                    ),
                ) + tail[2]
                candidates.append(
                    (
                        diagonal_cost ** p_exponent + tail[0],
                        max(diagonal_cost, tail[1]),
                        actions,
                    )
                )

        if not candidates:
            return None
        return min(
            candidates,
            key=lambda item: (item[0], item[1], _action_key(item[2])),
        )

    return solve(0, 0)


def optimal_p_wasserstein_transport(diagram_a, diagram_b, p_exponent: int):
    actions = []
    total_power = 0
    maximum_cost = 0
    for dimension in range(3):
        result = _optimal_dimension_transport(
            [item for item in diagram_a if item["dimension"] == dimension],
            [item for item in diagram_b if item["dimension"] == dimension],
            p_exponent,
        )
        if result is None:
            raise ValueError(f"no_finite_p_wasserstein_matching_dimension_{dimension}")
        total_power += result[0]
        maximum_cost = max(maximum_cost, result[1])
        actions.extend((dimension, *action) for action in result[2])

    actions.sort(
        key=lambda item: (
            item[0],
            _KIND_RANK[item[1]],
            item[2],
            item[3],
            item[4],
        )
    )
    matching = [
        {
            "match_id": f"match-{index:03d}",
            "dimension": dimension,
            "match_kind": kind,
            "left_interval_id": left_id,
            "right_interval_id": right_id,
            "cost_twice": cost,
            "cost_power": cost ** p_exponent,
        }
        for index, (dimension, kind, left_id, right_id, cost) in enumerate(
            actions, start=1
        )
    ]
    return total_power, maximum_cost, matching


def integer_nth_root_bounds(value: int, exponent: int):
    if value < 0 or exponent <= 0:
        raise ValueError("integer_nth_root_domain_invalid")
    if value in (0, 1) or exponent == 1:
        return value, value
    low, high = 0, 1
    while high ** exponent < value:
        high *= 2
    if high ** exponent == value:
        return high, high
    while low + 1 < high:
        middle = (low + high) // 2
        if middle ** exponent <= value:
            low = middle
        else:
            high = middle
    if low ** exponent == value:
        return low, low
    return low, high


def cost_moment_profile(matching, maximum_order: int):
    return [
        {
            "order": order,
            "power_sum_twice_units": sum(
                item["cost_twice"] ** order for item in matching
            ),
        }
        for order in range(1, maximum_order + 1)
    ]


def tail_profile(matching, thresholds_twice, p_exponent: int):
    output = []
    for threshold in thresholds_twice:
        count = sum(1 for item in matching if item["cost_twice"] >= threshold)
        output.append(
            {
                "threshold_twice": threshold,
                "count_at_or_above": count,
                "p_power_lower_bound": count * (threshold ** p_exponent),
            }
        )
    return output


__all__ = [
    "cost_moment_profile",
    "filtration_sup_norm",
    "integer_nth_root_bounds",
    "optimal_bottleneck_matching",
    "optimal_p_wasserstein_transport",
    "tail_profile",
    "validate_interval_endpoint_bindings",
]
