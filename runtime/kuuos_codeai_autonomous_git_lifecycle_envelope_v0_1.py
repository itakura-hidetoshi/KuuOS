#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Git Lifecycle v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_LOCAL_GIT_AUTHORIZED = "local_git_effect_authorized"
MODE_REMOTE_GIT_AUTHORIZED = "remote_git_effect_authorized"
MODE_PR_AUTHORIZED = "pull_request_effect_authorized"
MODE_MERGE_AUTHORIZED = "merge_effect_authorized"
MODE_AWAITING_CHECKS = "awaiting_required_checks"
MODE_DEGRADED_AUTONOMY = "degraded_autonomy"
MODE_COMPLETED = "completed"
MODE_HOLD = "hold"
MODE_ABSTAIN = "abstain"
MODE_REJECTED = "rejected"

PHASE_LOCAL_COMMIT = "local_commit"
PHASE_PUSH = "push_branch"
PHASE_CREATE_PR = "create_pull_request"
PHASE_MARK_PR_READY = "mark_pull_request_ready"
PHASE_AWAIT_CHECKS = "await_required_checks"
PHASE_MERGE = "merge_pull_request"
PHASE_COMPLETE = "complete"
PHASE_NONE = "none"

DISPOSITION_LOCAL_COMMIT_AUTHORIZED = "autonomous_local_commit_authorized"
DISPOSITION_PUSH_AUTHORIZED = "autonomous_branch_push_authorized"
DISPOSITION_PR_AUTHORIZED = "autonomous_pull_request_creation_authorized"
DISPOSITION_PR_READY_AUTHORIZED = "autonomous_pull_request_readiness_authorized"
DISPOSITION_CHECKS_PENDING = "required_checks_pending_hold"
DISPOSITION_CHECKS_FAILED = "required_checks_failed_degraded"
DISPOSITION_MERGE_GATE_HOLD = "pull_request_merge_gate_hold"
DISPOSITION_MERGE_AUTHORIZED = "autonomous_pull_request_merge_authorized"
DISPOSITION_COMPLETED = "autonomous_git_lifecycle_completed"
DISPOSITION_SOURCE_RECEIPT_REPAIR = "source_trajectory_receipt_repair_required"
DISPOSITION_REQUEST_PROVENANCE_REPAIR = "git_lifecycle_provenance_repair_required"
DISPOSITION_STATE_EVIDENCE_REPAIR = "git_lifecycle_state_evidence_repair_required"
DISPOSITION_CORRESPONDENCE_REPAIR = "git_lifecycle_correspondence_repair_required"
DISPOSITION_WINDOW_REPAIR = "git_lifecycle_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "git_lifecycle_replay_conflict_rejected"
DISPOSITION_SCOPE_ABSTAINED = "unsupported_git_lifecycle_scope_abstained"
DISPOSITION_DESTRUCTIVE_REJECTED = "destructive_git_effect_rejected"
DISPOSITION_HANDOVER_DEFERRED = "human_handover_deferred"
DISPOSITION_STATE_REPAIR = "git_lifecycle_state_repair_required"

REQUEST_DIGEST_FIELD = "codeai_autonomous_git_lifecycle_request_digest"
STATE_DIGEST_FIELD = "codeai_autonomous_git_lifecycle_state_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_git_lifecycle_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_git_lifecycle_receipt_digest"

