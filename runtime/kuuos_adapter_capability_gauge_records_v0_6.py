#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_adapter_capability_gauge_types_v0_6 import (
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    AdapterCapabilityGaugeResult,
    integer,
    sha,
    state_digest,
    without,
)


def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "federation_state": root / "kuuos_event_adapter_federation_state_v0_5.json",
        "federation_evidence": root / "kuuos_federated_effect_evidence_v0_5.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "next_wake": root / "kuuos_renewable_gauge_next_wake_v0_4.json",
        "bundle": root / "kuuos_adapter_capability_bundle_v0_6.json",
        "selection": root / "kuuos_adapter_capability_selection_v0_6.json",
        "calibration": root / "kuuos_adapter_capability_calibration_v0_6.json",
        "state": root / "kuuos_adapter_capability_state_v0_6.json",
        "receipt": root / "kuuos_adapter_capability_receipt_v0_6.json",
        "ledger": root / "kuuos_adapter_capability_ledger_v0_6.jsonl",
        "audit": root / "kuuos_adapter_capability_audit_v0_6.jsonl",
    }


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, artifact_paths: Mapping[str, pathlib.Path]
) -> AdapterCapabilityGaugeResult:
    return AdapterCapabilityGaugeResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        capability_run_id=str(row.get("capability_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        selected_federation_adapter_id=str(
            row.get("selected_federation_adapter_id", "")
        ),
        selected_adapter_profile_digest=str(
            row.get("selected_adapter_profile_digest", "")
        ),
        selection_score=float(row.get("selection_score", 0.0)),
        prior_connection=float(row.get("prior_connection", 0.0)),
        observed_utility=float(row.get("observed_utility", 0.0)),
        updated_connection=float(row.get("updated_connection", 0.0)),
        capability_curvature=float(row.get("capability_curvature", 0.0)),
        observation_count=integer(row.get("observation_count"), 0),
        child_federation_status=str(row.get("child_federation_status", "")),
        child_federation_run_id=str(row.get("child_federation_run_id", "")),
        child_evidence_digest=str(row.get("child_evidence_digest", "")),
        effect_receipt_digest=str(row.get("effect_receipt_digest", "")),
        next_wake_digest=str(row.get("next_wake_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(artifact_paths["state"]),
        bundle_path=str(artifact_paths["bundle"]),
        selection_path=str(artifact_paths["selection"]),
        calibration_path=str(artifact_paths["calibration"]),
        receipt_path=str(artifact_paths["receipt"]),
        ledger_path=str(artifact_paths["ledger"]),
        audit_path=str(artifact_paths["audit"]),
        blockers=[],
        warnings=["capability_run_replay_no_new_effect_or_calibration"],
    )


def pending_record(
    *,
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    source_batch_digest: str,
    previous_state_digest: str,
    previous_bundle_digest: str,
    selection: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    record = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "capability_run_id": run_id,
        "capability_plan_digest": plan.get("capability_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_capability_state_digest": previous_state_digest,
        "previous_capability_bundle_digest": previous_bundle_digest,
        "selection_digest": selection.get("selection_digest", ""),
        "selected_federation_adapter_id": selection.get(
            "selected_federation_adapter_id", ""
        ),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    record["pending_digest"] = sha(without(record, "pending_digest"))
    return record


def build_state_and_record(
    *,
    previous_state: Mapping[str, Any],
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    cycle_index: int,
    selection: Mapping[str, Any],
    calibration: Mapping[str, Any],
    bundle: Mapping[str, Any],
    child_result: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = {
        "version": STATE_VERSION,
        "capability_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_capability_state_digest": previous_state.get(
            "capability_state_digest", ""
        ),
        "capability_bundle_digest": bundle.get("capability_bundle_digest", ""),
        "selection_digest": selection.get("selection_digest", ""),
        "calibration_digest": calibration.get("calibration_digest", ""),
        "context_key": selection.get("context_key", ""),
        "selected_federation_adapter_id": selection.get(
            "selected_federation_adapter_id", ""
        ),
        "child_federation_run_id": child_result.get("federation_run_id", ""),
        "child_evidence_digest": child_result.get("evidence_digest", ""),
        "effect_receipt_digest": child_result.get("effect_receipt_digest", ""),
        "next_wake_digest": child_result.get("next_wake_digest", ""),
        "total_calibrations": integer(previous_state.get("total_calibrations"), 0)
        + 1,
        "capability_estimate_not_truth": True,
        "non_markov_holonomy_preserved": True,
        "epoch": int(time.time()),
    }
    state["capability_state_digest"] = state_digest(state)
    record = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "capability_run_id": run_id,
        "capability_plan_digest": plan.get("capability_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": selection.get("context_key", ""),
        "selected_federation_adapter_id": selection.get(
            "selected_federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selection.get(
            "selected_adapter_profile_digest", ""
        ),
        "selection_score": selection.get("selected_score", 0.0),
        "prior_connection": calibration.get("prior_connection", 0.0),
        "observed_utility": calibration.get("observed_utility", 0.0),
        "updated_connection": calibration.get("updated_connection", 0.0),
        "capability_curvature": calibration.get("capability_curvature", 0.0),
        "observation_count": calibration.get("observation_count", 0),
        "child_federation_status": child_result.get("status", ""),
        "child_federation_run_id": child_result.get("federation_run_id", ""),
        "child_evidence_digest": child_result.get("evidence_digest", ""),
        "effect_receipt_digest": child_result.get("effect_receipt_digest", ""),
        "next_wake_digest": child_result.get("next_wake_digest", ""),
        "capability_bundle_digest": bundle.get("capability_bundle_digest", ""),
        "capability_state_digest": state.get("capability_state_digest", ""),
        "record_digest": "",
    }
    record["record_digest"] = sha(without(record, "record_digest"))
    return state, record


def build_receipt(
    *,
    status: str,
    packet_id: str,
    run_id: str,
    cycle_index: int,
    selection: Mapping[str, Any],
    calibration: Mapping[str, Any],
    child_result: Mapping[str, Any],
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "capability_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": selection.get("context_key", ""),
        "selected_federation_adapter_id": selection.get(
            "selected_federation_adapter_id", ""
        ),
        "selected_adapter_profile_digest": selection.get(
            "selected_adapter_profile_digest", ""
        ),
        "selection_score": selection.get("selected_score", 0.0),
        "prior_connection": calibration.get("prior_connection", 0.0),
        "observed_utility": calibration.get("observed_utility", 0.0),
        "updated_connection": calibration.get("updated_connection", 0.0),
        "capability_curvature": calibration.get("capability_curvature", 0.0),
        "observation_count": calibration.get("observation_count", 0),
        "child_federation_status": child_result.get("status", ""),
        "child_federation_run_id": child_result.get("federation_run_id", ""),
        "child_evidence_digest": child_result.get("evidence_digest", ""),
        "effect_receipt_digest": child_result.get("effect_receipt_digest", ""),
        "next_wake_digest": child_result.get("next_wake_digest", ""),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
