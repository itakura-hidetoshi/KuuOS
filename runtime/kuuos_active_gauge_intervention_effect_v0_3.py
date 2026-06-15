#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    EFFECT_VERSION,
    LICENSE_VERSION as GAUGE_LICENSE_VERSION,
    PLAN_VERSION as GAUGE_PLAN_VERSION,
    REQUIRED_BOUNDARY as GAUGE_REQUIRED_BOUNDARY,
    effect_digest,
    plan_digest as gauge_plan_digest,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import clamp, read_json, sha


def effect_metrics(
    routed_action: str, action_scale: float, adapter: Mapping[str, Any]
) -> tuple[str, str, float, float, float, float, float]:
    confidence = 0.65 if adapter.get("idempotent_replay") is True else 0.92
    if routed_action == "advance_tick":
        return (
            "success", "continue", round(max(0.08, action_scale * 0.35), 6),
            round(min(1.0, 0.62 + action_scale * 0.28), 6), 0.01, 0.96, confidence,
        )
    if routed_action == "observe":
        return ("partial", "reobserve", 0.06, 0.42, 0.01, 0.99, confidence)
    if routed_action == "handover":
        return ("partial", "expand", 0.12, 0.52, 0.02, 0.98, confidence)
    if routed_action in {"notify", "ticket"}:
        return ("partial", "continue", 0.10, 0.48, 0.02, 0.97, confidence)
    if routed_action == "hold":
        return ("blocked", "reobserve", 0.0, 0.15, 0.03, 0.99, confidence)
    return ("blocked", "repair", 0.0, 0.05, 0.08, 0.98, confidence)


def build_effect_receipt(
    action: Mapping[str, Any],
    routed_action: str,
    adapter: Mapping[str, Any],
    intervention_id: str,
) -> dict[str, Any]:
    outcome, continuation, progress, benefit, harm, recoverability, confidence = effect_metrics(
        routed_action, clamp(action.get("action_scale")), adapter
    )
    receipt = {
        "version": EFFECT_VERSION,
        "effect_receipt_id": "effect-" + sha(
            {"action": action.get("covariant_action_digest"), "execution": adapter.get("local_execution_id")}
        )[:18],
        "source_action_digest": action.get("covariant_action_digest"),
        "action_id": action.get("action_id"),
        "section_id": action.get("section_id"),
        "outcome": outcome,
        "continuation_signal": continuation,
        "progress_delta": progress,
        "observed_benefit": benefit,
        "observed_harm": harm,
        "recoverability": recoverability,
        "confidence": confidence,
        "result_digest": adapter.get("ledger_entry_digest"),
        "domain_adapter_id": adapter.get("adapter_version"),
        "domain_action": routed_action,
        "local_execution_id": adapter.get("local_execution_id"),
        "intervention_id": intervention_id,
        "adapter_execution_committed": adapter.get("execution_committed") is True,
        "adapter_idempotent_replay": adapter.get("idempotent_replay") is True,
    }
    receipt["effect_receipt_digest"] = effect_digest(receipt)
    return receipt


def build_gauge_reentry_packets(
    root: pathlib.Path,
    plan: Mapping[str, Any],
    effect: Mapping[str, Any],
    previous_state: Mapping[str, Any],
    max_sections: int,
    max_new: int,
    max_transports: int,
    min_scale: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    telos = read_json(root / "kuuos_open_horizon_telos_state_v0_1.json")
    goals = read_json(root / "kuuos_open_horizon_goal_set_v0_1.json")
    seed = read_json(root / "kuuos_open_horizon_commitment_seed_v0_1.json")
    child = {
        "version": GAUGE_PLAN_VERSION,
        "gauge_run_id": str(plan.get("gauge_reentry_run_id")),
        "agent_id": str(plan.get("agent_id")),
        "expected_telos_state_digest": telos.get("telos_state_digest"),
        "expected_goal_set_digest": goals.get("goal_set_digest"),
        "expected_commitment_seed_digest": seed.get("commitment_seed_digest"),
        "expected_previous_gauge_state_digest": previous_state.get("gauge_state_digest"),
        "expected_effect_receipt_digest": effect.get("effect_receipt_digest"),
        "max_bundle_sections": max_sections,
        "max_new_sections_per_run": max_new,
        "max_transports_per_section": max_transports,
        "min_action_scale": min_scale,
        "boundary": dict(GAUGE_REQUIRED_BOUNDARY),
    }
    child["gauge_plan_digest"] = gauge_plan_digest(child)
    license_packet = {
        "version": GAUGE_LICENSE_VERSION,
        "bound_plan_digest": child["gauge_plan_digest"],
        "bound_telos_state_digest": telos.get("telos_state_digest"),
        "bound_goal_set_digest": goals.get("goal_set_digest"),
        "bound_commitment_seed_digest": seed.get("commitment_seed_digest"),
        "bound_effect_receipt_digest": effect.get("effect_receipt_digest"),
    }
    for field in (
        "source_read_allowed", "bundle_initialize_allowed", "telos_section_extension_allowed",
        "parallel_transport_allowed", "curvature_update_allowed", "local_gauge_correction_allowed",
        "holonomy_append_allowed", "covariant_action_prepare_allowed", "state_write_allowed",
        "bundle_write_allowed", "action_write_allowed", "ledger_append_allowed",
        "receipt_write_allowed", "audit_append_allowed",
    ):
        license_packet[field] = True
    return child, license_packet
