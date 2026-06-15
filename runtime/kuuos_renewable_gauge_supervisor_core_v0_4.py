#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_open_horizon_telos_genesis_core_v0_1 import (
    BLOCKED as TELOS_BLOCKED,
    READY as TELOS_READY,
    ROOT_VERSION,
    build_open_horizon_telos_genesis,
)
from runtime.kuuos_open_horizon_commitment_gauge_core_v0_2 import (
    BLOCKED as GAUGE_BLOCKED,
    READY as GAUGE_READY,
    build_open_horizon_commitment_gauge,
)
from runtime.kuuos_active_gauge_intervention_loop_core_v0_3 import (
    BLOCKED as INTERVENTION_BLOCKED,
    READY as INTERVENTION_READY,
    REPLAYED as INTERVENTION_REPLAYED,
    build_active_gauge_intervention_loop,
)
from runtime.kuuos_active_gauge_intervention_types_v0_3 import (
    ADAPTER_PROFILE_VERSION,
)
from runtime.kuuos_renewable_gauge_supervisor_children_v0_4 import (
    build_gauge_packets,
    build_intervention_packets,
    build_telos_packets,
    derive_next_wake,
    wake_to_observation,
)
from runtime.kuuos_renewable_gauge_supervisor_types_v0_4 import (
    ALLOWED_WAKE_KINDS,
    BLOCKED,
    LEDGER_VERSION,
    LICENSE_VERSION,
    PLAN_VERSION,
    READY,
    RENEWAL_WAKE_KINDS,
    REPLAYED,
    REQUIRED_BOUNDARY,
    STATE_VERSION,
    VERSION,
    WAKE_VERSION,
    RenewableGaugeSupervisorResult,
    append_jsonl,
    as_list,
    clamp,
    contains_graph_keys,
    integer,
    mapping,
    plan_digest,
    read_json,
    read_jsonl,
    safe_root,
    sha,
    state_digest,
    valid_digest,
    wake_digest,
    without,
    write_json,
)


def _paths(root: pathlib.Path) -> dict[str, pathlib.Path]:
    return {
        "telos_state": root / "kuuos_open_horizon_telos_state_v0_1.json",
        "goal_set": root / "kuuos_open_horizon_goal_set_v0_1.json",
        "seed": root / "kuuos_open_horizon_commitment_seed_v0_1.json",
        "gauge_state": root / "kuuos_open_horizon_commitment_gauge_state_v0_2.json",
        "bundle": root / "kuuos_open_horizon_commitment_gauge_bundle_v0_2.json",
        "action": root / "kuuos_open_horizon_covariant_action_v0_2.json",
        "state": root / "kuuos_renewable_gauge_supervisor_state_v0_4.json",
        "next_wake": root / "kuuos_renewable_gauge_next_wake_v0_4.json",
        "receipt": root / "kuuos_renewable_gauge_supervisor_receipt_v0_4.json",
        "ledger": root / "kuuos_renewable_gauge_supervisor_ledger_v0_4.jsonl",
        "audit": root / "kuuos_renewable_gauge_supervisor_audit_v0_4.jsonl",
    }


def _validate_wake(wake: Mapping[str, Any], blockers: list[str]) -> None:
    if wake.get("version") != WAKE_VERSION:
        blockers.append("wake_event_version_invalid")
    if not valid_digest(wake, "wake_event_digest"):
        blockers.append("wake_event_digest_invalid")
    if not str(wake.get("wake_event_id", "")):
        blockers.append("wake_event_id_missing")
    if str(wake.get("wake_kind", "")) not in ALLOWED_WAKE_KINDS:
        blockers.append("wake_kind_invalid")
    if wake.get("telos_renewal_requested") not in {True, False}:
        blockers.append("telos_renewal_requested_invalid")
    if wake.get("intervention_requested") not in {True, False}:
        blockers.append("intervention_requested_invalid")


