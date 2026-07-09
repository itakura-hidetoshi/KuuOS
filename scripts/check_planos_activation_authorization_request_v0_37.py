#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_materialization_execution_receipt_v0_36 import _ready_authorization_grant
from runtime.kuuos_planos_materialization_execution_receipt_v0_36 import build_materialization_execution_receipt
from runtime.kuuos_planos_activation_authorization_request_v0_37 import SOURCE_VERSION, VERSION, build_activation_authorization_request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_activation_authorization_request_v0_37"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_execution_receipt() -> dict:
    source = _ready_authorization_grant()
    return build_materialization_execution_receipt(authorization_grant=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_execution_receipt()
    require(source["version"] == SOURCE_VERSION, "source execution receipt version mismatch")
    require("materialization_execution_receipt" in source, "source execution receipt missing")
    receipt = build_activation_authorization_request(execution_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_READY", f"request status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["activation_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["materialization_authorization_granted"] is True, "authorization not preserved")
    require(receipt["boundary"]["materialization_executed"] is True, "materialization execution not preserved")
    require(receipt["boundary"]["activation_authorization_granted"] is False, "activation promoted")
    require(receipt["boundary"]["actos_invoked"] is False, "ActOS invoked")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["activation_authorization_request"]["activation_authorization_granted"] is False, "request authorization leaked")
    require(receipt["activation_authorization_request"]["actos_invoked"] is False, "request invocation leaked")

    activated = dict(source)
    boundary = dict(activated["boundary"])
    boundary["activation_authorization_granted"] = True
    activated["boundary"] = boundary
    blocked = build_activation_authorization_request(execution_receipt=activated).to_dict()
    require(blocked["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_BLOCKED", "activated source not blocked")
    require("source_boundary_activation_authorization_granted_promoted" in blocked["blockers"], "activation promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["materialization_execution_receipt"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["materialization_execution_receipt"] = record
    blocked_record = build_activation_authorization_request(execution_receipt=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_execution_receipt_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_activation_authorization_request_v0_37.py"
    source_runtime = ROOT / "runtime/kuuos_planos_materialization_execution_receipt_v0_36.py"
    formal = ROOT / "formal/KUOS/PlanOS/ActivationAuthorizationRequestV0_37.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/MaterializationExecutionReceiptV0_36.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_37.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_v0_37.md"
    manifest_path = ROOT / "manifests/kuuos_planos_activation_authorization_request_v0_37.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_activation_authorization_request", "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_READY", "PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_BLOCKED", "activation_authorization_request", "activation_authorization_request_only", "materialization_executed", "actos_invoked", "execution_granted"))
    require_tokens(formal, ("ActivationAuthorizationRequestSurface", "ActivationAuthorizationRequestBoundary", "PlanOSActivationAuthorizationRequestBridge", "source_execution_receipt_records_materialization_only", "request_binds_selected_candidate_to_execution_receipt", "request_preserves_materialization_without_activation_or_execution", "boundary_blocks_activation_invocation_commit_memory_and_blocker_release", "history_appends_one_activation_authorization_request_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSMaterializationExecutionReceiptBridge", "receipt_records_materialization_execution_but_not_activation_or_truth"))
    require_tokens(formal_root, ("KUOS.PlanOS.ActivationAuthorizationRequestV0_37",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ActivationAuthorizationRequestV0_37",))
    require_tokens(docs, ("PlanOS Activation Authorization Request v0.37", "selected candidate bound to execution receipt = true", "activation authorization request only = true", "materialization authorization granted = true", "materialization executed = true", "activation authorization granted = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_activation_authorization_request_v0_37.py", "v0.1-v0.37"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v037",))

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
    print("PlanOS activation authorization request v0.37 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
