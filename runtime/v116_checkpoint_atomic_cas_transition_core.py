#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_atomic_cas_transition_types_v1_16 import (
    TRANSITION_ABORTED,
    TRANSITION_COMMITTED,
    RepositoryCheckpointAtomicCasTransitionPolicy,
    RepositoryCheckpointAtomicCasTransitionRequest,
    RepositoryCheckpointAtomicCasTransitionResult,
    RepositoryCheckpointNonceRegistry,
    RepositoryCheckpointReferenceState,
    repository_checkpoint_atomic_cas_transition_policy_digest,
    repository_checkpoint_atomic_cas_transition_request_digest,
    repository_checkpoint_atomic_cas_transition_result_digest,
    repository_checkpoint_nonce_registry_digest,
    repository_checkpoint_reference_state_digest,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_decision_types_v1_15 import (
    DECISION_GRANTED,
    RepositoryCheckpointCasAuthorizationDecisionCertificate,
    RepositoryCheckpointCasAuthorizationDecisionPolicy,
    RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_decision_v1_15 import (
    repository_checkpoint_cas_authorization_decision_certificate_issues,
)
from runtime.kuuos_repository_checkpoint_cas_authorization_request_types_v1_14 import (
    RepositoryCheckpointCasAuthorizationRequest,
    RepositoryCheckpointCasAuthorizationRequestPolicy,
)
from runtime.kuuos_repository_checkpoint_cas_coherence_types_v1_13 import (
    RepositoryCheckpointCasCoherenceReceipt,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_CHECKPOINT_NAMESPACE = "refs/kuuos/checkpoints/"


def _canonical(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _oid_valid(oid: str) -> bool:
    return bool(_HEX40.fullmatch(oid) and oid != "0" * 40)


def build_repository_checkpoint_atomic_cas_transition_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    max_execution_duration_seconds: int,
    max_reference_state_age_seconds: int,
    max_nonce_registry_age_seconds: int,
) -> RepositoryCheckpointAtomicCasTransitionPolicy:
    policy = RepositoryCheckpointAtomicCasTransitionPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical(authorized_executor_ids),
        max_execution_duration_seconds=max_execution_duration_seconds,
        max_reference_state_age_seconds=max_reference_state_age_seconds,
        max_nonce_registry_age_seconds=max_nonce_registry_age_seconds,
        require_atomic_compare_and_swap=True,
        require_atomic_nonce_consumption=True,
        require_checkpoint_namespace=True,
        require_reference_store_source=True,
        require_working_tree_ignored=True,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_push=False,
        modeled_transition_only=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_checkpoint_atomic_cas_transition_policy_digest(policy),
    )
    issues = repository_checkpoint_atomic_cas_transition_policy_issues(policy)
    if issues:
        raise ValueError(f"checkpoint_atomic_cas_transition_policy_invalid:{issues[0]}")
    return policy


def repository_checkpoint_atomic_cas_transition_policy_issues(
    policy: RepositoryCheckpointAtomicCasTransitionPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("checkpoint_atomic_cas_transition_policy_id_missing")
    if policy.authorized_executor_ids != _canonical(policy.authorized_executor_ids):
        issues.append("checkpoint_atomic_cas_transition_executors_not_canonical")
    if not policy.authorized_executor_ids or any(
        not value for value in policy.authorized_executor_ids
    ):
        issues.append("checkpoint_atomic_cas_transition_executors_empty")
    if min(
        policy.max_execution_duration_seconds,
        policy.max_reference_state_age_seconds,
        policy.max_nonce_registry_age_seconds,
    ) <= 0:
        issues.append("checkpoint_atomic_cas_transition_age_or_duration_invalid")
    if not all(
        (
            policy.require_atomic_compare_and_swap,
            policy.require_atomic_nonce_consumption,
            policy.require_checkpoint_namespace,
            policy.require_reference_store_source,
            policy.require_working_tree_ignored,
            policy.modeled_transition_only,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_guard_disabled")
    if any(
        (
            policy.allow_force_update,
            policy.allow_reference_delete,
            policy.allow_push,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_forbidden_capability_enabled")
    if policy.policy_digest != repository_checkpoint_atomic_cas_transition_policy_digest(
        policy
    ):
        issues.append("checkpoint_atomic_cas_transition_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_reference_state(
    state_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    checkpoint_reference: str,
    current_oid: str,
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryCheckpointReferenceState:
    state = RepositoryCheckpointReferenceState(
        state_id=state_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        checkpoint_reference=checkpoint_reference,
        current_oid=current_oid,
        direct=True,
        symbolic=False,
        reference_store_source=True,
        working_tree_source=False,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        state_digest="",
    )
    state = replace(
        state,
        state_digest=repository_checkpoint_reference_state_digest(state),
    )
    issues = repository_checkpoint_reference_state_issues(state)
    if issues:
        raise ValueError(f"checkpoint_reference_state_invalid:{issues[0]}")
    return state


def repository_checkpoint_reference_state_issues(
    state: RepositoryCheckpointReferenceState,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            state.state_id,
            state.repository_id,
            state.git_dir_fingerprint,
            state.checkpoint_reference,
        )
    ):
        issues.append("checkpoint_reference_state_required_field_missing")
    if not state.checkpoint_reference.startswith(_CHECKPOINT_NAMESPACE):
        issues.append("checkpoint_reference_state_namespace_invalid")
    if not _oid_valid(state.current_oid):
        issues.append("checkpoint_reference_state_oid_invalid")
    if not state.direct or state.symbolic:
        issues.append("checkpoint_reference_state_not_direct")
    if not state.reference_store_source or state.working_tree_source:
        issues.append("checkpoint_reference_state_source_invalid")
    if state.sequence_number < 0 or state.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_reference_state_sequence_or_time_invalid")
    if state.state_digest != repository_checkpoint_reference_state_digest(state):
        issues.append("checkpoint_reference_state_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_nonce_registry(
    registry_id: str,
    *,
    authority_id: str,
    upstream_snapshot_digest: str,
    consumed_nonces: tuple[str, ...] = (),
    revoked_nonces: tuple[str, ...] = (),
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryCheckpointNonceRegistry:
    registry = RepositoryCheckpointNonceRegistry(
        registry_id=registry_id,
        authority_id=authority_id,
        upstream_snapshot_digest=upstream_snapshot_digest,
        consumed_nonces=_canonical(consumed_nonces),
        revoked_nonces=_canonical(revoked_nonces),
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        registry_digest="",
    )
    registry = replace(
        registry,
        registry_digest=repository_checkpoint_nonce_registry_digest(registry),
    )
    issues = repository_checkpoint_nonce_registry_issues(registry)
    if issues:
        raise ValueError(f"checkpoint_nonce_registry_invalid:{issues[0]}")
    return registry


def repository_checkpoint_nonce_registry_issues(
    registry: RepositoryCheckpointNonceRegistry,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            registry.registry_id,
            registry.authority_id,
            registry.upstream_snapshot_digest,
        )
    ):
        issues.append("checkpoint_nonce_registry_required_field_missing")
    if registry.consumed_nonces != _canonical(registry.consumed_nonces):
        issues.append("checkpoint_nonce_registry_consumed_not_canonical")
    if registry.revoked_nonces != _canonical(registry.revoked_nonces):
        issues.append("checkpoint_nonce_registry_revoked_not_canonical")
    if set(registry.consumed_nonces).intersection(registry.revoked_nonces):
        issues.append("checkpoint_nonce_registry_consumed_revoked_overlap")
    if registry.sequence_number < 0 or registry.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_nonce_registry_sequence_or_time_invalid")
    if registry.registry_digest != repository_checkpoint_nonce_registry_digest(registry):
        issues.append("checkpoint_nonce_registry_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_atomic_cas_transition_request(
    transaction_id: str,
    authorization: RepositoryCheckpointCasAuthorizationDecisionCertificate,
    *,
    executor_id: str,
    requested_at_epoch_seconds: int,
) -> RepositoryCheckpointAtomicCasTransitionRequest:
    request = RepositoryCheckpointAtomicCasTransitionRequest(
        transaction_id=transaction_id,
        authorization_certificate_digest=authorization.certificate_digest,
        decision_policy_digest=authorization.decision_policy_digest,
        request_digest=authorization.request_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        checkpoint_reference=authorization.checkpoint_reference,
        expected_current_oid=authorization.expected_current_oid,
        proposed_checkpoint_oid=authorization.proposed_checkpoint_oid,
        authorization_nonce=authorization.authorization_nonce,
        executor_id=executor_id,
        force_update_requested=False,
        delete_requested=False,
        push_requested=False,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest_v116="",
    )
    request = replace(
        request,
        request_digest_v116=repository_checkpoint_atomic_cas_transition_request_digest(
            request
        ),
    )
    issues = repository_checkpoint_atomic_cas_transition_request_issues(request)
    if issues:
        raise ValueError(f"checkpoint_atomic_cas_transition_request_invalid:{issues[0]}")
    return request


def repository_checkpoint_atomic_cas_transition_request_issues(
    request: RepositoryCheckpointAtomicCasTransitionRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.transaction_id,
        request.authorization_certificate_digest,
        request.decision_policy_digest,
        request.request_digest,
        request.repository_id,
        request.git_dir_fingerprint,
        request.checkpoint_reference,
        request.authorization_nonce,
        request.executor_id,
    )
    if any(not value for value in required):
        issues.append("checkpoint_atomic_cas_transition_request_field_missing")
    if not request.checkpoint_reference.startswith(_CHECKPOINT_NAMESPACE):
        issues.append("checkpoint_atomic_cas_transition_request_namespace_invalid")
    if not _oid_valid(request.expected_current_oid) or not _oid_valid(
        request.proposed_checkpoint_oid
    ):
        issues.append("checkpoint_atomic_cas_transition_request_oid_invalid")
    if request.expected_current_oid == request.proposed_checkpoint_oid:
        issues.append("checkpoint_atomic_cas_transition_request_oid_not_distinct")
    if any(
        (
            request.force_update_requested,
            request.delete_requested,
            request.push_requested,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_forbidden_request")
    if request.requested_at_epoch_seconds < 0:
        issues.append("checkpoint_atomic_cas_transition_request_time_invalid")
    if request.request_digest_v116 != (
        repository_checkpoint_atomic_cas_transition_request_digest(request)
    ):
        issues.append("checkpoint_atomic_cas_transition_request_digest_mismatch")
    return tuple(issues)


def construct_repository_checkpoint_atomic_cas_transition(
    transition_request: RepositoryCheckpointAtomicCasTransitionRequest,
    authorization: RepositoryCheckpointCasAuthorizationDecisionCertificate,
    upstream_request: RepositoryCheckpointCasAuthorizationRequest,
    coherence_receipt: RepositoryCheckpointCasCoherenceReceipt,
    request_policy: RepositoryCheckpointCasAuthorizationRequestPolicy,
    decision_policy,
    external_decision: RepositoryCheckpointCasExternalAuthorizationDecisionReceipt,
    nonce_status: RepositoryCheckpointCasAuthorizationNonceStatusReceipt,
    transition_policy: RepositoryCheckpointAtomicCasTransitionPolicy,
    source_reference_state: RepositoryCheckpointReferenceState,
    source_nonce_registry: RepositoryCheckpointNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[
    RepositoryCheckpointAtomicCasTransitionResult,
    RepositoryCheckpointReferenceState,
    RepositoryCheckpointNonceRegistry,
]:
    authorization_valid = not (
        repository_checkpoint_cas_authorization_decision_certificate_issues(
            authorization,
            upstream_request,
            coherence_receipt,
            request_policy,
            decision_policy,
            external_decision,
            nonce_status,
            evaluated_at_epoch_seconds=authorization.evaluated_at_epoch_seconds,
        )
    )
    authorization_granted = bool(
        authorization.status == DECISION_GRANTED
        and authorization.authorization_granted
        and authorization.single_use_cas_eligible
        and not authorization.nonce_consumed
        and not authorization.execution_performed
        and not authorization.live_git_command_invoked
        and not authorization.reference_mutated
    )
    authorization_binding_exact = bool(
        transition_request.authorization_certificate_digest
        == authorization.certificate_digest
        and transition_request.decision_policy_digest
        == authorization.decision_policy_digest
        and transition_request.request_digest == authorization.request_digest
        and transition_request.repository_id == authorization.repository_id
        and transition_request.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        and transition_request.checkpoint_reference
        == authorization.checkpoint_reference
        and transition_request.expected_current_oid
        == authorization.expected_current_oid
        and transition_request.proposed_checkpoint_oid
        == authorization.proposed_checkpoint_oid
        and transition_request.authorization_nonce
        == authorization.authorization_nonce
    )
    execution_policy_valid = not repository_checkpoint_atomic_cas_transition_policy_issues(
        transition_policy
    )
    transition_request_valid = not repository_checkpoint_atomic_cas_transition_request_issues(
        transition_request
    )
    transition_request_binding_exact = bool(
        transition_request.authorization_certificate_digest
        == authorization.certificate_digest
        and transition_request.request_digest == upstream_request.request_digest
        and transition_request.decision_policy_digest == decision_policy.policy_digest
    )
    executor_authorized = (
        transition_request.executor_id in transition_policy.authorized_executor_ids
    )
    reference_state_valid = not repository_checkpoint_reference_state_issues(
        source_reference_state
    )
    reference_state_binding_exact = bool(
        source_reference_state.repository_id == authorization.repository_id
        and source_reference_state.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        and source_reference_state.checkpoint_reference
        == authorization.checkpoint_reference
    )
    reference_age = (
        execution_started_at_epoch_seconds
        - source_reference_state.observed_at_epoch_seconds
    )
    reference_state_fresh = bool(
        reference_age >= 0
        and reference_age <= transition_policy.max_reference_state_age_seconds
    )
    current_oid_matches_expected = (
        source_reference_state.current_oid == authorization.expected_current_oid
    )
    nonce_registry_valid = not repository_checkpoint_nonce_registry_issues(
        source_nonce_registry
    )
    nonce_registry_authority_exact = (
        source_nonce_registry.authority_id == authorization.nonce_authority_id
    )
    nonce_registry_snapshot_bound = (
        source_nonce_registry.upstream_snapshot_digest
        == nonce_status.registry_snapshot_digest
    )
    nonce_age = (
        execution_started_at_epoch_seconds
        - source_nonce_registry.observed_at_epoch_seconds
    )
    nonce_registry_fresh = bool(
        nonce_age >= 0
        and nonce_age <= transition_policy.max_nonce_registry_age_seconds
    )
    nonce_unused = authorization.authorization_nonce not in (
        source_nonce_registry.consumed_nonces
    )
    nonce_not_revoked = authorization.authorization_nonce not in (
        source_nonce_registry.revoked_nonces
    )
    authorization_not_expired_at_execution = bool(
        execution_started_at_epoch_seconds >= external_decision.issued_at_epoch_seconds
        and execution_started_at_epoch_seconds
        < external_decision.expires_at_epoch_seconds
        and execution_started_at_epoch_seconds < upstream_request.expires_at_epoch_seconds
    )
    execution_duration = (
        execution_completed_at_epoch_seconds - execution_started_at_epoch_seconds
    )
    execution_duration_within_policy = bool(
        execution_duration >= 0
        and execution_duration <= transition_policy.max_execution_duration_seconds
    )
    no_future_evidence = bool(
        execution_started_at_epoch_seconds >= 0
        and transition_request.requested_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and authorization.evaluated_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and source_reference_state.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and source_nonce_registry.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and execution_completed_at_epoch_seconds >= execution_started_at_epoch_seconds
    )
    compare_and_swap_required = transition_policy.require_atomic_compare_and_swap
    atomic_nonce_consumption_required = (
        transition_policy.require_atomic_nonce_consumption
    )
    preconditions = all(
        (
            authorization_valid,
            authorization_granted,
            authorization_binding_exact,
            execution_policy_valid,
            transition_request_valid,
            transition_request_binding_exact,
            executor_authorized,
            reference_state_valid,
            reference_state_binding_exact,
            reference_state_fresh,
            source_reference_state.direct,
            not source_reference_state.symbolic,
            source_reference_state.reference_store_source,
            not source_reference_state.working_tree_source,
            nonce_registry_valid,
            nonce_registry_authority_exact,
            nonce_registry_snapshot_bound,
            nonce_registry_fresh,
            nonce_unused,
            nonce_not_revoked,
            authorization_not_expired_at_execution,
            execution_duration_within_policy,
            no_future_evidence,
            compare_and_swap_required,
            atomic_nonce_consumption_required,
            not transition_request.force_update_requested,
            not transition_request.delete_requested,
            not transition_request.push_requested,
        )
    )
    compare_and_swap_attempted = preconditions
    compare_and_swap_succeeded = bool(
        compare_and_swap_attempted and current_oid_matches_expected
    )
    committed = compare_and_swap_succeeded

    if committed:
        final_reference_state = RepositoryCheckpointReferenceState(
            state_id=f"{source_reference_state.state_id}:{transition_request.transaction_id}",
            repository_id=source_reference_state.repository_id,
            git_dir_fingerprint=source_reference_state.git_dir_fingerprint,
            checkpoint_reference=source_reference_state.checkpoint_reference,
            current_oid=authorization.proposed_checkpoint_oid,
            direct=True,
            symbolic=False,
            reference_store_source=True,
            working_tree_source=False,
            sequence_number=source_reference_state.sequence_number + 1,
            observed_at_epoch_seconds=execution_completed_at_epoch_seconds,
            state_digest="",
        )
        final_reference_state = replace(
            final_reference_state,
            state_digest=repository_checkpoint_reference_state_digest(
                final_reference_state
            ),
        )
        final_nonce_registry = RepositoryCheckpointNonceRegistry(
            registry_id=f"{source_nonce_registry.registry_id}:{transition_request.transaction_id}",
            authority_id=source_nonce_registry.authority_id,
            upstream_snapshot_digest=source_nonce_registry.registry_digest,
            consumed_nonces=_canonical(
                source_nonce_registry.consumed_nonces
                + (authorization.authorization_nonce,)
            ),
            revoked_nonces=source_nonce_registry.revoked_nonces,
            sequence_number=source_nonce_registry.sequence_number + 1,
            observed_at_epoch_seconds=execution_completed_at_epoch_seconds,
            registry_digest="",
        )
        final_nonce_registry = replace(
            final_nonce_registry,
            registry_digest=repository_checkpoint_nonce_registry_digest(
                final_nonce_registry
            ),
        )
    else:
        final_reference_state = source_reference_state
        final_nonce_registry = source_nonce_registry

    atomic_transition = bool(
        committed
        and final_reference_state.current_oid == authorization.proposed_checkpoint_oid
        and authorization.authorization_nonce in final_nonce_registry.consumed_nonces
        and final_reference_state.sequence_number
        == source_reference_state.sequence_number + 1
        and final_nonce_registry.sequence_number
        == source_nonce_registry.sequence_number + 1
    )
    status = TRANSITION_COMMITTED if committed else TRANSITION_ABORTED
    checks = {
        "authorization_valid": authorization_valid,
        "authorization_granted": authorization_granted,
        "authorization_binding_exact": authorization_binding_exact,
        "execution_policy_valid": execution_policy_valid,
        "transition_request_valid": transition_request_valid,
        "transition_request_binding_exact": transition_request_binding_exact,
        "executor_authorized": executor_authorized,
        "reference_state_valid": reference_state_valid,
        "reference_state_binding_exact": reference_state_binding_exact,
        "reference_state_fresh": reference_state_fresh,
        "current_oid_matches_expected": current_oid_matches_expected,
        "nonce_registry_valid": nonce_registry_valid,
        "nonce_registry_authority_exact": nonce_registry_authority_exact,
        "nonce_registry_snapshot_bound": nonce_registry_snapshot_bound,
        "nonce_registry_fresh": nonce_registry_fresh,
        "nonce_unused": nonce_unused,
        "nonce_not_revoked": nonce_not_revoked,
        "authorization_not_expired_at_execution": authorization_not_expired_at_execution,
        "execution_duration_within_policy": execution_duration_within_policy,
        "no_future_evidence": no_future_evidence,
        "compare_and_swap_attempted": compare_and_swap_attempted,
        "compare_and_swap_succeeded": compare_and_swap_succeeded,
        "atomic_reference_nonce_transition": atomic_transition,
        "transition_committed": committed,
        "live_git_command_invoked": False,
        "live_repository_mutated": False,
    }
    result = RepositoryCheckpointAtomicCasTransitionResult(
        transaction_id=transition_request.transaction_id,
        status=status,
        authorization_certificate_digest=authorization.certificate_digest,
        execution_policy_digest=transition_policy.policy_digest,
        transition_request_digest=transition_request.request_digest_v116,
        source_reference_state_digest=source_reference_state.state_digest,
        final_reference_state_digest=final_reference_state.state_digest,
        source_nonce_registry_digest=source_nonce_registry.registry_digest,
        final_nonce_registry_digest=final_nonce_registry.registry_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        checkpoint_reference=authorization.checkpoint_reference,
        expected_current_oid=authorization.expected_current_oid,
        proposed_checkpoint_oid=authorization.proposed_checkpoint_oid,
        authorization_nonce=authorization.authorization_nonce,
        executor_id=transition_request.executor_id,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        authorization_valid=authorization_valid,
        authorization_granted=authorization_granted,
        authorization_binding_exact=authorization_binding_exact,
        execution_policy_valid=execution_policy_valid,
        transition_request_valid=transition_request_valid,
        transition_request_binding_exact=transition_request_binding_exact,
        executor_authorized=executor_authorized,
        reference_state_valid=reference_state_valid,
        reference_state_binding_exact=reference_state_binding_exact,
        reference_state_fresh=reference_state_fresh,
        reference_direct=source_reference_state.direct,
        reference_not_symbolic=not source_reference_state.symbolic,
        reference_store_source=source_reference_state.reference_store_source,
        reference_working_tree_ignored=not source_reference_state.working_tree_source,
        current_oid_matches_expected=current_oid_matches_expected,
        nonce_registry_valid=nonce_registry_valid,
        nonce_registry_authority_exact=nonce_registry_authority_exact,
        nonce_registry_snapshot_bound=nonce_registry_snapshot_bound,
        nonce_registry_fresh=nonce_registry_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        authorization_not_expired_at_execution=authorization_not_expired_at_execution,
        execution_duration_within_policy=execution_duration_within_policy,
        no_future_evidence=no_future_evidence,
        compare_and_swap_required=compare_and_swap_required,
        compare_and_swap_attempted=compare_and_swap_attempted,
        compare_and_swap_succeeded=compare_and_swap_succeeded,
        atomic_nonce_consumption_required=atomic_nonce_consumption_required,
        atomic_reference_nonce_transition=atomic_transition,
        transition_committed=committed,
        modeled_reference_state_mutated=committed,
        modeled_nonce_registry_mutated=committed,
        nonce_consumed=committed,
        failure_preserved_reference_state=bool(
            not committed
            and final_reference_state.state_digest
            == source_reference_state.state_digest
        ),
        failure_preserved_nonce_registry=bool(
            not committed
            and final_nonce_registry.registry_digest
            == source_nonce_registry.registry_digest
        ),
        force_update_performed=False,
        reference_delete_performed=False,
        push_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        object_database_write_performed=False,
        reflog_write_performed=False,
        signing_performed=False,
        live_git_command_invoked=False,
        live_repository_mutated=False,
        checks=checks,
        evidence_digests={
            "authorization_decision": authorization.certificate_digest,
            "authorization_request": upstream_request.request_digest,
            "coherence_receipt": coherence_receipt.coherence_digest,
            "request_policy": request_policy.policy_digest,
            "decision_policy": decision_policy.policy_digest,
            "external_decision": external_decision.receipt_digest,
            "authorization_nonce_status": nonce_status.receipt_digest,
            "transition_policy": transition_policy.policy_digest,
            "transition_request": transition_request.request_digest_v116,
            "source_reference_state": source_reference_state.state_digest,
            "source_nonce_registry": source_nonce_registry.registry_digest,
        },
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_checkpoint_atomic_cas_transition_result_digest(
            result
        ),
    )
    return result, final_reference_state, final_nonce_registry


def derive_repository_checkpoint_atomic_cas_transition(*args, **kwargs):
    result, final_reference_state, final_nonce_registry = (
        construct_repository_checkpoint_atomic_cas_transition(*args, **kwargs)
    )
    issues = repository_checkpoint_atomic_cas_transition_result_issues(result)
    if issues:
        raise ValueError(f"checkpoint_atomic_cas_transition_invalid:{issues[0]}")
    return result, final_reference_state, final_nonce_registry


def repository_checkpoint_atomic_cas_transition_result_issues(
    result: RepositoryCheckpointAtomicCasTransitionResult,
) -> tuple[str, ...]:
    issues: list[str] = []
    if result.status not in (TRANSITION_COMMITTED, TRANSITION_ABORTED):
        issues.append("checkpoint_atomic_cas_transition_status_invalid")
    committed = result.status == TRANSITION_COMMITTED
    if result.transition_committed != committed:
        issues.append("checkpoint_atomic_cas_transition_commit_flag_mismatch")
    if result.compare_and_swap_succeeded != committed:
        issues.append("checkpoint_atomic_cas_transition_cas_flag_mismatch")
    if result.atomic_reference_nonce_transition != committed:
        issues.append("checkpoint_atomic_cas_transition_atomicity_mismatch")
    if result.nonce_consumed != committed:
        issues.append("checkpoint_atomic_cas_transition_nonce_consumption_mismatch")
    if committed and not all(
        (
            result.modeled_reference_state_mutated,
            result.modeled_nonce_registry_mutated,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_modeled_mutation_missing")
    if not committed and not all(
        (
            result.failure_preserved_reference_state,
            result.failure_preserved_nonce_registry,
            result.source_reference_state_digest
            == result.final_reference_state_digest,
            result.source_nonce_registry_digest
            == result.final_nonce_registry_digest,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_abort_not_preserving")
    if any(
        (
            result.force_update_performed,
            result.reference_delete_performed,
            result.push_performed,
            result.index_write_performed,
            result.working_tree_write_performed,
            result.object_database_write_performed,
            result.reflog_write_performed,
            result.signing_performed,
            result.live_git_command_invoked,
            result.live_repository_mutated,
        )
    ):
        issues.append("checkpoint_atomic_cas_transition_forbidden_live_effect")
    if result.result_digest != repository_checkpoint_atomic_cas_transition_result_digest(
        result
    ):
        issues.append("checkpoint_atomic_cas_transition_result_digest_mismatch")
    return tuple(issues)
