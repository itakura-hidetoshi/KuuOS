#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_creation_receipt_v1_03 import (
    repository_checkpoint_creation_receipt_issues,
)
from runtime.kuuos_repository_checkpoint_stability_types_v1_04 import (
    FAILURE_CHECKPOINT_LOST,
    FAILURE_CHECKPOINT_SUBSTITUTED,
    FAILURE_EVIDENCE_INVALID,
    FAILURE_NAME_CONFLICT,
    FAILURE_NONE,
    FAILURE_UNREACHABLE,
    FAILURE_UNSTABLE_WINDOW,
    STABILITY_CONFIRMED,
    STABILITY_REJECTED,
    RepositoryCheckpointStabilityCertificate,
    repository_checkpoint_stability_certificate_digest,
)
from runtime.v104_checkpoint_stability_observations_a import (
    repository_checkpoint_reachability_observation_issues,
    repository_delayed_checkpoint_observation_issues,
)
from runtime.v104_checkpoint_stability_observations_b import (
    repository_checkpoint_namespace_observation_issues,
)
from runtime.v104_checkpoint_stability_policy import (
    repository_checkpoint_stability_policy_issues,
)


def _v103_receipt_issues(receipt, context: Mapping[str, Any]) -> tuple[str, ...]:
    try:
        values = dict(context)
        values.pop("receipt_id", None)
        return repository_checkpoint_creation_receipt_issues(receipt, **values)
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_creation_receipt_context_invalid",)


