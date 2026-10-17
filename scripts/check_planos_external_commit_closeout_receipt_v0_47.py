#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_external_commit_receipt_v0_46 import _ready_external_commit_grant
from runtime.kuuos_planos_external_commit_receipt_v0_46 import build_external_commit_receipt
from runtime.kuuos_planos_external_commit_closeout_receipt_v0_47 import (
    SOURCE_VERSION,
    VERSION,
    build_external_commit_closeout_receipt,
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


def _ready_external_commit_receipt() -> dict:
    grant = _ready_external_commit_grant()
    return build_external_commit_receipt(external_commit_grant=grant).to_dict()


def _exercise_runtime() -> None:
    source = _ready_external_commit_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    closeout = build_external_commit_closeout_receipt(external_commit_receipt=source).to_dict()
    require(closeout["version"] == VERSION, "runtime version mismatch")
    require(closeout["status"] == "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_READY", f"closeout blocked: {closeout.get('blockers')}")
    require(closeout["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(closeout["boundary"]["external_commit_preserved"] is True, "external commit not preserved")
    require(closeout["boundary"]["external_commit_closeout_receipt_only"] is True, "closeout-only boundary missing")
    require(closeout["boundary"]["cycle_closed"] is True, "cycle not closed")
    require(closeout["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(closeout["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(closeout["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = closeout["external_commit_closeout_receipt"]
    require(record["external_commit_preserved"] is True, "record lost external commit")
    require(record["cycle_closed"] is True, "record did not close cycle")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["memory_overwrite_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_external_commit_closeout_receipt(external_commit_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_BLOCKED", "promoted source not blocked")
    require("source_boundary_memory_overwrite_granted_promoted" in blocked["blockers"], "memory blocker missing")

    mismatch = dict(source)
    source_record = dict(mismatch["external_commit_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["external_commit_receipt"] = source_record
    blocked_mismatch = build_external_commit_closeout_receipt(external_commit_receipt=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_BLOCKED", "mismatch not blocked")
    require("selected_candidate_digest_source_receipt_mismatch" in blocked_mismatch["blockers"], "digest mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_external_commit_closeout_receipt_v0_47.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitCloseoutReceiptV0_47.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_47.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_v0_47.md"
    manifest_path = ROOT / "manifests/kuuos_planos_external_commit_closeout_receipt_v0_47.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_external_commit_closeout_receipt",
        "PLANOS_EXTERNAL_COMMIT_CLOSEOUT_RECEIPT_READY",
        "external_commit_closeout_receipt_only",
        "cycle_closed",
        "memory_overwrite_granted",
    ))
    require_tokens(formal, (
        "ExternalCommitCloseoutReceiptSurface",
        "ExternalCommitCloseoutReceiptBoundary",
        "PlanOSExternalCommitCloseoutReceiptBridge",
        "source_receipt_records_external_commit_and_keeps_authority_closed",
        "closeout_binds_candidate_and_closes_cycle_without_new_authority",
        "boundary_is_external_commit_closeout_receipt_only",
        "history_appends_one_closeout_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.ExternalCommitCloseoutReceiptV0_47",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExternalCommitCloseoutReceiptV0_47",))
    require_tokens(docs, (
        "PlanOS External Commit Closeout Receipt v0.47",
        "external commit preserved = true",
        "cycle closed = true",
        "memory overwrite granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_external_commit_closeout_receipt_v0_47.py",
        "v0.1-v0.47",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v047",))

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
    print("PlanOS external commit closeout receipt v0.47 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
