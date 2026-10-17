#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_execution_authorization_request_v0_41 import _ready_selective_foresight_gate
from runtime.kuuos_planos_execution_authorization_request_v0_41 import build_execution_authorization_request
from runtime.kuuos_planos_execution_authorization_grant_v0_42 import SOURCE_VERSION, VERSION, build_execution_authorization_grant

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_execution_authorization_grant_v0_42"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_execution_request() -> dict:
    source = _ready_selective_foresight_gate()
    return build_execution_authorization_request(selective_foresight_gate=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_execution_request()
    require(source["version"] == SOURCE_VERSION, "source execution request version mismatch")
    require("execution_authorization_request" in source, "source execution request missing")
    receipt = build_execution_authorization_grant(execution_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXECUTION_AUTHORIZATION_GRANT_READY", f"grant status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["execution_authorization_grant_only"] is True, "grant-only boundary missing")
    require(receipt["boundary"]["execution_authorization_requested"] is True, "request flag missing")
    require(receipt["boundary"]["execution_authorization_granted"] is True, "authorization grant missing")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["execution_authorization_grant"]["execution_authorization_granted"] is True, "grant record missing authorization")
    require(receipt["execution_authorization_grant"]["execution_ready"] is False, "grant leaked execution readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["execution_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_execution_authorization_grant(execution_request=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXECUTION_AUTHORIZATION_GRANT_BLOCKED", "execution-promoted source not blocked")
    require("source_boundary_execution_granted_promoted" in blocked["blockers"], "execution promotion blocker missing")

    already_granted = dict(source)
    record = dict(already_granted["execution_authorization_request"])
    record["execution_authorization_granted"] = True
    already_granted["execution_authorization_request"] = record
    blocked_record = build_execution_authorization_grant(execution_request=already_granted).to_dict()
    require(blocked_record["status"] == "PLANOS_EXECUTION_AUTHORIZATION_GRANT_BLOCKED", "already granted record not blocked")
    require("source_record_execution_authorization_granted_promoted" in blocked_record["blockers"], "already-granted blocker missing")

    mismatch = dict(source)
    record2 = dict(mismatch["execution_authorization_request"])
    record2["selected_candidate_digest"] = "wrong-digest"
    mismatch["execution_authorization_request"] = record2
    blocked_mismatch = build_execution_authorization_grant(execution_request=mismatch).to_dict()
    require(blocked_mismatch["status"] == "PLANOS_EXECUTION_AUTHORIZATION_GRANT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_execution_request_mismatch" in blocked_mismatch["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_execution_authorization_grant_v0_42.py"
    source_runtime = ROOT / "runtime/kuuos_planos_execution_authorization_request_v0_41.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExecutionAuthorizationGrantV0_42.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExecutionAuthorizationRequestV0_41.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_42.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXECUTION_AUTHORIZATION_GRANT_v0_42.md"
    manifest_path = ROOT / "manifests/kuuos_planos_execution_authorization_grant_v0_42.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_execution_authorization_grant", "PLANOS_EXECUTION_AUTHORIZATION_GRANT_READY", "PLANOS_EXECUTION_AUTHORIZATION_GRANT_BLOCKED", "execution_authorization_grant", "execution_authorization_grant_only", "execution_authorization_granted", "execution_granted", "external_commit_granted"))
    require_tokens(formal, ("ExecutionAuthorizationGrantSurface", "ExecutionAuthorizationGrantBoundary", "PlanOSExecutionAuthorizationGrantBridge", "source_request_remains_request_only", "grant_binds_candidate_and_preserves_prerequisites", "grant_preserves_literature_grounded_execution_prerequisites", "grant_authorizes_execution_but_does_not_execute_or_commit", "history_appends_one_execution_authorization_grant_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExecutionAuthorizationRequestBridge", "request_does_not_grant_execution_truth_commit_memory_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExecutionAuthorizationGrantV0_42",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExecutionAuthorizationGrantV0_42",))
    require_tokens(docs, ("PlanOS Execution Authorization Grant v0.42", "execution authorization grant only = true", "execution authorization requested = true", "execution authorization granted = true", "execution granted = false", "truth authority granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_execution_authorization_grant_v0_42.py", "v0.1-v0.42"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v042",))

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
    print("PlanOS execution authorization grant v0.42 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
