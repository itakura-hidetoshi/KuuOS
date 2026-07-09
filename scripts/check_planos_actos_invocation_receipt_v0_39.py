#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_activation_authorization_grant_v0_38 import _ready_activation_request
from runtime.kuuos_planos_activation_authorization_grant_v0_38 import build_activation_authorization_grant
from runtime.kuuos_planos_actos_invocation_receipt_v0_39 import SOURCE_VERSION, VERSION, build_actos_invocation_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_actos_invocation_receipt_v0_39"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_activation_grant() -> dict:
    source = _ready_activation_request()
    return build_activation_authorization_grant(activation_request=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_activation_grant()
    require(source["version"] == SOURCE_VERSION, "source activation grant version mismatch")
    require("activation_authorization_grant" in source, "source activation grant missing")
    receipt = build_actos_invocation_receipt(activation_grant=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_ACTOS_INVOCATION_RECEIPT_READY", f"invocation status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["actos_invocation_receipt_only"] is True, "receipt-only boundary missing")
    require(receipt["boundary"]["activation_authorization_granted"] is True, "activation authorization not preserved")
    require(receipt["boundary"]["actos_invoked"] is True, "ActOS invocation not recorded")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["actos_invocation_receipt"]["actos_invoked"] is True, "receipt invocation missing")
    require(receipt["actos_invocation_receipt"]["execution_ready"] is False, "receipt execution leaked")

    execution_promoted = dict(source)
    boundary = dict(execution_promoted["boundary"])
    boundary["execution_granted"] = True
    execution_promoted["boundary"] = boundary
    blocked = build_actos_invocation_receipt(activation_grant=execution_promoted).to_dict()
    require(blocked["status"] == "PLANOS_ACTOS_INVOCATION_RECEIPT_BLOCKED", "execution-promoted source not blocked")
    require("source_boundary_execution_granted_promoted" in blocked["blockers"], "execution promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["activation_authorization_grant"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["activation_authorization_grant"] = record
    blocked_record = build_actos_invocation_receipt(activation_grant=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_ACTOS_INVOCATION_RECEIPT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_activation_grant_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_actos_invocation_receipt_v0_39.py"
    source_runtime = ROOT / "runtime/kuuos_planos_activation_authorization_grant_v0_38.py"
    formal = ROOT / "formal/KUOS/PlanOS/ActOSInvocationReceiptV0_39.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ActivationAuthorizationGrantV0_38.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_39.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_ACTOS_INVOCATION_RECEIPT_v0_39.md"
    manifest_path = ROOT / "manifests/kuuos_planos_actos_invocation_receipt_v0_39.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_actos_invocation_receipt", "PLANOS_ACTOS_INVOCATION_RECEIPT_READY", "PLANOS_ACTOS_INVOCATION_RECEIPT_BLOCKED", "actos_invocation_receipt", "actos_invocation_receipt_only", "actos_invoked", "execution_granted", "external_commit_granted"))
    require_tokens(formal, ("ActOSInvocationReceiptSurface", "ActOSInvocationReceiptBoundary", "PlanOSActOSInvocationReceiptBridge", "source_activation_grant_authorizes_activation_only", "receipt_binds_selected_candidate_to_activation_grant", "receipt_records_invocation_but_not_execution_or_truth", "boundary_blocks_execution_commit_memory_and_blocker_release", "history_appends_one_actos_invocation_receipt_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSActivationAuthorizationGrantBridge", "grant_authorizes_activation_but_not_invocation_execution_or_truth"))
    require_tokens(formal_root, ("KUOS.PlanOS.ActOSInvocationReceiptV0_39",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ActOSInvocationReceiptV0_39",))
    require_tokens(docs, ("PlanOS ActOS Invocation Receipt v0.39", "selected candidate bound to activation grant = true", "ActOS invocation receipt only = true", "activation authorization granted = true", "ActOS invoked = true", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_actos_invocation_receipt_v0_39.py", "v0.1-v0.39"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v039",))

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
    print("PlanOS ActOS invocation receipt v0.39 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
