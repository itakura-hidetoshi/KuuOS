from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping
import json

from runtime import kuuos_authorized_observation_world_feedback_v0_32 as core

CommitResult = core.CommitResult
canonical_json = core.canonical_json
digest = core.digest
make_envelope = core.make_envelope
make_observation_authorization_receipt = core.make_observation_authorization_receipt
validate_authorization_receipt = core.validate_authorization_receipt


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


def build_authorized_observe_request(
    source_report_envelope: Mapping[str, Any],
    authorization_receipt_envelope: Mapping[str, Any],
    *,
    requested_at_ms: int,
) -> dict[str, Any]:
    authorization = validate_authorization_receipt(authorization_receipt_envelope)
    request = core.build_authorized_observe_request(
        source_report_envelope,
        authorization_receipt_envelope,
        requested_at_ms=requested_at_ms,
    )
    body = dict(request["body"])
    body.update({
        "authorization_issued_at_ms": authorization["issued_at_ms"],
        "authorization_not_before_ms": authorization["not_before_ms"],
        "authorization_expires_at_ms": authorization["expires_at_ms"],
        "authorization_window_bound": True,
    })
    result = make_envelope(body)
    validate_observe_request(result)
    return result


def validate_observe_request(request_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = core.validate_observe_request(request_envelope)
    for field in (
        "authorization_issued_at_ms",
        "authorization_not_before_ms",
        "authorization_expires_at_ms",
    ):
        if not isinstance(body.get(field), int) or body[field] < 0:
            raise ValueError(f"{field}_invalid")
    if not (
        body["authorization_issued_at_ms"]
        <= body["authorization_not_before_ms"]
        <= body["requested_at_ms"]
        < body["authorization_expires_at_ms"]
    ):
        raise ValueError("request_authorization_window_invalid")
    if body.get("authorization_window_bound") is not True:
        raise ValueError("authorization_window_not_bound")
    return body


def make_observation_evidence_receipt(
    request_envelope: Mapping[str, Any],
    *,
    evidence_id: str,
    collected_at_ms: int,
    raw_artifact_digest: str,
    value_digest: str,
    collector_identity: str,
    independent_source_identity: str,
    uncertainty_digest: str,
    calibration_digest: str,
    context_digest: str,
    tamper_evidence_digest: str,
    provenance_chain_digest: str,
    relation: str,
) -> dict[str, Any]:
    request = validate_observe_request(request_envelope)
    if not request["requested_at_ms"] <= collected_at_ms < request["authorization_expires_at_ms"]:
        raise ValueError("evidence_collection_outside_authorization_window")
    receipt = core.make_observation_evidence_receipt(
        request_envelope,
        evidence_id=evidence_id,
        collected_at_ms=collected_at_ms,
        raw_artifact_digest=raw_artifact_digest,
        value_digest=value_digest,
        collector_identity=collector_identity,
        independent_source_identity=independent_source_identity,
        uncertainty_digest=uncertainty_digest,
        calibration_digest=calibration_digest,
        context_digest=context_digest,
        tamper_evidence_digest=tamper_evidence_digest,
        provenance_chain_digest=provenance_chain_digest,
        relation=relation,
    )
    body = dict(receipt["body"])
    body.update({
        "authorization_expires_at_ms": request["authorization_expires_at_ms"],
        "authorization_window_observed": True,
    })
    result = make_envelope(body)
    validate_evidence_receipt(result)
    return result


def validate_evidence_receipt(receipt_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = core.validate_evidence_receipt(receipt_envelope)
    if not isinstance(body.get("authorization_expires_at_ms"), int):
        raise ValueError("authorization_expires_at_ms_invalid")
    if not body["collected_at_ms"] < body["authorization_expires_at_ms"]:
        raise ValueError("evidence_collection_outside_authorization_window")
    if body.get("authorization_window_observed") is not True:
        raise ValueError("authorization_window_not_observed")
    return body


def build_world_feedback_candidate(
    source_report_envelope: Mapping[str, Any],
    evidence_receipt_envelope: Mapping[str, Any],
    *,
    generated_at_ms: int,
) -> dict[str, Any]:
    validate_evidence_receipt(evidence_receipt_envelope)
    feedback = core.build_world_feedback_candidate(
        source_report_envelope,
        evidence_receipt_envelope,
        generated_at_ms=generated_at_ms,
    )
    body = dict(feedback["body"])
    body["authorized_observation_window_preserved"] = True
    result = make_envelope(body)
    validate_world_feedback_candidate(result)
    return result


def validate_world_feedback_candidate(feedback_envelope: Mapping[str, Any]) -> dict[str, Any]:
    body = core.validate_world_feedback_candidate(feedback_envelope)
    if body.get("authorized_observation_window_preserved") is not True:
        raise ValueError("authorized_observation_window_not_preserved")
    return body


def commit_observe_request(*, ledger_path: Path, request_envelope: Mapping[str, Any]) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_observe_request)
    validate_observe_request(request_envelope)
    result = core.commit_observe_request(ledger_path=ledger_path, request_envelope=request_envelope)
    validate_observe_request(result.artifact)
    return result


def commit_evidence_receipt(*, ledger_path: Path, receipt_envelope: Mapping[str, Any]) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_evidence_receipt)
    validate_evidence_receipt(receipt_envelope)
    result = core.commit_evidence_receipt(ledger_path=ledger_path, receipt_envelope=receipt_envelope)
    validate_evidence_receipt(result.artifact)
    return result


def commit_world_feedback(*, ledger_path: Path, feedback_envelope: Mapping[str, Any]) -> CommitResult:
    _validate_existing_ledger(ledger_path, validate_world_feedback_candidate)
    validate_world_feedback_candidate(feedback_envelope)
    result = core.commit_world_feedback(ledger_path=ledger_path, feedback_envelope=feedback_envelope)
    validate_world_feedback_candidate(result.artifact)
    return result


__all__ = [
    "CommitResult",
    "build_authorized_observe_request",
    "build_world_feedback_candidate",
    "commit_evidence_receipt",
    "commit_observe_request",
    "commit_world_feedback",
    "make_observation_authorization_receipt",
    "make_observation_evidence_receipt",
    "validate_authorization_receipt",
    "validate_evidence_receipt",
    "validate_observe_request",
    "validate_world_feedback_candidate",
]
