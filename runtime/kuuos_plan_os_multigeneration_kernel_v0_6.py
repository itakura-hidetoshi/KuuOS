from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_plan_os_generational_driver_kernel_v0_5 import (
    validate_generational_cycle_receipt,
)
from runtime.kuuos_plan_os_multigeneration_types_v0_6 import (
    ACTIVE,
    BOUNDARY,
    CONTINUE,
    DECISION_VERSION,
    DECISIONS,
    EVENT_VERSION,
    HANDOVER,
    HANDOVER_AUTHORITY,
    HANDOVER_HUMAN,
    HOLD,
    HOLD_OBSERVATION_DEBT,
    HOLD_RECOVERY,
    NON_AUTHORITY,
    POLICY_VERSION,
    REPORT_VERSION,
    STATE_VERSION,
    STOP_CONVERGED,
    STOP_MAX_GENERATIONS,
    STOP_MISSION_COMPLETE,
    STOP_OSCILLATION,
    STOP_STAGNATION,
    STOPPED,
    TERMINAL_STATUSES,
    copy_boundary,
    copy_non_authority,
    decision_digest,
    event_digest,
    policy_digest,
    report_digest,
    require_int,
    require_string,
    state_digest,
    unit_number,
)


def build_multi_generation_policy(
    *,
    maximum_generations: int,
    convergence_threshold: float,
    stagnation_limit: int,
    oscillation_limit: int,
    observation_debt_limit: float,
    recovery_hold_threshold: float,
) -> dict[str, Any]:
    policy = {
        "version": POLICY_VERSION,
        "maximum_generations": require_int(
            maximum_generations, "maximum_generations", minimum=1
        ),
        "convergence_threshold": unit_number(
            convergence_threshold, "convergence_threshold"
        ),
        "stagnation_limit": require_int(
            stagnation_limit, "stagnation_limit", minimum=1
        ),
        "oscillation_limit": require_int(
            oscillation_limit, "oscillation_limit", minimum=1
        ),
        "observation_debt_limit": unit_number(
            observation_debt_limit, "observation_debt_limit"
        ),
        "recovery_hold_threshold": unit_number(
            recovery_hold_threshold, "recovery_hold_threshold"
        ),
        "terminal_state_blocks_automatic_continuation": True,
        "multi_generation_policy_digest": "",
    }
    policy["multi_generation_policy_digest"] = policy_digest(policy)
    return policy


