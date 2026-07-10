from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_review_request_v0_68"
EVALUATION_SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67"
ALLOWED_REVIEW_DISPOSITIONS = (
    "eligible",
    "eligible_with_conditions",
    "deferred",
    "rejected",
)
SELECTION_ELIGIBLE_DISPOSITIONS = (
    "eligible",
    "eligible_with_conditions",
)

SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_candidate_review_request_preserved": True,
    "source_candidate_evaluation_receipt_preserved": True,
    "selected_candidate_provenance_preserved": True,
    "candidate_set_digest_preserved": True,
    "evaluation_set_digest_preserved": True,
    "evaluation_count_exact_preserved": True,
    "review_scope_preserved": True,
    "review_criteria_digest_preserved": True,
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
    "subsequent_cycle_candidate_review_requested": True,
    "subsequent_cycle_candidate_review_receipt_only": True,
    "subsequent_cycle_all_evaluated_candidates_reviewed": True,
    "subsequent_cycle_candidate_review_count_exact": True,
    "subsequent_cycle_candidate_review_outcomes_recorded": True,
    "subsequent_cycle_candidate_review_completed": True,
    "subsequent_cycle_review_order_is_not_selection": True,
    "subsequent_cycle_selection_eligibility_recorded": True,
    "subsequent_cycle_selection_authority_granted": False,
    "subsequent_cycle_candidate_selection_requested": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

REQUIRED_REQUEST_BOUNDARY_TRUE = (
    "request_owned_by_plan_os",
    "source_candidate_evaluation_receipt_preserved",
    "selected_candidate_provenance_preserved",
    "candidate_set_digest_preserved",
    "evaluation_set_digest_preserved",
    "evaluation_count_exact_preserved",
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
    "subsequent_cycle_candidate_review_request_only",
    "subsequent_cycle_candidate_review_requested",
    "subsequent_cycle_review_scope_bound",
    "subsequent_cycle_review_criteria_digest_bound",
)

REQUIRED_REQUEST_BOUNDARY_FALSE = (
    "subsequent_cycle_selection_authority_granted",
    "subsequent_cycle_candidate_review_completed",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)

REQUIRED_EVALUATION_BOUNDARY_TRUE = (
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

REQUIRED_EVALUATION_BOUNDARY_FALSE = (
    "subsequent_cycle_candidate_review_requested",
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class CandidateReviewOutcome:
    candidate_id: str
    candidate_digest: str
    evaluation_digest: str
    total_score: int
    review_disposition: str
    selection_eligible: bool
    review_rationale_digest: str
    review_constraints_digest: str
    review_ordinal: int
    review_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateReviewRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
    source_candidate_review_request_digest: str
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
    review_set_digest: str
    review_count: int
    selection_eligible_count: int
    review_receipt_digest: str
    receipt_scope: str = "subsequent_cycle_candidate_review_receipt_only"
    memory_overwrite_preserved: bool = True
    truth_authority_preserved: bool = True
    blocker_release_preserved: bool = True
    next_cycle_cycle_closed: bool = True
    subsequent_cycle_replan_requested: bool = True
    subsequent_cycle_candidate_generation_started: bool = True
    subsequent_cycle_candidate_set_materialized: bool = True
    subsequent_cycle_candidate_evaluations_recorded: bool = True
    subsequent_cycle_candidate_review_requested: bool = True
    subsequent_cycle_all_evaluated_candidates_reviewed: bool = True
    subsequent_cycle_candidate_review_completed: bool = True
    subsequent_cycle_review_order_is_not_selection: bool = True
    subsequent_cycle_selection_eligibility_recorded: bool = True
    subsequent_cycle_selection_authority_granted: bool = False
    subsequent_cycle_candidate_selection_requested: bool = False
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateReviewReceipt:
    version: str
    source_version: str
    evaluation_source_version: str
    status: str
    source_candidate_review_request_digest: str
    source_candidate_evaluation_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    candidate_count: int
    evaluation_set_digest: str
    evaluation_count: int
    review_scope: str
    review_criteria_digest: str
    review_outcomes: list[dict[str, Any]]
    review_set_digest: str
    review_count: int
    selection_eligible_count: int
    subsequent_cycle_candidate_review_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _request_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("subsequent_cycle_candidate_review_request"))


def _evaluation_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("subsequent_cycle_candidate_evaluation_receipt"))


