#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67 import (
    _evaluation_specs,
    _ready_candidate_set_materialization_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_evaluation_receipt_v0_67 import (
    build_subsequent_cycle_candidate_evaluation_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_review_request_v0_68 import (
    REQUIRED_REVIEW_SCOPE,
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_review_request,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION
REVIEW_CRITERIA_DIGEST = "subsequent-cycle-review-criteria-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_candidate_evaluation_receipt() -> dict:
    source = _ready_candidate_set_materialization_receipt()
    return build_subsequent_cycle_candidate_evaluation_receipt(
        candidate_set_materialization_receipt=source,
        evaluation_specs=_evaluation_specs(),
    ).to_dict()


def _build(source: dict, *, scope: str = REQUIRED_REVIEW_SCOPE, criteria: str = REVIEW_CRITERIA_DIGEST) -> dict:
    return build_subsequent_cycle_candidate_review_request(
        candidate_evaluation_receipt=source,
        review_scope=scope,
        review_criteria_digest=criteria,
    ).to_dict()


def _exercise_runtime() -> None:
    source = _ready_candidate_evaluation_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    request = _build(source)
    require(request["version"] == VERSION, "runtime version mismatch")
    require(
        request["status"] == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_READY",
        f"candidate review request blocked: {request.get('blockers')}",
    )
    require(request["candidate_count"] == 3, "candidate count mismatch")
    require(request["evaluation_count"] == 3, "evaluation count mismatch")
    require(request["candidate_set_digest"] == source["candidate_set_digest"], "candidate-set digest changed")
    require(request["evaluation_set_digest"] == source["evaluation_set_digest"], "evaluation-set digest changed")
    require(request["review_scope"] == REQUIRED_REVIEW_SCOPE, "review scope mismatch")
    require(request["review_criteria_digest"] == REVIEW_CRITERIA_DIGEST, "review criteria mismatch")

    boundary = request["boundary"]
    for field in (
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
    ):
        require(boundary[field] is True, f"required boundary missing: {field}")
    for field in (
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_review_completed",
        "subsequent_cycle_candidate_selected",
        "subsequent_cycle_admission_requested",
    ):
        require(boundary[field] is False, f"closed boundary promoted: {field}")

    record = request["subsequent_cycle_candidate_review_request"]
    require(record["candidate_count"] == request["candidate_count"], "record candidate count mismatch")
    require(record["evaluation_count"] == request["evaluation_count"], "record evaluation count mismatch")
    require(record["candidate_set_digest"] == request["candidate_set_digest"], "record candidate-set digest mismatch")
    require(record["evaluation_set_digest"] == request["evaluation_set_digest"], "record evaluation-set digest mismatch")
    require(record["review_scope"] == REQUIRED_REVIEW_SCOPE, "record scope mismatch")
    require(record["review_criteria_digest"] == REVIEW_CRITERIA_DIGEST, "record criteria mismatch")
    require(record["review_request_digest"], "review request digest missing")
    require(record["subsequent_cycle_candidate_review_requested"] is True, "record did not request review")
    require(record["subsequent_cycle_selection_authority_granted"] is False, "record granted selection authority")
    require(record["subsequent_cycle_candidate_review_completed"] is False, "record completed review")
    require(record["subsequent_cycle_candidate_selected"] is False, "record selected candidate")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")
    require(record["source_candidate_set_materialization_receipt_digest"], "materialization digest missing")
    require(record["source_candidate_generation_start_receipt_digest"], "generation digest missing")
    require(record["source_subsequent_cycle_replan_request_digest"], "replan digest missing")

    invalid_scope = _build(source, scope="candidate_score_order")
    require(invalid_scope["status"].endswith("BLOCKED"), "invalid scope not blocked")
    require("review_scope_invalid" in invalid_scope["blockers"], "invalid-scope blocker missing")

    missing_criteria = _build(source, criteria="")
    require(missing_criteria["status"].endswith("BLOCKED"), "missing criteria not blocked")
    require("review_criteria_digest_missing" in missing_criteria["blockers"], "criteria blocker missing")

    tampered = dict(source)
    tampered_evaluations = [dict(evaluation) for evaluation in source["evaluations"]]
    tampered_evaluations[0]["total_score"] += 1
    tampered["evaluations"] = tampered_evaluations
    blocked_tamper = _build(tampered)
    require(blocked_tamper["status"].endswith("BLOCKED"), "tampered evaluations not blocked")
    require("source_evaluation_set_digest_invalid" in blocked_tamper["blockers"], "evaluation digest blocker missing")

    count_mismatch = dict(source)
    count_mismatch["evaluation_count"] = source["evaluation_count"] - 1
    blocked_count = _build(count_mismatch)
    require(blocked_count["status"].endswith("BLOCKED"), "count mismatch not blocked")
    require("source_evaluation_count_not_exact" in blocked_count["blockers"], "exact-count blocker missing")
    require("source_evaluation_list_count_mismatch" in blocked_count["blockers"], "list-count blocker missing")

    duplicate = dict(source)
    duplicate_evaluations = [dict(evaluation) for evaluation in source["evaluations"]]
    duplicate_evaluations[1]["candidate_id"] = duplicate_evaluations[0]["candidate_id"]
    duplicate["evaluations"] = duplicate_evaluations
    duplicate["evaluation_set_digest"] = __import__(
        "runtime.kuuos_belief_os_types_v0_1", fromlist=["sha"]
    ).sha(duplicate_evaluations)
    duplicate_record = dict(duplicate["subsequent_cycle_candidate_evaluation_receipt"])
    duplicate_record["evaluation_set_digest"] = duplicate["evaluation_set_digest"]
    duplicate["subsequent_cycle_candidate_evaluation_receipt"] = duplicate_record
    blocked_duplicate = _build(duplicate)
    require(blocked_duplicate["status"].endswith("BLOCKED"), "duplicate candidate evaluation not blocked")
    require("source_evaluation_candidate_ids_not_unique" in blocked_duplicate["blockers"], "duplicate-id blocker missing")

    pre_requested = dict(source)
    pre_requested_boundary = dict(pre_requested["boundary"])
    pre_requested_boundary["subsequent_cycle_candidate_review_requested"] = True
    pre_requested["boundary"] = pre_requested_boundary
    blocked_pre_requested = _build(pre_requested)
    require(blocked_pre_requested["status"].endswith("BLOCKED"), "pre-requested review not blocked")
    require(
        "source_boundary_subsequent_cycle_candidate_review_requested_promoted"
        in blocked_pre_requested["blockers"],
        "pre-requested boundary blocker missing",
    )

    preselected_record = dict(source)
    source_record = dict(preselected_record["subsequent_cycle_candidate_evaluation_receipt"])
    source_record["subsequent_cycle_candidate_selected"] = True
    preselected_record["subsequent_cycle_candidate_evaluation_receipt"] = source_record
    blocked_preselected = _build(preselected_record)
    require(blocked_preselected["status"].endswith("BLOCKED"), "preselected record not blocked")
    require("source_record_subsequent_cycle_candidate_selected_promoted" in blocked_preselected["blockers"], "preselected record blocker missing")

    provenance_mismatch = dict(source)
    provenance_record = dict(provenance_mismatch["subsequent_cycle_candidate_evaluation_receipt"])
    provenance_record["selected_candidate_digest"] = "wrong-digest"
    provenance_mismatch["subsequent_cycle_candidate_evaluation_receipt"] = provenance_record
    blocked_provenance = _build(provenance_mismatch)
    require(blocked_provenance["status"].endswith("BLOCKED"), "provenance mismatch not blocked")
    require(
        "selected_candidate_digest_evaluation_receipt_mismatch" in blocked_provenance["blockers"],
        "provenance blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_review_request_v0_68.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateReviewRequestV0_68.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_68.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_v0_68.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_review_request_v0_68.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_review_request",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_REVIEW_REQUEST_READY",
        "REQUIRED_REVIEW_SCOPE",
        "source_evaluation_set_digest_invalid",
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_review_completed",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateReviewRequestSurface",
        "SubsequentCycleCandidateReviewRequestBoundary",
        "PlanOSSubsequentCycleCandidateReviewRequestBridge",
        "source_records_complete_evaluations_without_review_or_selection",
        "review_request_preserves_evaluation_and_authority_chain",
        "request_binds_review_scope_without_selection_authority",
        "boundary_is_candidate_review_request_only",
        "history_appends_one_candidate_review_request",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateReviewRequestV0_68",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleCandidateReviewRequestV0_68",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Candidate Review Request v0.68",
        "review request is opened without selection authority",
        "subsequent-cycle selection authority granted = false",
        "evaluation order nonselection preserved = true",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_review_request_v0_68.py",
        "v0.1-v0.68",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v068",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["required_review_scope"] == REQUIRED_REVIEW_SCOPE, "review scope mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle candidate review request v0.68 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
