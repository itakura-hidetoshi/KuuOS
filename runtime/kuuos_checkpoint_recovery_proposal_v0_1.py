#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_repository_checkpoint_reflog_types_v1_24 import (
    REFLOG_RECORDED,
    REFLOG_REUSED,
    RepositoryCheckpointReflogResult,
    repository_checkpoint_reflog_result_digest,
)
from runtime.kuuos_checkpoint_recovery_proposal_types_v0_1 import (
    RECOVERY_OBJECTIVE_COMPARE_ONLY,
    RECOVERY_PROPOSAL_PROPOSED,
    RECOVERY_PROPOSAL_REJECTED,
    CheckpointRecoveryProposal,
    CheckpointRecoveryProposalPolicy,
    checkpoint_recovery_proposal_digest,
    checkpoint_recovery_proposal_policy_digest,
)

ZERO_OID = "0" * 40


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _target_reference_is_safe(reference: str) -> bool:
    return bool(
        reference.startswith("refs/")
        and not reference.startswith("refs/kuuos/checkpoints/")
        and not reference.endswith("/")
        and "//" not in reference
        and ".." not in reference
        and " " not in reference
    )


def build_checkpoint_recovery_proposal_policy(
    policy_id: str,
    *,
    authorized_requestor_ids: tuple[str, ...],
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
    allowed_target_references: tuple[str, ...],
    max_rationale_bytes: int = 4096,
) -> CheckpointRecoveryProposalPolicy:
    policy = CheckpointRecoveryProposalPolicy(
        policy_id=policy_id,
        authorized_requestor_ids=_canonical(authorized_requestor_ids),
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        allowed_target_references=_canonical(allowed_target_references),
        allowed_objectives=(RECOVERY_OBJECTIVE_COMPARE_ONLY,),
        max_rationale_bytes=max_rationale_bytes,
        require_accepted_v124_result=True,
        require_exact_source_binding=True,
        require_exact_target_allowlist=True,
        require_distinct_source_and_target=True,
        require_source_target_comparison=True,
        require_external_review=True,
        require_explicit_authorization_decision=True,
        require_read_only_proposal=True,
        continue_v124_mutation_series=False,
        allow_live_git_execution=False,
        allow_repository_mutation=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=checkpoint_recovery_proposal_policy_digest(policy),
    )
    issues = checkpoint_recovery_proposal_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_recovery_policy_invalid:{issues[0]}")
    return policy


