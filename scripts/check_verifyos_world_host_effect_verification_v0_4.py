#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_verifyos_world_host_effect_verification_v0_4"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/VerifyOS/WorldHostEffectVerificationReceiptV0_4.lean"
    formal_root = ROOT / "formal/KuuOSVerifyOSV0_4.lean"
    aggregate_root = ROOT / "formal/KuuOSFormal.lean"
    docs = ROOT / "docs/KUUOS_VERIFYOS_WORLD_HOST_EFFECT_VERIFICATION_v0_4.md"
    manifest_path = ROOT / "manifests/kuuos_verifyos_world_host_effect_verification_v0_4.json"
    workflow = ROOT / ".github/workflows/verifyos-world-host-effect-v0-4.yml"

    for path in (formal, formal_root, aggregate_root, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    import_token = "KUOS.VerifyOS.WorldHostEffectVerificationReceiptV0_4"
    require_tokens(formal_root, (import_token,))
    require_tokens(aggregate_root, (import_token,))
    require_tokens(ROOT / "formal/KUOS.lean", (import_token,))
    require_tokens(
        formal,
        (
            "QualifyingObservationBoundary",
            "IndependentVerificationExecutionBoundary",
            "WorldDispositionCandidate",
            "WorldDispositionCandidateBoundary",
            "VerificationReceiptBoundary",
            "WorldHostEffectVerificationBridge",
            "WorldHostEffectVerificationReceipt",
            "verification_requires_qualifying_observation",
            "qualification_gate_is_complete",
            "nonqualifying_observation_cannot_satisfy_gate",
            "verification_uses_exact_observe_cycle",
            "verification_preserves_full_lineage",
            "source_observation_criterion_and_evidence_are_exact",
            "criterion_challenge_and_falsification_are_complete",
            "verification_execution_is_independent_single_and_replay_safe",
            "passed_verification_maps_to_adopt_candidate",
            "failed_verification_maps_to_reject_candidate",
            "indeterminate_verification_maps_to_defer_or_reobserve",
            "verification_remains_candidate_not_truth_causality_or_commit",
            "verification_learning_handoff_is_future_only",
            "verification_receipt_is_immutable_append_only_and_single_use",
            "verification_events_append_exactly_once",
            "verification_history_appends_one_record",
            "verification_grants_no_downstream_authority",
            "verification_receipt_digest_is_exact",
        ),
    )
    require_tokens(
        docs,
        (
            "qualifying observation supplied = true",
            "fresh commit authorization supplied = false",
            "atomic commit ready = false",
            "automatic WORLD commit = false",
        ),
    )
    require_tokens(
        ROOT / "scripts/run_kuuos_runtime_full_check_v0_52.py",
        ("check_verifyos_v04",),
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

    print("VerifyOS world host-effect verification v0.4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
