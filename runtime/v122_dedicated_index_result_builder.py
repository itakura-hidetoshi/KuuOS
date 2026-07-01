#!/usr/bin/env python3
from dataclasses import fields, replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    RepositoryDedicatedIndexResult,
    repository_dedicated_index_result_digest,
)
from runtime.v122_dedicated_index_result import repository_dedicated_index_result_issues
from runtime.v122_dedicated_index_validation import file_sha256


def _blank_payload() -> dict:
    payload = {}
    for field in fields(RepositoryDedicatedIndexResult):
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


def build_dedicated_index_result(request, v120_request, v120_result, v121_result, policy, index_path, canonical_before, canonical_after, upstream, state):
    v120_request_valid, v120_result_valid, v120_accepted, v121_result_valid, v121_accepted, binding_exact = upstream
    canonical_unchanged = canonical_before == canonical_after
    payload = _blank_payload()
    payload.update({
        "operation_id": request.operation_id,
        "status": state["status"],
        "reason": state["reason"],
        "policy_digest": policy.policy_digest,
        "request_digest": request.request_digest,
        "v120_request_digest": v120_request.request_digest,
        "v120_result_digest": v120_result.result_digest,
        "v121_result_digest": v121_result.result_digest,
        "repository_path_digest": request.repository_path_digest,
        "repository_id": request.repository_id,
        "git_dir_fingerprint": request.git_dir_fingerprint,
        "executor_id": request.executor_id,
        "dedicated_index_filename": request.dedicated_index_filename,
        "dedicated_index_path_digest": canonical_digest({"index_path": str(index_path)}),
        "expected_tree_oid": request.expected_tree_oid,
        "published_commit_oid": request.published_commit_oid,
        "policy_valid": state["policy_valid"],
        "request_valid": state["request_valid"],
        "v120_request_valid": v120_request_valid,
        "v120_result_valid": v120_result_valid,
        "v120_result_accepted": v120_accepted,
        "v121_result_valid": v121_result_valid,
        "v121_result_accepted": v121_accepted,
        "request_binding_exact": binding_exact,
        "executor_authorized": state["executor_authorized"],
        "repository_path_allowed": state["repository_path_allowed"],
        "sandbox_marker_present": state["marker_present"],
        "sandbox_marker_exact": state["marker_exact"],
        "dedicated_index_path_exact": state["path_exact"],
        "dedicated_index_existed_before": state["existed_before"],
        "dedicated_index_present_after": state["present_after"],
        "index_entries_exact": state["entries_exact"],
        "canonical_index_unchanged": canonical_unchanged,
        "read_tree_command_attempted": state["read_attempted"],
        "read_tree_command_succeeded": state["read_succeeded"],
        "verify_index_command_attempted": state["verify_attempted"],
        "verify_index_command_succeeded": state["verify_succeeded"],
        "exact_existing_index_reused": state["reused"],
        "live_git_command_invoked": bool(state["receipts"]),
        "live_repository_mutated": state["write_performed"],
        "dedicated_index_write_performed": state["write_performed"],
        "canonical_index_write_performed": not canonical_unchanged,
        "prior_object_database_write_performed": v120_result.object_database_write_performed,
        "prior_checkpoint_reference_write_performed": v121_result.checkpoint_reference_write_performed,
        "command_receipts": tuple(state["receipts"]),
        "checks": dict(state["checks"], canonical_index_unchanged=canonical_unchanged),
        "evidence_digests": {
            "v120_request": v120_request.request_digest,
            "v120_result": v120_result.result_digest,
            "v121_result": v121_result.result_digest,
            "canonical_index_before": canonical_before,
            "canonical_index_after": canonical_after,
            "dedicated_index_after": file_sha256(index_path),
        },
        "version": "kuuos_repository_dedicated_index_v1_22",
    })
    result = RepositoryDedicatedIndexResult(**payload)
    result = replace(result, result_digest=repository_dedicated_index_result_digest(result))
    issues = repository_dedicated_index_result_issues(result)
    if issues:
        raise ValueError(f"dedicated_index_result_invalid:{issues[0]}")
    return result
