from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_act_os_lineage_types_v0_2 import handoff_receipt_digest
from runtime.kuuos_plan_os_closed_loop_intake_kernel_v0_4 import validate_bind_receipt
from runtime.kuuos_plan_os_generational_driver_types_v0_5 import (
    BOUNDARY,
    NON_AUTHORITY,
    RECEIPT_VERSION,
    copy_boundary,
    copy_non_authority,
    generational_receipt_digest,
    require_int,
    require_string,
)
from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
    next_cycle_compiler_receipt_digest,
)
from runtime.kuuos_plan_os_replan_kernel_v0_2 import validate_replan_state
from runtime.kuuos_plan_os_replan_types_v0_2 import replan_phase_receipt_digest
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state

EXPECTED_REPLAN_PHASES = [
    "history",
    "qi_condition",
    "generate",
    "constrain",
    "deliberate",
    "synthesize",
    "commit_next",
]


def _equal(packet: Mapping[str, Any], field: str, expected: Any, prefix: str) -> None:
    if packet.get(field) != expected:
        raise ValueError(f"{prefix}_{field}_mismatch")


def validate_generation_sources(
    *,
    bind_receipt: Mapping[str, Any],
    source_plan_state: Mapping[str, Any],
    committed_replan_state: Mapping[str, Any],
    replan_phase_receipt: Mapping[str, Any],
    compiled_plan_state: Mapping[str, Any],
    compiler_receipt: Mapping[str, Any],
    act_handoff_receipt: Mapping[str, Any],
) -> None:
    bind_errors = validate_bind_receipt(bind_receipt)
    if bind_errors:
        raise ValueError("generational_bind_invalid:" + ";".join(bind_errors))
    source_errors = validate_plan_state(source_plan_state)
    if source_errors:
        raise ValueError("generational_source_plan_invalid:" + ";".join(source_errors))
    compiled_errors = validate_plan_state(compiled_plan_state)
    if compiled_errors:
        raise ValueError("generational_compiled_plan_invalid:" + ";".join(compiled_errors))
    replan_errors = validate_replan_state(committed_replan_state)
    if replan_errors:
        raise ValueError("generational_replan_invalid:" + ";".join(replan_errors))
    if source_plan_state.get("current_phase") != "commit":
        raise ValueError("generational_source_plan_not_committed")
    if compiled_plan_state.get("current_phase") != "commit":
        raise ValueError("generational_compiled_plan_not_committed")
    if committed_replan_state.get("current_phase") != "commit_next":
        raise ValueError("generational_replan_not_committed")
    if committed_replan_state.get("event_index") != len(EXPECTED_REPLAN_PHASES):
        raise ValueError("generational_replan_event_count_invalid")
    actual_phases = [item.get("target_phase") for item in committed_replan_state.get("event_history", [])]
    if actual_phases != EXPECTED_REPLAN_PHASES:
        raise ValueError("generational_replan_phase_order_invalid")
    if committed_replan_state.get("committed_records") != 1:
        raise ValueError("generational_replan_commit_count_invalid")
    if committed_replan_state.get("next_plan_basis_committed") is not True:
        raise ValueError("generational_next_basis_not_committed")

    for field, expected in {
        "replan_id": bind_receipt.get("replan_id"),
        "source_plan_state_digest": bind_receipt.get("source_plan_state_digest"),
        "source_learn_state_digest": bind_receipt.get("source_learn_state_digest"),
        "source_learning_delta_digest": bind_receipt.get("source_learning_delta_digest"),
        "source_middle_way_report_digest": bind_receipt.get("source_middle_way_report_digest"),
        "current_cycle_index": bind_receipt.get("current_cycle_index"),
        "active_from_cycle": bind_receipt.get("active_from_cycle"),
    }.items():
        _equal(committed_replan_state, field, expected, "generational_replan")
    _equal(source_plan_state, "plan_state_digest", bind_receipt.get("source_plan_state_digest"), "generational_source_plan")

    if replan_phase_receipt.get("replan_phase_receipt_digest") != replan_phase_receipt_digest(replan_phase_receipt):
        raise ValueError("generational_replan_phase_receipt_digest_invalid")
    for field, expected in {
        "replan_id": committed_replan_state.get("replan_id"),
        "replan_state_digest": committed_replan_state.get("replan_state_digest"),
        "next_plan_basis_digest": committed_replan_state.get("next_plan_basis_digest"),
        "selected_candidate_digest": committed_replan_state.get("selected_candidate_digest"),
        "decision_receipt_digest": committed_replan_state.get("decision_receipt_digest"),
        "qi_condition_packet_digest": committed_replan_state.get("qi_condition_packet_digest"),
        "current_cycle_index": committed_replan_state.get("current_cycle_index"),
        "active_from_cycle": committed_replan_state.get("active_from_cycle"),
    }.items():
        _equal(replan_phase_receipt, field, expected, "generational_replan_receipt")

    if compiler_receipt.get("next_cycle_compiler_receipt_digest") != next_cycle_compiler_receipt_digest(compiler_receipt):
        raise ValueError("generational_compiler_receipt_digest_invalid")
    for field, expected in {
        "previous_plan_state_digest": source_plan_state.get("plan_state_digest"),
        "replan_state_digest": committed_replan_state.get("replan_state_digest"),
        "replan_phase_receipt_digest": replan_phase_receipt.get("replan_phase_receipt_digest"),
        "next_plan_basis_digest": committed_replan_state.get("next_plan_basis_digest"),
        "selected_candidate_digest": committed_replan_state.get("selected_candidate_digest"),
        "compiled_plan_id": compiled_plan_state.get("plan_id"),
        "compiled_plan_state_digest": compiled_plan_state.get("plan_state_digest"),
        "compiled_plan_basis_digest": compiled_plan_state.get("plan_basis_digest"),
        "mission_cycle_cycle_index": committed_replan_state.get("active_from_cycle"),
    }.items():
        _equal(compiler_receipt, field, expected, "generational_compiler")

    if act_handoff_receipt.get("act_lineage_handoff_receipt_digest") != handoff_receipt_digest(act_handoff_receipt):
        raise ValueError("generational_act_handoff_digest_invalid")
    for field, expected in {
        "compiled_plan_id": compiled_plan_state.get("plan_id"),
        "compiled_plan_state_digest": compiled_plan_state.get("plan_state_digest"),
        "next_cycle_compiler_receipt_digest": compiler_receipt.get("next_cycle_compiler_receipt_digest"),
        "mission_cycle_cycle_index": committed_replan_state.get("active_from_cycle"),
        "selected_candidate_digest": committed_replan_state.get("selected_candidate_digest"),
        "qi_condition_packet_digest": committed_replan_state.get("qi_condition_packet_digest"),
        "execution_granted": False,
        "host_license_granted": False,
    }.items():
        _equal(act_handoff_receipt, field, expected, "generational_act_handoff")


