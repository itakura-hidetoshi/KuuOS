from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import (
    CAPABILITY_KINDS,
    HOST_LICENSE,
)
from runtime.kuuos_plan_os_lease_monitor_kernel_v0_16 import (
    build_lease_monitor_tick,
)
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    build_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_next_cycle_session_scenarios_v0_15 import _sources
from runtime.kuuos_plan_os_suspension_recovery_kernel_v0_17 import (
    build_suspension_recovery_handoff,
)
from runtime.kuuos_plan_os_suspension_recovery_store_v0_17 import (
    SuspensionRecoveryStore,
    SuspensionRecoveryStoreError,
)
from runtime.kuuos_plan_os_suspension_recovery_types_v0_17 import (
    REVALIDATION_REQUIRED,
    V11_RENEWAL_REVIEW,
    V12_ESCALATION_REQUIRED,
    V12_REROTATION_REQUIRED,
    handoff_digest,
)


def _source(root: Path) -> tuple[dict, dict]:
    materialization, activation = _sources(root / "sources")
    session = build_next_cycle_plan_session(
        activation_receipt=activation,
        materialization_receipt=materialization,
        mission_cycle_index=13,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("recovery-mission-cycle-13"),
        requested_owner_id=activation["owner_id"],
        requested_epoch_digest=activation["epoch_digest"],
        now_ms=85_500,
    )
    return materialization, session


def _observations(session: dict, now_ms: int) -> dict[str, dict]:
    return {
        kind: {
            "owner_id": session["owner_id"],
            "epoch_digest": session["epoch_digest"],
            "scope_digest": session["scope_inventory"][kind],
            "expires_at_ms": clock["expires_at_ms"],
            "remaining_uses": clock["remaining_uses"],
            "remaining_cost_units": clock["remaining_cost_units"],
            "observed_at_ms": now_ms,
        }
        for kind, clock in session["lease_clocks"].items()
    }


def _handoff(
    *,
    session: dict,
    tick: dict,
    materialization: dict,
    label: str,
    now_ms: int,
) -> dict:
    return build_suspension_recovery_handoff(
        session=session,
        suspension_tick=tick,
        materialization_receipt=materialization,
        recovery_authority_id="recovery-board-v17",
        recovery_authority_receipt_digest=sha(label),
        now_ms=now_ms,
    )


def run_suspension_recovery(root: Path) -> dict:
    materialization, session = _source(root)

    revalidate_observations = _observations(session, 86_000)
    revalidate_observations[HOST_LICENSE]["observed_at_ms"] = 85_999
    revalidate_tick = build_lease_monitor_tick(
        session=session,
        observed_leases=revalidate_observations,
        tick_index=1,
        now_ms=86_000,
    )
    revalidate = _handoff(
        session=session,
        tick=revalidate_tick,
        materialization=materialization,
        label="revalidation-authority",
        now_ms=86_001,
    )
    assert revalidate["target_stage"] == REVALIDATION_REQUIRED
    assert revalidate["revalidation_observation_digest"] == revalidate_tick[
        "observation_digest"
    ]
    assert revalidate["renewal_candidate_kinds"] == []
    assert revalidate["escalation_required_kinds"] == []

    renewal_observations = _observations(session, 86_000)
    renewal_observations[HOST_LICENSE]["remaining_uses"] = 0
    renewal_tick = build_lease_monitor_tick(
        session=session,
        observed_leases=renewal_observations,
        tick_index=1,
        now_ms=86_000,
    )
    renewal = _handoff(
        session=session,
        tick=renewal_tick,
        materialization=materialization,
        label="renewal-review-authority",
        now_ms=86_002,
    )
    assert renewal["target_stage"] == V11_RENEWAL_REVIEW
    assert renewal["renewal_candidate_kinds"] == [HOST_LICENSE]
    assert renewal["escalation_required_kinds"] == []

    escalation_observations = _observations(session, 120_000)
    escalation_tick = build_lease_monitor_tick(
        session=session,
        observed_leases=escalation_observations,
        tick_index=1,
        now_ms=120_000,
    )
    escalation = _handoff(
        session=session,
        tick=escalation_tick,
        materialization=materialization,
        label="escalation-authority",
        now_ms=120_001,
    )
    assert escalation["target_stage"] == V12_ESCALATION_REQUIRED
    assert set(escalation["escalation_required_kinds"]) == set(CAPABILITY_KINDS)
    assert escalation["renewal_candidate_kinds"] == []

    rerotation_observations = _observations(session, 86_000)
    rerotation_observations[HOST_LICENSE]["owner_id"] = "owner-substituted"
    rerotation_tick = build_lease_monitor_tick(
        session=session,
        observed_leases=rerotation_observations,
        tick_index=1,
        now_ms=86_000,
    )
    rerotation = _handoff(
        session=session,
        tick=rerotation_tick,
        materialization=materialization,
        label="rerotation-authority",
        now_ms=86_003,
    )
    assert rerotation["target_stage"] == V12_REROTATION_REQUIRED
    assert rerotation["rerotation_required"] is True

    for handoff in (revalidate, renewal, escalation, rerotation):
        assert handoff["old_session_closed"] is True
        assert handoff["old_session_resume_allowed"] is False
        assert handoff["new_lineage_required"] is True
        assert handoff["new_activation_required"] is True
        assert handoff["new_session_required"] is True
        assert handoff["execution_granted"] is False

    substituted_session = deepcopy(session)
    substituted_session["owner_id"] = "owner-substituted"
    from runtime.kuuos_plan_os_next_cycle_session_types_v0_15 import session_digest

    substituted_session["plan_control_session_digest"] = ""
    substituted_session["plan_control_session_digest"] = session_digest(
        substituted_session
    )
    try:
        _handoff(
            session=substituted_session,
            tick=rerotation_tick,
            materialization=materialization,
            label="substituted-session-authority",
            now_ms=86_004,
        )
    except ValueError as exc:
        assert str(exc) == "recovery_source_session_mismatch"
    else:
        raise AssertionError("substituted suspended session accepted")

    store = SuspensionRecoveryStore(root / "recovery-store")
    store.initialize(
        session=session,
        suspension_tick=rerotation_tick,
        materialization_receipt=materialization,
    )
    assert store.commit(handoff=rerotation, now_ms=86_010)["status"] == "APPLIED"
    assert store.commit(handoff=rerotation, now_ms=86_011)["status"] == "REPLAYED"

    conflicting = deepcopy(rerotation)
    conflicting["recovery_authority_receipt_digest"] = sha(
        "conflicting-recovery-authority"
    )
    conflicting["suspension_recovery_handoff_digest"] = ""
    conflicting["suspension_recovery_handoff_digest"] = handoff_digest(
        conflicting
    )
    rejected = store.commit(handoff=conflicting, now_ms=86_012)
    assert rejected["status"] == "REJECTED"
    assert "recovery_already_routed" in rejected["errors"]

    snapshot = root / "recovery-store" / "recovery-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except SuspensionRecoveryStoreError as exc:
        assert str(exc) == "recovery_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt recovery snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["suspension_recovery_handoff_digest"] == recovered[
        "suspension_recovery_handoff_digest"
    ]
    return {
        "revalidate": revalidate,
        "renewal": renewal,
        "escalation": escalation,
        "rerotation": recovered,
    }
