from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import *

_BINDING_FIELDS = (
    "controller_repository", "controller_source_commit_sha",
    "predecessor_manifest_digest", "predecessor_smoke_pack_digest",
    "predecessor_smoke_receipt_digest", "predecessor_external_artifact_digest",
    "dataset_name", "dataset_revision", "dataset_split", "dataset_artifact_sha256",
    "harness_repository", "harness_commit_sha", "instance_id", "base_commit_sha",
    "prediction_digest", "execution_contract_digest",
)

def _validate_inputs(
    request: dict[str, Any],
    policy: dict[str, Any],
    predecessor_manifest: dict[str, Any],
    execution_plan: dict[str, Any],
    prediction: dict[str, Any],
    observation: dict[str, Any],
) -> None:
    surfaces = (
        (request, REQUEST_FIELDS, REQUEST_DIGEST_FIELD, "request"),
        (policy, POLICY_FIELDS, POLICY_DIGEST_FIELD, "policy"),
        (execution_plan, PLAN_FIELDS, PLAN_DIGEST_FIELD, "execution_plan"),
        (prediction, PREDICTION_FIELDS, PREDICTION_DIGEST_FIELD, "prediction"),
        (observation, OBSERVATION_FIELDS, OBSERVATION_DIGEST_FIELD, "observation"),
    )
    for value, fields, digest_field, label in surfaces:
        require_exact_fields(value, fields, label)
        require_profile(value, label)
        validate_seal(value, digest_field)

    require_sha256(request["predecessor_manifest_digest"], "predecessor_manifest_digest")
    require_sha256(request["predecessor_smoke_pack_digest"], "predecessor_smoke_pack_digest")
    require_sha256(request["predecessor_smoke_receipt_digest"], "predecessor_smoke_receipt_digest")
    require_sha256(request["predecessor_external_artifact_digest"], "predecessor_external_artifact_digest")
    require_sha256(request["dataset_artifact_sha256"], "dataset_artifact_sha256")
    require_sha256(request["prediction_digest"], "prediction_digest")
    require_sha256(request["execution_contract_digest"], "execution_contract_digest")
    require_git_sha(request["controller_source_commit_sha"], "controller_source_commit_sha")
    require_git_sha(request["harness_commit_sha"], "harness_commit_sha")
    require_git_sha(request["base_commit_sha"], "base_commit_sha")

    if canonical_digest(predecessor_manifest) != request["predecessor_manifest_digest"]:
        raise BlockedInput("predecessor manifest digest mismatch")
    if prediction[PREDICTION_DIGEST_FIELD] != request["prediction_digest"]:
        raise BlockedInput("prediction digest mismatch")

    for field in _BINDING_FIELDS:
        expected = policy["expected_" + field]
        if request[field] != expected:
            raise BlockedInput(f"request/policy mismatch: {field}")
        if execution_plan[field] != request[field]:
            raise BlockedInput(f"plan/request mismatch: {field}")
        if observation[field] != request[field]:
            raise BlockedInput(f"observation/request mismatch: {field}")

    for field in ("instance_id", "base_commit_sha"):
        if prediction[field] != request[field]:
            raise BlockedInput(f"prediction/request mismatch: {field}")

    if execution_plan["prediction_file_digest"] != canonical_digest(
        official_prediction(prediction)
    ):
        raise BlockedInput("prediction file digest mismatch")

    derived = derive_changed_paths(prediction["model_patch"])
    if prediction["changed_paths"] != derived:
        raise BlockedInput("changed paths were not independently derived")

    if policy["evaluation_epoch"] - request["request_created_epoch"] > policy["maximum_request_age"]:
        raise BlockedInput("stale request")
    if policy["evaluation_epoch"] - observation["observation_created_epoch"] > policy["maximum_observation_age"]:
        raise BlockedInput("stale observation")
    if request["request_created_epoch"] > policy["evaluation_epoch"]:
        raise BlockedInput("request from the future")
    if observation["observation_created_epoch"] > policy["evaluation_epoch"]:
        raise BlockedInput("observation from the future")

