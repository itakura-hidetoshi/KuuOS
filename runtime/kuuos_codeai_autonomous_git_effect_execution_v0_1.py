#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import *
from runtime.kuuos_codeai_autonomous_git_effect_execution_validation_v0_1 import *


def _invocation(request: Mapping[str, Any], policy: Mapping[str, Any]) -> GitEffectInvocation:
    return GitEffectInvocation(
        effect_phase=request["requested_effect_phase"],
        repository_full_name=request["repository_full_name"],
        source_commit_sha=request["source_commit_sha"],
        base_branch=request["base_branch"],
        head_branch=request["head_branch"],
        remote_name=request["remote_name"],
        merge_method=request["merge_method"],
        change_set_digest=request["change_set_digest"],
        commit_message=request["commit_message"],
        pull_request_title=request["pull_request_title"],
        pull_request_body=request["pull_request_body"],
        pull_request_draft=request["pull_request_draft"],
        pull_request_number=request["pull_request_number"],
        expected_head_sha=request["expected_head_sha"],
        maximum_command_count=policy["maximum_command_count"],
        maximum_output_bytes=policy["maximum_output_bytes"],
        maximum_timeout_seconds=policy["maximum_timeout_seconds"],
        opaque_token_use_allowed=policy["allow_opaque_token_use"],
        secret_material_read_allowed=policy["allow_secret_material_read"],
    )


def _exception_result(invocation: GitEffectInvocation, exc: BaseException, epoch: int) -> dict[str, Any]:
    return {
        "adapter_id": "exception-boundary",
        "adapter_session_id": "exception",
        "effect_phase": invocation.effect_phase,
        "status": "failed",
        "exit_code": 1,
        "command_count": 0,
        "stdout": "",
        "stderr": str(exc)[:4096],
        "completed_epoch": epoch,
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
        "pull_request_marked_ready": False,
        "merge_performed": False,
        "merged_head_sha": "",
        "merge_commit_sha": "",
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "deployment_performed": False,
        "secret_material_read": False,
        "token_material_emitted": False,
        "opaque_token_used": False,
        "exception_type": type(exc).__name__,
    }


