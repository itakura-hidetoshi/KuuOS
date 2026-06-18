from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_fixture_v0_1 import (
    prepared_assessed_state,
    source_act_state,
)
from runtime.kuuos_observe_os_kernel_v0_1 import build_observe_phase_receipt
from runtime.kuuos_observe_os_lineage_kernel_v0_2 import (
    build_observe_lineage_completion_receipt,
    build_observe_lineage_handoff_receipt,
)
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_verify_os_kernel_v0_1 import build_verify_phase_receipt
from runtime.kuuos_verify_os_lineage_kernel_v0_2 import (
    build_verify_lineage_completion_receipt,
    build_verify_lineage_handoff_receipt,
)
from runtime.kuuos_verify_os_lineage_store_v0_2 import (
    VerifyLineageStore,
    VerifyLineageStoreError,
    build_initial_verify_lineage_store_state,
)
from runtime.kuuos_verify_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    handoff_receipt_digest,
)
from runtime.v01_observe_os_effect_grounded_observation import (
    _finish as finish_observe,
)
from runtime.v01_verify_os_evidence_bound_verification import (
    _finish as finish_verify,
)
from runtime.v02_observe_os_replan_lineage_observation_envelope import (
    _act_lineage_packets,
)


def _observe_lineage_source(root: Path) -> tuple[dict, dict, dict]:
    act_state = source_act_state(root / "act-source")
    act_handoff, act_completion = _act_lineage_packets(act_state)
    observe_handoff = build_observe_lineage_handoff_receipt(
        committed_act_state=act_state,
        act_lineage_handoff_receipt=act_handoff,
        act_lineage_completion_receipt=act_completion,
        mission_cycle_phase="observe",
        mission_cycle_cycle_index=1,
        mission_cycle_state_digest=sha("verify-v02-observe-cycle-state"),
        observe_phase_event_digest=sha("verify-v02-observe-cycle-event"),
        now_ms=98_000,
    )
    observe_store, assessed = prepared_assessed_state(
        root=root / "observe-source",
        observe_id="verify-v02-observe-source",
        act_state=act_state,
    )
    observed, _ = finish_observe(
        store=observe_store,
        state=assessed,
        verdict="MATCHED",
        tick=5,
    )
    observe_phase_receipt = build_observe_phase_receipt(
        state=observed,
        mission_cycle_state_digest=sha("verify-v02-observe-phase-state"),
        observe_phase_event_digest=sha("verify-v02-observe-phase-event"),
        now_ms=100_100,
    )
    observe_completion = build_observe_lineage_completion_receipt(
        handoff_receipt=observe_handoff,
        committed_observe_state=observed,
        observe_phase_receipt=observe_phase_receipt,
        now_ms=100_200,
    )
    return observed, observe_handoff, observe_completion


