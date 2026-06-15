#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_basis_v0_12 import normalise_with_floor, previous_outcome_bias, section_for
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import as_list, clamp, integer, nonnegative

def transport_weights(*, geometry: Mapping[str, Any], arbitration_bundle: Mapping[str, Any], gauge_bundle: Mapping[str, Any], context_key: str, plan: Mapping[str, Any]) -> dict[str, Any]:
    hs = geometry["section"]
    ars = section_for(arbitration_bundle, context_key)
    cycles = max(1, integer(hs.get("cycle_count"), 0))
    progress = clamp(hs.get("mean_commitment_progress"))
    recovery = clamp(hs.get("mean_recovery_cost"))
    terminal = clamp(integer(hs.get("terminal_section_observation_count"), 0) / cycles)
    scale = max(1.0, nonnegative(plan.get("arbitration_holonomy_scale"), 8.0))
    holonomy = clamp(len(as_list(gauge_bundle.get("holonomy_trace"))) / scale)
    bias = previous_outcome_bias(ars, plan)
    d = geometry["dominants"]
    curvature = clamp(geometry.get("curvature"))
    fields = {
        "short": clamp(d["short"][1] + clamp(plan.get("short_curvature_response_gain")) * curvature + bias["short"]),
        "medium": clamp(d["medium"][1] + clamp(plan.get("medium_progress_response_gain")) * progress + clamp(plan.get("medium_recovery_response_gain")) * recovery + bias["medium"]),
        "long": clamp(d["long"][1] + clamp(plan.get("long_terminal_response_gain")) * terminal + clamp(plan.get("long_holonomy_response_gain")) * holonomy + bias["long"]),
    }
    mean_field = sum(fields.values()) / 3.0
    temperature = 1.0 + clamp(plan.get("curvature_temperature_gain")) * curvature
    gain = clamp(plan.get("parallel_transport_gain"))
    raw = {
        "short": clamp(plan.get("base_short_horizon_weight"), 0.5) + gain * (fields["short"] - mean_field) / temperature,
        "medium": clamp(plan.get("base_medium_horizon_weight"), 0.3) + gain * (fields["medium"] - mean_field) / temperature,
        "long": clamp(plan.get("base_long_horizon_weight"), 0.2) + gain * (fields["long"] - mean_field) / temperature,
    }
    weights = normalise_with_floor(raw, clamp(plan.get("minimum_horizon_weight"), 0.1))
    return {"fields": fields, "weights": weights, "progress": progress, "recovery": recovery, "terminal": terminal, "holonomy": holonomy}
