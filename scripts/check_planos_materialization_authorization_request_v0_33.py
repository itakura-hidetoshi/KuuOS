#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import build_path_integral_candidate_weighting_receipt
from runtime.kuuos_planos_weighted_decision_evidence_handoff_v0_26 import build_weighted_decision_evidence_handoff_receipt
from runtime.kuuos_planos_decision_review_intake_v0_27 import build_decision_review_intake_receipt
from runtime.kuuos_planos_decisionos_selection_request_v0_28 import build_decisionos_selection_request_receipt
from runtime.kuuos_planos_decisionos_selection_receipt_intake_v0_29 import DECISIONOS_SELECTION_VERSION, build_decisionos_selection_receipt_intake
from runtime.kuuos_planos_selected_candidate_synthesis_request_v0_30 import build_selected_candidate_synthesis_request_receipt
from runtime.kuuos_planos_selected_candidate_synthesis_receipt_v0_31 import build_selected_candidate_synthesis_receipt
from runtime.kuuos_planos_selected_candidate_materialization_preflight_v0_32 import build_selected_candidate_materialization_preflight_receipt
from runtime.kuuos_planos_materialization_authorization_request_v0_33 import SOURCE_VERSION, VERSION, build_materialization_authorization_request_receipt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_materialization_authorization_request_v0_33"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_materialization_preflight() -> dict:
    source_gate = {"source_admission_handoff_bound": True, "physical_quantum_qi_path_integral_rerouted": True, "activation_authorization_granted": False, "execution_granted": False}
    path = {"physical_quantum_qi_path_integral_reentry_considered": True, "dominant_reentry_mode": "reinforce_path_weight", "path_integral_candidate_weighting_only": True, "path_integral_truth_authority": False, "path_integral_execution_authority": False, "boundary": {"candidate_weighting_not_truth": True, "does_not_authorize_execution": True}}
    qi = {"process_tensor_visible": True, "transition_continuity_visible": True, "memory_continuity_visible": True, "nonmarkov_memory_visible": True, "grants_execution_authority": False}
    blocker = {"blocker_classified": True, "protective_blocker_preserved": True, "situational_blocker_rerouted": True, "missing_evidence_held": False, "blocker_release_granted": False, "blocker_bypass_granted": False}
    candidates = [
        {"candidate_id": "repair-route", "candidate_type": "repair", "estimated_risk": 0.2, "candidate_digest": "candidate-digest-repair-route"},
        {"candidate_id": "reroute-path", "candidate_type": "reroute", "estimated_risk": 0.3, "candidate_digest": "candidate-digest-reroute-path"},
    ]
    weighting = build_path_integral_candidate_weighting_receipt(source_gate=source_gate, path_integral=path, qi_process_tensor=qi, blocker=blocker, candidates=candidates).to_dict()
    handoff = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=weighting).to_dict()
    review = build_decision_review_intake_receipt(handoff_receipt=handoff).to_dict()
    request = build_decisionos_selection_request_receipt(review_intake_receipt=review).to_dict()
    decision = {
        "version": DECISIONOS_SELECTION_VERSION,
        "status": "DECISIONOS_ADMISSIBLE_CANDIDATE_SELECTED",
        "selected_candidate_id": "repair-route",
        "selected_candidate_digest": "candidate-digest-repair-route",
        "receipt_digest": "decisionos-selection-receipt-repair-route",
        "activation_authorization_granted": False,
        "actos_invoked": False,
        "execution_granted": False,
        "truth_authority_granted": False,
        "memory_overwrite_granted": False,
        "blocker_release_granted": False,
        "external_commit_granted": False,
    }
    intake = build_decisionos_selection_receipt_intake(selection_request_receipt=request, decisionos_selection_receipt=decision).to_dict()
    synth_request = build_selected_candidate_synthesis_request_receipt(selection_receipt_intake=intake).to_dict()
    synth_receipt = build_selected_candidate_synthesis_receipt(synthesis_request_receipt=synth_request).to_dict()
    return build_selected_candidate_materialization_preflight_receipt(synthesis_receipt=synth_receipt).to_dict()


def _exercise_runtime() -> None:
    source = _ready_materialization_preflight()
    require(source["version"] == SOURCE_VERSION, "source preflight version mismatch")
    require("materialization_preflight" in source, "source preflight record missing")
    receipt = build_materialization_authorization_request_receipt(materialization_preflight_receipt=source).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_READY", f"request status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["materialization_authorization_request_only"] is True, "request-only boundary missing")
    require(receipt["boundary"]["materialization_authorization_granted"] is False, "materialization authorization promoted")
    require(receipt["boundary"]["materialization_executed"] is False, "materialization executed")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["materialization_authorization_request"]["materialization_authorization_granted"] is False, "request authorization leaked")
    require(receipt["materialization_authorization_request"]["materialization_executed"] is False, "request execution leaked")

    promoted = dict(source)
    boundary = dict(promoted["boundary"])
    boundary["materialization_authorization_granted"] = True
    promoted["boundary"] = boundary
    blocked = build_materialization_authorization_request_receipt(materialization_preflight_receipt=promoted).to_dict()
    require(blocked["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_BLOCKED", "promoted source not blocked")
    require("source_boundary_materialization_authorization_granted_promoted" in blocked["blockers"], "authorization promotion blocker missing")

    mismatch = dict(source)
    record = dict(mismatch["materialization_preflight"])
    record["selected_candidate_digest"] = "wrong-digest"
    mismatch["materialization_preflight"] = record
    blocked_record = build_materialization_authorization_request_receipt(materialization_preflight_receipt=mismatch).to_dict()
    require(blocked_record["status"] == "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_BLOCKED", "record mismatch not blocked")
    require("selected_candidate_digest_preflight_mismatch" in blocked_record["blockers"], "record mismatch blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_materialization_authorization_request_v0_33.py"
    source_runtime = ROOT / "runtime/kuuos_planos_selected_candidate_materialization_preflight_v0_32.py"
    formal = ROOT / "formal/KUOS/PlanOS/MaterializationAuthorizationRequestV0_33.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/SelectedCandidateMaterializationPreflightV0_32.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_33.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_v0_33.md"
    manifest_path = ROOT / "manifests/kuuos_planos_materialization_authorization_request_v0_33.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_materialization_authorization_request_receipt", "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_READY", "PLANOS_MATERIALIZATION_AUTHORIZATION_REQUEST_BLOCKED", "materialization_preflight", "materialization_authorization_request_only", "materialization_authorization_granted", "materialization_executed", "execution_granted"))
    require_tokens(formal, ("MaterializationAuthorizationRequestSurface", "MaterializationAuthorizationRequestBoundary", "PlanOSMaterializationAuthorizationRequestBridge", "source_preflight_remains_preflight_only", "request_binds_selected_candidate_to_preflight", "request_grants_no_authorization_execution_activation_or_truth", "boundary_blocks_materialization_execution_commit_memory_and_blocker_release", "history_appends_one_authorization_request_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSSelectedCandidateMaterializationPreflightBridge", "preflight_binds_selected_candidate_to_synthesis_receipt"))
    require_tokens(formal_root, ("KUOS.PlanOS.MaterializationAuthorizationRequestV0_33",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.MaterializationAuthorizationRequestV0_33",))
    require_tokens(docs, ("PlanOS Materialization Authorization Request v0.33", "selected candidate bound to preflight = true", "materialization authorization request only = true", "materialization authorization granted = false", "materialization executed = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_materialization_authorization_request_v0_33.py", "v0.1-v0.33"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v033",))

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
    print("PlanOS materialization authorization request v0.33 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
