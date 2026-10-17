#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_execution_receipt_v0_43 import _ready_execution_grant
from runtime.kuuos_planos_execution_receipt_v0_43 import build_execution_receipt
from runtime.kuuos_planos_external_commit_authorization_request_v0_44 import SOURCE_VERSION, VERSION, build_external_commit_authorization_request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_external_commit_authorization_request_v0_44"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_execution_receipt() -> dict:
    source = _ready_execution_grant()
    return build_execution_receipt(execution_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_execution_receipt()
    require(source["version"] == SOURCE_VERSION, "source execution receipt version mismatch")
    require("execution_receipt" in source, "source execution receipt missing")
    receipt = build_external_commit_authorization_request(execution_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_READY", f"request status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["execution_granted"] is True, "execution not preserved")
    require(receipt["boundary"]["external_commit_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["external_commit_authorization_requested"] is True, "external commit request missing")
    require(receipt["boundary"]["external_commit_authorization_granted"] is False, "external commit authorization granted too early")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["external_commit_authorization_request"]["external_commit_authorization_requested"] is True, "request record missing request")
    require(receipt["external_commit_authorization_request"]["external_commit_authorization_granted"] is False, "request record granted authorization")
    require(receipt["external_commit_authorization_request"]["external_commit_ready"] is False, "request leaked external commit readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["external_commit_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_external_commit_authorization_request(execution_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_BLOCKED", "external-commit-promoted source not blocked")
    require("source_boundary_external_commit_granted_promoted" in blocked["blockers"], "external commit promotion blocker missing")

    missing_execution = dict(source)
    boundary2 = dict(missing_execution["boundary"])
    boundary2["execution_granted"] = False
    missing_execution["boundary"] = boundary2
    blocked_execution = build_external_commit_authorization_request(execution_receipt=missing_execution).to_dict()
    require(blocked_execution["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_BLOCKED", "missing execution not blocked")
    require("source_boundary_execution_granted_missing" in blocked_execution["blockers"], "missing execution blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["execution_receipt"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["execution_receipt"] = record
    blocked_record = build_external_commit_authorization_request(execution_receipt=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_execution_receipt_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_external_commit_authorization_request_v0_44.py"
    source_runtime = ROOT / "runtime/kuuos_planos_execution_receipt_v0_43.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitAuthorizationRequestV0_44.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExecutionReceiptV0_43.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_44.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_v0_44.md"
    manifest_path = ROOT / "manifests/kuuos_planos_external_commit_authorization_request_v0_44.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_external_commit_authorization_request", "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_READY", "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_REQUEST_BLOCKED", "external_commit_authorization_request", "external_commit_authorization_request_only", "external_commit_authorization_requested", "external_commit_authorization_granted", "external_commit_granted"))
    require_tokens(formal, ("ExternalCommitAuthorizationRequestSurface", "ExternalCommitAuthorizationRequestBoundary", "PlanOSExternalCommitAuthorizationRequestBridge", "source_receipt_records_execution_but_not_commit_memory_truth_or_blocker_release", "request_binds_candidate_and_preserves_execution_receipt_state", "request_asks_external_commit_but_does_not_grant_commit_memory_truth_or_blocker_release", "boundary_preserves_external_commit_authorization_request_only", "history_appends_one_external_commit_authorization_request_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExecutionReceiptBridge", "receipt_records_execution_but_not_commit_memory_truth_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExternalCommitAuthorizationRequestV0_44",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExternalCommitAuthorizationRequestV0_44",))
    require_tokens(docs, ("PlanOS External Commit Authorization Request v0.44", "external commit authorization request only = true", "external commit authorization requested = true", "external commit authorization granted = false", "external commit granted = false", "memory overwrite granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_external_commit_authorization_request_v0_44.py", "v0.1-v0.44"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v044",))

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
    print("PlanOS external commit authorization request v0.44 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
