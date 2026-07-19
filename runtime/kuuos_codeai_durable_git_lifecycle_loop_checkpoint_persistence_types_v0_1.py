#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Callable, Mapping

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as LIFECYCLE_RECEIPT_DIGEST_FIELD,
    STATE_DIGEST_FIELD as LIFECYCLE_STATE_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import (
    REGISTRY_DIGEST_FIELD as EXECUTION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_autonomous_git_effect_reobservation_v0_1 import (
    REGISTRY_DIGEST_FIELD as REOBSERVATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_reobservation_gated_git_lifecycle_continuation_v0_1 import (
    REGISTRY_DIGEST_FIELD as CONTINUATION_REGISTRY_DIGEST_FIELD,
)
from runtime.kuuos_codeai_bounded_autonomous_git_lifecycle_loop_orchestration_v0_1 import (
    DISPOSITION_COMPLETED as LOOP_COMPLETED,
    DISPOSITION_EFFECT_BUDGET_EXHAUSTED as LOOP_EFFECT_BUDGET_EXHAUSTED,
    DISPOSITION_EXECUTION_FAILED as LOOP_EXECUTION_FAILED,
    DISPOSITION_EXECUTION_QUARANTINED as LOOP_EXECUTION_QUARANTINED,
    DISPOSITION_REOBSERVATION_FAILED as LOOP_REOBSERVATION_FAILED,
    DISPOSITION_REOBSERVATION_QUARANTINED as LOOP_REOBSERVATION_QUARANTINED,
    DISPOSITION_STAGE_BLOCKED as LOOP_STAGE_BLOCKED,
    DISPOSITION_TERMINAL_HOLD as LOOP_TERMINAL_HOLD,
    EVIDENCE_DIGEST_FIELD as LOOP_EVIDENCE_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as LOOP_RECEIPT_DIGEST_FIELD,
    REGISTRY_DIGEST_FIELD as LOOP_REGISTRY_DIGEST_FIELD,
    canonical_digest,
    digest_without,
)

VERSION = "kuuos_codeai_durable_git_lifecycle_loop_checkpoint_persistence_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Durable Git Lifecycle Loop Checkpoint Persistence v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

DISPOSITION_PERSISTED = "durable_git_lifecycle_loop_checkpoint_persisted"
DISPOSITION_CONFLICT = "durable_git_lifecycle_loop_checkpoint_compare_and_swap_conflict"
DISPOSITION_FAILED = "durable_git_lifecycle_loop_checkpoint_persistence_failed"
DISPOSITION_EVIDENCE_QUARANTINED = (
    "durable_git_lifecycle_loop_checkpoint_persistence_evidence_quarantined"
)

ADAPTER_STATUS_COMMITTED = "committed"
ADAPTER_STATUS_CONFLICT = "conflict"
ADAPTER_STATUS_FAILED = "failed"
ADAPTER_STATUS_QUARANTINED = "quarantined"

REQUEST_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_persistence_request_digest"
)
POLICY_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_persistence_policy_digest"
)
REGISTRY_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_persistence_registry_digest"
)
STORE_STATE_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_store_state_digest"
)
CHECKPOINT_ENVELOPE_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_envelope_digest"
)
ADAPTER_RESULT_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_adapter_result_digest"
)
EVIDENCE_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_persistence_evidence_digest"
)
RECEIPT_DIGEST_FIELD = (
    "codeai_durable_git_lifecycle_loop_checkpoint_persistence_receipt_digest"
)

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_IDENTIFIER = re.compile(r"^[A-Za-z0-9_.:/-]+$")

SUPPORTED_LOOP_DISPOSITIONS = {
    LOOP_COMPLETED,
    LOOP_TERMINAL_HOLD,
    LOOP_EFFECT_BUDGET_EXHAUSTED,
    LOOP_EXECUTION_FAILED,
    LOOP_EXECUTION_QUARANTINED,
    LOOP_REOBSERVATION_FAILED,
    LOOP_REOBSERVATION_QUARANTINED,
    LOOP_STAGE_BLOCKED,
}

