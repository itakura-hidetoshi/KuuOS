#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_candidate_review_request_v0_68 import (
    REVIEW_CRITERIA_DIGEST,
    _ready_candidate_evaluation_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_review_request_v0_68 import (
    REQUIRED_REVIEW_SCOPE,
    build_subsequent_cycle_candidate_review_request,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69 import (
    ALLOWED_REVIEW_DISPOSITIONS,
    EVALUATION_SOURCE_VERSION,
    SELECTION_ELIGIBLE_DISPOSITIONS,
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_review_receipt,
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


def _ready_candidate_review_sources() -> tuple[dict, dict]:
    evaluation = _ready_candidate_evaluation_receipt()
    request = build_subsequent_cycle_candidate_review_request(
        candidate_evaluation_receipt=evaluation,
        review_scope=REQUIRED_REVIEW_SCOPE,
        review_criteria_digest=REVIEW_CRITERIA_DIGEST,
    ).to_dict()
    return request, evaluation


def _review_specs() -> list[dict[str, str]]:
    return [
        {
            "candidate_id": "repair-route::continuity",
            "review_disposition": "eligible",
            "review_rationale_digest": "review-rationale-continuity-v1",
            "review_constraints_digest": "review-constraints-continuity-v1",
        },
        {
            "candidate_id": "repair-route::refinement",
            "review_disposition": "eligible_with_conditions",
            "review_rationale_digest": "review-rationale-refinement-v1",
            "review_constraints_digest": "review-constraints-refinement-v1",
        },
        {
            "candidate_id": "repair-route::recovery",
            "review_disposition": "deferred",
            "review_rationale_digest": "review-rationale-recovery-v1",
            "review_constraints_digest": "review-constraints-recovery-v1",
        },
    ]


def _build(request: dict, evaluation: dict, specs: list[dict[str, str]] | None = None) -> dict:
    return build_subsequent_cycle_candidate_review_receipt(
        candidate_review_request=request,
        candidate_evaluation_receipt=evaluation,
        review_specs=_review_specs() if specs is None else specs,
    ).to_dict()


def _exercise_runtime() -> None:
    request, evaluation = _ready_candidate_review_sources()
    require(request["version"] == SOURCE_VERSION, "request source version mismatch")
    require(evaluation["version"] == EVALUATION_SOURCE_VERSION, "evaluation source version mismatch")
    receipt = _build(request, evaluation)
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_READY",
        f"candidate review receipt blocked: {receipt.get('blockers')}",
    )
    require(receipt["candidate_count"] == 3, "candidate count mismatch")
    require(receipt["evaluation_count"] == 3, "evaluation count mismatch")
    require(receipt["review_count"] == 3, "review count mismatch")
    require(receipt["selection_eligible_count"] == 2, "eligible count mismatch")
    require(receipt["candidate_set_digest"] == evaluation["candidate_set_digest"], "candidate-set digest changed")
    require(receipt["evaluation_set_digest"] == evaluation["evaluation_set_digest"], "evaluation-set digest changed")
    require(receipt["review_scope"] == REQUIRED_REVIEW_SCOPE, "review scope mismatch")
    require(receipt["review_criteria_digest"] == REVIEW_CRITERIA_DIGEST, "review criteria mismatch")
    require(receipt["review_set_digest"], "review-set digest missing")

    evaluation_by_id = {
        item["candidate_id"]: item for item in evaluation["evaluations"]
    }
    expected = {
        "repair-route::continuity": ("eligible", True),
        "repair-route::refinement": ("eligible_with_conditions", True),
        "repair-route::recovery": ("deferred", False),
    }
    for ordinal, outcome in enumerate(receipt["review_outcomes"]):
        candidate_id = outcome["candidate_id"]
        source = evaluation_by_id[candidate_id]
        disposition, eligible = expected[candidate_id]
        require(outcome["review_ordinal"] == ordinal, "review ordinal mismatch")
        require(outcome["candidate_digest"] == source["candidate_digest"], "candidate digest mismatch")
        require(outcome["evaluation_digest"] == source["evaluation_digest"], "evaluation digest mismatch")
        require(outcome["total_score"] == source["total_score"], "total score mismatch")
        require(outcome["review_disposition"] == disposition, "review disposition mismatch")
        require(outcome["selection_eligible"] is eligible, "selection eligibility mismatch")
        require(outcome["review_digest"], "review digest missing")

    boundary = receipt["boundary"]
    for field in (
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
    ):
        require(boundary[field] is True, f"required boundary missing: {field}")
    for field in (
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_selection_requested",
        "subsequent_cycle_candidate_selected",
        "subsequent_cycle_admission_requested",
    ):
        require(boundary[field] is False, f"closed boundary promoted: {field}")

    record = receipt["subsequent_cycle_candidate_review_receipt"]
    require(record["candidate_count"] == receipt["candidate_count"], "record candidate count mismatch")
    require(record["evaluation_count"] == receipt["evaluation_count"], "record evaluation count mismatch")
    require(record["review_count"] == receipt["review_count"], "record review count mismatch")
    require(record["selection_eligible_count"] == 2, "record eligible count mismatch")
    require(record["candidate_set_digest"] == receipt["candidate_set_digest"], "record candidate digest mismatch")
    require(record["evaluation_set_digest"] == receipt["evaluation_set_digest"], "record evaluation digest mismatch")
    require(record["review_set_digest"] == receipt["review_set_digest"], "record review-set digest mismatch")
    require(record["review_receipt_digest"], "record receipt digest missing")
    require(record["subsequent_cycle_candidate_review_requested"] is True, "record lost review request")
    require(record["subsequent_cycle_all_evaluated_candidates_reviewed"] is True, "record coverage missing")
    require(record["subsequent_cycle_candidate_review_completed"] is True, "record review incomplete")
    require(record["subsequent_cycle_review_order_is_not_selection"] is True, "record review order promoted")
    require(record["subsequent_cycle_selection_eligibility_recorded"] is True, "record eligibility missing")
    require(record["subsequent_cycle_selection_authority_granted"] is False, "record granted authority")
    require(record["subsequent_cycle_candidate_selection_requested"] is False, "record requested selection")
    require(record["subsequent_cycle_candidate_selected"] is False, "record selected candidate")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")

    missing = _build(request, evaluation, _review_specs()[:-1])
    require(missing["status"].endswith("BLOCKED"), "missing review not blocked")
    require("review_missing_evaluated_candidate" in missing["blockers"], "missing-review blocker absent")
    require("evaluated_candidate_review_coverage_incomplete" in missing["blockers"], "coverage blocker absent")

    unknown_specs = _review_specs() + [
        {
            "candidate_id": "unknown-candidate",
            "review_disposition": "eligible",
            "review_rationale_digest": "unknown-rationale",
            "review_constraints_digest": "unknown-constraints",
        }
    ]
    unknown = _build(request, evaluation, unknown_specs)
    require(unknown["status"].endswith("BLOCKED"), "unknown review not blocked")
    require("review_contains_unknown_candidate" in unknown["blockers"], "unknown-review blocker absent")

    duplicate_specs = _review_specs()
    duplicate_specs[1] = dict(duplicate_specs[1])
    duplicate_specs[1]["candidate_id"] = duplicate_specs[0]["candidate_id"]
    duplicate = _build(request, evaluation, duplicate_specs)
    require(duplicate["status"].endswith("BLOCKED"), "duplicate review not blocked")
    require("review_candidate_ids_not_unique" in duplicate["blockers"], "duplicate-review blocker absent")

    invalid_disposition_specs = _review_specs()
    invalid_disposition_specs[0] = dict(invalid_disposition_specs[0])
    invalid_disposition_specs[0]["review_disposition"] = "auto_select"
    invalid_disposition = _build(request, evaluation, invalid_disposition_specs)
    require(invalid_disposition["status"].endswith("BLOCKED"), "invalid disposition not blocked")
    require(
        "review_repair-route::continuity_disposition_invalid" in invalid_disposition["blockers"],
        "invalid-disposition blocker absent",
    )

    missing_rationale_specs = _review_specs()
    missing_rationale_specs[0] = dict(missing_rationale_specs[0])
    missing_rationale_specs[0]["review_rationale_digest"] = ""
    missing_rationale = _build(request, evaluation, missing_rationale_specs)
    require(missing_rationale["status"].endswith("BLOCKED"), "missing rationale not blocked")
    require(
        "review_repair-route::continuity_rationale_digest_missing" in missing_rationale["blockers"],
        "rationale blocker absent",
    )

    missing_constraints_specs = _review_specs()
    missing_constraints_specs[0] = dict(missing_constraints_specs[0])
    missing_constraints_specs[0]["review_constraints_digest"] = ""
    missing_constraints = _build(request, evaluation, missing_constraints_specs)
    require(missing_constraints["status"].endswith("BLOCKED"), "missing constraints not blocked")
    require(
        "review_repair-route::continuity_constraints_digest_missing" in missing_constraints["blockers"],
        "constraints blocker absent",
    )

    tampered_evaluation = dict(evaluation)
    tampered_items = [dict(item) for item in evaluation["evaluations"]]
    tampered_items[0]["total_score"] += 1
    tampered_evaluation["evaluations"] = tampered_items
    tampered = _build(request, tampered_evaluation)
    require(tampered["status"].endswith("BLOCKED"), "tampered evaluation not blocked")
    require("candidate_evaluation_set_digest_invalid" in tampered["blockers"], "evaluation digest blocker absent")

    mismatched_evaluation = dict(evaluation)
    mismatched_evaluation["receipt_digest"] = "wrong-evaluation-receipt-digest"
    mismatch = _build(request, mismatched_evaluation)
    require(mismatch["status"].endswith("BLOCKED"), "request-evaluation mismatch not blocked")
    require(
        "candidate_evaluation_receipt_digest_request_mismatch" in mismatch["blockers"],
        "request-evaluation link blocker absent",
    )

    precompleted = dict(request)
    precompleted_boundary = dict(precompleted["boundary"])
    precompleted_boundary["subsequent_cycle_candidate_review_completed"] = True
    precompleted["boundary"] = precompleted_boundary
    blocked_precompleted = _build(precompleted, evaluation)
    require(blocked_precompleted["status"].endswith("BLOCKED"), "precompleted request not blocked")
    require(
        "source_request_boundary_subsequent_cycle_candidate_review_completed_promoted"
        in blocked_precompleted["blockers"],
        "precompleted boundary blocker absent",
    )

    preauthorized = dict(request)
    preauthorized_record = dict(preauthorized["subsequent_cycle_candidate_review_request"])
    preauthorized_record["subsequent_cycle_selection_authority_granted"] = True
    preauthorized["subsequent_cycle_candidate_review_request"] = preauthorized_record
    blocked_preauthorized = _build(preauthorized, evaluation)
    require(blocked_preauthorized["status"].endswith("BLOCKED"), "preauthorized request not blocked")
    require(
        "source_request_record_subsequent_cycle_selection_authority_granted_promoted"
        in blocked_preauthorized["blockers"],
        "preauthorized record blocker absent",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateReviewReceiptV0_69.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_69.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_v0_69.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_review_receipt",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_RECEIPT_READY",
        "CandidateReviewOutcome",
        "candidate_evaluation_receipt_digest_request_mismatch",
        "review_missing_evaluated_candidate",
        "subsequent_cycle_candidate_selection_requested",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateReviewReceiptSurface",
        "SubsequentCycleCandidateReviewReceiptBoundary",
        "PlanOSSubsequentCycleCandidateReviewReceiptBridge",
        "source_request_opens_review_without_selection",
        "source_evaluation_is_complete_exact_and_nonselective",
        "review_receipt_preserves_request_evaluation_and_authority_chain",
        "review_is_complete_exact_digest_bound_without_selection",
        "boundary_is_candidate_review_receipt_only",
        "history_appends_one_candidate_review_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateReviewReceiptV0_69",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleCandidateReviewReceiptV0_69",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Candidate Review Receipt v0.69",
        "review input count equals evaluation count",
        "subsequent-cycle candidate selection requested = false",
        "review completion does not grant selection authority",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_review_receipt_v0_69.py",
        "v0.1-v0.69",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v069",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["evaluation_source_version"] == EVALUATION_SOURCE_VERSION, "evaluation source mismatch")
    require(tuple(manifest["allowed_review_dispositions"]) == ALLOWED_REVIEW_DISPOSITIONS, "allowed dispositions mismatch")
    require(tuple(manifest["selection_eligible_dispositions"]) == SELECTION_ELIGIBLE_DISPOSITIONS, "eligible dispositions mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle candidate review receipt v0.69 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
