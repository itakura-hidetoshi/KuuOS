#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD,
    METRICS_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD,
    STATUS_READY,
    build_codeai_generated_patch_error_baseline_replay_evaluation,
    digest_without,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"
MANIFEST = ROOT / "manifests" / "kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1.json"


def main() -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    result = build_codeai_generated_patch_error_baseline_replay_evaluation(
        dataset=payload["dataset"],
        request=payload["request"],
        policy=payload["policy"],
    )
    expected = payload["expected"]

    assert result.status == STATUS_READY, result.issues
    assert result.issues == ()
    assert result.evidence is not None
    assert result.receipt is not None

    evidence = result.evidence
    receipt = result.receipt
    metrics = evidence["metrics"]

    assert result.status == expected["status"]
    assert metrics["total_case_count"] == expected["total_case_count"]
    assert metrics["verified_patch_count"] == expected["verified_patch_count"]
    assert (
        metrics["stage_metrics"]["typecheck"]["failed_count"]
        == expected["typecheck_failed_count"]
    )
    assert (
        metrics["repeated_error_fingerprint_count"]
        == expected["repeated_error_fingerprint_count"]
    )
    assert (
        metrics["cases_with_repeated_error_fingerprint"]
        == expected["cases_with_repeated_error_fingerprint"]
    )

    assert metrics[METRICS_DIGEST_FIELD] == digest_without(
        metrics, METRICS_DIGEST_FIELD
    )
    assert evidence[EVIDENCE_DIGEST_FIELD] == digest_without(
        evidence, EVIDENCE_DIGEST_FIELD
    )
    assert receipt[RECEIPT_DIGEST_FIELD] == digest_without(
        receipt, RECEIPT_DIGEST_FIELD
    )

    for field in (
        "historical_code_reexecuted",
        "provider_invoked",
        "verification_runner_invoked",
        "repository_mutation_performed",
        "git_effect_performed",
        "network_accessed",
        "secret_material_read",
        "selection_authority_granted",
        "successor_stage_authority_granted",
    ):
        assert evidence[field] is False, field

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["profile_version"] == payload["profile_version"]
    for relative_path in manifest["artifacts"]:
        assert (ROOT / relative_path).exists(), relative_path

    print(
        "CodeAI Generated Patch Error Baseline Replay Evaluation v0.1: "
        f"{metrics['total_case_count']} cases, "
        f"{metrics['verified_patch_count']} verified patches, "
        f"{metrics['stage_metrics']['typecheck']['failed_count']} typecheck failures, "
        f"{metrics['repeated_error_fingerprint_count']} repeated fingerprints"
    )


if __name__ == "__main__":
    main()
