from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_act_os_lineage_kernel_v0_2 import (
    validate_completion_receipt as validate_act_completion_receipt,
    validate_handoff_receipt as validate_act_handoff_receipt,
)
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_observe_os_types_v0_1 import (
    OBSERVE_PHASE_RECEIPT_VERSION,
    observe_phase_receipt_digest,
)
from runtime.kuuos_observe_os_lineage_types_v0_2 import (
    COMPLETION_RECEIPT_VERSION,
    HANDOFF_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS,
    REQUIRED_BOUNDARY,
    completion_receipt_digest,
    copy_boundary,
    copy_non_authority,
    handoff_receipt_digest,
    require_int,
    require_string,
)


def _require_equal(
    packet: Mapping[str, Any], field: str, expected: Any, prefix: str
) -> None:
    if packet.get(field) != expected:
        raise ValueError(f"{prefix}_{field}_mismatch")


def build_observe_lineage_handoff_receipt(
    *,
    committed_act_state: Mapping[str, Any],
    act_lineage_handoff_receipt: Mapping[str, Any],
    act_lineage_completion_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_cycle_index: int,
    mission_cycle_state_digest: str,
    observe_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    act_errors = validate_act_state(committed_act_state)
    handoff_errors = validate_act_handoff_receipt(act_lineage_handoff_receipt)
    completion_errors = validate_act_completion_receipt(act_lineage_completion_receipt)
    if act_errors:
        raise ValueError("observe_lineage_act_state_invalid:" + ";".join(act_errors))
    if handoff_errors:
        raise ValueError("observe_lineage_act_handoff_invalid:" + ";".join(handoff_errors))
    if completion_errors:
        raise ValueError(
            "observe_lineage_act_completion_invalid:" + ";".join(completion_errors)
        )
    if committed_act_state.get("current_phase") != "commit":
        raise ValueError("observe_lineage_act_state_not_committed")
    if committed_act_state.get("route") != "EFFECT_RECORDED":
        raise ValueError("observe_lineage_source_effect_missing")
    if committed_act_state.get("effect_recorded") is not True:
        raise ValueError("observe_lineage_effect_flag_missing")
    if committed_act_state.get("observation_required") is not True:
        raise ValueError("observe_lineage_observation_debt_missing")
    if committed_act_state.get("verification_required") is not True:
        raise ValueError("observe_lineage_verification_debt_missing")

    _require_equal(
        act_lineage_completion_receipt,
        "act_lineage_handoff_receipt_digest",
        act_lineage_handoff_receipt.get("act_lineage_handoff_receipt_digest"),
        "observe_lineage_completion",
    )
    for field, expected in {
        "committed_act_state_digest": committed_act_state.get("act_state_digest"),
        "selected_step_digest": committed_act_state.get("selected_step_digest"),
        "host_receipt_digest": committed_act_state.get("host_receipt_digest"),
        "host_invocation_digest": committed_act_state.get("host_invocation_digest"),
        "route": "EFFECT_RECORDED",
        "effect_recorded": True,
        "observation_required": True,
        "verification_required": True,
    }.items():
        _require_equal(
            act_lineage_completion_receipt,
            field,
            expected,
            "observe_lineage_completion",
        )

    if mission_cycle_phase != "observe":
        raise ValueError("observe_lineage_observe_phase_required")
    cycle = require_int(mission_cycle_cycle_index, "mission_cycle_cycle_index")
    expected_cycle = int(act_lineage_handoff_receipt.get("mission_cycle_cycle_index", -1))
    if cycle != expected_cycle:
        raise ValueError("observe_lineage_cycle_mismatch")

    packet = {
        "version": HANDOFF_RECEIPT_VERSION,
        "lineage_id": require_string(
            act_lineage_handoff_receipt.get("lineage_id"), "lineage_id"
        ),
        "mission_contract_digest": require_string(
            act_lineage_handoff_receipt.get("mission_contract_digest"),
            "mission_contract_digest",
        ),
        "act_lineage_handoff_receipt_digest": act_lineage_handoff_receipt[
            "act_lineage_handoff_receipt_digest"
        ],
        "act_lineage_completion_receipt_digest": act_lineage_completion_receipt[
            "act_lineage_completion_receipt_digest"
        ],
        "authorization_envelope_digest": act_lineage_completion_receipt[
            "authorization_envelope_digest"
        ],
        "next_cycle_compiler_receipt_digest": act_lineage_completion_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "replan_phase_receipt_digest": act_lineage_completion_receipt[
            "replan_phase_receipt_digest"
        ],
        "qi_condition_packet_digest": act_lineage_completion_receipt[
            "qi_condition_packet_digest"
        ],
        "decision_receipt_digest": act_lineage_completion_receipt[
            "decision_receipt_digest"
        ],
        "selected_candidate_digest": act_lineage_completion_receipt[
            "selected_candidate_digest"
        ],
        "selected_step_id": act_lineage_handoff_receipt["selected_step_id"],
        "selected_step_digest": act_lineage_completion_receipt[
            "selected_step_digest"
        ],
        "operation_id": act_lineage_handoff_receipt["operation_id"],
        "committed_act_state_digest": committed_act_state["act_state_digest"],
        "host_receipt_digest": committed_act_state["host_receipt_digest"],
        "host_invocation_digest": committed_act_state["host_invocation_digest"],
        "expected_observation_digest": act_lineage_handoff_receipt[
            "expected_observation_digest"
        ],
        "verification_criterion_digest": act_lineage_handoff_receipt[
            "verification_criterion_digest"
        ],
        "mission_cycle_phase": "observe",
        "mission_cycle_cycle_index": cycle,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "observe_phase_event_digest": require_string(
            observe_phase_event_digest, "observe_phase_event_digest"
        ),
        "source_effect_recorded": True,
        "observation_required": True,
        "observation_not_verification": True,
        "verification_required": True,
        "single_use": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "observe_lineage_handoff_receipt_digest": "",
    }
    packet["observe_lineage_handoff_receipt_digest"] = handoff_receipt_digest(packet)
    return packet


def validate_handoff_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != HANDOFF_RECEIPT_VERSION:
            errors.append("observe_lineage_handoff_version_invalid")
        if receipt.get("observe_lineage_handoff_receipt_digest") != handoff_receipt_digest(
            receipt
        ):
            errors.append("observe_lineage_handoff_digest_invalid")
        for field in (
            "lineage_id",
            "mission_contract_digest",
            "act_lineage_handoff_receipt_digest",
            "act_lineage_completion_receipt_digest",
            "authorization_envelope_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "selected_step_id",
            "selected_step_digest",
            "operation_id",
            "committed_act_state_digest",
            "host_receipt_digest",
            "host_invocation_digest",
            "expected_observation_digest",
            "verification_criterion_digest",
            "mission_cycle_state_digest",
            "observe_phase_event_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("mission_cycle_cycle_index"), "mission_cycle_cycle_index")
        if receipt.get("mission_cycle_phase") != "observe":
            errors.append("observe_lineage_handoff_phase_invalid")
        for field, expected in {
            "source_effect_recorded": True,
            "observation_required": True,
            "observation_not_verification": True,
            "verification_required": True,
            "single_use": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"observe_lineage_handoff_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("observe_lineage_handoff_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("observe_lineage_handoff_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_observe_lineage_completion_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
    committed_observe_state: Mapping[str, Any],
    observe_phase_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    handoff_errors = validate_handoff_receipt(handoff_receipt)
    observe_errors = validate_observe_state(committed_observe_state)
    if handoff_errors:
        raise ValueError("observe_lineage_handoff_invalid:" + ";".join(handoff_errors))
    if observe_errors:
        raise ValueError("observe_lineage_state_invalid:" + ";".join(observe_errors))
    if committed_observe_state.get("current_phase") != "commit":
        raise ValueError("observe_lineage_state_not_committed")
    if observe_phase_receipt.get("version") != OBSERVE_PHASE_RECEIPT_VERSION:
        raise ValueError("observe_lineage_phase_receipt_version_invalid")
    if observe_phase_receipt.get("observe_phase_receipt_digest") != observe_phase_receipt_digest(
        observe_phase_receipt
    ):
        raise ValueError("observe_lineage_phase_receipt_digest_invalid")

    bindings = {
        "source_act_state_digest": handoff_receipt.get("committed_act_state_digest"),
        "host_receipt_digest": handoff_receipt.get("host_receipt_digest"),
        "host_invocation_digest": handoff_receipt.get("host_invocation_digest"),
        "selected_step_id": handoff_receipt.get("selected_step_id"),
        "selected_step_digest": handoff_receipt.get("selected_step_digest"),
        "operation_id": handoff_receipt.get("operation_id"),
        "expected_observation_digest": handoff_receipt.get(
            "expected_observation_digest"
        ),
        "verification_criterion_digest": handoff_receipt.get(
            "verification_criterion_digest"
        ),
        "mission_contract_digest": handoff_receipt.get("mission_contract_digest"),
    }
    for field, expected in bindings.items():
        _require_equal(
            committed_observe_state, field, expected, "observe_lineage_state"
        )
    for field, expected in {
        "observe_state_digest": committed_observe_state.get("observe_state_digest"),
        "source_act_state_digest": committed_observe_state.get(
            "source_act_state_digest"
        ),
        "host_receipt_digest": committed_observe_state.get("host_receipt_digest"),
        "host_invocation_digest": committed_observe_state.get(
            "host_invocation_digest"
        ),
        "route": committed_observe_state.get("route"),
        "observation_debt_discharged": committed_observe_state.get(
            "observation_debt_discharged"
        ),
        "reobservation_required": committed_observe_state.get(
            "reobservation_required"
        ),
        "verification_required": True,
        "mission_cycle_phase": "observe",
        "observation_not_verification": True,
    }.items():
        _require_equal(
            observe_phase_receipt, field, expected, "observe_lineage_phase_receipt"
        )

    packet = {
        "version": COMPLETION_RECEIPT_VERSION,
        "observe_lineage_handoff_receipt_digest": handoff_receipt[
            "observe_lineage_handoff_receipt_digest"
        ],
        "act_lineage_completion_receipt_digest": handoff_receipt[
            "act_lineage_completion_receipt_digest"
        ],
        "next_cycle_compiler_receipt_digest": handoff_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "replan_phase_receipt_digest": handoff_receipt[
            "replan_phase_receipt_digest"
        ],
        "qi_condition_packet_digest": handoff_receipt[
            "qi_condition_packet_digest"
        ],
        "decision_receipt_digest": handoff_receipt["decision_receipt_digest"],
        "selected_candidate_digest": handoff_receipt[
            "selected_candidate_digest"
        ],
        "selected_step_digest": handoff_receipt["selected_step_digest"],
        "committed_act_state_digest": handoff_receipt[
            "committed_act_state_digest"
        ],
        "committed_observe_state_digest": committed_observe_state[
            "observe_state_digest"
        ],
        "observe_phase_receipt_digest": observe_phase_receipt[
            "observe_phase_receipt_digest"
        ],
        "evidence_packet_digest": committed_observe_state[
            "evidence_packet_digest"
        ],
        "quality_report_digest": committed_observe_state[
            "quality_report_digest"
        ],
        "comparison_receipt_digest": committed_observe_state[
            "comparison_receipt_digest"
        ],
        "route": committed_observe_state["route"],
        "observation_recorded": bool(
            committed_observe_state.get("observation_recorded")
        ),
        "observation_debt_discharged": bool(
            committed_observe_state.get("observation_debt_discharged")
        ),
        "reobservation_required": bool(
            committed_observe_state.get("reobservation_required")
        ),
        "verification_required": True,
        "observation_not_verification": True,
        "source_lineage_preserved": True,
        "completed_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "observe_lineage_completion_receipt_digest": "",
    }
    packet["observe_lineage_completion_receipt_digest"] = completion_receipt_digest(
        packet
    )
    return packet


def validate_completion_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != COMPLETION_RECEIPT_VERSION:
            errors.append("observe_lineage_completion_version_invalid")
        if receipt.get(
            "observe_lineage_completion_receipt_digest"
        ) != completion_receipt_digest(receipt):
            errors.append("observe_lineage_completion_digest_invalid")
        for field in (
            "observe_lineage_handoff_receipt_digest",
            "act_lineage_completion_receipt_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "selected_step_digest",
            "committed_act_state_digest",
            "committed_observe_state_digest",
            "observe_phase_receipt_digest",
            "evidence_packet_digest",
            "quality_report_digest",
            "comparison_receipt_digest",
            "route",
        ):
            require_string(receipt.get(field), field)
        for field, expected in {
            "observation_recorded": True,
            "verification_required": True,
            "observation_not_verification": True,
            "source_lineage_preserved": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"observe_lineage_completion_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("observe_lineage_completion_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("observe_lineage_completion_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
