#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_READY,
    RepositoryCheckpointCandidate,
    repository_checkpoint_candidate_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import ZERO_OID
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    CONTRACT_NONE,
    CONTRACT_READY,
    CONTRACT_REJECTED,
    REASON_CURRENT_OID_CHANGED,
    REASON_EXPECTED_OID_CONFIRMED,
    REASON_INVALID_EVIDENCE,
    REASON_NO_READY_CANDIDATE,
    RepositoryCheckpointCasContract,
    RepositoryCheckpointCasPolicy,
    repository_checkpoint_cas_contract_digest,
    repository_checkpoint_cas_policy_digest,
)


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_checkpoint_cas_policy(
    policy_id: str,
    *,
    allowed_repository_ids: tuple[str, ...],
    allowed_checkpoint_references: tuple[str, ...],
) -> RepositoryCheckpointCasPolicy:
    policy = RepositoryCheckpointCasPolicy(
        policy_id=policy_id,
        allowed_repository_ids=_canonical(allowed_repository_ids),
        allowed_checkpoint_references=_canonical(allowed_checkpoint_references),
        require_ready_v109_candidate=True,
        require_exact_repository_binding=True,
        require_observed_oid_match=True,
        specification_only=True,
        policy_digest="",
    )
    policy = replace(policy, policy_digest=repository_checkpoint_cas_policy_digest(policy))
    issues = repository_checkpoint_cas_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_cas_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_cas_policy_issues(
    policy: RepositoryCheckpointCasPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_cas_policy_id_missing")
    if policy.allowed_repository_ids != _canonical(policy.allowed_repository_ids):
        issues.append("checkpoint_cas_repository_ids_not_canonical")
    if not policy.allowed_repository_ids:
        issues.append("checkpoint_cas_repository_ids_empty")
    if policy.allowed_checkpoint_references != _canonical(policy.allowed_checkpoint_references):
        issues.append("checkpoint_cas_references_not_canonical")
    if not policy.allowed_checkpoint_references:
        issues.append("checkpoint_cas_references_empty")
    if not all((
        policy.require_ready_v109_candidate,
        policy.require_exact_repository_binding,
        policy.require_observed_oid_match,
        policy.specification_only,
    )):
        issues.append("checkpoint_cas_guard_disabled")
    if policy.policy_digest != repository_checkpoint_cas_policy_digest(policy):
        issues.append("checkpoint_cas_policy_digest_mismatch")
    return tuple(issues)


def construct_repository_checkpoint_cas_contract(
    contract_id: str,
    candidate: RepositoryCheckpointCandidate,
    policy: RepositoryCheckpointCasPolicy,
    *,
    observed_current_oid: str,
) -> RepositoryCheckpointCasContract:
    candidate_valid = candidate.candidate_digest == repository_checkpoint_candidate_digest(candidate)
    policy_valid = not repository_checkpoint_cas_policy_issues(policy)
    binding_exact = bool(
        candidate.repository_id in policy.allowed_repository_ids
        and candidate.checkpoint_reference in policy.allowed_checkpoint_references
    )
    ready_candidate = bool(
        candidate.status == CANDIDATE_READY
        and candidate.dedicated_checkpoint_interface_required
        and not candidate.repository_change_authority_granted
        and not candidate.execution_performed
    )
    distinct_nonzero_oids = bool(
        candidate.expected_current_oid != ZERO_OID
        and candidate.proposed_checkpoint_oid != ZERO_OID
        and candidate.expected_current_oid != candidate.proposed_checkpoint_oid
    )
    observed_oid_well_formed = bool(observed_current_oid and observed_current_oid != ZERO_OID)
    observed_matches_expected = bool(
        observed_oid_well_formed
        and observed_current_oid == candidate.expected_current_oid
    )
    base_valid = candidate_valid and policy_valid and binding_exact

    if not base_valid or (ready_candidate and not distinct_nonzero_oids):
        status = CONTRACT_REJECTED
        reason = REASON_INVALID_EVIDENCE
    elif not ready_candidate:
        status = CONTRACT_NONE
        reason = REASON_NO_READY_CANDIDATE
    elif observed_matches_expected:
        status = CONTRACT_READY
        reason = REASON_EXPECTED_OID_CONFIRMED
    elif observed_oid_well_formed:
        status = CONTRACT_CONFLICT
        reason = REASON_CURRENT_OID_CHANGED
    else:
        status = CONTRACT_REJECTED
        reason = REASON_INVALID_EVIDENCE

    cas_required = status == CONTRACT_READY
    checks = {
        "candidate_valid": candidate_valid,
        "policy_valid": policy_valid,
        "repository_binding_exact": binding_exact,
        "ready_v109_candidate": ready_candidate,
        "distinct_nonzero_oids": distinct_nonzero_oids,
        "observed_oid_well_formed": observed_oid_well_formed,
        "observed_oid_matches_expected": observed_matches_expected,
        "compare_and_swap_required": cas_required,
        "checkpoint_namespace_only": True,
        "repository_change_authority_granted": False,
        "execution_performed": False,
        "live_git_command_invoked": False,
    }
    contract = RepositoryCheckpointCasContract(
        contract_id=contract_id,
        status=status,
        reason=reason,
        candidate_digest=candidate.candidate_digest,
        policy_digest=policy.policy_digest,
        repository_id=candidate.repository_id,
        git_dir_fingerprint=candidate.git_dir_fingerprint,
        checkpoint_reference=candidate.checkpoint_reference,
        expected_current_oid=candidate.expected_current_oid,
        observed_current_oid=observed_current_oid,
        proposed_checkpoint_oid=candidate.proposed_checkpoint_oid,
        compare_and_swap_required=cas_required,
        checkpoint_namespace_only=True,
        repository_change_authority_granted=False,
        execution_performed=False,
        live_git_command_invoked=False,
        checks=checks,
        evidence_digests={
            "checkpoint_candidate": candidate.candidate_digest,
            "checkpoint_cas_policy": policy.policy_digest,
        },
        contract_digest="",
    )
    return replace(contract, contract_digest=repository_checkpoint_cas_contract_digest(contract))


def derive_repository_checkpoint_cas_contract(
    contract_id: str,
    candidate: RepositoryCheckpointCandidate,
    policy: RepositoryCheckpointCasPolicy,
    *,
    observed_current_oid: str,
) -> RepositoryCheckpointCasContract:
    if not contract_id:
        raise ValueError("checkpoint_cas_contract_id_missing")
    contract = construct_repository_checkpoint_cas_contract(
        contract_id, candidate, policy, observed_current_oid=observed_current_oid
    )
    issues = repository_checkpoint_cas_contract_issues(
        contract, candidate, policy, observed_current_oid=observed_current_oid
    )
    if issues:
        raise ValueError(f"checkpoint_cas_contract_invalid:{issues[0]}")
    return contract


def repository_checkpoint_cas_contract_issues(
    contract: RepositoryCheckpointCasContract,
    candidate: RepositoryCheckpointCandidate,
    policy: RepositoryCheckpointCasPolicy,
    *,
    observed_current_oid: str,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_cas_contract(
        contract.contract_id, candidate, policy, observed_current_oid=observed_current_oid
    )
    issues: list[str] = []
    if contract.to_dict() != expected.to_dict():
        issues.append("checkpoint_cas_contract_recomputation_mismatch")
    if contract.status not in (
        CONTRACT_NONE,
        CONTRACT_READY,
        CONTRACT_CONFLICT,
        CONTRACT_REJECTED,
    ):
        issues.append("checkpoint_cas_contract_status_invalid")
    if contract.compare_and_swap_required != (contract.status == CONTRACT_READY):
        issues.append("checkpoint_cas_contract_cas_boundary_mismatch")
    if not contract.checkpoint_namespace_only:
        issues.append("checkpoint_cas_contract_namespace_boundary_missing")
    if any((
        contract.repository_change_authority_granted,
        contract.execution_performed,
        contract.live_git_command_invoked,
    )):
        issues.append("checkpoint_cas_contract_forbidden_claim")
    if contract.contract_digest != repository_checkpoint_cas_contract_digest(contract):
        issues.append("checkpoint_cas_contract_digest_mismatch")
    return tuple(issues)
