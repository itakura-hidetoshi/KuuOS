#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_memory_overwrite_receipt_v0_50 import _ready_memory_overwrite_grant
from runtime.kuuos_planos_memory_overwrite_receipt_v0_50 import build_memory_overwrite_receipt
from runtime.kuuos_planos_memory_overwrite_closeout_receipt_v0_51 import SOURCE_VERSION, VERSION, build_memory_overwrite_closeout_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_memory_overwrite_receipt() -> dict:
    source = _ready_memory_overwrite_grant()
    return build_memory_overwrite_receipt(memory_overwrite_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_memory_overwrite_receipt()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_memory_overwrite_closeout_receipt(memory_overwrite_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_READY", f"closeout blocked: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_preserved"] is True, "memory overwrite not preserved")
    require(receipt["boundary"]["memory_overwrite_closeout_receipt_only"] is True, "closeout-only boundary missing")
    require(receipt["boundary"]["cycle_closed"] is True, "cycle not closed")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["memory_overwrite_closeout_receipt"]
    require(record["memory_overwrite_preserved"] is True, "record missing memory preservation")
    require(record["cycle_closed"] is True, "record missing cycle close")
    require(record["truth_authority_ready"] is False, "record leaked truth readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["truth_authority_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_memory_overwrite_closeout_receipt(memory_overwrite_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_BLOCKED", "truth-promoted source not blocked")
    require("source_boundary_truth_authority_granted_promoted" in blocked["blockers"], "truth blocker missing")

    missing_overwrite = dict(source)
    boundary2 = dict(missing_overwrite["boundary"])
    boundary2["memory_overwrite_granted"] = False
    missing_overwrite["boundary"] = boundary2
    blocked_overwrite = build_memory_overwrite_closeout_receipt(memory_overwrite_receipt=missing_overwrite).to_dict()
    require(blocked_overwrite["status"] == "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_BLOCKED", "missing memory overwrite not blocked")
    require("source_boundary_memory_overwrite_granted_missing" in blocked_overwrite["blockers"], "missing memory overwrite blocker missing")

    mismatch = dict(source)
    source_record = dict(mismatch["memory_overwrite_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["memory_overwrite_receipt"] = source_record
    blocked_mismatch = build_memory_overwrite_closeout_receipt(memory_overwrite_receipt=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_BLOCKED", "mismatch not blocked")
    require("selected_candidate_digest_source_receipt_mismatch" in blocked_mismatch["blockers"], "digest mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_memory_overwrite_closeout_receipt_v0_51.py"
    formal = ROOT / "formal/KUOS/PlanOS/MemoryOverwriteCloseoutReceiptV0_51.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_51.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_v0_51.md"
    manifest_path = ROOT / "manifests/kuuos_planos_memory_overwrite_closeout_receipt_v0_51.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_memory_overwrite_closeout_receipt",
        "PLANOS_MEMORY_OVERWRITE_CLOSEOUT_RECEIPT_READY",
        "memory_overwrite_closeout_receipt_only",
        "cycle_closed",
        "truth_authority_granted",
    ))
    require_tokens(formal, (
        "MemoryOverwriteCloseoutReceiptSurface",
        "MemoryOverwriteCloseoutReceiptBoundary",
        "PlanOSMemoryOverwriteCloseoutReceiptBridge",
        "source_receipt_records_memory_overwrite_and_keeps_truth_and_release_closed",
        "closeout_binds_candidate_and_closes_memory_cycle_without_new_authority",
        "boundary_is_memory_overwrite_closeout_receipt_only",
        "history_appends_one_closeout_receipt",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.MemoryOverwriteCloseoutReceiptV0_51",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MemoryOverwriteCloseoutReceiptV0_51",))
    require_tokens(docs, (
        "PlanOS Memory Overwrite Closeout Receipt v0.51",
        "memory overwrite closeout receipt only = true",
        "cycle closed = true",
        "truth authority granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_memory_overwrite_closeout_receipt_v0_51.py",
        "v0.1-v0.51",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v051",))

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
    print("PlanOS memory overwrite closeout receipt v0.51 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
