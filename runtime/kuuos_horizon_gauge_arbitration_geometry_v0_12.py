#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_delayed_credit_multihorizon_model_v0_11 import section_for as horizon_section_for
from runtime.kuuos_horizon_gauge_arbitration_basis_v0_12 import connection_residual, credit_vector, dominant_mode
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import HORIZONS, clamp

def arbitration_geometry(context_key: str, horizon_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    section = horizon_section_for(horizon_bundle, context_key)
    vectors = {h: credit_vector(section, h) for h in HORIZONS}
    dominants = {h: dominant_mode(vectors[h]) for h in HORIZONS}
    sm = connection_residual(vectors["short"], vectors["medium"])
    ml = connection_residual(vectors["medium"], vectors["long"])
    sl = connection_residual(vectors["short"], vectors["long"])
    curvature = clamp((sm + ml + sl) / 3.0)
    modes = {m for m, strength in dominants.values() if m != "none" and strength > 0.0}
    consensus = next(iter(modes)) if len(modes) == 1 else ("none" if not modes else "plural")
    threshold = clamp(plan.get("plural_conflict_curvature_threshold"), 0.25)
    kind = "plural_transport" if curvature >= threshold or consensus == "plural" else "aligned_transport"
    return {
        "section": section,
        "vectors": vectors,
        "dominants": dominants,
        "short_medium_residual": sm,
        "medium_long_residual": ml,
        "short_long_residual": sl,
        "curvature": curvature,
        "consensus_mode": consensus,
        "arbitration_class": kind,
    }
