from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_finite_cycle_continuity_store_v0_27 import (
    FiniteCycleContinuityStore,
    FiniteCycleStoreError,
)
from runtime.kuuos_integrated_long_duration_operation_kernel_v0_27 import (
    apply_event,
    build_control_event,
    build_cycle_receipt,
    build_event,
    build_initial_state,
    build_integrated_operation_contract,
    build_recovery_receipt,
    validate_state,
)
from runtime.kuuos_integrated_long_duration_operation_types_v0_27 import (
    LOWER_COMPONENTS,
)


def _lower_digests(label: str) -> dict[str, str]:
    return {component: sha(f"{label}:{component}") for component in LOWER_COMPONENTS}


def _initial(
    root: Path, *, mission_id: str, lease_cycles: int = 3
) -> tuple[dict[str, Any], FiniteCycleContinuityStore]:
    contract = build_integrated_operation_contract(
        contract_id=mission_id + "-contract",
        mission_id=mission_id,
        lineage_id=mission_id + "-lineage",
        lower_contract_digests=_lower_digests(mission_id + ":contract"),
        initial_host_license_digest=sha(mission_id + ":host-license:0"),
        max_cycle_cost=10,
        max_cycle_steps=20,
        max_cycle_duration_ms=1_000,
        max_lease_cycles=4,
        max_lease_cost=40,
        initial_lease_id=mission_id + "-lease-0",
        initial_lease_cycles=lease_cycles,
        initial_lease_cost=lease_cycles * 10,
        initial_lease_expires_at_ms=1_000_000,
        user_control_policy_digest=sha(mission_id + ":control-policy"),
        recovery_policy_digest=sha(mission_id + ":recovery-policy"),
        audit_policy_digest=sha(mission_id + ":audit-policy"),
        created_at_ms=100_000,
    )
    state = build_initial_state(contract=contract, initialized_at_ms=100_001)
    store = FiniteCycleContinuityStore(root / "continuity-store")
    return store.initialize(state), store


