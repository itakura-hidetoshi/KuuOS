from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_receipt_v0_73"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_request_v0_72"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_RECEIPT_READY"

BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_candidate_selection_request_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "selection_eligible_candidates_preserved": True,
    "selection_scope_preserved": True,
    "selection_criteria_digest_preserved": True,
    "subsequent_cycle_candidate_selection_receipt_only": True,
    "subsequent_cycle_selection_authority_granted": True,
    "subsequent_cycle_candidate_selection_requested": True,
    "subsequent_cycle_candidate_selected": True,
    "subsequent_cycle_admission_requested": False,
}

@dataclass(frozen=True)
class CandidateSelectionRecord:
    source_selection_request_receipt_digest: str
    source_selection_request_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_scope: str
    selection_criteria_digest: str
    selection_rationale_digest: str
    selection_receipt_digest: str
    subsequent_cycle_selection_authority_granted: bool = True
    subsequent_cycle_candidate_selection_requested: bool = True
    subsequent_cycle_candidate_selected: bool = True
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class CandidateSelectionReceipt:
    version: str
    source_version: str
    status: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_scope: str
    selection_criteria_digest: str
    subsequent_cycle_candidate_selection_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}

def build_subsequent_cycle_candidate_selection_receipt(
    source_selection_request: Mapping[str, Any],
    *,
    selected_candidate_id: str,
    selection_rationale: Mapping[str, Any] | None = None,
) -> CandidateSelectionReceipt:
    blockers: list[str] = []
    if source_selection_request.get("version") != SOURCE_VERSION:
        blockers.append("source_selection_request_version_invalid")
    if source_selection_request.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_REQUEST_READY":
        blockers.append("source_selection_request_not_ready")
    boundary = _m(source_selection_request.get("boundary"))
    for field in (
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_selection_requested",
    ):
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in ("subsequent_cycle_candidate_selected", "subsequent_cycle_admission_requested"):
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    record = _m(source_selection_request.get("subsequent_cycle_candidate_selection_request"))
    if not record or not record.get("selection_request_digest"):
        blockers.append("source_selection_request_record_missing")
    ids = list(source_selection_request.get("eligible_candidate_ids", []) or [])
    digests = list(source_selection_request.get("eligible_candidate_digests", []) or [])
    if len(ids) != len(digests) or not ids:
        blockers.append("eligible_candidate_identity_set_invalid")
    if selected_candidate_id not in ids:
        blockers.append("selected_candidate_not_eligible")
    selected_digest = digests[ids.index(selected_candidate_id)] if selected_candidate_id in ids else ""
    rationale = dict(selection_rationale or {
        "review_eligibility_respected": True,
        "selection_scope_respected": True,
        "selection_criteria_applied": True,
        "admission_remains_closed": True,
    })
    if not rationale:
        blockers.append("selection_rationale_missing")
    for field in ("candidate_set_digest", "evaluation_set_digest", "review_set_digest", "selection_scope", "selection_criteria_digest"):
        if not source_selection_request.get(field):
            blockers.append(f"source_{field}_missing")
    receipt_record = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_RECEIPT_BLOCKED"
    if not blockers:
        payload = {
            "source_selection_request_receipt_digest": str(source_selection_request["receipt_digest"]),
            "source_selection_request_digest": str(record["selection_request_digest"]),
            "selected_candidate_id": selected_candidate_id,
            "selected_candidate_digest": selected_digest,
            "candidate_set_digest": str(source_selection_request["candidate_set_digest"]),
            "evaluation_set_digest": str(source_selection_request["evaluation_set_digest"]),
            "review_set_digest": str(source_selection_request["review_set_digest"]),
            "selection_scope": str(source_selection_request["selection_scope"]),
            "selection_criteria_digest": str(source_selection_request["selection_criteria_digest"]),
            "selection_rationale_digest": sha(rationale),
        }
        receipt_record = CandidateSelectionRecord(**payload, selection_receipt_digest=sha(payload)).to_dict()
        status = STATUS_READY
    outer = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "selected_candidate_id": selected_candidate_id,
        "selected_candidate_digest": selected_digest,
        "candidate_set_digest": str(source_selection_request.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_selection_request.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_selection_request.get("review_set_digest", "")),
        "selection_scope": str(source_selection_request.get("selection_scope", "")),
        "selection_criteria_digest": str(source_selection_request.get("selection_criteria_digest", "")),
        "subsequent_cycle_candidate_selection_receipt": receipt_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return CandidateSelectionReceipt(**outer, receipt_digest=sha(outer))
