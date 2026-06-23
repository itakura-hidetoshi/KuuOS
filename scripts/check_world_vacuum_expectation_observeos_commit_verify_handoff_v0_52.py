#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

# Comment-only diagnostic marker for the narrow v0.52 validator and full-check.
ROOT = pathlib.Path(__file__).resolve().parents[1]


def require_tokens(path: pathlib.Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        assert token in text, f"{path}: {token}"


def main() -> int:
    formal = (
        ROOT
        / "formal/KUOS/WORLD/VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52.lean"
    )
    require_tokens(
        formal,
        (
            "WorldVacuumExpectationOSReceiptCompositionBridge",
            "VacuumExpectationOSReceiptComposition",
            "VacuumExpectationIntakeCommitReceiptV0_3",
            "VacuumExpectationCommitVerificationReceiptV0_3",
            "VacuumExpectationVerificationFutureOnlyDeltaV0_3",
            "composition_lineage_digest_exact",
            "observe_stage_composes_exactly",
            "verification_stage_composes_exactly",
            "learning_stage_is_future_only",
            "os_ownership_boundary_preserved",
            "composed_candidate_value_remains_exact",
            "composition_preserves_non_authority",
            "runtime_remains_read_only",
            "worldConstructsObserveReceipt",
            "worldConstructsVerificationReceipt",
            "worldConstructsLearningReceipt",
        ),
    )

    require_tokens(
        ROOT / "formal/KUOS/ObserveOS/VacuumExpectationIntakeCommitReceiptV0_3.lean",
        (
            "VacuumExpectationIntakeCommitReceipt",
            "explicit_receipt_records_observation",
            "commit_preserves_verification_debt",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/VerifyOS/VacuumExpectationCommitVerificationReceiptV0_3.lean",
        (
            "VacuumExpectationCommitVerificationReceipt",
            "verification_verdict_and_record_are_exact",
            "verification_never_becomes_truth_or_causality",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/LearnOS/VacuumExpectationVerificationFutureOnlyDeltaV0_3.lean",
        (
            "VacuumExpectationVerificationLearningReceipt",
            "learning_delta_remains_future_only",
            "learning_commit_requires_replan_but_not_activation",
        ),
    )

    require_tokens(
        ROOT / "formal/KuuOSFormalV0_52.lean",
        ("VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52",),
    )
    require_tokens(
        ROOT / "formal/KUOS.lean",
        ("KUOS.WORLD.VacuumExpectationObserveOSCommitVerifyHandoffBridgeV0_52",),
    )
    require_tokens(ROOT / "lakefile.toml", ("KuuOSFormalV0_52",))
    require_tokens(
        ROOT / "docs/KU_WORLD_VACUUM_EXPECTATION_OBSERVEOS_COMMIT_VERIFY_HANDOFF_v0_52.md",
        (
            "receipt composition != receipt construction",
            "verification result != truth",
            "learning receipt != current-cycle mutation",
            "WORLD sidecar != LearnOS owner",
            "runtime remains read-only",
        ),
    )
    require_tokens(
        ROOT / "README.md",
        (
            "WORLD read-only mathematical sidecar             v0.52",
            "LearnOS WORLD-derived future-only delta          v0.3",
            "receipt composition != receipt construction",
            "run_kuuos_runtime_full_check_v0_52.py",
        ),
    )
    require_tokens(
        ROOT / "ROADMAP.md",
        (
            "implemented through v0.52",
            "OS receipt composition",
            "Strengthen WORLD v0.52 proof status",
        ),
    )

    manifest_path = (
        ROOT
        / "manifests/world_vacuum_expectation_observeos_commit_verify_handoff_v0_52.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert (
        manifest["manifest_version"]
        == "world_vacuum_expectation_observeos_commit_verify_handoff_v0_52"
    )
    assert manifest["status"] == "formal_read_only_os_receipt_composition_bridge"
    assert manifest["formal_root"] == "formal/KuuOSFormalV0_52.lean"
    assert manifest["formal_module"] == str(formal.relative_to(ROOT))
    assert len(manifest["composes_existing_modules"]) == 3
    assert "receipt_composition_not_receipt_construction" in manifest["boundaries"]
    assert "verification_result_not_truth" in manifest["boundaries"]
    assert "learning_future_only" in manifest["boundaries"]
    assert "world_not_learnos_owner" in manifest["boundaries"]
    assert "runtime_read_only" in manifest["boundaries"]
    assert "composition_lineage_digest_exact" in manifest["derived_results"]
    assert "learning_stage_is_future_only" in manifest["derived_results"]

    print("world_vacuum_expectation_os_receipt_composition_v0_52 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
