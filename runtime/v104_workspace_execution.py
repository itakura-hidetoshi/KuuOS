#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_evolution_workspace_types_v1_04 import (
    FAILURE_CANDIDATE_BINDING,
    FAILURE_COMPARE_AND_SWAP,
    FAILURE_INVALID_SOURCE,
    FAILURE_NONE,
    FAILURE_OPERATION_INVALID,
    FAILURE_PATH_CONFLICT,
    FAILURE_PLAN_BINDING,
    TRANSITION_COMMITTED,
    WORKSPACE_MATERIALIZED,
    WORKSPACE_READY,
    RepositoryCheckpointEvolutionWorkspace,
    repository_checkpoint_evolution_workspace_digest,
    repository_checkpoint_workspace_tree_digest,
)
from runtime.v104_workspace_helpers import (
    repository_checkpoint_evolution_workspace_issues,
    repository_checkpoint_workspace_plan_issues,
    repository_checkpoint_workspace_seed_issues,
    workspace_changed_paths,
    workspace_plan_proposal_digest,
)
from runtime.v104_workspace_transition import (
    abort_workspace_transition,
    apply_workspace_operations,
    build_workspace_transition,
    workspace_transition_issues,
)


def execute_repository_checkpoint_workspace_plan(
    transition_id,
    workspace,
    seed,
    candidate,
    plan,
):
    if not transition_id:
        raise ValueError("workspace_transition_id_missing")
    plan_digest = getattr(plan, "plan_digest", "")
    if (
        repository_checkpoint_evolution_workspace_issues(workspace)
        or repository_checkpoint_workspace_seed_issues(seed)
    ):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan_digest,
            FAILURE_INVALID_SOURCE,
        )
    if repository_checkpoint_workspace_plan_issues(plan):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan_digest,
            FAILURE_OPERATION_INVALID,
        )
    if (
        workspace.seed_digest != seed.seed_digest
        or workspace.repository_id != seed.repository_id
        or workspace.git_dir_fingerprint != seed.git_dir_fingerprint
        or workspace.checkpoint_reference != seed.checkpoint_reference
        or workspace.checkpoint_oid != seed.checkpoint_oid
        or workspace.status != WORKSPACE_READY
    ):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_INVALID_SOURCE,
        )
    if (
        not getattr(candidate, "candidate_id", "")
        or candidate.candidate_id != plan.candidate_id
        or candidate.source_frontier_commit_sha != seed.checkpoint_oid
        or candidate.source_frontier_commit_sha != plan.source_checkpoint_oid
        or tuple(candidate.changed_paths) != plan.changed_paths
    ):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_CANDIDATE_BINDING,
        )
    expected_proposal = workspace_plan_proposal_digest(
        plan.candidate_id,
        plan.source_checkpoint_oid,
        plan.operations,
    )
    if (
        plan.proposal_digest != expected_proposal
        or candidate.proposal_digest != expected_proposal
    ):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_PLAN_BINDING,
        )
    try:
        files = apply_workspace_operations(workspace.files, plan.operations)
    except LookupError:
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_COMPARE_AND_SWAP,
        )
    except FileExistsError:
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_PATH_CONFLICT,
        )
    except (TypeError, ValueError):
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_OPERATION_INVALID,
        )

    final = RepositoryCheckpointEvolutionWorkspace(
        workspace.workspace_id,
        workspace.seed_digest,
        workspace.repository_id,
        workspace.git_dir_fingerprint,
        workspace.checkpoint_reference,
        workspace.checkpoint_oid,
        candidate.candidate_id,
        WORKSPACE_MATERIALIZED,
        files,
        tuple(sorted(item.operation_digest for item in plan.operations)),
        workspace_changed_paths(plan.operations),
        workspace.sequence_number + 1,
        repository_checkpoint_workspace_tree_digest(files),
        "",
    )
    final = replace(
        final,
        workspace_digest=repository_checkpoint_evolution_workspace_digest(final),
    )
    final_issues = repository_checkpoint_evolution_workspace_issues(final)
    if final_issues:
        return abort_workspace_transition(
            transition_id,
            workspace,
            plan.plan_digest,
            FAILURE_OPERATION_INVALID,
        )
    transition = build_workspace_transition(
        transition_id,
        status=TRANSITION_COMMITTED,
        failure_kind=FAILURE_NONE,
        plan_digest=plan.plan_digest,
        source=workspace,
        final=final,
        changed_paths=plan.changed_paths,
    )
    issues = workspace_transition_issues(transition)
    if issues:
        raise ValueError(f"workspace_transition_invalid:{issues[0]}")
    return final, transition
