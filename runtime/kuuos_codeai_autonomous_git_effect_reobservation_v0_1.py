#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Mapping

from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import (
    ADAPTER_RESULT_FIELDS as SOURCE_ADAPTER_RESULT_FIELDS,
    DISPOSITION_COMPLETED as SOURCE_DISPOSITION_COMPLETED,
    DISPOSITION_EVIDENCE_QUARANTINED as SOURCE_DISPOSITION_QUARANTINED,
    DISPOSITION_FAILED as SOURCE_DISPOSITION_FAILED,
    EVIDENCE_DIGEST_FIELD as SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD,
    PHASE_CREATE_PR,
    PHASE_LOCAL_COMMIT,
    PHASE_MARK_PR_READY,
    PHASE_MERGE,
    PHASE_PUSH,
    RECEIPT_DIGEST_FIELD as SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD,
    SOURCE_FIELDS as SOURCE_LIFECYCLE_FIELDS,
    SOURCE_RECEIPT_DIGEST_FIELD as SOURCE_LIFECYCLE_RECEIPT_DIGEST_FIELD,
    SUPPORTED_PHASES,
    canonical_digest,
    digest_without,
)
from runtime.kuuos_codeai_autonomous_git_effect_execution_validation_v0_1 import (
    _validate_source as _validate_source_lifecycle_receipt,
)
from runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 import (
    STATE_DIGEST_FIELD,
    STATE_FIELDS,
    _validate_state as _validate_lifecycle_state,
)

VERSION = "kuuos_codeai_autonomous_git_effect_reobservation_v0_1"
SCHEMA_VERSION = "v0.1"
PROFILE_VERSION = "CodeAI Autonomous Git Effect Re-observation v0.1"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"

DISPOSITION_COMPLETED = "autonomous_git_effect_reobservation_completed"
DISPOSITION_FAILED = "autonomous_git_effect_reobservation_failed"
DISPOSITION_EVIDENCE_QUARANTINED = "autonomous_git_effect_reobservation_evidence_quarantined"

REQUEST_DIGEST_FIELD = "codeai_autonomous_git_effect_reobservation_request_digest"
POLICY_DIGEST_FIELD = "codeai_autonomous_git_effect_reobservation_policy_digest"
REGISTRY_DIGEST_FIELD = "codeai_autonomous_git_effect_reobservation_registry_digest"
EVIDENCE_DIGEST_FIELD = "codeai_autonomous_git_effect_reobservation_evidence_digest"
RECEIPT_DIGEST_FIELD = "codeai_autonomous_git_effect_reobservation_receipt_digest"

_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
_BRANCH = re.compile(r"^(?!/)(?!.*(?:\.\.|//|@\{|\\|[~^:?*\[]))(?!.*\.$)[^\s]+$")

SOURCE_EXECUTION_RECEIPT_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "execution_request_digest", "execution_policy_digest", "source_registry_digest",
    "next_registry_digest", "execution_evidence_digest", "lifecycle_id", "execution_id",
    "execution_session_id", "repository_full_name", "effect_phase", "codeai_disposition",
    "operating_mode", "route_receipt_recorded", "source_one_effect_lease_verified",
    "source_one_effect_lease_consumed", "execution_nonce_consumed", "registry_advanced_once",
    "exactly_one_adapter_invocation", "adapter_evidence_valid", "effect_completion_confirmed",
    "effect_failure_recorded", "evidence_quarantined", "reobservation_required",
    "local_commit_performed", "push_performed", "pull_request_created",
    "pull_request_marked_ready", "merge_performed", "force_push_performed",
    "remote_branch_deleted", "admin_merge_bypass_used", "deployment_performed",
    "secret_material_read", "token_material_emitted",
    "automatic_successor_effect_authority_granted", "general_git_authority_granted",
    "general_successor_stage_authority_granted", "effect_completion_treated_as_correctness",
    "merge_treated_as_truth", "history_read_only", "future_only", "active_now",
    SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD,
}

SOURCE_EXECUTION_EVIDENCE_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "execution_request_digest", "effect_phase", "adapter_result",
    "adapter_evidence_valid", "adapter_evidence_issues", "effect_completion_confirmed",
    SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD,
}

