from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_execution_completion_request_v0_81"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_execution_start_receipt_v0_80"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_execution_start_receipt_preserved": True,
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
    "subsequent_cycle_execution_started": True,
    "subsequent_cycle_execution_completion_requested": True,
    "subsequent_cycle_execution_completed": False,
}


@dataclass(frozen=True)
class SubsequentCycleExecutionCompletionRequestRecord:
    source_execution_start_receipt_digest: str
    source_execution_start_record_digest: str
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
    execution_completion_request_digest: str
    subsequent_cycle_execution_started: bool = True
    subsequent_cycle_execution_completion_requested: bool = True
    subsequent_cycle_execution_completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleExecutionCompletionRequestReceipt:
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
    subsequent_cycle_execution_completion_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_execution_completion_request(
    source_execution_start_receipt: Mapping[str, Any],
    *,
    completion_scope: str = "selected-candidate bounded subsequent-cycle execution completion",
    completion_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleExecutionCompletionRequestReceipt:
    blockers: list[str] = []
    if source_execution_start_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_execution_start_receipt_version_invalid")
    if source_execution_start_receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_START_RECEIPT_READY":
        blockers.append("source_execution_start_receipt_not_ready")
    if not source_execution_start_receipt.get("receipt_digest"):
        blockers.append("source_execution_start_receipt_digest_missing")

    boundary = _m(source_execution_start_receipt.get("boundary"))
    if boundary.get("subsequent_cycle_execution_started") is not True:
        blockers.append("source_boundary_execution_started_missing")
    if boundary.get("subsequent_cycle_execution_completed") is not False:
        blockers.append("source_boundary_execution_completed_promoted")

    record = _m(source_execution_start_receipt.get("subsequent_cycle_execution_start_receipt"))
    if not record or not record.get("execution_start_receipt_digest"):
        blockers.append("source_execution_start_record_missing")

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
        if not source_execution_start_receipt.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_execution_start_receipt.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    constraints = dict(completion_constraints or {
        "selected_candidate_only": True,
        "bounded_completion_scope": True,
        "completion_receipt_remains_separate": True,
        "post_completion_review_remains_separate": True,
    })
    if not completion_scope:
        blockers.append("completion_scope_missing")
    if not constraints:
        blockers.append("completion_constraints_missing")

    request_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_REQUEST_BLOCKED"
    constraints_digest = sha(constraints) if constraints else ""
    if not blockers:
        payload = {
            "source_execution_start_receipt_digest": str(source_execution_start_receipt["receipt_digest"]),
            "source_execution_start_record_digest": str(record["execution_start_receipt_digest"]),
            "selected_candidate_id": str(source_execution_start_receipt["selected_candidate_id"]),
            "selected_candidate_digest": str(source_execution_start_receipt["selected_candidate_digest"]),
            "candidate_set_digest": str(source_execution_start_receipt["candidate_set_digest"]),
            "evaluation_set_digest": str(source_execution_start_receipt["evaluation_set_digest"]),
            "review_set_digest": str(source_execution_start_receipt["review_set_digest"]),
            "admission_scope": str(source_execution_start_receipt["admission_scope"]),
            "admission_constraints_digest": str(source_execution_start_receipt["admission_constraints_digest"]),
            "start_scope": str(source_execution_start_receipt["start_scope"]),
            "start_constraints_digest": str(source_execution_start_receipt["start_constraints_digest"]),
            "execution_scope": str(source_execution_start_receipt["execution_scope"]),
            "execution_constraints_digest": str(source_execution_start_receipt["execution_constraints_digest"]),
            "completion_scope": completion_scope,
            "completion_constraints_digest": constraints_digest,
        }
        request_record = SubsequentCycleExecutionCompletionRequestRecord(
            **payload,
            execution_completion_request_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_execution_start_receipt.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_execution_start_receipt.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_execution_start_receipt.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_execution_start_receipt.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_execution_start_receipt.get("review_set_digest", "")),
        "admission_scope": str(source_execution_start_receipt.get("admission_scope", "")),
        "admission_constraints_digest": str(source_execution_start_receipt.get("admission_constraints_digest", "")),
        "start_scope": str(source_execution_start_receipt.get("start_scope", "")),
        "start_constraints_digest": str(source_execution_start_receipt.get("start_constraints_digest", "")),
        "execution_scope": str(source_execution_start_receipt.get("execution_scope", "")),
        "execution_constraints_digest": str(source_execution_start_receipt.get("execution_constraints_digest", "")),
        "completion_scope": completion_scope,
        "completion_constraints_digest": constraints_digest,
        "subsequent_cycle_execution_completion_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleExecutionCompletionRequestReceipt(**outer, receipt_digest=sha(outer))
