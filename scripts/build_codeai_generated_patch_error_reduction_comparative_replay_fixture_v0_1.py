#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.kuuos_codeai_generated_patch_error_baseline_replay_evaluation_v0_1 import (
    CASE_DIGEST_FIELD,
    CASE_PROFILE_VERSION,
    DATASET_DIGEST_FIELD,
    DATASET_PROFILE_VERSION,
    POLICY_DIGEST_FIELD as SOURCE_POLICY_DIGEST_FIELD,
    PROFILE_VERSION as SOURCE_PROFILE_VERSION,
    REQUEST_DIGEST_FIELD as SOURCE_REQUEST_DIGEST_FIELD,
    SCHEMA_VERSION,
    STAGE_FAILED,
    STAGE_NOT_RUN,
    STAGE_PASSED,
    VERIFICATION_NOT_RUN,
    VERIFICATION_PASSED,
    build_codeai_generated_patch_error_baseline_replay_evaluation,
    seal,
)
from runtime.kuuos_codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1 import (
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    build_codeai_generated_patch_error_reduction_comparative_replay_evaluation,
)

REPOSITORY = "itakura-hidetoshi/KuuOS"


def _digest(char: str) -> str:
    return char * 64


def _git_sha(char: str) -> str:
    return char * 40


def _make_case(
    *,
    case_id: str,
    candidate_char: str,
    stages: tuple[str, str, str, str, str, str],
    verification_status: str,
    repair_cycle_count: int,
    repair_reached_green: bool,
    provider_call_count: int,
    generated_output_bytes: int,
    error_fingerprints: list[str],
    observed_epoch: int,
) -> dict[str, Any]:
    application_required = stages[1] != STAGE_NOT_RUN
    verification_execution_required = any(
        stage != STAGE_NOT_RUN for stage in stages[4:]
    )
    independent_required = verification_status != VERIFICATION_NOT_RUN
    return seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": CASE_PROFILE_VERSION,
            "case_id": case_id,
            "repository_full_name": REPOSITORY,
            "source_commit_sha": _git_sha(candidate_char),
            "candidate_digest": _digest(candidate_char),
            "patch_artifact_digest": _digest(chr(ord(candidate_char) + 1)),
            "generation_receipt_digest": _digest(chr(ord(candidate_char) + 2)),
            "application_receipt_digest": (
                _digest(chr(ord(candidate_char) + 3))
                if application_required
                else None
            ),
            "verification_execution_receipt_digest": (
                _digest(chr(ord(candidate_char) + 4))
                if verification_execution_required
                else None
            ),
            "independent_verification_receipt_digest": (
                _digest(chr(ord(candidate_char) + 5))
                if independent_required
                else None
            ),
            "provider_id": "gpt",
            "model_id": "model-v1",
            "structured_output_status": stages[0],
            "patch_application_status": stages[1],
            "parse_status": stages[2],
            "typecheck_status": stages[3],
            "targeted_test_status": stages[4],
            "full_regression_status": stages[5],
            "independent_verification_status": verification_status,
            "repair_cycle_count": repair_cycle_count,
            "repair_reached_green": repair_reached_green,
            "provider_call_count": provider_call_count,
            "generated_output_bytes": generated_output_bytes,
            "error_fingerprints": error_fingerprints,
            "observed_epoch": observed_epoch,
        },
        CASE_DIGEST_FIELD,
    )


