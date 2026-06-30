#!/usr/bin/env python3
from dataclasses import replace

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import (
    VALID,
    checkpoint_candidate_validation_digest,
)
from runtime.kuuos_checkpoint_evidence_envelope_types_v1_12 import (
    ENVELOPE_CONFLICT,
    ENVELOPE_NONE,
    ENVELOPE_READY,
    ENVELOPE_REJECTED,
    CheckpointEvidenceEnvelope,
    checkpoint_evidence_envelope_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    CONTRACT_NONE,
    CONTRACT_READY,
    REASON_CURRENT_OID_CHANGED,
    REASON_EXPECTED_OID_CONFIRMED,
    REASON_NO_READY_CANDIDATE,
    repository_checkpoint_cas_contract_digest,
)
from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import ZERO_OID


def _contract_local_invariants_hold(contract) -> bool:
    checks = contract.checks
    common = all(
        (
            checks.get("candidate_valid") is True,
            checks.get("policy_valid") is True,
            checks.get("repository_binding_exact") is True,
            checks.get("compare_and_swap_required")
            == contract.compare_and_swap_required,
            checks.get("checkpoint_namespace_only")
            == contract.checkpoint_namespace_only,
            checks.get("repository_change_authority_granted")
            == contract.repository_change_authority_granted,
            checks.get("execution_performed") == contract.execution_performed,
            checks.get("live_git_command_invoked")
            == contract.live_git_command_invoked,
            contract.checkpoint_namespace_only,
            not contract.repository_change_authority_granted,
            not contract.execution_performed,
            not contract.live_git_command_invoked,
        )
    )
    if not common:
        return False

    if contract.status == CONTRACT_READY:
        return all(
            (
                contract.reason == REASON_EXPECTED_OID_CONFIRMED,
                contract.compare_and_swap_required,
                contract.observed_current_oid != ZERO_OID,
                contract.observed_current_oid == contract.expected_current_oid,
                checks.get("ready_v109_candidate") is True,
                checks.get("distinct_nonzero_oids") is True,
                checks.get("observed_oid_well_formed") is True,
                checks.get("observed_oid_matches_expected") is True,
            )
        )
    if contract.status == CONTRACT_CONFLICT:
        return all(
            (
                contract.reason == REASON_CURRENT_OID_CHANGED,
                not contract.compare_and_swap_required,
                contract.observed_current_oid != ZERO_OID,
                contract.observed_current_oid != contract.expected_current_oid,
                checks.get("ready_v109_candidate") is True,
                checks.get("distinct_nonzero_oids") is True,
                checks.get("observed_oid_well_formed") is True,
                checks.get("observed_oid_matches_expected") is False,
            )
        )
    if contract.status == CONTRACT_NONE:
        return all(
            (
                contract.reason == REASON_NO_READY_CANDIDATE,
                not contract.compare_and_swap_required,
                checks.get("ready_v109_candidate") is False,
            )
        )
    return False


def derive_checkpoint_evidence_envelope(envelope_id, contract, validation):
    contract_local_invariants = _contract_local_invariants_hold(contract)
    contract_valid = bool(
        contract.contract_digest == repository_checkpoint_cas_contract_digest(contract)
        and contract_local_invariants
    )
    validation_valid = bool(
        validation.status == VALID
        and validation.validation_digest == checkpoint_candidate_validation_digest(validation)
        and validation.upstream_chain_revalidated
        and validation.ready_candidate
        and validation.repository_matches
        and validation.checkpoint_matches
        and validation.distinct_nonzero_oids
        and not validation.operation_performed
    )
    matches = (
        contract.candidate_digest == validation.candidate_digest,
        contract.repository_id == validation.repository_id,
        contract.checkpoint_reference == validation.checkpoint_reference,
        contract.expected_current_oid == validation.expected_current_oid,
        contract.proposed_checkpoint_oid == validation.proposed_checkpoint_oid,
    )
    valid = bool(envelope_id and contract_valid and validation_valid and all(matches))
    if valid and contract.status == CONTRACT_READY and contract.compare_and_swap_required:
        status = ENVELOPE_READY
    elif valid and contract.status == CONTRACT_CONFLICT and not contract.compare_and_swap_required:
        status = ENVELOPE_CONFLICT
    elif valid and contract.status == CONTRACT_NONE and not contract.compare_and_swap_required:
        status = ENVELOPE_NONE
    else:
        status = ENVELOPE_REJECTED
    envelope = CheckpointEvidenceEnvelope(
        envelope_id=envelope_id,
        status=status,
        contract_digest=contract.contract_digest,
        validation_digest=validation.validation_digest,
        candidate_digest=contract.candidate_digest,
        repository_id=contract.repository_id,
        checkpoint_reference=contract.checkpoint_reference,
        expected_current_oid=contract.expected_current_oid,
        observed_current_oid=contract.observed_current_oid,
        proposed_checkpoint_oid=contract.proposed_checkpoint_oid,
        contract_valid=contract_valid,
        validation_valid=validation_valid,
        candidate_match=matches[0],
        repository_match=matches[1],
        checkpoint_match=matches[2],
        expected_oid_match=matches[3],
        proposed_oid_match=matches[4],
        upstream_revalidated=validation.upstream_chain_revalidated,
        eligible=status == ENVELOPE_READY,
        operation_performed=False,
        checks={
            "contract_valid": contract_valid,
            "contract_local_invariants": contract_local_invariants,
            "validation_valid": validation_valid,
            "exact_binding": all(matches),
            "eligible": status == ENVELOPE_READY,
            "operation_performed": False,
        },
        evidence_digests={
            "contract": contract.contract_digest,
            "validation": validation.validation_digest,
            "candidate": contract.candidate_digest,
        },
        envelope_digest="",
    )
    return replace(
        envelope,
        envelope_digest=checkpoint_evidence_envelope_digest(envelope),
    )
