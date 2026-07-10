from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import sys
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67"
SOURCE_VERSION = "kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66"
MIN_COMPONENT_SCORE = 0
MAX_COMPONENT_SCORE = 100

SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_BOUNDARY = {
    "receipt_owned_by_plan_os": True,
    "source_candidate_set_materialization_receipt_preserved": True,
    "selected_candidate_provenance_preserved": True,
    "candidate_set_digest_preserved": True,
    "candidate_set_nonempty_preserved": True,
    "candidate_ids_unique_preserved": True,
    "memory_overwrite_preserved": True,
    "truth_authority_preserved": True,
    "blocker_release_preserved": True,
    "next_cycle_cycle_closed": True,
    "subsequent_cycle_replan_requested": True,
    "subsequent_cycle_candidate_generation_started": True,
    "subsequent_cycle_candidate_set_materialized": True,
    "subsequent_cycle_candidate_evaluation_receipt_only": True,
    "subsequent_cycle_all_materialized_candidates_evaluated": True,
    "subsequent_cycle_candidate_evaluation_count_exact": True,
    "subsequent_cycle_candidate_evaluation_score_bounds_valid": True,
    "subsequent_cycle_candidate_evaluations_recorded": True,
    "subsequent_cycle_evaluation_order_is_not_selection": True,
    "subsequent_cycle_candidate_review_requested": False,
    "subsequent_cycle_candidate_selected": False,
    "subsequent_cycle_admission_requested": False,
}

REQUIRED_SOURCE_BOUNDARY_TRUE = (
    "receipt_owned_by_plan_os",
    "source_candidate_generation_start_receipt_preserved",
    "selected_candidate_provenance_bound_to_generation_start",
    "memory_overwrite_preserved",
    "memory_overwrite_closeout_preserved",
    "cycle_closed_preserved",
    "truth_authority_authorization_grant_preserved",
    "truth_authority_preserved",
    "truth_authority_cycle_closed_preserved",
    "blocker_release_authorization_request_preserved",
    "blocker_release_authorization_grant_preserved",
    "blocker_release_preserved",
    "blocker_release_cycle_closed_preserved",
    "next_cycle_admission_request_preserved",
    "next_cycle_admission_grant_preserved",
    "next_cycle_start_receipt_preserved",
    "next_cycle_closeout_receipt_preserved",
    "subsequent_cycle_replan_request_preserved",
    "candidate_generation_start_receipt_preserved",
    "next_cycle_cycle_closed",
    "subsequent_cycle_replan_requested",
    "subsequent_cycle_candidate_generation_started",
    "subsequent_cycle_candidate_set_materialization_receipt_only",
    "subsequent_cycle_candidate_set_materialized",
    "subsequent_cycle_candidate_set_nonempty",
    "subsequent_cycle_candidate_ids_unique",
)

REQUIRED_SOURCE_BOUNDARY_FALSE = (
    "subsequent_cycle_candidate_selected",
    "subsequent_cycle_admission_requested",
)


