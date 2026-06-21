from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_event_wakeup_control_resource_kernel_v0_25 import (
    apply_event,
    build_control_command,
    build_event,
    build_initial_state,
    build_resource_envelope,
    build_status_snapshot,
    build_trigger_event,
    validate_state,
)
from runtime.kuuos_event_wakeup_control_resource_store_v0_25 import (
    EventWakeupStore,
    EventWakeupStoreError,
)
from runtime.kuuos_transactional_effect_scenarios_v0_24 import _confirmed


def _resources(
    *,
    tokens: int,
    api_calls: int,
    cost: int,
    storage: int,
    worker: int,
) -> dict[str, int]:
    return {
        "tokens": tokens,
        "api_calls": api_calls,
        "cost_microunits": cost,
        "storage_bytes": storage,
        "worker_millis": worker,
    }


def _initial(
    root: Path,
    *,
    mission_id: str,
    remaining: Mapping[str, int] | None = None,
    hard_limits: Mapping[str, int] | None = None,
    renewable: bool = True,
    remaining_cycles: int = 5,
) -> tuple[dict[str, Any], EventWakeupStore]:
    confirmed, _, _ = _confirmed(root / "source-transaction")
    caps = _resources(
        tokens=10_000,
        api_calls=1_000,
        cost=1_000_000,
        storage=10_000_000,
        worker=10_000_000,
    )
    limits = dict(
        hard_limits
        or _resources(
            tokens=1_000,
            api_calls=100,
            cost=100_000,
            storage=1_000_000,
            worker=1_000_000,
        )
    )
    available = dict(remaining or limits)
    envelope = build_resource_envelope(
        envelope_id=mission_id + "-resources",
        mission_id=mission_id,
        authorized_by_digest=sha(mission_id + "-resource-authority"),
        allowed_model_tiers=["small", "standard", "advanced"],
        preferred_model_tier="advanced",
        governance_caps=caps,
        hard_limits=limits,
        reserve_floors=_resources(
            tokens=100,
            api_calls=10,
            cost=10_000,
            storage=100_000,
            worker=100_000,
        ),
        remaining=available,
        max_cycles=10,
        remaining_cycles=remaining_cycles,
        renewable=renewable,
        expires_at_ms=1_000_000,
    )
    state = build_initial_state(
        mission_id=mission_id,
        lineage_id=mission_id + "-lineage",
        source_transaction_final_receipt=confirmed["final_receipt"],
        resource_envelope=envelope,
        initialized_at_ms=200_000,
    )
    store = EventWakeupStore(root / "event-wakeup-store")
    state = store.initialize(state)
    return state, store


def _trigger(
    state: Mapping[str, Any],
    *,
    trigger_id: str,
    trigger_class: str = "clock_schedule",
    requested: Mapping[str, int] | None = None,
    tier: str = "advanced",
    observed_at_ms: int = 200_100,
) -> dict[str, Any]:
    return build_trigger_event(
        trigger_id=trigger_id,
        trigger_class=trigger_class,
        source_id=trigger_id + "-source",
        source_event_digest=sha(trigger_id + "-source-event"),
        mission_id=state["mission_id"],
        condition_digest=sha(trigger_id + "-condition"),
        condition_satisfied=True,
        requested_resources=dict(
            requested
            or _resources(
                tokens=100,
                api_calls=5,
                cost=5_000,
                storage=10_000,
                worker=10_000,
            )
        ),
        requested_model_tier=tier,
        cycle_duration_ms=60_000,
        due_at_ms=observed_at_ms - 1,
        observed_at_ms=observed_at_ms,
    )


def _control(
    state: Mapping[str, Any],
    *,
    command_id: str,
    command: str,
    payload: Mapping[str, Any] | None = None,
    mission_authority: bool = True,
    permission_authority: bool = False,
    budget_authority: bool = False,
    issued_at_ms: int,
) -> dict[str, Any]:
    return build_control_command(
        command_id=command_id,
        command=command,
        mission_id=state["mission_id"],
        principal_id="user-control-principal",
        principal_authority_digest=sha("user-control-authority"),
        expected_state_digest=state["event_wakeup_state_digest"],
        reason_digest=sha(command_id + "-reason"),
        payload=dict(payload or {}),
        mission_control_authority=mission_authority,
        permission_authority=permission_authority,
        budget_authority=budget_authority,
        issued_at_ms=issued_at_ms,
    )


