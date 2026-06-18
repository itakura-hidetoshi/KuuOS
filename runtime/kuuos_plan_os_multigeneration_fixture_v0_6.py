from __future__ import annotations

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_generational_driver_kernel_v0_5 import (
    EXPECTED_REPLAN_PHASES,
)
from runtime.kuuos_plan_os_generational_driver_types_v0_5 import (
    BOUNDARY as V05_BOUNDARY,
    NON_AUTHORITY as V05_NON_AUTHORITY,
    RECEIPT_VERSION as V05_RECEIPT_VERSION,
    generational_receipt_digest,
)
from runtime.kuuos_plan_os_multigeneration_kernel_v0_6 import (
    build_generation_supervision_decision,
    build_initial_multi_generation_state,
    build_multi_generation_policy,
    build_supervised_generation_report,
)


def v05_receipt(*, lineage: str, mission: str, source_cycle: int, tag: str) -> dict:
    def d(name: str) -> str:
        return sha({"tag": tag, "field": name})

    receipt = {
        "version": V05_RECEIPT_VERSION,
        "lineage_id": lineage,
        "mission_contract_digest": mission,
        "source_bind_receipt_digest": d("bind"),
        "source_plan_id": f"plan-{tag}",
        "source_plan_state_digest": d("source-plan-state"),
        "source_plan_basis_digest": d("source-plan-basis"),
        "source_learn_state_digest": d("learn-state"),
        "source_learning_delta_digest": d("learn-delta"),
        "planos_replan_input_digest": d("replan-input"),
        "replan_id": f"replan-{tag}",
        "committed_replan_state_digest": d("replan-state"),
        "replan_phase_receipt_digest": d("replan-receipt"),
        "history_packet_digest": d("history"),
        "qi_condition_packet_digest": d("qi"),
        "candidate_field_digest": d("candidates"),
        "constraint_field_digest": d("constraints"),
        "decision_receipt_digest": d("decision"),
        "selected_candidate_id": f"candidate-{tag}",
        "selected_candidate_digest": d("candidate"),
        "synthesis_packet_digest": d("synthesis"),
        "next_plan_basis_digest": d("next-basis"),
        "replan_route": "PLAN_CANDIDATE",
        "replan_event_count": len(EXPECTED_REPLAN_PHASES),
        "replan_phase_sequence": list(EXPECTED_REPLAN_PHASES),
        "source_cycle_index": source_cycle,
        "next_cycle_index": source_cycle + 1,
        "compiled_plan_id": f"compiled-{tag}",
        "compiled_plan_state_digest": d("compiled-plan-state"),
        "compiled_plan_basis_digest": d("compiled-plan-basis"),
        "compiler_receipt_digest": d("compiler"),
        "plan_activation_receipt_digest": d("activation"),
        "act_handoff_receipt_digest": d("act-handoff"),
        "act_selected_step_id": f"step-{tag}",
        "strict_phase_order_completed": True,
        "successor_cycle_compiled": True,
        "act_handoff_ready": True,
        "execution_granted": False,
        "host_license_granted": False,
        "current_cycle_unchanged_during_replan": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "single_use": True,
        "issued_at_ms": 100_000 + source_cycle,
        "non_authority": dict(V05_NON_AUTHORITY),
        "boundary": dict(V05_BOUNDARY),
        "generational_cycle_receipt_digest": "",
    }
    receipt["generational_cycle_receipt_digest"] = generational_receipt_digest(
        receipt
    )
    return receipt


def fresh_state(*, maximum_generations: int = 5, cycle: int = 20) -> dict:
    policy = build_multi_generation_policy(
        maximum_generations=maximum_generations,
        convergence_threshold=0.05,
        stagnation_limit=2,
        oscillation_limit=2,
        observation_debt_limit=0.80,
        recovery_hold_threshold=0.80,
    )
    return build_initial_multi_generation_state(
        supervisor_id=f"supervisor-{maximum_generations}-{cycle}",
        lineage_id="v06-lineage",
        mission_contract_digest=sha("v06-mission"),
        initial_cycle_index=cycle,
        policy=policy,
        now_ms=500,
    )


def report(
    state: dict,
    *,
    tag: str,
    plan_change: float = 0.4,
    residual: float = 0.5,
    stagnation: int = 0,
    oscillation: int = 0,
    debt: float = 0.1,
    recovery: float = 0.1,
    mission_complete: bool = False,
    human_handover: bool = False,
    authority_boundary: bool = False,
    now_ms: int = 1_000,
) -> dict:
    source = v05_receipt(
        lineage=state["lineage_id"],
        mission=state["mission_contract_digest"],
        source_cycle=state["current_cycle_index"],
        tag=tag,
    )
    return build_supervised_generation_report(
        supervisor_state=state,
        generational_cycle_receipt=source,
        plan_change_score=plan_change,
        objective_residual=residual,
        stagnation_count=stagnation,
        oscillation_count=oscillation,
        observation_debt=debt,
        recovery_protection=recovery,
        mission_complete=mission_complete,
        human_handover_requested=human_handover,
        authority_boundary_hit=authority_boundary,
        now_ms=now_ms,
    )


def decision_for(state: dict, **kwargs) -> str:
    item = report(state, **kwargs)
    decision = build_generation_supervision_decision(
        state=state, report=item, now_ms=int(item["issued_at_ms"]) + 1
    )
    return decision["decision"]
