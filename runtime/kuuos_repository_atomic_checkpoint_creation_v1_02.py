#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Mapping

from runtime.kuuos_checkpoint_authorization_strict_v101 import (
    repository_local_frontier_checkpoint_authorization_certificate_issues,
)
from runtime.kuuos_repository_atomic_checkpoint_creation_types_v1_02 import (
    CHECKPOINT_CREATION_ABORTED,
    CHECKPOINT_CREATION_COMMITTED,
    ZERO_OID,
    RepositoryAtomicCheckpointCreationPolicy,
    RepositoryAtomicCheckpointCreationRequest,
    RepositoryAtomicCheckpointCreationResult,
    RepositoryCheckpointNonceRegistry,
    RepositoryCheckpointState,
    repository_atomic_checkpoint_creation_policy_digest,
    repository_atomic_checkpoint_creation_request_digest,
    repository_atomic_checkpoint_creation_result_digest,
    repository_checkpoint_nonce_registry_digest,
    repository_checkpoint_state_digest,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_types_v1_01 import (
    AUTHORIZATION_GRANTED,
    RepositoryLocalFrontierCheckpointAuthorizationCertificate,
)
from runtime.kuuos_repository_local_frontier_checkpoint_authorization_v1_01 import (
    normalize_repository_checkpoint_reference_name,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_atomic_checkpoint_creation_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    max_execution_duration_seconds: int,
    max_checkpoint_state_age_seconds: int,
    max_nonce_registry_age_seconds: int,
) -> RepositoryAtomicCheckpointCreationPolicy:
    policy = RepositoryAtomicCheckpointCreationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical_strings(authorized_executor_ids),
        max_execution_duration_seconds=max_execution_duration_seconds,
        max_checkpoint_state_age_seconds=max_checkpoint_state_age_seconds,
        max_nonce_registry_age_seconds=max_nonce_registry_age_seconds,
        require_atomic_compare_and_swap_nonexistence=True,
        require_atomic_nonce_consumption=True,
        require_direct_checkpoint_reference=True,
        require_reference_store_source=True,
        require_working_tree_ignored=True,
        require_reflog_ignored=True,
        require_remote_ignored=True,
        allow_checkpoint_overwrite=False,
        allow_reference_delete=False,
        allow_force_update=False,
        allow_tag_creation=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_atomic_checkpoint_creation_policy_digest(policy),
    )
    issues = repository_atomic_checkpoint_creation_policy_issues(policy)
    if issues:
        raise ValueError(f"atomic_checkpoint_creation_policy_invalid:{issues[0]}")
    return policy


