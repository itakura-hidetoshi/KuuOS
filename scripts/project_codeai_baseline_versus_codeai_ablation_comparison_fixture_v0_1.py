from __future__ import annotations

from typing import Any

from scripts.build_codeai_baseline_versus_codeai_ablation_comparison_fixture_v0_1 import build_fixture


def project_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    pack = fixture["comparison_pack"]
    receipt = fixture["receipt"]
    codeai = next(
        item
        for item in fixture["observation_registry"]["observations"]
        if item["cohort_id"] == fixture["plan"]["codeai_cohort_id"]
    )
    return {
        "profile_version": pack["profile_version"],
        "decision": pack["decision"],
        "comparison_phase": pack["comparison_phase"],
        "predecessor_manifest_digest": pack["predecessor_manifest_digest"],
        "predecessor_ingestion_pack_digest": pack["predecessor_ingestion_pack_digest"],
        "predecessor_receipt_digest": pack["predecessor_receipt_digest"],
        "sample_binding_digest": pack["sample_binding_digest"],
        "holdout_partition_digest": pack["holdout_partition_digest"],
        "comparison_contract_digest": pack["comparison_contract_digest"],
        "cohort_registry_digest": pack["cohort_registry_digest"],
        "metric_registry_digest": pack["metric_registry_digest"],
        "observation_registry_digest": pack["observation_registry_digest"],
        "comparison_pack_digest": pack["comparison_pack_digest"],
        "receipt_digest": receipt["comparison_receipt_digest"],
        "cohort_ids": pack["cohort_ids"],
        "metric_ids": pack["metric_ids"],
        "pending_cohort_ids": pack["pending_cohort_ids"],
        "preregistration_completed": pack["preregistration_completed"],
        "performance_comparison_completed": pack["performance_comparison_completed"],
        "codeai_measured_sample_count": codeai["sample_count"],
        "codeai_measured_resolved_count": codeai["resolved_count"],
        "limited_aggregate_comparison_authority_granted": pack[
            "limited_aggregate_comparison_authority_granted"
        ],
        "raw_gold_visible": pack["raw_gold_visible"],
        "raw_test_names_visible": pack["raw_test_names_visible"],
        "raw_logs_visible": pack["raw_logs_visible"],
        "repository_mutation_authority_granted": pack[
            "repository_mutation_authority_granted"
        ],
        "git_authority_granted": pack["git_authority_granted"],
        "correctness_claimed": pack["correctness_claimed"],
        "performance_claimed": pack["performance_claimed"],
    }


def project_example(fixture: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": fixture["request"]["schema_version"],
        "profile_version": fixture["request"]["profile_version"],
        "comparison_phase": fixture["request"]["comparison_phase"],
        "request_digest": fixture["request"]["comparison_request_digest"],
        "policy_digest": fixture["policy"]["comparison_policy_digest"],
        "plan_digest": fixture["plan"]["comparison_plan_digest"],
        "cohort_registry_digest": fixture["cohort_registry"]["cohort_registry_digest"],
        "metric_registry_digest": fixture["metric_registry"]["metric_registry_digest"],
        "observation_registry_digest": fixture["observation_registry"][
            "observation_registry_digest"
        ],
        "cohorts": [
            {
                "cohort_id": item["cohort_id"],
                "role": item["role"],
                "target_sample_count": item["target_sample_count"],
            }
            for item in fixture["cohort_registry"]["cohorts"]
        ],
        "metrics": [
            {
                "metric_id": item["metric_id"],
                "direction": item["direction"],
                "primary": item["primary"],
            }
            for item in fixture["metric_registry"]["metrics"]
        ],
        "observations": [
            {
                "cohort_id": item["cohort_id"],
                "evidence_state": item["evidence_state"],
                "sample_count": item["sample_count"],
                "resolved_count": item["resolved_count"],
            }
            for item in fixture["observation_registry"]["observations"]
        ],
        "comparison_pack_digest": fixture["comparison_pack"]["comparison_pack_digest"],
        "receipt_digest": fixture["receipt"]["comparison_receipt_digest"],
        "performance_comparison_completed": fixture["comparison_pack"][
            "performance_comparison_completed"
        ],
    }


if __name__ == "__main__":
    import json
    print(json.dumps(project_fixture(build_fixture()), indent=2, sort_keys=True))
