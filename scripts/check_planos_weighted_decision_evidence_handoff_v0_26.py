#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import (
    build_path_integral_candidate_weighting_receipt,
)
from runtime.kuuos_planos_weighted_decision_evidence_handoff_v0_26 import (
    SOURCE_VERSION,
    VERSION,
    build_weighted_decision_evidence_handoff_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_weighted_decision_evidence_handoff_v0_26"


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


def _ready_weighting() -> dict:
    return build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path(),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()


def _exercise_runtime() -> None:
    weighting = _ready_weighting()
    require(weighting["version"] == SOURCE_VERSION, "source weighting version mismatch")
    handoff = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=weighting).to_dict()
    require(handoff["version"] == VERSION, "runtime version mismatch")
    require(handoff["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(handoff["status"] == "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY", "handoff status mismatch")
    require(handoff["evidence_item_count"] == 2, "evidence count mismatch")
    require(handoff["review_candidate_ids"] == ["repair-route", "reroute-path"], "review ids mismatch")
    require(handoff["boundary"]["decision_evidence_only"] is True, "decision evidence boundary missing")
    require(handoff["boundary"]["selection_owned_by_decision_os"] is True, "DecisionOS ownership missing")
    require(handoff["boundary"]["decision_made"] is False, "decision promoted")
    require(handoff["boundary"]["execution_granted"] is False, "execution promoted")
    require(all(item["execution_ready"] is False for item in handoff["decision_evidence_items"]), "execution readiness leaked")
    require(all(item["selection_authority_granted"] is False for item in handoff["decision_evidence_items"]), "selection authority leaked")

    bad = dict(weighting)
    bad_boundary = dict(bad["boundary"])
    bad_boundary["selection_authority_granted"] = True
    bad["boundary"] = bad_boundary
    blocked = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=bad).to_dict()
    require(blocked["status"] == "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_BLOCKED", "bad boundary not blocked")
    require("source_boundary_selection_authority_granted_promoted" in blocked["blockers"], "selection blocker missing")

    item_bad = dict(weighting)
    receipts = [dict(item) for item in item_bad["candidate_weight_receipts"]]
    receipts[0]["execution_ready"] = True
    item_bad["candidate_weight_receipts"] = receipts
    blocked_item = build_weighted_decision_evidence_handoff_receipt(weighting_receipt=item_bad).to_dict()
    require(blocked_item["status"] == "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_BLOCKED", "bad item not blocked")
    require("candidate_execution_ready_forbidden:repair-route" in blocked_item["blockers"], "candidate execution blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_weighted_decision_evidence_handoff_v0_26.py"
    source_runtime = ROOT / "runtime/kuuos_planos_path_integral_candidate_weighting_v0_25.py"
    formal = ROOT / "formal/KUOS/PlanOS/WeightedDecisionEvidenceHandoffV0_26.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/PathIntegralCandidateWeightingV0_25.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_26.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_v0_26.md"
    manifest_path = ROOT / "manifests/kuuos_planos_weighted_decision_evidence_handoff_v0_26.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        runtime,
        (
            "build_weighted_decision_evidence_handoff_receipt",
            "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY",
            "PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_BLOCKED",
            "selection_owned_by_decision_os",
            "decision_evidence_only",
            "selected_candidate_committed",
            "execution_granted",
            "blocker_release_granted",
        ),
    )
    require_tokens(
        formal,
        (
            "WeightedDecisionEvidenceSurface",
            "DecisionEvidenceHandoffBoundary",
            "PlanOSWeightedDecisionEvidenceHandoffBridge",
            "source_weighting_remains_advisory",
            "handoff_is_decision_evidence_only",
            "handoff_grants_no_decision_activation_execution_or_truth",
            "boundary_blocks_selection_and_commit_here",
            "history_appends_one_handoff_record",
            "digest_is_exact",
        ),
    )
    require_tokens(source_formal, ("PlanOSPathIntegralCandidateWeightingBridge", "path_integral_weighting_is_advisory"))
    require_tokens(formal_root, ("KUOS.PlanOS.WeightedDecisionEvidenceHandoffV0_26",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.WeightedDecisionEvidenceHandoffV0_26",))
    require_tokens(
        docs,
        (
            "PlanOS Weighted Decision Evidence Handoff v0.26",
            "DecisionOS-readable evidence handoff",
            "selected candidate committed = false",
            "decision made = false",
            "execution granted = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_plan_os_full_checks.py",
        ("check_planos_weighted_decision_evidence_handoff_v0_26.py", "v0.1-v0.26"),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v026",),
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
    print("PlanOS weighted DecisionOS evidence handoff v0.26 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
