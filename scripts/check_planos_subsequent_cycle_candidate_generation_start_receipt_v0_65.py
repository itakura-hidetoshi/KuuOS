#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_subsequent_cycle_replan_request_v0_64 import _ready_next_cycle_closeout_receipt
from runtime.kuuos_planos_subsequent_cycle_replan_request_v0_64 import build_subsequent_cycle_replan_request
from runtime.kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65 import (
    SOURCE_VERSION,
    VERSION,
    build_subsequent_cycle_candidate_generation_start_receipt,
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


def _ready_subsequent_cycle_replan_request() -> dict:
    source = _ready_next_cycle_closeout_receipt()
    return build_subsequent_cycle_replan_request(next_cycle_closeout_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_subsequent_cycle_replan_request()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_subsequent_cycle_candidate_generation_start_receipt(
        subsequent_cycle_replan_request=source
    ).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"]
        == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_READY",
        f"candidate-generation start blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")

    boundary = receipt["boundary"]
    require(boundary["receipt_owned_by_plan_os"] is True, "receipt owner missing")
    require(
        boundary["source_subsequent_cycle_replan_request_preserved"] is True,
        "source replan request not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_replan_request"] is True,
        "candidate provenance not bound to replan request",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(boundary["truth_authority_cycle_closed_preserved"] is True, "truth closeout not preserved")
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(boundary["blocker_release_cycle_closed_preserved"] is True, "blocker closeout not preserved")
    require(boundary["next_cycle_closeout_receipt_preserved"] is True, "next-cycle closeout not preserved")
    require(boundary["subsequent_cycle_replan_request_preserved"] is True, "replan request not preserved")
    require(boundary["subsequent_cycle_replan_requested"] is True, "replan request state lost")
    require(
        boundary["subsequent_cycle_candidate_generation_start_receipt_only"] is True,
        "start-receipt-only boundary missing",
    )
    require(
        boundary["subsequent_cycle_candidate_generation_started"] is True,
        "candidate generation did not start",
    )
    require(
        boundary["subsequent_cycle_candidate_set_materialized"] is False,
        "candidate set materialized early",
    )
    require(boundary["subsequent_cycle_candidate_selected"] is False, "candidate selected early")
    require(boundary["subsequent_cycle_admission_requested"] is False, "admission requested early")

    record = receipt["subsequent_cycle_candidate_generation_start_receipt"]
    require(record["subsequent_cycle_replan_requested"] is True, "record lost replan request")
    require(record["subsequent_cycle_candidate_generation_started"] is True, "record did not start generation")
    require(record["subsequent_cycle_candidate_set_materialized"] is False, "record materialized set")
    require(record["subsequent_cycle_candidate_selected"] is False, "record selected candidate")
    require(record["subsequent_cycle_admission_requested"] is False, "record requested admission")
    require(record["source_subsequent_cycle_replan_request_digest"], "replan request digest missing")
    require(record["source_blocker_release_authorization_request_digest"], "authority chain missing")

    pre_started = dict(source)
    pre_started_boundary = dict(pre_started["boundary"])
    pre_started_boundary["subsequent_cycle_candidate_generation_started"] = True
    pre_started["boundary"] = pre_started_boundary
    blocked_boundary = build_subsequent_cycle_candidate_generation_start_receipt(
        subsequent_cycle_replan_request=pre_started
    ).to_dict()
    require(
        blocked_boundary["status"]
        == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_BLOCKED",
        "pre-started boundary not blocked",
    )
    require(
        "source_boundary_subsequent_cycle_candidate_generation_started_promoted"
        in blocked_boundary["blockers"],
        "pre-start boundary blocker missing",
    )

    pre_started_record = dict(source)
    source_record = dict(pre_started_record["subsequent_cycle_replan_request"])
    source_record["subsequent_cycle_candidate_generation_started"] = True
    pre_started_record["subsequent_cycle_replan_request"] = source_record
    blocked_record = build_subsequent_cycle_candidate_generation_start_receipt(
        subsequent_cycle_replan_request=pre_started_record
    ).to_dict()
    require(
        blocked_record["status"]
        == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_BLOCKED",
        "pre-started record not blocked",
    )
    require(
        "source_record_subsequent_cycle_candidate_generation_started_promoted"
        in blocked_record["blockers"],
        "pre-start record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["subsequent_cycle_replan_request"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["subsequent_cycle_replan_request"] = mismatch_record
    blocked_mismatch = build_subsequent_cycle_candidate_generation_start_receipt(
        subsequent_cycle_replan_request=mismatch
    ).to_dict()
    require(
        blocked_mismatch["status"]
        == "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_BLOCKED",
        "digest mismatch not blocked",
    )
    require(
        "selected_candidate_digest_subsequent_cycle_replan_request_mismatch"
        in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65.py"
    formal = ROOT / "formal/KUOS/PlanOS/SubsequentCycleCandidateGenerationStartReceiptV0_65.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_65.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_v0_65.md"
    manifest_path = ROOT / "manifests/kuuos_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_subsequent_cycle_candidate_generation_start_receipt",
        "PLANOS_SUBSEQUENT_CYCLE_CANDIDATE_GENERATION_START_RECEIPT_READY",
        "subsequent_cycle_candidate_generation_start_receipt_only",
        "subsequent_cycle_candidate_set_materialized",
        "subsequent_cycle_candidate_selected",
    ))
    require_tokens(formal, (
        "SubsequentCycleCandidateGenerationStartReceiptSurface",
        "SubsequentCycleCandidateGenerationStartReceiptBoundary",
        "PlanOSSubsequentCycleCandidateGenerationStartReceiptBridge",
        "source_request_opens_replan_without_candidate_generation",
        "start_receipt_preserves_closed_authority_and_cycle_chain",
        "receipt_starts_candidate_generation_without_materialization_selection_or_admission",
        "boundary_is_candidate_generation_start_receipt_only",
        "history_appends_one_candidate_generation_start_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.SubsequentCycleCandidateGenerationStartReceiptV0_65",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.SubsequentCycleCandidateGenerationStartReceiptV0_65",))
    require_tokens(docs, (
        "PlanOS Subsequent-Cycle Candidate-Generation Start Receipt v0.65",
        "subsequent-cycle candidate-generation start receipt only = true",
        "subsequent-cycle candidate set materialized = false",
        "subsequent-cycle admission requested = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_subsequent_cycle_candidate_generation_start_receipt_v0_65.py",
        "v0.1-v0.65",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v065",))

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
    print("PlanOS subsequent-cycle candidate generation start receipt v0.65 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
