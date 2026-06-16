from __future__ import annotations
from typing import Any, Mapping
from runtime.context_math_v013 import HORIZONS, aggregate, curvature, overlap, transport
from runtime.kuuos_context_gauge_atlas_access_v0_13 import chart_for, has_observation
from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list, clamp, mapping


def chart_weights(chart: Mapping[str, Any], fallback: Mapping[str, float]) -> dict[str, float]:
    if not has_observation(chart):
        return dict(fallback)
    return {h: clamp(chart.get(f"last_{h}_weight"), fallback[h]) for h in HORIZONS}


def outcome_phase(chart: Mapping[str, Any], gain: float) -> dict[str, float]:
    phase = {h: 0.0 for h in HORIZONS}
    outcome = str(chart.get("last_commitment_outcome_class", ""))
    if outcome == "exploring":
        phase["short"] = gain
    elif outcome in {"progressing", "repairing"}:
        phase["medium"] = gain
    elif outcome == "stabilizing":
        phase["long"] = gain
    elif outcome == "plural_conflict":
        phase = {h: gain / 3.0 for h in HORIZONS}
    return phase


def transport_atlas(*, target_context_key: str, target_signature: Mapping[str, Any], atlas_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    fallback = {"short": clamp(plan.get("base_short_horizon_weight"), 0.5), "medium": clamp(plan.get("base_medium_horizon_weight"), 0.3), "long": clamp(plan.get("base_long_horizon_weight"), 0.2)}
    floor = clamp(plan.get("minimum_horizon_weight"), 0.12)
    target = chart_for(atlas_bundle, target_context_key, target_signature)
    local = chart_weights(target, fallback)
    weighted = [(clamp(plan.get("target_chart_retention"), 0.7), local)]
    sections = [local]
    transitions = []
    threshold = clamp(plan.get("minimum_chart_overlap"), 0.45)
    gain = clamp(plan.get("transition_phase_gain"), 0.06)
    for raw in as_list(atlas_bundle.get("charts")):
        chart = dict(mapping(raw))
        if not has_observation(chart) or chart.get("context_key") == target_context_key:
            continue
        score = overlap(mapping(chart.get("context_signature")), target_signature)
        if score < threshold:
            continue
        section = transport(chart_weights(chart, fallback), outcome_phase(chart, gain), floor)
        weighted.append((score, section))
        sections.append(section)
        transitions.append({"source_chart_id": chart.get("chart_id", ""), "source_context_key": chart.get("context_key", ""), "overlap": score, "transported_section": section})
    result = aggregate(weighted, fallback, floor)
    atlas_curvature, cocycle_defect = curvature(sections, result)
    return {"weights": result, "transitions": transitions, "compatible_chart_count": len(transitions), "atlas_curvature": atlas_curvature, "cocycle_defect": cocycle_defect}
