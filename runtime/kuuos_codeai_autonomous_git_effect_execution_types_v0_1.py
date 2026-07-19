#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping
import re

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
)

VERSION = "kuuos_codeai_autonomous_git_effect_execution_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Git Effect Execution v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

PHASE_LOCAL_COMMIT = "local_commit"
PHASE_PUSH = "push_branch"
PHASE_CREATE_PR = "create_pull_request"
PHASE_MARK_PR_READY = "mark_pull_request_ready"
PHASE_MERGE = "merge_pull_request"
SUPPORTED_PHASES = (
    PHASE_LOCAL_COMMIT,
    PHASE_PUSH,
    PHASE_CREATE_PR,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
)

DISPOSITION_COMPLETED = "autonomous_git_effect_execution_completed"
DISPOSITION_FAILED = "autonomous_git_effect_execution_failed"
DISPOSITION_EVIDENCE_QUARANTINED = "autonomous_git_effect_evidence_quarantined"

MODE_LOCAL = "bounded_local_git_effect_execution"
MODE_REMOTE = "bounded_remote_git_effect_execution"
MODE_PR = "bounded_pull_request_effect_execution"
MODE_MERGE = "bounded_merge_effect_execution"

REQUEST_DIGEST_FIELD = "codeai_autonomous_git_effect_execution_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_git_effect_execution_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_autonomous_git_effect_execution_registry_digest"
EVIDENCE_DIGEST_FIELD = "codeai_autonomous_git_effect_execution_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_git_effect_execution_receipt_digest"

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_BRANCH = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\|[~^:?*\[]))(?!.*\.$)[^\s]+$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")

_SOURCE_AUTHORITY_FIELDS = {
    PHASE_LOCAL_COMMIT: "local_commit_authority_granted",
    PHASE_PUSH: "push_authority_granted",
    PHASE_CREATE_PR: "pull_request_authority_granted",
    PHASE_MARK_PR_READY: "pull_request_readiness_authority_granted",
    PHASE_MERGE: "merge_authority_granted",
}
_SOURCE_DISPOSITIONS = {
    PHASE_LOCAL_COMMIT: "autonomous_local_commit_authorized",
    PHASE_PUSH: "autonomous_branch_push_authorized",
    PHASE_CREATE_PR: "autonomous_pull_request_creation_authorized",
    PHASE_MARK_PR_READY: "autonomous_pull_request_readiness_authorized",
    PHASE_MERGE: "autonomous_pull_request_merge_authorized",
}
_SOURCE_MODES = {
    PHASE_LOCAL_COMMIT: "local_git_effect_authorized",
    PHASE_PUSH: "remote_git_effect_authorized",
    PHASE_CREATE_PR: "pull_request_effect_authorized",
    PHASE_MARK_PR_READY: "pull_request_effect_authorized",
    PHASE_MERGE: "merge_effect_authorized",
}

