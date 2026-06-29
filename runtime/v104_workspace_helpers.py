#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Iterable

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_atomic_checkpoint_creation_types_v1_02 import (
    CHECKPOINT_CREATION_COMMITTED,
    ZERO_OID,
    repository_checkpoint_state_digest,
)
from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    OP_ADD,
    OP_DELETE,
    OP_MOVE,
    OP_REPLACE,
    OPERATION_KINDS,
    WORKSPACE_MATERIALIZED,
    WORKSPACE_READY,
    RepositoryCheckpointEvolutionWorkspace,
    RepositoryCheckpointWorkspaceFile,
    RepositoryCheckpointWorkspaceOperation,
    RepositoryCheckpointWorkspacePlan,
    RepositoryCheckpointWorkspaceSeed,
    repository_checkpoint_evolution_workspace_digest,
    repository_checkpoint_workspace_file_digest,
    repository_checkpoint_workspace_operation_digest,
    repository_checkpoint_workspace_plan_digest,
    repository_checkpoint_workspace_seed_digest,
    repository_checkpoint_workspace_tree_digest,
)
from runtime.v103_receipt_policy import RECEIPT_CONFIRMED
from runtime.v103_result import checkpoint_receipt_result_digest


def canonical_repository_path(path: str) -> str:
    if not isinstance(path, str) or not path:
        raise ValueError("workspace_path_required")
    if "\x00" in path or "\\" in path:
        raise ValueError("workspace_path_invalid_character")
    if path.startswith("/") or path.endswith("/"):
        raise ValueError("workspace_path_not_relative_file")
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("workspace_path_not_canonical")
    return path


def canonical_workspace_files(
    files: Iterable[RepositoryCheckpointWorkspaceFile],
) -> tuple[RepositoryCheckpointWorkspaceFile, ...]:
    values = tuple(files)
    for file in values:
        canonical_repository_path(file.path)
        if not isinstance(file.content, str):
            raise ValueError("workspace_file_content_not_text")
        if not isinstance(file.executable, bool):
            raise ValueError("workspace_file_executable_not_bool")
        if file.content_digest != repository_checkpoint_workspace_file_digest(file):
            raise ValueError("workspace_file_digest_mismatch")
    paths = tuple(file.path for file in values)
    if len(paths) != len(set(paths)):
        raise ValueError("workspace_file_path_duplicate")
    return tuple(sorted(values, key=lambda item: item.path))


def build_repository_checkpoint_workspace_file(
    path: str,
    content: str,
    *,
    executable: bool = False,
) -> RepositoryCheckpointWorkspaceFile:
    canonical_repository_path(path)
    if not isinstance(content, str):
        raise ValueError("workspace_file_content_not_text")
    if not isinstance(executable, bool):
        raise ValueError("workspace_file_executable_not_bool")
    file = RepositoryCheckpointWorkspaceFile(path, content, executable, "")
    return replace(
        file,
        content_digest=repository_checkpoint_workspace_file_digest(file),
    )


def workspace_changed_paths(
    operations: Iterable[RepositoryCheckpointWorkspaceOperation],
) -> tuple[str, ...]:
    paths: list[str] = []
    for operation in operations:
        paths.append(operation.path)
        if operation.kind == OP_MOVE:
            paths.append(operation.target_path)
    return tuple(sorted(set(paths)))


def workspace_plan_proposal_digest(
    candidate_id: str,
    source_checkpoint_oid: str,
    operations: Iterable[RepositoryCheckpointWorkspaceOperation],
) -> str:
    values = tuple(operations)
    return canonical_digest(
        {
            "candidate_id": candidate_id,
            "source_checkpoint_oid": source_checkpoint_oid,
            "operation_digests": [item.operation_digest for item in values],
            "changed_paths": list(workspace_changed_paths(values)),
        }
    )


def build_repository_checkpoint_workspace_operation(
    operation_id: str,
    kind: str,
    path: str,
    *,
    target_path: str = "",
    expected_old_content_digest: str = "",
    new_content: str = "",
    executable: bool = False,
) -> RepositoryCheckpointWorkspaceOperation:
    if not operation_id:
        raise ValueError("workspace_operation_id_missing")
    if kind not in OPERATION_KINDS:
        raise ValueError("workspace_operation_kind_invalid")
    canonical_repository_path(path)
    if kind == OP_ADD:
        if target_path or expected_old_content_digest:
            raise ValueError("workspace_add_binding_invalid")
        if not isinstance(new_content, str) or not isinstance(executable, bool):
            raise ValueError("workspace_add_payload_invalid")
    elif kind == OP_REPLACE:
        if target_path or not expected_old_content_digest:
            raise ValueError("workspace_replace_binding_invalid")
        if not isinstance(new_content, str) or not isinstance(executable, bool):
            raise ValueError("workspace_replace_payload_invalid")
    elif kind == OP_DELETE:
        if target_path or not expected_old_content_digest or new_content or executable:
            raise ValueError("workspace_delete_binding_invalid")
    elif kind == OP_MOVE:
        canonical_repository_path(target_path)
        if target_path == path:
            raise ValueError("workspace_move_target_equals_source")
        if not expected_old_content_digest or new_content or executable:
            raise ValueError("workspace_move_binding_invalid")
    operation = RepositoryCheckpointWorkspaceOperation(
        operation_id,
        kind,
        path,
        target_path,
        expected_old_content_digest,
        new_content,
        executable,
        "",
    )
    return replace(
        operation,
        operation_digest=repository_checkpoint_workspace_operation_digest(operation),
    )