REQUEST_FIELDS = {
    "reobservation_id", "reobservation_revision", "reobservation_session_id",
    "reobservation_nonce_digest", "source_lifecycle_receipt_digest",
    "source_execution_receipt_digest", "source_execution_evidence_digest", "lifecycle_id",
    "observer_id", "repository_full_name", "source_commit_sha", "base_branch",
    "head_branch", "remote_name", "change_set_digest", "commit_message_digest",
    "merge_method", "effect_phase", "request_created_epoch",
    "provenance_integrity_confirmed", "source_correspondence_confirmed", REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_source_lifecycle_receipt_digest", "expected_source_execution_receipt_digest",
    "expected_source_execution_evidence_digest", "expected_repository_full_name",
    "authorized_observer_ids", "allowed_effect_phases", "required_check_names",
    "maximum_command_count", "maximum_output_bytes", "maximum_request_age",
    "maximum_observation_age", "maximum_registry_entries", "evaluation_epoch",
    "network_access_allowed", "secret_access_allowed", "git_write_allowed",
    "deployment_allowed", POLICY_DIGEST_FIELD,
}

REGISTRY_FIELDS = {
    "registry_id", "registry_revision", "consumed_execution_receipt_digests",
    "consumed_reobservation_nonce_digests", "consumed_count", "last_reobservation_epoch",
    REGISTRY_DIGEST_FIELD,
}

_ADAPTER_META_FIELDS = {
    "adapter_id", "adapter_session_id", "status", "command_count", "output_bytes",
    "completed_epoch", "network_accessed", "secret_material_read", "git_write_performed",
    "deployment_performed", "exception_type",
}
ADAPTER_RESULT_FIELDS = _ADAPTER_META_FIELDS | (STATE_FIELDS - {STATE_DIGEST_FIELD})

SOURCE_EXECUTION_RECEIPT_STRING_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "execution_request_digest", "execution_policy_digest", "source_registry_digest",
    "next_registry_digest", "execution_evidence_digest", "lifecycle_id", "execution_id",
    "execution_session_id", "repository_full_name", "effect_phase", "codeai_disposition",
    "operating_mode", SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD,
}

SOURCE_EXECUTION_EVIDENCE_STRING_FIELDS = {
    "schema_version", "profile_version", "source_lifecycle_receipt_digest",
    "execution_request_digest", "effect_phase", SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD,
}

REQUEST_STRING_FIELDS = REQUEST_FIELDS - {
    "request_created_epoch", "provenance_integrity_confirmed", "source_correspondence_confirmed",
}

POLICY_LIST_FIELDS = {"authorized_observer_ids", "allowed_effect_phases", "required_check_names"}
POLICY_NAT_FIELDS = {
    "maximum_command_count", "maximum_output_bytes", "maximum_request_age",
    "maximum_observation_age", "maximum_registry_entries", "evaluation_epoch",
}
POLICY_STRING_FIELDS = {
    "expected_source_lifecycle_receipt_digest", "expected_source_execution_receipt_digest",
    "expected_source_execution_evidence_digest", "expected_repository_full_name",
    POLICY_DIGEST_FIELD,
}


@dataclass(frozen=True)
class GitEffectReobservationInvocation:
    lifecycle_id: str
    repository_full_name: str
    source_commit_sha: str
    base_branch: str
    head_branch: str
    remote_name: str
    change_set_digest: str
    commit_message_digest: str
    merge_method: str
    effect_phase: str
    required_check_names: tuple[str, ...]
    maximum_command_count: int
    maximum_output_bytes: int
    maximum_observation_age: int
    evaluation_epoch: int


GitEffectReobservationAdapter = Callable[[GitEffectReobservationInvocation], Mapping[str, Any]]


@dataclass(frozen=True)
class CodeAIAutonomousGitEffectReobservationResult:
    status: str
    issues: tuple[str, ...]
    evidence: dict[str, Any] | None
    next_registry: dict[str, Any] | None
    lifecycle_state: dict[str, Any] | None
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


def _validate_source_execution_receipt(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_EXECUTION_RECEIPT_FIELDS, "source_execution_receipt")
    if issues:
        return issues
    for field in SOURCE_EXECUTION_RECEIPT_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("source_execution_receipt_invalid_string:" + field)
    for field in SOURCE_EXECUTION_RECEIPT_FIELDS - SOURCE_EXECUTION_RECEIPT_STRING_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("source_execution_receipt_invalid_bool:" + field)
    if not _digest_ok(value, SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD):
        issues.append("source_execution_receipt_digest_mismatch")
    return issues


