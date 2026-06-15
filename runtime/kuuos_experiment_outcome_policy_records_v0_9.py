#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_experiment_outcome_policy_types_v0_9 import (
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    ExperimentOutcomePolicyResult,
    integer,
    sha,
    state_digest,
    without,
)


def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "capability_state": root / "kuuos_adapter_capability_state_v0_6.json",
        "capability_bundle": root / "kuuos_adapter_capability_bundle_v0_6.json",
        "source_portfolio_bundle": root / "kuuos_adapter_portfolio_bundle_v0_7.json",
        "experiment_state": root / "kuuos_bounded_portfolio_experiment_state_v0_8.json",
        "experiment_bundle": root / "kuuos_bounded_portfolio_experiment_bundle_v0_8.json",
        "experiment_decision": root / "kuuos_bounded_portfolio_experiment_decision_v0_8.json",
        "experiment_trial": root / "kuuos_bounded_portfolio_trial_record_v0_8.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_experiment_outcome_policy_bundle_v0_9.json",
        "decision": root / "kuuos_experiment_outcome_policy_decision_v0_9.json",
        "outcome": root / "kuuos_experiment_outcome_policy_outcome_v0_9.json",
        "child_plan": root / "kuuos_experiment_outcome_policy_child_plan_v0_9.json",
        "child_license": root / "kuuos_experiment_outcome_policy_child_license_v0_9.json",
        "child_registry": root / "kuuos_experiment_outcome_policy_child_registry_v0_9.json",
        "state": root / "kuuos_experiment_outcome_policy_state_v0_9.json",
        "receipt": root / "kuuos_experiment_outcome_policy_receipt_v0_9.json",
        "ledger": root / "kuuos_experiment_outcome_policy_ledger_v0_9.jsonl",
        "audit": root / "kuuos_experiment_outcome_policy_audit_v0_9.jsonl",
    }


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]
) -> ExperimentOutcomePolicyResult:
    return ExperimentOutcomePolicyResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        policy_run_id=str(row.get("policy_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        policy_mode=str(row.get("policy_mode", "")),
        policy_reason=str(row.get("policy_reason", "")),
        preview_baseline_adapter_id=str(row.get("preview_baseline_adapter_id", "")),
        preview_experiment_adapter_id=str(row.get("preview_experiment_adapter_id", "")),
        child_decision_mode=str(row.get("child_decision_mode", "")),
        child_live_adapter_id=str(row.get("child_live_adapter_id", "")),
        adapted_minimum_information_gain=float(
            row.get("adapted_minimum_information_gain", 0.0)
        ),
        adapted_trial_cooldown_cycles=integer(
            row.get("adapted_trial_cooldown_cycles"), 0
        ),
        experiment_pressure=float(row.get("experiment_pressure", 0.0)),
        reobserve_pressure=float(row.get("reobserve_pressure", 0.0)),
        posterior_experiment_success=float(
            row.get("posterior_experiment_success", 0.5)
        ),
        mean_net_experiment_value=float(row.get("mean_net_experiment_value", 0.0)),
        live_observed_utility=float(row.get("live_observed_utility", 0.0)),
        live_domain_action=str(row.get("live_domain_action", "")),
        compatible_shadow_resolved=row.get("compatible_shadow_resolved") is True,
        policy_bundle_digest=str(row.get("policy_bundle_digest", "")),
        child_experiment_bundle_digest=str(
            row.get("child_experiment_bundle_digest", "")
        ),
        child_effect_receipt_digest=str(row.get("child_effect_receipt_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        decision_path=str(p["decision"]),
        outcome_path=str(p["outcome"]),
        child_plan_path=str(p["child_plan"]),
        child_license_path=str(p["child_license"]),
        child_registry_path=str(p["child_registry"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=[],
        warnings=["policy_run_replay_no_new_child_cycle_or_policy_update"],
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
    previous_policy_state_digest: str,
    previous_policy_bundle_digest: str,
    decision: Mapping[str, Any],
    child_plan: Mapping[str, Any],
    child_registry: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "policy_run_id": run_id,
        "policy_plan_digest": plan.get("policy_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_capability_state_digest": previous_capability_state_digest,
        "previous_capability_bundle_digest": previous_capability_bundle_digest,
        "source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "previous_experiment_state_digest": previous_experiment_state_digest,
        "previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "previous_policy_state_digest": previous_policy_state_digest,
        "previous_policy_bundle_digest": previous_policy_bundle_digest,
        "policy_decision_digest": decision.get("policy_decision_digest", ""),
        "child_experiment_plan_digest": child_plan.get(
            "experiment_plan_digest", ""
        ),
        "child_adapter_registry_digest": child_registry.get(
            "adapter_registry_digest", ""
        ),
        "policy_mode": decision.get("policy_mode", ""),
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
    outcome: Mapping[str, Any],
    policy_bundle: Mapping[str, Any],
    child_experiment_bundle: Mapping[str, Any],
    child_effect: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    policy_mode = str(decision.get("policy_mode", ""))
    state = {
        "version": STATE_VERSION,
        "policy_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_policy_state_digest": previous_state.get("policy_state_digest", ""),
        "policy_bundle_digest": policy_bundle.get("policy_bundle_digest", ""),
        "policy_decision_digest": decision.get("policy_decision_digest", ""),
        "policy_outcome_digest": outcome.get("policy_outcome_digest", ""),
        "child_experiment_bundle_digest": child_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "child_effect_receipt_digest": child_effect.get("effect_receipt_digest", ""),
        "last_policy_mode": policy_mode,
        "last_child_decision_mode": outcome.get("child_decision_mode", ""),
        "last_live_domain_action": outcome.get("live_domain_action", ""),
        "last_compatible_shadow_resolved": outcome.get(
            "compatible_shadow_resolved"
        )
        is True,
        "total_cycles": integer(previous_state.get("total_cycles"), 0) + 1,
        "total_experiment_policy_cycles": integer(
            previous_state.get("total_experiment_policy_cycles"), 0
        )
        + (1 if policy_mode == "experiment" else 0),
        "total_reobserve_policy_cycles": integer(
            previous_state.get("total_reobserve_policy_cycles"), 0
        )
        + (1 if policy_mode == "reobserve" else 0),
        "total_exploit_policy_cycles": integer(
            previous_state.get("total_exploit_policy_cycles"), 0
        )
        + (1 if policy_mode == "exploit" else 0),
        "shadow_execution_count": 0,
        "hard_gate_bypass_count": 0,
        "epoch": int(time.time()),
    }
    state["policy_state_digest"] = state_digest(state)
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "policy_run_id": run_id,
        "policy_plan_digest": plan.get("policy_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "policy_mode": policy_mode,
        "policy_reason": decision.get("policy_reason", ""),
        "preview_baseline_adapter_id": decision.get(
            "preview_baseline_adapter_id", ""
        ),
        "preview_experiment_adapter_id": decision.get(
            "preview_experiment_adapter_id", ""
        ),
        "child_decision_mode": outcome.get("child_decision_mode", ""),
        "child_live_adapter_id": outcome.get("child_live_adapter_id", ""),
        "adapted_minimum_information_gain": decision.get(
            "adapted_minimum_information_gain", 0.0
        ),
        "adapted_trial_cooldown_cycles": decision.get(
            "adapted_trial_cooldown_cycles", 0
        ),
        "experiment_pressure": decision.get("experiment_pressure", 0.0),
        "reobserve_pressure": decision.get("reobserve_pressure", 0.0),
        "posterior_experiment_success": decision.get(
            "posterior_experiment_success", 0.5
        ),
        "mean_net_experiment_value": decision.get(
            "mean_net_experiment_value", 0.0
        ),
        "live_observed_utility": outcome.get("live_observed_utility", 0.0),
        "live_domain_action": outcome.get("live_domain_action", ""),
        "compatible_shadow_resolved": outcome.get("compatible_shadow_resolved")
        is True,
        "policy_bundle_digest": policy_bundle.get("policy_bundle_digest", ""),
        "child_experiment_bundle_digest": child_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "child_effect_receipt_digest": child_effect.get(
            "effect_receipt_digest", ""
        ),
        "policy_state_digest": state.get("policy_state_digest", ""),
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
    decision: Mapping[str, Any],
    outcome: Mapping[str, Any],
    policy_bundle: Mapping[str, Any],
    child_experiment_bundle: Mapping[str, Any],
    child_effect: Mapping[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "policy_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "policy_mode": decision.get("policy_mode", ""),
        "policy_reason": decision.get("policy_reason", ""),
        "preview_baseline_adapter_id": decision.get(
            "preview_baseline_adapter_id", ""
        ),
        "preview_experiment_adapter_id": decision.get(
            "preview_experiment_adapter_id", ""
        ),
        "child_decision_mode": outcome.get("child_decision_mode", ""),
        "child_live_adapter_id": outcome.get("child_live_adapter_id", ""),
        "adapted_minimum_information_gain": decision.get(
            "adapted_minimum_information_gain", 0.0
        ),
        "adapted_trial_cooldown_cycles": decision.get(
            "adapted_trial_cooldown_cycles", 0
        ),
        "experiment_pressure": decision.get("experiment_pressure", 0.0),
        "reobserve_pressure": decision.get("reobserve_pressure", 0.0),
        "posterior_experiment_success": decision.get(
            "posterior_experiment_success", 0.5
        ),
        "mean_net_experiment_value": decision.get(
            "mean_net_experiment_value", 0.0
        ),
        "live_observed_utility": outcome.get("live_observed_utility", 0.0),
        "live_domain_action": outcome.get("live_domain_action", ""),
        "compatible_shadow_resolved": outcome.get("compatible_shadow_resolved")
        is True,
        "policy_bundle_digest": policy_bundle.get("policy_bundle_digest", ""),
        "child_experiment_bundle_digest": child_experiment_bundle.get(
            "experiment_bundle_digest", ""
        ),
        "child_effect_receipt_digest": child_effect.get(
            "effect_receipt_digest", ""
        ),
        "one_child_cycle": True,
        "one_live_adapter": True,
        "shadow_execution_count": 0,
        "v0_8_hard_gate_bypass_count": 0,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
