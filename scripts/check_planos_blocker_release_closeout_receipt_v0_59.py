#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_blocker_release_receipt_v0_58 import _ready_blocker_release_grant
from runtime.kuuos_planos_blocker_release_receipt_v0_58 import build_blocker_release_receipt
from runtime.kuuos_planos_blocker_release_closeout_receipt_v0_59 import (
    SOURCE_VERSION,
    VERSION,
    build_blocker_release_closeout_receipt,
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


def _ready_blocker_release_receipt() -> dict:
    source = _ready_blocker_release_grant()
    return build_blocker_release_receipt(blocker_release_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_blocker_release_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_blocker_release_closeout_receipt(blocker_release_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_READY",
        f"closeout blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    boundary = receipt["boundary"]
    require(boundary["closeout_owned_by_plan_os"] is True, "closeout owner missing")
    require(boundary["source_blocker_release_receipt_preserved"] is True, "source receipt not preserved")
    require(
        boundary["selected_candidate_bound_to_blocker_release_receipt"] is True,
        "selected candidate not bound to receipt",
    )
    require(boundary["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(boundary["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(boundary["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(boundary["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        boundary["truth_authority_cycle_closed_preserved"] is True,
        "truth authority cycle closeout not preserved",
    )
    require(
        boundary["blocker_release_authorization_request_preserved"] is True,
        "blocker release request not preserved",
    )
    require(
        boundary["blocker_release_authorization_grant_preserved"] is True,
        "blocker release grant not preserved",
    )
    require(boundary["blocker_release_preserved"] is True, "blocker release not preserved")
    require(
        boundary["blocker_release_closeout_receipt_only"] is True,
        "closeout-only boundary missing",
    )
    require(boundary["blocker_release_cycle_closed"] is True, "blocker release cycle not closed")
    require(boundary["next_cycle_admission_requested"] is False, "next cycle opened early")

    record = receipt["blocker_release_closeout_receipt"]
    require(record["memory_overwrite_preserved"] is True, "closeout lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "closeout lost memory closeout")
    require(record["truth_authority_preserved"] is True, "closeout lost truth authority")
    require(record["truth_authority_cycle_closed_preserved"] is True, "closeout lost truth closeout")
    require(
        record["blocker_release_authorization_grant_preserved"] is True,
        "closeout lost blocker release authorization grant",
    )
    require(record["blocker_release_preserved"] is True, "closeout lost blocker release")
    require(record["blocker_release_cycle_closed"] is True, "closeout record did not close cycle")
    require(record["next_cycle_admission_ready"] is False, "closeout opened next cycle")

    preclosed = dict(source)
    preclosed_boundary = dict(preclosed["boundary"])
    preclosed_boundary["blocker_release_cycle_closed"] = True
    preclosed["boundary"] = preclosed_boundary
    blocked_preclosed = build_blocker_release_closeout_receipt(blocker_release_receipt=preclosed).to_dict()
    require(
        blocked_preclosed["status"] == "PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_BLOCKED",
        "preclosed source not blocked",
    )
    require(
        "source_boundary_blocker_release_cycle_closed_promoted" in blocked_preclosed["blockers"],
        "preclosed boundary blocker missing",
    )

    record_preclosed = dict(source)
    source_record = dict(record_preclosed["blocker_release_receipt"])
    source_record["blocker_release_cycle_closed"] = True
    record_preclosed["blocker_release_receipt"] = source_record
    blocked_record = build_blocker_release_closeout_receipt(blocker_release_receipt=record_preclosed).to_dict()
    require(
        blocked_record["status"] == "PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_BLOCKED",
        "preclosed source record not blocked",
    )
    require(
        "source_record_blocker_release_cycle_closed_promoted" in blocked_record["blockers"],
        "preclosed source record blocker missing",
    )

    mismatch = dict(source)
    mismatch_record = dict(mismatch["blocker_release_receipt"])
    mismatch_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["blocker_release_receipt"] = mismatch_record
    blocked_mismatch = build_blocker_release_closeout_receipt(blocker_release_receipt=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_blocker_release_receipt_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_blocker_release_closeout_receipt_v0_59.py"
    formal = ROOT / "formal/KUOS/PlanOS/BlockerReleaseCloseoutReceiptV0_59.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_59.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_v0_59.md"
    manifest_path = ROOT / "manifests/kuuos_planos_blocker_release_closeout_receipt_v0_59.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_blocker_release_closeout_receipt",
        "PLANOS_BLOCKER_RELEASE_CLOSEOUT_RECEIPT_READY",
        "blocker_release_closeout_receipt_only",
        "blocker_release_cycle_closed",
        "next_cycle_admission_requested",
    ))
    require_tokens(formal, (
        "BlockerReleaseCloseoutSurface",
        "BlockerReleaseCloseoutBoundary",
        "PlanOSBlockerReleaseCloseoutBridge",
        "source_receipt_records_release_but_keeps_cycle_open",
        "closeout_binds_candidate_and_preserves_release_state",
        "closeout_closes_release_cycle_without_opening_next_admission",
        "boundary_preserves_blocker_release_closeout_only",
        "history_appends_one_blocker_release_closeout_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.BlockerReleaseCloseoutReceiptV0_59",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.BlockerReleaseCloseoutReceiptV0_59",))
    require_tokens(docs, (
        "PlanOS Blocker Release Closeout Receipt v0.59",
        "blocker release closeout receipt only = true",
        "blocker release cycle closed = true",
        "next cycle admission requested = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_blocker_release_closeout_receipt_v0_59.py",
        "v0.1-v0.59",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v059",))

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
    print("PlanOS blocker release closeout receipt v0.59 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