def _validate_source_adapter_result(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_ADAPTER_RESULT_FIELDS, "source_execution_adapter_result")
    if issues:
        return issues
    strings = {
        "adapter_id", "adapter_session_id", "effect_phase", "status", "stdout", "stderr",
        "local_commit_sha", "local_commit_parent_sha", "pushed_head_sha",
        "pull_request_url_digest", "pr_head_sha", "pr_base_branch", "merged_head_sha",
        "merge_commit_sha", "exception_type",
    }
    nats = {"exit_code", "command_count", "completed_epoch", "pull_request_number"}
    for field in strings:
        if not isinstance(value.get(field), str):
            issues.append("source_execution_adapter_result_invalid_string:" + field)
    for field in nats:
        if _nat(value.get(field)) is None:
            issues.append("source_execution_adapter_result_invalid_nat:" + field)
    for field in SOURCE_ADAPTER_RESULT_FIELDS - strings - nats:
        if not isinstance(value.get(field), bool):
            issues.append("source_execution_adapter_result_invalid_bool:" + field)
    return issues


def _validate_source_execution_evidence(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, SOURCE_EXECUTION_EVIDENCE_FIELDS, "source_execution_evidence")
    if issues:
        return issues
    for field in SOURCE_EXECUTION_EVIDENCE_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("source_execution_evidence_invalid_string:" + field)
    for field in ("adapter_evidence_valid", "effect_completion_confirmed"):
        if not isinstance(value.get(field), bool):
            issues.append("source_execution_evidence_invalid_bool:" + field)
    if _strings(value.get("adapter_evidence_issues")) is None:
        issues.append("source_execution_evidence_invalid_issue_list")
    adapter_result = _mapping(value.get("adapter_result"))
    if adapter_result is None:
        issues.append("source_execution_evidence_adapter_result_not_mapping")
    else:
        issues.extend(_validate_source_adapter_result(adapter_result))
    if not _digest_ok(value, SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD):
        issues.append("source_execution_evidence_digest_mismatch")
    return issues


def _validate_request(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REQUEST_FIELDS, "git_effect_reobservation_request")
    if issues:
        return issues
    for field in REQUEST_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("git_effect_reobservation_request_invalid_string:" + field)
    if _nat(value.get("request_created_epoch")) is None:
        issues.append("git_effect_reobservation_request_invalid_nat:request_created_epoch")
    for field in ("provenance_integrity_confirmed", "source_correspondence_confirmed"):
        if not isinstance(value.get(field), bool):
            issues.append("git_effect_reobservation_request_invalid_bool:" + field)
    if not _digest_ok(value, REQUEST_DIGEST_FIELD):
        issues.append("git_effect_reobservation_request_digest_mismatch")
    return issues


def _validate_policy(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, POLICY_FIELDS, "git_effect_reobservation_policy")
    if issues:
        return issues
    for field in POLICY_STRING_FIELDS:
        if not isinstance(value.get(field), str):
            issues.append("git_effect_reobservation_policy_invalid_string:" + field)
    for field in POLICY_LIST_FIELDS:
        if _strings(value.get(field), nonempty=True) is None:
            issues.append("git_effect_reobservation_policy_invalid_nonempty_unique_list:" + field)
    for field in POLICY_NAT_FIELDS:
        if _nat(value.get(field), positive=field != "evaluation_epoch") is None:
            issues.append("git_effect_reobservation_policy_invalid_nat:" + field)
    for field in POLICY_FIELDS - POLICY_STRING_FIELDS - POLICY_LIST_FIELDS - POLICY_NAT_FIELDS:
        if not isinstance(value.get(field), bool):
            issues.append("git_effect_reobservation_policy_invalid_bool:" + field)
    if not _digest_ok(value, POLICY_DIGEST_FIELD):
        issues.append("git_effect_reobservation_policy_digest_mismatch")
    return issues


