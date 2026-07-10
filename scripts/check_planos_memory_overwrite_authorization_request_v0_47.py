#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_external_commit_receipt_v0_46 import _ready_external_commit_grant
from runtime.kuuos_planos_external_commit_receipt_v0_46 import build_external_commit_receipt
from runtime.kuuos_planos_memory_overwrite_authorization_request_v0_47 import SOURCE_VERSION, VERSION, build_memory_overwrite_authorization_request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_memory_overwrite_authorization_request_v0_47"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_external_commit_receipt() -> dict:
    source = _ready_external_commit_grant()
    return build_external_commit_receipt(external_commit_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_external_commit_receipt()
    require(source["version"] == SOURCE_VERSION, "source external commit receipt version mismatch")
    require("external_commit_receipt" in source, "source external commit receipt missing")
    receipt = build_memory_overwrite_authorization_request(external_commit_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY", f"request status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["external_commit_granted"] is True, "external commit not preserved")
    require(receipt["boundary"]["memory_overwrite_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["memory_overwrite_authorization_requested"] is True, "memory overwrite request missing")
    require(receipt["boundary"]["memory_overwrite_authorization_granted"] is False, "memory overwrite authorization granted too early")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["memory_overwrite_authorization_request"]["memory_overwrite_authorization_requested"] is True, "request record missing request")
    require(receipt["memory_overwrite_authorization_request"]["memory_overwrite_authorization_granted"] is False, "request record granted authorization")
    require(receipt["memory_overwrite_authorization_request"]["memory_overwrite_ready"] is False, "request leaked memory readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["memory_overwrite_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_memory_overwrite_authorization_request(external_commit_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "memory-promoted source not blocked")
    require("source_boundary_memory_overwrite_granted_promoted" in blocked["blockers"], "memory promotion blocker missing")

    missing_commit = dict(source)
    boundary2 = dict(missing_commit["boundary"])
    boundary2["external_commit_granted"] = False
    missing_commit["boundary"] = boundary2
    blocked_commit = build_memory_overwrite_authorization_request(external_commit_receipt=missing_commit).to_dict()
    require(blocked_commit["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "missing external commit not blocked")
    require("source_boundary_external_commit_granted_missing" in blocked_commit["blockers"], "missing external commit blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["external_commit_receipt"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["external_commit_receipt"] = record
    blocked_record = build_memory_overwrite_authorization_request(external_commit_receipt=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_external_commit_receipt_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_memory_overwrite_authorization_request_v0_47.py"
    source_runtime = ROOT / "runtime/kuuos_planos_external_commit_receipt_v0_46.py"
    formal = ROOT / "formal/KUOS/PlanOS/MemoryOverwriteAuthorizationRequestV0_47.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitReceiptV0_46.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_47.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_v0_47.md"
    manifest_path = ROOT / "manifests/kuuos_planos_memory_overwrite_authorization_request_v0_47.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_memory_overwrite_authorization_request", "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY", "PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_BLOCKED", "memory_overwrite_authorization_request", "memory_overwrite_authorization_request_only", "memory_overwrite_authorization_requested", "memory_overwrite_authorization_granted", "memory_overwrite_granted"))
    require_tokens(formal, ("MemoryOverwriteAuthorizationRequestSurface", "MemoryOverwriteAuthorizationRequestBoundary", "PlanOSMemoryOverwriteAuthorizationRequestBridge", "source_receipt_records_external_commit_but_not_memory_truth_or_blocker_release", "request_binds_candidate_and_preserves_external_commit_state", "request_asks_memory_overwrite_but_does_not_grant_overwrite_truth_or_blocker_release", "boundary_preserves_memory_overwrite_authorization_request_only", "history_appends_one_memory_overwrite_authorization_request_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExternalCommitReceiptBridge", "receipt_records_external_commit_but_not_memory_truth_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationRequestV0_47",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MemoryOverwriteAuthorizationRequestV0_47",))
    require_tokens(docs, ("PlanOS Memory Overwrite Authorization Request v0.47", "memory overwrite authorization request only = true", "memory overwrite authorization requested = true", "memory overwrite authorization granted = false", "memory overwrite granted = false", "truth authority granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_memory_overwrite_authorization_request_v0_47.py", "v0.1-v0.47"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v047",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for field, value in manifest["inputs"].items():
        require(value is True, f"input missing: {field}")
    for field, value in manifest["outputs"].items():
        require(value is True, f"output missing: {field}")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS memory overwrite authorization request v0.47 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
