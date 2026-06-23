#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_planos_world_host_effect_constraint_handoff_v0_26"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    core = ROOT / "formal/KUOS/PlanOS/WorldHostEffectConstraintDecisionHandoffCoreV0_26.lean"
    types = ROOT / "formal/KUOS/PlanOS/WorldHostEffectConstraintDecisionHandoffTypesV0_26.lean"
    formal = ROOT / "formal/KUOS/PlanOS/WorldHostEffectConstraintDecisionHandoffV0_26.lean"
    formal_root = ROOT / "formal/KuuOSPlanOSV0_26.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_PLANOS_WORLD_HOST_EFFECT_CONSTRAINT_HANDOFF_v0_26.md"
    manifest_path = ROOT / "manifests/kuuos_planos_world_host_effect_constraint_handoff_v0_26.json"
    workflow = ROOT / ".github/workflows/planos-world-host-effect-constraint-handoff-v0-26.yml"

    for path in (core, types, formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        core,
        (
            "WorldDispositionConstraintBoundary",
            "ConstraintHandoffReceiptBoundary",
            "constraint_handoff_preserves_world_disposition",
            "constraint_handoff_receipt_is_replay_safe",
        ),
    )
    require_tokens(
        types,
        (
            "WorldHostEffectConstraintDecisionHandoffBridge",
            "WorldHostEffectConstraintDecisionHandoffReceipt",
            "primaryExact",
            "holdExact",
            "holdIncluded",
            "historyExact",
        ),
    )
    require_tokens(
        formal,
        (
            "handoff_requires_committed_generation",
            "follows_constraint_deliberation_prefix",
            "hold_is_admissible_and_forwarded",
            "hold_exemption_is_explicit",
            "included_primary_requires_hysteresis_margin",
            "handoff_preserves_admissible_set",
            "handoff_is_not_selection_synthesis_or_execution",
            "handoff_preserves_world_disposition_candidate",
            "constraint_handoff_receipt_is_immutable_and_replay_safe",
            "events_append_strictly",
            "history_appends_two_records",
            "bridge_preserves_os_ownership",
            "bridge_grants_no_new_authority",
            "constraint_handoff_digest_is_exact",
        ),
    )
    import_token = "KUOS.PlanOS.WorldHostEffectConstraintDecisionHandoffV0_26"
    require_tokens(formal_root, ("import KUOS", import_token))
    require_tokens(aggregate_root, ("import KUOS",))
    require_tokens(
        docs,
        (
            "selection receipt supplied = false",
            "selection performed = false",
            "handoff resolves WORLD disposition = false",
            "silent substitution detected = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_planos_v026",),
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

    print("PlanOS world host-effect constraint handoff v0.26 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