def _apply(
    store: FiniteCycleContinuityStore,
    state: Mapping[str, Any],
    *,
    kind: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = build_event(
        state=state,
        event_kind=kind,
        payload=payload,
        created_at_ms=now_ms,
    )
    result = store.apply(event)
    if result["status"] != "APPLIED":
        raise AssertionError(result)
    return result["state"], event


def _cycle(
    store: FiniteCycleContinuityStore,
    state: Mapping[str, Any],
    *,
    label: str,
    start_ms: int,
    route: str = "CONTINUE",
    cost: int = 10,
    steps: int = 12,
) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = build_cycle_receipt(
        state=state,
        cycle_id=label,
        lower_cycle_receipt_digests=_lower_digests(label),
        cycle_authorization_digest=sha(label + ":cycle-authority"),
        host_license_digest=state["host_license_digest"],
        cycle_cost=cost,
        cycle_steps=steps,
        started_at_ms=start_ms,
        completed_at_ms=start_ms + 500,
        route=route,
        checkpoint_digest=sha(label + ":checkpoint"),
    )
    return _apply(
        store,
        state,
        kind="cycle",
        payload=receipt,
        now_ms=start_ms + 501,
    )


def _control(
    store: FiniteCycleContinuityStore,
    state: Mapping[str, Any],
    *,
    command: str,
    label: str,
    now_ms: int,
    payload: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    control = build_control_event(
        state=state,
        command=command,
        command_id=label,
        external_authority_digest=sha(label + ":external-authority"),
        reason_digest=sha(label + ":reason"),
        payload=dict(payload or {}),
        issued_at_ms=now_ms,
    )
    return _apply(
        store,
        state,
        kind="control",
        payload=control,
        now_ms=now_ms + 1,
    )


def _recovery(
    store: FiniteCycleContinuityStore,
    state: Mapping[str, Any],
    *,
    kind: str,
    label: str,
    now_ms: int,
    new_host_license_digest: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = build_recovery_receipt(
        state=state,
        recovery_kind=kind,
        ledger_root_digest=sha(label + ":ledger-root"),
        checkpoint_digest=state["latest_checkpoint_digest"],
        new_host_license_digest=new_host_license_digest,
        recovered_at_ms=now_ms,
    )
    return _apply(
        store,
        state,
        kind="recovery",
        payload=receipt,
        now_ms=now_ms + 1,
    )


def _repeatable_cycles_with_restarts(root: Path) -> tuple[
    dict[str, Any], FiniteCycleContinuityStore, dict[str, Any]
]:
    state, store = _initial(root, mission_id="mission-continuity", lease_cycles=3)
    state, _ = _cycle(
        store, state, label="cycle-1", start_ms=101_000
    )
    state, _ = _cycle(
        store, state, label="cycle-2", start_ms=102_000
    )

    state, _ = _recovery(
        store,
        state,
        kind="process_restart",
        label="process-restart-1",
        now_ms=103_000,
    )
    assert state["process_epoch"] == 1
    assert state["mode"] == "PAUSED"
    state, _ = _control(
        store,
        state,
        command="resume",
        label="resume-after-process-restart",
        now_ms=103_010,
    )
    state, _ = _cycle(
        store, state, label="cycle-3", start_ms=104_000
    )
    assert state["mode"] == "RENEWAL_REQUIRED"

    state, _ = _control(
        store,
        state,
        command="renew",
        label="renew-1",
        now_ms=105_000,
        payload={
            "lease_id": "mission-continuity-lease-1",
            "lease_cycles": 4,
            "lease_cost": 40,
            "lease_expires_at_ms": 1_100_000,
            "renewal_receipt_digest": sha("renewal-receipt-1"),
        },
    )
    assert state["lease_sequence"] == 1
    assert state["mode"] == "PAUSED"
    state, _ = _control(
        store,
        state,
        command="resume",
        label="resume-after-renewal",
        now_ms=105_010,
    )

    state, _ = _cycle(
        store, state, label="cycle-4", start_ms=106_000
    )
    state, _ = _recovery(
        store,
        state,
        kind="host_restart",
        label="host-restart-1",
        now_ms=107_000,
    )
    assert state["host_epoch"] == 1
    assert state["fresh_host_license_required"] is True
    blocked_resume = build_control_event(
        state=state,
        command="resume",
        command_id="blocked-resume-before-host-rebind",
        external_authority_digest=sha("blocked-resume-authority"),
        reason_digest=sha("blocked-resume-reason"),
        payload={},
        issued_at_ms=107_010,
    )
    blocked_event = build_event(
        state=state,
        event_kind="control",
        payload=blocked_resume,
        created_at_ms=107_011,
    )
    blocked = store.apply(blocked_event)
    assert blocked["status"] == "REJECTED"
    assert "resume_requires_host_rebind" in blocked["errors"]

    new_license = sha("mission-continuity:host-license:1")
    state, _ = _recovery(
        store,
        state,
        kind="host_rebind",
        label="host-rebind-1",
        now_ms=107_020,
        new_host_license_digest=new_license,
    )
    assert state["host_license_digest"] == new_license
    assert state["fresh_host_license_required"] is False
    state, _ = _control(
        store,
        state,
        command="resume",
        label="resume-after-host-rebind",
        now_ms=107_030,
    )
    state, _ = _cycle(
        store, state, label="cycle-5", start_ms=108_000
    )
    state, _ = _cycle(
        store, state, label="cycle-6", start_ms=109_000
    )
    state, replay_event = _cycle(
        store, state, label="cycle-7", start_ms=110_000
    )
    assert state["completed_cycles"] == 7
    assert state["lease_sequence"] == 1
    assert state["mode"] == "RENEWAL_REQUIRED"
    return state, store, replay_event


def _pause_resume_and_terminate(root: Path) -> dict[str, Any]:
    state, store = _initial(root, mission_id="mission-terminate", lease_cycles=2)
    state, _ = _control(
        store,
        state,
        command="pause",
        label="manual-pause",
        now_ms=101_000,
    )
    assert state["mode"] == "PAUSED"
    state, _ = _control(
        store,
        state,
        command="resume",
        label="manual-resume",
        now_ms=101_010,
    )
    state, _ = _cycle(
        store, state, label="terminate-cycle-1", start_ms=102_000
    )
    state, _ = _control(
        store,
        state,
        command="terminate",
        label="manual-terminate",
        now_ms=103_000,
    )
    assert state["mode"] == "TERMINATED"
    return state


def _handover(root: Path) -> dict[str, Any]:
    state, store = _initial(root, mission_id="mission-handover", lease_cycles=2)
    state, _ = _cycle(
        store, state, label="handover-cycle-1", start_ms=101_000
    )
    checkpoint = state["latest_checkpoint_digest"]
    state, _ = _control(
        store,
        state,
        command="handover",
        label="manual-handover",
        now_ms=102_000,
    )
    assert state["mode"] == "HANDED_OVER"
    assert state["latest_checkpoint_digest"] == checkpoint
    return state


def run_integrated_long_duration_operation_scenarios() -> dict[str, Any]:
    with TemporaryDirectory(prefix="kuuos-integrated-v027-") as temporary:
        root = Path(temporary)
        repeated, store, replay_event = _repeatable_cycles_with_restarts(
            root / "repeated"
        )
        terminated = _pause_resume_and_terminate(root / "terminated")
        handed_over = _handover(root / "handover")

        before = store.ledger_event_count()
        replay = store.apply(replay_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_event_count() == before

        stale = deepcopy(replay_event)
        stale["integrated_operation_event_digest"] = sha("stale-integrated-event")
        stale_result = apply_event(repeated, stale)
        assert stale_result["status"] == "REJECTED"
        assert "integrated_event_state_stale" in stale_result["errors"]

        store.snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except FiniteCycleStoreError as exc:
            assert str(exc) == "finite_cycle_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt continuity snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["integrated_operation_state_digest"] == recovered[
            "integrated_operation_state_digest"
        ]

        assert validate_state(repeated) == []
        assert all(
            summary["cycle_cost"] <= repeated["contract"]["max_cycle_cost"]
            and summary["cycle_steps"] <= repeated["contract"]["max_cycle_steps"]
            for summary in repeated["cycle_summaries"]
        )
        assert repeated["foreground_user_control_available"] is True
        assert repeated["automatic_renewal_performed"] is False
        assert repeated["automatic_resume_performed"] is False
        assert repeated["memory_root_overwrite"] is False

        return {
            "status": "KUUOS_INTEGRATED_LONG_DURATION_OPERATION_V0_27_OK",
            "completed_cycles": repeated["completed_cycles"],
            "lease_sequence": repeated["lease_sequence"],
            "process_epoch": repeated["process_epoch"],
            "host_epoch": repeated["host_epoch"],
            "repeatable_route": repeated["mode"],
            "terminate_route": terminated["mode"],
            "handover_route": handed_over["mode"],
            "replay_status": replay["status"],
            "stale_status": stale_result["status"],
            "foreground_control_available": repeated[
                "foreground_user_control_available"
            ],
            "automatic_renewal": repeated["automatic_renewal_performed"],
            "automatic_resume": repeated["automatic_resume_performed"],
            "authority_extended": False,
            "recovered_state_digest": recovered[
                "integrated_operation_state_digest"
            ],
        }


__all__ = ["run_integrated_long_duration_operation_scenarios"]