REQUEST_FIELDS = {
    "checkpoint_id", "checkpoint_revision", "persistence_session_id",
    "persistence_nonce_digest", "source_loop_receipt_digest",
    "source_loop_evidence_digest", "source_loop_registry_digest",
    "source_execution_registry_digest", "source_reobservation_registry_digest",
    "source_continuation_registry_digest", "final_lifecycle_receipt_digest",
    "final_lifecycle_state_digest", "loop_id", "lifecycle_id",
    "repository_full_name", "persister_id", "adapter_id", "store_id",
    "expected_store_revision", "request_created_epoch",
    "provenance_integrity_confirmed", "source_correspondence_confirmed",
    "persistence_requested", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_loop_receipt_digest", "expected_source_loop_evidence_digest",
    "expected_repository_full_name", "authorized_persister_ids",
    "allowed_adapter_ids", "allowed_store_ids", "maximum_request_age",
    "maximum_registry_entries", "maximum_store_entries",
    "maximum_adapter_command_count", "maximum_adapter_output_bytes",
    "evaluation_epoch", "allow_checkpoint_persistence",
    "require_atomic_compare_and_swap", "require_checkpoint_absence",
    "require_nonce_consumption", "allow_checkpoint_overwrite",
    "allow_checkpoint_delete", "allow_network_access",
    "allow_secret_material_read", "allow_git_effect", "allow_loop_execution",
    "allow_resume_input_issuance", "allow_automatic_resumption",
    "allow_general_successor_authority", POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_persistence_nonce_digests",
    "persisted_loop_receipt_digests", "persisted_checkpoint_ids",
    "persistence_attempt_count", "successful_persistence_count",
    "last_persistence_epoch", REGISTRY_DIGEST_FIELD,
}

STORE_STATE_FIELDS = {
    "schema_version", "profile_version", "store_id", "store_revision",
    "checkpoint_ids", "checkpoint_envelope_digests", "last_committed_epoch",
    STORE_STATE_DIGEST_FIELD,
}

ADAPTER_RESULT_FIELDS = {
    "adapter_id", "adapter_session_id", "store_id", "checkpoint_id",
    "expected_store_revision", "observed_store_revision",
    "committed_store_revision", "checkpoint_envelope_digest", "status",
    "command_count", "output_bytes", "completed_epoch",
    "atomic_compare_and_swap_attempted", "atomic_compare_and_swap_succeeded",
    "checkpoint_absent_before_write", "write_committed",
    "checkpoint_overwritten", "checkpoint_deleted", "network_accessed",
    "secret_material_read", "git_effect_performed", "loop_executed",
    "resume_input_issued", "arbitrary_command_executed", "exception_type",
    ADAPTER_RESULT_DIGEST_FIELD,
}

_REQUEST_STRING_FIELDS = REQUEST_FIELDS - {
    "checkpoint_revision", "expected_store_revision", "request_created_epoch",
    "provenance_integrity_confirmed", "source_correspondence_confirmed",
    "persistence_requested", REQUEST_DIGEST_FIELD,
}
_POLICY_LIST_FIELDS = {
    "authorized_persister_ids", "allowed_adapter_ids", "allowed_store_ids",
}
_POLICY_NAT_FIELDS = {
    "maximum_request_age", "maximum_registry_entries", "maximum_store_entries",
    "maximum_adapter_command_count", "maximum_adapter_output_bytes",
    "evaluation_epoch",
}
_POLICY_STRING_FIELDS = {
    "expected_source_loop_receipt_digest", "expected_source_loop_evidence_digest",
    "expected_repository_full_name", POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class DurableCheckpointPersistenceInvocation:
    adapter_id: str
    persistence_session_id: str
    store_id: str
    checkpoint_id: str
    expected_store_revision: int
    checkpoint_envelope_digest: str
    checkpoint_envelope: Mapping[str, Any]
    maximum_command_count: int
    maximum_output_bytes: int
    network_access_allowed: bool
    secret_material_read_allowed: bool


DurableCheckpointPersistenceAdapter = Callable[
    [DurableCheckpointPersistenceInvocation], Mapping[str, Any]
]


@dataclass(frozen=True)
class CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult:
    status: str
    issues: tuple[str, ...]
    checkpoint_envelope: dict[str, Any] | None
    evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    next_store_state: dict[str, Any] | None
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
    "DurableCheckpointPersistenceInvocation",
    "DurableCheckpointPersistenceAdapter",
    "CodeAIDurableGitLifecycleLoopCheckpointPersistenceResult",
    "asdict",
    "canonical_digest",
    "digest_without",
    "_mapping",
    "_nat",
    "_strings",
    "_exact_fields",
    "_digest_ok",
]
