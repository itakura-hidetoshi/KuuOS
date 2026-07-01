#!/usr/bin/env python3
from runtime.kuuos_repository_checkpoint_atomic_cas_transition_types_v1_16 import (
    TRANSITION_COMMITTED,
)
from runtime.kuuos_repository_checkpoint_atomic_cas_transition_v1_16 import (
    repository_checkpoint_atomic_cas_transition_result_issues,
)
from runtime.v117_checkpoint_live_git_preflight_core import (
    build_repository_checkpoint_live_git_preflight_policy,
    build_repository_checkpoint_live_git_preflight_request,
    execute_repository_checkpoint_live_git_preflight as _execute_preflight,
    repository_checkpoint_live_git_preflight_policy_issues,
    repository_checkpoint_live_git_preflight_receipt_issues,
    repository_checkpoint_live_git_preflight_request_issues,
)


def execute_repository_checkpoint_live_git_preflight(
    request,
    transition,
    policy,
    *,
    git_executable: str = "git",
):
    transition_issues = repository_checkpoint_atomic_cas_transition_result_issues(
        transition
    )
    if transition_issues:
        raise ValueError(f"checkpoint_v116_transition_invalid:{transition_issues[0]}")
    if not (
        transition.status == TRANSITION_COMMITTED
        and transition.transition_committed
        and transition.compare_and_swap_succeeded
        and transition.atomic_reference_nonce_transition
        and transition.nonce_consumed
        and not transition.live_git_command_invoked
        and not transition.live_repository_mutated
    ):
        raise ValueError("checkpoint_v116_transition_not_committed")
    if not (
        request.transition_result_digest == transition.result_digest
        and request.repository_id == transition.repository_id
        and request.git_dir_fingerprint == transition.git_dir_fingerprint
        and request.checkpoint_reference == transition.checkpoint_reference
        and request.expected_current_oid == transition.expected_current_oid
        and request.proposed_checkpoint_oid == transition.proposed_checkpoint_oid
    ):
        raise ValueError("checkpoint_live_git_preflight_transition_binding_mismatch")
    return _execute_preflight(
        request,
        transition,
        policy,
        git_executable=git_executable,
    )


__all__ = [
    "build_repository_checkpoint_live_git_preflight_policy",
    "repository_checkpoint_live_git_preflight_policy_issues",
    "build_repository_checkpoint_live_git_preflight_request",
    "repository_checkpoint_live_git_preflight_request_issues",
    "execute_repository_checkpoint_live_git_preflight",
    "repository_checkpoint_live_git_preflight_receipt_issues",
]
