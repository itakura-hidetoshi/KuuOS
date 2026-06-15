#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_adapter_portfolio_shadow_types_v0_7 import (
    LEDGER_VERSION,
    REPLAYED,
    STATE_VERSION,
    VERSION,
    AdapterPortfolioShadowResult,
    integer,
    sha,
    state_digest,
    without,
)


def paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "capability_state": root / "kuuos_adapter_capability_state_v0_6.json",
        "capability_bundle": root / "kuuos_adapter_capability_bundle_v0_6.json",
        "capability_selection": root / "kuuos_adapter_capability_selection_v0_6.json",
        "capability_calibration": root / "kuuos_adapter_capability_calibration_v0_6.json",
        "intervention_receipt": root / "kuuos_active_gauge_intervention_receipt_v0_3.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "bundle": root / "kuuos_adapter_portfolio_bundle_v0_7.json",
        "selection": root / "kuuos_adapter_portfolio_selection_v0_7.json",
        "projection": root / "kuuos_adapter_shadow_projection_v0_7.json",
        "resolution": root / "kuuos_adapter_shadow_resolution_v0_7.json",
        "state": root / "kuuos_adapter_portfolio_state_v0_7.json",
        "receipt": root / "kuuos_adapter_portfolio_receipt_v0_7.json",
        "ledger": root / "kuuos_adapter_portfolio_ledger_v0_7.jsonl",
        "audit": root / "kuuos_adapter_portfolio_audit_v0_7.jsonl",
    }


def replay_result(
    row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]
) -> AdapterPortfolioShadowResult:
    return AdapterPortfolioShadowResult(
        version=VERSION,
        status=REPLAYED,
        packet_id=str(row.get("packet_id", "")),
        portfolio_run_id=str(row.get("portfolio_run_id", "")),
        cycle_index=integer(row.get("cycle_index"), 0),
        runtime_root=str(root),
        context_key=str(row.get("context_key", "")),
        live_adapter_id=str(row.get("live_adapter_id", "")),
        live_adapter_profile_digest=str(
            row.get("live_adapter_profile_digest", "")
        ),
        live_base_score=float(row.get("live_base_score", 0.0)),
        live_portfolio_adjustment=float(
            row.get("live_portfolio_adjustment", 0.0)
        ),
        live_adjusted_score=float(row.get("live_adjusted_score", 0.0)),
        live_observed_utility=float(row.get("live_observed_utility", 0.0)),
        shadow_projection_count=integer(row.get("shadow_projection_count"), 0),
        resolved_shadow_count=integer(row.get("resolved_shadow_count"), 0),
        pending_shadow_count=integer(row.get("pending_shadow_count"), 0),
        child_capability_status=str(row.get("child_capability_status", "")),
        child_capability_run_id=str(row.get("child_capability_run_id", "")),
        live_effect_receipt_digest=str(
            row.get("live_effect_receipt_digest", "")
        ),
        portfolio_bundle_digest=str(row.get("portfolio_bundle_digest", "")),
        idempotent_replay=True,
        recovered_pending_run=False,
        state_path=str(p["state"]),
        bundle_path=str(p["bundle"]),
        selection_path=str(p["selection"]),
        projection_path=str(p["projection"]),
        resolution_path=str(p["resolution"]),
        receipt_path=str(p["receipt"]),
        ledger_path=str(p["ledger"]),
        audit_path=str(p["audit"]),
        blockers=[],
        warnings=["portfolio_run_replay_no_new_live_or_shadow_update"],
    )


