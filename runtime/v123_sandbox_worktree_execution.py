#!/usr/bin/env python3
from pathlib import Path

from runtime.kuuos_repository_sandbox_worktree_types_v1_23 import (
    SANDBOX_MARKER_FILENAME,
    WORKTREE_ERROR,
    WORKTREE_MATERIALIZED,
    WORKTREE_REJECTED,
    WORKTREE_REUSED,
)
from runtime.v120_tree_commit_materialization_policy import repository_path_digest
from runtime.v123_measured_result_builder import build_sandbox_worktree_result
from runtime.v123_protected_surface import protected_git_snapshot
from runtime.v123_sandbox_worktree_git_adapter import run_sandbox_checkout
from runtime.v123_sandbox_worktree_policy import (
    repository_sandbox_worktree_policy_issues,
    repository_sandbox_worktree_request_issues,
)
from runtime.v123_sandbox_worktree_validation import (
    file_sha256,
    inspect_sandbox,
    repository_root_snapshot,
    validate_upstream_binding,
)


def _command_ok(receipt, policy) -> bool:
    return bool(
        receipt.return_code == 0
        and not receipt.timed_out
        and receipt.stdout_size_bytes <= policy.max_output_bytes
        and receipt.stderr_size_bytes <= policy.max_output_bytes
    )


