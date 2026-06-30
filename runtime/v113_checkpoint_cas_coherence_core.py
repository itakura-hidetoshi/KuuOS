#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    COHERENCE_CONFLICT,
    COHERENCE_READY,
    COHERENCE_REJECTED,
    REASON_COHERENT_CONFLICT,
    REASON_COHERENT_READY,
    REASON_INCOHERENT_EVIDENCE,
    RepositoryCheckpointCasCoherenceReceipt,
    repository_checkpoint_cas_coherence_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    CONTRACT_READY,
    REASON_CURRENT_OID_CHANGED,
    REASON_EXPECTED_OID_CONFIRMED,
    RepositoryCheckpointCasContract,
    repository_checkpoint_cas_contract_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import ZERO_OID
from runtime.kuuos_repository_checkpoint_validated_cas_intake_types_v1_12 import (
    INTAKE_CONFLICT,
    INTAKE_READY,
    REASON_VALIDATED_CONFLICT,
    REASON_VALIDATED_READY,
    RepositoryCheckpointValidatedCasIntake,
    repository_checkpoint_validated_cas_intake_digest,
)


def repository_checkpoint_cas_contract_local_coherence(
    contract: RepositoryCheckpointCasContract,
) -> bool:
    checks = contract.checks
    evidence_exact = bool(
        contract.evidence_digests.get("checkpoint_candidate")
        == contract.candidate_digest
        and contract.evidence_digests.get("checkpoint_cas_policy")
        == contract.policy_digest
    )
    common = all(
        (
            contract.status in (CONTRACT_READY, CONTRACT_CONFLICT),
            bool(contract.contract_id),
            bool(contract.candidate_digest),
            bool(contract.policy_digest),
            bool(contract.repository_id),
            bool(contract.git_dir_fingerprint),
            bool(contract.checkpoint_reference),
            contract.expected_current_oid != ZERO_OID,
            contract.proposed_checkpoint_oid != ZERO_OID,
            contract.expected_current_oid != contract.proposed_checkpoint_oid,
            contract.observed_current_oid != ZERO_OID,
            contract.checkpoint_namespace_only,
            not contract.repository_change_authority_granted,
            not contract.execution_performed,
            not contract.live_git_command_invoked,
            evidence_exact,
            checks.get("candidate_valid") is True,
            checks.get("policy_valid") is True,
            checks.get("repository_binding_exact") is True,
            checks.get("ready_v109_candidate") is True,
            checks.get("distinct_nonzero_oids") is True,
            checks.get("observed_oid_well_formed") is True,
            checks.get("compare_and_swap_required")
            == contract.compare_and_swap_required,
            checks.get("checkpoint_namespace_only")
            == contract.checkpoint_namespace_only,
            checks.get("repository_change_authority_granted")
            == contract.repository_change_authority_granted,
            checks.get("execution_performed") == contract.execution_performed,
            checks.get("live_git_command_invoked")
            == contract.live_git_command_invoked,
        )
    )
    if not common:
        return False

    if contract.status == CONTRACT_READY:
        return all(
            (
                contract.reason == REASON_EXPECTED_OID_CONFIRMED,
                contract.compare_and_swap_required,
                contract.observed_current_oid == contract.expected_current_oid,
                checks.get("observed_oid_matches_expected") is True,
            )
        )
    return all(
        (
            contract.reason == REASON_CURRENT_OID_CHANGED,
            not contract.compare_and_swap_required,
            contract.observed_current_oid != contract.expected_current_oid,
            checks.get("observed_oid_matches_expected") is False,
        )
    )


