#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_next_cycle_start_receipt_v0_62 import _ready_next_cycle_admission_grant
from runtime.kuuos_planos_next_cycle_start_receipt_v0_62 import build_next_cycle_start_receipt
from runtime.kuuos_planos_next_cycle_closeout_receipt_v0_63 import (
    SOURCE_VERSION,
    VERSION,
    build_next_cycle_closeout_receipt,
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


def _ready_next_cycle_start_receipt() -> dict:
    source = _ready_next_cycle_admission_grant()
    return build_next_cycle_start_receipt(next_cycle_admission_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_next_cycle_start_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_next_cycle_closeout_receipt(next_cycle_start_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_READY",
        f"closeout blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["closeout_owned_by_plan_os"] is True, "closeout owner missing")
    require(
        boundary["source_next_cycle_start_receipt_preserved"] is True,
        "source start receipt not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_next_cycle_start_receipt"] is True,
        "selected candidate not bound to start receipt",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        boundary["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(
        boundary["blocker_release_cycle_closed_preserved"] is True,
        "blocker release closeout not preserved",
    )
    require(boundary["next_cycle_admission_request_preserved"] is True, "admission request not preserved")
    require(boundary["next_cycle_admission_grant_preserved"] is True, "admission grant not preserved")
    require(boundary["next_cycle_start_receipt_preserved"] is True, "start receipt not preserved")
    require(boundary["next_cycle_closeout_receipt_only"] is True, "closeout-only boundary missing")
    require(boundary["next_cycle_started"] is True, "next cycle start lost")
    require(boundary["next_cycle_cycle_closed"] is True, "next cycle not closed")
    require(boundary["subsequent_cycle_replan_requested"] is False, "subsequent replan opened early")

    record = receipt["next_cycle_closeout_receipt"]
    require(record["memory_overwrite_preserved"] is True, "closeout lost memory overwrite")
    require(record["truth_authority_preserved"] is True, "closeout lost truth authority")
    require(record["blocker_release_preserved"] is True, "closeout lost blocker release")
    require(record["next_cycle_admission_requested"] is True, "closeout lost admission request")
    require(record["next_cycle_admission_granted"] is True, "closeout lost admission grant")
    require(record["next_cycle_started"] is True, "closeout lost cycle start")
    require(record["next_cycle_cycle_closed"] is True, "closeout record did not close cycle")
    require(record["subsequent_cycle_replan_requested"] is False, "closeout record opened replan")
    require(record["source_blocker_release_authorization_request_digest"], "request digest not preserved")

    pre_closed = dict(source)
    pre_closed_boundary = dict(pre_closed["boundary"])
    pre_closed_boundary["next_cycle_cycle_closed"] = True
    pre_closed["boundary"] = pre_closed_boundary
    blocked_closed = build_next_cycle_closeout_receipt(next_cycle_start_receipt=pre_closed).to_dict()
    require(blocked_closed["status"] == "PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_BLOCKED", "pre-closed source not blocked")
    require(
        "source_boundary_next_cycle_cycle_closed_promoted" in blocked_closed["blockers"],
        "pre-close boundary blocker missing",
    )

    record_closed = dict(source)
    closed_record = dict(record_closed["next_cycle_start_receipt"])
    closed_record["next_cycle_cycle_closed"] = True
    record_closed["next_cycle_start_receipt"] = closed_record
    blocked_record = build_next_cycle_closeout_receipt(next_cycle_start_receipt=record_closed).to_dict()
    require(blocked_record["status"] == "PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_BLOCKED", "pre-closed record not blocked")
    require(
        "source_record_next_cycle_cycle_closed_promoted" in blocked_record["blockers"],
        "pre-close record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["next_cycle_start_receipt"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["next_cycle_start_receipt"] = mismatch_record
    blocked_mismatch = build_next_cycle_closeout_receipt(next_cycle_start_receipt=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_BLOCKED", "mismatch not blocked")
    require(
        "selected_candidate_digest_next_cycle_start_receipt_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_next_cycle_closeout_receipt_v0_63.py"
    formal = ROOT / "formal/KUOS/PlanOS/NextCycleCloseoutReceiptV0_63.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_63.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_v0_63.md"
    manifest_path = ROOT / "manifests/kuuos_planos_next_cycle_closeout_receipt_v0_63.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_next_cycle_closeout_receipt",
        "PLANOS_NEXT_CYCLE_CLOSEOUT_RECEIPT_READY",
        "next_cycle_closeout_receipt_only",
        "next_cycle_cycle_closed",
        "subsequent_cycle_replan_requested",
    ))
    require_tokens(formal, (
        "NextCycleCloseoutReceiptSurface",
        "NextCycleCloseoutReceiptBoundary",
        "PlanOSNextCycleCloseoutReceiptBridge",
        "source_start_records_started_but_open_cycle",
        "closeout_binds_candidate_and_preserves_prior_authority_chain",
        "receipt_closes_started_cycle_without_requesting_subsequent_replan",
        "boundary_is_next_cycle_closeout_receipt_only",
        "history_appends_one_next_cycle_closeout_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.NextCycleCloseoutReceiptV0_63",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.NextCycleCloseoutReceiptV0_63",))
    require_tokens(docs, (
        "PlanOS Next-Cycle Closeout Receipt v0.63",
        "next cycle closeout receipt only = true",
        "next cycle cycle closed = true",
        "subsequent cycle replan requested = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_next_cycle_closeout_receipt_v0_63.py",
        "v0.1-v0.63",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v063",))

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
    print("PlanOS next-cycle closeout receipt v0.63 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