def _adapter_result_valid(result: Mapping[str, Any], invocation: GitEffectInvocation, policy: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
    issues = _exact_fields(result, ADAPTER_RESULT_FIELDS, "git_effect_adapter_result")
    if issues:
        return False, tuple(issues)
    string_fields = {
        "adapter_id", "adapter_session_id", "effect_phase", "status", "stdout", "stderr",
        "local_commit_sha", "local_commit_parent_sha", "pushed_head_sha",
        "pull_request_url_digest", "pr_head_sha", "pr_base_branch", "merged_head_sha",
        "merge_commit_sha", "exception_type",
    }
    for field in string_fields:
        if not isinstance(result.get(field), str):
            issues.append("git_effect_adapter_result_invalid_string:" + field)
    for field in ("exit_code", "command_count", "completed_epoch", "pull_request_number"):
        if _nat(result.get(field)) is None:
            issues.append("git_effect_adapter_result_invalid_nat:" + field)
    bool_fields = ADAPTER_RESULT_FIELDS - string_fields - {
        "exit_code", "command_count", "completed_epoch", "pull_request_number"
    }
    for field in bool_fields:
        if not isinstance(result.get(field), bool):
            issues.append("git_effect_adapter_result_invalid_bool:" + field)
    if issues:
        return False, tuple(issues)
    output_bytes = len(result["stdout"].encode()) + len(result["stderr"].encode())
    forbidden = (
        result["force_push_performed"] or result["remote_branch_deleted"]
        or result["admin_merge_bypass_used"] or result["deployment_performed"]
        or result["secret_material_read"] or result["token_material_emitted"]
    )
    effect_flags = (
        result["local_commit_created"],
        result["branch_pushed"],
        result["pull_request_created"],
        result["pull_request_marked_ready"],
        result["merge_performed"],
    )
    failed_without_confirmed_effect = (
        result["status"] != "failed" or not any(effect_flags)
    )
    common = (
        result["effect_phase"] == invocation.effect_phase
        and result["status"] in {"completed", "failed"}
        and result["command_count"] <= policy["maximum_command_count"]
        and output_bytes <= policy["maximum_output_bytes"]
        and result["completed_epoch"] <= policy["evaluation_epoch"]
        and not forbidden
        and failed_without_confirmed_effect
        and (not result["opaque_token_used"] or policy["allow_opaque_token_use"])
    )
    if not common:
        issues.append("git_effect_adapter_result_common_contract_violation")
        return False, tuple(issues)
    return True, ()


def _phase_completion_valid(result: Mapping[str, Any], invocation: GitEffectInvocation) -> bool:
    if result["status"] != "completed" or result["exit_code"] != 0:
        return False
    phase = invocation.effect_phase
    if phase == PHASE_LOCAL_COMMIT:
        return (
            result["local_commit_created"] is True
            and bool(_SHA40.fullmatch(result["local_commit_sha"]))
            and result["local_commit_parent_sha"] == invocation.source_commit_sha
            and not result["branch_pushed"] and not result["pull_request_created"]
            and not result["pull_request_marked_ready"] and not result["merge_performed"]
        )
    if phase == PHASE_PUSH:
        return (
            result["branch_pushed"] is True
            and result["pushed_head_sha"] == invocation.expected_head_sha
            and not result["local_commit_created"] and not result["pull_request_created"]
            and not result["pull_request_marked_ready"] and not result["merge_performed"]
        )
    if phase == PHASE_CREATE_PR:
        return (
            result["pull_request_created"] is True
            and result["pull_request_number"] > 0
            and bool(_SHA256.fullmatch(result["pull_request_url_digest"]))
            and result["pull_request_draft"] is True
            and result["pr_head_sha"] == invocation.expected_head_sha
            and result["pr_base_branch"] == invocation.base_branch
            and not result["local_commit_created"] and not result["branch_pushed"]
            and not result["pull_request_marked_ready"] and not result["merge_performed"]
        )
    if phase == PHASE_MARK_PR_READY:
        return (
            result["pull_request_marked_ready"] is True
            and result["pull_request_number"] == invocation.pull_request_number
            and result["pr_head_sha"] == invocation.expected_head_sha
            and result["pull_request_draft"] is False
            and not result["pull_request_created"] and not result["merge_performed"]
        )
    if phase == PHASE_MERGE:
        return (
            result["merge_performed"] is True
            and result["pull_request_number"] == invocation.pull_request_number
            and result["merged_head_sha"] == invocation.expected_head_sha
            and bool(_SHA40.fullmatch(result["merge_commit_sha"]))
            and not result["pull_request_created"] and not result["pull_request_marked_ready"]
        )
    return False


def _next_registry(registry: Mapping[str, Any], source_digest: str, nonce: str, epoch: int) -> dict[str, Any]:
    next_registry = {
        "registry_id": registry["registry_id"],
        "registry_revision": registry["registry_revision"] + 1,
        "consumed_lifecycle_receipt_digests": [
            *registry["consumed_lifecycle_receipt_digests"], source_digest
        ],
        "consumed_execution_nonce_digests": [
            *registry["consumed_execution_nonce_digests"], nonce
        ],
        "consumed_count": registry["consumed_count"] + 1,
        "last_execution_epoch": epoch,
    }
    next_registry[REGISTRY_DIGEST_FIELD] = canonical_digest(next_registry)
    return next_registry


def _mode(phase: str) -> str:
    if phase == PHASE_LOCAL_COMMIT:
        return MODE_LOCAL
    if phase == PHASE_PUSH:
        return MODE_REMOTE
    if phase in {PHASE_CREATE_PR, PHASE_MARK_PR_READY}:
        return MODE_PR
    return MODE_MERGE


def build_codeai_autonomous_git_effect_execution(
    *,
    source_lifecycle_receipt: Any,
    execution_request: Any,
    execution_policy: Any,
    execution_registry: Any,
    adapter: GitEffectAdapter,
) -> CodeAIAutonomousGitEffectExecutionResult:
    source = _mapping(source_lifecycle_receipt)
    request = _mapping(execution_request)
    policy = _mapping(execution_policy)
    registry = _mapping(execution_registry)
    issues: list[str] = []
    if source is None:
        issues.append("source_lifecycle_receipt_not_mapping")
    else:
        issues.extend(_validate_source(source))
    if request is None:
        issues.append("git_effect_request_not_mapping")
    else:
        issues.extend(_validate_request(request))
    if policy is None:
        issues.append("git_effect_policy_not_mapping")
    else:
        issues.extend(_validate_policy(policy))
    if registry is None:
        issues.append("git_effect_registry_not_mapping")
    else:
        issues.extend(_validate_registry(registry))
    if issues or source is None or request is None or policy is None or registry is None:
        return CodeAIAutonomousGitEffectExecutionResult(STATUS_BLOCKED, tuple(issues), None, None, None)
    if not _source_supported(source):
        issues.append("source_lifecycle_receipt_not_active_one_effect_lease")
    if not _correspondence_valid(source, request, policy):
        issues.append("git_effect_correspondence_mismatch")
    if not _scope_valid(request, policy):
        issues.append("git_effect_scope_not_allowed")
    if not _phase_request_valid(source, request):
        issues.append("git_effect_phase_request_invalid")
    if not _fresh_and_replay_closed(source, request, policy, registry):
        issues.append("git_effect_freshness_or_replay_violation")
    if issues:
        return CodeAIAutonomousGitEffectExecutionResult(STATUS_BLOCKED, tuple(issues), None, None, None)

    invocation = _invocation(request, policy)
    try:
        raw = adapter(invocation)
        result = dict(raw) if isinstance(raw, Mapping) else {"malformed_result": raw}
    except BaseException as exc:
        result = _exception_result(invocation, exc, policy["evaluation_epoch"])

    valid, evidence_issues = _adapter_result_valid(result, invocation, policy)
    completed = valid and _phase_completion_valid(result, invocation)
    failed = valid and result["status"] == "failed"
    if completed:
        disposition = DISPOSITION_COMPLETED
    elif failed:
        disposition = DISPOSITION_FAILED
    else:
        disposition = DISPOSITION_EVIDENCE_QUARANTINED

    next_registry = _next_registry(
        registry,
        source[SOURCE_RECEIPT_DIGEST_FIELD],
        request["execution_nonce_digest"],
        policy["evaluation_epoch"],
    )
    evidence = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_lifecycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "execution_request_digest": request[REQUEST_DIGEST_FIELD],
        "effect_phase": request["requested_effect_phase"],
        "adapter_result": result,
        "adapter_evidence_valid": valid,
        "adapter_evidence_issues": list(evidence_issues),
        "effect_completion_confirmed": completed,
    }
    evidence[EVIDENCE_DIGEST_FIELD] = canonical_digest(evidence)

    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "source_lifecycle_receipt_digest": source[SOURCE_RECEIPT_DIGEST_FIELD],
        "execution_request_digest": request[REQUEST_DIGEST_FIELD],
        "execution_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_registry_digest": registry[REGISTRY_DIGEST_FIELD],
        "next_registry_digest": next_registry[REGISTRY_DIGEST_FIELD],
        "execution_evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "lifecycle_id": source["lifecycle_id"],
        "execution_id": request["execution_id"],
        "execution_session_id": request["execution_session_id"],
        "repository_full_name": request["repository_full_name"],
        "effect_phase": request["requested_effect_phase"],
        "codeai_disposition": disposition,
        "operating_mode": _mode(request["requested_effect_phase"]),
        "route_receipt_recorded": True,
        "source_one_effect_lease_verified": True,
        "source_one_effect_lease_consumed": True,
        "execution_nonce_consumed": True,
        "registry_advanced_once": True,
        "exactly_one_adapter_invocation": True,
        "adapter_evidence_valid": valid,
        "effect_completion_confirmed": completed,
        "effect_failure_recorded": failed,
        "evidence_quarantined": disposition == DISPOSITION_EVIDENCE_QUARANTINED,
        "reobservation_required": not completed,
        "local_commit_performed": completed and request["requested_effect_phase"] == PHASE_LOCAL_COMMIT,
        "push_performed": completed and request["requested_effect_phase"] == PHASE_PUSH,
        "pull_request_created": completed and request["requested_effect_phase"] == PHASE_CREATE_PR,
        "pull_request_marked_ready": completed and request["requested_effect_phase"] == PHASE_MARK_PR_READY,
        "merge_performed": completed and request["requested_effect_phase"] == PHASE_MERGE,
        "force_push_performed": False,
        "remote_branch_deleted": False,
        "admin_merge_bypass_used": False,
        "deployment_performed": False,
        "secret_material_read": False,
        "token_material_emitted": False,
        "automatic_successor_effect_authority_granted": False,
        "general_git_authority_granted": False,
        "general_successor_stage_authority_granted": False,
        "effect_completion_treated_as_correctness": False,
        "merge_treated_as_truth": False,
        "history_read_only": True,
        "future_only": False,
        "active_now": False,
    }
    receipt[RECEIPT_DIGEST_FIELD] = canonical_digest(receipt)
    return CodeAIAutonomousGitEffectExecutionResult(
        STATUS_READY, (), evidence, next_registry, receipt
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "GitEffectInvocation",
    "GitEffectAdapter",
    "CodeAIAutonomousGitEffectExecutionResult",
    "build_codeai_autonomous_git_effect_execution",
    "canonical_digest",
    "digest_without",
]
