from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import *
from runtime.kuuos_codeai_external_result_process_evidence_ingestion_v0_1 import (
    build_codeai_external_result_process_evidence_ingestion,
)

CONTROLLER_COMMIT = "30d6d57fe8b6681aa8e11404a774d0500076d497"
EPOCH = 3000
PREDECESSOR_EXECUTION_PACK = "3f5e691391b67e0e56d39d6ed241989d50a0a68cbc8eb901d9371ae6e3da4726"
PREDECESSOR_RECEIPT = "774e1a3835020c4d25b7f6eec9834958746ed4270a0b62b7d57654f9e7d86cff"
PREDECESSOR_WORKFLOW_RUN_ID = 29894633457
PREDECESSOR_WORKFLOW_HEAD_SHA = "13ac5c618d934e3812ca70cd3791a374a2058f6f"
PREDECESSOR_ARTIFACT_ID = 8520539325
PREDECESSOR_ARTIFACT_DIGEST = "27f69ffd9a982956d2bbc2aaeecc9e45ed527ea522afda324e0e3665b634c5a2"
INSTANCE_ID = "sympy__sympy-20590"
PREDICTION_DIGEST = "9a2aeff25ca565214ecbae781f20df4c23eea20db72b135702aa56d5de238050"
EXTERNAL_OBSERVATION_DIGEST = "689b63a246192b45af75f512aba7478ad87db7aba90689d96fc0aa91bc28cbca"
REPORT_DIGEST = "35493c1b427e375b3352d51e19a007d3602f23d6a45563ed14857dffb4f5c52f"
TEST_OUTPUT_DIGEST = "fe91940eaca527c3382dfeeca238b4af483ff3ff3fe7cdcab2260f57798d9eae"
INSTANCE_LOG_DIGEST = "89891077aec984c2787d2f27970578ae6e16d81b2ca97db3db6f637b2b7af665"

def h(label: str) -> str:
    return canonical_digest({"label": label})

PREDECESSOR_MANIFEST = {
    "correctness_claimed": False,
    "decision": "bounded_official_harness_execution_admitted",
    "evaluation_completed": True,
    "future_harness_execution_authority_granted": False,
    "git_authority_granted": False,
    "gold_access_granted": False,
    "instance_id": INSTANCE_ID,
    "instance_log_digest": "39f4b4cdd8c9f79aa6f0c17f41e2f65107886ed3beb442cd2f8606694c00e792",
    "model_name_or_path": "kuuos-codeai/bounded-smoke-v0.1",
    "patch_applied": True,
    "prediction_digest": PREDICTION_DIGEST,
    "profile_version": "CodeAI Bounded Official Harness Execution v0.1",
    "receipt_digest": PREDECESSOR_RECEIPT,
    "report_digest": "a381ff62e0cfd8af10dadf924e6abf75a2a2e55f2ce2b4662c237134e65c9bb3",
    "repository_mutation_authority_granted": False,
    "resolved": False,
    "test_output_digest": "2ae368f648890d932c7c5a567a6ddda259e3e83d14e83ab8eb99f2efc8aaff93",
}

