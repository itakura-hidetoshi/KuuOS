#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "kuuos_observeos_vacuum_expectation_intake_commit_receipt_v0_3"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_tokens(path: Path, tokens: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for token in tokens:
        require(token in text, f"{path}: missing {token}")


def main() -> int:
    formal = ROOT / "formal/KUOS/ObserveOS/VacuumExpectationIntakeCommitReceiptV0_3.lean"
    docs = ROOT / "docs/KUUOS_OBSERVEOS_VACUUM_EXPECTATION_INTAKE_COMMIT_RECEIPT_v0_3.md"
    manifest_path = ROOT / "manifests/kuuos_observeos_vacuum_expectation_intake_commit_receipt_v0_3.json"
    workflow = ROOT / ".github/workflows/observeos-vacuum-expectation-intake-commit-v0-3.yml"

    for path in (formal, docs, manifest_path, workflow):
        require(path.is_file(), f"missing file: {path}")

    require_tokens(
        formal,
        (
            "VacuumExpectationIntakeCommitBridge",
            "VacuumExpectationIntakeCommitReceipt",
            "source_intake_remains_precommit",
            "explicit_receipt_records_observation",
            "commit_preserves_verification_debt",
            "commit_receipt_digest_is_exact",
            "committed_history_snapshot_is_exact",
            "bridge_grants_no_downstream_authority",
            "committed_candidate_value_remains_exact",
            "historyAfter.committedRecords = historyBefore.committedRecords + 1",
            "worldSidecarCommitsObservation = false",
            "bridgeRuntimeCommitsObservation = false",
            "verificationCompletedByBridge = false",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/WORLD/VacuumExpectationObserveOSEvidenceIntakeBridgeV0_51.lean",
        (
            "observationCommitted",
            "observationCommitForbidden",
            "independentVerificationRequired",
            "intake_ownership_boundary_preserved",
        ),
    )
    require_tokens(
        ROOT / "formal/KUOS/ObserveOS/EffectGroundedObservationV0_1.lean",
        (
            "ComparisonBoundary",
            "ObservationDebtSemantics",
            "ObserveHistory",
            "every_observation_preserves_verification_debt",
        ),
    )
    require_tokens(
        docs,
        (
            "intake envelope != committed observation",
            "explicit ObserveOS receipt != automatic commit",
            "observation commit != verification",
            "verification debt remains open",
        ),
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest["version"] == VERSION, "manifest version mismatch")
    require(manifest["formal_module"] == str(formal.relative_to(ROOT)), "formal module mismatch")
    require(manifest["documentation"] == str(docs.relative_to(ROOT)), "documentation mismatch")
    require(manifest["workflow"] == str(workflow.relative_to(ROOT)), "workflow mismatch")

    boundaries = manifest["boundaries"]
    for field in (
        "source_intake_uncommitted",
        "explicit_observeos_receipt_required",
        "append_exactly_one_observation_record",
        "verifyos_handoff_required",
    ):
        require(boundaries[field] is True, f"required boundary missing: {field}")
    for field in (
        "observation_commit_is_verification",
        "world_sidecar_commits_observation",
        "bridge_runtime_commits_observation",
        "verification_completed_by_bridge",
        "truth_authority_granted",
        "belief_promoted",
        "planos_activated",
        "actos_authority_granted",
        "memory_overwritten",
        "world_updated",
    ):
        require(boundaries[field] is False, f"forbidden promotion: {field}")

    print("ObserveOS vacuum expectation intake commit receipt v0.3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