SOURCE_RECEIPT_FIELDS = {
    "schema_version",
    "profile_version",
    "source_verification_receipt_digest",
    "source_candidate_receipt_digest",
    "trajectory_request_digest",
    "trajectory_policy_digest",
    "candidate_id",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "verification_evidence_digest",
    "verification_outcome",
    "trajectory_id",
    "trajectory_revision",
    "trajectory_format",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "trajectory_node_ids",
    "trajectory_node_digests",
    "trajectory_step_count",
    "next_internal_step_kind",
    "codeai_disposition",
    "operating_mode",
    "route_receipt_recorded",
    "trajectory_synthesized_by_kernel",
    "trajectory_read_only",
    "trajectory_complete_for_available_receipts",
    "full_intent_lineage_reconstructed",
    "autonomous_deliberation_candidate_generated",
    "autonomous_repair_candidate_generated",
    "autonomous_reverification_candidate_generated",
    "clarification_required",
    "evidence_degraded",
    "abstained",
    "external_handover_deferred",
    "human_handover_performed",
    "external_authority_handover_performed",
    "candidate_selected",
    "patch_generated",
    "patch_applied",
    "execution_lease_issued",
    "repository_mutation_performed",
    "git_ref_changed",
    "branch_created",
    "commit_created",
    "push_performed",
    "pull_request_created",
    "merge_performed",
    "deployment_performed",
    "secret_access_performed",
    "selection_authority_granted",
    "verification_authority_granted",
    "execution_authority_granted",
    "merge_authority_granted",
    "deployment_authority_granted",
    "secret_access_authority_granted",
    "source_receipt_treated_as_successor_authority",
    "trajectory_treated_as_truth",
    "autonomous_candidate_treated_as_authority",
    "history_read_only",
    "future_only",
    "active_now",
    SOURCE_RECEIPT_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "lifecycle_id",
    "lifecycle_revision",
    "execution_session_id",
    "execution_nonce_digest",
    "source_trajectory_receipt_digest",
    "repository_full_name",
    "source_commit_sha",
    "executor_id",
    "base_branch",
    "head_branch",
    "remote_name",
    "change_set_digest",
    "commit_message_digest",
    "merge_method",
    "local_commit_requested",
    "push_requested",
    "pull_request_requested",
    "merge_requested",
    "force_push_requested",
    "remote_branch_delete_requested",
    "admin_merge_requested",
    "human_handover_requested",
    "request_created_epoch",
    "prior_execution_session_ids",
    "prior_execution_nonce_digests",
    "prior_lifecycle_receipt_digests",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    REQUEST_DIGEST_FIELD,
}

STATE_FIELDS = {
    "lifecycle_id",
    "source_trajectory_receipt_digest",
    "repository_full_name",
    "source_commit_sha",
    "executor_id",
    "base_branch",
    "head_branch",
    "remote_name",
    "change_set_digest",
    "commit_message_digest",
    "merge_method",
    "local_commit_created",
    "local_commit_sha",
    "local_commit_parent_sha",
    "branch_pushed",
    "pushed_head_sha",
    "pull_request_created",
    "pull_request_number",
    "pull_request_url_digest",
    "pull_request_draft",
    "pr_head_sha",
    "pr_base_branch",
    "checks_observed",
    "required_check_names",
    "successful_check_names",
    "pending_check_names",
    "failed_check_names",
    "mergeable",
    "unresolved_blocker_count",
    "merge_performed",
    "merged_head_sha",
    "merge_commit_sha",
    "force_push_performed",
    "remote_branch_deleted",
    "admin_merge_bypass_used",
    "human_handover_performed",
    "external_authority_handover_performed",
    "observed_at_epoch",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    STATE_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_trajectory_receipt_digest",
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "authorized_executor_ids",
    "allowed_base_branches",
    "allowed_head_branch_prefixes",
    "allowed_remote_names",
    "allowed_merge_methods",
    "required_check_names",
    "allow_local_commit",
    "allow_push",
    "allow_pull_request_creation",
    "allow_pull_request_readiness",
    "allow_merge",
    "allow_force_push",
    "allow_remote_branch_deletion",
    "allow_admin_merge_bypass",
    "require_non_draft_for_merge",
    "require_mergeable",
    "require_head_sha_pin",
    "require_no_unresolved_blockers",
    "explicit_automerge_license",
    "evaluation_epoch",
    "maximum_request_age",
    "maximum_state_age",
    POLICY_DIGEST_FIELD,
}

_SOURCE_STRING_FIELDS = (
    "schema_version",
    "profile_version",
    "source_verification_receipt_digest",
    "source_candidate_receipt_digest",
    "trajectory_request_digest",
    "trajectory_policy_digest",
    "candidate_id",
    "candidate_patch_digest",
    "patch_artifact_digest",
    "verification_evidence_digest",
    "verification_outcome",
    "trajectory_id",
    "trajectory_revision",
    "trajectory_format",
    "repository_full_name",
    "source_commit_sha",
    "resulting_commit_sha",
    "next_internal_step_kind",
    "codeai_disposition",
    "operating_mode",
    SOURCE_RECEIPT_DIGEST_FIELD,
)

_SOURCE_LIST_FIELDS = ("trajectory_node_ids", "trajectory_node_digests")
_SOURCE_NAT_FIELDS = ("trajectory_step_count",)
_SOURCE_BOOL_FIELDS = tuple(
    sorted(
        SOURCE_RECEIPT_FIELDS
        - set(_SOURCE_STRING_FIELDS)
        - set(_SOURCE_LIST_FIELDS)
        - set(_SOURCE_NAT_FIELDS)
    )
)

