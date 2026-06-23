#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_hysteresis_constraint_decision_handoff_v0_20"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_20.lean"
    top_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationHysteresisConstraintDecisionHandoffV0_20.lean"
    generation = ROOT / "formal/KUOS/PlanOS/VacuumExpectationHistoryQiCandidateGenerationV0_19.lean"
    replan = ROOT / "formal/KUOS/PlanOS/QiConditionedNonMarkovReplanV0_2.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_HYSTERESIS_CONSTRAINT_DECISION_HANDOFF_v0_20.md"
    manifest_path = ROOT / "manifests/kuuos_planos_hysteresis_constraint_decision_handoff_v0_20.json"
    workflow = ROOT / ".github/workflows/planos-hysteresis-constraint-decision-handoff-v0-20.yml"

    for path in (formal_root, top_root, formal, generation, replan, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationHysteresisConstraintDecisionHandoffV0_20"
    require_tokens(formal_root, (import_token,))
    require_tokens(top_root, (import_token,))
    require_tokens(
        formal,
        (
            "CandidateAdmissibilityReceipt",
            "DecisionOSAdmissibleSetHandoff",
            "VacuumExpectationHysteresisConstraintDecisionHandoffBridge",
            "VacuumExpectationHysteresisConstraintDecisionHandoffReceipt",
            "follows_constraint_deliberation_prefix",
            "hold_is_admissible_and_forwarded",
            "included_primary_requires_hysteresis_margin",
            "handoff_preserves_admissible_set",
            "handoff_is_not_selection_or_synthesis",
            "events_append_strictly",
            "history_appends_two_records",
            "preserves_identity_dissent_and_minority",
            "bridge_grants_no_new_authority",
            "digest_is_exact",
        ),
    )
    require_tokens(
        generation,
        (
            "VacuumExpectationHistoryQiCandidateGenerationReceipt",
            "generation_preserves_explicit_hold_alternative",
            "generation_commit_is_not_selection_synthesis_or_activation",
        ),
    )
    require_tokens(
        replan,
        (
            "HysteresisGate",
            "ConstraintBoundary",
            "DecisionSelectionBoundary",
            "switching_candidate_requires_hysteresis_margin",
            "admissible_candidate_preserves_mission_and_authority",
        ),
    )
    require_tokens(
        docs,
        (
            "holdは必須の適格代替",
            "DecisionSelectionBoundary supplied",
            "constraint pass != candidate selection",
            "DecisionOS handoff != DecisionOS selection receipt",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v020",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "source_generation_required",
        "hysteresis_gate_required",
        "constraint_boundary_required",
        "hold_admissible_and_forwarded",
        "admissible_set_nonempty",
        "candidate_identities_preserved",
        "alternatives_preserved",
        "dissent_visible",
        "minority_preserved",
        "constraint_owner_planos",
        "selection_owner_decisionos",
        "synthesis_owner_planos",
        "execution_owner_actos",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    require(boundaries["phase_event_append_count"] == 2, "phase append count mismatch")
    for field in (
        "selection_receipt_supplied",
        "selection_performed",
        "plan_synthesized",
        "replan_activated",
        "plan_activated",
        "execution_permitted",
        "host_license_granted",
        "memory_overwritten",
        "world_updated",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("PlanOS hysteresis constraint DecisionOS handoff v0.20 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
