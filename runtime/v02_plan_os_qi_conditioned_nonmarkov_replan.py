from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_replan_fixture_v0_2 import (
    apply,
    candidate,
    event,
    prepared_constrained_state,
    source_current_plan,
    source_learn_state,
)
from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
    build_decision_receipt,
    build_qi_condition_packet,
    build_replan_phase_receipt,
    build_synthesis_packet,
)
from runtime.kuuos_plan_os_replan_store_v0_2 import ReplanStore, ReplanStoreError
from runtime.kuuos_plan_os_replan_types_v0_2 import (
    copy_non_authority,
    qi_condition_packet_digest,
    replan_phase_receipt_digest,
    synthesis_packet_digest,
)


def _finish(
    *,
    store: ReplanStore,
    state: dict,
    selected_candidate_id: str,
    tick: int,
) -> tuple[dict, dict]:
    receipt = build_decision_receipt(
        state=state,
        decision_os_state_digest=sha("decision-os-state-" + selected_candidate_id),
        decision_basis_digest=sha("decision-basis-" + selected_candidate_id),
        wa_relational_harmony_digest=sha("wa-harmony-" + selected_candidate_id),
        selected_candidate_id=selected_candidate_id,
        retained_candidate_ids=[
            item["candidate_id"]
            for item in state["candidates"]
            if item["candidate_id"] != selected_candidate_id
        ],
        dissent_evidence_digests=[sha("dissent")],
        minority_stakeholder_digests=[sha("minority")],
        decided_at_ms=310_000 + tick,
    )
    state = apply(store, state, "deliberate", {"decision_receipt": receipt}, tick)
    selected = next(
        item for item in state["candidates"] if item["candidate_id"] == selected_candidate_id
    )
    synthesis = build_synthesis_packet(
        state=state,
        next_plan_goal_digest=selected["goal_digest"],
        next_plan_step_template_digests=selected["step_template_digests"],
        next_observation_point_digests=[selected["expected_observation_digest"]],
        next_verification_criterion_digests=[selected["verification_criterion_digest"]],
        next_stop_condition_digests=selected["stop_condition_digests"],
        next_rollback_point_digests=[selected["rollback_point_digest"]],
        resource_envelope_digest=sha("next-resource-envelope"),
        authority_boundary_digest=sha("next-authority-boundary"),
    )
    state = apply(store, state, "synthesize", {"synthesis_packet": synthesis}, tick + 1)
    commit_event = event(
        state,
        "commit_next",
        {
            "next_plan_basis_committed": True,
            "next_plan_phase_required": True,
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
            "plan_not_execution": True,
            "decision_not_execution": True,
            "qi_context_only": True,
            "host_license_granted": False,
            "non_authority": copy_non_authority(),
        },
        tick + 2,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _high_hysteresis_blocks_switch(
    root: Path, current_plan: dict, failed_learn: dict
) -> dict:
    candidates = [
        candidate(
            "repair-switch",
            "repair",
            target_scope="plan_assumption",
            cost=0.5,
            risk=0.3,
            transition_distance=0.5,
            switch_benefit=0.45,
        ),
        candidate(
            "hold-stable",
            "hold",
            target_scope="no_change",
            cost=0.0,
            risk=0.0,
            transition_distance=0.0,
            switch_benefit=0.0,
        ),
    ]
    store, state = prepared_constrained_state(
        root=root,
        replan_id="replan-high-hysteresis",
        current_plan=current_plan,
        learn_state=failed_learn,
        candidates=candidates,
        hysteresis=0.40,
        recovery=0.80,
        transition_readiness=0.80,
        oscillation_count=4,
    )
    assert "repair-switch" not in state["admissible_candidate_ids"]
    assert "hold-stable" in state["admissible_candidate_ids"]
    try:
        build_decision_receipt(
            state=state,
            decision_os_state_digest=sha("bad-decision"),
            decision_basis_digest=sha("bad-basis"),
            wa_relational_harmony_digest=sha("bad-wa"),
            selected_candidate_id="repair-switch",
            retained_candidate_ids=["hold-stable"],
            dissent_evidence_digests=[],
            minority_stakeholder_digests=[],
            decided_at_ms=320_000,
        )
    except ValueError as exc:
        assert str(exc) == "decision_selected_candidate_not_admissible"
    else:
        raise AssertionError("hysteresis-blocked switch was selected")
    hold, _ = _finish(
        store=store,
        state=state,
        selected_candidate_id="hold-stable",
        tick=40,
    )
    assert hold["route"] == "HOLD"
    return hold


def _qi_authority_claim_rejected(
    root: Path, current_plan: dict, failed_learn: dict
) -> None:
    store = ReplanStore(root)
    from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
        build_history_packet,
        build_initial_replan_state,
    )

    state = store.initialize(
        build_initial_replan_state(
            replan_id="replan-qi-authority",
            current_plan_state=current_plan,
            learn_state=failed_learn,
            current_cycle_index=2,
            plan_budget=1.0,
            maximum_candidate_risk=0.5,
            base_switch_threshold=0.1,
            now_ms=300_000,
        )
    )
    history = build_history_packet(
        state=state,
        previous_plan_change_digests=[],
        successful_transition_digests=[],
        failed_transition_digests=[],
        oscillation_history_digests=[],
        recovery_history_digests=[],
        stagnation_history_digests=[],
        action_history_digest=sha("a"),
        observation_history_digest=sha("o"),
        verification_history_digest=sha("v"),
        learning_history_digest=sha("l"),
        history_window=4,
        path_dependence_digest=sha("p"),
    )
    state = apply(store, state, "history", {"history_packet": history}, 60)
    qi = build_qi_condition_packet(
        state=state,
        process_tensor_digest=sha("tensor"),
        process_history_digest=sha("history"),
        activation=0.5,
        stagnation=0.2,
        tension=0.2,
        recovery=0.5,
        coherence=0.6,
        coupling=0.5,
        transition_readiness=0.7,
        local_global_balance=0.6,
        observation_debt=0.2,
        hysteresis=0.1,
        memory_horizon=8,
        intervention_history_digest=sha("interventions"),
    )
    qi["qi_grants_execution_authority"] = True
    qi["qi_condition_packet_digest"] = ""
    qi["qi_condition_packet_digest"] = qi_condition_packet_digest(qi)
    result = store.apply(event(state, "qi_condition", {"qi_condition_packet": qi}, 61))
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["qi_condition_qi_grants_execution_authority_invalid"]


