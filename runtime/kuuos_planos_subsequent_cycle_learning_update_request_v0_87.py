from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_learning_update_request_v0_87"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_post_closeout_review_receipt_v0_86"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_post_closeout_review_receipt_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "closeout_evidence_preserved": True,
    "post_closeout_review_evidence_preserved": True,
    "learning_update_scope_preserved": True,
    "learning_update_constraints_digest_preserved": True,
    "subsequent_cycle_learning_update_requested": True,
    "subsequent_cycle_learning_update_applied": False,
}


@dataclass(frozen=True)
class SubsequentCycleLearningUpdateRequest:
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
    learning_update_scope: str
    learning_update_constraints_digest: str
    subsequent_cycle_learning_update_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_learning_update_request(
    source_review_receipt: Mapping[str, Any],
    *,
    learning_update_scope: str = "subsequent-cycle-post-closeout-learning-update",
    learning_update_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleLearningUpdateRequest:
    blockers: list[str] = []
    if source_review_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_review_receipt_version_invalid")
    if source_review_receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_POST_CLOSEOUT_REVIEW_RECEIPT_READY":
        blockers.append("source_review_receipt_not_ready")
    if not source_review_receipt.get("receipt_digest"):
        blockers.append("source_review_receipt_digest_missing")

    boundary = _m(source_review_receipt.get("boundary"))
    if boundary.get("subsequent_cycle_post_closeout_review_completed") is not True:
        blockers.append("source_boundary_review_completed_missing")
    if boundary.get("subsequent_cycle_learning_update_requested") is not False:
        blockers.append("source_boundary_learning_update_requested_promoted")

    record = _m(source_review_receipt.get("subsequent_cycle_post_closeout_review_receipt"))
    if not record or not record.get("post_closeout_review_receipt_digest"):
        blockers.append("source_review_receipt_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "closeout_receipt_digest",
    )
    for field in fields:
        if not source_review_receipt.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_review_receipt.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    scope = str(learning_update_scope).strip()
    if not scope:
        blockers.append("learning_update_scope_missing")

    constraints = dict(learning_update_constraints or {
        "review_outcome_bound": True,
        "closeout_evidence_bound": True,
        "selected_candidate_identity_bound": True,
        "learning_update_application_remains_separate": True,
    })
    if not constraints:
        blockers.append("learning_update_constraints_missing")

    request_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_review_receipt_digest": str(source_review_receipt["receipt_digest"]),
            "source_review_record_digest": str(record["post_closeout_review_receipt_digest"]),
            **{field: str(source_review_receipt[field]) for field in fields},
            "post_closeout_review_receipt_digest": str(record["post_closeout_review_receipt_digest"]),
            "learning_update_scope": scope,
            "learning_update_constraints_digest": sha(constraints),
            "subsequent_cycle_learning_update_requested": True,
            "subsequent_cycle_learning_update_applied": False,
        }
        request_record = {**payload, "learning_update_request_digest": sha(payload)}
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_review_receipt.get(field, "")) for field in fields},
        "post_closeout_review_receipt_digest": str(record.get("post_closeout_review_receipt_digest", "")),
        "learning_update_scope": scope,
        "learning_update_constraints_digest": sha(constraints) if constraints else "",
        "subsequent_cycle_learning_update_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleLearningUpdateRequest(**outer, receipt_digest=sha(outer))