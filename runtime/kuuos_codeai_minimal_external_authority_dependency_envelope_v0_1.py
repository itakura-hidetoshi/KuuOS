#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping

from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    RECEIPT_DIGEST_FIELD as SOURCE_RECEIPT_DIGEST_FIELD,
    canonical_digest,
    digest_without,
    seal,
)

VERSION = "kuuos_codeai_minimal_external_authority_dependency_envelope_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Minimal External Authority Dependency v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

MODE_INTERNAL_SUBSTITUTE = "internal_substitute_authorized"
MODE_INTERNAL_CONTINUATION = "unaffected_internal_work_authorized"
MODE_PREAUTHORIZED_EXTERNAL_EFFECT = "preauthorized_external_effect_authorized"
MODE_REQUEST_PACKET = "minimal_external_request_packet_authorized"
MODE_NONBLOCKING_HOLD = "nonblocking_external_authority_hold"
MODE_DEGRADED = "degraded_autonomy"
MODE_COMPLETED = "completed"
MODE_ABSTAIN = "abstain"
MODE_REJECTED = "rejected"

PHASE_INTERNAL_SUBSTITUTE = "execute_internal_substitute"
PHASE_CONTINUE_INTERNAL = "continue_unaffected_internal_work"
PHASE_DEPLOY = "execute_bounded_deploy"
PHASE_SECRET_MUTATION = "execute_bounded_secret_mutation"
PHASE_PREPARE_PACKET = "prepare_minimal_external_request_packet"
PHASE_AWAIT_EXTERNAL = "await_external_authority"
PHASE_COMPLETE = "complete"
PHASE_NONE = "none"

KIND_NONE = "none"
KIND_HUMAN_HANDOVER = "human_handover"
KIND_DEPLOY = "deploy"
KIND_SECRET_MUTATION = "secret_mutation"

DISPOSITION_SOURCE_REPAIR = "source_git_lifecycle_receipt_repair_required"
DISPOSITION_PROVENANCE_REPAIR = "external_dependency_provenance_repair_required"
DISPOSITION_STATE_EVIDENCE_REPAIR = (
    "external_dependency_state_evidence_repair_required"
)
DISPOSITION_CORRESPONDENCE_REPAIR = (
    "external_dependency_correspondence_repair_required"
)
DISPOSITION_WINDOW_REPAIR = "external_dependency_window_repair_required"
DISPOSITION_REPLAY_REJECTED = "external_dependency_replay_conflict_rejected"
DISPOSITION_SCOPE_ABSTAINED = "unsupported_external_dependency_scope_abstained"
DISPOSITION_PLAINTEXT_SECRET_REJECTED = "plaintext_secret_path_rejected"
DISPOSITION_UNOWNED_EFFECT_REJECTED = "unowned_external_effect_observed_rejected"
DISPOSITION_STATE_REPAIR = "external_dependency_state_repair_required"
DISPOSITION_INTERNAL_SUBSTITUTE = "autonomous_internal_substitute_authorized"
DISPOSITION_INTERNAL_CONTINUATION = "unaffected_internal_work_continues"
DISPOSITION_DEPLOY_AUTHORIZED = "preauthorized_bounded_deploy_authorized"
DISPOSITION_SECRET_MUTATION_AUTHORIZED = (
    "preauthorized_bounded_secret_mutation_authorized"
)
DISPOSITION_PACKET_AUTHORIZED = "minimal_external_request_packet_authorized"
DISPOSITION_PENDING_HOLD = "external_authority_pending_nonblocking_hold"
DISPOSITION_FAILED_DEGRADED = "external_effect_failed_degraded"
DISPOSITION_COMPLETED = "minimal_external_dependency_completed"

REQUEST_DIGEST_FIELD = "codeai_minimal_external_dependency_request_digest"
STATE_DIGEST_FIELD = "codeai_minimal_external_dependency_state_digest"
POLICY_DIGEST_FIELD = "codeai_minimal_external_dependency_policy_digest"
RECEIPT_DIGEST_FIELD = "codeai_minimal_external_dependency_receipt_digest"

