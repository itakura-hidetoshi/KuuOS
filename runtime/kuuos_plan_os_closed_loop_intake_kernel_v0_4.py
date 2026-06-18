from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_learn_os_lineage_kernel_v0_2 import (
    validate_completion_receipt as validate_learn_completion_receipt,
    validate_handoff_receipt as validate_learn_handoff_receipt,
)
from runtime.kuuos_plan_os_closed_loop_intake_types_v0_4 import (
    BIND_RECEIPT_VERSION,
    INTAKE_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS,
    REQUIRED_BOUNDARY,
    bind_receipt_digest,
    copy_boundary,
    copy_non_authority,
    intake_receipt_digest,
    nonnegative_number,
    require_int,
    require_string,
    unit_number,
)
from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
    COMPILER_RECEIPT_VERSION,
    next_cycle_compiler_receipt_digest,
)
from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
    ALLOWED_CANDIDATES_BY_LEARNING_ROUTE,
    build_initial_replan_state,
    validate_replan_state,
)
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state


def _require_equal(
    packet: Mapping[str, Any], field: str, expected: Any, prefix: str
) -> None:
    if packet.get(field) != expected:
        raise ValueError(f"{prefix}_{field}_mismatch")


def validate_closed_loop_sources(
    *,
    current_plan_state: Mapping[str, Any],
    next_cycle_compiler_receipt: Mapping[str, Any],
    committed_learn_state: Mapping[str, Any],
    learn_lineage_handoff_receipt: Mapping[str, Any],
    learn_lineage_completion_receipt: Mapping[str, Any],
    current_cycle_index: int,
) -> None:
    plan_errors = validate_plan_state(current_plan_state)
    learn_errors = validate_learn_state(committed_learn_state)
    handoff_errors = validate_learn_handoff_receipt(
        learn_lineage_handoff_receipt
    )
    completion_errors = validate_learn_completion_receipt(
        learn_lineage_completion_receipt
    )
    if plan_errors:
        raise ValueError("closed_loop_current_plan_invalid:" + ";".join(plan_errors))
    if learn_errors:
        raise ValueError("closed_loop_learn_state_invalid:" + ";".join(learn_errors))
    if handoff_errors:
        raise ValueError("closed_loop_learn_handoff_invalid:" + ";".join(handoff_errors))
    if completion_errors:
        raise ValueError(
            "closed_loop_learn_completion_invalid:" + ";".join(completion_errors)
        )
    if current_plan_state.get("current_phase") != "commit":
        raise ValueError("closed_loop_current_plan_not_committed")
    if committed_learn_state.get("current_phase") != "commit":
        raise ValueError("closed_loop_learn_state_not_committed")
    if committed_learn_state.get("learning_recorded") is not True:
        raise ValueError("closed_loop_learning_not_recorded")
    if committed_learn_state.get("replan_required") is not True:
        raise ValueError("closed_loop_replan_debt_missing")

    if next_cycle_compiler_receipt.get("version") != COMPILER_RECEIPT_VERSION:
        raise ValueError("closed_loop_compiler_receipt_version_invalid")
    if next_cycle_compiler_receipt.get(
        "next_cycle_compiler_receipt_digest"
    ) != next_cycle_compiler_receipt_digest(next_cycle_compiler_receipt):
        raise ValueError("closed_loop_compiler_receipt_digest_invalid")

    for field, expected in {
        "compiled_plan_id": current_plan_state.get("plan_id"),
        "compiled_plan_state_digest": current_plan_state.get("plan_state_digest"),
        "compiled_plan_basis_digest": current_plan_state.get("plan_basis_digest"),
        "compiled_plan_route": current_plan_state.get("route"),
        "lineage_id": current_plan_state.get("lineage_id"),
        "mission_contract_digest": current_plan_state.get("mission_contract_digest"),
        "plan_committed": True,
        "plan_not_execution": True,
        "host_license_granted": False,
        "memory_overwrite": False,
    }.items():
        _require_equal(
            next_cycle_compiler_receipt,
            field,
            expected,
            "closed_loop_compiler_receipt",
        )

    _require_equal(
        learn_lineage_completion_receipt,
        "learn_lineage_handoff_receipt_digest",
        learn_lineage_handoff_receipt.get(
            "learn_lineage_handoff_receipt_digest"
        ),
        "closed_loop_learn_completion",
    )
    _require_equal(
        learn_lineage_handoff_receipt,
        "next_cycle_compiler_receipt_digest",
        next_cycle_compiler_receipt.get("next_cycle_compiler_receipt_digest"),
        "closed_loop_learn_handoff",
    )
    _require_equal(
        learn_lineage_completion_receipt,
        "next_cycle_compiler_receipt_digest",
        next_cycle_compiler_receipt.get("next_cycle_compiler_receipt_digest"),
        "closed_loop_learn_completion",
    )

    for field, expected in {
        "committed_learn_state_digest": committed_learn_state.get(
            "learn_state_digest"
        ),
        "learning_delta_digest": committed_learn_state.get(
            "learning_delta_digest"
        ),
        "middle_way_report_digest": committed_learn_state.get(
            "middle_way_report_digest"
        ),
        "learning_route": committed_learn_state.get("route"),
        "source_verification_evidence_digest": committed_learn_state.get(
            "source_verification_evidence_digest"
        ),
        "verification_criterion_digest": committed_learn_state.get(
            "verification_criterion_digest"
        ),
        "source_counterevidence_digest": committed_learn_state.get(
            "source_counterevidence_digest"
        ),
        "learning_recorded": True,
        "learning_debt_discharged": True,
        "replan_required": True,
        "replan_handoff_ready": True,
        "future_only": True,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_records_unchanged": True,
        "memory_overwrite": False,
        "activation_requires_planos_replan": True,
        "learn_delta_not_replan_activation": True,
        "replan_activation": False,
        "plan_activation": False,
        "execution_permission": False,
        "host_license_granted": False,
    }.items():
        _require_equal(
            learn_lineage_completion_receipt,
            field,
            expected,
            "closed_loop_learn_completion",
        )

    lineage_id = current_plan_state.get("lineage_id")
    mission_digest = current_plan_state.get("mission_contract_digest")
    for source, name in (
        (learn_lineage_handoff_receipt, "learn_handoff"),
        (committed_learn_state, "learn_state"),
    ):
        _require_equal(source, "lineage_id", lineage_id, f"closed_loop_{name}")
        _require_equal(
            source,
            "mission_contract_digest",
            mission_digest,
            f"closed_loop_{name}",
        )

    cycle = require_int(current_cycle_index, "current_cycle_index")
    compiler_cycle = require_int(
        next_cycle_compiler_receipt.get("mission_cycle_cycle_index"),
        "compiler_cycle_index",
    )
    learn_cycle = require_int(
        learn_lineage_handoff_receipt.get("mission_cycle_cycle_index"),
        "learn_cycle_index",
    )
    if cycle != compiler_cycle or cycle != learn_cycle:
        raise ValueError("closed_loop_cycle_mismatch")

    route = require_string(committed_learn_state.get("route"), "learning_route")
    expected_allowlist = ALLOWED_CANDIDATES_BY_LEARNING_ROUTE.get(route)
    if expected_allowlist is None:
        raise ValueError("closed_loop_learning_route_invalid")
    supplied_allowlist = set(
        learn_lineage_completion_receipt.get(
            "planos_candidate_type_allowlist", []
        )
    )
    if supplied_allowlist != set(expected_allowlist):
        raise ValueError("closed_loop_planos_candidate_allowlist_mismatch")


