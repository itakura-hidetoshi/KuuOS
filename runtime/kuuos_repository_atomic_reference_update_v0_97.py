#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re
from typing import Any, Mapping

from runtime.kuuos_repository_atomic_reference_update_types_v0_97 import (
    REFERENCE_UPDATE_ABORTED,
    REFERENCE_UPDATE_COMMITTED,
    RepositoryAtomicReferenceUpdatePolicy,
    RepositoryAtomicReferenceUpdateRequest,
    RepositoryAtomicReferenceUpdateResult,
    RepositoryReferenceNonceRegistry,
    RepositoryReferenceState,
    repository_atomic_reference_update_policy_digest,
    repository_atomic_reference_update_request_digest,
    repository_atomic_reference_update_result_digest,
    repository_reference_nonce_registry_digest,
    repository_reference_state_digest,
)
from runtime.kuuos_repository_reference_update_authorization_types_v0_96 import (
    AUTHORIZATION_GRANTED,
    RepositoryReferenceUpdateAuthorizationCertificate,
    ZERO_OID,
)
from runtime.kuuos_repository_reference_update_v0_96 import (
    repository_reference_update_authorization_certificate_issues,
)

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_atomic_reference_update_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    max_execution_duration_seconds: int,
    max_reference_state_age_seconds: int,
    max_nonce_registry_age_seconds: int,
) -> RepositoryAtomicReferenceUpdatePolicy:
    policy = RepositoryAtomicReferenceUpdatePolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical_strings(authorized_executor_ids),
        max_execution_duration_seconds=max_execution_duration_seconds,
        max_reference_state_age_seconds=max_reference_state_age_seconds,
        max_nonce_registry_age_seconds=max_nonce_registry_age_seconds,
        require_atomic_compare_and_swap=True,
        require_atomic_nonce_consumption=True,
        require_direct_local_branch=True,
        require_reference_store_source=True,
        require_working_tree_ignored=True,
        allow_force_update=False,
        allow_reference_delete=False,
        allow_push=False,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_atomic_reference_update_policy_digest(policy),
    )
    issues = repository_atomic_reference_update_policy_issues(policy)
    if issues:
        raise ValueError(f"atomic_reference_update_policy_invalid:{issues[0]}")
    return policy


