from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
import json

from runtime import kuuos_verifyos_world_adoption_v0_33 as core
from runtime import kuuos_authorized_observation_world_feedback_entry_v0_32 as v032

CommitResult = core.CommitResult
canonical_json = core.canonical_json
digest = core.digest
make_envelope = core.make_envelope
make_verification_protocol_receipt = core.make_verification_protocol_receipt
validate_verification_protocol_receipt = core.validate_verification_protocol_receipt
build_verifyos_request = core.build_verifyos_request
validate_verifyos_request = core.validate_verifyos_request


def _validate_existing_ledger(path: Path, validator) -> None:
    path = Path(path)
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError("ledger_entry_invalid")
        validator(value)


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
    if assessor_identity.strip() == independent_assessor_identity.strip():
        raise ValueError("independent_assessor_identity_must_be_distinct")
    if source_matched and source_divergent:
        raise ValueError("source_match_divergence_conflict")
    if verdict != "INDETERMINATE" and indeterminate_route != "DEFER":
        raise ValueError("non_indeterminate_route_must_be_defer")
    if not request["requested_at_ms"] <= completed_at_ms < request["protocol_expires_at_ms"]:
        raise ValueError("verification_completion_outside_protocol_window")
    receipt = core.make_verification_receipt(
        request_envelope,
        verification_id=verification_id,
        completed_at_ms=completed_at_ms,
        assessor_identity=assessor_identity,
        independent_assessor_identity=independent_assessor_identity,
        assessment_artifact_digest=assessment_artifact_digest,
        assessor_receipt_digest=assessor_receipt_digest,
        challenge_record_digest=challenge_record_digest,
        corroboration_record_digest=corroboration_record_digest,
        verdict=verdict,
        source_matched=source_matched,
        source_divergent=source_divergent,
        corroboration_admissible=corroboration_admissible,
        criterion_satisfied=criterion_satisfied,
        falsifier_triggered=falsifier_triggered,
        assessor_independent=assessor_independent,
        provenance_intact=provenance_intact,
        method_reproducible=method_reproducible,
        unresolved_conflict=unresolved_conflict,
        reobservation_required=reobservation_required,
        indeterminate_route=indeterminate_route,
    )
    body = dict(receipt["body"])
    body.update({
        "requested_at_ms": request["requested_at_ms"],
        "verification_window_preserved": True,
        "independent_assessor_identity_distinct": True,
        "source_match_divergence_consistent": True,
        "non_indeterminate_route_normalized": True,
    })
    result = make_envelope(body)
    validate_verification_receipt(result)
    return result


def validate_verification_receipt(receipt_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = core.validate_verification_receipt(receipt_envelope)
    requested_at_ms = body.get("requested_at_ms")
    if not isinstance(requested_at_ms, int) or isinstance(requested_at_ms, bool) or requested_at_ms < 0:
        raise ValueError("requested_at_ms_invalid")
    if not requested_at_ms <= body["completed_at_ms"] < body["protocol_expires_at_ms"]:
        raise ValueError("verification_completion_outside_protocol_window")
    if body["assessor_identity"] == body["independent_assessor_identity"]:
        raise ValueError("independent_assessor_identity_must_be_distinct")
    if body["source_matched"] and body["source_divergent"]:
        raise ValueError("source_match_divergence_conflict")
    if body["verdict"] != "INDETERMINATE" and body["indeterminate_route"] != "DEFER":
        raise ValueError("non_indeterminate_route_must_be_defer")
    for field in (
        "verification_window_preserved",
        "independent_assessor_identity_distinct",
        "source_match_divergence_consistent",
        "non_indeterminate_route_normalized",
    ):
        if body.get(field) is not True:
            raise ValueError(f"official_verification_receipt_boundary_invalid:{field}")
    return body


def build_world_disposition_candidate(
    source_feedback_envelope: Mapping[str, Any],
    verification_receipt_envelope: Mapping[str, Any],
    *,
    generated_at_ms: int,
) -> dict[str, Any]:
    feedback = v032.validate_world_feedback_candidate(source_feedback_envelope)
    receipt = validate_verification_receipt(verification_receipt_envelope)
    expected_bindings = {
        "source_feedback_digest": source_feedback_envelope.get("body_digest"),
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
    }
    for field, expected in expected_bindings.items():
        if receipt.get(field) != expected:
            raise ValueError(f"verification_receipt_feedback_binding_mismatch:{field}")
    if not isinstance(generated_at_ms, int) or isinstance(generated_at_ms, bool):
        raise ValueError("world_disposition_generated_at_invalid")
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

    candidate_world_fragment_digest = (
        feedback["proposed_world_fragment_digest"]
        if route == "ADOPT_CANDIDATE"
        else feedback["prior_world_fragment_digest"]
    )
    disposition_id = "world-disposition-" + digest({
        "verification_receipt_digest": verification_receipt_envelope["body_digest"],
        "route": route,
        "generated_at_ms": generated_at_ms,
    })[:24]
    body = {
        "disposition_version": core.DISPOSITION_VERSION,
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
        "disposition_is_candidate": True,
        "adoption_is_candidate": True,
        "rejection_is_candidate": True,
        "defer_is_candidate": True,
        "reobserve_is_candidate": True,
        "route_derived_from_verification": True,
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
    body = core.validate_world_disposition_candidate(candidate_envelope)
    route = body["route"]
    verdict = body["verification_verdict"]
    source_route = body["source_feedback_route"]
    if route == "ADOPT_CANDIDATE":
        if verdict != "PASSED" or source_route != "WORLD_UPDATE_CANDIDATE":
            raise ValueError("adopt_candidate_route_derivation_invalid")
    elif route == "REJECT_CANDIDATE":
        if verdict != "FAILED":
            raise ValueError("reject_candidate_route_derivation_invalid")
    elif route == "DEFER_CANDIDATE":
        if verdict != "INDETERMINATE":
            raise ValueError("defer_candidate_route_derivation_invalid")
    elif route == "REOBSERVE_CANDIDATE":
        if not (
            verdict == "INDETERMINATE"
            or (verdict == "PASSED" and source_route == "REOBSERVE")
        ):
            raise ValueError("reobserve_candidate_route_derivation_invalid")
    for field in (
        "disposition_is_candidate",
        "route_derived_from_verification",
    ):
        if body.get(field) is not True:
            raise ValueError(f"official_world_disposition_boundary_invalid:{field}")
    return body


def commit_verifyos_request(*, ledger_path: Path, request_envelope: Mapping[str, Any]) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_verifyos_request)
    validate_verifyos_request(request_envelope)
    result = core.commit_verifyos_request(
        ledger_path=ledger_path,
        request_envelope=request_envelope,
    )
    validate_verifyos_request(result.artifact)
    return result


def commit_verification_receipt(*, ledger_path: Path, receipt_envelope: Mapping[str, Any]) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_verification_receipt)
    validate_verification_receipt(receipt_envelope)
    result = core.commit_verification_receipt(
        ledger_path=ledger_path,
        receipt_envelope=receipt_envelope,
    )
    validate_verification_receipt(result.artifact)
    return result


def commit_world_disposition_candidate(
    *,
    ledger_path: Path,
    candidate_envelope: Mapping[str, Any],
) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_world_disposition_candidate)
    validate_world_disposition_candidate(candidate_envelope)
    result = core.commit_world_disposition_candidate(
        ledger_path=ledger_path,
        candidate_envelope=candidate_envelope,
    )
    validate_world_disposition_candidate(result.artifact)
    return result


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
