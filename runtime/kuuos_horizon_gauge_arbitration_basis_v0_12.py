#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import (
    BUNDLE_VERSION,
    HORIZONS,
    MODES,
    SECTION_VERSION,
    as_list,
    bundle_digest,
    clamp,
    mapping,
    section_digest,
    sha,
)


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": agent_id,
        "generation": 0,
        "sections": [],
        "arbitration_holonomy": [],
        "outcomes": [],
        "processed_child_horizon_outcome_digests": [],
        "processed_child_effect_digests": [],
        "last_horizon_bundle_digest": "",
        "last_gauge_bundle_digest": "",
    }
    packet["arbitration_bundle_digest"] = bundle_digest(packet)
    return packet


def initial_section(context_key: str) -> dict[str, Any]:
    packet = {
        "version": SECTION_VERSION,
        "section_id": "arbitration-section-" + sha(context_key)[:18],
        "context_key": context_key,
        "cycle_count": 0,
        "cumulative_curvature": 0.0,
        "mean_curvature": 0.0,
        "aligned_cycle_count": 0,
        "plural_cycle_count": 0,
        "exploring_count": 0,
        "progressing_count": 0,
        "repairing_count": 0,
        "stabilizing_count": 0,
        "plural_conflict_count": 0,
        "holding_count": 0,
        "last_arbitration_class": "",
        "last_commitment_outcome_class": "",
        "last_consensus_mode": "",
        "last_short_dominant_mode": "",
        "last_medium_dominant_mode": "",
        "last_long_dominant_mode": "",
        "last_arbitration_curvature": 0.0,
        "last_transported_short_weight": 0.0,
        "last_transported_medium_weight": 0.0,
        "last_transported_long_weight": 0.0,
        "last_child_horizon_outcome_digest": "",
        "last_child_effect_receipt_digest": "",
    }
    packet["arbitration_section_digest"] = section_digest(packet)
    return packet


def section_for(bundle: Mapping[str, Any], context_key: str) -> dict[str, Any]:
    for raw in as_list(bundle.get("sections")):
        section = dict(mapping(raw))
        if section.get("context_key") == context_key:
            return section
    return initial_section(context_key)


def credit_vector(section: Mapping[str, Any], horizon: str) -> dict[str, float]:
    return {mode: clamp(section.get(f"{horizon}_{mode}_credit")) for mode in MODES}


def dominant_mode(vector: Mapping[str, float]) -> tuple[str, float]:
    ordered = sorted(
        ((mode, float(vector.get(mode, 0.0))) for mode in MODES),
        key=lambda item: (-item[1], MODES.index(item[0])),
    )
    mode, strength = ordered[0]
    return (mode if strength > 0.0 else "none"), strength


def connection_residual(left: Mapping[str, float], right: Mapping[str, float]) -> float:
    return clamp(
        0.5
        * sum(
            abs(float(left.get(mode, 0.0)) - float(right.get(mode, 0.0)))
            for mode in MODES
        )
    )


def normalise_with_floor(raw: Mapping[str, float], floor: float) -> dict[str, float]:
    floor = max(0.0, min(1.0 / 3.0, floor))
    positive = {h: max(0.000001, float(raw.get(h, 0.0))) for h in HORIZONS}
    total = sum(positive.values())
    weights = {h: positive[h] / total for h in HORIZONS}
    fixed: dict[str, float] = {}
    free = list(HORIZONS)
    while True:
        below = [h for h in free if weights[h] < floor]
        if not below:
            break
        for horizon in below:
            fixed[horizon] = floor
            free.remove(horizon)
        if not free:
            break
        remaining = 1.0 - sum(fixed.values())
        free_total = sum(positive[h] for h in free)
        for horizon in free:
            weights[horizon] = remaining * positive[horizon] / free_total
    weights.update(fixed)
    normalizer = sum(weights.values())
    return {h: round(weights[h] / normalizer, 6) for h in HORIZONS}


def previous_outcome_bias(
    arbitration_section: Mapping[str, Any], plan: Mapping[str, Any]
) -> dict[str, float]:
    outcome = str(arbitration_section.get("last_commitment_outcome_class", ""))
    gain = clamp(plan.get("outcome_memory_gain"))
    bias = {h: 0.0 for h in HORIZONS}
    if outcome == "exploring":
        bias["short"] = gain
    elif outcome in {"progressing", "repairing"}:
        bias["medium"] = gain
    elif outcome == "stabilizing":
        bias["long"] = gain
    elif outcome == "plural_conflict":
        for horizon in HORIZONS:
            bias[horizon] = gain / 3.0
    return bias
