from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69"
STATUS_READY = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_candidate_review_receipt_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "candidate_review_completed_preserved": True,
    "selection_eligibility_preserved": True,
    "review_order_is_not_selection_preserved": True,
    "subsequent_cycle_candidate_selection_authorization_request_only": True,
    "subsequent_cycle_candidate_selection_authorization_requested": True,
    "subsequent_cycle_selection_authority_granted": False,
    "subsequent_cycle_candidate_selection_requested": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

SOURCE_TRUE = (
    "receipt_owned_by_plan_os",
    "source_candidate_review_request_preserved",
    "source_candidate_evaluation_receipt_preserved",
    "candidate_set_digest_preserved",
    "evaluation_set_digest_preserved",
    "review_scope_preserved",
    "review_criteria_digest_preserved",
    "subsequent_cycle_all_evaluated_candidates_reviewed",
    "subsequent_cycle_candidate_review_count_exact",
    "subsequent_cycle_candidate_review_outcomes_recorded",
    "subsequent_cycle_candidate_review_completed",
    "subsequent_cycle_review_order_is_not_selection",
    "subsequent_cycle_selection_eligibility_recorded",
)

SOURCE_FALSE = (
    "subsequent_cycle_selection_authority_granted",
    "subsequent_cycle_candidate_selection_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class SelectionAuthorizationRequestRecord:
    source_candidate_review_receipt_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    candidate_count: int
    evaluation_count: int
    review_count: int
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    authorization_request_digest: str
    subsequent_cycle_candidate_selection_authorization_requested: bool = True
    subsequent_cycle_selection_authority_granted: bool = False
    subsequent_cycle_candidate_selection_requested: bool = False
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectionAuthorizationRequestReceipt:
    version: str
    source_version: str
    status: str
    source_candidate_review_receipt_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    candidate_count: int
    evaluation_count: int
    review_count: int
    selection_eligible_count: int
    eligible_candidate_ids: list[str]
    eligible_candidate_digests: list[str]
    authorization_scope: str
    authorization_constraints_digest: str
    subsequent_cycle_candidate_selection_authorization_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _source_blockers(source: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_review_receipt_version_invalid")
    if source.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_READY":
        blockers.append("source_candidate_review_receipt_not_ready")
    if not source.get("receipt_digest"):
        blockers.append("source_candidate_review_receipt_digest_missing")

    boundary = _mapping(source.get("boundary"))
    for field in SOURCE_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in SOURCE_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    outcomes = source.get("review_outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        blockers.append("source_review_outcomes_missing_or_empty")
        outcomes = []

    candidate_count = source.get("candidate_count")
    evaluation_count = source.get("evaluation_count")
    review_count = source.get("review_count")
    eligible_count = source.get("selection_eligible_count")
    for name, value in (
        ("candidate_count", candidate_count),
        ("evaluation_count", evaluation_count),
        ("review_count", review_count),
        ("selection_eligible_count", eligible_count),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"source_{name}_invalid")
    if isinstance(candidate_count, int) and candidate_count <= 0:
        blockers.append("source_candidate_count_not_positive")
    if candidate_count != evaluation_count or evaluation_count != review_count:
        blockers.append("source_candidate_evaluation_review_count_mismatch")
    if review_count != len(outcomes):
        blockers.append("source_review_outcome_count_mismatch")
    if outcomes and sha(outcomes) != source.get("review_set_digest"):
        blockers.append("source_review_set_digest_invalid")

    eligible = [item for item in outcomes if _mapping(item).get("selection_eligible") is True]
    if eligible_count != len(eligible):
        blockers.append("source_selection_eligible_count_mismatch")
    if not eligible:
        blockers.append("source_no_selection_eligible_candidate")

    ids = [str(_mapping(item).get("candidate_id", "")) for item in eligible]
    digests = [str(_mapping(item).get("candidate_digest", "")) for item in eligible]
    if any(not value for value in ids):
        blockers.append("eligible_candidate_id_missing")
    if any(not value for value in digests):
        blockers.append("eligible_candidate_digest_missing")
    if len(ids) != len(set(ids)):
        blockers.append("eligible_candidate_id_duplicate")
    if len(digests) != len(set(digests)):
        blockers.append("eligible_candidate_digest_duplicate")

    for field in ("candidate_set_digest", "evaluation_set_digest", "review_set_digest"):
        if not source.get(field):
            blockers.append(f"source_{field}_missing")
    return blockers


def build_subsequent_cycle_candidate_selection_authorization_request(
    source_review_receipt: Mapping[str, Any],
    *,
    authorization_scope: str = "subsequent_cycle_candidate_selection_only",
    authorization_constraints: Mapping[str, Any] | None = None,
) -> SelectionAuthorizationRequestReceipt:
    blockers = _source_blockers(source_review_receipt)
    constraints = dict(authorization_constraints or {
        "selection_must_use_review_eligible_candidates_only": True,
        "review_order_must_not_be_used_as_selection": True,
        "total_score_must_remain_evidence_not_authority": True,
        "authorization_grant_required_before_selection_request": True,
        "candidate_selection_forbidden_at_request_layer": True,
        "admission_forbidden_at_request_layer": True,
    })
    if not authorization_scope:
        blockers.append("authorization_scope_missing")
    if not constraints:
        blockers.append("authorization_constraints_missing")

    outcomes = source_review_receipt.get("review_outcomes")
    outcomes = outcomes if isinstance(outcomes, list) else []
    eligible = [_mapping(item) for item in outcomes if _mapping(item).get("selection_eligible") is True]
    eligible_ids = [str(item.get("candidate_id", "")) for item in eligible]
    eligible_digests = [str(item.get("candidate_digest", "")) for item in eligible]
    constraints_digest = sha(constraints) if constraints else ""

    record: dict[str, Any] | None = None
    status = "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_BLOCKED"
    if not blockers:
        payload = {
            "source_candidate_review_receipt_digest": str(source_review_receipt["receipt_digest"]),
            "candidate_set_digest": str(source_review_receipt["candidate_set_digest"]),
            "evaluation_set_digest": str(source_review_receipt["evaluation_set_digest"]),
            "review_set_digest": str(source_review_receipt["review_set_digest"]),
            "candidate_count": int(source_review_receipt["candidate_count"]),
            "evaluation_count": int(source_review_receipt["evaluation_count"]),
            "review_count": int(source_review_receipt["review_count"]),
            "selection_eligible_count": int(source_review_receipt["selection_eligible_count"]),
            "eligible_candidate_ids": eligible_ids,
            "eligible_candidate_digests": eligible_digests,
            "authorization_scope": authorization_scope,
            "authorization_constraints_digest": constraints_digest,
        }
        request_digest = sha(payload)
        record = SelectionAuthorizationRequestRecord(
            **payload,
            authorization_request_digest=request_digest,
        ).to_dict()
        status = STATUS_READY

    receipt_payload = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_candidate_review_receipt_digest": str(source_review_receipt.get("receipt_digest", "")),
        "candidate_set_digest": str(source_review_receipt.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source_review_receipt.get("evaluation_set_digest", "")),
        "review_set_digest": str(source_review_receipt.get("review_set_digest", "")),
        "candidate_count": int(source_review_receipt.get("candidate_count", 0) or 0),
        "evaluation_count": int(source_review_receipt.get("evaluation_count", 0) or 0),
        "review_count": int(source_review_receipt.get("review_count", 0) or 0),
        "selection_eligible_count": int(source_review_receipt.get("selection_eligible_count", 0) or 0),
        "eligible_candidate_ids": eligible_ids,
        "eligible_candidate_digests": eligible_digests,
        "authorization_scope": authorization_scope,
        "authorization_constraints_digest": constraints_digest,
        "subsequent_cycle_candidate_selection_authorization_request": record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SelectionAuthorizationRequestReceipt(
        **receipt_payload,
        receipt_digest=sha(receipt_payload),
    )
