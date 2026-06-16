from __future__ import annotations
import time
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import VERSION


def build_receipt(*, status: str, packet_id: str, atlas_run_id: str, cycle_index: int, decision: Mapping[str, Any], outcome: Mapping[str, Any], atlas_bundle: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "atlas_run_id": atlas_run_id,
        "cycle_index": cycle_index,
        "target_context_key": decision.get("target_context_key", ""),
        "atlas_class": decision.get("atlas_class", ""),
        "compatible_chart_count": decision.get("compatible_chart_count", 0),
        "atlas_curvature": decision.get("atlas_curvature", 0.0),
        "cocycle_defect": decision.get("cocycle_defect", 0.0),
        "transported_short_weight": decision.get("transported_short_weight", 0.0),
        "transported_medium_weight": decision.get("transported_medium_weight", 0.0),
        "transported_long_weight": decision.get("transported_long_weight", 0.0),
        "child_arbitration_class": outcome.get("child_arbitration_class", ""),
        "child_commitment_outcome_class": outcome.get("child_commitment_outcome_class", ""),
        "child_policy_mode": outcome.get("child_policy_mode", ""),
        "child_live_adapter_id": outcome.get("child_live_adapter_id", ""),
        "child_live_domain_action": outcome.get("child_live_domain_action", ""),
        "atlas_bundle_digest": atlas_bundle.get("atlas_bundle_digest", ""),
        "child_arbitration_bundle_digest": outcome.get("child_arbitration_bundle_digest", ""),
        "child_arbitration_outcome_digest": outcome.get("child_arbitration_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "one_local_cycle": True,
        "chart_locality_bypass_count": 0,
        "cocycle_veto_count": 0,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
