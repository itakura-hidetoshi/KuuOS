from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_execution_start_receipt_v0_80"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_execution_authorization_grant_v0_79"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_START_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_execution_authorization_grant_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_evidence_preserved": True,
    "start_evidence_preserved": True,
    "execution_scope_preserved": True,
    "execution_constraints_digest_preserved": True,
    "subsequent_cycle_execution_start_receipt_only": True,
    "subsequent_cycle_execution_requested": True,
    "subsequent_cycle_execution_authority_granted": True,
    "subsequent_cycle_execution_started": True,
    "subsequent_cycle_execution_completed": False,
}


@dataclass(frozen=True)
class SubsequentCycleExecutionStartRecord:
    source_execution_authorization_grant_receipt_digest: str
    source_execution_authorization_grant_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    execution_scope: str
    execution_constraints_digest: str
    execution_start_rationale_digest: str
    execution_start_receipt_digest: str
    subsequent_cycle_execution_requested: bool = True
    subsequent_cycle_execution_authority_granted: bool = True
    subsequent_cycle_execution_started: bool = True
    subsequent_cycle_execution_completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleExecutionStartReceipt:
    version: str
    source_version: str
    status: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    execution_scope: str
    execution_constraints_digest: str
    subsequent_cycle_execution_start_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_execution_start_receipt(
    source_execution_authorization_grant: Mapping[str, Any],
    *,
    execution_start_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleExecutionStartReceipt:
    blockers: list[str] = []
    source = source_execution_authorization_grant
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_execution_authorization_grant_version_invalid")
    if source.get("status") != "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_AUTHORIZATION_GRANT_READY":
        blockers.append("source_execution_authorization_grant_not_ready")
    if not source.get("receipt_digest"):
        blockers.append("source_execution_authorization_grant_receipt_digest_missing")

    boundary = _m(source.get("boundary"))
    for field in (
        "subsequent_cycle_execution_requested",
        "subsequent_cycle_execution_authority_granted",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    if boundary.get("subsequent_cycle_execution_started") is not False:
        blockers.append("source_boundary_execution_started_promoted")

    record = _m(source.get("subsequent_cycle_execution_authorization_grant"))
    if not record or not record.get("execution_authorization_grant_digest"):
        blockers.append("source_execution_authorization_grant_record_missing")

    fields = (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
        "admission_scope",
        "admission_constraints_digest",
        "start_scope",
        "start_constraints_digest",
        "execution_scope",
        "execution_constraints_digest",
    )
    for field in fields:
        if not source.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(execution_start_rationale or {
        "execution_request_preserved": True,
        "execution_authority_preserved": True,
        "execution_scope_respected": True,
        "execution_constraints_respected": True,
        "execution_completion_remains_separate": True,
    })
    if not rationale:
        blockers.append("execution_start_rationale_missing")

    receipt_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_START_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_execution_authorization_grant_receipt_digest": str(source["receipt_digest"]),
            "source_execution_authorization_grant_digest": str(record["execution_authorization_grant_digest"]),
            **{field: str(source[field]) for field in fields},
            "execution_start_rationale_digest": sha(rationale),
        }
        receipt_record = SubsequentCycleExecutionStartRecord(
            **payload,
            execution_start_receipt_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source.get(field, "")) for field in fields},
        "subsequent_cycle_execution_start_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleExecutionStartReceipt(**outer, receipt_digest=sha(outer))