SOURCE_FIELDS = {
    "schema_version", "profile_version", "source_trajectory_receipt_digest",
    "git_lifecycle_request_digest", "git_lifecycle_state_digest",
    "git_lifecycle_policy_digest", "lifecycle_id", "execution_session_id",
    "repository_full_name", "source_commit_sha", "executor_id", "base_branch",
    "head_branch", "remote_name", "change_set_digest", "commit_message_digest",
    "merge_method", "next_effect_phase", "codeai_disposition", "operating_mode",
    "route_receipt_recorded", "execution_lease_issued",
    "local_commit_authority_granted", "push_authority_granted",
    "pull_request_authority_granted", "pull_request_readiness_authority_granted",
    "merge_authority_granted", "checks_wait_required", "human_handover_deferred",
    "effect_execution_performed_by_kernel", "local_commit_created_observed",
    "local_commit_sha", "branch_pushed_observed", "pushed_head_sha",
    "pull_request_created_observed", "pull_request_number",
    "pull_request_draft_observed", "required_checks_observed",
    "all_required_checks_successful", "no_pending_checks", "no_failed_checks",
    "successful_check_names", "pending_check_names", "failed_check_names",
    "mergeable_observed", "unresolved_blocker_count", "head_sha_pinned",
    "merge_performed_observed", "merge_commit_sha", "force_push_performed",
    "remote_branch_deleted", "admin_merge_bypass_used", "human_handover_performed",
    "external_authority_handover_performed", "deployment_authority_granted",
    "deployment_performed", "secret_access_authority_granted",
    "secret_access_performed", "source_receipt_treated_as_git_authority",
    "checks_treated_as_correctness_proof", "merge_treated_as_truth",
    "history_read_only", "future_only", "active_now", SOURCE_RECEIPT_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "execution_id", "execution_revision", "execution_session_id",
    "execution_nonce_digest", "source_lifecycle_receipt_digest", "lifecycle_id",
    "executor_id", "repository_full_name", "source_commit_sha", "base_branch",
    "head_branch", "remote_name", "merge_method", "change_set_digest",
    "commit_message", "commit_message_digest", "pull_request_title",
    "pull_request_body", "pull_request_body_digest", "pull_request_draft",
    "pull_request_number", "expected_head_sha", "requested_effect_phase",
    "request_created_epoch", "provenance_integrity_confirmed",
    "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_lifecycle_receipt_digest", "expected_repository_full_name",
    "authorized_executor_ids", "allowed_effect_phases", "allowed_base_branches",
    "allowed_head_branch_prefixes", "allowed_remote_names", "allowed_merge_methods",
    "allow_local_commit", "allow_push", "allow_pull_request_creation",
    "allow_pull_request_readiness", "allow_merge", "allow_force_push",
    "allow_remote_branch_deletion", "allow_admin_merge_bypass",
    "allow_deployment", "allow_secret_material_read", "allow_opaque_token_use",
    "maximum_command_count", "maximum_output_bytes", "maximum_timeout_seconds",
    "maximum_request_age", "maximum_registry_entries", "evaluation_epoch", POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_lifecycle_receipt_digests",
    "consumed_execution_nonce_digests", "consumed_count", "last_execution_epoch",
    REGISTRY_DIGEST_FIELD,
}

ADAPTER_RESULT_FIELDS = {
    "adapter_id", "adapter_session_id", "effect_phase", "status", "exit_code",
    "command_count", "stdout", "stderr", "completed_epoch",
    "local_commit_created", "local_commit_sha", "local_commit_parent_sha",
    "branch_pushed", "pushed_head_sha", "pull_request_created",
    "pull_request_number", "pull_request_url_digest", "pull_request_draft",
    "pr_head_sha", "pr_base_branch", "pull_request_marked_ready",
    "merge_performed", "merged_head_sha", "merge_commit_sha",
    "force_push_performed", "remote_branch_deleted", "admin_merge_bypass_used",
    "deployment_performed", "secret_material_read", "token_material_emitted",
    "opaque_token_used", "exception_type",
}


@dataclass(frozen=True)
class GitEffectInvocation:
    effect_phase: str
    repository_full_name: str
    source_commit_sha: str
    base_branch: str
    head_branch: str
    remote_name: str
    merge_method: str
    change_set_digest: str
    commit_message: str
    pull_request_title: str
    pull_request_body: str
    pull_request_draft: bool
    pull_request_number: int
    expected_head_sha: str
    maximum_command_count: int
    maximum_output_bytes: int
    maximum_timeout_seconds: int
    opaque_token_use_allowed: bool
    secret_material_read_allowed: bool


GitEffectAdapter = Callable[[GitEffectInvocation], Mapping[str, Any]]


@dataclass(frozen=True)
class CodeAIAutonomousGitEffectExecutionResult:
    status: str
    issues: tuple[str, ...]
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


def _strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _unique_strings(value: Any, *, nonempty: bool = False) -> tuple[str, ...] | None:
    parsed = _strings(value)
    if parsed is None or len(parsed) != len(set(parsed)):
        return None
    if nonempty and (not parsed or not all(parsed)):
        return None
    return parsed


__all__ = [name for name in globals() if not name.startswith("__")]
