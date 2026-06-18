from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_learn_os_types_v0_1 import (
    LEARN_PHASE_RECEIPT_VERSION,
    learn_phase_receipt_digest,
)
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.kuuos_verify_os_lineage_kernel_v0_2 import (
    validate_completion_receipt as validate_verify_completion_receipt,
    validate_handoff_receipt as validate_verify_handoff_receipt,
)
from runtime.kuuos_learn_os_lineage_types_v0_2 import (
    COMPLETION_RECEIPT_VERSION,
    HANDOFF_RECEIPT_VERSION,
    NON_AUTHORITY_FLAGS,
    PLANOS_CANDIDATE_TYPES_BY_LEARNING_ROUTE,
    REQUIRED_BOUNDARY,
    completion_receipt_digest,
    copy_boundary,
    copy_non_authority,
    handoff_receipt_digest,
    planos_replan_input_digest,
    require_int,
    require_string,
)


def _require_equal(
    packet: Mapping[str, Any], field: str, expected: Any, prefix: str
) -> None:
    if packet.get(field) != expected:
        raise ValueError(f"{prefix}_{field}_mismatch")


def build_learn_lineage_handoff_receipt(
    *,
    committed_verify_state: Mapping[str, Any],
    verify_lineage_handoff_receipt: Mapping[str, Any],
    verify_lineage_completion_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_cycle_index: int,
    mission_cycle_state_digest: str,
    learn_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    verify_errors = validate_verify_state(committed_verify_state)
    handoff_errors = validate_verify_handoff_receipt(verify_lineage_handoff_receipt)
    completion_errors = validate_verify_completion_receipt(
        verify_lineage_completion_receipt
    )
    if verify_errors:
        raise ValueError("learn_lineage_verify_state_invalid:" + ";".join(verify_errors))
    if handoff_errors:
        raise ValueError("learn_lineage_verify_handoff_invalid:" + ";".join(handoff_errors))
    if completion_errors:
        raise ValueError(
            "learn_lineage_verify_completion_invalid:" + ";".join(completion_errors)
        )
    if committed_verify_state.get("current_phase") != "commit":
        raise ValueError("learn_lineage_verify_state_not_committed")
    if committed_verify_state.get("route") == "PENDING":
        raise ValueError("learn_lineage_verify_route_pending")
    if committed_verify_state.get("verification_recorded") is not True:
        raise ValueError("learn_lineage_verification_missing")
    if committed_verify_state.get("learning_required") is not True:
        raise ValueError("learn_lineage_learning_debt_missing")

    _require_equal(
        verify_lineage_completion_receipt,
        "verify_lineage_handoff_receipt_digest",
        verify_lineage_handoff_receipt.get("verify_lineage_handoff_receipt_digest"),
        "learn_lineage_verify_completion",
    )
    for field, expected in {
        "committed_verify_state_digest": committed_verify_state.get("verify_state_digest"),
        "verification_criterion_digest": committed_verify_state.get(
            "verification_criterion_digest"
        ),
        "criterion_packet_digest": committed_verify_state.get("criterion_packet_digest"),
        "challenge_packet_digest": committed_verify_state.get("challenge_packet_digest"),
        "corroboration_report_digest": committed_verify_state.get(
            "corroboration_report_digest"
        ),
        "adjudication_receipt_digest": committed_verify_state.get(
            "adjudication_receipt_digest"
        ),
        "verification_evidence_digest": committed_verify_state.get(
            "verification_evidence_digest"
        ),
        "evidence_packet_digest": committed_verify_state.get("evidence_packet_digest"),
        "comparison_receipt_digest": committed_verify_state.get(
            "comparison_receipt_digest"
        ),
        "route": committed_verify_state.get("route"),
        "verification_recorded": True,
        "learning_required": True,
        "learning_must_be_future_only": True,
        "verification_not_truth": True,
        "causal_attribution_not_granted": True,
        "automatic_learning": False,
    }.items():
        _require_equal(
            verify_lineage_completion_receipt,
            field,
            expected,
            "learn_lineage_verify_completion",
        )

    for field, expected in {
        "committed_observe_state_digest": committed_verify_state.get(
            "source_observe_state_digest"
        ),
        "source_act_state_digest": committed_verify_state.get("source_act_state_digest"),
        "verification_criterion_digest": committed_verify_state.get(
            "verification_criterion_digest"
        ),
        "evidence_packet_digest": committed_verify_state.get("evidence_packet_digest"),
        "comparison_receipt_digest": committed_verify_state.get(
            "comparison_receipt_digest"
        ),
        "mission_contract_digest": committed_verify_state.get("mission_contract_digest"),
    }.items():
        _require_equal(
            verify_lineage_handoff_receipt,
            field,
            expected,
            "learn_lineage_verify_handoff",
        )

    if mission_cycle_phase != "learn":
        raise ValueError("learn_lineage_learn_phase_required")
    cycle = require_int(mission_cycle_cycle_index, "mission_cycle_cycle_index")
    expected_cycle = int(verify_lineage_handoff_receipt.get("mission_cycle_cycle_index", -1))
    if cycle != expected_cycle:
        raise ValueError("learn_lineage_cycle_mismatch")

    challenge = committed_verify_state.get("challenge_packet")
    if not isinstance(challenge, Mapping):
        raise ValueError("learn_lineage_source_challenge_missing")
    counterevidence = list(challenge.get("counterevidence_digests", []))
    falsification_attempts = list(challenge.get("falsification_attempt_digests", []))
    independent_assessors = list(challenge.get("independent_assessor_ids", []))
    if not falsification_attempts:
        raise ValueError("learn_lineage_source_falsification_missing")
    if not independent_assessors:
        raise ValueError("learn_lineage_source_independent_assessment_missing")
    if challenge.get("counterevidence_preserved") is not True:
        raise ValueError("learn_lineage_source_counterevidence_not_preserved")

    packet = {
        "version": HANDOFF_RECEIPT_VERSION,
        "lineage_id": verify_lineage_handoff_receipt["lineage_id"],
        "mission_contract_digest": verify_lineage_handoff_receipt[
            "mission_contract_digest"
        ],
        "verify_lineage_handoff_receipt_digest": verify_lineage_handoff_receipt[
            "verify_lineage_handoff_receipt_digest"
        ],
        "verify_lineage_completion_receipt_digest": verify_lineage_completion_receipt[
            "verify_lineage_completion_receipt_digest"
        ],
        "observe_lineage_completion_receipt_digest": verify_lineage_completion_receipt[
            "observe_lineage_completion_receipt_digest"
        ],
        "act_lineage_completion_receipt_digest": verify_lineage_completion_receipt[
            "act_lineage_completion_receipt_digest"
        ],
        "next_cycle_compiler_receipt_digest": verify_lineage_completion_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "replan_phase_receipt_digest": verify_lineage_completion_receipt[
            "replan_phase_receipt_digest"
        ],
        "qi_condition_packet_digest": verify_lineage_completion_receipt[
            "qi_condition_packet_digest"
        ],
        "decision_receipt_digest": verify_lineage_completion_receipt[
            "decision_receipt_digest"
        ],
        "selected_candidate_digest": verify_lineage_completion_receipt[
            "selected_candidate_digest"
        ],
        "selected_step_digest": verify_lineage_completion_receipt[
            "selected_step_digest"
        ],
        "committed_act_state_digest": verify_lineage_completion_receipt[
            "committed_act_state_digest"
        ],
        "committed_observe_state_digest": verify_lineage_completion_receipt[
            "committed_observe_state_digest"
        ],
        "committed_verify_state_digest": committed_verify_state["verify_state_digest"],
        "verify_phase_receipt_digest": verify_lineage_completion_receipt[
            "verify_phase_receipt_digest"
        ],
        "source_verification_route": committed_verify_state["route"],
        "source_verification_verdict": verify_lineage_completion_receipt["verdict"],
        "source_verification_evidence_digest": committed_verify_state[
            "verification_evidence_digest"
        ],
        "verification_criterion_digest": committed_verify_state[
            "verification_criterion_digest"
        ],
        "criterion_packet_digest": committed_verify_state["criterion_packet_digest"],
        "source_challenge_packet_digest": committed_verify_state[
            "challenge_packet_digest"
        ],
        "corroboration_report_digest": committed_verify_state[
            "corroboration_report_digest"
        ],
        "adjudication_receipt_digest": committed_verify_state[
            "adjudication_receipt_digest"
        ],
        "evidence_packet_digest": committed_verify_state["evidence_packet_digest"],
        "comparison_receipt_digest": committed_verify_state[
            "comparison_receipt_digest"
        ],
        "source_counterevidence_digests": counterevidence,
        "source_counterevidence_digest": sha(counterevidence),
        "source_falsification_attempt_digests": falsification_attempts,
        "source_independent_assessor_ids": independent_assessors,
        "source_reobservation_required": bool(
            committed_verify_state.get("reobservation_required")
        ),
        "source_corrective_action_required": bool(
            committed_verify_state.get("corrective_action_required")
        ),
        "mission_cycle_phase": "learn",
        "mission_cycle_cycle_index": cycle,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "learn_phase_event_digest": require_string(
            learn_phase_event_digest, "learn_phase_event_digest"
        ),
        "learning_required": True,
        "future_only": True,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_records_unchanged": True,
        "memory_overwrite": False,
        "activation_requires_planos_replan": True,
        "learn_delta_not_replan_activation": True,
        "replan_owned_by_planos": True,
        "selection_owned_by_decisionos": True,
        "execution_owned_by_actos": True,
        "qi_context_only": True,
        "single_use": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "learn_lineage_handoff_receipt_digest": "",
    }
    packet["learn_lineage_handoff_receipt_digest"] = handoff_receipt_digest(packet)
    return packet


def validate_handoff_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != HANDOFF_RECEIPT_VERSION:
            errors.append("learn_lineage_handoff_version_invalid")
        if receipt.get("learn_lineage_handoff_receipt_digest") != handoff_receipt_digest(
            receipt
        ):
            errors.append("learn_lineage_handoff_digest_invalid")
        for field in (
            "lineage_id",
            "mission_contract_digest",
            "verify_lineage_handoff_receipt_digest",
            "verify_lineage_completion_receipt_digest",
            "observe_lineage_completion_receipt_digest",
            "act_lineage_completion_receipt_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "selected_step_digest",
            "committed_act_state_digest",
            "committed_observe_state_digest",
            "committed_verify_state_digest",
            "verify_phase_receipt_digest",
            "source_verification_route",
            "source_verification_verdict",
            "source_verification_evidence_digest",
            "verification_criterion_digest",
            "criterion_packet_digest",
            "source_challenge_packet_digest",
            "corroboration_report_digest",
            "adjudication_receipt_digest",
            "evidence_packet_digest",
            "comparison_receipt_digest",
            "source_counterevidence_digest",
            "mission_cycle_state_digest",
            "learn_phase_event_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(receipt.get("mission_cycle_cycle_index"), "mission_cycle_cycle_index")
        if receipt.get("mission_cycle_phase") != "learn":
            errors.append("learn_lineage_handoff_phase_invalid")
        counterevidence = list(receipt.get("source_counterevidence_digests", []))
        if receipt.get("source_counterevidence_digest") != sha(counterevidence):
            errors.append("learn_lineage_handoff_counterevidence_digest_invalid")
        if not list(receipt.get("source_falsification_attempt_digests", [])):
            errors.append("learn_lineage_handoff_falsification_missing")
        if not list(receipt.get("source_independent_assessor_ids", [])):
            errors.append("learn_lineage_handoff_independent_assessment_missing")
        for field, expected in {
            "learning_required": True,
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_records_unchanged": True,
            "memory_overwrite": False,
            "activation_requires_planos_replan": True,
            "learn_delta_not_replan_activation": True,
            "replan_owned_by_planos": True,
            "selection_owned_by_decisionos": True,
            "execution_owned_by_actos": True,
            "qi_context_only": True,
            "single_use": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"learn_lineage_handoff_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("learn_lineage_handoff_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("learn_lineage_handoff_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_learn_lineage_completion_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
    committed_learn_state: Mapping[str, Any],
    learn_phase_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    handoff_errors = validate_handoff_receipt(handoff_receipt)
    learn_errors = validate_learn_state(committed_learn_state)
    if handoff_errors:
        raise ValueError("learn_lineage_handoff_invalid:" + ";".join(handoff_errors))
    if learn_errors:
        raise ValueError("learn_lineage_state_invalid:" + ";".join(learn_errors))
    if committed_learn_state.get("current_phase") != "commit":
        raise ValueError("learn_lineage_state_not_committed")
    if learn_phase_receipt.get("version") != LEARN_PHASE_RECEIPT_VERSION:
        raise ValueError("learn_lineage_phase_receipt_version_invalid")
    if learn_phase_receipt.get("learn_phase_receipt_digest") != learn_phase_receipt_digest(
        learn_phase_receipt
    ):
        raise ValueError("learn_lineage_phase_receipt_digest_invalid")

    for field, expected in {
        "source_verify_state_digest": handoff_receipt.get("committed_verify_state_digest"),
        "source_verification_route": handoff_receipt.get("source_verification_route"),
        "source_verification_evidence_digest": handoff_receipt.get(
            "source_verification_evidence_digest"
        ),
        "source_observe_state_digest": handoff_receipt.get(
            "committed_observe_state_digest"
        ),
        "source_act_state_digest": handoff_receipt.get("committed_act_state_digest"),
        "verification_criterion_digest": handoff_receipt.get(
            "verification_criterion_digest"
        ),
        "criterion_packet_digest": handoff_receipt.get("criterion_packet_digest"),
        "source_challenge_packet_digest": handoff_receipt.get(
            "source_challenge_packet_digest"
        ),
        "corroboration_report_digest": handoff_receipt.get(
            "corroboration_report_digest"
        ),
        "adjudication_receipt_digest": handoff_receipt.get(
            "adjudication_receipt_digest"
        ),
        "mission_contract_digest": handoff_receipt.get("mission_contract_digest"),
        "source_counterevidence_digest": handoff_receipt.get(
            "source_counterevidence_digest"
        ),
    }.items():
        _require_equal(committed_learn_state, field, expected, "learn_lineage_state")

    delta = committed_learn_state.get("learning_delta")
    middle_way = committed_learn_state.get("middle_way_report")
    abstraction = committed_learn_state.get("abstraction_packet")
    challenge = committed_learn_state.get("learning_challenge_packet")
    if not isinstance(delta, Mapping):
        raise ValueError("learn_lineage_learning_delta_missing")
    if not isinstance(middle_way, Mapping):
        raise ValueError("learn_lineage_middle_way_report_missing")
    if not isinstance(abstraction, Mapping):
        raise ValueError("learn_lineage_abstraction_packet_missing")
    if not isinstance(challenge, Mapping):
        raise ValueError("learn_lineage_learning_challenge_missing")
    for field, expected in {
        "future_only": True,
        "memory_overwrite": False,
        "active_now": False,
        "activation_requires_replan": True,
        "scope_widening": False,
        "invariant_removal": False,
        "current_cycle_mutation": False,
        "past_record_mutation": False,
    }.items():
        _require_equal(delta, field, expected, "learn_lineage_delta")
    if abstraction.get("counterevidence_preserved") is not True:
        raise ValueError("learn_lineage_abstraction_counterevidence_lost")
    if abstraction.get("qi_context_only") is not True:
        raise ValueError("learn_lineage_abstraction_qi_authority_invalid")
    if challenge.get("counterevidence_preserved") is not True:
        raise ValueError("learn_lineage_challenge_counterevidence_lost")
    if not list(challenge.get("anti_overgeneralization_test_digests", [])):
        raise ValueError("learn_lineage_anti_overgeneralization_missing")
    if middle_way.get("qi_grants_authority") is not False:
        raise ValueError("learn_lineage_middle_way_qi_authority_invalid")
    if middle_way.get("paramartha_non_reification_preserved") is not True:
        raise ValueError("learn_lineage_non_reification_missing")

    for field, expected in {
        "learn_state_digest": committed_learn_state.get("learn_state_digest"),
        "source_verify_state_digest": committed_learn_state.get(
            "source_verify_state_digest"
        ),
        "source_verification_evidence_digest": committed_learn_state.get(
            "source_verification_evidence_digest"
        ),
        "learning_delta_digest": committed_learn_state.get("learning_delta_digest"),
        "middle_way_report_digest": committed_learn_state.get(
            "middle_way_report_digest"
        ),
        "learning_route": committed_learn_state.get("route"),
        "mission_cycle_phase": "learn",
        "future_only": True,
        "memory_overwrite": False,
        "active_now": False,
        "replan_required": True,
    }.items():
        _require_equal(
            learn_phase_receipt, field, expected, "learn_lineage_phase_receipt"
        )

    learning_route = require_string(committed_learn_state.get("route"), "learning_route")
    allowed = PLANOS_CANDIDATE_TYPES_BY_LEARNING_ROUTE.get(learning_route)
    if allowed is None:
        raise ValueError("learn_lineage_learning_route_invalid")

    packet = {
        "version": COMPLETION_RECEIPT_VERSION,
        "learn_lineage_handoff_receipt_digest": handoff_receipt[
            "learn_lineage_handoff_receipt_digest"
        ],
        "verify_lineage_completion_receipt_digest": handoff_receipt[
            "verify_lineage_completion_receipt_digest"
        ],
        "observe_lineage_completion_receipt_digest": handoff_receipt[
            "observe_lineage_completion_receipt_digest"
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
        "committed_observe_state_digest": handoff_receipt[
            "committed_observe_state_digest"
        ],
        "committed_verify_state_digest": handoff_receipt[
            "committed_verify_state_digest"
        ],
        "committed_learn_state_digest": committed_learn_state[
            "learn_state_digest"
        ],
        "learn_phase_receipt_digest": learn_phase_receipt[
            "learn_phase_receipt_digest"
        ],
        "source_verification_route": handoff_receipt[
            "source_verification_route"
        ],
        "source_verification_evidence_digest": committed_learn_state[
            "source_verification_evidence_digest"
        ],
        "verification_criterion_digest": committed_learn_state[
            "verification_criterion_digest"
        ],
        "source_counterevidence_digest": committed_learn_state[
            "source_counterevidence_digest"
        ],
        "abstraction_packet_digest": committed_learn_state[
            "abstraction_packet_digest"
        ],
        "learning_challenge_packet_digest": committed_learn_state[
            "learning_challenge_packet_digest"
        ],
        "learning_delta_digest": committed_learn_state["learning_delta_digest"],
        "middle_way_report_digest": committed_learn_state[
            "middle_way_report_digest"
        ],
        "qi_process_history_digest": abstraction["qi_process_history_digest"],
        "learning_route": learning_route,
        "learning_kind": delta["learning_kind"],
        "target_scope": delta["target_scope"],
        "next_plan_basis_candidate_digest": learn_phase_receipt[
            "next_plan_basis_candidate_digest"
        ],
        "planos_candidate_type_allowlist": list(allowed),
        "learning_recorded": bool(committed_learn_state.get("learning_recorded")),
        "learning_debt_discharged": bool(
            committed_learn_state.get("learning_debt_discharged")
        ),
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
        "qi_context_only": True,
        "completed_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "planos_replan_input_digest": "",
        "learn_lineage_completion_receipt_digest": "",
    }
    packet["planos_replan_input_digest"] = planos_replan_input_digest(packet)
    packet["learn_lineage_completion_receipt_digest"] = completion_receipt_digest(packet)
    return packet


def validate_completion_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != COMPLETION_RECEIPT_VERSION:
            errors.append("learn_lineage_completion_version_invalid")
        if receipt.get(
            "learn_lineage_completion_receipt_digest"
        ) != completion_receipt_digest(receipt):
            errors.append("learn_lineage_completion_digest_invalid")
        if receipt.get("planos_replan_input_digest") != planos_replan_input_digest(
            receipt
        ):
            errors.append("learn_lineage_planos_replan_input_digest_invalid")
        for field in (
            "learn_lineage_handoff_receipt_digest",
            "verify_lineage_completion_receipt_digest",
            "observe_lineage_completion_receipt_digest",
            "act_lineage_completion_receipt_digest",
            "next_cycle_compiler_receipt_digest",
            "replan_phase_receipt_digest",
            "qi_condition_packet_digest",
            "decision_receipt_digest",
            "selected_candidate_digest",
            "selected_step_digest",
            "committed_act_state_digest",
            "committed_observe_state_digest",
            "committed_verify_state_digest",
            "committed_learn_state_digest",
            "learn_phase_receipt_digest",
            "source_verification_route",
            "source_verification_evidence_digest",
            "verification_criterion_digest",
            "source_counterevidence_digest",
            "abstraction_packet_digest",
            "learning_challenge_packet_digest",
            "learning_delta_digest",
            "middle_way_report_digest",
            "qi_process_history_digest",
            "learning_route",
            "learning_kind",
            "target_scope",
            "next_plan_basis_candidate_digest",
            "planos_replan_input_digest",
        ):
            require_string(receipt.get(field), field)
        route = receipt.get("learning_route")
        allowed = PLANOS_CANDIDATE_TYPES_BY_LEARNING_ROUTE.get(route)
        if allowed is None:
            errors.append("learn_lineage_completion_route_invalid")
        elif list(receipt.get("planos_candidate_type_allowlist", [])) != list(allowed):
            errors.append("learn_lineage_completion_planos_allowlist_invalid")
        for field, expected in {
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
            "qi_context_only": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"learn_lineage_completion_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("learn_lineage_completion_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("learn_lineage_completion_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