SOURCE_RECEIPT_FIELDS = {
    "active_now",
    "admin_merge_bypass_used",
    "all_required_checks_successful",
    "base_branch",
    "branch_pushed_observed",
    "change_set_digest",
    "checks_treated_as_correctness_proof",
    "checks_wait_required",
    SOURCE_RECEIPT_DIGEST_FIELD,
    "codeai_disposition",
    "commit_message_digest",
    "deployment_authority_granted",
    "deployment_performed",
    "effect_execution_performed_by_kernel",
    "execution_lease_issued",
    "execution_session_id",
    "executor_id",
    "external_authority_handover_performed",
    "failed_check_names",
    "force_push_performed",
    "future_only",
    "git_lifecycle_policy_digest",
    "git_lifecycle_request_digest",
    "git_lifecycle_state_digest",
    "head_branch",
    "head_sha_pinned",
    "history_read_only",
    "human_handover_deferred",
    "human_handover_performed",
    "lifecycle_id",
    "local_commit_authority_granted",
    "local_commit_created_observed",
    "local_commit_sha",
    "merge_authority_granted",
    "merge_commit_sha",
    "merge_method",
    "merge_performed_observed",
    "merge_treated_as_truth",
    "mergeable_observed",
    "next_effect_phase",
    "no_failed_checks",
    "no_pending_checks",
    "operating_mode",
    "pending_check_names",
    "profile_version",
    "pull_request_authority_granted",
    "pull_request_created_observed",
    "pull_request_draft_observed",
    "pull_request_number",
    "pull_request_readiness_authority_granted",
    "push_authority_granted",
    "pushed_head_sha",
    "remote_branch_deleted",
    "remote_name",
    "repository_full_name",
    "required_checks_observed",
    "route_receipt_recorded",
    "schema_version",
    "secret_access_authority_granted",
    "secret_access_performed",
    "source_commit_sha",
    "source_receipt_treated_as_git_authority",
    "source_trajectory_receipt_digest",
    "successful_check_names",
    "unresolved_blocker_count",
}

REQUEST_FIELDS = {
    "dependency_id",
    "dependency_revision",
    "execution_session_id",
    "execution_nonce_digest",
    "source_git_lifecycle_receipt_digest",
    "repository_full_name",
    "executor_id",
    "requested_effect_kind",
    "requested_effect_count",
    "effect_target",
    "effect_action",
    "effect_scope_digest",
    "effect_payload_digest",
    "artifact_digest",
    "critical_path_required",
    "internal_substitute_available",
    "parallel_internal_work_remaining",
    "plaintext_secret_requested",
    "request_created_epoch",
    "prior_execution_session_ids",
    "prior_execution_nonce_digests",
    "prior_dependency_receipt_digests",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    REQUEST_DIGEST_FIELD,
}

STATE_FIELDS = {
    "dependency_id",
    "source_git_lifecycle_receipt_digest",
    "repository_full_name",
    "executor_id",
    "requested_effect_kind",
    "effect_target",
    "effect_action",
    "effect_scope_digest",
    "internal_substitute_completed",
    "internal_continuation_consumed",
    "preauthorized_capability_present",
    "capability_kind",
    "capability_handle_digest",
    "capability_scope_digest",
    "capability_expires_epoch",
    "capability_one_shot",
    "capability_consumed",
    "external_request_packet_prepared",
    "external_request_packet_digest",
    "external_request_packet_count",
    "external_effect_observed",
    "external_effect_receipt_digest",
    "external_effect_failed",
    "failure_evidence_digest",
    "deployment_performed",
    "secret_mutation_performed",
    "human_handover_performed",
    "external_authority_handover_performed",
    "plaintext_secret_observed",
    "observed_at_epoch",
    "provenance_integrity_confirmed",
    "source_correspondence_confirmed",
    STATE_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_git_lifecycle_receipt_digest",
    "expected_repository_full_name",
    "authorized_executor_ids",
    "allowed_effect_kinds",
    "allowed_effect_targets",
    "allowed_effect_actions",
    "allow_internal_substitute",
    "allow_unaffected_internal_continuation",
    "allow_deploy_via_preauthorized_capability",
    "allow_secret_mutation_via_broker",
    "allow_minimal_external_request_packet",
    "allow_blocking_handover",
    "allow_plaintext_secret",
    "require_opaque_secret_handle",
    "require_one_shot_capability",
    "require_short_lived_capability",
    "maximum_capability_ttl",
    "maximum_external_effects_per_receipt",
    "maximum_handover_packets_per_request",
    "evaluation_epoch",
    "maximum_request_age",
    "maximum_state_age",
    POLICY_DIGEST_FIELD,
}

