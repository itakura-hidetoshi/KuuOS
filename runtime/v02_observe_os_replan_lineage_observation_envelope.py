from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_act_os_lineage_types_v0_2 import (
    COMPLETION_RECEIPT_VERSION as ACT_COMPLETION_VERSION,
    HANDOFF_RECEIPT_VERSION as ACT_HANDOFF_VERSION,
    completion_receipt_digest as act_completion_digest,
    copy_non_authority as copy_act_non_authority,
    handoff_receipt_digest as act_handoff_digest,
)
from runtime.kuuos_observe_os_fixture_v0_1 import (
    prepared_assessed_state,
    source_act_state,
)
from runtime.kuuos_observe_os_kernel_v0_1 import build_observe_phase_receipt
from runtime.kuuos_observe_os_lineage_kernel_v0_2 import (
    build_observe_lineage_completion_receipt,
    build_observe_lineage_handoff_receipt,
)
from runtime.kuuos_observe_os_lineage_store_v0_2 import (
    ObserveLineageStore,
    ObserveLineageStoreError,
)
from runtime.kuuos_observe_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    handoff_receipt_digest,
)
from runtime.v01_observe_os_effect_grounded_observation import _finish


def _act_lineage_packets(act_state: dict) -> tuple[dict, dict]:
    handoff = {
        "version": ACT_HANDOFF_VERSION,
        "lineage_id": act_state["lineage_id"],
        "mission_contract_digest": act_state["mission_contract_digest"],
        "next_cycle_compiler_receipt_digest": sha("observe-v02-compiler"),
        "compiled_plan_id": "observe-v02-plan",
        "compiled_plan_state_digest": act_state["source_plan_state_digest"],
        "compiled_plan_basis_digest": act_state["source_plan_basis_digest"],
        "committed_plan_digest": sha("observe-v02-committed-plan"),
        "plan_activation_receipt_digest": act_state[
            "plan_activation_receipt_digest"
        ],
        "replan_phase_receipt_digest": sha("observe-v02-replan-receipt"),
        "next_plan_activation_receipt_digest": sha("observe-v02-next-activation"),
        "materialization_packet_digest": sha("observe-v02-materialization"),
        "next_plan_basis_digest": sha("observe-v02-next-basis"),
        "selected_candidate_id": "observe-v02-candidate",
        "selected_candidate_digest": sha("observe-v02-candidate"),
        "qi_condition_packet_digest": sha("observe-v02-qi-condition"),
        "decision_receipt_digest": sha("observe-v02-decision"),
        "synthesis_packet_digest": sha("observe-v02-synthesis"),
        "selected_step_id": act_state["selected_step_id"],
        "selected_step_digest": act_state["selected_step_digest"],
        "expected_observation_digest": act_state[
            "expected_observation_digest"
        ],
        "verification_criterion_digest": act_state[
            "verification_criterion_digest"
        ],
        "stop_condition_digests": [sha("observe-v02-stop")],
        "requires_human_review": False,
        "requires_external_license": True,
        "operation_id": act_state["operation_id"],
        "operation_input_digest": act_state["operation_input_digest"],
        "mission_cycle_phase": "act",
        "mission_cycle_cycle_index": 1,
        "mission_cycle_state_digest": sha("observe-v02-act-cycle-state"),
        "act_phase_event_digest": sha("observe-v02-act-cycle-event"),
        "act_phase_receipt_digest": sha("observe-v02-act-cycle-receipt"),
        "plan_activation_is_not_execution": True,
        "step_authorization_still_required": True,
        "host_license_still_required": True,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "issued_at_ms": 97_000,
        "non_authority": copy_act_non_authority(),
        "act_lineage_handoff_receipt_digest": "",
    }
    handoff["act_lineage_handoff_receipt_digest"] = act_handoff_digest(handoff)
    completion = {
        "version": ACT_COMPLETION_VERSION,
        "act_lineage_handoff_receipt_digest": handoff[
            "act_lineage_handoff_receipt_digest"
        ],
        "authorization_envelope_digest": sha("observe-v02-authorization-envelope"),
        "next_cycle_compiler_receipt_digest": handoff[
            "next_cycle_compiler_receipt_digest"
        ],
        "replan_phase_receipt_digest": handoff["replan_phase_receipt_digest"],
        "qi_condition_packet_digest": handoff["qi_condition_packet_digest"],
        "decision_receipt_digest": handoff["decision_receipt_digest"],
        "selected_candidate_digest": handoff["selected_candidate_digest"],
        "selected_step_digest": act_state["selected_step_digest"],
        "committed_act_state_digest": act_state["act_state_digest"],
        "step_authorization_digest": act_state["step_authorization_digest"],
        "host_license_digest": act_state["host_license_digest"],
        "host_projection_digest": act_state["host_projection_digest"],
        "host_tick_digest": act_state["host_tick_digest"],
        "host_receipt_digest": act_state["host_receipt_digest"],
        "host_invocation_digest": act_state["host_invocation_digest"],
        "result_supervisor_bundle_digest": act_state[
            "result_supervisor_bundle_digest"
        ],
        "route": "EFFECT_RECORDED",
        "effect_recorded": True,
        "observation_required": True,
        "verification_required": True,
        "automatic_truth_promotion": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "lower_host_receipt_canonical": True,
        "completed_at_ms": 97_500,
        "non_authority": copy_act_non_authority(),
        "act_lineage_completion_receipt_digest": "",
    }
    completion["act_lineage_completion_receipt_digest"] = act_completion_digest(
        completion
    )
    return handoff, completion


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-observe-os-v02-") as temporary:
        root = Path(temporary)
        act_state = source_act_state(root / "source")
        act_handoff, act_completion = _act_lineage_packets(act_state)
        handoff = build_observe_lineage_handoff_receipt(
            committed_act_state=act_state,
            act_lineage_handoff_receipt=act_handoff,
            act_lineage_completion_receipt=act_completion,
            mission_cycle_phase="observe",
            mission_cycle_cycle_index=1,
            mission_cycle_state_digest=sha("observe-v02-cycle-state"),
            observe_phase_event_digest=sha("observe-v02-cycle-event"),
            now_ms=98_000,
        )
        assert handoff["qi_condition_packet_digest"] == act_completion[
            "qi_condition_packet_digest"
        ]
        assert handoff["observation_not_verification"] is True
        try:
            build_observe_lineage_handoff_receipt(
                committed_act_state=act_state,
                act_lineage_handoff_receipt=act_handoff,
                act_lineage_completion_receipt=act_completion,
                mission_cycle_phase="verify",
                mission_cycle_cycle_index=1,
                mission_cycle_state_digest=sha("wrong-phase"),
                observe_phase_event_digest=sha("wrong-phase-event"),
                now_ms=98_001,
            )
        except ValueError as exc:
            assert str(exc) == "observe_lineage_observe_phase_required"
        else:
            raise AssertionError("non-observe phase accepted")

        lineage_store = ObserveLineageStore(root / "lineage")
        lineage_store.initialize(store_id="observe-v02-lineage", now_ms=98_000)
        assert lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=98_010
        )["status"] == "COMMITTED"
        assert lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=98_011
        )["status"] == "REPLAYED"
        conflict = deepcopy(handoff)
        conflict["mission_cycle_state_digest"] = sha("conflicting-cycle")
        conflict["observe_lineage_handoff_receipt_digest"] = ""
        conflict["observe_lineage_handoff_receipt_digest"] = handoff_receipt_digest(
            conflict
        )
        try:
            lineage_store.commit(
                stage=STAGE_HANDOFF, receipt=conflict, now_ms=98_012
            )
        except ObserveLineageStoreError as exc:
            assert str(exc) == "observe_lineage_handoff_already_issued"
        else:
            raise AssertionError("conflicting handoff accepted")

        observe_store, assessed = prepared_assessed_state(
            root=root / "observe",
            observe_id="observe-v02-matched",
            act_state=act_state,
        )
        observed, _ = _finish(
            store=observe_store, state=assessed, verdict="MATCHED", tick=5
        )
        phase_receipt = build_observe_phase_receipt(
            state=observed,
            mission_cycle_state_digest=sha("observe-v02-phase-state"),
            observe_phase_event_digest=sha("observe-v02-phase-event"),
            now_ms=100_100,
        )
        completion = build_observe_lineage_completion_receipt(
            handoff_receipt=handoff,
            committed_observe_state=observed,
            observe_phase_receipt=phase_receipt,
            now_ms=100_200,
        )
        assert completion["route"] == "OBSERVATION_MATCHED"
        assert completion["observation_debt_discharged"] is True
        assert completion["verification_required"] is True
        assert lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=100_201
        )["status"] == "COMMITTED"
        assert lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=100_202
        )["status"] == "REPLAYED"
        return {
            "status": "OBSERVE_OS_REPLAN_LINEAGE_OBSERVATION_ENVELOPE_V0_2_OK",
            "handoff_receipt_digest": handoff[
                "observe_lineage_handoff_receipt_digest"
            ],
            "completion_receipt_digest": completion[
                "observe_lineage_completion_receipt_digest"
            ],
            "qi_condition_packet_digest": completion[
                "qi_condition_packet_digest"
            ],
            "route": completion["route"],
            "observation_debt_discharged": completion[
                "observation_debt_discharged"
            ],
            "verification_required": completion["verification_required"],
            "lineage_commits": lineage_store.ledger_commit_count(),
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
