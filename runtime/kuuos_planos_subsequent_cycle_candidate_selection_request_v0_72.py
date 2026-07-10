from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_request_v0_72"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_candidate_selection_authorization_grant_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "selection_eligible_candidates_preserved": True,
    "authorization_scope_preserved": True,
    "authorization_constraints_digest_preserved": True,
    "selection_authority_grant_preserved": True,
    "subsequent_cycle_candidate_selection_request_only": True,
    "subsequent_cycle_candidate_selection_authorization_requested": True,
    "subsequent_cycle_selection_authority_granted": True,
    "subsequent_cycle_candidate_selection_requested": True,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

SOURCE_TRUE = (
    "grant_owned_by_plan_os",
    "source_candidate_selection_authorization_request_preserved",
    "candidate_set_digest_preserved",
    "evaluation_set_digest_preserved",
    "review_set_digest_preserved",
    "selection_eligible_candidates_preserved",
    "authorization_scope_preserved",
    "authorization_constraints_digest_preserved",
    "subsequent_cycle_candidate_selection_authorization_grant_only",
    "subsequent_cycle_candidate_selection_authorization_requested",
    "subsequent_cycle_selection_authority_granted",
)
SOURCE_FALSE = (
    "subsequent_cycle_candidate_selection_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)

@dataclass(frozen=True)
class CandidateSelectionRequestRecord:
    source_authorization_grant_receipt_digest: str
    source_authorization_grant_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    selection_scope: str
    selection_criteria_digest: str
    selection_request_digest: str
    subsequent_cycle_candidate_selection_authorization_requested: bool = True
    subsequent_cycle_selection_authority_granted: bool = True
    subsequent_cycle_candidate_selection_requested: bool = True
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass(frozen=True)
class CandidateSelectionRequestReceipt:
    version: str
    source_version: str
    status: str
    source_authorization_grant_receipt_digest: str
    source_authorization_grant_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    selection_scope: str
    selection_criteria_digest: str
    subsequent_cycle_candidate_selection_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}

def _source_blockers(source: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_authorization_grant_version_invalid")
    if source.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_GRANT_READY":
        blockers.append("source_authorization_grant_not_ready")
    if not source.get("receipt_digest"):
        blockers.append("source_authorization_grant_receipt_digest_missing")
    boundary = _m(source.get("boundary"))
    for field in SOURCE_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    record = _m(source.get("subsequent_cycle_candidate_selection_authorization_grant"))
    if not record:
        blockers.append("source_authorization_grant_record_missing")
    elif not record.get("authorization_grant_digest"):
        blockers.append("source_authorization_grant_digest_missing")
    count = source.get("selection_eligible_count")
    ids = source.get("eligible_candidate_ids")
    digests = source.get("eligible_candidate_digests")
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        blockers.append("selection_eligible_count_not_positive")
    if not isinstance(ids, list) or not isinstance(digests, list):
        blockers.append("eligible_candidate_identity_set_invalid")
        ids, digests = [], []
    if count != len(ids) or count != len(digests):
        blockers.append("eligible_candidate_identity_count_mismatch")
    if any(not str(value) for value in ids) or len(ids) != len(set(ids)):
        blockers.append("eligible_candidate_ids_invalid")
    if any(not str(value) for value in digests) or len(digests) != len(set(digests)):
        blockers.append("eligible_candidate_digests_invalid")
    for field in (
        "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
        "authorization_scope", "authorization_constraints_digest",
    ):
        if not source.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source.get(field):
            blockers.append(f"source_record_{field}_mismatch")
    if record and record.get("selection_eligible_count") != count:
        blockers.append("source_record_selection_eligible_count_mismatch")
    if record and record.get("eligible_candidate_ids") != ids:
        blockers.append("source_record_eligible_candidate_ids_mismatch")
    if record and record.get("eligible_candidate_digests") != digests:
        blockers.append("source_record_eligible_candidate_digests_mismatch")
    return blockers

def build_subsequent_cycle_candidate_selection_request(
    source_authorization_grant: Mapping[str, Any],
    *,
    selection_scope: str = "subsequent_cycle_candidate_selection_only",
    selection_criteria: Mapping[str, Any] | None = None,
) -> CandidateSelectionRequestReceipt:
    blockers = _source_blockers(source_authorization_grant)
    criteria = dict(selection_criteria or {
        "eligible_candidates_only": True,
        "review_order_not_selection": True,
        "total_score_evidence_only": True,
        "single_candidate_selection_required": True,
        "admission_forbidden_at_request_layer": True,
    })
    if not selection_scope:
        blockers.append("selection_scope_missing")
    if not criteria:
        blockers.append("selection_criteria_missing")
    source_record = _m(source_authorization_grant.get("subsequent_cycle_candidate_selection_authorization_grant"))
    criteria_digest = sha(criteria) if criteria else ""
    record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_authorization_grant_receipt_digest": str(source_authorization_grant["receipt_digest"]),
            "source_authorization_grant_digest": str(source_record["authorization_grant_digest"]),
            "candidate_set_digest": str(source_authorization_grant["candidate_set_digest"]),
            "evaluation_set_digest": str(source_authorization_grant["evaluation_set_digest"]),
            "review_set_digest": str(source_authorization_grant["review_set_digest"]),
            "selection_eligible_count": int(source_authorization_grant["selection_eligible_count"]),
            "eligible_candidate_ids": list(source_authorization_grant["eligible_candidate_ids"]),
            "eligible_candidate_digests": list(source_authorization_grant["eligible_candidate_digests"]),
            "authorization_scope": str(source_authorization_grant["authorization_scope"]),
            "authorization_constraints_digest": str(source_authorization_grant["authorization_constraints_digest"]),
            "selection_scope": selection_scope,
            "selection_criteria_digest": criteria_digest,
        }
        record = CandidateSelectionRequestRecord(**payload, selection_request_digest=sha(payload)).to_dict()
        status = STATUS_READY
    receipt_payload = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_authorization_grant_receipt_digest": str(source_authorization_grant.get("receipt_digest", "")),
        "source_authorization_grant_digest": str(source_record.get("authorization_grant_digest", "")),
        "candidate_set_digest": str(source_authorization_grant.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_authorization_grant.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_authorization_grant.get("review_set_digest", "")),
        "selection_eligible_count": int(source_authorization_grant.get("selection_eligible_count", 0) or 0),
        "eligible_candidate_ids": list(source_authorization_grant.get("eligible_candidate_ids", []) or []),
        "eligible_candidate_digests": list(source_authorization_grant.get("eligible_candidate_digests", []) or []),
        "authorization_scope": str(source_authorization_grant.get("authorization_scope", "")),
        "authorization_constraints_digest": str(source_authorization_grant.get("authorization_constraints_digest", "")),
        "selection_scope": selection_scope,
        "selection_criteria_digest": criteria_digest,
        "subsequent_cycle_candidate_selection_request": record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return CandidateSelectionRequestReceipt(**receipt_payload, receipt_digest=sha(receipt_payload))
