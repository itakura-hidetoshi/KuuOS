#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_decisionos_world_selection_v0_5"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    core = ROOT / "formal/KUOS/DecisionOS/WorldHostEffectAdmissibleSelectionCoreV0_5.lean"
    bridge = ROOT / "formal/KUOS/DecisionOS/WorldSelectionBridgeV0_5.lean"
    receipt = ROOT / "formal/KUOS/DecisionOS/WorldSelectionReceiptV0_5.lean"
    types = ROOT / "formal/KUOS/DecisionOS/WorldHostEffectAdmissibleSelectionTypesV0_5.lean"
    formal = ROOT / "formal/KUOS/DecisionOS/SelectionV0_5.lean"
    formal_root = ROOT / "formal/KuuOSDecisionOSV0_5.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_DECISIONOS_WORLD_SELECTION_v0_5.md"
    manifest_path = ROOT / "manifests/kuuos_decisionos_world_selection_v0_5.json"
    workflow = ROOT / ".github/workflows/decisionos-world-selection-v0-5.yml"

    for path in (
        core,
        bridge,
        receipt,
        types,
        formal,
        formal_root,
        aggregate_root,
        docs,
        manifest_path,
        workflow,
    ):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        core,
        (
            "WorldDispositionSelectionBoundary",
            "DecisionSelectionReceiptBoundary",
            "selection_preserves_world_disposition",
            "decision_selection_receipt_is_replay_safe",
        ),
    )
    require_tokens(
        bridge,
        (
            "SourceConstraintReceiptV0_5",
            "WorldHostEffectAdmissibleSelectionBridge",
            "runtimeResolvesWorldDisposition",
        ),
    )
    require_tokens(
        receipt,
        (
            "WorldHostEffectAdmissibleSelectionReceipt",
            "selectedFromAdmissibleSet",
            "sourceSelectionNotPerformed",
            "digestExact",
        ),
    )
    require_tokens(types, ("WorldSelectionBridgeV0_5", "WorldSelectionReceiptV0_5"))
    require_tokens(
        formal,
        (
            "selection_requires_unselected_decisionos_handoff",
            "selected_candidate_is_from_admissible_set",
            "selection_preserves_admissibility_identity_and_alternatives",
            "selected_constraint_is_admissible_and_non_authoritative",
            "robust_certificate_separates_every_alternative",
            "wa_gate_preserves_dissent_minority_and_identity",
            "wa_plurality_forbids_silent_substitution",
            "selection_preserves_two_truths_and_middle_way",
            "selection_preserves_world_disposition_candidate",
            "selection_receipt_is_immutable_append_only_and_replay_safe",
            "selection_is_not_truth_execution_license_or_world_resolution",
            "selection_event_and_history_append_once",
            "selection_bridge_preserves_ownership",
            "selection_bridge_grants_no_downstream_authority",
            "selection_digest_is_exact",
        ),
    )
    require_tokens(formal_root, ("import KUOS", "KUOS.DecisionOS.SelectionV0_5"))
    require_tokens(aggregate_root, ("import KUOS",))
    require_tokens(
        docs,
        (
            "source selection performed = false",
            "new selection performed = true",
            "selection resolves WORLD disposition = false",
            "decision is execution = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_decisionos_v05",),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["core_module"] == str(core.relative_to(ROOT)), "core module mismatch")
    require(manifest["bridge_module"] == str(bridge.relative_to(ROOT)), "bridge module mismatch")
    require(manifest["receipt_module"] == str(receipt.relative_to(ROOT)), "receipt module mismatch")
    require(manifest["types_module"] == str(types.relative_to(ROOT)), "types module mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["formal_root"] == str(formal_root.relative_to(ROOT)), "formal root mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")
    for field, value in manifest["required"].items():
        require(value is True, f"required boundary missing: {field}")
    for field, value in manifest["forbidden"].items():
        require(value is False, f"forbidden promotion: {field}")

    print("DecisionOS world selection v0.5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
