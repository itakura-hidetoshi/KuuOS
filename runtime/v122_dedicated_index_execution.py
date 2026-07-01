#!/usr/bin/env python3
from pathlib import Path

from runtime.kuuos_repository_dedicated_index_types_v1_22 import (
    INDEX_ERROR,
    INDEX_MATERIALIZED,
    INDEX_REJECTED,
    INDEX_REUSED,
    SANDBOX_MARKER_FILENAME,
)
from runtime.v122_dedicated_index_git_adapter import (
    dedicated_index_path,
    run_dedicated_index_git_command,
)
from runtime.v122_dedicated_index_policy import (
    repository_dedicated_index_policy_issues,
    repository_dedicated_index_request_issues,
    repository_path_digest,
)
from runtime.v122_dedicated_index_result_builder import build_dedicated_index_result
from runtime.v122_dedicated_index_validation import (
    file_sha256,
    parse_index_entries,
    validate_upstream_binding,
)


def _command_ok(receipt, policy) -> bool:
    return bool(
        receipt.return_code == 0
        and not receipt.timed_out
        and receipt.stdout_size_bytes <= policy.max_output_bytes
        and receipt.stderr_size_bytes <= policy.max_output_bytes
    )


def execute_repository_dedicated_index(
    request,
    v120_request,
    v120_result,
    v121_result,
    policy,
    *,
    git_executable: str = "git",
):
    if git_executable != "git":
        raise ValueError("v122_git_executable_not_allowed")
    root = Path(request.repository_path).expanduser().resolve()
    actual_repository_path_digest = repository_path_digest(root)
    git_dir = root / ".git"
    index_path = dedicated_index_path(root, request.dedicated_index_filename)
    canonical_index = git_dir / "index"
    marker = git_dir / SANDBOX_MARKER_FILENAME
    upstream = validate_upstream_binding(
        request, v120_request, v120_result, v121_result
    )
    policy_valid = not repository_dedicated_index_policy_issues(policy)
    request_valid = not repository_dedicated_index_request_issues(request)
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
    path_exact = bool(
        actual_repository_path_digest == request.repository_path_digest
        and git_dir.is_dir()
        and not git_dir.is_symlink()
        and index_path.parent == git_dir
        and index_path.name == request.dedicated_index_filename
        and not index_path.is_symlink()
    )
    existed_before = index_path.is_file() and not index_path.is_symlink()
    canonical_before = file_sha256(canonical_index)
    state = {
        "status": INDEX_REJECTED,
        "reason": "DEDICATED_INDEX_PRECONDITION_REJECTED",
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "marker_present": marker_present,
        "marker_exact": marker_exact,
        "path_exact": path_exact,
        "existed_before": existed_before,
        "present_after": existed_before,
        "entries_exact": False,
        "read_attempted": False,
        "read_succeeded": False,
        "verify_attempted": False,
        "verify_succeeded": False,
        "reused": False,
        "write_performed": False,
        "receipts": [],
        "checks": {},
    }
    preconditions = all(
        (
            policy_valid,
            request_valid,
            upstream[0],
            upstream[2],
            upstream[4],
            upstream[5],
            executor_authorized,
            repository_path_allowed,
            marker_exact,
            path_exact,
        )
    )
    if preconditions and existed_before:
        state["verify_attempted"] = True
        receipt, stdout, _ = run_dedicated_index_git_command(
            root,
            index_path,
            ("ls-files", "--stage", "-z"),
            policy,
            sequence_number=1,
            operation="verify-index",
            mutating=False,
            git_executable=git_executable,
        )
        state["receipts"].append(receipt)
        state["verify_succeeded"] = _command_ok(receipt, policy)
        parsed = parse_index_entries(stdout) if state["verify_succeeded"] else None
        state["entries_exact"] = parsed == request.tree_entries
        if state["entries_exact"]:
            state["status"] = INDEX_REUSED
            state["reason"] = "EXACT_DEDICATED_INDEX_ALREADY_PRESENT"
            state["reused"] = True
        else:
            state["reason"] = "EXISTING_DEDICATED_INDEX_MISMATCH"
    elif preconditions:
        state["read_attempted"] = True
        receipt, _, _ = run_dedicated_index_git_command(
            root,
            index_path,
            ("read-tree", request.expected_tree_oid),
            policy,
            sequence_number=1,
            operation="read-tree",
            mutating=True,
            git_executable=git_executable,
        )
        state["receipts"].append(receipt)
        state["read_succeeded"] = _command_ok(receipt, policy)
        state["write_performed"] = index_path.is_file() and not index_path.is_symlink()
        if state["read_succeeded"] and state["write_performed"]:
            state["verify_attempted"] = True
            verify_receipt, stdout, _ = run_dedicated_index_git_command(
                root,
                index_path,
                ("ls-files", "--stage", "-z"),
                policy,
                sequence_number=2,
                operation="verify-index",
                mutating=False,
                git_executable=git_executable,
            )
            state["receipts"].append(verify_receipt)
            state["verify_succeeded"] = _command_ok(verify_receipt, policy)
            parsed = parse_index_entries(stdout) if state["verify_succeeded"] else None
            state["entries_exact"] = parsed == request.tree_entries
        if all(
            (
                state["read_succeeded"],
                state["write_performed"],
                state["verify_succeeded"],
                state["entries_exact"],
            )
        ):
            state["status"] = INDEX_MATERIALIZED
            state["reason"] = "EXACT_TREE_LOADED_INTO_DEDICATED_INDEX"
        else:
            state["status"] = INDEX_ERROR
            state["reason"] = (
                "DEDICATED_INDEX_WRITE_POSTCONDITION_ERROR"
                if state["write_performed"]
                else "DEDICATED_INDEX_COMMAND_ERROR"
            )
    state["present_after"] = index_path.is_file() and not index_path.is_symlink()
    canonical_after = file_sha256(canonical_index)
    if state["status"] in (INDEX_MATERIALIZED, INDEX_REUSED) and canonical_before != canonical_after:
        state["status"] = INDEX_ERROR
        state["reason"] = "CANONICAL_INDEX_POSTCONDITION_ERROR"
    state["checks"] = {
        "policy_valid": policy_valid,
        "request_valid": request_valid,
        "v120_result_accepted": upstream[2],
        "v121_result_accepted": upstream[4],
        "request_binding_exact": upstream[5],
        "executor_authorized": executor_authorized,
        "repository_path_allowed": repository_path_allowed,
        "sandbox_marker_exact": marker_exact,
        "dedicated_index_path_exact": path_exact,
        "index_entries_exact": state["entries_exact"],
    }
    return build_dedicated_index_result(
        request,
        v120_request,
        v120_result,
        v121_result,
        policy,
        index_path,
        canonical_before,
        canonical_after,
        upstream,
        state,
    )
