#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from runtime.kuuos_codeai_temporal_holdout_replay_corpus_v0_1 import (
    CORPUS_DIGEST_FIELD,
    DISPOSITION_SEALED,
    ENTRY_DIGEST_FIELD,
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    RECEIPT_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    SCENARIO_CLASSES,
    SCHEMA_VERSION,
    SPLIT_DEVELOPMENT,
    SPLIT_HOLDOUT,
    STATUS_READY,
    build_codeai_temporal_holdout_replay_corpus,
    seal,
)

REPOSITORY = "itakura-hidetoshi/KuuOS"
CUTOFF_COMMIT_SHA = "9df229a76ac2cd6ef2a33b503ee88008c3f8a864"
ENVIRONMENT_DIGEST = "1" * 64
PROVIDER_CONFIGURATION_DIGEST = "2" * 64
EVALUATION_PROTOCOL_DIGEST = "3" * 64


def _digest(seed: int) -> str:
    return format(seed % 16, "x") * 64


def _sha(seed: int) -> str:
    return format(seed % 16, "x") * 40


def _entry(
    *,
    case_id: str,
    seed: int,
    observed_epoch: int,
    split: str,
    scenario_class: str,
) -> dict[str, Any]:
    holdout = split == SPLIT_HOLDOUT
    return seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "case_id": case_id,
            "repository_full_name": REPOSITORY,
            "issue_digest": _digest(seed),
            "source_commit_sha": _sha(seed),
            "observed_epoch": observed_epoch,
            "split": split,
            "scenario_class": scenario_class,
            "replay_case_digest": _digest(seed + 6),
            "environment_digest": ENVIRONMENT_DIGEST,
            "provider_configuration_digest": PROVIDER_CONFIGURATION_DIGEST,
            "evaluation_protocol_digest": EVALUATION_PROTOCOL_DIGEST,
            "labels_available_to_candidate_generation": False if holdout else True,
            "used_for_threshold_tuning": False if holdout else True,
            "used_for_memory_training": False if holdout else True,
            "used_for_prompt_selection": False if holdout else True,
            "used_for_model_selection": False if holdout else True,
        },
        ENTRY_DIGEST_FIELD,
    )


def build_fixture() -> dict[str, Any]:
    entries = [
        _entry(
            case_id="development-verified-patch",
            seed=1,
            observed_epoch=80,
            split=SPLIT_DEVELOPMENT,
            scenario_class="verified_patch",
        ),
        _entry(
            case_id="development-typecheck-failure",
            seed=2,
            observed_epoch=85,
            split=SPLIT_DEVELOPMENT,
            scenario_class="typecheck_failure",
        ),
        _entry(
            case_id="development-overcorrection",
            seed=3,
            observed_epoch=90,
            split=SPLIT_DEVELOPMENT,
            scenario_class="overcorrection",
        ),
        _entry(
            case_id="holdout-test-overfit",
            seed=10,
            observed_epoch=110,
            split=SPLIT_HOLDOUT,
            scenario_class="test_overfit",
        ),
        _entry(
            case_id="holdout-abstention",
            seed=11,
            observed_epoch=115,
            split=SPLIT_HOLDOUT,
            scenario_class="abstention",
        ),
        _entry(
            case_id="holdout-environment-failure",
            seed=12,
            observed_epoch=120,
            split=SPLIT_HOLDOUT,
            scenario_class="environment_failure",
        ),
    ]
    development = [entry for entry in entries if entry["split"] == SPLIT_DEVELOPMENT]
    holdout = [entry for entry in entries if entry["split"] == SPLIT_HOLDOUT]
    corpus = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "corpus_id": "temporal-holdout-corpus-001",
            "repository_full_name": REPOSITORY,
            "cutoff_commit_sha": CUTOFF_COMMIT_SHA,
            "cutoff_epoch": 100,
            "development_window_start_epoch": 70,
            "development_window_end_epoch": 95,
            "holdout_window_start_epoch": 105,
            "holdout_window_end_epoch": 130,
            "entries": entries,
            "entry_digests": [entry[ENTRY_DIGEST_FIELD] for entry in entries],
            "development_entry_digests": [entry[ENTRY_DIGEST_FIELD] for entry in development],
            "holdout_entry_digests": [entry[ENTRY_DIGEST_FIELD] for entry in holdout],
            "development_case_count": len(development),
            "holdout_case_count": len(holdout),
            "scenario_classes": sorted({entry["scenario_class"] for entry in entries}),
            "environment_digest": ENVIRONMENT_DIGEST,
            "provider_configuration_digest": PROVIDER_CONFIGURATION_DIGEST,
            "evaluation_protocol_digest": EVALUATION_PROTOCOL_DIGEST,
            "content_addressed": True,
            "temporal_split_frozen": True,
            "holdout_hidden_from_candidate_generation": True,
            "holdout_excluded_from_threshold_tuning": True,
            "holdout_excluded_from_memory_training": True,
            "holdout_excluded_from_prompt_selection": True,
            "holdout_excluded_from_model_selection": True,
        },
        CORPUS_DIGEST_FIELD,
    )
    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "corpus_id": corpus["corpus_id"],
            "repository_full_name": REPOSITORY,
            "corpus_digest": corpus[CORPUS_DIGEST_FIELD],
            "evaluator_id": "codeai-temporal-holdout-evaluator",
            "request_created_epoch": 140,
            "seal_temporal_holdout_corpus": True,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "expected_repository_full_name": REPOSITORY,
            "expected_corpus_digest": corpus[CORPUS_DIGEST_FIELD],
            "authorized_evaluator_ids": ["codeai-temporal-holdout-evaluator"],
            "evaluation_epoch": 145,
            "maximum_request_age": 20,
            "minimum_development_cases": 3,
            "minimum_holdout_cases": 3,
            "required_scenario_classes": list(SCENARIO_CLASSES),
            "require_temporal_order": True,
            "require_distinct_case_ids_across_splits": True,
            "require_distinct_issue_digests_across_splits": True,
            "require_distinct_replay_case_digests_across_splits": True,
            "require_uniform_environment_digest": True,
            "require_uniform_provider_configuration_digest": True,
            "require_uniform_evaluation_protocol_digest": True,
            "require_holdout_hidden_from_candidate_generation": True,
            "require_holdout_excluded_from_threshold_tuning": True,
            "require_holdout_excluded_from_memory_training": True,
            "require_holdout_excluded_from_prompt_selection": True,
            "require_holdout_excluded_from_model_selection": True,
            "allow_read_only_corpus_sealing": True,
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
    result = build_codeai_temporal_holdout_replay_corpus(
        corpus=corpus,
        request=request,
        policy=policy,
    )
    if result.status != STATUS_READY or result.evidence is None or result.receipt is None:
        raise RuntimeError("temporal holdout fixture blocked: " + ",".join(result.issues))
    if result.receipt["codeai_disposition"] != DISPOSITION_SEALED:
        raise RuntimeError("temporal holdout fixture disposition mismatch")
    return {
        "corpus": corpus,
        "request": request,
        "policy": policy,
        "evidence": result.evidence,
        "receipt": result.receipt,
        "expected": {
            "status": result.status,
            "disposition": result.receipt["codeai_disposition"],
            "development_case_count": 3,
            "holdout_case_count": 3,
            "corpus_digest": corpus[CORPUS_DIGEST_FIELD],
            "evidence_digest": result.evidence[EVIDENCE_DIGEST_FIELD],
            "receipt_digest": result.receipt[RECEIPT_DIGEST_FIELD],
        },
    }


