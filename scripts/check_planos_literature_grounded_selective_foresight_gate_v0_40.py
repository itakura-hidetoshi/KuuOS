#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from scripts.check_planos_actos_invocation_receipt_v0_39 import _ready_activation_grant
from runtime.kuuos_planos_actos_invocation_receipt_v0_39 import build_actos_invocation_receipt
from runtime.kuuos_planos_literature_grounded_selective_foresight_gate_v0_40 import SOURCE_VERSION, VERSION, build_literature_grounded_selective_foresight_gate

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_literature_grounded_selective_foresight_gate_v0_40"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def _ready_actos_invocation_receipt() -> dict:
    source = _ready_activation_grant()
    return build_actos_invocation_receipt(activation_grant=source).to_dict()


def _literature_evidence() -> dict:
    return {
        "primary_sources": [
            "arXiv:2606.30639",
            "arXiv:2606.27483",
            "arXiv:2509.03581",
            "arXiv:2507.02076",
            "arXiv:2511.08798",
            "arXiv:2603.07670",
            "arXiv:2503.16416",
            "arXiv:2606.16576",
        ],
        "dynamic_planning_compute_accounted": True,
        "selective_foresight_required": True,
        "uncertainty_calibration_required": True,
        "memory_mismatch_review_required": True,
        "counterfactual_coverage_required": True,
        "cost_safety_robustness_evaluation_required": True,
        "execution_granted": False,
    }


def _exercise_runtime() -> None:
    source = _ready_actos_invocation_receipt()
    require(source["version"] == SOURCE_VERSION, "source ActOS invocation receipt version mismatch")
    require("actos_invocation_receipt" in source, "source ActOS invocation receipt missing")
    evidence = _literature_evidence()
    receipt = build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=source,
        literature_evidence=evidence,
    ).to_dict()
    require(receipt["version"] == VERSION, "runtime version mismatch")
    require(receipt["status"] == "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_READY", f"gate status mismatch: {receipt.get('blockers')}")
    require(receipt["selected_candidate_id"] == "repair-route", "selected id mismatch")
    require(receipt["boundary"]["selective_foresight_gate_only"] is True, "gate-only boundary missing")
    require(receipt["boundary"]["literature_grounding_preserved"] is True, "literature grounding missing")
    require(receipt["boundary"]["dynamic_planning_compute_accounted"] is True, "dynamic planning compute not accounted")
    require(receipt["boundary"]["uncertainty_calibration_required"] is True, "uncertainty calibration missing")
    require(receipt["boundary"]["memory_mismatch_review_required"] is True, "memory mismatch review missing")
    require(receipt["boundary"]["counterfactual_coverage_required"] is True, "counterfactual coverage missing")
    require(receipt["boundary"]["execution_granted"] is False, "execution promoted")
    require(receipt["boundary"]["external_commit_granted"] is False, "external commit promoted")
    require(receipt["selective_foresight_gate"]["execution_ready"] is False, "gate leaked execution readiness")

    weak_evidence = dict(evidence)
    weak_evidence["primary_sources"] = ["arXiv:2509.03581"]
    blocked = build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=source,
        literature_evidence=weak_evidence,
    ).to_dict()
    require(blocked["status"] == "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_BLOCKED", "weak literature not blocked")
    require("literature_primary_sources_insufficient" in blocked["blockers"], "insufficient literature blocker missing")

    missing_uncertainty = dict(evidence)
    missing_uncertainty["uncertainty_calibration_required"] = False
    blocked_uncertainty = build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=source,
        literature_evidence=missing_uncertainty,
    ).to_dict()
    require(blocked_uncertainty["status"] == "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_BLOCKED", "missing uncertainty not blocked")
    require("literature_signal_uncertainty_calibration_required_missing" in blocked_uncertainty["blockers"], "uncertainty blocker missing")

    execution_promoted = dict(source)
    boundary = dict(execution_promoted["boundary"])
    boundary["execution_granted"] = True
    execution_promoted["boundary"] = boundary
    blocked_source = build_literature_grounded_selective_foresight_gate(
        actos_invocation_receipt=execution_promoted,
        literature_evidence=evidence,
    ).to_dict()
    require(blocked_source["status"] == "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_BLOCKED", "execution-promoted source not blocked")
    require("source_boundary_execution_granted_promoted" in blocked_source["blockers"], "source execution promotion blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_literature_grounded_selective_foresight_gate_v0_40.py"
    source_runtime = ROOT / "runtime/kuuos_planos_actos_invocation_receipt_v0_39.py"
    formal = ROOT / "formal/KUOS/PlanOS/LiteratureGroundedSelectiveForesightGateV0_40.lean"
    source_formal = ROOT / "formal/KUOS/PlanOS/ActOSInvocationReceiptV0_39.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_40.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_v0_40.md"
    manifest_path = ROOT / "manifests/kuuos_planos_literature_grounded_selective_foresight_gate_v0_40.json"

    for path in (runtime, source_runtime, formal, source_formal, formal_root, aggregate_root, docs, manifest_path):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(runtime, ("build_literature_grounded_selective_foresight_gate", "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_READY", "PLANOS_LITERATURE_GROUNDED_SELECTIVE_FORESIGHT_GATE_BLOCKED", "selective_foresight_gate", "dynamic_planning_compute_accounted", "uncertainty_calibration_required", "memory_mismatch_review_required", "counterfactual_coverage_required", "execution_granted"))
    require_tokens(formal, ("LiteratureGroundedSelectiveForesightGateSurface", "LiteratureGroundedSelectiveForesightGateBoundary", "PlanOSLiteratureGroundedSelectiveForesightGateBridge", "source_invocation_receipt_records_invocation_only", "gate_binds_candidate_and_preserves_pre_execution_state", "literature_grounding_requires_foresight_uncertainty_memory_counterfactual_and_evaluation", "gate_does_not_grant_execution_truth_commit_memory_or_blocker_release", "history_appends_one_selective_foresight_gate_record", "digest_is_exact"))
    require_tokens(source_formal, ("PlanOSActOSInvocationReceiptBridge", "receipt_records_invocation_but_not_execution_or_truth"))
    require_tokens(formal_root, ("KUOS.PlanOS.LiteratureGroundedSelectiveForesightGateV0_40",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.LiteratureGroundedSelectiveForesightGateV0_40",))
    require_tokens(docs, ("PlanOS Literature-Grounded Selective Foresight Gate v0.40", "Self-Evolving World Models", "Learning When to Plan", "Structured Uncertainty", "dynamic planning compute", "selective foresight", "uncertainty calibration", "memory mismatch", "counterfactual coverage", "execution granted = false"))
    require_tokens(ROOT / "scripts/run_plan_os_full_checks.py", ("check_planos_literature_grounded_selective_foresight_gate_v0_40.py", "v0.1-v0.40"))
    require_tokens(ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py", ("check_planos_v040",))

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == SOURCE_VERSION, "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    require(len(manifest["literature_sources"]) >= 4, "literature source count mismatch")
    for field, value in manifest["inputs"].items():
        require(value is True, f"input missing: {field}")
    for field, value in manifest["outputs"].items():
        require(value is True, f"output missing: {field}")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS literature-grounded selective foresight gate v0.40 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