def _validate_registry(value: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(value, REGISTRY_FIELDS, "git_effect_reobservation_registry")
    if issues:
        return issues
    if not isinstance(value.get("registry_id"), str) or not value["registry_id"]:
        issues.append("git_effect_reobservation_registry_invalid_id")
    for field in ("registry_revision", "consumed_count", "last_reobservation_epoch"):
        if _nat(value.get(field)) is None:
            issues.append("git_effect_reobservation_registry_invalid_nat:" + field)
    histories = (
        "consumed_execution_receipt_digests", "consumed_reobservation_nonce_digests",
    )
    parsed: dict[str, tuple[str, ...] | None] = {}
    for field in histories:
        parsed[field] = _strings(value.get(field))
        if parsed[field] is None or not all(_SHA256.fullmatch(item) for item in parsed[field] or ()):
            issues.append("git_effect_reobservation_registry_invalid_digest_history:" + field)
    if all(parsed[field] is not None for field in histories):
        if len(parsed[histories[0]] or ()) != len(parsed[histories[1]] or ()):
            issues.append("git_effect_reobservation_registry_parallel_history_mismatch")
        if isinstance(value.get("consumed_count"), int) and value["consumed_count"] != len(parsed[histories[0]] or ()):
            issues.append("git_effect_reobservation_registry_count_mismatch")
    if not _digest_ok(value, REGISTRY_DIGEST_FIELD):
        issues.append("git_effect_reobservation_registry_digest_mismatch")
    return issues


def _source_execution_supported(receipt: Mapping[str, Any], evidence: Mapping[str, Any]) -> bool:
    dispositions = {
        SOURCE_DISPOSITION_COMPLETED,
        SOURCE_DISPOSITION_FAILED,
        SOURCE_DISPOSITION_QUARANTINED,
    }
    performed = (
        receipt["local_commit_performed"], receipt["push_performed"],
        receipt["pull_request_created"], receipt["pull_request_marked_ready"],
        receipt["merge_performed"],
    )
    completed = receipt["codeai_disposition"] == SOURCE_DISPOSITION_COMPLETED
    failed = receipt["codeai_disposition"] == SOURCE_DISPOSITION_FAILED
    quarantined = receipt["codeai_disposition"] == SOURCE_DISPOSITION_QUARANTINED
    return (
        receipt["schema_version"] == "v0.1"
        and receipt["profile_version"] == "CodeAI Autonomous Git Effect Execution v0.1"
        and receipt["codeai_disposition"] in dispositions
        and receipt["effect_phase"] in SUPPORTED_PHASES
        and receipt["route_receipt_recorded"] is True
        and receipt["source_one_effect_lease_verified"] is True
        and receipt["source_one_effect_lease_consumed"] is True
        and receipt["execution_nonce_consumed"] is True
        and receipt["registry_advanced_once"] is True
        and receipt["exactly_one_adapter_invocation"] is True
        and receipt["history_read_only"] is True
        and receipt["future_only"] is False
        and receipt["active_now"] is False
        and receipt["automatic_successor_effect_authority_granted"] is False
        and receipt["general_git_authority_granted"] is False
        and receipt["general_successor_stage_authority_granted"] is False
        and receipt["force_push_performed"] is False
        and receipt["remote_branch_deleted"] is False
        and receipt["admin_merge_bypass_used"] is False
        and receipt["deployment_performed"] is False
        and receipt["secret_material_read"] is False
        and receipt["token_material_emitted"] is False
        and receipt["effect_completion_treated_as_correctness"] is False
        and receipt["merge_treated_as_truth"] is False
        and receipt["effect_completion_confirmed"] is completed
        and receipt["effect_failure_recorded"] is failed
        and receipt["evidence_quarantined"] is quarantined
        and sum(bool(item) for item in performed) == (1 if completed else 0)
        and evidence["adapter_evidence_valid"] is receipt["adapter_evidence_valid"]
        and evidence["effect_completion_confirmed"] is receipt["effect_completion_confirmed"]
    )


def _correspondence_valid(
    lifecycle: Mapping[str, Any], execution: Mapping[str, Any], evidence: Mapping[str, Any],
    request: Mapping[str, Any], policy: Mapping[str, Any],
) -> bool:
    return (
        lifecycle[SOURCE_LIFECYCLE_RECEIPT_DIGEST_FIELD]
        == execution["source_lifecycle_receipt_digest"]
        == evidence["source_lifecycle_receipt_digest"]
        == request["source_lifecycle_receipt_digest"]
        == policy["expected_source_lifecycle_receipt_digest"]
        and execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD]
        == request["source_execution_receipt_digest"]
        == policy["expected_source_execution_receipt_digest"]
        and evidence[SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD]
        == execution["execution_evidence_digest"]
        == request["source_execution_evidence_digest"]
        == policy["expected_source_execution_evidence_digest"]
        and execution["execution_request_digest"] == evidence["execution_request_digest"]
        and request["lifecycle_id"] == lifecycle["lifecycle_id"] == execution["lifecycle_id"]
        and request["repository_full_name"]
        == lifecycle["repository_full_name"]
        == execution["repository_full_name"]
        == policy["expected_repository_full_name"]
        and request["source_commit_sha"] == lifecycle["source_commit_sha"]
        and request["base_branch"] == lifecycle["base_branch"]
        and request["head_branch"] == lifecycle["head_branch"]
        and request["remote_name"] == lifecycle["remote_name"]
        and request["change_set_digest"] == lifecycle["change_set_digest"]
        and request["commit_message_digest"] == lifecycle["commit_message_digest"]
        and request["merge_method"] == lifecycle["merge_method"]
        and request["effect_phase"]
        == lifecycle["next_effect_phase"]
        == execution["effect_phase"]
        == evidence["effect_phase"]
        and request["observer_id"] in policy["authorized_observer_ids"]
        and request["effect_phase"] in policy["allowed_effect_phases"]
        and request["provenance_integrity_confirmed"] is True
        and request["source_correspondence_confirmed"] is True
        and bool(_REPOSITORY.fullmatch(request["repository_full_name"]))
        and bool(_SHA40.fullmatch(request["source_commit_sha"]))
        and bool(_SHA256.fullmatch(request["change_set_digest"]))
        and bool(_SHA256.fullmatch(request["commit_message_digest"]))
        and bool(_BRANCH.fullmatch(request["base_branch"]))
        and bool(_BRANCH.fullmatch(request["head_branch"]))
        and request["base_branch"] != request["head_branch"]
    )


