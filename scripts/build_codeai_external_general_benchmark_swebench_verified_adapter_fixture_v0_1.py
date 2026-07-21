from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_schema_v0_1 import *
from runtime.kuuos_codeai_external_general_benchmark_swebench_verified_adapter_v0_1 import (
    build_codeai_external_general_benchmark_swebench_verified_adapter,
)

CONTROLLER_COMMIT = "f5bf17314041e0cdfefb5862990e6c1abea320d6"
HARNESS_COMMIT = "f7bbbb2ccdf479001d6467c9e34af59e44a840f9"
EPOCH = 1784678400


def h(label: str) -> str:
    return canonical_digest({"label": label})


def _instance(instance_id: str, base_commit: str, protected_paths: list[str]) -> dict[str, Any]:
    return seal(
        {
            "instance_id": instance_id,
            "base_commit_sha": base_commit,
            "problem_statement_digest": h("problem:" + instance_id),
            "test_patch_digest": h("test-patch:" + instance_id),
            "protected_test_paths": protected_paths,
            "instance_contract_created_epoch": EPOCH - 300,
        },
        INSTANCE_CONTRACT_DIGEST_FIELD,
    )


def _prediction(
    *,
    instance: dict[str, Any],
    model_patch: str,
    changed_paths: list[str],
    session: str,
) -> dict[str, Any]:
    return seal(
        {
            "instance_id": instance["instance_id"],
            "model_name_or_path": "kuuos-codeai/reference-provider-v0.1",
            "model_patch": model_patch,
            "changed_paths": changed_paths,
            "instance_contract_digest": instance[INSTANCE_CONTRACT_DIGEST_FIELD],
            "codeai_candidate_receipt_digest": h("candidate-receipt:" + instance["instance_id"]),
            "provider_session_digest": h("provider-session:" + session),
            "prediction_created_epoch": EPOCH - 60,
            "claims_harness_result": False,
            "claims_correctness": False,
        },
        PREDICTION_DIGEST_FIELD,
    )


