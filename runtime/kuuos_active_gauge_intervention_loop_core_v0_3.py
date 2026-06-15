#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    BLOCKED as GAUGE_BLOCKED,
    READY as GAUGE_READY,
    build_open_horizon_commitment_gauge,
)
from runtime.kuuos_active_gauge_intervention_effect_v0_3 import (
    build_effect_receipt,
    build_gauge_reentry_packets,
)
from runtime.kuuos_active_gauge_intervention_local_adapter_v0_3 import (
    execute_local_adapter,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    ADAPTER_PROFILE_VERSION,
    BLOCKED,
    LEDGER_VERSION,
    LICENSE_VERSION,
    LOCAL_ACTIONS,
    PLAN_VERSION,
    READY,
    REPLAYED,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    VERSION,
    ActiveGaugeInterventionResult,
    append_jsonl,
    as_list,
    mapping,
    plan_digest,
    profile_digest,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    state_digest,
    valid_digest,
    without,
    write_json,
)
from runtime.kuuos_active_gauge_intervention_validation_v0_3 import (
    route_action,
    validate_license,
    validate_plan,
    validate_profile,
    validate_upstream,
)


def _paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "gauge_state": root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "bundle": root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json",
        "action": root / "kuuos_open_horizon_covariant_action_v0_2.json",
        "state": root / "kuuos_active_gauge_intervention_state_v0_3.json",
        "effect": root / "kuuos_active_gauge_effect_receipt_v0_3.json",
        "receipt": root / "kuuos_active_gauge_intervention_receipt_v0_3.json",
        "ledger": root / "kuuos_active_gauge_intervention_ledger_v0_3.jsonl",
        "audit": root / "kuuos_active_gauge_intervention_audit_v0_3.jsonl",
    }


def _replayed_result(row: Mapping[str, Any], root: pathlib.Path, p: Mapping[str, pathlib.Path]) -> ActiveGaugeInterventionResult:
    return ActiveGaugeInterventionResult(
        VERSION, REPLAYED, str(row.get("packet_id", "")), str(row.get("intervention_run_id", "")),
        str(row.get("intervention_id", "")), str(root), str(row.get("adapter_id", "")),
        str(row.get("covariant_step_kind", "")), str(row.get("routed_domain_action", "")),
        str(row.get("source_action_digest", "")), bool(row.get("local_execution_committed")),
        str(row.get("local_execution_id", "")), bool(row.get("effect_receipt_ready")),
        str(row.get("effect_receipt_digest", "")), str(row.get("effect_outcome", "")),
        bool(row.get("curvature_reentry_applied")), str(row.get("gauge_reentry_status", "")),
        bool(row.get("next_action_ready")), str(row.get("next_covariant_step_kind", "")),
        str(row.get("next_action_digest", "")), True, False, str(p["state"]), str(p["effect"]),
        str(p["receipt"]), str(p["ledger"]), str(p["audit"]), [],
        ["idempotent_intervention_replay_no_new_effect"],
    )


def _pending_record(
    *, run_id: str, intervention_id: str, packet_id: str, adapter_id: str,
    plan: Mapping[str, Any], profile: Mapping[str, Any], action: Mapping[str, Any], routed: str,
) -> dict[str, Any]:
    record = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "intervention_run_id": run_id,
        "intervention_id": intervention_id,
        "packet_id": packet_id,
        "adapter_id": adapter_id,
        "intervention_plan_digest": plan.get("intervention_plan_digest"),
        "adapter_profile_digest": profile.get("adapter_profile_digest"),
        "gauge_reentry_run_id": plan.get("gauge_reentry_run_id"),
        "covariant_step_kind": action.get("covariant_step_kind"),
        "routed_domain_action": routed,
        "source_action_digest": action.get("covariant_action_digest"),
        "pending_digest": "",
    }
    record["pending_digest"] = sha(without(record, "pending_digest"))
    return record


