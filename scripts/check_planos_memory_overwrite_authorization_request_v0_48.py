#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_external_commit_closeout_receipt_v0_47 import _ready_external_commit_receipt
from runtime.kuuos_planos_external_commit_closeout_receipt_v0_47 import build_external_commit_closeout_receipt
from runtime.kuuos_planos_memory_overwrite_authorization_request_v0_48 import SOURCE_VERSION, VERSION, build_memory_overwrite_authorization_request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = VERSION


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_external_commit_closeout() -> dict:
    source = _ready_external_commit_receipt()
    return build_external_commit_closeout_receipt(external_commit_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_external_commit_closeout()
    require(source["version"] == SOURCE_VERSION, "source version mismatch")
    receipt = build_memory_overwrite_authorization_request(external_commit_closeout=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY", f"request blocked: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["external_commit_preserved"] is True, "external commit not preserved")
    require(receipt["boundary"]["cycle_closed_preserved"] is True, "cycle closeout not preserved")
    require(receipt["boundary"]["memory_overwrite_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["memory_overwrite_authorization_requested"] is True, "memory request missing")
    require(receipt["boundary"]["memory_overwrite_authorization_granted"] is False, "memory authorization granted too early")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    record = receipt["memory_overwrite_authorization_request"]
    require(record["memory_overwrite_authorization_requested"] is True, "record missing request")
    require(record["memory_overwrite_authorization_granted"] is False, "record granted authorization")
    require(record["memory_overwrite_ready"] is False, "record leaked memory readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["memory_overwrite_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_memory_overwrite_authorization_request(external_commit_closeout=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "memory-promoted source not blocked")
    require("source_boundary_memory_overwrite_granted_promoted" in blocked["blockers"], "memory blocker missing")

    missing_closeout = dict(source)
    boundary2 = dict(missing_closeout["boundary"])
    boundary2["cycle_closed"] = False
    missing_closeout["boundary"] = boundary2
    blocked_cycle = build_memory_overwrite_authorization_request(external_commit_closeout=missing_closeout).to_dict()
    require(blocked_cycle["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "missing closeout not blocked")
    require("source_boundary_cycle_closed_missing" in blocked_cycle["blockers"], "cycle closeout blocker missing")

    mismatch = dict(source)
    source_record = dict(mismatch["external_commit_closeout_receipt"])
    source_record["selected_candidate_digest"] = "wrong-digest"
    mismatch["external_commit_closeout_receipt"] = source_record
    blocked_mismatch = build_memory_overwrite_authorization_request(external_commit_closeout=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "mismatch not blocked")
    require("selected_candidate_digest_external_commit_closeout_mismatch" in blocked_mismatch["blockers"], "digest mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_memory_overwrite_authorization_request_v0_48.py"
    formal = ROOT / "formal/KUOS/PlanOS/MemoryOverwriteAuthorizationRequestV0_48.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_48.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_v0_48.md"
    manifest_path = ROOT / "manifests/kuuos_planos_memory_overwrite_authorization_request_v0_48.json"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, (
        "build_memory_overwrite_authorization_request",
        "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY",
        "memory_overwrite_authorization_request_only",
        "memory_overwrite_authorization_requested",
        "memory_overwrite_authorization_granted",
    ))
    require_tokens(formal, (
        "MemoryOverwriteAuthorizationRequestSurface",
        "MemoryOverwriteAuthorizationRequestBoundary",
        "PlanOSMemoryOverwriteAuthorizationRequestBridge",
        "source_closeout_preserves_external_commit_and_keeps_authority_closed",
        "request_binds_candidate_and_preserves_closeout_state",
        "request_asks_memory_overwrite_but_does_not_grant_overwrite_truth_or_blocker_release",
        "boundary_preserves_memory_overwrite_authorization_request_only",
        "history_appends_one_memory_overwrite_authorization_request_record",
        "digest_is_exact",
    ))
    require_tokens(formal_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationRequestV0_48",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationRequestV0_48",))
    require_tokens(docs, (
        "PlanOS Memory Overwrite Authorization Request v0.48",
        "memory overwrite authorization request only = true",
        "memory overwrite authorization requested = true",
        "memory overwrite authorization granted = false",
        "memory overwrite granted = false",
    ))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", (
        "check_planos_memory_overwrite_authorization_request_v0_48.py",
        "v0.1-v0.48",
    ))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v048",))

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
    print("PlanOS memory overwrite authorization request v0.48 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
