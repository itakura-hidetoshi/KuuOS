#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Callable, Mapping

from runtime.kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1 import (
    ADAPTER_RESULT_DIGEST_FIELD as PERSISTENCE_ADAPTER_RESULT_DIGEST_FIELD,
    CHECKPOINT_ENVELOPE_DIGEST_FIELD,
    DISPOSITION_PERSISTED,
    EVIDENCE_DIGEST_FIELD as PERSISTENCE_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as PERSISTENCE_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as PERSISTENCE_REGISTRY_DIGEST_FIELD,
    STORE_STATE_DIGEST_FIELD,
    canonical_digest,
    digest_without,
)

VERSION = "kuuos_codeai_durable_git_lifecycle_loop_resumption_admission_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Durable Git Lifecycle Loop Resumption Admission v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

DISPOSITION_ADMITTED = "durable_git_lifecycle_loop_resumption_input_admitted"
DISPOSITION_UNAVAILABLE = "durable_git_lifecycle_loop_checkpoint_read_unavailable"
DISPOSITION_FAILED = "durable_git_lifecycle_loop_checkpoint_read_failed"
DISPOSITION_EVIDENCE_QUARANTINED = (
    "durable_git_lifecycle_loop_checkpoint_read_evidence_quarantined"
)

ADAPTER_STATUS_VERIFIED = "verified"
ADAPTER_STATUS_UNAVAILABLE = "unavailable"
ADAPTER_STATUS_FAILED = "failed"
ADAPTER_STATUS_QUARANTINED = "quarantined"

REQUEST_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_admission_request_digest"
POLICY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_admission_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_admission_registry_digest"
READ_RESULT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_checkpoint_read_result_digest"
RESUME_INPUT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resume_input_digest"
EVIDENCE_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_admission_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_durable_git_lifecycle_loop_resumption_admission_receipt_digest"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")

REQUEST_FIELDS = {
    "resumption_session_id", "resumption_nonce_digest", "checkpoint_id",
    "checkpoint_envelope_digest", "source_persistence_receipt_digest",
    "source_persistence_evidence_digest", "source_persistence_registry_digest",
    "source_store_state_digest", "loop_id", "lifecycle_id",
    "repository_full_name", "store_id", "reader_id", "adapter_id",
    "requested_resume_effect_budget", "requested_resume_execution_command_budget",
    "requested_resume_execution_output_bytes", "request_created_epoch",
    "provenance_integrity_confirmed", "source_correspondence_confirmed",
    "checkpoint_read_requested", "resumption_input_requested", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_persistence_receipt_digest",
    "expected_source_persistence_evidence_digest",
    "expected_checkpoint_envelope_digest", "expected_repository_full_name",
    "authorized_reader_ids", "allowed_adapter_ids", "allowed_store_ids",
    "maximum_request_age", "maximum_registry_entries",
    "maximum_adapter_command_count", "maximum_adapter_output_bytes",
    "maximum_resume_effect_budget", "maximum_resume_execution_command_budget",
    "maximum_resume_execution_output_bytes", "evaluation_epoch",
    "allow_checkpoint_read", "require_committed_checkpoint",
    "require_exact_checkpoint_envelope_digest", "require_nonce_consumption",
    "allow_resumption_input_issuance", "allow_loop_execution", "allow_git_effect",
    "allow_automatic_resumption", "allow_network_access",
    "allow_secret_material_read", "allow_general_successor_authority",
    POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_resumption_nonce_digests",
    "admitted_checkpoint_ids", "admitted_checkpoint_envelope_digests",
    "admitted_persistence_receipt_digests", "resumption_attempt_count",
    "successful_resumption_admission_count", "last_resumption_epoch",
    REGISTRY_DIGEST_FIELD,
}

READ_RESULT_FIELDS = {
    "adapter_id", "adapter_session_id", "store_id", "checkpoint_id",
    "checkpoint_envelope_digest", "checkpoint_envelope", "status",
    "command_count", "output_bytes", "completed_epoch", "checkpoint_found",
    "checkpoint_read_performed", "network_accessed", "secret_material_read",
    "git_effect_performed", "loop_executed", "resume_input_issued",
    "arbitrary_command_executed", "exception_type", READ_RESULT_DIGEST_FIELD,
}

CHECKPOINT_ENVELOPE_REQUIRED_FIELDS = {
    "schema_version", "profile_version", "checkpoint_id", "checkpoint_revision",
    "source_loop_receipt_digest", "source_loop_evidence_digest",
    "source_loop_registry_digest", "source_execution_registry_digest",
    "source_reobservation_registry_digest", "source_continuation_registry_digest",
    "final_lifecycle_receipt_digest", "final_lifecycle_state_digest", "loop_id",
    "lifecycle_id", "repository_full_name", "loop_disposition", "effect_count",
    "maximum_effect_count", "final_lifecycle_completed",
    "final_execution_lease_issued", "persistence_request_digest",
    "persistence_policy_digest", "created_epoch", "resume_input_issued",
    "automatic_resumption_performed", "general_successor_stage_authority_granted",
    CHECKPOINT_ENVELOPE_DIGEST_FIELD,
}


@dataclass(frozen=True)
class DurableCheckpointReadInvocation:
    adapter_id: str
    resumption_session_id: str
    store_id: str
    checkpoint_id: str
    checkpoint_envelope_digest: str
    maximum_command_count: int
    maximum_output_bytes: int
    network_access_allowed: bool
    secret_material_read_allowed: bool


DurableCheckpointReadAdapter = Callable[
    [DurableCheckpointReadInvocation], Mapping[str, Any]
]


@dataclass(frozen=True)
class CodeAIDurableGitLifecycleLoopResumptionAdmissionResult:
    status: str
    issues: tuple[str, ...]
    resume_input: dict[str, Any] | None
    evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any, *, positive: bool = False) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    if positive and value == 0:
        return None
    return value


def _strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    parsed = tuple(value)
    if len(parsed) != len(set(parsed)):
        return None
    if nonempty and (not parsed or not all(parsed)):
        return None
    return parsed


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _digest_ok(value: Mapping[str, Any], field: str) -> bool:
    return value.get(field) == digest_without(value, field)


__all__ = [name for name in globals() if name.isupper()] + [
    "DurableCheckpointReadInvocation",
    "DurableCheckpointReadAdapter",
    "CodeAIDurableGitLifecycleLoopResumptionAdmissionResult",
    "asdict", "canonical_digest", "digest_without", "_mapping", "_nat",
    "_strings", "_exact_fields", "_digest_ok",
]
