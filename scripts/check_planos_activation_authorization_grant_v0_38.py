#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_activation_authorization_request_v0_37 import _ready_execution_receipt
from runtime.kuuos_planos_activation_authorization_request_v0_37 import build_activation_authorization_request
from runtime.kuuos_planos_activation_authorization_grant_v0_38 import SOURCE_VERSION, VERSION, build_activation_authorization_grant

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_activation_authorization_grant_v0_38"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_activation_request() -> dict:
    source = _ready_execution_receipt()
    return build_activation_authorization_request(execution_receipt=source).to_dict()


def _exercise_runtime() -> None:
    source = _ready_activation_request()
    require(source["version"] == SOURCE_VERSION, "source activation request version mismatch")
    require("activation_authorization_request" in source, "source activation request missing")
    receipt = build_activation_authorization_grant(activation_request=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_READY", f"grant status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["activation_authorization_grant_only"] is True, "grant-only boundary missing")
    require(receipt["boundary"]["materialization_authorization_granted"] is True, "materialization authorization not preserved")
    require(receipt["boundary"]["materialization_executed"] is True, "materialization execution not preserved")
    require(receipt["boundary"]["activation_authorization_granted"] is True, "activation authorization not granted")
    require(receipt["boundary"]["actos_invoked"] is False, "ActOS invoked")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["activation_authorization_grant"]["activation_authorization_granted"] is True, "grant authorization missing")
    require(receipt["activation_authorization_grant"]["actos_invoked"] is False, "grant invocation leaked")

    invoked = dict(source)
    boundary = dict(invoked["boundary"])
    boundary["actos_invoked"] = True
    invoked["boundary"] = boundary
    blocked = build_activation_authorization_grant(activation_request=invoked).to_dict()
    require(blocked["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_BLOCKED", "invoked source not blocked")
    require("source_boundary_actos_invoked_promoted" in blocked["blockers"], "ActOS promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["activation_authorization_request"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["activation_authorization_request"] = record
    blocked_record = build_activation_authorization_grant(activation_request=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_activation_request_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_activation_authorization_grant_v0_38.py"
    source_runtime = ROOT / "runtime/kuuos_planos_activation_authorization_request_v0_37.py"
    formal = ROOT / "formal/KUOS/PlanOS/ActivationAuthorizationGrantV0_38.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ActivationAuthorizationRequestV0_37.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_38.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_ACTIVATION_AUTHORIZATION_GRANT_v0_38.md"
    manifest_path = ROOT / "manifests/kuuos_planos_activation_authorization_grant_v0_38.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_activation_authorization_grant", "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_READY", "PLANOS_ACTIVATION_AUTHORIZATION_GRANT_BLOCKED", "activation_authorization_grant", "activation_authorization_grant_only", "activation_authorization_granted", "actos_invoked", "execution_granted"))
    require_tokens(formal, ("ActivationAuthorizationGrantSurface", "ActivationAuthorizationGrantBoundary", "PlanOSActivationAuthorizationGrantBridge", "source_activation_request_remains_request_only", "grant_binds_selected_candidate_to_activation_request", "grant_authorizes_activation_but_not_invocation_execution_or_truth", "boundary_blocks_invocation_execution_commit_memory_and_blocker_release", "history_appends_one_activation_authorization_grant_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSActivationAuthorizationRequestBridge", "request_preserves_materialization_without_activation_or_execution"))
    require_tokens(formal_root, ("KUOS.PlanOS.ActivationAuthorizationGrantV0_38",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ActivationAuthorizationGrantV0_38",))
    require_tokens(docs, ("PlanOS Activation Authorization Grant v0.38", "selected candidate bound to activation request = true", "activation authorization grant only = true", "activation authorization granted = true", "ActOS invoked = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_activation_authorization_grant_v0_38.py", "v0.1-v0.38"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v038",))

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
    print("PlanOS activation authorization grant v0.38 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
