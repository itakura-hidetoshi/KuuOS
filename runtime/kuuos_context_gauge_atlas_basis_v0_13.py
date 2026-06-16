from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import BUNDLE_VERSION, CHART_VERSION, as_list, bundle_digest, chart_digest, integer, mapping, sha


def empty_bundle(agent_id: str) -> dict[str, Any]:
    packet = {"version": BUNDLE_VERSION, "agent_id": agent_id, "generation": 0, "charts": [], "atlas_holonomy": [], "outcomes": [], "processed_outcome_digests": [], "processed_receipt_digests": [], "last_arbitration_bundle_digest": ""}
    packet["atlas_bundle_digest"] = bundle_digest(packet)
    return packet