def _make_source_bundle(*, successor: bool) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if successor:
        cases = [
            _make_case(
                case_id="case-pass",
                candidate_char="4",
                stages=(STAGE_PASSED,) * 6,
                verification_status=VERIFICATION_PASSED,
                repair_cycle_count=0,
                repair_reached_green=False,
                provider_call_count=2,
                generated_output_bytes=1000,
                error_fingerprints=[],
                observed_epoch=200,
            ),
            _make_case(
                case_id="case-type-fail",
                candidate_char="5",
                stages=(STAGE_PASSED,) * 6,
                verification_status=VERIFICATION_PASSED,
                repair_cycle_count=0,
                repair_reached_green=False,
                provider_call_count=1,
                generated_output_bytes=450,
                error_fingerprints=[],
                observed_epoch=200,
            ),
            _make_case(
                case_id="case-repaired",
                candidate_char="6",
                stages=(STAGE_PASSED,) * 6,
                verification_status=VERIFICATION_PASSED,
                repair_cycle_count=1,
                repair_reached_green=True,
                provider_call_count=2,
                generated_output_bytes=1200,
                error_fingerprints=[],
                observed_epoch=200,
            ),
        ]
        dataset_id = "successor-dataset-001"
        evaluation_id = "successor-evaluation-001"
        evaluator_id = "codeai-successor-evaluator"
        window_start, window_end = 190, 210
        request_epoch, evaluation_epoch = 220, 225
    else:
        cases = [
            _make_case(
                case_id="case-pass",
                candidate_char="1",
                stages=(STAGE_PASSED,) * 6,
                verification_status=VERIFICATION_PASSED,
                repair_cycle_count=0,
                repair_reached_green=False,
                provider_call_count=2,
                generated_output_bytes=1000,
                error_fingerprints=[],
                observed_epoch=100,
            ),
            _make_case(
                case_id="case-type-fail",
                candidate_char="2",
                stages=(
                    STAGE_PASSED,
                    STAGE_PASSED,
                    STAGE_PASSED,
                    STAGE_FAILED,
                    STAGE_NOT_RUN,
                    STAGE_NOT_RUN,
                ),
                verification_status=VERIFICATION_NOT_RUN,
                repair_cycle_count=0,
                repair_reached_green=False,
                provider_call_count=1,
                generated_output_bytes=500,
                error_fingerprints=["TYPE_MISMATCH"],
                observed_epoch=100,
            ),
            _make_case(
                case_id="case-repaired",
                candidate_char="3",
                stages=(STAGE_PASSED,) * 6,
                verification_status=VERIFICATION_PASSED,
                repair_cycle_count=1,
                repair_reached_green=True,
                provider_call_count=3,
                generated_output_bytes=1500,
                error_fingerprints=["TYPE_MISMATCH"],
                observed_epoch=100,
            ),
        ]
        dataset_id = "baseline-dataset-001"
        evaluation_id = "baseline-evaluation-001"
        evaluator_id = "codeai-baseline-evaluator"
        window_start, window_end = 90, 110
        request_epoch, evaluation_epoch = 120, 125

    dataset = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": DATASET_PROFILE_VERSION,
            "dataset_id": dataset_id,
            "repository_full_name": REPOSITORY,
            "window_start_epoch": window_start,
            "window_end_epoch": window_end,
            "case_digests": [case[CASE_DIGEST_FIELD] for case in cases],
            "cases": cases,
        },
        DATASET_DIGEST_FIELD,
    )
    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": SOURCE_PROFILE_VERSION,
            "evaluation_id": evaluation_id,
            "dataset_digest": dataset[DATASET_DIGEST_FIELD],
            "repository_full_name": REPOSITORY,
            "evaluator_id": evaluator_id,
            "request_created_epoch": request_epoch,
            "compute_stage_baseline": True,
            "compute_error_fingerprint_baseline": True,
            "compute_repair_efficiency": True,
        },
        SOURCE_REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": SOURCE_PROFILE_VERSION,
            "expected_repository_full_name": REPOSITORY,
            "expected_dataset_digest": dataset[DATASET_DIGEST_FIELD],
            "authorized_evaluator_ids": [evaluator_id],
            "maximum_request_age": 20,
            "maximum_cases": 16,
            "maximum_error_fingerprints_per_case": 8,
            "maximum_repair_cycles_per_case": 4,
            "maximum_provider_calls_per_case": 8,
            "maximum_generated_output_bytes_per_case": 10000,
            "evaluation_epoch": evaluation_epoch,
            "require_exact_case_digests": True,
            "require_sequential_stage_evidence": True,
            "allow_read_only_replay_evaluation": True,
            "allow_execution": False,
            "allow_repository_mutation": False,
            "allow_git_effect": False,
            "allow_network_access": False,
            "allow_secret_read": False,
            "allow_selection_authority": False,
            "allow_successor_authority": False,
        },
        SOURCE_POLICY_DIGEST_FIELD,
    )
    return dataset, request, policy


