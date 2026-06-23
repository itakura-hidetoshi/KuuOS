#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_world_host_effect_replan_intake_v0_24"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/PlanOS/WorldHostEffectLearningReplanIntakeV0_24.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_24.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_WORLD_HOST_EFFECT_REPLAN_INTAKE_v0_24.md"
    manifest_path = ROOT / "manifests/kuuos_planos_world_host_effect_replan_intake_v0_24.json"
    workflow = ROOT / ".github/workflows/planos-world-host-effect-replan-intake-v0-24.yml"

    for path in (formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.PlanOS.WorldHostEffectLearningReplanIntakeV0_24"
    require_tokens(formal_root, ("import KUOS", import_token))
    require_tokens(aggregate_root, ("import KUOS",))
    require_tokens(
        formal,
        (
            "WorldDispositionReplanBoundary",
            "ReplanIntakeReceiptBoundary",
            "WorldHostEffectLearningReplanIntakeBridge",
            "WorldHostEffectLearningReplanIntakeReceipt",
            "intake_requires_committed_future_only_learning",
            "intake_binds_existing_replan_source",
            "intake_enters_pristine_planos_bind",
            "intake_preserves_future_boundary",
            "intake_preserves_world_disposition_candidate",
            "intake_preserves_planos_decisionos_actos_ownership",
            "intake_commit_is_not_activation_generation_selection_or_execution",
            "intake_receipt_is_immutable_append_only_and_replay_safe",
            "intake_event_index_appends_exactly_once",
            "intake_history_appends_one_record",
            "intake_grants_no_downstream_authority",
            "intake_digest_is_exact",
        ),
    )
    require_tokens(
        docs,
        (
            "learning inactive now = true",
            "replan intake resolves WORLD disposition = false",
            "candidate generation = false",
            "candidate selection = false",
            "plan synthesis = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_planos_v024",),
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

    print("PlanOS world host-effect replan intake v0.24 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