def repository_atomic_checkpoint_creation_policy_issues(
    policy: RepositoryAtomicCheckpointCreationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("atomic_checkpoint_policy_id_missing")
    if (
        policy.authorized_executor_ids
        != _canonical_strings(policy.authorized_executor_ids)
        or not policy.authorized_executor_ids
        or any(not value for value in policy.authorized_executor_ids)
    ):
        issues.append("atomic_checkpoint_executor_ids_invalid")
    if any(
        value <= 0
        for value in (
            policy.max_execution_duration_seconds,
            policy.max_checkpoint_state_age_seconds,
            policy.max_nonce_registry_age_seconds,
        )
    ):
        issues.append("atomic_checkpoint_policy_bound_invalid")
    required = (
        policy.require_atomic_compare_and_swap_nonexistence,
        policy.require_atomic_nonce_consumption,
        policy.require_direct_checkpoint_reference,
        policy.require_reference_store_source,
        policy.require_working_tree_ignored,
        policy.require_reflog_ignored,
        policy.require_remote_ignored,
    )
    if not all(required):
        issues.append("atomic_checkpoint_required_safeguard_disabled")
    forbidden = (
        policy.allow_checkpoint_overwrite,
        policy.allow_reference_delete,
        policy.allow_force_update,
        policy.allow_tag_creation,
        policy.allow_push,
    )
    if any(forbidden):
        issues.append("atomic_checkpoint_forbidden_authority_enabled")
    if policy.policy_digest != repository_atomic_checkpoint_creation_policy_digest(
        policy
    ):
        issues.append("atomic_checkpoint_policy_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_state(
    state_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    checkpoint_reference: str,
    current_oid: str,
    direct: bool,
    symbolic: bool,
    reference_store_source: bool,
    working_tree_source: bool,
    reflog_source: bool,
    remote_source: bool,
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryCheckpointState:
    state = RepositoryCheckpointState(
        state_id=state_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        checkpoint_reference=checkpoint_reference,
        current_oid=current_oid,
        direct=direct,
        symbolic=symbolic,
        reference_store_source=reference_store_source,
        working_tree_source=working_tree_source,
        reflog_source=reflog_source,
        remote_source=remote_source,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        state_digest="",
    )
    state = replace(state, state_digest=repository_checkpoint_state_digest(state))
    issues = repository_checkpoint_state_issues(state)
    if issues:
        raise ValueError(f"checkpoint_state_invalid:{issues[0]}")
    return state


def repository_checkpoint_state_issues(
    state: RepositoryCheckpointState,
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
        issues.append("checkpoint_state_required_field_missing")
    if not _HEX64.fullmatch(state.git_dir_fingerprint):
        issues.append("checkpoint_state_git_dir_invalid")
    if not _HEX40.fullmatch(state.current_oid):
        issues.append("checkpoint_state_oid_invalid")
    if (
        normalize_repository_checkpoint_reference_name(state.checkpoint_reference)
        != state.checkpoint_reference
    ):
        issues.append("checkpoint_state_reference_invalid")
    if state.sequence_number < 0:
        issues.append("checkpoint_state_sequence_negative")
    if state.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_state_observed_at_negative")
    if state.state_digest != repository_checkpoint_state_digest(state):
        issues.append("checkpoint_state_digest_mismatch")
    return tuple(issues)


def build_repository_checkpoint_nonce_registry(
    registry_id: str,
    *,
    authority_id: str,
    upstream_snapshot_digest: str,
    consumed_nonces: tuple[str, ...],
    revoked_nonces: tuple[str, ...],
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryCheckpointNonceRegistry:
    registry = RepositoryCheckpointNonceRegistry(
        registry_id=registry_id,
        authority_id=authority_id,
        upstream_snapshot_digest=upstream_snapshot_digest,
        consumed_nonces=_canonical_strings(consumed_nonces),
        revoked_nonces=_canonical_strings(revoked_nonces),
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
    if not registry.registry_id or not registry.authority_id:
        issues.append("checkpoint_nonce_registry_required_field_missing")
    if not _HEX64.fullmatch(registry.upstream_snapshot_digest):
        issues.append("checkpoint_nonce_registry_upstream_digest_invalid")
    if registry.consumed_nonces != _canonical_strings(registry.consumed_nonces):
        issues.append("checkpoint_nonce_registry_consumed_not_canonical")
    if registry.revoked_nonces != _canonical_strings(registry.revoked_nonces):
        issues.append("checkpoint_nonce_registry_revoked_not_canonical")
    if any(not value for value in registry.consumed_nonces + registry.revoked_nonces):
        issues.append("checkpoint_nonce_registry_nonce_invalid")
    if set(registry.consumed_nonces) & set(registry.revoked_nonces):
        issues.append("checkpoint_nonce_registry_state_overlap")
    if registry.sequence_number < 0:
        issues.append("checkpoint_nonce_registry_sequence_negative")
    if registry.observed_at_epoch_seconds < 0:
        issues.append("checkpoint_nonce_registry_observed_at_negative")
    if registry.registry_digest != repository_checkpoint_nonce_registry_digest(
        registry
    ):
        issues.append("checkpoint_nonce_registry_digest_mismatch")
    return tuple(issues)


def build_repository_atomic_checkpoint_creation_request(
    request_id: str,
    transaction_id: str,
    authorization: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    *,
    authorization_scope_digest: str,
    authorization_nonce: str,
    executor_id: str,
    requested_at_epoch_seconds: int,
    create_requested: bool = True,
    overwrite_requested: bool = False,
    delete_requested: bool = False,
    force_update_requested: bool = False,
    tag_creation_requested: bool = False,
    push_requested: bool = False,
) -> RepositoryAtomicCheckpointCreationRequest:
    request = RepositoryAtomicCheckpointCreationRequest(
        request_id=request_id,
        transaction_id=transaction_id,
        authorization_certificate_digest=authorization.certificate_digest,
        authorization_scope_digest=authorization_scope_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        checkpoint_reference=authorization.checkpoint_reference,
        expected_old_oid=authorization.expected_old_oid,
        proposed_new_oid=authorization.proposed_new_oid,
        authorization_nonce=authorization_nonce,
        executor_id=executor_id,
        create_requested=create_requested,
        overwrite_requested=overwrite_requested,
        delete_requested=delete_requested,
        force_update_requested=force_update_requested,
        tag_creation_requested=tag_creation_requested,
        push_requested=push_requested,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_atomic_checkpoint_creation_request_digest(
            request
        ),
    )
    issues = repository_atomic_checkpoint_creation_request_issues(request)
    if issues:
        raise ValueError(f"atomic_checkpoint_creation_request_invalid:{issues[0]}")
    return request


def repository_atomic_checkpoint_creation_request_issues(
    request: RepositoryAtomicCheckpointCreationRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.request_id,
        request.transaction_id,
        request.repository_id,
        request.checkpoint_reference,
        request.authorization_nonce,
        request.executor_id,
    )
    if any(not value for value in required):
        issues.append("atomic_checkpoint_request_required_field_missing")
    for digest in (
        request.authorization_certificate_digest,
        request.authorization_scope_digest,
        request.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("atomic_checkpoint_request_digest_invalid")
            break
    if request.expected_old_oid != ZERO_OID:
        issues.append("atomic_checkpoint_request_expected_old_not_zero")
    if (
        not _HEX40.fullmatch(request.proposed_new_oid)
        or request.proposed_new_oid == ZERO_OID
    ):
        issues.append("atomic_checkpoint_request_new_oid_invalid")
    if (
        normalize_repository_checkpoint_reference_name(
            request.checkpoint_reference
        )
        != request.checkpoint_reference
    ):
        issues.append("atomic_checkpoint_request_reference_invalid")
    if request.requested_at_epoch_seconds < 0:
        issues.append("atomic_checkpoint_request_time_negative")
    if request.request_digest != repository_atomic_checkpoint_creation_request_digest(
        request
    ):
        issues.append("atomic_checkpoint_request_digest_mismatch")
    return tuple(issues)


def _validate_authorization(
    authorization: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_local_frontier_checkpoint_authorization_certificate_issues(
            authorization,
            **dict(authorization_inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_authorization_inputs_invalid",)


def _construct_atomic_checkpoint_creation(
    transaction_id: str,
    authorization: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicCheckpointCreationPolicy,
    request: RepositoryAtomicCheckpointCreationRequest,
    source_checkpoint_state: RepositoryCheckpointState,
    source_nonce_registry: RepositoryCheckpointNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[
    RepositoryAtomicCheckpointCreationResult,
    RepositoryCheckpointState,
    RepositoryCheckpointNonceRegistry,
]:
    scope = authorization_inputs.get("scope")
    nonce_status = authorization_inputs.get("nonce_status")
    authorization_issues = _validate_authorization(
        authorization,
        authorization_inputs,
    )
    authorization_valid = not authorization_issues
    authorization_granted = bool(
        authorization_valid
        and authorization.status == AUTHORIZATION_GRANTED
        and authorization.checkpoint_creation_authority_granted
        and authorization.checkpoint_creation_authorized
        and authorization.single_use_checkpoint_creation_eligible
    )
    authorization_binding_exact = bool(
        scope is not None
        and request.authorization_certificate_digest
        == authorization.certificate_digest
        and request.authorization_scope_digest
        == authorization.checkpoint_scope_digest
        == scope.scope_digest
        and request.repository_id
        == authorization.repository_id
        == scope.repository_id
        and request.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        == scope.git_dir_fingerprint
        and request.checkpoint_reference
        == authorization.checkpoint_reference
        == scope.checkpoint_reference
        and request.expected_old_oid
        == authorization.expected_old_oid
        == scope.expected_old_oid
        == ZERO_OID
        and request.proposed_new_oid
        == authorization.proposed_new_oid
        == scope.proposed_new_oid
        and request.authorization_nonce == scope.authorization_nonce
        and request.transaction_id == authorization.transaction_id == scope.transaction_id
    )
    execution_policy_valid = not repository_atomic_checkpoint_creation_policy_issues(
        policy
    )
    request_valid = not repository_atomic_checkpoint_creation_request_issues(request)
    request_binding_exact = bool(
        request.transaction_id == transaction_id
        and request.requested_at_epoch_seconds
        >= authorization.evaluated_at_epoch_seconds
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids

    checkpoint_state_valid = not repository_checkpoint_state_issues(
        source_checkpoint_state
    )
    checkpoint_state_binding_exact = bool(
        source_checkpoint_state.repository_id == authorization.repository_id
        and source_checkpoint_state.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        and source_checkpoint_state.checkpoint_reference
        == authorization.checkpoint_reference
    )
    checkpoint_age = (
        execution_started_at_epoch_seconds
        - source_checkpoint_state.observed_at_epoch_seconds
    )
    checkpoint_state_fresh = bool(
        0 <= checkpoint_age <= policy.max_checkpoint_state_age_seconds
    )
    checkpoint_reference_direct = bool(
        source_checkpoint_state.direct
        and policy.require_direct_checkpoint_reference
    )
    checkpoint_reference_not_symbolic = not source_checkpoint_state.symbolic
    checkpoint_reference_store_source = bool(
        source_checkpoint_state.reference_store_source
        and policy.require_reference_store_source
    )
    checkpoint_working_tree_ignored = bool(
        not source_checkpoint_state.working_tree_source
        and policy.require_working_tree_ignored
    )
    checkpoint_reflog_ignored = bool(
        not source_checkpoint_state.reflog_source
        and policy.require_reflog_ignored
    )
    checkpoint_remote_ignored = bool(
        not source_checkpoint_state.remote_source
        and policy.require_remote_ignored
    )
    checkpoint_absent_before_creation = (
        source_checkpoint_state.current_oid == ZERO_OID
    )
    current_oid_matches_expected_zero = bool(
        source_checkpoint_state.current_oid
        == request.expected_old_oid
        == authorization.expected_old_oid
        == ZERO_OID
    )

    nonce_registry_valid = not repository_checkpoint_nonce_registry_issues(
        source_nonce_registry
    )
    nonce_registry_authority_exact = bool(
        nonce_status is not None
        and source_nonce_registry.authority_id == nonce_status.authority_id
    )
    nonce_registry_snapshot_bound = bool(
        nonce_status is not None
        and source_nonce_registry.upstream_snapshot_digest
        == nonce_status.registry_snapshot_digest
    )
    registry_age = (
        execution_started_at_epoch_seconds
        - source_nonce_registry.observed_at_epoch_seconds
    )
    nonce_registry_fresh = bool(
        0 <= registry_age <= policy.max_nonce_registry_age_seconds
    )
    nonce_unused = bool(
        nonce_status is not None
        and not nonce_status.consumed
        and request.authorization_nonce
        not in source_nonce_registry.consumed_nonces
    )
    nonce_not_revoked = bool(
        nonce_status is not None
        and not nonce_status.revoked
        and request.authorization_nonce
        not in source_nonce_registry.revoked_nonces
    )

    authorization_not_expired_at_execution = bool(
        scope is not None
        and scope.issued_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        <= scope.expires_at_epoch_seconds
    )
    duration = (
        execution_completed_at_epoch_seconds
        - execution_started_at_epoch_seconds
    )
    execution_duration_within_policy = bool(
        0 <= duration <= policy.max_execution_duration_seconds
    )
    no_future_evidence = bool(
        request.requested_at_epoch_seconds <= execution_started_at_epoch_seconds
        and authorization.evaluated_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and source_checkpoint_state.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and source_nonce_registry.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and execution_started_at_epoch_seconds
        <= execution_completed_at_epoch_seconds
    )
    permitted_request_exact = bool(
        request.create_requested
        and not request.overwrite_requested
        and not request.delete_requested
        and not request.force_update_requested
        and not request.tag_creation_requested
        and not request.push_requested
        and not policy.allow_checkpoint_overwrite
        and not policy.allow_reference_delete
        and not policy.allow_force_update
        and not policy.allow_tag_creation
        and not policy.allow_push
    )
    base_ready = all(
        (
            authorization_valid,
            authorization_granted,
            authorization_binding_exact,
            execution_policy_valid,
            request_valid,
            request_binding_exact,
            executor_authorized,
            checkpoint_state_valid,
            checkpoint_state_binding_exact,
            checkpoint_state_fresh,
            checkpoint_reference_direct,
            checkpoint_reference_not_symbolic,
            checkpoint_reference_store_source,
            checkpoint_working_tree_ignored,
            checkpoint_reflog_ignored,
            checkpoint_remote_ignored,
            nonce_registry_valid,
            nonce_registry_authority_exact,
            nonce_registry_snapshot_bound,
            nonce_registry_fresh,
            nonce_unused,
            nonce_not_revoked,
            authorization_not_expired_at_execution,
            execution_duration_within_policy,
            no_future_evidence,
            permitted_request_exact,
            policy.require_atomic_compare_and_swap_nonexistence,
            policy.require_atomic_nonce_consumption,
        )
    )
    compare_and_swap_attempted = base_ready
    compare_and_swap_succeeded = bool(
        compare_and_swap_attempted
        and checkpoint_absent_before_creation
        and current_oid_matches_expected_zero
    )
    committed = compare_and_swap_succeeded

    if committed:
        final_checkpoint_state = build_repository_checkpoint_state(
            f"{source_checkpoint_state.state_id}:{transaction_id}:committed",
            repository_id=source_checkpoint_state.repository_id,
            git_dir_fingerprint=source_checkpoint_state.git_dir_fingerprint,
            checkpoint_reference=source_checkpoint_state.checkpoint_reference,
            current_oid=authorization.proposed_new_oid,
            direct=True,
            symbolic=False,
            reference_store_source=True,
            working_tree_source=False,
            reflog_source=False,
            remote_source=False,
            sequence_number=source_checkpoint_state.sequence_number + 1,
            observed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        )
        final_nonce_registry = build_repository_checkpoint_nonce_registry(
            f"{source_nonce_registry.registry_id}:{transaction_id}:committed",
            authority_id=source_nonce_registry.authority_id,
            upstream_snapshot_digest=source_nonce_registry.registry_digest,
            consumed_nonces=source_nonce_registry.consumed_nonces
            + (request.authorization_nonce,),
            revoked_nonces=source_nonce_registry.revoked_nonces,
            sequence_number=source_nonce_registry.sequence_number + 1,
            observed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        )
    else:
        final_checkpoint_state = source_checkpoint_state
        final_nonce_registry = source_nonce_registry

    result = RepositoryAtomicCheckpointCreationResult(
        transaction_id=transaction_id,
        status=(
            CHECKPOINT_CREATION_COMMITTED
            if committed
            else CHECKPOINT_CREATION_ABORTED
        ),
        authorization_certificate_digest=authorization.certificate_digest,
        execution_policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        source_checkpoint_state_digest=source_checkpoint_state.state_digest,
        final_checkpoint_state_digest=final_checkpoint_state.state_digest,
        source_nonce_registry_digest=source_nonce_registry.registry_digest,
        final_nonce_registry_digest=final_nonce_registry.registry_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        checkpoint_reference=authorization.checkpoint_reference,
        expected_old_oid=authorization.expected_old_oid,
        proposed_new_oid=authorization.proposed_new_oid,
        authorization_nonce=request.authorization_nonce,
        executor_id=request.executor_id,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        authorization_valid=authorization_valid,
        authorization_granted=authorization_granted,
        authorization_binding_exact=authorization_binding_exact,
        execution_policy_valid=execution_policy_valid,
        request_valid=request_valid,
        request_binding_exact=request_binding_exact,
        executor_authorized=executor_authorized,
        checkpoint_state_valid=checkpoint_state_valid,
        checkpoint_state_binding_exact=checkpoint_state_binding_exact,
        checkpoint_state_fresh=checkpoint_state_fresh,
        checkpoint_reference_direct=checkpoint_reference_direct,
        checkpoint_reference_not_symbolic=checkpoint_reference_not_symbolic,
        checkpoint_reference_store_source=checkpoint_reference_store_source,
        checkpoint_working_tree_ignored=checkpoint_working_tree_ignored,
        checkpoint_reflog_ignored=checkpoint_reflog_ignored,
        checkpoint_remote_ignored=checkpoint_remote_ignored,
        checkpoint_absent_before_creation=checkpoint_absent_before_creation,
        current_oid_matches_expected_zero=current_oid_matches_expected_zero,
        nonce_registry_valid=nonce_registry_valid,
        nonce_registry_authority_exact=nonce_registry_authority_exact,
        nonce_registry_snapshot_bound=nonce_registry_snapshot_bound,
        nonce_registry_fresh=nonce_registry_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        authorization_not_expired_at_execution=(
            authorization_not_expired_at_execution
        ),
        execution_duration_within_policy=execution_duration_within_policy,
        no_future_evidence=no_future_evidence,
        compare_and_swap_nonexistence_required=(
            policy.require_atomic_compare_and_swap_nonexistence
        ),
        compare_and_swap_attempted=compare_and_swap_attempted,
        compare_and_swap_succeeded=compare_and_swap_succeeded,
        atomic_nonce_consumption_required=policy.require_atomic_nonce_consumption,
        atomic_checkpoint_nonce_transition=committed,
        checkpoint_creation_transition_committed=committed,
        checkpoint_state_mutated=committed,
        checkpoint_created=committed,
        nonce_consumed=committed,
        failure_preserved_checkpoint_state=bool(
            not committed and final_checkpoint_state == source_checkpoint_state
        ),
        failure_preserved_nonce_registry=bool(
            not committed and final_nonce_registry == source_nonce_registry
        ),
        checkpoint_overwrite_performed=False,
        force_update_performed=False,
        reference_delete_performed=False,
        branch_updated=False,
        tag_updated=False,
        remote_reference_updated=False,
        push_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        object_database_write_performed=False,
        reflog_write_performed=False,
        signing_performed=False,
        live_git_command_invoked=False,
        live_repository_mutated=False,
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_atomic_checkpoint_creation_result_digest(result),
    )
    return result, final_checkpoint_state, final_nonce_registry


def execute_atomic_repository_checkpoint_creation(
    transaction_id: str,
    authorization: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicCheckpointCreationPolicy,
    request: RepositoryAtomicCheckpointCreationRequest,
    source_checkpoint_state: RepositoryCheckpointState,
    source_nonce_registry: RepositoryCheckpointNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[
    RepositoryAtomicCheckpointCreationResult,
    RepositoryCheckpointState,
    RepositoryCheckpointNonceRegistry,
]:
    if not transaction_id:
        raise ValueError("atomic_checkpoint_transaction_id_missing")
    if (
        execution_started_at_epoch_seconds < 0
        or execution_completed_at_epoch_seconds < 0
    ):
        raise ValueError("atomic_checkpoint_execution_time_negative")
    authorization_issues = _validate_authorization(
        authorization,
        authorization_inputs,
    )
    if authorization_issues:
        raise ValueError(
            f"checkpoint_authorization_invalid:{authorization_issues[0]}"
        )
    for issues, prefix in (
        (
            repository_atomic_checkpoint_creation_policy_issues(policy),
            "atomic_checkpoint_policy_invalid",
        ),
        (
            repository_atomic_checkpoint_creation_request_issues(request),
            "atomic_checkpoint_request_invalid",
        ),
        (
            repository_checkpoint_state_issues(source_checkpoint_state),
            "checkpoint_state_invalid",
        ),
        (
            repository_checkpoint_nonce_registry_issues(source_nonce_registry),
            "checkpoint_nonce_registry_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    result, final_state, final_registry = _construct_atomic_checkpoint_creation(
        transaction_id,
        authorization,
        authorization_inputs,
        policy,
        request,
        source_checkpoint_state,
        source_nonce_registry,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
    )
    issues = repository_atomic_checkpoint_creation_result_issues(
        result,
        final_state,
        final_registry,
        authorization,
        authorization_inputs,
        policy,
        request,
        source_checkpoint_state,
        source_nonce_registry,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"atomic_checkpoint_result_invalid:{issues[0]}")
    return result, final_state, final_registry


def repository_atomic_checkpoint_creation_result_issues(
    result: RepositoryAtomicCheckpointCreationResult,
    final_checkpoint_state: RepositoryCheckpointState,
    final_nonce_registry: RepositoryCheckpointNonceRegistry,
    authorization: RepositoryLocalFrontierCheckpointAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicCheckpointCreationPolicy,
    request: RepositoryAtomicCheckpointCreationRequest,
    source_checkpoint_state: RepositoryCheckpointState,
    source_nonce_registry: RepositoryCheckpointNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _validate_authorization(authorization, authorization_inputs):
        issues.append("checkpoint_authorization_invalid")
        return tuple(issues)
    for validator, name in (
        (
            repository_atomic_checkpoint_creation_policy_issues(policy),
            "policy_invalid",
        ),
        (
            repository_atomic_checkpoint_creation_request_issues(request),
            "request_invalid",
        ),
        (
            repository_checkpoint_state_issues(source_checkpoint_state),
            "source_state_invalid",
        ),
        (
            repository_checkpoint_nonce_registry_issues(source_nonce_registry),
            "source_registry_invalid",
        ),
        (
            repository_checkpoint_state_issues(final_checkpoint_state),
            "final_state_invalid",
        ),
        (
            repository_checkpoint_nonce_registry_issues(final_nonce_registry),
            "final_registry_invalid",
        ),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected_result, expected_state, expected_registry = (
        _construct_atomic_checkpoint_creation(
            result.transaction_id,
            authorization,
            authorization_inputs,
            policy,
            request,
            source_checkpoint_state,
            source_nonce_registry,
            execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
            execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        )
    )
    if result.to_dict() != expected_result.to_dict():
        issues.append("atomic_checkpoint_recomputation_mismatch")
    if final_checkpoint_state.to_dict() != expected_state.to_dict():
        issues.append("atomic_checkpoint_final_state_mismatch")
    if final_nonce_registry.to_dict() != expected_registry.to_dict():
        issues.append("atomic_checkpoint_final_registry_mismatch")
    if result.status not in (
        CHECKPOINT_CREATION_COMMITTED,
        CHECKPOINT_CREATION_ABORTED,
    ):
        issues.append("atomic_checkpoint_status_invalid")
    forbidden = (
        result.checkpoint_overwrite_performed,
        result.force_update_performed,
        result.reference_delete_performed,
        result.branch_updated,
        result.tag_updated,
        result.remote_reference_updated,
        result.push_performed,
        result.index_write_performed,
        result.working_tree_write_performed,
        result.object_database_write_performed,
        result.reflog_write_performed,
        result.signing_performed,
        result.live_git_command_invoked,
        result.live_repository_mutated,
    )
    if any(forbidden):
        issues.append("atomic_checkpoint_forbidden_effect")
    if result.status == CHECKPOINT_CREATION_COMMITTED:
        required = (
            result.authorization_valid,
            result.authorization_granted,
            result.authorization_binding_exact,
            result.execution_policy_valid,
            result.request_valid,
            result.request_binding_exact,
            result.executor_authorized,
            result.checkpoint_state_valid,
            result.checkpoint_state_binding_exact,
            result.checkpoint_state_fresh,
            result.checkpoint_reference_direct,
            result.checkpoint_reference_not_symbolic,
            result.checkpoint_reference_store_source,
            result.checkpoint_working_tree_ignored,
            result.checkpoint_reflog_ignored,
            result.checkpoint_remote_ignored,
            result.checkpoint_absent_before_creation,
            result.current_oid_matches_expected_zero,
            result.nonce_registry_valid,
            result.nonce_registry_authority_exact,
            result.nonce_registry_snapshot_bound,
            result.nonce_registry_fresh,
            result.nonce_unused,
            result.nonce_not_revoked,
            result.authorization_not_expired_at_execution,
            result.execution_duration_within_policy,
            result.no_future_evidence,
            result.compare_and_swap_nonexistence_required,
            result.compare_and_swap_attempted,
            result.compare_and_swap_succeeded,
            result.atomic_nonce_consumption_required,
            result.atomic_checkpoint_nonce_transition,
            result.checkpoint_creation_transition_committed,
            result.checkpoint_state_mutated,
            result.checkpoint_created,
            result.nonce_consumed,
        )
        if not all(required):
            issues.append("atomic_checkpoint_committed_invariant_false")
        if final_checkpoint_state.current_oid != result.proposed_new_oid:
            issues.append("atomic_checkpoint_final_oid_mismatch")
        if result.authorization_nonce not in final_nonce_registry.consumed_nonces:
            issues.append("atomic_checkpoint_nonce_not_consumed")
        if final_checkpoint_state.sequence_number != (
            source_checkpoint_state.sequence_number + 1
        ):
            issues.append("atomic_checkpoint_state_sequence_mismatch")
        if final_nonce_registry.sequence_number != (
            source_nonce_registry.sequence_number + 1
        ):
            issues.append("atomic_checkpoint_registry_sequence_mismatch")
    else:
        if final_checkpoint_state != source_checkpoint_state:
            issues.append("atomic_checkpoint_abort_changed_state")
        if final_nonce_registry != source_nonce_registry:
            issues.append("atomic_checkpoint_abort_changed_nonce_registry")
        if not result.failure_preserved_checkpoint_state:
            issues.append("atomic_checkpoint_abort_state_not_preserved")
        if not result.failure_preserved_nonce_registry:
            issues.append("atomic_checkpoint_abort_nonce_not_preserved")
        if any(
            (
                result.compare_and_swap_succeeded,
                result.atomic_checkpoint_nonce_transition,
                result.checkpoint_creation_transition_committed,
                result.checkpoint_state_mutated,
                result.checkpoint_created,
                result.nonce_consumed,
            )
        ):
            issues.append("atomic_checkpoint_abort_effect_present")
    if result.result_digest != repository_atomic_checkpoint_creation_result_digest(
        result
    ):
        issues.append("atomic_checkpoint_result_digest_mismatch")
    return tuple(issues)
