from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_start_receipt_v0_77"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_start_request_v0_76"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_START_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_subsequent_cycle_start_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_scope_preserved": True,
    "admission_constraints_digest_preserved": True,
    "start_scope_preserved": True,
    "start_constraints_digest_preserved": True,
    "subsequent_cycle_start_receipt_only": True,
    "subsequent_cycle_start_requested": True,
    "subsequent_cycle_started": True,
    "subsequent_cycle_execution_requested": False,
}


@dataclass(frozen=True)
class SubsequentCycleStartRecord:
    source_start_request_receipt_digest: str
    source_start_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    start_scope: str
    start_constraints_digest: str
    start_rationale_digest: str
    subsequent_cycle_start_receipt_digest: str
    subsequent_cycle_start_requested: bool = True
    subsequent_cycle_started: bool = True
    subsequent_cycle_execution_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleStartReceipt:
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
    subsequent_cycle_start_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_start_receipt(
    source_start_request: Mapping[str, Any],
    *,
    start_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleStartReceipt:
    blockers: list[str] = []
    if source_start_request.get("version") != SOURCE_VERSION:
        blockers.append("source_start_request_version_invalid")
    if source_start_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_START_REQUEST_READY":
        blockers.append("source_start_request_not_ready")
    if not source_start_request.get("receipt_digest"):
        blockers.append("source_start_request_receipt_digest_missing")

    boundary = _m(source_start_request.get("boundary"))
    for field in (
        "subsequent_cycle_admission_granted",
        "subsequent_cycle_start_requested",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    if boundary.get("subsequent_cycle_started") is not False:
        blockers.append("source_boundary_subsequent_cycle_started_promoted")

    record = _m(source_start_request.get("subsequent_cycle_start_request"))
    if not record or not record.get("start_request_digest"):
        blockers.append("source_start_request_record_missing")

    for field in (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
        "admission_scope",
        "admission_constraints_digest",
        "start_scope",
        "start_constraints_digest",
    ):
        if not source_start_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_start_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(start_rationale or {
        "admission_grant_preserved": True,
        "start_scope_respected": True,
        "start_constraints_respected": True,
        "execution_remains_separate": True,
    })
    if not rationale:
        blockers.append("start_rationale_missing")

    receipt_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_START_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_start_request_receipt_digest": str(source_start_request["receipt_digest"]),
            "source_start_request_digest": str(record["start_request_digest"]),
            "selected_candidate_id": str(source_start_request["selected_candidate_id"]),
            "selected_candidate_digest": str(source_start_request["selected_candidate_digest"]),
            "candidate_set_digest": str(source_start_request["candidate_set_digest"]),
            "evaluation_set_digest": str(source_start_request["evaluation_set_digest"]),
            "review_set_digest": str(source_start_request["review_set_digest"]),
            "admission_scope": str(source_start_request["admission_scope"]),
            "admission_constraints_digest": str(source_start_request["admission_constraints_digest"]),
            "start_scope": str(source_start_request["start_scope"]),
            "start_constraints_digest": str(source_start_request["start_constraints_digest"]),
            "start_rationale_digest": sha(rationale),
        }
        receipt_record = SubsequentCycleStartRecord(
            **payload,
            subsequent_cycle_start_receipt_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_start_request.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_start_request.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_start_request.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_start_request.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_start_request.get("review_set_digest", "")),
        "admission_scope": str(source_start_request.get("admission_scope", "")),
        "admission_constraints_digest": str(source_start_request.get("admission_constraints_digest", "")),
        "start_scope": str(source_start_request.get("start_scope", "")),
        "start_constraints_digest": str(source_start_request.get("start_constraints_digest", "")),
        "subsequent_cycle_start_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleStartReceipt(**outer, receipt_digest=sha(outer))
