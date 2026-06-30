#!/usr/bin/env python3
from dataclasses import replace

from runtime.kuuos_checkpoint_candidate_validation_v1_11 import VALID, checkpoint_candidate_validation_digest
from runtime.kuuos_checkpoint_evidence_envelope_types_v1_12 import (
    ENVELOPE_CONFLICT, ENVELOPE_NONE, ENVELOPE_READY, ENVELOPE_REJECTED,
    CheckpointEvidenceEnvelope, checkpoint_evidence_envelope_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT, CONTRACT_NONE, CONTRACT_READY,
    repository_checkpoint_cas_contract_digest,
)


def derive_checkpoint_evidence_envelope(envelope_id, contract, validation):
    contract_valid = contract.contract_digest == repository_checkpoint_cas_contract_digest(contract)
    validation_valid = (
        validation.status == VALID
        and validation.validation_digest == checkpoint_candidate_validation_digest(validation)
        and validation.upstream_chain_revalidated
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
        envelope_id=envelope_id, status=status,
        contract_digest=contract.contract_digest,
        validation_digest=validation.validation_digest,
        candidate_digest=contract.candidate_digest,
        repository_id=contract.repository_id,
        checkpoint_reference=contract.checkpoint_reference,
        expected_current_oid=contract.expected_current_oid,
        observed_current_oid=contract.observed_current_oid,
        proposed_checkpoint_oid=contract.proposed_checkpoint_oid,
        contract_valid=contract_valid, validation_valid=validation_valid,
        candidate_match=matches[0], repository_match=matches[1],
        checkpoint_match=matches[2], expected_oid_match=matches[3],
        proposed_oid_match=matches[4],
        upstream_revalidated=validation.upstream_chain_revalidated,
        eligible=status == ENVELOPE_READY, operation_performed=False,
        checks={"exact_binding": all(matches), "eligible": status == ENVELOPE_READY},
        evidence_digests={"contract": contract.contract_digest, "validation": validation.validation_digest},
        envelope_digest="",
    )
    return replace(envelope, envelope_digest=checkpoint_evidence_envelope_digest(envelope))