def project_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    corpus = fixture["corpus"]
    evidence = fixture["evidence"]
    receipt = fixture["receipt"]
    return {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "corpus_id": corpus["corpus_id"],
        "repository_full_name": corpus["repository_full_name"],
        "cutoff_commit_sha": corpus["cutoff_commit_sha"],
        "cutoff_epoch": corpus["cutoff_epoch"],
        "development_case_count": corpus["development_case_count"],
        "holdout_case_count": corpus["holdout_case_count"],
        "scenario_classes": corpus["scenario_classes"],
        "corpus_digest": corpus[CORPUS_DIGEST_FIELD],
        "request_digest": fixture["request"][REQUEST_DIGEST_FIELD],
        "policy_digest": fixture["policy"][POLICY_DIGEST_FIELD],
        "evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
        "receipt_digest": receipt[RECEIPT_DIGEST_FIELD],
        "codeai_disposition": receipt["codeai_disposition"],
        "temporal_order_verified": evidence["temporal_order_verified"],
        "cross_split_case_id_overlap_count": evidence["cross_split_case_id_overlap_count"],
        "cross_split_issue_digest_overlap_count": evidence["cross_split_issue_digest_overlap_count"],
        "cross_split_replay_case_digest_overlap_count": evidence["cross_split_replay_case_digest_overlap_count"],
        "holdout_hidden_from_candidate_generation": evidence["holdout_hidden_from_candidate_generation"],
        "holdout_excluded_from_threshold_tuning": evidence["holdout_excluded_from_threshold_tuning"],
        "holdout_excluded_from_memory_training": evidence["holdout_excluded_from_memory_training"],
        "holdout_excluded_from_prompt_selection": evidence["holdout_excluded_from_prompt_selection"],
        "holdout_excluded_from_model_selection": evidence["holdout_excluded_from_model_selection"],
        "representativeness_claimed": evidence["representativeness_claimed"],
        "randomness_claimed": evidence["randomness_claimed"],
        "unbiasedness_claimed": evidence["unbiasedness_claimed"],
    }


def main() -> int:
    output = Path("examples/codeai_temporal_holdout_replay_corpus_v0_1.json")
    output.write_text(
        json.dumps(project_fixture(build_fixture()), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
