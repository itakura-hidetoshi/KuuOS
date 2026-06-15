#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_basis_v0_12 import section_for
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import clamp, integer, nonnegative, section_digest

def update_arbitration_section(*, previous_bundle: Mapping[str, Any], decision: Mapping[str, Any], outcome: Mapping[str, Any]) -> dict[str, Any]:
    context_key = str(decision.get("context_key", ""))
    old = section_for(previous_bundle, context_key)
    count = integer(old.get("cycle_count"), 0)
    curvature = clamp(decision.get("arbitration_curvature"))
    outcome_class = str(outcome.get("commitment_outcome_class", "holding"))
    section = dict(old)
    section.update({
        "cycle_count": count + 1,
        "cumulative_curvature": round(nonnegative(old.get("cumulative_curvature")) + curvature, 6),
        "mean_curvature": round((nonnegative(old.get("mean_curvature")) * count + curvature) / (count + 1), 6),
        "aligned_cycle_count": integer(old.get("aligned_cycle_count"), 0) + (decision.get("arbitration_class") == "aligned_transport"),
        "plural_cycle_count": integer(old.get("plural_cycle_count"), 0) + (decision.get("arbitration_class") == "plural_transport"),
        f"{outcome_class}_count": integer(old.get(f"{outcome_class}_count"), 0) + 1,
        "last_arbitration_class": decision.get("arbitration_class", ""),
        "last_commitment_outcome_class": outcome_class,
        "last_consensus_mode": decision.get("consensus_mode", ""),
        "last_short_dominant_mode": decision.get("short_dominant_mode", ""),
        "last_medium_dominant_mode": decision.get("medium_dominant_mode", ""),
        "last_long_dominant_mode": decision.get("long_dominant_mode", ""),
        "last_arbitration_curvature": round(curvature, 6),
        "last_transported_short_weight": decision.get("transported_short_weight", 0.0),
        "last_transported_medium_weight": decision.get("transported_medium_weight", 0.0),
        "last_transported_long_weight": decision.get("transported_long_weight", 0.0),
        "last_child_horizon_outcome_digest": outcome.get("child_horizon_outcome_digest", ""),
        "last_child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
    })
    section["arbitration_section_digest"] = section_digest(section)
    return section
