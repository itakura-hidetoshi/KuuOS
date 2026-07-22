from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_checks_v0_1 import *


def build_codeai_external_result_process_evidence_ingestion(
    *, request: dict[str, Any], policy: dict[str, Any], predecessor_manifest: dict[str, Any],
    plan: dict[str, Any], result_evidence: dict[str, Any], process_evidence: dict[str, Any]
) -> IngestionResult:
    try:
        validate_structure(
            request=request, policy=policy, predecessor_manifest=predecessor_manifest,
            plan=plan, result_evidence=result_evidence, process_evidence=process_evidence,
        )
        if not exact_binding(request, policy, plan, result_evidence, process_evidence):
            raise BlockedInput("exact binding mismatch")
        if request["predecessor_manifest_digest"] != canonical_digest(predecessor_manifest):
            raise BlockedInput("predecessor manifest digest mismatch")
        if not freshness_ok(request, policy, result_evidence, process_evidence):
            raise BlockedInput("stale or future-dated evidence")
    except BlockedInput as exc:
        return IngestionResult(STATUS_BLOCKED, (str(exc),), None, None)

    reasons: list[str] = []
    if predecessor_manifest["decision"] != "bounded_official_harness_execution_admitted":
        reasons.append("predecessor not admitted")
    if predecessor_manifest["receipt_digest"] != request["predecessor_receipt_digest"]:
        reasons.append("predecessor receipt mismatch")
    if predecessor_manifest["prediction_digest"] != request["prediction_digest"]:
        reasons.append("predecessor prediction mismatch")
    if not predecessor_manifest["patch_applied"] or not predecessor_manifest["evaluation_completed"]:
        reasons.append("predecessor execution incomplete")

    if plan["ingestion_mode"] != "aggregate-only": reasons.append("ingestion mode not aggregate-only")
    if plan["result_count"] != policy["required_result_count"]: reasons.append("result count mismatch")
    if plan["process_evidence_count"] != policy["required_process_evidence_count"]: reasons.append("process evidence count mismatch")
    if not plan["source_artifact_retained_externally"]: reasons.append("source artifact not externally retained")
    if plan["raw_artifact_committed"]: reasons.append("raw artifact committed")
    if plan["raw_test_names_ingested"]: reasons.append("raw test names ingested")
    if plan["raw_logs_ingested"]: reasons.append("raw logs ingested")
    if plan["candidate_generation_feedback_enabled"]: reasons.append("candidate-generation feedback enabled")
    if plan["repair_memory_feedback_enabled"]: reasons.append("repair-memory feedback enabled")
    if plan["comparison_authority_granted"]: reasons.append("comparison authority granted")

    if not result_evidence["patch_exists"] or not result_evidence["patch_applied"]:
        reasons.append("patch evidence incomplete")
    if not result_evidence["evaluation_completed"]: reasons.append("evaluation incomplete")
    if result_evidence["error_count"] != 0: reasons.append("execution errors observed")
    if result_evidence["raw_test_names_included"]: reasons.append("raw test names included")
    if result_evidence["gold_material_included"]: reasons.append("gold material included")

    for field in ("workflow_completed", "docker_used", "image_available", "container_started",
                  "patch_applied_cleanly", "evaluation_completed", "git_diff_stable",
                  "container_removed", "image_removed", "report_observed", "logs_observed"):
        if not process_evidence[field]: reasons.append(f"missing process evidence: {field}")
    if process_evidence["artifact_expired"]: reasons.append("artifact expired")
    if process_evidence["harness_executed_by_kernel"]: reasons.append("kernel executed harness")
    if process_evidence["raw_logs_committed"]: reasons.append("raw logs committed")
    if process_evidence["repository_mutated"]: reasons.append("repository mutated")
    if process_evidence["git_authority"]: reasons.append("Git authority granted")
    if process_evidence["correctness_claimed"]: reasons.append("correctness claimed")

    for field in (
        "claims_raw_gold_access", "claims_raw_test_name_access",
        "claims_candidate_generation_feedback", "claims_repair_memory_feedback",
        "claims_repository_mutation_authority", "claims_git_authority", "claims_correctness",
    ):
        if request[field]: reasons.append(f"request overclaim: {field}")
    for field in (
        "allow_raw_gold_access", "allow_raw_test_names", "allow_raw_logs_committed",
        "allow_candidate_generation_feedback", "allow_repair_memory_feedback",
        "allow_kernel_harness_execution", "allow_repository_mutation",
        "allow_git_authority", "allow_correctness_claim",
    ):
        if policy[field]: reasons.append(f"policy authority enabled: {field}")

    if reasons:
        return IngestionResult(STATUS_HELD, tuple(sorted(set(reasons))), None, None)

    disposition = "measured_resolved" if result_evidence["resolved"] else "measured_unresolved"
    pack_material = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision": DECISION_ADMITTED,
        **{field: request[field] for field in BINDING_FIELDS},
        "plan_digest": plan[PLAN_DIGEST_FIELD],
        "result_evidence_digest": result_evidence[RESULT_DIGEST_FIELD],
        "process_evidence_digest": process_evidence[PROCESS_DIGEST_FIELD],
        "report_digest": result_evidence["report_digest"],
        "test_output_digest": process_evidence["test_output_digest"],
        "instance_log_digest": process_evidence["instance_log_digest"],
        "outcome_disposition": disposition,
        "execution_valid": True,
        "resolved": result_evidence["resolved"],
        "fail_to_pass_success_count": result_evidence["fail_to_pass_success_count"],
        "fail_to_pass_failure_count": result_evidence["fail_to_pass_failure_count"],
        "pass_to_pass_success_count": result_evidence["pass_to_pass_success_count"],
        "pass_to_pass_failure_count": result_evidence["pass_to_pass_failure_count"],
        "raw_gold_ingested": False,
        "raw_test_names_ingested": False,
        "raw_logs_committed": False,
        "candidate_generation_feedback_enabled": False,
        "repair_memory_feedback_enabled": False,
        "comparison_authority_granted": False,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }
    pack = seal(pack_material, PACK_DIGEST_FIELD)
    receipt = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "decision": DECISION_ADMITTED,
        "ingestion_pack_digest": pack[PACK_DIGEST_FIELD],
        "predecessor_artifact_digest": request["predecessor_artifact_digest"],
        "external_observation_digest": request["external_observation_digest"],
        "instance_id": request["instance_id"],
        "prediction_digest": request["prediction_digest"],
        "outcome_disposition": disposition,
        "execution_valid": True,
        "resolved": result_evidence["resolved"],
        "downstream_comparison_authority_granted": False,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
    }, RECEIPT_DIGEST_FIELD)
    return IngestionResult(STATUS_ADMITTED, (), pack, receipt)
