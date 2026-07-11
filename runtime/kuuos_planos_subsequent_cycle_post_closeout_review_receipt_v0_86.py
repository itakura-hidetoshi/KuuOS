from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_post_closeout_review_receipt_v0_86"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_post_closeout_review_request_v0_85"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_POST_CLOSEOUT_REVIEW_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_post_closeout_review_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "closeout_evidence_preserved": True,
    "post_closeout_review_scope_preserved": True,
    "post_closeout_review_criteria_digest_preserved": True,
    "subsequent_cycle_post_closeout_review_requested": True,
    "subsequent_cycle_post_closeout_review_completed": True,
    "subsequent_cycle_learning_update_requested": False,
}

@dataclass(frozen=True)
class SubsequentCyclePostCloseoutReviewReceipt:
    version: str
    source_version: str
    status: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    closeout_receipt_digest: str
    post_closeout_review_scope: str
    post_closeout_review_criteria_digest: str
    subsequent_cycle_post_closeout_review_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_post_closeout_review_receipt(
    source_review_request: Mapping[str, Any],
    *,
    review_outcome: Mapping[str, Any] | None = None,
) -> SubsequentCyclePostCloseoutReviewReceipt:
    blockers: list[str] = []
    if source_review_request.get("version") != SOURCE_VERSION:
        blockers.append("source_review_request_version_invalid")
    if source_review_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_POST_CLOSEOUT_REVIEW_REQUEST_READY":
        blockers.append("source_review_request_not_ready")
    if not source_review_request.get("receipt_digest"):
        blockers.append("source_review_request_receipt_digest_missing")

    boundary = _m(source_review_request.get("boundary"))
    if boundary.get("subsequent_cycle_post_closeout_review_requested") is not True:
        blockers.append("source_boundary_review_requested_missing")
    if boundary.get("subsequent_cycle_post_closeout_review_completed") is not False:
        blockers.append("source_boundary_review_completed_promoted")

    record = _m(source_review_request.get("subsequent_cycle_post_closeout_review_request"))
    if not record or not record.get("post_closeout_review_request_digest"):
        blockers.append("source_review_request_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "closeout_receipt_digest", "post_closeout_review_scope",
        "post_closeout_review_criteria_digest",
    )
    for field in fields:
        if not source_review_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_review_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    outcome = dict(review_outcome or {
        "closeout_evidence_accepted": True,
        "execution_completion_consistent": True,
        "review_scope_satisfied": True,
        "learning_update_remains_separate": True,
    })
    if not outcome:
        blockers.append("review_outcome_missing")

    review_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_POST_CLOSEOUT_REVIEW_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_review_request_receipt_digest": str(source_review_request["receipt_digest"]),
            "source_review_request_digest": str(record["post_closeout_review_request_digest"]),
            **{field: str(source_review_request[field]) for field in fields},
            "review_outcome_digest": sha(outcome),
            "subsequent_cycle_post_closeout_review_requested": True,
            "subsequent_cycle_post_closeout_review_completed": True,
            "subsequent_cycle_learning_update_requested": False,
        }
        review_record = {**payload, "post_closeout_review_receipt_digest": sha(payload)}
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_review_request.get(field, "")) for field in fields},
        "subsequent_cycle_post_closeout_review_receipt": review_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCyclePostCloseoutReviewReceipt(**outer, receipt_digest=sha(outer))
