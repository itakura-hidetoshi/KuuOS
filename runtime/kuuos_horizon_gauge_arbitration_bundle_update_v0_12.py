#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import BUNDLE_VERSION, as_list, bundle_digest, integer, mapping

def update_bundle(*, previous_bundle: Mapping[str, Any], section: Mapping[str, Any], outcome: Mapping[str, Any], child_horizon_bundle: Mapping[str, Any], gauge_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    context_key = str(section.get("context_key", ""))
    sections = [dict(mapping(item)) for item in as_list(previous_bundle.get("sections")) if mapping(item).get("context_key") != context_key]
    sections.append(dict(section))
    sections.sort(key=lambda item: str(item.get("context_key", "")))
    record = {
        "arbitration_run_id": outcome.get("arbitration_run_id", ""),
        "cycle_index": outcome.get("cycle_index", 0),
        "context_key": context_key,
        "arbitration_class": outcome.get("arbitration_class", ""),
        "commitment_outcome_class": outcome.get("commitment_outcome_class", ""),
        "arbitration_curvature": outcome.get("arbitration_curvature", 0.0),
        "transported_weights": {
            "short": outcome.get("transported_short_weight", 0.0),
            "medium": outcome.get("transported_medium_weight", 0.0),
            "long": outcome.get("transported_long_weight", 0.0),
        },
        "arbitration_outcome_digest": outcome.get("arbitration_outcome_digest", ""),
    }
    child_digest = str(outcome.get("child_horizon_outcome_digest", ""))
    effect_digest = str(outcome.get("child_effect_receipt_digest", ""))
    processed = {str(item) for item in as_list(previous_bundle.get("processed_child_horizon_outcome_digests"))}
    effects = {str(item) for item in as_list(previous_bundle.get("processed_child_effect_digests"))}
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": previous_bundle.get("agent_id", ""),
        "generation": integer(previous_bundle.get("generation"), 0) + 1,
        "sections": sections,
        "arbitration_holonomy": (as_list(previous_bundle.get("arbitration_holonomy")) + [record])[-integer(plan.get("max_arbitration_holonomy"), 256):],
        "outcomes": (as_list(previous_bundle.get("outcomes")) + [dict(outcome)])[-integer(plan.get("max_arbitration_outcomes"), 256):],
        "processed_child_horizon_outcome_digests": sorted(processed | {child_digest}),
        "processed_child_effect_digests": sorted(effects | {effect_digest}),
        "last_horizon_bundle_digest": child_horizon_bundle.get("horizon_bundle_digest", ""),
        "last_gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
    }
    packet["arbitration_bundle_digest"] = bundle_digest(packet)
    return packet
