from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69"
REQUIRED_SELECTION_SCOPE = "subsequent_cycle_selection_eligible_candidates"

BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_candidate_review_receipt_preserved": True,
    "selected_candidate_provenance_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "review_set_digest_preserved": True,
    "review_count_exact_preserved": True,
    "candidate_review_completed_preserved": True,
    "selection_eligibility_preserved": True,
    "selection_eligible_set_nonempty": True,
    "memory_overwrite_preserved": True,
    "truth_authority_preserved": True,
    "blocker_release_preserved": True,
    "next_cycle_cycle_closed": True,
    "subsequent_cycle_replan_requested": True,
    "subsequent_cycle_candidate_generation_started": True,
    "subsequent_cycle_candidate_set_materialized": True,
    "subsequent_cycle_candidate_evaluations_recorded": True,
    "subsequent_cycle_candidate_review_requested": True,
    "subsequent_cycle_candidate_review_completed": True,
    "subsequent_cycle_candidate_selection_authorization_request_only": True,
    "subsequent_cycle_candidate_selection_authorization_requested": True,
    "subsequent_cycle_selection_scope_bound": True,
    "subsequent_cycle_selection_policy_digest_bound": True,
    "subsequent_cycle_selection_authority_granted": False,
    "subsequent_cycle_candidate_selection_requested": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

REQUIRED_SOURCE_TRUE = (
    "receipt_owned_by_plan_os",
    "source_candidate_review_request_preserved",
    "source_candidate_evaluation_receipt_preserved",
    "selected_candidate_provenance_preserved",
    "candidate_set_digest_preserved",
    "evaluation_set_digest_preserved",
    "evaluation_count_exact_preserved",
    "review_scope_preserved",
    "review_criteria_digest_preserved",
    "all_materialized_candidates_evaluated_preserved",
    "evaluation_score_bounds_valid_preserved",
    "evaluation_order_nonselection_preserved",
    "memory_overwrite_preserved",
    "truth_authority_preserved",
    "blocker_release_preserved",
    "next_cycle_cycle_closed",
    "subsequent_cycle_replan_requested",
    "subsequent_cycle_candidate_generation_started",
    "subsequent_cycle_candidate_set_materialized",
    "subsequent_cycle_candidate_evaluations_recorded",
    "subsequent_cycle_candidate_review_requested",
    "subsequent_cycle_candidate_review_receipt_only",
    "subsequent_cycle_all_evaluated_candidates_reviewed",
    "subsequent_cycle_candidate_review_count_exact",
    "subsequent_cycle_candidate_review_outcomes_recorded",
    "subsequent_cycle_candidate_review_completed",
    "subsequent_cycle_review_order_is_not_selection",
    "subsequent_cycle_selection_eligibility_recorded",
)