def execute_repository_sandbox_worktree(
    request,
    v122_request,
    v122_result,
    policy,
    *,
    git_executable: str = "git",
):
    if git_executable != "git":
        raise ValueError("v123_git_executable_not_allowed")
    root = Path(request.repository_path).expanduser().resolve()
    actual_repository_path_digest = repository_path_digest(root)
    git_dir = root / ".git"
    index_path = git_dir / request.dedicated_index_filename
    canonical_index = git_dir / "index"
    sandbox_path = root / request.sandbox_directory_name
    marker = git_dir / SANDBOX_MARKER_FILENAME
    upstream = validate_upstream_binding(request, v122_request, v122_result)
    policy_valid = not repository_sandbox_worktree_policy_issues(policy)
    request_valid = not repository_sandbox_worktree_request_issues(request)
    entry_count_within_policy = len(request.tree_entries) <= policy.max_worktree_entries
    paths_within_policy = all(
        len(entry.path.encode("utf-8")) <= policy.max_worktree_path_bytes
        for entry in request.tree_entries
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids
    repository_path_allowed = bool(
        actual_repository_path_digest == request.repository_path_digest
        and actual_repository_path_digest in policy.allowed_repository_path_digests
    )
    marker_present = marker.is_file() and not marker.is_symlink()
    marker_exact = bool(
        marker_present
        and marker.read_bytes()
        == (request.sandbox_marker_token + "\n").encode("ascii")
    )
    index_path_exact = bool(
        git_dir.is_dir()
        and not git_dir.is_symlink()
        and index_path.parent == git_dir
        and index_path.name == request.dedicated_index_filename
        and not index_path.is_symlink()
    )
    index_present = index_path.is_file() and not index_path.is_symlink()
    sandbox_path_exact = bool(
        sandbox_path.parent == root
        and sandbox_path.name == request.sandbox_directory_name
        and not sandbox_path.is_symlink()
    )
    existed_before = sandbox_path.exists()
    before = {
        "dedicated_index": file_sha256(index_path),
        "canonical_index": file_sha256(canonical_index),
        "repository_root": repository_root_snapshot(root, request.sandbox_directory_name),
        **protected_git_snapshot(git_dir),
    }
    state = {
        "status": WORKTREE_REJECTED,
        "reason": "SANDBOX_WORKTREE_PRECONDITION_REJECTED",
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "marker_present": marker_present,
        "marker_exact": marker_exact,
        "index_path_exact": index_path_exact,
        "index_present": index_present,
        "sandbox_path_exact": sandbox_path_exact,
        "existed_before": existed_before,
        "present_after": existed_before,
        "files_exact": False,
        "modes_exact": False,
        "no_extra": False,
        "total_bytes": 0,
        "checkout_attempted": False,
        "checkout_succeeded": False,
        "reused": False,
        "write_performed": False,
        "receipts": [],
        "checks": {},
    }
    preconditions = all(
        (
            policy_valid,
            request_valid,
            entry_count_within_policy,
            paths_within_policy,
            upstream[0],
            upstream[2],
            upstream[3],
            executor_authorized,
            repository_path_allowed,
            marker_exact,
            index_path_exact,
            index_present,
            sandbox_path_exact,
        )
    )
    if preconditions and existed_before:
        (
            state["files_exact"],
            state["modes_exact"],
            state["no_extra"],
            state["total_bytes"],
        ) = inspect_sandbox(sandbox_path, request.tree_entries, policy.max_total_file_bytes)
        if all((state["files_exact"], state["modes_exact"], state["no_extra"])):
            state["status"] = WORKTREE_REUSED
            state["reason"] = "EXACT_SANDBOX_WORKING_TREE_ALREADY_PRESENT"
            state["reused"] = True
        else:
            state["reason"] = "EXISTING_SANDBOX_WORKING_TREE_MISMATCH"
    elif preconditions:
        state["checkout_attempted"] = True
        receipt = run_sandbox_checkout(
            root,
            index_path,
            sandbox_path,
            request.sandbox_directory_name,
            policy,
            git_executable=git_executable,
        )
        state["receipts"].append(receipt)
        state["checkout_succeeded"] = _command_ok(receipt, policy)
        state["write_performed"] = sandbox_path.exists()
        (
            state["files_exact"],
            state["modes_exact"],
            state["no_extra"],
            state["total_bytes"],
        ) = inspect_sandbox(sandbox_path, request.tree_entries, policy.max_total_file_bytes)
        if all(
            (
                state["checkout_succeeded"],
                state["write_performed"],
                state["files_exact"],
                state["modes_exact"],
                state["no_extra"],
            )
        ):
            state["status"] = WORKTREE_MATERIALIZED
            state["reason"] = "EXACT_INDEX_REFLECTED_IN_SANDBOX_WORKING_TREE"
        else:
            state["status"] = WORKTREE_ERROR
            state["reason"] = (
                "SANDBOX_WORKTREE_WRITE_POSTCONDITION_ERROR"
                if state["write_performed"]
                else "SANDBOX_WORKTREE_COMMAND_ERROR"
            )
    state["present_after"] = sandbox_path.is_dir() and not sandbox_path.is_symlink()
    after = {
        "dedicated_index": file_sha256(index_path),
        "canonical_index": file_sha256(canonical_index),
        "repository_root": repository_root_snapshot(root, request.sandbox_directory_name),
        **protected_git_snapshot(git_dir),
    }
    protected_unchanged = all(
        before[name] == after[name]
        for name in (
            "dedicated_index",
            "canonical_index",
            "repository_root",
            "objects",
            "references",
            "reflogs",
        )
    )
    if state["status"] in (WORKTREE_MATERIALIZED, WORKTREE_REUSED) and not protected_unchanged:
        state["status"] = WORKTREE_ERROR
        state["reason"] = "SANDBOX_WORKTREE_PROTECTED_SURFACE_CHANGED"
    state["checks"] = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "entry_count_within_policy": entry_count_within_policy,
        "paths_within_policy": paths_within_policy,
        "v122_result_accepted": upstream[2],
        "request_binding_exact": upstream[3],
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "sandbox_marker_exact": marker_exact,
        "dedicated_index_path_exact": index_path_exact,
        "sandbox_path_exact": sandbox_path_exact,
        "sandbox_files_exact": state["files_exact"],
        "sandbox_modes_exact": state["modes_exact"],
        "sandbox_has_no_extra_entries": state["no_extra"],
    }
    return build_sandbox_worktree_result(
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
    )
