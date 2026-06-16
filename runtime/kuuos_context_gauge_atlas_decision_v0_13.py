from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_transport_v0_13 import transport_atlas
from runtime.kuuos_context_gauge_atlas_types_v0_13 import DECISION_VERSION, clamp, decision_digest


def build_atlas_decision(*, atlas_run_id: str, cycle_index: int, target_context_key: str, target_signature: Mapping[str, Any], atlas_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    transport = transport_atlas(target_context_key=target_context_key, target_signature=target_signature, atlas_bundle=atlas_bundle, plan=plan)
    threshold = clamp(plan.get("plural_atlas_curvature_threshold"), 0.08)
    count = int(transport["compatible_chart_count"])
    atlas_class = "isolated_chart" if count == 0 else ("plural_atlas_transport" if transport["atlas_curvature"] >= threshold else "compatible_chart_transport")
    weights = transport["weights"]
    packet = {
        "version": DECISION_VERSION,
        "atlas_run_id": atlas_run_id,
        "cycle_index": cycle_index,
        "target_context_key": target_context_key,
        "target_context_signature": dict(target_signature),
        "source_atlas_bundle_digest": atlas_bundle.get("atlas_bundle_digest", ""),
        "atlas_class": atlas_class,
        "compatible_chart_count": count,
        "transitions": transport["transitions"],
        "atlas_curvature": transport["atlas_curvature"],
        "cocycle_defect": transport["cocycle_defect"],
        "transported_short_weight": weights["short"],
        "transported_medium_weight": weights["medium"],
        "transported_long_weight": weights["long"],
        "weight_sum": round(sum(weights.values()), 6),
        "chart_locality_preserved": True,
        "cocycle_defect_is_not_a_veto": True,
        "atlas_decision_digest": "",
    }
    packet["atlas_decision_digest"] = decision_digest(packet)
    return packet
