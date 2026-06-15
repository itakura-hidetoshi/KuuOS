#!/usr/bin/env python3
from runtime.kuuos_adapter_capability_gauge_model_v0_6 import context_signature
from runtime.kuuos_event_adapter_federation_normalization_v0_5 import normalize_sources
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import integer, sha


def attach_identity(data):
    blockers = data["blockers"]
    normalized = normalize_sources(data["sources"]) if not blockers else {}
    context_key, _ = (
        context_signature(data["sources"], normalized)
        if not blockers
        else ("", {})
    )
    pending = data["pending"]
    cycle_index = (
        integer(pending.get("cycle_index"), 0)
        if pending is not None
        else integer(data["state"].get("cycle_index"), 0) + 1
    )
    packet_id = "kuuos-horizon-arbitration-" + sha(
        {
            "run": data["run_id"],
            "source_batch": data["source_batch"],
            "cycle": cycle_index,
        }
    )[:18]
    data.update(
        {
            "context_key": context_key,
            "cycle_index": cycle_index,
            "packet_id": packet_id,
        }
    )
    return data