def construct_repository_checkpoint_stability_certificate(
    certificate_id: str,
    creation_receipt,
    v103_context: Mapping[str, Any],
    policy,
    delayed_observation,
    reachability_observation,
    namespace_observation,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointStabilityCertificate:
    result = v103_context.get("result")
    immediate = v103_context.get("reference_snapshot", {})
    receipt_valid = not _v103_receipt_issues(creation_receipt, v103_context)
    receipt_confirmed = bool(
        receipt_valid and creation_receipt.status == "REPOSITORY_CHECKPOINT_CREATION_RECEIPT_CONFIRMED"
    )
    receipt_committed = bool(
        receipt_confirmed
        and creation_receipt.checks.get("committed_receipt_confirmed", False)
    )
    policy_valid = not repository_checkpoint_stability_policy_issues(policy)
    delayed_valid = not repository_delayed_checkpoint_observation_issues(
        delayed_observation
    )
    reachability_valid = not repository_checkpoint_reachability_observation_issues(
        reachability_observation
    )
    namespace_valid = not repository_checkpoint_namespace_observation_issues(
        namespace_observation
    )

    result_available = result is not None
    binding_exact = bool(
        result_available
        and creation_receipt.receipt_digest
        == delayed_observation.creation_receipt_digest
        == reachability_observation.creation_receipt_digest
        == namespace_observation.creation_receipt_digest
        and result.transaction_id
        == delayed_observation.transaction_id
        == reachability_observation.transaction_id
        == namespace_observation.transaction_id
        and result.repository_id
        == delayed_observation.repository_id
        == reachability_observation.repository_id
        == namespace_observation.repository_id
        and result.git_dir_fingerprint
        == delayed_observation.git_dir_fingerprint
        == reachability_observation.git_dir_fingerprint
        == namespace_observation.git_dir_fingerprint
        and result.checkpoint_reference
        == delayed_observation.checkpoint_reference
        == reachability_observation.checkpoint_reference
        == namespace_observation.checkpoint_reference
        and result.proposed_new_oid
        == delayed_observation.expected_oid
        == reachability_observation.object_oid
    )
    observer_authorized = bool(
        delayed_observation.observer_id
        == reachability_observation.observer_id
        == namespace_observation.observer_id
        and delayed_observation.observer_id in policy.authorized_observer_ids
    )
    initial_sequence = immediate.get("sequence_number", -1)
    sequence_ordered = bool(
        initial_sequence < delayed_observation.sequence_number
        < reachability_observation.sequence_number
        < namespace_observation.sequence_number
    )
    initial_time = immediate.get("recorded_at_epoch_seconds", -1)
    times_ordered = bool(
        initial_time <= delayed_observation.observed_at_epoch_seconds
        <= reachability_observation.observed_at_epoch_seconds
        <= namespace_observation.observed_at_epoch_seconds
        <= evaluated_at_epoch_seconds
    )
    stability_interval = delayed_observation.observed_at_epoch_seconds - initial_time
    interval_within_policy = bool(
        policy.min_stability_interval_seconds
        <= stability_interval
        <= policy.max_stability_interval_seconds
    )
    observations_fresh = bool(
        all(
            0 <= evaluated_at_epoch_seconds - value <= policy.max_observation_age_seconds
            for value in (
                delayed_observation.observed_at_epoch_seconds,
                namespace_observation.observed_at_epoch_seconds,
            )
        )
    )
    reachability_fresh = bool(
        0
        <= evaluated_at_epoch_seconds
        - reachability_observation.observed_at_epoch_seconds
        <= policy.max_reachability_age_seconds
    )
    no_future_evidence = bool(
        times_ordered
        and creation_receipt.checks.get("no_future_evidence", False)
    )

    delayed_source_exact = bool(
        delayed_observation.direct
        and not delayed_observation.symbolic
        and delayed_observation.reference_store_read
        and delayed_observation.object_database_read
        and not delayed_observation.working_tree_read
        and not delayed_observation.reflog_read
        and not delayed_observation.remote_read
    )
    reference_present = bool(delayed_observation.reference_present)
    checkpoint_oid_exact = bool(
        reference_present
        and result_available
        and delayed_observation.observed_oid == result.proposed_new_oid
    )
    no_substitution = bool(
        checkpoint_oid_exact
        and not delayed_observation.overwrite_observed
        and not delayed_observation.force_update_observed
    )
    reachability_exact = bool(
        result_available
        and reachability_observation.object_oid == result.proposed_new_oid
        and reachability_observation.object_present
        and reachability_observation.object_type == "commit"
        and reachability_observation.object_database_read
        and not reachability_observation.working_tree_read
        and not reachability_observation.reflog_read
        and not reachability_observation.remote_read
    )
    namespace_unique = bool(
        namespace_observation.checkpoint_namespace_prefix
        == policy.checkpoint_namespace_prefix
        and namespace_observation.checkpoint_reference
        in namespace_observation.observed_checkpoint_references
        and namespace_observation.target_occurrences == 1
        and not namespace_observation.conflicting_reference_names
        and namespace_observation.reference_store_read
        and not namespace_observation.working_tree_read
        and not namespace_observation.reflog_read
        and not namespace_observation.remote_read
        and all(
            value.startswith(policy.checkpoint_namespace_prefix)
            for value in namespace_observation.observed_checkpoint_references
        )
    )
    immutable_policy_enforced = bool(
        policy.immutable_by_default
        and not any(
            (
                policy.allow_checkpoint_overwrite,
                policy.allow_checkpoint_delete,
                policy.allow_force_update,
                policy.allow_branch_update,
                policy.allow_tag_update,
                policy.allow_remote_reference_update,
                policy.allow_push,
            )
        )
    )

    evidence_core_valid = bool(
        receipt_valid
        and receipt_confirmed
        and receipt_committed
        and policy_valid
        and delayed_valid
        and reachability_valid
        and namespace_valid
        and binding_exact
        and observer_authorized
        and sequence_ordered
        and no_future_evidence
    )
    if not evidence_core_valid:
        failure_kind = FAILURE_EVIDENCE_INVALID
    elif not interval_within_policy or not observations_fresh or not reachability_fresh:
        failure_kind = FAILURE_UNSTABLE_WINDOW
    elif not reference_present:
        failure_kind = FAILURE_CHECKPOINT_LOST
    elif not delayed_source_exact or not no_substitution:
        failure_kind = FAILURE_CHECKPOINT_SUBSTITUTED
    elif not namespace_unique:
        failure_kind = FAILURE_NAME_CONFLICT
    elif not reachability_exact:
        failure_kind = FAILURE_UNREACHABLE
    else:
        failure_kind = FAILURE_NONE

    stability_confirmed = bool(
        failure_kind == FAILURE_NONE
        and immutable_policy_enforced
    )
    checks = {
        "creation_receipt_valid": receipt_valid,
        "creation_receipt_confirmed": receipt_confirmed,
        "creation_receipt_committed": receipt_committed,
        "stability_policy_valid": policy_valid,
        "delayed_observation_valid": delayed_valid,
        "reachability_observation_valid": reachability_valid,
        "namespace_observation_valid": namespace_valid,
        "evidence_binding_exact": binding_exact,
        "observer_authorized": observer_authorized,
        "observation_sequence_ordered": sequence_ordered,
        "observation_times_ordered": times_ordered,
        "stability_interval_within_policy": interval_within_policy,
        "observations_fresh": observations_fresh,
        "reachability_fresh": reachability_fresh,
        "no_future_evidence": no_future_evidence,
        "delayed_reference_source_exact": delayed_source_exact,
        "checkpoint_reference_present": reference_present,
        "checkpoint_oid_exact": checkpoint_oid_exact,
        "checkpoint_not_substituted": no_substitution,
        "checkpoint_object_reachable": reachability_exact,
        "checkpoint_name_unique": namespace_unique,
        "immutable_policy_enforced": immutable_policy_enforced,
        "checkpoint_stability_confirmed": stability_confirmed,
        "checkpoint_overwrite_authorized": False,
        "checkpoint_delete_authorized": False,
        "force_update_authorized": False,
        "restore_authorized": False,
        "recovery_authorized": False,
        "branch_update_authorized": False,
        "tag_update_authorized": False,
        "remote_reference_update_authorized": False,
        "push_authorized": False,
        "certificate_performed_reference_mutation": False,
        "certificate_performed_object_write": False,
        "certificate_invoked_live_git_command": False,
        "certificate_mutated_live_repository": False,
    }
    evidence_digests = {
        "creation_receipt": creation_receipt.receipt_digest,
        "policy": policy.policy_digest,
        "delayed_observation": delayed_observation.observation_digest,
        "reachability_observation": reachability_observation.observation_digest,
        "namespace_observation": namespace_observation.observation_digest,
    }
    certificate = RepositoryCheckpointStabilityCertificate(
        certificate_id=certificate_id,
        status=STABILITY_CONFIRMED if stability_confirmed else STABILITY_REJECTED,
        failure_kind=failure_kind,
        creation_receipt_digest=creation_receipt.receipt_digest,
        stability_policy_digest=policy.policy_digest,
        delayed_observation_digest=delayed_observation.observation_digest,
        reachability_observation_digest=reachability_observation.observation_digest,
        namespace_observation_digest=namespace_observation.observation_digest,
        transaction_id=result.transaction_id if result_available else "",
        repository_id=result.repository_id if result_available else "",
        git_dir_fingerprint=result.git_dir_fingerprint if result_available else "",
        checkpoint_reference=result.checkpoint_reference if result_available else "",
        expected_oid=result.proposed_new_oid if result_available else "",
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        checks=checks,
        evidence_digests=evidence_digests,
        certificate_digest="",
    )
    return replace(
        certificate,
        certificate_digest=repository_checkpoint_stability_certificate_digest(
            certificate
        ),
    )
