from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_act_os_lineage_kernel_v0_2 import build_act_lineage_handoff_receipt
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_closed_loop_fixture_v0_4 import closed_loop_learning_source
from runtime.kuuos_plan_os_closed_loop_intake_kernel_v0_4 import (
    build_bound_replan_state,
    build_closed_loop_bind_receipt,
    build_closed_loop_intake_receipt,
)
from runtime.kuuos_plan_os_closed_loop_intake_store_v0_4 import (
    ClosedLoopIntakeStore,
    build_initial_closed_loop_intake_store_state,
)
from runtime.kuuos_plan_os_closed_loop_intake_types_v0_4 import STAGE_BIND, STAGE_INTAKE
from runtime.kuuos_plan_os_closed_loop_monotone_patch_v0_4 import install_monotone_stage_fixtures
from runtime.kuuos_plan_os_generational_driver_kernel_v0_5 import (
    build_generational_cycle_receipt,
)
from runtime.kuuos_plan_os_generational_driver_store_v0_5 import (
    GenerationalCycleStore,
    GenerationalCycleStoreError,
    build_initial_generational_store_state,
)
from runtime.kuuos_plan_os_generational_driver_types_v0_5 import generational_receipt_digest
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_plan_os_next_cycle_kernel_v0_3 import (
    build_legacy_compat_activation_receipt,
    build_materialization_packet,
    build_next_cycle_compiler_receipt,
    build_next_cycle_initial_plan_state,
)
from runtime.kuuos_plan_os_replan_fixture_v0_2 import candidate, standard_checks
from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
    build_decision_receipt,
    build_history_packet,
    build_qi_condition_packet,
    build_replan_event,
    build_replan_phase_receipt,
    build_synthesis_packet,
)
from runtime.kuuos_plan_os_replan_store_v0_2 import ReplanStore
from runtime.kuuos_plan_os_replan_types_v0_2 import copy_non_authority
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.v01_plan_os_replan_bound_synthesis import _complete_plan
from runtime.v03_plan_os_next_cycle_basis_compiler_adapter import (
    _activation,
    _current_plan,
    _materialized_steps,
)

install_monotone_stage_fixtures()


