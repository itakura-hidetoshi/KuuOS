from __future__ import annotations

from typing import Any

from runtime.kuuos_apoptosis_bounded_execution_preparation_types_v0_8 import (
    ApoptosisBoundedExecutionPreparationEvidence,
    ApoptosisBoundedExecutionPreparationPolicy,
    ApoptosisBoundedExecutionPreparationRecord,
    ApoptosisBoundedExecutionPreparationRequest,
)


SOURCE_LAYOUT = (
    ("authorization_request", "request_digest"),
    ("authorization_evidence", "evidence_digest"),
    ("authorization_policy", "policy_digest"),
    ("authorization_record", "record_digest"),
    ("external_request", "request_digest"),
    ("external_evidence", "evidence_digest"),
    ("external_policy", "policy_digest"),
    ("external_record", "record_digest"),
    ("quiescence_request", "request_digest"),
    ("quiescence_evidence", "evidence_digest"),
    ("quiescence_policy", "policy_digest"),
    ("quiescence_record", "record_digest"),
    ("authority_request", "request_digest"),
    ("authority_evidence", "evidence_digest"),
    ("authority_policy", "policy_digest"),
    ("authority_record", "record_digest"),
    ("dependency_request", "request_digest"),
    ("dependency_evidence", "evidence_digest"),
    ("dependency_policy", "policy_digest"),
    ("dependency_record", "record_digest"),
    ("observation_input", "input_digest"),
    ("observation_policy", "policy_digest"),
    ("observation_record", "record_digest"),
    ("candidate_request", "request_digest"),
    ("candidate_policy", "policy_digest"),
    ("candidate_record", "candidate_digest"),
)


def named_source(source_args: tuple[Any, ...]) -> dict[str, Any]:
    if len(source_args) != len(SOURCE_LAYOUT):
        raise ValueError("source_argument_count_invalid")
    return {
        name: value
        for (name, _), value in zip(SOURCE_LAYOUT, source_args, strict=True)
    }


def source_digests(
    preparation_request: ApoptosisBoundedExecutionPreparationRequest,
    preparation_evidence: ApoptosisBoundedExecutionPreparationEvidence,
    preparation_policy: ApoptosisBoundedExecutionPreparationPolicy,
    preparation_record: ApoptosisBoundedExecutionPreparationRecord,
    source_args: tuple[Any, ...],
) -> dict[str, str]:
    named = named_source(source_args)
    result = {
        name: getattr(named[name], field)
        for name, field in SOURCE_LAYOUT
    }
    result.update(
        preparation_request=preparation_request.request_digest,
        preparation_evidence=preparation_evidence.evidence_digest,
        preparation_policy=preparation_policy.policy_digest,
        preparation_record=preparation_record.record_digest,
    )
    return result
