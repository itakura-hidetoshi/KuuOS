#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_observeos_world_host_effect_observation_v0_4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/ObserveOS/WorldHostEffectObservationReceiptV0_4.lean"
    formal_root = ROOT / "formal/KuuOSObserveOSV0_4.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_OBSERVEOS_WORLD_HOST_EFFECT_OBSERVATION_v0_4.md"
    manifest_path = ROOT / "manifests/kuuos_observeos_world_host_effect_observation_v0_4.json"
    workflow = ROOT / ".github/workflows/evidence-cycle-os-validation.yml"

    for path in (formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.ObserveOS.WorldHostEffectObservationReceiptV0_4"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(ROOT / "formal/KUOS.lean", (import_token,))
    require_tokens(
        formal,
        (
            "EffectObservationIdentityBoundary",
            "IndependentEvidenceCollectionBoundary",
            "ObservationReceiptBoundary",
            "WorldCommitObservationPrerequisiteBoundary",
            "WorldHostEffectObservationBridge",
            "WorldHostEffectObservationReceipt",
            "observation_requires_ready_uncommitted_world_intake",
            "observation_uses_exact_act_cycle",
            "observation_preserves_upstream_lineage",
            "source_effect_and_identity_are_exactly_bound",
            "evidence_collection_is_independent_complete_and_single",
            "evidence_contract_reuses_world_intake_requirements",
            "comparison_is_observation_not_verification_truth_or_causality",
            "matched_observation_discharges_observation_debt",
            "divergent_observation_discharges_observation_debt",
            "inconclusive_observation_requires_reobservation",
            "conflicted_observation_requires_reobservation",
            "every_observation_receipt_preserves_verification_debt",
            "observation_receipt_is_immutable_append_only_and_replay_safe",
            "observation_receipt_grants_no_verification_truth_causality_or_world_update",
            "evidence_collection_and_receipt_are_single_use",
            "observation_events_append_strictly",
            "observation_history_appends_two_records",
            "ownership_is_separated",
            "observation_receipt_digest_is_exact",
        ),
    )
    require_tokens(
        docs,
        (
            "host receipt used as independent evidence = false",
            "verification required = true",
            "atomic commit ready = false",
            "receipt immutable = true",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_observeos_v04",),
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

    print("ObserveOS world host-effect observation v0.4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
