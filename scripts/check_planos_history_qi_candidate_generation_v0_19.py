#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_history_qi_candidate_generation_v0_19"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_19.lean"
    top_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationHistoryQiCandidateGenerationV0_19.lean"
    intake = ROOT / "formal/KUOS/PlanOS/VacuumExpectationLearningReplanIntakeV0_18.lean"
    replan = ROOT / "formal/KUOS/PlanOS/QiConditionedNonMarkovReplanV0_2.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_HISTORY_QI_CANDIDATE_GENERATION_v0_19.md"
    manifest_path = ROOT / "manifests/kuuos_planos_history_qi_candidate_generation_v0_19.json"
    workflow = ROOT / ".github/workflows/plan-os-validation.yml"

    for path in (
        formal_root,
        top_root,
        formal,
        intake,
        replan,
        docs,
        manifest_path,
        workflow,
    ):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationHistoryQiCandidateGenerationV0_19"
    require_tokens(formal_root, (import_token,))
    require_tokens(top_root, (import_token,))
    require_tokens(
        formal,
        (
            "replanCandidateOfLearningKind",
            "VacuumExpectationHistoryQiCandidateGenerationBridge",
            "VacuumExpectationHistoryQiCandidateGenerationReceipt",
            "generation_requires_exact_planos_intake",
            "generation_follows_deterministic_phase_prefix",
            "generation_phase_events_append_strictly",
            "generation_history_is_nonmarkov_and_read_only",
            "generation_qi_is_context_without_authority",
            "passed_verification_generates_strengthen_or_hold",
            "failed_verification_generates_repair_or_hold",
            "indeterminate_verification_generates_reobserve_or_hold",
            "generation_preserves_explicit_hold_alternative",
            "generation_history_appends_three_phase_records",
            "generation_commit_is_not_selection_synthesis_or_activation",
            "generation_preserves_os_ownership",
            "generation_bridge_grants_no_new_authority",
            "generation_digest_is_exact",
            "generated_candidate_value_remains_exact",
        ),
    )
    require_tokens(
        intake,
        (
            "VacuumExpectationLearningReplanIntakeReceipt",
            "intake_event_index_appends_exactly_once",
            "intake_commit_is_not_activation_plan_or_execution",
        ),
    )
    require_tokens(
        replan,
        (
            "NonMarkovHistoryBoundary",
            "QiReplanBoundary",
            "ReplanCandidateType",
            "ReplanPhase",
            "ReplanEventIndex",
            "ReplanHistory",
        ),
    )
    require_tokens(
        docs,
        (
            "reinforcement → strengthen",
            "passed        → strengthen or hold",
            "candidate generation owner = PlanOS",
            "candidate selection owner  = DecisionOS",
            "candidate generation != plan synthesis",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v019",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    require(manifest["candidate_mapping"]["reinforcement"] == "strengthen", "reinforcement mapping mismatch")
    require(manifest["candidate_mapping"]["repair"] == "repair", "repair mapping mismatch")
    require(manifest["candidate_mapping"]["reobservation"] == "reobserve", "reobservation mapping mismatch")
    require(manifest["candidate_mapping"]["hold"] == "hold", "hold mapping mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "exact_planos_intake_required",
        "nonmarkov_history_required",
        "history_read_only",
        "qi_context_required",
        "hold_alternative_preserved",
        "candidate_generation_owned_by_planos",
        "candidate_selection_owned_by_decisionos",
        "plan_synthesis_owned_by_planos",
        "execution_owned_by_actos",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    require(boundaries["phase_event_append_count"] == 3, "phase append count mismatch")
    for field in (
        "qi_authority_granted",
        "candidate_selected",
        "plan_synthesized",
        "replan_activated",
        "plan_activated",
        "execution_permitted",
        "host_license_granted",
        "memory_overwritten",
        "world_updated",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("PlanOS history Qi candidate generation v0.19 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
