#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    AUTHORITY_MARKER_FILENAME,
    REFLOG_ERROR,
    REFLOG_RECORDED,
    REFLOG_REJECTED,
    REFLOG_REUSED,
)
from runtime.v120_tree_commit_materialization_policy import repository_path_digest
from runtime.v124_checkpoint_reflog_git_adapter import (
    run_checkpoint_reflog_git_command,
)
from runtime.v124_checkpoint_reflog_policy import (
    repository_checkpoint_reflog_policy_issues,
    repository_checkpoint_reflog_request_issues,
    valid_checkpoint_reference,
)
from runtime.v124_checkpoint_reflog_result_builder import (
    build_checkpoint_reflog_result,
)
from runtime.v124_checkpoint_reflog_surfaces import (
    protected_checkpoint_reflog_snapshot,
)
from runtime.v124_checkpoint_reflog_validation import (
    inspect_target_reflog,
    target_reflog_path,
    target_reflog_path_is_exact,
    validate_upstream_binding,
)


def _command_ok(receipt, policy) -> bool:
    return bool(
        receipt.return_code == 0
        and not receipt.timed_out
        and receipt.stdout_size_bytes <= policy.max_output_bytes
        and receipt.stderr_size_bytes <= policy.max_output_bytes
        and receipt.fixed_argument_shape
    )


