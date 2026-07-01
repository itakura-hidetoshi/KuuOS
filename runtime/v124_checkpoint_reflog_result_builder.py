#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    RepositoryCheckpointReflogResult,
    repository_checkpoint_reflog_result_digest,
)
from runtime.v124_checkpoint_reflog_result import (
    repository_checkpoint_reflog_result_issues,
)


def build_checkpoint_reflog_result(
    request,
    v121_request,
    v121_result,
    v123_request,
    v123_result,
    policy,
    target_path,
    upstream,
    before,
    after,
    state,
):
    (
        v121_request_valid,
        v121_result_valid,
        v121_accepted,
        v123_request_valid,
        v123_result_valid,
        v123_accepted,
        binding_exact,
    ) = upstream
    target_changed = before["target_reflog"] != after["target_reflog"]
    other_logs_changed = before["other_logs"] != after["other_logs"]
    objects_changed = before["objects"] != after["objects"]
    references_changed = before["references"] != after["references"]
    standard_index_changed = before["standard_index"] != after["standard_index"]
    dedicated_index_changed = before["dedicated_index"] != after["dedicated_index"]
    working_tree_changed = before["working_tree"] != after["working_tree"]
    index_changed = standard_index_changed or dedicated_index_changed
    live_mutated = any(
        (
            target_changed,
            other_logs_changed,
            objects_changed,
            references_changed,
            index_changed,
            working_tree_changed,
        )
    )
    result = RepositoryCheckpointReflogResult(
        operation_id=request.operation_id,
        status=state["status"],
        reason=state["reason"],
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        v121_request_digest=v121_request.request_digest,
        v121_result_digest=v121_result.result_digest,
        v123_request_digest=v123_request.request_digest,
        v123_result_digest=v123_result.result_digest,
        repository_path_digest=request.repository_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        checkpoint_reference=request.checkpoint_reference,
        transition_old_oid=request.transition_old_oid,
        transition_new_oid=request.transition_new_oid,
        executor_id=request.executor_id,
        target_reflog_path_digest=canonical_digest(
            {"target_reflog_path": str(target_path)}
        ),
        policy_valid=state["policy_valid"],
        request_valid=state["request_valid"],
        v121_request_valid=v121_request_valid,
        v121_result_valid=v121_result_valid,
        v121_result_accepted=v121_accepted,
        v123_request_valid=v123_request_valid,
        v123_result_valid=v123_result_valid,
        v123_result_accepted=v123_accepted,
        cross_stage_binding_exact=binding_exact,
        executor_authorized=state["executor_authorized"],
        repository_path_allowed=state["repository_path_allowed"],
        checkpoint_namespace_exact=state["checkpoint_namespace_exact"],
        authority_marker_present=state["marker_present"],
        authority_marker_exact=state["marker_exact"],
        current_ref_exact_before=state["current_ref_exact_before"],
        current_ref_exact_after=state["current_ref_exact_after"],
        old_object_present=state["old_object_present"],
        new_object_present=state["new_object_present"],
        target_reflog_path_exact=state["target_path_exact"],
        target_reflog_existed_before=state["target_existed_before"],
        target_reflog_present_after=state["target_present_after"],
        target_reflog_entry_exact=state["target_entry_exact"],
        target_reflog_single_entry=state["target_single_entry"],
        exact_existing_reflog_reused=state["reused"],
        reflog_write_command_attempted=state["write_attempted"],
        reflog_write_command_succeeded=state["write_succeeded"],
        live_git_command_invoked=bool(state["receipts"]),
        live_repository_mutated=live_mutated,
        checkpoint_reflog_write_performed=target_changed,
        other_reflog_write_performed=other_logs_changed,
        current_object_database_write_performed=objects_changed,
        current_reference_write_performed=references_changed,
        index_write_performed=index_changed,
        working_tree_write_performed=working_tree_changed,
        push_performed=False,
        signing_performed=False,
        prior_object_database_write_performed=(
            v123_result.prior_object_database_write_performed
        ),
        prior_checkpoint_reference_write_performed=(
            v123_result.prior_checkpoint_reference_write_performed
        ),
        prior_dedicated_index_write_performed=(
            v123_result.prior_dedicated_index_write_performed
        ),
        prior_sandbox_working_tree_write_performed=(
            v123_result.sandbox_working_tree_write_performed
        ),
        command_receipts=tuple(state["receipts"]),
        checks=dict(
            state["checks"],
            target_reflog_changed=target_changed,
            other_reflogs_unchanged=not other_logs_changed,
            object_database_unchanged=not objects_changed,
            references_unchanged=not references_changed,
            standard_index_unchanged=not standard_index_changed,
            dedicated_index_unchanged=not dedicated_index_changed,
            working_tree_unchanged=not working_tree_changed,
        ),
        evidence_digests={
            "v121_request": v121_request.request_digest,
            "v121_result": v121_result.result_digest,
            "v123_request": v123_request.request_digest,
            "v123_result": v123_result.result_digest,
            "target_reflog_before": before["target_reflog"],
            "target_reflog_after": after["target_reflog"],
            "other_logs_before": canonical_digest(
                {"snapshot": before["other_logs"]}
            ),
            "other_logs_after": canonical_digest(
                {"snapshot": after["other_logs"]}
            ),
            "objects_before": canonical_digest({"snapshot": before["objects"]}),
            "objects_after": canonical_digest({"snapshot": after["objects"]}),
            "references_before": canonical_digest(
                {"snapshot": before["references"]}
            ),
            "references_after": canonical_digest(
                {"snapshot": after["references"]}
            ),
            "standard_index_before": before["standard_index"],
            "standard_index_after": after["standard_index"],
            "dedicated_index_before": before["dedicated_index"],
            "dedicated_index_after": after["dedicated_index"],
            "working_tree_before": canonical_digest(
                {"snapshot": before["working_tree"]}
            ),
            "working_tree_after": canonical_digest(
                {"snapshot": after["working_tree"]}
            ),
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_checkpoint_reflog_result_digest(result),
    )
    issues = repository_checkpoint_reflog_result_issues(result)
    if issues:
        raise ValueError(f"checkpoint_reflog_result_invalid:{issues[0]}")
    return result
