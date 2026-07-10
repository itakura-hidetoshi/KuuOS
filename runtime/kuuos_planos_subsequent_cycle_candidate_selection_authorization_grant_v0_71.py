from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_authorization_grant_v0_71"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_GRANT_READY"

BOUNDARY = {
    "grant_owned_by_plan_os": True,
    "source_candidate_selection_authorization_request_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "selection_eligible_candidates_preserved": True,
    "authorization_scope_preserved": True,
    "authorization_constraints_digest_preserved": True,
    "subsequent_cycle_candidate_selection_authorization_grant_only": True,
    "subsequent_cycle_candidate_selection_authorization_requested": True,
    "subsequent_cycle_selection_authority_granted": True,
    "subsequent_cycle_candidate_selection_requested": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

SOURCE_TRUE = (
    "request_owned_by_plan_os",
    "source_candidate_review_receipt_preserved",
    "candidate_set_digest_preserved",
    "evaluation_set_digest_preserved",
    "review_set_digest_preserved",
    "candidate_review_completed_preserved",
    "selection_eligibility_preserved",
    "review_order_is_not_selection_preserved",
    "subsequent_cycle_candidate_selection_authorization_request_only",
    "subsequent_cycle_candidate_selection_authorization_requested",
)
SOURCE_FALSE = (
    "subsequent_cycle_selection_authority_granted",
    "subsequent_cycle_candidate_selection_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class SelectionAuthorizationGrantRecord:
    source_authorization_request_receipt_digest: str
    source_authorization_request_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    grant_rationale_digest: str
    authorization_grant_digest: str
    subsequent_cycle_candidate_selection_authorization_requested: bool = True
    subsequent_cycle_selection_authority_granted: bool = True
    subsequent_cycle_candidate_selection_requested: bool = False
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectionAuthorizationGrantReceipt:
    version: str
    source_version: str
    status: str
    source_authorization_request_receipt_digest: str
    source_authorization_request_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    grant_rationale_digest: str
    subsequent_cycle_candidate_selection_authorization_grant: dict[str, Any] | None
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
        blockers.append("source_authorization_request_version_invalid")
    if source.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY":
        blockers.append("source_authorization_request_not_ready")
    if not source.get("receipt_digest"):
        blockers.append("source_authorization_request_receipt_digest_missing")
    boundary = _m(source.get("boundary"))
    for field in SOURCE_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    record = _m(source.get("subsequent_cycle_candidate_selection_authorization_request"))
    if not record:
        blockers.append("source_authorization_request_record_missing")
    elif not record.get("authorization_request_digest"):
        blockers.append("source_authorization_request_digest_missing")
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
        "candidate_set_digest",
        "evaluation_set_digest",
        "review_set_digest",
        "authorization_scope",
        "authorization_constraints_digest",
    ):
        if not source.get(field):
            blockers.append(f"source_{field}_missing")
        if record and record.get(field) != source.get(field):
            blockers.append(f"source_record_{field}_mismatch")
    return blockers


def build_subsequent_cycle_candidate_selection_authorization_grant(
    source_authorization_request: Mapping[str, Any],
    *,
    grant_rationale: Mapping[str, Any] | None = None,
) -> SelectionAuthorizationGrantReceipt:
    blockers = _source_blockers(source_authorization_request)
    rationale = dict(grant_rationale or {
        "review_completed": True,
        "eligible_candidate_set_nonempty": True,
        "selection_remains_separate_from_authorization": True,
        "admission_remains_closed": True,
    })
    if not rationale:
        blockers.append("grant_rationale_missing")
    record_source = _m(source_authorization_request.get("subsequent_cycle_candidate_selection_authorization_request"))
    rationale_digest = sha(rationale) if rationale else ""
    record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_GRANT_BLOCKED"
    if not blockers:
        payload = {
            "source_authorization_request_receipt_digest": str(source_authorization_request["receipt_digest"]),
            "source_authorization_request_digest": str(record_source["authorization_request_digest"]),
            "candidate_set_digest": str(source_authorization_request["candidate_set_digest"]),
            "evaluation_set_digest": str(source_authorization_request["evaluation_set_digest"]),
            "review_set_digest": str(source_authorization_request["review_set_digest"]),
            "selection_eligible_count": int(source_authorization_request["selection_eligible_count"]),
            "eligible_candidate_ids": list(source_authorization_request["eligible_candidate_ids"]),
            "eligible_candidate_digests": list(source_authorization_request["eligible_candidate_digests"]),
            "authorization_scope": str(source_authorization_request["authorization_scope"]),
            "authorization_constraints_digest": str(source_authorization_request["authorization_constraints_digest"]),
            "grant_rationale_digest": rationale_digest,
        }
        record = SelectionAuthorizationGrantRecord(
            **payload,
            authorization_grant_digest=sha(payload),
        ).to_dict()
        status = STATUS_READY
    receipt_payload = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_authorization_request_receipt_digest": str(source_authorization_request.get("receipt_digest", "")),
        "source_authorization_request_digest": str(record_source.get("authorization_request_digest", "")),
        "candidate_set_digest": str(source_authorization_request.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_authorization_request.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_authorization_request.get("review_set_digest", "")),
        "selection_eligible_count": int(source_authorization_request.get("selection_eligible_count", 0) or 0),
        "eligible_candidate_ids": list(source_authorization_request.get("eligible_candidate_ids", []) or []),
        "eligible_candidate_digests": list(source_authorization_request.get("eligible_candidate_digests", []) or []),
        "authorization_scope": str(source_authorization_request.get("authorization_scope", "")),
        "authorization_constraints_digest": str(source_authorization_request.get("authorization_constraints_digest", "")),
        "grant_rationale_digest": rationale_digest,
        "subsequent_cycle_candidate_selection_authorization_grant": record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SelectionAuthorizationGrantReceipt(**receipt_payload, receipt_digest=sha(receipt_payload))