def build_fixture() -> dict[str, Any]:
    baseline_dataset, baseline_request, baseline_policy = _make_source_bundle(
        successor=False
    )
    successor_dataset, successor_request, successor_policy = _make_source_bundle(
        successor=True
    )
    baseline_result = build_codeai_generated_patch_error_baseline_replay_evaluation(
        dataset=baseline_dataset,
        request=baseline_request,
        policy=baseline_policy,
    )
    successor_result = build_codeai_generated_patch_error_baseline_replay_evaluation(
        dataset=successor_dataset,
        request=successor_request,
        policy=successor_policy,
    )
    if baseline_result.evidence is None or baseline_result.receipt is None:
        raise RuntimeError("baseline fixture did not evaluate")
    if successor_result.evidence is None or successor_result.receipt is None:
        raise RuntimeError("successor fixture did not evaluate")

    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "comparison_id": "generated-patch-error-reduction-comparison-001",
            "repository_full_name": REPOSITORY,
            "baseline_evidence_digest": baseline_result.evidence[
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "baseline_receipt_digest": baseline_result.receipt[
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "successor_evidence_digest": successor_result.evidence[
                "codeai_generated_patch_error_baseline_evidence_digest"
            ],
            "successor_receipt_digest": successor_result.receipt[
                "codeai_generated_patch_error_baseline_receipt_digest"
            ],
            "evaluator_id": "codeai-comparative-replay-evaluator",
            "request_created_epoch": 300,
            "compare_stage_pass_rates": True,
            "compare_verification_outcomes": True,
            "compare_error_recurrence": True,
            "compare_repair_and_generation_cost": True,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "expected_repository_full_name": REPOSITORY,
            "expected_baseline_evidence_digest": request["baseline_evidence_digest"],
            "expected_baseline_receipt_digest": request["baseline_receipt_digest"],
            "expected_successor_evidence_digest": request["successor_evidence_digest"],
            "expected_successor_receipt_digest": request["successor_receipt_digest"],
            "authorized_evaluator_ids": ["codeai-comparative-replay-evaluator"],
            "evaluation_epoch": 305,
            "maximum_request_age": 20,
            "require_distinct_dataset_digests": True,
            "require_equal_case_count": True,
            "require_defined_ratio_deltas": True,
            "minimum_independent_verification_pass_rate_delta_basis_points": 0,
            "minimum_verified_patch_count_delta": 1,
            "maximum_typecheck_first_failure_count_delta": -1,
            "maximum_repeated_error_fingerprint_count_delta": -1,
            "maximum_cases_with_repeated_error_fingerprint_delta": -2,
            "maximum_repair_cycles_per_verified_patch_delta_basis_points": 0,
            "maximum_provider_calls_per_verified_patch_delta_basis_points": 0,
            "maximum_generated_output_bytes_per_verified_patch_delta_basis_points": 0,
            "allow_read_only_comparison": True,
            "allow_historical_code_reexecution": False,
            "allow_provider_invocation": False,
            "allow_verification_runner_invocation": False,
            "allow_repository_mutation": False,
            "allow_git_effect": False,
            "allow_network_access": False,
            "allow_secret_read": False,
            "allow_selection_authority": False,
            "allow_successor_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    comparison_result = build_codeai_generated_patch_error_reduction_comparative_replay_evaluation(
        baseline_evidence=baseline_result.evidence,
        baseline_receipt=baseline_result.receipt,
        successor_evidence=successor_result.evidence,
        successor_receipt=successor_result.receipt,
        request=request,
        policy=policy,
    )
    if comparison_result.evidence is None or comparison_result.receipt is None:
        raise RuntimeError("comparative fixture did not evaluate")
    return {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "baseline": {
            "dataset": baseline_dataset,
            "request": baseline_request,
            "policy": baseline_policy,
            "evidence": baseline_result.evidence,
            "receipt": baseline_result.receipt,
        },
        "successor": {
            "dataset": successor_dataset,
            "request": successor_request,
            "policy": successor_policy,
            "evidence": successor_result.evidence,
            "receipt": successor_result.receipt,
        },
        "comparison_request": request,
        "comparison_policy": policy,
        "comparison_evidence": comparison_result.evidence,
        "comparison_receipt": comparison_result.receipt,
        "expected": {
            "status": comparison_result.status,
            "disposition": comparison_result.receipt["codeai_disposition"],
            "error_reduction_confirmed": comparison_result.receipt[
                "error_reduction_confirmed"
            ],
            "comparison_evidence_digest": comparison_result.evidence[
                EVIDENCE_DIGEST_FIELD
            ],
            "comparison_receipt_digest": comparison_result.receipt[
                RECEIPT_DIGEST_FIELD
            ],
        },
    }


def main() -> int:
    output = Path(
        "examples/codeai_generated_patch_error_reduction_comparative_replay_evaluation_v0_1.json"
    )
    output.write_text(
        json.dumps(build_fixture(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
