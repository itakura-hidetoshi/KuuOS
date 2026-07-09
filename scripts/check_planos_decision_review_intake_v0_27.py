#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import build_path_integral_candidate_weighting_receipt
from runtime.kuuos_planos_weighted_decision_evidence_handoff_v0_26 import build_weighted_decision_evidence_handoff_receipt
from runtime.kuuos_planos_decision_review_intake_v0_27 import (
    SOURCE_VERSION,
    VERSION,
    build_decision_review_intake_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_decision_review_intake_v0_27"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _source_gate() -> dict:
    return {"source_admission_handoff_bound": True, "physical_quantum_qi_path_integral_rerouted": True, "activation_authorization_granted": False, "execution_granted": False}


def _path(mode: str = "reinforce_path_weight") -> dict:
    return {
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": mode,
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


def _ready_handoff() -> dict:
    weighting = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path(),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    return build_weighted_decision_evidence_handoff_receipt(weighting_receipt=weighting).to_dict()


def _exercise_runtime() -> None:
    handoff = _ready_handoff()
    require(handoff["version"] == SOURCE_VERSION, "source handoff version mismatch")
    intake = build_decision_review_intake_receipt(handoff_receipt=handoff).to_dict()
    require(intake["version"] == VERSION, "runtime version mismatch")
    require(intake["status"] == "PLANOS_DECISION_REVIEW_INTAKE_READY", "intake status mismatch")
    require(intake["review_item_count"] == 2, "review item count mismatch")
    require(intake["review_candidate_ids"] == ["repair-route", "reroute-path"], "review ids mismatch")
    require(intake["boundary"]["decision_review_input_only"] is True, "review input boundary missing")
    require(intake["boundary"]["candidate_selection_authority_granted"] is False, "selection promoted")
    require(intake["boundary"]["decision_receipt_issued"] is False, "decision receipt promoted")
    require(intake["boundary"]["execution_granted"] is False, "execution promoted")
    require(all(item["selectable_here"] is False for item in intake["decision_review_items"]), "selectable flag leaked")
    require(all(item["execution_ready"] is False for item in intake["decision_review_items"]), "execution readiness leaked")

    substituted = dict(handoff)
    substituted["review_candidate_ids"] = ["reroute-path", "repair-route"]
    blocked = build_decision_review_intake_receipt(handoff_receipt=substituted).to_dict()
    require(blocked["status"] == "PLANOS_DECISION_REVIEW_INTAKE_BLOCKED", "silent substitution not blocked")
    require("review_candidate_ids_silent_substitution_detected" in blocked["blockers"], "silent substitution blocker missing")

    barrier = dict(handoff)
    items = [dict(item) for item in barrier["decision_evidence_items"]]
    items[0]["barrier_required"] = True
    barrier["decision_evidence_items"] = items
    barrier["barrier_candidate_ids"] = ["repair-route"]
    barrier["review_candidate_ids"] = ["repair-route", "reroute-path"]
    blocked_barrier = build_decision_review_intake_receipt(handoff_receipt=barrier).to_dict()
    require(blocked_barrier["status"] == "PLANOS_DECISION_REVIEW_INTAKE_BLOCKED", "barrier not blocked")
    require("repair-route" in blocked_barrier["excluded_barrier_candidate_ids"], "barrier exclusion missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_decision_review_intake_v0_27.py"
    source_runtime = ROOT / "runtime/kuuos_planos_weighted_decision_evidence_handoff_v0_26.py"
    formal = ROOT / "formal/KUOS/PlanOS/DecisionReviewIntakeV0_27.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/WeightedDecisionEvidenceHandoffV0_26.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_27.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_DECISION_REVIEW_INTAKE_v0_27.md"
    manifest_path = ROOT / "manifests/kuuos_planos_decision_review_intake_v0_27.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_decision_review_intake_receipt", "PLANOS_DECISION_REVIEW_INTAKE_READY", "PLANOS_DECISION_REVIEW_INTAKE_BLOCKED", "silent_substitution_forbidden", "barrier_candidate_review_blocked_here", "candidate_selection_authority_granted", "decision_receipt_issued", "execution_granted"))
    require_tokens(formal, ("DecisionReviewIntakeSurface", "DecisionReviewIntakeBoundary", "PlanOSDecisionReviewIntakeBridge", "source_handoff_remains_evidence_only", "intake_is_review_input_only", "intake_grants_no_selection_decision_activation_execution_or_truth", "boundary_blocks_execution_commit_memory_and_blocker_release", "history_appends_one_review_intake_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSWeightedDecisionEvidenceHandoffBridge", "handoff_is_decision_evidence_only"))
    require_tokens(formal_root, ("KUOS.PlanOS.DecisionReviewIntakeV0_27",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.DecisionReviewIntakeV0_27",))
    require_tokens(docs, ("PlanOS DecisionOS Review Intake v0.27", "silent substitution forbidden = true", "candidate selection authority granted = false", "decision receipt issued = false", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_decision_review_intake_v0_27.py", "PASS: PlanOS v0.1-v0."))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v027",))

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
    print("PlanOS DecisionOS review intake v0.27 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
