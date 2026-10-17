#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_literature_grounded_selective_foresight_gate_v0_40 import _literature_evidence, _ready_actos_invocation_receipt
from runtime.kuuos_planos_literature_grounded_selective_foresight_gate_v0_40 import build_literature_grounded_selective_foresight_gate
from runtime.kuuos_planos_execution_authorization_request_v0_41 import SOURCE_VERSION, VERSION, build_execution_authorization_request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_execution_authorization_request_v0_41"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_selective_foresight_gate() -> dict:
    source = _ready_actos_invocation_receipt()
    evidence = _literature_evidence()
    return build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=source,
        literature_evidence=evidence,
    ).to_dict()


def _exercise_runtime() -> None:
    source = _ready_selective_foresight_gate()
    require(source["version"] == SOURCE_VERSION, "source selective foresight gate version mismatch")
    require("selective_foresight_gate" in source, "source selective foresight gate missing")
    receipt = build_execution_authorization_request(selective_foresight_gate=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_READY", f"request status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["execution_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["execution_authorization_requested"] is True, "request flag missing")
    require(receipt["boundary"]["execution_authorization_granted"] is False, "authorization granted too early")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["execution_authorization_request"]["execution_authorization_requested"] is True, "request record missing request flag")
    require(receipt["execution_authorization_request"]["execution_authorization_granted"] is False, "request record granted authorization")
    require(receipt["execution_authorization_request"]["execution_ready"] is False, "request record leaked execution readiness")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["execution_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_execution_authorization_request(selective_foresight_gate=promoted).to_dict()
    require(blocked["status"] == "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_BLOCKED", "execution-promoted source not blocked")
    require("source_boundary_execution_granted_promoted" in blocked["blockers"], "execution promotion blocker missing")

    missing_literature = dict(source)
    boundary2 = dict(missing_literature["boundary"])
    boundary2["uncertainty_calibration_required"] = False
    missing_literature["boundary"] = boundary2
    blocked_lit = build_execution_authorization_request(selective_foresight_gate=missing_literature).to_dict()
    require(blocked_lit["status"] == "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_BLOCKED", "missing uncertainty not blocked")
    require("source_boundary_uncertainty_calibration_required_missing" in blocked_lit["blockers"], "uncertainty blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["selective_foresight_gate"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["selective_foresight_gate"] = record
    blocked_record = build_execution_authorization_request(selective_foresight_gate=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_foresight_gate_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_execution_authorization_request_v0_41.py"
    source_runtime = ROOT / "runtime/kuuos_planos_literature_grounded_selective_foresight_gate_v0_40.py"
    formal = ROOT / "formal/KUOS/PlanOS/ExecutionAuthorizationRequestV0_41.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/LiteratureGroundedSelectiveForesightGateV0_40.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_41.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_EXECUTION_AUTHORIZATION_REQUEST_v0_41.md"
    manifest_path = ROOT / "manifests/kuuos_planos_execution_authorization_request_v0_41.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_execution_authorization_request", "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_READY", "PLANOS_EXECUTION_AUTHORIZATION_REQUEST_BLOCKED", "execution_authorization_request", "execution_authorization_request_only", "execution_authorization_requested", "execution_authorization_granted", "execution_granted"))
    require_tokens(formal, ("ExecutionAuthorizationRequestSurface", "ExecutionAuthorizationRequestBoundary", "PlanOSExecutionAuthorizationRequestBridge", "source_gate_preserves_pre_execution_selective_foresight", "request_binds_candidate_and_preserves_gate_state", "request_preserves_literature_grounded_execution_prerequisites", "request_does_not_grant_execution_truth_commit_memory_or_blocker_release", "history_appends_one_execution_authorization_request_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSLiteratureGroundedSelectiveForesightGateBridge", "gate_does_not_grant_execution_truth_commit_memory_or_blocker_release"))
    require_tokens(formal_root, ("KUOS.PlanOS.ExecutionAuthorizationRequestV0_41",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.ExecutionAuthorizationRequestV0_41",))
    require_tokens(docs, ("PlanOS Execution Authorization Request v0.41", "execution authorization request only = true", "execution authorization requested = true", "execution authorization granted = false", "execution granted = false", "truth authority granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_execution_authorization_request_v0_41.py", "v0.1-v0.41"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v041",))

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
    print("PlanOS execution authorization request v0.41 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
