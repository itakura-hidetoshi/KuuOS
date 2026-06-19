from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_reentry_fixture_v0_7 import controller_for, valid_receipt
from runtime.kuuos_plan_os_reentry_kernel_v0_7 import (
    apply_reentry_event,
    build_reentry_decision,
    build_reentry_event,
)
from runtime.kuuos_plan_os_reentry_types_v0_7 import decision_digest
from runtime.kuuos_plan_os_ownership_continuity_kernel_v0_8 import (
    apply_ownership_stage_receipt,
    build_ownership_continuity_state,
    build_ownership_stage_receipt,
)
from runtime.kuuos_plan_os_ownership_continuity_store_v0_8 import (
    OwnershipContinuityStore,
    OwnershipContinuityStoreError,
)
from runtime.kuuos_plan_os_ownership_continuity_types_v0_8 import (
    ACT,
    COMPLETED,
    LEARN,
    OBSERVE,
    PLAN,
    VERIFY,
)
from runtime.v02_act_os_replan_lineage_authority_envelope import (
    run_kernel as run_act,
)
from runtime.v02_learn_os_replan_lineage_future_only_learning_envelope import (
    run_kernel as run_learn,
)
from runtime.v02_observe_os_replan_lineage_observation_envelope import (
    run_kernel as run_observe,
)
from runtime.v02_verify_os_replan_lineage_verification_envelope import (
    run_kernel as run_verify,
)


def _reentry(kind: str) -> tuple[dict, dict, dict, dict, dict]:
    controller = controller_for(kind)
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
    continuity = build_ownership_continuity_state(
        source_controller_state=controller,
        external_reentry_receipt=receipt,
        reentry_decision=decision,
        reentry_event=event,
        reentered_controller_state=result["state"],
        now_ms=4_000,
    )
    return controller, receipt, decision, event, continuity


def _stage_packets(continuity: dict) -> list[tuple[str, str, str, str]]:
    plan = {
        "status": "PLAN_REENTRY_TARGET_ACTIVE",
        "reentry_decision_digest": continuity["reentry_decision_digest"],
        "target_active_state_digest": continuity["target_active_state_digest"],
    }
    act = run_act()
    observe = run_observe()
    verify = run_verify()
    learn = run_learn()
    assert act["status"] == "ACT_OS_REPLAN_LINEAGE_AUTHORITY_ENVELOPE_V0_2_OK"
    assert observe["status"] == "OBSERVE_OS_REPLAN_LINEAGE_OBSERVATION_ENVELOPE_V0_2_OK"
    assert verify["status"] == "VERIFY_OS_REPLAN_LINEAGE_VERIFICATION_ENVELOPE_V0_2_OK"
    assert learn["status"] == "LEARN_OS_REPLAN_LINEAGE_FUTURE_ONLY_LEARNING_ENVELOPE_V0_2_OK"
    return [
        (
            PLAN,
            continuity["reentry_decision_digest"],
            continuity["target_active_state_digest"],
            sha(plan),
        ),
        (
            ACT,
            act["handoff_receipt_digest"],
            act["completion_receipt_digest"],
            sha(act),
        ),
        (
            OBSERVE,
            observe["handoff_receipt_digest"],
            observe["completion_receipt_digest"],
            sha(observe),
        ),
        (
            VERIFY,
            verify["handoff_receipt_digest"],
            verify["completion_receipt_digest"],
            sha(verify),
        ),
        (
            LEARN,
            learn["handoff_receipt_digest"],
            learn["completion_receipt_digest"],
            sha(learn),
        ),
    ]