def build_generational_cycle_receipt(
    *,
    bind_receipt: Mapping[str, Any],
    source_plan_state: Mapping[str, Any],
    committed_replan_state: Mapping[str, Any],
    replan_phase_receipt: Mapping[str, Any],
    compiled_plan_state: Mapping[str, Any],
    compiler_receipt: Mapping[str, Any],
    plan_activation_receipt: Mapping[str, Any],
    act_handoff_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    validate_generation_sources(
        bind_receipt=bind_receipt,
        source_plan_state=source_plan_state,
        committed_replan_state=committed_replan_state,
        replan_phase_receipt=replan_phase_receipt,
        compiled_plan_state=compiled_plan_state,
        compiler_receipt=compiler_receipt,
        act_handoff_receipt=act_handoff_receipt,
    )
    source_cycle = require_int(committed_replan_state.get("current_cycle_index"), "source_cycle_index")
    next_cycle = require_int(committed_replan_state.get("active_from_cycle"), "next_cycle_index")
    if next_cycle != source_cycle + 1:
        raise ValueError("generational_successor_cycle_invalid")
    packet = {
        "version": RECEIPT_VERSION,
        "lineage_id": require_string(committed_replan_state.get("lineage_id"), "lineage_id"),
        "mission_contract_digest": require_string(committed_replan_state.get("mission_contract_digest"), "mission_contract_digest"),
        "source_bind_receipt_digest": bind_receipt["closed_loop_bind_receipt_digest"],
        "source_plan_id": source_plan_state["plan_id"],
        "source_plan_state_digest": source_plan_state["plan_state_digest"],
        "source_plan_basis_digest": source_plan_state["plan_basis_digest"],
        "source_learn_state_digest": committed_replan_state["source_learn_state_digest"],
        "source_learning_delta_digest": committed_replan_state["source_learning_delta_digest"],
        "planos_replan_input_digest": bind_receipt["planos_replan_input_digest"],
        "replan_id": committed_replan_state["replan_id"],
        "committed_replan_state_digest": committed_replan_state["replan_state_digest"],
        "replan_phase_receipt_digest": replan_phase_receipt["replan_phase_receipt_digest"],
        "history_packet_digest": committed_replan_state["history_packet_digest"],
        "qi_condition_packet_digest": committed_replan_state["qi_condition_packet_digest"],
        "candidate_field_digest": committed_replan_state["candidate_field_digest"],
        "constraint_field_digest": committed_replan_state["constraint_field_digest"],
        "decision_receipt_digest": committed_replan_state["decision_receipt_digest"],
        "selected_candidate_id": committed_replan_state["selected_candidate_id"],
        "selected_candidate_digest": committed_replan_state["selected_candidate_digest"],
        "synthesis_packet_digest": committed_replan_state["synthesis_packet_digest"],
        "next_plan_basis_digest": committed_replan_state["next_plan_basis_digest"],
        "replan_route": committed_replan_state["route"],
        "replan_event_count": committed_replan_state["event_index"],
        "replan_phase_sequence": list(EXPECTED_REPLAN_PHASES),
        "source_cycle_index": source_cycle,
        "next_cycle_index": next_cycle,
        "compiled_plan_id": compiled_plan_state["plan_id"],
        "compiled_plan_state_digest": compiled_plan_state["plan_state_digest"],
        "compiled_plan_basis_digest": compiled_plan_state["plan_basis_digest"],
        "compiler_receipt_digest": compiler_receipt["next_cycle_compiler_receipt_digest"],
        "plan_activation_receipt_digest": require_string(plan_activation_receipt.get("plan_phase_activation_receipt_digest"), "plan_activation_receipt_digest"),
        "act_handoff_receipt_digest": act_handoff_receipt["act_lineage_handoff_receipt_digest"],
        "act_selected_step_id": act_handoff_receipt["selected_step_id"],
        "strict_phase_order_completed": True,
        "successor_cycle_compiled": True,
        "act_handoff_ready": True,
        "execution_granted": False,
        "host_license_granted": False,
        "current_cycle_unchanged_during_replan": True,
        "past_plan_unchanged": True,
        "memory_overwrite": False,
        "single_use": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "generational_cycle_receipt_digest": "",
    }
    packet["generational_cycle_receipt_digest"] = generational_receipt_digest(packet)
    return packet


def validate_generational_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("generational_receipt_version_invalid")
        if receipt.get("generational_cycle_receipt_digest") != generational_receipt_digest(receipt):
            errors.append("generational_receipt_digest_invalid")
        for field in (
            "lineage_id", "mission_contract_digest", "source_bind_receipt_digest",
            "source_plan_id", "source_plan_state_digest", "source_plan_basis_digest",
            "source_learn_state_digest", "source_learning_delta_digest",
            "planos_replan_input_digest", "replan_id", "committed_replan_state_digest",
            "replan_phase_receipt_digest", "history_packet_digest",
            "qi_condition_packet_digest", "candidate_field_digest",
            "constraint_field_digest", "decision_receipt_digest",
            "selected_candidate_id", "selected_candidate_digest",
            "synthesis_packet_digest", "next_plan_basis_digest", "replan_route",
            "compiled_plan_id", "compiled_plan_state_digest", "compiled_plan_basis_digest",
            "compiler_receipt_digest", "plan_activation_receipt_digest",
            "act_handoff_receipt_digest", "act_selected_step_id",
        ):
            require_string(receipt.get(field), field)
        source_cycle = require_int(receipt.get("source_cycle_index"), "source_cycle_index")
        next_cycle = require_int(receipt.get("next_cycle_index"), "next_cycle_index")
        if next_cycle != source_cycle + 1:
            errors.append("generational_receipt_successor_cycle_invalid")
        if receipt.get("replan_event_count") != len(EXPECTED_REPLAN_PHASES):
            errors.append("generational_receipt_event_count_invalid")
        if list(receipt.get("replan_phase_sequence", [])) != EXPECTED_REPLAN_PHASES:
            errors.append("generational_receipt_phase_sequence_invalid")
        for field, expected in {
            "strict_phase_order_completed": True,
            "successor_cycle_compiled": True,
            "act_handoff_ready": True,
            "execution_granted": False,
            "host_license_granted": False,
            "current_cycle_unchanged_during_replan": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
            "single_use": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"generational_receipt_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("generational_receipt_authority_invalid")
        if dict(receipt.get("boundary", {})) != BOUNDARY:
            errors.append("generational_receipt_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
