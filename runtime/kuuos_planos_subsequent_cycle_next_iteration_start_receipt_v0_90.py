from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_next_iteration_start_receipt_v0_90"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_next_iteration_request_v0_89"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_NEXT_ITERATION_START_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_next_iteration_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "closeout_evidence_preserved": True,
    "post_closeout_review_evidence_preserved": True,
    "learning_update_evidence_preserved": True,
    "next_iteration_scope_preserved": True,
    "next_iteration_constraints_digest_preserved": True,
    "subsequent_cycle_next_iteration_requested": True,
    "subsequent_cycle_next_iteration_started": True,
    "subsequent_cycle_next_iteration_planning_requested": False,
}


@dataclass(frozen=True)
class SubsequentCycleNextIterationStartReceipt:
    version: str
    source_version: str
    status: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    closeout_receipt_digest: str
    post_closeout_review_receipt_digest: str
    learning_update_receipt_digest: str
    next_iteration_scope: str
    next_iteration_constraints_digest: str
    subsequent_cycle_next_iteration_start_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_next_iteration_start_receipt(
    source_next_iteration_request: Mapping[str, Any],
    *,
    start_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleNextIterationStartReceipt:
    blockers: list[str] = []
    if source_next_iteration_request.get("version") != SOURCE_VERSION:
        blockers.append("source_next_iteration_request_version_invalid")
    if source_next_iteration_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_NEXT_ITERATION_REQUEST_READY":
        blockers.append("source_next_iteration_request_not_ready")
    if not source_next_iteration_request.get("receipt_digest"):
        blockers.append("source_next_iteration_request_receipt_digest_missing")

    boundary = _m(source_next_iteration_request.get("boundary"))
    if boundary.get("subsequent_cycle_next_iteration_requested") is not True:
        blockers.append("source_boundary_next_iteration_requested_missing")
    if boundary.get("subsequent_cycle_next_iteration_started") is not False:
        blockers.append("source_boundary_next_iteration_started_promoted")

    record = _m(source_next_iteration_request.get("subsequent_cycle_next_iteration_request"))
    if not record or not record.get("next_iteration_request_digest"):
        blockers.append("source_next_iteration_request_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "closeout_receipt_digest", "post_closeout_review_receipt_digest",
        "learning_update_receipt_digest", "next_iteration_scope",
        "next_iteration_constraints_digest",
    )
    for field in fields:
        if not source_next_iteration_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_next_iteration_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(start_rationale or {
        "learning_update_evidence_accepted": True,
        "next_iteration_scope_respected": True,
        "next_iteration_constraints_respected": True,
        "planning_request_remains_separate": True,
    })
    if not rationale:
        blockers.append("next_iteration_start_rationale_missing")

    start_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_NEXT_ITERATION_START_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_next_iteration_request_receipt_digest": str(source_next_iteration_request["receipt_digest"]),
            "source_next_iteration_request_digest": str(record["next_iteration_request_digest"]),
            **{field: str(source_next_iteration_request[field]) for field in fields},
            "next_iteration_start_rationale_digest": sha(rationale),
            "subsequent_cycle_next_iteration_requested": True,
            "subsequent_cycle_next_iteration_started": True,
            "subsequent_cycle_next_iteration_planning_requested": False,
        }
        start_record = {**payload, "next_iteration_start_receipt_digest": sha(payload)}
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_next_iteration_request.get(field, "")) for field in fields},
        "subsequent_cycle_next_iteration_start_receipt": start_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleNextIterationStartReceipt(**outer, receipt_digest=sha(outer))
