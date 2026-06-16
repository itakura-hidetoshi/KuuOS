from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_access_v0_13 import chart_for
from runtime.kuuos_context_gauge_atlas_types_v0_13 import chart_digest, integer, nonnegative


def update_chart(*, atlas_bundle: Mapping[str, Any], decision: Mapping[str, Any], outcome: Mapping[str, Any]) -> dict[str, Any]:
    key = str(decision.get("target_context_key", ""))
    signature = decision.get("target_context_signature", {})
    old = chart_for(atlas_bundle, key, signature)
    count = integer(old.get("cycle_count"), 0)
    curvature = nonnegative(decision.get("atlas_curvature"))
    chart = dict(old)
    chart["context_signature"] = dict(signature)
    chart["cycle_count"] = count + 1
    chart["transition_count"] = integer(old.get("transition_count"), 0) + integer(decision.get("compatible_chart_count"), 0)
    chart["mean_atlas_curvature"] = round((nonnegative(old.get("mean_atlas_curvature")) * count + curvature) / (count + 1), 6)
    chart["cumulative_cocycle_defect"] = round(nonnegative(old.get("cumulative_cocycle_defect")) + nonnegative(decision.get("cocycle_defect")), 6)
    chart["last_short_weight"] = outcome.get("transported_short_weight", 0.0)
    chart["last_medium_weight"] = outcome.get("transported_medium_weight", 0.0)
    chart["last_long_weight"] = outcome.get("transported_long_weight", 0.0)
    chart["last_commitment_outcome_class"] = outcome.get("child_commitment_outcome_class", "")
    chart["last_child_arbitration_outcome_digest"] = outcome.get("child_arbitration_outcome_digest", "")
    chart["last_child_effect_receipt_digest"] = outcome.get("child_effect_receipt_digest", "")
    chart["chart_digest"] = chart_digest(chart)
    return chart
