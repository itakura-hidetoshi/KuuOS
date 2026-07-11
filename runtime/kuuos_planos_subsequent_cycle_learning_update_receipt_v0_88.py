from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_learning_update_receipt_v0_88"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_learning_update_request_v0_87"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_learning_update_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "closeout_evidence_preserved": True,
    "post_closeout_review_evidence_preserved": True,
    "learning_update_scope_preserved": True,
    "learning_update_constraints_digest_preserved": True,
    "subsequent_cycle_learning_update_requested": True,
    "subsequent_cycle_learning_update_applied": True,
    "subsequent_cycle_next_iteration_requested": False,
}

@dataclass(frozen=True)
class SubsequentCycleLearningUpdateReceipt:
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
    subsequent_cycle_learning_update_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_learning_update_receipt(
    source_learning_update_request: Mapping[str, Any],
    *,
    learning_update_result: Mapping[str, Any] | None = None,
) -> SubsequentCycleLearningUpdateReceipt:
    blockers: list[str] = []
    if source_learning_update_request.get("version") != SOURCE_VERSION:
        blockers.append("source_learning_update_request_version_invalid")
    if source_learning_update_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_REQUEST_READY":
        blockers.append("source_learning_update_request_not_ready")
    if not source_learning_update_request.get("receipt_digest"):
        blockers.append("source_learning_update_request_receipt_digest_missing")

    boundary = _m(source_learning_update_request.get("boundary"))
    if boundary.get("subsequent_cycle_learning_update_requested") is not True:
        blockers.append("source_boundary_learning_update_requested_missing")
    if boundary.get("subsequent_cycle_learning_update_applied") is not False:
        blockers.append("source_boundary_learning_update_applied_promoted")

    record = _m(source_learning_update_request.get("subsequent_cycle_learning_update_request"))
    if not record or not record.get("learning_update_request_digest"):
        blockers.append("source_learning_update_request_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "closeout_receipt_digest", "post_closeout_review_receipt_digest",
        "learning_update_scope", "learning_update_constraints_digest",
    )
    for field in fields:
        if not source_learning_update_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_learning_update_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    result = dict(learning_update_result or {
        "review_outcome_integrated": True,
        "closeout_evidence_preserved": True,
        "selected_candidate_learning_bound": True,
        "next_iteration_remains_separate": True,
    })
    if not result:
        blockers.append("learning_update_result_missing")

    update_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_learning_update_request_receipt_digest": str(source_learning_update_request["receipt_digest"]),
            "source_learning_update_request_digest": str(record["learning_update_request_digest"]),
            **{field: str(source_learning_update_request[field]) for field in fields},
            "learning_update_result_digest": sha(result),
            "subsequent_cycle_learning_update_requested": True,
            "subsequent_cycle_learning_update_applied": True,
            "subsequent_cycle_next_iteration_requested": False,
        }
        update_record = {**payload, "learning_update_receipt_digest": sha(payload)}
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_learning_update_request.get(field, "")) for field in fields},
        "subsequent_cycle_learning_update_receipt": update_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleLearningUpdateReceipt(**outer, receipt_digest=sha(outer))
