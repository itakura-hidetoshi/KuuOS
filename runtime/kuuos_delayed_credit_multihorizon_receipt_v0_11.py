#!/usr/bin/env python3
from __future__ import annotations

import time
from typing import Any, Mapping

from runtime.kuuos_delayed_credit_multihorizon_ledger_v0_11 import credits
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import VERSION


def build_receipt(
    *, status: str, packet_id: str, run_id: str, cycle_index: int,
    decision: Mapping[str, Any], outcome: Mapping[str, Any],
    horizon_bundle: Mapping[str, Any], child_regret_bundle: Mapping[str, Any],
    child_regret_outcome: Mapping[str, Any], blockers: list[str], warnings: list[str],
) -> dict[str, Any]:
    section = next(
        (item for item in horizon_bundle.get("sections", [])
         if item.get("context_key") == decision.get("context_key")),
        {},
    )
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "horizon_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "child_policy_mode": outcome.get("child_policy_mode", ""),
        "child_live_adapter_id": child_regret_outcome.get("child_live_adapter_id", ""),
        "child_live_domain_action": outcome.get("child_live_domain_action", ""),
        "commitment_progress_score": outcome.get("commitment_progress_score", 0.0),
        "recovery_cost": outcome.get("recovery_cost", 0.0),
        "terminal_section_ratio": outcome.get("terminal_section_ratio", 0.0),
        "mean_curvature_norm": outcome.get("mean_curvature_norm", 0.0),
        "delayed_compatible_evidence_count": outcome.get("delayed_compatible_evidence_count", 0),
        **credits(section),
        "aggregate_support_after": outcome.get("aggregate_support_after", {}),
        "adapted_base_experiment_threshold": decision.get("adapted_base_experiment_threshold", 0.0),
        "adapted_base_reobserve_threshold": decision.get("adapted_base_reobserve_threshold", 0.0),
        "adapted_base_experiment_interval": decision.get("adapted_base_experiment_interval", 0),
        "adapted_base_reobserve_interval": decision.get("adapted_base_reobserve_interval", 0),
        "horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "child_regret_bundle_digest": child_regret_bundle.get("regret_bundle_digest", ""),
        "child_regret_outcome_digest": child_regret_outcome.get("regret_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "one_child_regret_cycle": True,
        "effectless_credit_update_count": 0,
        "multiple_child_cycle_count": 0,
        "hard_gate_bypass_count": 0,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
