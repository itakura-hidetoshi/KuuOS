from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_execution_completion_receipt_v0_82"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_execution_completion_request_v0_81"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_execution_completion_request_preserved": True,
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
    "subsequent_cycle_execution_completion_receipt_only": True,
    "subsequent_cycle_execution_completion_requested": True,
    "subsequent_cycle_execution_completed": True,
    "subsequent_cycle_closeout_requested": False,
}


@dataclass(frozen=True)
class SubsequentCycleExecutionCompletionRecord:
    source_completion_request_receipt_digest: str
    source_completion_request_digest: str
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
    completion_rationale_digest: str
    execution_completion_receipt_digest: str
    subsequent_cycle_execution_completion_requested: bool = True
    subsequent_cycle_execution_completed: bool = True
    subsequent_cycle_closeout_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleExecutionCompletionReceipt:
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
    subsequent_cycle_execution_completion_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_execution_completion_receipt(
    source_completion_request: Mapping[str, Any],
    *,
    completion_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleExecutionCompletionReceipt:
    blockers: list[str] = []
    if source_completion_request.get("version") != SOURCE_VERSION:
        blockers.append("source_completion_request_version_invalid")
    if source_completion_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_REQUEST_READY":
        blockers.append("source_completion_request_not_ready")
    if not source_completion_request.get("receipt_digest"):
        blockers.append("source_completion_request_receipt_digest_missing")

    boundary = _m(source_completion_request.get("boundary"))
    if boundary.get("subsequent_cycle_execution_completion_requested") is not True:
        blockers.append("source_boundary_completion_requested_missing")
    if boundary.get("subsequent_cycle_execution_completed") is not False:
        blockers.append("source_boundary_execution_completed_promoted")

    record = _m(source_completion_request.get("subsequent_cycle_execution_completion_request"))
    if not record or not record.get("execution_completion_request_digest"):
        blockers.append("source_completion_request_record_missing")

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
        "completion_scope",
        "completion_constraints_digest",
    )
    for field in fields:
        if not source_completion_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_completion_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(completion_rationale or {
        "execution_start_preserved": True,
        "completion_scope_respected": True,
        "completion_constraints_respected": True,
        "closeout_remains_separate": True,
    })
    if not rationale:
        blockers.append("completion_rationale_missing")

    receipt_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_EXECUTION_COMPLETION_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_completion_request_receipt_digest": str(source_completion_request["receipt_digest"]),
            "source_completion_request_digest": str(record["execution_completion_request_digest"]),
            "selected_candidate_id": str(source_completion_request["selected_candidate_id"]),
            "selected_candidate_digest": str(source_completion_request["selected_candidate_digest"]),
            "candidate_set_digest": str(source_completion_request["candidate_set_digest"]),
            "evaluation_set_digest": str(source_completion_request["evaluation_set_digest"]),
            "review_set_digest": str(source_completion_request["review_set_digest"]),
            "admission_scope": str(source_completion_request["admission_scope"]),
            "admission_constraints_digest": str(source_completion_request["admission_constraints_digest"]),
            "start_scope": str(source_completion_request["start_scope"]),
            "start_constraints_digest": str(source_completion_request["start_constraints_digest"]),
            "execution_scope": str(source_completion_request["execution_scope"]),
            "execution_constraints_digest": str(source_completion_request["execution_constraints_digest"]),
            "completion_scope": str(source_completion_request["completion_scope"]),
            "completion_constraints_digest": str(source_completion_request["completion_constraints_digest"]),
            "completion_rationale_digest": sha(rationale),
        }
        receipt_record = SubsequentCycleExecutionCompletionRecord(
            **payload,
            execution_completion_receipt_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_completion_request.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_completion_request.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_completion_request.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_completion_request.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_completion_request.get("review_set_digest", "")),
        "admission_scope": str(source_completion_request.get("admission_scope", "")),
        "admission_constraints_digest": str(source_completion_request.get("admission_constraints_digest", "")),
        "start_scope": str(source_completion_request.get("start_scope", "")),
        "start_constraints_digest": str(source_completion_request.get("start_constraints_digest", "")),
        "execution_scope": str(source_completion_request.get("execution_scope", "")),
        "execution_constraints_digest": str(source_completion_request.get("execution_constraints_digest", "")),
        "completion_scope": str(source_completion_request.get("completion_scope", "")),
        "completion_constraints_digest": str(source_completion_request.get("completion_constraints_digest", "")),
        "subsequent_cycle_execution_completion_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleExecutionCompletionReceipt(**outer, receipt_digest=sha(outer))
