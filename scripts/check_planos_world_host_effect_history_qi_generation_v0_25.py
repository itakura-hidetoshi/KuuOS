#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_world_host_effect_history_qi_generation_v0_25"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    core = ROOT / "formal/KUOS/PlanOS/WorldHostEffectHistoryQiCandidateGenerationCoreV0_25.lean"
    types = ROOT / "formal/KUOS/PlanOS/WorldHostEffectHistoryQiCandidateGenerationTypesV0_25.lean"
    formal = ROOT / "formal/KUOS/PlanOS/WorldHostEffectHistoryQiCandidateGenerationV0_25.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_25.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_WORLD_HOST_EFFECT_HISTORY_QI_GENERATION_v0_25.md"
    manifest_path = ROOT / "manifests/kuuos_planos_world_host_effect_history_qi_generation_v0_25.json"
    workflow = ROOT / ".github/workflows/planos-world-host-effect-history-qi-v0-25.yml"

    for path in (core, types, formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        core,
        (
            "WorldDispositionGenerationBoundary",
            "CandidateGenerationReceiptBoundary",
            "world_generation_preserves_disposition_candidate",
            "generation_receipt_is_replay_safe",
        ),
    )
    require_tokens(
        types,
        (
            "WorldHostEffectHistoryQiCandidateGenerationBridge",
            "WorldHostEffectHistoryQiCandidateGenerationReceipt",
            "primaryCandidateExact",
            "holdAlternativeExact",
            "historyAppendExact",
        ),
    )
    require_tokens(
        formal,
        (
            "generation_requires_exact_planos_intake",
            "generation_follows_deterministic_phase_prefix",
            "generation_phase_events_append_strictly",
            "generation_history_is_nonmarkov_and_read_only",
            "generation_qi_is_context_without_authority",
            "passed_verification_generates_strengthen_or_hold",
            "failed_verification_generates_repair_or_hold",
            "indeterminate_verification_generates_reobserve_or_hold",
            "generation_preserves_explicit_hold_alternative",
            "generation_preserves_world_disposition_candidate",
            "generation_history_appends_three_phase_records",
            "generation_commit_is_not_selection_synthesis_or_activation",
            "generation_preserves_os_ownership",
            "generation_bridge_grants_no_new_authority",
            "generation_digest_is_exact",
        ),
    )
    import_token = "KUOS.PlanOS.WorldHostEffectHistoryQiCandidateGenerationV0_25"
    require_tokens(formal_root, ("import KUOS", import_token))
    require_tokens(aggregate_root, ("import KUOS",))
    require_tokens(
        docs,
        (
            "generated candidate is WORLD disposition = false",
            "generation resolves WORLD disposition = false",
            "Qi truth authority = false",
            "candidate generation != candidate selection",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_planos_v025",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["core_module"] == str(core.relative_to(ROOT)), "core module mismatch")
    require(manifest["types_module"] == str(types.relative_to(ROOT)), "types module mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["formal_root"] == str(formal_root.relative_to(ROOT)), "formal root mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {field}")

    print("PlanOS world host-effect history Qi generation v0.25 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
