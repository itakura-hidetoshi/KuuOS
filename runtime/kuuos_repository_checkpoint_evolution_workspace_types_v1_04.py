#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest

VERSION = "kuuos_repository_checkpoint_evolution_workspace_v1_04"

WORKSPACE_READY = "REPOSITORY_CHECKPOINT_WORKSPACE_READY"
WORKSPACE_MATERIALIZED = "REPOSITORY_CHECKPOINT_WORKSPACE_MATERIALIZED"

TRANSITION_COMMITTED = "REPOSITORY_CHECKPOINT_WORKSPACE_TRANSITION_COMMITTED"
TRANSITION_ABORTED = "REPOSITORY_CHECKPOINT_WORKSPACE_TRANSITION_ABORTED"

OP_ADD = "ADD"
OP_REPLACE = "REPLACE"
OP_DELETE = "DELETE"
OP_MOVE = "MOVE"
OPERATION_KINDS = (OP_ADD, OP_DELETE, OP_MOVE, OP_REPLACE)

FAILURE_NONE = "NONE"
FAILURE_INVALID_SOURCE = "INVALID_SOURCE"
FAILURE_CANDIDATE_BINDING = "CANDIDATE_BINDING_MISMATCH"
FAILURE_PLAN_BINDING = "PLAN_BINDING_MISMATCH"
FAILURE_PATH_CONFLICT = "PATH_CONFLICT"
FAILURE_COMPARE_AND_SWAP = "COMPARE_AND_SWAP_FAILED"
FAILURE_OPERATION_INVALID = "OPERATION_INVALID"


@dataclass(frozen=True)
class RepositoryCheckpointWorkspaceFile:
    path: str
    content: str
    executable: bool
    content_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_workspace_file_digest(
    file: RepositoryCheckpointWorkspaceFile,
) -> str:
    payload = file.to_dict()
    payload.pop("content_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointWorkspaceOperation:
    operation_id: str
    kind: str
    path: str
    target_path: str
    expected_old_content_digest: str
    new_content: str
    executable: bool
    operation_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def repository_checkpoint_workspace_operation_digest(
    operation: RepositoryCheckpointWorkspaceOperation,
) -> str:
    payload = operation.to_dict()
    payload.pop("operation_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointWorkspaceSeed:
    seed_id: str
    transaction_id: str
    checkpoint_receipt_digest: str
    checkpoint_result_digest: str
    checkpoint_state_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    checkpoint_oid: str
    files: tuple[RepositoryCheckpointWorkspaceFile, ...]
    tree_digest: str
    seed_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["files"] = [file.to_dict() for file in self.files]
        return payload


def repository_checkpoint_workspace_seed_digest(
    seed: RepositoryCheckpointWorkspaceSeed,
) -> str:
    payload = seed.to_dict()
    payload.pop("seed_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointWorkspacePlan:
    plan_id: str
    candidate_id: str
    source_checkpoint_oid: str
    operations: tuple[RepositoryCheckpointWorkspaceOperation, ...]
    changed_paths: tuple[str, ...]
    proposal_digest: str
    plan_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["operations"] = [operation.to_dict() for operation in self.operations]
        payload["changed_paths"] = list(self.changed_paths)
        return payload


def repository_checkpoint_workspace_plan_digest(
    plan: RepositoryCheckpointWorkspacePlan,
) -> str:
    payload = plan.to_dict()
    payload.pop("plan_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointEvolutionWorkspace:
    workspace_id: str
    seed_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    checkpoint_oid: str
    candidate_id: str
    status: str
    files: tuple[RepositoryCheckpointWorkspaceFile, ...]
    applied_operation_digests: tuple[str, ...]
    changed_paths: tuple[str, ...]
    sequence_number: int
    tree_digest: str
    workspace_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["files"] = [file.to_dict() for file in self.files]
        payload["applied_operation_digests"] = list(self.applied_operation_digests)
        payload["changed_paths"] = list(self.changed_paths)
        return payload


def repository_checkpoint_evolution_workspace_digest(
    workspace: RepositoryCheckpointEvolutionWorkspace,
) -> str:
    payload = workspace.to_dict()
    payload.pop("workspace_digest", None)
    return canonical_digest(payload)


@dataclass(frozen=True)
class RepositoryCheckpointWorkspaceTransition:
    transition_id: str
    status: str
    failure_kind: str
    plan_digest: str
    source_workspace_digest: str
    final_workspace_digest: str
    sequence_before: int
    sequence_after: int
    changed_paths: tuple[str, ...]
    source_preserved_on_abort: bool
    transition_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["changed_paths"] = list(self.changed_paths)
        return payload


def repository_checkpoint_workspace_transition_digest(
    transition: RepositoryCheckpointWorkspaceTransition,
) -> str:
    payload = transition.to_dict()
    payload.pop("transition_digest", None)
    return canonical_digest(payload)


def repository_checkpoint_workspace_tree_digest(
    files: tuple[RepositoryCheckpointWorkspaceFile, ...],
) -> str:
    return canonical_digest([file.to_dict() for file in files])
