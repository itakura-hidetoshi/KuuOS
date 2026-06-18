from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
    build_history_packet,
    build_initial_replan_state,
    build_qi_condition_packet,
    build_replan_event,
)
from runtime.kuuos_plan_os_replan_store_v0_2 import ReplanStore
from runtime.v01_plan_os_replan_bound_synthesis import _validate_candidate_plan
from runtime.kuuos_learn_os_fixture_v0_1 import (
    prepared_gated_state,
    source_verify_state,
)
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn


def source_current_plan(root: Path) -> dict[str, Any]:
    state, _, _ = _validate_candidate_plan(root / "current-plan")
    return state


def source_learn_state(root: Path, *, verdict: str) -> dict[str, Any]:
    verify = source_verify_state(root / "verify-source", verdict=verdict)
    normalized = verdict.upper()
    if normalized == "PASSED":
        kind, scope = "reinforcement", "belief_candidate"
    elif normalized == "FAILED":
        kind, scope = "repair", "plan_assumption"
    elif normalized == "INDETERMINATE":
        kind, scope = "reobservation", "observation_policy"
    else:
        raise ValueError("learn_source_verdict_invalid")
    store, state = prepared_gated_state(
        root=root / "learn-source",
        learn_id="replan-learn-" + normalized.lower(),
        verify_state=verify,
        learning_kind=kind,
        target_scope=scope,
    )
    committed, _ = finish_learn(store=store, state=state, tick=90)
    return committed


def event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], tick: int
) -> dict[str, Any]:
    return build_replan_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=310_000 + tick,
    )


def apply(
    store: ReplanStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def candidate(
    candidate_id: str,
    candidate_type: str,
    *,
    target_scope: str,
    cost: float,
    risk: float,
    transition_distance: float,
    switch_benefit: float,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "candidate_type": candidate_type,
        "target_scope": target_scope,
        "goal_digest": sha("goal-" + candidate_id),
        "step_template_digests": [sha("step-1-" + candidate_id), sha("step-2-" + candidate_id)],
        "expected_observation_digest": sha("observation-" + candidate_id),
        "verification_criterion_digest": sha("verification-" + candidate_id),
        "estimated_cost": cost,
        "estimated_risk": risk,
        "reversibility": 0.85,
        "transition_distance": transition_distance,
        "switch_benefit": switch_benefit,
        "stop_condition_digests": [sha("stop-" + candidate_id)],
        "rollback_point_digest": sha("rollback-" + candidate_id),
        "stakeholder_scope_digests": [sha("stakeholder-" + candidate_id)],
    }


def standard_checks(candidate_ids: list[str]) -> dict[str, dict[str, bool]]:
    return {
        candidate_id: {
            "mission_invariants_preserved": True,
            "authority_boundary_preserved": True,
            "applicability_condition_valid": True,
            "reversal_condition_visible": True,
            "expiration_condition_valid": True,
            "scope_compatible": True,
            "verification_debt_visible": True,
        }
        for candidate_id in candidate_ids
    }


def prepared_constrained_state(
    *,
    root: Path,
    replan_id: str,
    current_plan: Mapping[str, Any],
    learn_state: Mapping[str, Any],
    candidates: list[dict[str, Any]],
    hysteresis: float = 0.10,
    recovery: float = 0.30,
    transition_readiness: float = 0.80,
    oscillation_count: int = 1,
) -> tuple[ReplanStore, dict[str, Any]]:
    store = ReplanStore(root)
    state = store.initialize(
        build_initial_replan_state(
            replan_id=replan_id,
            current_plan_state=current_plan,
            learn_state=learn_state,
            current_cycle_index=7,
            plan_budget=2.0,
            maximum_candidate_risk=0.50,
            base_switch_threshold=0.10,
            now_ms=300_000,
        )
    )
    history = build_history_packet(
        state=state,
        previous_plan_change_digests=[sha("plan-change-1")],
        successful_transition_digests=[sha("success-1")],
        failed_transition_digests=[sha("failure-1")],
        oscillation_history_digests=[sha(f"oscillation-{i}") for i in range(oscillation_count)],
        recovery_history_digests=[sha("recovery-history")],
        stagnation_history_digests=[sha("stagnation-history")],
        action_history_digest=sha("action-history"),
        observation_history_digest=sha("observation-history"),
        verification_history_digest=sha("verification-history"),
        learning_history_digest=sha("learning-history"),
        history_window=12,
        path_dependence_digest=sha("path-dependence"),
    )
    state = apply(store, state, "history", {"history_packet": history}, 1)
    qi = build_qi_condition_packet(
        state=state,
        process_tensor_digest=sha("qi-process-tensor"),
        process_history_digest=sha("qi-process-history"),
        activation=0.55,
        stagnation=0.30,
        tension=0.35,
        recovery=recovery,
        coherence=0.70,
        coupling=0.60,
        transition_readiness=transition_readiness,
        local_global_balance=0.65,
        observation_debt=0.25,
        hysteresis=hysteresis,
        memory_horizon=16,
        intervention_history_digest=sha("intervention-history"),
    )
    state = apply(store, state, "qi_condition", {"qi_condition_packet": qi}, 2)
    state = apply(store, state, "generate", {"candidates": candidates}, 3)
    state = apply(
        store,
        state,
        "constrain",
        {
            "candidate_checks": standard_checks([item["candidate_id"] for item in candidates]),
            "mission_invariant_receipt_digest": sha("mission-invariants"),
            "authority_boundary_receipt_digest": sha("authority-boundary"),
            "resource_envelope_digest": sha("resource-envelope"),
            "scope_compatibility_digest": sha("scope-compatibility"),
        },
        4,
    )
    return store, state
