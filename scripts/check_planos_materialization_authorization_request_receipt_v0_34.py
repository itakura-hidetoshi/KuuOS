#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_materialization_authorization_request_v0_33 import _ready_materialization_preflight
from runtime.kuuos_planos_materialization_authorization_request_v0_33 import build_materialization_authorization_request_receipt as build_v33_authorization_request_receipt
from runtime.kuuos_planos_materialization_authorization_request_receipt_v0_34 import SOURCE_VERSION, VERSION, build_materialization_authorization_request_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_materialization_authorization_request_receipt_v0_34"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_authorization_request() -> dict:
    source = _ready_materialization_preflight()
    return build_v33_authorization_request_receipt(materialization_preflight_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_authorization_request()
    require(source["version"] == SOURCE_VERSION, "source request version mismatch")
    require("materialization_authorization_request" in source, "source authorization request missing")
    receipt = build_materialization_authorization_request_receipt(authorization_request_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_READY", f"receipt status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["materialization_authorization_request_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["materialization_authorization_granted"] is False, "materialization authorization promoted")
    require(receipt["boundary"]["materialization_executed"] is False, "materialization executed")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["materialization_authorization_request_receipt"]["materialization_authorization_granted"] is False, "receipt authorization leaked")
    require(receipt["materialization_authorization_request_receipt"]["materialization_executed"] is False, "receipt execution leaked")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["materialization_authorization_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_materialization_authorization_request_receipt(authorization_request_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_BLOCKED", "promoted source not blocked")
    require("source_boundary_materialization_authorization_granted_promoted" in blocked["blockers"], "authorization promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["materialization_authorization_request"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["materialization_authorization_request"] = record
    blocked_record = build_materialization_authorization_request_receipt(authorization_request_receipt=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_authorization_request_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_request_receipt_v0_34.py"
    source_runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_request_v0_33.py"
    formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationRequestReceiptV0_34.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationRequestV0_33.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_34.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_v0_34.md"
    manifest_path = ROOT / "manifests/kuuos_planos_materialization_authorization_request_receipt_v0_34.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_materialization_authorization_request_receipt", "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_READY", "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_RECEIPT_BLOCKED", "materialization_authorization_request", "materialization_authorization_request_receipt_only", "materialization_authorization_granted", "materialization_executed", "execution_granted"))
    require_tokens(formal, ("MaterializationAuthorizationRequestReceiptSurface", "MaterializationAuthorizationRequestReceiptBoundary", "PlanOSMaterializationAuthorizationRequestReceiptBridge", "source_request_remains_request_only", "receipt_binds_selected_candidate_to_authorization_request", "receipt_grants_no_authorization_execution_activation_or_truth", "boundary_blocks_materialization_execution_commit_memory_and_blocker_release", "history_appends_one_authorization_request_receipt_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSMaterializationAuthorizationRequestBridge", "request_binds_selected_candidate_to_preflight"))
    require_tokens(formal_root, ("KUOS.PlanOS.MaterializationAuthorizationRequestReceiptV0_34",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MaterializationAuthorizationRequestReceiptV0_34",))
    require_tokens(docs, ("PlanOS Materialization Authorization Request Receipt v0.34", "selected candidate bound to authorization request = true", "materialization authorization request receipt only = true", "materialization authorization granted = false", "materialization executed = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_materialization_authorization_request_receipt_v0_34.py", "v0.1-v0.34"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v034",))

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
    print("PlanOS materialization authorization request receipt v0.34 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