_REQUEST_STRING_FIELDS = (
    "lifecycle_id",
    "lifecycle_revision",
    "execution_session_id",
    "execution_nonce_digest",
    "source_trajectory_receipt_digest",
    "repository_full_name",
    "source_commit_sha",
    "executor_id",
    "base_branch",
    "head_branch",
    "remote_name",
    "change_set_digest",
    "commit_message_digest",
    "merge_method",
    REQUEST_DIGEST_FIELD,
)
_REQUEST_LIST_FIELDS = (
    "prior_execution_session_ids",
    "prior_execution_nonce_digests",
    "prior_lifecycle_receipt_digests",
)
_REQUEST_NAT_FIELDS = ("request_created_epoch",)
_REQUEST_BOOL_FIELDS = tuple(
    sorted(
        REQUEST_FIELDS
        - set(_REQUEST_STRING_FIELDS)
        - set(_REQUEST_LIST_FIELDS)
        - set(_REQUEST_NAT_FIELDS)
    )
)

_STATE_STRING_FIELDS = (
    "lifecycle_id",
    "source_trajectory_receipt_digest",
    "repository_full_name",
    "source_commit_sha",
    "executor_id",
    "base_branch",
    "head_branch",
    "remote_name",
    "change_set_digest",
    "commit_message_digest",
    "merge_method",
    "local_commit_sha",
    "local_commit_parent_sha",
    "pushed_head_sha",
    "pull_request_url_digest",
    "pr_head_sha",
    "pr_base_branch",
    "merged_head_sha",
    "merge_commit_sha",
    STATE_DIGEST_FIELD,
)
_STATE_LIST_FIELDS = (
    "required_check_names",
    "successful_check_names",
    "pending_check_names",
    "failed_check_names",
)
_STATE_NAT_FIELDS = (
    "pull_request_number",
    "unresolved_blocker_count",
    "observed_at_epoch",
)
_STATE_BOOL_FIELDS = tuple(
    sorted(
        STATE_FIELDS
        - set(_STATE_STRING_FIELDS)
        - set(_STATE_LIST_FIELDS)
        - set(_STATE_NAT_FIELDS)
    )
)

_POLICY_STRING_LIST_FIELDS = (
    "authorized_executor_ids",
    "allowed_base_branches",
    "allowed_head_branch_prefixes",
    "allowed_remote_names",
    "allowed_merge_methods",
    "required_check_names",
)

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_BRANCH = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\|[~^:?*\[]))(?!.*\.$)[^\s]+$")


@dataclass(frozen=True)
class CodeAIAutonomousGitLifecycleResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _positive_nat(value: Any) -> int | None:
    parsed = _nat(value)
    return parsed if parsed is not None and parsed > 0 else None


