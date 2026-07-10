from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_admission_grant_v0_75"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_admission_request_v0_74"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_GRANT_READY"

BOUNDARY = {
    "grant_owned_by_plan_os": True,
    "source_subsequent_cycle_admission_request_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "admission_scope_preserved": True,
    "admission_constraints_digest_preserved": True,
    "subsequent_cycle_admission_grant_only": True,
    "subsequent_cycle_admission_requested": True,
    "subsequent_cycle_admission_granted": True,
    "subsequent_cycle_started": False,
}


@dataclass(frozen=True)
class SubsequentCycleAdmissionGrantRecord:
    source_admission_request_receipt_digest: str
    source_admission_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    grant_rationale_digest: str
    admission_grant_digest: str
    subsequent_cycle_admission_requested: bool = True
    subsequent_cycle_admission_granted: bool = True
    subsequent_cycle_started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleAdmissionGrantReceipt:
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
    grant_rationale_digest: str
    subsequent_cycle_admission_grant: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def build_subsequent_cycle_admission_grant(
    source_admission_request: Mapping[str, Any],
    *,
    grant_rationale: Mapping[str, Any] | None = None,
) -> SubsequentCycleAdmissionGrantReceipt:
    blockers: list[str] = []
    if source_admission_request.get("version") != SOURCE_VERSION:
        blockers.append("source_admission_request_version_invalid")
    if source_admission_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_REQUEST_READY":
        blockers.append("source_admission_request_not_ready")
    if not source_admission_request.get("receipt_digest"):
        blockers.append("source_admission_request_receipt_digest_missing")

    boundary = _m(source_admission_request.get("boundary"))
    for field in (
        "subsequent_cycle_candidate_selected",
        "subsequent_cycle_admission_requested",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in ("subsequent_cycle_admission_granted", "subsequent_cycle_started"):
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    record = _m(source_admission_request.get("subsequent_cycle_admission_request"))
    if not record:
        blockers.append("source_admission_request_record_missing")
    elif not record.get("admission_request_digest"):
        blockers.append("source_admission_request_digest_missing")

    for field in (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
        "admission_scope",
        "admission_constraints_digest",
    ):
        if not source_admission_request.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_admission_request.get(field):
            blockers.append(f"source_record_{field}_mismatch")

    rationale = dict(grant_rationale or {
        "selected_candidate_evidence_preserved": True,
        "admission_constraints_satisfied": True,
        "admission_grant_separate_from_cycle_start": True,
        "cycle_start_remains_closed": True,
    })
    if not rationale:
        blockers.append("grant_rationale_missing")
    rationale_digest = sha(rationale) if rationale else ""

    grant_record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_GRANT_BLOCKED"
    if not blockers:
        payload = {
            "source_admission_request_receipt_digest": str(source_admission_request["receipt_digest"]),
            "source_admission_request_digest": str(record["admission_request_digest"]),
            "selected_candidate_id": str(source_admission_request["selected_candidate_id"]),
            "selected_candidate_digest": str(source_admission_request["selected_candidate_digest"]),
            "candidate_set_digest": str(source_admission_request["candidate_set_digest"]),
            "evaluation_set_digest": str(source_admission_request["evaluation_set_digest"]),
            "review_set_digest": str(source_admission_request["review_set_digest"]),
            "admission_scope": str(source_admission_request["admission_scope"]),
            "admission_constraints_digest": str(source_admission_request["admission_constraints_digest"]),
            "grant_rationale_digest": rationale_digest,
        }
        grant_record = SubsequentCycleAdmissionGrantRecord(
            **payload,
            admission_grant_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY

    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_admission_request.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_admission_request.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_admission_request.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_admission_request.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_admission_request.get("review_set_digest", "")),
        "admission_scope": str(source_admission_request.get("admission_scope", "")),
        "admission_constraints_digest": str(source_admission_request.get("admission_constraints_digest", "")),
        "grant_rationale_digest": rationale_digest,
        "subsequent_cycle_admission_grant": grant_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleAdmissionGrantReceipt(**outer, receipt_digest=sha(outer))
