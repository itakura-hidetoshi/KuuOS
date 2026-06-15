#!/usr/bin/env python3
from __future__ import annotations

import pathlib
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_qi_local_execution_adapter_v0_2 import (
    build_qi_local_execution_adapter,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import sha


def build_local_adapter_packets(
    action: Mapping[str, Any], routed_action: str, intervention_id: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    engine_id = "gauge-engine-" + sha(
        {"action": action.get("covariant_action_digest"), "route": routed_action}
    )[:16]
    finality_id = "gauge-finality-" + sha({"engine": engine_id})[:16]
    engine = {
        "engine_status": "QI_AUTONOMOUS_EXECUTION_ENGINE_READY",
        "engine_packet_id": engine_id,
        "selected_action": routed_action,
        "execution_intent_staged": True,
        "execution_committed": False,
        "execution_intent_packet": {
            "engine_packet_id": engine_id,
            "selected_action": routed_action,
            "source_covariant_action_digest": action.get("covariant_action_digest"),
            "source_section_id": action.get("section_id"),
            "source_goal_id": action.get("goal_id"),
            "action_scale": action.get("action_scale"),
            "intervention_id": intervention_id,
        },
    }
    health = {
        "chain_status": "QI_EXECUTION_HEALTH_PACKET_CHAIN_READY",
        "finality_packet_id": finality_id,
        "finality_packet": {
            "packet_status": "QI_EXECUTION_HEALTH_FINALITY_PACKET_READY",
            "packet_id": finality_id,
        },
    }
    local_license = {
        "license_status": "QI_LOCAL_EXECUTION_LICENSE_READY",
        "local_runtime_state_write_allowed": True,
        "local_execution_ledger_append_allowed": True,
        "local_outbox_append_allowed": True,
        "external_side_effects_allowed": False,
    }
    return engine, health, local_license


def execute_local_adapter(
    *,
    root: pathlib.Path,
    action: Mapping[str, Any],
    routed_action: str,
    intervention_id: str,
    allowed_domain_actions: list[Any],
) -> dict[str, Any]:
    engine, health, local_license = build_local_adapter_packets(
        action, routed_action, intervention_id
    )
    result = build_qi_local_execution_adapter(
        engine_packet=engine,
        health_packet_chain=health,
        execution_license_packet=local_license,
        runtime_context={
            "runtime_root": str(root),
            "qi_local_execution_adapter_enabled": True,
            "commit_local_effects": True,
            "allowed_actions": sorted({str(item) for item in allowed_domain_actions}),
            "execution_nonce": str(action.get("covariant_action_digest", "")),
        },
    )
    return result.to_dict()
