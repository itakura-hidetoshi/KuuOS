from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_rotation_scenarios_v0_9 import run_handover_rotation
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS, HOST_LICENSE
from runtime.kuuos_plan_os_capability_consumption_v0_10 import (
    apply_lease_consumption,
    build_lease_consumption_receipt,
)
from runtime.kuuos_plan_os_capability_lease_kernel_v0_10 import (
    build_capability_lease_state,
    refresh_expired_leases,
)
from runtime.kuuos_plan_os_capability_lease_store_v0_10 import (
    CapabilityLeaseStore,
    CapabilityLeaseStoreError,
)
from runtime.kuuos_plan_os_capability_lease_types_v0_10 import EXHAUSTED, EXPIRED
from runtime.kuuos_plan_os_capability_renewal_v0_10 import (
    apply_lease_renewal,
    build_lease_renewal_receipt,
)


def lease_specs() -> dict[str, dict]:
    return {
        kind: {
            "allowed_stages": ["ACT"],
            "operation_allowlist": [f"operation.{kind.lower()}"],
            "scope_digest": sha({"scope": kind}),
            "max_uses": 2,
            "max_cost_units": 10,
            "not_before_ms": 30_000,
            "expires_at_ms": 40_000,
        }
        for kind in CAPABILITY_KINDS
    }


def initial_state(root: Path) -> dict:
    capability_state = run_handover_rotation(root / "v09-source")
    return build_capability_lease_state(
        capability_state=capability_state,
        lease_specs=lease_specs(),
        now_ms=29_000,
    )


def run_consumption_and_renewal(root: Path) -> dict:
    state = initial_state(root)
    lease = state["leases"][HOST_LICENSE]

    for kwargs, expected in (
        ({"owner_id": "owner-alpha"}, "lease_owner_mismatch"),
        ({"epoch_digest": state["current_epoch_digest"] + "x"}, "lease_epoch_mismatch"),
        ({"stage": "VERIFY"}, "lease_stage_not_allowed"),
        ({"operation_id": "operation.other"}, "lease_operation_not_allowed"),
        ({"scope_digest": sha("wrong-scope")}, "lease_scope_mismatch"),
        ({"cost_units": 11}, "lease_cost_budget_exceeded"),
    ):
        base = {
            "state": state,
            "kind": HOST_LICENSE,
            "owner_id": state["current_owner_id"],
            "epoch_digest": state["current_epoch_digest"],
            "stage": "ACT",
            "operation_id": "operation.host_license",
            "scope_digest": lease["scope_digest"],
            "cost_units": 5,
            "usage_id": "reject-" + expected,
            "now_ms": 31_000,
        }
        base.update(kwargs)
        try:
            build_lease_consumption_receipt(**base)
        except ValueError as exc:
            assert str(exc) == expected
        else:
            raise AssertionError(expected + " was accepted")

    store = CapabilityLeaseStore(root / "lease-store")
    store.initialize(state)
    current = state
    first = build_lease_consumption_receipt(
        state=current,
        kind=HOST_LICENSE,
        owner_id=current["current_owner_id"],
        epoch_digest=current["current_epoch_digest"],
        stage="ACT",
        operation_id="operation.host_license",
        scope_digest=current["leases"][HOST_LICENSE]["scope_digest"],
        cost_units=4,
        usage_id="host-use-1",
        now_ms=31_000,
    )
    applied = store.commit(event_type="CONSUME", receipt=first, now_ms=31_001)
    assert applied["status"] == "APPLIED"
    current = applied["state"]
    assert current["leases"][HOST_LICENSE]["remaining_uses"] == 1
    assert current["leases"][HOST_LICENSE]["remaining_cost_units"] == 6
    assert store.commit(event_type="CONSUME", receipt=first, now_ms=31_002)["status"] == "REPLAYED"

    second = build_lease_consumption_receipt(
        state=current,
        kind=HOST_LICENSE,
        owner_id=current["current_owner_id"],
        epoch_digest=current["current_epoch_digest"],
        stage="ACT",
        operation_id="operation.host_license",
        scope_digest=current["leases"][HOST_LICENSE]["scope_digest"],
        cost_units=6,
        usage_id="host-use-2",
        now_ms=32_000,
    )
    applied = store.commit(event_type="CONSUME", receipt=second, now_ms=32_001)
    current = applied["state"]
    assert current["leases"][HOST_LICENSE]["status"] == EXHAUSTED
    assert current["leases"][HOST_LICENSE]["remaining_uses"] == 0
    assert current["leases"][HOST_LICENSE]["remaining_cost_units"] == 0

    try:
        build_lease_consumption_receipt(
            state=current,
            kind=HOST_LICENSE,
            owner_id=current["current_owner_id"],
            epoch_digest=current["current_epoch_digest"],
            stage="ACT",
            operation_id="operation.host_license",
            scope_digest=current["leases"][HOST_LICENSE]["scope_digest"],
            cost_units=1,
            usage_id="host-use-3",
            now_ms=33_000,
        )
    except ValueError as exc:
        assert str(exc) == "lease_not_active"
    else:
        raise AssertionError("exhausted lease accepted consumption")

    renewal = build_lease_renewal_receipt(
        state=current,
        kind=HOST_LICENSE,
        owner_id=current["current_owner_id"],
        epoch_digest=current["current_epoch_digest"],
        scope_digest=current["leases"][HOST_LICENSE]["scope_digest"],
        external_renewal_receipt_digest=sha("external-renewal-1"),
        additional_uses=1,
        additional_cost_units=3,
        new_expires_at_ms=50_000,
        now_ms=34_000,
    )
    renewed = store.commit(event_type="RENEW", receipt=renewal, now_ms=34_001)
    assert renewed["status"] == "APPLIED"
    current = renewed["state"]
    assert current["leases"][HOST_LICENSE]["remaining_uses"] == 1
    assert current["leases"][HOST_LICENSE]["remaining_cost_units"] == 3
    assert current["leases"][HOST_LICENSE]["renewal_count"] == 1
    assert store.commit(event_type="RENEW", receipt=renewal, now_ms=34_002)["status"] == "REPLAYED"

    try:
        build_lease_renewal_receipt(
            state=current,
            kind=HOST_LICENSE,
            owner_id="owner-alpha",
            epoch_digest=current["current_epoch_digest"],
            scope_digest=current["leases"][HOST_LICENSE]["scope_digest"],
            external_renewal_receipt_digest=sha("wrong-owner-renewal"),
            additional_uses=1,
            additional_cost_units=1,
            new_expires_at_ms=60_000,
            now_ms=35_000,
        )
    except ValueError as exc:
        assert str(exc) == "renewal_owner_mismatch"
    else:
        raise AssertionError("old owner renewed lease")

    snapshot = root / "lease-store" / "lease-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except CapabilityLeaseStoreError as exc:
        assert str(exc) == "lease_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt lease snapshot accepted")
    store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert store.ledger_commit_count() == 3
    return recovered


def run_expiry(root: Path) -> dict:
    state = initial_state(root / "expiry")
    expired = refresh_expired_leases(state, now_ms=40_000)
    assert all(lease["status"] == EXPIRED for lease in expired["leases"].values())
    receipt = {
        "consumed_at_ms": 40_000,
        "lease_consumption_receipt_digest": sha("expired-probe"),
    }
    result = apply_lease_consumption(expired, receipt)
    assert result["status"] == "REJECTED"
    return expired
