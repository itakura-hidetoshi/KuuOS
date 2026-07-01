#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_bounded_tree_commit_types_v1_20 import (
    SANDBOX_MARKER_FILENAME,
    TREE_COMMIT_ERROR,
    TREE_COMMIT_MATERIALIZED,
    TREE_COMMIT_REJECTED,
    TREE_COMMIT_REUSED,
    RepositoryBoundedTreeCommitPolicy,
    RepositoryBoundedTreeCommitRequest,
    RepositoryBoundedTreeCommitResult,
    repository_bounded_tree_commit_result_digest,
)
from runtime.kuuos_repository_commit_candidate_strict_v0_93 import (
    repository_commit_candidate_certificate_issues,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    CANDIDATE_CERTIFIED,
    GITLINK_MODE,
    TREE_MODE,
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_live_object_materialization_types_v1_19 import (
    OBJECT_MATERIALIZED,
    OBJECT_REUSED,
    RepositoryLiveObjectMaterializationResult,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot
from runtime.v119_live_object_materialization_result import (
    repository_live_object_materialization_result_issues,
)
from runtime.v120_bounded_tree_commit_git_adapter import (
    run_bounded_tree_commit_git_command,
)
from runtime.v120_bounded_tree_commit_policy import (
    commit_candidate_payload,
    git_object_oid,
    repository_bounded_tree_commit_policy_issues,
    repository_bounded_tree_commit_request_issues,
    repository_path_digest,
    tree_candidate_payload,
    unique_tree_candidates_in_write_order,
)
from runtime.v120_bounded_tree_commit_result import (
    repository_bounded_tree_commit_result_issues,
)


def execute_repository_bounded_tree_commit(
    request: RepositoryBoundedTreeCommitRequest,
    candidate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    v119_results: tuple[RepositoryLiveObjectMaterializationResult, ...],
    policy: RepositoryBoundedTreeCommitPolicy,
    *,
    git_executable: str = "git",
) -> RepositoryBoundedTreeCommitResult:
    policy_valid = not repository_bounded_tree_commit_policy_issues(policy)
    request_valid = not repository_bounded_tree_commit_request_issues(request)
    candidate_issues = repository_commit_candidate_certificate_issues(
        candidate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
    )
    candidate_valid = bool(
        not candidate_issues
        and candidate.status == CANDIDATE_CERTIFIED
        and not candidate.object_database_write_performed
        and not candidate.index_write_performed
        and not candidate.working_tree_write_performed
        and not candidate.commit_created
        and not candidate.reference_mutated
        and not candidate.signing_performed
    )
    try:
        trees = unique_tree_candidates_in_write_order(candidate)
        tree_payload_by_oid = {
            tree.git_tree_oid: tree_candidate_payload(tree) for tree in trees
        }
        tree_payloads_exact = bool(
            trees
            and all(
                git_object_oid("tree", payload) == oid
                for oid, payload in tree_payload_by_oid.items()
            )
        )
    except (ValueError, UnicodeError):
        trees = ()
        tree_payload_by_oid = {}
        tree_payloads_exact = False
    commit_payload = commit_candidate_payload(candidate)
    commit_payload_exact = bool(
        hashlib.sha256(commit_payload).hexdigest() == candidate.commit_payload_digest
        and git_object_oid("commit", commit_payload) == candidate.candidate_commit_oid
    )
    expected_tree_oids = tuple(sorted(tree_payload_by_oid))
    total_payload_bytes = sum(len(payload) for payload in tree_payload_by_oid.values()) + len(
        commit_payload
    )
    payloads_within_policy = bool(
        len(trees) <= policy.max_tree_count
        and total_payload_bytes <= policy.max_total_payload_bytes
    )

    resolved_root = Path(request.repository_path).expanduser().resolve()
    actual_path_digest = repository_path_digest(resolved_root)
    request_binding_exact = bool(
        request.repository_path == str(resolved_root)
        and request.repository_path_digest == actual_path_digest
        and request.candidate_certificate_digest == candidate.certificate_digest
        and request.expected_tree_oids == expected_tree_oids
        and request.expected_root_tree_oid == candidate.root_tree_oid
        and request.expected_commit_oid == candidate.candidate_commit_oid
        and request.v119_result_digests
        == tuple(sorted(result.result_digest for result in v119_results))
    )
    v119_results_valid = bool(
        v119_results
        and all(
            not repository_live_object_materialization_result_issues(result)
            and result.status in (OBJECT_MATERIALIZED, OBJECT_REUSED)
            and result.object_present_after
            and result.object_type_blob
            and result.object_size_exact
            and result.object_content_exact
            and result.repository_path_digest == actual_path_digest
            and result.repository_id == request.repository_id
            and result.git_dir_fingerprint == request.git_dir_fingerprint
            and not result.reference_write_performed
            and not result.index_write_performed
            and not result.working_tree_write_performed
            and not result.reflog_write_performed
            and not result.push_performed
            and not result.signing_performed
            for result in v119_results
        )
    )
    candidate_blob_oids = {blob.git_blob_oid for blob in candidate.blob_candidates}
    result_blob_oids = {result.expected_blob_oid for result in v119_results}
    blob_result_coverage_exact = candidate_blob_oids == result_blob_oids
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

    leaf_expectations: dict[str, str] = {}
    leaf_shape_valid = True
    for tree in trees:
        for mode, oid in zip(tree.entry_modes, tree.entry_oids):
            if mode == TREE_MODE:
                continue
            expected_type = "commit" if mode == GITLINK_MODE else "blob"
            previous = leaf_expectations.get(oid)
            if previous is not None and previous != expected_type:
                leaf_shape_valid = False
            leaf_expectations[oid] = expected_type
    tree_payloads_exact = tree_payloads_exact and leaf_shape_valid

    preconditions = all(
        (
            policy_valid,
            request_valid,
            candidate_valid,
            request_binding_exact,
            v119_results_valid,
            blob_result_coverage_exact,
            executor_authorized,
            repository_path_allowed,
            sandbox_marker_present,
            sandbox_marker_exact,
            tree_payloads_exact,
            commit_payload_exact,
            payloads_within_policy,
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
            or receipt.return_code in (-124, -126, -127)
            or not receipt.fixed_argument_shape
            or receipt.stdout_size_bytes > policy.max_output_bytes
            or receipt.stderr_size_bytes > policy.max_output_bytes
        ):
            command_error = True
        return receipt, stdout, stderr

    object_format_sha1 = False
    parent_commit_present = False
    parent_commit_type_exact = False
    referenced_objects_present = False
    referenced_object_types_exact = False
    observed_tree_oids: set[str] = set()
    tree_write_count = 0
    tree_reuse_count = 0
    commit_write_count = 0
    commit_reused = False
    commit_object_present_after = False
    commit_object_type_exact = False
    commit_object_content_exact = False
    observed_commit_oid = ""

    if preconditions:
        format_receipt, format_stdout, _ = run(
            ("rev-parse", "--show-object-format"),
            operation="observe-object-format",
        )
        object_format_sha1 = bool(
            format_receipt.return_code == 0 and format_stdout.strip() == b"sha1"
        )
        parent_exists, _, _ = run(
            ("cat-file", "-e", candidate.parent_commit_sha),
            operation="observe-parent-commit",
        )
        parent_commit_present = parent_exists.return_code == 0
        parent_type, parent_type_stdout, _ = run(
            ("cat-file", "-t", candidate.parent_commit_sha),
            operation="verify-parent-commit-type",
        )
        parent_commit_type_exact = bool(
            parent_type.return_code == 0 and parent_type_stdout.strip() == b"commit"
        )
        references_present = True
        reference_types_exact = True
        for oid, expected_type in sorted(leaf_expectations.items()):
            exists_receipt, _, _ = run(
                ("cat-file", "-e", oid),
                operation="observe-referenced-object",
            )
            type_receipt, type_stdout, _ = run(
                ("cat-file", "-t", oid),
                operation="verify-referenced-object-type",
            )
            references_present = references_present and exists_receipt.return_code == 0
            reference_types_exact = bool(
                reference_types_exact
                and type_receipt.return_code == 0
                and type_stdout.decode("ascii", errors="ignore").strip() == expected_type
            )
        referenced_objects_present = references_present
        referenced_object_types_exact = reference_types_exact
        if not all(
            (
                object_format_sha1,
                parent_commit_present,
                parent_commit_type_exact,
                referenced_objects_present,
                referenced_object_types_exact,
            )
        ):
            command_error = True

    if preconditions and not command_error:
        for tree in trees:
            oid = tree.git_tree_oid
            payload = tree_payload_by_oid[oid]
            candidate_receipt, candidate_stdout, _ = run(
                ("hash-object", "-t", "tree", "--stdin"),
                stdin=payload,
                operation="calculate-tree-oid",
            )
            calculated = candidate_stdout.decode("ascii", errors="ignore").strip().lower()
            if candidate_receipt.return_code != 0 or calculated != oid:
                command_error = True
                break
            exists_receipt, _, _ = run(
                ("cat-file", "-e", oid),
                operation="observe-tree-before",
            )
            existed = exists_receipt.return_code == 0
            if exists_receipt.return_code == 1:
                write_receipt, _, _ = run(
                    ("hash-object", "-t", "tree", "-w", "--stdin"),
                    stdin=payload,
                    operation="materialize-tree-object",
                    mutating=True,
                )
                if write_receipt.return_code == 0:
                    tree_write_count += 1
                else:
                    command_error = True
            elif exists_receipt.return_code != 0:
                command_error = True
            present_receipt, _, _ = run(
                ("cat-file", "-e", oid),
                operation="observe-tree-after",
            )
            type_receipt, type_stdout, _ = run(
                ("cat-file", "-t", oid),
                operation="verify-tree-type",
            )
            size_receipt, size_stdout, _ = run(
                ("cat-file", "-s", oid),
                operation="verify-tree-size",
            )
            content_receipt, content_stdout, _ = run(
                ("cat-file", "tree", oid),
                operation="verify-tree-content",
            )
            try:
                observed_size = int(size_stdout.strip())
            except ValueError:
                observed_size = -1
            tree_exact = bool(
                present_receipt.return_code == 0
                and type_receipt.return_code == 0
                and type_stdout.strip() == b"tree"
                and size_receipt.return_code == 0
                and observed_size == len(payload)
                and content_receipt.return_code == 0
                and content_stdout == payload
            )
            if tree_exact:
                observed_tree_oids.add(oid)
                if existed:
                    tree_reuse_count += 1
            else:
                command_error = True
                break

    if preconditions and not command_error:
        commit_oid_receipt, commit_oid_stdout, _ = run(
            ("hash-object", "-t", "commit", "--stdin"),
            stdin=commit_payload,
            operation="calculate-commit-oid",
        )
        calculated_commit_oid = commit_oid_stdout.decode(
            "ascii", errors="ignore"
        ).strip().lower()
        if (
            commit_oid_receipt.return_code != 0
            or calculated_commit_oid != candidate.candidate_commit_oid
        ):
            command_error = True
        else:
            commit_exists, _, _ = run(
                ("cat-file", "-e", candidate.candidate_commit_oid),
                operation="observe-commit-before",
            )
            commit_existed = commit_exists.return_code == 0
            if commit_exists.return_code == 1:
                commit_write, _, _ = run(
                    ("hash-object", "-t", "commit", "-w", "--stdin"),
                    stdin=commit_payload,
                    operation="materialize-commit-object",
                    mutating=True,
                )
                if commit_write.return_code == 0:
                    commit_write_count = 1
                else:
                    command_error = True
            elif commit_exists.return_code != 0:
                command_error = True
            commit_present, _, _ = run(
                ("cat-file", "-e", candidate.candidate_commit_oid),
                operation="observe-commit-after",
            )
            commit_type, commit_type_stdout, _ = run(
                ("cat-file", "-t", candidate.candidate_commit_oid),
                operation="verify-commit-type",
            )
            commit_size, commit_size_stdout, _ = run(
                ("cat-file", "-s", candidate.candidate_commit_oid),
                operation="verify-commit-size",
            )
            commit_content, commit_content_stdout, _ = run(
                ("cat-file", "commit", candidate.candidate_commit_oid),
                operation="verify-commit-content",
            )
            try:
                observed_commit_size = int(commit_size_stdout.strip())
            except ValueError:
                observed_commit_size = -1
            commit_object_present_after = commit_present.return_code == 0
            commit_object_type_exact = bool(
                commit_type.return_code == 0 and commit_type_stdout.strip() == b"commit"
            )
            commit_object_content_exact = bool(
                commit_size.return_code == 0
                and observed_commit_size == len(commit_payload)
                and commit_content.return_code == 0
                and commit_content_stdout == commit_payload
            )
            if all(
                (
                    commit_object_present_after,
                    commit_object_type_exact,
                    commit_object_content_exact,
                )
            ):
                observed_commit_oid = candidate.candidate_commit_oid
                commit_reused = commit_existed
            else:
                command_error = True

    observed_tree_tuple = tuple(sorted(observed_tree_oids))
    tree_objects_present_after = observed_tree_tuple == expected_tree_oids
    tree_objects_type_exact = tree_objects_present_after
    tree_objects_content_exact = tree_objects_present_after
    success_checks = all(
        (
            policy_valid,
            request_valid,
            candidate_valid,
            request_binding_exact,
            v119_results_valid,
            blob_result_coverage_exact,
            executor_authorized,
            repository_path_allowed,
            sandbox_marker_present,
            sandbox_marker_exact,
            object_format_sha1,
            parent_commit_present,
            parent_commit_type_exact,
            referenced_objects_present,
            referenced_object_types_exact,
            tree_payloads_exact,
            commit_payload_exact,
            tree_objects_present_after,
            commit_object_present_after,
            tree_objects_type_exact,
            commit_object_type_exact,
            tree_objects_content_exact,
            commit_object_content_exact,
        )
    )
    write_performed = tree_write_count > 0 or commit_write_count > 0
    if success_checks and not command_error and write_performed:
        status = TREE_COMMIT_MATERIALIZED
        reason = "LIVE_TREE_AND_COMMIT_OBJECTS_MATERIALIZED_AND_VERIFIED"
    elif success_checks and not command_error and not write_performed:
        status = TREE_COMMIT_REUSED
        reason = "EXACT_EXISTING_TREE_AND_COMMIT_OBJECTS_REUSED"
    elif not preconditions:
        status = TREE_COMMIT_REJECTED
        reason = "LIVE_TREE_COMMIT_PRECONDITION_REJECTED"
    else:
        status = TREE_COMMIT_ERROR
        reason = "LIVE_TREE_COMMIT_COMMAND_OR_POSTCONDITION_ERROR"

    result = RepositoryBoundedTreeCommitResult(
        operation_id=request.operation_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        candidate_certificate_digest=candidate.certificate_digest,
        v119_result_digests=tuple(sorted(result.result_digest for result in v119_results)),
        repository_path_digest=actual_path_digest,
        repository_id=request.repository_id,
        git_dir_fingerprint=request.git_dir_fingerprint,
        executor_id=request.executor_id,
        expected_tree_oids=expected_tree_oids,
        observed_tree_oids=observed_tree_tuple,
        expected_root_tree_oid=candidate.root_tree_oid,
        observed_root_tree_oid=(candidate.root_tree_oid if candidate.root_tree_oid in observed_tree_oids else ""),
        expected_commit_oid=candidate.candidate_commit_oid,
        observed_commit_oid=observed_commit_oid,
        policy_valid=policy_valid,
        request_valid=request_valid,
        candidate_valid=candidate_valid,
        request_binding_exact=request_binding_exact,
        v119_results_valid=v119_results_valid,
        blob_result_coverage_exact=blob_result_coverage_exact,
        executor_authorized=executor_authorized,
        repository_path_allowed=repository_path_allowed,
        sandbox_marker_present=sandbox_marker_present,
        sandbox_marker_exact=sandbox_marker_exact,
        object_format_sha1=object_format_sha1,
        parent_commit_present=parent_commit_present,
        parent_commit_type_exact=parent_commit_type_exact,
        referenced_objects_present=referenced_objects_present,
        referenced_object_types_exact=referenced_object_types_exact,
        tree_payloads_exact=tree_payloads_exact,
        commit_payload_exact=commit_payload_exact,
        tree_objects_present_after=tree_objects_present_after,
        commit_object_present_after=commit_object_present_after,
        tree_objects_type_exact=tree_objects_type_exact,
        commit_object_type_exact=commit_object_type_exact,
        tree_objects_content_exact=tree_objects_content_exact,
        commit_object_content_exact=commit_object_content_exact,
        tree_write_count=tree_write_count,
        commit_write_count=commit_write_count,
        tree_reuse_count=tree_reuse_count,
        commit_reused=commit_reused,
        object_database_write_performed=write_performed,
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
            "candidate_valid": candidate_valid,
            "request_binding_exact": request_binding_exact,
            "v119_results_valid": v119_results_valid,
            "blob_result_coverage_exact": blob_result_coverage_exact,
            "executor_authorized": executor_authorized,
            "repository_path_allowed": repository_path_allowed,
            "sandbox_marker_present": sandbox_marker_present,
            "sandbox_marker_exact": sandbox_marker_exact,
            "object_format_sha1": object_format_sha1,
            "parent_commit_present": parent_commit_present,
            "parent_commit_type_exact": parent_commit_type_exact,
            "referenced_objects_present": referenced_objects_present,
            "referenced_object_types_exact": referenced_object_types_exact,
            "tree_payloads_exact": tree_payloads_exact,
            "commit_payload_exact": commit_payload_exact,
            "tree_objects_present_after": tree_objects_present_after,
            "commit_object_present_after": commit_object_present_after,
            "tree_objects_type_exact": tree_objects_type_exact,
            "commit_object_type_exact": commit_object_type_exact,
            "tree_objects_content_exact": tree_objects_content_exact,
            "commit_object_content_exact": commit_object_content_exact,
        },
        evidence_digests={
            "candidate_certificate": candidate.certificate_digest,
            "candidate_application_receipt": application_receipt.receipt_digest,
            "candidate_snapshot": snapshot.digest,
            "candidate_parent_inventory": parent_tree_inventory.inventory_digest,
            "candidate_policy": candidate_policy.policy_digest,
            "v120_policy": policy.policy_digest,
            "v120_request": request.request_digest,
            "repository_path": actual_path_digest,
            "sandbox_marker": canonical_digest(
                {"marker": marker_content if sandbox_marker_exact else ""}
            ),
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_bounded_tree_commit_result_digest(result),
    )
    issues = repository_bounded_tree_commit_result_issues(result)
    if issues:
        raise ValueError(f"bounded_tree_commit_result_invalid:{issues[0]}")
    return result