@dataclass(frozen=True)
class CandidateEvaluation:
    candidate_id: str
    candidate_digest: str
    continuity_score: int
    constraint_score: int
    reversibility_score: int
    uncertainty_penalty: int
    total_score: int
    rationale_digest: str
    evaluation_ordinal: int
    evaluation_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateEvaluationRecord:
    selected_candidate_id: str
    selected_candidate_digest: str
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
    evaluation_receipt_digest: str
    evaluation_scope: str = "subsequent_cycle_candidate_evaluation_receipt_only"
    memory_overwrite_preserved: bool = True
    truth_authority_preserved: bool = True
    blocker_release_preserved: bool = True
    next_cycle_cycle_closed: bool = True
    subsequent_cycle_replan_requested: bool = True
    subsequent_cycle_candidate_generation_started: bool = True
    subsequent_cycle_candidate_set_materialized: bool = True
    subsequent_cycle_all_materialized_candidates_evaluated: bool = True
    subsequent_cycle_candidate_evaluations_recorded: bool = True
    subsequent_cycle_candidate_review_requested: bool = False
    subsequent_cycle_candidate_selected: bool = False
    subsequent_cycle_admission_requested: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubsequentCycleCandidateEvaluationReceipt:
    version: str
    source_version: str
    status: str
    source_candidate_set_materialization_receipt_digest: str
    selected_candidate_id: str
    selected_candidate_digest: str
    candidate_set_digest: str
    candidate_count: int
    evaluations: list[dict[str, Any]]
    evaluation_set_digest: str
    evaluation_count: int
    subsequent_cycle_candidate_evaluation_receipt: dict[str, Any] | None
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _source_materialization_record(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    return _m(receipt.get("subsequent_cycle_candidate_set_materialization_receipt"))


def _is_int_score(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _source_blockers(receipt: Mapping[str, Any]) -> list[str]:
    blockers: list[str] = []
    if receipt.get("version") != SOURCE_VERSION:
        blockers.append("source_candidate_set_materialization_receipt_version_invalid")
    if receipt.get("status") != "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SET_MATERIALIZATION_RECEIPT_READY":
        blockers.append("source_candidate_set_materialization_receipt_not_ready")
    boundary = _m(receipt.get("boundary"))
    for field in REQUIRED_SOURCE_BOUNDARY_TRUE:
        if boundary.get(field) is not True:
            blockers.append(f"source_boundary_{field}_missing")
    for field in REQUIRED_SOURCE_BOUNDARY_FALSE:
        if boundary.get(field) is not False:
            blockers.append(f"source_boundary_{field}_promoted")
    if not receipt.get("receipt_digest"):
        blockers.append("source_candidate_set_materialization_receipt_digest_missing")

    candidate_set = receipt.get("candidate_set")
    if not isinstance(candidate_set, list) or not candidate_set:
        blockers.append("source_candidate_set_missing_or_empty")
        candidate_set = []
    candidate_count = receipt.get("candidate_count")
    if candidate_count != len(candidate_set):
        blockers.append("source_candidate_count_mismatch")
    candidate_set_digest = str(receipt.get("candidate_set_digest", ""))
    if not candidate_set_digest:
        blockers.append("source_candidate_set_digest_missing")
    elif candidate_set and sha(candidate_set) != candidate_set_digest:
        blockers.append("source_candidate_set_digest_invalid")

    candidate_ids: list[str] = []
    candidate_digests: list[str] = []
    for ordinal, raw_candidate in enumerate(candidate_set):
        candidate = _m(raw_candidate)
        candidate_id = str(candidate.get("candidate_id", ""))
        candidate_digest = str(candidate.get("candidate_digest", ""))
        if not candidate_id:
            blockers.append(f"source_candidate_{ordinal}_id_missing")
        if not candidate_digest:
            blockers.append(f"source_candidate_{ordinal}_digest_missing")
        if candidate_id:
            candidate_ids.append(candidate_id)
        if candidate_digest:
            candidate_digests.append(candidate_digest)
    if len(candidate_ids) != len(set(candidate_ids)):
        blockers.append("source_candidate_ids_not_unique")
    if len(candidate_digests) != len(set(candidate_digests)):
        blockers.append("source_candidate_digests_not_unique")

    record = _source_materialization_record(receipt)
    if not record:
        blockers.append("source_candidate_set_materialization_record_missing")
    else:
        if record.get("candidate_count") != len(candidate_set):
            blockers.append("source_record_candidate_count_mismatch")
        if str(record.get("candidate_set_digest", "")) != candidate_set_digest:
            blockers.append("source_record_candidate_set_digest_mismatch")
        if record.get("subsequent_cycle_candidate_set_materialized") is not True:
            blockers.append("source_record_candidate_set_materialized_missing")
        if record.get("subsequent_cycle_candidate_selected") is not False:
            blockers.append("source_record_candidate_selected_promoted")
        if record.get("subsequent_cycle_admission_requested") is not False:
            blockers.append("source_record_admission_requested_promoted")
    return blockers


def _build_evaluations(
    *,
    candidate_set: Sequence[Mapping[str, Any]],
    evaluation_specs: Sequence[Mapping[str, Any]],
) -> tuple[list[CandidateEvaluation], list[str]]:
    blockers: list[str] = []
    spec_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_spec in enumerate(evaluation_specs):
        spec = _m(raw_spec)
        candidate_id = str(spec.get("candidate_id", "")).strip()
        if not candidate_id:
            blockers.append(f"evaluation_spec_{index}_candidate_id_missing")
            continue
        if candidate_id in spec_by_id:
            blockers.append("evaluation_candidate_ids_not_unique")
        else:
            spec_by_id[candidate_id] = spec

    source_ids = [str(_m(candidate).get("candidate_id", "")) for candidate in candidate_set]
    source_id_set = set(source_ids)
    extra_ids = sorted(set(spec_by_id) - source_id_set)
    missing_ids = sorted(source_id_set - set(spec_by_id))
    if extra_ids:
        blockers.append("evaluation_contains_unknown_candidate")
    if missing_ids:
        blockers.append("evaluation_missing_materialized_candidate")
    if len(evaluation_specs) != len(candidate_set):
        blockers.append("evaluation_count_does_not_match_candidate_count")

    evaluations: list[CandidateEvaluation] = []
    for ordinal, raw_candidate in enumerate(candidate_set):
        candidate = _m(raw_candidate)
        candidate_id = str(candidate.get("candidate_id", ""))
        candidate_digest = str(candidate.get("candidate_digest", ""))
        spec = spec_by_id.get(candidate_id)
        if spec is None:
            continue
        values: dict[str, int] = {}
        for field in (
            "continuity_score",
            "constraint_score",
            "reversibility_score",
            "uncertainty_penalty",
        ):
            value = spec.get(field)
            if not _is_int_score(value):
                blockers.append(f"evaluation_{candidate_id}_{field}_not_integer")
                continue
            if value < MIN_COMPONENT_SCORE or value > MAX_COMPONENT_SCORE:
                blockers.append(f"evaluation_{candidate_id}_{field}_out_of_bounds")
                continue
            values[field] = value
        rationale_digest = str(spec.get("rationale_digest", "")).strip()
        if not rationale_digest:
            blockers.append(f"evaluation_{candidate_id}_rationale_digest_missing")
        if len(values) != 4 or not rationale_digest:
            continue
        total_score = (
            values["continuity_score"]
            + values["constraint_score"]
            + values["reversibility_score"]
            - values["uncertainty_penalty"]
        )
        evaluation_digest = sha({
            "candidate_id": candidate_id,
            "candidate_digest": candidate_digest,
            "continuity_score": values["continuity_score"],
            "constraint_score": values["constraint_score"],
            "reversibility_score": values["reversibility_score"],
            "uncertainty_penalty": values["uncertainty_penalty"],
            "total_score": total_score,
            "rationale_digest": rationale_digest,
            "evaluation_ordinal": ordinal,
        })
        evaluations.append(
            CandidateEvaluation(
                candidate_id=candidate_id,
                candidate_digest=candidate_digest,
                continuity_score=values["continuity_score"],
                constraint_score=values["constraint_score"],
                reversibility_score=values["reversibility_score"],
                uncertainty_penalty=values["uncertainty_penalty"],
                total_score=total_score,
                rationale_digest=rationale_digest,
                evaluation_ordinal=ordinal,
                evaluation_digest=evaluation_digest,
            )
        )
    return evaluations, blockers


def build_subsequent_cycle_candidate_evaluation_receipt(
    *,
    candidate_set_materialization_receipt: Mapping[str, Any],
    evaluation_specs: Sequence[Mapping[str, Any]],
) -> SubsequentCycleCandidateEvaluationReceipt:
    source = _m(candidate_set_materialization_receipt)
    blockers = _source_blockers(source)
    candidate_set_raw = source.get("candidate_set")
    candidate_set = candidate_set_raw if isinstance(candidate_set_raw, list) else []
    evaluations_obj, evaluation_blockers = _build_evaluations(
        candidate_set=candidate_set,
        evaluation_specs=evaluation_specs,
    )
    blockers.extend(evaluation_blockers)
    evaluations = [evaluation.to_dict() for evaluation in evaluations_obj]
    if len(evaluations) != len(candidate_set):
        blockers.append("materialized_candidate_evaluation_coverage_incomplete")
    evaluation_set_digest = sha(evaluations) if evaluations else ""

    selected_id = str(source.get("selected_candidate_id", ""))
    selected_digest = str(source.get("selected_candidate_digest", ""))
    candidate_set_digest = str(source.get("candidate_set_digest", ""))
    source_record = _source_materialization_record(source)
    evaluation_record = None
    if candidate_set and evaluations and not blockers:
        record_obj = SubsequentCycleCandidateEvaluationRecord(
            selected_candidate_id=selected_id,
            selected_candidate_digest=selected_digest,
            source_candidate_set_materialization_receipt_digest=str(source.get("receipt_digest", "")),
            source_candidate_generation_start_receipt_digest=str(source_record.get("source_candidate_generation_start_receipt_digest", "")),
            source_subsequent_cycle_replan_request_digest=str(source_record.get("source_subsequent_cycle_replan_request_digest", "")),
            source_next_cycle_closeout_receipt_digest=str(source_record.get("source_next_cycle_closeout_receipt_digest", "")),
            source_blocker_release_authorization_request_digest=str(source_record.get("source_blocker_release_authorization_request_digest", "")),
            source_truth_authority_closeout_receipt_digest=str(source_record.get("source_truth_authority_closeout_receipt_digest", "")),
            source_memory_overwrite_closeout_receipt_digest=str(source_record.get("source_memory_overwrite_closeout_receipt_digest", "")),
            candidate_set_digest=candidate_set_digest,
            candidate_count=len(candidate_set),
            evaluation_set_digest=evaluation_set_digest,
            evaluation_count=len(evaluations),
            evaluation_receipt_digest=sha({
                "source_candidate_set_materialization_receipt_digest": source.get("receipt_digest"),
                "candidate_set_digest": candidate_set_digest,
                "candidate_count": len(candidate_set),
                "evaluation_set_digest": evaluation_set_digest,
                "evaluation_count": len(evaluations),
                "scope": "subsequent_cycle_candidate_evaluation_receipt_only",
            }),
        )
        evaluation_record = record_obj.to_dict()

    status = (
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY"
        if not blockers
        else "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_BLOCKED"
    )
    partial = {
        "version": VERSION,
        "source_version": SOURCE_VERSION,
        "status": status,
        "source_candidate_set_materialization_receipt_digest": str(source.get("receipt_digest", "")),
        "selected_candidate_id": selected_id,
        "selected_candidate_digest": selected_digest,
        "candidate_set_digest": candidate_set_digest,
        "candidate_count": len(candidate_set),
        "evaluations": evaluations,
        "evaluation_set_digest": evaluation_set_digest,
        "evaluation_count": len(evaluations),
        "subsequent_cycle_candidate_evaluation_receipt": evaluation_record,
        "blockers": blockers,
        "boundary": dict(SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_BOUNDARY),
    }
    return SubsequentCycleCandidateEvaluationReceipt(receipt_digest=sha(partial), **partial)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "usage: kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67.py "
            "CANDIDATE_SET_MATERIALIZATION_RECEIPT.json EVALUATION_SPECS.json",
            file=sys.stderr,
        )
        return 2
    with open(argv[1], "r", encoding="utf-8") as handle:
        source = json.load(handle)
    with open(argv[2], "r", encoding="utf-8") as handle:
        evaluation_specs = json.load(handle)
    if not isinstance(evaluation_specs, list):
        print("evaluation specs must be a JSON array", file=sys.stderr)
        return 2
    receipt = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=evaluation_specs,
    )
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.status.endswith("READY") else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