def repository_checkpoint_workspace_operation_issues(
    operation: RepositoryCheckpointWorkspaceOperation,
) -> tuple[str, ...]:
    try:
        rebuilt = build_repository_checkpoint_workspace_operation(
            operation.operation_id,
            operation.kind,
            operation.path,
            target_path=operation.target_path,
            expected_old_content_digest=operation.expected_old_content_digest,
            new_content=operation.new_content,
            executable=operation.executable,
        )
    except (TypeError, ValueError) as exc:
        return (str(exc),)
    if rebuilt.to_dict() != operation.to_dict():
        return ("workspace_operation_recomputation_mismatch",)
    return ()


def build_repository_checkpoint_workspace_plan(
    plan_id: str,
    candidate_id: str,
    source_checkpoint_oid: str,
    operations: Iterable[RepositoryCheckpointWorkspaceOperation],
) -> RepositoryCheckpointWorkspacePlan:
    if not plan_id or not candidate_id:
        raise ValueError("workspace_plan_identity_missing")
    if not isinstance(source_checkpoint_oid, str) or len(source_checkpoint_oid) != 40:
        raise ValueError("workspace_plan_source_oid_invalid")
    values = tuple(operations)
    if not values:
        raise ValueError("workspace_plan_operations_empty")
    if tuple(sorted(item.operation_id for item in values)) != tuple(
        item.operation_id for item in values
    ):
        raise ValueError("workspace_plan_operations_not_canonical")
    if len({item.operation_id for item in values}) != len(values):
        raise ValueError("workspace_plan_operation_id_duplicate")
    if any(repository_checkpoint_workspace_operation_issues(item) for item in values):
        raise ValueError("workspace_plan_operation_invalid")
    affected: list[str] = []
    for item in values:
        affected.append(item.path)
        if item.kind == OP_MOVE:
            affected.append(item.target_path)
    if len(affected) != len(set(affected)):
        raise ValueError("workspace_plan_path_conflict")
    changed_paths = tuple(sorted(affected))
    proposal_digest = workspace_plan_proposal_digest(
        candidate_id,
        source_checkpoint_oid,
        values,
    )
    plan = RepositoryCheckpointWorkspacePlan(
        plan_id,
        candidate_id,
        source_checkpoint_oid,
        values,
        changed_paths,
        proposal_digest,
        "",
    )
    return replace(plan, plan_digest=repository_checkpoint_workspace_plan_digest(plan))


def repository_checkpoint_workspace_plan_issues(
    plan: RepositoryCheckpointWorkspacePlan,
) -> tuple[str, ...]:
    try:
        rebuilt = build_repository_checkpoint_workspace_plan(
            plan.plan_id,
            plan.candidate_id,
            plan.source_checkpoint_oid,
            plan.operations,
        )
    except (TypeError, ValueError) as exc:
        return (str(exc),)
    if rebuilt.to_dict() != plan.to_dict():
        return ("workspace_plan_recomputation_mismatch",)
    return ()


def build_repository_checkpoint_workspace_seed(
    seed_id: str,
    checkpoint_receipt,
    checkpoint_result,
    checkpoint_state,
    files: Iterable[RepositoryCheckpointWorkspaceFile],
) -> RepositoryCheckpointWorkspaceSeed:
    if not seed_id:
        raise ValueError("workspace_seed_id_missing")
    if checkpoint_receipt.receipt_digest != checkpoint_receipt_result_digest(
        checkpoint_receipt
    ):
        raise ValueError("workspace_checkpoint_receipt_digest_invalid")
    if checkpoint_receipt.status != RECEIPT_CONFIRMED:
        raise ValueError("workspace_checkpoint_receipt_not_confirmed")
    if not checkpoint_receipt.checks.get("committed_receipt_confirmed"):
        raise ValueError("workspace_checkpoint_creation_not_committed")
    if not checkpoint_receipt.checks.get("supplied_external_report_consistent"):
        raise ValueError("workspace_checkpoint_report_inconsistent")
    if checkpoint_receipt.result_digest != checkpoint_result.result_digest:
        raise ValueError("workspace_checkpoint_result_binding_mismatch")
    if checkpoint_result.status != CHECKPOINT_CREATION_COMMITTED:
        raise ValueError("workspace_checkpoint_result_not_committed")
    if not checkpoint_result.checkpoint_created:
        raise ValueError("workspace_checkpoint_not_created")
    if checkpoint_state.state_digest != repository_checkpoint_state_digest(
        checkpoint_state
    ):
        raise ValueError("workspace_checkpoint_state_digest_invalid")
    if checkpoint_result.final_checkpoint_state_digest != checkpoint_state.state_digest:
        raise ValueError("workspace_checkpoint_state_binding_mismatch")
    if (
        checkpoint_result.repository_id != checkpoint_state.repository_id
        or checkpoint_result.git_dir_fingerprint != checkpoint_state.git_dir_fingerprint
        or checkpoint_result.checkpoint_reference != checkpoint_state.checkpoint_reference
        or checkpoint_result.proposed_new_oid != checkpoint_state.current_oid
    ):
        raise ValueError("workspace_checkpoint_identity_mismatch")
    if checkpoint_state.current_oid == ZERO_OID:
        raise ValueError("workspace_checkpoint_oid_zero")
    if not checkpoint_state.direct or checkpoint_state.symbolic:
        raise ValueError("workspace_checkpoint_reference_not_direct")
    if (
        not checkpoint_state.reference_store_source
        or checkpoint_state.working_tree_source
        or checkpoint_state.reflog_source
        or checkpoint_state.remote_source
    ):
        raise ValueError("workspace_checkpoint_source_invalid")
    canonical_files = canonical_workspace_files(files)
    tree_digest = repository_checkpoint_workspace_tree_digest(canonical_files)
    seed = RepositoryCheckpointWorkspaceSeed(
        seed_id,
        checkpoint_receipt.transaction_id,
        checkpoint_receipt.receipt_digest,
        checkpoint_result.result_digest,
        checkpoint_state.state_digest,
        checkpoint_state.repository_id,
        checkpoint_state.git_dir_fingerprint,
        checkpoint_state.checkpoint_reference,
        checkpoint_state.current_oid,
        canonical_files,
        tree_digest,
        "",
    )
    return replace(seed, seed_digest=repository_checkpoint_workspace_seed_digest(seed))


