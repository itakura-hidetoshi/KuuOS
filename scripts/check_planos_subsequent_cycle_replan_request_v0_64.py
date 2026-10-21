#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_next_cycle_closeout_receipt_v0_63 import _ready_next_cycle_start_receipt
from runtime.kuuos_planos_next_cycle_closeout_receipt_v0_63 import build_next_cycle_closeout_receipt
from runtime.kuuos_planos_subsequent_cycle_replan_request_v0_64 import (
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_replan_request,
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


def _ready_next_cycle_closeout_receipt() -> dict:
    source = _ready_next_cycle_start_receipt()
    return build_next_cycle_closeout_receipt(next_cycle_start_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_next_cycle_closeout_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_subsequent_cycle_replan_request(next_cycle_closeout_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_READY",
        f"replan request blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["request_owned_by_plan_os"] is True, "request owner missing")
    require(boundary["source_next_cycle_closeout_receipt_preserved"] is True, "source closeout not preserved")
    require(boundary["selected_candidate_bound_to_next_cycle_closeout"] is True, "candidate not bound to closeout")
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(boundary["truth_authority_cycle_closed_preserved"] is True, "truth closeout not preserved")
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(boundary["blocker_release_cycle_closed_preserved"] is True, "blocker closeout not preserved")
    require(boundary["next_cycle_admission_request_preserved"] is True, "admission request not preserved")
    require(boundary["next_cycle_admission_grant_preserved"] is True, "admission grant not preserved")
    require(boundary["next_cycle_start_receipt_preserved"] is True, "start receipt not preserved")
    require(boundary["next_cycle_closeout_receipt_preserved"] is True, "closeout receipt not preserved")
    require(boundary["next_cycle_cycle_closed"] is True, "closed next cycle not preserved")
    require(boundary["subsequent_cycle_replan_request_only"] is True, "request-only boundary missing")
    require(boundary["subsequent_cycle_replan_requested"] is True, "replan request missing")
    require(boundary["subsequent_cycle_candidate_generation_started"] is False, "candidate generation started early")
    require(boundary["subsequent_cycle_admission_requested"] is False, "subsequent admission requested early")

    record = receipt["subsequent_cycle_replan_request"]
    require(record["next_cycle_cycle_closed"] is True, "request lost next-cycle closeout")
    require(record["subsequent_cycle_replan_requested"] is True, "record did not request replan")
    require(record["subsequent_cycle_candidate_generation_started"] is False, "record started candidate generation")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")
    require(record["source_blocker_release_authorization_request_digest"], "request digest chain missing")

    pre_requested = dict(source)
    pre_requested_boundary = dict(pre_requested["boundary"])
    pre_requested_boundary["subsequent_cycle_replan_requested"] = True
    pre_requested["boundary"] = pre_requested_boundary
    blocked_boundary = build_subsequent_cycle_replan_request(next_cycle_closeout_receipt=pre_requested).to_dict()
    require(blocked_boundary["status"] == "PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_BLOCKED", "pre-requested boundary not blocked")
    require(
        "source_boundary_subsequent_cycle_replan_requested_promoted" in blocked_boundary["blockers"],
        "pre-request boundary blocker missing",
    )

    pre_requested_record = dict(source)
    source_record = dict(pre_requested_record["next_cycle_closeout_receipt"])
    source_record["subsequent_cycle_replan_requested"] = True
    pre_requested_record["next_cycle_closeout_receipt"] = source_record
    blocked_record = build_subsequent_cycle_replan_request(next_cycle_closeout_receipt=pre_requested_record).to_dict()
    require(blocked_record["status"] == "PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_BLOCKED", "pre-requested record not blocked")
    require(
        "source_record_subsequent_cycle_replan_requested_promoted" in blocked_record["blockers"],
        "pre-request record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["next_cycle_closeout_receipt"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["next_cycle_closeout_receipt"] = mismatch_record
    blocked_mismatch = build_subsequent_cycle_replan_request(next_cycle_closeout_receipt=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_BLOCKED", "mismatch not blocked")
    require(
        "selected_candidate_digest_next_cycle_closeout_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_replan_request_v0_64.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleReplanRequestV0_64.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_64.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_v0_64.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_replan_request_v0_64.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_replan_request",
        "PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_READY",
        "subsequent_cycle_replan_request_only",
        "subsequent_cycle_candidate_generation_started",
        "subsequent_cycle_admission_requested",
    ))
    require_tokens(formal, (
        "SubsequentCycleReplanRequestSurface",
        "SubsequentCycleReplanRequestBoundary",
        "PlanOSSubsequentCycleReplanRequestBridge",
        "source_closeout_closes_cycle_without_replan_request",
        "request_preserves_closed_authority_and_cycle_chain",
        "request_opens_replan_without_candidate_generation_or_admission",
        "boundary_is_subsequent_cycle_replan_request_only",
        "history_appends_one_subsequent_cycle_replan_request",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleReplanRequestV0_64",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleReplanRequestV0_64",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Replan Request v0.64",
        "subsequent cycle replan request only = true",
        "subsequent cycle candidate generation started = false",
        "subsequent cycle admission requested = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_replan_request_v0_64.py",
        "v0.1-v0.64",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v064",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for section in ("inputs", "outputs", "required"):
        for field, value in manifest[section].items():
            require(value is True, f"{section} field missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS subsequent-cycle replan request v0.64 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
