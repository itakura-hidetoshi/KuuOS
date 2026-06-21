from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import json
import os

from runtime import kuuos_authorized_observation_world_feedback_entry_v0_32 as v032

VERSION = "v0.33"
PROTOCOL_VERSION = "verification_protocol_receipt_v0_33"
REQUEST_VERSION = "verifyos_request_v0_33"
RECEIPT_VERSION = "verification_receipt_v0_33"
DISPOSITION_VERSION = "world_disposition_candidate_v0_33"

VERDICTS = {"PASSED", "FAILED", "INDETERMINATE"}
INDETERMINATE_ROUTES = {"DEFER", "REOBSERVE"}
DISPOSITION_ROUTES = {
    "ADOPT_CANDIDATE",
    "REJECT_CANDIDATE",
    "DEFER_CANDIDATE",
    "REOBSERVE_CANDIDATE",
}
VERIFIABLE_FEEDBACK_ROUTES = {"WORLD_UPDATE_CANDIDATE", "REOBSERVE"}


def canonical_json(value: Any) -> str:
    return v032.canonical_json(value)


def digest(value: Any) -> str:
    return v032.digest(value)


def make_envelope(body: Mapping[str, Any]) -> dict[str, Any]:
    return v032.make_envelope(body)


def validate_envelope(envelope: Mapping[str, Any], *, label: str) -> dict[str, Any]:
    return v032.core.validate_envelope(envelope, label=label)


def _hex_digest(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field}_invalid")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field}_invalid") from exc
    return value


def _text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _bool(value: Any, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field}_invalid")
    return value


