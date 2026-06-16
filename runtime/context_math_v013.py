from __future__ import annotations
from typing import Any, Mapping

HORIZONS = ("short", "medium", "long")


def _items(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    return {str(item) for item in value if str(item)}


def overlap(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    fields = ("source_kinds", "signal_kinds", "source_ids")
    scores = []
    for field in fields:
        a, b = _items(left.get(field)), _items(right.get(field))
        scores.append(1.0 if not a and not b else (len(a & b) / len(a | b) if a and b else 0.0))
    wake = 1.0 if str(left.get("wake_kind", "")) == str(right.get("wake_kind", "")) else 0.0
    return round((wake + sum(scores)) / 4.0, 6)


def normalize(weights: Mapping[str, float], floor: float) -> dict[str, float]:
    floor = max(0.0, min(1.0 / 3.0, float(floor)))
    raw = {h: max(0.000001, float(weights.get(h, 0.0))) for h in HORIZONS}
    total = sum(raw.values())
    values = {h: raw[h] / total for h in HORIZONS}
    low = [h for h in HORIZONS if values[h] < floor]
    fixed = {h: floor for h in low}
    free = [h for h in HORIZONS if h not in low]
    remain = 1.0 - sum(fixed.values())
    free_total = sum(raw[h] for h in free) or 1.0
    for h in free:
        fixed[h] = remain * raw[h] / free_total
    total = sum(fixed.values())
    return {h: round(fixed[h] / total, 6) for h in HORIZONS}


def transport(section: Mapping[str, float], phase: Mapping[str, float], floor: float) -> dict[str, float]:
    return normalize({h: float(section.get(h, 0.0)) + float(phase.get(h, 0.0)) for h in HORIZONS}, floor)


def distance(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    return round(min(1.0, 0.5 * sum(abs(float(left[h]) - float(right[h])) for h in HORIZONS)), 6)


def aggregate(sections: list[tuple[float, Mapping[str, float]]], fallback: Mapping[str, float], floor: float) -> dict[str, float]:
    total = sum(weight for weight, _ in sections)
    if total <= 0.0:
        return normalize(fallback, floor)
    return normalize({h: sum(weight * float(section[h]) for weight, section in sections) / total for h in HORIZONS}, floor)


def curvature(sections: list[Mapping[str, float]], aggregate_section: Mapping[str, float]) -> tuple[float, float]:
    if not sections:
        return 0.0, 0.0
    local = sum(distance(section, aggregate_section) for section in sections) / len(sections)
    pairwise = [distance(sections[i], sections[j]) for i in range(len(sections)) for j in range(i + 1, len(sections))]
    return round(min(1.0, local), 6), round(max(pairwise, default=0.0), 6)