def _fresh_and_replay_closed(
    execution: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any],
    registry: Mapping[str, Any],
) -> bool:
    return (
        request["request_created_epoch"] <= policy["evaluation_epoch"]
        <= request["request_created_epoch"] + policy["maximum_request_age"]
        and execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD]
        not in registry["consumed_execution_receipt_digests"]
        and request["reobservation_nonce_digest"]
        not in registry["consumed_reobservation_nonce_digests"]
        and bool(_SHA256.fullmatch(request["reobservation_nonce_digest"]))
        and registry["consumed_count"] < policy["maximum_registry_entries"]
        and len(registry["consumed_execution_receipt_digests"]) < policy["maximum_registry_entries"]
    )


def _invocation(request: Mapping[str, Any], policy: Mapping[str, Any]) -> GitEffectReobservationInvocation:
    return GitEffectReobservationInvocation(
        lifecycle_id=request["lifecycle_id"],
        repository_full_name=request["repository_full_name"],
        source_commit_sha=request["source_commit_sha"],
        base_branch=request["base_branch"],
        head_branch=request["head_branch"],
        remote_name=request["remote_name"],
        change_set_digest=request["change_set_digest"],
        commit_message_digest=request["commit_message_digest"],
        merge_method=request["merge_method"],
        effect_phase=request["effect_phase"],
        required_check_names=tuple(policy["required_check_names"]),
        maximum_command_count=policy["maximum_command_count"],
        maximum_output_bytes=policy["maximum_output_bytes"],
        maximum_observation_age=policy["maximum_observation_age"],
        evaluation_epoch=policy["evaluation_epoch"],
    )


def _blank_state(invocation: GitEffectReobservationInvocation, epoch: int) -> dict[str, Any]:
    return {
        "lifecycle_id": invocation.lifecycle_id,
        "source_trajectory_receipt_digest": "0" * 64,
        "repository_full_name": invocation.repository_full_name,
        "source_commit_sha": invocation.source_commit_sha,
        "executor_id": "",
        "base_branch": invocation.base_branch,
        "head_branch": invocation.head_branch,
        "remote_name": invocation.remote_name,
        "change_set_digest": invocation.change_set_digest,
        "commit_message_digest": invocation.commit_message_digest,
        "merge_method": invocation.merge_method,
        "local_commit_created": False,
        "local_commit_sha": "",
        "local_commit_parent_sha": "",
        "branch_pushed": False,
        "pushed_head_sha": "",
        "pull_request_created": False,
        "pull_request_number": 0,
        "pull_request_url_digest": "",
        "pull_request_draft": False,
        "pr_head_sha": "",
        "pr_base_branch": "",
        "checks_observed": False,
        "required_check_names": list(invocation.required_check_names),
        "successful_check_names": [],
        "pending_check_names": [],
        "failed_check_names": [],
        "mergeable": False,
        "unresolved_blocker_count": 0,
        "merge_performed": False,
        "merged_head_sha": "",
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "human_handover_performed": False,
        "external_authority_handover_performed": False,
        "observed_at_epoch": epoch,
        "provenance_integrity_confirmed": False,
        "source_correspondence_confirmed": False,
    }


def _exception_result(invocation: GitEffectReobservationInvocation, exc: BaseException) -> dict[str, Any]:
    return {
        "adapter_id": "exception-boundary",
        "adapter_session_id": "exception",
        "status": "failed",
        "command_count": 0,
        "output_bytes": min(len(str(exc).encode()), invocation.maximum_output_bytes),
        "completed_epoch": invocation.evaluation_epoch,
        "network_accessed": False,
        "secret_material_read": False,
        "git_write_performed": False,
        "deployment_performed": False,
        "exception_type": type(exc).__name__,
        **_blank_state(invocation, invocation.evaluation_epoch),
    }


