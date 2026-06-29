#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    FAILURE_NONE,
    OP_ADD,
    OP_DELETE,
    OP_MOVE,
    OP_REPLACE,
    TRANSITION_ABORTED,
    TRANSITION_COMMITTED,
    RepositoryCheckpointWorkspaceTransition,
    repository_checkpoint_workspace_transition_digest,
)
from runtime.v104_workspace_helpers import (
    build_repository_checkpoint_workspace_file,
    canonical_workspace_files,
    repository_checkpoint_workspace_operation_issues,
)


def build_workspace_transition(
    transition_id,
    *,
    status,
    failure_kind,
    plan_digest,
    source,
    final,
    changed_paths,
):
    transition = RepositoryCheckpointWorkspaceTransition(
        transition_id,
        status,
        failure_kind,
        plan_digest,
        source.workspace_digest,
        final.workspace_digest,
        source.sequence_number,
        final.sequence_number,
        changed_paths,
        status == TRANSITION_ABORTED and source.to_dict() == final.to_dict(),
        "",
    )
    return replace(
        transition,
        transition_digest=repository_checkpoint_workspace_transition_digest(
            transition
        ),
    )


def workspace_transition_issues(transition):
    issues = []
    if not transition.transition_id:
        issues.append("workspace_transition_id_missing")
    if transition.status not in (TRANSITION_COMMITTED, TRANSITION_ABORTED):
        issues.append("workspace_transition_status_invalid")
    if transition.sequence_before < 0 or transition.sequence_after < 0:
        issues.append("workspace_transition_sequence_negative")
    if tuple(sorted(set(transition.changed_paths))) != transition.changed_paths:
        issues.append("workspace_transition_changed_paths_not_canonical")
    if transition.status == TRANSITION_COMMITTED:
        if transition.failure_kind != FAILURE_NONE:
            issues.append("workspace_committed_failure_kind_invalid")
        if transition.sequence_after != transition.sequence_before + 1:
            issues.append("workspace_committed_sequence_invalid")
        if transition.source_preserved_on_abort:
            issues.append("workspace_committed_marked_preserved")
    else:
        if transition.failure_kind == FAILURE_NONE:
            issues.append("workspace_aborted_failure_missing")
        if transition.sequence_after != transition.sequence_before:
            issues.append("workspace_aborted_sequence_advanced")
        if transition.source_workspace_digest != transition.final_workspace_digest:
            issues.append("workspace_aborted_state_changed")
        if not transition.source_preserved_on_abort:
            issues.append("workspace_aborted_source_not_preserved")
        if transition.changed_paths:
            issues.append("workspace_aborted_changed_paths_present")
    if transition.transition_digest != (
        repository_checkpoint_workspace_transition_digest(transition)
    ):
        issues.append("workspace_transition_digest_mismatch")
    return tuple(issues)


def abort_workspace_transition(
    transition_id,
    source,
    plan_digest,
    failure_kind,
):
    transition = build_workspace_transition(
        transition_id,
        status=TRANSITION_ABORTED,
        failure_kind=failure_kind,
        plan_digest=plan_digest,
        source=source,
        final=source,
        changed_paths=(),
    )
    issues = workspace_transition_issues(transition)
    if issues:
        raise ValueError(f"workspace_abort_transition_invalid:{issues[0]}")
    return source, transition


def apply_workspace_operations(files, operations):
    file_map = {file.path: file for file in files}
    for operation in operations:
        if repository_checkpoint_workspace_operation_issues(operation):
            raise ValueError("workspace_operation_invalid")
        if operation.kind == OP_ADD:
            if operation.path in file_map:
                raise LookupError("workspace_compare_and_swap_failed")
            file_map[operation.path] = build_repository_checkpoint_workspace_file(
                operation.path,
                operation.new_content,
                executable=operation.executable,
            )
        elif operation.kind == OP_REPLACE:
            current = file_map.get(operation.path)
            if current is None or current.content_digest != (
                operation.expected_old_content_digest
            ):
                raise LookupError("workspace_compare_and_swap_failed")
            file_map[operation.path] = build_repository_checkpoint_workspace_file(
                operation.path,
                operation.new_content,
                executable=operation.executable,
            )
        elif operation.kind == OP_DELETE:
            current = file_map.get(operation.path)
            if current is None or current.content_digest != (
                operation.expected_old_content_digest
            ):
                raise LookupError("workspace_compare_and_swap_failed")
            del file_map[operation.path]
        elif operation.kind == OP_MOVE:
            current = file_map.get(operation.path)
            if current is None or current.content_digest != (
                operation.expected_old_content_digest
            ):
                raise LookupError("workspace_compare_and_swap_failed")
            if operation.target_path in file_map:
                raise FileExistsError("workspace_move_target_exists")
            del file_map[operation.path]
            file_map[operation.target_path] = (
                build_repository_checkpoint_workspace_file(
                    operation.target_path,
                    current.content,
                    executable=current.executable,
                )
            )
        else:
            raise ValueError("workspace_operation_kind_invalid")
    return canonical_workspace_files(file_map.values())
