#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_vacuum_expectation_learning_replan_intake_v0_18"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSPlanOSV0_18.lean"
    top_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/PlanOS/VacuumExpectationLearningReplanIntakeV0_18.lean"
    learning = ROOT / "formal/KUOS/LearnOS/VacuumExpectationVerificationFutureOnlyDeltaV0_3.lean"
    replan = ROOT / "formal/KUOS/PlanOS/QiConditionedNonMarkovReplanV0_2.lean"
    closed_loop = ROOT / "formal/KUOS/PlanOS/ClosedLoopReplanIntakeAdapterV0_4.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_VACUUM_EXPECTATION_LEARNING_REPLAN_INTAKE_v0_18.md"
    manifest_path = ROOT / "manifests/kuuos_planos_vacuum_expectation_learning_replan_intake_v0_18.json"
    workflow = ROOT / ".github/workflows/planos-vacuum-expectation-learning-replan-intake-v0-18.yml"

    for path in (
        formal_root,
        top_root,
        formal,
        learning,
        replan,
        closed_loop,
        docs,
        manifest_path,
        workflow,
    ):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.VacuumExpectationLearningReplanIntakeV0_18"
    require_tokens(formal_root, (import_token,))
    require_tokens(top_root, (import_token,))
    require_tokens(
        formal,
        (
            "VacuumExpectationLearningReplanIntakeBridge",
            "VacuumExpectationLearningReplanIntakeReceipt",
            "intake_requires_committed_future_only_learning",
            "intake_binds_existing_replan_source",
            "intake_enters_pristine_planos_bind",
            "intake_event_index_appends_exactly_once",
            "intake_history_appends_exactly_once",
            "intake_preserves_planos_decisionos_actos_ownership",
            "intake_commit_is_not_activation_plan_or_execution",
            "intake_future_boundary_preserves_current_and_past",
            "intake_bridge_grants_no_new_authority",
            "intake_digest_is_exact",
            "intake_candidate_value_remains_exact",
        ),
    )
    require_tokens(
        learning,
        (
            "VacuumExpectationVerificationLearningReceipt",
            "learning_delta_remains_future_only",
            "learning_commit_requires_replan_but_not_activation",
        ),
    )
    require_tokens(
        replan,
        (
            "ReplanSourceBinding",
            "ReplanOwnership",
            "ReplanEventIndex",
            "ReplanHistory",
        ),
    )
    require_tokens(
        closed_loop,
        (
            "ClosedLoopBindState",
            "ClosedLoopFutureBoundary",
            "ClosedLoopActivationSeparation",
            "closed_loop_enters_pristine_bind",
        ),
    )
    require_tokens(
        docs,
        (
            "intake commitはreplan activationではない",
            "replan owner = PlanOS",
            "candidate selection owner = DecisionOS",
            "execution owner = ActOS",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_planos_v018",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "source_learning_required",
        "committed_current_plan_required",
        "pristine_bind_required",
        "intake_event_append_once",
        "planos_owns_replan",
        "decisionos_owns_selection",
        "planos_owns_synthesis",
        "actos_owns_execution",
        "future_only",
        "current_cycle_unchanged",
        "past_plan_unchanged",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    for field in (
        "replan_activated",
        "plan_activated",
        "execution_permitted",
        "host_license_granted",
        "memory_overwritten",
        "world_updated",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("PlanOS vacuum expectation learning replan intake v0.18 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