def checkpoint_recovery_proposal_policy_issues(
    policy: CheckpointRecoveryProposalPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("recovery_policy_id_missing")
    for field_name in (
        "authorized_requestor_ids",
        "allowed_repository_ids",
        "allowed_checkpoint_references",
        "allowed_target_references",
        "allowed_objectives",
    ):
        values = getattr(policy, field_name)
        if values != _canonical(values):
            issues.append(f"{field_name}_not_canonical")
        if not values:
            issues.append(f"{field_name}_empty")
    if policy.allowed_objectives != (RECOVERY_OBJECTIVE_COMPARE_ONLY,):
        issues.append("recovery_objective_not_compare_only")
    if not all(
        reference.startswith("refs/kuuos/checkpoints/")
        for reference in policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_reference_namespace_invalid")
    if not all(
        _target_reference_is_safe(reference)
        for reference in policy.allowed_target_references
    ):
        issues.append("target_reference_allowlist_invalid")
    if policy.max_rationale_bytes <= 0:
        issues.append("max_rationale_bytes_invalid")
    if not all(
        (
            policy.require_accepted_v124_result,
            policy.require_exact_source_binding,
            policy.require_exact_target_allowlist,
            policy.require_distinct_source_and_target,
            policy.require_source_target_comparison,
            policy.require_external_review,
            policy.require_explicit_authorization_decision,
            policy.require_read_only_proposal,
        )
    ):
        issues.append("required_recovery_guard_disabled")
    if policy.continue_v124_mutation_series:
        issues.append("v124_mutation_series_continuation_forbidden")
    if policy.allow_live_git_execution:
        issues.append("live_git_execution_forbidden")
    if policy.allow_repository_mutation:
        issues.append("repository_mutation_forbidden")
    if policy.policy_digest != checkpoint_recovery_proposal_policy_digest(policy):
        issues.append("recovery_policy_digest_mismatch")
    return tuple(issues)


def _accepted_v124_result(result: RepositoryCheckpointReflogResult) -> bool:
    write_accounting_exact = bool(
        (
            result.status == REFLOG_RECORDED
            and result.checkpoint_reflog_write_performed
            and result.reflog_write_command_attempted
            and result.reflog_write_command_succeeded
            and result.live_git_command_invoked
            and result.live_repository_mutated
            and not result.exact_existing_reflog_reused
        )
        or (
            result.status == REFLOG_REUSED
            and result.exact_existing_reflog_reused
            and not result.checkpoint_reflog_write_performed
            and not result.reflog_write_command_attempted
            and not result.live_repository_mutated
        )
    )
    return bool(
        result.result_digest == repository_checkpoint_reflog_result_digest(result)
        and result.status in (REFLOG_RECORDED, REFLOG_REUSED)
        and result.policy_valid
        and result.request_valid
        and result.v121_request_valid
        and result.v121_result_valid
        and result.v121_result_accepted
        and result.v123_request_valid
        and result.v123_result_valid
        and result.v123_result_accepted
        and result.cross_stage_binding_exact
        and result.executor_authorized
        and result.repository_path_allowed
        and result.checkpoint_namespace_exact
        and result.authority_marker_present
        and result.authority_marker_exact
        and result.current_ref_exact_before
        and result.current_ref_exact_after
        and result.old_object_present
        and result.new_object_present
        and result.target_reflog_path_exact
        and result.target_reflog_present_after
        and result.target_reflog_entry_exact
        and result.target_reflog_single_entry
        and write_accounting_exact
        and not result.other_reflog_write_performed
        and not result.current_object_database_write_performed
        and not result.current_reference_write_performed
        and not result.index_write_performed
        and not result.working_tree_write_performed
        and not result.push_performed
        and not result.signing_performed
        and result.prior_object_database_write_performed
        and result.prior_checkpoint_reference_write_performed
        and result.prior_dedicated_index_write_performed
        and result.prior_sandbox_working_tree_write_performed
        and result.transition_new_oid != ZERO_OID
    )


def _rationale_digest(rationale: str) -> str:
    return canonical_digest({"rationale": rationale})


def construct_checkpoint_recovery_proposal(
    proposal_id: str,
    source_result: RepositoryCheckpointReflogResult,
    policy: CheckpointRecoveryProposalPolicy,
    *,
    target_reference: str,
    requestor_id: str,
    rationale: str,
    proposed_at_epoch_seconds: int,
    objective: str = RECOVERY_OBJECTIVE_COMPARE_ONLY,
) -> CheckpointRecoveryProposal:
    source_result_valid = bool(
        source_result.result_digest
        == repository_checkpoint_reflog_result_digest(source_result)
    )
    source_result_accepted = _accepted_v124_result(source_result)
    policy_valid = not checkpoint_recovery_proposal_policy_issues(policy)
    source_binding_exact = bool(
        source_result.repository_id in policy.allowed_repository_ids
        and source_result.checkpoint_reference
        in policy.allowed_checkpoint_references
        and source_result.checkpoint_reference.startswith("refs/kuuos/checkpoints/")
        and bool(source_result.git_dir_fingerprint)
        and source_result.transition_new_oid != ZERO_OID
    )
    requestor_authorized = requestor_id in policy.authorized_requestor_ids
    target_reference_allowed = bool(
        target_reference in policy.allowed_target_references
        and _target_reference_is_safe(target_reference)
    )
    source_target_distinct = bool(
        target_reference != source_result.checkpoint_reference
    )
    objective_allowed = objective in policy.allowed_objectives
    rationale_valid = bool(
        rationale
        and len(rationale.encode("utf-8")) <= policy.max_rationale_bytes
    )
    timestamp_valid = proposed_at_epoch_seconds >= 0

    accepted = all(
        (
            bool(proposal_id),
            source_result_valid,
            source_result_accepted,
            policy_valid,
            source_binding_exact,
            requestor_authorized,
            target_reference_allowed,
            source_target_distinct,
            objective_allowed,
            rationale_valid,
            timestamp_valid,
        )
    )
    status = (
        RECOVERY_PROPOSAL_PROPOSED
        if accepted
        else RECOVERY_PROPOSAL_REJECTED
    )
    reason = "proposal_ready_for_comparison_and_review" if accepted else "proposal_rejected"

    checks = {
        "proposal_id_present": bool(proposal_id),
        "source_result_valid": source_result_valid,
        "source_result_accepted": source_result_accepted,
        "policy_valid": policy_valid,
        "source_binding_exact": source_binding_exact,
        "requestor_authorized": requestor_authorized,
        "target_reference_allowed": target_reference_allowed,
        "source_target_distinct": source_target_distinct,
        "objective_allowed": objective_allowed,
        "rationale_valid": rationale_valid,
        "timestamp_valid": timestamp_valid,
        "comparison_required": accepted,
        "source_target_comparison_performed": False,
        "external_review_required": accepted,
        "explicit_authorization_decision_required": accepted,
        "recovery_authority_granted": False,
        "live_git_execution_performed": False,
        "repository_mutation_performed": False,
        "continues_v124_mutation_series": False,
    }
    proposal = CheckpointRecoveryProposal(
        proposal_id=proposal_id,
        status=status,
        reason=reason,
        policy_digest=policy.policy_digest,
        source_v124_result_digest=source_result.result_digest,
        source_v124_status=source_result.status,
        repository_id=source_result.repository_id,
        git_dir_fingerprint=source_result.git_dir_fingerprint,
        source_checkpoint_reference=source_result.checkpoint_reference,
        source_checkpoint_oid=source_result.transition_new_oid,
        target_reference=target_reference,
        objective=objective,
        requestor_id=requestor_id,
        rationale_digest=_rationale_digest(rationale),
        proposed_at_epoch_seconds=proposed_at_epoch_seconds,
        source_result_valid=source_result_valid,
        source_result_accepted=source_result_accepted,
        source_binding_exact=source_binding_exact,
        requestor_authorized=requestor_authorized,
        target_reference_allowed=target_reference_allowed,
        source_target_distinct=source_target_distinct,
        objective_allowed=objective_allowed,
        rationale_valid=rationale_valid,
        comparison_required=accepted,
        source_target_comparison_performed=False,
        external_review_required=accepted,
        explicit_authorization_decision_required=accepted,
        recovery_authority_granted=False,
        live_git_execution_performed=False,
        repository_mutation_performed=False,
        continues_v124_mutation_series=False,
        checks=checks,
        evidence_digests={
            "source_v124_result": source_result.result_digest,
            "proposal_policy": policy.policy_digest,
            "rationale": _rationale_digest(rationale),
        },
        proposal_digest="",
    )
    return replace(
        proposal,
        proposal_digest=checkpoint_recovery_proposal_digest(proposal),
    )


def propose_checkpoint_recovery(
    proposal_id: str,
    source_result: RepositoryCheckpointReflogResult,
    policy: CheckpointRecoveryProposalPolicy,
    *,
    target_reference: str,
    requestor_id: str,
    rationale: str,
    proposed_at_epoch_seconds: int,
    objective: str = RECOVERY_OBJECTIVE_COMPARE_ONLY,
) -> CheckpointRecoveryProposal:
    proposal = construct_checkpoint_recovery_proposal(
        proposal_id,
        source_result,
        policy,
        target_reference=target_reference,
        requestor_id=requestor_id,
        rationale=rationale,
        proposed_at_epoch_seconds=proposed_at_epoch_seconds,
        objective=objective,
    )
    issues = checkpoint_recovery_proposal_issues(
        proposal,
        source_result,
        policy,
        target_reference=target_reference,
        requestor_id=requestor_id,
        rationale=rationale,
        proposed_at_epoch_seconds=proposed_at_epoch_seconds,
        objective=objective,
    )
    if issues:
        raise ValueError(f"checkpoint_recovery_proposal_invalid:{issues[0]}")
    return proposal


def checkpoint_recovery_proposal_issues(
    proposal: CheckpointRecoveryProposal,
    source_result: RepositoryCheckpointReflogResult,
    policy: CheckpointRecoveryProposalPolicy,
    *,
    target_reference: str,
    requestor_id: str,
    rationale: str,
    proposed_at_epoch_seconds: int,
    objective: str = RECOVERY_OBJECTIVE_COMPARE_ONLY,
) -> tuple[str, ...]:
    expected = construct_checkpoint_recovery_proposal(
        proposal.proposal_id,
        source_result,
        policy,
        target_reference=target_reference,
        requestor_id=requestor_id,
        rationale=rationale,
        proposed_at_epoch_seconds=proposed_at_epoch_seconds,
        objective=objective,
    )
    issues: list[str] = []
    if proposal.to_dict() != expected.to_dict():
        issues.append("recovery_proposal_recomputation_mismatch")
    if proposal.status not in (
        RECOVERY_PROPOSAL_PROPOSED,
        RECOVERY_PROPOSAL_REJECTED,
    ):
        issues.append("recovery_proposal_status_invalid")
    if proposal.status == RECOVERY_PROPOSAL_PROPOSED:
        if not proposal.comparison_required:
            issues.append("recovery_comparison_not_required")
        if not proposal.external_review_required:
            issues.append("recovery_external_review_not_required")
        if not proposal.explicit_authorization_decision_required:
            issues.append("recovery_authorization_decision_not_required")
    if proposal.source_target_comparison_performed:
        issues.append("recovery_comparison_performed_too_early")
    if proposal.recovery_authority_granted:
        issues.append("recovery_authority_granted_too_early")
    if proposal.live_git_execution_performed:
        issues.append("recovery_live_git_execution_forbidden")
    if proposal.repository_mutation_performed:
        issues.append("recovery_repository_mutation_forbidden")
    if proposal.continues_v124_mutation_series:
        issues.append("recovery_mutation_series_continuation_forbidden")
    if proposal.proposal_digest != checkpoint_recovery_proposal_digest(proposal):
        issues.append("recovery_proposal_digest_mismatch")
    return tuple(issues)


__all__ = [
    "build_checkpoint_recovery_proposal_policy",
    "checkpoint_recovery_proposal_policy_issues",
    "construct_checkpoint_recovery_proposal",
    "propose_checkpoint_recovery",
    "checkpoint_recovery_proposal_issues",
]
