#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_materialization_authorization_request_receipt_v0_34 import _ready_authorization_request
from runtime.kuuos_planos_materialization_authorization_request_receipt_v0_34 import build_materialization_authorization_request_receipt
from runtime.kuuos_planos_materialization_authorization_grant_v0_35 import SOURCE_VERSION, VERSION, build_materialization_authorization_grant

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_materialization_authorization_grant_v0_35"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_request_receipt() -> dict:
    source = _ready_authorization_request()
    return build_materialization_authorization_request_receipt(authorization_request_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_request_receipt()
    require(source["version"] == SOURCE_VERSION, "source request receipt version mismatch")
    require("materialization_authorization_request_receipt" in source, "source request receipt missing")
    grant = build_materialization_authorization_grant(request_receipt=source).to_dict()
    require(grant["version"] == VERSION, "runtime version mismatch")
    require(grant["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_READY", f"grant status mismatch: {grant.get('blockers')}")
    require(grant["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(grant["boundary"]["materialization_authorization_grant_only"] is True, "grant-only boundary missing")
    require(grant["boundary"]["materialization_authorization_granted"] is True, "authorization not granted")
    require(grant["boundary"]["materialization_executed"] is False, "materialization executed")
    require(grant["boundary"]["execution_granted"] is False, "execution promoted")
    require(grant["materialization_authorization_grant"]["materialization_authorization_granted"] is True, "grant record not authorized")
    require(grant["materialization_authorization_grant"]["materialization_executed"] is False, "grant execution leaked")

    executed = dict(source)
    boundary = dict(executed["boundary"])
    boundary["materialization_executed"] = True
    executed["boundary"] = boundary
    blocked = build_materialization_authorization_grant(request_receipt=executed).to_dict()
    require(blocked["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_BLOCKED", "executed source not blocked")
    require("source_boundary_materialization_executed_promoted" in blocked["blockers"], "execution promotion blocker missing")

    pre_promoted = dict(source)
    record = dict(pre_promoted["materialization_authorization_request_receipt"])
    record["materialization_authorization_granted"] = True
    pre_promoted["materialization_authorization_request_receipt"] = record
    blocked_record = build_materialization_authorization_grant(request_receipt=pre_promoted).to_dict()
    require(blocked_record["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_BLOCKED", "pre-promoted grant record not blocked")
    require("source_record_materialization_authorization_granted_pre_promoted" in blocked_record["blockers"], "pre-promotion blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_grant_v0_35.py"
    source_runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_request_receipt_v0_34.py"
    formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationGrantV0_35.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationRequestReceiptV0_34.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_35.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_v0_35.md"
    manifest_path = ROOT / "manifests/kuuos_planos_materialization_authorization_grant_v0_35.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_materialization_authorization_grant", "PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_READY", "PLANOS_MATERIALIZATION_AUTHORIZATION_GRANT_BLOCKED", "materialization_authorization_grant", "materialization_authorization_grant_only", "materialization_authorization_granted", "materialization_executed", "execution_granted"))
    require_tokens(formal, ("MaterializationAuthorizationGrantSurface", "MaterializationAuthorizationGrantBoundary", "PlanOSMaterializationAuthorizationGrantBridge", "source_request_receipt_remains_receipt_only", "grant_binds_selected_candidate_to_request_receipt", "grant_authorizes_materialization_but_not_execution_activation_or_truth", "boundary_blocks_materialization_execution_commit_memory_and_blocker_release", "history_appends_one_materialization_authorization_grant_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSMaterializationAuthorizationRequestReceiptBridge", "receipt_binds_selected_candidate_to_authorization_request"))
    require_tokens(formal_root, ("KUOS.PlanOS.MaterializationAuthorizationGrantV0_35",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MaterializationAuthorizationGrantV0_35",))
    require_tokens(docs, ("PlanOS Materialization Authorization Grant v0.35", "selected candidate bound to request receipt = true", "materialization authorization grant only = true", "materialization authorization granted = true", "materialization executed = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_materialization_authorization_grant_v0_35.py", "v0.1-v0.35"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v035",))

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
    print("PlanOS materialization authorization grant v0.35 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