def build_closed_loop_intake_receipt(
    *,
    current_plan_state: Mapping[str, Any],
    next_cycle_compiler_receipt: Mapping[str, Any],
    committed_learn_state: Mapping[str, Any],
    learn_lineage_handoff_receipt: Mapping[str, Any],
    learn_lineage_completion_receipt: Mapping[str, Any],
    current_cycle_index: int,
    plan_budget: float,
    maximum_candidate_risk: float,
    base_switch_threshold: float,
    mission_cycle_state_digest: str,
    replan_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    validate_closed_loop_sources(
        current_plan_state=current_plan_state,
        next_cycle_compiler_receipt=next_cycle_compiler_receipt,
        committed_learn_state=committed_learn_state,
        learn_lineage_handoff_receipt=learn_lineage_handoff_receipt,
        learn_lineage_completion_receipt=learn_lineage_completion_receipt,
        current_cycle_index=current_cycle_index,
    )
    cycle = require_int(current_cycle_index, "current_cycle_index")
    packet = {
        "version": INTAKE_RECEIPT_VERSION,
        "lineage_id": current_plan_state["lineage_id"],
        "mission_contract_digest": current_plan_state[
            "mission_contract_digest"
        ],
        "current_plan_id": current_plan_state["plan_id"],
        "current_plan_state_digest": current_plan_state[
            "plan_state_digest"
        ],
        "current_committed_plan_digest": current_plan_state[
            "latest_committed_plan_digest"
        ],
        "current_plan_basis_digest": current_plan_state["plan_basis_digest"],
        "current_plan_route": current_plan_state["route"],
        "next_cycle_compiler_receipt_digest": next_cycle_compiler_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "source_replan_phase_receipt_digest": next_cycle_compiler_receipt[
            "replan_phase_receipt_digest"
        ],
        "source_qi_condition_packet_digest": next_cycle_compiler_receipt[
            "qi_condition_packet_digest"
        ],
        "source_decision_receipt_digest": next_cycle_compiler_receipt[
            "decision_receipt_digest"
        ],
        "source_selected_candidate_digest": next_cycle_compiler_receipt[
            "selected_candidate_digest"
        ],
        "learn_lineage_handoff_receipt_digest": learn_lineage_handoff_receipt[
            "learn_lineage_handoff_receipt_digest"
        ],
        "learn_lineage_completion_receipt_digest": learn_lineage_completion_receipt[
            "learn_lineage_completion_receipt_digest"
        ],
        "verify_lineage_completion_receipt_digest": learn_lineage_completion_receipt[
            "verify_lineage_completion_receipt_digest"
        ],
        "observe_lineage_completion_receipt_digest": learn_lineage_completion_receipt[
            "observe_lineage_completion_receipt_digest"
        ],
        "act_lineage_completion_receipt_digest": learn_lineage_completion_receipt[
            "act_lineage_completion_receipt_digest"
        ],
        "committed_act_state_digest": learn_lineage_completion_receipt[
            "committed_act_state_digest"
        ],
        "committed_observe_state_digest": learn_lineage_completion_receipt[
            "committed_observe_state_digest"
        ],
        "committed_verify_state_digest": learn_lineage_completion_receipt[
            "committed_verify_state_digest"
        ],
        "committed_learn_state_digest": committed_learn_state[
            "learn_state_digest"
        ],
        "source_learning_route": committed_learn_state["route"],
        "source_learning_delta_digest": committed_learn_state[
            "learning_delta_digest"
        ],
        "source_middle_way_report_digest": committed_learn_state[
            "middle_way_report_digest"
        ],
        "source_verification_evidence_digest": committed_learn_state[
            "source_verification_evidence_digest"
        ],
        "source_counterevidence_digest": committed_learn_state[
            "source_counterevidence_digest"
        ],
        "planos_replan_input_digest": learn_lineage_completion_receipt[
            "planos_replan_input_digest"
        ],
        "planos_candidate_type_allowlist": list(
            learn_lineage_completion_receipt[
                "planos_candidate_type_allowlist"
            ]
        ),
        "current_cycle_index": cycle,
        "active_from_cycle": cycle + 1,
        "plan_budget": nonnegative_number(plan_budget, "plan_budget"),
        "maximum_candidate_risk": unit_number(
            maximum_candidate_risk, "maximum_candidate_risk"
        ),
        "base_switch_threshold": unit_number(
            base_switch_threshold, "base_switch_threshold"
        ),
        "mission_cycle_phase": "replan",
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "replan_phase_event_digest": require_string(
            replan_phase_event_digest, "replan_phase_event_digest"
        ),
        "intake_ready": True,
        "planos_v02_bind_only": True,
        "history_phase_required_after_bind": True,
        "future_only": True,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "execution_permission": False,
        "host_license_granted": False,
        "single_use": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "closed_loop_intake_receipt_digest": "",
    }
    packet["closed_loop_intake_receipt_digest"] = intake_receipt_digest(
        packet
    )
    return packet


def validate_intake_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != INTAKE_RECEIPT_VERSION:
            errors.append("closed_loop_intake_version_invalid")
        if receipt.get("closed_loop_intake_receipt_digest") != intake_receipt_digest(
            receipt
        ):
            errors.append("closed_loop_intake_digest_invalid")
        for field in (
            "lineage_id",
            "mission_contract_digest",
            "current_plan_id",
            "current_plan_state_digest",
            "current_committed_plan_digest",
            "current_plan_basis_digest",
            "current_plan_route",
            "next_cycle_compiler_receipt_digest",
            "source_replan_phase_receipt_digest",
            "source_qi_condition_packet_digest",
            "source_decision_receipt_digest",
            "source_selected_candidate_digest",
            "learn_lineage_handoff_receipt_digest",
            "learn_lineage_completion_receipt_digest",
            "verify_lineage_completion_receipt_digest",
            "observe_lineage_completion_receipt_digest",
            "act_lineage_completion_receipt_digest",
            "committed_act_state_digest",
            "committed_observe_state_digest",
            "committed_verify_state_digest",
            "committed_learn_state_digest",
            "source_learning_route",
            "source_learning_delta_digest",
            "source_middle_way_report_digest",
            "source_verification_evidence_digest",
            "source_counterevidence_digest",
            "planos_replan_input_digest",
            "mission_cycle_state_digest",
            "replan_phase_event_digest",
        ):
            require_string(receipt.get(field), field)
        cycle = require_int(receipt.get("current_cycle_index"), "current_cycle_index")
        if receipt.get("active_from_cycle") != cycle + 1:
            errors.append("closed_loop_intake_active_cycle_invalid")
        nonnegative_number(receipt.get("plan_budget"), "plan_budget")
        unit_number(receipt.get("maximum_candidate_risk"), "maximum_candidate_risk")
        unit_number(receipt.get("base_switch_threshold"), "base_switch_threshold")
        if receipt.get("mission_cycle_phase") != "replan":
            errors.append("closed_loop_intake_phase_invalid")
        if not list(receipt.get("planos_candidate_type_allowlist", [])):
            errors.append("closed_loop_intake_candidate_allowlist_missing")
        for field, expected in {
            "intake_ready": True,
            "planos_v02_bind_only": True,
            "history_phase_required_after_bind": True,
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
            "execution_permission": False,
            "host_license_granted": False,
            "single_use": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"closed_loop_intake_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("closed_loop_intake_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("closed_loop_intake_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_bound_replan_state(
    *,
    intake_receipt: Mapping[str, Any],
    replan_id: str,
    current_plan_state: Mapping[str, Any],
    committed_learn_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_intake_receipt(intake_receipt)
    if errors:
        raise ValueError("closed_loop_intake_invalid:" + ";".join(errors))
    for field, expected in {
        "current_plan_state_digest": current_plan_state.get("plan_state_digest"),
        "committed_learn_state_digest": committed_learn_state.get(
            "learn_state_digest"
        ),
        "source_learning_delta_digest": committed_learn_state.get(
            "learning_delta_digest"
        ),
        "source_middle_way_report_digest": committed_learn_state.get(
            "middle_way_report_digest"
        ),
        "source_learning_route": committed_learn_state.get("route"),
        "lineage_id": current_plan_state.get("lineage_id"),
        "mission_contract_digest": current_plan_state.get(
            "mission_contract_digest"
        ),
    }.items():
        _require_equal(
            intake_receipt,
            field,
            expected,
            "closed_loop_intake",
        )
    state = build_initial_replan_state(
        replan_id=require_string(replan_id, "replan_id"),
        current_plan_state=current_plan_state,
        learn_state=committed_learn_state,
        current_cycle_index=require_int(
            intake_receipt.get("current_cycle_index"),
            "current_cycle_index",
        ),
        plan_budget=nonnegative_number(
            intake_receipt.get("plan_budget"), "plan_budget"
        ),
        maximum_candidate_risk=unit_number(
            intake_receipt.get("maximum_candidate_risk"),
            "maximum_candidate_risk",
        ),
        base_switch_threshold=unit_number(
            intake_receipt.get("base_switch_threshold"),
            "base_switch_threshold",
        ),
        now_ms=require_int(now_ms, "now_ms"),
    )
    state_errors = validate_replan_state(state)
    if state_errors:
        raise ValueError("closed_loop_bound_replan_invalid:" + ";".join(state_errors))
    for field, expected in {
        "source_plan_state_digest": intake_receipt.get(
            "current_plan_state_digest"
        ),
        "source_committed_plan_digest": intake_receipt.get(
            "current_committed_plan_digest"
        ),
        "source_plan_basis_digest": intake_receipt.get(
            "current_plan_basis_digest"
        ),
        "source_learn_state_digest": intake_receipt.get(
            "committed_learn_state_digest"
        ),
        "source_learning_route": intake_receipt.get(
            "source_learning_route"
        ),
        "source_learning_delta_digest": intake_receipt.get(
            "source_learning_delta_digest"
        ),
        "source_middle_way_report_digest": intake_receipt.get(
            "source_middle_way_report_digest"
        ),
        "current_cycle_index": intake_receipt.get("current_cycle_index"),
        "active_from_cycle": intake_receipt.get("active_from_cycle"),
        "current_phase": "bind",
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "host_license_granted": False,
    }.items():
        _require_equal(state, field, expected, "closed_loop_bound_replan")
    return state


def build_closed_loop_bind_receipt(
    *,
    intake_receipt: Mapping[str, Any],
    bound_replan_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    intake_errors = validate_intake_receipt(intake_receipt)
    state_errors = validate_replan_state(bound_replan_state)
    if intake_errors:
        raise ValueError("closed_loop_intake_invalid:" + ";".join(intake_errors))
    if state_errors:
        raise ValueError("closed_loop_replan_state_invalid:" + ";".join(state_errors))
    if bound_replan_state.get("current_phase") != "bind":
        raise ValueError("closed_loop_replan_bind_phase_required")
    if bound_replan_state.get("event_index") != 0:
        raise ValueError("closed_loop_replan_bind_must_be_pristine")
    for field, expected in {
        "source_plan_state_digest": intake_receipt.get(
            "current_plan_state_digest"
        ),
        "source_learn_state_digest": intake_receipt.get(
            "committed_learn_state_digest"
        ),
        "source_learning_delta_digest": intake_receipt.get(
            "source_learning_delta_digest"
        ),
        "source_middle_way_report_digest": intake_receipt.get(
            "source_middle_way_report_digest"
        ),
        "current_cycle_index": intake_receipt.get("current_cycle_index"),
        "active_from_cycle": intake_receipt.get("active_from_cycle"),
    }.items():
        _require_equal(
            bound_replan_state,
            field,
            expected,
            "closed_loop_replan_state",
        )
    packet = {
        "version": BIND_RECEIPT_VERSION,
        "closed_loop_intake_receipt_digest": intake_receipt[
            "closed_loop_intake_receipt_digest"
        ],
        "lineage_id": intake_receipt["lineage_id"],
        "mission_contract_digest": intake_receipt[
            "mission_contract_digest"
        ],
        "planos_replan_input_digest": intake_receipt[
            "planos_replan_input_digest"
        ],
        "next_cycle_compiler_receipt_digest": intake_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "learn_lineage_completion_receipt_digest": intake_receipt[
            "learn_lineage_completion_receipt_digest"
        ],
        "replan_id": bound_replan_state["replan_id"],
        "replan_state_digest": bound_replan_state["replan_state_digest"],
        "source_plan_state_digest": bound_replan_state[
            "source_plan_state_digest"
        ],
        "source_learn_state_digest": bound_replan_state[
            "source_learn_state_digest"
        ],
        "source_learning_delta_digest": bound_replan_state[
            "source_learning_delta_digest"
        ],
        "source_middle_way_report_digest": bound_replan_state[
            "source_middle_way_report_digest"
        ],
        "source_learning_route": bound_replan_state[
            "source_learning_route"
        ],
        "current_cycle_index": bound_replan_state[
            "current_cycle_index"
        ],
        "active_from_cycle": bound_replan_state["active_from_cycle"],
        "current_phase": "bind",
        "next_phase": "history",
        "history_phase_required": True,
        "bind_committed": True,
        "replan_active_now": False,
        "plan_active_now": False,
        "execution_permission": False,
        "host_license_granted": False,
        "current_cycle_unchanged": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "closed_loop_bind_receipt_digest": "",
    }
    packet["closed_loop_bind_receipt_digest"] = bind_receipt_digest(packet)
    return packet


def validate_bind_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != BIND_RECEIPT_VERSION:
            errors.append("closed_loop_bind_version_invalid")
        if receipt.get("closed_loop_bind_receipt_digest") != bind_receipt_digest(
            receipt
        ):
            errors.append("closed_loop_bind_digest_invalid")
        for field in (
            "closed_loop_intake_receipt_digest",
            "lineage_id",
            "mission_contract_digest",
            "planos_replan_input_digest",
            "next_cycle_compiler_receipt_digest",
            "learn_lineage_completion_receipt_digest",
            "replan_id",
            "replan_state_digest",
            "source_plan_state_digest",
            "source_learn_state_digest",
            "source_learning_delta_digest",
            "source_middle_way_report_digest",
            "source_learning_route",
        ):
            require_string(receipt.get(field), field)
        cycle = require_int(receipt.get("current_cycle_index"), "current_cycle_index")
        if receipt.get("active_from_cycle") != cycle + 1:
            errors.append("closed_loop_bind_active_cycle_invalid")
        if receipt.get("current_phase") != "bind":
            errors.append("closed_loop_bind_phase_invalid")
        if receipt.get("next_phase") != "history":
            errors.append("closed_loop_bind_next_phase_invalid")
        for field, expected in {
            "history_phase_required": True,
            "bind_committed": True,
            "replan_active_now": False,
            "plan_active_now": False,
            "execution_permission": False,
            "host_license_granted": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"closed_loop_bind_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("closed_loop_bind_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("closed_loop_bind_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
