from __future__ import annotations

import json
import tempfile
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_verify_os_fixture_v0_1 import (
    apply,
    event,
    prepared_corroborated_state,
    source_observe_state,
)
from runtime.kuuos_verify_os_kernel_v0_1 import (
    build_adjudication_receipt,
    build_challenge_packet,
    build_criterion_packet,
    build_initial_verify_state,
    build_verify_phase_receipt,
)
from runtime.kuuos_verify_os_store_v0_1 import VerifyStore, VerifyStoreError
from runtime.kuuos_verify_os_types_v0_1 import (
    copy_non_authority,
    criterion_packet_digest,
    verify_phase_receipt_digest,
)


def _finish(
    *,
    store: VerifyStore,
    state: dict,
    verdict: str,
    criterion_satisfied: bool,
    tick: int,
) -> tuple[dict, dict]:
    adjudication = build_adjudication_receipt(
        state=state,
        adjudication_id=state["verify_id"] + "-adjudication",
        verdict=verdict,
        criterion_satisfied=criterion_satisfied,
        adjudication_method_digest=sha("adjudication-method"),
        rationale_digest=sha("adjudication-rationale-" + verdict),
        adjudicated_at_ms=120_000 + tick,
    )
    state = apply(
        store,
        state,
        "adjudicate",
        {"adjudication_receipt": adjudication},
        tick,
    )
    commit_event = event(
        state,
        "commit",
        {
            "verification_not_truth": True,
            "causal_attribution_not_granted": True,
            "counterevidence_preserved": True,
            "learning_required": True,
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_belief_update": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "automatic_causal_attribution": False,
            "non_authority": copy_non_authority(),
        },
        tick + 1,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _criterion_substitution_rejected(root: Path, observe_state: dict) -> None:
    store = VerifyStore(root)
    state = store.initialize(
        build_initial_verify_state(
            verify_id="verify-criterion-substitution",
            observe_state=observe_state,
            now_ms=110_000,
        )
    )
    criterion = build_criterion_packet(
        state=state,
        criterion_type="contract",
        evaluation_method_digest=sha("criterion-method"),
        success_condition_digest=sha("criterion-success"),
        failure_condition_digest=sha("criterion-failure"),
        falsification_condition_digest=sha("criterion-falsifier"),
        evidence_requirements_digest=sha("criterion-evidence"),
        minimum_independent_assessors=2,
    )
    criterion["verification_criterion_digest"] = sha("substituted-criterion")
    criterion["criterion_packet_digest"] = ""
    criterion["criterion_packet_digest"] = criterion_packet_digest(criterion)
    result = store.apply(
        event(
            state,
            "criterion",
            {"criterion_packet": criterion},
            20,
        )
    )
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["criterion_packet_verification_criterion_digest_mismatch"]


def _insufficient_assessors_rejected(root: Path, observe_state: dict) -> None:
    store = VerifyStore(root)
    state = store.initialize(
        build_initial_verify_state(
            verify_id="verify-insufficient-assessors",
            observe_state=observe_state,
            now_ms=110_000,
        )
    )
    criterion = build_criterion_packet(
        state=state,
        criterion_type="contract",
        evaluation_method_digest=sha("assessor-method"),
        success_condition_digest=sha("assessor-success"),
        failure_condition_digest=sha("assessor-failure"),
        falsification_condition_digest=sha("assessor-falsifier"),
        evidence_requirements_digest=sha("assessor-evidence"),
        minimum_independent_assessors=2,
    )
    state = apply(
        store,
        state,
        "criterion",
        {"criterion_packet": criterion},
        21,
    )
    try:
        build_challenge_packet(
            state=state,
            counterevidence_digests=[],
            falsification_attempt_digests=[sha("single-falsification")],
            independent_assessor_ids=["only-assessor"],
            assessor_receipt_digests=[sha("only-assessor-receipt")],
            conflict_disclosure_digest=sha("single-assessor-conflict"),
            falsifier_triggered=False,
        )
    except ValueError as exc:
        assert str(exc) == "independent_assessors_insufficient"
    else:
        raise AssertionError("insufficient independent assessors accepted")


def _triggered_falsifier_blocks_passed(root: Path, observe_state: dict) -> None:
    store, state = prepared_corroborated_state(
        root=root,
        verify_id="verify-triggered-falsifier",
        observe_state=observe_state,
        falsifier_triggered=True,
        admissible=True,
    )
    adjudication = build_adjudication_receipt(
        state=state,
        adjudication_id="triggered-falsifier-adjudication",
        verdict="PASSED",
        criterion_satisfied=True,
        adjudication_method_digest=sha("triggered-method"),
        rationale_digest=sha("triggered-rationale"),
        adjudicated_at_ms=120_030,
    )
    result = store.apply(
        event(
            state,
            "adjudicate",
            {"adjudication_receipt": adjudication},
            30,
        )
    )
    assert result["status"] == "REJECTED"
    assert result["errors"] == ["passed_forbids_triggered_falsifier"]


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-verify-os-v01-") as temporary:
        root = Path(temporary)
        matched_observe = source_observe_state(root / "matched-source", verdict="MATCHED")
        divergent_observe = source_observe_state(root / "divergent-source", verdict="DIVERGENT")
        conflicted_observe = source_observe_state(root / "conflicted-source", verdict="CONFLICTED")

        passed_store, passed_state = prepared_corroborated_state(
            root=root / "passed",
            verify_id="verify-passed",
            observe_state=matched_observe,
        )
        passed, commit_event = _finish(
            store=passed_store,
            state=passed_state,
            verdict="PASSED",
            criterion_satisfied=True,
            tick=4,
        )
        assert passed["route"] == "VERIFICATION_PASSED"
        assert passed["verification_recorded"] is True
        assert passed["verification_debt_discharged"] is True
        assert passed["verification_required"] is False
        assert passed["reobservation_required"] is False
        assert passed["corrective_action_required"] is False
        assert passed["learning_required"] is True
        assert passed["automatic_truth_promotion"] is False
        assert passed["automatic_causal_attribution"] is False

        phase_receipt = build_verify_phase_receipt(
            state=passed,
            mission_cycle_state_digest=sha("mission-cycle-verify-state"),
            verify_phase_event_digest=sha("mission-cycle-verify-event"),
            now_ms=120_100,
        )
        assert phase_receipt["mission_cycle_phase"] == "verify"
        assert phase_receipt["verdict"] == "passed"
        assert phase_receipt["verification_not_truth"] is True
        assert phase_receipt["causal_attribution_not_granted"] is True
        assert phase_receipt["verify_phase_receipt_digest"] == verify_phase_receipt_digest(
            phase_receipt
        )

        before_replay = passed_store.ledger_commit_count()
        replay = passed_store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert passed_store.ledger_commit_count() == before_replay

        snapshot_path = root / "passed" / "verify-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            passed_store.recover(require_snapshot_match=True)
        except VerifyStoreError as exc:
            assert str(exc) == "verify_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt verify snapshot accepted")
        repaired = passed_store.repair_snapshot()
        recovered = passed_store.recover(require_snapshot_match=True)
        assert repaired["verify_state_digest"] == recovered["verify_state_digest"]

        failed_store, failed_state = prepared_corroborated_state(
            root=root / "failed",
            verify_id="verify-failed",
            observe_state=divergent_observe,
        )
        failed, _ = _finish(
            store=failed_store,
            state=failed_state,
            verdict="FAILED",
            criterion_satisfied=False,
            tick=40,
        )
        assert failed["route"] == "VERIFICATION_FAILED"
        assert failed["verification_debt_discharged"] is True
        assert failed["verification_required"] is False
        assert failed["corrective_action_required"] is True
        assert failed["learning_required"] is True

        indeterminate_store, indeterminate_state = prepared_corroborated_state(
            root=root / "indeterminate",
            verify_id="verify-indeterminate",
            observe_state=conflicted_observe,
            admissible=False,
        )
        indeterminate, _ = _finish(
            store=indeterminate_store,
            state=indeterminate_state,
            verdict="INDETERMINATE",
            criterion_satisfied=False,
            tick=50,
        )
        assert indeterminate["route"] == "VERIFICATION_INDETERMINATE"
        assert indeterminate["verification_debt_discharged"] is False
        assert indeterminate["verification_required"] is True
        assert indeterminate["reobservation_required"] is True
        assert indeterminate["corrective_action_required"] is False
        assert indeterminate["learning_required"] is True

        _criterion_substitution_rejected(root / "criterion-substitution", matched_observe)
        _insufficient_assessors_rejected(root / "insufficient-assessors", matched_observe)
        _triggered_falsifier_blocks_passed(root / "triggered-falsifier", matched_observe)

        return {
            "status": "VERIFY_OS_EVIDENCE_BOUND_VERIFICATION_V0_1_OK",
            "passed_route": passed["route"],
            "passed_verification_evidence_digest": passed["verification_evidence_digest"],
            "passed_verification_debt_discharged": passed[
                "verification_debt_discharged"
            ],
            "failed_route": failed["route"],
            "failed_corrective_action_required": failed[
                "corrective_action_required"
            ],
            "indeterminate_route": indeterminate["route"],
            "indeterminate_reobservation_required": indeterminate[
                "reobservation_required"
            ],
            "ledger_commits": passed_store.ledger_commit_count(),
            "recovered_verify_state_digest": recovered["verify_state_digest"],
            "verify_phase_receipt_digest": phase_receipt[
                "verify_phase_receipt_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