def _apply(
    store: EventWakeupStore,
    state: Mapping[str, Any],
    *,
    kind: str,
    payload: Mapping[str, Any],
    created_at_ms: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = build_event(
        state=state,
        event_kind=kind,
        payload=payload,
        created_at_ms=created_at_ms,
    )
    result = store.apply(event)
    if result["status"] != "APPLIED":
        raise AssertionError(result)
    return result["state"], event


def _admitted_and_replay(root: Path) -> dict[str, Any]:
    state, store = _initial(root, mission_id="mission-admitted")
    trigger = _trigger(state, trigger_id="trigger-admitted")
    state, event = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_101,
    )
    assert state["latest_wakeup_route"] == "WAKEUP_PROPOSED"
    assert state["latest_resource_route"] == "ADMIT"
    assert len(state["pending_cycle_ids"]) == 1
    proposal = next(iter(state["wakeup_proposals"].values()))
    assert proposal["new_bounded_cycle"] is True
    assert proposal["fresh_cycle_license_required"] is True
    assert proposal["fresh_actos_authorization_required"] is True
    assert proposal["inherited_execution_authority"] is False
    assert proposal["queue_entry_only"] is True
    assert proposal["running"] is False
    assert state["queue_is_running"] is False
    before = store.ledger_event_count()
    replay = store.apply(event)
    assert replay["status"] == "REPLAYED"
    assert store.ledger_event_count() == before
    return state


def _degraded(root: Path) -> dict[str, Any]:
    state, store = _initial(
        root,
        mission_id="mission-degraded",
        remaining=_resources(
            tokens=170,
            api_calls=14,
            cost=13_500,
            storage=107_000,
            worker=107_000,
        ),
        hard_limits=_resources(
            tokens=500,
            api_calls=50,
            cost=50_000,
            storage=500_000,
            worker=500_000,
        ),
    )
    trigger = _trigger(
        state,
        trigger_id="trigger-degraded",
        requested=_resources(
            tokens=100,
            api_calls=5,
            cost=5_000,
            storage=10_000,
            worker=10_000,
        ),
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_101,
    )
    assert state["latest_resource_route"] == "DEGRADE_MODEL"
    assert state["latest_wakeup_route"] == "WAKEUP_DEGRADED"
    proposal = next(iter(state["wakeup_proposals"].values()))
    assert proposal["selected_model_tier"] == "standard"
    return state


def _pause_resume(root: Path) -> dict[str, Any]:
    state, store = _initial(root, mission_id="mission-pause-resume")
    pause = _control(
        state,
        command_id="control-pause",
        command="pause",
        issued_at_ms=200_010,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=pause,
        created_at_ms=200_011,
    )
    assert state["control_mode"] == "PAUSED"
    trigger = _trigger(
        state,
        trigger_id="trigger-while-paused",
        observed_at_ms=200_020,
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_021,
    )
    assert state["latest_wakeup_route"] == "WAKEUP_BLOCKED_PAUSED"
    assert not state["pending_cycle_ids"]
    resume = _control(
        state,
        command_id="control-resume",
        command="resume",
        issued_at_ms=200_030,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=resume,
        created_at_ms=200_031,
    )
    assert state["control_mode"] == "ACTIVE"
    trigger = _trigger(
        state,
        trigger_id="trigger-after-resume",
        observed_at_ms=200_040,
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_041,
    )
    assert state["latest_wakeup_route"] == "WAKEUP_PROPOSED"
    return state


def _renewal_then_resume(root: Path) -> dict[str, Any]:
    state, store = _initial(
        root,
        mission_id="mission-renewal",
        remaining=_resources(
            tokens=110,
            api_calls=11,
            cost=10_100,
            storage=100_100,
            worker=100_100,
        ),
        hard_limits=_resources(
            tokens=500,
            api_calls=50,
            cost=50_000,
            storage=500_000,
            worker=500_000,
        ),
        remaining_cycles=1,
    )
    trigger = _trigger(state, trigger_id="trigger-resource-shortfall")
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_101,
    )
    assert state["control_mode"] == "AWAITING_RENEWAL"
    assert state["latest_wakeup_route"] == "WAKEUP_BLOCKED_RENEWAL"

    replenishment_event = _trigger(
        state,
        trigger_id="trigger-resource-replenished",
        trigger_class="resource_replenished",
        requested=_resources(tokens=1, api_calls=1, cost=1, storage=1, worker=1),
        tier="small",
        observed_at_ms=200_110,
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=replenishment_event,
        created_at_ms=200_111,
    )
    assert state["control_mode"] == "AWAITING_RENEWAL"
    assert state["latest_wakeup_route"] == "WAKEUP_BLOCKED_RENEWAL"

    increase = _control(
        state,
        command_id="control-increase-budget",
        command="increase_budget",
        budget_authority=True,
        payload={
            "hard_limit_increase": _resources(
                tokens=500,
                api_calls=50,
                cost=50_000,
                storage=500_000,
                worker=500_000,
            ),
            "remaining_replenishment": _resources(
                tokens=500,
                api_calls=50,
                cost=50_000,
                storage=500_000,
                worker=500_000,
            ),
            "cycle_limit_increase": 5,
            "cycle_replenishment": 5,
            "new_authorization_digest": sha("renewal-budget-authority"),
        },
        issued_at_ms=200_120,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=increase,
        created_at_ms=200_121,
    )
    assert state["control_mode"] == "AWAITING_RENEWAL"
    resume = _control(
        state,
        command_id="control-resume-after-renewal",
        command="resume",
        issued_at_ms=200_130,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=resume,
        created_at_ms=200_131,
    )
    assert state["control_mode"] == "ACTIVE"
    trigger = _trigger(
        state,
        trigger_id="trigger-after-renewal",
        observed_at_ms=200_140,
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_141,
    )
    assert state["latest_wakeup_route"] == "WAKEUP_PROPOSED"
    return state


