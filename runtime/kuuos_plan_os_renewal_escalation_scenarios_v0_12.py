from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_bounded_renewal_scenarios_v0_11 import (
    run_bounded_renewal,
)
from runtime.kuuos_plan_os_capability_rotation_types_v0_9 import HOST_LICENSE
from runtime.kuuos_plan_os_renewal_escalation_decision_v0_12 import (
    apply_escalation_decision,
    build_escalation_decision,
)
from runtime.kuuos_plan_os_renewal_escalation_state_v0_12 import (
    build_renewal_escalation_state,
)
from runtime.kuuos_plan_os_renewal_escalation_store_v0_12 import (
    RenewalEscalationStore,
    RenewalEscalationStoreError,
)
from runtime.kuuos_plan_os_renewal_escalation_types_v0_12 import (
    DENY,
    HANDOVER_PENDING,
    HUMAN_HANDOVER,
    RE_ROTATE,
    RESOLVED_DENIED,
    REROTATION_AUTHORIZED,
)


def _open_state(root: Path) -> dict:
    bounded = run_bounded_renewal(root / "v11-source")
    return build_renewal_escalation_state(
        bounded_renewal_state=bounded,
        capability_kind=HOST_LICENSE,
        now_ms=70_000,
    )


def run_deny(root: Path) -> dict:
    state = _open_state(root)
    try:
        build_escalation_decision(
            state=state,
            route=DENY,
            governance_authority_id="governance-board",
            governance_receipt_digest=sha("deny-governance"),
            target_owner_id="owner-beta",
            now_ms=70_100,
        )
    except ValueError as exc:
        assert str(exc) == "deny_route_extra_fields_forbidden"
    else:
        raise AssertionError("deny route accepted extra continuation fields")
    decision = build_escalation_decision(
        state=state,
        route=DENY,
        governance_authority_id="governance-board",
        governance_receipt_digest=sha("deny-governance"),
        now_ms=70_100,
    )
    applied = apply_escalation_decision(state, decision)
    assert applied["status"] == "APPLIED"
    resolved = applied["state"]
    assert resolved["status"] == RESOLVED_DENIED
    assert resolved["continuation_granted"] is False
    assert resolved["old_lease_lineage_closed"] is True
    assert apply_escalation_decision(resolved, decision)["status"] == "REPLAYED"
    return resolved


def run_handover(root: Path) -> dict:
    state = _open_state(root)
    try:
        build_escalation_decision(
            state=state,
            route=HUMAN_HANDOVER,
            governance_authority_id="governance-board",
            governance_receipt_digest=sha("handover-governance"),
            target_owner_id=state["current_owner_id"],
            human_acceptance_digest=sha("same-owner-acceptance"),
            now_ms=70_200,
        )
    except ValueError as exc:
        assert str(exc) == "handover_target_must_differ"
    else:
        raise AssertionError("same-owner handover accepted")
    decision = build_escalation_decision(
        state=state,
        route=HUMAN_HANDOVER,
        governance_authority_id="governance-board",
        governance_receipt_digest=sha("handover-governance"),
        target_owner_id="human-owner-gamma",
        human_acceptance_digest=sha("human-gamma-acceptance"),
        now_ms=70_200,
    )
    applied = apply_escalation_decision(state, decision)
    assert applied["status"] == "APPLIED"
    resolved = applied["state"]
    assert resolved["status"] == HANDOVER_PENDING
    assert resolved["target_owner_id"] == "human-owner-gamma"
    assert resolved["new_v09_chain_required"] is False
    return resolved


def run_rerotation(root: Path) -> dict:
    state = _open_state(root)
    try:
        build_escalation_decision(
            state=state,
            route=RE_ROTATE,
            governance_authority_id="governance-board",
            governance_receipt_digest=sha("rerotation-governance"),
            target_owner_id="owner-alpha",
            rerotation_scope_digest=sha("rerotation-scope"),
            now_ms=70_300,
        )
    except ValueError as exc:
        assert str(exc) == "rerotation_owner_mismatch"
    else:
        raise AssertionError("rerotation accepted substituted owner")

    decision = build_escalation_decision(
        state=state,
        route=RE_ROTATE,
        governance_authority_id="governance-board",
        governance_receipt_digest=sha("rerotation-governance"),
        target_owner_id=state["current_owner_id"],
        rerotation_scope_digest=sha("rerotation-scope"),
        now_ms=70_300,
    )
    store = RenewalEscalationStore(root / "escalation-store")
    store.initialize(state)
    applied = store.commit(decision=decision, now_ms=70_301)
    assert applied["status"] == "APPLIED"
    resolved = applied["state"]
    assert resolved["status"] == REROTATION_AUTHORIZED
    assert resolved["next_epoch_index"] == state["current_epoch_index"] + 1
    assert resolved["next_epoch_seed_digest"]
    assert resolved["new_v09_chain_required"] is True
    assert resolved["continuation_granted"] is True
    assert resolved["execution_granted"] is False
    assert store.commit(decision=decision, now_ms=70_302)["status"] == "REPLAYED"

    conflicting = build_escalation_decision(
        state=state,
        route=DENY,
        governance_authority_id="governance-board",
        governance_receipt_digest=sha("conflicting-deny"),
        now_ms=70_400,
    )
    rejected = store.commit(decision=conflicting, now_ms=70_401)
    assert rejected["status"] == "REJECTED"
    assert "escalation_already_resolved" in rejected["errors"]

    snapshot = root / "escalation-store" / "escalation-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except RenewalEscalationStoreError as exc:
        assert str(exc) == "escalation_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt escalation snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["renewal_escalation_state_digest"] == recovered[
        "renewal_escalation_state_digest"
    ]
    return recovered