def _apply(store: ReplanStore, state: dict, phase: str, payload: dict, now_ms: int) -> dict:
    event = build_replan_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": payload, "now_ms": now_ms}),
        payload=payload,
        now_ms=now_ms,
    )
    result = store.apply(event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _drive_replan(root: Path, bound: dict, intake: dict) -> tuple[dict, dict]:
    store = ReplanStore(root)
    state = store.initialize(bound)
    history = build_history_packet(
        state=state,
        previous_plan_change_digests=[intake["source_replan_phase_receipt_digest"]],
        successful_transition_digests=[intake["act_lineage_completion_receipt_digest"]],
        failed_transition_digests=[],
        oscillation_history_digests=[],
        recovery_history_digests=[sha("v05-recovery-history")],
        stagnation_history_digests=[],
        action_history_digest=intake["committed_act_state_digest"],
        observation_history_digest=intake["committed_observe_state_digest"],
        verification_history_digest=intake["committed_verify_state_digest"],
        learning_history_digest=intake["committed_learn_state_digest"],
        history_window=16,
        path_dependence_digest=sha({
            "plan": intake["current_plan_state_digest"],
            "learn": intake["committed_learn_state_digest"],
            "cycle": intake["current_cycle_index"],
        }),
    )
    state = _apply(store, state, "history", {"history_packet": history}, 570_001)
    qi = build_qi_condition_packet(
        state=state,
        process_tensor_digest=sha("v05-qi-process-tensor"),
        process_history_digest=sha("v05-qi-process-history"),
        activation=0.62,
        stagnation=0.18,
        tension=0.24,
        recovery=0.38,
        coherence=0.78,
        coupling=0.70,
        transition_readiness=0.86,
        local_global_balance=0.74,
        observation_debt=0.12,
        hysteresis=0.05,
        memory_horizon=24,
        intervention_history_digest=sha("v05-intervention-history"),
    )
    state = _apply(store, state, "qi_condition", {"qi_condition_packet": qi}, 570_002)
    strengthen = candidate(
        "v05-strengthen-second-generation",
        "strengthen",
        target_scope="belief_candidate",
        cost=0.60,
        risk=0.24,
        transition_distance=0.28,
        switch_benefit=0.82,
    )
    strengthen["step_template_digests"] = [
        sha("v05-template-prepare"),
        sha("v05-template-act"),
        sha("v05-template-repair"),
        sha("v05-template-observe"),
        sha("v05-template-verify"),
    ]
    hold = candidate(
        "v05-hold-alternative",
        "hold",
        target_scope="no_change",
        cost=0.0,
        risk=0.0,
        transition_distance=0.0,
        switch_benefit=0.0,
    )
    candidates = [strengthen, hold]
    state = _apply(store, state, "generate", {"candidates": candidates}, 570_003)
    state = _apply(
        store,
        state,
        "constrain",
        {
            "candidate_checks": standard_checks([item["candidate_id"] for item in candidates]),
            "mission_invariant_receipt_digest": sha("v05-mission-invariants"),
            "authority_boundary_receipt_digest": sha("v05-authority-boundary"),
            "resource_envelope_digest": sha("v05-resource-envelope"),
            "scope_compatibility_digest": sha("v05-scope-compatibility"),
        },
        570_004,
    )
    selected_id = strengthen["candidate_id"]
    decision = build_decision_receipt(
        state=state,
        decision_os_state_digest=sha("v05-decision-os-state"),
        decision_basis_digest=sha("v05-decision-basis"),
        wa_relational_harmony_digest=sha("v05-wa-relational-harmony"),
        selected_candidate_id=selected_id,
        retained_candidate_ids=[hold["candidate_id"]],
        dissent_evidence_digests=[sha("v05-dissent-evidence")],
        minority_stakeholder_digests=[sha("v05-minority-stakeholder")],
        decided_at_ms=570_005,
    )
    state = _apply(store, state, "deliberate", {"decision_receipt": decision}, 570_005)
    selected = next(item for item in state["candidates"] if item["candidate_id"] == selected_id)
    synthesis = build_synthesis_packet(
        state=state,
        next_plan_goal_digest=selected["goal_digest"],
        next_plan_step_template_digests=selected["step_template_digests"],
        next_observation_point_digests=[selected["expected_observation_digest"]],
        next_verification_criterion_digests=[selected["verification_criterion_digest"]],
        next_stop_condition_digests=selected["stop_condition_digests"],
        next_rollback_point_digests=[selected["rollback_point_digest"]],
        resource_envelope_digest=sha("v05-next-resource-envelope"),
        authority_boundary_digest=sha("v05-next-authority-boundary"),
    )
    state = _apply(store, state, "synthesize", {"synthesis_packet": synthesis}, 570_006)
    commit_payload = {
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
    }
    state = _apply(store, state, "commit_next", commit_payload, 570_007)
    receipt = build_replan_phase_receipt(
        state=state,
        mission_cycle_state_digest=sha("v05-replan-mission-state"),
        replan_phase_event_digest=sha("v05-replan-phase-event"),
        now_ms=570_010,
    )
    assert store.ledger_commit_count() == 7
    return state, receipt


def _compile_successor(
    root: Path,
    *,
    source_plan: dict,
    wa_state: dict,
    replan_state: dict,
    replan_receipt: dict,
) -> tuple[dict, dict, dict, dict]:
    cycle = replan_state["active_from_cycle"]
    activation = _activation(
        current_plan=source_plan,
        wa_state=wa_state,
        replan_state=replan_state,
        replan_receipt=replan_receipt,
        cycle=cycle,
    )
    materialization = build_materialization_packet(
        current_plan_state=source_plan,
        replan_state=replan_state,
        next_plan_activation_receipt=activation,
        steps=_materialized_steps(replan_state),
    )
    legacy = build_legacy_compat_activation_receipt(
        source_wa_state=wa_state,
        replan_phase_receipt=replan_receipt,
        next_plan_activation_receipt=activation,
        now_ms=580_000,
    )
    plan_store = PlanStore(root / "compiled-second-generation")
    plan = plan_store.initialize(
        build_next_cycle_initial_plan_state(
            plan_id="v05-second-generation-plan",
            source_wa_state=wa_state,
            legacy_compat_activation_receipt=legacy,
            replan_state=replan_state,
            next_plan_activation_receipt=activation,
            plan_budget=2.0,
            maximum_step_risk=0.40,
            now_ms=590_000,
        )
    )
    plan, _ = _complete_plan(plan_store, plan, materialization["v01_steps"], 500_000)
    compiler = build_next_cycle_compiler_receipt(
        previous_plan_state=source_plan,
        replan_state=replan_state,
        next_plan_activation_receipt=activation,
        materialization_packet=materialization,
        compiled_plan_state=plan,
        now_ms=610_000,
    )
    plan_activation = build_plan_phase_activation_receipt(
        state=plan,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("v05-plan-mission-state"),
        plan_phase_receipt_digest=sha("v05-plan-phase-receipt"),
        now_ms=620_000,
    )
    handoff = build_act_lineage_handoff_receipt(
        compiled_plan_state=plan,
        plan_activation_receipt=plan_activation,
        next_cycle_compiler_receipt=compiler,
        selected_step_id="act-candidate",
        operation_id="fixture.success",
        operation_input_digest=sha({"v05": "second-generation"}),
        mission_cycle_phase="act",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("v05-act-mission-state"),
        act_phase_event_digest=sha("v05-act-phase-event"),
        act_phase_receipt_digest=sha("v05-act-phase-receipt"),
        now_ms=630_000,
    )
    return plan, compiler, plan_activation, handoff


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v05-") as temporary:
        root = Path(temporary)
        source_plan, source_compiler, learn_state, learn_handoff, learn_completion = (
            closed_loop_learning_source(root / "cycle-one")
        )
        _, wa_state = _current_plan(root / "deterministic-wa-source")
        assert source_plan["source_wa_state_digest"] == wa_state["wa_state_digest"]
        assert source_plan["source_committed_wa_digest"] == wa_state["latest_committed_wa_digest"]
        assert source_plan["source_wa_basis_digest"] == wa_state["wa_basis_digest"]
        cycle = source_compiler["mission_cycle_cycle_index"]
        intake = build_closed_loop_intake_receipt(
            current_plan_state=source_plan,
            next_cycle_compiler_receipt=source_compiler,
            committed_learn_state=learn_state,
            learn_lineage_handoff_receipt=learn_handoff,
            learn_lineage_completion_receipt=learn_completion,
            current_cycle_index=cycle,
            plan_budget=2.0,
            maximum_candidate_risk=0.50,
            base_switch_threshold=0.10,
            mission_cycle_state_digest=sha("v05-intake-mission-state"),
            replan_phase_event_digest=sha("v05-intake-phase-event"),
            now_ms=550_000,
        )
        bound = build_bound_replan_state(
            intake_receipt=intake,
            replan_id="v05-second-generation-replan",
            current_plan_state=source_plan,
            committed_learn_state=learn_state,
            now_ms=560_000,
        )
        bind = build_closed_loop_bind_receipt(
            intake_receipt=intake,
            bound_replan_state=bound,
            now_ms=560_010,
        )
        intake_store = ClosedLoopIntakeStore(root / "intake-store")
        intake_store.initialize(build_initial_closed_loop_intake_store_state(store_id="v05-intake-store", now_ms=549_000))
        assert intake_store.commit(stage=STAGE_INTAKE, receipt=intake, now_ms=550_001)["status"] == "COMMITTED"
        assert intake_store.commit(stage=STAGE_BIND, receipt=bind, now_ms=560_011)["status"] == "COMMITTED"

        committed_replan, replan_receipt = _drive_replan(root / "replan-store", bound, intake)
        second_plan, second_compiler, plan_activation, act_handoff = _compile_successor(
            root,
            source_plan=source_plan,
            wa_state=wa_state,
            replan_state=committed_replan,
            replan_receipt=replan_receipt,
        )
        assert second_compiler["mission_cycle_cycle_index"] == cycle + 1
        assert act_handoff["mission_cycle_cycle_index"] == cycle + 1
        assert act_handoff["execution_granted"] is False
        receipt = build_generational_cycle_receipt(
            bind_receipt=bind,
            source_plan_state=source_plan,
            committed_replan_state=committed_replan,
            replan_phase_receipt=replan_receipt,
            compiled_plan_state=second_plan,
            compiler_receipt=second_compiler,
            plan_activation_receipt=plan_activation,
            act_handoff_receipt=act_handoff,
            now_ms=640_000,
        )
        store = GenerationalCycleStore(root / "generation-store")
        store.initialize(build_initial_generational_store_state(store_id="v05-generation-store", now_ms=639_000))
        assert store.commit(receipt, now_ms=640_001)["status"] == "COMMITTED"
        before_replay = store.ledger_commit_count()
        assert store.commit(receipt, now_ms=640_002)["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        conflict = deepcopy(receipt)
        conflict["act_selected_step_id"] = "substituted-step"
        conflict["generational_cycle_receipt_digest"] = ""
        conflict["generational_cycle_receipt_digest"] = generational_receipt_digest(conflict)
        try:
            store.commit(conflict, now_ms=640_003)
        except GenerationalCycleStoreError as exc:
            assert str(exc) == "generational_source_already_consumed"
        else:
            raise AssertionError("conflicting generation accepted")

        snapshot = root / "generation-store" / "generational-cycle-snapshot.json"
        snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except GenerationalCycleStoreError as exc:
            assert str(exc) == "generational_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt generation snapshot accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["generational_cycle_store_state_digest"] == recovered["generational_cycle_store_state_digest"]

        return {
            "status": "PLAN_OS_GENERATIONAL_REPLAN_CYCLE_DRIVER_V0_5_OK",
            "source_cycle_index": cycle,
            "next_cycle_index": cycle + 1,
            "replan_phase_sequence": [item["target_phase"] for item in committed_replan["event_history"]],
            "selected_candidate_id": committed_replan["selected_candidate_id"],
            "second_generation_plan_id": second_plan["plan_id"],
            "second_generation_plan_digest": second_plan["plan_state_digest"],
            "compiler_receipt_digest": second_compiler["next_cycle_compiler_receipt_digest"],
            "act_handoff_receipt_digest": act_handoff["act_lineage_handoff_receipt_digest"],
            "execution_granted": act_handoff["execution_granted"],
            "ledger_commits": store.ledger_commit_count(),
            "recovered_state_digest": recovered["generational_cycle_store_state_digest"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
