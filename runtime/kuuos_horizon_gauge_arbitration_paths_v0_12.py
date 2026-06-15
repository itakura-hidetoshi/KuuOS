#!/usr/bin/env python3
from __future__ import annotations
import pathlib
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import REPLAYED, VERSION, HorizonGaugeArbitrationResult, integer

def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "capability_state": root / "kuuos_adapter_capability_state_v0_6.json",
        "capability_bundle": root / "kuuos_adapter_capability_bundle_v0_6.json",
        "source_portfolio_bundle": root / "kuuos_adapter_portfolio_bundle_v0_7.json",
        "experiment_state": root / "kuuos_bounded_portfolio_experiment_state_v0_8.json",
        "experiment_bundle": root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json",
        "policy_state": root / "kuuos_experiment_outcome_policy_state_v0_9.json",
        "policy_bundle": root / "kuuos_experiment_outcome_policy_bundle_v0_9.json",
        "regret_state": root / "kuuos_policy_regret_cadence_state_v0_10.json",
        "regret_bundle": root / "kuuos_policy_regret_cadence_bundle_v0_10.json",
        "horizon_state": root / "kuuos_delayed_credit_multihorizon_state_v0_11.json",
        "horizon_bundle": root / "kuuos_delayed_credit_multihorizon_bundle_v0_11.json",
        "horizon_outcome": root / "kuuos_delayed_credit_multihorizon_outcome_v0_11.json",
        "gauge_state": root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "gauge_bundle": root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_horizon_gauge_arbitration_bundle_v0_12.json",
        "decision": root / "kuuos_horizon_gauge_arbitration_decision_v0_12.json",
        "outcome": root / "kuuos_horizon_gauge_arbitration_outcome_v0_12.json",
        "child_plan": root / "kuuos_horizon_gauge_arbitration_child_plan_v0_12.json",
        "child_license": root / "kuuos_horizon_gauge_arbitration_child_license_v0_12.json",
        "state": root / "kuuos_horizon_gauge_arbitration_state_v0_12.json",
        "receipt": root / "kuuos_horizon_gauge_arbitration_receipt_v0_12.json",
        "ledger": root / "kuuos_horizon_gauge_arbitration_ledger_v0_12.jsonl",
        "audit": root / "kuuos_horizon_gauge_arbitration_audit_v0_12.jsonl",
    }

def _float(row: Mapping[str, Any], field: str) -> float:
    try:
        return float(row.get(field, 0.0))
    except (TypeError, ValueError):
        return 0.0

def replay_result(row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]) -> HorizonGaugeArbitrationResult:
    return HorizonGaugeArbitrationResult(
        version=VERSION, status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        arbitration_run_id=str(row.get("arbitration_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root), context_key=str(row.get("context_key", "")),
        arbitration_class=str(row.get("arbitration_class", "")),
        commitment_outcome_class=str(row.get("commitment_outcome_class", "")),
        consensus_mode=str(row.get("consensus_mode", "")),
        short_dominant_mode=str(row.get("short_dominant_mode", "")),
        medium_dominant_mode=str(row.get("medium_dominant_mode", "")),
        long_dominant_mode=str(row.get("long_dominant_mode", "")),
        short_medium_residual=_float(row, "short_medium_residual"),
        medium_long_residual=_float(row, "medium_long_residual"),
        short_long_residual=_float(row, "short_long_residual"),
        arbitration_curvature=_float(row, "arbitration_curvature"),
        transported_short_weight=_float(row, "transported_short_weight"),
        transported_medium_weight=_float(row, "transported_medium_weight"),
        transported_long_weight=_float(row, "transported_long_weight"),
        child_policy_mode=str(row.get("child_policy_mode", "")),
        child_live_adapter_id=str(row.get("child_live_adapter_id", "")),
        child_live_domain_action=str(row.get("child_live_domain_action", "")),
        commitment_progress_score=_float(row, "commitment_progress_score"),
        recovery_cost=_float(row, "recovery_cost"),
        terminal_section_ratio=_float(row, "terminal_section_ratio"),
        arbitration_bundle_digest=str(row.get("arbitration_bundle_digest", "")),
        child_horizon_bundle_digest=str(row.get("child_horizon_bundle_digest", "")),
        child_horizon_outcome_digest=str(row.get("child_horizon_outcome_digest", "")),
        child_effect_receipt_digest=str(row.get("child_effect_receipt_digest", "")),
        idempotent_replay=True, recovered_pending_run=False,
        state_path=str(p["state"]), bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]), outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]), child_license_path=str(p["child_license"]),
        receipt_path=str(p["receipt"]), ledger_path=str(p["ledger"]), audit_path=str(p["audit"]),
        blockers=[], warnings=["arbitration_run_replay_no_new_horizon_cycle_or_transport"],
    )
