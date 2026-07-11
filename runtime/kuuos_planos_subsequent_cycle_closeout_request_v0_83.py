from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_closeout_request_v0_83"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_execution_completion_receipt_v0_82"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CLOSEOUT_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_execution_completion_receipt_preserved": True,
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
    "subsequent_cycle_closeout_request_only": True,
    "subsequent_cycle_execution_completed": True,
    "subsequent_cycle_closeout_requested": True,
    "subsequent_cycle_closed": False,
}


@dataclass(frozen=True)
class SubsequentCycleCloseoutRequestRecord:
    source_execution_completion_receipt_digest: str
    source_execution_completion_record_digest: str
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
    closeout_request_digest: str
    subsequent_cycle_execution_completed: bool = True
    subsequent_cycle_closeout_requested: bool = True
    subsequent_cycle_closed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCloseoutRequestReceipt:
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
    subsequent_cycle_closeout_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_closeout_request(
    source_completion_receipt: Mapping[str, Any],
    *,
    closeout_scope: str = "completed subsequent-cycle bounded closeout",
    closeout_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleCloseoutRequestReceipt:
    blockers: list[str] = []
    if source_completion_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_completion_receipt_version_invalid")
    if source_completion_receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_RECEIPT_READY":
        blockers.append("source_completion_receipt_not_ready")
    if not source_completion_receipt.get("receipt_digest"):
        blockers.append("source_completion_receipt_digest_missing")

    boundary = _m(source_completion_receipt.get("boundary"))
    if boundary.get("subsequent_cycle_execution_completed") is not True:
        blockers.append("source_boundary_execution_completed_missing")
    if boundary.get("subsequent_cycle_closeout_requested") is not False:
        blockers.append("source_boundary_closeout_requested_promoted")

    record = _m(source_completion_receipt.get("subsequent_cycle_execution_completion_receipt"))
    if not record or not record.get("execution_completion_receipt_digest"):
        blockers.append("source_execution_completion_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest", "candidate_set_digest",
        "evaluation_set_digest", "review_set_digest", "admission_scope",
        "admission_constraints_digest", "start_scope", "start_constraints_digest",
        "execution_scope", "execution_constraints_digest", "completion_scope",
        "completion_constraints_digest",
    )
    for field in fields:
        if not source_completion_receipt.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_completion_receipt.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    constraints = dict(closeout_constraints or {
        "execution_completion_required": True,
        "preserve_selected_candidate_evidence": True,
        "bounded_closeout_scope": True,
        "actual_close_remains_separate": True,
    })
    if not closeout_scope:
        blockers.append("closeout_scope_missing")
    if not constraints:
        blockers.append("closeout_constraints_missing")

    request_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CLOSEOUT_REQUEST_BLOCKED"
    constraints_digest = sha(constraints) if constraints else ""
    if not blockers:
        payload = {
            "source_execution_completion_receipt_digest": str(source_completion_receipt["receipt_digest"]),
            "source_execution_completion_record_digest": str(record["execution_completion_receipt_digest"]),
            "selected_candidate_id": str(source_completion_receipt["selected_candidate_id"]),
            "selected_candidate_digest": str(source_completion_receipt["selected_candidate_digest"]),
            "candidate_set_digest": str(source_completion_receipt["candidate_set_digest"]),
            "evaluation_set_digest": str(source_completion_receipt["evaluation_set_digest"]),
            "review_set_digest": str(source_completion_receipt["review_set_digest"]),
            "admission_scope": str(source_completion_receipt["admission_scope"]),
            "admission_constraints_digest": str(source_completion_receipt["admission_constraints_digest"]),
            "start_scope": str(source_completion_receipt["start_scope"]),
            "start_constraints_digest": str(source_completion_receipt["start_constraints_digest"]),
            "execution_scope": str(source_completion_receipt["execution_scope"]),
            "execution_constraints_digest": str(source_completion_receipt["execution_constraints_digest"]),
            "completion_scope": str(source_completion_receipt["completion_scope"]),
            "completion_constraints_digest": str(source_completion_receipt["completion_constraints_digest"]),
            "closeout_scope": closeout_scope,
            "closeout_constraints_digest": constraints_digest,
        }
        request_record = SubsequentCycleCloseoutRequestRecord(
            **payload, closeout_request_digest=sha(payload)
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_completion_receipt.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_completion_receipt.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_completion_receipt.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_completion_receipt.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_completion_receipt.get("review_set_digest", "")),
        "admission_scope": str(source_completion_receipt.get("admission_scope", "")),
        "admission_constraints_digest": str(source_completion_receipt.get("admission_constraints_digest", "")),
        "start_scope": str(source_completion_receipt.get("start_scope", "")),
        "start_constraints_digest": str(source_completion_receipt.get("start_constraints_digest", "")),
        "execution_scope": str(source_completion_receipt.get("execution_scope", "")),
        "execution_constraints_digest": str(source_completion_receipt.get("execution_constraints_digest", "")),
        "completion_scope": str(source_completion_receipt.get("completion_scope", "")),
        "completion_constraints_digest": str(source_completion_receipt.get("completion_constraints_digest", "")),
        "closeout_scope": closeout_scope,
        "closeout_constraints_digest": constraints_digest,
        "subsequent_cycle_closeout_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleCloseoutRequestReceipt(**outer, receipt_digest=sha(outer))
