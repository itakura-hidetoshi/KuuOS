from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_materialized_chain_activation_kernel_v0_14 import (
    build_materialized_chain_activation_receipt,
)
from runtime.kuuos_plan_os_next_cycle_session_kernel_v0_15 import (
    build_next_cycle_plan_session,
)
from runtime.kuuos_plan_os_next_cycle_session_store_v0_15 import (
    NextCycleSessionStore,
    NextCycleSessionStoreError,
)
from runtime.kuuos_plan_os_next_cycle_session_types_v0_15 import session_digest
from runtime.kuuos_plan_os_rerotation_materialization_scenarios_v0_13 import (
    run_materialization,
)


def _sources(root: Path) -> tuple[dict, dict]:
    materialization = run_materialization(root / "materialization")
    activation = build_materialized_chain_activation_receipt(
        materialization_receipt=materialization,
        requested_owner_id=materialization["current_owner_id"],
        requested_epoch_digest=materialization["current_epoch_digest"],
        current_cycle_index=12,
        mission_cycle_state_digest=sha("mission-cycle-12"),
        activation_authority_id="activation-board-v15",
        activation_authority_receipt_digest=sha("activation-authority-v15"),
        now_ms=85_000,
    )
    return materialization, activation


def run_session_bootstrap(root: Path) -> dict:
    materialization, activation = _sources(root)
    common = {
        "activation_receipt": activation,
        "materialization_receipt": materialization,
        "mission_cycle_index": 13,
        "mission_cycle_phase": "plan",
        "mission_cycle_state_digest": sha("mission-cycle-13"),
        "requested_owner_id": activation["owner_id"],
        "requested_epoch_digest": activation["epoch_digest"],
        "now_ms": 85_500,
    }
    for field, value, expected in (
        ("mission_cycle_index", 12, "session_cycle_mismatch"),
        ("mission_cycle_phase", "replan", "session_phase_mismatch"),
        ("requested_owner_id", "owner-substituted", "session_owner_mismatch"),
        ("requested_epoch_digest", sha("epoch-substituted"), "session_epoch_mismatch"),
    ):
        kwargs = dict(common)
        kwargs[field] = value
        try:
            build_next_cycle_plan_session(**kwargs)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(expected + " accepted")

    expired = dict(common)
    expired["now_ms"] = 90_000
    try:
        build_next_cycle_plan_session(**expired)
    except ValueError as exc:
        assert str(exc).startswith("session_lease_expired:")
    else:
        raise AssertionError("expired lease session accepted")

    session = build_next_cycle_plan_session(**common)
    assert session["status"] == "SESSION_ACTIVE"
    assert session["mission_cycle_index"] == 13
    assert session["mission_cycle_phase"] == "plan"
    assert session["plan_bootstrap_state"]["current_phase"] == "bind"
    assert session["plan_bootstrap_state"]["event_index"] == 0
    assert session["plan_bootstrap_state"]["steps"] == []
    assert session["lease_monitor_started_at_ms"] == 85_500
    assert session["lease_monitor_deadline_ms"] == 90_000
    assert len(session["lease_clocks"]) == 4
    assert session["execution_granted"] is False

    store = NextCycleSessionStore(root / "session-store")
    store.initialize(
        activation_receipt=activation,
        materialization_receipt=materialization,
    )
    applied = store.commit(session=session, now_ms=85_501)
    assert applied["status"] == "APPLIED"
    assert store.commit(session=session, now_ms=85_502)["status"] == "REPLAYED"

    conflicting = deepcopy(session)
    conflicting["mission_cycle_state_digest"] = sha("conflicting-cycle-13")
    conflicting["plan_control_session_digest"] = ""
    conflicting["plan_control_session_digest"] = session_digest(conflicting)
    rejected = store.commit(session=conflicting, now_ms=85_503)
    assert rejected["status"] == "REJECTED"
    assert "session_already_bootstrapped" in rejected["errors"]

    snapshot = root / "session-store" / "session-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except NextCycleSessionStoreError as exc:
        assert str(exc) == "session_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt session snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["plan_control_session_digest"] == recovered[
        "plan_control_session_digest"
    ]
    return recovered