def _request_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_review_request_version_invalid")
    if receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_READY":
        blockers.append("source_candidate_review_request_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_REQUEST_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_request_boundary_{field}_missing")
    for field in REQUIRED_REQUEST_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_request_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_candidate_review_request_digest_missing")

    candidate_count = receipt.get("candidate_count")
    evaluation_count = receipt.get("evaluation_count")
    if not isinstance(candidate_count, int) or isinstance(candidate_count, bool) or candidate_count <= 0:
        blockers.append("source_request_candidate_count_invalid")
    if not isinstance(evaluation_count, int) or isinstance(evaluation_count, bool) or evaluation_count <= 0:
        blockers.append("source_request_evaluation_count_invalid")
    if candidate_count != evaluation_count:
        blockers.append("source_request_evaluation_count_not_exact")
    if not receipt.get("candidate_set_digest"):
        blockers.append("source_request_candidate_set_digest_missing")
    if not receipt.get("evaluation_set_digest"):
        blockers.append("source_request_evaluation_set_digest_missing")
    if not receipt.get("review_scope"):
        blockers.append("source_request_review_scope_missing")
    if not receipt.get("review_criteria_digest"):
        blockers.append("source_request_review_criteria_digest_missing")

    record = _request_record(receipt)
    if not record:
        blockers.append("source_candidate_review_request_record_missing")
    else:
        for field in (
            "selected_candidate_id",
            "selected_candidate_digest",
            "source_candidate_evaluation_receipt_digest",
            "candidate_set_digest",
            "candidate_count",
            "evaluation_set_digest",
            "evaluation_count",
            "review_scope",
            "review_criteria_digest",
        ):
            if record.get(field) != receipt.get(field):
                blockers.append(f"source_request_record_{field}_mismatch")
        if not record.get("review_request_digest"):
            blockers.append("source_request_record_review_request_digest_missing")
        if record.get("subsequent_cycle_candidate_review_requested") is not True:
            blockers.append("source_request_record_review_requested_missing")
        for field in (
            "subsequent_cycle_selection_authority_granted",
            "subsequent_cycle_candidate_review_completed",
            "subsequent_cycle_candidate_selected",
            "subsequent_cycle_admission_requested",
        ):
            if record.get(field) is not False:
                blockers.append(f"source_request_record_{field}_promoted")
    return blockers


