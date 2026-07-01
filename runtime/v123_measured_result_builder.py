#!/usr/bin/env python3
from dataclasses import fields, replace
from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import RepositorySandboxWorktreeResult, VERSION, repository_sandbox_worktree_result_digest
from runtime.v123_sandbox_worktree_result import repository_sandbox_worktree_result_issues


def _empty():
    data = {}
    for field in fields(RepositorySandboxWorktreeResult):
        kind = str(field.type)
        data[field.name] = False if "bool" in kind else (() if "tuple" in kind else ({} if "dict" in kind else ""))
    return data


def build_sandbox_worktree_result(request, v122_request, v122_result, policy, index_path, sandbox_path, upstream, before, after, state):
    request_ok, result_ok, accepted, binding = upstream
    unchanged = {name: before[name] == after[name] for name in ("dedicated_index", "canonical_index", "repository_root", "objects", "references", "reflogs")}
    data = _empty()
    data.update({
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
        "dedicated_index_path_digest": canonical_digest({"path": str(index_path)}),
        "sandbox_directory_name": request.sandbox_directory_name,
        "sandbox_path_digest": canonical_digest({"path": str(sandbox_path)}),
        "expected_tree_oid": request.expected_tree_oid,
        "published_commit_oid": request.published_commit_oid,
        "policy_valid": state["policy_valid"],
        "request_valid": state["request_valid"],
        "v122_request_valid": request_ok,
        "v122_result_valid": result_ok,
        "v122_result_accepted": accepted,
        "request_binding_exact": binding,
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
        "dedicated_index_unchanged": unchanged["dedicated_index"],
        "canonical_index_unchanged": unchanged["canonical_index"],
        "repository_root_unchanged": unchanged["repository_root"],
        "checkout_command_attempted": state["checkout_attempted"],
        "checkout_command_succeeded": state["checkout_succeeded"],
        "exact_existing_sandbox_reused": state["reused"],
        "live_git_command_invoked": bool(state["receipts"]),
        "live_repository_mutated": state["write_performed"],
        "sandbox_working_tree_write_performed": state["write_performed"],
        "repository_root_working_tree_write_performed": not unchanged["repository_root"],
        "dedicated_index_write_performed": not unchanged["dedicated_index"],
        "canonical_index_write_performed": not unchanged["canonical_index"],
        "current_object_database_write_performed": not unchanged["objects"],
        "current_reference_write_performed": not unchanged["references"],
        "reflog_write_performed": not unchanged["reflogs"],
        "push_performed": False,
        "signing_performed": False,
        "prior_object_database_write_performed": v122_result.prior_object_database_write_performed,
        "prior_checkpoint_reference_write_performed": v122_result.prior_checkpoint_reference_write_performed,
        "prior_dedicated_index_write_performed": v122_result.dedicated_index_write_performed,
        "command_receipts": tuple(state["receipts"]),
        "checks": dict(state["checks"], **{name + "_unchanged": value for name, value in unchanged.items()}),
        "evidence_digests": {name + "_before": canonical_digest({"value": before[name]}) for name in unchanged} | {name + "_after": canonical_digest({"value": after[name]}) for name in unchanged},
        "result_digest": "",
        "version": VERSION,
    })
    result = RepositorySandboxWorktreeResult(**data)
    result = replace(result, result_digest=repository_sandbox_worktree_result_digest(result))
    issues = repository_sandbox_worktree_result_issues(result)
    if issues:
        raise ValueError(f"sandbox_worktree_result_invalid:{issues[0]}")
    return result
