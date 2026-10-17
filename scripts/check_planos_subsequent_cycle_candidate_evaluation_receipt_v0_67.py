#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66 import (
    _candidate_specs,
    _ready_candidate_generation_start_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_set_materialization_receipt_v0_66 import (
    build_subsequent_cycle_candidate_set_materialization_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67 import (
    MAX_COMPONENT_SCORE,
    MIN_COMPONENT_SCORE,
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_evaluation_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_candidate_set_materialization_receipt() -> dict:
    source = _ready_candidate_generation_start_receipt()
    return build_subsequent_cycle_candidate_set_materialization_receipt(
        candidate_generation_start_receipt=source,
        candidate_specs=_candidate_specs(),
    ).to_dict()


def _evaluation_specs() -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "repair-route::continuity",
            "continuity_score": 90,
            "constraint_score": 88,
            "reversibility_score": 94,
            "uncertainty_penalty": 10,
            "rationale_digest": "rationale-continuity-v1",
        },
        {
            "candidate_id": "repair-route::refinement",
            "continuity_score": 82,
            "constraint_score": 95,
            "reversibility_score": 85,
            "uncertainty_penalty": 15,
            "rationale_digest": "rationale-refinement-v1",
        },
        {
            "candidate_id": "repair-route::recovery",
            "continuity_score": 76,
            "constraint_score": 90,
            "reversibility_score": 98,
            "uncertainty_penalty": 20,
            "rationale_digest": "rationale-recovery-v1",
        },
    ]


