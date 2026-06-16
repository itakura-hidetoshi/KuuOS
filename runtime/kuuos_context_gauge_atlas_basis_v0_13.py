from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import BUNDLE_VERSION, CHART_VERSION, as_list, bundle_digest, chart_digest, integer, mapping, sha


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {"version": BUNDLE_VERSION, "agent_id": agent_id, "generation": 0, "charts": [], "atlas_holonomy": [], "outcomes": [], "processed_outcome_digests": [], "processed_receipt_digests": [], "last_arbitration_bundle_digest": ""}
    packet["atlas_bundle_digest"] = bundle_digest(packet)
    return packet


def initial_chart(context_key: str, signature: Mapping[str, Any]) -> dict[str, Any]:
    packet = {"version": CHART_VERSION, "chart_id": "atlas-chart-" + sha(context_key)[:18], "context_key": context_key, "context_signature": dict(signature), "cycle_count": 0, "transition_count": 0, "mean_atlas_curvature": 0.0, "cumulative_cocycle_defect": 0.0, "last_short_weight": 0.0, "last_medium_weight": 0.0, "last_long_weight": 0.0, "last_commitment_outcome_class": "", "last_child_arbitration_outcome_digest": "", "last_child_effect_receipt_digest": ""}
    packet["chart_digest"] = chart_digest(packet)
    return packet
