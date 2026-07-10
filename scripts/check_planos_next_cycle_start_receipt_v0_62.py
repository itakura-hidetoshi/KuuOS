#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_next_cycle_admission_grant_v0_61 import _ready_next_cycle_admission_request
from runtime.kuuos_planos_next_cycle_admission_grant_v0_61 import build_next_cycle_admission_grant
from runtime.kuuos_planos_next_cycle_start_receipt_v0_62 import (
    SOURCE_VERSION,
    VERSION,
    build_next_cycle_start_receipt,
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


def _ready_next_cycle_admission_grant() -> dict:
    source = _ready_next_cycle_admission_request()
    return build_next_cycle_admission_grant(next_cycle_admission_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_next_cycle_admission_grant()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_next_cycle_start_receipt(next_cycle_admission_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_NEXT_CYCLE_START_RECEIPT_READY",
        f"start receipt blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["receipt_owned_by_plan_os"] is True, "receipt owner missing")
    require(
        boundary["source_next_cycle_admission_grant_preserved"] is True,
        "source grant not preserved",
    )
    require(
        boundary["selected_candidate_bound_to_next_cycle_admission_grant"] is True,
        "selected candidate not bound to grant",
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
    require(
        boundary["next_cycle_admission_request_preserved"] is True,
        "admission request not preserved",
    )
    require(
        boundary["next_cycle_admission_grant_preserved"] is True,
        "admission grant not preserved",
    )
    require(boundary["next_cycle_start_receipt_only"] is True, "start-receipt-only boundary missing")
    require(boundary["next_cycle_admission_requested"] is True, "admission request missing")
    require(boundary["next_cycle_admission_granted"] is True, "admission grant missing")
    require(boundary["next_cycle_started"] is True, "next cycle not started")
    require(boundary["next_cycle_cycle_closed"] is False, "next cycle closed early")

    record = receipt["next_cycle_start_receipt"]
    require(record["memory_overwrite_preserved"] is True, "start lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "start lost memory closeout")
    require(record["truth_authority_preserved"] is True, "start lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "start lost truth closeout")
    require(record["blocker_release_preserved"] is True, "start lost blocker release")
    require(
        record["blocker_release_cycle_closed_preserved"] is True,
        "start lost blocker release closeout",
    )
    require(record["next_cycle_admission_requested"] is True, "start lost admission request")
    require(record["next_cycle_admission_granted"] is True, "start lost admission grant")
    require(record["next_cycle_started"] is True, "start record did not start cycle")
    require(record["next_cycle_cycle_closed"] is False, "start record closed cycle")
    require(record["source_blocker_release_authorization_request_digest"], "request digest not preserved")

    pre_started = dict(source)
    pre_started_boundary = dict(pre_started["boundary"])
    pre_started_boundary["next_cycle_started"] = True
    pre_started["boundary"] = pre_started_boundary
    blocked_started = build_next_cycle_start_receipt(next_cycle_admission_grant=pre_started).to_dict()
    require(
        blocked_started["status"] == "PLANOS_NEXT_CYCLE_START_RECEIPT_BLOCKED",
        "pre-started source not blocked",
    )
    require(
        "source_boundary_next_cycle_started_promoted" in blocked_started["blockers"],
        "pre-start boundary blocker missing",
    )

    record_started = dict(source)
    started_record = dict(record_started["next_cycle_admission_grant"])
    started_record["next_cycle_started"] = True
    record_started["next_cycle_admission_grant"] = started_record
    blocked_record = build_next_cycle_start_receipt(next_cycle_admission_grant=record_started).to_dict()
    require(
        blocked_record["status"] == "PLANOS_NEXT_CYCLE_START_RECEIPT_BLOCKED",
        "pre-started source record not blocked",
    )
    require(
        "source_record_next_cycle_started_promoted" in blocked_record["blockers"],
        "pre-start record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["next_cycle_admission_grant"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["next_cycle_admission_grant"] = mismatch_record
    blocked_mismatch = build_next_cycle_start_receipt(next_cycle_admission_grant=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_NEXT_CYCLE_START_RECEIPT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_next_cycle_admission_grant_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_next_cycle_start_receipt_v0_62.py"
    formal = ROOT / "formal/KUOS/PlanOS/NextCycleStartReceiptV0_62.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_62.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_NEXT_CYCLE_START_RECEIPT_v0_62.md"
    manifest_path = ROOT / "manifests/kuuos_planos_next_cycle_start_receipt_v0_62.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_next_cycle_start_receipt",
        "PLANOS_NEXT_CYCLE_START_RECEIPT_READY",
        "next_cycle_start_receipt_only",
        "next_cycle_started",
        "next_cycle_cycle_closed",
    ))
    require_tokens(formal, (
        "NextCycleStartReceiptSurface",
        "NextCycleStartReceiptBoundary",
        "PlanOSNextCycleStartReceiptBridge",
        "source_grant_authorizes_admission_but_does_not_start_cycle",
        "start_receipt_binds_candidate_and_preserves_prior_closeouts",
        "receipt_starts_next_cycle_without_closing_it",
        "boundary_is_next_cycle_start_receipt_only",
        "history_appends_one_next_cycle_start_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.NextCycleStartReceiptV0_62",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.NextCycleStartReceiptV0_62",))
    require_tokens(docs, (
        "PlanOS Next-Cycle Start Receipt v0.62",
        "next cycle start receipt only = true",
        "next cycle started = true",
        "next cycle cycle closed = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_next_cycle_start_receipt_v0_62.py",
        "v0.1-v0.62",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v062",))

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
    for field, value in manifest["open"].items():
        require(value is False, f"open boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS next-cycle start receipt v0.62 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
