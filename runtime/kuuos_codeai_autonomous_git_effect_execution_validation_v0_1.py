#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_autonomous_git_effect_execution_types_v0_1 import *


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


def _text_digest(label: str, value: str) -> str:
    return canonical_digest({label: value})


def _validate_source(source: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(source, SOURCE_FIELDS, "source_lifecycle_receipt")
    if issues:
        return issues
    string_fields = SOURCE_FIELDS - {
        "route_receipt_recorded", "execution_lease_issued",
        "local_commit_authority_granted", "push_authority_granted",
        "pull_request_authority_granted", "pull_request_readiness_authority_granted",
        "merge_authority_granted", "checks_wait_required", "human_handover_deferred",
        "effect_execution_performed_by_kernel", "local_commit_created_observed",
        "branch_pushed_observed", "pull_request_created_observed",
        "pull_request_draft_observed", "required_checks_observed",
        "all_required_checks_successful", "no_pending_checks", "no_failed_checks",
        "mergeable_observed", "head_sha_pinned", "merge_performed_observed",
        "force_push_performed", "remote_branch_deleted", "admin_merge_bypass_used",
        "human_handover_performed", "external_authority_handover_performed",
        "deployment_authority_granted", "deployment_performed",
        "secret_access_authority_granted", "secret_access_performed",
        "source_receipt_treated_as_git_authority", "checks_treated_as_correctness_proof",
        "merge_treated_as_truth", "history_read_only", "future_only", "active_now",
        "pull_request_number", "unresolved_blocker_count", "successful_check_names",
        "pending_check_names", "failed_check_names",
    }
    for field in string_fields:
        if not isinstance(source.get(field), str):
            issues.append("source_lifecycle_receipt_invalid_string:" + field)
    for field in ("successful_check_names", "pending_check_names", "failed_check_names"):
        if _unique_strings(source.get(field)) is None:
            issues.append("source_lifecycle_receipt_invalid_string_list:" + field)
    for field in ("pull_request_number", "unresolved_blocker_count"):
        if _nat(source.get(field)) is None:
            issues.append("source_lifecycle_receipt_invalid_nat:" + field)
    bool_fields = SOURCE_FIELDS - string_fields - {
        "pull_request_number", "unresolved_blocker_count", "successful_check_names",
        "pending_check_names", "failed_check_names",
    }
    for field in bool_fields:
        if not isinstance(source.get(field), bool):
            issues.append("source_lifecycle_receipt_invalid_bool:" + field)
    if not _digest_ok(source, SOURCE_RECEIPT_DIGEST_FIELD):
        issues.append("source_lifecycle_receipt_digest_mismatch")
    return issues


def _validate_request(request: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(request, REQUEST_FIELDS, "git_effect_request")
    if issues:
        return issues
    string_fields = REQUEST_FIELDS - {
        "pull_request_draft", "pull_request_number", "request_created_epoch",
        "provenance_integrity_confirmed", "source_correspondence_confirmed",
    }
    for field in string_fields:
        if not isinstance(request.get(field), str):
            issues.append("git_effect_request_invalid_string:" + field)
    for field in ("pull_request_number", "request_created_epoch"):
        if _nat(request.get(field)) is None:
            issues.append("git_effect_request_invalid_nat:" + field)
    for field in ("pull_request_draft", "provenance_integrity_confirmed", "source_correspondence_confirmed"):
        if not isinstance(request.get(field), bool):
            issues.append("git_effect_request_invalid_bool:" + field)
    if not _digest_ok(request, REQUEST_DIGEST_FIELD):
        issues.append("git_effect_request_digest_mismatch")
    return issues


def _validate_policy(policy: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(policy, POLICY_FIELDS, "git_effect_policy")
    if issues:
        return issues
    for field in (
        "expected_source_lifecycle_receipt_digest", "expected_repository_full_name",
        POLICY_DIGEST_FIELD,
    ):
        if not isinstance(policy.get(field), str):
            issues.append("git_effect_policy_invalid_string:" + field)
    list_fields = (
        "authorized_executor_ids", "allowed_effect_phases", "allowed_base_branches",
        "allowed_head_branch_prefixes", "allowed_remote_names", "allowed_merge_methods",
    )
    for field in list_fields:
        if _unique_strings(policy.get(field), nonempty=True) is None:
            issues.append("git_effect_policy_invalid_nonempty_unique_list:" + field)
    for field in (
        "maximum_command_count", "maximum_output_bytes", "maximum_timeout_seconds",
        "maximum_request_age", "maximum_registry_entries",
    ):
        if _nat(policy.get(field), positive=True) is None:
            issues.append("git_effect_policy_invalid_positive_nat:" + field)
    if _nat(policy.get("evaluation_epoch")) is None:
        issues.append("git_effect_policy_invalid_nat:evaluation_epoch")
    non_bool = {
        "expected_source_lifecycle_receipt_digest", "expected_repository_full_name",
        *list_fields, "maximum_command_count", "maximum_output_bytes",
        "maximum_timeout_seconds", "maximum_request_age", "maximum_registry_entries", "evaluation_epoch",
        POLICY_DIGEST_FIELD,
    }
    for field in POLICY_FIELDS - non_bool:
        if not isinstance(policy.get(field), bool):
            issues.append("git_effect_policy_invalid_bool:" + field)
    if not _digest_ok(policy, POLICY_DIGEST_FIELD):
        issues.append("git_effect_policy_digest_mismatch")
    return issues


def _validate_registry(registry: Mapping[str, Any]) -> list[str]:
    issues = _exact_fields(registry, REGISTRY_FIELDS, "git_effect_registry")
    if issues:
        return issues
    if not isinstance(registry.get("registry_id"), str) or not registry["registry_id"]:
        issues.append("git_effect_registry_invalid_registry_id")
    for field in ("registry_revision", "consumed_count", "last_execution_epoch"):
        if _nat(registry.get(field)) is None:
            issues.append("git_effect_registry_invalid_nat:" + field)
    for field in ("consumed_lifecycle_receipt_digests", "consumed_execution_nonce_digests"):
        values = _unique_strings(registry.get(field))
        if values is None or not all(_SHA256.fullmatch(item) for item in values):
            issues.append("git_effect_registry_invalid_digest_history:" + field)
    if (
        isinstance(registry.get("consumed_lifecycle_receipt_digests"), list)
        and isinstance(registry.get("consumed_execution_nonce_digests"), list)
        and len(registry["consumed_lifecycle_receipt_digests"])
        != len(registry["consumed_execution_nonce_digests"])
    ):
        issues.append("git_effect_registry_parallel_history_mismatch")
    if isinstance(registry.get("consumed_count"), int) and isinstance(
        registry.get("consumed_lifecycle_receipt_digests"), list
    ) and registry["consumed_count"] != len(registry["consumed_lifecycle_receipt_digests"]):
        issues.append("git_effect_registry_count_mismatch")
    if not _digest_ok(registry, REGISTRY_DIGEST_FIELD):
        issues.append("git_effect_registry_digest_mismatch")
    return issues


def _source_supported(source: Mapping[str, Any]) -> bool:
    phase = source["next_effect_phase"]
    if phase not in SUPPORTED_PHASES:
        return False
    authority_values = {
        p: source[field] for p, field in _SOURCE_AUTHORITY_FIELDS.items()
    }
    return (
        source["schema_version"] == "v0.1"
        and source["profile_version"] == "CodeAI Autonomous Git Lifecycle v0.1"
        and source["route_receipt_recorded"] is True
        and source["codeai_disposition"] == _SOURCE_DISPOSITIONS[phase]
        and source["operating_mode"] == _SOURCE_MODES[phase]
        and source["execution_lease_issued"] is True
        and source["effect_execution_performed_by_kernel"] is False
        and source["active_now"] is True
        and source["future_only"] is True
        and authority_values[phase] is True
        and sum(bool(v) for v in authority_values.values()) == 1
        and source["checks_wait_required"] is False
        and source["human_handover_deferred"] is False
        and source["force_push_performed"] is False
        and source["remote_branch_deleted"] is False
        and source["admin_merge_bypass_used"] is False
        and source["deployment_authority_granted"] is False
        and source["deployment_performed"] is False
        and source["secret_access_authority_granted"] is False
        and source["secret_access_performed"] is False
        and source["repository_full_name"]
        and bool(_REPOSITORY.fullmatch(source["repository_full_name"]))
        and bool(_SHA40.fullmatch(source["source_commit_sha"]))
        and bool(_SHA256.fullmatch(source["change_set_digest"]))
        and bool(_SHA256.fullmatch(source["commit_message_digest"]))
        and bool(_BRANCH.fullmatch(source["base_branch"]))
        and bool(_BRANCH.fullmatch(source["head_branch"]))
        and source["base_branch"] != source["head_branch"]
    )


def _phase_enabled(phase: str, policy: Mapping[str, Any]) -> bool:
    return {
        PHASE_LOCAL_COMMIT: policy["allow_local_commit"],
        PHASE_PUSH: policy["allow_push"],
        PHASE_CREATE_PR: policy["allow_pull_request_creation"],
        PHASE_MARK_PR_READY: policy["allow_pull_request_readiness"],
        PHASE_MERGE: policy["allow_merge"],
    }[phase]


def _correspondence_valid(
    source: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any]
) -> bool:
    return (
        request["source_lifecycle_receipt_digest"]
        == source[SOURCE_RECEIPT_DIGEST_FIELD]
        == policy["expected_source_lifecycle_receipt_digest"]
        and request["lifecycle_id"] == source["lifecycle_id"]
        and request["executor_id"] == source["executor_id"]
        and request["repository_full_name"]
        == source["repository_full_name"]
        == policy["expected_repository_full_name"]
        and request["source_commit_sha"] == source["source_commit_sha"]
        and request["base_branch"] == source["base_branch"]
        and request["head_branch"] == source["head_branch"]
        and request["remote_name"] == source["remote_name"]
        and request["merge_method"] == source["merge_method"]
        and request["change_set_digest"] == source["change_set_digest"]
        and request["commit_message_digest"] == source["commit_message_digest"]
        and request["requested_effect_phase"] == source["next_effect_phase"]
        and request["provenance_integrity_confirmed"] is True
        and request["source_correspondence_confirmed"] is True
    )


def _scope_valid(request: Mapping[str, Any], policy: Mapping[str, Any]) -> bool:
    phase = request["requested_effect_phase"]
    return (
        request["executor_id"] in policy["authorized_executor_ids"]
        and phase in policy["allowed_effect_phases"]
        and _phase_enabled(phase, policy)
        and request["base_branch"] in policy["allowed_base_branches"]
        and any(request["head_branch"].startswith(p) for p in policy["allowed_head_branch_prefixes"])
        and request["remote_name"] in policy["allowed_remote_names"]
        and request["merge_method"] in policy["allowed_merge_methods"]
        and policy["allow_force_push"] is False
        and policy["allow_remote_branch_deletion"] is False
        and policy["allow_admin_merge_bypass"] is False
        and policy["allow_deployment"] is False
        and policy["allow_secret_material_read"] is False
    )


def _phase_request_valid(source: Mapping[str, Any], request: Mapping[str, Any]) -> bool:
    phase = request["requested_effect_phase"]
    empty_pr_text = request["pull_request_title"] == request["pull_request_body"] == ""
    zero_pr = request["pull_request_number"] == 0
    if phase == PHASE_LOCAL_COMMIT:
        return (
            bool(request["commit_message"])
            and _text_digest("commit_message", request["commit_message"])
            == request["commit_message_digest"]
            and empty_pr_text
            and request["pull_request_body_digest"] == _text_digest("pull_request_body", "")
            and request["pull_request_draft"] is False
            and zero_pr
            and request["expected_head_sha"] == source["source_commit_sha"]
            and source["local_commit_created_observed"] is False
        )
    if request["commit_message"] != "":
        return False
    empty_body_digest = request["pull_request_body_digest"] == _text_digest("pull_request_body", "")
    if phase == PHASE_PUSH:
        return (
            empty_pr_text and empty_body_digest and zero_pr and request["pull_request_draft"] is False
            and request["expected_head_sha"] == source["local_commit_sha"]
            and bool(_SHA40.fullmatch(source["local_commit_sha"]))
            and source["local_commit_created_observed"] is True
            and source["branch_pushed_observed"] is False
        )
    if phase == PHASE_CREATE_PR:
        return (
            bool(request["pull_request_title"])
            and bool(request["pull_request_body"])
            and request["pull_request_body_digest"]
            == _text_digest("pull_request_body", request["pull_request_body"])
            and request["pull_request_draft"] is True
            and zero_pr
            and request["expected_head_sha"] == source["pushed_head_sha"]
            and bool(_SHA40.fullmatch(source["pushed_head_sha"]))
            and source["branch_pushed_observed"] is True
            and source["pull_request_created_observed"] is False
        )
    if phase == PHASE_MARK_PR_READY:
        return (
            empty_pr_text and empty_body_digest and request["pull_request_draft"] is False
            and request["pull_request_number"] == source["pull_request_number"] > 0
            and request["expected_head_sha"] == source["local_commit_sha"]
            and source["pull_request_created_observed"] is True
            and source["pull_request_draft_observed"] is True
        )
    if phase == PHASE_MERGE:
        return (
            empty_pr_text and empty_body_digest and request["pull_request_draft"] is False
            and request["pull_request_number"] == source["pull_request_number"] > 0
            and request["expected_head_sha"] == source["local_commit_sha"]
            and source["pull_request_created_observed"] is True
            and source["pull_request_draft_observed"] is False
            and source["required_checks_observed"] is True
            and source["all_required_checks_successful"] is True
            and source["no_pending_checks"] is True
            and source["no_failed_checks"] is True
            and source["mergeable_observed"] is True
            and source["unresolved_blocker_count"] == 0
            and source["head_sha_pinned"] is True
        )
    return False


def _fresh_and_replay_closed(
    source: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any], registry: Mapping[str, Any]
) -> bool:
    now = policy["evaluation_epoch"]
    return (
        request["request_created_epoch"] <= now
        and now - request["request_created_epoch"] <= policy["maximum_request_age"]
        and registry["last_execution_epoch"] <= now
        and len(registry["consumed_lifecycle_receipt_digests"]) < policy["maximum_registry_entries"]
        and source[SOURCE_RECEIPT_DIGEST_FIELD] not in registry["consumed_lifecycle_receipt_digests"]
        and request["execution_nonce_digest"] not in registry["consumed_execution_nonce_digests"]
        and bool(_SHA256.fullmatch(request["execution_nonce_digest"]))
    )


__all__ = [name for name in globals() if not name.startswith("__")]
