from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_observe_os_lineage_kernel_v0_2 import (
    validate_completion_receipt as validate_observe_completion_receipt,
    validate_handoff_receipt as validate_observe_handoff_receipt,
)
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.kuuos_verify_os_types_v0_1 import (
    VERIFY_PHASE_RECEIPT_VERSION,
    verify_phase_receipt_digest,
)
from runtime.kuuos_verify_os_lineage_types_v0_2 import (
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


def build_verify_lineage_handoff_receipt(
    *,
    committed_observe_state: Mapping[str, Any],
    observe_lineage_handoff_receipt: Mapping[str, Any],
    observe_lineage_completion_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_cycle_index: int,
    mission_cycle_state_digest: str,
    verify_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    observe_errors = validate_observe_state(committed_observe_state)
    handoff_errors = validate_observe_handoff_receipt(
        observe_lineage_handoff_receipt
    )
    completion_errors = validate_observe_completion_receipt(
        observe_lineage_completion_receipt
    )
    if observe_errors:
        raise ValueError(
            "verify_lineage_observe_state_invalid:" + ";".join(observe_errors)
        )
    if handoff_errors:
        raise ValueError(
            "verify_lineage_observe_handoff_invalid:" + ";".join(handoff_errors)
        )
    if completion_errors:
        raise ValueError(
            "verify_lineage_observe_completion_invalid:"
            + ";".join(completion_errors)
        )
    if committed_observe_state.get("current_phase") != "commit":
        raise ValueError("verify_lineage_observe_state_not_committed")
    if committed_observe_state.get("route") == "PENDING":
        raise ValueError("verify_lineage_observe_route_pending")
    if committed_observe_state.get("observation_recorded") is not True:
        raise ValueError("verify_lineage_observation_missing")
    if committed_observe_state.get("verification_required") is not True:
        raise ValueError("verify_lineage_verification_debt_missing")

    _require_equal(
        observe_lineage_completion_receipt,
        "observe_lineage_handoff_receipt_digest",
        observe_lineage_handoff_receipt.get(
            "observe_lineage_handoff_receipt_digest"
        ),
        "verify_lineage_observe_completion",
    )
    for field, expected in {
        "committed_observe_state_digest": committed_observe_state.get(
            "observe_state_digest"
        ),
        "evidence_packet_digest": committed_observe_state.get(
            "evidence_packet_digest"
        ),
        "quality_report_digest": committed_observe_state.get(
            "quality_report_digest"
        ),
        "comparison_receipt_digest": committed_observe_state.get(
            "comparison_receipt_digest"
        ),
        "route": committed_observe_state.get("route"),
        "observation_recorded": True,
        "verification_required": True,
        "observation_not_verification": True,
        "source_lineage_preserved": True,
    }.items():
        _require_equal(
            observe_lineage_completion_receipt,
            field,
            expected,
            "verify_lineage_observe_completion",
        )

    for field, expected in {
        "committed_act_state_digest": committed_observe_state.get(
            "source_act_state_digest"
        ),
        "host_receipt_digest": committed_observe_state.get(
            "host_receipt_digest"
        ),
        "host_invocation_digest": committed_observe_state.get(
            "host_invocation_digest"
        ),
        "expected_observation_digest": committed_observe_state.get(
            "expected_observation_digest"
        ),
        "verification_criterion_digest": committed_observe_state.get(
            "verification_criterion_digest"
        ),
        "mission_contract_digest": committed_observe_state.get(
            "mission_contract_digest"
        ),
    }.items():
        _require_equal(
            observe_lineage_handoff_receipt,
            field,
            expected,
            "verify_lineage_observe_handoff",
        )

    if mission_cycle_phase != "verify":
        raise ValueError("verify_lineage_verify_phase_required")
    cycle = require_int(mission_cycle_cycle_index, "mission_cycle_cycle_index")
    expected_cycle = int(
        observe_lineage_handoff_receipt.get(
            "mission_cycle_cycle_index", -1
        )
    )
    if cycle != expected_cycle:
        raise ValueError("verify_lineage_cycle_mismatch")

    packet = {
        "version": HANDOFF_RECEIPT_VERSION,
        "lineage_id": observe_lineage_handoff_receipt["lineage_id"],
        "mission_contract_digest": observe_lineage_handoff_receipt[
            "mission_contract_digest"
        ],
        "observe_lineage_handoff_receipt_digest": observe_lineage_handoff_receipt[
            "observe_lineage_handoff_receipt_digest"
        ],
        "observe_lineage_completion_receipt_digest": observe_lineage_completion_receipt[
            "observe_lineage_completion_receipt_digest"
        ],
        "act_lineage_completion_receipt_digest": observe_lineage_completion_receipt[
            "act_lineage_completion_receipt_digest"
        ],
        "next_cycle_compiler_receipt_digest": observe_lineage_completion_receipt[
            "next_cycle_compiler_receipt_digest"
        ],
        "replan_phase_receipt_digest": observe_lineage_completion_receipt[
            "replan_phase_receipt_digest"
        ],
        "qi_condition_packet_digest": observe_lineage_completion_receipt[
            "qi_condition_packet_digest"
        ],
        "decision_receipt_digest": observe_lineage_completion_receipt[
            "decision_receipt_digest"
        ],
        "selected_candidate_digest": observe_lineage_completion_receipt[
            "selected_candidate_digest"
        ],
        "selected_step_digest": observe_lineage_completion_receipt[
            "selected_step_digest"
        ],
        "committed_act_state_digest": observe_lineage_completion_receipt[
            "committed_act_state_digest"
        ],
        "committed_observe_state_digest": committed_observe_state[
            "observe_state_digest"
        ],
        "observe_phase_receipt_digest": observe_lineage_completion_receipt[
            "observe_phase_receipt_digest"
        ],
        "source_observation_route": committed_observe_state["route"],
        "source_observation_debt_discharged": bool(
            committed_observe_state.get("observation_debt_discharged")
        ),
        "source_reobservation_required": bool(
            committed_observe_state.get("reobservation_required")
        ),
        "source_act_state_digest": committed_observe_state[
            "source_act_state_digest"
        ],
        "host_receipt_digest": committed_observe_state[
            "host_receipt_digest"
        ],
        "host_invocation_digest": committed_observe_state[
            "host_invocation_digest"
        ],
        "expected_observation_digest": committed_observe_state[
            "expected_observation_digest"
        ],
        "verification_criterion_digest": committed_observe_state[
            "verification_criterion_digest"
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
        "mission_cycle_phase": "verify",
        "mission_cycle_cycle_index": cycle,
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "verify_phase_event_digest": require_string(
            verify_phase_event_digest, "verify_phase_event_digest"
        ),
        "observation_recorded": True,
        "verification_required": True,
        "criterion_binding_required": True,
        "falsification_required": True,
        "independent_assessment_required": True,
        "verification_not_truth": True,
        "causal_attribution_not_granted": True,
        "learning_future_only": True,
        "single_use": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "verify_lineage_handoff_receipt_digest": "",
    }
    packet["verify_lineage_handoff_receipt_digest"] = handoff_receipt_digest(
        packet
    )
    return packet


def validate_handoff_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != HANDOFF_RECEIPT_VERSION:
            errors.append("verify_lineage_handoff_version_invalid")
        if receipt.get("verify_lineage_handoff_receipt_digest") != handoff_receipt_digest(
            receipt
        ):
            errors.append("verify_lineage_handoff_digest_invalid")
        for field in (
            "lineage_id",
            "mission_contract_digest",
            "observe_lineage_handoff_receipt_digest",
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
            "observe_phase_receipt_digest",
            "source_observation_route",
            "source_act_state_digest",
            "host_receipt_digest",
            "host_invocation_digest",
            "expected_observation_digest",
            "verification_criterion_digest",
            "evidence_packet_digest",
            "quality_report_digest",
            "comparison_receipt_digest",
            "mission_cycle_state_digest",
            "verify_phase_event_digest",
        ):
            require_string(receipt.get(field), field)
        require_int(
            receipt.get("mission_cycle_cycle_index"),
            "mission_cycle_cycle_index",
        )
        if receipt.get("mission_cycle_phase") != "verify":
            errors.append("verify_lineage_handoff_phase_invalid")
        for field, expected in {
            "observation_recorded": True,
            "verification_required": True,
            "criterion_binding_required": True,
            "falsification_required": True,
            "independent_assessment_required": True,
            "verification_not_truth": True,
            "causal_attribution_not_granted": True,
            "learning_future_only": True,
            "single_use": True,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"verify_lineage_handoff_{field}_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("verify_lineage_handoff_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("verify_lineage_handoff_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_verify_lineage_completion_receipt(
    *,
    handoff_receipt: Mapping[str, Any],
    committed_verify_state: Mapping[str, Any],
    verify_phase_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    handoff_errors = validate_handoff_receipt(handoff_receipt)
    verify_errors = validate_verify_state(committed_verify_state)
    if handoff_errors:
        raise ValueError("verify_lineage_handoff_invalid:" + ";".join(handoff_errors))
    if verify_errors:
        raise ValueError("verify_lineage_state_invalid:" + ";".join(verify_errors))
    if committed_verify_state.get("current_phase") != "commit":
        raise ValueError("verify_lineage_state_not_committed")
    if verify_phase_receipt.get("version") != VERIFY_PHASE_RECEIPT_VERSION:
        raise ValueError("verify_lineage_phase_receipt_version_invalid")
    if verify_phase_receipt.get("verify_phase_receipt_digest") != verify_phase_receipt_digest(
        verify_phase_receipt
    ):
        raise ValueError("verify_lineage_phase_receipt_digest_invalid")

    bindings = {
        "source_observe_state_digest": handoff_receipt.get(
            "committed_observe_state_digest"
        ),
        "source_observation_route": handoff_receipt.get(
            "source_observation_route"
        ),
        "source_observation_debt_discharged": handoff_receipt.get(
            "source_observation_debt_discharged"
        ),
        "source_reobservation_required": handoff_receipt.get(
            "source_reobservation_required"
        ),
        "source_act_state_digest": handoff_receipt.get(
            "source_act_state_digest"
        ),
        "host_receipt_digest": handoff_receipt.get("host_receipt_digest"),
        "host_invocation_digest": handoff_receipt.get(
            "host_invocation_digest"
        ),
        "expected_observation_digest": handoff_receipt.get(
            "expected_observation_digest"
        ),
        "verification_criterion_digest": handoff_receipt.get(
            "verification_criterion_digest"
        ),
        "evidence_packet_digest": handoff_receipt.get(
            "evidence_packet_digest"
        ),
        "quality_report_digest": handoff_receipt.get(
            "quality_report_digest"
        ),
        "comparison_receipt_digest": handoff_receipt.get(
            "comparison_receipt_digest"
        ),
        "mission_contract_digest": handoff_receipt.get(
            "mission_contract_digest"
        ),
    }
    for field, expected in bindings.items():
        _require_equal(
            committed_verify_state, field, expected, "verify_lineage_state"
        )

    challenge = committed_verify_state.get("challenge_packet", {})
    if not isinstance(challenge, Mapping):
        raise ValueError("verify_lineage_challenge_packet_missing")
    if not list(challenge.get("falsification_attempt_digests", [])):
        raise ValueError("verify_lineage_falsification_attempt_missing")
    if not list(challenge.get("independent_assessor_ids", [])):
        raise ValueError("verify_lineage_independent_assessment_missing")
    if challenge.get("counterevidence_preserved") is not True:
        raise ValueError("verify_lineage_counterevidence_not_preserved")

    for field, expected in {
        "verify_state_digest": committed_verify_state.get(
            "verify_state_digest"
        ),
        "source_observe_state_digest": committed_verify_state.get(
            "source_observe_state_digest"
        ),
        "source_act_state_digest": committed_verify_state.get(
            "source_act_state_digest"
        ),
        "verification_criterion_digest": committed_verify_state.get(
            "verification_criterion_digest"
        ),
        "verification_evidence_digest": committed_verify_state.get(
            "verification_evidence_digest"
        ),
        "adjudication_receipt_digest": committed_verify_state.get(
            "adjudication_receipt_digest"
        ),
        "route": committed_verify_state.get("route"),
        "verification_debt_discharged": committed_verify_state.get(
            "verification_debt_discharged"
        ),
        "verification_required": committed_verify_state.get(
            "verification_required"
        ),
        "reobservation_required": committed_verify_state.get(
            "reobservation_required"
        ),
        "corrective_action_required": committed_verify_state.get(
            "corrective_action_required"
        ),
        "learning_required": True,
        "mission_cycle_phase": "verify",
        "verification_not_truth": True,
        "causal_attribution_not_granted": True,
    }.items():
        _require_equal(
            verify_phase_receipt,
            field,
            expected,
            "verify_lineage_phase_receipt",
        )

    packet = {
        "version": COMPLETION_RECEIPT_VERSION,
        "verify_lineage_handoff_receipt_digest": handoff_receipt[
            "verify_lineage_handoff_receipt_digest"
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
        "decision_receipt_digest": handoff_receipt[
            "decision_receipt_digest"
        ],
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
        "committed_verify_state_digest": committed_verify_state[
            "verify_state_digest"
        ],
        "verify_phase_receipt_digest": verify_phase_receipt[
            "verify_phase_receipt_digest"
        ],
        "verification_criterion_digest": committed_verify_state[
            "verification_criterion_digest"
        ],
        "criterion_packet_digest": committed_verify_state[
            "criterion_packet_digest"
        ],
        "challenge_packet_digest": committed_verify_state[
            "challenge_packet_digest"
        ],
        "corroboration_report_digest": committed_verify_state[
            "corroboration_report_digest"
        ],
        "adjudication_receipt_digest": committed_verify_state[
            "adjudication_receipt_digest"
        ],
        "verification_evidence_digest": committed_verify_state[
            "verification_evidence_digest"
        ],
        "evidence_packet_digest": committed_verify_state[
            "evidence_packet_digest"
        ],
        "comparison_receipt_digest": committed_verify_state[
            "comparison_receipt_digest"
        ],
        "route": committed_verify_state["route"],
        "verdict": verify_phase_receipt["verdict"],
        "verification_recorded": bool(
            committed_verify_state.get("verification_recorded")
        ),
        "verification_debt_discharged": bool(
            committed_verify_state.get("verification_debt_discharged")
        ),
        "verification_required": bool(
            committed_verify_state.get("verification_required")
        ),
        "reobservation_required": bool(
            committed_verify_state.get("reobservation_required")
        ),
        "corrective_action_required": bool(
            committed_verify_state.get("corrective_action_required")
        ),
        "learning_required": True,
        "learning_must_be_future_only": True,
        "counterevidence_preserved": True,
        "falsification_attempted": True,
        "independent_assessment_preserved": True,
        "verification_not_truth": True,
        "causal_attribution_not_granted": True,
        "automatic_learning": False,
        "completed_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "verify_lineage_completion_receipt_digest": "",
    }
    packet["verify_lineage_completion_receipt_digest"] = completion_receipt_digest(
        packet
    )
    return packet


def validate_completion_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != COMPLETION_RECEIPT_VERSION:
            errors.append("verify_lineage_completion_version_invalid")
        if receipt.get(
            "verify_lineage_completion_receipt_digest"
        ) != completion_receipt_digest(receipt):
            errors.append("verify_lineage_completion_digest_invalid")
        for field in (
            "verify_lineage_handoff_receipt_digest",
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
            "verification_criterion_digest",
            "criterion_packet_digest",
            "challenge_packet_digest",
            "corroboration_report_digest",
            "adjudication_receipt_digest",
            "verification_evidence_digest",
            "evidence_packet_digest",
            "comparison_receipt_digest",
            "route",
            "verdict",
        ):
            require_string(receipt.get(field), field)
        for field, expected in {
            "verification_recorded": True,
            "learning_required": True,
            "learning_must_be_future_only": True,
            "counterevidence_preserved": True,
            "falsification_attempted": True,
            "independent_assessment_preserved": True,
            "verification_not_truth": True,
            "causal_attribution_not_granted": True,
            "automatic_learning": False,
        }.items():
            if receipt.get(field) != expected:
                errors.append(f"verify_lineage_completion_{field}_invalid")
        if receipt.get("route") == "VERIFICATION_PASSED":
            if receipt.get("verification_debt_discharged") is not True:
                errors.append("verify_lineage_passed_debt_not_discharged")
            if receipt.get("verification_required") is not False:
                errors.append("verify_lineage_passed_verification_still_required")
        elif receipt.get("route") == "VERIFICATION_FAILED":
            if receipt.get("corrective_action_required") is not True:
                errors.append("verify_lineage_failed_corrective_action_missing")
        elif receipt.get("route") == "VERIFICATION_INDETERMINATE":
            if receipt.get("verification_required") is not True:
                errors.append("verify_lineage_indeterminate_debt_lost")
            if receipt.get("reobservation_required") is not True:
                errors.append("verify_lineage_indeterminate_reobservation_missing")
        else:
            errors.append("verify_lineage_completion_route_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("verify_lineage_completion_authority_invalid")
        if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("verify_lineage_completion_boundary_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
