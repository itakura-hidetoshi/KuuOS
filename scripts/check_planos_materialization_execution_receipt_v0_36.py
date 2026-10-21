#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_materialization_authorization_grant_v0_35 import _ready_request_receipt
from runtime.kuuos_planos_materialization_authorization_grant_v0_35 import build_materialization_authorization_grant
from runtime.kuuos_planos_materialization_execution_receipt_v0_36 import SOURCE_VERSION, VERSION, build_materialization_execution_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_materialization_execution_receipt_v0_36"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_authorization_grant() -> dict:
    source = _ready_request_receipt()
    return build_materialization_authorization_grant(request_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_authorization_grant()
    require(source["version"] == SOURCE_VERSION, "source authorization grant version mismatch")
    require("materialization_authorization_grant" in source, "source authorization grant missing")
    receipt = build_materialization_execution_receipt(authorization_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_READY", f"receipt status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["materialization_execution_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["materialization_authorization_granted"] is True, "authorization not preserved")
    require(receipt["boundary"]["materialization_executed"] is True, "materialization not recorded")
    require(receipt["boundary"]["activation_authorization_granted"] is False, "activation promoted")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["materialization_execution_receipt"]["materialization_executed"] is True, "receipt execution not recorded")
    require(receipt["materialization_execution_receipt"]["activation_authorization_granted"] is False, "receipt activation leaked")

    pre_executed = dict(source)
    boundary = dict(pre_executed["boundary"])
    boundary["materialization_executed"] = True
    pre_executed["boundary"] = boundary
    blocked = build_materialization_execution_receipt(authorization_grant=pre_executed).to_dict()
    require(blocked["status"] == "PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_BLOCKED", "pre-executed source not blocked")
    require("source_boundary_materialization_executed_promoted" in blocked["blockers"], "pre-executed blocker missing")

    activation_promoted = dict(source)
    record = dict(activation_promoted["materialization_authorization_grant"])
    record["activation_authorization_granted"] = True
    activation_promoted["materialization_authorization_grant"] = record
    blocked_record = build_materialization_execution_receipt(authorization_grant=activation_promoted).to_dict()
    require(blocked_record["status"] == "PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_BLOCKED", "activation-promoted record not blocked")
    require("source_record_activation_authorization_granted_promoted" in blocked_record["blockers"], "activation blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_materialization_execution_receipt_v0_36.py"
    source_runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_grant_v0_35.py"
    formal = ROOT / "formal/KUOS/PlanOS/MaterializationExecutionReceiptV0_36.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationGrantV0_35.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_36.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_v0_36.md"
    manifest_path = ROOT / "manifests/kuuos_planos_materialization_execution_receipt_v0_36.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_materialization_execution_receipt", "PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_READY", "PLANOS_MATERIALIZATION_EXECUTION_RECEIPT_BLOCKED", "materialization_execution_receipt", "materialization_execution_receipt_only", "materialization_executed", "activation_authorization_granted", "execution_granted"))
    require_tokens(formal, ("MaterializationExecutionReceiptSurface", "MaterializationExecutionReceiptBoundary", "PlanOSMaterializationExecutionReceiptBridge", "source_authorization_grant_remains_grant_only", "receipt_binds_selected_candidate_to_authorization_grant", "receipt_records_materialization_execution_but_not_activation_or_truth", "boundary_blocks_activation_commit_memory_and_blocker_release", "history_appends_one_materialization_execution_receipt_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSMaterializationAuthorizationGrantBridge", "grant_authorizes_materialization_but_not_execution_activation_or_truth"))
    require_tokens(formal_root, ("KUOS.PlanOS.MaterializationExecutionReceiptV0_36",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MaterializationExecutionReceiptV0_36",))
    require_tokens(docs, ("PlanOS Materialization Execution Receipt v0.36", "selected candidate bound to authorization grant = true", "materialization execution receipt only = true", "materialization authorization granted = true", "materialization executed = true", "activation authorization granted = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_materialization_execution_receipt_v0_36.py", "v0.1-v0.36"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v036",))

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
    print("PlanOS materialization execution receipt v0.36 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
