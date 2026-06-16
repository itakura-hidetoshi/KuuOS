from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.context_math_v013 import HORIZONS, distance, normalize, transport


def bounded(value: Any) -> float:
    try:
        return round(max(0.0, min(1.0, float(value))), 6)
    except (TypeError, ValueError):
        return 0.0


def bounded_min(values: Sequence[Any]) -> float:
    normalized = [bounded(value) for value in values]
    return min(normalized, default=0.0)


def triple_overlap(source_pair_overlap: Any, left_target_overlap: Any, right_target_overlap: Any) -> float:
    return bounded_min((source_pair_overlap, left_target_overlap, right_target_overlap))


def quadruple_overlap(first_second_overlap: Any, first_third_overlap: Any, first_target_overlap: Any, second_third_overlap: Any, second_target_overlap: Any, third_target_overlap: Any) -> float:
    return bounded_min((first_second_overlap, first_third_overlap, first_target_overlap, second_third_overlap, second_target_overlap, third_target_overlap))


def sequential_transport(section: Mapping[str, float], phases: Sequence[Mapping[str, float]], floor: float) -> dict[str, float]:
    current = normalize({horizon: float(section.get(horizon, 0.0)) for horizon in HORIZONS}, floor)
    for phase in phases:
        current = transport(current, phase, floor)
    return current


def postcomposition_residue(direct_section: Mapping[str, float], composite_phases: Sequence[Mapping[str, float]], floor: float) -> tuple[dict[str, float], dict[str, float], float]:
    direct = sequential_transport(direct_section, (), floor)
    composite = sequential_transport(direct, composite_phases, floor)
    return direct, composite, bounded(distance(direct, composite))


def order_residue(direct_section: Mapping[str, float], left_phases: Sequence[Mapping[str, float]], right_phases: Sequence[Mapping[str, float]], floor: float) -> tuple[dict[str, float], dict[str, float], float]:
    left = sequential_transport(direct_section, left_phases, floor)
    right = sequential_transport(direct_section, right_phases, floor)
    return left, right, bounded(distance(left, right))
