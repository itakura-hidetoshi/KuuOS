#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_live_ref_cas_types_v1_18 import (
    LIVE_REF_CAS_COMMITTED,
    RepositoryCheckpointLiveRefCasResult,
)
from runtime.kuuos_repository_checkpoint_live_ref_cas_v1_18 import (
    repository_checkpoint_live_ref_cas_result_issues,
)
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_ERROR,
    OBJECT_MATERIALIZED,
    OBJECT_REJECTED,
    OBJECT_REUSED,
    SANDBOX_MARKER_FILENAME,
    RepositoryLiveObjectMaterializationPolicy,
    RepositoryLiveObjectMaterializationRequest,
    RepositoryLiveObjectMaterializationResult,
    repository_live_object_materialization_result_digest,
)
from runtime.v119_live_object_git_adapter import run_bounded_object_git_command
from runtime.v119_live_object_materialization_policy import (
    repository_live_object_materialization_policy_issues,
    repository_live_object_materialization_request_issues,
    repository_path_digest,
    git_blob_oid,
)
from runtime.v119_live_object_materialization_result import (
    repository_live_object_materialization_result_issues,
)


def execute_repository_live_object_materialization(
    request: RepositoryLiveObjectMaterializationRequest,
    v118_result: RepositoryCheckpointLiveRefCasResult,
    payload: bytes,
    policy: RepositoryLiveObjectMaterializationPolicy,
    *,
    git_executable: str = "git",
) -> RepositoryLiveObjectMaterializationResult:
    policy_valid = not repository_live_object_materialization_policy_issues(policy)
    request_valid = not repository_live_object_materialization_request_issues(request)
    payload_binding_exact = bool(
        len(payload) == request.payload_size_bytes
        and hashlib.sha256(payload).hexdigest() == request.payload_sha256
        and git_blob_oid(payload) == request.expected_blob_oid
        and len(payload) <= policy.max_payload_bytes
    )
    v118_valid = not repository_checkpoint_live_ref_cas_result_issues(v118_result)
    v118_committed = bool(
        v118_valid
        and v118_result.status == LIVE_REF_CAS_COMMITTED
        and v118_result.reference_cas_committed
        and v118_result.checkpoint_reference_write_performed
        and v118_result.live_repository_mutated
        and not v118_result.object_database_write_performed
        and not v118_result.index_write_performed
        and not v118_result.working_tree_write_performed
        and not v118_result.reflog_write_performed
    )
    resolved_root = Path(request.repository_path).expanduser().resolve()
    actual_path_digest = repository_path_digest(resolved_root)
    request_binding_exact = bool(
        request.v118_result_digest == v118_result.result_digest
        and request.repository_path_digest == actual_path_digest
        == v118_result.repository_path_digest
        and request.repository_id == v118_result.repository_id
        and request.git_dir_fingerprint == v118_result.git_dir_fingerprint
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

    preconditions = all(
        (
            policy_valid,
            request_valid,
            payload_binding_exact,
            v118_committed,
            request_binding_exact,
            executor_authorized,
            repository_path_allowed,
            sandbox_marker_present,
            sandbox_marker_exact,
        )
    )
    receipts = []
    sequence = 0
    command_error = False

    def run(arguments, stdin=b"", operation="observe", mutating=False):
        nonlocal sequence, command_error
        sequence += 1
        receipt, stdout, stderr = run_bounded_object_git_command(
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
            or receipt.return_code in (-124, -127)
            or not receipt.fixed_argument_shape
            or receipt.stdout_size_bytes > policy.max_output_bytes
            or receipt.stderr_size_bytes > policy.max_output_bytes
        ):
            command_error = True
        return receipt, stdout, stderr

    object_format_sha1 = False
    candidate_oid = ""
    candidate_oid_exact = False
    object_existed_before = False
    write_attempted = False
    write_succeeded = False

    if preconditions:
        format_receipt, format_stdout, _ = run(
            ("rev-parse", "--show-object-format"),
            operation="observe-object-format",
        )
        object_format_sha1 = bool(
            format_receipt.return_code == 0
            and format_stdout.strip() == b"sha1"
        )
        candidate_receipt, candidate_stdout, _ = run(
            ("hash-object", "--stdin"),
            stdin=payload,
            operation="calculate-blob-oid",
        )
        candidate_oid = candidate_stdout.decode(
            "ascii", errors="ignore"
        ).strip().lower()
        candidate_oid_exact = bool(
            candidate_receipt.return_code == 0
            and candidate_oid == request.expected_blob_oid
        )
        if object_format_sha1 and candidate_oid_exact and not command_error:
            exists_receipt, _, _ = run(
                ("cat-file", "-e", request.expected_blob_oid),
                operation="observe-object-before",
            )
            object_existed_before = exists_receipt.return_code == 0
            if exists_receipt.return_code == 1:
                write_attempted = True
                write_receipt, write_stdout, _ = run(
                    ("hash-object", "-w", "--stdin"),
                    stdin=payload,
                    operation="materialize-blob-object",
                    mutating=True,
                )
                write_succeeded = bool(
                    write_receipt.return_code == 0
                    and write_stdout.decode(
                        "ascii", errors="ignore"
                    ).strip().lower() == request.expected_blob_oid
                )
            elif exists_receipt.return_code != 0:
                command_error = True

    object_present_after = False
    observed_type = ""
    observed_size = -1
    observed_payload_sha256 = ""
    if (
        preconditions
        and object_format_sha1
        and candidate_oid_exact
        and not command_error
        and (object_existed_before or write_succeeded)
    ):
        present_receipt, _, _ = run(
            ("cat-file", "-e", request.expected_blob_oid),
            operation="observe-object-after",
        )
        object_present_after = present_receipt.return_code == 0
        type_receipt, type_stdout, _ = run(
            ("cat-file", "-t", request.expected_blob_oid),
            operation="verify-object-type",
        )
        observed_type = type_stdout.decode("ascii", errors="ignore").strip()
        size_receipt, size_stdout, _ = run(
            ("cat-file", "-s", request.expected_blob_oid),
            operation="verify-object-size",
        )
        try:
            observed_size = int(size_stdout.strip())
        except ValueError:
            observed_size = -1
        content_receipt, content_stdout, _ = run(
            ("cat-file", "blob", request.expected_blob_oid),
            operation="verify-object-content",
        )
        observed_payload_sha256 = hashlib.sha256(content_stdout).hexdigest()
        if any(
            receipt.return_code != 0
            for receipt in (
                present_receipt,
                type_receipt,
                size_receipt,
                content_receipt,
            )
        ):
            command_error = True

    object_type_blob = observed_type == "blob"
    object_size_exact = observed_size == request.payload_size_bytes
    object_content_exact = observed_payload_sha256 == request.payload_sha256
    write_performed = bool(
        write_attempted and write_succeeded and not object_existed_before
    )
    exact_reuse = bool(
        object_existed_before
        and object_present_after
        and object_type_blob
        and object_size_exact
        and object_content_exact
    )
    materialized = bool(
        write_performed
        and object_present_after
        and object_type_blob
        and object_size_exact
        and object_content_exact
        and not command_error
    )
    reused = bool(
        exact_reuse
        and policy.allow_exact_existing_object_reuse
        and not command_error
    )
    if materialized:
        status = OBJECT_MATERIALIZED
        reason = "LIVE_BLOB_OBJECT_MATERIALIZED_AND_VERIFIED"
    elif reused:
        status = OBJECT_REUSED
        reason = "EXACT_EXISTING_BLOB_OBJECT_REUSED"
    elif write_attempted or command_error:
        status = OBJECT_ERROR
        reason = "LIVE_BLOB_OBJECT_COMMAND_OR_POSTCONDITION_ERROR"
    else:
        status = OBJECT_REJECTED
        reason = "LIVE_BLOB_OBJECT_PRECONDITION_REJECTED"

    result = RepositoryLiveObjectMaterializationResult(
        operation_id=request.operation_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        v118_result_digest=v118_result.result_digest,
        repository_path_digest=actual_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        executor_id=request.executor_id,
        payload_sha256=request.payload_sha256,
        payload_size_bytes=request.payload_size_bytes,
        expected_blob_oid=request.expected_blob_oid,
        candidate_blob_oid=candidate_oid,
        observed_object_type=observed_type,
        observed_object_size_bytes=observed_size,
        observed_payload_sha256=observed_payload_sha256,
        policy_valid=policy_valid,
        request_valid=request_valid,
        payload_binding_exact=payload_binding_exact,
        v118_result_valid=v118_valid,
        v118_result_committed=v118_committed,
        request_binding_exact=request_binding_exact,
        executor_authorized=executor_authorized,
        repository_path_allowed=repository_path_allowed,
        sandbox_marker_present=sandbox_marker_present,
        sandbox_marker_exact=sandbox_marker_exact,
        object_format_sha1=object_format_sha1,
        candidate_oid_exact=candidate_oid_exact,
        object_existed_before=object_existed_before,
        object_present_after=object_present_after,
        object_type_blob=object_type_blob,
        object_size_exact=object_size_exact,
        object_content_exact=object_content_exact,
        write_command_attempted=write_attempted,
        write_command_succeeded=write_succeeded,
        object_database_write_performed=write_performed,
        exact_existing_object_reused=exact_reuse,
        live_git_command_invoked=bool(receipts),
        live_repository_mutated=write_performed,
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
            "payload_binding_exact": payload_binding_exact,
            "v118_result_valid": v118_valid,
            "v118_result_committed": v118_committed,
            "request_binding_exact": request_binding_exact,
            "executor_authorized": executor_authorized,
            "repository_path_allowed": repository_path_allowed,
            "sandbox_marker_present": sandbox_marker_present,
            "sandbox_marker_exact": sandbox_marker_exact,
            "object_format_sha1": object_format_sha1,
            "candidate_oid_exact": candidate_oid_exact,
            "object_present_after": object_present_after,
            "object_type_blob": object_type_blob,
            "object_size_exact": object_size_exact,
            "object_content_exact": object_content_exact,
        },
        evidence_digests={
            "v118_result": v118_result.result_digest,
            "v119_policy": policy.policy_digest,
            "v119_request": request.request_digest,
            "repository_path": actual_path_digest,
            "payload": request.payload_sha256,
            "sandbox_marker": canonical_digest(
                {"marker": marker_content if sandbox_marker_exact else ""}
            ),
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_live_object_materialization_result_digest(result),
    )
    issues = repository_live_object_materialization_result_issues(result)
    if issues:
        raise ValueError(f"live_object_materialization_result_invalid:{issues[0]}")
    return result