def _evaluation_blockers(
    receipt: Mapping[str, Any],
    request: Mapping[str, Any],
) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != EVALUATION_SOURCE_VERSION:
        blockers.append("candidate_evaluation_receipt_version_invalid")
    if receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY":
        blockers.append("candidate_evaluation_receipt_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_EVALUATION_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"evaluation_boundary_{field}_missing")
    for field in REQUIRED_EVALUATION_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"evaluation_boundary_{field}_promoted")

    request_source_digest = str(request.get("source_candidate_evaluation_receipt_digest", ""))
    if str(receipt.get("receipt_digest", "")) != request_source_digest:
        blockers.append("candidate_evaluation_receipt_digest_request_mismatch")
    for field in (
        "selected_candidate_id",
        "selected_candidate_digest",
        "candidate_set_digest",
        "candidate_count",
        "evaluation_set_digest",
        "evaluation_count",
    ):
        if receipt.get(field) != request.get(field):
            blockers.append(f"candidate_evaluation_{field}_request_mismatch")

    evaluations = receipt.get("evaluations")
    if not isinstance(evaluations, list) or not evaluations:
        blockers.append("candidate_evaluations_missing_or_empty")
        evaluations = []
    if receipt.get("evaluation_count") != len(evaluations):
        blockers.append("candidate_evaluation_list_count_mismatch")
    evaluation_set_digest = str(receipt.get("evaluation_set_digest", ""))
    if evaluations and sha(evaluations) != evaluation_set_digest:
        blockers.append("candidate_evaluation_set_digest_invalid")

    candidate_ids: list[str] = []
    candidate_digests: list[str] = []
    evaluation_digests: list[str] = []
    for ordinal, raw_evaluation in enumerate(evaluations):
        evaluation = _m(raw_evaluation)
        candidate_id = str(evaluation.get("candidate_id", ""))
        candidate_digest = str(evaluation.get("candidate_digest", ""))
        evaluation_digest = str(evaluation.get("evaluation_digest", ""))
        if not candidate_id:
            blockers.append(f"candidate_evaluation_{ordinal}_candidate_id_missing")
        if not candidate_digest:
            blockers.append(f"candidate_evaluation_{ordinal}_candidate_digest_missing")
        if not evaluation_digest:
            blockers.append(f"candidate_evaluation_{ordinal}_evaluation_digest_missing")
        if evaluation.get("evaluation_ordinal") != ordinal:
            blockers.append(f"candidate_evaluation_{ordinal}_ordinal_mismatch")
        if candidate_id:
            candidate_ids.append(candidate_id)
        if candidate_digest:
            candidate_digests.append(candidate_digest)
        if evaluation_digest:
            evaluation_digests.append(evaluation_digest)
    if len(candidate_ids) != len(set(candidate_ids)):
        blockers.append("candidate_evaluation_candidate_ids_not_unique")
    if len(candidate_digests) != len(set(candidate_digests)):
        blockers.append("candidate_evaluation_candidate_digests_not_unique")
    if len(evaluation_digests) != len(set(evaluation_digests)):
        blockers.append("candidate_evaluation_digests_not_unique")

    record = _evaluation_record(receipt)
    if not record:
        blockers.append("candidate_evaluation_record_missing")
    else:
        for field in (
            "selected_candidate_id",
            "selected_candidate_digest",
            "candidate_set_digest",
            "candidate_count",
            "evaluation_set_digest",
            "evaluation_count",
        ):
            if record.get(field) != receipt.get(field):
                blockers.append(f"candidate_evaluation_record_{field}_mismatch")
        if record.get("subsequent_cycle_all_materialized_candidates_evaluated") is not True:
            blockers.append("candidate_evaluation_record_coverage_missing")
        if record.get("subsequent_cycle_candidate_evaluations_recorded") is not True:
            blockers.append("candidate_evaluation_record_evaluations_missing")
    return blockers


