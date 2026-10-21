#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_planos_path_integral_candidate_weighting_v0_25 import (
    VERSION,
    build_path_integral_candidate_weighting_receipt,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_VERSION = "kuuos_planos_path_integral_candidate_weighting_v0_25"


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


def _path(mode: str) -> dict:
    return {
        "physical_quantum_qi_path_integral_reentry_considered": True,
        "dominant_reentry_mode": mode,
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


def _blocker(*, missing: bool = False) -> dict:
    return {
        "blocker_classified": True,
        "protective_blocker_preserved": True,
        "situational_blocker_rerouted": True,
        "missing_evidence_held": missing,
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
            "candidate_id": "reobserve-route",
            "candidate_type": "reobserve",
            "estimated_risk": 0.1,
            "candidate_digest": "candidate-digest-reobserve-route",
        },
    ]


def _exercise_runtime() -> None:
    reinforce = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path("reinforce_path_weight"),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    require(reinforce["version"] == VERSION, "runtime version mismatch")
    require(reinforce["status"] == "PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_READY", "reinforce status mismatch")
    require(reinforce["dominant_reentry_mode"] == "reinforce_path_weight", "reinforce mode mismatch")
    require("repair-route" in reinforce["retained_candidate_ids"], "repair candidate not retained")
    require(reinforce["boundary"]["execution_granted"] is False, "execution boundary promoted")
    require(reinforce["boundary"]["selection_authority_granted"] is False, "selection boundary promoted")

    probe = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path("open_probe_potential"),
        qi_process_tensor=_qi(),
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    require(probe["probe_candidate_ids"] == ["repair-route", "reobserve-route"], "probe candidates mismatch")
    require(all(item["probe_required"] is True for item in probe["candidate_weight_receipts"]), "probe flag missing")

    barrier = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path("add_barrier_potential"),
        qi_process_tensor=_qi(),
        blocker=_blocker(missing=True),
        candidates=_candidates(),
    ).to_dict()
    require(barrier["barrier_candidate_ids"] == ["repair-route", "reobserve-route"], "barrier candidates mismatch")
    require(all(item["execution_ready"] is False for item in barrier["candidate_weight_receipts"]), "execution readiness promoted")

    bad_qi = dict(_qi())
    bad_qi["grants_execution_authority"] = True
    blocked = build_path_integral_candidate_weighting_receipt(
        source_gate=_source_gate(),
        path_integral=_path("reinforce_path_weight"),
        qi_process_tensor=bad_qi,
        blocker=_blocker(),
        candidates=_candidates(),
    ).to_dict()
    require(blocked["status"] == "PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_BLOCKED", "authority escalation not blocked")
    require("qi_execution_authority_forbidden" in blocked["blockers"], "qi authority blocker missing")


def main() -> int:
    runtime = ROOT / "runtime/kuuos_planos_path_integral_candidate_weighting_v0_25.py"
    formal = ROOT / "formal/KUOS/PlanOS/PathIntegralCandidateWeightingV0_25.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_25.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_PATH_INTEGRAL_CANDIDATE_WEIGHTING_v0_25.md"
    manifest_path = ROOT / "manifests/kuuos_planos_path_integral_candidate_weighting_v0_25.json"
    source_formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationQiBlockerForesightPlanGateV0_24.lean"

    for path in (runtime, formal, formal_root, aggregate_root, docs, manifest_path, source_formal):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        runtime,
        (
            "build_path_integral_candidate_weighting_receipt",
            "reinforce_path_weight",
            "open_probe_potential",
            "add_barrier_potential",
            "candidate_weighting_advisory_only",
            "selection_authority_granted",
            "execution_granted",
            "blocker_release_granted",
        ),
    )
    require_tokens(
        formal,
        (
            "PathIntegralCandidateWeightSurface",
            "CandidateWeightReceiptBoundary",
            "PlanOSPathIntegralCandidateWeightingBridge",
            "uses_v024_path_integral_evidence",
            "path_integral_weighting_is_advisory",
            "reroute_modes_are_visible",
            "receipt_is_replan_recommendation_only",
            "receipt_grants_no_selection_activation_execution_or_commit",
            "history_appends_one_weighting_record",
            "digest_is_exact",
        ),
    )
    require_tokens(formal_root, ("KUOS.PlanOS.PathIntegralCandidateWeightingV0_25",))
    require_tokens(aggregate_root, ("KUOS.PlanOS.PathIntegralCandidateWeightingV0_25",))
    require_tokens(source_formal, ("PhysicalQuantumQiPathIntegralRerouteEvidence", "path_integral_grants_no_truth_or_execution"))
    require_tokens(
        docs,
        (
            "PlanOS Path Integral Candidate Weighting v0.25",
            "replan recommendation only",
            "selection authority granted = false",
            "execution granted = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_plan_os_full_checks.py",
        ("check_planos_path_integral_candidate_weighting_v0_25.py", "PASS: PlanOS v0.1-v0."),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v025",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == MANIFEST_VERSION, "manifest version mismatch")
    require(manifest["runtime"] == str(runtime.relative_to(ROOT)), "runtime mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "docs mismatch")
    require(manifest["source_version"] == "kuuos_planos_qi_blocker_foresight_plan_gate_v0_24", "source version mismatch")
    require(manifest["history_delta"] == 1, "history delta mismatch")
    for field, value in manifest["inputs"].items():
        require(value is True, f"input missing: {field}")
    for field, value in manifest["outputs"].items():
        require(value is True, f"output missing: {field}")
    for field, value in manifest["reentry_modes"].items():
        require(value is True, f"reentry mode missing: {field}")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["closed"].items():
        require(value is False, f"closed boundary promoted: {field}")

    _exercise_runtime()
    print("PlanOS path integral candidate weighting v0.25 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
