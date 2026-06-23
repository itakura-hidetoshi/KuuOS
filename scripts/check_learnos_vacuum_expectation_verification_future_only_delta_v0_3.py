#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_learnos_vacuum_expectation_verification_future_only_delta_v0_3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal_root = ROOT / "formal/KuuOSLearnOSV0_3.lean"
    top_root = ROOT / "formal/KuuOSFormal.lean"
    formal = ROOT / "formal/KUOS/LearnOS/VacuumExpectationVerificationFutureOnlyDeltaV0_3.lean"
    verify = ROOT / "formal/KUOS/VerifyOS/VacuumExpectationCommitVerificationReceiptV0_3.lean"
    docs = ROOT / "docs/KUUOS_LEARNOS_VACUUM_EXPECTATION_VERIFICATION_FUTURE_ONLY_DELTA_v0_3.md"
    manifest_path = ROOT / "manifests/kuuos_learnos_vacuum_expectation_verification_future_only_delta_v0_3.json"
    workflow = ROOT / ".github/workflows/learnos-vacuum-expectation-verification-future-only-v0-3.yml"

    for path in (formal_root, top_root, formal, verify, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.LearnOS.VacuumExpectationVerificationFutureOnlyDeltaV0_3"
    require_tokens(formal_root, (import_token,))
    require_tokens(top_root, (import_token,))
    require_tokens(
        formal,
        (
            "learningRouteOfKind",
            "VacuumExpectationVerificationLearningBridge",
            "VacuumExpectationVerificationLearningReceipt",
            "learning_requires_explicit_verification",
            "learning_receipt_digest_is_exact",
            "learning_index_appends_exactly_once",
            "passed_verification_yields_reinforcement_or_hold",
            "failed_verification_yields_repair_or_hold",
            "indeterminate_verification_yields_reobservation_or_hold",
            "learning_delta_remains_future_only",
            "learning_commit_requires_replan_but_not_activation",
            "admissible_learning_preserves_middle_way",
            "learning_history_appends_exactly_once",
            "learning_bridge_grants_no_downstream_authority",
            "learned_candidate_value_remains_exact",
        ),
    )
    require_tokens(
        verify,
        (
            "verificationRecorded",
            "learningRequired",
            "verification_bridge_grants_no_downstream_authority",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/LearnOS/FutureOnlyEvidenceLearningV0_1.lean",
        (
            "VerdictKindCompatibility",
            "LearningDeltaBoundary",
            "TwoTruthsMiddleWayBoundary",
            "LearningDebtSemantics",
            "LearnEventIndex",
            "LearnHistory",
        ),
    )
    require_tokens(
        docs,
        (
            "passed        → reinforcement or hold",
            "failed        → repair or hold",
            "indeterminate → reobservation or hold",
            "learning receipt != Replan activation",
            "learning receipt != execution permission",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_51.py",
        ("check_learnos_v03",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "source_verification_required",
        "explicit_learning_receipt_required",
        "learning_index_append_once",
        "future_only",
        "current_cycle_unchanged",
        "past_records_unchanged",
        "replan_handoff_required",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    for field in (
        "active_now",
        "automatic_replan_activation",
        "automatic_plan_activation",
        "automatic_execution",
        "automatic_memory_overwrite",
        "automatic_world_update",
        "truth_authority_granted",
        "causal_authority_granted",
        "self_modification_authority_granted",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("LearnOS vacuum expectation verification future-only delta v0.3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