def _build_review_outcomes(
    *,
    evaluations: Sequence[Mapping[str, Any]],
    review_specs: Sequence[Mapping[str, Any]],
) -> tuple[list[CandidateReviewOutcome], list[str]]:
    blockers: list[str] = []
    specs_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_spec in enumerate(review_specs):
        spec = _m(raw_spec)
        candidate_id = str(spec.get("candidate_id", "")).strip()
        if not candidate_id:
            blockers.append(f"review_spec_{index}_candidate_id_missing")
            continue
        if candidate_id in specs_by_id:
            blockers.append("review_candidate_ids_not_unique")
        else:
            specs_by_id[candidate_id] = spec

    evaluation_ids = [str(_m(evaluation).get("candidate_id", "")) for evaluation in evaluations]
    evaluation_id_set = set(evaluation_ids)
    if set(specs_by_id) - evaluation_id_set:
        blockers.append("review_contains_unknown_candidate")
    if evaluation_id_set - set(specs_by_id):
        blockers.append("review_missing_evaluated_candidate")
    if len(review_specs) != len(evaluations):
        blockers.append("review_count_does_not_match_evaluation_count")

    outcomes: list[CandidateReviewOutcome] = []
    for ordinal, raw_evaluation in enumerate(evaluations):
        evaluation = _m(raw_evaluation)
        candidate_id = str(evaluation.get("candidate_id", ""))
        spec = specs_by_id.get(candidate_id)
        if spec is None:
            continue
        disposition = str(spec.get("review_disposition", "")).strip()
        if disposition not in ALLOWED_REVIEW_DISPOSITIONS:
            blockers.append(f"review_{candidate_id}_disposition_invalid")
        rationale_digest = str(spec.get("review_rationale_digest", "")).strip()
        constraints_digest = str(spec.get("review_constraints_digest", "")).strip()
        if not rationale_digest:
            blockers.append(f"review_{candidate_id}_rationale_digest_missing")
        if not constraints_digest:
            blockers.append(f"review_{candidate_id}_constraints_digest_missing")
        if (
            disposition not in ALLOWED_REVIEW_DISPOSITIONS
            or not rationale_digest
            or not constraints_digest
        ):
            continue
        selection_eligible = disposition in SELECTION_ELIGIBLE_DISPOSITIONS
        candidate_digest = str(evaluation.get("candidate_digest", ""))
        evaluation_digest = str(evaluation.get("evaluation_digest", ""))
        total_score = evaluation.get("total_score")
        if not isinstance(total_score, int) or isinstance(total_score, bool):
            blockers.append(f"review_{candidate_id}_source_total_score_invalid")
            continue
        review_digest = sha({
            "candidate_id": candidate_id,
            "candidate_digest": candidate_digest,
            "evaluation_digest": evaluation_digest,
            "total_score": total_score,
            "review_disposition": disposition,
            "selection_eligible": selection_eligible,
            "review_rationale_digest": rationale_digest,
            "review_constraints_digest": constraints_digest,
            "review_ordinal": ordinal,
        })
        outcomes.append(
            CandidateReviewOutcome(
                candidate_id=candidate_id,
                candidate_digest=candidate_digest,
                evaluation_digest=evaluation_digest,
                total_score=total_score,
                review_disposition=disposition,
                selection_eligible=selection_eligible,
                review_rationale_digest=rationale_digest,
                review_constraints_digest=constraints_digest,
                review_ordinal=ordinal,
                review_digest=review_digest,
            )
        )
    return outcomes, blockers


