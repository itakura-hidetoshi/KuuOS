#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    REPLAYED,
    VERSION,
    DelayedCreditMultiHorizonResult,
    integer,
)


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
        "regret_outcome": root / "kuuos_policy_regret_cadence_outcome_v0_10.json",
        "gauge_state": root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "gauge_bundle": root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_delayed_credit_multihorizon_bundle_v0_11.json",
        "decision": root / "kuuos_delayed_credit_multihorizon_decision_v0_11.json",
        "outcome": root / "kuuos_delayed_credit_multihorizon_outcome_v0_11.json",
        "child_plan": root / "kuuos_delayed_credit_multihorizon_child_plan_v0_11.json",
        "child_license": root / "kuuos_delayed_credit_multihorizon_child_license_v0_11.json",
        "state": root / "kuuos_delayed_credit_multihorizon_state_v0_11.json",
        "receipt": root / "kuuos_delayed_credit_multihorizon_receipt_v0_11.json",
        "ledger": root / "kuuos_delayed_credit_multihorizon_ledger_v0_11.jsonl",
        "audit": root / "kuuos_delayed_credit_multihorizon_audit_v0_11.jsonl",
    }


def _float(row: Mapping[str, Any], field: str) -> float:
    try:
        return float(row.get(field, 0.0))
    except (TypeError, ValueError):
        return 0.0


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]
) -> DelayedCreditMultiHorizonResult:
    return DelayedCreditMultiHorizonResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        horizon_run_id=str(row.get("horizon_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        child_policy_mode=str(row.get("child_policy_mode", "")),
        child_live_adapter_id=str(row.get("child_live_adapter_id", "")),
        child_live_domain_action=str(row.get("child_live_domain_action", "")),
        commitment_progress_score=_float(row, "commitment_progress_score"),
        recovery_cost=_float(row, "recovery_cost"),
        terminal_section_ratio=_float(row, "terminal_section_ratio"),
        mean_curvature_norm=_float(row, "mean_curvature_norm"),
        delayed_compatible_evidence_count=integer(row.get("delayed_compatible_evidence_count"), 0),
        short_experiment_credit=_float(row, "short_experiment_credit"),
        short_reobserve_credit=_float(row, "short_reobserve_credit"),
        short_exploit_credit=_float(row, "short_exploit_credit"),
        medium_experiment_credit=_float(row, "medium_experiment_credit"),
        medium_reobserve_credit=_float(row, "medium_reobserve_credit"),
        medium_exploit_credit=_float(row, "medium_exploit_credit"),
        long_experiment_credit=_float(row, "long_experiment_credit"),
        long_reobserve_credit=_float(row, "long_reobserve_credit"),
        long_exploit_credit=_float(row, "long_exploit_credit"),
        aggregate_experiment_support=_float(row, "aggregate_experiment_support"),
        aggregate_reobserve_support=_float(row, "aggregate_reobserve_support"),
        aggregate_exploit_support=_float(row, "aggregate_exploit_support"),
        adapted_base_experiment_threshold=_float(row, "adapted_base_experiment_threshold"),
        adapted_base_reobserve_threshold=_float(row, "adapted_base_reobserve_threshold"),
        adapted_base_experiment_interval=integer(row.get("adapted_base_experiment_interval"), 0),
        adapted_base_reobserve_interval=integer(row.get("adapted_base_reobserve_interval"), 0),
        horizon_bundle_digest=str(row.get("horizon_bundle_digest", "")),
        child_regret_bundle_digest=str(row.get("child_regret_bundle_digest", "")),
        child_regret_outcome_digest=str(row.get("child_regret_outcome_digest", "")),
        child_effect_receipt_digest=str(row.get("child_effect_receipt_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]),
        child_license_path=str(p["child_license"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=[],
        warnings=["horizon_run_replay_no_new_regret_cycle_or_credit_update"],
    )