_SOURCE_STRING_FIELDS = {
    "schema_version",
    "profile_version",
    "source_trajectory_receipt_digest",
    "git_lifecycle_request_digest",
    "git_lifecycle_state_digest",
    "git_lifecycle_policy_digest",
    "lifecycle_id",
    "execution_session_id",
    "repository_full_name",
    "source_commit_sha",
    "executor_id",
    "base_branch",
    "head_branch",
    "remote_name",
    "change_set_digest",
    "commit_message_digest",
    "merge_method",
    "next_effect_phase",
    "codeai_disposition",
    "operating_mode",
    "local_commit_sha",
    "pushed_head_sha",
    "merge_commit_sha",
    SOURCE_RECEIPT_DIGEST_FIELD,
}
_SOURCE_LIST_FIELDS = {
    "successful_check_names",
    "pending_check_names",
    "failed_check_names",
}
_SOURCE_NAT_FIELDS = {"pull_request_number", "unresolved_blocker_count"}
_SOURCE_BOOL_FIELDS = SOURCE_RECEIPT_FIELDS - _SOURCE_STRING_FIELDS - _SOURCE_LIST_FIELDS - _SOURCE_NAT_FIELDS

_REQUEST_STRING_FIELDS = {
    "dependency_id",
    "dependency_revision",
    "execution_session_id",
    "execution_nonce_digest",
    "source_git_lifecycle_receipt_digest",
    "repository_full_name",
    "executor_id",
    "requested_effect_kind",
    "effect_target",
    "effect_action",
    "effect_scope_digest",
    "effect_payload_digest",
    "artifact_digest",
    REQUEST_DIGEST_FIELD,
}
_REQUEST_LIST_FIELDS = {
    "prior_execution_session_ids",
    "prior_execution_nonce_digests",
    "prior_dependency_receipt_digests",
}
_REQUEST_NAT_FIELDS = {"requested_effect_count", "request_created_epoch"}
_REQUEST_BOOL_FIELDS = REQUEST_FIELDS - _REQUEST_STRING_FIELDS - _REQUEST_LIST_FIELDS - _REQUEST_NAT_FIELDS

_STATE_STRING_FIELDS = {
    "dependency_id",
    "source_git_lifecycle_receipt_digest",
    "repository_full_name",
    "executor_id",
    "requested_effect_kind",
    "effect_target",
    "effect_action",
    "effect_scope_digest",
    "capability_kind",
    "capability_handle_digest",
    "capability_scope_digest",
    "external_request_packet_digest",
    "external_effect_receipt_digest",
    "failure_evidence_digest",
    STATE_DIGEST_FIELD,
}
_STATE_NAT_FIELDS = {
    "capability_expires_epoch",
    "external_request_packet_count",
    "observed_at_epoch",
}
_STATE_BOOL_FIELDS = STATE_FIELDS - _STATE_STRING_FIELDS - _STATE_NAT_FIELDS