def _nonnegative_time(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _validate_source_chain(
    source_feedback_envelope: Mapping[str, Any],
    evidence_receipt_envelope: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    feedback = v032.validate_world_feedback_candidate(source_feedback_envelope)
    evidence = v032.validate_evidence_receipt(evidence_receipt_envelope)
    if feedback["evidence_receipt_digest"] != evidence_receipt_envelope.get("body_digest"):
        raise ValueError("feedback_evidence_receipt_mismatch")
    if feedback["source_report_digest"] != evidence["source_report_digest"]:
        raise ValueError("feedback_source_report_mismatch")
    if feedback["source_state_digest"] != evidence["source_state_digest"]:
        raise ValueError("feedback_source_state_mismatch")
    if feedback["root_lineage_digest"] != evidence["root_lineage_digest"]:
        raise ValueError("feedback_root_lineage_mismatch")
    if feedback["prior_world_fragment_digest"] != evidence["prior_world_fragment_digest"]:
        raise ValueError("feedback_prior_world_fragment_mismatch")
    if feedback["mission_candidate_id"] != evidence["mission_candidate_id"]:
        raise ValueError("feedback_mission_candidate_mismatch")
    if feedback["observation_candidate_id"] != evidence["observation_candidate_id"]:
        raise ValueError("feedback_observation_candidate_mismatch")
    if feedback["source_item_id"] != evidence["source_item_id"]:
        raise ValueError("feedback_source_item_mismatch")
    if feedback["new_evidence_ref"] != evidence_receipt_envelope.get("body_digest"):
        raise ValueError("feedback_new_evidence_ref_mismatch")
    if feedback["route"] not in VERIFIABLE_FEEDBACK_ROUTES:
        raise ValueError("feedback_route_not_verifiable")
    return feedback, evidence


def make_verification_protocol_receipt(
    *,
    protocol_id: str,
    source_feedback_envelope: Mapping[str, Any],
    evidence_receipt_envelope: Mapping[str, Any],
    criterion_digest: str,
    evaluation_method_digest: str,
    success_condition_digest: str,
    failure_condition_digest: str,
    falsification_condition_digest: str,
    evidence_requirements_digest: str,
    assessor_policy_digest: str,
    host_license_digest: str,
    issued_by: str,
    issued_at_ms: int,
    not_before_ms: int,
    expires_at_ms: int,
) -> dict[str, Any]:
    feedback, evidence = _validate_source_chain(
        source_feedback_envelope,
        evidence_receipt_envelope,
    )
    protocol_id = _text(protocol_id, field="protocol_id")
    issued_by = _text(issued_by, field="issued_by")
    for field, value in (
        ("criterion_digest", criterion_digest),
        ("evaluation_method_digest", evaluation_method_digest),
        ("success_condition_digest", success_condition_digest),
        ("failure_condition_digest", failure_condition_digest),
        ("falsification_condition_digest", falsification_condition_digest),
        ("evidence_requirements_digest", evidence_requirements_digest),
        ("assessor_policy_digest", assessor_policy_digest),
        ("host_license_digest", host_license_digest),
    ):
        _hex_digest(value, field=field)
    issued_at_ms = _nonnegative_time(issued_at_ms, field="issued_at_ms")
    not_before_ms = _nonnegative_time(not_before_ms, field="not_before_ms")
    expires_at_ms = _nonnegative_time(expires_at_ms, field="expires_at_ms")
    if not issued_at_ms <= not_before_ms < expires_at_ms:
        raise ValueError("verification_protocol_window_invalid")
    body = {
        "protocol_version": PROTOCOL_VERSION,
        "protocol_id": protocol_id,
        "source_feedback_digest": source_feedback_envelope["body_digest"],
        "source_evidence_receipt_digest": evidence_receipt_envelope["body_digest"],
        "source_report_digest": feedback["source_report_digest"],
        "source_state_digest": feedback["source_state_digest"],
        "root_lineage_digest": feedback["root_lineage_digest"],
        "prior_world_fragment_digest": feedback["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": feedback["proposed_world_fragment_digest"],
        "mission_candidate_id": feedback["mission_candidate_id"],
        "observation_candidate_id": feedback["observation_candidate_id"],
        "source_item_id": feedback["source_item_id"],
        "source_feedback_route": feedback["route"],
        "source_candidate_state": feedback["candidate_state"],
        "source_evidence_relation": evidence["relation"],
        "criterion_digest": criterion_digest,
        "evaluation_method_digest": evaluation_method_digest,
        "success_condition_digest": success_condition_digest,
        "failure_condition_digest": failure_condition_digest,
        "falsification_condition_digest": falsification_condition_digest,
        "evidence_requirements_digest": evidence_requirements_digest,
        "assessor_policy_digest": assessor_policy_digest,
        "host_license_digest": host_license_digest,
        "criterion_defined_before_adjudication": True,
        "falsification_required": True,
        "independent_assessment_required": True,
        "counterevidence_preservation_required": True,
        "issued_by": issued_by,
        "issued_at_ms": issued_at_ms,
        "not_before_ms": not_before_ms,
        "expires_at_ms": expires_at_ms,
        "max_verifications": 1,
        "single_use": True,
        "grants_verify_invocation": True,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_world_adoption_authority": False,
        "grants_world_commit_authority": False,
        "grants_root_rewrite_authority": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_memory_overwrite_authority": False,
    }
    receipt = make_envelope(body)
    validate_verification_protocol_receipt(receipt)
    return receipt


def validate_verification_protocol_receipt(
    protocol_envelope: Mapping[str, Any],
) -> dict[str, Any]:
    body = validate_envelope(protocol_envelope, label="verification_protocol")
    if body.get("protocol_version") != PROTOCOL_VERSION:
        raise ValueError("verification_protocol_version_invalid")
    for field in (
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "criterion_digest",
        "evaluation_method_digest",
        "success_condition_digest",
        "failure_condition_digest",
        "falsification_condition_digest",
        "evidence_requirements_digest",
        "assessor_policy_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "protocol_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "source_candidate_state",
        "issued_by",
    ):
        _text(body.get(field), field=field)
    if body.get("source_feedback_route") not in VERIFIABLE_FEEDBACK_ROUTES:
        raise ValueError("source_feedback_route_invalid")
    if body.get("source_evidence_relation") not in v032.core.EVIDENCE_RELATIONS:
        raise ValueError("source_evidence_relation_invalid")
    for field in (
        "criterion_defined_before_adjudication",
        "falsification_required",
        "independent_assessment_required",
        "counterevidence_preservation_required",
        "single_use",
        "grants_verify_invocation",
    ):
        if body.get(field) is not True:
            raise ValueError(f"verification_protocol_required_flag_invalid:{field}")
    if body.get("max_verifications") != 1:
        raise ValueError("verification_protocol_not_single_use")
    issued_at_ms = _nonnegative_time(body.get("issued_at_ms"), field="issued_at_ms")
    not_before_ms = _nonnegative_time(body.get("not_before_ms"), field="not_before_ms")
    expires_at_ms = _nonnegative_time(body.get("expires_at_ms"), field="expires_at_ms")
    if not issued_at_ms <= not_before_ms < expires_at_ms:
        raise ValueError("verification_protocol_window_invalid")
    for field in (
        "grants_truth_authority",
        "grants_causal_attribution",
        "grants_world_adoption_authority",
        "grants_world_commit_authority",
        "grants_root_rewrite_authority",
        "grants_plan_activation",
        "grants_actos_invocation",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"verification_protocol_boundary_invalid:{field}")
    return body


def build_verifyos_request(
    source_feedback_envelope: Mapping[str, Any],
    evidence_receipt_envelope: Mapping[str, Any],
    protocol_envelope: Mapping[str, Any],
    *,
    requested_at_ms: int,
) -> dict[str, Any]:
    feedback, evidence = _validate_source_chain(
        source_feedback_envelope,
        evidence_receipt_envelope,
    )
    protocol = validate_verification_protocol_receipt(protocol_envelope)
    exact_bindings = {
        "source_feedback_digest": source_feedback_envelope.get("body_digest"),
        "source_evidence_receipt_digest": evidence_receipt_envelope.get("body_digest"),
        "source_report_digest": feedback["source_report_digest"],
        "source_state_digest": feedback["source_state_digest"],
        "root_lineage_digest": feedback["root_lineage_digest"],
        "prior_world_fragment_digest": feedback["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": feedback["proposed_world_fragment_digest"],
        "mission_candidate_id": feedback["mission_candidate_id"],
        "observation_candidate_id": feedback["observation_candidate_id"],
        "source_item_id": feedback["source_item_id"],
        "source_feedback_route": feedback["route"],
        "source_candidate_state": feedback["candidate_state"],
        "source_evidence_relation": evidence["relation"],
    }
    for field, expected in exact_bindings.items():
        if protocol.get(field) != expected:
            raise ValueError(f"verification_protocol_binding_mismatch:{field}")
    requested_at_ms = _nonnegative_time(requested_at_ms, field="requested_at_ms")
    if not protocol["not_before_ms"] <= requested_at_ms < protocol["expires_at_ms"]:
        raise ValueError("verification_protocol_not_current")
    request_id = "verify-" + digest({
        "protocol_digest": protocol_envelope["body_digest"],
        "source_feedback_digest": source_feedback_envelope["body_digest"],
        "requested_at_ms": requested_at_ms,
    })[:24]
    body = {
        "request_version": REQUEST_VERSION,
        "request_id": request_id,
        "protocol_digest": protocol_envelope["body_digest"],
        "protocol_id": protocol["protocol_id"],
        **exact_bindings,
        "criterion_digest": protocol["criterion_digest"],
        "evaluation_method_digest": protocol["evaluation_method_digest"],
        "success_condition_digest": protocol["success_condition_digest"],
        "failure_condition_digest": protocol["failure_condition_digest"],
        "falsification_condition_digest": protocol["falsification_condition_digest"],
        "evidence_requirements_digest": protocol["evidence_requirements_digest"],
        "assessor_policy_digest": protocol["assessor_policy_digest"],
        "host_license_digest": protocol["host_license_digest"],
        "requested_at_ms": requested_at_ms,
        "protocol_issued_at_ms": protocol["issued_at_ms"],
        "protocol_not_before_ms": protocol["not_before_ms"],
        "protocol_expires_at_ms": protocol["expires_at_ms"],
        "verification_index": 1,
        "single_use": True,
        "criterion_defined_before_adjudication": True,
        "falsification_required": True,
        "independent_assessment_required": True,
        "counterevidence_preservation_required": True,
        "grants_verify_invocation": True,
        "grants_truth_authority": False,
        "grants_world_adoption_authority": False,
        "grants_world_commit_authority": False,
        "grants_root_rewrite_authority": False,
    }
    request = make_envelope(body)
    validate_verifyos_request(request)
    return request


def validate_verifyos_request(request_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(request_envelope, label="verifyos_request")
    if body.get("request_version") != REQUEST_VERSION:
        raise ValueError("verifyos_request_version_invalid")
    for field in (
        "protocol_digest",
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "criterion_digest",
        "evaluation_method_digest",
        "success_condition_digest",
        "failure_condition_digest",
        "falsification_condition_digest",
        "evidence_requirements_digest",
        "assessor_policy_digest",
        "host_license_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "request_id",
        "protocol_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "source_candidate_state",
    ):
        _text(body.get(field), field=field)
    if body.get("source_feedback_route") not in VERIFIABLE_FEEDBACK_ROUTES:
        raise ValueError("source_feedback_route_invalid")
    if body.get("source_evidence_relation") not in v032.core.EVIDENCE_RELATIONS:
        raise ValueError("source_evidence_relation_invalid")
    if body.get("verification_index") != 1 or body.get("single_use") is not True:
        raise ValueError("verifyos_request_not_single_use")
    for field in (
        "criterion_defined_before_adjudication",
        "falsification_required",
        "independent_assessment_required",
        "counterevidence_preservation_required",
        "grants_verify_invocation",
    ):
        if body.get(field) is not True:
            raise ValueError(f"verifyos_request_required_flag_invalid:{field}")
    issued_at_ms = _nonnegative_time(body.get("protocol_issued_at_ms"), field="protocol_issued_at_ms")
    not_before_ms = _nonnegative_time(body.get("protocol_not_before_ms"), field="protocol_not_before_ms")
    requested_at_ms = _nonnegative_time(body.get("requested_at_ms"), field="requested_at_ms")
    expires_at_ms = _nonnegative_time(body.get("protocol_expires_at_ms"), field="protocol_expires_at_ms")
    if not issued_at_ms <= not_before_ms <= requested_at_ms < expires_at_ms:
        raise ValueError("verifyos_request_window_invalid")
    for field in (
        "grants_truth_authority",
        "grants_world_adoption_authority",
        "grants_world_commit_authority",
        "grants_root_rewrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"verifyos_request_boundary_invalid:{field}")
    return body


def make_verification_receipt(
    request_envelope: Mapping[str, Any],
    *,
    verification_id: str,
    completed_at_ms: int,
    assessor_identity: str,
    independent_assessor_identity: str,
    assessment_artifact_digest: str,
    assessor_receipt_digest: str,
    challenge_record_digest: str,
    corroboration_record_digest: str,
    verdict: str,
    source_matched: bool,
    source_divergent: bool,
    corroboration_admissible: bool,
    criterion_satisfied: bool,
    falsifier_triggered: bool,
    assessor_independent: bool,
    provenance_intact: bool,
    method_reproducible: bool,
    unresolved_conflict: bool,
    reobservation_required: bool,
    indeterminate_route: str = "DEFER",
) -> dict[str, Any]:
    request = validate_verifyos_request(request_envelope)
    verification_id = _text(verification_id, field="verification_id")
    assessor_identity = _text(assessor_identity, field="assessor_identity")
    independent_assessor_identity = _text(
        independent_assessor_identity,
        field="independent_assessor_identity",
    )
    for field, value in (
        ("assessment_artifact_digest", assessment_artifact_digest),
        ("assessor_receipt_digest", assessor_receipt_digest),
        ("challenge_record_digest", challenge_record_digest),
        ("corroboration_record_digest", corroboration_record_digest),
    ):
        _hex_digest(value, field=field)
    completed_at_ms = _nonnegative_time(completed_at_ms, field="completed_at_ms")
    if not request["requested_at_ms"] <= completed_at_ms < request["protocol_expires_at_ms"]:
        raise ValueError("verification_completion_outside_protocol_window")
    if verdict not in VERDICTS:
        raise ValueError("verification_verdict_invalid")
    for field, value in (
        ("source_matched", source_matched),
        ("source_divergent", source_divergent),
        ("corroboration_admissible", corroboration_admissible),
        ("criterion_satisfied", criterion_satisfied),
        ("falsifier_triggered", falsifier_triggered),
        ("assessor_independent", assessor_independent),
        ("provenance_intact", provenance_intact),
        ("method_reproducible", method_reproducible),
        ("unresolved_conflict", unresolved_conflict),
        ("reobservation_required", reobservation_required),
    ):
        _bool(value, field=field)
    if indeterminate_route not in INDETERMINATE_ROUTES:
        raise ValueError("indeterminate_route_invalid")

    if verdict == "PASSED":
        if not (
            source_matched
            and not source_divergent
            and corroboration_admissible
            and criterion_satisfied
            and not falsifier_triggered
            and assessor_independent
            and provenance_intact
            and method_reproducible
            and not unresolved_conflict
            and not reobservation_required
        ):
            raise ValueError("passed_verification_conditions_invalid")
        verification_debt_discharged = True
        verification_required = False
        corrective_action_required = False
    elif verdict == "FAILED":
        if not (
            corroboration_admissible
            and assessor_independent
            and provenance_intact
            and method_reproducible
            and not unresolved_conflict
            and (source_divergent or not criterion_satisfied or falsifier_triggered)
            and not reobservation_required
        ):
            raise ValueError("failed_verification_conditions_invalid")
        verification_debt_discharged = True
        verification_required = False
        corrective_action_required = True
    else:
        if corroboration_admissible:
            raise ValueError("indeterminate_corroboration_must_be_inadmissible")
        if indeterminate_route == "REOBSERVE" and not reobservation_required:
            raise ValueError("indeterminate_reobserve_flag_required")
        if indeterminate_route == "DEFER" and reobservation_required:
            raise ValueError("indeterminate_defer_cannot_require_reobservation")
        verification_debt_discharged = False
        verification_required = True
        corrective_action_required = False

    body = {
        "receipt_version": RECEIPT_VERSION,
        "verification_id": verification_id,
        "request_digest": request_envelope["body_digest"],
        "protocol_digest": request["protocol_digest"],
        "protocol_id": request["protocol_id"],
        "source_feedback_digest": request["source_feedback_digest"],
        "source_evidence_receipt_digest": request["source_evidence_receipt_digest"],
        "source_report_digest": request["source_report_digest"],
        "source_state_digest": request["source_state_digest"],
        "root_lineage_digest": request["root_lineage_digest"],
        "prior_world_fragment_digest": request["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": request["proposed_world_fragment_digest"],
        "mission_candidate_id": request["mission_candidate_id"],
        "observation_candidate_id": request["observation_candidate_id"],
        "source_item_id": request["source_item_id"],
        "source_feedback_route": request["source_feedback_route"],
        "source_candidate_state": request["source_candidate_state"],
        "source_evidence_relation": request["source_evidence_relation"],
        "criterion_digest": request["criterion_digest"],
        "evaluation_method_digest": request["evaluation_method_digest"],
        "success_condition_digest": request["success_condition_digest"],
        "failure_condition_digest": request["failure_condition_digest"],
        "falsification_condition_digest": request["falsification_condition_digest"],
        "evidence_requirements_digest": request["evidence_requirements_digest"],
        "assessor_policy_digest": request["assessor_policy_digest"],
        "host_license_digest": request["host_license_digest"],
        "assessor_identity": assessor_identity,
        "independent_assessor_identity": independent_assessor_identity,
        "assessment_artifact_digest": assessment_artifact_digest,
        "assessor_receipt_digest": assessor_receipt_digest,
        "challenge_record_digest": challenge_record_digest,
        "corroboration_record_digest": corroboration_record_digest,
        "completed_at_ms": completed_at_ms,
        "protocol_expires_at_ms": request["protocol_expires_at_ms"],
        "verdict": verdict,
        "source_matched": source_matched,
        "source_divergent": source_divergent,
        "corroboration_admissible": corroboration_admissible,
        "criterion_satisfied": criterion_satisfied,
        "falsifier_triggered": falsifier_triggered,
        "assessor_independent": assessor_independent,
        "provenance_intact": provenance_intact,
        "method_reproducible": method_reproducible,
        "unresolved_conflict": unresolved_conflict,
        "reobservation_required": reobservation_required,
        "indeterminate_route": indeterminate_route,
        "verification_recorded": True,
        "verification_not_truth": True,
        "verification_not_causal_attribution": True,
        "verification_not_world_adoption": True,
        "verification_debt_discharged": verification_debt_discharged,
        "verification_required": verification_required,
        "corrective_action_required": corrective_action_required,
        "learning_required": True,
        "learning_future_only": True,
        "automatic_learning": False,
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_world_adoption_authority": False,
        "grants_world_commit_authority": False,
        "grants_root_rewrite_authority": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_memory_overwrite_authority": False,
    }
    receipt = make_envelope(body)
    validate_verification_receipt(receipt)
    return receipt


def validate_verification_receipt(receipt_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(receipt_envelope, label="verification_receipt")
    if body.get("receipt_version") != RECEIPT_VERSION:
        raise ValueError("verification_receipt_version_invalid")
    for field in (
        "request_digest",
        "protocol_digest",
        "source_feedback_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "criterion_digest",
        "evaluation_method_digest",
        "success_condition_digest",
        "failure_condition_digest",
        "falsification_condition_digest",
        "evidence_requirements_digest",
        "assessor_policy_digest",
        "host_license_digest",
        "assessment_artifact_digest",
        "assessor_receipt_digest",
        "challenge_record_digest",
        "corroboration_record_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "verification_id",
        "protocol_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "source_candidate_state",
        "assessor_identity",
        "independent_assessor_identity",
    ):
        _text(body.get(field), field=field)
    if body.get("source_feedback_route") not in VERIFIABLE_FEEDBACK_ROUTES:
        raise ValueError("source_feedback_route_invalid")
    if body.get("source_evidence_relation") not in v032.core.EVIDENCE_RELATIONS:
        raise ValueError("source_evidence_relation_invalid")
    verdict = body.get("verdict")
    if verdict not in VERDICTS:
        raise ValueError("verification_verdict_invalid")
    if body.get("indeterminate_route") not in INDETERMINATE_ROUTES:
        raise ValueError("indeterminate_route_invalid")
    for field in (
        "source_matched",
        "source_divergent",
        "corroboration_admissible",
        "criterion_satisfied",
        "falsifier_triggered",
        "assessor_independent",
        "provenance_intact",
        "method_reproducible",
        "unresolved_conflict",
        "reobservation_required",
        "verification_debt_discharged",
        "verification_required",
        "corrective_action_required",
    ):
        _bool(body.get(field), field=field)
    completed_at_ms = _nonnegative_time(body.get("completed_at_ms"), field="completed_at_ms")
    expires_at_ms = _nonnegative_time(body.get("protocol_expires_at_ms"), field="protocol_expires_at_ms")
    if not completed_at_ms < expires_at_ms:
        raise ValueError("verification_completion_outside_protocol_window")

    if verdict == "PASSED":
        if not (
            body["source_matched"]
            and not body["source_divergent"]
            and body["corroboration_admissible"]
            and body["criterion_satisfied"]
            and not body["falsifier_triggered"]
            and body["assessor_independent"]
            and body["provenance_intact"]
            and body["method_reproducible"]
            and not body["unresolved_conflict"]
            and not body["reobservation_required"]
            and body["verification_debt_discharged"]
            and not body["verification_required"]
            and not body["corrective_action_required"]
        ):
            raise ValueError("passed_verification_conditions_invalid")
    elif verdict == "FAILED":
        if not (
            body["corroboration_admissible"]
            and body["assessor_independent"]
            and body["provenance_intact"]
            and body["method_reproducible"]
            and not body["unresolved_conflict"]
            and (body["source_divergent"] or not body["criterion_satisfied"] or body["falsifier_triggered"])
            and not body["reobservation_required"]
            and body["verification_debt_discharged"]
            and not body["verification_required"]
            and body["corrective_action_required"]
        ):
            raise ValueError("failed_verification_conditions_invalid")
    else:
        if body["corroboration_admissible"]:
            raise ValueError("indeterminate_corroboration_must_be_inadmissible")
        if body["verification_debt_discharged"] or not body["verification_required"]:
            raise ValueError("indeterminate_verification_debt_invalid")
        if body["corrective_action_required"]:
            raise ValueError("indeterminate_corrective_action_invalid")
        if body["indeterminate_route"] == "REOBSERVE" and not body["reobservation_required"]:
            raise ValueError("indeterminate_reobserve_flag_required")
        if body["indeterminate_route"] == "DEFER" and body["reobservation_required"]:
            raise ValueError("indeterminate_defer_cannot_require_reobservation")

    for field in (
        "verification_recorded",
        "verification_not_truth",
        "verification_not_causal_attribution",
        "verification_not_world_adoption",
        "learning_required",
        "learning_future_only",
        "counterevidence_preserved",
        "uncertainty_preserved",
    ):
        if body.get(field) is not True:
            raise ValueError(f"verification_receipt_required_flag_invalid:{field}")
    if body.get("automatic_learning") is not False:
        raise ValueError("automatic_learning_forbidden")
    for field in (
        "grants_truth_authority",
        "grants_causal_attribution",
        "grants_world_adoption_authority",
        "grants_world_commit_authority",
        "grants_root_rewrite_authority",
        "grants_plan_activation",
        "grants_actos_invocation",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"verification_receipt_boundary_invalid:{field}")
    return body


def build_world_disposition_candidate(
    source_feedback_envelope: Mapping[str, Any],
    verification_receipt_envelope: Mapping[str, Any],
    *,
    generated_at_ms: int,
) -> dict[str, Any]:
    feedback = v032.validate_world_feedback_candidate(source_feedback_envelope)
    receipt = validate_verification_receipt(verification_receipt_envelope)
    if receipt["source_feedback_digest"] != source_feedback_envelope.get("body_digest"):
        raise ValueError("verification_receipt_feedback_mismatch")
    for field in (
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "source_feedback_route",
        "source_candidate_state",
    ):
        expected = feedback["route"] if field == "source_feedback_route" else feedback.get(field)
        if receipt.get(field) != expected:
            raise ValueError(f"verification_receipt_feedback_binding_mismatch:{field}")
    generated_at_ms = _nonnegative_time(generated_at_ms, field="generated_at_ms")
    if generated_at_ms < receipt["completed_at_ms"]:
        raise ValueError("world_disposition_generated_at_invalid")

    if receipt["verdict"] == "PASSED":
        route = (
            "REOBSERVE_CANDIDATE"
            if feedback["route"] == "REOBSERVE"
            else "ADOPT_CANDIDATE"
        )
    elif receipt["verdict"] == "FAILED":
        route = "REJECT_CANDIDATE"
    elif receipt["indeterminate_route"] == "REOBSERVE":
        route = "REOBSERVE_CANDIDATE"
    else:
        route = "DEFER_CANDIDATE"

    if route == "ADOPT_CANDIDATE":
        candidate_world_fragment_digest = feedback["proposed_world_fragment_digest"]
    else:
        candidate_world_fragment_digest = feedback["prior_world_fragment_digest"]

    disposition_id = "world-disposition-" + digest({
        "verification_receipt_digest": verification_receipt_envelope["body_digest"],
        "route": route,
        "generated_at_ms": generated_at_ms,
    })[:24]
    body = {
        "disposition_version": DISPOSITION_VERSION,
        "disposition_id": disposition_id,
        "source_feedback_digest": source_feedback_envelope["body_digest"],
        "verification_receipt_digest": verification_receipt_envelope["body_digest"],
        "source_evidence_receipt_digest": receipt["source_evidence_receipt_digest"],
        "source_report_digest": feedback["source_report_digest"],
        "source_state_digest": feedback["source_state_digest"],
        "root_lineage_digest": feedback["root_lineage_digest"],
        "prior_world_fragment_digest": feedback["prior_world_fragment_digest"],
        "proposed_world_fragment_digest": feedback["proposed_world_fragment_digest"],
        "candidate_world_fragment_digest": candidate_world_fragment_digest,
        "mission_candidate_id": feedback["mission_candidate_id"],
        "observation_candidate_id": feedback["observation_candidate_id"],
        "source_item_id": feedback["source_item_id"],
        "source_feedback_route": feedback["route"],
        "source_candidate_state": feedback["candidate_state"],
        "verification_verdict": receipt["verdict"],
        "generated_at_ms": generated_at_ms,
        "route": route,
        "adoption_is_candidate": True,
        "rejection_is_candidate": True,
        "defer_is_candidate": True,
        "reobserve_is_candidate": True,
        "governance_review_required": True,
        "world_commit_required_separately": True,
        "same_root_required": True,
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "learning_required": True,
        "learning_future_only": True,
        "automatic_learning": False,
        "automatic_world_adoption": False,
        "automatic_world_rejection": False,
        "automatic_world_commit": False,
        "automatic_root_rewrite": False,
        "automatic_mission_completion": False,
        "grants_truth_authority": False,
        "grants_causal_attribution": False,
        "grants_plan_activation": False,
        "grants_actos_invocation": False,
        "grants_memory_overwrite_authority": False,
    }
    candidate = make_envelope(body)
    validate_world_disposition_candidate(candidate)
    return candidate


def validate_world_disposition_candidate(candidate_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = validate_envelope(candidate_envelope, label="world_disposition_candidate")
    if body.get("disposition_version") != DISPOSITION_VERSION:
        raise ValueError("world_disposition_version_invalid")
    if body.get("route") not in DISPOSITION_ROUTES:
        raise ValueError("world_disposition_route_invalid")
    if body.get("verification_verdict") not in VERDICTS:
        raise ValueError("verification_verdict_invalid")
    for field in (
        "source_feedback_digest",
        "verification_receipt_digest",
        "source_evidence_receipt_digest",
        "source_report_digest",
        "source_state_digest",
        "root_lineage_digest",
        "prior_world_fragment_digest",
        "proposed_world_fragment_digest",
        "candidate_world_fragment_digest",
    ):
        _hex_digest(body.get(field), field=field)
    for field in (
        "disposition_id",
        "mission_candidate_id",
        "observation_candidate_id",
        "source_item_id",
        "source_candidate_state",
    ):
        _text(body.get(field), field=field)
    if body.get("source_feedback_route") not in VERIFIABLE_FEEDBACK_ROUTES:
        raise ValueError("source_feedback_route_invalid")
    if body["route"] == "ADOPT_CANDIDATE":
        if body["verification_verdict"] != "PASSED":
            raise ValueError("adopt_candidate_requires_passed_verification")
        if body["source_feedback_route"] != "WORLD_UPDATE_CANDIDATE":
            raise ValueError("adopt_candidate_requires_world_update_feedback")
        if body["candidate_world_fragment_digest"] != body["proposed_world_fragment_digest"]:
            raise ValueError("adopt_candidate_fragment_mismatch")
    else:
        if body["candidate_world_fragment_digest"] != body["prior_world_fragment_digest"]:
            raise ValueError("non_adopt_candidate_must_preserve_prior_fragment")
    if body["route"] == "REJECT_CANDIDATE" and body["verification_verdict"] != "FAILED":
        raise ValueError("reject_candidate_requires_failed_verification")
    if body["route"] in {"DEFER_CANDIDATE", "REOBSERVE_CANDIDATE"}:
        if body["verification_verdict"] == "FAILED":
            raise ValueError("failed_verification_cannot_defer_or_reobserve")
    for field in (
        "adoption_is_candidate",
        "rejection_is_candidate",
        "defer_is_candidate",
        "reobserve_is_candidate",
        "governance_review_required",
        "world_commit_required_separately",
        "same_root_required",
        "counterevidence_preserved",
        "uncertainty_preserved",
        "learning_required",
        "learning_future_only",
    ):
        if body.get(field) is not True:
            raise ValueError(f"world_disposition_required_flag_invalid:{field}")
    for field in (
        "automatic_learning",
        "automatic_world_adoption",
        "automatic_world_rejection",
        "automatic_world_commit",
        "automatic_root_rewrite",
        "automatic_mission_completion",
        "grants_truth_authority",
        "grants_causal_attribution",
        "grants_plan_activation",
        "grants_actos_invocation",
        "grants_memory_overwrite_authority",
    ):
        if body.get(field) is not False:
            raise ValueError(f"world_disposition_boundary_invalid:{field}")
    return body


def _read_jsonl(path: Path, validator) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError("ledger_entry_invalid")
        validator(value)
        entries.append(value)
    return entries


def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(value) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


@dataclass(frozen=True)
class CommitResult:
    status: str
    artifact: dict[str, Any]
    ledger_entries: int


def commit_verifyos_request(*, ledger_path: Path, request_envelope: Mapping[str, Any]) -> CommitResult:
    request = validate_verifyos_request(request_envelope)
    entries = _read_jsonl(Path(ledger_path), validate_verifyos_request)
    for entry in entries:
        body = validate_verifyos_request(entry)
        if entry["body_digest"] == request_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["protocol_id"] == request["protocol_id"]:
            raise ValueError("verification_protocol_already_consumed")
        if body["protocol_digest"] == request["protocol_digest"]:
            raise ValueError("verification_protocol_digest_already_consumed")
    _append_jsonl(Path(ledger_path), request_envelope)
    return CommitResult("COMMITTED", dict(request_envelope), len(entries) + 1)


def commit_verification_receipt(*, ledger_path: Path, receipt_envelope: Mapping[str, Any]) -> CommitResult:
    receipt = validate_verification_receipt(receipt_envelope)
    entries = _read_jsonl(Path(ledger_path), validate_verification_receipt)
    for entry in entries:
        body = validate_verification_receipt(entry)
        if entry["body_digest"] == receipt_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["request_digest"] == receipt["request_digest"]:
            raise ValueError("verifyos_request_already_has_receipt")
        if body["verification_id"] == receipt["verification_id"]:
            raise ValueError("verification_id_reuse")
    _append_jsonl(Path(ledger_path), receipt_envelope)
    return CommitResult("COMMITTED", dict(receipt_envelope), len(entries) + 1)


def commit_world_disposition_candidate(
    *,
    ledger_path: Path,
    candidate_envelope: Mapping[str, Any],
) -> CommitResult:
    candidate = validate_world_disposition_candidate(candidate_envelope)
    entries = _read_jsonl(Path(ledger_path), validate_world_disposition_candidate)
    for entry in entries:
        body = validate_world_disposition_candidate(entry)
        if entry["body_digest"] == candidate_envelope.get("body_digest"):
            return CommitResult("REPLAYED", entry, len(entries))
        if body["verification_receipt_digest"] == candidate["verification_receipt_digest"]:
            raise ValueError("verification_receipt_already_has_world_disposition")
        if body["disposition_id"] == candidate["disposition_id"]:
            raise ValueError("world_disposition_id_reuse")
    _append_jsonl(Path(ledger_path), candidate_envelope)
    return CommitResult("COMMITTED", dict(candidate_envelope), len(entries) + 1)


__all__ = [
    "CommitResult",
    "build_verifyos_request",
    "build_world_disposition_candidate",
    "commit_verification_receipt",
    "commit_verifyos_request",
    "commit_world_disposition_candidate",
    "make_verification_protocol_receipt",
    "make_verification_receipt",
    "validate_verification_protocol_receipt",
    "validate_verification_receipt",
    "validate_verifyos_request",
    "validate_world_disposition_candidate",
]
