#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import replace
import re

from runtime.kuuos_repository_checkpoint_restore_authorization_types_v1_06 import (
    RepositoryCheckpointRestoreObservation,
    repository_checkpoint_restore_observation_digest,
)
from runtime.v106_restore_policy import CHECKPOINT_PREFIX

_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def build_repository_checkpoint_restore_observation(
    observation_id: str,
    observer_id: str,
    stability_certificate,
    *,
    reference_present: bool,
    observed_current_oid: str,
    rechecked_current_oid: str,
    target_object_present: bool,
    target_object_type: str,
    sequence_number: int,
    observed_at_epoch_seconds: int,
    rechecked_at_epoch_seconds: int,
    direct: bool = True,
    symbolic: bool = False,
    reference_store_read: bool = True,
    object_database_read: bool = True,
    working_tree_read: bool = False,
    reflog_read: bool = False,
    remote_read: bool = False,
) -> RepositoryCheckpointRestoreObservation:
    observation = RepositoryCheckpointRestoreObservation(
        observation_id=observation_id,
        observer_id=observer_id,
        stability_certificate_digest=stability_certificate.certificate_digest,
        repository_id=stability_certificate.repository_id,
        git_dir_fingerprint=stability_certificate.git_dir_fingerprint,
        checkpoint_reference=stability_certificate.checkpoint_reference,
        expected_restore_oid=stability_certificate.expected_oid,
        reference_present=reference_present,
        observed_current_oid=observed_current_oid,
        rechecked_current_oid=rechecked_current_oid,
        target_object_present=target_object_present,
        target_object_type=target_object_type,
        direct=direct,
        symbolic=symbolic,
        reference_store_read=reference_store_read,
        object_database_read=object_database_read,
        working_tree_read=working_tree_read,
        reflog_read=reflog_read,
        remote_read=remote_read,
        sequence_number=sequence_number,
        observed_at_epoch_seconds=observed_at_epoch_seconds,
        rechecked_at_epoch_seconds=rechecked_at_epoch_seconds,
        observation_digest="",
    )
    observation = replace(
        observation,
        observation_digest=repository_checkpoint_restore_observation_digest(observation),
    )
    issues = repository_checkpoint_restore_observation_issues(observation)
    if issues:
        raise ValueError(f"checkpoint_restore_observation_invalid:{issues[0]}")
    return observation


def repository_checkpoint_restore_observation_issues(
    observation: RepositoryCheckpointRestoreObservation,
) -> tuple[str, ...]:
    issues: list[str] = []
    required = (
        observation.observation_id,
        observation.observer_id,
        observation.stability_certificate_digest,
        observation.repository_id,
        observation.git_dir_fingerprint,
        observation.checkpoint_reference,
        observation.target_object_type,
    )
    if any(not value for value in required):
        issues.append("restore_observation_required_field_missing")
    if not _HEX64.fullmatch(observation.stability_certificate_digest):
        issues.append("restore_observation_stability_digest_invalid")
    if not _HEX64.fullmatch(observation.git_dir_fingerprint):
        issues.append("restore_observation_git_dir_invalid")
    for oid, name in (
        (observation.expected_restore_oid, "expected_restore_oid"),
        (observation.observed_current_oid, "observed_current_oid"),
        (observation.rechecked_current_oid, "rechecked_current_oid"),
    ):
        if not _HEX40.fullmatch(oid):
            issues.append(f"restore_observation_{name}_invalid")
    if not observation.checkpoint_reference.startswith(CHECKPOINT_PREFIX):
        issues.append("restore_observation_reference_invalid")
    if observation.sequence_number < 0:
        issues.append("restore_observation_sequence_negative")
    if observation.observed_at_epoch_seconds < 0:
        issues.append("restore_observation_time_negative")
    if observation.rechecked_at_epoch_seconds < observation.observed_at_epoch_seconds:
        issues.append("restore_observation_recheck_before_observation")
    if observation.observation_digest != repository_checkpoint_restore_observation_digest(observation):
        issues.append("restore_observation_digest_mismatch")
    return tuple(issues)