def _validate_adapter_result(
    result: Mapping[str, Any], invocation: GitEffectReobservationInvocation,
) -> tuple[bool, tuple[str, ...]]:
    issues = _exact_fields(result, ADAPTER_RESULT_FIELDS, "git_effect_reobservation_adapter_result")
    if issues:
        return False, tuple(issues)
    for field in ("adapter_id", "adapter_session_id", "status", "exception_type"):
        if not isinstance(result.get(field), str):
            issues.append("git_effect_reobservation_adapter_result_invalid_string:" + field)
    for field in ("command_count", "output_bytes", "completed_epoch"):
        if _nat(result.get(field)) is None:
            issues.append("git_effect_reobservation_adapter_result_invalid_nat:" + field)
    for field in ("network_accessed", "secret_material_read", "git_write_performed", "deployment_performed"):
        if not isinstance(result.get(field), bool):
            issues.append("git_effect_reobservation_adapter_result_invalid_bool:" + field)
    state = {field: result[field] for field in STATE_FIELDS if field != STATE_DIGEST_FIELD}
    state[STATE_DIGEST_FIELD] = canonical_digest(state)
    issues.extend(_validate_lifecycle_state(state))
    if issues:
        return False, tuple(issues)
    common = (
        result["status"] in {"observed", "failed"}
        and result["command_count"] <= invocation.maximum_command_count
        and result["output_bytes"] <= invocation.maximum_output_bytes
        and result["completed_epoch"] <= invocation.evaluation_epoch
        and result["observed_at_epoch"] <= invocation.evaluation_epoch
        and invocation.evaluation_epoch - result["observed_at_epoch"] <= invocation.maximum_observation_age
        and result["network_accessed"] is False
        and result["secret_material_read"] is False
        and result["git_write_performed"] is False
        and result["deployment_performed"] is False
        and result["force_push_performed"] is False
        and result["remote_branch_deleted"] is False
        and result["admin_merge_bypass_used"] is False
        and result["human_handover_performed"] is False
        and result["external_authority_handover_performed"] is False
    )
    if not common:
        issues.append("git_effect_reobservation_adapter_result_common_contract_violation")
        return False, tuple(issues)
    return True, ()


def _state_correspondence_valid(
    result: Mapping[str, Any], lifecycle: Mapping[str, Any],
    invocation: GitEffectReobservationInvocation,
) -> bool:
    required = tuple(result["required_check_names"])
    success = tuple(result["successful_check_names"])
    pending = tuple(result["pending_check_names"])
    failed = tuple(result["failed_check_names"])
    partition = (
        len(success) == len(set(success))
        and len(pending) == len(set(pending))
        and len(failed) == len(set(failed))
        and not (set(success) & set(pending))
        and not (set(success) & set(failed))
        and not (set(pending) & set(failed))
        and (
            (result["checks_observed"] and set(required) == set(success) | set(pending) | set(failed))
            or (not result["checks_observed"] and not success and not pending and not failed)
        )
    )
    baseline = (
        (not lifecycle["local_commit_created_observed"] or result["local_commit_created"])
        and (not lifecycle["branch_pushed_observed"] or result["branch_pushed"])
        and (not lifecycle["pull_request_created_observed"] or result["pull_request_created"])
        and (not lifecycle["required_checks_observed"] or result["checks_observed"])
        and (not lifecycle["merge_performed_observed"] or result["merge_performed"])
    )
    return (
        result["status"] == "observed"
        and result["lifecycle_id"] == lifecycle["lifecycle_id"] == invocation.lifecycle_id
        and result["source_trajectory_receipt_digest"] == lifecycle["source_trajectory_receipt_digest"]
        and result["repository_full_name"] == invocation.repository_full_name
        and result["source_commit_sha"] == invocation.source_commit_sha
        and result["executor_id"] == lifecycle["executor_id"]
        and result["base_branch"] == invocation.base_branch
        and result["head_branch"] == invocation.head_branch
        and result["remote_name"] == invocation.remote_name
        and result["change_set_digest"] == invocation.change_set_digest
        and result["commit_message_digest"] == invocation.commit_message_digest
        and result["merge_method"] == invocation.merge_method
        and tuple(result["required_check_names"]) == invocation.required_check_names
        and result["provenance_integrity_confirmed"] is True
        and result["source_correspondence_confirmed"] is True
        and partition
        and baseline
    )


