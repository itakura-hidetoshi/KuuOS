#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_execution_authorization_grant_v0_42 import _ready_execution_request
from runtime.kuuos_planos_execution_authorization_grant_v0_42 import build_execution_authorization_grant
from runtime.kuuos_planos_execution_receipt_v0_43 import SOURCE_VERSION, VERSION, build_execution_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_execution_receipt_v0_43"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_execution_grant() -> dict:
    source = _ready_execution_request()
    return build_execution_authorization_grant(execution_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_execution_grant()
    require(source["version"] == SOURCE_VERSION, "source execution grant version mismatch")
    require("execution_authorization_grant" in source, "source execution grant missing")
    receipt = build_execution_receipt(execution_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXECUTION_RECEIPT_READY", f"execution receipt status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["execution_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["execution_authorization_granted"] is True, "authorization grant not preserved")
    require(receipt["boundary"]["execution_granted"] is True, "execution not recorded")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["boundary"]["memory_overwrite_granted"] is False, "memory overwrite promoted")
    require(receipt["boundary"]["truth_authority_granted"] is False, "truth authority promoted")
    require(receipt["execution_receipt"]["execution_granted"] is True, "execution receipt missing execution")
    require(receipt["execution_receipt"]["external_commit_ready"] is False, "receipt leaked external commit readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["external_commit_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_execution_receipt(execution_grant=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXECUTION_RECEIPT_BLOCKED", "external-commit-promoted source not blocked")
    require("source_boundary_external_commit_granted_promoted" in blocked["blockers"], "external commit promotion blocker missing")

    execution_promoted = dict(source)
    boundary2 = dict(execution_promoted["boundary"])
    boundary2["execution_granted"] = True
    execution_promoted["boundary"] = boundary2
    blocked_execution = build_execution_receipt(execution_grant=execution_promoted).to_dict()
    require(blocked_execution["status"] == "PLANOS_EXECUTION_RECEIPT_BLOCKED", "pre-executed source not blocked")
    require("source_boundary_execution_granted_promoted" in blocked_execution["blockers"], "pre-execution blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["execution_authorization_grant"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["execution_authorization_grant"] = record
    blocked_record = build_execution_receipt(execution_grant=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_EXECUTION_RECEIPT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_execution_grant_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_execution_receipt_v0_43.py"
    source_runtime = ROOT / "runtime/kuuos_planos_execution_authorization_grant_v0_42.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExecutionReceiptV0_43.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ExecutionAuthorizationGrantV0_42.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_43.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXECUTION_RECEIPT_v0_43.md"
    manifest_path = ROOT / "manifests/kuuos_planos_execution_receipt_v0_43.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_execution_receipt", "PLANOS_EXECUTION_RECEIPT_READY", "PLANOS_EXECUTION_RECEIPT_BLOCKED", "execution_receipt", "execution_receipt_only", "execution_granted", "external_commit_granted", "memory_overwrite_granted"))
    require_tokens(formal, ("ExecutionReceiptSurface", "ExecutionReceiptBoundary", "PlanOSExecutionReceiptBridge", "source_grant_authorizes_but_does_not_execute", "receipt_binds_candidate_and_preserves_prerequisites", "receipt_records_execution_but_not_commit_memory_truth_or_blocker_release", "boundary_preserves_execution_receipt_only", "history_appends_one_execution_receipt_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSExecutionAuthorizationGrantBridge", "grant_authorizes_execution_but_does_not_execute_or_commit"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExecutionReceiptV0_43",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExecutionReceiptV0_43",))
    require_tokens(docs, ("PlanOS Execution Receipt v0.43", "execution receipt only = true", "execution authorization granted = true", "execution granted = true", "external commit granted = false", "memory overwrite granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_execution_receipt_v0_43.py", "v0.1-v0.43"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v043",))

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
    print("PlanOS execution receipt v0.43 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