def _strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _unique_nonempty(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _exact_fields(value: Mapping[str, Any], fields: set[str], prefix: str) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
    return issues


def _validate_typed_mapping(
    value: Mapping[str, Any],
    *,
    fields: set[str],
    strings: tuple[str, ...],
    lists: tuple[str, ...],
    nats: tuple[str, ...],
    bools: tuple[str, ...],
    prefix: str,
    digest_field: str,
) -> list[str]:
    issues = _exact_fields(value, fields, prefix)
    if issues:
        return issues
    for field in strings:
        if not isinstance(value.get(field), str):
            issues.append(prefix + "_invalid_string:" + field)
    for field in lists:
        if _strings(value.get(field)) is None:
            issues.append(prefix + "_invalid_string_list:" + field)
    for field in nats:
        if _nat(value.get(field)) is None:
            issues.append(prefix + "_invalid_nat:" + field)
    for field in bools:
        if not isinstance(value.get(field), bool):
            issues.append(prefix + "_invalid_bool:" + field)
    if value.get(digest_field) != digest_without(value, digest_field):
        issues.append(prefix + "_digest_mismatch")
    return issues


def _validate_source(value: Mapping[str, Any]) -> list[str]:
    return _validate_typed_mapping(
        value,
        fields=SOURCE_RECEIPT_FIELDS,
        strings=_SOURCE_STRING_FIELDS,
        lists=_SOURCE_LIST_FIELDS,
        nats=_SOURCE_NAT_FIELDS,
        bools=_SOURCE_BOOL_FIELDS,
        prefix="source_trajectory_receipt",
        digest_field=SOURCE_RECEIPT_DIGEST_FIELD,
    )


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    return _validate_typed_mapping(
        value,
        fields=REQUEST_FIELDS,
        strings=_REQUEST_STRING_FIELDS,
        lists=_REQUEST_LIST_FIELDS,
        nats=_REQUEST_NAT_FIELDS,
        bools=_REQUEST_BOOL_FIELDS,
        prefix="git_lifecycle_request",
        digest_field=REQUEST_DIGEST_FIELD,
    )


def _validate_state(value: Mapping[str, Any]) -> list[str]:
    return _validate_typed_mapping(
        value,
        fields=STATE_FIELDS,
        strings=_STATE_STRING_FIELDS,
        lists=_STATE_LIST_FIELDS,
        nats=_STATE_NAT_FIELDS,
        bools=_STATE_BOOL_FIELDS,
        prefix="git_lifecycle_state",
        digest_field=STATE_DIGEST_FIELD,
    )


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "git_lifecycle_policy")
    if issues:
        return issues
    for field in (
        "expected_source_trajectory_receipt_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(value.get(field), str):
            issues.append("git_lifecycle_policy_invalid_string:" + field)
    for field in _POLICY_STRING_LIST_FIELDS:
        parsed = _strings(value.get(field))
        if parsed is None:
            issues.append("git_lifecycle_policy_invalid_string_list:" + field)
        elif not parsed or not all(parsed) or len(parsed) != len(set(parsed)):
            issues.append("git_lifecycle_policy_invalid_nonempty_unique_list:" + field)
    for field in ("evaluation_epoch",):
        if _nat(value.get(field)) is None:
            issues.append("git_lifecycle_policy_invalid_nat:" + field)
    for field in ("maximum_request_age", "maximum_state_age"):
        if _positive_nat(value.get(field)) is None:
            issues.append("git_lifecycle_policy_invalid_positive_nat:" + field)
    bool_fields = POLICY_FIELDS - {
        "expected_source_trajectory_receipt_digest",
        "expected_repository_full_name",
        "expected_source_commit_sha",
        *_POLICY_STRING_LIST_FIELDS,
        "evaluation_epoch",
        "maximum_request_age",
        "maximum_state_age",
        POLICY_DIGEST_FIELD,
    }
    for field in sorted(bool_fields):
        if not isinstance(value.get(field), bool):
            issues.append("git_lifecycle_policy_invalid_bool:" + field)
    if value.get(POLICY_DIGEST_FIELD) != digest_without(value, POLICY_DIGEST_FIELD):
        issues.append("git_lifecycle_policy_digest_mismatch")
    return issues


def _preflight(
    source_trajectory_receipt: Any,
    lifecycle_request: Any,
    lifecycle_state: Any,
    lifecycle_policy: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    tuple[str, ...],
]:
    source = _mapping(source_trajectory_receipt)
    request = _mapping(lifecycle_request)
    state = _mapping(lifecycle_state)
    policy = _mapping(lifecycle_policy)
    issues: list[str] = []
    if source is None:
        issues.append("source_trajectory_receipt_not_mapping")
    else:
        issues.extend(_validate_source(source))
    if request is None:
        issues.append("git_lifecycle_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if state is None:
        issues.append("git_lifecycle_state_not_mapping")
    else:
        issues.extend(_validate_state(state))
    if policy is None:
        issues.append("git_lifecycle_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    return source, request, state, policy, tuple(issues)


def _source_supported(source: Mapping[str, Any]) -> bool:
    false_fields = (
        "autonomous_repair_candidate_generated",
        "autonomous_reverification_candidate_generated",
        "clarification_required",
        "evidence_degraded",
        "abstained",
        "external_handover_deferred",
        "human_handover_performed",
        "external_authority_handover_performed",
        "candidate_selected",
        "patch_generated",
        "patch_applied",
        "execution_lease_issued",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
        "source_receipt_treated_as_successor_authority",
        "trajectory_treated_as_truth",
        "autonomous_candidate_treated_as_authority",
        "active_now",
    )
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI Autonomous Trajectory Synthesis v0.1"
        and source["codeai_disposition"]
        == "autonomous_deliberation_candidate_synthesized"
        and source["operating_mode"] == "autonomous_read_only"
        and source["verification_outcome"] == "passed"
        and source["next_internal_step_kind"] == "internal_deliberation_candidate"
        and source["route_receipt_recorded"] is True
        and source["trajectory_synthesized_by_kernel"] is True
        and source["trajectory_read_only"] is True
        and source["trajectory_complete_for_available_receipts"] is True
        and source["full_intent_lineage_reconstructed"] is False
        and source["autonomous_deliberation_candidate_generated"] is True
        and source["history_read_only"] is True
        and source["future_only"] is True
        and source["source_commit_sha"] == source["resulting_commit_sha"]
        and source["trajectory_step_count"] == len(source["trajectory_node_ids"])
        == len(source["trajectory_node_digests"])
        and source["trajectory_step_count"] > 0
        and _unique_nonempty(source["trajectory_node_ids"])
        and _unique_nonempty(source["trajectory_node_digests"])
        and all(_SHA256.fullmatch(item) for item in source["trajectory_node_digests"])
        and bool(_SHA256.fullmatch(source[SOURCE_RECEIPT_DIGEST_FIELD]))
        and bool(_SHA40.fullmatch(source["source_commit_sha"]))
        and all(source[field] is False for field in false_fields)
    )


def _request_provenance_valid(request: Mapping[str, Any]) -> bool:
    return (
        bool(request["lifecycle_id"])
        and bool(request["lifecycle_revision"])
        and bool(request["execution_session_id"])
        and bool(request["executor_id"])
        and request["provenance_integrity_confirmed"] is True
        and _unique_nonempty(request["prior_execution_session_ids"])
        and _unique_nonempty(request["prior_execution_nonce_digests"])
        and _unique_nonempty(request["prior_lifecycle_receipt_digests"])
        and bool(_SHA256.fullmatch(request["execution_nonce_digest"]))
        and bool(_SHA256.fullmatch(request["source_trajectory_receipt_digest"]))
        and bool(_SHA256.fullmatch(request["change_set_digest"]))
        and bool(_SHA256.fullmatch(request["commit_message_digest"]))
        and bool(_SHA40.fullmatch(request["source_commit_sha"]))
        and all(
            _SHA256.fullmatch(item)
            for item in request["prior_execution_nonce_digests"]
        )
        and all(
            _SHA256.fullmatch(item)
            for item in request["prior_lifecycle_receipt_digests"]
        )
    )


def _state_evidence_valid(state: Mapping[str, Any]) -> bool:
    return (
        bool(state["lifecycle_id"])
        and bool(state["executor_id"])
        and state["provenance_integrity_confirmed"] is True
        and bool(_SHA256.fullmatch(state["source_trajectory_receipt_digest"]))
        and bool(_SHA256.fullmatch(state["change_set_digest"]))
        and bool(_SHA256.fullmatch(state["commit_message_digest"]))
        and bool(_SHA40.fullmatch(state["source_commit_sha"]))
    )


def _correspondence_valid(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    shared = (
        "repository_full_name",
        "source_commit_sha",
        "executor_id",
        "base_branch",
        "head_branch",
        "remote_name",
        "change_set_digest",
        "commit_message_digest",
        "merge_method",
    )
    return (
        request["source_trajectory_receipt_digest"]
        == source[SOURCE_RECEIPT_DIGEST_FIELD]
        == state["source_trajectory_receipt_digest"]
        == policy["expected_source_trajectory_receipt_digest"]
        and request["repository_full_name"]
        == source["repository_full_name"]
        == state["repository_full_name"]
        == policy["expected_repository_full_name"]
        and request["source_commit_sha"]
        == source["source_commit_sha"]
        == state["source_commit_sha"]
        == policy["expected_source_commit_sha"]
        and request["lifecycle_id"] == state["lifecycle_id"]
        and all(request[field] == state[field] for field in shared)
        and request["source_correspondence_confirmed"] is True
        and state["source_correspondence_confirmed"] is True
    )


def _window_valid(
    request: Mapping[str, Any], state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    evaluated = policy["evaluation_epoch"]
    created = request["request_created_epoch"]
    observed = state["observed_at_epoch"]
    return (
        created <= observed <= evaluated
        and evaluated - created <= policy["maximum_request_age"]
        and evaluated - observed <= policy["maximum_state_age"]
    )


def _replay_closed(request: Mapping[str, Any]) -> bool:
    return (
        request["execution_session_id"] not in request["prior_execution_session_ids"]
        and request["execution_nonce_digest"]
        not in request["prior_execution_nonce_digests"]
        and request[REQUEST_DIGEST_FIELD]
        not in request["prior_lifecycle_receipt_digests"]
    )


def _branch_valid(value: str) -> bool:
    return bool(value) and bool(_BRANCH.fullmatch(value)) and not value.startswith("-")


def _scope_supported(
    request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["executor_id"] in policy["authorized_executor_ids"]
        and request["base_branch"] in policy["allowed_base_branches"]
        and any(
            request["head_branch"].startswith(prefix)
            for prefix in policy["allowed_head_branch_prefixes"]
        )
        and request["remote_name"] in policy["allowed_remote_names"]
        and request["merge_method"] in policy["allowed_merge_methods"]
        and _branch_valid(request["base_branch"])
        and _branch_valid(request["head_branch"])
        and request["base_branch"] != request["head_branch"]
        and request["local_commit_requested"] is True
        and request["push_requested"] is True
        and request["pull_request_requested"] is True
        and request["merge_requested"] is True
        and policy["allow_local_commit"] is True
        and policy["allow_push"] is True
        and policy["allow_pull_request_creation"] is True
        and policy["allow_pull_request_readiness"] is True
        and policy["allow_merge"] is True
        and policy["explicit_automerge_license"] is True
    )


def _destructive_requested(
    request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["force_push_requested"]
        or request["remote_branch_delete_requested"]
        or request["admin_merge_requested"]
        or policy["allow_force_push"]
        or policy["allow_remote_branch_deletion"]
        or policy["allow_admin_merge_bypass"]
    )


def _check_partition_valid(
    state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    required = tuple(state["required_check_names"])
    successful = tuple(state["successful_check_names"])
    pending = tuple(state["pending_check_names"])
    failed = tuple(state["failed_check_names"])
    if state["checks_observed"] is False:
        return not required and not successful and not pending and not failed
    parts = (successful, pending, failed)
    return (
        required == tuple(sorted(required))
        and required == tuple(sorted(policy["required_check_names"]))
        and all(part == tuple(sorted(part)) for part in parts)
        and len(required) == len(set(required))
        and all(len(part) == len(set(part)) for part in parts)
        and set(successful).isdisjoint(pending)
        and set(successful).isdisjoint(failed)
        and set(pending).isdisjoint(failed)
        and set(successful).union(pending, failed) == set(required)
    )


def _state_consistent(
    state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    forbidden_observed = (
        state["force_push_performed"]
        or state["remote_branch_deleted"]
        or state["admin_merge_bypass_used"]
        or state["human_handover_performed"]
        or state["external_authority_handover_performed"]
    )
    if forbidden_observed or not _check_partition_valid(state, policy):
        return False
    if not state["local_commit_created"]:
        return (
            state["local_commit_sha"] == ""
            and state["local_commit_parent_sha"] == ""
            and state["branch_pushed"] is False
            and state["pushed_head_sha"] == ""
            and state["pull_request_created"] is False
            and state["pull_request_number"] == 0
            and state["pull_request_url_digest"] == ""
            and state["pull_request_draft"] is False
            and state["pr_head_sha"] == ""
            and state["pr_base_branch"] == ""
            and state["checks_observed"] is False
            and state["merge_performed"] is False
            and state["merged_head_sha"] == ""
            and state["merge_commit_sha"] == ""
        )
    commit = state["local_commit_sha"]
    if (
        not _SHA40.fullmatch(commit)
        or state["local_commit_parent_sha"] != state["source_commit_sha"]
    ):
        return False
    if not state["branch_pushed"]:
        return (
            state["pushed_head_sha"] == ""
            and state["pull_request_created"] is False
            and state["checks_observed"] is False
            and state["merge_performed"] is False
        )
    if state["pushed_head_sha"] != commit:
        return False
    if not state["pull_request_created"]:
        return (
            state["pull_request_number"] == 0
            and state["pull_request_url_digest"] == ""
            and state["pull_request_draft"] is False
            and state["pr_head_sha"] == ""
            and state["pr_base_branch"] == ""
            and state["checks_observed"] is False
            and state["merge_performed"] is False
        )
    if (
        _positive_nat(state["pull_request_number"]) is None
        or not _SHA256.fullmatch(state["pull_request_url_digest"])
        or state["pr_head_sha"] != commit
        or state["pr_base_branch"] != state["base_branch"]
    ):
        return False
    if state["merge_performed"]:
        return (
            state["checks_observed"] is True
            and not state["pull_request_draft"]
            and state["mergeable"] is True
            and state["unresolved_blocker_count"] == 0
            and set(state["successful_check_names"])
            == set(policy["required_check_names"])
            and not state["pending_check_names"]
            and not state["failed_check_names"]
            and state["merged_head_sha"] == commit
            and bool(_SHA40.fullmatch(state["merge_commit_sha"]))
        )
    return state["merged_head_sha"] == "" and state["merge_commit_sha"] == ""


def _checks_successful(state: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        state["checks_observed"] is True
        and set(state["successful_check_names"]) == set(policy["required_check_names"])
        and not state["pending_check_names"]
        and not state["failed_check_names"]
    )


def _merge_gate_ready(state: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    return (
        (not policy["require_non_draft_for_merge"] or not state["pull_request_draft"])
        and (not policy["require_mergeable"] or state["mergeable"] is True)
        and (
            not policy["require_no_unresolved_blockers"]
            or state["unresolved_blocker_count"] == 0
        )
        and (
            not policy["require_head_sha_pin"]
            or state["pr_head_sha"] == state["local_commit_sha"]
        )
        and _checks_successful(state, policy)
    )


def _disposition_mode_phase(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[str, str, str]:
    if not _source_supported(source):
        return DISPOSITION_SOURCE_RECEIPT_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _request_provenance_valid(request):
        return DISPOSITION_REQUEST_PROVENANCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _state_evidence_valid(state):
        return DISPOSITION_STATE_EVIDENCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _correspondence_valid(source, request, state, policy):
        return DISPOSITION_CORRESPONDENCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _window_valid(request, state, policy):
        return DISPOSITION_WINDOW_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _replay_closed(request):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED, PHASE_NONE
    if not _scope_supported(request, policy):
        return DISPOSITION_SCOPE_ABSTAINED, MODE_ABSTAIN, PHASE_NONE
    if _destructive_requested(request, policy):
        return DISPOSITION_DESTRUCTIVE_REJECTED, MODE_REJECTED, PHASE_NONE
    if request["human_handover_requested"]:
        return DISPOSITION_HANDOVER_DEFERRED, MODE_HOLD, PHASE_NONE
    if not _state_consistent(state, policy):
        return DISPOSITION_STATE_REPAIR, MODE_REJECTED, PHASE_NONE
    if state["merge_performed"]:
        return DISPOSITION_COMPLETED, MODE_COMPLETED, PHASE_COMPLETE
    if not state["local_commit_created"]:
        return (
            DISPOSITION_LOCAL_COMMIT_AUTHORIZED,
            MODE_LOCAL_GIT_AUTHORIZED,
            PHASE_LOCAL_COMMIT,
        )
    if not state["branch_pushed"]:
        return DISPOSITION_PUSH_AUTHORIZED, MODE_REMOTE_GIT_AUTHORIZED, PHASE_PUSH
    if not state["pull_request_created"]:
        return DISPOSITION_PR_AUTHORIZED, MODE_PR_AUTHORIZED, PHASE_CREATE_PR
    if state["pull_request_draft"]:
        return (
            DISPOSITION_PR_READY_AUTHORIZED,
            MODE_PR_AUTHORIZED,
            PHASE_MARK_PR_READY,
        )
    if not state["checks_observed"] or state["pending_check_names"]:
        return DISPOSITION_CHECKS_PENDING, MODE_AWAITING_CHECKS, PHASE_AWAIT_CHECKS
    if state["failed_check_names"]:
        return DISPOSITION_CHECKS_FAILED, MODE_DEGRADED_AUTONOMY, PHASE_AWAIT_CHECKS
    if not _merge_gate_ready(state, policy):
        return DISPOSITION_MERGE_GATE_HOLD, MODE_HOLD, PHASE_AWAIT_CHECKS
    return DISPOSITION_MERGE_AUTHORIZED, MODE_MERGE_AUTHORIZED, PHASE_MERGE


def _receipt(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
    next_phase: str,
) -> dict[str, Any]:
    authorized = next_phase in {
        PHASE_LOCAL_COMMIT,
        PHASE_PUSH,
        PHASE_CREATE_PR,
        PHASE_MARK_PR_READY,
        PHASE_MERGE,
    }
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_trajectory_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "git_lifecycle_request_digest": request[REQUEST_DIGEST_FIELD],
        "git_lifecycle_state_digest": state[STATE_DIGEST_FIELD],
        "git_lifecycle_policy_digest": policy[POLICY_DIGEST_FIELD],
        "lifecycle_id": request["lifecycle_id"],
        "execution_session_id": request["execution_session_id"],
        "repository_full_name": request["repository_full_name"],
        "source_commit_sha": request["source_commit_sha"],
        "executor_id": request["executor_id"],
        "base_branch": request["base_branch"],
        "head_branch": request["head_branch"],
        "remote_name": request["remote_name"],
        "change_set_digest": request["change_set_digest"],
        "commit_message_digest": request["commit_message_digest"],
        "merge_method": request["merge_method"],
        "next_effect_phase": next_phase,
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "route_receipt_recorded": True,
        "execution_lease_issued": authorized,
        "local_commit_authority_granted": next_phase == PHASE_LOCAL_COMMIT,
        "push_authority_granted": next_phase == PHASE_PUSH,
        "pull_request_authority_granted": next_phase == PHASE_CREATE_PR,
        "pull_request_readiness_authority_granted": next_phase
        == PHASE_MARK_PR_READY,
        "merge_authority_granted": next_phase == PHASE_MERGE,
        "checks_wait_required": next_phase == PHASE_AWAIT_CHECKS,
        "human_handover_deferred": disposition == DISPOSITION_HANDOVER_DEFERRED,
        "effect_execution_performed_by_kernel": False,
        "local_commit_created_observed": state["local_commit_created"],
        "local_commit_sha": state["local_commit_sha"],
        "branch_pushed_observed": state["branch_pushed"],
        "pushed_head_sha": state["pushed_head_sha"],
        "pull_request_created_observed": state["pull_request_created"],
        "pull_request_number": state["pull_request_number"],
        "pull_request_draft_observed": state["pull_request_draft"],
        "required_checks_observed": state["checks_observed"],
        "all_required_checks_successful": _checks_successful(state, policy),
        "no_pending_checks": not state["pending_check_names"],
        "no_failed_checks": not state["failed_check_names"],
        "successful_check_names": list(state["successful_check_names"]),
        "pending_check_names": list(state["pending_check_names"]),
        "failed_check_names": list(state["failed_check_names"]),
        "mergeable_observed": state["mergeable"],
        "unresolved_blocker_count": state["unresolved_blocker_count"],
        "head_sha_pinned": state["pull_request_created"]
        and state["pr_head_sha"] == state["local_commit_sha"],
        "merge_performed_observed": state["merge_performed"],
        "merge_commit_sha": state["merge_commit_sha"],
        "force_push_performed": state["force_push_performed"],
        "remote_branch_deleted": state["remote_branch_deleted"],
        "admin_merge_bypass_used": state["admin_merge_bypass_used"],
        "human_handover_performed": state["human_handover_performed"],
        "external_authority_handover_performed": state[
            "external_authority_handover_performed"
        ],
        "deployment_authority_granted": False,
        "deployment_performed": False,
        "secret_access_authority_granted": False,
        "secret_access_performed": False,
        "source_receipt_treated_as_git_authority": False,
        "checks_treated_as_correctness_proof": False,
        "merge_treated_as_truth": False,
        "history_read_only": True,
        "future_only": not state["merge_performed"],
        "active_now": authorized,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_autonomous_git_lifecycle_envelope(
    *,
    source_trajectory_receipt: Any,
    lifecycle_request: Any,
    lifecycle_state: Any,
    lifecycle_policy: Any,
) -> CodeAIAutonomousGitLifecycleResult:
    source, request, state, policy, issues = _preflight(
        source_trajectory_receipt,
        lifecycle_request,
        lifecycle_state,
        lifecycle_policy,
    )
    if (
        issues
        or source is None
        or request is None
        or state is None
        or policy is None
    ):
        return CodeAIAutonomousGitLifecycleResult(STATUS_BLOCKED, issues, None)
    disposition, operating_mode, next_phase = _disposition_mode_phase(
        source, request, state, policy
    )
    return CodeAIAutonomousGitLifecycleResult(
        STATUS_READY,
        (),
        _receipt(
            source,
            request,
            state,
            policy,
            disposition,
            operating_mode,
            next_phase,
        ),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIAutonomousGitLifecycleResult",
    "build_codeai_autonomous_git_lifecycle_envelope",
    "canonical_digest",
    "digest_without",
    "seal",
]