def _validate_root(root_packet: Mapping[str, Any], blockers: list[str]) -> None:
    if root_packet.get("version") != ROOT_VERSION:
        blockers.append("root_principles_version_invalid")
    if not valid_digest(root_packet, "root_principles_digest"):
        blockers.append("root_principles_digest_invalid")
    if root_packet.get("protected") is not True:
        blockers.append("root_principles_not_protected")
    if root_packet.get("self_rewrite_allowed") is not False:
        blockers.append("root_principles_self_rewrite_not_denied")


def _validate_profile(profile: Mapping[str, Any], blockers: list[str]) -> None:
    if profile.get("version") != ADAPTER_PROFILE_VERSION:
        blockers.append("adapter_profile_version_invalid")
    if not valid_digest(profile, "adapter_profile_digest"):
        blockers.append("adapter_profile_digest_invalid")
    if profile.get("backend") != "qi_local_execution_adapter_v0_2":
        blockers.append("adapter_backend_unsupported")


def _validate_plan(
    plan: Mapping[str, Any],
    wake: Mapping[str, Any],
    root_packet: Mapping[str, Any],
    profile: Mapping[str, Any],
    previous_state: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if plan.get("version") != PLAN_VERSION:
        blockers.append("supervisor_plan_version_invalid")
    if not valid_digest(plan, "supervisor_plan_digest"):
        blockers.append("supervisor_plan_digest_invalid")
    for field in ("supervisor_run_id", "agent_id"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field, expected in {
        "expected_wake_event_digest": wake.get("wake_event_digest"),
        "expected_root_principles_digest": root_packet.get("root_principles_digest"),
        "expected_adapter_profile_digest": profile.get("adapter_profile_digest"),
        "expected_previous_supervisor_state_digest": previous_state.get("supervisor_state_digest", ""),
    }.items():
        if plan.get(field, "") != expected:
            blockers.append(f"{field}_mismatch")
    for field, expected in REQUIRED_BOUNDARY.items():
        if mapping(plan.get("boundary")).get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    max_generated = integer(plan.get("max_generated_goals"), 0)
    max_selected = integer(plan.get("max_selected_goals"), 0)
    renewal_window = integer(plan.get("renewal_window_steps"), 0)
    max_sections = integer(plan.get("max_bundle_sections"), 0)
    max_new = integer(plan.get("max_new_sections_per_run"), 0)
    max_transports = integer(plan.get("max_transports_per_section"), 0)
    min_goal = clamp(plan.get("min_goal_score"), -1.0)
    min_scale = clamp(plan.get("min_action_scale"), -1.0)
    if not 1 <= max_generated <= 32:
        blockers.append("max_generated_goals_invalid")
    if not 1 <= max_selected <= min(max_generated, 8):
        blockers.append("max_selected_goals_invalid")
    if not 1 <= renewal_window <= 1000:
        blockers.append("renewal_window_steps_invalid")
    if not 2 <= max_sections <= 4096:
        blockers.append("max_bundle_sections_invalid")
    if not 1 <= max_new <= 32:
        blockers.append("max_new_sections_per_run_invalid")
    if not 1 <= max_transports <= 20:
        blockers.append("max_transports_per_section_invalid")
    if min_goal < 0.0:
        blockers.append("min_goal_score_invalid")
    if min_scale < 0.0 or min_scale > 0.25:
        blockers.append("min_action_scale_invalid")


def _validate_license(
    license_packet: Mapping[str, Any],
    plan: Mapping[str, Any],
    wake: Mapping[str, Any],
    root_packet: Mapping[str, Any],
    profile: Mapping[str, Any],
    blockers: list[str],
) -> None:
    if license_packet.get("version") != LICENSE_VERSION:
        blockers.append("supervisor_license_version_invalid")
    for field, expected in {
        "bound_plan_digest": plan.get("supervisor_plan_digest"),
        "bound_wake_event_digest": wake.get("wake_event_digest"),
        "bound_root_principles_digest": root_packet.get("root_principles_digest"),
        "bound_adapter_profile_digest": profile.get("adapter_profile_digest"),
    }.items():
        if license_packet.get(field) != expected:
            blockers.append(f"license_{field}_mismatch")
    for field in (
        "wake_consume_allowed", "telos_renewal_allowed", "gauge_sync_allowed",
        "local_intervention_allowed", "next_wake_write_allowed", "state_write_allowed",
        "ledger_append_allowed", "receipt_write_allowed", "audit_append_allowed",
    ):
        if license_packet.get(field) is not True:
            blockers.append(field.replace("allowed", "not_allowed"))
    if license_packet.get("external_network_effect_allowed") is not False:
        blockers.append("external_network_effect_not_denied")


def _replay_result(
    row: Mapping[str, Any], root: pathlib.Path, paths: Mapping[str, pathlib.Path]
) -> RenewableGaugeSupervisorResult:
    return RenewableGaugeSupervisorResult(
        VERSION,
        REPLAYED,
        str(row.get("packet_id", "")),
        str(row.get("supervisor_run_id", "")),
        integer(row.get("cycle_index"), 0),
        str(root),
        str(row.get("wake_event_id", "")),
        str(row.get("wake_kind", "")),
        bool(row.get("telos_renewal_applied")),
        integer(row.get("telos_generation"), 0),
        bool(row.get("gauge_synchronization_applied")),
        bool(row.get("intervention_applied")),
        str(row.get("intervention_status", "")),
        str(row.get("effect_receipt_digest", "")),
        bool(row.get("next_action_ready")),
        str(row.get("next_action_digest", "")),
        str(row.get("next_wake_kind", "")),
        str(row.get("next_wake_digest", "")),
        integer(row.get("local_steps_since_telos"), 0),
        integer(row.get("total_interventions"), 0),
        True,
        False,
        str(paths["state"]),
        str(paths["next_wake"]),
        str(paths["receipt"]),
        str(paths["ledger"]),
        str(paths["audit"]),
        [],
        ["supervisor_replay_no_new_local_effect"],
    )


def build_renewable_gauge_supervisor(
    *,
    runtime_context: Mapping[str, Any],
    wake_event: Mapping[str, Any],
    root_principles_packet: Mapping[str, Any],
    supervisor_plan: Mapping[str, Any],
    supervisor_license: Mapping[str, Any],
    adapter_profile: Mapping[str, Any],
) -> RenewableGaugeSupervisorResult:
    context = mapping(runtime_context)
    wake = mapping(wake_event)
    root_packet = mapping(root_principles_packet)
    plan = mapping(supervisor_plan)
    license_packet = mapping(supervisor_license)
    profile = mapping(adapter_profile)
    blockers: list[str] = []
    warnings: list[str] = []
    root = safe_root(context.get("runtime_root"), blockers)
    paths = _paths(root)
    previous_state = read_json(paths["state"])
    ledger = read_jsonl(paths["ledger"])
    run_id = str(plan.get("supervisor_run_id", ""))
    wake_sha = str(wake.get("wake_event_digest", ""))

    if any(row.get("_invalid") for row in ledger):
        blockers.append("supervisor_ledger_invalid")
    committed = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "committed" and row.get("supervisor_run_id") == run_id
        ),
        None,
    )
    if committed is not None:
        if committed.get("supervisor_plan_digest") == plan.get("supervisor_plan_digest"):
            return _replay_result(committed, root, paths)
        blockers.append("supervisor_run_id_reused_with_different_plan")

    if context.get("renewable_gauge_supervisor_enabled") is not True:
        blockers.append("renewable_gauge_supervisor_enabled_not_true")
    if context.get("execute_one_supervisor_cycle") is not True:
        blockers.append("execute_one_supervisor_cycle_not_true")
    _validate_wake(wake, blockers)
    _validate_root(root_packet, blockers)
    _validate_profile(profile, blockers)
    if previous_state and (
        previous_state.get("version") != STATE_VERSION
        or not valid_digest(previous_state, "supervisor_state_digest")
    ):
        blockers.append("previous_supervisor_state_invalid")
    _validate_plan(plan, wake, root_packet, profile, previous_state, blockers)
    _validate_license(license_packet, plan, wake, root_packet, profile, blockers)

    if any(
        row.get("phase") == "committed"
        and row.get("wake_event_digest") == wake_sha
        and row.get("supervisor_run_id") != run_id
        for row in ledger
    ):
        blockers.append("wake_event_already_consumed")
    pending_other = next(
        (
            row
            for row in ledger
            if row.get("phase") == "pending"
            and row.get("wake_event_digest") == wake_sha
            and row.get("supervisor_run_id") != run_id
        ),
        None,
    )
    if pending_other is not None:
        blockers.append("wake_event_claimed_by_pending_run")
    pending = next(
        (
            row
            for row in reversed(ledger)
            if row.get("phase") == "pending" and row.get("supervisor_run_id") == run_id
        ),
        None,
    )
    recovered_pending = pending is not None
    if recovered_pending:
        warnings.append("recovering_pending_supervisor_cycle")

    current_telos = read_json(paths["telos_state"])
    local_steps_before = integer(previous_state.get("local_steps_since_telos"), 0)
    wake_requests_renewal = (
        wake.get("telos_renewal_requested") is True
        or str(wake.get("wake_kind", "")) in RENEWAL_WAKE_KINDS
        or not current_telos
    )
    renewal_due = local_steps_before >= integer(plan.get("renewal_window_steps"), 3)
    renewal_needed = wake_requests_renewal or renewal_due
    if renewal_needed and not as_list(wake.get("signals")):
        blockers.append("telos_renewal_signals_missing")

    cycle_index = integer(previous_state.get("cycle_index"), 0) + 1
    packet_id = "kuuos-renewable-gauge-" + sha(
        {"run": run_id, "wake": wake_sha, "cycle": cycle_index}
    )[:18]
    if not blockers and pending is None:
        pending_record = {
            "version": LEDGER_VERSION,
            "phase": "pending",
            "packet_id": packet_id,
            "supervisor_run_id": run_id,
            "supervisor_plan_digest": plan.get("supervisor_plan_digest"),
            "wake_event_id": wake.get("wake_event_id"),
            "wake_event_digest": wake_sha,
            "wake_kind": wake.get("wake_kind"),
            "cycle_index": cycle_index,
            "pending_digest": "",
        }
        pending_record["pending_digest"] = sha(without(pending_record, "pending_digest"))
        append_jsonl(paths["ledger"], pending_record)

    telos_renewal_applied = False
    gauge_sync_applied = False
    intervention_applied = False
    intervention_status = "not_requested"
    effect_receipt_digest = ""

    if not blockers and renewal_needed:
        observation = wake_to_observation(wake)
        if current_telos.get("source_observation_digest") == observation.get("observation_digest"):
            telos_renewal_applied = True
            warnings.append("recovered_existing_telos_generation_for_wake")
        else:
            observation, telos_plan, telos_license = build_telos_packets(
                wake=wake,
                root_packet=root_packet,
                supervisor_plan=plan,
                current_telos_state=current_telos,
            )
            result = build_open_horizon_telos_genesis(
                runtime_context={
                    "runtime_root": str(root),
                    "open_horizon_telos_genesis_enabled": True,
                    "apply_open_horizon_telos_genesis": True,
                },
                observation_packet=observation,
                root_principles_packet=root_packet,
                telos_plan=telos_plan,
                telos_license=telos_license,
            )
            if result.status == TELOS_BLOCKED:
                blockers.extend([f"telos_{item}" for item in result.blockers])
            elif result.status == TELOS_READY:
                telos_renewal_applied = True
        current_telos = read_json(paths["telos_state"])

    goal_set = read_json(paths["goal_set"])
    seed = read_json(paths["seed"])
    gauge_state = read_json(paths["gauge_state"])
    bundle = read_json(paths["bundle"])
    gauge_needs_sync = bool(current_telos) and (
        not gauge_state
        or gauge_state.get("last_integrated_telos_state_digest")
        != current_telos.get("telos_state_digest")
    )
    if not blockers and gauge_needs_sync:
        gauge_plan, gauge_license = build_gauge_packets(
            runtime_root=root,
            supervisor_plan=plan,
            telos_state=current_telos,
            goal_set=goal_set,
            seed=seed,
            current_gauge_state=gauge_state,
        )
        result = build_open_horizon_commitment_gauge(
            runtime_context={
                "runtime_root": str(root),
                "open_horizon_commitment_gauge_enabled": True,
                "apply_open_horizon_commitment_gauge": True,
            },
            gauge_plan=gauge_plan,
            gauge_license=gauge_license,
        )
        if result.status == GAUGE_BLOCKED:
            blockers.extend([f"gauge_{item}" for item in result.blockers])
        elif result.status == GAUGE_READY:
            gauge_sync_applied = True
        gauge_state = read_json(paths["gauge_state"])
        bundle = read_json(paths["bundle"])

    action = read_json(paths["action"])
    if contains_graph_keys(bundle) or contains_graph_keys(action):
        blockers.append("graph_semantics_present")

    if not blockers and wake.get("intervention_requested") is True:
        if action.get("action_ready") is True:
            intervention_plan, intervention_license = build_intervention_packets(
                supervisor_plan=plan,
                adapter_profile=profile,
                gauge_state=gauge_state,
                bundle=bundle,
                action=action,
            )
            result = build_active_gauge_intervention_loop(
                runtime_context={
                    "runtime_root": str(root),
                    "active_gauge_intervention_enabled": True,
                    "execute_domain_intervention": True,
                    "allowed_domain_actions": as_list(context.get("allowed_domain_actions")),
                },
                intervention_plan=intervention_plan,
                intervention_license=intervention_license,
                adapter_profile=profile,
            )
            intervention_status = result.status
            if result.status == INTERVENTION_BLOCKED:
                blockers.extend([f"intervention_{item}" for item in result.blockers])
            elif result.status in {INTERVENTION_READY, INTERVENTION_REPLAYED}:
                intervention_applied = True
                effect_receipt_digest = result.effect_receipt_digest
        else:
            intervention_status = "no_covariant_action_ready"
            warnings.append("intervention_requested_without_ready_action")

    final_action = read_json(paths["action"])
    final_telos = read_json(paths["telos_state"])
    final_seed = read_json(paths["seed"])
    local_steps = 0 if telos_renewal_applied else local_steps_before
    if intervention_applied:
        local_steps += 1
    total_interventions = integer(previous_state.get("total_interventions"), 0) + (
        1 if intervention_applied else 0
    )
    total_renewals = integer(previous_state.get("total_telos_renewals"), 0) + (
        1 if telos_renewal_applied else 0
    )
    next_wake = derive_next_wake(
        supervisor_run_id=run_id,
        cycle_index=cycle_index,
        action=final_action,
        commitment_seed=final_seed,
    )

    status = READY if not blockers else BLOCKED
    if status == READY:
        state = {
            "version": STATE_VERSION,
            "supervisor_run_id": run_id,
            "cycle_index": cycle_index,
            "previous_supervisor_state_digest": previous_state.get("supervisor_state_digest", ""),
            "wake_event_digest": wake_sha,
            "telos_state_digest": final_telos.get("telos_state_digest", ""),
            "telos_generation": integer(final_telos.get("generation_index"), 0),
            "gauge_state_digest": read_json(paths["gauge_state"]).get("gauge_state_digest", ""),
            "next_action_digest": final_action.get("covariant_action_digest", ""),
            "next_wake_digest": next_wake.get("next_wake_digest", ""),
            "local_steps_since_telos": local_steps,
            "total_interventions": total_interventions,
            "total_telos_renewals": total_renewals,
            "one_finite_cycle_completed": True,
            "local_intervention_count": 1 if intervention_applied else 0,
            "local_intervention_limit": 1,
            "renewable_horizon": True,
            "root_principles_unchanged": True,
            "non_markov_holonomy_preserved": True,
            "epoch": int(time.time()),
        }
        state["supervisor_state_digest"] = state_digest(state)
        write_json(paths["state"], state)
        write_json(paths["next_wake"], next_wake)
        committed_record = {
            "version": LEDGER_VERSION,
            "phase": "committed",
            "packet_id": packet_id,
            "supervisor_run_id": run_id,
            "supervisor_plan_digest": plan.get("supervisor_plan_digest"),
            "wake_event_id": wake.get("wake_event_id"),
            "wake_event_digest": wake_sha,
            "wake_kind": wake.get("wake_kind"),
            "cycle_index": cycle_index,
            "telos_renewal_applied": telos_renewal_applied,
            "telos_generation": state["telos_generation"],
            "gauge_synchronization_applied": gauge_sync_applied,
            "intervention_applied": intervention_applied,
            "intervention_status": intervention_status,
            "effect_receipt_digest": effect_receipt_digest,
            "next_action_ready": final_action.get("action_ready") is True,
            "next_action_digest": final_action.get("covariant_action_digest", ""),
            "next_wake_kind": next_wake.get("wake_kind"),
            "next_wake_digest": next_wake.get("next_wake_digest"),
            "local_steps_since_telos": local_steps,
            "total_interventions": total_interventions,
            "supervisor_state_digest": state["supervisor_state_digest"],
            "record_digest": "",
        }
        committed_record["record_digest"] = sha(without(committed_record, "record_digest"))
        append_jsonl(paths["ledger"], committed_record)

    receipt = {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "supervisor_run_id": run_id,
        "cycle_index": cycle_index,
        "wake_event_id": wake.get("wake_event_id", ""),
        "wake_kind": wake.get("wake_kind", ""),
        "telos_renewal_applied": telos_renewal_applied,
        "telos_generation": integer(final_telos.get("generation_index"), 0),
        "gauge_synchronization_applied": gauge_sync_applied,
        "intervention_applied": intervention_applied,
        "intervention_status": intervention_status,
        "effect_receipt_digest": effect_receipt_digest,
        "next_action_ready": final_action.get("action_ready") is True,
        "next_action_digest": final_action.get("covariant_action_digest", ""),
        "next_wake_kind": next_wake.get("wake_kind", ""),
        "next_wake_digest": next_wake.get("next_wake_digest", ""),
        "local_steps_since_telos": local_steps,
        "total_interventions": total_interventions,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_packet.get("receipt_write_allowed") is True:
        write_json(paths["receipt"], receipt)
    if license_packet.get("audit_append_allowed") is True:
        append_jsonl(paths["audit"], {**receipt, "audit_record_digest": sha(receipt)})

    return RenewableGaugeSupervisorResult(
        VERSION,
        status,
        packet_id,
        run_id,
        cycle_index,
        str(root),
        str(wake.get("wake_event_id", "")),
        str(wake.get("wake_kind", "")),
        telos_renewal_applied,
        integer(final_telos.get("generation_index"), 0),
        gauge_sync_applied,
        intervention_applied,
        intervention_status,
        effect_receipt_digest,
        final_action.get("action_ready") is True,
        str(final_action.get("covariant_action_digest", "")),
        str(next_wake.get("wake_kind", "")),
        str(next_wake.get("next_wake_digest", "")),
        local_steps,
        total_interventions,
        False,
        recovered_pending,
        str(paths["state"]),
        str(paths["next_wake"]),
        str(paths["receipt"]),
        str(paths["ledger"]),
        str(paths["audit"]),
        blockers,
        warnings,
    )