def repository_checkpoint_workspace_seed_issues(
    seed: RepositoryCheckpointWorkspaceSeed,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not seed.seed_id or not seed.transaction_id:
        issues.append("workspace_seed_identity_missing")
    try:
        files = canonical_workspace_files(seed.files)
    except (TypeError, ValueError) as exc:
        issues.append(str(exc))
        files = ()
    if files and files != seed.files:
        issues.append("workspace_seed_files_not_canonical")
    if seed.tree_digest != repository_checkpoint_workspace_tree_digest(seed.files):
        issues.append("workspace_seed_tree_digest_mismatch")
    if seed.seed_digest != repository_checkpoint_workspace_seed_digest(seed):
        issues.append("workspace_seed_digest_mismatch")
    return tuple(issues)


def initialize_repository_checkpoint_evolution_workspace(
    workspace_id: str,
    seed: RepositoryCheckpointWorkspaceSeed,
) -> RepositoryCheckpointEvolutionWorkspace:
    if not workspace_id:
        raise ValueError("workspace_id_missing")
    issues = repository_checkpoint_workspace_seed_issues(seed)
    if issues:
        raise ValueError(f"workspace_seed_invalid:{issues[0]}")
    workspace = RepositoryCheckpointEvolutionWorkspace(
        workspace_id,
        seed.seed_digest,
        seed.repository_id,
        seed.git_dir_fingerprint,
        seed.checkpoint_reference,
        seed.checkpoint_oid,
        "",
        WORKSPACE_READY,
        seed.files,
        (),
        (),
        0,
        seed.tree_digest,
        "",
    )
    return replace(
        workspace,
        workspace_digest=repository_checkpoint_evolution_workspace_digest(workspace),
    )


def repository_checkpoint_evolution_workspace_issues(
    workspace: RepositoryCheckpointEvolutionWorkspace,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not workspace.workspace_id or not workspace.seed_digest:
        issues.append("workspace_identity_missing")
    if workspace.status not in (WORKSPACE_READY, WORKSPACE_MATERIALIZED):
        issues.append("workspace_status_invalid")
    if workspace.sequence_number < 0:
        issues.append("workspace_sequence_negative")
    try:
        files = canonical_workspace_files(workspace.files)
    except (TypeError, ValueError) as exc:
        issues.append(str(exc))
        files = ()
    if files and files != workspace.files:
        issues.append("workspace_files_not_canonical")
    if tuple(sorted(set(workspace.applied_operation_digests))) != (
        workspace.applied_operation_digests
    ):
        issues.append("workspace_operation_digests_not_canonical")
    if tuple(sorted(set(workspace.changed_paths))) != workspace.changed_paths:
        issues.append("workspace_changed_paths_not_canonical")
    if workspace.status == WORKSPACE_READY and (
        workspace.candidate_id
        or workspace.applied_operation_digests
        or workspace.changed_paths
    ):
        issues.append("workspace_ready_state_not_clean")
    if workspace.status == WORKSPACE_MATERIALIZED and not workspace.candidate_id:
        issues.append("workspace_materialized_candidate_missing")
    if workspace.tree_digest != repository_checkpoint_workspace_tree_digest(
        workspace.files
    ):
        issues.append("workspace_tree_digest_mismatch")
    if workspace.workspace_digest != repository_checkpoint_evolution_workspace_digest(
        workspace
    ):
        issues.append("workspace_digest_mismatch")
    return tuple(issues)
