from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_closeout_receipt_v0_84"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_closeout_request_v0_83"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CLOSEOUT_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_subsequent_cycle_closeout_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_scope_preserved": True,
    "admission_constraints_digest_preserved": True,
    "start_scope_preserved": True,
    "start_constraints_digest_preserved": True,
    "execution_scope_preserved": True,
    "execution_constraints_digest_preserved": True,
    "completion_scope_preserved": True,
    "completion_constraints_digest_preserved": True,
    "closeout_scope_preserved": True,
    "closeout_constraints_digest_preserved": True,
    "subsequent_cycle_closeout_receipt_only": True,
    "subsequent_cycle_closeout_requested": True,
    "subsequent_cycle_closed": True,
    "subsequent_cycle_post_closeout_review_requested": False,
}


@dataclass(frozen=True)
class SubsequentCycleCloseoutRecord:
    source_closeout_request_receipt_digest: str
    source_closeout_request_digest: str
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
    completion_scope: str
    completion_constraints_digest: str
    closeout_scope: str
    closeout_constraints_digest: str
    closeout_rationale_digest: str
    closeout_receipt_digest: str
    subsequent_cycle_closeout_requested: bool = True
    subsequent_cycle_closed: bool = True
    subsequent_cycle_post_closeout_review_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCloseoutReceipt:
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
    completion_scope: str
    completion_constraints_digest: str
    closeout_scope: str
    closeout_constraints_digest: str
    subsequent_cycle_closeout_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_closeout_receipt(
    source_closeout_request: Mapping[str, Any],
    *,
    closeout_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleCloseoutReceipt:
    blockers: list[str] = []
    if source_closeout_request.get("version") != SOURCE_VERSION:
        blockers.append("source_closeout_request_version_invalid")
    if source_closeout_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CLOSEOUT_REQUEST_READY":
        blockers.append("source_closeout_request_not_ready")
    if not source_closeout_request.get("receipt_digest"):
        blockers.append("source_closeout_request_receipt_digest_missing")

    boundary = _m(source_closeout_request.get("boundary"))
    if boundary.get("subsequent_cycle_closeout_requested") is not True:
        blockers.append("source_boundary_closeout_requested_missing")
    if boundary.get("subsequent_cycle_closed") is not False:
        blockers.append("source_boundary_subsequent_cycle_closed_promoted")

    record = _m(source_closeout_request.get("subsequent_cycle_closeout_request"))
    if not record or not record.get("closeout_request_digest"):
        blockers.append("source_closeout_request_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "admission_scope", "admission_constraints_digest",
        "start_scope", "start_constraints_digest",
        "execution_scope", "execution_constraints_digest",
        "completion_scope", "completion_constraints_digest",
        "closeout_scope", "closeout_constraints_digest",
    )
    for field in fields:
        if not source_closeout_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_closeout_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(closeout_rationale or {
        "execution_completion_preserved": True,
        "closeout_scope_respected": True,
        "closeout_constraints_respected": True,
        "post_closeout_review_remains_separate": True,
    })
    if not rationale:
        blockers.append("closeout_rationale_missing")

    closeout_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CLOSEOUT_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_closeout_request_receipt_digest": str(source_closeout_request["receipt_digest"]),
            "source_closeout_request_digest": str(record["closeout_request_digest"]),
            **{field: str(source_closeout_request[field]) for field in fields},
            "closeout_rationale_digest": sha(rationale),
        }
        closeout_record = SubsequentCycleCloseoutRecord(
            **payload,
            closeout_receipt_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_closeout_request.get(field, "")) for field in fields},
        "subsequent_cycle_closeout_receipt": closeout_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleCloseoutReceipt(**outer, receipt_digest=sha(outer))
