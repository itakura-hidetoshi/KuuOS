#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import build_path_integral_candidate_weighting_receipt
from runtime.kuuos_planos_weighted_decision_evidence_handoff_v0_26 import build_weighted_decision_evidence_handoff_receipt
from runtime.kuuos_planos_decision_review_intake_v0_27 import build_decision_review_intake_receipt
from runtime.kuuos_planos_decisionos_selection_request_v0_28 import build_decisionos_selection_request_receipt
from runtime.kuuos_planos_decisionos_selection_receipt_intake_v0_29 import (
    DECISIONOS_SELECTION_VERSION,
    SOURCE_VERSION,
    VERSION,
    build_decisionos_selection_receipt_intake,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_decisionos_selection_receipt_intake_v0_29"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _source_gate() -> dict:
    return {"source_admission_handoff_bound": True, "physical_quantum_qi_path_integral_rerouted": True, "activation_authorization_granted": False, "execution_granted": False}


def _path() -> dict:
    return {
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": "reinforce_path_weight",
        "path_integral_candidate_weighting_only": True,
        "path_integral_truth_authority": False,
        "path_integral_execution_authority": False,
        "boundary": {"candidate_weighting_not_truth": True, "does_not_authorize_execution": True},
    }


def _qi() -> dict:
    return {"process_tensor_visible": True, "transition_continuity_visible": True, "memory_continuity_visible": True, "nonmarkov_memory_visible": True, "grants_execution_authority": False}


def _blocker() -> dict:
    return {"blocker_classified": True, "protective_blocker_preserved": True, "situational_blocker_rerouted": True, "missing_evidence_held": False, "blocker_release_granted": False, "blocker_bypass_granted": False}


def _candidates() -> list[dict]:
    return [
        {"candidate_id": "repair-route", "candidate_type": "repair", "estimated_risk": 0.2, "candidate_digest": "candidate-digest-repair-route"},
        {"candidate_id": "reroute-path", "candidate_type": "reroute", "estimated_risk": 0.3, "candidate_digest": "candidate-digest-reroute-path"},
    ]


def _ready_request() -> dict:
    weighting = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path(),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    handoff = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=weighting).to_dict()
    intake = build_decision_review_intake_receipt(handoff_receipt=handoff).to_dict()
    return build_decisionos_selection_request_receipt(review_intake_receipt=intake).to_dict()


def _decisionos_receipt(candidate_id: str = "repair-route", candidate_digest: str = "candidate-digest-repair-route") -> dict:
    return {
        "version": DECISIONOS_SELECTION_VERSION,
        "status": "DECISIONOS_ADMISSIBLE_CANDIDATE_SELECTED",
        "selected_candidate_id": candidate_id,
        "selected_candidate_digest": candidate_digest,
        "receipt_digest": f"decisionos-selection-receipt-{candidate_id}",
        "activation_authorization_granted": False,
        "actos_invoked": False,
        "execution_granted": False,
        "truth_authority_granted": False,
        "memory_overwrite_granted": False,
        "blocker_release_granted": False,
        "external_commit_granted": False,
    }


def _exercise_runtime() -> None:
    request = _ready_request()
    require(request["version"] == SOURCE_VERSION, "source request version mismatch")
    receipt = build_decisionos_selection_receipt_intake(
        selection_request_receipt=request,
        decisionos_selection_receipt=_decisionos_receipt(),
    ).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_READY", "receipt intake status mismatch")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["selected_candidate_digest"] == "candidate-digest-repair-route", "selected digest mismatch")
    require(receipt["boundary"]["selection_receipt_intake_only"] is True, "intake-only boundary missing")
    require(receipt["boundary"]["selected_candidate_bound_to_request"] is True, "request binding boundary missing")
    require(receipt["boundary"]["selected_candidate_committed_here"] is False, "selection commit promoted")
    require(receipt["boundary"]["plan_synthesis_granted"] is False, "synthesis promoted")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["intake_record"]["selected_candidate_committed_here"] is False, "record commit leaked")
    require(receipt["intake_record"]["plan_synthesis_ready"] is False, "record synthesis leaked")

    bad_candidate = build_decisionos_selection_receipt_intake(
        selection_request_receipt=request,
        decisionos_selection_receipt=_decisionos_receipt(candidate_id="missing-route", candidate_digest="missing-digest"),
    ).to_dict()
    require(bad_candidate["status"] == "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_BLOCKED", "missing candidate not blocked")
    require("selected_candidate_not_in_requested_ids" in bad_candidate["blockers"], "membership blocker missing")

    bad_digest = build_decisionos_selection_receipt_intake(
        selection_request_receipt=request,
        decisionos_selection_receipt=_decisionos_receipt(candidate_id="repair-route", candidate_digest="wrong-digest"),
    ).to_dict()
    require(bad_digest["status"] == "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_BLOCKED", "bad digest not blocked")
    require("selected_candidate_digest_mismatch" in bad_digest["blockers"], "digest blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_decisionos_selection_receipt_intake_v0_29.py"
    source_runtime = ROOT / "runtime/kuuos_planos_decisionos_selection_request_v0_28.py"
    formal = ROOT / "formal/KUOS/PlanOS/DecisionOSSelectionReceiptIntakeV0_29.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/DecisionOSSelectionRequestV0_28.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_29.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_v0_29.md"
    manifest_path = ROOT / "manifests/kuuos_planos_decisionos_selection_receipt_intake_v0_29.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_decisionos_selection_receipt_intake", "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_READY", "PLANOS_DECISIONOS_SELECTION_RECEIPT_INTAKE_BLOCKED", "selected_candidate_bound_to_request", "selected_candidate_committed_here", "plan_synthesis_granted", "execution_granted"))
    require_tokens(formal, ("DecisionOSSelectionReceiptIntakeSurface", "DecisionOSSelectionReceiptIntakeBoundary", "PlanOSDecisionOSSelectionReceiptIntakeBridge", "source_request_remains_selection_request_only", "intake_binds_decisionos_selection_to_request", "intake_grants_no_commit_synthesis_activation_execution_or_truth", "boundary_blocks_plan_synthesis_commit_memory_and_blocker_release", "history_appends_one_selection_receipt_intake_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSDecisionOSSelectionRequestBridge", "request_is_selection_request_only"))
    require_tokens(formal_root, ("KUOS.PlanOS.DecisionOSSelectionReceiptIntakeV0_29",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.DecisionOSSelectionReceiptIntakeV0_29",))
    require_tokens(docs, ("PlanOS DecisionOS Selection Receipt Intake v0.29", "selected candidate bound to request = true", "selected candidate committed here = false", "plan synthesis granted = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_decisionos_selection_receipt_intake_v0_29.py", "PASS: PlanOS v0.1-v0."))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v029",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["decisionos_selection_version"] == DECISIONOS_SELECTION_VERSION, "decisionos version mismatch")
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
    print("PlanOS DecisionOS selection receipt intake v0.29 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
