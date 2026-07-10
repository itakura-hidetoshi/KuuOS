#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_candidate_review_receipt_v0_69 import (
    _ready_candidate_review_sources,
    _review_specs,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_review_receipt_v0_69 import (
    build_subsequent_cycle_candidate_review_receipt,
)
from runtime.kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70 import (
    REQUIRED_SELECTION_SCOPE,
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_selection_authorization_request,
)

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIGEST = "subsequent-cycle-selection-policy-v1"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_review_receipt() -> dict:
    request, evaluation = _ready_candidate_review_sources()
    return build_subsequent_cycle_candidate_review_receipt(
        candidate_review_request=request,
        candidate_evaluation_receipt=evaluation,
        review_specs=_review_specs(),
    ).to_dict()


def _build(source: dict, *, scope: str = REQUIRED_SELECTION_SCOPE, policy: str = POLICY_DIGEST) -> dict:
    return build_subsequent_cycle_candidate_selection_authorization_request(
        candidate_review_receipt=source,
        selection_scope=scope,
        selection_policy_digest=policy,
    ).to_dict()


def _exercise_runtime() -> None:
    source = _ready_review_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    request = _build(source)
    require(request["version"] == VERSION, "runtime version mismatch")
    require(
        request["status"] == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY",
        f"authorization request blocked: {request.get('blockers')}",
    )
    require(request["candidate_count"] == 3, "candidate count mismatch")
    require(request["evaluation_count"] == 3, "evaluation count mismatch")
    require(request["review_count"] == 3, "review count mismatch")
    require(request["selection_eligible_count"] == 2, "eligible count mismatch")
    require(len(request["selection_eligible_candidates"]) == 2, "eligible projection mismatch")
    require(request["selection_eligible_set_digest"], "eligible-set digest missing")
    require(request["selection_scope"] == REQUIRED_SELECTION_SCOPE, "selection scope mismatch")
    require(request["selection_policy_digest"] == POLICY_DIGEST, "selection policy mismatch")

    ids = [item["candidate_id"] for item in request["selection_eligible_candidates"]]
    require(ids == ["repair-route::continuity", "repair-route::refinement"], "eligible candidates mismatch")
    for item in request["selection_eligible_candidates"]:
        require(item["candidate_digest"], "candidate digest missing")
        require(item["evaluation_digest"], "evaluation digest missing")
        require(item["review_digest"], "review digest missing")

    boundary = request["boundary"]
    for field in (
        "request_owned_by_plan_os",
        "source_candidate_review_receipt_preserved",
        "selected_candidate_provenance_preserved",
        "candidate_set_digest_preserved",
        "evaluation_set_digest_preserved",
        "review_set_digest_preserved",
        "review_count_exact_preserved",
        "candidate_review_completed_preserved",
        "selection_eligibility_preserved",
        "selection_eligible_set_nonempty",
        "memory_overwrite_preserved",
        "truth_authority_preserved",
        "blocker_release_preserved",
        "next_cycle_cycle_closed",
        "subsequent_cycle_replan_requested",
        "subsequent_cycle_candidate_generation_started",
        "subsequent_cycle_candidate_set_materialized",
        "subsequent_cycle_candidate_evaluations_recorded",
        "subsequent_cycle_candidate_review_requested",
        "subsequent_cycle_candidate_review_completed",
        "subsequent_cycle_candidate_selection_authorization_request_only",
        "subsequent_cycle_candidate_selection_authorization_requested",
        "subsequent_cycle_selection_scope_bound",
        "subsequent_cycle_selection_policy_digest_bound",
    ):
        require(boundary[field] is True, f"required boundary missing: {field}")
    for field in (
        "subsequent_cycle_selection_authority_granted",
        "subsequent_cycle_candidate_selection_requested",
        "subsequent_cycle_candidate_selected",
        "subsequent_cycle_admission_requested",
    ):
        require(boundary[field] is False, f"closed boundary promoted: {field}")

    record = request["subsequent_cycle_candidate_selection_authorization_request"]
    require(record["selection_eligible_count"] == 2, "record eligible count mismatch")
    require(record["selection_eligible_set_digest"] == request["selection_eligible_set_digest"], "record eligible digest mismatch")
    require(record["authorization_request_digest"], "authorization request digest missing")
    require(record["candidate_selection_authorization_requested"] is True, "authorization not requested")
    require(record["selection_authority_granted"] is False, "authority granted")
    require(record["candidate_selection_requested"] is False, "selection requested")
    require(record["candidate_selected"] is False, "candidate selected")
    require(record["admission_requested"] is False, "admission requested")

    invalid_scope = _build(source, scope="highest_score_candidate")
    require(invalid_scope["status"].endswith("BLOCKED"), "invalid scope not blocked")
    require("selection_scope_invalid" in invalid_scope["blockers"], "scope blocker missing")

    missing_policy = _build(source, policy="")
    require(missing_policy["status"].endswith("BLOCKED"), "missing policy not blocked")
    require("selection_policy_digest_missing" in missing_policy["blockers"], "policy blocker missing")

    tampered = dict(source)
    outcomes = [dict(outcome) for outcome in source["review_outcomes"]]
    outcomes[0]["selection_eligible"] = False
    tampered["review_outcomes"] = outcomes
    blocked_tamper = _build(tampered)
    require(blocked_tamper["status"].endswith("BLOCKED"), "tampered review not blocked")
    require("source_review_set_digest_invalid" in blocked_tamper["blockers"], "review digest blocker missing")
    require("source_selection_eligible_count_mismatch" in blocked_tamper["blockers"], "eligible count blocker missing")

    empty = dict(source)
    empty_outcomes = [dict(outcome) for outcome in source["review_outcomes"]]
    for outcome in empty_outcomes:
        outcome["selection_eligible"] = False
    from runtime.kuuos_belief_os_types_v0_1 import sha
    empty["review_outcomes"] = empty_outcomes
    empty["review_set_digest"] = sha(empty_outcomes)
    empty["selection_eligible_count"] = 0
    empty_record = dict(empty["subsequent_cycle_candidate_review_receipt"])
    empty_record["review_set_digest"] = empty["review_set_digest"]
    empty_record["selection_eligible_count"] = 0
    empty["subsequent_cycle_candidate_review_receipt"] = empty_record
    blocked_empty = _build(empty)
    require(blocked_empty["status"].endswith("BLOCKED"), "empty eligible set not blocked")
    require("source_selection_eligible_set_empty" in blocked_empty["blockers"], "empty eligible blocker missing")
    require("selection_eligible_candidates_missing" in blocked_empty["blockers"], "eligible projection blocker missing")

    duplicate = dict(source)
    duplicate_outcomes = [dict(outcome) for outcome in source["review_outcomes"]]
    duplicate_outcomes[1]["candidate_id"] = duplicate_outcomes[0]["candidate_id"]
    duplicate["review_outcomes"] = duplicate_outcomes
    duplicate["review_set_digest"] = sha(duplicate_outcomes)
    duplicate_record = dict(duplicate["subsequent_cycle_candidate_review_receipt"])
    duplicate_record["review_set_digest"] = duplicate["review_set_digest"]
    duplicate["subsequent_cycle_candidate_review_receipt"] = duplicate_record
    blocked_duplicate = _build(duplicate)
    require(blocked_duplicate["status"].endswith("BLOCKED"), "duplicate candidate not blocked")
    require("source_review_candidate_ids_not_unique" in blocked_duplicate["blockers"], "duplicate blocker missing")

    pregranted = dict(source)
    pregranted_boundary = dict(pregranted["boundary"])
    pregranted_boundary["subsequent_cycle_selection_authority_granted"] = True
    pregranted["boundary"] = pregranted_boundary
    blocked_pregranted = _build(pregranted)
    require(blocked_pregranted["status"].endswith("BLOCKED"), "pregranted authority not blocked")
    require("source_boundary_subsequent_cycle_selection_authority_granted_promoted" in blocked_pregranted["blockers"], "pregrant blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateSelectionAuthorizationRequestV0_70.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_70.lean"
    aggregate = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_v0_70.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70.json"
    for path in (runtime, formal, formal_root, aggregate, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_selection_authorization_request",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_SELECTION_AUTHORIZATION_REQUEST_READY",
        "selection_eligible_set_digest",
        "selection_scope_invalid",
        "selection_policy_digest_missing",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateSelectionAuthorizationRequestSurface",
        "PlanOSSubsequentCycleCandidateSelectionAuthorizationRequestBridge",
        "source_review_is_complete_without_selection",
        "request_is_bounded_and_does_not_select",
        "boundary_is_selection_authorization_request_only",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateSelectionAuthorizationRequestV0_70",))
    require_tokens(aggregate, ("KUOS.PlanOS.SubsequentCycleCandidateSelectionAuthorizationRequestV0_70",))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_selection_authorization_request_v0_70.py",
        "v0.1-v0.70",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v070",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "manifest source mismatch")
    require(manifest["required_selection_scope"] == REQUIRED_SELECTION_SCOPE, "manifest scope mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle candidate selection authorization request v0.70 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