def pending_record(
    *,
    packet_id: str,
    run_id: str,
    plan: Mapping[str, Any],
    source_batch_digest: str,
    previous_capability_state_digest: str,
    previous_capability_bundle_digest: str,
    previous_portfolio_state_digest: str,
    previous_portfolio_bundle_digest: str,
    selection: Mapping[str, Any],
    cycle_index: int,
) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "portfolio_run_id": run_id,
        "portfolio_plan_digest": plan.get("portfolio_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_capability_state_digest": previous_capability_state_digest,
        "previous_capability_bundle_digest": previous_capability_bundle_digest,
        "previous_portfolio_state_digest": previous_portfolio_state_digest,
        "previous_portfolio_bundle_digest": previous_portfolio_bundle_digest,
        "portfolio_selection_digest": selection.get(
            "portfolio_selection_digest", ""
        ),
        "live_adapter_id": selection.get("live_adapter_id", ""),
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
    selection: Mapping[str, Any],
    projection: Mapping[str, Any],
    resolution: Mapping[str, Any],
    bundle: Mapping[str, Any],
    child_result: Mapping[str, Any],
    live_observed_utility: float,
    live_effect_receipt_digest: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    resolved_count = 1 if resolution.get("resolved") is True else 0
    state = {
        "version": STATE_VERSION,
        "portfolio_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_portfolio_state_digest": previous_state.get(
            "portfolio_state_digest", ""
        ),
        "portfolio_bundle_digest": bundle.get("portfolio_bundle_digest", ""),
        "portfolio_selection_digest": selection.get(
            "portfolio_selection_digest", ""
        ),
        "shadow_projection_digest": projection.get(
            "shadow_projection_digest", ""
        ),
        "shadow_resolution_digest": resolution.get(
            "shadow_resolution_digest", ""
        ),
        "live_adapter_id": selection.get("live_adapter_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "total_live_cycles": integer(previous_state.get("total_live_cycles"), 0)
        + 1,
        "total_shadow_projections": integer(
            previous_state.get("total_shadow_projections"), 0
        )
        + integer(projection.get("projection_count"), 0),
        "total_shadow_resolutions": integer(
            previous_state.get("total_shadow_resolutions"), 0
        )
        + resolved_count,
        "shadow_execution_count": 0,
        "shadow_prediction_not_truth": True,
        "epoch": int(time.time()),
    }
    state["portfolio_state_digest"] = state_digest(state)
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "portfolio_run_id": run_id,
        "portfolio_plan_digest": plan.get("portfolio_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": selection.get("context_key", ""),
        "live_adapter_id": selection.get("live_adapter_id", ""),
        "live_adapter_profile_digest": selection.get(
            "live_adapter_profile_digest", ""
        ),
        "live_base_score": selection.get("live_base_score", 0.0),
        "live_portfolio_adjustment": selection.get(
            "live_portfolio_adjustment", 0.0
        ),
        "live_adjusted_score": selection.get("live_adjusted_score", 0.0),
        "live_observed_utility": round(live_observed_utility, 6),
        "shadow_projection_count": projection.get("projection_count", 0),
        "resolved_shadow_count": resolved_count,
        "pending_shadow_count": len(bundle.get("pending_predictions", [])),
        "child_capability_status": child_result.get("status", ""),
        "child_capability_run_id": child_result.get("capability_run_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "portfolio_bundle_digest": bundle.get("portfolio_bundle_digest", ""),
        "portfolio_state_digest": state.get("portfolio_state_digest", ""),
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
    selection: Mapping[str, Any],
    projection: Mapping[str, Any],
    resolution: Mapping[str, Any],
    bundle: Mapping[str, Any],
    child_result: Mapping[str, Any],
    live_observed_utility: float,
    live_effect_receipt_digest: str,
    blockers: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "portfolio_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": selection.get("context_key", ""),
        "live_adapter_id": selection.get("live_adapter_id", ""),
        "live_adapter_profile_digest": selection.get(
            "live_adapter_profile_digest", ""
        ),
        "live_base_score": selection.get("live_base_score", 0.0),
        "live_portfolio_adjustment": selection.get(
            "live_portfolio_adjustment", 0.0
        ),
        "live_adjusted_score": selection.get("live_adjusted_score", 0.0),
        "live_observed_utility": round(live_observed_utility, 6),
        "shadow_projection_count": projection.get("projection_count", 0),
        "resolved_shadow_count": 1 if resolution.get("resolved") is True else 0,
        "pending_shadow_count": len(bundle.get("pending_predictions", [])),
        "child_capability_status": child_result.get("status", ""),
        "child_capability_run_id": child_result.get("capability_run_id", ""),
        "live_effect_receipt_digest": live_effect_receipt_digest,
        "portfolio_bundle_digest": bundle.get("portfolio_bundle_digest", ""),
        "shadow_non_actuating": True,
        "shadow_prediction_not_truth": True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
