from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_observe_os_types_v0_1 import (
    COMPARISON_RECEIPT_VERSION,
    comparison_receipt_digest,
)
from runtime.kuuos_verify_os_types_v0_1 import (
    ADJUDICATION_RECEIPT_VERSION,
    ADJUDICATION_VERDICTS,
    APPLY_RESULT_VERSION,
    CHALLENGE_PACKET_VERSION,
    CORROBORATION_REPORT_VERSION,
    CRITERION_PACKET_VERSION,
    CRITERION_TYPES,
    EVENT_VERSION,
    NON_AUTHORITY_FLAGS,
    PHASES,
    REQUIRED_BOUNDARY,
    ROUTES,
    STATE_VERSION,
    VERIFY_PHASE_RECEIPT_VERSION,
    adjudication_receipt_digest,
    apply_result_digest,
    challenge_packet_digest,
    copy_boundary,
    copy_non_authority,
    corroboration_report_digest,
    criterion_packet_digest,
    event_digest,
    next_phase,
    require_bool,
    require_int,
    require_string,
    state_digest,
    unit_number,
    unique_strings,
    verify_phase_receipt_digest,
)


def _seal(packet: dict[str, Any], field: str, supplied: Any = None) -> dict[str, Any]:
    packet[field] = ""
    expected = sha({key: value for key, value in packet.items() if key != field})
    packet[field] = expected
    if supplied not in (None, "", expected):
        raise ValueError(f"{field}_invalid")
    return packet


