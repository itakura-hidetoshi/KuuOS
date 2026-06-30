#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from runtime.kuuos_repository_checkpoint_discrepancy_review_types_v1_06 import (
    DISCREPANCY_EVIDENCE_INVALID,
    DISCREPANCY_LOST,
    DISCREPANCY_NONE,
    DISCREPANCY_OTHER,
    DISCREPANCY_SUBSTITUTED,
    REVIEW_CLEAN,
    REVIEW_REJECTED,
    REVIEW_REQUIRED,
    ZERO_OID,
    RepositoryCheckpointReviewObservation,
    RepositoryCheckpointReviewPolicy,
    RepositoryCheckpointReviewRecord,
    repository_checkpoint_review_record_digest,
)
from runtime.kuuos_repository_checkpoint_stability_types_v1_05 import (
    FAILURE_CHECKPOINT_LOST,
    FAILURE_CHECKPOINT_SUBSTITUTED,
    FAILURE_NONE,
)
from runtime.kuuos_repository_checkpoint_stability_v1_05 import (
    repository_checkpoint_stability_certificate_issues,
)
from runtime.v106_review_evidence import (
    repository_checkpoint_review_observation_issues,
    repository_checkpoint_review_policy_issues,
)


def _stability_issues(
    stability_certificate,
    v105_context: Mapping[str, Any],
) -> tuple[str, ...]:
    try:
        values = dict(v105_context)
        values.pop("certificate_id", None)
        return repository_checkpoint_stability_certificate_issues(
            stability_certificate,
            **values,
        )
    except (TypeError, ValueError, AttributeError, KeyError):
        return ("checkpoint_stability_context_invalid",)