def _committed_record(
    *, run_id: str, intervention_id: str, packet_id: str, adapter_id: str,
    plan: Mapping[str, Any], profile: Mapping[str, Any], action: Mapping[str, Any], routed: str,
    adapter: Mapping[str, Any], effect: Mapping[str, Any], gauge_result: Mapping[str, Any],
    next_action: Mapping[str, Any], intervention_state_digest: str,
) -> dict[str, Any]:
    record = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "intervention_run_id": run_id,
        "intervention_id": intervention_id,
        "packet_id": packet_id,
        "adapter_id": adapter_id,
        "intervention_plan_digest": plan.get("intervention_plan_digest"),
        "adapter_profile_digest": profile.get("adapter_profile_digest"),
        "gauge_reentry_run_id": plan.get("gauge_reentry_run_id"),
        "covariant_step_kind": action.get("covariant_step_kind"),
        "routed_domain_action": routed,
        "source_action_digest": action.get("covariant_action_digest"),
        "local_execution_committed": adapter.get("execution_committed") is True,
        "local_execution_id": adapter.get("local_execution_id", ""),
        "effect_receipt_ready": True,
        "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        "effect_outcome": effect.get("outcome", ""),
        "curvature_reentry_applied": gauge_result.get("status") == GAUGE_READY,
        "gauge_reentry_status": gauge_result.get("status", ""),
        "next_action_ready": next_action.get("action_ready") is True,
        "next_covariant_step_kind": next_action.get("covariant_step_kind", "none"),
        "next_action_digest": next_action.get("covariant_action_digest", ""),
        "intervention_state_digest": intervention_state_digest,
        "record_digest": "",
    }
    record["record_digest"] = sha(without(record, "record_digest"))
    return record


