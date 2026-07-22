from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_checks_v0_1 import (
    derive_changed_paths,
    validate_benchmark_contract,
    validate_prediction,
    validate_run_plan,
)
from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIExternalGeneralBenchmarkAdapterResult:
    return CodeAIExternalGeneralBenchmarkAdapterResult(
        STATUS_BLOCKED, tuple(sorted(set(issues))), None, None
    )


def _receipt(pack: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "adapter_pack_digest": pack[PACK_DIGEST_FIELD],
        "request_digest": pack["request_digest"],
        "policy_digest": pack["policy_digest"],
        "benchmark_contract_digest": pack["benchmark_contract_digest"],
        "run_plan_digest": pack["run_plan_digest"],
        "official_predictions_digest": pack["official_predictions_digest"],
        "benchmark_id": pack["benchmark_id"],
        "dataset_name": pack["dataset_name"],
        "split": pack["split"],
        "sample_count": pack["sample_count"],
        "adapter_decision": pack["adapter_decision"],
        "hold_reasons": pack["hold_reasons"],
        "protocol_projection_only": True,
        "harness_execution_performed": False,
        "benchmark_result_ingested": False,
        "network_access_performed": False,
        "secret_access_performed": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def _official_prediction(prediction: Mapping[str, Any]) -> dict[str, str]:
    return {
        "instance_id": str(prediction["instance_id"]),
        "model_name_or_path": str(prediction["model_name_or_path"]),
        "model_patch": str(prediction["model_patch"]),
    }


def build_codeai_external_general_benchmark_swebench_verified_adapter(
    *,
    request: Any,
    policy: Any,
    benchmark_contract: Any,
    run_plan: Any,
    predictions: Any,
) -> CodeAIExternalGeneralBenchmarkAdapterResult:
    request_map = mapping(request)
    policy_map = mapping(policy)
    contract_map = mapping(benchmark_contract)
    plan_map = mapping(run_plan)
    if any(item is None for item in (request_map, policy_map, contract_map, plan_map)):
        return _blocked("input_not_mapping")
    if not isinstance(predictions, list) or not predictions:
        return _blocked("predictions_not_nonempty_list")
    prediction_maps: list[Mapping[str, Any]] = []
    for index, item in enumerate(predictions):
        item_map = mapping(item)
        if item_map is None:
            return _blocked(f"prediction_not_mapping:{index}")
        prediction_maps.append(item_map)

    assert request_map is not None and policy_map is not None
    assert contract_map is not None and plan_map is not None

    issues = (
        validate_request(request_map)
        + validate_policy(policy_map)
        + validate_benchmark_contract(contract_map)
        + validate_run_plan(plan_map)
    )
    for index, prediction in enumerate(prediction_maps):
        issues.extend(f"prediction:{index}:{issue}" for issue in validate_prediction(prediction))
    if issues:
        return _blocked(*issues)

    required_true = (
        "require_exact_binding",
        "require_official_verified_dataset",
        "require_expected_instance_count",
        "require_frozen_sample",
        "require_holdout_labels_hidden",
        "require_gold_patch_hidden",
        "require_pinned_harness",
        "require_containerized_harness",
        "require_official_prediction_shape",
        "require_unique_instances",
        "require_patch_digest",
        "require_derived_changed_paths",
        "require_protected_test_path_nonoverlap",
        "allow_protocol_projection",
    )
    if any(policy_map[field] is not True for field in required_true):
        return _blocked("policy_required_guarantee_disabled")

    forbidden_policy = (
        "allow_harness_execution",
        "allow_network_access",
        "allow_secret_access",
        "allow_repository_mutation",
        "allow_git_authority",
        "allow_correctness_claim",
    )
    if any(policy_map[field] is not False for field in forbidden_policy):
        return _blocked("policy_effect_or_authority_enabled")

    if request_map["unresolved_questions"]:
        return _blocked("request_unresolved_questions_present")
    if any(
        request_map[field]
        for field in (
            "claims_harness_execution_authority",
            "claims_network_authority",
            "claims_secret_authority",
            "claims_repository_mutation_authority",
            "claims_git_authority",
            "claims_correctness",
        )
    ):
        return _blocked("request_claims_authority_or_correctness")

    binding_issues = [
        "request_policy_binding_mismatch:" + field
        for field in BINDING_FIELDS
        if request_map[field] != policy_map["expected_" + field]
    ]
    if request_map["benchmark_contract_digest"] != contract_map[CONTRACT_DIGEST_FIELD]:
        binding_issues.append("request_contract_digest_mismatch")
    if request_map["run_plan_digest"] != plan_map[RUN_PLAN_DIGEST_FIELD]:
        binding_issues.append("request_run_plan_digest_mismatch")
    if binding_issues:
        return _blocked(*binding_issues)

    evaluation_epoch = int(policy_map["evaluation_epoch"])
    if not (
        evaluation_epoch - int(policy_map["maximum_request_age"])
        <= int(request_map["request_created_epoch"])
        <= evaluation_epoch
    ):
        return _blocked("request_window_invalid")

    hold_reasons: list[str] = []

    exact_contract_checks = (
        (contract_map["benchmark_id"] == BENCHMARK_ID, "benchmark_id_not_swebench_verified"),
        (contract_map["dataset_name"] == DATASET_NAME, "dataset_name_not_official_verified"),
        (contract_map["split"] == DATASET_SPLIT, "dataset_split_not_test"),
        (
            contract_map["expected_instance_count"] == EXPECTED_INSTANCE_COUNT,
            "dataset_instance_count_not_500",
        ),
        (
            contract_map["harness_repository"] == HARNESS_REPOSITORY,
            "harness_repository_not_official",
        ),
        (
            contract_map["harness_entrypoint"] == HARNESS_ENTRYPOINT,
            "harness_entrypoint_not_official",
        ),
        (
            tuple(contract_map["prediction_fields"]) == OFFICIAL_PREDICTION_FIELDS,
            "prediction_fields_not_official",
        ),
        (contract_map["containerized_harness"] is True, "harness_not_containerized"),
        (contract_map["official_harness"] is True, "harness_not_official"),
        (contract_map["corpus_frozen"] is True, "benchmark_corpus_not_frozen"),
        (
            contract_map["test_patch_paths_sealed"] is True,
            "benchmark_test_patch_paths_unsealed",
        ),
    )
    hold_reasons.extend(reason for condition, reason in exact_contract_checks if not condition)

    for field in (
        "harness_execution_performed",
        "network_access_performed",
        "secret_access_performed",
        "repository_mutation_performed",
        "git_authority_granted",
        "correctness_claimed",
    ):
        if contract_map[field]:
            hold_reasons.append("benchmark_contract_forbidden_effect:" + field)

    plan_checks = (
        (
            plan_map["evaluation_mode"] in policy_map["allowed_evaluation_modes"],
            "run_plan_evaluation_mode_not_allowed",
        ),
        (
            plan_map["cache_level"] in policy_map["allowed_cache_levels"],
            "run_plan_cache_level_not_allowed",
        ),
        (
            policy_map["minimum_sample_count"]
            <= plan_map["sample_count"]
            <= policy_map["maximum_sample_count"],
            "run_plan_sample_count_out_of_bounds",
        ),
        (
            plan_map["selection_frozen_before_execution"] is True,
            "run_plan_selection_not_frozen",
        ),
        (plan_map["holdout_labels_exposed"] is False, "run_plan_holdout_labels_exposed"),
        (plan_map["gold_patches_exposed"] is False, "run_plan_gold_patches_exposed"),
    )
    hold_reasons.extend(reason for condition, reason in plan_checks if not condition)

    for field in (
        "harness_execution_requested",
        "network_access_requested",
        "secret_access_requested",
        "repository_mutation_requested",
        "git_authority_requested",
        "correctness_claimed",
    ):
        if plan_map[field]:
            hold_reasons.append("run_plan_forbidden_request:" + field)

    instance_contracts = {
        item["instance_id"]: item for item in plan_map["instances"]
    }
    prediction_ids = [prediction["instance_id"] for prediction in prediction_maps]
    plan_ids = [item["instance_id"] for item in plan_map["instances"]]
    if len(prediction_ids) != len(set(prediction_ids)):
        hold_reasons.append("prediction_instance_ids_not_unique")
    if prediction_ids != plan_ids:
        hold_reasons.append("prediction_instance_order_or_set_mismatch")

    total_patch_bytes = 0
    for prediction in prediction_maps:
        instance_id = prediction["instance_id"]
        patch_bytes = len(prediction["model_patch"].encode("utf-8"))
        total_patch_bytes += patch_bytes
        if patch_bytes > policy_map["maximum_patch_bytes"]:
            hold_reasons.append("prediction_patch_budget_exceeded:" + instance_id)
        derived_paths = derive_changed_paths(prediction["model_patch"])
        if len(derived_paths) > policy_map["maximum_changed_paths_per_prediction"]:
            hold_reasons.append("prediction_changed_path_budget_exceeded:" + instance_id)
        contract = instance_contracts.get(instance_id)
        if contract is None:
            hold_reasons.append("prediction_instance_contract_missing:" + instance_id)
            continue
        if (
            prediction["instance_contract_digest"]
            != contract[INSTANCE_CONTRACT_DIGEST_FIELD]
        ):
            hold_reasons.append("prediction_instance_contract_digest_mismatch:" + instance_id)
        overlap = sorted(set(derived_paths).intersection(contract["protected_test_paths"]))
        if overlap:
            hold_reasons.append(
                "prediction_protected_test_path_overlap:"
                + instance_id
                + ":"
                + ",".join(overlap)
            )
        if prediction["claims_harness_result"]:
            hold_reasons.append("prediction_claims_unexecuted_harness_result:" + instance_id)
        if prediction["claims_correctness"]:
            hold_reasons.append("prediction_claims_correctness:" + instance_id)

    if total_patch_bytes > policy_map["maximum_total_patch_bytes"]:
        hold_reasons.append("prediction_total_patch_budget_exceeded")

    official_predictions = [_official_prediction(item) for item in prediction_maps]
    if any(tuple(item.keys()) != OFFICIAL_PREDICTION_FIELDS for item in official_predictions):
        hold_reasons.append("official_prediction_projection_shape_invalid")

    hold_reasons = sorted(set(hold_reasons))
    decision = DECISION_ADMIT if not hold_reasons else DECISION_HOLD
    official_predictions_digest = canonical_digest(official_predictions)

    pack = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_digest": request_map[REQUEST_DIGEST_FIELD],
        "policy_digest": policy_map[POLICY_DIGEST_FIELD],
        "benchmark_contract_digest": contract_map[CONTRACT_DIGEST_FIELD],
        "run_plan_digest": plan_map[RUN_PLAN_DIGEST_FIELD],
        "controller_repository_full_name": request_map["controller_repository_full_name"],
        "controller_source_commit_sha": request_map["controller_source_commit_sha"],
        "benchmark_id": contract_map["benchmark_id"],
        "dataset_name": contract_map["dataset_name"],
        "split": contract_map["split"],
        "expected_instance_count": contract_map["expected_instance_count"],
        "harness_repository": contract_map["harness_repository"],
        "harness_commit_sha": contract_map["harness_commit_sha"],
        "harness_entrypoint": contract_map["harness_entrypoint"],
        "evaluation_mode": plan_map["evaluation_mode"],
        "sample_count": plan_map["sample_count"],
        "selected_instance_ids_digest": plan_map["selected_instance_ids_digest"],
        "prediction_count": len(prediction_maps),
        "total_patch_bytes": total_patch_bytes,
        "official_prediction_fields": list(OFFICIAL_PREDICTION_FIELDS),
        "official_predictions": official_predictions,
        "official_predictions_digest": official_predictions_digest,
        "adapter_decision": decision,
        "hold_reasons": hold_reasons,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_PROTOCOL_ONLY,
        "protocol_projection_only": True,
        "harness_execution_performed": False,
        "benchmark_result_ingested": False,
        "network_access_performed": False,
        "secret_access_performed": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack, PACK_DIGEST_FIELD)
    return CodeAIExternalGeneralBenchmarkAdapterResult(
        STATUS_READY, (), pack, _receipt(pack)
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIExternalGeneralBenchmarkAdapterResult",
    "build_codeai_external_general_benchmark_swebench_verified_adapter",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
