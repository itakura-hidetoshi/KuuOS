#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import (
    build_path_integral_candidate_weighting_receipt,
)
from runtime.kuuos_planos_weighted_decision_evidence_handoff_v0_26 import (
    build_weighted_decision_evidence_handoff_receipt,
)
from runtime.kuuos_planos_decision_review_intake_v0_27 import (
    build_decision_review_intake_receipt,
)
from runtime.kuuos_planos_decisionos_selection_request_v0_28 import (
    SOURCE_VERSION,
    VERSION,
    build_decisionos_selection_request_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_decisionos_selection_request_v0_28"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _source_gate() -> dict:
    return {
        "source_admission_handoff_bound": True,
        "physical_quantum_qi_path_integral_rerouted": True,
        "activation_authorization_granted": False,
        "execution_granted": False,
    }


def _path() -> dict:
    return {
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": "reinforce_path_weight",
        "path_integral_candidate_weighting_only": True,
        "path_integral_truth_authority": False,
        "path_integral_execution_authority": False,
        "boundary": {
            "candidate_weighting_not_truth": True,
            "does_not_authorize_execution": True,
        },
    }


def _qi() -> dict:
    return {
        "process_tensor_visible": True,
        "transition_continuity_visible": True,
        "memory_continuity_visible": True,
        "nonmarkov_memory_visible": True,
        "grants_execution_authority": False,
    }


def _blocker() -> dict:
    return {
        "blocker_classified": True,
        "protective_blocker_preserved": True,
        "situational_blocker_rerouted": True,
        "missing_evidence_held": False,
        "blocker_release_granted": False,
        "blocker_bypass_granted": False,
    }


def _candidates() -> list[dict]:
    return [
        {
            "candidate_id": "repair-route",
            "candidate_type": "repair",
            "estimated_risk": 0.2,
            "candidate_digest": "candidate-digest-repair-route",
        },
        {
            "candidate_id": "reroute-path",
            "candidate_type": "reroute",
            "estimated_risk": 0.3,
            "candidate_digest": "candidate-digest-reroute-path",
        },
    ]


def _ready_intake() -> dict:
    weighting = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path(),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    handoff = build_weighted_decision_evidence_handoff_receipt(
        weighting_receipt=weighting,
    ).to_dict()
    return build_decision_review_intake_receipt(handoff_receipt=handoff).to_dict()


def _exercise_runtime() -> None:
    intake = _ready_intake()
    require(intake["version"] == SOURCE_VERSION, "source intake version mismatch")
    request = build_decisionos_selection_request_receipt(review_intake_receipt=intake).to_dict()
    require(request["version"] == VERSION, "runtime version mismatch")
    require(request["status"] == "PLANOS_DECISIONOS_SELECTION_REQUEST_READY", "request status mismatch")
    require(request["selection_request_item_count"] == 2, "request item count mismatch")
    require(request["requested_candidate_ids"] == ["repair-route", "reroute-path"], "requested ids mismatch")
    require(request["boundary"]["selection_request_only"] is True, "selection request boundary missing")
    require(request["boundary"]["selection_owned_by_decision_os"] is True, "DecisionOS selection owner missing")
    require(request["boundary"]["candidate_selection_authority_granted"] is False, "selection authority promoted")
    require(request["boundary"]["selected_candidate_committed"] is False, "selection commit promoted")
    require(request["boundary"]["decision_receipt_issued"] is False, "decision receipt promoted")
    require(request["boundary"]["execution_granted"] is False, "execution promoted")
    require(all(item["selectable_by_this_layer"] is False for item in request["selection_request_items"]), "selectable flag leaked")
    require(all(item["selected_candidate_committed"] is False for item in request["selection_request_items"]), "selection commit leaked")

    substituted = dict(intake)
    substituted["review_candidate_ids"] = ["reroute-path", "repair-route"]
    blocked = build_decisionos_selection_request_receipt(review_intake_receipt=substituted).to_dict()
    require(blocked["status"] == "PLANOS_DECISIONOS_SELECTION_REQUEST_BLOCKED", "substitution not blocked")
    require("selection_request_ids_do_not_match_review_intake" in blocked["blockers"], "request mismatch blocker missing")

    promoted = dict(intake)
    boundary = dict(promoted["boundary"])
    boundary["decision_receipt_issued"] = True
    promoted["boundary"] = boundary
    blocked_boundary = build_decisionos_selection_request_receipt(review_intake_receipt=promoted).to_dict()
    require(blocked_boundary["status"] == "PLANOS_DECISIONOS_SELECTION_REQUEST_BLOCKED", "promoted boundary not blocked")
    require("source_boundary_decision_receipt_issued_promoted" in blocked_boundary["blockers"], "decision receipt blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_decisionos_selection_request_v0_28.py"
    source_runtime = ROOT / "runtime/kuuos_planos_decision_review_intake_v0_27.py"
    formal = ROOT / "formal/KUOS/PlanOS/DecisionOSSelectionRequestV0_28.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/DecisionReviewIntakeV0_27.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_28.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_DECISIONOS_SELECTION_REQUEST_v0_28.md"
    manifest_path = ROOT / "manifests/kuuos_planos_decisionos_selection_request_v0_28.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        runtime,
        (
            "build_decisionos_selection_request_receipt",
            "PLANOS_DECISIONOS_SELECTION_REQUEST_READY",
            "PLANOS_DECISIONOS_SELECTION_REQUEST_BLOCKED",
            "selection_owned_by_decision_os",
            "selection_request_only",
            "candidate_selection_authority_granted",
            "selected_candidate_committed",
            "decision_receipt_issued",
            "execution_granted",
        ),
    )
    require_tokens(
        formal,
        (
            "DecisionOSSelectionRequestSurface",
            "DecisionOSSelectionRequestBoundary",
            "PlanOSDecisionOSSelectionRequestBridge",
            "source_intake_remains_review_input_only",
            "request_is_selection_request_only",
            "request_grants_no_selection_decision_activation_execution_or_truth",
            "boundary_blocks_commit_memory_and_blocker_release",
            "history_appends_one_selection_request_record",
            "digest_is_exact",
        ),
    )
    require_tokens(source_formal, ("PlanOSDecisionReviewIntakeBridge", "intake_is_review_input_only"))
    require_tokens(formal_root, ("KUOS.PlanOS.DecisionOSSelectionRequestV0_28",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.DecisionOSSelectionRequestV0_28",))
    require_tokens(
        docs,
        (
            "PlanOS DecisionOS Selection Request v0.28",
            "selection owned by DecisionOS = true",
            "selection request only = true",
            "selected candidate committed = false",
            "decision receipt issued = false",
            "execution granted = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_plan_os_full_checks.py",
        ("check_planos_decisionos_selection_request_v0_28.py", "PASS: PlanOS v0.1-v0."),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v028",),
    )

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
    print("PlanOS DecisionOS selection request v0.28 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