def construct_repository_checkpoint_review_record(
    review_id: str,
    stability_certificate,
    v105_context: Mapping[str, Any],
    policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointReviewRecord:
    stability_valid = not _stability_issues(stability_certificate, v105_context)
    policy_valid = not repository_checkpoint_review_policy_issues(policy)
    observation_valid = not repository_checkpoint_review_observation_issues(
        observation
    )
    binding_exact = bool(
        observation.stability_certificate_digest
        == stability_certificate.certificate_digest
        and observation.repository_id == stability_certificate.repository_id
        and observation.git_dir_fingerprint
        == stability_certificate.git_dir_fingerprint
        and observation.checkpoint_reference
        == stability_certificate.checkpoint_reference
        and observation.expected_oid == stability_certificate.expected_oid
        and observation.repository_id in policy.allowed_repository_ids
        and observation.checkpoint_reference
        in policy.allowed_checkpoint_references
    )
    observer_accepted = observation.observer_id in policy.authorized_observer_ids
    observation_fresh = bool(
        0
        <= evaluated_at_epoch_seconds - observation.rechecked_at_epoch_seconds
        <= policy.max_observation_age_seconds
    )
    no_future_evidence = bool(
        observation.observed_at_epoch_seconds
        <= observation.rechecked_at_epoch_seconds
        <= evaluated_at_epoch_seconds
    )
    source_exact = bool(
        observation.direct
        and not observation.symbolic
        and observation.reference_store_read
        and observation.object_database_read
        and not observation.working_tree_read
        and not observation.reflog_read
        and not observation.remote_read
    )
    recheck_stable = observation.observed_oid == observation.rechecked_oid
    target_object_exact = bool(
        observation.target_object_present
        and observation.target_object_type == "commit"
    )
    current_clean = bool(
        observation.reference_present
        and observation.rechecked_oid == observation.expected_oid
        and target_object_exact
    )
    current_lost = bool(
        not observation.reference_present
        and observation.observed_oid == ZERO_OID
        and observation.rechecked_oid == ZERO_OID
        and target_object_exact
    )
    current_substituted = bool(
        observation.reference_present
        and observation.rechecked_oid != observation.expected_oid
        and observation.rechecked_oid != ZERO_OID
        and target_object_exact
    )
    disposition_matches = bool(
        (
            stability_certificate.failure_kind == FAILURE_NONE
            and current_clean
        )
        or (
            stability_certificate.failure_kind == FAILURE_CHECKPOINT_LOST
            and current_lost
        )
        or (
            stability_certificate.failure_kind == FAILURE_CHECKPOINT_SUBSTITUTED
            and current_substituted
        )
    )
    evidence_valid = bool(
        stability_valid
        and policy_valid
        and observation_valid
        and binding_exact
        and observer_accepted
        and observation_fresh
        and no_future_evidence
        and source_exact
        and recheck_stable
        and disposition_matches
    )

    if not evidence_valid:
        status = REVIEW_REJECTED
        discrepancy_kind = DISCREPANCY_EVIDENCE_INVALID
        human_review_required = False
    elif stability_certificate.failure_kind == FAILURE_NONE:
        status = REVIEW_CLEAN
        discrepancy_kind = DISCREPANCY_NONE
        human_review_required = False
    elif stability_certificate.failure_kind == FAILURE_CHECKPOINT_LOST:
        status = REVIEW_REQUIRED
        discrepancy_kind = DISCREPANCY_LOST
        human_review_required = True
    elif stability_certificate.failure_kind == FAILURE_CHECKPOINT_SUBSTITUTED:
        status = REVIEW_REQUIRED
        discrepancy_kind = DISCREPANCY_SUBSTITUTED
        human_review_required = True
    else:
        status = REVIEW_REJECTED
        discrepancy_kind = DISCREPANCY_OTHER
        human_review_required = False

    checks = {
        "stability_certificate_valid": stability_valid,
        "review_policy_valid": policy_valid,
        "review_observation_valid": observation_valid,
        "evidence_binding_exact": binding_exact,
        "observer_accepted": observer_accepted,
        "observation_fresh": observation_fresh,
        "no_future_evidence": no_future_evidence,
        "direct_local_sources_only": source_exact,
        "current_state_recheck_stable": recheck_stable,
        "target_commit_present": target_object_exact,
        "stability_disposition_matches_current_state": disposition_matches,
        "checkpoint_clean": current_clean,
        "checkpoint_lost": current_lost,
        "checkpoint_substituted": current_substituted,
        "human_review_required": human_review_required,
        "review_granted_repository_change_authority": False,
        "review_performed_reference_mutation": False,
        "review_performed_object_write": False,
        "review_invoked_live_git_command": False,
        "review_mutated_live_repository": False,
        "review_consumed_nonce": False,
    }
    evidence_digests = {
        "stability_certificate": stability_certificate.certificate_digest,
        "review_policy": policy.policy_digest,
        "review_observation": observation.observation_digest,
    }
    record = RepositoryCheckpointReviewRecord(
        review_id=review_id,
        status=status,
        discrepancy_kind=discrepancy_kind,
        stability_certificate_digest=stability_certificate.certificate_digest,
        review_policy_digest=policy.policy_digest,
        review_observation_digest=observation.observation_digest,
        repository_id=stability_certificate.repository_id,
        git_dir_fingerprint=stability_certificate.git_dir_fingerprint,
        checkpoint_reference=stability_certificate.checkpoint_reference,
        expected_current_oid=observation.rechecked_oid,
        expected_target_oid=stability_certificate.expected_oid,
        human_review_required=human_review_required,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
        checks=checks,
        evidence_digests=evidence_digests,
        record_digest="",
    )
    return replace(
        record,
        record_digest=repository_checkpoint_review_record_digest(record),
    )


def review_repository_checkpoint_discrepancy(
    review_id: str,
    stability_certificate,
    v105_context: Mapping[str, Any],
    policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    *,
    evaluated_at_epoch_seconds: int,
) -> RepositoryCheckpointReviewRecord:
    if not review_id:
        raise ValueError("checkpoint_review_id_missing")
    if evaluated_at_epoch_seconds < 0:
        raise ValueError("checkpoint_review_evaluation_time_negative")
    record = construct_repository_checkpoint_review_record(
        review_id,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues = repository_checkpoint_review_record_issues(
        record,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    if issues:
        raise ValueError(f"checkpoint_review_record_invalid:{issues[0]}")
    return record


def repository_checkpoint_review_record_issues(
    record: RepositoryCheckpointReviewRecord,
    stability_certificate,
    v105_context: Mapping[str, Any],
    policy: RepositoryCheckpointReviewPolicy,
    observation: RepositoryCheckpointReviewObservation,
    *,
    evaluated_at_epoch_seconds: int,
) -> tuple[str, ...]:
    expected = construct_repository_checkpoint_review_record(
        record.review_id,
        stability_certificate,
        v105_context,
        policy,
        observation,
        evaluated_at_epoch_seconds=evaluated_at_epoch_seconds,
    )
    issues: list[str] = []
    if record.to_dict() != expected.to_dict():
        issues.append("checkpoint_review_recomputation_mismatch")
    if record.status not in (REVIEW_CLEAN, REVIEW_REQUIRED, REVIEW_REJECTED):
        issues.append("checkpoint_review_status_invalid")
    if record.discrepancy_kind not in (
        DISCREPANCY_NONE,
        DISCREPANCY_LOST,
        DISCREPANCY_SUBSTITUTED,
        DISCREPANCY_OTHER,
        DISCREPANCY_EVIDENCE_INVALID,
    ):
        issues.append("checkpoint_review_discrepancy_invalid")
    if record.human_review_required != (record.status == REVIEW_REQUIRED):
        issues.append("checkpoint_review_human_boundary_mismatch")
    forbidden_claims = (
        "review_granted_repository_change_authority",
        "review_performed_reference_mutation",
        "review_performed_object_write",
        "review_invoked_live_git_command",
        "review_mutated_live_repository",
        "review_consumed_nonce",
    )
    if any(record.checks.get(key, False) for key in forbidden_claims):
        issues.append("checkpoint_review_forbidden_claim")
    if record.record_digest != repository_checkpoint_review_record_digest(record):
        issues.append("checkpoint_review_record_digest_mismatch")
    return tuple(issues)