def build_subsequent_cycle_candidate_review_receipt(
    *,
    candidate_review_request: Mapping[str, Any],
    candidate_evaluation_receipt: Mapping[str, Any],
    review_specs: Sequence[Mapping[str, Any]],
) -> SubsequentCycleCandidateReviewReceipt:
    request = _m(candidate_review_request)
    evaluation = _m(candidate_evaluation_receipt)
    blockers = _request_blockers(request)
    blockers.extend(_evaluation_blockers(evaluation, request))

    evaluations_raw = evaluation.get("evaluations")
    evaluations = evaluations_raw if isinstance(evaluations_raw, list) else []
    outcomes_obj, outcome_blockers = _build_review_outcomes(
        evaluations=evaluations,
        review_specs=review_specs,
    )
    blockers.extend(outcome_blockers)
    outcomes = [outcome.to_dict() for outcome in outcomes_obj]
    if len(outcomes) != len(evaluations):
        blockers.append("evaluated_candidate_review_coverage_incomplete")
    review_set_digest = sha(outcomes) if outcomes else ""
    selection_eligible_count = sum(
        1 for outcome in outcomes if outcome.get("selection_eligible") is True
    )

    selected_id = str(request.get("selected_candidate_id", ""))
    selected_digest = str(request.get("selected_candidate_digest", ""))
    candidate_set_digest = str(request.get("candidate_set_digest", ""))
    evaluation_set_digest = str(request.get("evaluation_set_digest", ""))
    candidate_count = request.get("candidate_count")
    evaluation_count = request.get("evaluation_count")
    review_scope = str(request.get("review_scope", ""))
    review_criteria_digest = str(request.get("review_criteria_digest", ""))
    request_record = _request_record(request)

    review_record = None
    if evaluations and outcomes and not blockers:
        record_obj = SubsequentCycleCandidateReviewRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_candidate_review_request_digest=str(request.get("receipt_digest", "")),
            source_candidate_evaluation_receipt_digest=str(evaluation.get("receipt_digest", "")),
            source_candidate_set_materialization_receipt_digest=str(request_record.get("source_candidate_set_materialization_receipt_digest", "")),
            source_candidate_generation_start_receipt_digest=str(request_record.get("source_candidate_generation_start_receipt_digest", "")),
            source_subsequent_cycle_replan_request_digest=str(request_record.get("source_subsequent_cycle_replan_request_digest", "")),
            source_next_cycle_closeout_receipt_digest=str(request_record.get("source_next_cycle_closeout_receipt_digest", "")),
            source_blocker_release_authorization_request_digest=str(request_record.get("source_blocker_release_authorization_request_digest", "")),
            source_truth_authority_closeout_receipt_digest=str(request_record.get("source_truth_authority_closeout_receipt_digest", "")),
            source_memory_overwrite_closeout_receipt_digest=str(request_record.get("source_memory_overwrite_closeout_receipt_digest", "")),
            candidate_set_digest=candidate_set_digest,
            candidate_count=int(candidate_count),
            evaluation_set_digest=evaluation_set_digest,
            evaluation_count=int(evaluation_count),
            review_scope=review_scope,
            review_criteria_digest=review_criteria_digest,
            review_set_digest=review_set_digest,
            review_count=len(outcomes),
            selection_eligible_count=selection_eligible_count,
            review_receipt_digest=sha({
                "source_candidate_review_request_digest": request.get("receipt_digest"),
                "source_candidate_evaluation_receipt_digest": evaluation.get("receipt_digest"),
                "candidate_set_digest": candidate_set_digest,
                "candidate_count": candidate_count,
                "evaluation_set_digest": evaluation_set_digest,
                "evaluation_count": evaluation_count,
                "review_scope": review_scope,
                "review_criteria_digest": review_criteria_digest,
                "review_set_digest": review_set_digest,
                "review_count": len(outcomes),
                "selection_eligible_count": selection_eligible_count,
                "scope": "subsequent_cycle_candidate_review_receipt_only",
            }),
        )
        review_record = record_obj.to_dict()

    status = (
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_READY"
        if not blockers
        else "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "evaluation_source_version": EVALUATION_SOURCE_VERSION,
        "status": status,
        "source_candidate_review_request_digest": str(request.get("receipt_digest", "")),
        "source_candidate_evaluation_receipt_digest": str(evaluation.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "candidate_set_digest": candidate_set_digest,
        "candidate_count": candidate_count if isinstance(candidate_count, int) else 0,
        "evaluation_set_digest": evaluation_set_digest,
        "evaluation_count": evaluation_count if isinstance(evaluation_count, int) else 0,
        "review_scope": review_scope,
        "review_criteria_digest": review_criteria_digest,
        "review_outcomes": outcomes,
        "review_set_digest": review_set_digest,
        "review_count": len(outcomes),
        "selection_eligible_count": selection_eligible_count,
        "subsequent_cycle_candidate_review_receipt": review_record,
        "blockers": blockers,
        "boundary": dict(SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_BOUNDARY),
    }
    return SubsequentCycleCandidateReviewReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(
            "usage: kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69.py "
            "CANDIDATE_REVIEW_REQUEST.json CANDIDATE_EVALUATION_RECEIPT.json REVIEW_SPECS.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        review_request = json.load(handle)
    with open(argv[2], "r", encoding="utf-8") as handle:
        evaluation_receipt = json.load(handle)
    with open(argv[3], "r", encoding="utf-8") as handle:
        review_specs = json.load(handle)
    if not isinstance(review_specs, list):
        print("review specs must be a JSON array", file=sys.stderr)
        return 2
    receipt = build_subsequent_cycle_candidate_review_receipt(
        candidate_review_request=review_request,
        candidate_evaluation_receipt=evaluation_receipt,
        review_specs=review_specs,
    )
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
