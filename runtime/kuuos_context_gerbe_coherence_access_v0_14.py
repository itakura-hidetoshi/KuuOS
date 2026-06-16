from __future__ import annotations

from typing import Any, Mapping

from runtime.context_math_v013 import normalize
from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, clamp, mapping


def atlas_base_section(
    atlas_decision: Mapping[str, Any],
    plan: Mapping[str, Any],
    floor: float,
) -> dict[str, float]:
    fallback = {
        "short": clamp(plan.get("base_short_horizon_weight"), 0.5),
        "medium": clamp(plan.get("base_medium_horizon_weight"), 0.3),
        "long": clamp(plan.get("base_long_horizon_weight"), 0.2),
    }
    return normalize(
        {
            "short": atlas_decision.get("transported_short_weight", fallback["short"]),
            "medium": atlas_decision.get("transported_medium_weight", fallback["medium"]),
            "long": atlas_decision.get("transported_long_weight", fallback["long"]),
        },
        floor,
    )


def chart_index(atlas_bundle: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for raw in as_list(atlas_bundle.get("charts")):
        chart = dict(mapping(raw))
        chart_id = str(chart.get("chart_id", ""))
        if chart_id:
            index[chart_id] = chart
    return index


def atlas_transitions(
    *,
    atlas_decision: Mapping[str, Any],
    atlas_bundle: Mapping[str, Any],
    floor: float,
) -> list[dict[str, Any]]:
    charts = chart_index(atlas_bundle)
    transitions: list[dict[str, Any]] = []
    for raw in as_list(atlas_decision.get("transitions")):
        transition = dict(mapping(raw))
        chart_id = str(transition.get("source_chart_id", ""))
        chart = charts.get(chart_id)
        if chart is None:
            raise ValueError("atlas_transition_source_chart_missing")
        transitions.append(
            {
                "source_chart_id": chart_id,
                "source_context_key": transition.get("source_context_key", ""),
                "target_overlap": clamp(transition.get("overlap"), 0.0),
                "transported_section": normalize(
                    mapping(transition.get("transported_section")), floor
                ),
                "chart": chart,
            }
        )
    transitions.sort(
        key=lambda item: (
            str(item.get("source_context_key", "")),
            str(item.get("source_chart_id", "")),
        )
    )
    return transitions