def run_handover_continuity(root: Path) -> dict:
    controller, receipt, decision, event, continuity = _reentry("HANDOVER")
    assert continuity["previous_owner_id"] == "owner-alpha"
    assert continuity["current_owner_id"] == "owner-beta"
    assert continuity["handover"] is True

    try:
        build_ownership_stage_receipt(
            state=continuity,
            stage=ACT,
            owner_id="owner-beta",
            handoff_receipt_digest=sha("early-act-handoff"),
            completion_receipt_digest=sha("early-act-completion"),
            stage_packet_digest=sha("early-act-packet"),
            now_ms=4_100,
        )
    except ValueError as exc:
        assert str(exc) == "ownership_stage_order_invalid:expected_PLAN"
    else:
        raise AssertionError("out-of-order ACT ownership receipt accepted")

    try:
        build_ownership_stage_receipt(
            state=continuity,
            stage=PLAN,
            owner_id="owner-alpha",
            handoff_receipt_digest=decision["reentry_decision_digest"],
            completion_receipt_digest=continuity["target_active_state_digest"],
            stage_packet_digest=sha("old-owner-plan"),
            now_ms=4_101,
        )
    except ValueError as exc:
        assert str(exc) == "ownership_current_owner_mismatch"
    else:
        raise AssertionError("previous owner reused after handover")

    substituted = deepcopy(decision)
    substituted["next_owner_id"] = "owner-gamma"
    substituted["reentry_decision_digest"] = ""
    substituted["reentry_decision_digest"] = decision_digest(substituted)
    try:
        build_ownership_continuity_state(
            source_controller_state=controller,
            external_reentry_receipt=receipt,
            reentry_decision=substituted,
            reentry_event=event,
            reentered_controller_state=apply_reentry_event(controller, event)["state"],
            now_ms=4_000,
        )
    except ValueError as exc:
        assert str(exc) == "ownership_reentry_decision_not_canonical"
    else:
        raise AssertionError("substituted re-entry owner accepted")

    store = OwnershipContinuityStore(root / "ownership-store")
    store.initialize(continuity)
    state = continuity
    stage_receipts: list[dict] = []
    for offset, (stage, handoff, completion, packet) in enumerate(
        _stage_packets(continuity), start=1
    ):
        if stage == ACT:
            try:
                build_ownership_stage_receipt(
                    state=state,
                    stage=stage,
                    owner_id="owner-alpha",
                    handoff_receipt_digest=handoff,
                    completion_receipt_digest=completion,
                    stage_packet_digest=packet,
                    now_ms=5_000 + offset,
                )
            except ValueError as exc:
                assert str(exc) == "ownership_current_owner_mismatch"
            else:
                raise AssertionError("old owner accepted during ACT")
        wrapper = build_ownership_stage_receipt(
            state=state,
            stage=stage,
            owner_id="owner-beta",
            handoff_receipt_digest=handoff,
            completion_receipt_digest=completion,
            stage_packet_digest=packet,
            now_ms=5_000 + offset,
        )
        applied = store.commit(stage_receipt=wrapper, now_ms=6_000 + offset)
        assert applied["status"] == "APPLIED"
        state = applied["state"]
        stage_receipts.append(wrapper)
        replay = store.commit(stage_receipt=wrapper, now_ms=7_000 + offset)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == offset

    assert state["status"] == COMPLETED
    assert state["stage_index"] == 5
    assert state["current_owner_id"] == "owner-beta"
    assert state["execution_granted"] is False
    try:
        build_ownership_stage_receipt(
            state=state,
            stage=LEARN,
            owner_id="owner-beta",
            handoff_receipt_digest=sha("late-handoff"),
            completion_receipt_digest=sha("late-completion"),
            stage_packet_digest=sha("late-packet"),
            now_ms=8_000,
        )
    except ValueError as exc:
        assert str(exc) == "ownership_continuity_already_completed"
    else:
        raise AssertionError("post-completion ownership receipt accepted")

    snapshot = root / "ownership-store" / "ownership-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except OwnershipContinuityStoreError as exc:
        assert str(exc) == "ownership_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt ownership snapshot accepted")
    repaired = store.repair_snapshot()
    recovered = store.recover(require_snapshot_match=True)
    assert repaired["ownership_continuity_state_digest"] == recovered[
        "ownership_continuity_state_digest"
    ]
    return recovered


def run_hold_continuity() -> dict:
    _, _, decision, _, continuity = _reentry("HOLD")
    assert continuity["handover"] is False
    assert continuity["previous_owner_id"] == "owner-alpha"
    assert continuity["current_owner_id"] == "owner-alpha"
    wrapper = build_ownership_stage_receipt(
        state=continuity,
        stage=PLAN,
        owner_id="owner-alpha",
        handoff_receipt_digest=decision["reentry_decision_digest"],
        completion_receipt_digest=continuity["target_active_state_digest"],
        stage_packet_digest=sha("hold-plan-stage"),
        now_ms=4_100,
    )
    result = apply_ownership_stage_receipt(continuity, wrapper)
    assert result["status"] == "APPLIED"
    return result["state"]
