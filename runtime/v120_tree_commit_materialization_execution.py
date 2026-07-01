#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import re

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_MATERIALIZED,
    OBJECT_REUSED,
    RepositoryLiveObjectMaterializationResult,
)
from runtime.kuuos_repository_tree_commit_materialization_types_v1_20 import (
    SANDBOX_MARKER_FILENAME,
    TREE_COMMIT_ERROR,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
    RepositoryTreeCommitMaterializationPolicy,
    RepositoryTreeCommitMaterializationRequest,
    RepositoryTreeCommitMaterializationResult,
    repository_tree_commit_materialization_result_digest,
)
from runtime.v119_live_object_materialization_result import (
    repository_live_object_materialization_result_issues,
)
from runtime.v120_tree_commit_git_adapter import (
    run_bounded_tree_commit_git_command,
)
from runtime.v120_tree_commit_materialization_policy import (
    git_commit_oid,
    git_tree_oid,
    limited_commit_payload,
    limited_tree_mktree_input,
    limited_tree_payload,
    repository_path_digest,
    repository_tree_commit_materialization_policy_issues,
    repository_tree_commit_materialization_request_issues,
)
from runtime.v120_tree_commit_materialization_result import (
    repository_tree_commit_materialization_result_issues,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def execute_repository_tree_commit_materialization(
    request: RepositoryTreeCommitMaterializationRequest,
    v119_result: RepositoryLiveObjectMaterializationResult,
    message: str,
    policy: RepositoryTreeCommitMaterializationPolicy,
    *,
    git_executable: str = "git",
) -> RepositoryTreeCommitMaterializationResult:
    policy_valid = not repository_tree_commit_materialization_policy_issues(policy)
    request_valid = not repository_tree_commit_materialization_request_issues(request)
    v119_valid = not repository_live_object_materialization_result_issues(v119_result)
    v119_accepted = bool(
        v119_valid
        and v119_result.status in (OBJECT_MATERIALIZED, OBJECT_REUSED)
        and v119_result.object_present_after
        and v119_result.object_type_blob
        and v119_result.object_size_exact
        and v119_result.object_content_exact
        and not v119_result.reference_write_performed
        and not v119_result.index_write_performed
        and not v119_result.working_tree_write_performed
        and not v119_result.reflog_write_performed
        and not v119_result.push_performed
        and not v119_result.signing_performed
    )
    resolved_root = Path(request.repository_path).expanduser().resolve()
    actual_path_digest = repository_path_digest(resolved_root)
    request_binding_exact = bool(
        request.v119_result_digest == v119_result.result_digest
        and request.repository_path_digest == actual_path_digest
        == v119_result.repository_path_digest
        and request.repository_id == v119_result.repository_id
        and request.git_dir_fingerprint == v119_result.git_dir_fingerprint
        and any(
            entry.blob_oid == v119_result.expected_blob_oid
            for entry in request.tree_entries
        )
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids
    repository_path_allowed = bool(
        resolved_root.exists()
        and resolved_root.is_dir()
        and actual_path_digest in policy.allowed_repository_path_digests
    )
    git_dir = resolved_root / ".git"
    marker_path = git_dir / SANDBOX_MARKER_FILENAME
    sandbox_marker_present = bool(
        git_dir.is_dir()
        and marker_path.exists()
        and marker_path.is_file()
        and not marker_path.is_symlink()
    )
    marker_content = ""
    if sandbox_marker_present:
        try:
            if marker_path.stat().st_size <= 256:
                marker_content = marker_path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError):
            marker_content = ""
    sandbox_marker_exact = marker_content == request.sandbox_marker_token

    try:
        message_bytes = message.rstrip("\n").encode("utf-8") + b"\n"
        commit_payload = limited_commit_payload(
            tree_oid=request.expected_tree_oid,
            parent_commit_oid=request.parent_commit_oid,
            author_name=request.author_name,
            author_email=request.author_email,
            committer_name=request.committer_name,
            committer_email=request.committer_email,
            commit_epoch_seconds=request.commit_epoch_seconds,
            commit_timezone=request.commit_timezone,
            message=message,
        )
    except (UnicodeError, ValueError):
        message_bytes = b""
        commit_payload = b""
    tree_payload = limited_tree_payload(request.tree_entries)
    tree_binding_exact = bool(
        len(request.tree_entries) <= policy.max_tree_entries
        and all(
            len(entry.path.encode("utf-8")) <= policy.max_tree_path_bytes
            for entry in request.tree_entries
        )
        and git_tree_oid(request.tree_entries) == request.expected_tree_oid
    )
    commit_binding_exact = bool(
        message_bytes
        and len(message_bytes) == request.commit_message_size_bytes
        and len(message_bytes) <= policy.max_commit_message_bytes
        and hashlib.sha256(message_bytes).hexdigest()
        == request.commit_message_sha256
        and git_commit_oid(
            tree_oid=request.expected_tree_oid,
            parent_commit_oid=request.parent_commit_oid,
            author_name=request.author_name,
            author_email=request.author_email,
            committer_name=request.committer_name,
            committer_email=request.committer_email,
            commit_epoch_seconds=request.commit_epoch_seconds,
            commit_timezone=request.commit_timezone,
            message=message,
        )
        == request.expected_commit_oid
    )

    preconditions = all(
        (
            policy_valid,
            request_valid,
            v119_accepted,
            request_binding_exact,
            executor_authorized,
            repository_path_allowed,
            sandbox_marker_present,
            sandbox_marker_exact,
            tree_binding_exact,
            commit_binding_exact,
        )
    )
    receipts = []
    sequence = 0
    command_error = False

    def run(arguments, stdin=b"", operation="observe", mutating=False):
        nonlocal sequence, command_error
        sequence += 1
        receipt, stdout, stderr = run_bounded_tree_commit_git_command(
            resolved_root,
            arguments,
            stdin,
            policy,
            sequence_number=sequence,
            operation=operation,
            mutating=mutating,
            git_executable=git_executable,
        )
        receipts.append(receipt)
        if (
            receipt.timed_out
            or receipt.return_code in (-124, -127, -126)
            or not receipt.fixed_argument_shape
            or receipt.stdout_size_bytes > policy.max_output_bytes
            or receipt.stderr_size_bytes > policy.max_output_bytes
        ):
            command_error = True
        return receipt, stdout, stderr

    object_format_sha1 = False
    referenced_blobs_exact = False
    parent_commit_exact = False
    candidate_tree_oid = request.expected_tree_oid if tree_binding_exact else ""
    candidate_commit_oid = ""
    tree_existed_before = False
    commit_existed_before = False
    tree_write_attempted = False
    tree_write_succeeded = False
    commit_write_attempted = False
    commit_write_succeeded = False

    if preconditions:
        format_receipt, format_stdout, _ = run(
            ("rev-parse", "--show-object-format"),
            operation="observe-object-format",
        )
        object_format_sha1 = bool(
            format_receipt.return_code == 0 and format_stdout.strip() == b"sha1"
        )
        if object_format_sha1 and not command_error:
            referenced_blobs_exact = True
            for index, entry in enumerate(request.tree_entries):
                exists_receipt, _, _ = run(
                    ("cat-file", "-e", entry.blob_oid),
                    operation=f"observe-blob-{index}",
                )
                if exists_receipt.return_code == 1:
                    referenced_blobs_exact = False
                    break
                if exists_receipt.return_code != 0:
                    referenced_blobs_exact = False
                    command_error = True
                    break
                type_receipt, type_stdout, _ = run(
                    ("cat-file", "-t", entry.blob_oid),
                    operation=f"verify-blob-type-{index}",
                )
                if type_receipt.return_code != 0 or type_stdout.strip() != b"blob":
                    referenced_blobs_exact = False
                    if type_receipt.return_code != 0:
                        command_error = True
                    break
            parent_exists_receipt, _, _ = run(
                ("cat-file", "-e", request.parent_commit_oid),
                operation="observe-parent-commit",
            )
            if parent_exists_receipt.return_code == 0:
                parent_type_receipt, parent_type_stdout, _ = run(
                    ("cat-file", "-t", request.parent_commit_oid),
                    operation="verify-parent-commit-type",
                )
                parent_commit_exact = bool(
                    parent_type_receipt.return_code == 0
                    and parent_type_stdout.strip() == b"commit"
                )
                if parent_type_receipt.return_code != 0:
                    command_error = True
            elif parent_exists_receipt.return_code != 1:
                command_error = True

        if referenced_blobs_exact and parent_commit_exact and not command_error:
            candidate_receipt, candidate_stdout, _ = run(
                ("hash-object", "-t", "commit", "--stdin"),
                stdin=commit_payload,
                operation="calculate-commit-oid",
            )
            candidate_commit_oid = candidate_stdout.decode(
                "ascii", errors="ignore"
            ).strip().lower()
            commit_binding_exact = bool(
                commit_binding_exact
                and candidate_receipt.return_code == 0
                and candidate_commit_oid == request.expected_commit_oid
            )
            if candidate_receipt.return_code != 0:
                command_error = True

        if commit_binding_exact and referenced_blobs_exact and parent_commit_exact and not command_error:
            tree_exists_receipt, _, _ = run(
                ("cat-file", "-e", request.expected_tree_oid),
                operation="observe-tree-before",
            )
            tree_existed_before = tree_exists_receipt.return_code == 0
            if tree_exists_receipt.return_code not in (0, 1):
                command_error = True
            commit_exists_receipt, _, _ = run(
                ("cat-file", "-e", request.expected_commit_oid),
                operation="observe-commit-before",
            )
            commit_existed_before = commit_exists_receipt.return_code == 0
            if commit_exists_receipt.return_code not in (0, 1):
                command_error = True

        if not tree_existed_before and not command_error and referenced_blobs_exact and parent_commit_exact and commit_binding_exact:
            tree_write_attempted = True
            tree_write_receipt, tree_write_stdout, _ = run(
                ("mktree",),
                stdin=limited_tree_mktree_input(request.tree_entries),
                operation="materialize-tree-object",
                mutating=True,
            )
            written_tree_oid = tree_write_stdout.decode(
                "ascii", errors="ignore"
            ).strip().lower()
            tree_write_succeeded = bool(
                tree_write_receipt.return_code == 0
                and _HEX40.fullmatch(written_tree_oid)
            )
            if not tree_write_succeeded or written_tree_oid != request.expected_tree_oid:
                command_error = True

    tree_present_after = False
    tree_type_exact = False
    tree_content_exact = False
    if preconditions and object_format_sha1 and referenced_blobs_exact and parent_commit_exact and commit_binding_exact and not command_error:
        tree_after_receipt, _, _ = run(
            ("cat-file", "-e", request.expected_tree_oid),
            operation="observe-tree-after",
        )
        tree_present_after = tree_after_receipt.return_code == 0
        tree_type_receipt, tree_type_stdout, _ = run(
            ("cat-file", "-t", request.expected_tree_oid),
            operation="verify-tree-type",
        )
        tree_type_exact = bool(
            tree_type_receipt.return_code == 0 and tree_type_stdout.strip() == b"tree"
        )
        tree_content_receipt, tree_content_stdout, _ = run(
            ("cat-file", "tree", request.expected_tree_oid),
            operation="verify-tree-content",
        )
        tree_content_exact = bool(
            tree_content_receipt.return_code == 0 and tree_content_stdout == tree_payload
        )
        if any(
            receipt.return_code != 0
            for receipt in (
                tree_after_receipt,
                tree_type_receipt,
                tree_content_receipt,
            )
        ):
            command_error = True

    if (
        tree_present_after
        and tree_type_exact
        and tree_content_exact
        and not commit_existed_before
        and not command_error
    ):
        commit_write_attempted = True
        commit_write_receipt, commit_write_stdout, _ = run(
            ("hash-object", "-t", "commit", "-w", "--stdin"),
            stdin=commit_payload,
            operation="materialize-commit-object",
            mutating=True,
        )
        written_commit_oid = commit_write_stdout.decode(
            "ascii", errors="ignore"
        ).strip().lower()
        commit_write_succeeded = bool(
            commit_write_receipt.return_code == 0
            and _HEX40.fullmatch(written_commit_oid)
        )
        if not commit_write_succeeded or written_commit_oid != request.expected_commit_oid:
            command_error = True

    commit_present_after = False
    commit_type_exact = False
    commit_content_exact = False
    if (
        preconditions
        and object_format_sha1
        and tree_present_after
        and tree_type_exact
        and tree_content_exact
        and (commit_existed_before or commit_write_succeeded)
        and not command_error
    ):
        commit_after_receipt, _, _ = run(
            ("cat-file", "-e", request.expected_commit_oid),
            operation="observe-commit-after",
        )
        commit_present_after = commit_after_receipt.return_code == 0
        commit_type_receipt, commit_type_stdout, _ = run(
            ("cat-file", "-t", request.expected_commit_oid),
            operation="verify-commit-type",
        )
        commit_type_exact = bool(
            commit_type_receipt.return_code == 0
            and commit_type_stdout.strip() == b"commit"
        )
        commit_content_receipt, commit_content_stdout, _ = run(
            ("cat-file", "commit", request.expected_commit_oid),
            operation="verify-commit-content",
        )
        commit_content_exact = bool(
            commit_content_receipt.return_code == 0
            and commit_content_stdout == commit_payload
        )
        if any(
            receipt.return_code != 0
            for receipt in (
                commit_after_receipt,
                commit_type_receipt,
                commit_content_receipt,
            )
        ):
            command_error = True

    tree_write_performed = bool(
        tree_write_attempted and tree_write_succeeded and not tree_existed_before
    )
    commit_write_performed = bool(
        commit_write_attempted and commit_write_succeeded and not commit_existed_before
    )
    any_write_performed = tree_write_performed or commit_write_performed
    exact_tree_reuse = bool(
        tree_existed_before
        and tree_present_after
        and tree_type_exact
        and tree_content_exact
    )
    exact_commit_reuse = bool(
        commit_existed_before
        and commit_present_after
        and commit_type_exact
        and commit_content_exact
    )
    postconditions = all(
        (
            tree_present_after,
            commit_present_after,
            tree_type_exact,
            commit_type_exact,
            tree_content_exact,
            commit_content_exact,
        )
    )
    materialized = bool(any_write_performed and postconditions and not command_error)
    reused = bool(
        exact_tree_reuse
        and exact_commit_reuse
        and policy.allow_exact_existing_tree_reuse
        and policy.allow_exact_existing_commit_reuse
        and not any_write_performed
        and not command_error
    )
    if materialized:
        status = TREE_COMMIT_MATERIALIZED
        reason = "LIMITED_TREE_COMMIT_OBJECTS_MATERIALIZED_AND_VERIFIED"
    elif reused:
        status = TREE_COMMIT_REUSED
        reason = "EXACT_EXISTING_TREE_COMMIT_OBJECTS_REUSED"
    elif any_write_performed or command_error:
        status = TREE_COMMIT_ERROR
        reason = "LIMITED_TREE_COMMIT_COMMAND_OR_POSTCONDITION_ERROR"
    else:
        status = TREE_COMMIT_REJECTED
        reason = "LIMITED_TREE_COMMIT_PRECONDITION_REJECTED"

    result = RepositoryTreeCommitMaterializationResult(
        operation_id=request.operation_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        v119_result_digest=v119_result.result_digest,
        repository_path_digest=actual_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        executor_id=request.executor_id,
        expected_tree_oid=request.expected_tree_oid,
        candidate_tree_oid=candidate_tree_oid,
        expected_commit_oid=request.expected_commit_oid,
        candidate_commit_oid=candidate_commit_oid,
        parent_commit_oid=request.parent_commit_oid,
        policy_valid=policy_valid,
        request_valid=request_valid,
        v119_result_valid=v119_valid,
        v119_result_accepted=v119_accepted,
        request_binding_exact=request_binding_exact,
        executor_authorized=executor_authorized,
        repository_path_allowed=repository_path_allowed,
        sandbox_marker_present=sandbox_marker_present,
        sandbox_marker_exact=sandbox_marker_exact,
        object_format_sha1=object_format_sha1,
        tree_binding_exact=tree_binding_exact,
        commit_binding_exact=commit_binding_exact,
        referenced_blobs_exact=referenced_blobs_exact,
        parent_commit_exact=parent_commit_exact,
        tree_existed_before=tree_existed_before,
        commit_existed_before=commit_existed_before,
        tree_present_after=tree_present_after,
        commit_present_after=commit_present_after,
        tree_type_exact=tree_type_exact,
        commit_type_exact=commit_type_exact,
        tree_content_exact=tree_content_exact,
        commit_content_exact=commit_content_exact,
        tree_write_command_attempted=tree_write_attempted,
        tree_write_command_succeeded=tree_write_succeeded,
        commit_write_command_attempted=commit_write_attempted,
        commit_write_command_succeeded=commit_write_succeeded,
        tree_object_database_write_performed=tree_write_performed,
        commit_object_database_write_performed=commit_write_performed,
        object_database_write_performed=any_write_performed,
        exact_existing_tree_reused=exact_tree_reuse,
        exact_existing_commit_reused=exact_commit_reuse,
        live_git_command_invoked=bool(receipts),
        live_repository_mutated=any_write_performed,
        reference_write_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        reflog_write_performed=False,
        push_performed=False,
        signing_performed=False,
        command_receipts=tuple(receipts),
        checks={
            "policy_valid": policy_valid,
            "request_valid": request_valid,
            "v119_result_valid": v119_valid,
            "v119_result_accepted": v119_accepted,
            "request_binding_exact": request_binding_exact,
            "executor_authorized": executor_authorized,
            "repository_path_allowed": repository_path_allowed,
            "sandbox_marker_present": sandbox_marker_present,
            "sandbox_marker_exact": sandbox_marker_exact,
            "object_format_sha1": object_format_sha1,
            "tree_binding_exact": tree_binding_exact,
            "commit_binding_exact": commit_binding_exact,
            "referenced_blobs_exact": referenced_blobs_exact,
            "parent_commit_exact": parent_commit_exact,
            "tree_present_after": tree_present_after,
            "commit_present_after": commit_present_after,
            "tree_type_exact": tree_type_exact,
            "commit_type_exact": commit_type_exact,
            "tree_content_exact": tree_content_exact,
            "commit_content_exact": commit_content_exact,
        },
        evidence_digests={
            "v119_result": v119_result.result_digest,
            "v120_policy": policy.policy_digest,
            "v120_request": request.request_digest,
            "repository_path": actual_path_digest,
            "tree_payload": hashlib.sha256(tree_payload).hexdigest(),
            "commit_payload": hashlib.sha256(commit_payload).hexdigest(),
            "sandbox_marker": canonical_digest(
                {"marker": marker_content if sandbox_marker_exact else ""}
            ),
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_tree_commit_materialization_result_digest(result),
    )
    issues = repository_tree_commit_materialization_result_issues(result)
    if issues:
        raise ValueError(f"tree_commit_materialization_result_invalid:{issues[0]}")
    return result
