#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_geometry_v0_12 import arbitration_geometry
from runtime.kuuos_horizon_gauge_arbitration_transport_v0_12 import transport_weights
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import DECISION_VERSION, MODES, clamp, decision_digest

def build_arbitration_decision(*, arbitration_run_id: str, cycle_index: int, context_key: str, horizon_bundle: Mapping[str, Any], arbitration_bundle: Mapping[str, Any], gauge_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    geometry = arbitration_geometry(context_key, horizon_bundle, plan)
    transport = transport_weights(
        geometry=geometry,
        arbitration_bundle=arbitration_bundle,
        gauge_bundle=gauge_bundle,
        context_key=context_key,
        plan=plan,
    )
    vectors = geometry["vectors"]
    d = geometry["dominants"]
    weights = transport["weights"]
    packet = {
        "version": DECISION_VERSION,
        "arbitration_run_id": arbitration_run_id,
        "cycle_index": cycle_index,
        "context_key": context_key,
        "source_horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "source_arbitration_bundle_digest": arbitration_bundle.get("arbitration_bundle_digest", ""),
        "source_gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
        "horizon_credit_vectors": vectors,
        "short_dominant_mode": d["short"][0],
        "medium_dominant_mode": d["medium"][0],
        "long_dominant_mode": d["long"][0],
        "consensus_mode": geometry["consensus_mode"],
        "short_medium_connection": {m: round(vectors["medium"][m] - vectors["short"][m], 6) for m in MODES},
        "medium_long_connection": {m: round(vectors["long"][m] - vectors["medium"][m], 6) for m in MODES},
        "short_long_connection": {m: round(vectors["long"][m] - vectors["short"][m], 6) for m in MODES},
        "short_medium_residual": round(geometry["short_medium_residual"], 6),
        "medium_long_residual": round(geometry["medium_long_residual"], 6),
        "short_long_residual": round(geometry["short_long_residual"], 6),
        "arbitration_curvature": round(geometry["curvature"], 6),
        "arbitration_class": geometry["arbitration_class"],
        "short_transport_field": round(transport["fields"]["short"], 6),
        "medium_transport_field": round(transport["fields"]["medium"], 6),
        "long_transport_field": round(transport["fields"]["long"], 6),
        "transported_short_weight": weights["short"],
        "transported_medium_weight": weights["medium"],
        "transported_long_weight": weights["long"],
        "weight_sum": round(sum(weights.values()), 6),
        "minimum_horizon_weight": round(clamp(plan.get("minimum_horizon_weight"), 0.1), 6),
        "gauge_curvature_is_not_a_veto": True,
        "active_parallel_transport_enabled": True,
        "arbitration_decision_digest": "",
    }
    packet["arbitration_decision_digest"] = decision_digest(packet)
    return packet