REQUIRED_SOURCE_FALSE = (
    "subsequent_cycle_selection_authority_granted",
    "subsequent_cycle_candidate_selection_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class SelectionAuthorizationRequestRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_candidate_review_receipt_digest: str
    source_candidate_review_request_digest: str
    source_candidate_evaluation_receipt_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    candidate_count: int
    evaluation_count: int
    review_count: int
    selection_eligible_count: int
    selection_eligible_set_digest: str
    selection_scope: str
    selection_policy_digest: str
    authorization_request_digest: str
    request_scope: str = "subsequent_cycle_candidate_selection_authorization_request_only"
    candidate_review_completed: bool = True
    selection_eligibility_preserved: bool = True
    candidate_selection_authorization_requested: bool = True
    selection_authority_granted: bool = False
    candidate_selection_requested: bool = False
    candidate_selected: bool = False
    admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SelectionAuthorizationRequest:
    version: str
    source_version: str
    status: str
    source_candidate_review_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    evaluation_set_digest: str
    review_set_digest: str
    candidate_count: int
    evaluation_count: int
    review_count: int
    selection_eligible_count: int
    selection_eligible_candidates: list[dict[str, Any]]
    selection_eligible_set_digest: str
    selection_scope: str
    selection_policy_digest: str
    subsequent_cycle_candidate_selection_authorization_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _record(source: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(source.get("subsequent_cycle_candidate_review_receipt"))


def _source_blockers(source: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if source.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_review_receipt_version_invalid")
    if source.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_READY":
        blockers.append("source_candidate_review_receipt_not_ready")
    boundary = _m(source.get("boundary"))
    for field in REQUIRED_SOURCE_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not source.get("receipt_digest"):
        blockers.append("source_candidate_review_receipt_digest_missing")

    counts = {
        "candidate_count": source.get("candidate_count"),
        "evaluation_count": source.get("evaluation_count"),
        "review_count": source.get("review_count"),
        "selection_eligible_count": source.get("selection_eligible_count"),
    }
    for field, value in counts.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            blockers.append(f"source_{field}_invalid")
    if counts["candidate_count"] <= 0:
        blockers.append("source_candidate_count_not_positive")
    if counts["candidate_count"] != counts["evaluation_count"]:
        blockers.append("source_evaluation_count_not_exact")
    if counts["evaluation_count"] != counts["review_count"]:
        blockers.append("source_review_count_not_exact")
    if counts["selection_eligible_count"] <= 0:
        blockers.append("source_selection_eligible_set_empty")

    outcomes = source.get("review_outcomes")
    if not isinstance(outcomes, list) or not outcomes:
        blockers.append("source_review_outcomes_missing_or_empty")
        outcomes = []
    if len(outcomes) != counts["review_count"]:
        blockers.append("source_review_outcome_count_mismatch")
    if outcomes and sha(outcomes) != str(source.get("review_set_digest", "")):
        blockers.append("source_review_set_digest_invalid")

    eligible_count = 0
    candidate_ids: list[str] = []
    review_digests: list[str] = []
    for ordinal, raw in enumerate(outcomes):
        outcome = _m(raw)
        candidate_id = str(outcome.get("candidate_id", ""))
        review_digest = str(outcome.get("review_digest", ""))
        if not candidate_id:
            blockers.append(f"source_review_{ordinal}_candidate_id_missing")
        if not review_digest:
            blockers.append(f"source_review_{ordinal}_review_digest_missing")
        if outcome.get("review_ordinal") != ordinal:
            blockers.append(f"source_review_{ordinal}_ordinal_mismatch")
        if outcome.get("selection_eligible") is True:
            eligible_count += 1
        if candidate_id:
            candidate_ids.append(candidate_id)
        if review_digest:
            review_digests.append(review_digest)
    if len(candidate_ids) != len(set(candidate_ids)):
        blockers.append("source_review_candidate_ids_not_unique")
    if len(review_digests) != len(set(review_digests)):
        blockers.append("source_review_digests_not_unique")
    if eligible_count != counts["selection_eligible_count"]:
        blockers.append("source_selection_eligible_count_mismatch")

    record = _record(source)
    if not record:
        blockers.append("source_candidate_review_record_missing")
    else:
        for field in (
            "selected_candidate_id", "selected_candidate_digest",
            "candidate_set_digest", "evaluation_set_digest", "review_set_digest",
            "candidate_count", "evaluation_count", "review_count", "selection_eligible_count",
        ):
            if record.get(field) != source.get(field):
                blockers.append(f"source_record_{field}_mismatch")
        if record.get("subsequent_cycle_candidate_review_completed") is not True:
            blockers.append("source_record_candidate_review_completed_missing")
        if record.get("subsequent_cycle_selection_eligibility_recorded") is not True:
            blockers.append("source_record_selection_eligibility_missing")
        for field in (
            "subsequent_cycle_selection_authority_granted",
            "subsequent_cycle_candidate_selection_requested",
            "subsequent_cycle_candidate_selected",
            "subsequent_cycle_admission_requested",
        ):
            if record.get(field) is not False:
                blockers.append(f"source_record_{field}_promoted")
    return blockers


def build_subsequent_cycle_candidate_selection_authorization_request(
    *,
    candidate_review_receipt: Mapping[str, Any],
    selection_scope: str,
    selection_policy_digest: str,
) -> SelectionAuthorizationRequest:
    source = _m(candidate_review_receipt)
    blockers = _source_blockers(source)
    normalized_scope = str(selection_scope).strip()
    normalized_policy = str(selection_policy_digest).strip()
    if normalized_scope != REQUIRED_SELECTION_SCOPE:
        blockers.append("selection_scope_invalid")
    if not normalized_policy:
        blockers.append("selection_policy_digest_missing")

    outcomes = source.get("review_outcomes") if isinstance(source.get("review_outcomes"), list) else []
    eligible = [
        {
            "candidate_id": str(_m(outcome).get("candidate_id", "")),
            "candidate_digest": str(_m(outcome).get("candidate_digest", "")),
            "evaluation_digest": str(_m(outcome).get("evaluation_digest", "")),
            "review_digest": str(_m(outcome).get("review_digest", "")),
            "total_score": _m(outcome).get("total_score"),
            "review_disposition": str(_m(outcome).get("review_disposition", "")),
        }
        for outcome in outcomes
        if _m(outcome).get("selection_eligible") is True
    ]
    eligible_digest = sha(eligible) if eligible else ""
    if not eligible:
        blockers.append("selection_eligible_candidates_missing")

    record = _record(source)
    request_record = None
    if not blockers:
        obj = SelectionAuthorizationRequestRecord(
            selected_candidate_id=str(source.get("selected_candidate_id", "")),
            selected_candidate_digest=str(source.get("selected_candidate_digest", "")),
            source_candidate_review_receipt_digest=str(source.get("receipt_digest", "")),
            source_candidate_review_request_digest=str(record.get("source_candidate_review_request_digest", "")),
            source_candidate_evaluation_receipt_digest=str(record.get("source_candidate_evaluation_receipt_digest", "")),
            candidate_set_digest=str(source.get("candidate_set_digest", "")),
            evaluation_set_digest=str(source.get("evaluation_set_digest", "")),
            review_set_digest=str(source.get("review_set_digest", "")),
            candidate_count=int(source.get("candidate_count", 0)),
            evaluation_count=int(source.get("evaluation_count", 0)),
            review_count=int(source.get("review_count", 0)),
            selection_eligible_count=int(source.get("selection_eligible_count", 0)),
            selection_eligible_set_digest=eligible_digest,
            selection_scope=normalized_scope,
            selection_policy_digest=normalized_policy,
            authorization_request_digest=sha({
                "source_candidate_review_receipt_digest": source.get("receipt_digest"),
                "review_set_digest": source.get("review_set_digest"),
                "selection_eligible_set_digest": eligible_digest,
                "selection_eligible_count": source.get("selection_eligible_count"),
                "selection_scope": normalized_scope,
                "selection_policy_digest": normalized_policy,
                "scope": "subsequent_cycle_candidate_selection_authorization_request_only",
            }),
        )
        request_record = obj.to_dict()

    status = (
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY"
        if not blockers else
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_candidate_review_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": str(source.get("selected_candidate_id", "")),
        "selected_candidate_digest": str(source.get("selected_candidate_digest", "")),
        "candidate_set_digest": str(source.get("candidate_set_digest", "")),
        "evaluation_set_digest": str(source.get("evaluation_set_digest", "")),
        "review_set_digest": str(source.get("review_set_digest", "")),
        "candidate_count": source.get("candidate_count") if isinstance(source.get("candidate_count"), int) else 0,
        "evaluation_count": source.get("evaluation_count") if isinstance(source.get("evaluation_count"), int) else 0,
        "review_count": source.get("review_count") if isinstance(source.get("review_count"), int) else 0,
        "selection_eligible_count": source.get("selection_eligible_count") if isinstance(source.get("selection_eligible_count"), int) else 0,
        "selection_eligible_candidates": eligible,
        "selection_eligible_set_digest": eligible_digest,
        "selection_scope": normalized_scope,
        "selection_policy_digest": normalized_policy,
        "subsequent_cycle_candidate_selection_authorization_request": request_record,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return SelectionAuthorizationRequest(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: ... REVIEW_RECEIPT.json SELECTION_SCOPE SELECTION_POLICY_DIGEST", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    result = build_subsequent_cycle_candidate_selection_authorization_request(
        candidate_review_receipt=source,
        selection_scope=argv[2],
        selection_policy_digest=argv[3],
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