def build_initial_verify_state(
    *, verify_id: str, observe_state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    errors = validate_observe_state(observe_state)
    if errors:
        raise ValueError("invalid_source_observe_state:" + ";".join(errors))
    if observe_state.get("current_phase") != "commit":
        raise ValueError("source_observe_not_committed")
    if observe_state.get("route") == "PENDING":
        raise ValueError("source_observe_route_pending")
    if observe_state.get("observation_recorded") is not True:
        raise ValueError("source_observation_not_recorded")
    if observe_state.get("verification_required") is not True:
        raise ValueError("source_verification_debt_missing")
    comparison = observe_state.get("comparison_receipt")
    if not isinstance(comparison, Mapping):
        raise ValueError("source_comparison_receipt_missing")
    if comparison.get("version") != COMPARISON_RECEIPT_VERSION:
        raise ValueError("source_comparison_receipt_version_invalid")
    if comparison.get("comparison_receipt_digest") != comparison_receipt_digest(comparison):
        raise ValueError("source_comparison_receipt_digest_invalid")
    if comparison.get("comparison_receipt_digest") != observe_state.get("comparison_receipt_digest"):
        raise ValueError("source_comparison_receipt_binding_mismatch")

    state = {
        "version": STATE_VERSION,
        "verify_id": require_string(verify_id, "verify_id"),
        "lineage_id": require_string(observe_state.get("lineage_id"), "lineage_id"),
        "source_observe_id": require_string(observe_state.get("observe_id"), "source_observe_id"),
        "source_observe_state_digest": require_string(
            observe_state.get("observe_state_digest"), "source_observe_state_digest"
        ),
        "source_observe_version": require_int(
            observe_state.get("observe_version"), "source_observe_version"
        ),
        "source_observe_updated_at_ms": require_int(
            observe_state.get("updated_at_ms"), "source_observe_updated_at_ms"
        ),
        "source_observation_route": require_string(
            observe_state.get("route"), "source_observation_route"
        ),
        "source_observation_debt_discharged": require_bool(
            observe_state.get("observation_debt_discharged"),
            "source_observation_debt_discharged",
        ),
        "source_reobservation_required": require_bool(
            observe_state.get("reobservation_required"), "source_reobservation_required"
        ),
        "source_act_state_digest": require_string(
            observe_state.get("source_act_state_digest"), "source_act_state_digest"
        ),
        "host_receipt_digest": require_string(
            observe_state.get("host_receipt_digest"), "host_receipt_digest"
        ),
        "host_invocation_digest": require_string(
            observe_state.get("host_invocation_digest"), "host_invocation_digest"
        ),
        "expected_observation_digest": require_string(
            observe_state.get("expected_observation_digest"), "expected_observation_digest"
        ),
        "verification_criterion_digest": require_string(
            observe_state.get("verification_criterion_digest"), "verification_criterion_digest"
        ),
        "evidence_packet_digest": require_string(
            observe_state.get("evidence_packet_digest"), "evidence_packet_digest"
        ),
        "quality_report_digest": require_string(
            observe_state.get("quality_report_digest"), "quality_report_digest"
        ),
        "comparison_receipt_digest": require_string(
            observe_state.get("comparison_receipt_digest"), "comparison_receipt_digest"
        ),
        "mission_contract_digest": require_string(
            observe_state.get("mission_contract_digest"), "mission_contract_digest"
        ),
        "current_phase": "bind",
        "route": "PENDING",
        "event_index": 0,
        "verify_version": 0,
        "committed_records": 0,
        "updated_at_ms": require_int(now_ms, "now_ms"),
        "predecessor_verify_state_digest": "",
        "verify_state_digest": "",
        "criterion_packet": {},
        "criterion_packet_digest": "",
        "challenge_packet": {},
        "challenge_packet_digest": "",
        "corroboration_report": {},
        "corroboration_report_digest": "",
        "adjudication_receipt": {},
        "adjudication_receipt_digest": "",
        "verification_evidence_digest": "",
        "verification_recorded": False,
        "verification_debt_discharged": False,
        "verification_required": True,
        "reobservation_required": bool(observe_state.get("reobservation_required", False)),
        "corrective_action_required": False,
        "learning_required": False,
        "automatic_truth_promotion": False,
        "automatic_belief_update": False,
        "automatic_plan_completion": False,
        "automatic_rollback": False,
        "automatic_causal_attribution": False,
        "processed_event_digests": [],
        "event_history": [],
        "record_summaries": [],
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
    }
    state["verify_state_digest"] = state_digest(state)
    return state


def validate_verify_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("verify_state_version_invalid")
        for field in (
            "verify_id",
            "lineage_id",
            "source_observe_id",
            "source_observe_state_digest",
            "source_observation_route",
            "source_act_state_digest",
            "host_receipt_digest",
            "host_invocation_digest",
            "expected_observation_digest",
            "verification_criterion_digest",
            "evidence_packet_digest",
            "quality_report_digest",
            "comparison_receipt_digest",
            "mission_contract_digest",
        ):
            require_string(state.get(field), field)
        for field in (
            "source_observe_version",
            "source_observe_updated_at_ms",
            "event_index",
            "verify_version",
            "committed_records",
            "updated_at_ms",
        ):
            require_int(state.get(field), field)
        for field in (
            "source_observation_debt_discharged",
            "source_reobservation_required",
            "verification_recorded",
            "verification_debt_discharged",
            "verification_required",
            "reobservation_required",
            "corrective_action_required",
            "learning_required",
        ):
            require_bool(state.get(field), field)
        if state.get("current_phase") not in PHASES:
            errors.append("verify_state_phase_invalid")
        if state.get("route") not in ROUTES:
            errors.append("verify_state_route_invalid")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("verify_state_authority_escalation")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("verify_state_boundary_invalid")
        if state.get("verify_state_digest") != state_digest(state):
            errors.append("verify_state_digest_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("verify_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("verify_event_history_count_mismatch")
        for field in (
            "automatic_truth_promotion",
            "automatic_belief_update",
            "automatic_plan_completion",
            "automatic_rollback",
            "automatic_causal_attribution",
        ):
            if state.get(field) is not False:
                errors.append(f"verify_{field}_forbidden")
        if state.get("verification_recorded") is True:
            route = state.get("route")
            if route == "PENDING":
                errors.append("verify_recorded_route_pending")
            discharged = state.get("verification_debt_discharged") is True
            required = state.get("verification_required") is True
            reobserve = state.get("reobservation_required") is True
            corrective = state.get("corrective_action_required") is True
            if state.get("learning_required") is not True:
                errors.append("verify_learning_debt_missing")
            if route == "VERIFICATION_PASSED":
                if not discharged or required or reobserve or corrective:
                    errors.append("verify_passed_debt_semantics_invalid")
            elif route == "VERIFICATION_FAILED":
                if not discharged or required or reobserve or not corrective:
                    errors.append("verify_failed_debt_semantics_invalid")
            elif route == "VERIFICATION_INDETERMINATE":
                if discharged or not required or not reobserve or corrective:
                    errors.append("verify_indeterminate_debt_semantics_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_verify_event(
    *,
    state: Mapping[str, Any],
    target_phase: str,
    artifact_digest: str,
    payload: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    event = {
        "version": EVENT_VERSION,
        "verify_id": require_string(state.get("verify_id"), "verify_id"),
        "lineage_id": require_string(state.get("lineage_id"), "lineage_id"),
        "expected_verify_state_digest": require_string(
            state.get("verify_state_digest"), "expected_verify_state_digest"
        ),
        "source_phase": require_string(state.get("current_phase"), "source_phase"),
        "target_phase": require_string(target_phase, "target_phase"),
        "event_index": require_int(state.get("event_index"), "event_index") + 1,
        "artifact_digest": require_string(artifact_digest, "artifact_digest"),
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "verify_event_digest": "",
    }
    event["verify_event_digest"] = event_digest(event)
    return event


def build_criterion_packet(
    *,
    state: Mapping[str, Any],
    criterion_type: str,
    evaluation_method_digest: str,
    success_condition_digest: str,
    failure_condition_digest: str,
    falsification_condition_digest: str,
    evidence_requirements_digest: str,
    minimum_independent_assessors: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "bind":
        raise ValueError("criterion_requires_bound_state")
    normalized_type = require_string(criterion_type, "criterion_type")
    if normalized_type not in CRITERION_TYPES:
        raise ValueError("criterion_type_invalid")
    minimum = require_int(minimum_independent_assessors, "minimum_independent_assessors")
    if minimum < 1:
        raise ValueError("minimum_independent_assessors_positive_required")
    packet = {
        "version": CRITERION_PACKET_VERSION,
        "verify_id": state["verify_id"],
        "source_observe_state_digest": state["source_observe_state_digest"],
        "verification_criterion_digest": state["verification_criterion_digest"],
        "criterion_type": normalized_type,
        "evaluation_method_digest": require_string(
            evaluation_method_digest, "evaluation_method_digest"
        ),
        "success_condition_digest": require_string(
            success_condition_digest, "success_condition_digest"
        ),
        "failure_condition_digest": require_string(
            failure_condition_digest, "failure_condition_digest"
        ),
        "falsification_condition_digest": require_string(
            falsification_condition_digest, "falsification_condition_digest"
        ),
        "evidence_requirements_digest": require_string(
            evidence_requirements_digest, "evidence_requirements_digest"
        ),
        "minimum_independent_assessors": minimum,
        "criterion_defined_before_adjudication": True,
        "permits_causal_attribution": False,
        "criterion_packet_digest": "",
    }
    packet["criterion_packet_digest"] = criterion_packet_digest(packet)
    return packet


def build_challenge_packet(
    *,
    state: Mapping[str, Any],
    counterevidence_digests: list[str],
    falsification_attempt_digests: list[str],
    independent_assessor_ids: list[str],
    assessor_receipt_digests: list[str],
    conflict_disclosure_digest: str,
    falsifier_triggered: bool,
) -> dict[str, Any]:
    if state.get("current_phase") != "criterion":
        raise ValueError("challenge_requires_criterion_state")
    assessors = unique_strings(independent_assessor_ids, "independent_assessor_ids")
    receipts = unique_strings(assessor_receipt_digests, "assessor_receipt_digests")
    if len(assessors) != len(receipts):
        raise ValueError("assessor_receipt_count_mismatch")
    minimum = int(state["criterion_packet"]["minimum_independent_assessors"])
    if len(assessors) < minimum:
        raise ValueError("independent_assessors_insufficient")
    packet = {
        "version": CHALLENGE_PACKET_VERSION,
        "verify_id": state["verify_id"],
        "source_observe_state_digest": state["source_observe_state_digest"],
        "criterion_packet_digest": state["criterion_packet_digest"],
        "counterevidence_digests": unique_strings(
            counterevidence_digests, "counterevidence_digests", allow_empty=True
        ),
        "falsification_attempt_digests": unique_strings(
            falsification_attempt_digests, "falsification_attempt_digests"
        ),
        "independent_assessor_ids": assessors,
        "assessor_receipt_digests": receipts,
        "conflict_disclosure_digest": require_string(
            conflict_disclosure_digest, "conflict_disclosure_digest"
        ),
        "falsifier_triggered": require_bool(falsifier_triggered, "falsifier_triggered"),
        "challenge_complete": True,
        "counterevidence_preserved": True,
        "challenge_packet_digest": "",
    }
    packet["challenge_packet_digest"] = challenge_packet_digest(packet)
    return packet


def build_adjudication_receipt(
    *,
    state: Mapping[str, Any],
    adjudication_id: str,
    verdict: str,
    criterion_satisfied: bool,
    adjudication_method_digest: str,
    rationale_digest: str,
    adjudicated_at_ms: int,
) -> dict[str, Any]:
    if state.get("current_phase") != "corroborate":
        raise ValueError("adjudication_requires_corroborated_state")
    normalized = require_string(verdict, "verdict")
    if normalized not in ADJUDICATION_VERDICTS:
        raise ValueError("adjudication_verdict_invalid")
    packet = {
        "version": ADJUDICATION_RECEIPT_VERSION,
        "adjudication_id": require_string(adjudication_id, "adjudication_id"),
        "verify_id": state["verify_id"],
        "source_observe_state_digest": state["source_observe_state_digest"],
        "source_observation_route": state["source_observation_route"],
        "verification_criterion_digest": state["verification_criterion_digest"],
        "criterion_packet_digest": state["criterion_packet_digest"],
        "challenge_packet_digest": state["challenge_packet_digest"],
        "corroboration_report_digest": state["corroboration_report_digest"],
        "evidence_packet_digest": state["evidence_packet_digest"],
        "comparison_receipt_digest": state["comparison_receipt_digest"],
        "verdict": normalized,
        "criterion_satisfied": require_bool(criterion_satisfied, "criterion_satisfied"),
        "falsifier_triggered": bool(state["challenge_packet"]["falsifier_triggered"]),
        "adjudication_method_digest": require_string(
            adjudication_method_digest, "adjudication_method_digest"
        ),
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "adjudicated_at_ms": require_int(adjudicated_at_ms, "adjudicated_at_ms"),
        "verification_is_absolute_truth": False,
        "causal_attribution_granted": False,
        "adjudication_receipt_digest": "",
    }
    packet["adjudication_receipt_digest"] = adjudication_receipt_digest(packet)
    return packet


def build_verify_phase_receipt(
    *,
    state: Mapping[str, Any],
    mission_cycle_state_digest: str,
    verify_phase_event_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    errors = validate_verify_state(state)
    if errors:
        raise ValueError("invalid_verify_state:" + ";".join(errors))
    if state.get("current_phase") != "commit" or state.get("route") == "PENDING":
        raise ValueError("verify_phase_receipt_requires_committed_verification")
    verdict_map = {
        "VERIFICATION_PASSED": "passed",
        "VERIFICATION_FAILED": "failed",
        "VERIFICATION_INDETERMINATE": "indeterminate",
    }
    packet = {
        "version": VERIFY_PHASE_RECEIPT_VERSION,
        "verify_id": state["verify_id"],
        "verify_state_digest": state["verify_state_digest"],
        "source_observe_state_digest": state["source_observe_state_digest"],
        "source_act_state_digest": state["source_act_state_digest"],
        "verification_criterion_digest": state["verification_criterion_digest"],
        "verification_evidence_digest": state["verification_evidence_digest"],
        "adjudication_receipt_digest": state["adjudication_receipt_digest"],
        "route": state["route"],
        "verdict": verdict_map[state["route"]],
        "verification_debt_discharged": state["verification_debt_discharged"],
        "verification_required": state["verification_required"],
        "reobservation_required": state["reobservation_required"],
        "corrective_action_required": state["corrective_action_required"],
        "learning_required": True,
        "mission_cycle_phase": "verify",
        "mission_cycle_state_digest": require_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "verify_phase_event_digest": require_string(
            verify_phase_event_digest, "verify_phase_event_digest"
        ),
        "verification_not_truth": True,
        "causal_attribution_not_granted": True,
        "issued_at_ms": require_int(now_ms, "now_ms"),
        "non_authority": copy_non_authority(),
        "verify_phase_receipt_digest": "",
    }
    packet["verify_phase_receipt_digest"] = verify_phase_receipt_digest(packet)
    return packet


def _validate_event_base(state: Mapping[str, Any], event: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("verify_event_version_invalid")
    if event.get("verify_id") != state.get("verify_id"):
        errors.append("verify_event_id_mismatch")
    if event.get("lineage_id") != state.get("lineage_id"):
        errors.append("verify_event_lineage_mismatch")
    if event.get("verify_event_digest") != event_digest(event):
        errors.append("verify_event_digest_invalid")
    if dict(event.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
        errors.append("verify_event_authority_escalation")
    source = str(event.get("source_phase", ""))
    if source != state.get("current_phase"):
        errors.append("verify_event_source_phase_stale")
    if event.get("target_phase") != next_phase(source):
        errors.append("verify_event_phase_order_invalid")
    if event.get("event_index") != int(state.get("event_index", -1)) + 1:
        errors.append("verify_event_index_invalid")
    if event.get("expected_verify_state_digest") != state.get("verify_state_digest"):
        errors.append("verify_event_state_digest_stale")
    if int(event.get("created_at_ms", -1)) < int(state.get("updated_at_ms", 0)):
        errors.append("verify_event_time_regression")
    return errors


def _normalize_corroboration(state: Mapping[str, Any], raw: Mapping[str, Any]) -> dict[str, Any]:
    report = {
        "version": CORROBORATION_REPORT_VERSION,
        "verify_id": state["verify_id"],
        "source_observe_state_digest": state["source_observe_state_digest"],
        "criterion_packet_digest": state["criterion_packet_digest"],
        "challenge_packet_digest": state["challenge_packet_digest"],
        "evidence_packet_digest": state["evidence_packet_digest"],
        "quality_report_digest": state["quality_report_digest"],
        "comparison_receipt_digest": state["comparison_receipt_digest"],
        "evidence_sufficiency": unit_number(raw.get("evidence_sufficiency"), "evidence_sufficiency"),
        "assessor_independence": unit_number(raw.get("assessor_independence"), "assessor_independence"),
        "provenance_integrity": unit_number(raw.get("provenance_integrity"), "provenance_integrity"),
        "method_reproducibility": unit_number(raw.get("method_reproducibility"), "method_reproducibility"),
        "criterion_coverage": unit_number(raw.get("criterion_coverage"), "criterion_coverage"),
        "unresolved_conflict": require_bool(raw.get("unresolved_conflict"), "unresolved_conflict"),
        "corroboration_method_digest": require_string(
            raw.get("corroboration_method_digest"), "corroboration_method_digest"
        ),
        "corroboration_report_digest": "",
    }
    directional = state["source_observation_route"] in {
        "OBSERVATION_MATCHED",
        "OBSERVATION_DIVERGENT",
    }
    report["admissible_for_conclusive_verdict"] = bool(
        directional
        and state["source_observation_debt_discharged"] is True
        and state["source_reobservation_required"] is False
        and report["evidence_sufficiency"] >= 0.75
        and report["assessor_independence"] >= 0.75
        and report["provenance_integrity"] >= 0.8
        and report["method_reproducibility"] >= 0.7
        and report["criterion_coverage"] >= 0.8
        and report["unresolved_conflict"] is False
    )
    return _seal(report, "corroboration_report_digest", raw.get("corroboration_report_digest"))


def _apply_payload(state: dict[str, Any], phase: str, payload: Mapping[str, Any]) -> None:
    if phase == "criterion":
        packet = payload.get("criterion_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("criterion_packet_required")
        if packet.get("version") != CRITERION_PACKET_VERSION:
            raise ValueError("criterion_packet_version_invalid")
        if packet.get("criterion_packet_digest") != criterion_packet_digest(packet):
            raise ValueError("criterion_packet_digest_invalid")
        bindings = {
            "verify_id": state["verify_id"],
            "source_observe_state_digest": state["source_observe_state_digest"],
            "verification_criterion_digest": state["verification_criterion_digest"],
        }
        for field, expected in bindings.items():
            if packet.get(field) != expected:
                raise ValueError(f"criterion_packet_{field}_mismatch")
        if packet.get("criterion_type") not in CRITERION_TYPES:
            raise ValueError("criterion_type_invalid")
        if int(packet.get("minimum_independent_assessors", 0)) < 1:
            raise ValueError("minimum_independent_assessors_positive_required")
        if packet.get("criterion_defined_before_adjudication") is not True:
            raise ValueError("criterion_must_precede_adjudication")
        if packet.get("permits_causal_attribution") is not False:
            raise ValueError("criterion_causal_attribution_forbidden")
        state["criterion_packet"] = deepcopy(dict(packet))
        state["criterion_packet_digest"] = packet["criterion_packet_digest"]
        return

    if phase == "challenge":
        packet = payload.get("challenge_packet")
        if not isinstance(packet, Mapping):
            raise ValueError("challenge_packet_required")
        if packet.get("version") != CHALLENGE_PACKET_VERSION:
            raise ValueError("challenge_packet_version_invalid")
        if packet.get("challenge_packet_digest") != challenge_packet_digest(packet):
            raise ValueError("challenge_packet_digest_invalid")
        bindings = {
            "verify_id": state["verify_id"],
            "source_observe_state_digest": state["source_observe_state_digest"],
            "criterion_packet_digest": state["criterion_packet_digest"],
        }
        for field, expected in bindings.items():
            if packet.get(field) != expected:
                raise ValueError(f"challenge_packet_{field}_mismatch")
        attempts = unique_strings(packet.get("falsification_attempt_digests"), "falsification_attempt_digests")
        assessors = unique_strings(packet.get("independent_assessor_ids"), "independent_assessor_ids")
        receipts = unique_strings(packet.get("assessor_receipt_digests"), "assessor_receipt_digests")
        unique_strings(packet.get("counterevidence_digests"), "counterevidence_digests", allow_empty=True)
        if not attempts:
            raise ValueError("falsification_attempt_required")
        if len(assessors) != len(receipts):
            raise ValueError("assessor_receipt_count_mismatch")
        minimum = int(state["criterion_packet"]["minimum_independent_assessors"])
        if len(assessors) < minimum:
            raise ValueError("independent_assessors_insufficient")
        if packet.get("challenge_complete") is not True:
            raise ValueError("challenge_complete_required")
        if packet.get("counterevidence_preserved") is not True:
            raise ValueError("counterevidence_preservation_required")
        require_bool(packet.get("falsifier_triggered"), "falsifier_triggered")
        require_string(packet.get("conflict_disclosure_digest"), "conflict_disclosure_digest")
        state["challenge_packet"] = deepcopy(dict(packet))
        state["challenge_packet_digest"] = packet["challenge_packet_digest"]
        return

    if phase == "corroborate":
        raw = payload.get("corroboration_report")
        if not isinstance(raw, Mapping):
            raise ValueError("corroboration_report_required")
        report = _normalize_corroboration(state, raw)
        state["corroboration_report"] = report
        state["corroboration_report_digest"] = report["corroboration_report_digest"]
        return

    if phase == "adjudicate":
        receipt = payload.get("adjudication_receipt")
        if not isinstance(receipt, Mapping):
            raise ValueError("adjudication_receipt_required")
        if receipt.get("version") != ADJUDICATION_RECEIPT_VERSION:
            raise ValueError("adjudication_receipt_version_invalid")
        if receipt.get("adjudication_receipt_digest") != adjudication_receipt_digest(receipt):
            raise ValueError("adjudication_receipt_digest_invalid")
        bindings = {
            "verify_id": state["verify_id"],
            "source_observe_state_digest": state["source_observe_state_digest"],
            "source_observation_route": state["source_observation_route"],
            "verification_criterion_digest": state["verification_criterion_digest"],
            "criterion_packet_digest": state["criterion_packet_digest"],
            "challenge_packet_digest": state["challenge_packet_digest"],
            "corroboration_report_digest": state["corroboration_report_digest"],
            "evidence_packet_digest": state["evidence_packet_digest"],
            "comparison_receipt_digest": state["comparison_receipt_digest"],
        }
        for field, expected in bindings.items():
            if receipt.get(field) != expected:
                raise ValueError(f"adjudication_receipt_{field}_mismatch")
        if receipt.get("verification_is_absolute_truth") is not False:
            raise ValueError("verification_truth_claim_forbidden")
        if receipt.get("causal_attribution_granted") is not False:
            raise ValueError("verification_causal_attribution_forbidden")
        verdict = str(receipt.get("verdict", ""))
        if verdict not in ADJUDICATION_VERDICTS:
            raise ValueError("adjudication_verdict_invalid")
        criterion_satisfied = require_bool(receipt.get("criterion_satisfied"), "criterion_satisfied")
        falsifier = require_bool(receipt.get("falsifier_triggered"), "falsifier_triggered")
        if falsifier != bool(state["challenge_packet"]["falsifier_triggered"]):
            raise ValueError("adjudication_falsifier_binding_mismatch")
        admissible = bool(state["corroboration_report"].get("admissible_for_conclusive_verdict", False))
        route = state["source_observation_route"]
        if verdict == "PASSED":
            if not admissible:
                raise ValueError("passed_requires_admissible_corroboration")
            if route != "OBSERVATION_MATCHED":
                raise ValueError("passed_requires_matched_observation")
            if criterion_satisfied is not True:
                raise ValueError("passed_requires_criterion_satisfied")
            if falsifier is True:
                raise ValueError("passed_forbids_triggered_falsifier")
            state["route"] = "VERIFICATION_PASSED"
            state["verification_debt_discharged"] = True
            state["verification_required"] = False
            state["reobservation_required"] = False
            state["corrective_action_required"] = False
        elif verdict == "FAILED":
            if not admissible:
                raise ValueError("failed_requires_admissible_corroboration")
            failure_basis = route == "OBSERVATION_DIVERGENT" or criterion_satisfied is False or falsifier is True
            if not failure_basis:
                raise ValueError("failed_requires_conclusive_failure_basis")
            state["route"] = "VERIFICATION_FAILED"
            state["verification_debt_discharged"] = True
            state["verification_required"] = False
            state["reobservation_required"] = False
            state["corrective_action_required"] = True
        else:
            if admissible:
                raise ValueError("indeterminate_requires_nonadmissible_corroboration")
            state["route"] = "VERIFICATION_INDETERMINATE"
            state["verification_debt_discharged"] = False
            state["verification_required"] = True
            state["reobservation_required"] = True
            state["corrective_action_required"] = False
        state["adjudication_receipt"] = deepcopy(dict(receipt))
        state["adjudication_receipt_digest"] = receipt["adjudication_receipt_digest"]
        state["verification_evidence_digest"] = sha(
            {
                "source_observe_state_digest": state["source_observe_state_digest"],
                "criterion_packet_digest": state["criterion_packet_digest"],
                "challenge_packet_digest": state["challenge_packet_digest"],
                "corroboration_report_digest": state["corroboration_report_digest"],
                "adjudication_receipt_digest": state["adjudication_receipt_digest"],
            }
        )
        state["verification_recorded"] = True
        state["learning_required"] = True
        return

    if phase == "commit":
        required = {
            "verification_not_truth": True,
            "causal_attribution_not_granted": True,
            "counterevidence_preserved": True,
            "learning_required": True,
            "memory_overwrite": False,
            "automatic_truth_promotion": False,
            "automatic_belief_update": False,
            "automatic_plan_completion": False,
            "automatic_rollback": False,
            "automatic_causal_attribution": False,
        }
        for field, expected in required.items():
            if payload.get(field) != expected:
                raise ValueError(f"verify_commit_{field}_invalid")
        if dict(payload.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            raise ValueError("verify_commit_authority_escalation")
        if state["route"] == "PENDING" or not state["verification_recorded"]:
            raise ValueError("verify_adjudication_not_recorded")
        return

    raise ValueError("verify_target_phase_unsupported")


def _result(
    *, status: str, state: Mapping[str, Any], event_id: str, predecessor: str, errors: list[str]
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "verify_event_digest": event_id,
        "predecessor_verify_state_digest": predecessor,
        "result_verify_state_digest": state["verify_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "verify_apply_result_digest": "",
    }
    packet["verify_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_verify_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_verify_state(state)
    if state_errors:
        raise ValueError("invalid_verify_state:" + ";".join(state_errors))
    event_id = str(event.get("verify_event_digest", ""))
    predecessor = str(state["verify_state_digest"])
    if event_id and event_id in set(state.get("processed_event_digests", [])):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors = _validate_event_base(state, event)
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    next_state = deepcopy(dict(state))
    phase = str(event["target_phase"])
    try:
        _apply_payload(next_state, phase, dict(event.get("payload", {})))
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["predecessor_verify_state_digest"] = predecessor
    next_state["current_phase"] = phase
    next_state["event_index"] = int(event["event_index"])
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["processed_event_digests"] = list(next_state["processed_event_digests"]) + [event_id]
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": event["event_index"],
            "source_phase": event["source_phase"],
            "target_phase": phase,
            "artifact_digest": event["artifact_digest"],
            "verify_event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
        }
    ]
    if phase == "commit":
        next_state["verify_version"] += 1
        next_state["committed_records"] += 1
        next_state["record_summaries"] = list(next_state["record_summaries"]) + [
            {
                "verify_version": next_state["verify_version"],
                "route": next_state["route"],
                "source_observe_state_digest": next_state["source_observe_state_digest"],
                "verification_criterion_digest": next_state["verification_criterion_digest"],
                "verification_evidence_digest": next_state["verification_evidence_digest"],
                "adjudication_receipt_digest": next_state["adjudication_receipt_digest"],
                "verification_debt_discharged": next_state["verification_debt_discharged"],
                "verification_required": next_state["verification_required"],
                "reobservation_required": next_state["reobservation_required"],
                "corrective_action_required": next_state["corrective_action_required"],
                "learning_required": True,
            }
        ]
    next_state["verify_state_digest"] = ""
    next_state["verify_state_digest"] = state_digest(next_state)
    next_errors = validate_verify_state(next_state)
    if next_errors:
        raise ValueError("next_verify_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )
