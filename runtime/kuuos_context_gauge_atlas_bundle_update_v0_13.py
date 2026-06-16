from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_chart_update_v0_13 import update_chart
from runtime.kuuos_context_gauge_atlas_types_v0_13 import BUNDLE_VERSION, as_list, bundle_digest, integer, mapping


def commit_atlas(*, previous: Mapping[str, Any], decision: Mapping[str, Any], outcome: Mapping[str, Any], plan: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    child_digest = str(outcome.get("child_arbitration_outcome_digest", ""))
    processed = {str(item) for item in as_list(previous.get("processed_outcome_digests"))}
    if child_digest and child_digest in processed:
        return dict(previous), True
    chart = update_chart(atlas_bundle=previous, decision=decision, outcome=outcome)
    key = str(chart.get("context_key", ""))
    charts = [dict(mapping(item)) for item in as_list(previous.get("charts")) if mapping(item).get("context_key") != key]
    charts.append(chart)
    charts.sort(key=lambda item: str(item.get("context_key", "")))
    receipt_digest = str(outcome.get("child_effect_receipt_digest", ""))
    receipts = {str(item) for item in as_list(previous.get("processed_receipt_digests"))}
    holonomy = as_list(previous.get("atlas_holonomy")) + [{
        "atlas_run_id": outcome.get("atlas_run_id", ""),
        "cycle_index": outcome.get("cycle_index", 0),
        "target_context_key": key,
        "atlas_class": outcome.get("atlas_class", ""),
        "compatible_chart_count": outcome.get("compatible_chart_count", 0),
        "atlas_curvature": outcome.get("atlas_curvature", 0.0),
        "cocycle_defect": outcome.get("cocycle_defect", 0.0),
        "atlas_outcome_digest": outcome.get("atlas_outcome_digest", ""),
    }]
    packet = {
        "version": BUNDLE_VERSION,
        "agent_id": previous.get("agent_id", ""),
        "generation": integer(previous.get("generation"), 0) + 1,
        "charts": charts,
        "atlas_holonomy": holonomy[-integer(plan.get("max_atlas_holonomy"), 256):],
        "outcomes": (as_list(previous.get("outcomes")) + [dict(outcome)])[-integer(plan.get("max_atlas_outcomes"), 256):],
        "processed_outcome_digests": sorted(processed | ({child_digest} if child_digest else set())),
        "processed_receipt_digests": sorted(receipts | ({receipt_digest} if receipt_digest else set())),
        "last_arbitration_bundle_digest": outcome.get("child_arbitration_bundle_digest", ""),
    }
    packet["atlas_bundle_digest"] = bundle_digest(packet)
    return packet, False
