#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_learnos_world_host_effect_future_only_learning_v0_4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/LearnOS/WorldHostEffectVerificationFutureOnlyLearningV0_4.lean"
    formal_root = ROOT / "formal/KuuOSLearnOSV0_4.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_LEARNOS_WORLD_HOST_EFFECT_FUTURE_ONLY_LEARNING_v0_4.md"
    manifest_path = ROOT / "manifests/kuuos_learnos_world_host_effect_future_only_learning_v0_4.json"
    workflow = ROOT / ".github/workflows/learnos-world-host-effect-v0-4.yml"

    for path in (formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.LearnOS.WorldHostEffectVerificationFutureOnlyLearningV0_4"
    require_tokens(formal_root, ("import KUOS", import_token))
    require_tokens(aggregate_root, ("import KUOS",))
    require_tokens(
        formal,
        (
            "WorldDispositionLearningBoundary",
            "LearningReceiptCommitBoundary",
            "WorldHostEffectVerificationLearningBridge",
            "WorldHostEffectVerificationLearningReceipt",
            "world_learning_requires_committed_verification",
            "world_learning_preserves_verification_lineage",
            "world_learning_preserves_evidence_uncertainty_and_qi",
            "world_passed_verification_yields_reinforcement_or_hold",
            "world_failed_verification_yields_repair_or_hold",
            "world_indeterminate_verification_yields_reobservation_or_hold",
            "world_learning_delta_remains_future_only",
            "world_disposition_remains_candidate_and_commit_separate",
            "world_learning_requires_replan_without_activation",
            "world_learning_receipt_is_immutable_append_only_and_replay_safe",
            "world_learning_events_append_after_verification",
            "world_learning_history_appends_one_record",
            "world_learning_grants_no_downstream_authority",
            "world_learning_receipt_digest_is_exact",
        ),
    )
    require_tokens(
        docs,
        (
            "future only = true",
            "active now = false",
            "fresh commit authorization supplied = false",
            "automatic WORLD commit = false",
            "learning != replan activation",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_learnos_v04",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["formal_root"] == str(formal_root.relative_to(ROOT)), "formal root mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {field}")

    print("LearnOS world host-effect future-only learning v0.4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
