from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_goal_portfolio_v0_20 import (
    validate_goal_portfolio,
    validate_goal_proposal,
)
from runtime.kuuos_mission_contract_types_v0_20 import (
    sha,
    validate_mission_contract,
)
from runtime.kuuos_mission_state_v0_20 import validate_mission_state
from runtime.kuuos_observation_belief_state_kernel_v0_21 import validate_belief_state
from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_append_writeback_v0_1 import (
    run_qi_memoryos_process_tensor_append_writeback,
)
from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import (
    build_qi_memoryos_process_tensor_retrieval_replay,
)
from runtime.kuuos_runtime_daemon_qi_process_tensor_observation_debt_scheduler_v0_1 import (
    compile_qi_process_tensor_observation_debt_schedule,
)
from runtime.kuuos_runtime_daemon_qi_process_tensor_recoverability_projection_v0_1 import (
    compile_qi_process_tensor_recoverability_projection,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    validate_semantic_plan,
    validate_verification_receipt_static,
)
from src.physical_quantum_qi_process_tensor_runtime_v0_2F import (
    build_qi_process_tensor_result,
)

VERSION = "kuuos_nonmarkov_cognitive_loop_kernel_v0_23"
EPISODE_VERSION = "kuuos_nonmarkov_cognitive_episode_v0_23"
STRATEGY_VERSION = "kuuos_future_strategy_delta_v0_23"
HANDOFF_VERSION = "kuuos_cognitive_loop_handoff_v0_23"

VERIFICATION_ROUTES = frozenset({"passed", "failed", "indeterminate"})
OBSERVATION_ROUTES = frozenset({"matched", "divergent", "inconclusive", "conflicted"})
PLAN_ROUTES = frozenset(
    {
        "continue_candidate",
        "complete_candidate",
        "reobserve",
        "replan",
        "suspend_revalidate",
        "renew_or_escalate",
        "rerotate_required",
    }
)
STEP_OUTCOMES = frozenset({"succeeded", "failed", "unknown", "not_observed"})

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_world_rewrite_authority": False,
    "grants_final_commitment_authority": False,
    "grants_self_modification_authority": False,
    "grants_clinical_authority": False,
    "grants_theorem_authority": False,
}

REQUIRED_BOUNDARY = {
    "belief_plurality_preserved": True,
    "belief_coherence_defect_widens_uncertainty": True,
    "observation_is_not_verification": True,
    "verification_is_not_truth": True,
    "every_verification_route_creates_learning_debt": True,
    "learning_is_future_only": True,
    "automatic_learning_is_forbidden": True,
    "memory_consolidation_is_append_only": True,
    "memory_overwrite_is_forbidden": True,
    "process_history_is_not_replaced_by_snapshot": True,
    "observation_backaction_is_preserved": True,
    "nonmarkov_trace_is_preserved": True,
    "plan_remains_proposal_only": True,
    "execution_success_is_not_mission_success": True,
    "suspension_recovery_grants_no_execution_authority": True,
    "qi_is_context_not_authority": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def episode_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_episode_digest"))


def strategy_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "strategy_delta_digest"))


def handoff_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_loop_handoff_digest"))


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0:
        raise ValueError(f"{name}_negative")
    return result