def build_fixture() -> dict[str, Any]:
    instances = [
        _instance(
            "sympy__sympy-20590",
            "1" * 40,
            ["sympy/core/tests/test_basic.py"],
        ),
        _instance(
            "django__django-16877",
            "2" * 40,
            ["tests/template_tests/filter_tests/test_escapeseq.py"],
        ),
        _instance(
            "astropy__astropy-12907",
            "3" * 40,
            ["astropy/modeling/tests/test_core.py"],
        ),
    ]

    benchmark_contract = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "benchmark_id": BENCHMARK_ID,
            "dataset_name": DATASET_NAME,
            "split": DATASET_SPLIT,
            "expected_instance_count": EXPECTED_INSTANCE_COUNT,
            "corpus_digest": h("reference-external-corpus-contract"),
            "instance_ids_digest": h("reference-external-500-instance-id-contract"),
            "harness_repository": HARNESS_REPOSITORY,
            "harness_commit_sha": HARNESS_COMMIT,
            "harness_entrypoint": HARNESS_ENTRYPOINT,
            "prediction_fields": list(OFFICIAL_PREDICTION_FIELDS),
            "containerized_harness": True,
            "official_harness": True,
            "corpus_frozen": True,
            "test_patch_paths_sealed": True,
            "contract_created_epoch": EPOCH - 600,
            "harness_execution_performed": False,
            "network_access_performed": False,
            "secret_access_performed": False,
            "repository_mutation_performed": False,
            "git_authority_granted": False,
            "correctness_claimed": False,
        },
        CONTRACT_DIGEST_FIELD,
    )

    instance_ids = [item["instance_id"] for item in instances]
    run_plan = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "run_id": "kuuos-swebench-verified-smoke-v0-1",
            "evaluation_mode": "smoke",
            "selection_method": "precommitted-lexicographic-three-instance-smoke",
            "instances": instances,
            "sample_count": len(instances),
            "selected_instance_ids_digest": canonical_digest(instance_ids),
            "selection_frozen_before_execution": True,
            "holdout_labels_exposed": False,
            "gold_patches_exposed": False,
            "max_workers": 1,
            "timeout_seconds": 1800,
            "cache_level": "env",
            "harness_execution_requested": False,
            "network_access_requested": False,
            "secret_access_requested": False,
            "repository_mutation_requested": False,
            "git_authority_requested": False,
            "correctness_claimed": False,
            "run_plan_created_epoch": EPOCH - 240,
        },
        RUN_PLAN_DIGEST_FIELD,
    )

    predictions = [
        _prediction(
            instance=instances[0],
            session="sympy",
            changed_paths=["sympy/core/basic.py"],
            model_patch=(
                "diff --git a/sympy/core/basic.py b/sympy/core/basic.py\n"
                "--- a/sympy/core/basic.py\n"
                "+++ b/sympy/core/basic.py\n"
                "@@ -1,1 +1,2 @@\n"
                " # reference protocol-only prediction\n"
                "+# no benchmark result is claimed\n"
            ),
        ),
        _prediction(
            instance=instances[1],
            session="django",
            changed_paths=["django/template/defaultfilters.py"],
            model_patch=(
                "diff --git a/django/template/defaultfilters.py b/django/template/defaultfilters.py\n"
                "--- a/django/template/defaultfilters.py\n"
                "+++ b/django/template/defaultfilters.py\n"
                "@@ -1,1 +1,2 @@\n"
                " # reference protocol-only prediction\n"
                "+# protected test paths are excluded\n"
            ),
        ),
        _prediction(
            instance=instances[2],
            session="astropy",
            changed_paths=["astropy/modeling/core.py"],
            model_patch=(
                "diff --git a/astropy/modeling/core.py b/astropy/modeling/core.py\n"
                "--- a/astropy/modeling/core.py\n"
                "+++ b/astropy/modeling/core.py\n"
                "@@ -1,1 +1,2 @@\n"
                " # reference protocol-only prediction\n"
                "+# external harness execution remains separate\n"
            ),
        ),
    ]

    model_configuration_digest = h("reference-model-configuration")
    codeai_pipeline_digest = h("codeai-main-f5bf173-pipeline")
    harness_contract_digest = h("official-harness-contract:" + HARNESS_COMMIT)
    evaluation_protocol_digest = h("external-general-benchmark-protocol-v0.1")
    source_tree_digest = h("kuuos-source-tree:" + CONTROLLER_COMMIT)

    binding = {
        "controller_repository_full_name": "itakura-hidetoshi/KuuOS",
        "controller_source_commit_sha": CONTROLLER_COMMIT,
        "controller_source_tree_digest": source_tree_digest,
        "benchmark_contract_digest": benchmark_contract[CONTRACT_DIGEST_FIELD],
        "run_plan_digest": run_plan[RUN_PLAN_DIGEST_FIELD],
        "model_configuration_digest": model_configuration_digest,
        "codeai_pipeline_digest": codeai_pipeline_digest,
        "harness_contract_digest": harness_contract_digest,
        "evaluation_protocol_digest": evaluation_protocol_digest,
    }

    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "request_id": "external-benchmark-request-v0-1",
            "request_revision": "reference-1",
            **binding,
            "request_created_epoch": EPOCH - 30,
            "unresolved_questions": [],
            "claims_harness_execution_authority": False,
            "claims_network_authority": False,
            "claims_secret_authority": False,
            "claims_repository_mutation_authority": False,
            "claims_git_authority": False,
            "claims_correctness": False,
        },
        REQUEST_DIGEST_FIELD,
    )

    policy = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            **{"expected_" + key: value for key, value in binding.items()},
            "evaluation_epoch": EPOCH,
            "maximum_request_age": 3600,
            "minimum_sample_count": 1,
            "maximum_sample_count": EXPECTED_INSTANCE_COUNT,
            "maximum_patch_bytes": 100_000,
            "maximum_total_patch_bytes": 20_000_000,
            "maximum_changed_paths_per_prediction": 32,
            "allowed_evaluation_modes": list(EVALUATION_MODES),
            "allowed_cache_levels": list(CACHE_LEVELS),
            "require_exact_binding": True,
            "require_official_verified_dataset": True,
            "require_expected_instance_count": True,
            "require_frozen_sample": True,
            "require_holdout_labels_hidden": True,
            "require_gold_patch_hidden": True,
            "require_pinned_harness": True,
            "require_containerized_harness": True,
            "require_official_prediction_shape": True,
            "require_unique_instances": True,
            "require_patch_digest": True,
            "require_derived_changed_paths": True,
            "require_protected_test_path_nonoverlap": True,
            "allow_protocol_projection": True,
            "allow_harness_execution": False,
            "allow_network_access": False,
            "allow_secret_access": False,
            "allow_repository_mutation": False,
            "allow_git_authority": False,
            "allow_correctness_claim": False,
        },
        POLICY_DIGEST_FIELD,
    )

    result = build_codeai_external_general_benchmark_swebench_verified_adapter(
        request=request,
        policy=policy,
        benchmark_contract=benchmark_contract,
        run_plan=run_plan,
        predictions=predictions,
    )
    assert result.status == STATUS_READY
    assert result.adapter_pack is not None and result.receipt is not None
    return {
        "request": request,
        "policy": policy,
        "benchmark_contract": benchmark_contract,
        "run_plan": run_plan,
        "predictions": predictions,
        "adapter_pack": result.adapter_pack,
        "receipt": result.receipt,
    }


def clone_fixture() -> dict[str, Any]:
    return deepcopy(build_fixture())


if __name__ == "__main__":
    import json
    print(json.dumps(build_fixture(), indent=2, sort_keys=True))