def _negative_handoff_cases(
    observed: dict, observe_handoff: dict, observe_completion: dict
) -> None:
    try:
        build_verify_lineage_handoff_receipt(
            committed_observe_state=observed,
            observe_lineage_handoff_receipt=observe_handoff,
            observe_lineage_completion_receipt=observe_completion,
            mission_cycle_phase="learn",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("wrong-phase-state"),
            verify_phase_event_digest=sha("wrong-phase-event"),
            now_ms=101_000,
        )
    except ValueError as exc:
        assert str(exc) == "verify_lineage_verify_phase_required"
    else:
        raise AssertionError("non-verify phase accepted")

    try:
        build_verify_lineage_handoff_receipt(
            committed_observe_state=observed,
            observe_lineage_handoff_receipt=observe_handoff,
            observe_lineage_completion_receipt=observe_completion,
            mission_cycle_phase="verify",
            mission_cycle_cycle_index=2,
            mission_cycle_state_digest=sha("wrong-cycle-state"),
            verify_phase_event_digest=sha("wrong-cycle-event"),
            now_ms=101_001,
        )
    except ValueError as exc:
        assert str(exc) == "verify_lineage_cycle_mismatch"
    else:
        raise AssertionError("wrong Verify cycle accepted")

    substituted = deepcopy(observe_completion)
    substituted["qi_condition_packet_digest"] = sha("substituted-qi")
    try:
        build_verify_lineage_handoff_receipt(
            committed_observe_state=observed,
            observe_lineage_handoff_receipt=observe_handoff,
            observe_lineage_completion_receipt=substituted,
            mission_cycle_phase="verify",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("substituted-state"),
            verify_phase_event_digest=sha("substituted-event"),
            now_ms=101_002,
        )
    except ValueError as exc:
        assert str(exc).startswith(
            "verify_lineage_observe_completion_invalid:"
        )
    else:
        raise AssertionError("substituted Observe lineage accepted")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-verify-os-v02-") as temporary:
        root = Path(temporary)
        observed, observe_handoff, observe_completion = _observe_lineage_source(
            root / "source"
        )
        _negative_handoff_cases(
            observed, observe_handoff, observe_completion
        )

        handoff = build_verify_lineage_handoff_receipt(
            committed_observe_state=observed,
            observe_lineage_handoff_receipt=observe_handoff,
            observe_lineage_completion_receipt=observe_completion,
            mission_cycle_phase="verify",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("verify-v02-cycle-state"),
            verify_phase_event_digest=sha("verify-v02-cycle-event"),
            now_ms=101_000,
        )
        assert handoff["qi_condition_packet_digest"] == observe_completion[
            "qi_condition_packet_digest"
        ]
        assert handoff["verification_criterion_digest"] == observed[
            "verification_criterion_digest"
        ]
        assert handoff["evidence_packet_digest"] == observed[
            "evidence_packet_digest"
        ]
        assert handoff["verification_not_truth"] is True
        assert handoff["learning_future_only"] is True

        lineage_store = VerifyLineageStore(root / "lineage-store")
        lineage_store.initialize(
            build_initial_verify_lineage_store_state(
                store_id="verify-v02-lineage-store", now_ms=100_900
            )
        )
        issued = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=101_010
        )
        assert issued["status"] == "COMMITTED"
        before_handoff_replay = lineage_store.ledger_commit_count()
        replay = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=101_011
        )
        assert replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_handoff_replay

        conflict = deepcopy(handoff)
        conflict["mission_cycle_state_digest"] = sha(
            "verify-v02-conflicting-cycle-state"
        )
        conflict["verify_lineage_handoff_receipt_digest"] = ""
        conflict["verify_lineage_handoff_receipt_digest"] = handoff_receipt_digest(
            conflict
        )
        try:
            lineage_store.commit(
                stage=STAGE_HANDOFF, receipt=conflict, now_ms=101_012
            )
        except VerifyLineageStoreError as exc:
            assert str(exc) == "verify_lineage_handoff_already_issued"
        else:
            raise AssertionError("conflicting Verify handoff accepted")

        verify_store, corroborated = prepared_corroborated_state(
            root=root / "verify-store",
            verify_id="verify-v02-passed",
            observe_state=observed,
        )
        verified, _ = finish_verify(
            store=verify_store,
            state=corroborated,
            verdict="PASSED",
            criterion_satisfied=True,
            tick=4,
        )
        phase_receipt = build_verify_phase_receipt(
            state=verified,
            mission_cycle_state_digest=sha("verify-v02-phase-state"),
            verify_phase_event_digest=sha("verify-v02-phase-event"),
            now_ms=120_100,
        )
        completion = build_verify_lineage_completion_receipt(
            handoff_receipt=handoff,
            committed_verify_state=verified,
            verify_phase_receipt=phase_receipt,
            now_ms=120_200,
        )
        assert completion["route"] == "VERIFICATION_PASSED"
        assert completion["verdict"] == "passed"
        assert completion["verification_debt_discharged"] is True
        assert completion["verification_required"] is False
        assert completion["learning_required"] is True
        assert completion["learning_must_be_future_only"] is True
        assert completion["counterevidence_preserved"] is True
        assert completion["falsification_attempted"] is True
        assert completion["automatic_learning"] is False
        assert completion["qi_condition_packet_digest"] == handoff[
            "qi_condition_packet_digest"
        ]

        committed = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=120_201
        )
        assert committed["status"] == "COMMITTED"
        before_completion_replay = lineage_store.ledger_commit_count()
        completion_replay = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=120_202
        )
        assert completion_replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_completion_replay

        snapshot_path = root / "lineage-store" / "verify-lineage-snapshot.json"
        snapshot_path.write_text(
            json.dumps({"corrupt": True}), encoding="utf-8"
        )
        try:
            lineage_store.recover(require_snapshot_match=True)
        except VerifyLineageStoreError as exc:
            assert str(exc) == "verify_lineage_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt Verify lineage snapshot accepted")
        repaired = lineage_store.repair_snapshot()
        recovered = lineage_store.recover(require_snapshot_match=True)
        assert repaired["verify_lineage_store_state_digest"] == recovered[
            "verify_lineage_store_state_digest"
        ]

        return {
            "status": "VERIFY_OS_REPLAN_LINEAGE_VERIFICATION_ENVELOPE_V0_2_OK",
            "handoff_receipt_digest": handoff[
                "verify_lineage_handoff_receipt_digest"
            ],
            "completion_receipt_digest": completion[
                "verify_lineage_completion_receipt_digest"
            ],
            "observe_completion_receipt_digest": completion[
                "observe_lineage_completion_receipt_digest"
            ],
            "qi_condition_packet_digest": completion[
                "qi_condition_packet_digest"
            ],
            "route": completion["route"],
            "verdict": completion["verdict"],
            "verification_debt_discharged": completion[
                "verification_debt_discharged"
            ],
            "learning_required": completion["learning_required"],
            "learning_must_be_future_only": completion[
                "learning_must_be_future_only"
            ],
            "ledger_commits": lineage_store.ledger_commit_count(),
            "recovered_state_digest": recovered[
                "verify_lineage_store_state_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
