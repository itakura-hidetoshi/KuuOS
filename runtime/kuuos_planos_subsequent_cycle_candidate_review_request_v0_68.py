from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_review_request_v0_68"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67"
REQUIRED_REVIEW_SCOPE = "subsequent_cycle_candidate_evaluation_set"

SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_BOUNDARY = {
    "request_owned_by_plan_os": True,
    "source_candidate_evaluation_receipt_preserved": True,
    "selected_candidate_provenance_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "evaluation_count_exact_preserved": True,
    "all_materialized_candidates_evaluated_preserved": True,
    "evaluation_score_bounds_valid_preserved": True,
    "evaluation_order_nonselection_preserved": True,
    "memory_overwrite_preserved": True,
    "truth_authority_preserved": True,
    "blocker_release_preserved": True,
    "next_cycle_cycle_closed": True,
    "subsequent_cycle_replan_requested": True,
    "subsequent_cycle_candidate_generation_started": True,
    "subsequent_cycle_candidate_set_materialized": True,
    "subsequent_cycle_candidate_evaluations_recorded": True,
    "subsequent_cycle_candidate_review_request_only": True,
    "subsequent_cycle_candidate_review_requested": True,
    "subsequent_cycle_review_scope_bound": True,
    "subsequent_cycle_review_criteria_digest_bound": True,
    "subsequent_cycle_selection_authority_granted": False,
    "subsequent_cycle_candidate_review_completed": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "receipt_owned_by_plan_os",
    "source_candidate_set_materialization_receipt_preserved",
    "selected_candidate_provenance_preserved",
    "candidate_set_digest_preserved",
    "candidate_set_nonempty_preserved",
    "candidate_ids_unique_preserved",
    "memory_overwrite_preserved",
    "truth_authority_preserved",
    "blocker_release_preserved",
    "next_cycle_cycle_closed",
    "subsequent_cycle_replan_requested",
    "subsequent_cycle_candidate_generation_started",
    "subsequent_cycle_candidate_set_materialized",
    "subsequent_cycle_candidate_evaluation_receipt_only",
    "subsequent_cycle_all_materialized_candidates_evaluated",
    "subsequent_cycle_candidate_evaluation_count_exact",
    "subsequent_cycle_candidate_evaluation_score_bounds_valid",
    "subsequent_cycle_candidate_evaluations_recorded",
    "subsequent_cycle_evaluation_order_is_not_selection",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "subsequent_cycle_candidate_review_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class SubsequentCycleCandidateReviewRequestRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_candidate_evaluation_receipt_digest: str
    source_candidate_set_materialization_receipt_digest: str
    source_candidate_generation_start_receipt_digest: str
    source_subsequent_cycle_replan_request_digest: str
    source_next_cycle_closeout_receipt_digest: str
    source_blocker_release_authorization_request_digest: str
    source_truth_authority_closeout_receipt_digest: str
    source_memory_overwrite_closeout_receipt_digest: str
    candidate_set_digest: str
    candidate_count: int
    evaluation_set_digest: str
    evaluation_count: int
    review_scope: str
    review_criteria_digest: str
    review_request_digest: str
    request_scope: str = "subsequent_cycle_candidate_review_request_only"
    memory_overwrite_preserved: bool = True
    truth_authority_preserved: bool = True
    blocker_release_preserved: bool = True
    next_cycle_cycle_closed: bool = True
    subsequent_cycle_replan_requested: bool = True
    subsequent_cycle_candidate_generation_started: bool = True
    subsequent_cycle_candidate_set_materialized: bool = True
    subsequent_cycle_candidate_evaluations_recorded: bool = True
    subsequent_cycle_candidate_review_requested: bool = True
    subsequent_cycle_selection_authority_granted: bool = False
    subsequent_cycle_candidate_review_completed: bool = False
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateReviewRequest:
    version: str
    source_version: str
    status: str
    source_candidate_evaluation_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    candidate_count: int
    evaluation_set_digest: str
    evaluation_count: int
    review_scope: str
    review_criteria_digest: str
    subsequent_cycle_candidate_review_request: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _source_evaluation_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("subsequent_cycle_candidate_evaluation_receipt"))


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_evaluation_receipt_version_invalid")
    if receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY":
        blockers.append("source_candidate_evaluation_receipt_not_ready")

    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")

    if not receipt.get("receipt_digest"):
        blockers.append("source_candidate_evaluation_receipt_digest_missing")

    candidate_count = receipt.get("candidate_count")
    evaluation_count = receipt.get("evaluation_count")
    if not isinstance(candidate_count, int) or isinstance(candidate_count, bool) or candidate_count <= 0:
        blockers.append("source_candidate_count_invalid")
    if not isinstance(evaluation_count, int) or isinstance(evaluation_count, bool) or evaluation_count <= 0:
        blockers.append("source_evaluation_count_invalid")
    if candidate_count != evaluation_count:
        blockers.append("source_evaluation_count_not_exact")

    evaluations = receipt.get("evaluations")
    if not isinstance(evaluations, list) or not evaluations:
        blockers.append("source_evaluations_missing_or_empty")
        evaluations = []
    if evaluation_count != len(evaluations):
        blockers.append("source_evaluation_list_count_mismatch")

    candidate_ids: list[str] = []
    candidate_digests: list[str] = []
    evaluation_digests: list[str] = []
    for ordinal, raw_evaluation in enumerate(evaluations):
        evaluation = _m(raw_evaluation)
        candidate_id = str(evaluation.get("candidate_id", ""))
        candidate_digest = str(evaluation.get("candidate_digest", ""))
        evaluation_digest = str(evaluation.get("evaluation_digest", ""))
        evaluation_ordinal = evaluation.get("evaluation_ordinal")
        if not candidate_id:
            blockers.append(f"source_evaluation_{ordinal}_candidate_id_missing")
        if not candidate_digest:
            blockers.append(f"source_evaluation_{ordinal}_candidate_digest_missing")
        if not evaluation_digest:
            blockers.append(f"source_evaluation_{ordinal}_evaluation_digest_missing")
        if evaluation_ordinal != ordinal:
            blockers.append(f"source_evaluation_{ordinal}_ordinal_mismatch")
        if candidate_id:
            candidate_ids.append(candidate_id)
        if candidate_digest:
            candidate_digests.append(candidate_digest)
        if evaluation_digest:
            evaluation_digests.append(evaluation_digest)
    if len(candidate_ids) != len(set(candidate_ids)):
        blockers.append("source_evaluation_candidate_ids_not_unique")
    if len(candidate_digests) != len(set(candidate_digests)):
        blockers.append("source_evaluation_candidate_digests_not_unique")
    if len(evaluation_digests) != len(set(evaluation_digests)):
        blockers.append("source_evaluation_digests_not_unique")

    candidate_set_digest = str(receipt.get("candidate_set_digest", ""))
    evaluation_set_digest = str(receipt.get("evaluation_set_digest", ""))
    if not candidate_set_digest:
        blockers.append("source_candidate_set_digest_missing")
    if not evaluation_set_digest:
        blockers.append("source_evaluation_set_digest_missing")
    elif evaluations and sha(evaluations) != evaluation_set_digest:
        blockers.append("source_evaluation_set_digest_invalid")

    record = _source_evaluation_record(receipt)
    if not record:
        blockers.append("source_candidate_evaluation_record_missing")
    else:
        for field, expected in (
            ("candidate_count", candidate_count),
            ("evaluation_count", evaluation_count),
            ("candidate_set_digest", candidate_set_digest),
            ("evaluation_set_digest", evaluation_set_digest),
        ):
            if record.get(field) != expected:
                blockers.append(f"source_record_{field}_mismatch")
        for field in (
            "subsequent_cycle_all_materialized_candidates_evaluated",
            "subsequent_cycle_candidate_evaluations_recorded",
        ):
            if record.get(field) is not True:
                blockers.append(f"source_record_{field}_missing")
        for field in (
            "subsequent_cycle_candidate_review_requested",
            "subsequent_cycle_candidate_selected",
            "subsequent_cycle_admission_requested",
        ):
            if record.get(field) is not False:
                blockers.append(f"source_record_{field}_promoted")
    return blockers


