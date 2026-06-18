from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_fixture_v0_1 import prepared_gated_state
from runtime.kuuos_learn_os_kernel_v0_1 import build_learn_phase_receipt
from runtime.kuuos_learn_os_lineage_kernel_v0_2 import (
    build_learn_lineage_completion_receipt,
    build_learn_lineage_handoff_receipt,
)
from runtime.kuuos_learn_os_lineage_store_v0_2 import (
    LearnLineageStore,
    LearnLineageStoreError,
    build_initial_learn_lineage_store_state,
)
from runtime.kuuos_learn_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    handoff_receipt_digest,
)
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_verify_os_kernel_v0_1 import build_verify_phase_receipt
from runtime.kuuos_verify_os_lineage_kernel_v0_2 import (
    build_verify_lineage_completion_receipt,
    build_verify_lineage_handoff_receipt,
)
from runtime.v01_learn_os_future_only_evidence_learning import (
    _finish as finish_learn,
)
from runtime.v01_verify_os_evidence_bound_verification import (
    _finish as finish_verify,
)
from runtime.v02_verify_os_replan_lineage_verification_envelope import (
    _observe_lineage_source,
)


def _verify_lineage_source(root: Path) -> tuple[dict, dict, dict]:
    observed, observe_handoff, observe_completion = _observe_lineage_source(
        root / "observe-lineage"
    )
    verify_handoff = build_verify_lineage_handoff_receipt(
        committed_observe_state=observed,
        observe_lineage_handoff_receipt=observe_handoff,
        observe_lineage_completion_receipt=observe_completion,
        mission_cycle_phase="verify",
        mission_cycle_cycle_index=1,
        mission_cycle_state_digest=sha("learn-v02-verify-cycle-state"),
        verify_phase_event_digest=sha("learn-v02-verify-cycle-event"),
        now_ms=101_000,
    )
    verify_store, corroborated = prepared_corroborated_state(
        root=root / "verify-source",
        verify_id="learn-v02-verify-source",
        observe_state=observed,
    )
    verified, _ = finish_verify(
        store=verify_store,
        state=corroborated,
        verdict="PASSED",
        criterion_satisfied=True,
        tick=4,
    )
    verify_phase_receipt = build_verify_phase_receipt(
        state=verified,
        mission_cycle_state_digest=sha("learn-v02-verify-phase-state"),
        verify_phase_event_digest=sha("learn-v02-verify-phase-event"),
        now_ms=120_100,
    )
    verify_completion = build_verify_lineage_completion_receipt(
        handoff_receipt=verify_handoff,
        committed_verify_state=verified,
        verify_phase_receipt=verify_phase_receipt,
        now_ms=120_200,
    )
    return verified, verify_handoff, verify_completion


