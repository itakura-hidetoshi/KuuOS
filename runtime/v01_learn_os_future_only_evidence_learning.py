from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_fixture_v0_1 import (
    apply,
    event,
    prepared_gated_state,
    source_verify_state,
)
from runtime.kuuos_learn_os_kernel_v0_1 import (
    build_abstraction_packet,
    build_initial_learn_state,
    build_learn_event,
    build_learn_phase_receipt,
    build_learning_challenge_packet,
    build_learning_delta,
)
from runtime.kuuos_learn_os_store_v0_1 import LearnStore, LearnStoreError
from runtime.kuuos_learn_os_types_v0_1 import (
    copy_non_authority,
    learn_phase_receipt_digest,
    learning_delta_digest,
)
from runtime.kuuos_verify_os_fixture_v0_1 import (
    prepared_corroborated_state,
    source_observe_state,
)
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify


def _finish(
    *, store: LearnStore, state: dict, tick: int
) -> tuple[dict, dict]:
    commit_event = event(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "active_now": False,
            "activation_requires_replan": True,
            "current_cycle_unchanged": True,
            "past_records_unchanged": True,
            "counterevidence_preserved": True,
            "verification_not_truth": True,
            "qi_context_only": True,
            "automatic_truth_promotion": False,
            "automatic_belief_update": False,
            "automatic_plan_update": False,
            "automatic_criterion_update": False,
            "automatic_policy_activation": False,
            "automatic_rollback": False,
            "automatic_self_modification": False,
            "non_authority": copy_non_authority(),
        },
        tick,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _incompatible_learning_kind_rejected(root: Path, failed_verify: dict) -> None:
    store = LearnStore(root)
    state = store.initialize(
        build_initial_learn_state(
            learn_id="learn-incompatible-kind",
            verify_state=failed_verify,
            now_ms=200_000,
        )
    )
    abstraction = build_abstraction_packet(
        state=state,
        supported_pattern_digests=[],
        failed_pattern_digests=[sha("failed-pattern")],
        unresolved_pattern_digests=[],
        counterevidence_digests=list(state["source_counterevidence_digests"]),
        uncertainty_digest=sha("uncertainty"),
        residual_digest=sha("residual"),
        scope_digest=sha("scope"),
        qi_process_history_digest=sha("qi-history"),
        abstraction_method_digest=sha("abstraction-method"),
    )
    state = apply(store, state, "abstract", {"abstraction_packet": abstraction}, 20)
    challenge = build_learning_challenge_packet(
        state=state,
        alternative_explanation_digests=[],
        anti_overgeneralization_test_digests=[sha("anti-generalization")],
        distribution_shift_risk_digest=sha("shift-risk"),
        observer_bias_risk_digest=sha("observer-risk"),
        negative_transfer_risk_digest=sha("transfer-risk"),
    )
    state = apply(
        store,
        state,
        "challenge",
        {"learning_challenge_packet": challenge},
        21,
    )
    try:
        build_learning_delta(
            state=state,
            learning_delta_id="bad-reinforcement",
            learning_kind="reinforcement",
            target_scope="belief_candidate",
            before_digest=sha("before"),
            after_candidate_digest=sha("after"),
            change_rationale_digest=sha("rationale"),
            applicability_condition_digest=sha("applicability"),
            reversal_condition_digest=sha("reversal"),
            expiration_condition_digest=sha("expiration"),
        )
    except ValueError as exc:
        assert str(exc) == "learning_kind_incompatible_with_verification_route"
    else:
        raise AssertionError("failed verification accepted reinforcement learning")


