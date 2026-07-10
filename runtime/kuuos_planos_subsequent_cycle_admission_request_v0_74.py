from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_admission_request_v0_74"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_receipt_v0_73"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_candidate_selection_receipt_preserved": True,
    "selected_candidate_identity_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "selection_scope_preserved": True,
    "selection_criteria_digest_preserved": True,
    "subsequent_cycle_admission_request_only": True,
    "subsequent_cycle_selection_authority_granted": True,
    "subsequent_cycle_candidate_selection_requested": True,
    "subsequent_cycle_candidate_selected": True,
    "subsequent_cycle_admission_requested": True,
    "subsequent_cycle_admission_granted": False,
    "subsequent_cycle_started": False,
}

@dataclass(frozen=True)
class SubsequentCycleAdmissionRequestRecord:
    source_selection_receipt_digest: str
    source_selection_record_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    admission_scope: str
    admission_constraints_digest: str
    admission_request_digest: str
    subsequent_cycle_admission_requested: bool = True
    subsequent_cycle_admission_granted: bool = False
    subsequent_cycle_started: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class SubsequentCycleAdmissionRequestReceipt:
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
    subsequent_cycle_admission_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}

def build_subsequent_cycle_admission_request(
    source_selection_receipt: Mapping[str, Any],
    *,
    admission_scope: str = "selected_candidate_subsequent_cycle_only",
    admission_constraints: Mapping[str, Any] | None = None,
) -> SubsequentCycleAdmissionRequestReceipt:
    blockers: list[str] = []
    if source_selection_receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_selection_receipt_version_invalid")
    if source_selection_receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_RECEIPT_READY":
        blockers.append("source_selection_receipt_not_ready")
    boundary = _m(source_selection_receipt.get("boundary"))
    for field in (
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_selection_requested",
        "subsequent_cycle_candidate_selected",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    if boundary.get("subsequent_cycle_admission_requested") is not False:
        blockers.append("source_boundary_subsequent_cycle_admission_requested_promoted")
    record = _m(source_selection_receipt.get("subsequent_cycle_candidate_selection_receipt"))
    if not record or not record.get("selection_receipt_digest"):
        blockers.append("source_selection_record_missing")
    for field in (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
    ):
        if not source_selection_receipt.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source_selection_receipt.get(field):
            blockers.append(f"source_record_{field}_mismatch")
    constraints = dict(admission_constraints or {
        "selected_candidate_identity_must_be_preserved": True,
        "admission_grant_required_before_cycle_start": True,
        "cycle_start_forbidden_at_request_layer": True,
    })
    if not admission_scope:
        blockers.append("admission_scope_missing")
    if not constraints:
        blockers.append("admission_constraints_missing")
    constraints_digest = sha(constraints) if constraints else ""
    request_record = None
    status = "PLANOS_SUBSEQUENT_CYCLE_ADMISSION_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_selection_receipt_digest": str(source_selection_receipt["receipt_digest"]),
            "source_selection_record_digest": str(record["selection_receipt_digest"]),
            "selected_candidate_id": str(source_selection_receipt["selected_candidate_id"]),
            "selected_candidate_digest": str(source_selection_receipt["selected_candidate_digest"]),
            "candidate_set_digest": str(source_selection_receipt["candidate_set_digest"]),
            "evaluation_set_digest": str(source_selection_receipt["evaluation_set_digest"]),
            "review_set_digest": str(source_selection_receipt["review_set_digest"]),
            "admission_scope": admission_scope,
            "admission_constraints_digest": constraints_digest,
        }
        request_record = SubsequentCycleAdmissionRequestRecord(
            **payload,
            admission_request_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY
    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": str(source_selection_receipt.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source_selection_receipt.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source_selection_receipt.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_selection_receipt.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_selection_receipt.get("review_set_digest", "")),
        "admission_scope": admission_scope,
        "admission_constraints_digest": constraints_digest,
        "subsequent_cycle_admission_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SubsequentCycleAdmissionRequestReceipt(**outer, receipt_digest=sha(outer))