def _exercise_runtime() -> None:
    source = _ready_candidate_set_materialization_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    specs = _evaluation_specs()
    receipt = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=specs,
    ).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY",
        f"candidate evaluation blocked: {receipt.get('blockers')}",
    )
    require(receipt["candidate_count"] == 3, "candidate count mismatch")
    require(receipt["evaluation_count"] == receipt["candidate_count"], "evaluation count mismatch")
    require(receipt["candidate_set_digest"] == source["candidate_set_digest"], "candidate-set digest changed")
    require(receipt["evaluation_set_digest"], "evaluation-set digest missing")
    require(len(receipt["evaluations"]) == 3, "evaluation list length mismatch")

    expected_totals = {
        "repair-route::continuity": 262,
        "repair-route::refinement": 247,
        "repair-route::recovery": 244,
    }
    source_by_id = {candidate["candidate_id"]: candidate for candidate in source["candidate_set"]}
    for ordinal, evaluation in enumerate(receipt["evaluations"]):
        candidate_id = evaluation["candidate_id"]
        require(evaluation["evaluation_ordinal"] == ordinal, "evaluation ordinal mismatch")
        require(evaluation["candidate_digest"] == source_by_id[candidate_id]["candidate_digest"], "candidate digest mismatch")
        require(evaluation["total_score"] == expected_totals[candidate_id], "total score mismatch")
        require(evaluation["evaluation_digest"], "evaluation digest missing")
        for field in (
            "continuity_score",
            "constraint_score",
            "reversibility_score",
            "uncertainty_penalty",
        ):
            require(MIN_COMPONENT_SCORE <= evaluation[field] <= MAX_COMPONENT_SCORE, f"score out of bounds: {field}")

    boundary = receipt["boundary"]
    for field in (
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
    ):
        require(boundary[field] is True, f"required boundary missing: {field}")
    for field in (
        "subsequent_cycle_candidate_review_requested",
        "subsequent_cycle_candidate_selected",
        "subsequent_cycle_admission_requested",
    ):
        require(boundary[field] is False, f"closed boundary promoted: {field}")

    record = receipt["subsequent_cycle_candidate_evaluation_receipt"]
    require(record["candidate_count"] == receipt["candidate_count"], "record candidate count mismatch")
    require(record["evaluation_count"] == receipt["evaluation_count"], "record evaluation count mismatch")
    require(record["candidate_set_digest"] == receipt["candidate_set_digest"], "record candidate-set digest mismatch")
    require(record["evaluation_set_digest"] == receipt["evaluation_set_digest"], "record evaluation-set digest mismatch")
    require(record["subsequent_cycle_all_materialized_candidates_evaluated"] is True, "record coverage missing")
    require(record["subsequent_cycle_candidate_review_requested"] is False, "record requested review")
    require(record["subsequent_cycle_candidate_selected"] is False, "record selected candidate")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")
    require(record["source_candidate_generation_start_receipt_digest"], "generation start digest missing")
    require(record["source_subsequent_cycle_replan_request_digest"], "replan digest missing")

    missing_specs = _evaluation_specs()[:-1]
    missing = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=missing_specs,
    ).to_dict()
    require(missing["status"].endswith("BLOCKED"), "missing evaluation not blocked")
    require("evaluation_missing_materialized_candidate" in missing["blockers"], "missing-candidate blocker absent")
    require("materialized_candidate_evaluation_coverage_incomplete" in missing["blockers"], "coverage blocker absent")

    extra_specs = _evaluation_specs() + [
        {
            "candidate_id": "unknown-candidate",
            "continuity_score": 50,
            "constraint_score": 50,
            "reversibility_score": 50,
            "uncertainty_penalty": 50,
            "rationale_digest": "unknown-rationale",
        }
    ]
    extra = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=extra_specs,
    ).to_dict()
    require(extra["status"].endswith("BLOCKED"), "unknown evaluation not blocked")
    require("evaluation_contains_unknown_candidate" in extra["blockers"], "unknown-candidate blocker absent")

    duplicate_specs = _evaluation_specs()
    duplicate_specs[1] = dict(duplicate_specs[1])
    duplicate_specs[1]["candidate_id"] = duplicate_specs[0]["candidate_id"]
    duplicate = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=duplicate_specs,
    ).to_dict()
    require(duplicate["status"].endswith("BLOCKED"), "duplicate evaluation not blocked")
    require("evaluation_candidate_ids_not_unique" in duplicate["blockers"], "duplicate blocker absent")

    out_of_bounds_specs = _evaluation_specs()
    out_of_bounds_specs[0] = dict(out_of_bounds_specs[0])
    out_of_bounds_specs[0]["continuity_score"] = MAX_COMPONENT_SCORE + 1
    out_of_bounds = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=out_of_bounds_specs,
    ).to_dict()
    require(out_of_bounds["status"].endswith("BLOCKED"), "out-of-bounds score not blocked")
    require(
        "evaluation_repair-route::continuity_continuity_score_out_of_bounds" in out_of_bounds["blockers"],
        "score-bound blocker absent",
    )

    noninteger_specs = _evaluation_specs()
    noninteger_specs[0] = dict(noninteger_specs[0])
    noninteger_specs[0]["continuity_score"] = 90.5
    noninteger = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=noninteger_specs,
    ).to_dict()
    require(noninteger["status"].endswith("BLOCKED"), "noninteger score not blocked")
    require(
        "evaluation_repair-route::continuity_continuity_score_not_integer" in noninteger["blockers"],
        "integer blocker absent",
    )

    tampered = dict(source)
    tampered_set = [dict(candidate) for candidate in source["candidate_set"]]
    tampered_set[0]["objective"] = "tampered objective"
    tampered["candidate_set"] = tampered_set
    tampered_receipt = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=tampered,
        evaluation_specs=specs,
    ).to_dict()
    require(tampered_receipt["status"].endswith("BLOCKED"), "tampered candidate set not blocked")
    require("source_candidate_set_digest_invalid" in tampered_receipt["blockers"], "digest blocker absent")

    preselected = dict(source)
    preselected_boundary = dict(preselected["boundary"])
    preselected_boundary["subsequent_cycle_candidate_selected"] = True
    preselected["boundary"] = preselected_boundary
    preselected_receipt = build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=preselected,
        evaluation_specs=specs,
    ).to_dict()
    require(preselected_receipt["status"].endswith("BLOCKED"), "preselected source not blocked")
    require(
        "source_boundary_subsequent_cycle_candidate_selected_promoted" in preselected_receipt["blockers"],
        "preselected boundary blocker absent",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateEvaluationReceiptV0_67.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_67.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_v0_67.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_evaluation_receipt",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_EVALUATION_RECEIPT_READY",
        "CandidateEvaluation",
        "evaluation_set_digest",
        "evaluation_missing_materialized_candidate",
        "evaluation_contains_unknown_candidate",
        "source_candidate_set_digest_invalid",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateEvaluationReceiptSurface",
        "SubsequentCycleCandidateEvaluationReceiptBoundary",
        "PlanOSSubsequentCycleCandidateEvaluationReceiptBridge",
        "source_materializes_nonempty_unique_set_without_selection",
        "evaluation_is_complete_exact_bounded_and_digest_bound",
        "receipt_records_evaluations_without_review_selection_or_admission",
        "boundary_is_candidate_evaluation_receipt_only",
        "history_appends_one_candidate_evaluation_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateEvaluationReceiptV0_67",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleCandidateEvaluationReceiptV0_67",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Candidate Evaluation Receipt v0.67",
        "evaluation input count equals candidate count",
        "subsequent-cycle candidate review requested = false",
        "evaluation order is not selection = true",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67.py",
        "v0.1-v0.67",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v067",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["score_bounds"]["minimum"] == MIN_COMPONENT_SCORE, "minimum score mismatch")
    require(manifest["score_bounds"]["maximum"] == MAX_COMPONENT_SCORE, "maximum score mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle candidate evaluation receipt v0.67 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
