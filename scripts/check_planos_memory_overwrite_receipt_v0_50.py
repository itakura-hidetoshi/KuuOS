#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_memory_overwrite_authorization_grant_v0_49 import _ready_memory_overwrite_request
from runtime.kuuos_planos_memory_overwrite_authorization_grant_v0_49 import build_memory_overwrite_authorization_grant
from runtime.kuuos_planos_memory_overwrite_receipt_v0_50 import SOURCE_VERSION, VERSION, build_memory_overwrite_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_memory_overwrite_grant() -> dict:
    source = _ready_memory_overwrite_request()
    return build_memory_overwrite_authorization_grant(memory_overwrite_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_memory_overwrite_grant()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_memory_overwrite_receipt(memory_overwrite_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MEMORY_OVERWRITE_RECEIPT_READY", f"receipt blocked: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["memory_overwrite_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["memory_overwrite_authorization_granted"] is True, "authorization not preserved")
    require(receipt["boundary"]["memory_overwrite_granted"] is True, "memory overwrite not recorded")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["boundary"]["blocker_release_granted"] is False, "blocker release promoted")
    record = receipt["memory_overwrite_receipt"]
    require(record["memory_overwrite_granted"] is True, "receipt record missing memory overwrite")
    require(record["truth_authority_ready"] is False, "receipt leaked truth authority")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["memory_overwrite_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_memory_overwrite_receipt(memory_overwrite_grant=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MEMORY_OVERWRITE_RECEIPT_BLOCKED", "pre-overwritten source not blocked")
    require("source_boundary_memory_overwrite_granted_promoted" in blocked["blockers"], "pre-overwrite blocker missing")

    truth_promoted = dict(source)
    boundary2 = dict(truth_promoted["boundary"])
    boundary2["truth_authority_granted"] = True
    truth_promoted["boundary"] = boundary2
    blocked_truth = build_memory_overwrite_receipt(memory_overwrite_grant=truth_promoted).to_dict()
    require(blocked_truth["status"] == "PLANOS_MEMORY_OVERWRITE_RECEIPT_BLOCKED", "truth-promoted source not blocked")
    require("source_boundary_truth_authority_granted_promoted" in blocked_truth["blockers"], "truth blocker missing")

    mismatch = dict(source)
    grant_record = dict(mismatch["memory_overwrite_authorization_grant"])
    grant_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["memory_overwrite_authorization_grant"] = grant_record
    blocked_mismatch = build_memory_overwrite_receipt(memory_overwrite_grant=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_MEMORY_OVERWRITE_RECEIPT_BLOCKED", "mismatch not blocked")
    require("selected_candidate_digest_memory_overwrite_grant_mismatch" in blocked_mismatch["blockers"], "digest mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_memory_overwrite_receipt_v0_50.py"
    formal = ROOT / "formal/KUOS/PlanOS/MemoryOverwriteReceiptV0_50.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_50.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MEMORY_OVERWRITE_RECEIPT_v0_50.md"
    manifest_path = ROOT / "manifests/kuuos_planos_memory_overwrite_receipt_v0_50.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_memory_overwrite_receipt",
        "PLANOS_MEMORY_OVERWRITE_RECEIPT_READY",
        "memory_overwrite_receipt_only",
        "memory_overwrite_authorization_granted",
        "memory_overwrite_granted",
    ))
    require_tokens(formal, (
        "MemoryOverwriteReceiptSurface",
        "MemoryOverwriteReceiptBoundary",
        "PlanOSMemoryOverwriteReceiptBridge",
        "source_grant_authorizes_but_does_not_apply_memory",
        "receipt_binds_candidate_and_preserves_authorized_state",
        "receipt_records_memory_overwrite_but_not_truth_or_blocker_release",
        "boundary_preserves_memory_overwrite_receipt_only",
        "history_appends_one_memory_overwrite_receipt_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.MemoryOverwriteReceiptV0_50",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MemoryOverwriteReceiptV0_50",))
    require_tokens(docs, (
        "PlanOS Memory Overwrite Receipt v0.50",
        "memory overwrite receipt only = true",
        "memory overwrite authorization granted = true",
        "memory overwrite granted = true",
        "truth authority granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_memory_overwrite_receipt_v0_50.py",
        "v0.1-v0.50",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v050",))

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
    print("PlanOS memory overwrite receipt v0.50 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