def _present_activation_rejected(root: Path, passed_verify: dict) -> None:
    store, state = prepared_gated_state(
        root=root,
        learn_id="learn-present-activation",
        verify_state=passed_verify,
        learning_kind="reinforcement",
        target_scope="belief_candidate",
    )
    del store
    delta = dict(state["learning_delta"])
    delta["active_now"] = True
    delta["learning_delta_digest"] = ""
    delta["learning_delta_digest"] = learning_delta_digest(delta)

    fresh_store = LearnStore(root.parent / "activation-reject-fresh")
    fresh = fresh_store.initialize(
        build_initial_learn_state(
            learn_id="learn-present-activation-fresh",
            verify_state=passed_verify,
            now_ms=200_000,
        )
    )
    abstraction = build_abstraction_packet(
        state=fresh,
        supported_pattern_digests=[sha("supported")],
        failed_pattern_digests=[],
        unresolved_pattern_digests=[],
        counterevidence_digests=list(fresh["source_counterevidence_digests"]),
        uncertainty_digest=sha("activation-uncertainty"),
        residual_digest=sha("activation-residual"),
        scope_digest=sha("activation-scope"),
        qi_process_history_digest=sha("activation-qi"),
        abstraction_method_digest=sha("activation-method"),
    )
    fresh = apply(
        fresh_store,
        fresh,
        "abstract",
        {"abstraction_packet": abstraction},
        30,
    )
    challenge = build_learning_challenge_packet(
        state=fresh,
        alternative_explanation_digests=[],
        anti_overgeneralization_test_digests=[sha("activation-test")],
        distribution_shift_risk_digest=sha("activation-shift"),
        observer_bias_risk_digest=sha("activation-observer"),
        negative_transfer_risk_digest=sha("activation-transfer"),
    )
    fresh = apply(
        fresh_store,
        fresh,
        "challenge",
        {"learning_challenge_packet": challenge},
        31,
    )
    delta["learn_id"] = fresh["learn_id"]
    delta["source_verify_state_digest"] = fresh["source_verify_state_digest"]
    delta["source_verification_evidence_digest"] = fresh[
        "source_verification_evidence_digest"
    ]
    delta["abstraction_packet_digest"] = fresh["abstraction_packet_digest"]
    delta["learning_challenge_packet_digest"] = fresh[
        "learning_challenge_packet_digest"
    ]
    delta["source_scope_digest"] = fresh["abstraction_packet"]["scope_digest"]
    delta["source_uncertainty_digest"] = fresh["abstraction_packet"][
        "uncertainty_digest"
    ]
    delta["source_counterevidence_digest"] = fresh["source_counterevidence_digest"]
    delta["qi_process_history_digest"] = fresh["abstraction_packet"][
        "qi_process_history_digest"
    ]
    delta["learning_delta_digest"] = ""
    delta["learning_delta_digest"] = learning_delta_digest(delta)
    result = fresh_store.apply(
        build_learn_event(
            state=fresh,
            target_phase="delta",
            artifact_digest=sha("activation-artifact"),
            payload={"learning_delta": delta},
            now_ms=210_032,
        )
    )
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["learning_delta_active_now_invalid"]


def _counterevidence_erasure_rejected(root: Path) -> None:
    observe = source_observe_state(root / "observe", verdict="DIVERGENT")
    verify_store, verify_state = prepared_corroborated_state(
        root=root / "verify",
        verify_id="learn-counterevidence-source",
        observe_state=observe,
        falsifier_triggered=True,
        admissible=True,
    )
    committed, _ = finish_verify(
        store=verify_store,
        state=verify_state,
        verdict="FAILED",
        criterion_satisfied=False,
        tick=40,
    )
    learn_state = build_initial_learn_state(
        learn_id="learn-counterevidence-erasure",
        verify_state=committed,
        now_ms=200_000,
    )
    assert learn_state["source_counterevidence_digests"]
    try:
        build_abstraction_packet(
            state=learn_state,
            supported_pattern_digests=[],
            failed_pattern_digests=[sha("failure")],
            unresolved_pattern_digests=[],
            counterevidence_digests=[],
            uncertainty_digest=sha("uncertainty"),
            residual_digest=sha("residual"),
            scope_digest=sha("scope"),
            qi_process_history_digest=sha("qi"),
            abstraction_method_digest=sha("method"),
        )
    except ValueError as exc:
        assert str(exc) == "abstraction_counterevidence_binding_mismatch"
    else:
        raise AssertionError("counterevidence erasure accepted")