def _source_effect_correspondence(
    result: Mapping[str, Any], execution: Mapping[str, Any], evidence: Mapping[str, Any],
) -> bool:
    if execution["codeai_disposition"] != SOURCE_DISPOSITION_COMPLETED:
        return True
    source_result = evidence["adapter_result"]
    phase = execution["effect_phase"]
    if phase == PHASE_LOCAL_COMMIT:
        return (
            result["local_commit_created"] is True
            and result["local_commit_sha"] == source_result["local_commit_sha"]
            and result["local_commit_parent_sha"] == source_result["local_commit_parent_sha"]
        )
    if phase == PHASE_PUSH:
        return result["branch_pushed"] is True and result["pushed_head_sha"] == source_result["pushed_head_sha"]
    if phase == PHASE_CREATE_PR:
        return (
            result["pull_request_created"] is True
            and result["pull_request_number"] == source_result["pull_request_number"]
            and result["pull_request_url_digest"] == source_result["pull_request_url_digest"]
            and result["pull_request_draft"] == source_result["pull_request_draft"]
            and result["pr_head_sha"] == source_result["pr_head_sha"]
            and result["pr_base_branch"] == source_result["pr_base_branch"]
        )
    if phase == PHASE_MARK_PR_READY:
        return (
            result["pull_request_created"] is True
            and result["pull_request_number"] == source_result["pull_request_number"]
            and result["pull_request_draft"] is False
            and result["pr_head_sha"] == source_result["pr_head_sha"]
            and result["pr_base_branch"] == source_result["pr_base_branch"]
        )
    if phase == PHASE_MERGE:
        return (
            result["merge_performed"] is True
            and result["merged_head_sha"] == source_result["merged_head_sha"]
            and result["merge_commit_sha"] == source_result["merge_commit_sha"]
        )
    return False


def _next_registry(
    registry: Mapping[str, Any], execution_digest: str, nonce: str, epoch: int,
) -> dict[str, Any]:
    next_registry = {
        "registry_id": registry["registry_id"],
        "registry_revision": registry["registry_revision"] + 1,
        "consumed_execution_receipt_digests": [
            *registry["consumed_execution_receipt_digests"], execution_digest,
        ],
        "consumed_reobservation_nonce_digests": [
            *registry["consumed_reobservation_nonce_digests"], nonce,
        ],
        "consumed_count": registry["consumed_count"] + 1,
        "last_reobservation_epoch": epoch,
    }
    next_registry[REGISTRY_DIGEST_FIELD] = canonical_digest(next_registry)
    return next_registry


