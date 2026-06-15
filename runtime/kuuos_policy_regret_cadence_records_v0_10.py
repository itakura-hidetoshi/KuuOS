#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_policy_regret_cadence_types_v0_10 import (
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    PolicyRegretCadenceResult,
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
        "policy_state": root / "kuuos_experiment_outcome_policy_state_v0_9.json",
        "policy_bundle": root / "kuuos_experiment_outcome_policy_bundle_v0_9.json",
        "policy_outcome": root / "kuuos_experiment_outcome_policy_outcome_v0_9.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_policy_regret_cadence_bundle_v0_10.json",
        "decision": root / "kuuos_policy_regret_cadence_decision_v0_10.json",
        "outcome": root / "kuuos_policy_regret_cadence_outcome_v0_10.json",
        "child_plan": root / "kuuos_policy_regret_cadence_child_plan_v0_10.json",
        "child_license": root / "kuuos_policy_regret_cadence_child_license_v0_10.json",
        "state": root / "kuuos_policy_regret_cadence_state_v0_10.json",
        "receipt": root / "kuuos_policy_regret_cadence_receipt_v0_10.json",
        "ledger": root / "kuuos_policy_regret_cadence_ledger_v0_10.jsonl",
        "audit": root / "kuuos_policy_regret_cadence_audit_v0_10.jsonl",
    }


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]
) -> PolicyRegretCadenceResult:
    return PolicyRegretCadenceResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        regret_run_id=str(row.get("regret_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        child_policy_mode=str(row.get("child_policy_mode", "")),
        child_policy_reason=str(row.get("child_policy_reason", "")),
        child_live_adapter_id=str(row.get("child_live_adapter_id", "")),
        child_live_domain_action=str(row.get("child_live_domain_action", "")),
        chosen_value=float(row.get("chosen_value", 0.0)),
        best_alternative_mode=str(row.get("best_alternative_mode", "")),
        best_alternative_value=float(row.get("best_alternative_value", 0.0)),
        best_alternative_confidence=float(
            row.get("best_alternative_confidence", 0.0)
        ),
        bounded_regret=float(row.get("bounded_regret", 0.0)),
        experiment_regret_credit=float(row.get("experiment_regret_credit", 0.0)),
        reobserve_regret_credit=float(row.get("reobserve_regret_credit", 0.0)),
        exploit_regret_credit=float(row.get("exploit_regret_credit", 0.0)),
        adapted_experiment_pressure_threshold=float(
            row.get("adapted_experiment_pressure_threshold", 0.0)
        ),
        adapted_reobserve_pressure_threshold=float(
            row.get("adapted_reobserve_pressure_threshold", 0.0)
        ),
        adapted_experiment_interval=integer(
            row.get("adapted_experiment_interval"), 0
        ),
        adapted_reobserve_interval=integer(
            row.get("adapted_reobserve_interval"), 0
        ),
        delayed_compatible_evidence_count=integer(
            row.get("delayed_compatible_evidence_count"), 0
        ),
        pending_counterfactual_evidence_count=integer(
            row.get("pending_counterfactual_evidence_count"), 0
        ),
        regret_bundle_digest=str(row.get("regret_bundle_digest", "")),
        child_policy_bundle_digest=str(row.get("child_policy_bundle_digest", "")),
        child_policy_outcome_digest=str(row.get("child_policy_outcome_digest", "")),
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
        warnings=["regret_run_replay_no_new_policy_cycle_or_regret_update"],
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
    previous_regret_state_digest: str,
    previous_regret_bundle_digest: str,
    decision: Mapping[str, Any],
    child_plan: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "regret_run_id": run_id,
        "regret_plan_digest": plan.get("regret_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_capability_state_digest": previous_capability_state_digest,
        "previous_capability_bundle_digest": previous_capability_bundle_digest,
        "source_portfolio_bundle_digest": source_portfolio_bundle_digest,
        "previous_experiment_state_digest": previous_experiment_state_digest,
        "previous_experiment_bundle_digest": previous_experiment_bundle_digest,
        "previous_policy_state_digest": previous_policy_state_digest,
        "previous_policy_bundle_digest": previous_policy_bundle_digest,
        "previous_regret_state_digest": previous_regret_state_digest,
        "previous_regret_bundle_digest": previous_regret_bundle_digest,
        "regret_decision_digest": decision.get("regret_decision_digest", ""),
        "child_policy_plan_digest": child_plan.get("policy_plan_digest", ""),
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
    regret_bundle: Mapping[str, Any],
    child_policy_bundle: Mapping[str, Any],
    child_policy_outcome: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    regret = float(outcome.get("bounded_regret", 0.0))
    child_mode = str(outcome.get("child_policy_mode", ""))
    state = {
        "version": STATE_VERSION,
        "regret_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_regret_state_digest": previous_state.get("regret_state_digest", ""),
        "regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "regret_decision_digest": decision.get("regret_decision_digest", ""),
        "regret_outcome_digest": outcome.get("regret_outcome_digest", ""),
        "child_policy_bundle_digest": child_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "child_policy_outcome_digest": child_policy_outcome.get(
            "policy_outcome_digest", ""
        ),
        "child_effect_receipt_digest": child_policy_outcome.get(
            "child_effect_receipt_digest", ""
        ),
        "last_child_policy_mode": child_mode,
        "last_best_alternative_mode": outcome.get("best_alternative_mode", ""),
        "last_bounded_regret": regret,
        "total_cycles": integer(previous_state.get("total_cycles"), 0) + 1,
        "total_positive_regret_cycles": integer(
            previous_state.get("total_positive_regret_cycles"), 0
        )
        + (1 if regret > 0.0 else 0),
        "total_zero_regret_cycles": integer(
            previous_state.get("total_zero_regret_cycles"), 0
        )
        + (1 if regret <= 0.0 else 0),
        "total_experiment_children": integer(
            previous_state.get("total_experiment_children"), 0
        )
        + (1 if child_mode == "experiment" else 0),
        "total_reobserve_children": integer(
            previous_state.get("total_reobserve_children"), 0
        )
        + (1 if child_mode == "reobserve" else 0),
        "total_exploit_children": integer(
            previous_state.get("total_exploit_children"), 0
        )
        + (1 if child_mode == "exploit" else 0),
        "shadow_execution_count": 0,
        "counterfactual_truth_promotion_count": 0,
        "hard_gate_bypass_count": 0,
        "epoch": int(time.time()),
    }
    state["regret_state_digest"] = state_digest(state)
    section = next(
        (
            item
            for item in regret_bundle.get("sections", [])
            if item.get("context_key") == decision.get("context_key")
        ),
        {},
    )
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "regret_run_id": run_id,
        "regret_plan_digest": plan.get("regret_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "child_policy_mode": child_mode,
        "child_policy_reason": child_policy_outcome.get("policy_reason", ""),
        "child_live_adapter_id": child_policy_outcome.get(
            "child_live_adapter_id", ""
        ),
        "child_live_domain_action": child_policy_outcome.get(
            "live_domain_action", ""
        ),
        "chosen_value": outcome.get("chosen_value", 0.0),
        "best_alternative_mode": outcome.get("best_alternative_mode", ""),
        "best_alternative_value": outcome.get("best_alternative_value", 0.0),
        "best_alternative_confidence": outcome.get(
            "best_alternative_confidence", 0.0
        ),
        "bounded_regret": regret,
        "experiment_regret_credit": section.get("experiment_regret_credit", 0.0),
        "reobserve_regret_credit": section.get("reobserve_regret_credit", 0.0),
        "exploit_regret_credit": section.get("exploit_regret_credit", 0.0),
        "adapted_experiment_pressure_threshold": decision.get(
            "adapted_experiment_pressure_threshold", 0.0
        ),
        "adapted_reobserve_pressure_threshold": decision.get(
            "adapted_reobserve_pressure_threshold", 0.0
        ),
        "adapted_experiment_interval": decision.get(
            "adapted_experiment_interval", 0
        ),
        "adapted_reobserve_interval": decision.get(
            "adapted_reobserve_interval", 0
        ),
        "delayed_compatible_evidence_count": outcome.get(
            "delayed_compatible_evidence_count", 0
        ),
        "pending_counterfactual_evidence_count": outcome.get(
            "pending_counterfactual_evidence_count", 0
        ),
        "regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "child_policy_bundle_digest": child_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "child_policy_outcome_digest": child_policy_outcome.get(
            "policy_outcome_digest", ""
        ),
        "child_effect_receipt_digest": child_policy_outcome.get(
            "child_effect_receipt_digest", ""
        ),
        "regret_state_digest": state.get("regret_state_digest", ""),
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
    regret_bundle: Mapping[str, Any],
    child_policy_bundle: Mapping[str, Any],
    child_policy_outcome: Mapping[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    section = next(
        (
            item
            for item in regret_bundle.get("sections", [])
            if item.get("context_key") == decision.get("context_key")
        ),
        {},
    )
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "regret_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "child_policy_mode": outcome.get("child_policy_mode", ""),
        "child_policy_reason": child_policy_outcome.get("policy_reason", ""),
        "child_live_adapter_id": child_policy_outcome.get(
            "child_live_adapter_id", ""
        ),
        "child_live_domain_action": child_policy_outcome.get(
            "live_domain_action", ""
        ),
        "chosen_value": outcome.get("chosen_value", 0.0),
        "best_alternative_mode": outcome.get("best_alternative_mode", ""),
        "best_alternative_value": outcome.get("best_alternative_value", 0.0),
        "best_alternative_confidence": outcome.get(
            "best_alternative_confidence", 0.0
        ),
        "bounded_regret": outcome.get("bounded_regret", 0.0),
        "experiment_regret_credit": section.get("experiment_regret_credit", 0.0),
        "reobserve_regret_credit": section.get("reobserve_regret_credit", 0.0),
        "exploit_regret_credit": section.get("exploit_regret_credit", 0.0),
        "adapted_experiment_pressure_threshold": decision.get(
            "adapted_experiment_pressure_threshold", 0.0
        ),
        "adapted_reobserve_pressure_threshold": decision.get(
            "adapted_reobserve_pressure_threshold", 0.0
        ),
        "adapted_experiment_interval": decision.get(
            "adapted_experiment_interval", 0
        ),
        "adapted_reobserve_interval": decision.get(
            "adapted_reobserve_interval", 0
        ),
        "delayed_compatible_evidence_count": outcome.get(
            "delayed_compatible_evidence_count", 0
        ),
        "pending_counterfactual_evidence_count": outcome.get(
            "pending_counterfactual_evidence_count", 0
        ),
        "regret_bundle_digest": regret_bundle.get("regret_bundle_digest", ""),
        "child_policy_bundle_digest": child_policy_bundle.get(
            "policy_bundle_digest", ""
        ),
        "child_policy_outcome_digest": child_policy_outcome.get(
            "policy_outcome_digest", ""
        ),
        "child_effect_receipt_digest": child_policy_outcome.get(
            "child_effect_receipt_digest", ""
        ),
        "one_child_policy_cycle": True,
        "counterfactual_truth_promotion_count": 0,
        "shadow_execution_count": 0,
        "hard_gate_bypass_count": 0,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