def repository_atomic_reference_update_policy_issues(
    policy: RepositoryAtomicReferenceUpdatePolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("atomic_reference_update_policy_id_missing")
    if (
        policy.authorized_executor_ids
        != _canonical_strings(policy.authorized_executor_ids)
        or not policy.authorized_executor_ids
        or any(not value for value in policy.authorized_executor_ids)
    ):
        issues.append("atomic_reference_update_executor_ids_invalid")
    if any(
        value <= 0
        for value in (
            policy.max_execution_duration_seconds,
            policy.max_reference_state_age_seconds,
            policy.max_nonce_registry_age_seconds,
        )
    ):
        issues.append("atomic_reference_update_policy_bound_invalid")
    required = (
        policy.require_atomic_compare_and_swap,
        policy.require_atomic_nonce_consumption,
        policy.require_direct_local_branch,
        policy.require_reference_store_source,
        policy.require_working_tree_ignored,
    )
    if not all(required):
        issues.append("atomic_reference_update_required_safeguard_disabled")
    if policy.allow_force_update:
        issues.append("atomic_reference_update_force_policy_forbidden")
    if policy.allow_reference_delete:
        issues.append("atomic_reference_update_delete_policy_forbidden")
    if policy.allow_push:
        issues.append("atomic_reference_update_push_policy_forbidden")
    if policy.policy_digest != repository_atomic_reference_update_policy_digest(policy):
        issues.append("atomic_reference_update_policy_digest_mismatch")
    return tuple(issues)


def build_repository_reference_state(
    state_id: str,
    *,
    repository_id: str,
    git_dir_fingerprint: str,
    target_reference: str,
    current_oid: str,
    direct: bool,
    symbolic: bool,
    reference_store_source: bool,
    working_tree_source: bool,
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryReferenceState:
    state = RepositoryReferenceState(
        state_id=state_id,
        repository_id=repository_id,
        git_dir_fingerprint=git_dir_fingerprint,
        target_reference=target_reference,
        current_oid=current_oid,
        direct=direct,
        symbolic=symbolic,
        reference_store_source=reference_store_source,
        working_tree_source=working_tree_source,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        state_digest="",
    )
    state = replace(state, state_digest=repository_reference_state_digest(state))
    issues = repository_reference_state_issues(state)
    if issues:
        raise ValueError(f"reference_state_invalid:{issues[0]}")
    return state


def repository_reference_state_issues(
    state: RepositoryReferenceState,
) -> tuple[str, ...]:
    issues: list[str] = []
    if any(
        not value
        for value in (
            state.state_id,
            state.repository_id,
            state.git_dir_fingerprint,
            state.target_reference,
        )
    ):
        issues.append("reference_state_required_field_missing")
    if not _HEX64.fullmatch(state.git_dir_fingerprint):
        issues.append("reference_state_git_dir_fingerprint_invalid")
    if not _HEX40.fullmatch(state.current_oid) or state.current_oid == ZERO_OID:
        issues.append("reference_state_oid_invalid")
    if state.sequence_number < 0:
        issues.append("reference_state_sequence_negative")
    if state.observed_at_epoch_seconds < 0:
        issues.append("reference_state_observed_at_negative")
    if state.state_digest != repository_reference_state_digest(state):
        issues.append("reference_state_digest_mismatch")
    return tuple(issues)


def build_repository_reference_nonce_registry(
    registry_id: str,
    *,
    authority_id: str,
    upstream_snapshot_digest: str,
    consumed_nonces: tuple[str, ...],
    revoked_nonces: tuple[str, ...],
    sequence_number: int,
    observed_at_epoch_seconds: int,
) -> RepositoryReferenceNonceRegistry:
    registry = RepositoryReferenceNonceRegistry(
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
        registry_digest=repository_reference_nonce_registry_digest(registry),
    )
    issues = repository_reference_nonce_registry_issues(registry)
    if issues:
        raise ValueError(f"reference_nonce_registry_invalid:{issues[0]}")
    return registry


def repository_reference_nonce_registry_issues(
    registry: RepositoryReferenceNonceRegistry,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not registry.registry_id or not registry.authority_id:
        issues.append("reference_nonce_registry_required_field_missing")
    if not _HEX64.fullmatch(registry.upstream_snapshot_digest):
        issues.append("reference_nonce_registry_upstream_digest_invalid")
    if registry.consumed_nonces != _canonical_strings(registry.consumed_nonces):
        issues.append("reference_nonce_registry_consumed_not_canonical")
    if registry.revoked_nonces != _canonical_strings(registry.revoked_nonces):
        issues.append("reference_nonce_registry_revoked_not_canonical")
    if any(not value for value in registry.consumed_nonces + registry.revoked_nonces):
        issues.append("reference_nonce_registry_nonce_invalid")
    if set(registry.consumed_nonces) & set(registry.revoked_nonces):
        issues.append("reference_nonce_registry_state_overlap")
    if registry.sequence_number < 0:
        issues.append("reference_nonce_registry_sequence_negative")
    if registry.observed_at_epoch_seconds < 0:
        issues.append("reference_nonce_registry_observed_at_negative")
    if registry.registry_digest != repository_reference_nonce_registry_digest(registry):
        issues.append("reference_nonce_registry_digest_mismatch")
    return tuple(issues)


def build_repository_atomic_reference_update_request(
    request_id: str,
    transaction_id: str,
    authorization: RepositoryReferenceUpdateAuthorizationCertificate,
    *,
    authorization_scope_digest: str,
    authorization_nonce: str,
    executor_id: str,
    requested_at_epoch_seconds: int,
    force_update_requested: bool = False,
    delete_requested: bool = False,
    push_requested: bool = False,
) -> RepositoryAtomicReferenceUpdateRequest:
    request = RepositoryAtomicReferenceUpdateRequest(
        request_id=request_id,
        transaction_id=transaction_id,
        authorization_certificate_digest=authorization.certificate_digest,
        authorization_scope_digest=authorization_scope_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        target_reference=authorization.target_reference,
        expected_old_oid=authorization.expected_old_oid,
        proposed_new_oid=authorization.proposed_new_oid,
        authorization_nonce=authorization_nonce,
        executor_id=executor_id,
        force_update_requested=force_update_requested,
        delete_requested=delete_requested,
        push_requested=push_requested,
        requested_at_epoch_seconds=requested_at_epoch_seconds,
        request_digest="",
    )
    request = replace(
        request,
        request_digest=repository_atomic_reference_update_request_digest(request),
    )
    issues = repository_atomic_reference_update_request_issues(request)
    if issues:
        raise ValueError(f"atomic_reference_update_request_invalid:{issues[0]}")
    return request


def repository_atomic_reference_update_request_issues(
    request: RepositoryAtomicReferenceUpdateRequest,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        request.request_id,
        request.transaction_id,
        request.repository_id,
        request.target_reference,
        request.authorization_nonce,
        request.executor_id,
    )
    if any(not value for value in required):
        issues.append("atomic_reference_update_request_required_field_missing")
    for digest in (
        request.authorization_certificate_digest,
        request.authorization_scope_digest,
        request.git_dir_fingerprint,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("atomic_reference_update_request_digest_invalid")
            break
    if not _HEX40.fullmatch(request.expected_old_oid) or request.expected_old_oid == ZERO_OID:
        issues.append("atomic_reference_update_request_old_oid_invalid")
    if not _HEX40.fullmatch(request.proposed_new_oid) or request.proposed_new_oid == ZERO_OID:
        issues.append("atomic_reference_update_request_new_oid_invalid")
    if request.requested_at_epoch_seconds < 0:
        issues.append("atomic_reference_update_request_time_negative")
    if request.request_digest != repository_atomic_reference_update_request_digest(request):
        issues.append("atomic_reference_update_request_digest_mismatch")
    return tuple(issues)


def _validate_authorization(
    authorization: RepositoryReferenceUpdateAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        return repository_reference_update_authorization_certificate_issues(
            authorization,
            **dict(authorization_inputs),
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("reference_update_authorization_inputs_invalid",)


def _construct_atomic_reference_update(
    transaction_id: str,
    authorization: RepositoryReferenceUpdateAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicReferenceUpdatePolicy,
    request: RepositoryAtomicReferenceUpdateRequest,
    source_reference_state: RepositoryReferenceState,
    source_nonce_registry: RepositoryReferenceNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[
    RepositoryAtomicReferenceUpdateResult,
    RepositoryReferenceState,
    RepositoryReferenceNonceRegistry,
]:
    scope = authorization_inputs.get("scope")
    nonce_status = authorization_inputs.get("nonce_status")
    authorization_issues = _validate_authorization(authorization, authorization_inputs)
    authorization_valid = not authorization_issues
    authorization_granted = bool(
        authorization_valid
        and authorization.status == AUTHORIZATION_GRANTED
        and authorization.reference_update_authority_granted
        and authorization.single_use_reference_update_eligible
    )
    authorization_binding_exact = bool(
        scope is not None
        and request.authorization_certificate_digest == authorization.certificate_digest
        and request.authorization_scope_digest == authorization.reference_update_scope_digest
        == scope.scope_digest
        and request.repository_id == authorization.repository_id == scope.repository_id
        and request.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        == scope.git_dir_fingerprint
        and request.target_reference == authorization.target_reference == scope.target_reference
        and request.expected_old_oid == authorization.expected_old_oid == scope.expected_old_oid
        and request.proposed_new_oid == authorization.proposed_new_oid == scope.proposed_new_oid
        and request.authorization_nonce == scope.authorization_nonce
    )
    execution_policy_valid = not repository_atomic_reference_update_policy_issues(policy)
    request_valid = not repository_atomic_reference_update_request_issues(request)
    request_binding_exact = bool(
        request.transaction_id == transaction_id
        and request.requested_at_epoch_seconds >= authorization.evaluated_at_epoch_seconds
    )
    executor_authorized = request.executor_id in policy.authorized_executor_ids

    reference_state_valid = not repository_reference_state_issues(source_reference_state)
    reference_state_binding_exact = bool(
        source_reference_state.repository_id == authorization.repository_id
        and source_reference_state.git_dir_fingerprint == authorization.git_dir_fingerprint
        and source_reference_state.target_reference == authorization.target_reference
    )
    reference_age = execution_started_at_epoch_seconds - source_reference_state.observed_at_epoch_seconds
    reference_state_fresh = bool(
        0 <= reference_age <= policy.max_reference_state_age_seconds
    )
    reference_direct = bool(
        source_reference_state.direct and policy.require_direct_local_branch
    )
    reference_not_symbolic = not source_reference_state.symbolic
    reference_store_source = bool(
        source_reference_state.reference_store_source
        and policy.require_reference_store_source
    )
    reference_working_tree_ignored = bool(
        not source_reference_state.working_tree_source
        and policy.require_working_tree_ignored
    )
    current_oid_matches_expected_old = (
        source_reference_state.current_oid == authorization.expected_old_oid
    )

    nonce_registry_valid = not repository_reference_nonce_registry_issues(
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
    registry_age = execution_started_at_epoch_seconds - source_nonce_registry.observed_at_epoch_seconds
    nonce_registry_fresh = bool(
        0 <= registry_age <= policy.max_nonce_registry_age_seconds
    )
    nonce_unused = bool(
        nonce_status is not None
        and not nonce_status.consumed
        and request.authorization_nonce not in source_nonce_registry.consumed_nonces
    )
    nonce_not_revoked = bool(
        nonce_status is not None
        and not nonce_status.revoked
        and request.authorization_nonce not in source_nonce_registry.revoked_nonces
    )

    authorization_not_expired_at_execution = bool(
        scope is not None
        and scope.issued_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        <= scope.expires_at_epoch_seconds
    )
    execution_duration = (
        execution_completed_at_epoch_seconds - execution_started_at_epoch_seconds
    )
    execution_duration_within_policy = bool(
        0 <= execution_duration <= policy.max_execution_duration_seconds
    )
    no_future_evidence = bool(
        request.requested_at_epoch_seconds <= execution_started_at_epoch_seconds
        and authorization.evaluated_at_epoch_seconds <= execution_started_at_epoch_seconds
        and source_reference_state.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and source_nonce_registry.observed_at_epoch_seconds
        <= execution_started_at_epoch_seconds
        and execution_started_at_epoch_seconds <= execution_completed_at_epoch_seconds
    )

    forbidden_request_absent = bool(
        not request.force_update_requested
        and not request.delete_requested
        and not request.push_requested
        and not policy.allow_force_update
        and not policy.allow_reference_delete
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
            reference_state_valid,
            reference_state_binding_exact,
            reference_state_fresh,
            reference_direct,
            reference_not_symbolic,
            reference_store_source,
            reference_working_tree_ignored,
            nonce_registry_valid,
            nonce_registry_authority_exact,
            nonce_registry_snapshot_bound,
            nonce_registry_fresh,
            nonce_unused,
            nonce_not_revoked,
            authorization_not_expired_at_execution,
            execution_duration_within_policy,
            no_future_evidence,
            forbidden_request_absent,
            policy.require_atomic_compare_and_swap,
            policy.require_atomic_nonce_consumption,
        )
    )
    compare_and_swap_attempted = base_ready
    compare_and_swap_succeeded = bool(
        compare_and_swap_attempted and current_oid_matches_expected_old
    )
    committed = compare_and_swap_succeeded

    if committed:
        final_reference_state = build_repository_reference_state(
            f"{source_reference_state.state_id}:{transaction_id}:committed",
            repository_id=source_reference_state.repository_id,
            git_dir_fingerprint=source_reference_state.git_dir_fingerprint,
            target_reference=source_reference_state.target_reference,
            current_oid=authorization.proposed_new_oid,
            direct=source_reference_state.direct,
            symbolic=source_reference_state.symbolic,
            reference_store_source=True,
            working_tree_source=False,
            sequence_number=source_reference_state.sequence_number + 1,
            observed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        )
        final_nonce_registry = build_repository_reference_nonce_registry(
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
        final_reference_state = source_reference_state
        final_nonce_registry = source_nonce_registry

    result = RepositoryAtomicReferenceUpdateResult(
        transaction_id=transaction_id,
        status=REFERENCE_UPDATE_COMMITTED if committed else REFERENCE_UPDATE_ABORTED,
        authorization_certificate_digest=authorization.certificate_digest,
        execution_policy_digest=policy.policy_digest,
        request_digest=request.request_digest,
        source_reference_state_digest=source_reference_state.state_digest,
        final_reference_state_digest=final_reference_state.state_digest,
        source_nonce_registry_digest=source_nonce_registry.registry_digest,
        final_nonce_registry_digest=final_nonce_registry.registry_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        target_reference=authorization.target_reference,
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
        reference_state_valid=reference_state_valid,
        reference_state_binding_exact=reference_state_binding_exact,
        reference_state_fresh=reference_state_fresh,
        reference_direct=reference_direct,
        reference_not_symbolic=reference_not_symbolic,
        reference_store_source=reference_store_source,
        reference_working_tree_ignored=reference_working_tree_ignored,
        current_oid_matches_expected_old=current_oid_matches_expected_old,
        nonce_registry_valid=nonce_registry_valid,
        nonce_registry_authority_exact=nonce_registry_authority_exact,
        nonce_registry_snapshot_bound=nonce_registry_snapshot_bound,
        nonce_registry_fresh=nonce_registry_fresh,
        nonce_unused=nonce_unused,
        nonce_not_revoked=nonce_not_revoked,
        authorization_not_expired_at_execution=authorization_not_expired_at_execution,
        execution_duration_within_policy=execution_duration_within_policy,
        no_future_evidence=no_future_evidence,
        compare_and_swap_required=policy.require_atomic_compare_and_swap,
        compare_and_swap_attempted=compare_and_swap_attempted,
        compare_and_swap_succeeded=compare_and_swap_succeeded,
        atomic_nonce_consumption_required=policy.require_atomic_nonce_consumption,
        atomic_reference_nonce_transition=committed,
        reference_update_transition_committed=committed,
        reference_state_mutated=committed,
        branch_state_updated=committed,
        nonce_consumed=committed,
        failure_preserved_reference_state=bool(
            not committed and final_reference_state == source_reference_state
        ),
        failure_preserved_nonce_registry=bool(
            not committed and final_nonce_registry == source_nonce_registry
        ),
        force_update_performed=False,
        reference_delete_performed=False,
        head_updated=False,
        tag_updated=False,
        remote_reference_updated=False,
        push_performed=False,
        index_write_performed=False,
        working_tree_write_performed=False,
        object_database_write_performed=False,
        signing_performed=False,
        live_git_command_invoked=False,
        live_repository_mutated=False,
        result_digest="",
    )
    result = replace(
        result,
        result_digest=repository_atomic_reference_update_result_digest(result),
    )
    return result, final_reference_state, final_nonce_registry


def execute_atomic_repository_reference_update(
    transaction_id: str,
    authorization: RepositoryReferenceUpdateAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicReferenceUpdatePolicy,
    request: RepositoryAtomicReferenceUpdateRequest,
    source_reference_state: RepositoryReferenceState,
    source_nonce_registry: RepositoryReferenceNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[
    RepositoryAtomicReferenceUpdateResult,
    RepositoryReferenceState,
    RepositoryReferenceNonceRegistry,
]:
    if not transaction_id:
        raise ValueError("atomic_reference_update_transaction_id_missing")
    if execution_started_at_epoch_seconds < 0 or execution_completed_at_epoch_seconds < 0:
        raise ValueError("atomic_reference_update_execution_time_negative")
    authorization_issues = _validate_authorization(authorization, authorization_inputs)
    if authorization_issues:
        raise ValueError(
            f"reference_update_authorization_invalid:{authorization_issues[0]}"
        )
    for issues, prefix in (
        (
            repository_atomic_reference_update_policy_issues(policy),
            "atomic_reference_update_policy_invalid",
        ),
        (
            repository_atomic_reference_update_request_issues(request),
            "atomic_reference_update_request_invalid",
        ),
        (repository_reference_state_issues(source_reference_state), "reference_state_invalid"),
        (
            repository_reference_nonce_registry_issues(source_nonce_registry),
            "reference_nonce_registry_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")
    result, final_reference_state, final_nonce_registry = (
        _construct_atomic_reference_update(
            transaction_id,
            authorization,
            authorization_inputs,
            policy,
            request,
            source_reference_state,
            source_nonce_registry,
            execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
            execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
        )
    )
    issues = repository_atomic_reference_update_result_issues(
        result,
        final_reference_state,
        final_nonce_registry,
        authorization,
        authorization_inputs,
        policy,
        request,
        source_reference_state,
        source_nonce_registry,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"atomic_reference_update_result_invalid:{issues[0]}")
    return result, final_reference_state, final_nonce_registry


def repository_atomic_reference_update_result_issues(
    result: RepositoryAtomicReferenceUpdateResult,
    final_reference_state: RepositoryReferenceState,
    final_nonce_registry: RepositoryReferenceNonceRegistry,
    authorization: RepositoryReferenceUpdateAuthorizationCertificate,
    authorization_inputs: Mapping[str, Any],
    policy: RepositoryAtomicReferenceUpdatePolicy,
    request: RepositoryAtomicReferenceUpdateRequest,
    source_reference_state: RepositoryReferenceState,
    source_nonce_registry: RepositoryReferenceNonceRegistry,
    *,
    execution_started_at_epoch_seconds: int,
    execution_completed_at_epoch_seconds: int,
) -> tuple[str, ...]:
    issues: list[str] = []
    if _validate_authorization(authorization, authorization_inputs):
        issues.append("reference_update_authorization_invalid")
        return tuple(issues)
    for validator, name in (
        (repository_atomic_reference_update_policy_issues(policy), "policy_invalid"),
        (repository_atomic_reference_update_request_issues(request), "request_invalid"),
        (repository_reference_state_issues(source_reference_state), "source_state_invalid"),
        (repository_reference_nonce_registry_issues(source_nonce_registry), "source_registry_invalid"),
        (repository_reference_state_issues(final_reference_state), "final_state_invalid"),
        (repository_reference_nonce_registry_issues(final_nonce_registry), "final_registry_invalid"),
    ):
        if validator:
            issues.append(name)
            return tuple(issues)
    expected_result, expected_state, expected_registry = _construct_atomic_reference_update(
        result.transaction_id,
        authorization,
        authorization_inputs,
        policy,
        request,
        source_reference_state,
        source_nonce_registry,
        execution_started_at_epoch_seconds=execution_started_at_epoch_seconds,
        execution_completed_at_epoch_seconds=execution_completed_at_epoch_seconds,
    )
    if result.to_dict() != expected_result.to_dict():
        issues.append("atomic_reference_update_recomputation_mismatch")
    if final_reference_state.to_dict() != expected_state.to_dict():
        issues.append("atomic_reference_update_final_state_mismatch")
    if final_nonce_registry.to_dict() != expected_registry.to_dict():
        issues.append("atomic_reference_update_final_registry_mismatch")
    if result.status not in (REFERENCE_UPDATE_COMMITTED, REFERENCE_UPDATE_ABORTED):
        issues.append("atomic_reference_update_status_invalid")
    forbidden = (
        result.force_update_performed,
        result.reference_delete_performed,
        result.head_updated,
        result.tag_updated,
        result.remote_reference_updated,
        result.push_performed,
        result.index_write_performed,
        result.working_tree_write_performed,
        result.object_database_write_performed,
        result.signing_performed,
        result.live_git_command_invoked,
        result.live_repository_mutated,
    )
    if any(forbidden):
        issues.append("atomic_reference_update_forbidden_effect")
    if result.status == REFERENCE_UPDATE_COMMITTED:
        required = (
            result.authorization_valid,
            result.authorization_granted,
            result.authorization_binding_exact,
            result.execution_policy_valid,
            result.request_valid,
            result.request_binding_exact,
            result.executor_authorized,
            result.reference_state_valid,
            result.reference_state_binding_exact,
            result.reference_state_fresh,
            result.reference_direct,
            result.reference_not_symbolic,
            result.reference_store_source,
            result.reference_working_tree_ignored,
            result.current_oid_matches_expected_old,
            result.nonce_registry_valid,
            result.nonce_registry_authority_exact,
            result.nonce_registry_snapshot_bound,
            result.nonce_registry_fresh,
            result.nonce_unused,
            result.nonce_not_revoked,
            result.authorization_not_expired_at_execution,
            result.execution_duration_within_policy,
            result.no_future_evidence,
            result.compare_and_swap_required,
            result.compare_and_swap_attempted,
            result.compare_and_swap_succeeded,
            result.atomic_nonce_consumption_required,
            result.atomic_reference_nonce_transition,
            result.reference_update_transition_committed,
            result.reference_state_mutated,
            result.branch_state_updated,
            result.nonce_consumed,
        )
        if not all(required):
            issues.append("atomic_reference_update_committed_invariant_false")
        if final_reference_state.current_oid != result.proposed_new_oid:
            issues.append("atomic_reference_update_final_oid_mismatch")
        if result.authorization_nonce not in final_nonce_registry.consumed_nonces:
            issues.append("atomic_reference_update_nonce_not_consumed")
    else:
        if final_reference_state != source_reference_state:
            issues.append("atomic_reference_update_abort_changed_reference")
        if final_nonce_registry != source_nonce_registry:
            issues.append("atomic_reference_update_abort_changed_nonce_registry")
        if not result.failure_preserved_reference_state:
            issues.append("atomic_reference_update_abort_reference_not_preserved")
        if not result.failure_preserved_nonce_registry:
            issues.append("atomic_reference_update_abort_nonce_not_preserved")
        if any(
            (
                result.compare_and_swap_succeeded,
                result.atomic_reference_nonce_transition,
                result.reference_update_transition_committed,
                result.reference_state_mutated,
                result.branch_state_updated,
                result.nonce_consumed,
            )
        ):
            issues.append("atomic_reference_update_abort_effect_present")
    if result.result_digest != repository_atomic_reference_update_result_digest(result):
        issues.append("atomic_reference_update_result_digest_mismatch")
    return tuple(issues)