def build_active_gauge_intervention_loop(
    *,
    runtime_context: Mapping[str, Any],
    intervention_plan: Mapping[str, Any],
    intervention_license: Mapping[str, Any],
    adapter_profile: Mapping[str, Any],
) -> ActiveGaugeInterventionResult:
    context, plan = mapping(runtime_context), mapping(intervention_plan)
    license_packet, profile = mapping(intervention_license), mapping(adapter_profile)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    p = _paths(root)
    run_id = str(plan.get("intervention_run_id", ""))
    ledger = read_jsonl(p["ledger"])
    if any(row.get("_invalid") for row in ledger):
        blockers.append("intervention_ledger_invalid")

    committed = next((row for row in reversed(ledger) if row.get("phase") == "committed" and row.get("intervention_run_id") == run_id), None)
    if committed is not None:
        if valid_digest(plan, "intervention_plan_digest") and committed.get("intervention_plan_digest") == plan.get("intervention_plan_digest"):
            return _replayed_result(committed, root, p)
        blockers.append("intervention_run_id_reused_with_different_plan")

    gauge_state, bundle, action = read_json(p["gauge_state"]), read_json(p["bundle"]), read_json(p["action"])
    if context.get("active_gauge_intervention_enabled") is not True:
        blockers.append("active_gauge_intervention_enabled_not_true")
    if context.get("execute_domain_intervention") is not True:
        blockers.append("execute_domain_intervention_not_true")
    max_sections, max_new, max_transports, min_scale = validate_plan(plan, blockers)
    validate_profile(profile, plan, blockers)
    validate_upstream(gauge_state, bundle, action, plan, blockers)
    validate_license(license_packet, plan, profile, gauge_state, bundle, action, blockers)
    routed = route_action(action, plan, profile, context, blockers)

    source_digest = str(action.get("covariant_action_digest", ""))
    if any(row.get("phase") == "committed" and row.get("source_action_digest") == source_digest for row in ledger):
        blockers.append("covariant_action_already_consumed")
    pending = next((row for row in reversed(ledger) if row.get("phase") == "pending" and row.get("intervention_run_id") == run_id), None)
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_intervention_run")

    adapter_id = str(profile.get("adapter_id", ""))
    intervention_id = "intervention-" + sha({"run": run_id, "action": source_digest, "adapter": adapter_id, "route": routed})[:18]
    packet_id = "kuuos-active-gauge-" + sha({"intervention": intervention_id})[:18]
    adapter: dict[str, Any] = {}
    effect: dict[str, Any] = {}
    gauge_result: dict[str, Any] = {}
    next_action: dict[str, Any] = {}

    if not blockers:
        if pending is None:
            append_jsonl(p["ledger"], _pending_record(
                run_id=run_id, intervention_id=intervention_id, packet_id=packet_id,
                adapter_id=adapter_id, plan=plan, profile=profile, action=action, routed=routed,
            ))
        adapter = execute_local_adapter(
            root=root, action=action, routed_action=routed, intervention_id=intervention_id,
            allowed_domain_actions=as_list(context.get("allowed_domain_actions")),
        )
        if adapter.get("adapter_status") == "QI_LOCAL_EXECUTION_ADAPTER_BLOCKED":
            blockers.extend([f"domain_adapter_{item}" for item in as_list(adapter.get("blockers"))])
        else:
            warnings.extend([str(item) for item in as_list(adapter.get("warnings"))])

    if not blockers and adapter.get("execution_committed") is True:
        effect = build_effect_receipt(action, routed, adapter, intervention_id)
        write_json(p["effect"], effect)
        child_plan, child_license = build_gauge_reentry_packets(
            root, plan, effect, gauge_state, max_sections, max_new, max_transports, min_scale
        )
        raw = build_open_horizon_commitment_gauge(
            runtime_context={
                "runtime_root": str(root),
                "open_horizon_commitment_gauge_enabled": True,
                "apply_open_horizon_commitment_gauge": True,
            },
            gauge_plan=child_plan,
            gauge_license=child_license,
            effect_receipt=effect,
        )
        gauge_result = raw.to_dict()
        if gauge_result.get("status") == GAUGE_BLOCKED:
            blockers.extend([f"gauge_reentry_{item}" for item in as_list(gauge_result.get("blockers"))])
        else:
            next_action = read_json(p["action"])

    reentered = gauge_result.get("status") == GAUGE_READY
    status = READY if not blockers and reentered else BLOCKED
    if status == READY:
        next_gauge_state = read_json(p["gauge_state"])
        state = {
            "version": STATE_VERSION,
            "intervention_run_id": run_id,
            "intervention_id": intervention_id,
            "source_action_digest": source_digest,
            "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
            "gauge_reentry_state_digest": next_gauge_state.get("gauge_state_digest", ""),
            "next_action_digest": next_action.get("covariant_action_digest", ""),
            "loop_closed": True,
            "next_action_ready": next_action.get("action_ready") is True,
            "non_markov_holonomy_preserved": True,
            "epoch": int(time.time()),
        }
        state["intervention_state_digest"] = state_digest(state)
        write_json(p["state"], state)
        append_jsonl(p["ledger"], _committed_record(
            run_id=run_id, intervention_id=intervention_id, packet_id=packet_id,
            adapter_id=adapter_id, plan=plan, profile=profile, action=action, routed=routed,
            adapter=adapter, effect=effect, gauge_result=gauge_result, next_action=next_action,
            intervention_state_digest=state["intervention_state_digest"],
        ))

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "intervention_run_id": run_id,
        "intervention_id": intervention_id,
        "adapter_id": adapter_id,
        "covariant_step_kind": action.get("covariant_step_kind", ""),
        "routed_domain_action": routed,
        "source_action_digest": source_digest,
        "local_execution_committed": adapter.get("execution_committed") is True,
        "local_execution_id": adapter.get("local_execution_id", ""),
        "effect_receipt_ready": bool(effect),
        "effect_receipt_digest": effect.get("effect_receipt_digest", ""),
        "effect_outcome": effect.get("outcome", ""),
        "curvature_reentry_applied": reentered,
        "gauge_reentry_status": gauge_result.get("status", ""),
        "next_action_ready": next_action.get("action_ready") is True,
        "next_covariant_step_kind": next_action.get("covariant_step_kind", "none"),
        "next_action_digest": next_action.get("covariant_action_digest", ""),
        "loop_closed": status == READY,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_packet.get("receipt_write_allowed") is True:
        write_json(p["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(p["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    return ActiveGaugeInterventionResult(
        VERSION, status, packet_id, run_id, intervention_id, str(root), adapter_id,
        str(action.get("covariant_step_kind", "")), routed, source_digest,
        adapter.get("execution_committed") is True, str(adapter.get("local_execution_id", "")),
        bool(effect), str(effect.get("effect_receipt_digest", "")), str(effect.get("outcome", "")),
        reentered, str(gauge_result.get("status", "")), next_action.get("action_ready") is True,
        str(next_action.get("covariant_step_kind", "none")), str(next_action.get("covariant_action_digest", "")),
        False, recovered_pending, str(p["state"]), str(p["effect"]), str(p["receipt"]),
        str(p["ledger"]), str(p["audit"]), blockers, warnings,
    )