def build_subsequent_cycle_candidate_review_request(
    *,
    candidate_evaluation_receipt: Mapping[str, Any],
    review_scope: str,
    review_criteria_digest: str,
) -> SubsequentCycleCandidateReviewRequest:
    source = _m(candidate_evaluation_receipt)
    blockers = _source_blockers(source)

    normalized_scope = str(review_scope).strip()
    normalized_criteria_digest = str(review_criteria_digest).strip()
    if normalized_scope != REQUIRED_REVIEW_SCOPE:
        blockers.append("review_scope_invalid")
    if not normalized_criteria_digest:
        blockers.append("review_criteria_digest_missing")

    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    candidate_set_digest = str(source.get("candidate_set_digest", ""))
    evaluation_set_digest = str(source.get("evaluation_set_digest", ""))
    candidate_count = source.get("candidate_count")
    evaluation_count = source.get("evaluation_count")
    if not selected_id:
        blockers.append("selected_candidate_id_missing")
    if not selected_digest:
        blockers.append("selected_candidate_digest_missing")

    source_record = _source_evaluation_record(source)
    if source_record:
        if selected_id and source_record.get("selected_candidate_id") != selected_id:
            blockers.append("selected_candidate_id_evaluation_receipt_mismatch")
        if selected_digest and source_record.get("selected_candidate_digest") != selected_digest:
            blockers.append("selected_candidate_digest_evaluation_receipt_mismatch")

    review_request = None
    if not blockers:
        request_obj = SubsequentCycleCandidateReviewRequestRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_candidate_evaluation_receipt_digest=str(source.get("receipt_digest", "")),
            source_candidate_set_materialization_receipt_digest=str(source_record.get("source_candidate_set_materialization_receipt_digest", "")),
            source_candidate_generation_start_receipt_digest=str(source_record.get("source_candidate_generation_start_receipt_digest", "")),
            source_subsequent_cycle_replan_request_digest=str(source_record.get("source_subsequent_cycle_replan_request_digest", "")),
            source_next_cycle_closeout_receipt_digest=str(source_record.get("source_next_cycle_closeout_receipt_digest", "")),
            source_blocker_release_authorization_request_digest=str(source_record.get("source_blocker_release_authorization_request_digest", "")),
            source_truth_authority_closeout_receipt_digest=str(source_record.get("source_truth_authority_closeout_receipt_digest", "")),
            source_memory_overwrite_closeout_receipt_digest=str(source_record.get("source_memory_overwrite_closeout_receipt_digest", "")),
            candidate_set_digest=candidate_set_digest,
            candidate_count=int(candidate_count),
            evaluation_set_digest=evaluation_set_digest,
            evaluation_count=int(evaluation_count),
            review_scope=normalized_scope,
            review_criteria_digest=normalized_criteria_digest,
            review_request_digest=sha({
                "source_candidate_evaluation_receipt_digest": source.get("receipt_digest"),
                "candidate_set_digest": candidate_set_digest,
                "candidate_count": candidate_count,
                "evaluation_set_digest": evaluation_set_digest,
                "evaluation_count": evaluation_count,
                "review_scope": normalized_scope,
                "review_criteria_digest": normalized_criteria_digest,
                "scope": "subsequent_cycle_candidate_review_request_only",
            }),
        )
        review_request = request_obj.to_dict()

    status = (
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_READY"
        if not blockers
        else "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_candidate_evaluation_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "candidate_set_digest": candidate_set_digest,
        "candidate_count": candidate_count if isinstance(candidate_count, int) else 0,
        "evaluation_set_digest": evaluation_set_digest,
        "evaluation_count": evaluation_count if isinstance(evaluation_count, int) else 0,
        "review_scope": normalized_scope,
        "review_criteria_digest": normalized_criteria_digest,
        "subsequent_cycle_candidate_review_request": review_request,
        "blockers": blockers,
        "boundary": dict(SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_BOUNDARY),
    }
    return SubsequentCycleCandidateReviewRequest(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "usage: kuuos_planos_subsequent_cycle_candidate_review_request_v0_68.py "
            "CANDIDATE_EVALUATION_RECEIPT.json REVIEW_SCOPE REVIEW_CRITERIA_DIGEST",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    request = build_subsequent_cycle_candidate_review_request(
        candidate_evaluation_receipt=source,
        review_scope=argv[2],
        review_criteria_digest=argv[3],
    )
    print(json.dumps(request.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if request.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