def repository_checkpoint_validated_cas_intake_local_coherence(
    intake: RepositoryCheckpointValidatedCasIntake,
) -> bool:
    checks = intake.checks
    evidence_exact = bool(
        intake.evidence_digests.get("checkpoint_candidate_validation")
        == intake.validation_digest
        and intake.evidence_digests.get("checkpoint_cas_contract")
        == intake.contract_digest
        and intake.evidence_digests.get("validated_cas_intake_policy")
        == intake.policy_digest
    )
    common = all(
        (
            intake.status in (INTAKE_READY, INTAKE_CONFLICT),
            bool(intake.intake_id),
            bool(intake.validation_digest),
            bool(intake.contract_digest),
            bool(intake.candidate_digest),
            bool(intake.policy_digest),
            bool(intake.repository_id),
            bool(intake.git_dir_fingerprint),
            bool(intake.checkpoint_reference),
            intake.upstream_chain_revalidated,
            intake.validation_receipt_valid,
            intake.contract_valid,
            intake.candidate_binding_exact,
            intake.repository_binding_exact,
            intake.checkpoint_binding_exact,
            intake.oid_binding_exact,
            not intake.repository_change_authority_granted,
            not intake.execution_performed,
            not intake.live_git_command_invoked,
            evidence_exact,
            checks.get("policy_valid") is True,
            checks.get("validation_evidence_exact") is True,
            checks.get("validation_receipt_valid")
            == intake.validation_receipt_valid,
            checks.get("upstream_chain_revalidated")
            == intake.upstream_chain_revalidated,
            checks.get("contract_evidence_exact") is True,
            checks.get("contract_valid") == intake.contract_valid,
            checks.get("candidate_binding_exact")
            == intake.candidate_binding_exact,
            checks.get("repository_binding_exact")
            == intake.repository_binding_exact,
            checks.get("checkpoint_binding_exact")
            == intake.checkpoint_binding_exact,
            checks.get("oid_binding_exact") == intake.oid_binding_exact,
            checks.get("compare_and_swap_required")
            == intake.compare_and_swap_required,
            checks.get("repository_change_authority_granted")
            == intake.repository_change_authority_granted,
            checks.get("execution_performed") == intake.execution_performed,
            checks.get("live_git_command_invoked")
            == intake.live_git_command_invoked,
        )
    )
    if not common:
        return False

    if intake.status == INTAKE_READY:
        return all(
            (
                intake.reason == REASON_VALIDATED_READY,
                intake.compare_and_swap_required,
            )
        )
    return all(
        (
            intake.reason == REASON_VALIDATED_CONFLICT,
            not intake.compare_and_swap_required,
        )
    )


def repository_checkpoint_contract_intake_binding_exact(
    contract: RepositoryCheckpointCasContract,
    intake: RepositoryCheckpointValidatedCasIntake,
) -> bool:
    status_exact = bool(
        (contract.status == CONTRACT_READY and intake.status == INTAKE_READY)
        or (
            contract.status == CONTRACT_CONFLICT
            and intake.status == INTAKE_CONFLICT
        )
    )
    return all(
        (
            intake.contract_digest == contract.contract_digest,
            intake.candidate_digest == contract.candidate_digest,
            intake.repository_id == contract.repository_id,
            intake.git_dir_fingerprint == contract.git_dir_fingerprint,
            intake.checkpoint_reference == contract.checkpoint_reference,
            intake.expected_current_oid == contract.expected_current_oid,
            intake.observed_current_oid == contract.observed_current_oid,
            intake.proposed_checkpoint_oid == contract.proposed_checkpoint_oid,
            intake.compare_and_swap_required
            == contract.compare_and_swap_required,
            status_exact,
        )
    )


