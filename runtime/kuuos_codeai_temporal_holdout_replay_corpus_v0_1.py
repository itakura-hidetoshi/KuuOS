#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_temporal_holdout_replay_corpus_checks_v0_1 import (
    validate_corpus,
    validate_policy,
    validate_request,
)
from runtime.kuuos_codeai_temporal_holdout_replay_corpus_schema_v0_1 import *


def _blocked(issues: list[str]) -> CodeAITemporalHoldoutReplayCorpusResult:
    return CodeAITemporalHoldoutReplayCorpusResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def build_codeai_temporal_holdout_replay_corpus(
    *, corpus: Mapping[str, Any], request: Mapping[str, Any], policy: Mapping[str, Any]
) -> CodeAITemporalHoldoutReplayCorpusResult:
    corpus_map = mapping(corpus)
    request_map = mapping(request)
    policy_map = mapping(policy)
    issues: list[str] = []
    if corpus_map is None:
        issues.append("corpus_not_mapping")
    if request_map is None:
        issues.append("request_not_mapping")
    if policy_map is None:
        issues.append("policy_not_mapping")
    if issues:
        return _blocked(issues)
    assert corpus_map is not None and request_map is not None and policy_map is not None

    issues.extend(validate_corpus(corpus_map))
    issues.extend(validate_request(request_map))
    issues.extend(validate_policy(policy_map))
    if issues:
        return _blocked(issues)

    if request_map["corpus_id"] != corpus_map["corpus_id"]:
        issues.append("request_corpus_id_mismatch")
    if request_map["repository_full_name"] != corpus_map["repository_full_name"]:
        issues.append("request_repository_mismatch")
    if request_map["corpus_digest"] != corpus_map[CORPUS_DIGEST_FIELD]:
        issues.append("request_corpus_digest_mismatch")
    if policy_map["expected_repository_full_name"] != corpus_map["repository_full_name"]:
        issues.append("policy_repository_mismatch")
    if policy_map["expected_corpus_digest"] != corpus_map[CORPUS_DIGEST_FIELD]:
        issues.append("policy_corpus_digest_mismatch")
    if request_map["evaluator_id"] not in policy_map["authorized_evaluator_ids"]:
        issues.append("evaluator_not_authorized")
    evaluation_epoch = policy_map["evaluation_epoch"]
    request_epoch = request_map["request_created_epoch"]
    if request_epoch > evaluation_epoch:
        issues.append("request_from_future")
    elif evaluation_epoch - request_epoch > policy_map["maximum_request_age"]:
        issues.append("request_stale")

    cutoff = corpus_map["cutoff_epoch"]
    development_start = corpus_map["development_window_start_epoch"]
    development_end = corpus_map["development_window_end_epoch"]
    holdout_start = corpus_map["holdout_window_start_epoch"]
    holdout_end = corpus_map["holdout_window_end_epoch"]
    if not (
        development_start <= development_end <= cutoff < holdout_start <= holdout_end
    ):
        issues.append("temporal_window_order_invalid")

    entries = [dict(item) for item in corpus_map["entries"]]
    development = [item for item in entries if item["split"] == SPLIT_DEVELOPMENT]
    holdout = [item for item in entries if item["split"] == SPLIT_HOLDOUT]
    if len(development) < policy_map["minimum_development_cases"]:
        issues.append("development_case_floor_not_met")
    if len(holdout) < policy_map["minimum_holdout_cases"]:
        issues.append("holdout_case_floor_not_met")

    if policy_map["require_temporal_order"]:
        for item in development:
            if not (
                development_start <= item["observed_epoch"] <= development_end <= cutoff
            ):
                issues.append("development_entry_outside_window:" + item["case_id"])
        for item in holdout:
            if not (
                cutoff < holdout_start <= item["observed_epoch"] <= holdout_end
            ):
                issues.append("holdout_entry_outside_window:" + item["case_id"])

    def overlap(field: str) -> set[str]:
        return {item[field] for item in development} & {item[field] for item in holdout}

    case_overlap = overlap("case_id")
    issue_overlap = overlap("issue_digest")
    replay_overlap = overlap("replay_case_digest")
    if policy_map["require_distinct_case_ids_across_splits"] and case_overlap:
        issues.append("cross_split_case_id_overlap:" + ",".join(sorted(case_overlap)))
    if policy_map["require_distinct_issue_digests_across_splits"] and issue_overlap:
        issues.append("cross_split_issue_digest_overlap")
    if policy_map["require_distinct_replay_case_digests_across_splits"] and replay_overlap:
        issues.append("cross_split_replay_case_digest_overlap")

    missing_scenarios = set(policy_map["required_scenario_classes"]) - {
        item["scenario_class"] for item in entries
    }
    if missing_scenarios:
        issues.append(
            "required_scenario_classes_missing:" + ",".join(sorted(missing_scenarios))
        )

    for field in (
        "environment_digest", "provider_configuration_digest",
        "evaluation_protocol_digest",
    ):
        if len({item[field] for item in entries}) != 1:
            issues.append("uniform_binding_violated:" + field)

    for item in holdout:
        if (
            policy_map["require_holdout_hidden_from_candidate_generation"]
            and item["labels_available_to_candidate_generation"]
        ):
            issues.append("holdout_label_exposed:" + item["case_id"])
        for policy_field, entry_field, code in (
            (
                "require_holdout_excluded_from_threshold_tuning",
                "used_for_threshold_tuning", "holdout_used_for_threshold_tuning",
            ),
            (
                "require_holdout_excluded_from_memory_training",
                "used_for_memory_training", "holdout_used_for_memory_training",
            ),
            (
                "require_holdout_excluded_from_prompt_selection",
                "used_for_prompt_selection", "holdout_used_for_prompt_selection",
            ),
            (
                "require_holdout_excluded_from_model_selection",
                "used_for_model_selection", "holdout_used_for_model_selection",
            ),
        ):
            if policy_map[policy_field] and item[entry_field]:
                issues.append(code + ":" + item["case_id"])

    for field in (
        "content_addressed", "temporal_split_frozen",
        "holdout_hidden_from_candidate_generation",
        "holdout_excluded_from_threshold_tuning",
        "holdout_excluded_from_memory_training",
        "holdout_excluded_from_prompt_selection",
        "holdout_excluded_from_model_selection",
    ):
        if corpus_map[field] is not True:
            issues.append("corpus_required_true:" + field)

    if issues:
        return _blocked(issues)

    available_scenarios = sorted({item["scenario_class"] for item in entries})
    evidence = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "corpus_id": corpus_map["corpus_id"],
            "repository_full_name": corpus_map["repository_full_name"],
            "cutoff_commit_sha": corpus_map["cutoff_commit_sha"],
            "cutoff_epoch": cutoff,
            "corpus_digest": corpus_map[CORPUS_DIGEST_FIELD],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "development_case_count": len(development),
            "holdout_case_count": len(holdout),
            "scenario_classes": available_scenarios,
            "cross_split_case_id_overlap_count": len(case_overlap),
            "cross_split_issue_digest_overlap_count": len(issue_overlap),
            "cross_split_replay_case_digest_overlap_count": len(replay_overlap),
            "uniform_environment_binding_verified": True,
            "uniform_provider_configuration_binding_verified": True,
            "uniform_evaluation_protocol_binding_verified": True,
            "temporal_order_verified": True,
            "holdout_hidden_from_candidate_generation": True,
            "holdout_excluded_from_threshold_tuning": True,
            "holdout_excluded_from_memory_training": True,
            "holdout_excluded_from_prompt_selection": True,
            "holdout_excluded_from_model_selection": True,
            "read_only_corpus_sealing_completed": True,
            "historical_code_reexecuted": False,
            "provider_invoked": False,
            "verification_runner_invoked": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "selection_authority_granted": False,
            "successor_stage_authority_granted": False,
            "representativeness_claimed": False,
            "randomness_claimed": False,
            "unbiasedness_claimed": False,
            "correctness_proof_claimed": False,
        },
        EVIDENCE_DIGEST_FIELD,
    )
    receipt = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "codeai_disposition": DISPOSITION_SEALED,
            "corpus_id": corpus_map["corpus_id"],
            "repository_full_name": corpus_map["repository_full_name"],
            "corpus_digest": corpus_map[CORPUS_DIGEST_FIELD],
            "request_digest": request_map[REQUEST_DIGEST_FIELD],
            "policy_digest": policy_map[POLICY_DIGEST_FIELD],
            "evidence_digest": evidence[EVIDENCE_DIGEST_FIELD],
            "development_case_count": len(development),
            "holdout_case_count": len(holdout),
            "route_receipt_recorded": True,
            "temporal_holdout_corpus_sealed": True,
            "holdout_protection_verified": True,
            "read_only_corpus_sealing_completed": True,
            "historical_code_reexecuted": False,
            "provider_invoked": False,
            "verification_runner_invoked": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
            "network_accessed": False,
            "secret_material_read": False,
            "selection_authority_granted": False,
            "successor_stage_authority_granted": False,
            "representativeness_claimed": False,
            "randomness_claimed": False,
            "unbiasedness_claimed": False,
            "correctness_proof_claimed": False,
        },
        RECEIPT_DIGEST_FIELD,
    )
    return CodeAITemporalHoldoutReplayCorpusResult(STATUS_READY, (), evidence, receipt)


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAITemporalHoldoutReplayCorpusResult",
    "build_codeai_temporal_holdout_replay_corpus",
    "canonical_digest", "canonical_json", "digest_without", "seal",
]
