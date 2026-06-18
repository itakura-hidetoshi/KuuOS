from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_plan_os_reentry_fixture_v0_7 import (
    controller_for,
    terminal_state,
    valid_receipt,
)
from runtime.kuuos_plan_os_reentry_kernel_v0_7 import (
    apply_reentry_event,
    build_external_reentry_receipt,
    build_reentry_controller_state,
    build_reentry_decision,
    build_reentry_event,
)
from runtime.kuuos_plan_os_reentry_store_v0_7 import (
    ReentryControllerStore,
    ReentryStoreError,
)
from runtime.kuuos_plan_os_reentry_types_v0_7 import (
    ACCEPT_HANDOVER,
    RESUME_HOLD,
    receipt_digest,
)


def run_hold_resume(root: Path) -> dict:
    controller = controller_for("HOLD")
    receipt = valid_receipt(controller)
    decision = build_reentry_decision(
        controller_state=controller, receipt=receipt, now_ms=3_100
    )
    event = build_reentry_event(
        controller_state=controller,
        receipt=receipt,
        decision=decision,
        now_ms=3_200,
    )
    store = ReentryControllerStore(root / "hold-store")
    store.initialize(controller)
    result = store.apply(event)
    assert result["status"] == "APPLIED"
    state = result["state"]
    assert state["status"] == "REENTERED"
    assert state["current_owner_id"] == "owner-alpha"
    assert state["target_active_state"]["status"] == "ACTIVE"
    assert state["target_active_state"]["next_generation_authorized"] is True
    assert state["target_active_state"]["execution_granted"] is False
    assert store.apply(event)["status"] == "REPLAYED"
    assert store.ledger_commit_count() == 1

    snapshot = root / "hold-store" / "reentry-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except ReentryStoreError as exc:
        assert str(exc) == "reentry_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt reentry snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["reentry_controller_state_digest"] == recovered[
        "reentry_controller_state_digest"
    ]
    return recovered


def run_handover_acceptance() -> dict:
    controller = controller_for("HANDOVER")
    receipt = valid_receipt(controller)
    decision = build_reentry_decision(
        controller_state=controller, receipt=receipt, now_ms=3_100
    )
    event = build_reentry_event(
        controller_state=controller,
        receipt=receipt,
        decision=decision,
        now_ms=3_200,
    )
    result = apply_reentry_event(controller, event)
    assert result["status"] == "APPLIED"
    state = result["state"]
    assert state["current_owner_id"] == "owner-beta"
    assert state["target_active_state"]["status"] == "ACTIVE"
    assert state["execution_granted"] is False
    try:
        valid_receipt(state)
    except ValueError as exc:
        assert str(exc) == "reentry_controller_already_consumed"
    else:
        raise AssertionError("consumed controller issued a second receipt")
    return state


def verify_rejections() -> list[str]:
    checked: list[str] = []
    try:
        build_reentry_controller_state(
            source_terminal_state=terminal_state("STOPPED"),
            current_owner_id="owner-alpha",
            now_ms=2_000,
        )
    except ValueError as exc:
        assert str(exc) == "reentry_source_must_be_hold_or_handover"
        checked.append("stopped_not_resumable")
    else:
        raise AssertionError("STOPPED state accepted for reentry")

    hold = controller_for("HOLD")
    wrong_owner = build_external_reentry_receipt(
        controller_state=hold,
        kind=RESUME_HOLD,
        proposed_owner_id="owner-beta",
        delegated_by_owner_id="owner-alpha",
        accepted_by_owner_id="owner-beta",
        authority_scope_digest="scope",
        evidence_digest="evidence",
        issued_at_ms=3_000,
        expires_at_ms=4_000,
    )
    try:
        build_reentry_decision(
            controller_state=hold, receipt=wrong_owner, now_ms=3_100
        )
    except ValueError as exc:
        assert str(exc) == "hold_resume_requires_same_owner"
        checked.append("hold_same_owner_required")
    else:
        raise AssertionError("HOLD owner substitution accepted")

    handover = controller_for("HANDOVER")
    same_owner = build_external_reentry_receipt(
        controller_state=handover,
        kind=ACCEPT_HANDOVER,
        proposed_owner_id="owner-alpha",
        delegated_by_owner_id="owner-alpha",
        accepted_by_owner_id="owner-alpha",
        authority_scope_digest="scope",
        evidence_digest="evidence",
        issued_at_ms=3_000,
        expires_at_ms=4_000,
    )
    try:
        build_reentry_decision(
            controller_state=handover, receipt=same_owner, now_ms=3_100
        )
    except ValueError as exc:
        assert str(exc) == "handover_requires_distinct_new_owner"
        checked.append("handover_distinct_owner_required")
    else:
        raise AssertionError("same-owner handover accepted")

    expired = valid_receipt(hold)
    try:
        build_reentry_decision(
            controller_state=hold, receipt=expired, now_ms=4_000
        )
    except ValueError as exc:
        assert str(exc) == "external_reentry_receipt_not_current"
        checked.append("receipt_expiry_enforced")
    else:
        raise AssertionError("expired reentry receipt accepted")

    tampered = deepcopy(valid_receipt(hold))
    tampered["policy_digest"] = "wrong-policy"
    tampered["external_reentry_receipt_digest"] = ""
    tampered["external_reentry_receipt_digest"] = receipt_digest(tampered)
    try:
        build_reentry_decision(
            controller_state=hold, receipt=tampered, now_ms=3_100
        )
    except ValueError as exc:
        assert str(exc) == "external_reentry_policy_digest_mismatch"
        checked.append("policy_binding_enforced")
    else:
        raise AssertionError("policy substitution accepted")
    return checked
