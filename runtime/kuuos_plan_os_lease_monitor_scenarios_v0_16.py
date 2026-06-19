from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS, HOST_LICENSE
from runtime.kuuos_plan_os_next_cycle_session_scenarios_v0_15 import run_session_bootstrap
from runtime.kuuos_plan_os_lease_monitor_kernel_v0_16 import build_lease_monitor_tick
from runtime.kuuos_plan_os_lease_monitor_store_v0_16 import (
    LeaseMonitorStore,
    LeaseMonitorStoreError,
)
from runtime.kuuos_plan_os_lease_monitor_types_v0_16 import (
    CONTINUE,
    REVALIDATE,
    RENEW_OR_ESCALATE,
    REROTATE_REQUIRED,
    SESSION_HEALTHY,
    SESSION_SUSPENDED,
)


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


def _assert_route(session: dict, observations: dict, now_ms: int, route: str) -> None:
    tick = build_lease_monitor_tick(
        session=session,
        observed_leases=observations,
        tick_index=1,
        now_ms=now_ms,
    )
    assert tick["session_status_after"] == SESSION_SUSPENDED
    assert tick["recovery_route"] == route
    assert tick["plan_progress_allowed"] is False


def run_lease_monitor(root: Path) -> dict:
    session = run_session_bootstrap(root / "v15-source")

    expired = _observations(session, 90_000)
    _assert_route(session, expired, 90_000, RENEW_OR_ESCALATE)

    use_empty = _observations(session, 86_000)
    use_empty[HOST_LICENSE]["remaining_uses"] = 0
    _assert_route(session, use_empty, 86_000, RENEW_OR_ESCALATE)

    cost_empty = _observations(session, 86_000)
    cost_empty[HOST_LICENSE]["remaining_cost_units"] = 0
    _assert_route(session, cost_empty, 86_000, RENEW_OR_ESCALATE)

    owner_mismatch = _observations(session, 86_000)
    owner_mismatch[HOST_LICENSE]["owner_id"] = "owner-substituted"
    _assert_route(session, owner_mismatch, 86_000, REROTATE_REQUIRED)

    epoch_mismatch = _observations(session, 86_000)
    epoch_mismatch[HOST_LICENSE]["epoch_digest"] = sha("epoch-substituted")
    _assert_route(session, epoch_mismatch, 86_000, REROTATE_REQUIRED)

    scope_mismatch = _observations(session, 86_000)
    scope_mismatch[HOST_LICENSE]["scope_digest"] = sha("scope-substituted")
    _assert_route(session, scope_mismatch, 86_000, REROTATE_REQUIRED)

    budget_increase = _observations(session, 86_000)
    budget_increase[HOST_LICENSE]["remaining_uses"] += 1
    _assert_route(session, budget_increase, 86_000, REVALIDATE)

    time_mismatch = _observations(session, 86_000)
    time_mismatch[HOST_LICENSE]["observed_at_ms"] = 85_999
    _assert_route(session, time_mismatch, 86_000, REVALIDATE)

    healthy_observations = _observations(session, 86_000)
    for observation in healthy_observations.values():
        observation["remaining_uses"] -= 1
        observation["remaining_cost_units"] -= 2
    healthy = build_lease_monitor_tick(
        session=session,
        observed_leases=healthy_observations,
        tick_index=1,
        now_ms=86_000,
    )
    assert healthy["session_status_after"] == SESSION_HEALTHY
    assert healthy["recovery_route"] == CONTINUE
    assert healthy["plan_progress_allowed"] is True
    assert healthy["suspension_reasons"] == []

    suspended_observations = deepcopy(healthy_observations)
    for observation in suspended_observations.values():
        observation["observed_at_ms"] = 87_000
    suspended_observations[HOST_LICENSE]["remaining_uses"] = 0
    suspended = build_lease_monitor_tick(
        session=session,
        observed_leases=suspended_observations,
        tick_index=2,
        now_ms=87_000,
    )
    assert suspended["session_status_after"] == SESSION_SUSPENDED
    assert suspended["recovery_route"] == RENEW_OR_ESCALATE
    assert suspended["suspension_terminal"] is True

    store = LeaseMonitorStore(root / "monitor-store")
    store.initialize(session)
    assert store.commit(tick=healthy, now_ms=86_001)["status"] == "APPLIED"
    assert store.commit(tick=healthy, now_ms=86_002)["status"] == "REPLAYED"
    assert store.commit(tick=suspended, now_ms=87_001)["status"] == "APPLIED"
    assert store.commit(tick=suspended, now_ms=87_002)["status"] == "REPLAYED"

    post_suspend = deepcopy(healthy)
    post_suspend["tick_index"] = 3
    post_suspend["tick_at_ms"] = 88_000
    post_suspend["observed_leases"] = _observations(session, 88_000)
    from runtime.kuuos_plan_os_lease_monitor_types_v0_16 import tick_digest

    post_suspend["observation_digest"] = sha(post_suspend["observed_leases"])
    post_suspend["lease_monitor_tick_digest"] = ""
    post_suspend["lease_monitor_tick_digest"] = tick_digest(post_suspend)
    rejected = store.commit(tick=post_suspend, now_ms=88_001)
    assert rejected["status"] == "REJECTED"
    assert "monitor_session_suspended" in rejected["errors"]

    snapshot = root / "monitor-store" / "monitor-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except LeaseMonitorStoreError as exc:
        assert str(exc) == "monitor_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt monitor snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["latest_tick"]["lease_monitor_tick_digest"] == recovered[
        "latest_tick"
    ]["lease_monitor_tick_digest"]
    assert recovered["latest_tick"]["session_status_after"] == SESSION_SUSPENDED
    assert set(recovered["latest_tick"]["per_kind"]) == set(CAPABILITY_KINDS)
    return recovered
