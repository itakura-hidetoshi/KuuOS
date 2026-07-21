#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1 import (
    DISPOSITION_CONFIRMED,
    STATUS_READY,
    build_codeai_generated_patch_error_reduction_comparative_replay_evaluation,
)
from scripts.build_codeai_generated_patch_error_reduction_comparative_replay_fixture_v0_1 import (
    build_fixture,
    project_fixture,
)

EXAMPLE = Path(
    "examples/codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1.json"
)


def main() -> int:
    committed = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    rebuilt = build_fixture()
    if committed != project_fixture(rebuilt):
        raise SystemExit("comparative replay fixture is not deterministic")

    result = build_codeai_generated_patch_error_reduction_comparative_replay_evaluation(
        baseline_evidence=rebuilt["baseline"]["evidence"],
        baseline_receipt=rebuilt["baseline"]["receipt"],
        successor_evidence=rebuilt["successor"]["evidence"],
        successor_receipt=rebuilt["successor"]["receipt"],
        request=rebuilt["comparison_request"],
        policy=rebuilt["comparison_policy"],
    )
    if result.status != STATUS_READY:
        raise SystemExit("comparative replay evaluation did not become ready")
    if result.receipt is None or result.evidence is None:
        raise SystemExit("comparative replay evaluation omitted sealed outputs")
    if result.receipt["codeai_disposition"] != DISPOSITION_CONFIRMED:
        raise SystemExit("reference error reduction was not confirmed")
    if not result.receipt["error_reduction_confirmed"]:
        raise SystemExit("reference confirmation flag is false")
    metrics = result.evidence["comparison_metrics"]
    if metrics["verified_patch_count_delta"] != 1:
        raise SystemExit("unexpected verified-patch delta")
    if metrics["first_failure_count_deltas"]["typecheck"] != -1:
        raise SystemExit("unexpected typecheck first-failure delta")
    if metrics["repeated_error_fingerprint_count_delta"] != -1:
        raise SystemExit("unexpected repeated-fingerprint delta")
    if metrics["cases_with_repeated_error_fingerprint_delta"] != -2:
        raise SystemExit("unexpected repeated-error-case delta")
    if not metrics["all_targets_met"]:
        raise SystemExit("reference comparison targets are not all met")
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
        "correctness_proof_claimed",
        "probability_claimed",
        "dataset_unbiasedness_claimed",
    ):
        if result.receipt[field]:
            raise SystemExit("forbidden effect or claim present: " + field)
    print("CodeAI generated-patch error-reduction comparative replay v0.1: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
