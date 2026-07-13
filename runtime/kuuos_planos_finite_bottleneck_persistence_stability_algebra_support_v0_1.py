from __future__ import annotations

from functools import lru_cache

_KIND_RANK = {
    "point_to_point": 0,
    "left_to_diagonal": 1,
    "diagonal_to_right": 2,
}


def interval_point_cost_twice(left: dict, right: dict):
    if left["dimension"] != right["dimension"]:
        return None
    death_left, death_right = left["death"], right["death"]
    if death_left is None and death_right is None:
        return 2 * abs(left["birth"] - right["birth"])
    if (death_left is None) != (death_right is None):
        return None
    return 2 * max(
        abs(left["birth"] - right["birth"]),
        abs(death_left - death_right),
    )


def interval_diagonal_cost_twice(interval: dict):
    if interval["death"] is None:
        return None
    return interval["death"] - interval["birth"]


def validate_interval_endpoint_bindings(intervals, perturbation_records, side: str):
    blockers: list[str] = []
    by_id = {item["simplex_id"]: item for item in perturbation_records}
    filtration_key = f"filtration_{side}"
    for interval in intervals:
        birth = by_id.get(interval["birth_simplex_id"])
        if birth is None:
            blockers.append(f"diagram_{side}_birth_simplex_missing_{interval['interval_id']}")
        elif birth["dimension"] != interval["dimension"]:
            blockers.append(
                f"diagram_{side}_birth_simplex_dimension_mismatch_{interval['interval_id']}"
            )
        elif birth[filtration_key] != interval["birth"]:
            blockers.append(
                f"diagram_{side}_birth_filtration_mismatch_{interval['interval_id']}"
            )
        if interval["death"] is None:
            continue
        death = by_id.get(interval["death_simplex_id"])
        if death is None:
            blockers.append(f"diagram_{side}_death_simplex_missing_{interval['interval_id']}")
        elif death["dimension"] != interval["dimension"] + 1:
            blockers.append(
                f"diagram_{side}_death_simplex_dimension_mismatch_{interval['interval_id']}"
            )
        elif death[filtration_key] != interval["death"]:
            blockers.append(
                f"diagram_{side}_death_filtration_mismatch_{interval['interval_id']}"
            )
    return blockers


def filtration_sup_norm(records):
    return max(abs(item["filtration_a"] - item["filtration_b"]) for item in records)


def _action_key(actions):
    return tuple(
        (_KIND_RANK[kind], left_id, right_id, cost)
        for kind, left_id, right_id, cost in actions
    )


def _optimal_dimension_matching(left_intervals, right_intervals):
    left = tuple(sorted(left_intervals, key=lambda item: item["interval_id"]))
    right = tuple(sorted(right_intervals, key=lambda item: item["interval_id"]))
    left_count, right_count = len(left), len(right)

    @lru_cache(maxsize=None)
    def solve(left_index: int, used_right_mask: int):
        if left_index == left_count:
            actions = []
            bottleneck = 0
            for right_index, interval in enumerate(right):
                if (used_right_mask >> right_index) & 1:
                    continue
                cost = interval_diagonal_cost_twice(interval)
                if cost is None:
                    return None
                actions.append(("diagonal_to_right", "", interval["interval_id"], cost))
                bottleneck = max(bottleneck, cost)
            return bottleneck, tuple(actions)

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
            ) + tail[1]
            candidates.append((max(cost, tail[0]), actions))

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
                ) + tail[1]
                candidates.append((max(diagonal_cost, tail[0]), actions))

        if not candidates:
            return None
        return min(candidates, key=lambda item: (item[0], _action_key(item[1])))

    return solve(0, 0)


def optimal_bottleneck_matching(diagram_a, diagram_b):
    actions = []
    bottleneck = 0
    for dimension in range(3):
        result = _optimal_dimension_matching(
            [item for item in diagram_a if item["dimension"] == dimension],
            [item for item in diagram_b if item["dimension"] == dimension],
        )
        if result is None:
            raise ValueError(f"no_finite_bottleneck_matching_dimension_{dimension}")
        bottleneck = max(bottleneck, result[0])
        actions.extend((dimension, *action) for action in result[1])
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
        }
        for index, (dimension, kind, left_id, right_id, cost) in enumerate(
            actions, start=1
        )
    ]
    return bottleneck, matching
