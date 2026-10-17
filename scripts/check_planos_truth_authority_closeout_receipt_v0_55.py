#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_truth_authority_receipt_v0_54 import _ready_truth_authority_grant
from runtime.kuuos_planos_truth_authority_receipt_v0_54 import build_truth_authority_receipt
from runtime.kuuos_planos_truth_authority_closeout_receipt_v0_55 import (
    SOURCE_VERSION,
    VERSION,
    build_truth_authority_closeout_receipt,
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


def _ready_truth_authority_receipt() -> dict:
    source = _ready_truth_authority_grant()
    return build_truth_authority_receipt(truth_authority_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_truth_authority_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_truth_authority_closeout_receipt(truth_authority_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(
        receipt["status"] == "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_READY",
        f"closeout blocked: {receipt.get('blockers')}",
    )
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_preserved"] is True, "memory closeout not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "memory cycle closeout not preserved")
    require(
        receipt["boundary"]["truth_authority_authorization_grant_preserved"] is True,
        "truth authorization grant not preserved",
    )
    require(receipt["boundary"]["truth_authority_preserved"] is True, "truth authority not preserved")
    require(
        receipt["boundary"]["truth_authority_closeout_receipt_only"] is True,
        "truth closeout-only boundary missing",
    )
    require(receipt["boundary"]["truth_authority_cycle_closed"] is True, "truth cycle not closed")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["truth_authority_closeout_receipt"]
    require(record["memory_overwrite_preserved"] is True, "record lost memory overwrite")
    require(record["memory_overwrite_closeout_preserved"] is True, "record lost memory closeout")
    require(record["cycle_closed_preserved"] is True, "record lost memory cycle closeout")
    require(record["truth_authority_preserved"] is True, "record lost truth authority")
    require(record["truth_authority_cycle_closed"] is True, "record missing truth cycle closeout")
    require(record["blocker_release_ready"] is False, "record released blockers")

    missing_truth = dict(source)
    boundary = dict(missing_truth["boundary"])
    boundary["truth_authority_granted"] = False
    missing_truth["boundary"] = boundary
    blocked_truth = build_truth_authority_closeout_receipt(truth_authority_receipt=missing_truth).to_dict()
    require(
        blocked_truth["status"] == "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_BLOCKED",
        "missing truth authority not blocked",
    )
    require(
        "source_boundary_truth_authority_granted_missing" in blocked_truth["blockers"],
        "missing truth blocker missing",
    )

    release_promoted = dict(source)
    boundary2 = dict(release_promoted["boundary"])
    boundary2["blocker_release_granted"] = True
    release_promoted["boundary"] = boundary2
    blocked_release = build_truth_authority_closeout_receipt(truth_authority_receipt=release_promoted).to_dict()
    require(
        blocked_release["status"] == "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_BLOCKED",
        "blocker-release source not blocked",
    )
    require(
        "source_boundary_blocker_release_granted_promoted" in blocked_release["blockers"],
        "blocker release blocker missing",
    )

    mismatch = dict(source)
    source_record = dict(mismatch["truth_authority_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["truth_authority_receipt"] = source_record
    blocked_mismatch = build_truth_authority_closeout_receipt(truth_authority_receipt=mismatch).to_dict()
    require(
        blocked_mismatch["status"] == "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_BLOCKED",
        "mismatch not blocked",
    )
    require(
        "selected_candidate_digest_source_receipt_mismatch" in blocked_mismatch["blockers"],
        "digest mismatch blocker missing",
    )


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_truth_authority_closeout_receipt_v0_55.py"
    formal = ROOT / "formal/KUOS/PlanOS/TruthAuthorityCloseoutReceiptV0_55.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_55.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_v0_55.md"
    manifest_path = ROOT / "manifests/kuuos_planos_truth_authority_closeout_receipt_v0_55.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_truth_authority_closeout_receipt",
        "PLANOS_TRUTH_AUTHORITY_CLOSEOUT_RECEIPT_READY",
        "truth_authority_closeout_receipt_only",
        "truth_authority_cycle_closed",
        "blocker_release_granted",
    ))
    require_tokens(formal, (
        "TruthAuthorityCloseoutReceiptSurface",
        "TruthAuthorityCloseoutReceiptBoundary",
        "PlanOSTruthAuthorityCloseoutReceiptBridge",
        "source_receipt_records_truth_and_keeps_release_closed",
        "closeout_binds_candidate_and_closes_truth_cycle_without_release",
        "boundary_is_truth_authority_closeout_receipt_only",
        "history_appends_one_truth_authority_closeout_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.TruthAuthorityCloseoutReceiptV0_55",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.TruthAuthorityCloseoutReceiptV0_55",))
    require_tokens(docs, (
        "PlanOS Truth Authority Closeout Receipt v0.55",
        "truth authority closeout receipt only = true",
        "truth authority preserved = true",
        "truth authority cycle closed = true",
        "blocker release granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_truth_authority_closeout_receipt_v0_55.py",
        "v0.1-v0.55",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v055",))

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
    print("PlanOS truth authority closeout receipt v0.55 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
