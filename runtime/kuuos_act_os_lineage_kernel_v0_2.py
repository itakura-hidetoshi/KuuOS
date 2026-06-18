from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_act_os_types_v0_1 import (
    AUTHORIZATION_VERSION,
    authorization_digest,
)
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import license_digest
from runtime.kuuos_plan_os_state_v0_1 import validate_plan_state
from runtime.kuuos_plan_os_types_v0_1 import (
    ACTIVATION_RECEIPT_VERSION as PLAN_ACTIVATION_VERSION,
    plan_activation_receipt_digest,
)
from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
    COMPILER_RECEIPT_VERSION,
    next_cycle_compiler_receipt_digest,
)
from runtime.kuuos_act_os_lineage_types_v0_2 import (
    AUTHORIZATION_ENVELOPE_VERSION,
    COMPLETION_RECEIPT_VERSION,
    HANDOFF_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS,
    authorization_envelope_digest,
    completion_receipt_digest,
    copy_non_authority,
    handoff_receipt_digest,
    require_int,
    require_string,
)


def _selected_step(plan_state: Mapping[str, Any], step_id: str) -> dict[str, Any]:
    for raw in plan_state.get("steps", []):
        if str(raw.get("step_id", "")) == step_id:
            return deepcopy(dict(raw))
    raise ValueError("lineage_selected_step_not_found")


