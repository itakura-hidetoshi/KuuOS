from __future__ import annotations

import re
from typing import Any, Mapping

from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1 import *

DIFF_HEADER = re.compile(r"^diff --git a/(.+) b/(.+)$")


def derive_changed_paths(model_patch: str) -> list[str]:
    paths: list[str] = []
    for line in model_patch.splitlines():
        match = DIFF_HEADER.fullmatch(line)
        if not match:
            continue
        left, right = match.groups()
        path = right if right != "/dev/null" else left
        if path not in paths:
            paths.append(path)
    return sorted(paths)


def _valid_path_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and PATH.fullmatch(item) is not None for item in value)
        and len(value) == len(set(value))
        and (bool(value) or not nonempty)
    )


def validate_benchmark_contract(contract: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "benchmark_id",
        "dataset_name",
        "split",
        "expected_instance_count",
        "corpus_digest",
        "instance_ids_digest",
        "harness_repository",
        "harness_commit_sha",
        "harness_entrypoint",
        "prediction_fields",
        "containerized_harness",
        "official_harness",
        "corpus_frozen",
        "test_patch_paths_sealed",
        "contract_created_epoch",
        "harness_execution_performed",
        "network_access_performed",
        "secret_access_performed",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
        CONTRACT_DIGEST_FIELD,
    }
    issues = exact_fields(contract, required, "benchmark_contract")
    if issues:
        return issues
    if contract["schema_version"] != SCHEMA_VERSION or contract["profile_version"] != PROFILE_VERSION:
        issues.append("benchmark_contract_profile_invalid")
    for field in ("benchmark_id", "dataset_name", "split", "harness_repository", "harness_entrypoint"):
        if not isinstance(contract[field], str) or not contract[field]:
            issues.append("benchmark_contract_string_invalid:" + field)
    if not positive_int(contract["expected_instance_count"]):
        issues.append("benchmark_contract_instance_count_invalid")
    for field in ("corpus_digest", "instance_ids_digest"):
        if not isinstance(contract[field], str) or SHA256.fullmatch(contract[field]) is None:
            issues.append("benchmark_contract_digest_invalid:" + field)
    if not isinstance(contract["harness_commit_sha"], str) or SHA40.fullmatch(contract["harness_commit_sha"]) is None:
        issues.append("benchmark_contract_harness_commit_invalid")
    if (
        not isinstance(contract["prediction_fields"], list)
        or tuple(contract["prediction_fields"]) != OFFICIAL_PREDICTION_FIELDS
    ):
        issues.append("benchmark_contract_prediction_fields_invalid")
    for field in (
        "containerized_harness",
        "official_harness",
        "corpus_frozen",
        "test_patch_paths_sealed",
        "harness_execution_performed",
        "network_access_performed",
        "secret_access_performed",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if not isinstance(contract[field], bool):
            issues.append("benchmark_contract_boolean_invalid:" + field)
    if not nonnegative_int(contract["contract_created_epoch"]):
        issues.append("benchmark_contract_epoch_invalid")
    if not digest_ok(contract, CONTRACT_DIGEST_FIELD):
        issues.append("benchmark_contract_digest_mismatch")
    return sorted(set(issues))


def validate_instance_contract(instance: Mapping[str, Any]) -> list[str]:
    required = {
        "instance_id",
        "base_commit_sha",
        "problem_statement_digest",
        "test_patch_digest",
        "protected_test_paths",
        "instance_contract_created_epoch",
        INSTANCE_CONTRACT_DIGEST_FIELD,
    }
    issues = exact_fields(instance, required, "instance_contract")
    if issues:
        return issues
    if not isinstance(instance["instance_id"], str) or INSTANCE_ID.fullmatch(instance["instance_id"]) is None:
        issues.append("instance_contract_id_invalid")
    if not isinstance(instance["base_commit_sha"], str) or SHA40.fullmatch(instance["base_commit_sha"]) is None:
        issues.append("instance_contract_base_commit_invalid")
    for field in ("problem_statement_digest", "test_patch_digest"):
        if not isinstance(instance[field], str) or SHA256.fullmatch(instance[field]) is None:
            issues.append("instance_contract_digest_invalid:" + field)
    if not _valid_path_list(instance["protected_test_paths"], nonempty=True):
        issues.append("instance_contract_protected_paths_invalid")
    if not nonnegative_int(instance["instance_contract_created_epoch"]):
        issues.append("instance_contract_epoch_invalid")
    if not digest_ok(instance, INSTANCE_CONTRACT_DIGEST_FIELD):
        issues.append("instance_contract_digest_mismatch")
    return sorted(set(issues))


def validate_run_plan(plan: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "run_id",
        "evaluation_mode",
        "selection_method",
        "instances",
        "sample_count",
        "selected_instance_ids_digest",
        "selection_frozen_before_execution",
        "holdout_labels_exposed",
        "gold_patches_exposed",
        "max_workers",
        "timeout_seconds",
        "cache_level",
        "harness_execution_requested",
        "network_access_requested",
        "secret_access_requested",
        "repository_mutation_requested",
        "git_authority_requested",
        "correctness_claimed",
        "run_plan_created_epoch",
        RUN_PLAN_DIGEST_FIELD,
    }
    issues = exact_fields(plan, required, "run_plan")
    if issues:
        return issues
    if plan["schema_version"] != SCHEMA_VERSION or plan["profile_version"] != PROFILE_VERSION:
        issues.append("run_plan_profile_invalid")
    for field in ("run_id", "selection_method"):
        if not isinstance(plan[field], str) or IDENTIFIER.fullmatch(plan[field]) is None:
            issues.append("run_plan_identifier_invalid:" + field)
    if plan["evaluation_mode"] not in EVALUATION_MODES:
        issues.append("run_plan_mode_invalid")
    if plan["cache_level"] not in CACHE_LEVELS:
        issues.append("run_plan_cache_level_invalid")
    if not isinstance(plan["instances"], list) or not plan["instances"]:
        issues.append("run_plan_instances_invalid")
    else:
        for index, item in enumerate(plan["instances"]):
            item_map = mapping(item)
            if item_map is None:
                issues.append(f"run_plan_instance_not_mapping:{index}")
            else:
                issues.extend(f"run_plan_instance:{index}:{issue}" for issue in validate_instance_contract(item_map))
        ids = [item.get("instance_id") for item in plan["instances"] if isinstance(item, Mapping)]
        if len(ids) != len(set(ids)):
            issues.append("run_plan_duplicate_instance_id")
        if plan["sample_count"] != len(plan["instances"]):
            issues.append("run_plan_sample_count_mismatch")
        if isinstance(plan["selected_instance_ids_digest"], str):
            expected = canonical_digest(ids)
            if plan["selected_instance_ids_digest"] != expected:
                issues.append("run_plan_instance_ids_digest_mismatch")
    if not positive_int(plan["sample_count"]):
        issues.append("run_plan_sample_count_invalid")
    if not isinstance(plan["selected_instance_ids_digest"], str) or SHA256.fullmatch(plan["selected_instance_ids_digest"]) is None:
        issues.append("run_plan_selected_ids_digest_invalid")
    for field in ("max_workers", "timeout_seconds"):
        if not positive_int(plan[field]):
            issues.append("run_plan_positive_integer_invalid:" + field)
    for field in (
        "selection_frozen_before_execution",
        "holdout_labels_exposed",
        "gold_patches_exposed",
        "harness_execution_requested",
        "network_access_requested",
        "secret_access_requested",
        "repository_mutation_requested",
        "git_authority_requested",
        "correctness_claimed",
    ):
        if not isinstance(plan[field], bool):
            issues.append("run_plan_boolean_invalid:" + field)
    if not nonnegative_int(plan["run_plan_created_epoch"]):
        issues.append("run_plan_epoch_invalid")
    if not digest_ok(plan, RUN_PLAN_DIGEST_FIELD):
        issues.append("run_plan_digest_mismatch")
    return sorted(set(issues))


def validate_prediction(prediction: Mapping[str, Any]) -> list[str]:
    required = {
        "instance_id",
        "model_name_or_path",
        "model_patch",
        "changed_paths",
        "instance_contract_digest",
        "codeai_candidate_receipt_digest",
        "provider_session_digest",
        "prediction_created_epoch",
        "claims_harness_result",
        "claims_correctness",
        PREDICTION_DIGEST_FIELD,
    }
    issues = exact_fields(prediction, required, "prediction")
    if issues:
        return issues
    if not isinstance(prediction["instance_id"], str) or INSTANCE_ID.fullmatch(prediction["instance_id"]) is None:
        issues.append("prediction_instance_id_invalid")
    if not isinstance(prediction["model_name_or_path"], str) or not prediction["model_name_or_path"]:
        issues.append("prediction_model_invalid")
    if not isinstance(prediction["model_patch"], str) or not prediction["model_patch"]:
        issues.append("prediction_patch_invalid")
    if not _valid_path_list(prediction["changed_paths"], nonempty=True):
        issues.append("prediction_changed_paths_invalid")
    elif isinstance(prediction["model_patch"], str):
        derived = derive_changed_paths(prediction["model_patch"])
        if prediction["changed_paths"] != derived:
            issues.append("prediction_changed_paths_mismatch")
    for field in (
        "instance_contract_digest",
        "codeai_candidate_receipt_digest",
        "provider_session_digest",
    ):
        if not isinstance(prediction[field], str) or SHA256.fullmatch(prediction[field]) is None:
            issues.append("prediction_digest_invalid:" + field)
    if not nonnegative_int(prediction["prediction_created_epoch"]):
        issues.append("prediction_epoch_invalid")
    for field in ("claims_harness_result", "claims_correctness"):
        if not isinstance(prediction[field], bool):
            issues.append("prediction_boolean_invalid:" + field)
    if not digest_ok(prediction, PREDICTION_DIGEST_FIELD):
        issues.append("prediction_digest_mismatch")
    return sorted(set(issues))


def binding_mismatches(value: Mapping[str, Any], request: Mapping[str, Any]) -> list[str]:
    return [field for field in BINDING_FIELDS if value.get(field) != request.get(field)]


__all__ = [
    "binding_mismatches",
    "derive_changed_paths",
    "validate_benchmark_contract",
    "validate_instance_contract",
    "validate_prediction",
    "validate_run_plan",
]
