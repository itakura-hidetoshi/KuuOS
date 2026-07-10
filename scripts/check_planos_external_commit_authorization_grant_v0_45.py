#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_external_commit_authorization_request_v0_44 import _ready_execution_receipt
from runtime.kuuos_planos_external_commit_authorization_request_v0_44 import build_external_commit_authorization_request
from runtime.kuuos_planos_external_commit_authorization_grant_v0_45 import SOURCE_VERSION, VERSION, build_external_commit_authorization_grant

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_external_commit_authorization_grant_v0_45"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_external_commit_request() -> dict:
    source = _ready_execution_receipt()
    return build_external_commit_authorization_request(execution_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_external_commit_request()
    require(source["version"] == SOURCE_VERSION, "source external commit request version mismatch")
    require("external_commit_authorization_request" in source, "source external commit request missing")
    receipt = build_external_commit_authorization_grant(external_commit_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_READY", f"grant status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["execution_granted"] is True, "execution not preserved")
    require(receipt["boundary"]["external_commit_authorization_grant_only"] is True, "grant-only boundary missing")
    require(receipt["boundary"]["external_commit_authorization_requested"] is True, "external commit request missing")
    require(receipt["boundary"]["external_commit_authorization_granted"] is True, "external commit authorization grant missing")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["external_commit_authorization_grant"]["external_commit_authorization_granted"] is True, "grant record missing authorization")
    require(receipt["external_commit_authorization_grant"]["external_commit_ready"] is False, "grant leaked external commit readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["external_commit_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_external_commit_authorization_grant(external_commit_request=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_BLOCKED", "external-commit-promoted source not blocked")
    require("source_boundary_external_commit_granted_promoted" in blocked["blockers"], "external commit promotion blocker missing")

    already_granted = dict(source)
    record = dict(already_granted["external_commit_authorization_request"])
    record["external_commit_authorization_granted"] = True
    already_granted["external_commit_authorization_request"] = record
    blocked_record = build_external_commit_authorization_grant(external_commit_request=already_granted).to_dict()
    require(blocked_record["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_BLOCKED", "already-granted record not blocked")
    require("source_record_external_commit_authorization_granted_promoted" in blocked_record["blockers"], "already-granted blocker missing")

    mismatch = dict(source)
    record2 = dict(mismatch["external_commit_authorization_request"])
    record2["selected_candidate_digest"] = "wrong-digest"
    mismatch["external_commit_authorization_request"] = record2
    blocked_mismatch = build_external_commit_authorization_grant(external_commit_request=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_external_commit_request_mismatch" in blocked_mismatch["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_external_commit_authorization_grant_v0_45.py"
    source_runtime = ROOT / "runtime/kuuos_planos_external_commit_authorization_request_v0_44.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitAuthorizationGrantV0_45.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExternalCommitAuthorizationRequestV0_44.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_45.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_v0_45.md"
    manifest_path = ROOT / "manifests/kuuos_planos_external_commit_authorization_grant_v0_45.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_external_commit_authorization_grant", "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_READY", "PLANOS_EXTERNAL_COMMIT_AUTHORIZATION_GRANT_BLOCKED", "external_commit_authorization_grant", "external_commit_authorization_grant_only", "external_commit_authorization_granted", "external_commit_granted", "memory_overwrite_granted"))
    require_tokens(formal, ("ExternalCommitAuthorizationGrantSurface", "ExternalCommitAuthorizationGrantBoundary", "PlanOSExternalCommitAuthorizationGrantBridge", "source_request_asks_but_does_not_grant_external_commit", "grant_binds_candidate_and_preserves_execution_state", "grant_authorizes_external_commit_but_does_not_commit_memory_truth_or_blocker_release", "boundary_preserves_external_commit_authorization_grant_only", "history_appends_one_external_commit_authorization_grant_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExternalCommitAuthorizationRequestBridge", "request_asks_external_commit_but_does_not_grant_commit_memory_truth_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExternalCommitAuthorizationGrantV0_45",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExternalCommitAuthorizationGrantV0_45",))
    require_tokens(docs, ("PlanOS External Commit Authorization Grant v0.45", "external commit authorization grant only = true", "external commit authorization requested = true", "external commit authorization granted = true", "external commit granted = false", "memory overwrite granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_external_commit_authorization_grant_v0_45.py", "v0.1-v0.45"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v045",))

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
    print("PlanOS external commit authorization grant v0.45 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