def _validate_compiler_receipt(
    plan_state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> None:
    if receipt.get("version") != COMPILER_RECEIPT_VERSION:
        raise ValueError("lineage_compiler_receipt_version_invalid")
    if receipt.get("next_cycle_compiler_receipt_digest") != next_cycle_compiler_receipt_digest(
        receipt
    ):
        raise ValueError("lineage_compiler_receipt_digest_invalid")
    bindings = {
        "compiled_plan_id": plan_state.get("plan_id"),
        "compiled_plan_state_digest": plan_state.get("plan_state_digest"),
        "compiled_plan_basis_digest": plan_state.get("plan_basis_digest"),
        "compiled_plan_route": plan_state.get("route"),
        "next_plan_basis_digest": plan_state.get("next_plan_basis_digest"),
        "lineage_id": plan_state.get("lineage_id"),
        "mission_contract_digest": plan_state.get("mission_contract_digest"),
    }
    for field, expected in bindings.items():
        if receipt.get(field) != expected:
            raise ValueError(f"lineage_compiler_receipt_{field}_mismatch")
    required = {
        "projected_plan_route": "PLAN_CANDIDATE",
        "structured_compiler": "PlanOS_v0_1",
        "single_use_activation": True,
        "plan_committed": True,
        "plan_not_execution": True,
        "host_license_granted": False,
        "memory_overwrite": False,
    }
    for field, expected in required.items():
        if receipt.get(field) != expected:
            raise ValueError(f"lineage_compiler_receipt_{field}_invalid")
    for field in (
        "replan_phase_receipt_digest",
        "next_plan_activation_receipt_digest",
        "materialization_packet_digest",
        "selected_candidate_id",
        "selected_candidate_digest",
        "qi_condition_packet_digest",
        "decision_receipt_digest",
        "synthesis_packet_digest",
    ):
        require_string(receipt.get(field), field)


def _validate_plan_activation(
    plan_state: Mapping[str, Any], receipt: Mapping[str, Any]
) -> None:
    if receipt.get("version") != PLAN_ACTIVATION_VERSION:
        raise ValueError("lineage_plan_activation_version_invalid")
    if receipt.get("plan_activation_receipt_digest") != plan_activation_receipt_digest(
        receipt
    ):
        raise ValueError("lineage_plan_activation_digest_invalid")
    bindings = {
        "plan_id": plan_state.get("plan_id"),
        "plan_state_digest": plan_state.get("plan_state_digest"),
        "committed_plan_digest": plan_state.get("latest_committed_plan_digest"),
        "plan_basis_digest": plan_state.get("plan_basis_digest"),
        "next_plan_basis_digest": plan_state.get("next_plan_basis_digest"),
        "route": "PLAN_CANDIDATE",
    }
    for field, expected in bindings.items():
        if receipt.get(field) != expected:
            raise ValueError(f"lineage_plan_activation_{field}_mismatch")
    if receipt.get("mission_cycle_phase") != "plan":
        raise ValueError("lineage_plan_activation_phase_invalid")
    if receipt.get("plan_not_execution") is not True:
        raise ValueError("lineage_plan_activation_nonexecution_required")
    if receipt.get("host_license_granted") is not False:
        raise ValueError("lineage_plan_activation_license_forbidden")


def build_act_lineage_handoff_receipt(
    *,
    compiled_plan_state: Mapping[str, Any],
    plan_activation_receipt: Mapping[str, Any],
    next_cycle_compiler_receipt: Mapping[str, Any],
    selected_step_id: str,
    operation_id: str,
    operation_input_digest: str,
    mission_cycle_phase: str,
    mission_cycle_cycle_index: int,
    mission_cycle_state_digest: str,
    act_phase_event_digest: str,
    act_phase_receipt_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_plan_state(compiled_plan_state)
    if errors:
        raise ValueError("lineage_compiled_plan_invalid:" + ";".join(errors))
    if compiled_plan_state.get("current_phase") != "commit":
        raise ValueError("lineage_compiled_plan_not_committed")
    if compiled_plan_state.get("route") != "PLAN_CANDIDATE":
        raise ValueError("lineage_compiled_plan_not_effect_candidate")
    _validate_compiler_receipt(compiled_plan_state, next_cycle_compiler_receipt)
    _validate_plan_activation(compiled_plan_state, plan_activation_receipt)
    if mission_cycle_phase != "act":
        raise ValueError("lineage_act_phase_required")
    cycle = require_int(mission_cycle_cycle_index, "mission_cycle_cycle_index")
    expected_cycle = int(next_cycle_compiler_receipt.get("mission_cycle_cycle_index", -1))
    if cycle != expected_cycle:
        raise ValueError("lineage_act_cycle_mismatch")
    step = _selected_step(
        compiled_plan_state, require_string(selected_step_id, "selected_step_id")
    )
    if step.get("step_class") != "act_candidate" or step.get("effectful") is not True:
        raise ValueError("lineage_selected_step_not_effectful_act_candidate")
    if not step.get("stop_condition_digests"):
        raise ValueError("lineage_selected_step_stop_conditions_missing")
    require_string(step.get("step_digest"), "selected_step_digest")
    require_string(step.get("expected_observation_digest"), "expected_observation_digest")
    require_string(
        step.get("verification_criterion_digest"), "verification_criterion_digest"
    )
    packet = {
        "version": HANDOFF_RECEIPT_VERSION,
        "lineage_id": compiled_plan_state["lineage_id"],
        "mission_contract_digest": compiled_plan_state["mission_contract_digest"],
        "next_cycle_compiler_receipt_digest": next_cycle_compiler_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "compiled_plan_id": compiled_plan_state["plan_id"],
        "compiled_plan_state_digest": compiled_plan_state["plan_state_digest"],
        "compiled_plan_basis_digest": compiled_plan_state["plan_basis_digest"],
        "committed_plan_digest": compiled_plan_state["latest_committed_plan_digest"],
        "plan_activation_receipt_digest": plan_activation_receipt[
            "plan_activation_receipt_digest"
        ],
        "replan_phase_receipt_digest": next_cycle_compiler_receipt[
            "replan_phase_receipt_digest"
        ],
        "next_plan_activation_receipt_digest": next_cycle_compiler_receipt[
            "next_plan_activation_receipt_digest"
        ],
        "materialization_packet_digest": next_cycle_compiler_receipt[
            "materialization_packet_digest"
        ],
        "next_plan_basis_digest": next_cycle_compiler_receipt[
            "next_plan_basis_digest"
        ],
        "selected_candidate_id": next_cycle_compiler_receipt[
            "selected_candidate_id"
        ],
        "selected_candidate_digest": next_cycle_compiler_receipt[
            "selected_candidate_digest"
        ],
        "qi_condition_packet_digest": next_cycle_compiler_receipt[
            "qi_condition_packet_digest"
        ],
        "decision_receipt_digest": next_cycle_compiler_receipt[
            "decision_receipt_digest"
        ],
        "synthesis_packet_digest": next_cycle_compiler_receipt[
            "synthesis_packet_digest"
        ],
        "selected_step_id": step["step_id"],
        "selected_step_digest": step["step_digest"],
        "expected_observation_digest": step["expected_observation_digest"],
        "verification_criterion_digest": step["verification_criterion_digest"],
        "stop_condition_digests": list(step["stop_condition_digests"]),
        "requires_human_review": bool(step.get("requires_human_review")),
        "requires_external_license": bool(step.get("requires_external_license")),
        "operation_id": require_string(operation_id, "operation_id"),
        "operation_input_digest": require_string(
            operation_input_digest, "operation_input_digest"
        ),
        "mission_cycle_phase": "act",
        "mission_cycle_cycle_index": cycle,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "act_phase_event_digest": require_string(
            act_phase_event_digest, "act_phase_event_digest"
        ),
        "act_phase_receipt_digest": require_string(
            act_phase_receipt_digest, "act_phase_receipt_digest"
        ),
        "plan_activation_is_not_execution": True,
        "step_authorization_still_required": True,
        "host_license_still_required": True,
        "single_use": True,
        "execution_granted": False,
        "host_license_granted": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "act_lineage_handoff_receipt_digest": "",
    }
    packet["act_lineage_handoff_receipt_digest"] = handoff_receipt_digest(packet)
    return packet


def validate_handoff_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != HANDOFF_RECEIPT_VERSION:
            errors.append("lineage_handoff_version_invalid")
        if receipt.get("act_lineage_handoff_receipt_digest") != handoff_receipt_digest(
            receipt
        ):
            errors.append("lineage_handoff_digest_invalid")
        for field in (
            "lineage_id",
            "mission_contract_digest",
            "next_cycle_compiler_receipt_digest",
            "compiled_plan_state_digest",
            "compiled_plan_basis_digest",
            "committed_plan_digest",
            "plan_activation_receipt_digest",
            "replan_phase_receipt_digest",
            "next_plan_activation_receipt_digest",
            "materialization_packet_digest",
            "next_plan_basis_digest",
            "selected_candidate_id",
            "selected_candidate_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "synthesis_packet_digest",
            "selected_step_id",
            "selected_step_digest",
            "operation_id",
            "operation_input_digest",
            "act_phase_receipt_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("mission_cycle_cycle_index"), "mission_cycle_cycle_index")
        if receipt.get("mission_cycle_phase") != "act":
            errors.append("lineage_handoff_act_phase_invalid")
        for field, expected in {
            "plan_activation_is_not_execution": True,
            "step_authorization_still_required": True,
            "host_license_still_required": True,
            "single_use": True,
            "execution_granted": False,
            "host_license_granted": False,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"lineage_handoff_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("lineage_handoff_authority_widening")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_authorization_envelope(
    *,
    handoff_receipt: Mapping[str, Any],
    act_state: Mapping[str, Any],
    step_authorization: Mapping[str, Any],
    host_license: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    handoff_errors = validate_handoff_receipt(handoff_receipt)
    if handoff_errors:
        raise ValueError("invalid_lineage_handoff:" + ";".join(handoff_errors))
    act_errors = validate_act_state(act_state)
    if act_errors:
        raise ValueError("invalid_selected_act_state:" + ";".join(act_errors))
    if act_state.get("current_phase") != "select":
        raise ValueError("lineage_authorization_requires_selected_act_state")
    if step_authorization.get("version") != AUTHORIZATION_VERSION:
        raise ValueError("lineage_inner_authorization_version_invalid")
    if step_authorization.get("step_authorization_digest") != authorization_digest(
        step_authorization
    ):
        raise ValueError("lineage_inner_authorization_digest_invalid")
    bindings = {
        "source_plan_state_digest": handoff_receipt.get("compiled_plan_state_digest"),
        "source_plan_basis_digest": handoff_receipt.get("compiled_plan_basis_digest"),
        "plan_activation_receipt_digest": handoff_receipt.get(
            "plan_activation_receipt_digest"
        ),
        "selected_step_id": handoff_receipt.get("selected_step_id"),
        "selected_step_digest": handoff_receipt.get("selected_step_digest"),
        "operation_id": handoff_receipt.get("operation_id"),
        "operation_input_digest": handoff_receipt.get("operation_input_digest"),
        "act_phase_receipt_digest": handoff_receipt.get("act_phase_receipt_digest"),
    }
    for field, expected in bindings.items():
        if step_authorization.get(field) != expected:
            raise ValueError(f"lineage_inner_authorization_{field}_mismatch")
    state_bindings = {
        "source_plan_state_digest": handoff_receipt.get("compiled_plan_state_digest"),
        "source_plan_basis_digest": handoff_receipt.get("compiled_plan_basis_digest"),
        "plan_activation_receipt_digest": handoff_receipt.get(
            "plan_activation_receipt_digest"
        ),
        "selected_step_id": handoff_receipt.get("selected_step_id"),
        "selected_step_digest": handoff_receipt.get("selected_step_digest"),
        "operation_id": handoff_receipt.get("operation_id"),
        "operation_input_digest": handoff_receipt.get("operation_input_digest"),
    }
    for field, expected in state_bindings.items():
        if act_state.get(field) != expected:
            raise ValueError(f"lineage_act_state_{field}_mismatch")
    if host_license.get("host_license_digest") != license_digest(host_license):
        raise ValueError("lineage_host_license_digest_invalid")
    if step_authorization.get("host_license_digest") != host_license.get(
        "host_license_digest"
    ):
        raise ValueError("lineage_authorization_host_license_mismatch")
    if step_authorization.get("authorization_does_not_widen_license") is not True:
        raise ValueError("lineage_authorization_license_widening_forbidden")
    if handoff_receipt.get("requires_human_review") is True:
        require_string(
            step_authorization.get("human_approval_receipt_digest"),
            "human_approval_receipt_digest",
        )
        require_string(step_authorization.get("human_approver_id"), "human_approver_id")
    packet = {
        "version": AUTHORIZATION_ENVELOPE_VERSION,
        "act_lineage_handoff_receipt_digest": handoff_receipt[
            "act_lineage_handoff_receipt_digest"
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
        "selected_candidate_digest": handoff_receipt["selected_candidate_digest"],
        "materialization_packet_digest": handoff_receipt[
            "materialization_packet_digest"
        ],
        "act_state_digest": act_state["act_state_digest"],
        "step_authorization_digest": step_authorization[
            "step_authorization_digest"
        ],
        "selected_step_id": handoff_receipt["selected_step_id"],
        "selected_step_digest": handoff_receipt["selected_step_digest"],
        "operation_id": handoff_receipt["operation_id"],
        "operation_input_digest": handoff_receipt["operation_input_digest"],
        "act_phase_receipt_digest": handoff_receipt["act_phase_receipt_digest"],
        "host_license_digest": host_license["host_license_digest"],
        "human_approval_receipt_digest": str(
            step_authorization.get("human_approval_receipt_digest", "")
        ),
        "human_approver_id": str(step_authorization.get("human_approver_id", "")),
        "inner_authorization_unchanged": True,
        "authorization_does_not_widen_license": True,
        "single_use": True,
        "execution_granted_by_envelope": False,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "authorization_envelope_digest": "",
    }
    packet["authorization_envelope_digest"] = authorization_envelope_digest(packet)
    return packet


def validate_authorization_envelope(envelope: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if envelope.get("version") != AUTHORIZATION_ENVELOPE_VERSION:
            errors.append("lineage_authorization_envelope_version_invalid")
        if envelope.get("authorization_envelope_digest") != authorization_envelope_digest(
            envelope
        ):
            errors.append("lineage_authorization_envelope_digest_invalid")
        for field in (
            "act_lineage_handoff_receipt_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "materialization_packet_digest",
            "act_state_digest",
            "step_authorization_digest",
            "selected_step_id",
            "selected_step_digest",
            "operation_id",
            "operation_input_digest",
            "act_phase_receipt_digest",
            "host_license_digest",
        ):
            require_string(envelope.get(field), field)
        for field, expected in {
            "inner_authorization_unchanged": True,
            "authorization_does_not_widen_license": True,
            "single_use": True,
            "execution_granted_by_envelope": False,
        }.items():
            if envelope.get(field) != expected:
                errors.append(f"lineage_authorization_envelope_{field}_invalid")
        if dict(envelope.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("lineage_authorization_envelope_authority_widening")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_act_lineage_completion_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
    authorization_envelope: Mapping[str, Any],
    committed_act_state: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    handoff_errors = validate_handoff_receipt(handoff_receipt)
    envelope_errors = validate_authorization_envelope(authorization_envelope)
    act_errors = validate_act_state(committed_act_state)
    if handoff_errors:
        raise ValueError("invalid_lineage_handoff:" + ";".join(handoff_errors))
    if envelope_errors:
        raise ValueError("invalid_authorization_envelope:" + ";".join(envelope_errors))
    if act_errors:
        raise ValueError("invalid_committed_act_state:" + ";".join(act_errors))
    if committed_act_state.get("current_phase") != "commit":
        raise ValueError("lineage_act_state_not_committed")
    bindings = {
        "source_plan_state_digest": handoff_receipt.get("compiled_plan_state_digest"),
        "source_plan_basis_digest": handoff_receipt.get("compiled_plan_basis_digest"),
        "plan_activation_receipt_digest": handoff_receipt.get(
            "plan_activation_receipt_digest"
        ),
        "selected_step_id": handoff_receipt.get("selected_step_id"),
        "selected_step_digest": handoff_receipt.get("selected_step_digest"),
        "operation_id": handoff_receipt.get("operation_id"),
        "operation_input_digest": handoff_receipt.get("operation_input_digest"),
    }
    for field, expected in bindings.items():
        if committed_act_state.get(field) != expected:
            raise ValueError(f"lineage_completion_{field}_mismatch")
    if authorization_envelope.get(
        "act_lineage_handoff_receipt_digest"
    ) != handoff_receipt.get("act_lineage_handoff_receipt_digest"):
        raise ValueError("lineage_completion_handoff_mismatch")
    if authorization_envelope.get("step_authorization_digest") != committed_act_state.get(
        "step_authorization_digest"
    ):
        raise ValueError("lineage_completion_authorization_mismatch")
    effect_recorded = bool(committed_act_state.get("effect_recorded"))
    if effect_recorded:
        if committed_act_state.get("route") != "EFFECT_RECORDED":
            raise ValueError("lineage_completion_effect_route_mismatch")
        if committed_act_state.get("observation_required") is not True:
            raise ValueError("lineage_completion_observation_debt_missing")
        if committed_act_state.get("verification_required") is not True:
            raise ValueError("lineage_completion_verification_debt_missing")
    elif committed_act_state.get("route") == "EFFECT_RECORDED":
        raise ValueError("lineage_completion_false_effect_promotion")
    packet = {
        "version": COMPLETION_RECEIPT_VERSION,
        "act_lineage_handoff_receipt_digest": handoff_receipt[
            "act_lineage_handoff_receipt_digest"
        ],
        "authorization_envelope_digest": authorization_envelope[
            "authorization_envelope_digest"
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
        "selected_candidate_digest": handoff_receipt["selected_candidate_digest"],
        "selected_step_digest": handoff_receipt["selected_step_digest"],
        "committed_act_state_digest": committed_act_state["act_state_digest"],
        "step_authorization_digest": committed_act_state[
            "step_authorization_digest"
        ],
        "host_license_digest": committed_act_state["host_license_digest"],
        "host_projection_digest": committed_act_state["host_projection_digest"],
        "host_tick_digest": committed_act_state["host_tick_digest"],
        "host_receipt_digest": committed_act_state["host_receipt_digest"],
        "host_invocation_digest": committed_act_state["host_invocation_digest"],
        "result_supervisor_bundle_digest": committed_act_state[
            "result_supervisor_bundle_digest"
        ],
        "route": committed_act_state["route"],
        "effect_recorded": effect_recorded,
        "observation_required": bool(
            committed_act_state.get("observation_required")
        ),
        "verification_required": bool(
            committed_act_state.get("verification_required")
        ),
        "automatic_truth_promotion": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "lower_host_receipt_canonical": True,
        "completed_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "act_lineage_completion_receipt_digest": "",
    }
    packet["act_lineage_completion_receipt_digest"] = completion_receipt_digest(
        packet
    )
    return packet


def validate_completion_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != COMPLETION_RECEIPT_VERSION:
            errors.append("lineage_completion_version_invalid")
        if receipt.get("act_lineage_completion_receipt_digest") != completion_receipt_digest(
            receipt
        ):
            errors.append("lineage_completion_digest_invalid")
        for field in (
            "act_lineage_handoff_receipt_digest",
            "authorization_envelope_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "selected_step_digest",
            "committed_act_state_digest",
            "step_authorization_digest",
            "host_license_digest",
            "host_projection_digest",
            "host_tick_digest",
            "host_receipt_digest",
            "host_invocation_digest",
        ):
            require_string(receipt.get(field), field)
        if receipt.get("effect_recorded") is True:
            if receipt.get("route") != "EFFECT_RECORDED":
                errors.append("lineage_completion_effect_route_invalid")
            if receipt.get("observation_required") is not True:
                errors.append("lineage_completion_observation_debt_missing")
            if receipt.get("verification_required") is not True:
                errors.append("lineage_completion_verification_debt_missing")
        for field in (
            "automatic_truth_promotion",
            "automatic_plan_completion",
            "automatic_rollback",
        ):
            if receipt.get(field) is not False:
                errors.append(f"lineage_completion_{field}_forbidden")
        if receipt.get("lower_host_receipt_canonical") is not True:
            errors.append("lineage_completion_lower_receipt_required")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("lineage_completion_authority_widening")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