def build_fixture() -> dict[str, Any]:
    predecessor_manifest = deepcopy(PREDECESSOR_MANIFEST)
    binding = {
        "controller_repository": "itakura-hidetoshi/KuuOS",
        "controller_source_commit_sha": CONTROLLER_COMMIT,
        "predecessor_manifest_digest": canonical_digest(predecessor_manifest),
        "predecessor_execution_pack_digest": PREDECESSOR_EXECUTION_PACK,
        "predecessor_receipt_digest": PREDECESSOR_RECEIPT,
        "predecessor_workflow_run_id": PREDECESSOR_WORKFLOW_RUN_ID,
        "predecessor_artifact_id": PREDECESSOR_ARTIFACT_ID,
        "predecessor_artifact_digest": PREDECESSOR_ARTIFACT_DIGEST,
        "instance_id": INSTANCE_ID,
        "prediction_digest": PREDICTION_DIGEST,
        "external_observation_digest": EXTERNAL_OBSERVATION_DIGEST,
        "ingestion_contract_digest": h("external-result-process-evidence-ingestion-contract-v0.1"),
    }
    request = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "external-result-ingestion-request-001",
        "request_revision": "external-result-ingestion-rev-001",
        **binding,
        "request_created_epoch": EPOCH - 10,
        "claims_raw_gold_access": False,
        "claims_raw_test_name_access": False,
        "claims_candidate_generation_feedback": False,
        "claims_repair_memory_feedback": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
        "claims_correctness": False,
    }, REQUEST_DIGEST_FIELD)
    policy = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + k: v for k, v in binding.items()},
        "evaluation_epoch": EPOCH,
        "maximum_request_age": 100,
        "maximum_result_age": 100,
        "maximum_process_evidence_age": 100,
        "required_result_count": 1,
        "required_process_evidence_count": 1,
        "require_exact_binding": True,
        "require_predecessor_admitted": True,
        "require_completed_workflow": True,
        "require_unexpired_artifact": True,
        "require_aggregate_only_ingestion": True,
        "require_patch_applied": True,
        "require_evaluation_completed": True,
        "require_report_and_logs": True,
        "allow_resolved_or_unresolved": True,
        "allow_raw_gold_access": False,
        "allow_raw_test_names": False,
        "allow_raw_logs_committed": False,
        "allow_candidate_generation_feedback": False,
        "allow_repair_memory_feedback": False,
        "allow_kernel_harness_execution": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
        "allow_correctness_claim": False,
    }, POLICY_DIGEST_FIELD)
    plan = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "ingestion_id": "kuuos-external-result-ingestion-001",
        "ingestion_mode": "aggregate-only",
        "result_count": 1,
        "process_evidence_count": 1,
        "source_artifact_retained_externally": True,
        "raw_artifact_committed": False,
        "raw_test_names_ingested": False,
        "raw_logs_ingested": False,
        "candidate_generation_feedback_enabled": False,
        "repair_memory_feedback_enabled": False,
        "comparison_authority_granted": False,
        "plan_created_epoch": EPOCH - 9,
    }, PLAN_DIGEST_FIELD)
    result_evidence = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "report_digest": REPORT_DIGEST,
        "result_created_epoch": EPOCH - 2,
        "patch_exists": True,
        "patch_applied": True,
        "evaluation_completed": True,
        "resolved": False,
        "fail_to_pass_success_count": 0,
        "fail_to_pass_failure_count": 1,
        "pass_to_pass_success_count": 21,
        "pass_to_pass_failure_count": 0,
        "error_count": 0,
        "raw_test_names_included": False,
        "gold_material_included": False,
    }, RESULT_DIGEST_FIELD)
    process_evidence = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "test_output_digest": TEST_OUTPUT_DIGEST,
        "instance_log_digest": INSTANCE_LOG_DIGEST,
        "process_created_epoch": EPOCH - 1,
        "workflow_completed": True,
        "artifact_expired": False,
        "docker_used": True,
        "image_available": True,
        "container_started": True,
        "patch_applied_cleanly": True,
        "evaluation_completed": True,
        "git_diff_stable": True,
        "container_removed": True,
        "image_removed": True,
        "report_observed": True,
        "logs_observed": True,
        "network_used_by_external_harness": True,
        "harness_executed_by_kernel": False,
        "raw_logs_committed": False,
        "repository_mutated": False,
        "git_authority": False,
        "correctness_claimed": False,
    }, PROCESS_DIGEST_FIELD)
    built = build_codeai_external_result_process_evidence_ingestion(
        request=request, policy=policy, predecessor_manifest=predecessor_manifest,
        plan=plan, result_evidence=result_evidence, process_evidence=process_evidence,
    )
    assert built.status == STATUS_ADMITTED
    assert built.ingestion_pack is not None and built.receipt is not None
    return {
        "request": request,
        "policy": policy,
        "predecessor_manifest": predecessor_manifest,
        "plan": plan,
        "result_evidence": result_evidence,
        "process_evidence": process_evidence,
        "ingestion_pack": built.ingestion_pack,
        "receipt": built.receipt,
    }

def clone_fixture() -> dict[str, Any]:
    return deepcopy(build_fixture())

if __name__ == "__main__":
    import json
    print(json.dumps(build_fixture(), indent=2, sort_keys=True))