def build_codeai_autonomous_git_effect_reobservation(
    *,
    source_lifecycle_receipt: Any,
    source_execution_receipt: Any,
    source_execution_evidence: Any,
    reobservation_request: Any,
    reobservation_policy: Any,
    reobservation_registry: Any,
    adapter: GitEffectReobservationAdapter,
) -> CodeAIAutonomousGitEffectReobservationResult:
    lifecycle = _mapping(source_lifecycle_receipt)
    execution = _mapping(source_execution_receipt)
    source_evidence = _mapping(source_execution_evidence)
    request = _mapping(reobservation_request)
    policy = _mapping(reobservation_policy)
    registry = _mapping(reobservation_registry)
    issues: list[str] = []
    if lifecycle is None:
        issues.append("source_lifecycle_receipt_not_mapping")
    else:
        issues.extend(_validate_source_lifecycle_receipt(lifecycle))
    if execution is None:
        issues.append("source_execution_receipt_not_mapping")
    else:
        issues.extend(_validate_source_execution_receipt(execution))
    if source_evidence is None:
        issues.append("source_execution_evidence_not_mapping")
    else:
        issues.extend(_validate_source_execution_evidence(source_evidence))
    if request is None:
        issues.append("git_effect_reobservation_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("git_effect_reobservation_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    if registry is None:
        issues.append("git_effect_reobservation_registry_not_mapping")
    else:
        issues.extend(_validate_registry(registry))
    if issues or None in (lifecycle, execution, source_evidence, request, policy, registry):
        return CodeAIAutonomousGitEffectReobservationResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None,
        )
    assert lifecycle is not None and execution is not None and source_evidence is not None
    assert request is not None and policy is not None and registry is not None
    if not _source_execution_supported(execution, source_evidence):
        issues.append("source_execution_receipt_not_supported")
    if not _correspondence_valid(lifecycle, execution, source_evidence, request, policy):
        issues.append("git_effect_reobservation_correspondence_mismatch")
    if not _fresh_and_replay_closed(execution, request, policy, registry):
        issues.append("git_effect_reobservation_freshness_or_replay_violation")
    if (
        policy["network_access_allowed"]
        or policy["secret_access_allowed"]
        or policy["git_write_allowed"]
        or policy["deployment_allowed"]
    ):
        issues.append("git_effect_reobservation_policy_effect_authority_not_denied")
    if issues:
        return CodeAIAutonomousGitEffectReobservationResult(
            STATUS_BLOCKED, tuple(issues), None, None, None, None,
        )

    invocation = _invocation(request, policy)
    try:
        raw = adapter(invocation)
        adapter_result = dict(raw) if isinstance(raw, Mapping) else {"malformed_result": raw}
    except BaseException as exc:
        adapter_result = _exception_result(invocation, exc)

    valid, adapter_issues = _validate_adapter_result(adapter_result, invocation)
    state_correspondence = valid and _state_correspondence_valid(adapter_result, lifecycle, invocation)
    effect_correspondence = (
        state_correspondence
        and _source_effect_correspondence(adapter_result, execution, source_evidence)
    )
    observed = valid and state_correspondence and effect_correspondence
    failed = valid and adapter_result["status"] == "failed"
    if observed:
        disposition = DISPOSITION_COMPLETED
    elif failed:
        disposition = DISPOSITION_FAILED
    else:
        disposition = DISPOSITION_EVIDENCE_QUARANTINED

    next_registry = _next_registry(
        registry,
        execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD],
        request["reobservation_nonce_digest"],
        policy["evaluation_epoch"],
    )
    lifecycle_state: dict[str, Any] | None = None
    if observed:
        lifecycle_state = {
            field: adapter_result[field] for field in STATE_FIELDS if field != STATE_DIGEST_FIELD
        }
        lifecycle_state[STATE_DIGEST_FIELD] = canonical_digest(lifecycle_state)

    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_lifecycle_receipt_digest": lifecycle[SOURCE_LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_execution_receipt_digest": execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD],
        "source_execution_evidence_digest": source_evidence[SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD],
        "reobservation_request_digest": request[REQUEST_DIGEST_FIELD],
        "effect_phase": request["effect_phase"],
        "source_execution_disposition": execution["codeai_disposition"],
        "adapter_result": adapter_result,
        "adapter_evidence_valid": valid,
        "adapter_evidence_issues": list(adapter_issues),
        "lifecycle_state_correspondence_confirmed": state_correspondence,
        "source_effect_correspondence_confirmed": effect_correspondence,
        "fresh_lifecycle_state_issued": lifecycle_state is not None,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_lifecycle_receipt_digest": lifecycle[SOURCE_LIFECYCLE_RECEIPT_DIGEST_FIELD],
        "source_execution_receipt_digest": execution[SOURCE_EXECUTION_RECEIPT_DIGEST_FIELD],
        "source_execution_evidence_digest": source_evidence[SOURCE_EXECUTION_EVIDENCE_DIGEST_FIELD],
        "reobservation_request_digest": request[REQUEST_DIGEST_FIELD],
        "reobservation_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "reobservation_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "lifecycle_state_digest": lifecycle_state[STATE_DIGEST_FIELD] if lifecycle_state else "",
        "lifecycle_id": request["lifecycle_id"],
        "reobservation_id": request["reobservation_id"],
        "reobservation_session_id": request["reobservation_session_id"],
        "repository_full_name": request["repository_full_name"],
        "effect_phase": request["effect_phase"],
        "source_execution_disposition": execution["codeai_disposition"],
        "codeai_disposition": disposition,
        "operating_mode": "autonomous_read_only_git_effect_reobservation",
        "route_receipt_recorded": True,
        "source_lifecycle_receipt_verified": True,
        "source_execution_receipt_verified": True,
        "source_execution_evidence_verified": True,
        "source_execution_receipt_consumed_for_reobservation": True,
        "reobservation_nonce_consumed": True,
        "registry_advanced_once": True,
        "exactly_one_adapter_invocation": True,
        "adapter_evidence_valid": valid,
        "lifecycle_state_correspondence_confirmed": state_correspondence,
        "source_effect_correspondence_confirmed": effect_correspondence,
        "fresh_lifecycle_state_issued": lifecycle_state is not None,
        "reobservation_failure_recorded": failed,
        "evidence_quarantined": disposition == DISPOSITION_EVIDENCE_QUARANTINED,
        "network_accessed": False,
        "secret_material_read": False,
        "git_write_performed": False,
        "deployment_performed": False,
        "effect_execution_performed": False,
        "automatic_successor_effect_authority_granted": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "observation_treated_as_correctness": False,
        "merge_treated_as_truth": False,
        "history_read_only": True,
        "future_only": False,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIAutonomousGitEffectReobservationResult(
        STATUS_READY, (), evidence, next_registry, lifecycle_state, receipt,
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "GitEffectReobservationInvocation",
    "GitEffectReobservationAdapter",
    "CodeAIAutonomousGitEffectReobservationResult",
    "build_codeai_autonomous_git_effect_reobservation",
    "canonical_digest",
    "digest_without",
]