def _negative_handoff_cases(
    verified: dict, verify_handoff: dict, verify_completion: dict
) -> None:
    try:
        build_learn_lineage_handoff_receipt(
            committed_verify_state=verified,
            verify_lineage_handoff_receipt=verify_handoff,
            verify_lineage_completion_receipt=verify_completion,
            mission_cycle_phase="plan",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("wrong-learn-phase-state"),
            learn_phase_event_digest=sha("wrong-learn-phase-event"),
            now_ms=121_000,
        )
    except ValueError as exc:
        assert str(exc) == "learn_lineage_learn_phase_required"
    else:
        raise AssertionError("non-learn phase accepted")

    try:
        build_learn_lineage_handoff_receipt(
            committed_verify_state=verified,
            verify_lineage_handoff_receipt=verify_handoff,
            verify_lineage_completion_receipt=verify_completion,
            mission_cycle_phase="learn",
            mission_cycle_cycle_index=2,
            mission_cycle_state_digest=sha("wrong-learn-cycle-state"),
            learn_phase_event_digest=sha("wrong-learn-cycle-event"),
            now_ms=121_001,
        )
    except ValueError as exc:
        assert str(exc) == "learn_lineage_cycle_mismatch"
    else:
        raise AssertionError("wrong Learn cycle accepted")

    substituted = deepcopy(verify_completion)
    substituted["qi_condition_packet_digest"] = sha("substituted-learn-qi")
    try:
        build_learn_lineage_handoff_receipt(
            committed_verify_state=verified,
            verify_lineage_handoff_receipt=verify_handoff,
            verify_lineage_completion_receipt=substituted,
            mission_cycle_phase="learn",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("substituted-learn-state"),
            learn_phase_event_digest=sha("substituted-learn-event"),
            now_ms=121_002,
        )
    except ValueError as exc:
        assert str(exc).startswith("learn_lineage_verify_completion_invalid:")
    else:
        raise AssertionError("substituted Verify lineage accepted")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-learn-os-v02-") as temporary:
        root = Path(temporary)
        verified, verify_handoff, verify_completion = _verify_lineage_source(
            root / "source"
        )
        _negative_handoff_cases(verified, verify_handoff, verify_completion)

        handoff = build_learn_lineage_handoff_receipt(
            committed_verify_state=verified,
            verify_lineage_handoff_receipt=verify_handoff,
            verify_lineage_completion_receipt=verify_completion,
            mission_cycle_phase="learn",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("learn-v02-cycle-state"),
            learn_phase_event_digest=sha("learn-v02-cycle-event"),
            now_ms=121_000,
        )
        assert handoff["qi_condition_packet_digest"] == verify_completion[
            "qi_condition_packet_digest"
        ]
        assert handoff["source_verification_evidence_digest"] == verified[
            "verification_evidence_digest"
        ]
        assert handoff["source_counterevidence_digest"] == sha(
            verified["challenge_packet"]["counterevidence_digests"]
        )
        assert handoff["future_only"] is True
        assert handoff["active_now"] is False
        assert handoff["learn_delta_not_replan_activation"] is True

        lineage_store = LearnLineageStore(root / "lineage-store")
        lineage_store.initialize(
            build_initial_learn_lineage_store_state(
                store_id="learn-v02-lineage-store", now_ms=120_900
            )
        )
        issued = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=121_010
        )
        assert issued["status"] == "COMMITTED"
        before_handoff_replay = lineage_store.ledger_commit_count()
        replay = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=121_011
        )
        assert replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_handoff_replay

        conflict = deepcopy(handoff)
        conflict["mission_cycle_state_digest"] = sha(
            "learn-v02-conflicting-cycle-state"
        )
        conflict["learn_lineage_handoff_receipt_digest"] = ""
        conflict["learn_lineage_handoff_receipt_digest"] = handoff_receipt_digest(
            conflict
        )
        try:
            lineage_store.commit(
                stage=STAGE_HANDOFF, receipt=conflict, now_ms=121_012
            )
        except LearnLineageStoreError as exc:
            assert str(exc) == "learn_lineage_handoff_already_issued"
        else:
            raise AssertionError("conflicting Learn handoff accepted")

        learn_store, gated = prepared_gated_state(
            root=root / "learn-store",
            learn_id="learn-v02-reinforcement",
            verify_state=verified,
            learning_kind="reinforcement",
            target_scope="belief_candidate",
        )
        learned, _ = finish_learn(store=learn_store, state=gated, tick=5)
        phase_receipt = build_learn_phase_receipt(
            state=learned,
            mission_cycle_state_digest=sha("learn-v02-phase-state"),
            learn_phase_event_digest=sha("learn-v02-phase-event"),
            now_ms=210_100,
        )
        completion = build_learn_lineage_completion_receipt(
            handoff_receipt=handoff,
            committed_learn_state=learned,
            learn_phase_receipt=phase_receipt,
            now_ms=210_200,
        )
        assert completion["learning_route"] == "LEARNING_REINFORCEMENT_CANDIDATE"
        assert completion["learning_kind"] == "reinforcement"
        assert completion["planos_candidate_type_allowlist"] == [
            "continue",
            "strengthen",
            "slow_down",
            "hold",
        ]
        assert completion["learning_recorded"] is True
        assert completion["learning_debt_discharged"] is True
        assert completion["replan_required"] is True
        assert completion["replan_handoff_ready"] is True
        assert completion["future_only"] is True
        assert completion["active_now"] is False
        assert completion["replan_activation"] is False
        assert completion["plan_activation"] is False
        assert completion["execution_permission"] is False
        assert completion["host_license_granted"] is False
        assert completion["qi_condition_packet_digest"] == handoff[
            "qi_condition_packet_digest"
        ]

        committed = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=210_201
        )
        assert committed["status"] == "COMMITTED"
        before_completion_replay = lineage_store.ledger_commit_count()
        completion_replay = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=210_202
        )
        assert completion_replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_completion_replay

        snapshot_path = root / "lineage-store" / "learn-lineage-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            lineage_store.recover(require_snapshot_match=True)
        except LearnLineageStoreError as exc:
            assert str(exc) == "learn_lineage_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt Learn lineage snapshot accepted")
        repaired = lineage_store.repair_snapshot()
        recovered = lineage_store.recover(require_snapshot_match=True)
        assert repaired["learn_lineage_store_state_digest"] == recovered[
            "learn_lineage_store_state_digest"
        ]

        return {
            "status": "LEARN_OS_REPLAN_LINEAGE_FUTURE_ONLY_LEARNING_ENVELOPE_V0_2_OK",
            "handoff_receipt_digest": handoff[
                "learn_lineage_handoff_receipt_digest"
            ],
            "completion_receipt_digest": completion[
                "learn_lineage_completion_receipt_digest"
            ],
            "verify_completion_receipt_digest": completion[
                "verify_lineage_completion_receipt_digest"
            ],
            "qi_condition_packet_digest": completion[
                "qi_condition_packet_digest"
            ],
            "learning_route": completion["learning_route"],
            "learning_kind": completion["learning_kind"],
            "planos_replan_input_digest": completion[
                "planos_replan_input_digest"
            ],
            "replan_handoff_ready": completion["replan_handoff_ready"],
            "future_only": completion["future_only"],
            "ledger_commits": lineage_store.ledger_commit_count(),
            "recovered_state_digest": recovered[
                "learn_lineage_store_state_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
