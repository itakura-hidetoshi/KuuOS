#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace

from runtime.kuuos_repository_alignment_normal_form_v0_80 import (
    certify_repository_alignment_normal_form,
)
from runtime.kuuos_repository_application_authorization_types_v0_91 import (
    AUTHORIZATION_GRANTED,
    RepositoryApplicationAuthorizationCertificate,
    RepositoryApplicationScope,
)
from runtime.kuuos_repository_application_authorization_v0_91 import (
    repository_application_authorization_certificate_issues,
    repository_application_scope_issues,
)
from runtime.kuuos_repository_atomic_application_contracts_v0_92 import (
    build_repository_rollback_material,
    repository_atomic_application_policy_issues,
    repository_authorization_nonce_registry_issues,
    repository_authorized_patch_bundle_issues,
)
from runtime.kuuos_repository_atomic_application_pure_v0_92 import (
    apply_patch_bundle_to_snapshot,
    changed_paths,
    matching_nonce_entries,
    normal_form_certificate_matches_snapshot,
    registry_with_nonce_marked_used,
    rollback_material_restores_source,
)
from runtime.kuuos_repository_atomic_application_receipt_v0_92 import (
    repository_atomic_application_receipt_issues,
    repository_nonce_consumption_receipt_issues,
)
from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    APPLICATION_ABORTED,
    APPLICATION_APPLIED,
    RepositoryAtomicApplicationPolicy,
    RepositoryAtomicApplicationReceipt,
    RepositoryAuthorizationNonceRegistry,
    RepositoryAuthorizedPatchBundle,
    RepositoryNonceConsumptionReceipt,
    RepositoryRollbackMaterial,
    repository_atomic_application_receipt_digest,
    repository_nonce_consumption_receipt_digest,
)
from runtime.kuuos_repository_git_revision_types_v0_83 import (
    GitRevisionObservation,
    git_revision_observation_digest,
)
from runtime.kuuos_repository_structure_observer_v0_79 import (
    observe_repository_structure,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot


def apply_repository_authorized_patch_atomically(
    transaction_id: str,
    authorization: RepositoryApplicationAuthorizationCertificate,
    scope: RepositoryApplicationScope,
    policy: RepositoryAtomicApplicationPolicy,
    patch_bundle: RepositoryAuthorizedPatchBundle,
    source_revision: GitRevisionObservation,
    source_snapshot: RepositorySnapshot,
    nonce_registry: RepositoryAuthorizationNonceRegistry,
    *,
    executor_id: str,
    started_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
) -> tuple[
    RepositorySnapshot,
    RepositoryAuthorizationNonceRegistry,
    RepositoryAtomicApplicationReceipt,
    RepositoryNonceConsumptionReceipt,
    RepositoryRollbackMaterial,
]:
    if not transaction_id:
        raise ValueError("atomic_application_transaction_id_missing")
    authorization_issues = repository_application_authorization_certificate_issues(
        authorization
    )
    if authorization_issues:
        raise ValueError(
            f"application_authorization_certificate_invalid:{authorization_issues[0]}"
        )
    scope_issues = repository_application_scope_issues(scope)
    if scope_issues:
        raise ValueError(f"application_scope_invalid:{scope_issues[0]}")
    policy_issues = repository_atomic_application_policy_issues(policy)
    if policy_issues:
        raise ValueError(f"atomic_application_policy_invalid:{policy_issues[0]}")
    bundle_issues = repository_authorized_patch_bundle_issues(patch_bundle)
    if bundle_issues:
        raise ValueError(f"authorized_patch_bundle_invalid:{bundle_issues[0]}")
    registry_issues = repository_authorization_nonce_registry_issues(nonce_registry)
    if registry_issues:
        raise ValueError(f"authorization_nonce_registry_invalid:{registry_issues[0]}")
    if source_revision.observation_digest != git_revision_observation_digest(
        source_revision
    ):
        raise ValueError("atomic_application_source_revision_digest_mismatch")

    source_observation = observe_repository_structure(source_snapshot)
    authorization_valid = all((
        authorization.status == AUTHORIZATION_GRANTED,
        authorization.application_authorization_granted,
        authorization.single_use_application_eligible,
        not authorization.patch_application_executed,
        not authorization.commit_authority_granted,
        not authorization.reference_mutation_authority_granted,
    ))
    authorization_scope_bound = all((
        authorization.application_scope_digest == scope.scope_digest,
        authorization.patch_bundle_digest == scope.patch_bundle_digest,
        authorization.source_commit_sha == scope.source_commit_sha,
        authorization.source_snapshot_digest == scope.source_snapshot_digest,
        authorization.expected_changed_paths == scope.expected_changed_paths,
        authorization.authorization_nonce == scope.authorization_nonce,
    ))
    transaction_time_order_valid = (
        authorization.evaluated_at_epoch_seconds
        <= started_at_epoch_seconds
        <= completed_at_epoch_seconds
    )
    duration_within_policy = (
        completed_at_epoch_seconds - started_at_epoch_seconds
        <= policy.max_application_duration_seconds
        if started_at_epoch_seconds <= completed_at_epoch_seconds
        else False
    )
    authorization_not_expired = (
        transaction_time_order_valid
        and completed_at_epoch_seconds < scope.expires_at_epoch_seconds
    )
    application_policy_bound = all((
        policy.require_exact_changed_paths,
        policy.require_result_normal_form,
    ))
    executor_authorized = executor_id in policy.authorized_executor_ids

    bundle_paths = tuple(patch.path for patch in patch_bundle.patches)
    patch_paths_unique = len(bundle_paths) == len(set(bundle_paths))
    patch_paths_exact = bundle_paths == scope.expected_changed_paths
    patch_bundle_bound = all((
        patch_bundle.bundle_digest == authorization.patch_bundle_digest,
        patch_bundle.bundle_digest == scope.patch_bundle_digest,
        patch_bundle.source_snapshot_digest == source_snapshot.digest,
        len(patch_bundle.patches) == scope.patch_count,
    ))
    patch_count_within_policy = (
        0 < len(patch_bundle.patches) <= policy.max_patch_count
    )
    source_commit_unchanged = all((
        source_revision.current_commit_sha == scope.source_commit_sha,
        source_revision.current_commit_sha == authorization.source_commit_sha,
    ))
    source_snapshot_unchanged = all((
        source_revision.current_snapshot_digest == source_snapshot.digest,
        source_snapshot.digest == scope.source_snapshot_digest,
        source_snapshot.digest == authorization.source_snapshot_digest,
    ))
    object_database_source = source_revision.object_database_read
    working_tree_ignored = not source_revision.working_tree_read

    nonce_entries = matching_nonce_entries(nonce_registry, scope)
    nonce_registry_bound = len(nonce_entries) == 1
    nonce_unused_before = nonce_registry_bound and not nonce_entries[0].consumed
    nonce_not_revoked = nonce_registry_bound and not nonce_entries[0].revoked

    candidate_snapshot, patch_before_digests_exact = (
        apply_patch_bundle_to_snapshot(source_snapshot, patch_bundle)
    )
    actual_changed_paths = changed_paths(source_snapshot, candidate_snapshot)
    actual_changed_paths_exact = all((
        actual_changed_paths == scope.expected_changed_paths,
        len(actual_changed_paths) <= policy.max_changed_path_count,
    ))
    candidate_observation = observe_repository_structure(candidate_snapshot)
    result_snapshot_materialized = all((
        candidate_snapshot.digest != source_snapshot.digest,
        bool(actual_changed_paths),
    ))
    result_observation_exact = (
        candidate_observation.snapshot_digest == candidate_snapshot.digest
    )

    try:
        normal_form_certificate = certify_repository_alignment_normal_form(
            candidate_snapshot
        )
        result_normal_form_certified = normal_form_certificate_matches_snapshot(
            normal_form_certificate,
            candidate_snapshot,
        )
        normal_form_digest = normal_form_certificate.certificate_digest
    except ValueError:
        result_normal_form_certified = False
        normal_form_digest = ""

    rollback_material = build_repository_rollback_material(
        source_snapshot,
        candidate_snapshot,
        actual_changed_paths,
    )
    rollback_material_exact = rollback_material_restores_source(
        rollback_material,
        source_snapshot,
        candidate_snapshot,
    )

    prerequisites = all((
        authorization_valid,
        authorization_scope_bound,
        authorization_not_expired,
        application_policy_bound,
        executor_authorized,
        transaction_time_order_valid,
        duration_within_policy,
        patch_bundle_bound,
        patch_count_within_policy,
        patch_paths_unique,
        patch_paths_exact,
        patch_before_digests_exact,
        source_commit_unchanged,
        source_snapshot_unchanged,
        object_database_source,
        working_tree_ignored,
        nonce_registry_bound,
        nonce_unused_before,
        nonce_not_revoked,
        actual_changed_paths_exact,
        result_snapshot_materialized,
        result_observation_exact,
        result_normal_form_certified,
        rollback_material_exact,
    ))

    final_snapshot = candidate_snapshot if prerequisites else source_snapshot
    final_registry = (
        registry_with_nonce_marked_used(nonce_registry, scope)
        if prerequisites
        else nonce_registry
    )
    final_observation = observe_repository_structure(final_snapshot)
    consumed_before = nonce_entries[0].consumed if nonce_registry_bound else False
    consumed_after = prerequisites or consumed_before
    revoked = nonce_entries[0].revoked if nonce_registry_bound else False

    nonce_receipt = RepositoryNonceConsumptionReceipt(
        transaction_id=transaction_id,
        authorization_nonce=scope.authorization_nonce,
        authorization_scope_digest=scope.scope_digest,
        registry_before_digest=nonce_registry.registry_digest,
        registry_after_digest=final_registry.registry_digest,
        consumed_before=consumed_before,
        consumed_after=consumed_after,
        revoked=revoked,
        application_committed=prerequisites,
        atomic_with_application=True,
        receipt_digest="",
    )
    nonce_receipt = replace(
        nonce_receipt,
        receipt_digest=repository_nonce_consumption_receipt_digest(nonce_receipt),
    )
    nonce_receipt_issues = repository_nonce_consumption_receipt_issues(
        nonce_receipt
    )
    if nonce_receipt_issues:
        raise ValueError(
            f"nonce_consumption_receipt_invalid:{nonce_receipt_issues[0]}"
        )

    atomic_state_transition = (
        prerequisites
        and final_snapshot.digest == candidate_snapshot.digest
        and final_registry.registry_digest != nonce_registry.registry_digest
        and consumed_after
    ) or (
        not prerequisites
        and final_snapshot.digest == source_snapshot.digest
        and final_registry.registry_digest == nonce_registry.registry_digest
        and consumed_after == consumed_before
    )
    failure_no_effect = (
        not prerequisites
        and final_snapshot.digest == source_snapshot.digest
        and final_registry.registry_digest == nonce_registry.registry_digest
    )

    receipt = RepositoryAtomicApplicationReceipt(
        transaction_id=transaction_id,
        status=APPLICATION_APPLIED if prerequisites else APPLICATION_ABORTED,
        authorization_certificate_digest=authorization.certificate_digest,
        application_scope_digest=scope.scope_digest,
        application_policy_digest=policy.policy_digest,
        patch_bundle_digest=patch_bundle.bundle_digest,
        source_commit_sha=scope.source_commit_sha,
        source_snapshot_digest=source_snapshot.digest,
        candidate_snapshot_digest=candidate_snapshot.digest,
        final_snapshot_digest=final_snapshot.digest,
        source_observation_digest=source_observation.digest,
        candidate_observation_digest=candidate_observation.digest,
        final_observation_digest=final_observation.digest,
        normal_form_certificate_digest=normal_form_digest,
        rollback_material_digest=rollback_material.material_digest,
        nonce_consumption_receipt_digest=nonce_receipt.receipt_digest,
        registry_before_digest=nonce_registry.registry_digest,
        registry_after_digest=final_registry.registry_digest,
        expected_changed_paths=scope.expected_changed_paths,
        actual_changed_paths=actual_changed_paths,
        executor_id=executor_id,
        started_at_epoch_seconds=started_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        authorization_valid=authorization_valid,
        authorization_scope_bound=authorization_scope_bound,
        authorization_not_expired_at_completion=authorization_not_expired,
        application_policy_bound=application_policy_bound,
        executor_authorized=executor_authorized,
        transaction_time_order_valid=transaction_time_order_valid,
        duration_within_policy=duration_within_policy,
        patch_bundle_bound=patch_bundle_bound,
        patch_count_within_policy=patch_count_within_policy,
        patch_paths_unique=patch_paths_unique,
        patch_paths_exact=patch_paths_exact,
        patch_before_digests_exact=patch_before_digests_exact,
        source_commit_unchanged=source_commit_unchanged,
        source_snapshot_unchanged=source_snapshot_unchanged,
        object_database_source=object_database_source,
        working_tree_ignored=working_tree_ignored,
        nonce_registry_bound=nonce_registry_bound,
        nonce_unused_before=nonce_unused_before,
        nonce_not_revoked=nonce_not_revoked,
        actual_changed_paths_exact=actual_changed_paths_exact,
        result_snapshot_materialized=result_snapshot_materialized,
        result_observation_exact=result_observation_exact,
        result_normal_form_certified=result_normal_form_certified,
        rollback_material_exact=rollback_material_exact,
        nonce_consumption_committed=prerequisites,
        application_effect_committed=prerequisites,
        atomic_state_transition=atomic_state_transition,
        failure_no_effect=failure_no_effect,
        isolated_snapshot_only=True,
        live_repository_write_performed=False,
        commit_created=False,
        reference_mutated=False,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=repository_atomic_application_receipt_digest(receipt),
    )
    receipt_issues = repository_atomic_application_receipt_issues(receipt)
    if receipt_issues:
        raise ValueError(f"atomic_application_receipt_invalid:{receipt_issues[0]}")
    return final_snapshot, final_registry, receipt, nonce_receipt, rollback_material
