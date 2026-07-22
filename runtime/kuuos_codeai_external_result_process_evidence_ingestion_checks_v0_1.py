from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import *

DIGEST_BINDINGS = {
    "predecessor_manifest_digest", "predecessor_execution_pack_digest",
    "predecessor_receipt_digest", "predecessor_artifact_digest",
    "prediction_digest", "external_observation_digest", "ingestion_contract_digest",
}

def validate_structure(
    *, request: dict[str, Any], policy: dict[str, Any], predecessor_manifest: dict[str, Any],
    plan: dict[str, Any], result_evidence: dict[str, Any], process_evidence: dict[str, Any]
) -> None:
    require_exact_fields(request, REQUEST_FIELDS, "request")
    require_exact_fields(policy, POLICY_FIELDS, "policy")
    require_exact_fields(predecessor_manifest, PREDECESSOR_MANIFEST_FIELDS, "predecessor_manifest")
    require_exact_fields(plan, PLAN_FIELDS, "plan")
    require_exact_fields(result_evidence, RESULT_FIELDS, "result_evidence")
    require_exact_fields(process_evidence, PROCESS_FIELDS, "process_evidence")
    for label, value, digest_field in (
        ("request", request, REQUEST_DIGEST_FIELD),
        ("policy", policy, POLICY_DIGEST_FIELD),
        ("plan", plan, PLAN_DIGEST_FIELD),
        ("result_evidence", result_evidence, RESULT_DIGEST_FIELD),
        ("process_evidence", process_evidence, PROCESS_DIGEST_FIELD),
    ):
        require_profile(value, label)
        validate_seal(value, digest_field)
    require_sha256(canonical_digest(predecessor_manifest), "predecessor manifest canonical digest")
    for field in BINDING_FIELDS:
        if field == "controller_source_commit_sha":
            require_git_sha(request[field], field)
        elif field in DIGEST_BINDINGS:
            require_sha256(request[field], field)
        elif field in {"predecessor_workflow_run_id", "predecessor_artifact_id"}:
            require_nonnegative_int(request[field], field)
    for field in ("report_digest",):
        require_sha256(result_evidence[field], field)
    for field in ("test_output_digest", "instance_log_digest"):
        require_sha256(process_evidence[field], field)
    for field in (
        "fail_to_pass_success_count", "fail_to_pass_failure_count",
        "pass_to_pass_success_count", "pass_to_pass_failure_count", "error_count",
    ):
        require_nonnegative_int(result_evidence[field], field)
    for value, fields in (
        (request, [f for f in request if f.startswith("claims_")]),
        (plan, ["source_artifact_retained_externally", "raw_artifact_committed",
                "raw_test_names_ingested", "raw_logs_ingested",
                "candidate_generation_feedback_enabled", "repair_memory_feedback_enabled",
                "comparison_authority_granted"]),
        (result_evidence, ["patch_exists", "patch_applied", "evaluation_completed", "resolved",
                           "raw_test_names_included", "gold_material_included"]),
        (process_evidence, ["workflow_completed", "artifact_expired", "docker_used",
                            "image_available", "container_started", "patch_applied_cleanly",
                            "evaluation_completed", "git_diff_stable", "container_removed",
                            "image_removed", "report_observed", "logs_observed",
                            "network_used_by_external_harness", "harness_executed_by_kernel",
                            "raw_logs_committed", "repository_mutated", "git_authority",
                            "correctness_claimed"]),
    ):
        for field in fields:
            require_bool(value[field], field)

def exact_binding(request: dict[str, Any], policy: dict[str, Any], *evidence: dict[str, Any]) -> bool:
    for field in BINDING_FIELDS:
        expected = policy["expected_" + field]
        if request[field] != expected:
            return False
        for item in evidence:
            if item[field] != expected:
                return False
    return True

def freshness_ok(request: dict[str, Any], policy: dict[str, Any], result: dict[str, Any], process: dict[str, Any]) -> bool:
    epoch = policy["evaluation_epoch"]
    return (
        0 <= epoch - request["request_created_epoch"] <= policy["maximum_request_age"]
        and 0 <= epoch - result["result_created_epoch"] <= policy["maximum_result_age"]
        and 0 <= epoch - process["process_created_epoch"] <= policy["maximum_process_evidence_age"]
    )
