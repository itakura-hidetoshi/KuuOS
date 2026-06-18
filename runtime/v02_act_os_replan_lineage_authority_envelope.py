from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_act_os_fixture_v0_1 import apply, host_inputs
from runtime.kuuos_act_os_kernel_v0_1 import (
    build_initial_act_state,
    build_step_authorization,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_act_os_lineage_kernel_v0_2 import (
    build_act_lineage_completion_receipt,
    build_act_lineage_handoff_receipt,
    build_authorization_envelope,
)
from runtime.kuuos_act_os_lineage_store_v0_2 import (
    ActLineageStore,
    ActLineageStoreError,
    build_initial_act_lineage_store_state,
)
from runtime.kuuos_act_os_lineage_types_v0_2 import (
    STAGE_COMPLETION,
    STAGE_HANDOFF,
    handoff_receipt_digest,
)
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_plan_os_next_cycle_kernel_v0_3 import (
    build_legacy_compat_activation_receipt,
    build_materialization_packet,
    build_next_cycle_compiler_receipt,
    build_next_cycle_initial_plan_state,
)
from runtime.kuuos_plan_os_replan_fixture_v0_2 import source_learn_state
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.v01_plan_os_replan_bound_synthesis import _complete_plan
from runtime.v03_plan_os_next_cycle_basis_compiler_adapter import (
    _activation,
    _committed_replan,
    _current_plan,
    _materialized_steps,
)


def _compiled_next_plan(root: Path) -> tuple[dict, dict, dict, dict]:
    current_plan, wa_state = _current_plan(root / "source")
    learn_state = source_learn_state(root / "learn", verdict="PASSED")
    replan_state, replan_receipt = _committed_replan(
        root, current_plan, learn_state
    )
    next_activation = _activation(
        current_plan=current_plan,
        wa_state=wa_state,
        replan_state=replan_state,
        replan_receipt=replan_receipt,
        cycle=replan_state["active_from_cycle"],
    )
    materialization = build_materialization_packet(
        current_plan_state=current_plan,
        replan_state=replan_state,
        next_plan_activation_receipt=next_activation,
        steps=_materialized_steps(replan_state),
    )
    legacy = build_legacy_compat_activation_receipt(
        source_wa_state=wa_state,
        replan_phase_receipt=replan_receipt,
        next_plan_activation_receipt=next_activation,
        now_ms=440_000,
    )
    plan_store = PlanStore(root / "compiled-plan")
    compiled_plan = plan_store.initialize(
        build_next_cycle_initial_plan_state(
            plan_id="act-v02-compiled-plan",
            source_wa_state=wa_state,
            legacy_compat_activation_receipt=legacy,
            replan_state=replan_state,
            next_plan_activation_receipt=next_activation,
            plan_budget=2.0,
            maximum_step_risk=0.40,
            now_ms=450_000,
        )
    )
    compiled_plan, _ = _complete_plan(
        plan_store,
        compiled_plan,
        materialization["v01_steps"],
        400_000,
    )
    compiler_receipt = build_next_cycle_compiler_receipt(
        previous_plan_state=current_plan,
        replan_state=replan_state,
        next_plan_activation_receipt=next_activation,
        materialization_packet=materialization,
        compiled_plan_state=compiled_plan,
        now_ms=470_000,
    )
    plan_activation = build_plan_phase_activation_receipt(
        state=compiled_plan,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("act-v02-plan-mission-state"),
        plan_phase_receipt_digest=sha("act-v02-plan-phase-receipt"),
        now_ms=480_000,
    )
    return compiled_plan, plan_activation, compiler_receipt, replan_state


def _handoff(
    *,
    plan: dict,
    plan_activation: dict,
    compiler_receipt: dict,
    cycle: int,
    selected_step_id: str = "act-candidate",
    operation_id: str = "fixture.success",
) -> dict:
    return build_act_lineage_handoff_receipt(
        compiled_plan_state=plan,
        plan_activation_receipt=plan_activation,
        next_cycle_compiler_receipt=compiler_receipt,
        selected_step_id=selected_step_id,
        operation_id=operation_id,
        operation_input_digest=sha({"value": 1}),
        mission_cycle_phase="act",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("act-v02-act-mission-state"),
        act_phase_event_digest=sha("act-v02-act-phase-event"),
        act_phase_receipt_digest=sha("act-v02-act-phase-receipt"),
        now_ms=490_000,
    )


def _negative_handoff_cases(
    plan: dict, plan_activation: dict, compiler_receipt: dict
) -> None:
    cycle = compiler_receipt["mission_cycle_cycle_index"]
    try:
        _handoff(
            plan=plan,
            plan_activation=plan_activation,
            compiler_receipt=compiler_receipt,
            cycle=cycle + 1,
        )
    except ValueError as exc:
        assert str(exc) == "lineage_act_cycle_mismatch"
    else:
        raise AssertionError("wrong Act cycle accepted")
    try:
        _handoff(
            plan=plan,
            plan_activation=plan_activation,
            compiler_receipt=compiler_receipt,
            cycle=cycle,
            selected_step_id="prepare",
        )
    except ValueError as exc:
        assert str(exc) == "lineage_selected_step_not_effectful_act_candidate"
    else:
        raise AssertionError("non-effectful step accepted")
    substituted = deepcopy(compiler_receipt)
    substituted["qi_condition_packet_digest"] = sha("substituted-qi")
    try:
        _handoff(
            plan=plan,
            plan_activation=plan_activation,
            compiler_receipt=substituted,
            cycle=cycle,
        )
    except ValueError as exc:
        assert str(exc) == "lineage_compiler_receipt_digest_invalid"
    else:
        raise AssertionError("substituted compiler receipt accepted")


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-act-os-v02-") as temporary:
        root = Path(temporary)
        plan, plan_activation, compiler_receipt, replan_state = _compiled_next_plan(
            root
        )
        _negative_handoff_cases(plan, plan_activation, compiler_receipt)
        handoff = _handoff(
            plan=plan,
            plan_activation=plan_activation,
            compiler_receipt=compiler_receipt,
            cycle=compiler_receipt["mission_cycle_cycle_index"],
        )
        assert handoff["qi_condition_packet_digest"] == replan_state[
            "qi_condition_packet_digest"
        ]
        assert handoff["selected_candidate_digest"] == replan_state[
            "selected_candidate_digest"
        ]
        assert handoff["execution_granted"] is False

        lineage_store = ActLineageStore(root / "lineage-store")
        lineage_store.initialize(
            build_initial_act_lineage_store_state(
                store_id="act-v02-lineage-store", now_ms=480_000
            )
        )
        issued = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=490_001
        )
        assert issued["status"] == "COMMITTED"
        before_handoff_replay = lineage_store.ledger_commit_count()
        replay = lineage_store.commit(
            stage=STAGE_HANDOFF, receipt=handoff, now_ms=490_002
        )
        assert replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_handoff_replay

        conflict = deepcopy(handoff)
        conflict["operation_id"] = "fixture.other"
        conflict["act_lineage_handoff_receipt_digest"] = ""
        conflict["act_lineage_handoff_receipt_digest"] = handoff_receipt_digest(
            conflict
        )
        try:
            lineage_store.commit(
                stage=STAGE_HANDOFF, receipt=conflict, now_ms=490_003
            )
        except ActLineageStoreError as exc:
            assert str(exc) == "act_lineage_handoff_already_issued"
        else:
            raise AssertionError("conflicting handoff accepted")

        policy, bundle, host_license, projection = host_inputs(
            job_id="act-v02-lineage-job"
        )
        act_store = ActStore(root / "act-store")
        act_state = act_store.initialize(
            build_initial_act_state(
                act_id="act-v02-lineage",
                plan_state=plan,
                plan_activation_receipt=plan_activation,
                now_ms=500_000,
            )
        )
        operation_input_digest = handoff["operation_input_digest"]
        act_state = apply(
            act_store,
            act_state,
            "select",
            {
                "plan_state": plan,
                "selected_step_id": handoff["selected_step_id"],
                "operation_id": handoff["operation_id"],
                "operation_input_digest": operation_input_digest,
            },
            410_001,
        )
        inner_authorization = build_step_authorization(
            state=act_state,
            authorization_id="act-v02-inner-authorization",
            operation_id=handoff["operation_id"],
            operation_input_digest=operation_input_digest,
            act_phase_receipt_digest=handoff["act_phase_receipt_digest"],
            invocation_id="act-v02-invocation",
            source_supervisor_bundle_digest=projection[
                "source_supervisor_bundle_digest"
            ],
            host_job_id="act-v02-lineage-job",
            host_step_id="step-1",
            host_license=host_license,
            human_approval_receipt_digest=sha("act-v02-human-approval"),
            human_approver_id="human-operator",
            issued_at_ms=500_000,
            expires_at_ms=580_000,
        )
        envelope = build_authorization_envelope(
            handoff_receipt=handoff,
            act_state=act_state,
            step_authorization=inner_authorization,
            host_license=host_license,
            now_ms=500_001,
        )
        assert envelope["inner_authorization_unchanged"] is True
        assert envelope["execution_granted_by_envelope"] is False

        wrong_authorization = deepcopy(inner_authorization)
        wrong_authorization["operation_input_digest"] = sha("wrong-input")
        from runtime.kuuos_act_os_types_v0_1 import authorization_digest

        wrong_authorization["step_authorization_digest"] = ""
        wrong_authorization["step_authorization_digest"] = authorization_digest(
            wrong_authorization
        )
        try:
            build_authorization_envelope(
                handoff_receipt=handoff,
                act_state=act_state,
                step_authorization=wrong_authorization,
                host_license=host_license,
                now_ms=500_002,
            )
        except ValueError as exc:
            assert str(exc) == (
                "lineage_inner_authorization_operation_input_digest_mismatch"
            )
        else:
            raise AssertionError("substituted operation input accepted")

        act_state = apply(
            act_store,
            act_state,
            "authorize",
            {
                "step_authorization": inner_authorization,
                "host_license": host_license,
            },
            410_002,
        )
        act_state = apply(
            act_store,
            act_state,
            "project",
            {"host_projection": projection},
            410_003,
        )
        committed_act, _ = finish_act(
            store=act_store,
            state=act_state,
            bundle=bundle,
            policy=policy,
            invoke_ms=500_004,
        )
        completion = build_act_lineage_completion_receipt(
            handoff_receipt=handoff,
            authorization_envelope=envelope,
            committed_act_state=committed_act,
            now_ms=500_010,
        )
        assert completion["effect_recorded"] is True
        assert completion["observation_required"] is True
        assert completion["verification_required"] is True
        completed = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=500_011
        )
        assert completed["status"] == "COMMITTED"
        before_completion_replay = lineage_store.ledger_commit_count()
        completion_replay = lineage_store.commit(
            stage=STAGE_COMPLETION, receipt=completion, now_ms=500_012
        )
        assert completion_replay["status"] == "REPLAYED"
        assert lineage_store.ledger_commit_count() == before_completion_replay

        snapshot_path = root / "lineage-store" / "act-lineage-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            lineage_store.recover(require_snapshot_match=True)
        except ActLineageStoreError as exc:
            assert str(exc) == "act_lineage_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt lineage snapshot accepted")
        repaired = lineage_store.repair_snapshot()
        recovered = lineage_store.recover(require_snapshot_match=True)
        assert repaired["act_lineage_store_state_digest"] == recovered[
            "act_lineage_store_state_digest"
        ]

        return {
            "status": "ACT_OS_REPLAN_LINEAGE_AUTHORITY_ENVELOPE_V0_2_OK",
            "handoff_receipt_digest": handoff[
                "act_lineage_handoff_receipt_digest"
            ],
            "authorization_envelope_digest": envelope[
                "authorization_envelope_digest"
            ],
            "completion_receipt_digest": completion[
                "act_lineage_completion_receipt_digest"
            ],
            "qi_condition_packet_digest": completion[
                "qi_condition_packet_digest"
            ],
            "route": completion["route"],
            "effect_recorded": completion["effect_recorded"],
            "observation_required": completion["observation_required"],
            "verification_required": completion["verification_required"],
            "ledger_commits": lineage_store.ledger_commit_count(),
            "recovered_state_digest": recovered[
                "act_lineage_store_state_digest"
            ],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
