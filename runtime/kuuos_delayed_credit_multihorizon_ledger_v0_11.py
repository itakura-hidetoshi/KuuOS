#!/usr/bin/env python3
from __future__ import annotations

import time
from typing import Any, Mapping

from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import (
    LEDGER_VERSION,
    STATE_VERSION,
    integer,
    sha,
    state_digest,
    without,
)

CREDIT_FIELDS = (
    "short_experiment_credit", "short_reobserve_credit", "short_exploit_credit",
    "medium_experiment_credit", "medium_reobserve_credit", "medium_exploit_credit",
    "long_experiment_credit", "long_reobserve_credit", "long_exploit_credit",
)


def credits(section: Mapping[str, Any]) -> dict[str, float]:
    return {field: float(section.get(field, 0.0)) for field in CREDIT_FIELDS}


def pending_record(
    *, packet_id: str, run_id: str, plan: Mapping[str, Any],
    source_batch_digest: str, previous_regret_state_digest: str,
    previous_regret_bundle_digest: str, previous_horizon_state_digest: str,
    previous_horizon_bundle_digest: str, decision: Mapping[str, Any],
    child_plan: Mapping[str, Any], cycle_index: int,
) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "horizon_run_id": run_id,
        "horizon_plan_digest": plan.get("horizon_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_regret_state_digest": previous_regret_state_digest,
        "previous_regret_bundle_digest": previous_regret_bundle_digest,
        "previous_horizon_state_digest": previous_horizon_state_digest,
        "previous_horizon_bundle_digest": previous_horizon_bundle_digest,
        "horizon_decision_digest": decision.get("horizon_decision_digest", ""),
        "child_regret_plan_digest": child_plan.get("regret_plan_digest", ""),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    row["pending_digest"] = sha(without(row, "pending_digest"))
    return row


def build_state_and_record(
    *, previous_state: Mapping[str, Any], packet_id: str, run_id: str,
    plan: Mapping[str, Any], cycle_index: int, decision: Mapping[str, Any],
    outcome: Mapping[str, Any], horizon_bundle: Mapping[str, Any],
    child_regret_bundle: Mapping[str, Any], child_regret_outcome: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    mode = str(outcome.get("child_policy_mode", ""))
    progress = float(outcome.get("commitment_progress_score", 0.0))
    recovery = float(outcome.get("recovery_cost", 0.0))
    state = {
        "version": STATE_VERSION,
        "horizon_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_horizon_state_digest": previous_state.get("horizon_state_digest", ""),
        "horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "horizon_decision_digest": decision.get("horizon_decision_digest", ""),
        "horizon_outcome_digest": outcome.get("horizon_outcome_digest", ""),
        "child_regret_bundle_digest": child_regret_bundle.get("regret_bundle_digest", ""),
        "child_regret_outcome_digest": child_regret_outcome.get("regret_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "last_child_policy_mode": mode,
        "last_commitment_progress_score": progress,
        "last_recovery_cost": recovery,
        "total_cycles": integer(previous_state.get("total_cycles"), 0) + 1,
        "total_experiment_children": integer(previous_state.get("total_experiment_children"), 0) + (mode == "experiment"),
        "total_reobserve_children": integer(previous_state.get("total_reobserve_children"), 0) + (mode == "reobserve"),
        "total_exploit_children": integer(previous_state.get("total_exploit_children"), 0) + (mode == "exploit"),
        "total_progress_positive_cycles": integer(previous_state.get("total_progress_positive_cycles"), 0) + (progress > 0.0),
        "total_recovery_cost_positive_cycles": integer(previous_state.get("total_recovery_cost_positive_cycles"), 0) + (recovery > 0.0),
        "effectless_credit_update_count": 0,
        "multiple_child_cycle_count": 0,
        "hard_gate_bypass_count": 0,
        "epoch": int(time.time()),
    }
    state["horizon_state_digest"] = state_digest(state)
    section = next((item for item in horizon_bundle.get("sections", []) if item.get("context_key") == decision.get("context_key")), {})
    support = outcome.get("aggregate_support_after", {})
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "horizon_run_id": run_id,
        "horizon_plan_digest": plan.get("horizon_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "child_policy_mode": mode,
        "child_live_adapter_id": child_regret_outcome.get("child_live_adapter_id", ""),
        "child_live_domain_action": outcome.get("child_live_domain_action", ""),
        "commitment_progress_score": progress,
        "recovery_cost": recovery,
        "terminal_section_ratio": outcome.get("terminal_section_ratio", 0.0),
        "mean_curvature_norm": outcome.get("mean_curvature_norm", 0.0),
        "delayed_compatible_evidence_count": outcome.get("delayed_compatible_evidence_count", 0),
        **credits(section),
        "aggregate_experiment_support": support.get("experiment", 0.0),
        "aggregate_reobserve_support": support.get("reobserve", 0.0),
        "aggregate_exploit_support": support.get("exploit", 0.0),
        "adapted_base_experiment_threshold": decision.get("adapted_base_experiment_threshold", 0.0),
        "adapted_base_reobserve_threshold": decision.get("adapted_base_reobserve_threshold", 0.0),
        "adapted_base_experiment_interval": decision.get("adapted_base_experiment_interval", 0),
        "adapted_base_reobserve_interval": decision.get("adapted_base_reobserve_interval", 0),
        "horizon_bundle_digest": horizon_bundle.get("horizon_bundle_digest", ""),
        "child_regret_bundle_digest": child_regret_bundle.get("regret_bundle_digest", ""),
        "child_regret_outcome_digest": child_regret_outcome.get("regret_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "horizon_state_digest": state["horizon_state_digest"],
        "record_digest": "",
    }
    row["record_digest"] = sha(without(row, "record_digest"))
    return state, row