def execute_repository_checkpoint_reflog(
    request,
    v121_request,
    v121_result,
    v123_request,
    v123_result,
    policy,
    *,
    git_executable: str = "git",
):
    if git_executable != "git":
        raise ValueError("v124_git_executable_not_allowed")
    root = Path(request.repository_path).expanduser().resolve()
    git_dir = root / ".git"
    target_path = target_reflog_path(git_dir, request.checkpoint_reference)
    marker = git_dir / AUTHORITY_MARKER_FILENAME
    upstream = validate_upstream_binding(
        request,
        v121_request,
        v121_result,
        v123_request,
        v123_result,
    )
    policy_valid = not repository_checkpoint_reflog_policy_issues(policy)
    request_valid = not repository_checkpoint_reflog_request_issues(request)
    executor_authorized = request.executor_id in policy.authorized_executor_ids
    actual_repository_digest = repository_path_digest(root)
    repository_path_allowed = bool(
        actual_repository_digest == request.repository_path_digest
        and actual_repository_digest in policy.allowed_repository_path_digests
    )
    checkpoint_namespace_exact = valid_checkpoint_reference(
        request.checkpoint_reference
    )
    marker_present = marker.is_file() and not marker.is_symlink()
    marker_exact = bool(
        marker_present
        and marker.read_bytes()
        == (request.authority_marker_token + "\n").encode("ascii")
    )
    target_path_exact = target_reflog_path_is_exact(
        git_dir,
        request.checkpoint_reference,
        target_path,
    )
    message_within_policy = (
        len(request.message.encode("utf-8")) <= policy.max_message_bytes
    )
    target_existed_before = target_path.exists()
    before = protected_checkpoint_reflog_snapshot(
        root,
        v123_request.dedicated_index_filename,
        target_path,
    )
    state = {
        "status": REFLOG_REJECTED,
        "reason": "CHECKPOINT_REFLOG_PRECONDITION_REJECTED",
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "checkpoint_namespace_exact": checkpoint_namespace_exact,
        "marker_present": marker_present,
        "marker_exact": marker_exact,
        "target_path_exact": target_path_exact,
        "target_existed_before": target_existed_before,
        "target_present_after": target_existed_before,
        "target_entry_exact": False,
        "target_single_entry": False,
        "current_ref_exact_before": False,
        "current_ref_exact_after": False,
        "old_object_present": False,
        "new_object_present": False,
        "write_attempted": False,
        "write_succeeded": False,
        "reused": False,
        "receipts": [],
        "checks": {},
    }
    basic_preconditions = all(
        (
            policy_valid,
            request_valid,
            upstream[0],
            upstream[2],
            upstream[3],
            upstream[5],
            upstream[6],
            executor_authorized,
            repository_path_allowed,
            checkpoint_namespace_exact,
            marker_exact,
            target_path_exact,
            message_within_policy,
            git_dir.is_dir(),
            not git_dir.is_symlink(),
        )
    )
    sequence = 0

    def run(operation, arguments, mutating=False):
        nonlocal sequence
        sequence += 1
        receipt, stdout, stderr = run_checkpoint_reflog_git_command(
            root,
            target_path,
            request,
            policy,
            sequence_number=sequence,
            operation=operation,
            arguments=arguments,
            mutating=mutating,
            git_executable=git_executable,
        )
        state["receipts"].append(receipt)
        return receipt, stdout, stderr

    if basic_preconditions:
        pre_receipt, pre_stdout, _ = run(
            "pre-read-ref",
            (
                "show-ref",
                "--verify",
                "--hash",
                request.checkpoint_reference,
            ),
        )
        state["current_ref_exact_before"] = bool(
            _command_ok(pre_receipt, policy)
            and pre_stdout.strip() == request.transition_new_oid
            and len(pre_stdout.splitlines()) == 1
        )
        old_receipt, _, _ = run(
            "verify-old-object",
            (
                "cat-file",
                "-e",
                f"{request.transition_old_oid}^{{object}}",
            ),
        )
        state["old_object_present"] = _command_ok(old_receipt, policy)
        new_receipt, _, _ = run(
            "verify-new-object",
            (
                "cat-file",
                "-e",
                f"{request.transition_new_oid}^{{object}}",
            ),
        )
        state["new_object_present"] = _command_ok(new_receipt, policy)
        live_preconditions = all(
            (
                state["current_ref_exact_before"],
                state["old_object_present"],
                state["new_object_present"],
            )
        )
        if live_preconditions and target_existed_before:
            (
                state["target_entry_exact"],
                state["target_single_entry"],
            ) = inspect_target_reflog(target_path, request)
            if all(
                (
                    state["target_entry_exact"],
                    state["target_single_entry"],
                    policy.allow_exact_existing_reflog_reuse,
                )
            ):
                state["status"] = REFLOG_REUSED
                state["reason"] = "EXACT_CHECKPOINT_REFLOG_ALREADY_PRESENT"
                state["reused"] = True
                state["current_ref_exact_after"] = True
            else:
                state["reason"] = "EXISTING_CHECKPOINT_REFLOG_MISMATCH"
                state["current_ref_exact_after"] = state[
                    "current_ref_exact_before"
                ]
        elif live_preconditions:
            state["write_attempted"] = True
            write_receipt, _, _ = run(
                "write-checkpoint-reflog",
                (
                    "reflog",
                    "write",
                    request.checkpoint_reference,
                    request.transition_old_oid,
                    request.transition_new_oid,
                    request.message,
                ),
                mutating=True,
            )
            state["write_succeeded"] = _command_ok(write_receipt, policy)
            post_receipt, post_stdout, _ = run(
                "post-read-ref",
                (
                    "show-ref",
                    "--verify",
                    "--hash",
                    request.checkpoint_reference,
                ),
            )
            state["current_ref_exact_after"] = bool(
                _command_ok(post_receipt, policy)
                and post_stdout.strip() == request.transition_new_oid
                and len(post_stdout.splitlines()) == 1
            )
        else:
            state["reason"] = "CHECKPOINT_REFLOG_LIVE_STATE_REJECTED"
            state["current_ref_exact_after"] = state[
                "current_ref_exact_before"
            ]
    state["target_present_after"] = target_path.is_file() and not target_path.is_symlink()
    if state["target_present_after"]:
        (
            state["target_entry_exact"],
            state["target_single_entry"],
        ) = inspect_target_reflog(target_path, request)
    after = protected_checkpoint_reflog_snapshot(
        root,
        v123_request.dedicated_index_filename,
        target_path,
    )
    protected_unchanged = all(
        before[name] == after[name]
        for name in (
            "objects",
            "references",
            "standard_index",
            "dedicated_index",
            "working_tree",
            "other_logs",
        )
    )
    target_changed = before["target_reflog"] != after["target_reflog"]
    if state["write_attempted"]:
        if all(
            (
                state["write_succeeded"],
                target_changed,
                state["target_present_after"],
                state["target_entry_exact"],
                state["target_single_entry"],
                state["current_ref_exact_after"],
                protected_unchanged,
            )
        ):
            state["status"] = REFLOG_RECORDED
            state["reason"] = "EXACT_CHECKPOINT_TRANSITION_REFLOG_RECORDED"
        else:
            state["status"] = REFLOG_ERROR
            state["reason"] = (
                "CHECKPOINT_REFLOG_WRITE_POSTCONDITION_ERROR"
                if target_changed
                else "CHECKPOINT_REFLOG_COMMAND_ERROR"
            )
    elif state["status"] == REFLOG_REUSED and not protected_unchanged:
        state["status"] = REFLOG_ERROR
        state["reason"] = "CHECKPOINT_REFLOG_REUSE_PROTECTED_SURFACE_CHANGED"
    state["checks"] = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "v121_result_accepted": upstream[2],
        "v123_result_accepted": upstream[5],
        "cross_stage_binding_exact": upstream[6],
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "checkpoint_namespace_exact": checkpoint_namespace_exact,
        "authority_marker_exact": marker_exact,
        "target_reflog_path_exact": target_path_exact,
        "message_within_policy": message_within_policy,
        "current_ref_exact_before": state["current_ref_exact_before"],
        "current_ref_exact_after": state["current_ref_exact_after"],
        "old_object_present": state["old_object_present"],
        "new_object_present": state["new_object_present"],
        "target_reflog_entry_exact": state["target_entry_exact"],
        "target_reflog_single_entry": state["target_single_entry"],
        "protected_surfaces_unchanged": protected_unchanged,
    }
    return build_checkpoint_reflog_result(
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
    )
