#!/usr/bin/env python3
from dataclasses import fields, replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    RepositorySandboxWorktreeResult,
    VERSION,
    repository_sandbox_worktree_result_digest,
)
from runtime.v123_sandbox_worktree_result import (
    repository_sandbox_worktree_result_issues,
)
from runtime.v123_sandbox_worktree_validation import file_sha256


def _blank_payload() -> dict:
    payload = {}
    for field in fields(RepositorySandboxWorktreeResult):
        kind = str(field.type)
        if "bool" in kind:
            payload[field.name] = False
        elif "tuple" in kind:
            payload[field.name] = ()
        elif "dict" in kind:
            payload[field.name] = {}
        else:
            payload[field.name] = ""
    return payload


def build_sandbox_worktree_result(
    request,
    v122_request,
    v122_result,
    policy,
    index_path,
    sandbox_path,
    upstream,
    before,
    after,
    state,
):
    v122_request_valid, v122_result_valid, v122_accepted, binding_exact = upstream
    dedicated_index_unchanged = before["dedicated_index"] == after["dedicated_index"]
    canonical_index_unchanged = before["canonical_index"] == after["canonical_index"]
    repository_root_unchanged = before["repository_root"] == after["repository_root"]
    payload = _blank_payload()
    payload.update(
        {
            "operation_id": request.operation_id,
            "status": state["status"],
            "reason": state["reason"],
            "policy_digest": policy.policy_digest,
            "request_digest": request.request_digest,
            "v122_request_digest": v122_request.request_digest,
            "v122_result_digest": v122_result.result_digest,
            "repository_path_digest": request.repository_path_digest,
            "repository_id": request.repository_id,
            "git_dir_fingerprint": request.git_dir_fingerprint,
            "executor_id": request.executor_id,
            "dedicated_index_filename": request.dedicated_index_filename,
            "dedicated_index_path_digest": canonical_digest({"index_path": str(index_path)}),
            "sandbox_directory_name": request.sandbox_directory_name,
            "sandbox_path_digest": canonical_digest({"sandbox_path": str(sandbox_path)}),
            "expected_tree_oid": request.expected_tree_oid,
            "published_commit_oid": request.published_commit_oid,
            "policy_valid": state["policy_valid"],
            "request_valid": state["request_valid"],
            "v122_request_valid": v122_request_valid,
            "v122_result_valid": v122_result_valid,
            "v122_result_accepted": v122_accepted,
            "request_binding_exact": binding_exact,
            "executor_authorized": state["executor_authorized"],
            "repository_path_allowed": state["repository_path_allowed"],
            "sandbox_marker_present": state["marker_present"],
            "sandbox_marker_exact": state["marker_exact"],
            "dedicated_index_path_exact": state["index_path_exact"],
            "dedicated_index_present": state["index_present"],
            "sandbox_path_exact": state["sandbox_path_exact"],
            "sandbox_existed_before": state["existed_before"],
            "sandbox_present_after": state["present_after"],
            "sandbox_files_exact": state["files_exact"],
            "sandbox_modes_exact": state["modes_exact"],
            "sandbox_has_no_extra_entries": state["no_extra"],
            "dedicated_index_unchanged": dedicated_index_unchanged,
            "canonical_index_unchanged": canonical_index_unchanged,
            "repository_root_unchanged": repository_root_unchanged,
            "checkout_command_attempted": state["checkout_attempted"],
            "checkout_command_succeeded": state["checkout_succeeded"],
            "exact_existing_sandbox_reused": state["reused"],
            "live_git_command_invoked": bool(state["receipts"]),
            "live_repository_mutated": state["write_performed"],
            "sandbox_working_tree_write_performed": state["write_performed"],
            "repository_root_working_tree_write_performed": not repository_root_unchanged,
            "dedicated_index_write_performed": not dedicated_index_unchanged,
            "canonical_index_write_performed": not canonical_index_unchanged,
            "current_object_database_write_performed": False,
            "current_reference_write_performed": False,
            "reflog_write_performed": False,
            "push_performed": False,
            "signing_performed": False,
            "prior_object_database_write_performed": v122_result.prior_object_database_write_performed,
            "prior_checkpoint_reference_write_performed": v122_result.prior_checkpoint_reference_write_performed,
            "prior_dedicated_index_write_performed": v122_result.dedicated_index_write_performed,
            "command_receipts": tuple(state["receipts"]),
            "checks": dict(
                state["checks"],
                dedicated_index_unchanged=dedicated_index_unchanged,
                canonical_index_unchanged=canonical_index_unchanged,
                repository_root_unchanged=repository_root_unchanged,
            ),
            "evidence_digests": {
                "v122_request": v122_request.request_digest,
                "v122_result": v122_result.result_digest,
                "dedicated_index_before": before["dedicated_index"],
                "dedicated_index_after": after["dedicated_index"],
                "canonical_index_before": before["canonical_index"],
                "canonical_index_after": after["canonical_index"],
                "repository_root_before": canonical_digest({"snapshot": before["repository_root"]}),
                "repository_root_after": canonical_digest({"snapshot": after["repository_root"]}),
                "sandbox_after": canonical_digest(
                    {
                        "files_exact": state["files_exact"],
                        "modes_exact": state["modes_exact"],
                        "no_extra": state["no_extra"],
                        "total_bytes": state["total_bytes"],
                    }
                ),
                "dedicated_index_file_after": file_sha256(index_path),
            },
            "result_digest": "",
            "version": VERSION,
        }
    )
    result = RepositorySandboxWorktreeResult(**payload)
    result = replace(result, result_digest=repository_sandbox_worktree_result_digest(result))
    issues = repository_sandbox_worktree_result_issues(result)
    if issues:
        raise ValueError(f"sandbox_worktree_result_invalid:{issues[0]}")
    return result
