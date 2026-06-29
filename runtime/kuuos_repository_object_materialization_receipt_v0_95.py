#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_atomic_application_types_v0_92 import (
    RepositoryAtomicApplicationReceipt,
)
from runtime.kuuos_repository_commit_candidate_types_v0_93 import (
    RepositoryCommitCandidateCertificate,
    RepositoryCommitCandidatePolicy,
    RepositoryParentTreeInventory,
)
from runtime.kuuos_repository_object_materialization_authorization_types_v0_94 import (
    AUTHORIZATION_GRANTED,
    GIT_OBJECT_FORMAT_SHA1,
    RepositoryObjectDatabaseEntry,
    RepositoryObjectDatabaseObservation,
    RepositoryObjectMaterializationAuthorizationCertificate,
    RepositoryObjectMaterializationAuthorizationPolicy,
    RepositoryObjectMaterializationNonceStatusReceipt,
    RepositoryObjectMaterializationScope,
)
from runtime.kuuos_repository_object_materialization_authorization_v0_94 import (
    repository_object_database_observation_issues,
    repository_object_materialization_authorization_certificate_issues,
)
from runtime.kuuos_repository_object_materialization_receipt_types_v0_95 import (
    ITEM_REUSED,
    ITEM_WRITTEN,
    MATERIALIZATION_ABORTED,
    MATERIALIZATION_COMMITTED,
    RepositoryObjectMaterializationExecutionItem,
    RepositoryObjectMaterializationExecutionReport,
    RepositoryObjectMaterializationNonceConsumptionReceipt,
    RepositoryObjectMaterializationPolicy,
    RepositoryObjectMaterializationReceipt,
    repository_object_materialization_execution_report_digest,
    repository_object_materialization_nonce_consumption_receipt_digest,
    repository_object_materialization_policy_digest,
    repository_object_materialization_receipt_digest,
)
from runtime.kuuos_repository_structure_types_v0_79 import RepositorySnapshot

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical_strings(values: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def build_repository_object_materialization_policy(
    policy_id: str,
    *,
    authorized_executor_ids: tuple[str, ...],
    max_materialization_duration_seconds: int,
    max_post_observation_age_seconds: int,
) -> RepositoryObjectMaterializationPolicy:
    policy = RepositoryObjectMaterializationPolicy(
        policy_id=policy_id,
        authorized_executor_ids=_canonical_strings(authorized_executor_ids),
        max_materialization_duration_seconds=max_materialization_duration_seconds,
        max_post_observation_age_seconds=max_post_observation_age_seconds,
        require_exact_plan_order=True,
        require_nonce_atomicity=True,
        require_reference_nonmutation=True,
        policy_digest="",
    )
    policy = replace(
        policy,
        policy_digest=repository_object_materialization_policy_digest(policy),
    )
    issues = repository_object_materialization_policy_issues(policy)
    if issues:
        raise ValueError(f"object_materialization_policy_invalid:{issues[0]}")
    return policy


def repository_object_materialization_policy_issues(
    policy: RepositoryObjectMaterializationPolicy,
) -> tuple[str, ...]:
    issues: list[str] = []
    if not policy.policy_id:
        issues.append("object_materialization_policy_id_missing")
    if policy.authorized_executor_ids != _canonical_strings(
        policy.authorized_executor_ids
    ):
        issues.append("object_materialization_executor_ids_not_canonical")
    if not policy.authorized_executor_ids or any(
        not value for value in policy.authorized_executor_ids
    ):
        issues.append("object_materialization_executor_ids_invalid")
    if (
        policy.max_materialization_duration_seconds <= 0
        or policy.max_post_observation_age_seconds <= 0
    ):
        issues.append("object_materialization_policy_bound_invalid")
    if not policy.require_exact_plan_order:
        issues.append("object_materialization_exact_plan_order_not_required")
    if not policy.require_nonce_atomicity:
        issues.append("object_materialization_nonce_atomicity_not_required")
    if not policy.require_reference_nonmutation:
        issues.append("object_materialization_reference_nonmutation_not_required")
    if policy.policy_digest != repository_object_materialization_policy_digest(policy):
        issues.append("object_materialization_policy_digest_mismatch")
    return tuple(issues)


def _expected_execution_items(
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
) -> tuple[RepositoryObjectMaterializationExecutionItem, ...]:
    return tuple(
        RepositoryObjectMaterializationExecutionItem(
            kind=item.kind,
            oid=item.oid,
            payload_size=item.payload_size,
            payload_digest=item.payload_digest,
            outcome=ITEM_WRITTEN if item.write_required else ITEM_REUSED,
            write_order=item.write_order,
        )
        for item in authorization.plan_items
    )


def build_repository_object_materialization_execution_report(
    execution_id: str,
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    *,
    executor_id: str,
    started_at_epoch_seconds: int,
    completed_at_epoch_seconds: int,
    items: tuple[RepositoryObjectMaterializationExecutionItem, ...] | None = None,
    object_database_write_attempted: bool | None = None,
    index_write_performed: bool = False,
    working_tree_write_performed: bool = False,
    reference_mutated: bool = False,
    signing_performed: bool = False,
) -> RepositoryObjectMaterializationExecutionReport:
    report_items = _expected_execution_items(authorization) if items is None else items
    write_attempted = (
        authorization.new_object_count > 0
        if object_database_write_attempted is None
        else object_database_write_attempted
    )
    report = RepositoryObjectMaterializationExecutionReport(
        execution_id=execution_id,
        authorization_certificate_digest=authorization.certificate_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        executor_id=executor_id,
        started_at_epoch_seconds=started_at_epoch_seconds,
        completed_at_epoch_seconds=completed_at_epoch_seconds,
        items=report_items,
        object_database_write_attempted=write_attempted,
        index_write_performed=index_write_performed,
        working_tree_write_performed=working_tree_write_performed,
        reference_mutated=reference_mutated,
        signing_performed=signing_performed,
        report_digest="",
    )
    report = replace(
        report,
        report_digest=repository_object_materialization_execution_report_digest(report),
    )
    issues = repository_object_materialization_execution_report_issues(report)
    if issues:
        raise ValueError(f"object_materialization_execution_report_invalid:{issues[0]}")
    return report


def repository_object_materialization_execution_report_issues(
    report: RepositoryObjectMaterializationExecutionReport,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        report.execution_id,
        report.authorization_certificate_digest,
        report.repository_id,
        report.git_dir_fingerprint,
        report.executor_id,
    )
    if any(not value for value in required):
        issues.append("object_materialization_execution_required_field_missing")
    if not _HEX64.fullmatch(report.authorization_certificate_digest):
        issues.append("object_materialization_execution_authorization_digest_invalid")
    if not _HEX64.fullmatch(report.git_dir_fingerprint):
        issues.append("object_materialization_execution_git_dir_fingerprint_invalid")
    if report.started_at_epoch_seconds < 0:
        issues.append("object_materialization_execution_started_at_negative")
    if report.completed_at_epoch_seconds < 0:
        issues.append("object_materialization_execution_completed_at_negative")
    if not report.items:
        issues.append("object_materialization_execution_items_empty")
    if len({item.oid for item in report.items}) != len(report.items):
        issues.append("object_materialization_execution_oid_duplicate")
    for item in report.items:
        if item.kind not in ("blob", "tree", "commit"):
            issues.append("object_materialization_execution_kind_invalid")
            break
        if not _HEX40.fullmatch(item.oid):
            issues.append("object_materialization_execution_oid_invalid")
            break
        if item.payload_size < 0 or not _HEX64.fullmatch(item.payload_digest):
            issues.append("object_materialization_execution_payload_invalid")
            break
        if item.outcome not in (ITEM_WRITTEN, ITEM_REUSED):
            issues.append("object_materialization_execution_outcome_invalid")
            break
        if item.outcome == ITEM_WRITTEN and item.write_order < 0:
            issues.append("object_materialization_execution_write_order_invalid")
            break
        if item.outcome == ITEM_REUSED and item.write_order != -1:
            issues.append("object_materialization_execution_reuse_order_invalid")
            break
    if report.report_digest != repository_object_materialization_execution_report_digest(
        report
    ):
        issues.append("object_materialization_execution_report_digest_mismatch")
    return tuple(issues)


def build_repository_object_materialization_nonce_consumption_receipt(
    transaction_id: str,
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    scope: RepositoryObjectMaterializationScope,
    *,
    registry_before_digest: str,
    registry_after_digest: str,
    consumed_before: bool,
    consumed_after: bool,
    revoked: bool,
    materialization_committed: bool,
    atomic_with_materialization: bool,
) -> RepositoryObjectMaterializationNonceConsumptionReceipt:
    receipt = RepositoryObjectMaterializationNonceConsumptionReceipt(
        transaction_id=transaction_id,
        authorization_nonce=scope.authorization_nonce,
        authorization_scope_digest=scope.scope_digest,
        authorization_certificate_digest=authorization.certificate_digest,
        registry_before_digest=registry_before_digest,
        registry_after_digest=registry_after_digest,
        consumed_before=consumed_before,
        consumed_after=consumed_after,
        revoked=revoked,
        materialization_committed=materialization_committed,
        atomic_with_materialization=atomic_with_materialization,
        receipt_digest="",
    )
    receipt = replace(
        receipt,
        receipt_digest=(
            repository_object_materialization_nonce_consumption_receipt_digest(receipt)
        ),
    )
    issues = repository_object_materialization_nonce_consumption_receipt_issues(receipt)
    if issues:
        raise ValueError(f"object_materialization_nonce_consumption_invalid:{issues[0]}")
    return receipt


def repository_object_materialization_nonce_consumption_receipt_issues(
    receipt: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        receipt.transaction_id,
        receipt.authorization_nonce,
        receipt.authorization_scope_digest,
        receipt.authorization_certificate_digest,
        receipt.registry_before_digest,
        receipt.registry_after_digest,
    )
    if any(not value for value in required):
        issues.append("object_materialization_nonce_consumption_required_field_missing")
    for digest in (
        receipt.authorization_scope_digest,
        receipt.authorization_certificate_digest,
        receipt.registry_before_digest,
        receipt.registry_after_digest,
    ):
        if not _HEX64.fullmatch(digest):
            issues.append("object_materialization_nonce_consumption_digest_invalid")
            break
    if receipt.registry_before_digest == receipt.registry_after_digest:
        issues.append("object_materialization_nonce_registry_unchanged")
    if receipt.receipt_digest != (
        repository_object_materialization_nonce_consumption_receipt_digest(receipt)
    ):
        issues.append("object_materialization_nonce_consumption_digest_mismatch")
    return tuple(issues)


def _entry_map(
    observation: RepositoryObjectDatabaseObservation,
) -> dict[str, RepositoryObjectDatabaseEntry]:
    return {entry.oid: entry for entry in observation.existing_objects}


def _entry_matches_plan(entry, item) -> bool:
    return bool(
        entry is not None
        and entry.kind == item.kind
        and entry.oid == item.oid
        and entry.payload_size == item.payload_size
        and entry.payload_digest == item.payload_digest
    )


def _execution_identity(item) -> tuple[str, str, int, str]:
    return item.kind, item.oid, item.payload_size, item.payload_digest


def _construct_materialization_receipt(
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    policy: RepositoryObjectMaterializationPolicy,
    scope: RepositoryObjectMaterializationScope,
    pre_observation: RepositoryObjectDatabaseObservation,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> RepositoryObjectMaterializationReceipt:
    expected_items = _expected_execution_items(authorization)
    expected_by_oid = {item.oid: item for item in authorization.plan_items}
    execution_by_oid = {item.oid: item for item in execution_report.items}
    pre_by_oid = _entry_map(pre_observation)
    post_by_oid = _entry_map(post_observation)

    expected_identities = tuple(_execution_identity(item) for item in expected_items)
    actual_identities = tuple(_execution_identity(item) for item in execution_report.items)
    plan_item_set_exact = set(expected_identities) == set(actual_identities)
    plan_order_exact = expected_identities == actual_identities and tuple(
        item.write_order for item in expected_items
    ) == tuple(item.write_order for item in execution_report.items)
    expected_write_oids = {
        item.oid for item in authorization.plan_items if item.write_required
    }
    expected_reuse_oids = {
        item.oid for item in authorization.plan_items if not item.write_required
    }
    actual_write_oids = {
        item.oid for item in execution_report.items if item.outcome == ITEM_WRITTEN
    }
    actual_reuse_oids = {
        item.oid for item in execution_report.items if item.outcome == ITEM_REUSED
    }
    write_set_exact = expected_write_oids == actual_write_oids
    reuse_set_exact = expected_reuse_oids == actual_reuse_oids
    execution_payloads_exact = all(
        oid in expected_by_oid
        and _execution_identity(item)
        == _execution_identity(expected_items[index])
        for index, (oid, item) in enumerate(
            (item.oid, item) for item in execution_report.items
        )
        if index < len(expected_items)
    ) and len(execution_report.items) == len(expected_items)

    expected_queries = _canonical_strings(
        tuple(item.oid for item in authorization.plan_items)
        + (authorization.parent_commit_sha,)
    )
    post_query_set_exact = post_observation.queried_oids == expected_queries
    pre_parent = pre_by_oid.get(authorization.parent_commit_sha)
    post_parent = post_by_oid.get(authorization.parent_commit_sha)
    parent_commit_preserved = bool(
        pre_parent is not None
        and post_parent is not None
        and pre_parent.to_dict() == post_parent.to_dict()
        and post_parent.kind == "commit"
    )
    all_candidate_objects_present = all(
        item.oid in post_by_oid for item in authorization.plan_items
    )
    all_candidate_payloads_exact = all(
        _entry_matches_plan(post_by_oid.get(item.oid), item)
        for item in authorization.plan_items
    )
    reused_objects_preserved = all(
        _entry_matches_plan(pre_by_oid.get(item.oid), item)
        and _entry_matches_plan(post_by_oid.get(item.oid), item)
        for item in authorization.plan_items
        if not item.write_required
    )
    commit_plan = next(
        (item for item in authorization.plan_items if item.kind == "commit"),
        None,
    )
    candidate_commit_present = bool(
        commit_plan is not None
        and commit_plan.oid == authorization.candidate_commit_oid
        and _entry_matches_plan(post_by_oid.get(commit_plan.oid), commit_plan)
    )

    authorization_granted = bool(
        authorization.status == AUTHORIZATION_GRANTED
        and authorization.materialization_authorization_granted
        and authorization.single_use_materialization_eligible
        and authorization.object_database_write_authority_granted
        and authorization.commit_object_materialization_authority_granted
    )
    authorization_binding_exact = bool(
        execution_report.authorization_certificate_digest
        == authorization.certificate_digest
        and nonce_consumption.authorization_certificate_digest
        == authorization.certificate_digest
        and authorization.materialization_scope_digest == scope.scope_digest
        and authorization.object_database_observation_digest
        == pre_observation.receipt_digest
    )
    executor_authorized = execution_report.executor_id in policy.authorized_executor_ids
    transaction_time_order_valid = (
        0
        <= execution_report.started_at_epoch_seconds
        <= execution_report.completed_at_epoch_seconds
        <= post_observation.observed_at_epoch_seconds
    )
    duration_within_policy = (
        execution_report.completed_at_epoch_seconds
        - execution_report.started_at_epoch_seconds
        <= policy.max_materialization_duration_seconds
    )
    execution_report_bound = (
        execution_report.execution_id == nonce_consumption.transaction_id
        and execution_report.authorization_certificate_digest
        == authorization.certificate_digest
    )
    repository_identity_exact = bool(
        execution_report.repository_id == authorization.repository_id
        == pre_observation.repository_id
        == post_observation.repository_id
        and execution_report.git_dir_fingerprint
        == authorization.git_dir_fingerprint
        == pre_observation.git_dir_fingerprint
        == post_observation.git_dir_fingerprint
        and pre_observation.object_format == post_observation.object_format
        == GIT_OBJECT_FORMAT_SHA1
    )
    expected_write_attempt = authorization.new_object_count > 0
    object_database_write_attempted = (
        execution_report.object_database_write_attempted == expected_write_attempt
    )
    post_observation_bound = bool(
        post_observation.source_commit_sha == authorization.parent_commit_sha
        and post_observation.observed_at_epoch_seconds
        >= execution_report.completed_at_epoch_seconds
    )
    post_observation_delay = (
        post_observation.observed_at_epoch_seconds
        - execution_report.completed_at_epoch_seconds
    )
    post_observation_fresh = (
        0 <= post_observation_delay <= policy.max_post_observation_age_seconds
    )
    post_observation_object_database_source = post_observation.object_database_read
    post_observation_working_tree_ignored = not post_observation.working_tree_read

    nonce_scope_bound = bool(
        nonce_consumption.authorization_nonce == scope.authorization_nonce
        and nonce_consumption.authorization_scope_digest == scope.scope_digest
    )
    nonce_authorization_bound = (
        nonce_consumption.authorization_certificate_digest
        == authorization.certificate_digest
    )
    nonce_unused_before = not nonce_consumption.consumed_before
    nonce_consumed_after = nonce_consumption.consumed_after
    nonce_not_revoked = not nonce_consumption.revoked
    nonce_consumption_committed = nonce_consumption.materialization_committed
    nonce_atomic_with_materialization = (
        nonce_consumption.atomic_with_materialization
        and policy.require_nonce_atomicity
    )

    actual_written_object_count = len(actual_write_oids)
    actual_reused_object_count = len(actual_reuse_oids)
    actual_written_payload_bytes = sum(
        item.payload_size
        for item in execution_report.items
        if item.outcome == ITEM_WRITTEN
    )
    counts_exact = (
        actual_written_object_count == authorization.new_object_count
        and actual_reused_object_count == authorization.reused_existing_object_count
        and actual_written_payload_bytes == authorization.new_payload_bytes
    )
    forbidden_effects_absent = not any(
        (
            execution_report.index_write_performed,
            execution_report.working_tree_write_performed,
            execution_report.reference_mutated,
            execution_report.signing_performed,
        )
    )

    commit_object_written = bool(
        commit_plan is not None
        and commit_plan.write_required
        and commit_plan.oid in actual_write_oids
        and candidate_commit_present
    )

    success_inputs = (
        authorization_granted,
        authorization_binding_exact,
        executor_authorized,
        transaction_time_order_valid,
        duration_within_policy,
        execution_report_bound,
        repository_identity_exact,
        plan_item_set_exact,
        plan_order_exact,
        write_set_exact,
        reuse_set_exact,
        execution_payloads_exact,
        object_database_write_attempted,
        post_observation_bound,
        post_observation_fresh,
        post_observation_object_database_source,
        post_observation_working_tree_ignored,
        post_query_set_exact,
        parent_commit_preserved,
        all_candidate_objects_present,
        all_candidate_payloads_exact,
        reused_objects_preserved,
        candidate_commit_present,
        nonce_scope_bound,
        nonce_authorization_bound,
        nonce_unused_before,
        nonce_consumed_after,
        nonce_not_revoked,
        nonce_consumption_committed,
        nonce_atomic_with_materialization,
        counts_exact,
        forbidden_effects_absent,
        policy.require_exact_plan_order,
        policy.require_reference_nonmutation,
    )
    committed = all(success_inputs)
    failure_no_effect = bool(
        not committed
        and not execution_report.object_database_write_attempted
        and not nonce_consumption.consumed_after
        and forbidden_effects_absent
    )

    receipt = RepositoryObjectMaterializationReceipt(
        transaction_id=nonce_consumption.transaction_id,
        status=MATERIALIZATION_COMMITTED if committed else MATERIALIZATION_ABORTED,
        authorization_certificate_digest=authorization.certificate_digest,
        materialization_policy_digest=policy.policy_digest,
        execution_report_digest=execution_report.report_digest,
        pre_observation_digest=pre_observation.receipt_digest,
        post_observation_digest=post_observation.receipt_digest,
        nonce_consumption_receipt_digest=nonce_consumption.receipt_digest,
        repository_id=authorization.repository_id,
        git_dir_fingerprint=authorization.git_dir_fingerprint,
        parent_commit_sha=authorization.parent_commit_sha,
        candidate_commit_oid=authorization.candidate_commit_oid,
        expected_object_count=authorization.unique_candidate_object_count,
        expected_new_object_count=authorization.new_object_count,
        expected_reused_object_count=authorization.reused_existing_object_count,
        expected_new_payload_bytes=authorization.new_payload_bytes,
        actual_written_object_count=actual_written_object_count,
        actual_reused_object_count=actual_reused_object_count,
        actual_written_payload_bytes=actual_written_payload_bytes,
        executor_id=execution_report.executor_id,
        started_at_epoch_seconds=execution_report.started_at_epoch_seconds,
        completed_at_epoch_seconds=execution_report.completed_at_epoch_seconds,
        authorization_valid=True,
        authorization_granted=authorization_granted,
        authorization_binding_exact=authorization_binding_exact,
        materialization_policy_bound=True,
        executor_authorized=executor_authorized,
        transaction_time_order_valid=transaction_time_order_valid,
        duration_within_policy=duration_within_policy,
        execution_report_bound=execution_report_bound,
        repository_identity_exact=repository_identity_exact,
        plan_item_set_exact=plan_item_set_exact,
        plan_order_exact=plan_order_exact,
        write_set_exact=write_set_exact,
        reuse_set_exact=reuse_set_exact,
        execution_payloads_exact=execution_payloads_exact,
        object_database_write_attempted=object_database_write_attempted,
        post_observation_bound=post_observation_bound,
        post_observation_fresh=post_observation_fresh,
        post_observation_object_database_source=(
            post_observation_object_database_source
        ),
        post_observation_working_tree_ignored=(
            post_observation_working_tree_ignored
        ),
        post_query_set_exact=post_query_set_exact,
        parent_commit_preserved=parent_commit_preserved,
        all_candidate_objects_present=all_candidate_objects_present,
        all_candidate_payloads_exact=all_candidate_payloads_exact,
        reused_objects_preserved=reused_objects_preserved,
        candidate_commit_present=candidate_commit_present,
        nonce_scope_bound=nonce_scope_bound,
        nonce_authorization_bound=nonce_authorization_bound,
        nonce_unused_before=nonce_unused_before,
        nonce_consumed_after=nonce_consumed_after,
        nonce_not_revoked=nonce_not_revoked,
        nonce_consumption_committed=nonce_consumption_committed,
        nonce_atomic_with_materialization=nonce_atomic_with_materialization,
        object_database_materialization_committed=committed,
        commit_object_written=commit_object_written,
        atomic_state_transition=committed,
        failure_no_effect=failure_no_effect,
        index_write_performed=execution_report.index_write_performed,
        working_tree_write_performed=execution_report.working_tree_write_performed,
        reference_mutated=execution_report.reference_mutated,
        signing_performed=execution_report.signing_performed,
        receipt_digest="",
    )
    return replace(
        receipt,
        receipt_digest=repository_object_materialization_receipt_digest(receipt),
    )


def certify_repository_object_materialization_receipt(
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    authorization_policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    pre_observation: RepositoryObjectDatabaseObservation,
    pre_nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    policy: RepositoryObjectMaterializationPolicy,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> RepositoryObjectMaterializationReceipt:
    authorization_issues = (
        repository_object_materialization_authorization_certificate_issues(
            authorization,
            candidate_certificate,
            application_receipt,
            snapshot,
            parent_tree_inventory,
            candidate_policy,
            authorization_policy,
            scope,
            pre_observation,
            pre_nonce_status,
            evaluated_at_epoch_seconds=authorization.evaluated_at_epoch_seconds,
        )
    )
    if authorization_issues:
        raise ValueError(
            "object_materialization_authorization_invalid:"
            f"{authorization_issues[0]}"
        )
    for issues, prefix in (
        (
            repository_object_materialization_policy_issues(policy),
            "object_materialization_policy_invalid",
        ),
        (
            repository_object_materialization_execution_report_issues(
                execution_report
            ),
            "object_materialization_execution_report_invalid",
        ),
        (
            repository_object_database_observation_issues(post_observation),
            "object_materialization_post_observation_invalid",
        ),
        (
            repository_object_materialization_nonce_consumption_receipt_issues(
                nonce_consumption
            ),
            "object_materialization_nonce_consumption_invalid",
        ),
    ):
        if issues:
            raise ValueError(f"{prefix}:{issues[0]}")

    receipt = _construct_materialization_receipt(
        authorization,
        policy,
        scope,
        pre_observation,
        execution_report,
        post_observation,
        nonce_consumption,
    )
    issues = repository_object_materialization_receipt_issues(
        receipt,
        authorization,
        candidate_certificate,
        application_receipt,
        snapshot,
        parent_tree_inventory,
        candidate_policy,
        authorization_policy,
        scope,
        pre_observation,
        pre_nonce_status,
        policy,
        execution_report,
        post_observation,
        nonce_consumption,
    )
    if issues:
        raise ValueError(f"object_materialization_receipt_invalid:{issues[0]}")
    return receipt


def repository_object_materialization_receipt_issues(
    receipt: RepositoryObjectMaterializationReceipt,
    authorization: RepositoryObjectMaterializationAuthorizationCertificate,
    candidate_certificate: RepositoryCommitCandidateCertificate,
    application_receipt: RepositoryAtomicApplicationReceipt,
    snapshot: RepositorySnapshot,
    parent_tree_inventory: RepositoryParentTreeInventory,
    candidate_policy: RepositoryCommitCandidatePolicy,
    authorization_policy: RepositoryObjectMaterializationAuthorizationPolicy,
    scope: RepositoryObjectMaterializationScope,
    pre_observation: RepositoryObjectDatabaseObservation,
    pre_nonce_status: RepositoryObjectMaterializationNonceStatusReceipt,
    policy: RepositoryObjectMaterializationPolicy,
    execution_report: RepositoryObjectMaterializationExecutionReport,
    post_observation: RepositoryObjectDatabaseObservation,
    nonce_consumption: RepositoryObjectMaterializationNonceConsumptionReceipt,
) -> tuple[str, ...]:
    issues: list[str] = []
    authorization_issues = (
        repository_object_materialization_authorization_certificate_issues(
            authorization,
            candidate_certificate,
            application_receipt,
            snapshot,
            parent_tree_inventory,
            candidate_policy,
            authorization_policy,
            scope,
            pre_observation,
            pre_nonce_status,
            evaluated_at_epoch_seconds=authorization.evaluated_at_epoch_seconds,
        )
    )
    if authorization_issues:
        issues.append("object_materialization_authorization_invalid")
        return tuple(issues)
    if repository_object_materialization_policy_issues(policy):
        issues.append("object_materialization_policy_invalid")
        return tuple(issues)
    if repository_object_materialization_execution_report_issues(execution_report):
        issues.append("object_materialization_execution_report_invalid")
        return tuple(issues)
    if repository_object_database_observation_issues(post_observation):
        issues.append("object_materialization_post_observation_invalid")
        return tuple(issues)
    if repository_object_materialization_nonce_consumption_receipt_issues(
        nonce_consumption
    ):
        issues.append("object_materialization_nonce_consumption_invalid")
        return tuple(issues)

    expected = _construct_materialization_receipt(
        authorization,
        policy,
        scope,
        pre_observation,
        execution_report,
        post_observation,
        nonce_consumption,
    )
    if receipt.to_dict() != expected.to_dict():
        issues.append("object_materialization_receipt_recomputation_mismatch")
    if receipt.status not in (MATERIALIZATION_COMMITTED, MATERIALIZATION_ABORTED):
        issues.append("object_materialization_receipt_status_invalid")
    if receipt.status == MATERIALIZATION_COMMITTED:
        required_true = (
            receipt.authorization_valid,
            receipt.authorization_granted,
            receipt.authorization_binding_exact,
            receipt.materialization_policy_bound,
            receipt.executor_authorized,
            receipt.transaction_time_order_valid,
            receipt.duration_within_policy,
            receipt.execution_report_bound,
            receipt.repository_identity_exact,
            receipt.plan_item_set_exact,
            receipt.plan_order_exact,
            receipt.write_set_exact,
            receipt.reuse_set_exact,
            receipt.execution_payloads_exact,
            receipt.object_database_write_attempted,
            receipt.post_observation_bound,
            receipt.post_observation_fresh,
            receipt.post_observation_object_database_source,
            receipt.post_observation_working_tree_ignored,
            receipt.post_query_set_exact,
            receipt.parent_commit_preserved,
            receipt.all_candidate_objects_present,
            receipt.all_candidate_payloads_exact,
            receipt.reused_objects_preserved,
            receipt.candidate_commit_present,
            receipt.nonce_scope_bound,
            receipt.nonce_authorization_bound,
            receipt.nonce_unused_before,
            receipt.nonce_consumed_after,
            receipt.nonce_not_revoked,
            receipt.nonce_consumption_committed,
            receipt.nonce_atomic_with_materialization,
            receipt.object_database_materialization_committed,
            receipt.atomic_state_transition,
        )
        if not all(required_true):
            issues.append("object_materialization_committed_invariant_false")
        if any(
            (
                receipt.index_write_performed,
                receipt.working_tree_write_performed,
                receipt.reference_mutated,
                receipt.signing_performed,
            )
        ):
            issues.append("object_materialization_forbidden_effect")
    if receipt.status == MATERIALIZATION_ABORTED and (
        receipt.object_database_materialization_committed
        or receipt.atomic_state_transition
    ):
        issues.append("object_materialization_aborted_with_committed_effect")
    if receipt.receipt_digest != repository_object_materialization_receipt_digest(
        receipt
    ):
        issues.append("object_materialization_receipt_digest_mismatch")
    return tuple(issues)
