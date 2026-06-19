from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_capability_lease_scenarios_v0_10 import initial_state
from runtime.kuuos_plan_os_capability_renewal_v0_10 import build_lease_renewal_receipt
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import CAPABILITY_KINDS, HOST_LICENSE
from runtime.kuuos_plan_os_bounded_renewal_state_v0_11 import build_bounded_renewal_state
from runtime.kuuos_plan_os_bounded_renewal_store_v0_11 import (
    BoundedRenewalStore,
    BoundedRenewalStoreError,
)
from runtime.kuuos_plan_os_bounded_renewal_types_v0_11 import ESCALATION_REQUIRED
from runtime.kuuos_plan_os_governed_renewal_v0_11 import build_governed_renewal_receipt


def policies() -> dict[str, dict]:
    return {
        kind: {
            "renewal_authority_id": "renewal-board",
            "max_renewals": 2,
            "max_cumulative_added_uses": 2,
            "max_cumulative_added_cost_units": 4,
            "absolute_expires_at_ms": 60_000,
            "cooldown_ms": 1_000,
        }
        for kind in CAPABILITY_KINDS
    }


def _inner(state: dict, *, expiry: int, now_ms: int, tag: str) -> dict:
    lease = state["leases"][HOST_LICENSE]
    return build_lease_renewal_receipt(
        state=state,
        kind=HOST_LICENSE,
        owner_id=state["current_owner_id"],
        epoch_digest=state["current_epoch_digest"],
        scope_digest=lease["scope_digest"],
        external_renewal_receipt_digest=sha({"external": tag}),
        additional_uses=1,
        additional_cost_units=2,
        new_expires_at_ms=expiry,
        now_ms=now_ms,
    )


def run_bounded_renewal(root: Path) -> dict:
    lease_state = initial_state(root / "v10-source")
    state = build_bounded_renewal_state(
        lease_state=lease_state, policies=policies(), now_ms=40_100
    )

    first_inner = _inner(
        state["current_lease_state"], expiry=50_000, now_ms=41_000, tag="one"
    )
    try:
        build_governed_renewal_receipt(
            state=state,
            lease_renewal_receipt=first_inner,
            renewal_authority_id="wrong-board",
            authority_receipt_digest=sha("wrong-authority"),
            now_ms=41_000,
        )
    except ValueError as exc:
        assert str(exc) == "bounded_renewal_authority_mismatch"
    else:
        raise AssertionError("wrong renewal authority accepted")

    too_far = _inner(
        state["current_lease_state"], expiry=70_000, now_ms=41_000, tag="far"
    )
    try:
        build_governed_renewal_receipt(
            state=state,
            lease_renewal_receipt=too_far,
            renewal_authority_id="renewal-board",
            authority_receipt_digest=sha("authority-far"),
            now_ms=41_000,
        )
    except ValueError as exc:
        assert str(exc) == "bounded_renewal_absolute_expiry_ceiling"
    else:
        raise AssertionError("absolute expiry ceiling bypassed")

    store = BoundedRenewalStore(root / "renewal-store")
    store.initialize(state)
    first = build_governed_renewal_receipt(
        state=state,
        lease_renewal_receipt=first_inner,
        renewal_authority_id="renewal-board",
        authority_receipt_digest=sha("authority-one"),
        now_ms=41_000,
    )
    applied = store.commit(receipt=first, now_ms=41_001)
    assert applied["status"] == "APPLIED"
    current = applied["state"]
    assert store.commit(receipt=first, now_ms=41_002)["status"] == "REPLAYED"

    cooldown_inner = _inner(
        current["current_lease_state"],
        expiry=55_000,
        now_ms=41_500,
        tag="cooldown",
    )
    try:
        build_governed_renewal_receipt(
            state=current,
            lease_renewal_receipt=cooldown_inner,
            renewal_authority_id="renewal-board",
            authority_receipt_digest=sha("authority-cooldown"),
            now_ms=41_500,
        )
    except ValueError as exc:
        assert str(exc) == "bounded_renewal_cooldown_active"
    else:
        raise AssertionError("renewal cooldown bypassed")

    second_inner = _inner(
        current["current_lease_state"], expiry=60_000, now_ms=42_000, tag="two"
    )
    second = build_governed_renewal_receipt(
        state=current,
        lease_renewal_receipt=second_inner,
        renewal_authority_id="renewal-board",
        authority_receipt_digest=sha("authority-two"),
        now_ms=42_000,
    )
    applied = store.commit(receipt=second, now_ms=42_001)
    assert applied["status"] == "APPLIED"
    current = applied["state"]
    policy = current["policies"][HOST_LICENSE]
    assert policy["renewal_count"] == 2
    assert policy["cumulative_added_uses"] == 2
    assert policy["cumulative_added_cost_units"] == 4
    assert policy["status"] == ESCALATION_REQUIRED

    try:
        third_inner = _inner(
            current["current_lease_state"],
            expiry=61_000,
            now_ms=43_000,
            tag="three",
        )
        build_governed_renewal_receipt(
            state=current,
            lease_renewal_receipt=third_inner,
            renewal_authority_id="renewal-board",
            authority_receipt_digest=sha("authority-three"),
            now_ms=43_000,
        )
    except ValueError as exc:
        assert str(exc) in {
            "renewal_expiry_not_extended",
            "bounded_renewal_escalation_required",
        }
    else:
        raise AssertionError("renewal after ceiling accepted")

    snapshot = root / "renewal-store" / "renewal-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except BoundedRenewalStoreError as exc:
        assert str(exc) == "renewal_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt renewal snapshot accepted")
    store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert store.ledger_commit_count() == 2
    return recovered
