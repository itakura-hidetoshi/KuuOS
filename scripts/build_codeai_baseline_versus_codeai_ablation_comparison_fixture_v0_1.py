from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_schema_v0_1 import *
from runtime.kuuos_codeai_baseline_versus_codeai_ablation_comparison_v0_1 import (
    build_codeai_baseline_versus_codeai_ablation_comparison,
)

CONTROLLER_COMMIT = "b842d6bd04aad4f202d41e400d7130c64f4d054f"
EPOCH = 4000
PREDECESSOR_INGESTION_PACK = "f1c2a5d24c4d1a54e2e539ca7fef7c409c10aae83b4f5815174674b7df8db9e6"
PREDECESSOR_RECEIPT = "3e1711fa4aa26feb8a19feb8829f44ceb06a0e7a23f1bbf32c8db67615f3191f"

BASELINE_COHORT = "baseline-deterministic-patch"
CODEAI_COHORT = "codeai-full"
ABLATION_COHORTS = [
    "ablation-no-repair-memory",
    "ablation-no-specialist-routing",
    "ablation-no-evidence-weighted-selection",
]
COHORT_IDS = [BASELINE_COHORT, CODEAI_COHORT, *ABLATION_COHORTS]
METRIC_IDS = [
    "resolved-rate",
    "fail-to-pass-success-rate",
    "pass-to-pass-preservation-rate",
    "execution-valid-rate",
    "error-rate",
]

PREDECESSOR_MANIFEST = {
    "candidate_generation_feedback_enabled": False,
    "comparison_authority_granted": False,
    "correctness_claimed": False,
    "decision": "external_result_process_evidence_ingestion_admitted",
    "execution_valid": True,
    "external_observation_digest": "689b63a246192b45af75f512aba7478ad87db7aba90689d96fc0aa91bc28cbca",
    "fail_to_pass_failure_count": 1,
    "fail_to_pass_success_count": 0,
    "git_authority_granted": False,
    "ingestion_pack_digest": PREDECESSOR_INGESTION_PACK,
    "instance_id": "sympy__sympy-20590",
    "outcome_disposition": "measured_unresolved",
    "pass_to_pass_failure_count": 0,
    "pass_to_pass_success_count": 21,
    "predecessor_artifact_digest": "27f69ffd9a982956d2bbc2aaeecc9e45ed527ea522afda324e0e3665b634c5a2",
    "predecessor_artifact_id": 8520539325,
    "predecessor_workflow_run_id": 29894633457,
    "prediction_digest": "9a2aeff25ca565214ecbae781f20df4c23eea20db72b135702aa56d5de238050",
    "profile_version": "CodeAI External Result and Process-Evidence Ingestion v0.1",
    "raw_gold_ingested": False,
    "raw_logs_committed": False,
    "raw_test_names_ingested": False,
    "receipt_digest": PREDECESSOR_RECEIPT,
    "repair_memory_feedback_enabled": False,
    "repository_mutation_authority_granted": False,
    "resolved": False,
}

def h(label: str) -> str:
    return canonical_digest({"label": label})

def _cohort(
    cohort_id: str,
    role: str,
    system_variant: str,
    sample_binding_digest: str,
    holdout_partition_digest: str,
) -> dict[str, Any]:
    return {
        "cohort_id": cohort_id,
        "role": role,
        "system_variant": system_variant,
        "target_sample_count": 100,
        "sample_binding_digest": sample_binding_digest,
        "holdout_partition_digest": holdout_partition_digest,
        "frozen_before_observation": True,
        "aggregate_only": True,
        "gold_access_granted": False,
        "raw_test_name_access_granted": False,
        "raw_log_access_granted": False,
        "candidate_feedback_enabled": False,
        "repair_memory_feedback_enabled": False,
    }

def _pending_observation(
    cohort_id: str,
    sample_binding_digest: str,
    holdout_partition_digest: str,
) -> dict[str, Any]:
    return {
        "cohort_id": cohort_id,
        "evidence_state": "pending",
        "source_kind": "pending-preregistered",
        "source_receipt_digest": h("pending-observation:" + cohort_id),
        "sample_binding_digest": sample_binding_digest,
        "holdout_partition_digest": holdout_partition_digest,
        "sample_count": 0,
        "execution_valid_count": 0,
        "resolved_count": 0,
        "fail_to_pass_success_count": 0,
        "fail_to_pass_failure_count": 0,
        "pass_to_pass_success_count": 0,
        "pass_to_pass_failure_count": 0,
        "error_count": 0,
        "metric_values_complete": False,
        "raw_gold_included": False,
        "raw_test_names_included": False,
        "raw_logs_included": False,
        "observation_created_epoch": EPOCH - 1,
    }