_POLICY_STRING_FIELDS = {
    "expected_source_git_lifecycle_receipt_digest",
    "expected_repository_full_name",
    POLICY_DIGEST_FIELD,
}
_POLICY_LIST_FIELDS = {
    "authorized_executor_ids",
    "allowed_effect_kinds",
    "allowed_effect_targets",
    "allowed_effect_actions",
}
_POLICY_NAT_FIELDS = {
    "maximum_capability_ttl",
    "maximum_external_effects_per_receipt",
    "maximum_handover_packets_per_request",
    "evaluation_epoch",
    "maximum_request_age",
    "maximum_state_age",
}
_POLICY_BOOL_FIELDS = POLICY_FIELDS - _POLICY_STRING_FIELDS - _POLICY_LIST_FIELDS - _POLICY_NAT_FIELDS

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CodeAIMinimalExternalAuthorityDependencyResult:
    status: str
    issues: tuple[str, ...]
    receipt: dict[str, Any] | None


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _nat(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _strings(value: Any) -> tuple[str, ...] | None:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return tuple(value)


def _unique_nonempty(value: Any) -> bool:
    parsed = _strings(value)
    return parsed is not None and all(parsed) and len(parsed) == len(set(parsed))


def _validate_typed_mapping(
    value: Mapping[str, Any],
    *,
    fields: set[str],
    strings: set[str],
    lists: set[str],
    nats: set[str],
    bools: set[str],
    prefix: str,
    digest_field: str,
) -> list[str]:
    issues: list[str] = []
    missing = fields.difference(value)
    extra = set(value).difference(fields)
    if missing:
        issues.append(prefix + "_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append(prefix + "_extra_fields:" + ",".join(sorted(extra)))
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
            issues.append(prefix + "_invalid_natural:" + field)
    for field in bools:
        if not isinstance(value.get(field), bool):
            issues.append(prefix + "_invalid_boolean:" + field)
    digest = value.get(digest_field)
    if isinstance(digest, str) and digest_without(value, digest_field) != digest:
        issues.append(prefix + "_digest_mismatch")
    return issues


def _preflight(
    source_value: Any,
    request_value: Any,
    state_value: Any,
    policy_value: Any,
) -> tuple[
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    Mapping[str, Any] | None,
    tuple[str, ...],
]:
    source = _mapping(source_value)
    request = _mapping(request_value)
    state = _mapping(state_value)
    policy = _mapping(policy_value)
    issues: list[str] = []
    if source is None:
        issues.append("source_git_lifecycle_receipt_not_mapping")
    else:
        issues.extend(
            _validate_typed_mapping(
                source,
                fields=SOURCE_RECEIPT_FIELDS,
                strings=_SOURCE_STRING_FIELDS,
                lists=_SOURCE_LIST_FIELDS,
                nats=_SOURCE_NAT_FIELDS,
                bools=_SOURCE_BOOL_FIELDS,
                prefix="source_git_lifecycle_receipt",
                digest_field=SOURCE_RECEIPT_DIGEST_FIELD,
            )
        )
    if request is None:
        issues.append("external_dependency_request_not_mapping")
    else:
        issues.extend(
            _validate_typed_mapping(
                request,
                fields=REQUEST_FIELDS,
                strings=_REQUEST_STRING_FIELDS,
                lists=_REQUEST_LIST_FIELDS,
                nats=_REQUEST_NAT_FIELDS,
                bools=_REQUEST_BOOL_FIELDS,
                prefix="external_dependency_request",
                digest_field=REQUEST_DIGEST_FIELD,
            )
        )
    if state is None:
        issues.append("external_dependency_state_not_mapping")
    else:
        issues.extend(
            _validate_typed_mapping(
                state,
                fields=STATE_FIELDS,
                strings=_STATE_STRING_FIELDS,
                lists=set(),
                nats=_STATE_NAT_FIELDS,
                bools=_STATE_BOOL_FIELDS,
                prefix="external_dependency_state",
                digest_field=STATE_DIGEST_FIELD,
            )
        )
    if policy is None:
        issues.append("external_dependency_policy_not_mapping")
    else:
        issues.extend(
            _validate_typed_mapping(
                policy,
                fields=POLICY_FIELDS,
                strings=_POLICY_STRING_FIELDS,
                lists=_POLICY_LIST_FIELDS,
                nats=_POLICY_NAT_FIELDS,
                bools=_POLICY_BOOL_FIELDS,
                prefix="external_dependency_policy",
                digest_field=POLICY_DIGEST_FIELD,
            )
        )
    return source, request, state, policy, tuple(issues)


def _source_supported(source: Mapping[str, Any]) -> bool:
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI Autonomous Git Lifecycle v0.1"
        and source["codeai_disposition"] == "autonomous_git_lifecycle_completed"
        and source["operating_mode"] == "completed"
        and source["next_effect_phase"] == "complete"
        and source["route_receipt_recorded"]
        and source["merge_performed_observed"]
        and not source["execution_lease_issued"]
        and not source["active_now"]
        and not source["force_push_performed"]
        and not source["remote_branch_deleted"]
        and not source["admin_merge_bypass_used"]
        and not source["human_handover_performed"]
        and not source["external_authority_handover_performed"]
        and not source["deployment_performed"]
        and not source["secret_access_performed"]
        and bool(_SHA40.fullmatch(source["merge_commit_sha"]))
        and bool(_SHA256.fullmatch(source[SOURCE_RECEIPT_DIGEST_FIELD]))
    )


def _provenance_valid(
    request: Mapping[str, Any], state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["provenance_integrity_confirmed"]
        and request["source_correspondence_confirmed"]
        and state["provenance_integrity_confirmed"]
        and state["source_correspondence_confirmed"]
        and _unique_nonempty(policy["authorized_executor_ids"])
        and _unique_nonempty(policy["allowed_effect_kinds"])
        and _unique_nonempty(policy["allowed_effect_targets"])
        and _unique_nonempty(policy["allowed_effect_actions"])
        and request["executor_id"] in policy["authorized_executor_ids"]
        and bool(_SHA256.fullmatch(request["execution_nonce_digest"]))
    )


def _state_evidence_valid(state: Mapping[str, Any]) -> bool:
    digest_fields = (
        "external_request_packet_digest",
        "external_effect_receipt_digest",
        "failure_evidence_digest",
    )
    for field in digest_fields:
        if state[field] and not _SHA256.fullmatch(state[field]):
            return False
    if state["preauthorized_capability_present"]:
        if state["capability_kind"] not in {KIND_DEPLOY, KIND_SECRET_MUTATION}:
            return False
        if not _SHA256.fullmatch(state["capability_handle_digest"]):
            return False
        if not _SHA256.fullmatch(state["capability_scope_digest"]):
            return False
        if state["capability_expires_epoch"] == 0:
            return False
    else:
        if any(
            (
                state["capability_kind"],
                state["capability_handle_digest"],
                state["capability_scope_digest"],
                state["capability_expires_epoch"],
                state["capability_one_shot"],
                state["capability_consumed"],
            )
        ):
            return False
    if state["external_request_packet_prepared"]:
        if (
            state["external_request_packet_count"] != 1
            or not _SHA256.fullmatch(state["external_request_packet_digest"])
        ):
            return False
    elif state["external_request_packet_count"] != 0 or state[
        "external_request_packet_digest"
    ]:
        return False
    return True


def _correspondence_valid(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> bool:
    source_digest = source[SOURCE_RECEIPT_DIGEST_FIELD]
    return (
        request["source_git_lifecycle_receipt_digest"] == source_digest
        and state["source_git_lifecycle_receipt_digest"] == source_digest
        and policy["expected_source_git_lifecycle_receipt_digest"] == source_digest
        and request["repository_full_name"] == source["repository_full_name"]
        and state["repository_full_name"] == source["repository_full_name"]
        and policy["expected_repository_full_name"] == source["repository_full_name"]
        and state["dependency_id"] == request["dependency_id"]
        and state["executor_id"] == request["executor_id"]
        and state["requested_effect_kind"] == request["requested_effect_kind"]
        and state["effect_target"] == request["effect_target"]
        and state["effect_action"] == request["effect_action"]
        and state["effect_scope_digest"] == request["effect_scope_digest"]
    )


def _window_valid(
    request: Mapping[str, Any], state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    now = policy["evaluation_epoch"]
    return (
        request["request_created_epoch"] <= now
        and now - request["request_created_epoch"] <= policy["maximum_request_age"]
        and state["observed_at_epoch"] <= now
        and now - state["observed_at_epoch"] <= policy["maximum_state_age"]
    )


def _replay_safe(request: Mapping[str, Any]) -> bool:
    sessions = request["prior_execution_session_ids"]
    nonces = request["prior_execution_nonce_digests"]
    receipts = request["prior_dependency_receipt_digests"]
    return (
        len(sessions) == len(set(sessions))
        and len(nonces) == len(set(nonces))
        and len(receipts) == len(set(receipts))
        and request["execution_session_id"] not in sessions
        and request["execution_nonce_digest"] not in nonces
        and all(_SHA256.fullmatch(item) for item in nonces)
        and all(_SHA256.fullmatch(item) for item in receipts)
    )


def _scope_supported(
    request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    kind = request["requested_effect_kind"]
    if policy["maximum_external_effects_per_receipt"] != 1:
        return False
    if policy["maximum_handover_packets_per_request"] != 1:
        return False
    if (
        policy["allow_blocking_handover"]
        or policy["maximum_capability_ttl"] == 0
        or policy["maximum_request_age"] == 0
        or policy["maximum_state_age"] == 0
        or not policy["require_one_shot_capability"]
        or not policy["require_short_lived_capability"]
    ):
        return False
    if kind == KIND_NONE:
        return (
            request["requested_effect_count"] == 0
            and not request["effect_target"]
            and not request["effect_action"]
            and not request["effect_scope_digest"]
            and not request["effect_payload_digest"]
            and not request["artifact_digest"]
        )
    return (
        kind in policy["allowed_effect_kinds"]
        and request["requested_effect_count"] == 1
        and request["effect_target"] in policy["allowed_effect_targets"]
        and request["effect_action"] in policy["allowed_effect_actions"]
        and bool(_SHA256.fullmatch(request["effect_scope_digest"]))
        and bool(_SHA256.fullmatch(request["effect_payload_digest"]))
        and (
            kind != KIND_DEPLOY
            or bool(_SHA256.fullmatch(request["artifact_digest"]))
        )
        and (kind == KIND_DEPLOY or not request["artifact_digest"])
    )


def _unsafe_secret_path(
    request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["plaintext_secret_requested"]
        or policy["allow_plaintext_secret"]
        or not policy["require_opaque_secret_handle"]
    )


def _unowned_effect_observed(state: Mapping[str, Any]) -> bool:
    return (
        state["human_handover_performed"]
        or state["external_authority_handover_performed"]
        or state["plaintext_secret_observed"]
        or (
            state["deployment_performed"]
            and state["requested_effect_kind"] != KIND_DEPLOY
        )
        or (
            state["secret_mutation_performed"]
            and state["requested_effect_kind"] != KIND_SECRET_MUTATION
        )
    )


def _state_consistent(state: Mapping[str, Any]) -> bool:
    if state["internal_substitute_completed"] and (
        state["external_effect_observed"] or state["external_effect_failed"]
    ):
        return False
    if state["external_effect_observed"]:
        if not _SHA256.fullmatch(state["external_effect_receipt_digest"]):
            return False
        if state["external_effect_failed"] or state["failure_evidence_digest"]:
            return False
    elif state["external_effect_receipt_digest"]:
        return False
    if state["external_effect_failed"]:
        if not _SHA256.fullmatch(state["failure_evidence_digest"]):
            return False
        if state["deployment_performed"] or state["secret_mutation_performed"]:
            return False
    elif state["failure_evidence_digest"]:
        return False
    if state["deployment_performed"] or state["secret_mutation_performed"]:
        if not state["external_effect_observed"]:
            return False
    if state["capability_consumed"] and not state["external_effect_observed"]:
        return False
    return True


def _capability_valid(
    request: Mapping[str, Any], state: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    if not state["preauthorized_capability_present"]:
        return False
    ttl = state["capability_expires_epoch"] - policy["evaluation_epoch"]
    return (
        state["capability_kind"] == request["requested_effect_kind"]
        and state["capability_scope_digest"] == request["effect_scope_digest"]
        and state["capability_expires_epoch"] > policy["evaluation_epoch"]
        and ttl <= policy["maximum_capability_ttl"]
        and state["capability_one_shot"]
        and not state["capability_consumed"]
        and policy["require_one_shot_capability"]
        and policy["require_short_lived_capability"]
    )


def _route(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> tuple[str, str, str]:
    if not _source_supported(source):
        return DISPOSITION_SOURCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _provenance_valid(request, state, policy):
        return DISPOSITION_PROVENANCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _state_evidence_valid(state):
        return DISPOSITION_STATE_EVIDENCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _correspondence_valid(source, request, state, policy):
        return DISPOSITION_CORRESPONDENCE_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _window_valid(request, state, policy):
        return DISPOSITION_WINDOW_REPAIR, MODE_REJECTED, PHASE_NONE
    if not _replay_safe(request):
        return DISPOSITION_REPLAY_REJECTED, MODE_REJECTED, PHASE_NONE
    if not _scope_supported(request, policy):
        return DISPOSITION_SCOPE_ABSTAINED, MODE_ABSTAIN, PHASE_NONE
    if _unsafe_secret_path(request, policy):
        return DISPOSITION_PLAINTEXT_SECRET_REJECTED, MODE_REJECTED, PHASE_NONE
    if _unowned_effect_observed(state):
        return DISPOSITION_UNOWNED_EFFECT_REJECTED, MODE_REJECTED, PHASE_NONE
    if not _state_consistent(state):
        return DISPOSITION_STATE_REPAIR, MODE_REJECTED, PHASE_NONE
    if state["external_effect_failed"]:
        return DISPOSITION_FAILED_DEGRADED, MODE_DEGRADED, PHASE_AWAIT_EXTERNAL
    if (
        request["requested_effect_kind"] == KIND_NONE
        or state["internal_substitute_completed"]
        or state["external_effect_observed"]
    ):
        return DISPOSITION_COMPLETED, MODE_COMPLETED, PHASE_COMPLETE
    if (
        request["internal_substitute_available"]
        and policy["allow_internal_substitute"]
    ):
        return (
            DISPOSITION_INTERNAL_SUBSTITUTE,
            MODE_INTERNAL_SUBSTITUTE,
            PHASE_INTERNAL_SUBSTITUTE,
        )
    if (
        request["parallel_internal_work_remaining"]
        and not request["critical_path_required"]
        and not state["internal_continuation_consumed"]
        and policy["allow_unaffected_internal_continuation"]
    ):
        return (
            DISPOSITION_INTERNAL_CONTINUATION,
            MODE_INTERNAL_CONTINUATION,
            PHASE_CONTINUE_INTERNAL,
        )
    if _capability_valid(request, state, policy):
        if (
            request["requested_effect_kind"] == KIND_DEPLOY
            and policy["allow_deploy_via_preauthorized_capability"]
        ):
            return (
                DISPOSITION_DEPLOY_AUTHORIZED,
                MODE_PREAUTHORIZED_EXTERNAL_EFFECT,
                PHASE_DEPLOY,
            )
        if (
            request["requested_effect_kind"] == KIND_SECRET_MUTATION
            and policy["allow_secret_mutation_via_broker"]
        ):
            return (
                DISPOSITION_SECRET_MUTATION_AUTHORIZED,
                MODE_PREAUTHORIZED_EXTERNAL_EFFECT,
                PHASE_SECRET_MUTATION,
            )
    if (
        not state["external_request_packet_prepared"]
        and policy["allow_minimal_external_request_packet"]
    ):
        return (
            DISPOSITION_PACKET_AUTHORIZED,
            MODE_REQUEST_PACKET,
            PHASE_PREPARE_PACKET,
        )
    return DISPOSITION_PENDING_HOLD, MODE_NONBLOCKING_HOLD, PHASE_AWAIT_EXTERNAL


def _receipt(
    source: Mapping[str, Any],
    request: Mapping[str, Any],
    state: Mapping[str, Any],
    policy: Mapping[str, Any],
    disposition: str,
    operating_mode: str,
    next_phase: str,
) -> dict[str, Any]:
    lease_issued = next_phase in {
        PHASE_INTERNAL_SUBSTITUTE,
        PHASE_CONTINUE_INTERNAL,
        PHASE_DEPLOY,
        PHASE_SECRET_MUTATION,
        PHASE_PREPARE_PACKET,
    }
    external_effect_lease = next_phase in {PHASE_DEPLOY, PHASE_SECRET_MUTATION}
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_git_lifecycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "external_dependency_request_digest": request[REQUEST_DIGEST_FIELD],
        "external_dependency_state_digest": state[STATE_DIGEST_FIELD],
        "external_dependency_policy_digest": policy[POLICY_DIGEST_FIELD],
        "dependency_id": request["dependency_id"],
        "execution_session_id": request["execution_session_id"],
        "repository_full_name": request["repository_full_name"],
        "executor_id": request["executor_id"],
        "requested_effect_kind": request["requested_effect_kind"],
        "effect_target": request["effect_target"],
        "effect_action": request["effect_action"],
        "effect_scope_digest": request["effect_scope_digest"],
        "next_effect_phase": next_phase,
        "codeai_disposition": disposition,
        "operating_mode": operating_mode,
        "route_receipt_recorded": True,
        "execution_lease_issued": lease_issued,
        "external_effect_lease_issued": external_effect_lease,
        "internal_substitute_authority_granted": next_phase
        == PHASE_INTERNAL_SUBSTITUTE,
        "internal_continuation_authority_granted": next_phase
        == PHASE_CONTINUE_INTERNAL,
        "deployment_authority_granted": next_phase == PHASE_DEPLOY,
        "secret_mutation_authority_granted": next_phase == PHASE_SECRET_MUTATION,
        "external_request_packet_authority_granted": next_phase
        == PHASE_PREPARE_PACKET,
        "human_handover_authority_granted": False,
        "secret_access_authority_granted": False,
        "critical_path_blocked": next_phase == PHASE_AWAIT_EXTERNAL
        and request["critical_path_required"],
        "unaffected_work_may_continue": request["parallel_internal_work_remaining"]
        and not request["critical_path_required"],
        "human_handover_deferred": request["requested_effect_kind"]
        == KIND_HUMAN_HANDOVER
        and not state["external_effect_observed"],
        "external_request_packet_minimized": next_phase
        in {PHASE_PREPARE_PACKET, PHASE_AWAIT_EXTERNAL},
        "effect_execution_performed_by_kernel": False,
        "internal_substitute_completed_observed": state[
            "internal_substitute_completed"
        ],
        "internal_continuation_consumed_observed": state[
            "internal_continuation_consumed"
        ],
        "preauthorized_capability_observed": state[
            "preauthorized_capability_present"
        ],
        "capability_handle_exposed": False,
        "capability_one_shot": state["capability_one_shot"],
        "capability_consumed_observed": state["capability_consumed"],
        "external_request_packet_prepared_observed": state[
            "external_request_packet_prepared"
        ],
        "external_effect_observed": state["external_effect_observed"],
        "external_effect_failed_observed": state["external_effect_failed"],
        "deployment_performed_observed": state["deployment_performed"],
        "secret_mutation_performed_observed": state[
            "secret_mutation_performed"
        ],
        "human_handover_performed": state["human_handover_performed"],
        "external_authority_handover_performed": state[
            "external_authority_handover_performed"
        ],
        "plaintext_secret_observed": state["plaintext_secret_observed"],
        "blocking_handover_allowed": policy["allow_blocking_handover"],
        "source_receipt_treated_as_external_authority": False,
        "external_result_treated_as_truth": False,
        "history_read_only": True,
        "future_only": next_phase != PHASE_COMPLETE,
        "active_now": lease_issued,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return receipt


def build_codeai_minimal_external_authority_dependency_envelope(
    *,
    source_git_lifecycle_receipt: Any,
    dependency_request: Any,
    dependency_state: Any,
    dependency_policy: Any,
) -> CodeAIMinimalExternalAuthorityDependencyResult:
    source, request, state, policy, issues = _preflight(
        source_git_lifecycle_receipt,
        dependency_request,
        dependency_state,
        dependency_policy,
    )
    if (
        issues
        or source is None
        or request is None
        or state is None
        or policy is None
    ):
        return CodeAIMinimalExternalAuthorityDependencyResult(
            STATUS_BLOCKED, issues, None
        )
    disposition, operating_mode, next_phase = _route(
        source, request, state, policy
    )
    return CodeAIMinimalExternalAuthorityDependencyResult(
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
    "CodeAIMinimalExternalAuthorityDependencyResult",
    "build_codeai_minimal_external_authority_dependency_envelope",
    "canonical_digest",
    "digest_without",
    "seal",
]
