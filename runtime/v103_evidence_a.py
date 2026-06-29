#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.v103_receipt_policy import VERSION


@dataclass(frozen=True)
class RepositoryCheckpointCreationExecutionReport:
    report_id: str
    transaction_id: str
    authorization_certificate_digest: str
    execution_policy_digest: str
    request_digest: str
    v102_result_digest: str
    repository_id: str
    git_dir_fingerprint: str
    checkpoint_reference: str
    expected_old_oid: str
    proposed_new_oid: str
    authorization_nonce: str
    executor_id: str
    executor_sequence_number: int
    creation_attempted: bool
    compare_and_swap_succeeded: bool
    checkpoint_created: bool
    nonce_consumed: bool
    aborted_without_mutation: bool
    reported_effects: tuple[str, ...]
    execution_started_at_epoch_seconds: int
    execution_completed_at_epoch_seconds: int
    report_digest: str
    version: str = VERSION

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["reported_effects"] = list(self.reported_effects)
        return payload


def repository_checkpoint_creation_execution_report_digest(
    report: RepositoryCheckpointCreationExecutionReport,
) -> str:
    payload = report.to_dict()
    payload.pop("report_digest", None)
    return canonical_digest(payload)