def _permission_and_status(root: Path) -> dict[str, Any]:
    state, store = _initial(root, mission_id="mission-permission-status")
    approval = _control(
        state,
        command_id="control-approve-permission",
        command="approve_permission",
        permission_authority=True,
        payload={"permission_approval_digest": sha("permission-approval")},
        issued_at_ms=200_010,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=approval,
        created_at_ms=200_011,
    )
    assert len(state["permission_approval_digests"]) == 1
    assert approval["direct_execution"] is False
    assert approval["direct_plan_activation"] is False
    status = build_status_snapshot(
        state=state,
        reason_digest=sha("status-inspection"),
        observed_at_ms=200_012,
    )
    assert status["foreground_channel_available"] is True
    assert status["status_grants_execution_authority"] is False
    assert set(status) >= {
        "state",
        "reason_digest",
        "completed_work",
        "checkpoint",
        "next_condition",
        "resource_state",
        "worker_state",
        "valid_user_actions",
    }
    return status


def _cancel_and_stale(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    state, store = _initial(root, mission_id="mission-cancel")
    stale_trigger = _trigger(
        state,
        trigger_id="trigger-stale",
        observed_at_ms=200_020,
    )
    stale_event = build_event(
        state=state,
        event_kind="trigger",
        payload=stale_trigger,
        created_at_ms=200_021,
    )
    cancel = _control(
        state,
        command_id="control-cancel",
        command="cancel",
        issued_at_ms=200_010,
    )
    state, _ = _apply(
        store,
        state,
        kind="control",
        payload=cancel,
        created_at_ms=200_011,
    )
    assert state["control_mode"] == "CANCELLED"
    stale_result = apply_event(state, stale_event)
    assert stale_result["status"] == "REJECTED"
    assert "event_state_digest_stale" in stale_result["errors"]
    trigger = _trigger(
        state,
        trigger_id="trigger-after-cancel",
        observed_at_ms=200_030,
    )
    state, _ = _apply(
        store,
        state,
        kind="trigger",
        payload=trigger,
        created_at_ms=200_031,
    )
    assert state["latest_wakeup_route"] == "WAKEUP_BLOCKED_CANCELLED"
    assert not state["pending_cycle_ids"]
    return state, stale_result


def run_event_wakeup_control_resource_scenarios() -> dict[str, Any]:
    with TemporaryDirectory(prefix="kuuos-event-wakeup-v025-") as temporary:
        root = Path(temporary)
        admitted = _admitted_and_replay(root / "admitted")
        degraded = _degraded(root / "degraded")
        resumed = _pause_resume(root / "pause-resume")
        renewed = _renewal_then_resume(root / "renewal")
        status = _permission_and_status(root / "permission-status")
        cancelled, stale = _cancel_and_stale(root / "cancel")

        store = EventWakeupStore(root / "admitted" / "event-wakeup-store")
        snapshot = store.snapshot_path
        snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except EventWakeupStoreError as exc:
            assert str(exc) == "event_wakeup_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt event-wakeup snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["event_wakeup_state_digest"] == recovered[
            "event_wakeup_state_digest"
        ]

        assert validate_state(admitted) == []
        assert admitted["conversation_model_running_as_daemon"] is False
        assert admitted["foreground_user_control_available"] is True
        assert admitted["queue_is_running"] is False
        assert admitted["running_is_verified"] is False

        return {
            "status": "KUUOS_EVENT_WAKEUP_CONTROL_RESOURCE_V0_25_OK",
            "admitted_route": admitted["latest_wakeup_route"],
            "degraded_route": degraded["latest_wakeup_route"],
            "degraded_model_tier": next(
                iter(degraded["wakeup_proposals"].values())
            )["selected_model_tier"],
            "pause_resume_route": resumed["latest_wakeup_route"],
            "renewal_resume_route": renewed["latest_wakeup_route"],
            "cancelled_route": cancelled["latest_wakeup_route"],
            "stale_status": stale["status"],
            "status_worker_state": status["worker_state"],
            "foreground_control_available": status[
                "foreground_channel_available"
            ],
            "hidden_daemon_started": admitted[
                "conversation_model_running_as_daemon"
            ],
            "queue_is_running": admitted["queue_is_running"],
            "execution_authority_granted": False,
            "recovered_state_digest": recovered["event_wakeup_state_digest"],
        }


__all__ = ["run_event_wakeup_control_resource_scenarios"]