def build_fixture() -> dict[str, Any]:
    predecessor_manifest = deepcopy(PREDECESSOR_MANIFEST)
    sample_binding_digest = canonical_digest({
        "dataset": "princeton-nlp/SWE-bench_Verified",
        "dataset_revision": "c104f840cc67f8b6eec6f759ebc8b2693d585d4a",
        "selection_rule": "frozen-balanced-holdout-v0.1",
        "target_sample_count_per_cohort": 100,
    })
    holdout_partition_digest = canonical_digest({
        "partition": "comparison-holdout-v0.1",
        "gold_hidden": True,
        "raw_test_names_hidden": True,
        "same_instances_across_cohorts": True,
    })
    binding = {
        "controller_repository": "itakura-hidetoshi/KuuOS",
        "controller_source_commit_sha": CONTROLLER_COMMIT,
        "predecessor_manifest_digest": canonical_digest(predecessor_manifest),
        "predecessor_ingestion_pack_digest": PREDECESSOR_INGESTION_PACK,
        "predecessor_receipt_digest": PREDECESSOR_RECEIPT,
        "sample_binding_digest": sample_binding_digest,
        "holdout_partition_digest": holdout_partition_digest,
        "comparison_contract_digest": h("baseline-versus-codeai-ablation-comparison-contract-v0.1"),
    }

    request = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "baseline-codeai-ablation-comparison-request-001",
        "request_revision": "baseline-codeai-ablation-comparison-rev-001",
        **binding,
        "request_created_epoch": EPOCH - 10,
        "comparison_phase": "preregistration",
        "claims_raw_gold_access": False,
        "claims_raw_test_name_access": False,
        "claims_raw_log_access": False,
        "claims_candidate_generation_feedback": False,
        "claims_repair_memory_feedback": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
        "claims_correctness": False,
    }, REQUEST_DIGEST_FIELD)

    policy = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + key: value for key, value in binding.items()},
        "evaluation_epoch": EPOCH,
        "maximum_request_age": 100,
        "maximum_registry_age": 100,
        "required_cohort_ids": COHORT_IDS,
        "required_metric_ids": METRIC_IDS,
        "required_ablation_count": len(ABLATION_COHORTS),
        "required_primary_metric_count": 1,
        "require_exact_binding": True,
        "require_predecessor_admitted": True,
        "require_predecessor_execution_valid": True,
        "require_aggregate_only": True,
        "require_frozen_holdout": True,
        "require_equal_target_sample_count": True,
        "require_balanced_measured_cohorts": True,
        "require_execution_failure_as_unresolved": True,
        "require_missing_evidence_hold": True,
        "allow_preregistration_with_pending_observations": True,
        "allow_limited_comparison_authority": True,
        "allow_raw_gold_access": False,
        "allow_raw_test_names": False,
        "allow_raw_logs": False,
        "allow_candidate_feedback": False,
        "allow_repair_memory_feedback": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
        "allow_correctness_claim": False,
    }, POLICY_DIGEST_FIELD)

    cohort_registry = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "cohort_registry_id": "baseline-codeai-ablation-cohorts-001",
        "registry_created_epoch": EPOCH - 8,
        "cohorts": [
            _cohort(BASELINE_COHORT, "baseline", "deterministic-patch-baseline-v0.1",
                    sample_binding_digest, holdout_partition_digest),
            _cohort(CODEAI_COHORT, "codeai", "kuuos-codeai-full-v0.1",
                    sample_binding_digest, holdout_partition_digest),
            _cohort(ABLATION_COHORTS[0], "ablation", "kuuos-codeai-without-repair-memory-v0.1",
                    sample_binding_digest, holdout_partition_digest),
            _cohort(ABLATION_COHORTS[1], "ablation", "kuuos-codeai-without-specialist-routing-v0.1",
                    sample_binding_digest, holdout_partition_digest),
            _cohort(ABLATION_COHORTS[2], "ablation", "kuuos-codeai-without-evidence-weighted-selection-v0.1",
                    sample_binding_digest, holdout_partition_digest),
        ],
    }, COHORT_DIGEST_FIELD)

    metric_registry = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "metric_registry_id": "baseline-codeai-ablation-metrics-001",
        "registry_created_epoch": EPOCH - 7,
        "metrics": [
            {
                "metric_id": "resolved-rate",
                "metric_kind": "ratio",
                "numerator_field": "resolved_count",
                "denominator_field": "sample_count",
                "direction": "higher-is-better",
                "primary": True,
                "missing_evidence_disposition": "hold",
                "execution_failure_disposition": "count-as-unresolved",
                "predeclared": True,
            },
            {
                "metric_id": "fail-to-pass-success-rate",
                "metric_kind": "ratio",
                "numerator_field": "fail_to_pass_success_count",
                "denominator_field": "fail_to_pass_total_count",
                "direction": "higher-is-better",
                "primary": False,
                "missing_evidence_disposition": "hold",
                "execution_failure_disposition": "count-as-unresolved",
                "predeclared": True,
            },
            {
                "metric_id": "pass-to-pass-preservation-rate",
                "metric_kind": "ratio",
                "numerator_field": "pass_to_pass_success_count",
                "denominator_field": "pass_to_pass_total_count",
                "direction": "higher-is-better",
                "primary": False,
                "missing_evidence_disposition": "hold",
                "execution_failure_disposition": "count-as-unresolved",
                "predeclared": True,
            },
            {
                "metric_id": "execution-valid-rate",
                "metric_kind": "ratio",
                "numerator_field": "execution_valid_count",
                "denominator_field": "sample_count",
                "direction": "higher-is-better",
                "primary": False,
                "missing_evidence_disposition": "hold",
                "execution_failure_disposition": "count-as-unresolved",
                "predeclared": True,
            },
            {
                "metric_id": "error-rate",
                "metric_kind": "ratio",
                "numerator_field": "error_count",
                "denominator_field": "sample_count",
                "direction": "lower-is-better",
                "primary": False,
                "missing_evidence_disposition": "hold",
                "execution_failure_disposition": "count-as-unresolved",
                "predeclared": True,
            },
        ],
    }, METRIC_DIGEST_FIELD)

    observations = [
        _pending_observation(BASELINE_COHORT, sample_binding_digest, holdout_partition_digest),
        {
            "cohort_id": CODEAI_COHORT,
            "evidence_state": "measured",
            "source_kind": "admitted-ingestion-receipt",
            "source_receipt_digest": PREDECESSOR_RECEIPT,
            "sample_binding_digest": sample_binding_digest,
            "holdout_partition_digest": holdout_partition_digest,
            "sample_count": 1,
            "execution_valid_count": 1,
            "resolved_count": 0,
            "fail_to_pass_success_count": 0,
            "fail_to_pass_failure_count": 1,
            "pass_to_pass_success_count": 21,
            "pass_to_pass_failure_count": 0,
            "error_count": 0,
            "metric_values_complete": True,
            "raw_gold_included": False,
            "raw_test_names_included": False,
            "raw_logs_included": False,
            "observation_created_epoch": EPOCH - 1,
        },
        *[
            _pending_observation(cohort_id, sample_binding_digest, holdout_partition_digest)
            for cohort_id in ABLATION_COHORTS
        ],
    ]
    observation_registry = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "observation_registry_id": "baseline-codeai-ablation-observations-001",
        "registry_created_epoch": EPOCH - 6,
        "observation_mode": "aggregate-only-preregistration",
        "observations": observations,
    }, OBSERVATION_DIGEST_FIELD)

    plan = seal({
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding,
        "comparison_id": "baseline-codeai-ablation-comparison-001",
        "comparison_phase": "preregistration",
        "comparison_mode": "aggregate-only-preregistered",
        "cohort_registry_id": cohort_registry["cohort_registry_id"],
        "metric_registry_id": metric_registry["metric_registry_id"],
        "observation_registry_id": observation_registry["observation_registry_id"],
        "baseline_cohort_id": BASELINE_COHORT,
        "codeai_cohort_id": CODEAI_COHORT,
        "ablation_cohort_ids": ABLATION_COHORTS,
        "comparison_pairs": [
            [BASELINE_COHORT, CODEAI_COHORT],
            *[[CODEAI_COHORT, cohort_id] for cohort_id in ABLATION_COHORTS],
        ],
        "aggregate_only": True,
        "holdout_frozen": True,
        "missing_evidence_disposition": "hold",
        "execution_failure_disposition": "count-as-unresolved",
        "comparison_direction_predeclared": True,
        "limited_comparison_authority_granted": True,
        "repository_mutation_authority_granted": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "plan_created_epoch": EPOCH - 5,
    }, PLAN_DIGEST_FIELD)

    built = build_codeai_baseline_versus_codeai_ablation_comparison(
        request=request,
        policy=policy,
        predecessor_manifest=predecessor_manifest,
        plan=plan,
        cohort_registry=cohort_registry,
        metric_registry=metric_registry,
        observation_registry=observation_registry,
    )
    assert built.status == STATUS_ADMITTED, built.reasons
    assert built.comparison_pack is not None and built.receipt is not None
    return {
        "request": request,
        "policy": policy,
        "predecessor_manifest": predecessor_manifest,
        "plan": plan,
        "cohort_registry": cohort_registry,
        "metric_registry": metric_registry,
        "observation_registry": observation_registry,
        "comparison_pack": built.comparison_pack,
        "receipt": built.receipt,
    }

def clone_fixture() -> dict[str, Any]:
    return deepcopy(build_fixture())

if __name__ == "__main__":
    import json
    print(json.dumps(build_fixture(), indent=2, sort_keys=True))
