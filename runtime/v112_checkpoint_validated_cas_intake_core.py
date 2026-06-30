#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    VALID,
    CheckpointCandidateValidationReceipt,
    checkpoint_candidate_validation_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    CONTRACT_READY,
    RepositoryCheckpointCasContract,
    repository_checkpoint_cas_contract_digest,
)
from runtime.kuuos_repository_checkpoint_validated_cas_intake_types_v1_12 import (
    INTAKE_CONFLICT,
    INTAKE_READY,
    INTAKE_REJECTED,
    REASON_INVALID_BINDING,
    REASON_VALIDATED_CONFLICT,
    REASON_VALIDATED_READY,
    RepositoryCheckpointValidatedCasIntake,
    RepositoryCheckpointValidatedCasIntakePolicy,
    repository_checkpoint_validated_cas_intake_digest,
    repository_checkpoint_validated_cas_intake_policy_digest,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_validated_cas_intake_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
) -> RepositoryCheckpointValidatedCasIntakePolicy:
    policy = RepositoryCheckpointValidatedCasIntakePolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        require_valid_v111_receipt=True,
        require_valid_v110_contract=True,
        require_exact_candidate_binding=True,
        require_exact_oid_binding=True,
        read_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_validated_cas_intake_policy_digest(policy),
    )
    issues = repository_checkpoint_validated_cas_intake_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_validated_cas_intake_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_validated_cas_intake_policy_issues(
    policy: RepositoryCheckpointValidatedCasIntakePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_validated_cas_intake_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("checkpoint_validated_cas_intake_repository_ids_not_canonical")
    if not policy.allowed_repository_ids:
        issues.append("checkpoint_validated_cas_intake_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(
        policy.allowed_checkpoint_references
    ):
        issues.append("checkpoint_validated_cas_intake_references_not_canonical")
    if not policy.allowed_checkpoint_references:
        issues.append("checkpoint_validated_cas_intake_references_empty")
    if not all(
        (
            policy.require_valid_v111_receipt,
            policy.require_valid_v110_contract,
            policy.require_exact_candidate_binding,
            policy.require_exact_oid_binding,
            policy.read_only,
        )
    ):
        issues.append("checkpoint_validated_cas_intake_guard_disabled")
    if policy.policy_digest != repository_checkpoint_validated_cas_intake_policy_digest(
        policy
    ):
        issues.append("checkpoint_validated_cas_intake_policy_digest_mismatch")
    return tuple(issues)


def construct_repository_checkpoint_validated_cas_intake(
    intake_id: str,
    validation: CheckpointCandidateValidationReceipt,
    contract: RepositoryCheckpointCasContract,
    policy: RepositoryCheckpointValidatedCasIntakePolicy,
) -> RepositoryCheckpointValidatedCasIntake:
    policy_valid = not repository_checkpoint_validated_cas_intake_policy_issues(policy)
    validation_evidence_exact = (
        validation.evidence_digests.get("candidate") == validation.candidate_digest
    )
    contract_evidence_exact = (
        contract.evidence_digests.get("checkpoint_candidate")
        == contract.candidate_digest
    )
    validation_receipt_valid = bool(
        validation.validation_digest == checkpoint_candidate_validation_digest(validation)
        and validation.status == VALID
        and validation.upstream_chain_revalidated
        and validation.ready_candidate
        and validation.repository_matches
        and validation.checkpoint_matches
        and validation.distinct_nonzero_oids
        and validation_evidence_exact
        and not validation.operation_performed
    )
    contract_valid = bool(
        contract.contract_digest == repository_checkpoint_cas_contract_digest(contract)
        and contract.status in (CONTRACT_READY, CONTRACT_CONFLICT)
        and contract.checkpoint_namespace_only
        and contract_evidence_exact
        and not contract.repository_change_authority_granted
        and not contract.execution_performed
        and not contract.live_git_command_invoked
    )
    candidate_binding_exact = contract.candidate_digest == validation.candidate_digest
    repository_binding_exact = bool(
        contract.repository_id == validation.repository_id
        and contract.repository_id in policy.allowed_repository_ids
    )
    checkpoint_binding_exact = bool(
        contract.checkpoint_reference == validation.checkpoint_reference
        and contract.checkpoint_reference in policy.allowed_checkpoint_references
    )
    oid_binding_exact = bool(
        contract.expected_current_oid == validation.expected_current_oid
        and contract.proposed_checkpoint_oid == validation.proposed_checkpoint_oid
    )
    base_valid = all(
        (
            bool(intake_id),
            policy_valid,
            validation_receipt_valid,
            contract_valid,
            candidate_binding_exact,
            repository_binding_exact,
            checkpoint_binding_exact,
            oid_binding_exact,
        )
    )

    if not base_valid:
        status = INTAKE_REJECTED
        reason = REASON_INVALID_BINDING
    elif contract.status == CONTRACT_READY and contract.compare_and_swap_required:
        status = INTAKE_READY
        reason = REASON_VALIDATED_READY
    elif contract.status == CONTRACT_CONFLICT and not contract.compare_and_swap_required:
        status = INTAKE_CONFLICT
        reason = REASON_VALIDATED_CONFLICT
    else:
        status = INTAKE_REJECTED
        reason = REASON_INVALID_BINDING

    cas_required = status == INTAKE_READY
    checks = {
        "policy_valid": policy_valid,
        "validation_evidence_exact": validation_evidence_exact,
        "validation_receipt_valid": validation_receipt_valid,
        "upstream_chain_revalidated": validation.upstream_chain_revalidated,
        "contract_evidence_exact": contract_evidence_exact,
        "contract_valid": contract_valid,
        "candidate_binding_exact": candidate_binding_exact,
        "repository_binding_exact": repository_binding_exact,
        "checkpoint_binding_exact": checkpoint_binding_exact,
        "oid_binding_exact": oid_binding_exact,
        "compare_and_swap_required": cas_required,
        "repository_change_authority_granted": False,
        "execution_performed": False,
        "live_git_command_invoked": False,
    }
    intake = RepositoryCheckpointValidatedCasIntake(
        intake_id=intake_id,
        status=status,
        reason=reason,
        validation_digest=validation.validation_digest,
        contract_digest=contract.contract_digest,
        candidate_digest=validation.candidate_digest,
        policy_digest=policy.policy_digest,
        repository_id=contract.repository_id,
        git_dir_fingerprint=contract.git_dir_fingerprint,
        checkpoint_reference=contract.checkpoint_reference,
        expected_current_oid=contract.expected_current_oid,
        observed_current_oid=contract.observed_current_oid,
        proposed_checkpoint_oid=contract.proposed_checkpoint_oid,
        upstream_chain_revalidated=validation.upstream_chain_revalidated,
        validation_receipt_valid=validation_receipt_valid,
        contract_valid=contract_valid,
        candidate_binding_exact=candidate_binding_exact,
        repository_binding_exact=repository_binding_exact,
        checkpoint_binding_exact=checkpoint_binding_exact,
        oid_binding_exact=oid_binding_exact,
        compare_and_swap_required=cas_required,
        repository_change_authority_granted=False,
        execution_performed=False,
        live_git_command_invoked=False,
        checks=checks,
        evidence_digests={
            "checkpoint_candidate_validation": validation.validation_digest,
            "checkpoint_cas_contract": contract.contract_digest,
            "validated_cas_intake_policy": policy.policy_digest,
        },
        intake_digest="",
    )
    return replace(
        intake,
        intake_digest=repository_checkpoint_validated_cas_intake_digest(intake),
    )


def derive_repository_checkpoint_validated_cas_intake(
    intake_id: str,
    validation: CheckpointCandidateValidationReceipt,
    contract: RepositoryCheckpointCasContract,
    policy: RepositoryCheckpointValidatedCasIntakePolicy,
) -> RepositoryCheckpointValidatedCasIntake:
    intake = construct_repository_checkpoint_validated_cas_intake(
        intake_id,
        validation,
        contract,
        policy,
    )
    issues = repository_checkpoint_validated_cas_intake_issues(
        intake,
        validation,
        contract,
        policy,
    )
    if issues:
        raise ValueError(f"checkpoint_validated_cas_intake_invalid:{issues[0]}")
    return intake


def repository_checkpoint_validated_cas_intake_issues(
    intake: RepositoryCheckpointValidatedCasIntake,
    validation: CheckpointCandidateValidationReceipt,
    contract: RepositoryCheckpointCasContract,
    policy: RepositoryCheckpointValidatedCasIntakePolicy,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_validated_cas_intake(
        intake.intake_id,
        validation,
        contract,
        policy,
    )
    issues: list[str] = []
    if intake.to_dict() != expected.to_dict():
        issues.append("checkpoint_validated_cas_intake_recomputation_mismatch")
    if intake.status not in (INTAKE_READY, INTAKE_CONFLICT, INTAKE_REJECTED):
        issues.append("checkpoint_validated_cas_intake_status_invalid")
    if intake.compare_and_swap_required != (intake.status == INTAKE_READY):
        issues.append("checkpoint_validated_cas_intake_cas_boundary_mismatch")
    if any(
        (
            intake.repository_change_authority_granted,
            intake.execution_performed,
            intake.live_git_command_invoked,
        )
    ):
        issues.append("checkpoint_validated_cas_intake_forbidden_claim")
    if intake.intake_digest != repository_checkpoint_validated_cas_intake_digest(
        intake
    ):
        issues.append("checkpoint_validated_cas_intake_digest_mismatch")
    return tuple(issues)