def construct_repository_checkpoint_cas_coherence_receipt(
    receipt_id: str,
    contract: RepositoryCheckpointCasContract,
    intake: RepositoryCheckpointValidatedCasIntake,
) -> RepositoryCheckpointCasCoherenceReceipt:
    contract_digest_valid = bool(
        contract.contract_digest == repository_checkpoint_cas_contract_digest(contract)
    )
    contract_local_coherence = repository_checkpoint_cas_contract_local_coherence(
        contract
    )
    intake_digest_valid = bool(
        intake.intake_digest
        == repository_checkpoint_validated_cas_intake_digest(intake)
    )
    intake_local_coherence = (
        repository_checkpoint_validated_cas_intake_local_coherence(intake)
    )
    exact_binding = repository_checkpoint_contract_intake_binding_exact(
        contract,
        intake,
    )
    accepted = all(
        (
            bool(receipt_id),
            contract_digest_valid,
            contract_local_coherence,
            intake_digest_valid,
            intake_local_coherence,
            exact_binding,
        )
    )

    if accepted and contract.status == CONTRACT_READY:
        status = COHERENCE_READY
        reason = REASON_COHERENT_READY
    elif accepted and contract.status == CONTRACT_CONFLICT:
        status = COHERENCE_CONFLICT
        reason = REASON_COHERENT_CONFLICT
    else:
        status = COHERENCE_REJECTED
        reason = REASON_INCOHERENT_EVIDENCE

    cas_required = status == COHERENCE_READY
    receipt = RepositoryCheckpointCasCoherenceReceipt(
        receipt_id=receipt_id,
        status=status,
        reason=reason,
        contract_digest=contract.contract_digest,
        intake_digest=intake.intake_digest,
        candidate_digest=contract.candidate_digest,
        repository_id=contract.repository_id,
        git_dir_fingerprint=contract.git_dir_fingerprint,
        checkpoint_reference=contract.checkpoint_reference,
        expected_current_oid=contract.expected_current_oid,
        observed_current_oid=contract.observed_current_oid,
        proposed_checkpoint_oid=contract.proposed_checkpoint_oid,
        contract_digest_valid=contract_digest_valid,
        contract_local_coherence=contract_local_coherence,
        intake_digest_valid=intake_digest_valid,
        intake_local_coherence=intake_local_coherence,
        exact_contract_intake_binding=exact_binding,
        compare_and_swap_required=cas_required,
        repository_change_authority_granted=False,
        execution_performed=False,
        live_git_command_invoked=False,
        checks={
            "contract_digest_valid": contract_digest_valid,
            "contract_local_coherence": contract_local_coherence,
            "intake_digest_valid": intake_digest_valid,
            "intake_local_coherence": intake_local_coherence,
            "exact_contract_intake_binding": exact_binding,
            "compare_and_swap_required": cas_required,
            "repository_change_authority_granted": False,
            "execution_performed": False,
            "live_git_command_invoked": False,
        },
        evidence_digests={
            "checkpoint_cas_contract": contract.contract_digest,
            "validated_cas_intake": intake.intake_digest,
        },
        coherence_digest="",
    )
    return replace(
        receipt,
        coherence_digest=repository_checkpoint_cas_coherence_digest(receipt),
    )


def derive_repository_checkpoint_cas_coherence_receipt(
    receipt_id: str,
    contract: RepositoryCheckpointCasContract,
    intake: RepositoryCheckpointValidatedCasIntake,
) -> RepositoryCheckpointCasCoherenceReceipt:
    receipt = construct_repository_checkpoint_cas_coherence_receipt(
        receipt_id,
        contract,
        intake,
    )
    issues = repository_checkpoint_cas_coherence_receipt_issues(
        receipt,
        contract,
        intake,
    )
    if issues:
        raise ValueError(f"checkpoint_cas_coherence_receipt_invalid:{issues[0]}")
    return receipt


def repository_checkpoint_cas_coherence_receipt_issues(
    receipt: RepositoryCheckpointCasCoherenceReceipt,
    contract: RepositoryCheckpointCasContract,
    intake: RepositoryCheckpointValidatedCasIntake,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_cas_coherence_receipt(
        receipt.receipt_id,
        contract,
        intake,
    )
    issues: list[str] = []
    if receipt.to_dict() != expected.to_dict():
        issues.append("checkpoint_cas_coherence_recomputation_mismatch")
    if receipt.status not in (
        COHERENCE_READY,
        COHERENCE_CONFLICT,
        COHERENCE_REJECTED,
    ):
        issues.append("checkpoint_cas_coherence_status_invalid")
    if receipt.compare_and_swap_required != (receipt.status == COHERENCE_READY):
        issues.append("checkpoint_cas_coherence_cas_boundary_mismatch")
    if any(
        (
            receipt.repository_change_authority_granted,
            receipt.execution_performed,
            receipt.live_git_command_invoked,
        )
    ):
        issues.append("checkpoint_cas_coherence_forbidden_claim")
    if receipt.coherence_digest != repository_checkpoint_cas_coherence_digest(
        receipt
    ):
        issues.append("checkpoint_cas_coherence_digest_mismatch")
    return tuple(issues)
