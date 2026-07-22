from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_external_result_process_evidence_ingestion_schema_v0_1 import (
    PACK_DIGEST_FIELD, RECEIPT_DIGEST_FIELD,
)

def project_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    pack = fixture["ingestion_pack"]
    receipt = fixture["receipt"]
    return {
        "profile_version": pack["profile_version"],
        "decision": pack["decision"],
        "instance_id": pack["instance_id"],
        "prediction_digest": pack["prediction_digest"],
        "predecessor_workflow_run_id": pack["predecessor_workflow_run_id"],
        "predecessor_artifact_id": pack["predecessor_artifact_id"],
        "predecessor_artifact_digest": pack["predecessor_artifact_digest"],
        "external_observation_digest": pack["external_observation_digest"],
        "outcome_disposition": pack["outcome_disposition"],
        "execution_valid": pack["execution_valid"],
        "resolved": pack["resolved"],
        "fail_to_pass_success_count": pack["fail_to_pass_success_count"],
        "fail_to_pass_failure_count": pack["fail_to_pass_failure_count"],
        "pass_to_pass_success_count": pack["pass_to_pass_success_count"],
        "pass_to_pass_failure_count": pack["pass_to_pass_failure_count"],
        "raw_gold_ingested": pack["raw_gold_ingested"],
        "raw_test_names_ingested": pack["raw_test_names_ingested"],
        "raw_logs_committed": pack["raw_logs_committed"],
        "candidate_generation_feedback_enabled": pack["candidate_generation_feedback_enabled"],
        "repair_memory_feedback_enabled": pack["repair_memory_feedback_enabled"],
        "comparison_authority_granted": pack["comparison_authority_granted"],
        "repository_mutation_authority_granted": pack["repository_mutation_authority_granted"],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "ingestion_pack_digest": pack[PACK_DIGEST_FIELD],
        "receipt_digest": receipt[RECEIPT_DIGEST_FIELD],
    }