def validate_multi_generation_policy(policy: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if policy.get("version") != POLICY_VERSION:
            errors.append("multi_generation_policy_version_invalid")
        if policy.get("multi_generation_policy_digest") != policy_digest(policy):
            errors.append("multi_generation_policy_digest_invalid")
        require_int(policy.get("maximum_generations"), "maximum_generations", minimum=1)
        unit_number(policy.get("convergence_threshold"), "convergence_threshold")
        require_int(policy.get("stagnation_limit"), "stagnation_limit", minimum=1)
        require_int(policy.get("oscillation_limit"), "oscillation_limit", minimum=1)
        unit_number(policy.get("observation_debt_limit"), "observation_debt_limit")
        unit_number(
            policy.get("recovery_hold_threshold"), "recovery_hold_threshold"
        )
        if policy.get("terminal_state_blocks_automatic_continuation") is not True:
            errors.append("multi_generation_terminal_block_required")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_multi_generation_state(
    *,
    supervisor_id: str,
    lineage_id: str,
    mission_contract_digest: str,
    initial_cycle_index: int,
    policy: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    policy_errors = validate_multi_generation_policy(policy)
    if policy_errors:
        raise ValueError("multi_generation_policy_invalid:" + ";".join(policy_errors))
    state = {
        "version": STATE_VERSION,
        "supervisor_id": require_string(supervisor_id, "supervisor_id"),
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "mission_contract_digest": require_string(
            mission_contract_digest, "mission_contract_digest"
        ),
        "policy": deepcopy(dict(policy)),
        "policy_digest": policy["multi_generation_policy_digest"],
        "status": ACTIVE,
        "terminal_reason": "",
        "completed_generations": 0,
        "current_cycle_index": require_int(
            initial_cycle_index, "initial_cycle_index"
        ),
        "last_generation_report_digest": "",
        "last_v05_generation_receipt_digest": "",
        "next_generation_authorized": True,
        "event_index": 0,
        "processed_event_digests": [],
        "generation_history": [],
        "created_at_ms": require_int(now_ms, "now_ms"),
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "multi_generation_supervisor_state_digest": "",
    }
    state["multi_generation_supervisor_state_digest"] = state_digest(state)
    return state


def validate_multi_generation_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("multi_generation_state_version_invalid")
        if state.get("multi_generation_supervisor_state_digest") != state_digest(state):
            errors.append("multi_generation_state_digest_invalid")
        require_string(state.get("supervisor_id"), "supervisor_id")
        require_string(state.get("lineage_id"), "lineage_id")
        require_string(state.get("mission_contract_digest"), "mission_contract_digest")
        policy_errors = validate_multi_generation_policy(dict(state.get("policy", {})))
        if policy_errors:
            errors.extend(policy_errors)
        if state.get("policy_digest") != dict(state.get("policy", {})).get(
            "multi_generation_policy_digest"
        ):
            errors.append("multi_generation_state_policy_binding_invalid")
        status = state.get("status")
        if status not in {ACTIVE, HOLD, STOPPED, HANDOVER}:
            errors.append("multi_generation_state_status_invalid")
        completed = require_int(
            state.get("completed_generations"), "completed_generations"
        )
        maximum = int(dict(state.get("policy", {})).get("maximum_generations", 0))
        if completed > maximum:
            errors.append("multi_generation_state_bound_exceeded")
        require_int(state.get("current_cycle_index"), "current_cycle_index")
        require_int(state.get("event_index"), "event_index")
        history = list(state.get("generation_history", []))
        processed = list(state.get("processed_event_digests", []))
        if len(history) != completed:
            errors.append("multi_generation_history_count_mismatch")
        if len(processed) != int(state.get("event_index", -1)):
            errors.append("multi_generation_event_count_mismatch")
        if len(processed) != len(set(processed)):
            errors.append("multi_generation_event_duplicate")
        if status == ACTIVE:
            if state.get("terminal_reason"):
                errors.append("multi_generation_active_terminal_reason_forbidden")
            if state.get("next_generation_authorized") is not True:
                errors.append("multi_generation_active_authorization_required")
        if status in TERMINAL_STATUSES:
            require_string(state.get("terminal_reason"), "terminal_reason")
            if state.get("next_generation_authorized") is not False:
                errors.append("multi_generation_terminal_authorization_forbidden")
        for field, expected in {
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if state.get(field) != expected:
                errors.append(f"multi_generation_state_{field}_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("multi_generation_state_authority_invalid")
        if dict(state.get("boundary", {})) != BOUNDARY:
            errors.append("multi_generation_state_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_supervised_generation_report(
    *,
    supervisor_state: Mapping[str, Any],
    generational_cycle_receipt: Mapping[str, Any],
    plan_change_score: float,
    objective_residual: float,
    stagnation_count: int,
    oscillation_count: int,
    observation_debt: float,
    recovery_protection: float,
    mission_complete: bool,
    human_handover_requested: bool,
    authority_boundary_hit: bool,
    now_ms: int,
) -> dict[str, Any]:
    state_errors = validate_multi_generation_state(supervisor_state)
    if state_errors:
        raise ValueError("multi_generation_state_invalid:" + ";".join(state_errors))
    source_errors = validate_generational_cycle_receipt(generational_cycle_receipt)
    if source_errors:
        raise ValueError("v05_generation_receipt_invalid:" + ";".join(source_errors))
    if supervisor_state.get("status") != ACTIVE:
        raise ValueError("multi_generation_supervisor_not_active")
    if generational_cycle_receipt.get("lineage_id") != supervisor_state.get(
        "lineage_id"
    ):
        raise ValueError("multi_generation_lineage_mismatch")
    if generational_cycle_receipt.get(
        "mission_contract_digest"
    ) != supervisor_state.get("mission_contract_digest"):
        raise ValueError("multi_generation_mission_mismatch")
    report = {
        "version": REPORT_VERSION,
        "supervisor_id": supervisor_state["supervisor_id"],
        "lineage_id": supervisor_state["lineage_id"],
        "mission_contract_digest": supervisor_state["mission_contract_digest"],
        "generation_index": int(supervisor_state["completed_generations"]) + 1,
        "source_cycle_index": generational_cycle_receipt["source_cycle_index"],
        "next_cycle_index": generational_cycle_receipt["next_cycle_index"],
        "previous_generation_report_digest": supervisor_state[
            "last_generation_report_digest"
        ],
        "generational_cycle_receipt_digest": generational_cycle_receipt[
            "generational_cycle_receipt_digest"
        ],
        "compiled_plan_state_digest": generational_cycle_receipt[
            "compiled_plan_state_digest"
        ],
        "act_handoff_receipt_digest": generational_cycle_receipt[
            "act_handoff_receipt_digest"
        ],
        "selected_candidate_digest": generational_cycle_receipt[
            "selected_candidate_digest"
        ],
        "plan_change_score": unit_number(plan_change_score, "plan_change_score"),
        "objective_residual": unit_number(objective_residual, "objective_residual"),
        "stagnation_count": require_int(stagnation_count, "stagnation_count"),
        "oscillation_count": require_int(oscillation_count, "oscillation_count"),
        "observation_debt": unit_number(observation_debt, "observation_debt"),
        "recovery_protection": unit_number(
            recovery_protection, "recovery_protection"
        ),
        "mission_complete": bool(mission_complete),
        "human_handover_requested": bool(human_handover_requested),
        "authority_boundary_hit": bool(authority_boundary_hit),
        "source_execution_granted": generational_cycle_receipt[
            "execution_granted"
        ],
        "source_host_license_granted": generational_cycle_receipt[
            "host_license_granted"
        ],
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "supervised_generation_report_digest": "",
    }
    report["supervised_generation_report_digest"] = report_digest(report)
    return report


def validate_supervised_generation_report(report: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if report.get("version") != REPORT_VERSION:
            errors.append("supervised_generation_report_version_invalid")
        if report.get("supervised_generation_report_digest") != report_digest(report):
            errors.append("supervised_generation_report_digest_invalid")
        for field in (
            "supervisor_id",
            "lineage_id",
            "mission_contract_digest",
            "generational_cycle_receipt_digest",
            "compiled_plan_state_digest",
            "act_handoff_receipt_digest",
            "selected_candidate_digest",
        ):
            require_string(report.get(field), field)
        require_int(report.get("generation_index"), "generation_index", minimum=1)
        source_cycle = require_int(report.get("source_cycle_index"), "source_cycle_index")
        next_cycle = require_int(report.get("next_cycle_index"), "next_cycle_index")
        if next_cycle != source_cycle + 1:
            errors.append("supervised_generation_successor_cycle_invalid")
        unit_number(report.get("plan_change_score"), "plan_change_score")
        unit_number(report.get("objective_residual"), "objective_residual")
        require_int(report.get("stagnation_count"), "stagnation_count")
        require_int(report.get("oscillation_count"), "oscillation_count")
        unit_number(report.get("observation_debt"), "observation_debt")
        unit_number(report.get("recovery_protection"), "recovery_protection")
        for field in (
            "mission_complete",
            "human_handover_requested",
            "authority_boundary_hit",
        ):
            if not isinstance(report.get(field), bool):
                errors.append(f"supervised_generation_{field}_bool_required")
        for field, expected in {
            "source_execution_granted": False,
            "source_host_license_granted": False,
        }.items():
            if report.get(field) != expected:
                errors.append(f"supervised_generation_{field}_invalid")
        if dict(report.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("supervised_generation_authority_invalid")
        if dict(report.get("boundary", {})) != BOUNDARY:
            errors.append("supervised_generation_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _decision_code(state: Mapping[str, Any], report: Mapping[str, Any]) -> str:
    policy = dict(state["policy"])
    generation = int(report["generation_index"])
    if report["human_handover_requested"]:
        return HANDOVER_HUMAN
    if report["authority_boundary_hit"]:
        return HANDOVER_AUTHORITY
    if report["mission_complete"]:
        return STOP_MISSION_COMPLETE
    if generation >= int(policy["maximum_generations"]):
        return STOP_MAX_GENERATIONS
    threshold = float(policy["convergence_threshold"])
    if (
        float(report["objective_residual"]) <= threshold
        and float(report["plan_change_score"]) <= threshold
    ):
        return STOP_CONVERGED
    if int(report["stagnation_count"]) >= int(policy["stagnation_limit"]):
        return STOP_STAGNATION
    if int(report["oscillation_count"]) >= int(policy["oscillation_limit"]):
        return STOP_OSCILLATION
    if float(report["observation_debt"]) >= float(
        policy["observation_debt_limit"]
    ):
        return HOLD_OBSERVATION_DEBT
    if float(report["recovery_protection"]) >= float(
        policy["recovery_hold_threshold"]
    ):
        return HOLD_RECOVERY
    return CONTINUE


def build_generation_supervision_decision(
    *, state: Mapping[str, Any], report: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    state_errors = validate_multi_generation_state(state)
    if state_errors:
        raise ValueError("multi_generation_state_invalid:" + ";".join(state_errors))
    report_errors = validate_supervised_generation_report(report)
    if report_errors:
        raise ValueError("supervised_generation_report_invalid:" + ";".join(report_errors))
    if state.get("status") != ACTIVE:
        raise ValueError("multi_generation_terminal_state_blocks_continuation")
    expected_generation = int(state["completed_generations"]) + 1
    if report.get("generation_index") != expected_generation:
        raise ValueError("multi_generation_generation_index_mismatch")
    if report.get("source_cycle_index") != state.get("current_cycle_index"):
        raise ValueError("multi_generation_source_cycle_mismatch")
    if report.get("next_cycle_index") != int(state["current_cycle_index"]) + 1:
        raise ValueError("multi_generation_next_cycle_mismatch")
    if report.get("previous_generation_report_digest") != state.get(
        "last_generation_report_digest"
    ):
        raise ValueError("multi_generation_report_chain_broken")
    for field in ("supervisor_id", "lineage_id", "mission_contract_digest"):
        if report.get(field) != state.get(field):
            raise ValueError(f"multi_generation_{field}_mismatch")
    code = _decision_code(state, report)
    target_status = (
        ACTIVE
        if code == CONTINUE
        else HANDOVER
        if code in {HANDOVER_HUMAN, HANDOVER_AUTHORITY}
        else HOLD
        if code in {HOLD_OBSERVATION_DEBT, HOLD_RECOVERY}
        else STOPPED
    )
    decision = {
        "version": DECISION_VERSION,
        "supervisor_id": state["supervisor_id"],
        "generation_index": report["generation_index"],
        "report_digest": report["supervised_generation_report_digest"],
        "policy_digest": state["policy_digest"],
        "decision": code,
        "target_status": target_status,
        "next_generation_authorized": code == CONTINUE,
        "automatic_continuation": code == CONTINUE,
        "execution_granted": False,
        "host_license_granted": False,
        "memory_overwrite": False,
        "decided_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "generation_supervision_decision_digest": "",
    }
    decision["generation_supervision_decision_digest"] = decision_digest(decision)
    return decision


def validate_generation_supervision_decision(
    decision: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if decision.get("version") != DECISION_VERSION:
            errors.append("generation_supervision_decision_version_invalid")
        if decision.get("generation_supervision_decision_digest") != decision_digest(
            decision
        ):
            errors.append("generation_supervision_decision_digest_invalid")
        require_string(decision.get("supervisor_id"), "supervisor_id")
        require_int(decision.get("generation_index"), "generation_index", minimum=1)
        require_string(decision.get("report_digest"), "report_digest")
        require_string(decision.get("policy_digest"), "policy_digest")
        code = decision.get("decision")
        if code not in DECISIONS:
            errors.append("generation_supervision_decision_code_invalid")
        expected_status = (
            ACTIVE
            if code == CONTINUE
            else HANDOVER
            if code in {HANDOVER_HUMAN, HANDOVER_AUTHORITY}
            else HOLD
            if code in {HOLD_OBSERVATION_DEBT, HOLD_RECOVERY}
            else STOPPED
        )
        if decision.get("target_status") != expected_status:
            errors.append("generation_supervision_target_status_invalid")
        expected_continue = code == CONTINUE
        if decision.get("next_generation_authorized") is not expected_continue:
            errors.append("generation_supervision_authorization_invalid")
        if decision.get("automatic_continuation") is not expected_continue:
            errors.append("generation_supervision_continuation_invalid")
        for field, expected in {
            "execution_granted": False,
            "host_license_granted": False,
            "memory_overwrite": False,
        }.items():
            if decision.get(field) != expected:
                errors.append(f"generation_supervision_{field}_invalid")
        if dict(decision.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("generation_supervision_authority_invalid")
        if dict(decision.get("boundary", {})) != BOUNDARY:
            errors.append("generation_supervision_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_multi_generation_event(
    *,
    state: Mapping[str, Any],
    report: Mapping[str, Any],
    decision: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    if report.get("supervised_generation_report_digest") != decision.get(
        "report_digest"
    ):
        raise ValueError("multi_generation_event_report_decision_mismatch")
    event = {
        "version": EVENT_VERSION,
        "supervisor_id": state["supervisor_id"],
        "event_index": int(state["event_index"]) + 1,
        "predecessor_state_digest": state[
            "multi_generation_supervisor_state_digest"
        ],
        "report": deepcopy(dict(report)),
        "decision": deepcopy(dict(decision)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "multi_generation_supervisor_event_digest": "",
    }
    event["multi_generation_supervisor_event_digest"] = event_digest(event)
    return event


def apply_multi_generation_event(
    state: Mapping[str, Any], event: Mapping[str, Any]
) -> dict[str, Any]:
    state_errors = validate_multi_generation_state(state)
    if state_errors:
        raise ValueError("multi_generation_state_invalid:" + ";".join(state_errors))
    event_id = str(event.get("multi_generation_supervisor_event_digest", ""))
    if event_id in set(state.get("processed_event_digests", [])):
        return {"status": "REPLAYED", "state": deepcopy(dict(state)), "errors": []}
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("multi_generation_event_version_invalid")
    if event_id != event_digest(event):
        errors.append("multi_generation_event_digest_invalid")
    if event.get("supervisor_id") != state.get("supervisor_id"):
        errors.append("multi_generation_event_supervisor_mismatch")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("multi_generation_event_index_invalid")
    if event.get("predecessor_state_digest") != state.get(
        "multi_generation_supervisor_state_digest"
    ):
        errors.append("multi_generation_event_predecessor_invalid")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("multi_generation_event_time_regression")
    report = dict(event.get("report", {}))
    decision = dict(event.get("decision", {}))
    errors.extend(validate_supervised_generation_report(report))
    errors.extend(validate_generation_supervision_decision(decision))
    if report.get("supervised_generation_report_digest") != decision.get(
        "report_digest"
    ):
        errors.append("multi_generation_event_receipt_binding_invalid")
    if errors:
        return {"status": "REJECTED", "state": deepcopy(dict(state)), "errors": errors}
    try:
        expected = build_generation_supervision_decision(
            state=state, report=report, now_ms=int(decision["decided_at_ms"])
        )
    except (TypeError, ValueError) as exc:
        return {
            "status": "REJECTED",
            "state": deepcopy(dict(state)),
            "errors": [str(exc)],
        }
    if expected.get("generation_supervision_decision_digest") != decision.get(
        "generation_supervision_decision_digest"
    ):
        return {
            "status": "REJECTED",
            "state": deepcopy(dict(state)),
            "errors": ["multi_generation_decision_not_canonical"],
        }
    next_state = deepcopy(dict(state))
    next_state["completed_generations"] = int(report["generation_index"])
    next_state["current_cycle_index"] = int(report["next_cycle_index"])
    next_state["last_generation_report_digest"] = report[
        "supervised_generation_report_digest"
    ]
    next_state["last_v05_generation_receipt_digest"] = report[
        "generational_cycle_receipt_digest"
    ]
    next_state["status"] = decision["target_status"]
    next_state["terminal_reason"] = (
        "" if decision["decision"] == CONTINUE else decision["decision"]
    )
    next_state["next_generation_authorized"] = decision[
        "next_generation_authorized"
    ]
    next_state["event_index"] = int(event["event_index"])
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["generation_history"] = list(next_state["generation_history"]) + [
        {
            "generation_index": report["generation_index"],
            "source_cycle_index": report["source_cycle_index"],
            "next_cycle_index": report["next_cycle_index"],
            "report_digest": report["supervised_generation_report_digest"],
            "v05_generation_receipt_digest": report[
                "generational_cycle_receipt_digest"
            ],
            "decision": decision["decision"],
            "decision_digest": decision[
                "generation_supervision_decision_digest"
            ],
            "event_digest": event_id,
        }
    ]
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["multi_generation_supervisor_state_digest"] = ""
    next_state["multi_generation_supervisor_state_digest"] = state_digest(next_state)
    next_errors = validate_multi_generation_state(next_state)
    if next_errors:
        raise ValueError("multi_generation_next_state_invalid:" + ";".join(next_errors))
    return {"status": "APPLIED", "state": next_state, "errors": []}
