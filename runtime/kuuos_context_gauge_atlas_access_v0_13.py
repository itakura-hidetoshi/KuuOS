from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_basis_v0_13 import initial_chart
from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, integer, mapping


def chart_for(bundle: Mapping[str, Any], context_key: str, signature: Mapping[str, Any]) -> dict[str, Any]:
    for raw in as_list(bundle.get("charts")):
        chart = dict(mapping(raw))
        if chart.get("context_key") == context_key:
            return chart
    return initial_chart(context_key, signature)


def has_observation(chart: Mapping[str, Any]) -> bool:
    return integer(chart.get("cycle_count"), 0) > 0