def _unit(value: Any, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_not_finite")
    if result < 0.0 or result > 1.0:
        raise ValueError(f"{name}_outside_unit_interval")
    return result


def _strings(values: Sequence[Any], name: str, *, allow_empty: bool = False) -> list[str]:
    result = [_text(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _source_errors(
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> list[str]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    errors.extend(
        "belief_state:" + item
        for item in validate_belief_state(belief_state, contract, mission_state)
    )
    errors.extend("goal:" + item for item in validate_goal_proposal(goal, contract))
    errors.extend(
        "goal_portfolio:" + item
        for item in validate_goal_portfolio(goal_portfolio, contract)
    )
    errors.extend(
        "plan:" + item
        for item in validate_semantic_plan(
            plan,
            contract,
            mission_state,
            belief_state,
            goal,
            goal_portfolio,
        )
    )
    return errors


def _process_tensor_summary(
    packet: Mapping[str, Any], result: Mapping[str, Any]
) -> dict[str, Any]:
    process = packet.get("process_tensor", {})
    if not isinstance(process, Mapping):
        process = {}
    operations = process.get("operations", [])
    memory_links = process.get("memory_links", [])
    if not isinstance(operations, list):
        operations = []
    if not isinstance(memory_links, list):
        memory_links = []
    valid = result.get("valid") is True
    transition_visible = len(operations) >= 2 and all(
        isinstance(item, Mapping) and item.get("backaction_visible") is True
        for item in operations
    )
    memory_visible = bool(memory_links) and all(
        isinstance(item, Mapping) and item.get("tail_residue_visible") is True
        for item in memory_links
    )
    candidate = result.get("candidate_payload", {})
    if not isinstance(candidate, Mapping):
        candidate = {}
    return {
        "process_tensor_visible": valid,
        "transition_continuity_visible": transition_visible,
        "memory_continuity_visible": memory_visible,
        "nonmarkov_memory_visible": candidate.get("non_markov_primary") is True,
        "process_history_length": len(operations),
        "missing_process_requirements": list(result.get("errors", [])),
    }


def _belief_coherence_projection(
    belief_state: Mapping[str, Any],
    plan: Mapping[str, Any],
    coherence_defect: float,
) -> dict[str, Any]:
    claims = belief_state.get("claims", {})
    if not isinstance(claims, Mapping):
        claims = {}
    claim_ids = [str(item) for item in plan.get("required_claim_ids", [])]
    selected = [claims[item] for item in claim_ids if item in claims]
    confidences = [float(item.get("confidence", 0.0)) for item in selected]
    base_confidence = min(confidences) if confidences else 0.0
    contradiction_count = sum(
        1 for item in selected if str(item.get("status")) == "contradicted"
    )
    unknown_count = sum(
        1
        for item in selected
        if str(item.get("status")) in {"unknown", "stale"}
    )
    residue_count = len(belief_state.get("contradiction_residues", []))
    selected_count = max(1, len(selected))
    endogenous_defect = min(
        1.0,
        (contradiction_count + 0.5 * unknown_count + 0.25 * residue_count)
        / selected_count,
    )
    defect = max(coherence_defect, endogenous_defect)
    lower = max(0.0, base_confidence - defect)
    upper = min(1.0, base_confidence + defect)
    return {
        "base_confidence": round(base_confidence, 6),
        "coherence_defect": round(defect, 6),
        "coherent_lower": round(lower, 6),
        "coherent_upper": round(upper, 6),
        "required_claim_count": len(claim_ids),
        "available_claim_count": len(selected),
        "contradiction_count": contradiction_count,
        "unknown_or_stale_count": unknown_count,
        "plurality_preserved": True,
        "global_winner_selected": False,
        "global_trivialization_used": False,
        "residue_grants_authority": False,
        "residue_grants_veto": False,
    }


def _verification_route(status: str) -> str:
    if status == "verified_success":
        return "passed"
    if status in {"contradicted", "regression_detected"}:
        return "failed"
    return "indeterminate"


def _observation_route(
    verification_status: str,
    expected: set[str],
    actual: set[str],
) -> str:
    if verification_status in {"contradicted", "regression_detected"}:
        return "conflicted"
    if expected and expected.issubset(actual):
        return "matched"
    if actual and expected - actual:
        return "divergent"
    return "inconclusive"


def _plan_route(
    *,
    verification_route: str,
    missing_expected: Sequence[str],
    observation_action: str,
    recovery_unsafe: bool,
    hold_reasons: Sequence[str],
    suspension_context: Mapping[str, Any],
) -> str:
    if suspension_context.get("suspended") is True:
        requested = str(suspension_context.get("recovery_route") or "revalidate")
        return {
            "revalidate": "suspend_revalidate",
            "renew_or_escalate": "renew_or_escalate",
            "rerotate_required": "rerotate_required",
        }.get(requested, "suspend_revalidate")
    if recovery_unsafe or hold_reasons:
        return "suspend_revalidate"
    if verification_route == "failed":
        return "replan"
    if (
        verification_route == "indeterminate"
        or bool(missing_expected)
        or observation_action in {"observe", "reobserve"}
    ):
        return "reobserve"
    if verification_route == "passed":
        return "complete_candidate"
    return "continue_candidate"


def _normalize_step_outcomes(
    plan: Mapping[str, Any],
    step_outcomes: Sequence[Mapping[str, Any]],
    verification_route: str,
) -> list[dict[str, Any]]:
    declared_steps = {
        str(item.get("step_id")): item
        for item in plan.get("steps", [])
        if isinstance(item, Mapping)
    }
    supplied: dict[str, Mapping[str, Any]] = {}
    for item in step_outcomes:
        step_id = _text(item.get("step_id"), "step_id")
        if step_id not in declared_steps:
            raise ValueError("step_outcome_unknown_step")
        if step_id in supplied:
            raise ValueError("step_outcome_duplicate")
        supplied[step_id] = item

    result: list[dict[str, Any]] = []
    for step_id, step in declared_steps.items():
        source = supplied.get(step_id, {})
        outcome = str(source.get("outcome") or "unknown")
        if outcome not in STEP_OUTCOMES:
            raise ValueError("step_outcome_invalid")
        evidence_refs = _strings(
            source.get("evidence_refs", []),
            "step_evidence_refs",
            allow_empty=True,
        )
        raw_credit = {
            "succeeded": 1.0,
            "failed": -1.0,
            "unknown": 0.0,
            "not_observed": 0.0,
        }[outcome]
        bounded_credit = min(raw_credit, 0.5) if verification_route != "passed" else raw_credit
        action = {
            "succeeded": "retain_candidate",
            "failed": "repair_or_deprioritize",
            "unknown": "request_observation",
            "not_observed": "preserve_unresolved",
        }[outcome]
        result.append(
            {
                "step_id": step_id,
                "plan_step_digest": step.get("plan_step_digest"),
                "outcome": outcome,
                "bounded_credit": bounded_credit,
                "strategy_action": action,
                "evidence_refs": evidence_refs,
                "local_step_credit_only": True,
                "mission_success_credit": False,
            }
        )
    return result


def build_future_strategy_delta(
    *,
    contract: Mapping[str, Any],
    plan: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    step_outcomes: Sequence[Mapping[str, Any]],
    memory_replay: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    route = _verification_route(str(verification_receipt.get("status")))
    normalized = _normalize_step_outcomes(plan, step_outcomes, route)
    mean_credit = (
        sum(float(item["bounded_credit"]) for item in normalized) / len(normalized)
        if normalized
        else 0.0
    )
    replay_hint = str(memory_replay.get("probe_planner_reuse_hint") or "")
    delta = {
        "version": STRATEGY_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_plan_digest": plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "verification_route": route,
        "step_credit_assignments": normalized,
        "aggregate_bounded_credit": round(mean_credit, 6),
        "memory_replay_hint": replay_hint,
        "future_only": True,
        "automatic_application": False,
        "current_plan_mutated": False,
        "current_belief_root_mutated": False,
        "memory_root_overwritten": False,
        "candidate_weighting_not_truth": True,
        "created_at_ms": _nonnegative_int(created_at_ms, "created_at_ms"),
        "non_authority": deepcopy(NON_AUTHORITY),
        "strategy_delta_digest": "",
    }
    delta["strategy_delta_digest"] = strategy_digest(delta)
    errors = validate_future_strategy_delta(delta)
    if errors:
        raise ValueError(";".join(errors))
    return delta


def validate_future_strategy_delta(delta: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if delta.get("version") != STRATEGY_VERSION:
        errors.append("strategy_version_invalid")
    if delta.get("verification_route") not in VERIFICATION_ROUTES:
        errors.append("strategy_verification_route_invalid")
    assignments = delta.get("step_credit_assignments")
    if not isinstance(assignments, list):
        errors.append("strategy_assignments_invalid")
    else:
        identifiers = [str(item.get("step_id", "")) for item in assignments]
        if len(identifiers) != len(set(identifiers)):
            errors.append("strategy_assignment_duplicate")
        for item in assignments:
            try:
                credit = float(item.get("bounded_credit"))
                if not math.isfinite(credit) or credit < -1.0 or credit > 1.0:
                    errors.append("strategy_credit_out_of_bounds")
            except (TypeError, ValueError):
                errors.append("strategy_credit_invalid")
            if item.get("local_step_credit_only") is not True:
                errors.append("strategy_local_credit_boundary_invalid")
            if item.get("mission_success_credit") is not False:
                errors.append("strategy_mission_success_credit_forbidden")
    for field, expected in (
        ("future_only", True),
        ("automatic_application", False),
        ("current_plan_mutated", False),
        ("current_belief_root_mutated", False),
        ("memory_root_overwritten", False),
        ("candidate_weighting_not_truth", True),
    ):
        if delta.get(field) is not expected:
            errors.append(f"strategy_{field}_invalid")
    if dict(delta.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("strategy_non_authority_invalid")
    if delta.get("strategy_delta_digest") != strategy_digest(delta):
        errors.append("strategy_digest_invalid")
    return errors


def _build_memory_probe_result(
    plan: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    trace_digest: str,
) -> dict[str, Any]:
    return {
        "execution_status": "QI_ONE_SHOT_PROBE_EXECUTION_PERFORMED",
        "probe_type": "nonmarkov_cognitive_cycle_observation",
        "probe_result_summary": (
            "Observed one bounded cognitive cycle with plan, independent verification, "
            "and Qi process-tensor history preserved"
        ),
        "probe_execution_performed": True,
        "probe_result_artifact_only": True,
        "one_shot_token_consumed": True,
        "token_reuse_allowed": False,
        "source_plan_digest": plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "process_tensor_trace_digest": trace_digest,
        "grants_probe_execution_authority": False,
        "grants_execution_authority": False,
        "grants_memory_overwrite_authority": False,
        "grants_world_update_authority": False,
        "grants_control_packet_authority": False,
        "grants_scheduler_authority": False,
        "memory_write_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "scheduler_state_mutation_performed": False,
    }


def build_nonmarkov_cognitive_episode(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    plan: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    qi_process_tensor_packet: Mapping[str, Any],
    prior_memory_entries: Sequence[Mapping[str, Any]],
    actual_observation_labels: Sequence[str],
    step_outcomes: Sequence[Mapping[str, Any]],
    coherence_defect: float,
    cycle_index: int,
    created_at_ms: int,
    suspension_context: Mapping[str, Any] | None = None,
    reentry_plan: Mapping[str, Any] | None = None,
    license_gate: Mapping[str, Any] | None = None,
    invocation_boundary: Mapping[str, Any] | None = None,
    executor_receipt: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    errors = _source_errors(
        contract,
        mission_state,
        belief_state,
        goal,
        goal_portfolio,
        plan,
    )
    errors.extend(
        "verification:" + item
        for item in validate_verification_receipt_static(verification_receipt)
    )
    if errors:
        raise ValueError(";".join(errors))
    if verification_receipt.get("mission_id") != contract.get("mission_id"):
        raise ValueError("verification_mission_mismatch")
    if verification_receipt.get("source_plan_digest") != plan.get(
        "semantic_plan_digest"
    ):
        raise ValueError("verification_plan_mismatch")
    if verification_receipt.get("chart_id") != belief_state.get("chart_id"):
        raise ValueError("verification_chart_mismatch")

    defect = _unit(coherence_defect, "coherence_defect")
    cycle = _nonnegative_int(cycle_index, "cycle_index")
    created = _nonnegative_int(created_at_ms, "created_at_ms")
    actual_labels = set(
        _strings(
            actual_observation_labels,
            "actual_observation_labels",
            allow_empty=True,
        )
    )

    qi_result_object = build_qi_process_tensor_result(qi_process_tensor_packet)
    qi_result = qi_result_object.to_dict()
    if not qi_result["valid"]:
        raise ValueError("qi_process_tensor_invalid:" + ";".join(qi_result["errors"]))
    process_summary = _process_tensor_summary(qi_process_tensor_packet, qi_result)
    process = qi_process_tensor_packet.get("process_tensor", {})
    if not isinstance(process, Mapping):
        process = {}
    trace_digest = sha(
        {
            "packet_id": qi_result["packet_id"],
            "operations": process.get("operations", []),
            "memory_links": process.get("memory_links", []),
        }
    )

    memory_replay_object = build_qi_memoryos_process_tensor_retrieval_replay(
        memory_entries=prior_memory_entries,
        replay_context={
            "request_memory_write": False,
            "request_memory_overwrite": False,
            "request_world_update": False,
            "request_scheduler_mutation": False,
            "request_probe_execution": False,
        },
    )
    memory_replay = memory_replay_object.to_dict()
    memory_mode = (
        "history_replay_ready"
        if memory_replay["replay_status"]
        == "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY"
        else "cold_start_or_history_gap"
    )

    recoverability_object = compile_qi_process_tensor_recoverability_projection(
        process_tensor_summary=process_summary,
        reentry_plan=reentry_plan or {},
        license_gate=license_gate or {},
        invocation_boundary=invocation_boundary or {},
        executor_receipt=executor_receipt or {},
    )
    recoverability = recoverability_object.to_dict()
    observation_schedule_object = compile_qi_process_tensor_observation_debt_schedule(
        process_tensor_summary=process_summary,
        recoverability_projection=recoverability,
    )
    observation_schedule = observation_schedule_object.to_dict()

    expected_labels = {
        str(label)
        for step in plan.get("steps", [])
        if isinstance(step, Mapping)
        for label in step.get("expected_observations", [])
    }
    missing_expected = sorted(expected_labels - actual_labels)
    verify_route = _verification_route(str(verification_receipt["status"]))
    observe_route = _observation_route(
        str(verification_receipt["status"]), expected_labels, actual_labels
    )
    coherence = _belief_coherence_projection(belief_state, plan, defect)
    suspension = suspension_context or {}
    plan_route = _plan_route(
        verification_route=verify_route,
        missing_expected=missing_expected,
        observation_action=str(
            observation_schedule["recommended_observation_action"]
        ),
        recovery_unsafe=bool(recoverability["recovery_unsafe"]),
        hold_reasons=observation_schedule["hold_reasons"],
        suspension_context=suspension,
    )

    strategy_delta = build_future_strategy_delta(
        contract=contract,
        plan=plan,
        verification_receipt=verification_receipt,
        step_outcomes=step_outcomes,
        memory_replay=memory_replay,
        created_at_ms=created,
    )

    memory_probe_result = _build_memory_probe_result(
        plan, verification_receipt, trace_digest
    )
    append_receipt_object = run_qi_memoryos_process_tensor_append_writeback(
        probe_result=memory_probe_result,
        writeback_context={
            "memory_entry_kind": "nonmarkov_cognitive_episode",
            "memory_entry_summary": (
                f"cycle={cycle}; verification={verification_receipt['status']}; "
                f"plan_route={plan_route}; observation_route={observe_route}"
            ),
            "memoryos_target_stream": "memoryos/nonmarkov_cognitive_loop/append_only",
            "append_only_required": True,
            "lineage_preserved": True,
            "process_tensor_trace_preserved": True,
            "nonmarkov_trace_preserved": True,
            "observation_debt_trace_preserved": True,
            "recoverability_trace_preserved": True,
            "safe_reentry_trace_preserved": True,
            "no_memory_overwrite": True,
            "no_world_update": True,
            "no_control_packet_mutation": True,
            "request_memory_overwrite": False,
            "request_memory_delete": False,
            "request_world_update": False,
            "request_control_packet_mutation": False,
            "request_scheduler_mutation": False,
        },
    )
    append_receipt = append_receipt_object.to_dict()
    if append_receipt["writeback_status"] != (
        "QI_MEMORYOS_PROCESS_TENSOR_APPEND_WRITEBACK_PERFORMED"
    ):
        raise ValueError(
            "memory_append_writeback_blocked:"
            + ";".join(append_receipt["writeback_blockers"])
        )

    handoff = {
        "version": HANDOFF_VERSION,
        "beliefos": {
            "coherence_projection": coherence,
            "local_chart_preserved": True,
            "plurality_preserved": True,
            "truth_authority_granted": False,
        },
        "observeos": {
            "route": observe_route,
            "expected_observation_labels": sorted(expected_labels),
            "actual_observation_labels": sorted(actual_labels),
            "missing_expected_observation_labels": missing_expected,
            "observation_debt_schedule": observation_schedule,
            "observation_not_verification": True,
        },
        "verifyos": {
            "route": verify_route,
            "verification_status": verification_receipt["status"],
            "falsification_surface_preserved": True,
            "counterevidence_preserved": True,
            "independent_assessment_preserved": True,
            "verification_not_truth": True,
            "learning_required": True,
        },
        "planos": {
            "route": plan_route,
            "old_session_closed": bool(suspension.get("suspended")),
            "old_session_resume_allowed": False
            if suspension.get("suspended") is True
            else True,
            "new_lineage_required": plan_route == "rerotate_required",
            "new_activation_required": plan_route
            in {"suspend_revalidate", "renew_or_escalate", "rerotate_required"},
            "new_session_required": plan_route
            in {"suspend_revalidate", "renew_or_escalate", "rerotate_required"},
            "execution_granted": False,
            "host_access_granted": False,
            "memory_overwrite": False,
        },
        "memoryos": {
            "mode": memory_mode,
            "retrieval_replay": memory_replay,
            "append_writeback_receipt": append_receipt,
            "append_only": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite": False,
        },
        "qi_process_tensor": {
            "packet_id": qi_result["packet_id"],
            "trace_digest": trace_digest,
            "process_summary": process_summary,
            "recoverability_projection": recoverability,
            "history_state_not_replaced_by_snapshot": True,
            "observation_backaction_visible": True,
            "tail_residue_visible": True,
            "authority_granted": False,
        },
        "strategy_learning": strategy_delta,
        "cognitive_loop_handoff_digest": "",
    }
    handoff["cognitive_loop_handoff_digest"] = handoff_digest(handoff)

    packet = {
        "version": EPISODE_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_belief_state_digest": belief_state[
            "observation_belief_state_digest"
        ],
        "chart_id": belief_state["chart_id"],
        "goal_id": goal["goal_id"],
        "source_plan_digest": plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "cycle_index": cycle,
        "verification_route": verify_route,
        "observation_route": observe_route,
        "plan_route": plan_route,
        "process_tensor_trace_digest": trace_digest,
        "memory_mode": memory_mode,
        "coherence_projection": coherence,
        "missing_expected_observation_labels": missing_expected,
        "strategy_delta_digest": strategy_delta["strategy_delta_digest"],
        "handoff": handoff,
        "created_at_ms": created,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "cognitive_episode_digest": "",
    }
    packet["cognitive_episode_digest"] = episode_digest(packet)
    episode_errors = validate_nonmarkov_cognitive_episode(packet)
    if episode_errors:
        raise ValueError(";".join(episode_errors))
    return packet


def validate_nonmarkov_cognitive_episode(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("version") != EPISODE_VERSION:
        errors.append("episode_version_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "contract_digest",
        "source_mission_state_digest",
        "source_belief_state_digest",
        "chart_id",
        "goal_id",
        "source_plan_digest",
        "source_verification_digest",
        "process_tensor_trace_digest",
        "strategy_delta_digest",
    ):
        if not str(packet.get(field, "")).strip():
            errors.append(f"episode_{field}_missing")
    if packet.get("verification_route") not in VERIFICATION_ROUTES:
        errors.append("episode_verification_route_invalid")
    if packet.get("observation_route") not in OBSERVATION_ROUTES:
        errors.append("episode_observation_route_invalid")
    if packet.get("plan_route") not in PLAN_ROUTES:
        errors.append("episode_plan_route_invalid")
    if packet.get("memory_mode") not in {
        "history_replay_ready",
        "cold_start_or_history_gap",
    }:
        errors.append("episode_memory_mode_invalid")
    if not isinstance(packet.get("missing_expected_observation_labels"), list):
        errors.append("episode_missing_observations_invalid")
    handoff = packet.get("handoff")
    if not isinstance(handoff, Mapping):
        errors.append("episode_handoff_invalid")
    else:
        if handoff.get("cognitive_loop_handoff_digest") != handoff_digest(handoff):
            errors.append("episode_handoff_digest_invalid")
        memory = handoff.get("memoryos", {})
        if not isinstance(memory, Mapping):
            errors.append("episode_memoryos_invalid")
        else:
            if memory.get("append_only") is not True:
                errors.append("episode_memory_append_only_invalid")
            if memory.get("memory_overwrite") is not False:
                errors.append("episode_memory_overwrite_forbidden")
            if memory.get("durable_persistence_performed_by_this_kernel") is not False:
                errors.append("episode_durable_persistence_claim_forbidden")
        strategy = handoff.get("strategy_learning", {})
        if not isinstance(strategy, Mapping):
            errors.append("episode_strategy_invalid")
        else:
            errors.extend(
                "strategy:" + item for item in validate_future_strategy_delta(strategy)
            )
            if packet.get("strategy_delta_digest") != strategy.get(
                "strategy_delta_digest"
            ):
                errors.append("episode_strategy_digest_mismatch")
        qi = handoff.get("qi_process_tensor", {})
        if not isinstance(qi, Mapping):
            errors.append("episode_qi_invalid")
        else:
            for field, expected in (
                ("history_state_not_replaced_by_snapshot", True),
                ("observation_backaction_visible", True),
                ("tail_residue_visible", True),
                ("authority_granted", False),
            ):
                if qi.get(field) is not expected:
                    errors.append(f"episode_qi_{field}_invalid")
        observe = handoff.get("observeos", {})
        if not isinstance(observe, Mapping) or observe.get(
            "observation_not_verification"
        ) is not True:
            errors.append("episode_observation_verification_boundary_invalid")
        verify = handoff.get("verifyos", {})
        if not isinstance(verify, Mapping):
            errors.append("episode_verifyos_invalid")
        else:
            if verify.get("verification_not_truth") is not True:
                errors.append("episode_verification_truth_boundary_invalid")
            if verify.get("learning_required") is not True:
                errors.append("episode_learning_debt_missing")
        plan = handoff.get("planos", {})
        if not isinstance(plan, Mapping):
            errors.append("episode_planos_invalid")
        else:
            for field in ("execution_granted", "host_access_granted", "memory_overwrite"):
                if plan.get(field) is not False:
                    errors.append(f"episode_planos_{field}_forbidden")
    if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("episode_non_authority_invalid")
    if dict(packet.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("episode_boundary_invalid")
    if packet.get("cognitive_episode_digest") != episode_digest(packet):
        errors.append("episode_digest_invalid")
    return errors


__all__ = [
    "EPISODE_VERSION",
    "HANDOFF_VERSION",
    "NON_AUTHORITY",
    "OBSERVATION_ROUTES",
    "PLAN_ROUTES",
    "REQUIRED_BOUNDARY",
    "STEP_OUTCOMES",
    "STRATEGY_VERSION",
    "VERIFICATION_ROUTES",
    "VERSION",
    "build_future_strategy_delta",
    "build_nonmarkov_cognitive_episode",
    "episode_digest",
    "handoff_digest",
    "strategy_digest",
    "validate_future_strategy_delta",
    "validate_nonmarkov_cognitive_episode",
]