def _hold_reasons(
    request: dict[str, Any],
    policy: dict[str, Any],
    predecessor_manifest: dict[str, Any],
    execution_plan: dict[str, Any],
    prediction: dict[str, Any],
    observation: dict[str, Any],
) -> list[str]:
    reasons: list[str] = []
    checks = [
        (policy["require_predecessor_smoke_admitted"] and predecessor_manifest.get("decision") != "gold_patch_environment_smoke_admitted", "predecessor smoke not admitted"),
        (policy["require_frozen_sample"] and not execution_plan["sample_frozen"], "sample not frozen"),
        (policy["require_frozen_prediction"] and not execution_plan["prediction_frozen"], "prediction not frozen"),
        (policy["require_official_prediction_shape"] and not execution_plan["official_prediction_shape"], "official prediction shape not established"),
        (policy["require_non_gold_prediction"] and (not execution_plan["non_gold_prediction"] or prediction["gold_derived"] or prediction["gold_accessed"]), "prediction is not independently non-gold"),
        (execution_plan["sample_count"] != policy["required_sample_count"], "sample count mismatch"),
        (execution_plan["maximum_workers"] > policy["maximum_workers"], "worker budget exceeded"),
        (execution_plan["timeout_seconds"] != policy["timeout_seconds"], "timeout mismatch"),
        (policy["require_patch_applied"] and not observation["patch_applied"], "patch not applied"),
        (policy["require_evaluation_completed"] and not observation["evaluation_completed"], "evaluation incomplete"),
        (policy["require_report_observed"] and not observation["report_observed"], "report missing"),
        (policy["require_logs_observed"] and not observation["logs_observed"], "logs missing"),
        (not observation["external_harness_execution_observed"], "external harness execution not observed"),
        (not observation["docker_used"], "docker not observed"),
        (not observation["image_available"], "image unavailable"),
        (not observation["container_started"], "container not started"),
        (observation["harness_execution_performed_by_kernel"] and not policy["allow_kernel_harness_execution"], "kernel executed harness"),
        ((request["claims_gold_access"] or execution_plan["gold_available_to_solver"] or observation["gold_exposed_to_solver"] or observation["gold_used_for_candidate_generation"] or observation["gold_used_for_repair_memory"]) and not policy["allow_gold_access"], "gold isolation violated"),
        ((request["claims_repository_mutation_authority"] or observation["repository_mutated"]) and not policy["allow_repository_mutation"], "repository mutation boundary violated"),
        ((request["claims_git_authority"] or observation["git_authority"]) and not policy["allow_git_authority"], "git authority boundary violated"),
        ((request["claims_correctness"] or prediction["claims_correctness"] or observation["correctness_claimed"]) and not policy["allow_correctness_claim"], "correctness overclaim"),
        (request["claims_kernel_harness_execution"] and not policy["allow_kernel_harness_execution"], "request claims kernel harness execution"),
    ]
    for condition, reason in checks:
        if condition:
            reasons.append(reason)
    return reasons

def build_codeai_bounded_official_harness_execution(
    *,
    request: dict[str, Any],
    policy: dict[str, Any],
    predecessor_manifest: dict[str, Any],
    execution_plan: dict[str, Any],
    prediction: dict[str, Any],
    observation: dict[str, Any],
) -> ExecutionResult:
    try:
        _validate_inputs(
            request, policy, predecessor_manifest, execution_plan, prediction, observation
        )
    except BlockedInput as exc:
        return ExecutionResult(STATUS_BLOCKED, (str(exc),), None, None)

    reasons = _hold_reasons(
        request, policy, predecessor_manifest, execution_plan, prediction, observation
    )
    decision = DECISION_HELD if reasons else DECISION_ADMITTED
    status = STATUS_HELD if reasons else STATUS_ADMITTED
    pack = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "decision": decision,
            "request_digest": request[REQUEST_DIGEST_FIELD],
            "policy_digest": policy[POLICY_DIGEST_FIELD],
            "predecessor_manifest_digest": request["predecessor_manifest_digest"],
            "predecessor_smoke_pack_digest": request["predecessor_smoke_pack_digest"],
            "predecessor_smoke_receipt_digest": request["predecessor_smoke_receipt_digest"],
            "predecessor_external_artifact_digest": request["predecessor_external_artifact_digest"],
            "execution_plan_digest": execution_plan[PLAN_DIGEST_FIELD],
            "prediction_digest": prediction[PREDICTION_DIGEST_FIELD],
            "observation_digest": observation[OBSERVATION_DIGEST_FIELD],
            "instance_id": request["instance_id"],
            "base_commit_sha": request["base_commit_sha"],
            "resolved": observation["resolved"],
            "hold_reasons": reasons,
            "kernel_harness_execution_authority_granted": False,
            "gold_access_granted": False,
            "repository_mutation_authority_granted": False,
            "git_authority_granted": False,
            "correctness_claimed": False,
        },
        PACK_DIGEST_FIELD,
    )
    receipt = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "decision": decision,
            "execution_pack_digest": pack[PACK_DIGEST_FIELD],
            "instance_id": request["instance_id"],
            "model_name_or_path": prediction["model_name_or_path"],
            "prediction_digest": prediction[PREDICTION_DIGEST_FIELD],
            "patch_applied": observation["patch_applied"],
            "evaluation_completed": observation["evaluation_completed"],
            "resolved": observation["resolved"],
            "report_digest": observation["report_digest"],
            "test_output_digest": observation["test_output_digest"],
            "instance_log_digest": observation["instance_log_digest"],
            "gold_access_granted": False,
            "future_harness_execution_authority_granted": False,
            "repository_mutation_authority_granted": False,
            "git_authority_granted": False,
            "correctness_claimed": False,
            "hold_reasons": reasons,
        },
        RECEIPT_DIGEST_FIELD,
    )
    return ExecutionResult(status, tuple(reasons), pack, receipt)