def _present_activation_rejected(
    root: Path, current_plan: dict, failed_learn: dict
) -> None:
    candidates = [
        candidate(
            "repair",
            "repair",
            target_scope="plan_assumption",
            cost=0.4,
            risk=0.25,
            transition_distance=0.4,
            switch_benefit=0.8,
        ),
        candidate(
            "hold",
            "hold",
            target_scope="no_change",
            cost=0.0,
            risk=0.0,
            transition_distance=0.0,
            switch_benefit=0.0,
        ),
    ]
    store, state = prepared_constrained_state(
        root=root,
        replan_id="replan-present-activation",
        current_plan=current_plan,
        learn_state=failed_learn,
        candidates=candidates,
    )
    receipt = build_decision_receipt(
        state=state,
        decision_os_state_digest=sha("decision"),
        decision_basis_digest=sha("basis"),
        wa_relational_harmony_digest=sha("wa"),
        selected_candidate_id="repair",
        retained_candidate_ids=["hold"],
        dissent_evidence_digests=[],
        minority_stakeholder_digests=[],
        decided_at_ms=330_000,
    )
    state = apply(store, state, "deliberate", {"decision_receipt": receipt}, 70)
    selected = next(item for item in state["candidates"] if item["candidate_id"] == "repair")
    packet = build_synthesis_packet(
        state=state,
        next_plan_goal_digest=selected["goal_digest"],
        next_plan_step_template_digests=selected["step_template_digests"],
        next_observation_point_digests=[selected["expected_observation_digest"]],
        next_verification_criterion_digests=[selected["verification_criterion_digest"]],
        next_stop_condition_digests=selected["stop_condition_digests"],
        next_rollback_point_digests=[selected["rollback_point_digest"]],
        resource_envelope_digest=sha("resource"),
        authority_boundary_digest=sha("authority"),
    )
    packet["active_now"] = True
    packet["next_plan_basis_digest"] = sha(
        {
            key: value
            for key, value in packet.items()
            if key not in {"synthesis_packet_digest", "next_plan_basis_digest"}
        }
    )
    packet["synthesis_packet_digest"] = ""
    packet["synthesis_packet_digest"] = synthesis_packet_digest(packet)
    result = store.apply(event(state, "synthesize", {"synthesis_packet": packet}, 71))
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["synthesis_active_now_invalid"]


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v02-") as temporary:
        root = Path(temporary)
        current_plan = source_current_plan(root / "current")
        failed_learn = source_learn_state(root / "failed-learn", verdict="FAILED")
        assert current_plan["mission_contract_digest"] == failed_learn["mission_contract_digest"]

        candidates = [
            candidate(
                "repair-primary",
                "repair",
                target_scope="plan_assumption",
                cost=0.5,
                risk=0.3,
                transition_distance=0.5,
                switch_benefit=0.8,
            ),
            candidate(
                "slow-down",
                "slow_down",
                target_scope="plan_assumption",
                cost=0.2,
                risk=0.15,
                transition_distance=0.2,
                switch_benefit=0.5,
            ),
            candidate(
                "hold-safe",
                "hold",
                target_scope="no_change",
                cost=0.0,
                risk=0.0,
                transition_distance=0.0,
                switch_benefit=0.0,
            ),
        ]
        store, state = prepared_constrained_state(
            root=root / "repair-replan",
            replan_id="replan-repair-primary",
            current_plan=current_plan,
            learn_state=failed_learn,
            candidates=candidates,
            hysteresis=0.10,
            recovery=0.30,
            transition_readiness=0.80,
            oscillation_count=1,
        )
        assert "repair-primary" in state["admissible_candidate_ids"]
        committed, commit_event = _finish(
            store=store,
            state=state,
            selected_candidate_id="repair-primary",
            tick=10,
        )
        assert committed["route"] == "REPAIR_PLAN_CANDIDATE"
        assert committed["next_plan_basis_committed"] is True
        assert committed["next_plan_phase_required"] is True
        assert committed["active_now"] is False
        assert committed["active_from_cycle"] == committed["current_cycle_index"] + 1
        assert committed["current_cycle_unchanged"] is True
        assert committed["past_plan_unchanged"] is True
        assert committed["host_license_granted"] is False

        phase_receipt = build_replan_phase_receipt(
            state=committed,
            mission_cycle_state_digest=sha("mission-cycle-replan-state"),
            replan_phase_event_digest=sha("mission-cycle-replan-event"),
            now_ms=311_000,
        )
        assert phase_receipt["mission_cycle_phase"] == "replan"
        assert phase_receipt["active_now"] is False
        assert phase_receipt["next_plan_phase_required"] is True
        assert phase_receipt["replan_phase_receipt_digest"] == replan_phase_receipt_digest(
            phase_receipt
        )

        before_replay = store.ledger_commit_count()
        replay = store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        snapshot_path = root / "repair-replan" / "replan-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except ReplanStoreError as exc:
            assert str(exc) == "replan_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt replan snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["replan_state_digest"] == recovered["replan_state_digest"]

        hold = _high_hysteresis_blocks_switch(
            root / "high-hysteresis", current_plan, failed_learn
        )
        _qi_authority_claim_rejected(root / "qi-authority", current_plan, failed_learn)
        _present_activation_rejected(
            root / "present-activation", current_plan, failed_learn
        )

        return {
            "status": "PLAN_OS_QI_CONDITIONED_NONMARKOV_REPLAN_V0_2_OK",
            "route": committed["route"],
            "selected_candidate_id": committed["selected_candidate_id"],
            "next_plan_basis_digest": committed["next_plan_basis_digest"],
            "active_from_cycle": committed["active_from_cycle"],
            "active_now": committed["active_now"],
            "next_plan_phase_required": committed["next_plan_phase_required"],
            "high_hysteresis_route": hold["route"],
            "ledger_commits": store.ledger_commit_count(),
            "recovered_replan_state_digest": recovered["replan_state_digest"],
            "replan_phase_receipt_digest": phase_receipt[
                "replan_phase_receipt_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
