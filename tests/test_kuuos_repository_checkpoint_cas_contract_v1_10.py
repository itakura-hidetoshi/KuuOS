from dataclasses import replace

from runtime.kuuos_repository_checkpoint_candidate_types_v1_09 import (
    CANDIDATE_NONE,
    CANDIDATE_READY,
    REASON_CHECKPOINT_INTERFACE_REQUIRED,
    REASON_CLEAN_NOOP,
    RepositoryCheckpointCandidate,
    repository_checkpoint_candidate_digest,
)
from runtime.kuuos_repository_checkpoint_cas_contract_types_v1_10 import (
    CONTRACT_CONFLICT,
    CONTRACT_NONE,
    CONTRACT_READY,
    CONTRACT_REJECTED,
    REASON_CURRENT_OID_CHANGED,
    REASON_EXPECTED_OID_CONFIRMED,
    REASON_INVALID_EVIDENCE,
    REASON_NO_READY_CANDIDATE,
)
from runtime.v110_checkpoint_cas_contract_core import (
    build_repository_checkpoint_cas_policy,
    derive_repository_checkpoint_cas_contract,
)

REPOSITORY_ID = "repo:kuuos"
CHECKPOINT_REFERENCE = "refs/kuuos/checkpoints/stable"
CURRENT_OID = "1" * 40
PROPOSED_OID = "2" * 40
OTHER_OID = "3" * 40


def candidate(*, ready: bool = True) -> RepositoryCheckpointCandidate:
    value = RepositoryCheckpointCandidate(
        candidate_id="candidate-v109",
        status=CANDIDATE_READY if ready else CANDIDATE_NONE,
        reason=(
            REASON_CHECKPOINT_INTERFACE_REQUIRED if ready else REASON_CLEAN_NOOP
        ),
        namespace_gate_decision_digest="gate-digest",
        candidate_policy_digest="candidate-policy-digest",
        repository_id=REPOSITORY_ID,
        git_dir_fingerprint="git-dir-fingerprint",
        checkpoint_reference=CHECKPOINT_REFERENCE,
        expected_current_oid=CURRENT_OID,
        proposed_checkpoint_oid=PROPOSED_OID,
        dedicated_checkpoint_interface_required=ready,
        human_review_required=False,
        repository_change_authority_granted=False,
        execution_performed=False,
        evaluated_at_epoch_seconds=100,
        checks={},
        evidence_digests={},
        candidate_digest="",
    )
    return replace(value, candidate_digest=repository_checkpoint_candidate_digest(value))


def policy():
    return build_repository_checkpoint_cas_policy(
        "checkpoint-cas-policy-v110",
        allowed_repository_ids=(REPOSITORY_ID,),
        allowed_checkpoint_references=(CHECKPOINT_REFERENCE,),
    )


def test_matching_observation_produces_ready_specification() -> None:
    contract = derive_repository_checkpoint_cas_contract(
        "contract-ready", candidate(), policy(), observed_current_oid=CURRENT_OID
    )
    assert contract.status == CONTRACT_READY
    assert contract.reason == REASON_EXPECTED_OID_CONFIRMED
    assert contract.compare_and_swap_required
    assert not contract.execution_performed
    assert not contract.repository_change_authority_granted


def test_changed_observation_produces_conflict_without_execution() -> None:
    contract = derive_repository_checkpoint_cas_contract(
        "contract-conflict", candidate(), policy(), observed_current_oid=OTHER_OID
    )
    assert contract.status == CONTRACT_CONFLICT
    assert contract.reason == REASON_CURRENT_OID_CHANGED
    assert not contract.compare_and_swap_required
    assert not contract.live_git_command_invoked


def test_nonready_candidate_produces_no_contract() -> None:
    contract = derive_repository_checkpoint_cas_contract(
        "contract-none", candidate(ready=False), policy(), observed_current_oid=CURRENT_OID
    )
    assert contract.status == CONTRACT_NONE
    assert contract.reason == REASON_NO_READY_CANDIDATE


def test_zero_observation_is_rejected() -> None:
    contract = derive_repository_checkpoint_cas_contract(
        "contract-rejected", candidate(), policy(), observed_current_oid="0" * 40
    )
    assert contract.status == CONTRACT_REJECTED
    assert contract.reason == REASON_INVALID_EVIDENCE


def test_same_input_is_deterministic() -> None:
    first = derive_repository_checkpoint_cas_contract(
        "contract-deterministic", candidate(), policy(), observed_current_oid=CURRENT_OID
    )
    second = derive_repository_checkpoint_cas_contract(
        "contract-deterministic", candidate(), policy(), observed_current_oid=CURRENT_OID
    )
    assert first.to_dict() == second.to_dict()
