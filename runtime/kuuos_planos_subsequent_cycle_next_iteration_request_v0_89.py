from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_next_iteration_request_v0_89"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_learning_update_receipt_v0_88"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_NEXT_ITERATION_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_learning_update_receipt_preserved": True,
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
    "subsequent_cycle_next_iteration_started": False,
}


@dataclass(frozen=True)
class SubsequentCycleNextIterationRequest:
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
    subsequent_cycle_next_iteration_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_next_iteration_request(
    source_learning_update_receipt: Mapping[str, Any],
    *,
    next_iteration_scope: str = "subsequent-cycle-next-iteration",
    next_iteration_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleNextIterationRequest:
    blockers: list[str] = []
    if source_learning_update_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_learning_update_receipt_version_invalid")
    if source_learning_update_receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_LEARNING_UPDATE_RECEIPT_READY":
        blockers.append("source_learning_update_receipt_not_ready")
    if not source_learning_update_receipt.get("receipt_digest"):
        blockers.append("source_learning_update_receipt_digest_missing")

    boundary = _m(source_learning_update_receipt.get("boundary"))
    if boundary.get("subsequent_cycle_learning_update_applied") is not True:
        blockers.append("source_boundary_learning_update_applied_missing")
    if boundary.get("subsequent_cycle_next_iteration_requested") is not False:
        blockers.append("source_boundary_next_iteration_requested_promoted")

    record = _m(source_learning_update_receipt.get("subsequent_cycle_learning_update_receipt"))
    if not record or not record.get("learning_update_receipt_digest"):
        blockers.append("source_learning_update_receipt_record_missing")

    fields = (
        "selected_candidate_id", "selected_candidate_digest",
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "closeout_receipt_digest", "post_closeout_review_receipt_digest",
    )
    for field in fields:
        if not source_learning_update_receipt.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_learning_update_receipt.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    scope = str(next_iteration_scope).strip()
    if not scope:
        blockers.append("next_iteration_scope_missing")

    constraints = dict(next_iteration_constraints or {
        "learning_update_bound": True,
        "selected_candidate_identity_bound": True,
        "closed_cycle_history_preserved": True,
        "next_iteration_start_remains_separate": True,
    })
    if not constraints:
        blockers.append("next_iteration_constraints_missing")

    request_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_NEXT_ITERATION_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_learning_update_receipt_digest": str(source_learning_update_receipt["receipt_digest"]),
            "source_learning_update_record_digest": str(record["learning_update_receipt_digest"]),
            **{field: str(source_learning_update_receipt[field]) for field in fields},
            "learning_update_receipt_digest": str(record["learning_update_receipt_digest"]),
            "next_iteration_scope": scope,
            "next_iteration_constraints_digest": sha(constraints),
            "subsequent_cycle_next_iteration_requested": True,
            "subsequent_cycle_next_iteration_started": False,
        }
        request_record = {**payload, "next_iteration_request_digest": sha(payload)}
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        **{field: str(source_learning_update_receipt.get(field, "")) for field in fields},
        "learning_update_receipt_digest": str(record.get("learning_update_receipt_digest", "")),
        "next_iteration_scope": scope,
        "next_iteration_constraints_digest": sha(constraints) if constraints else "",
        "subsequent_cycle_next_iteration_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleNextIterationRequest(**outer, receipt_digest=sha(outer))
