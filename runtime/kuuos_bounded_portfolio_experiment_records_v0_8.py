#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_bounded_portfolio_experiment_types_v0_8 import (
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    BoundedPortfolioExperimentResult,
    as_list,
    integer,
    nonnegative,
    sha,
    state_digest,
    without,
)


def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "capability_state": root / "kuuos_adapter_capability_state_v0_6.json",
        "capability_bundle": root / "kuuos_adapter_capability_bundle_v0_6.json",
        "capability_calibration": root / "kuuos_adapter_capability_calibration_v0_6.json",
        "source_portfolio_bundle": root / "kuuos_adapter_portfolio_bundle_v0_7.json",
        "intervention_receipt": root / "kuuos_active_gauge_intervention_receipt_v0_3.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json",
        "decision": root / "kuuos_bounded_portfolio_experiment_decision_v0_8.json",
        "selection": root / "kuuos_bounded_portfolio_experiment_selection_v0_8.json",
        "projection": root / "kuuos_bounded_portfolio_experiment_shadow_projection_v0_8.json",
        "resolution": root / "kuuos_bounded_portfolio_experiment_shadow_resolution_v0_8.json",
        "trial": root / "kuuos_bounded_portfolio_trial_record_v0_8.json",
        "state": root / "kuuos_bounded_portfolio_experiment_state_v0_8.json",
        "receipt": root / "kuuos_bounded_portfolio_experiment_receipt_v0_8.json",
        "ledger": root / "kuuos_bounded_portfolio_experiment_ledger_v0_8.jsonl",
        "audit": root / "kuuos_bounded_portfolio_experiment_audit_v0_8.jsonl",
    }


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]
) -> BoundedPortfolioExperimentResult:
    return BoundedPortfolioExperimentResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        experiment_run_id=str(row.get("experiment_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        decision_mode=str(row.get("decision_mode", "")),
        baseline_adapter_id=str(row.get("baseline_adapter_id", "")),
        live_adapter_id=str(row.get("live_adapter_id", "")),
        experiment_adapter_id=str(row.get("experiment_adapter_id", "")),
        expected_information_gain=float(row.get("expected_information_gain", 0.0)),
        trial_cost=float(row.get("trial_cost", 0.0)),
        trial_risk=float(row.get("trial_risk", 0.0)),
        trial_recoverability=float(row.get("trial_recoverability", 1.0)),
        trial_budget_before=float(row.get("trial_budget_before", 0.0)),
        trial_budget_after=float(row.get("trial_budget_after", 0.0)),
        total_trial_count=integer(row.get("total_trial_count"), 0),
        total_exploit_count=integer(row.get("total_exploit_count"), 0),
        shadow_projection_count=integer(row.get("shadow_projection_count"), 0),
        resolved_shadow_count=integer(row.get("resolved_shadow_count"), 0),
        child_capability_status=str(row.get("child_capability_status", "")),
        child_capability_run_id=str(row.get("child_capability_run_id", "")),
        live_effect_receipt_digest=str(row.get("live_effect_receipt_digest", "")),
        experiment_bundle_digest=str(row.get("experiment_bundle_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        selection_path=str(p["selection"]),
        projection_path=str(p["projection"]),
        resolution_path=str(p["resolution"]),
        trial_path=str(p["trial"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=[],
        warnings=["experiment_run_replay_no_new_live_effect_or_budget_debit"],
    )


def pending_record(
    *,
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    source_batch_digest: str,
    previous_capability_state_digest: str,
    previous_capability_bundle_digest: str,
    source_portfolio_bundle_digest: str,
    previous_experiment_state_digest: str,
    previous_experiment_bundle_digest: str,
    decision: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "experiment_run_id": run_id,
        "experiment_plan_digest": plan.get("experiment_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_capability_state_digest": previous_capability_state_digest,
        "previous_capability_bundle_digest": previous_capability_bundle_digest,
        "source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "previous_experiment_state_digest": previous_experiment_state_digest,
        "previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "experiment_decision_digest": decision.get("experiment_decision_digest", ""),
        "decision_mode": decision.get("decision_mode", ""),
        "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
        "live_adapter_id": decision.get("live_adapter_id", ""),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    row["pending_digest"] = sha(without(row, "pending_digest"))
    return row


def build_state_and_record(
    *,
    previous_state: Mapping[str, Any],
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    cycle_index: int,
    decision: Mapping[str, Any],
    selection: Mapping[str, Any],
    projection: Mapping[str, Any],
    resolution: Mapping[str, Any],
    trial_record: Mapping[str, Any],
    bundle: Mapping[str, Any],
    child_result: Mapping[str, Any],
    live_effect_receipt_digest: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    is_trial = decision.get("decision_mode") == "licensed_experiment"
    state = {
        "version": STATE_VERSION,
        "experiment_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_experiment_state_digest": previous_state.get(
            "experiment_state_digest", ""
        ),
        "experiment_bundle_digest": bundle.get("experiment_bundle_digest", ""),
        "experiment_decision_digest": decision.get("experiment_decision_digest", ""),
        "portfolio_selection_digest": selection.get("portfolio_selection_digest", ""),
        "shadow_projection_digest": projection.get("shadow_projection_digest", ""),
        "shadow_resolution_digest": resolution.get("shadow_resolution_digest", ""),
        "trial_record_digest": trial_record.get("trial_record_digest", ""),
        "decision_mode": decision.get("decision_mode", ""),
        "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
        "live_adapter_id": decision.get("live_adapter_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "total_cycles": integer(previous_state.get("total_cycles"), 0) + 1,
        "total_trial_count": integer(bundle.get("total_trial_count"), 0),
        "total_exploit_count": integer(bundle.get("total_exploit_count"), 0),
        "trial_budget_spent": nonnegative(bundle.get("trial_budget_spent"), 0.0),
        "last_cycle_was_experiment": is_trial,
        "shadow_execution_count": 0,
        "multiple_live_adapter_count": 0,
        "epoch": int(time.time()),
    }
    state["experiment_state_digest"] = state_digest(state)
    total_budget = nonnegative(plan.get("total_trial_budget"), 0.0)
    spent_after = nonnegative(bundle.get("trial_budget_spent"), 0.0)
    spent_before = nonnegative(trial_record.get("trial_budget_spent_before"), spent_after)
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "experiment_run_id": run_id,
        "experiment_plan_digest": plan.get("experiment_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "decision_mode": decision.get("decision_mode", ""),
        "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
        "live_adapter_id": decision.get("live_adapter_id", ""),
        "experiment_adapter_id": decision.get("experiment_adapter_id", ""),
        "expected_information_gain": decision.get("expected_information_gain", 0.0),
        "trial_cost": trial_record.get("trial_cost", 0.0),
        "trial_risk": decision.get("trial_risk", 0.0),
        "trial_recoverability": decision.get("trial_recoverability", 1.0),
        "trial_budget_before": round(max(0.0, total_budget - spent_before), 6),
        "trial_budget_after": round(max(0.0, total_budget - spent_after), 6),
        "total_trial_count": bundle.get("total_trial_count", 0),
        "total_exploit_count": bundle.get("total_exploit_count", 0),
        "shadow_projection_count": projection.get("projection_count", 0),
        "resolved_shadow_count": 1 if resolution.get("resolved") is True else 0,
        "child_capability_status": child_result.get("status", ""),
        "child_capability_run_id": child_result.get("capability_run_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "experiment_bundle_digest": bundle.get("experiment_bundle_digest", ""),
        "experiment_state_digest": state.get("experiment_state_digest", ""),
        "record_digest": "",
    }
    row["record_digest"] = sha(without(row, "record_digest"))
    return state, row


def build_receipt(
    *,
    status: str,
    packet_id: str,
    run_id: str,
    cycle_index: int,
    plan: Mapping[str, Any],
    decision: Mapping[str, Any],
    projection: Mapping[str, Any],
    resolution: Mapping[str, Any],
    trial_record: Mapping[str, Any],
    bundle: Mapping[str, Any],
    child_result: Mapping[str, Any],
    live_effect_receipt_digest: str,
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    total_budget = nonnegative(plan.get("total_trial_budget"), 0.0)
    spent_after = nonnegative(bundle.get("trial_budget_spent"), 0.0)
    spent_before = nonnegative(trial_record.get("trial_budget_spent_before"), spent_after)
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "experiment_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "decision_mode": decision.get("decision_mode", ""),
        "baseline_adapter_id": decision.get("baseline_adapter_id", ""),
        "live_adapter_id": decision.get("live_adapter_id", ""),
        "experiment_adapter_id": decision.get("experiment_adapter_id", ""),
        "expected_information_gain": decision.get("expected_information_gain", 0.0),
        "trial_cost": trial_record.get("trial_cost", 0.0),
        "trial_risk": decision.get("trial_risk", 0.0),
        "trial_recoverability": decision.get("trial_recoverability", 1.0),
        "trial_budget_before": round(max(0.0, total_budget - spent_before), 6),
        "trial_budget_after": round(max(0.0, total_budget - spent_after), 6),
        "total_trial_count": bundle.get("total_trial_count", 0),
        "total_exploit_count": bundle.get("total_exploit_count", 0),
        "shadow_projection_count": projection.get("projection_count", 0),
        "resolved_shadow_count": 1 if resolution.get("resolved") is True else 0,
        "child_capability_status": child_result.get("status", ""),
        "child_capability_run_id": child_result.get("capability_run_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "experiment_bundle_digest": bundle.get("experiment_bundle_digest", ""),
        "one_live_adapter": True,
        "shadow_execution_count": 0,
        "trial_budget_debited_only_after_live_effect": True,
        "information_gain_estimate_not_truth": True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