def _anti_overgeneralization_required(root: Path, passed_verify: dict) -> None:
    store = LearnStore(root)
    state = store.initialize(
        build_initial_learn_state(
            learn_id="learn-anti-generalization",
            verify_state=passed_verify,
            now_ms=200_000,
        )
    )
    abstraction = build_abstraction_packet(
        state=state,
        supported_pattern_digests=[sha("supported")],
        failed_pattern_digests=[],
        unresolved_pattern_digests=[],
        counterevidence_digests=list(state["source_counterevidence_digests"]),
        uncertainty_digest=sha("uncertainty"),
        residual_digest=sha("residual"),
        scope_digest=sha("scope"),
        qi_process_history_digest=sha("qi"),
        abstraction_method_digest=sha("method"),
    )
    state = apply(store, state, "abstract", {"abstraction_packet": abstraction}, 50)
    try:
        build_learning_challenge_packet(
            state=state,
            alternative_explanation_digests=[],
            anti_overgeneralization_test_digests=[],
            distribution_shift_risk_digest=sha("shift"),
            observer_bias_risk_digest=sha("observer"),
            negative_transfer_risk_digest=sha("transfer"),
        )
    except ValueError as exc:
        assert str(exc) == "anti_overgeneralization_test_digests_nonempty_required"
    else:
        raise AssertionError("challenge without anti-overgeneralization test accepted")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-learn-os-v01-") as temporary:
        root = Path(temporary)
        passed_verify = source_verify_state(root / "passed-source", verdict="PASSED")
        failed_verify = source_verify_state(root / "failed-source", verdict="FAILED")
        indeterminate_verify = source_verify_state(
            root / "indeterminate-source", verdict="INDETERMINATE"
        )

        reinforcement_store, reinforcement_state = prepared_gated_state(
            root=root / "reinforcement",
            learn_id="learn-reinforcement",
            verify_state=passed_verify,
            learning_kind="reinforcement",
            target_scope="belief_candidate",
        )
        reinforcement, commit_event = _finish(
            store=reinforcement_store,
            state=reinforcement_state,
            tick=5,
        )
        assert reinforcement["route"] == "LEARNING_REINFORCEMENT_CANDIDATE"
        assert reinforcement["learning_recorded"] is True
        assert reinforcement["learning_debt_discharged"] is True
        assert reinforcement["replan_required"] is True
        assert reinforcement["active_now"] is False
        assert reinforcement["current_cycle_unchanged"] is True
        assert reinforcement["past_records_unchanged"] is True

        phase_receipt = build_learn_phase_receipt(
            state=reinforcement,
            mission_cycle_state_digest=sha("mission-cycle-learn-state"),
            learn_phase_event_digest=sha("mission-cycle-learn-event"),
            now_ms=210_100,
        )
        assert phase_receipt["mission_cycle_phase"] == "learn"
        assert phase_receipt["future_only"] is True
        assert phase_receipt["memory_overwrite"] is False
        assert phase_receipt["active_now"] is False
        assert phase_receipt["replan_required"] is True
        assert phase_receipt["learn_phase_receipt_digest"] == learn_phase_receipt_digest(
            phase_receipt
        )

        before_replay = reinforcement_store.ledger_commit_count()
        replay = reinforcement_store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert reinforcement_store.ledger_commit_count() == before_replay

        snapshot_path = root / "reinforcement" / "learn-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            reinforcement_store.recover(require_snapshot_match=True)
        except LearnStoreError as exc:
            assert str(exc) == "learn_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt learn snapshot accepted")
        repaired = reinforcement_store.repair_snapshot()
        recovered = reinforcement_store.recover(require_snapshot_match=True)
        assert repaired["learn_state_digest"] == recovered["learn_state_digest"]

        repair_store, repair_state = prepared_gated_state(
            root=root / "repair",
            learn_id="learn-repair",
            verify_state=failed_verify,
            learning_kind="repair",
            target_scope="plan_assumption",
        )
        repair, _ = _finish(store=repair_store, state=repair_state, tick=60)
        assert repair["route"] == "LEARNING_REPAIR_CANDIDATE"
        assert repair["corrective_action_required"] is True
        assert repair["reobservation_required"] is False
        assert repair["active_now"] is False

        reobserve_store, reobserve_state = prepared_gated_state(
            root=root / "reobservation",
            learn_id="learn-reobservation",
            verify_state=indeterminate_verify,
            learning_kind="reobservation",
            target_scope="observation_policy",
        )
        reobserve, _ = _finish(
            store=reobserve_store,
            state=reobserve_state,
            tick=70,
        )
        assert reobserve["route"] == "LEARNING_REOBSERVATION_CANDIDATE"
        assert reobserve["reobservation_required"] is True
        assert reobserve["corrective_action_required"] is False

        hold_store, hold_state = prepared_gated_state(
            root=root / "hold",
            learn_id="learn-hold",
            verify_state=passed_verify,
            learning_kind="reinforcement",
            target_scope="belief_candidate",
            admissible=False,
        )
        hold, _ = _finish(store=hold_store, state=hold_state, tick=80)
        assert hold["route"] == "LEARNING_HOLD"
        assert hold["active_now"] is False
        assert hold["replan_required"] is True

        _incompatible_learning_kind_rejected(
            root / "incompatible-kind", failed_verify
        )
        _present_activation_rejected(root / "activation-reject", passed_verify)
        _counterevidence_erasure_rejected(root / "counterevidence-erasure")
        _anti_overgeneralization_required(
            root / "anti-generalization", passed_verify
        )

        return {
            "status": "LEARN_OS_FUTURE_ONLY_EVIDENCE_LEARNING_V0_1_OK",
            "reinforcement_route": reinforcement["route"],
            "repair_route": repair["route"],
            "reobservation_route": reobserve["route"],
            "hold_route": hold["route"],
            "future_only": phase_receipt["future_only"],
            "active_now": phase_receipt["active_now"],
            "replan_required": phase_receipt["replan_required"],
            "ledger_commits": reinforcement_store.ledger_commit_count(),
            "recovered_learn_state_digest": recovered["learn_state_digest"],
            "learn_phase_receipt_digest": phase_receipt[
                "learn_phase_receipt_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
