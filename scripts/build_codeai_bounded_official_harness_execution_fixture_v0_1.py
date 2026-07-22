from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_bounded_official_harness_execution_schema_v0_1 import *
from runtime.kuuos_codeai_bounded_official_harness_execution_v0_1 import (
    build_codeai_bounded_official_harness_execution,
)

EPOCH = 2000
CONTROLLER_SHA = "51255adf60e78cba5569993a1164c6ba830f252f"
PREDECESSOR_EXTERNAL_ARTIFACT_DIGEST = "bf820bfff2f3a17e528b63777f5f30803b821bed67f7aa338116ef333a8d3b3d"
DATASET_SHA256 = "a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd"
HARNESS_SHA = "f7bbbb2ccdf479001d6467c9e34af59e44a840f9"
BASE_COMMIT = "cffd4e0f86fefd4802349a9f9b19ed70934ea354"
INSTANCE_ID = "sympy__sympy-20590"

MODEL_PATCH = 'diff --git a/sympy/core/_print_helpers.py b/sympy/core/_print_helpers.py\n--- a/sympy/core/_print_helpers.py\n+++ b/sympy/core/_print_helpers.py\n@@ -1,5 +1,6 @@\n """\n Base class to provide str and repr hooks that `init_printing` can overwrite.\n+This line is a bounded harness smoke marker and makes no correctness claim.\n\n This is exposed publicly in the `printing.defaults` module,\n but cannot be defined there without causing circular imports.\n'

PREDECESSOR_MANIFEST = {'correctness_claimed': False, 'dataset_artifact_sha256': 'a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd', 'dataset_name': 'princeton-nlp/SWE-bench_Verified', 'dataset_revision': 'c104f840cc67f8b6eec6f759ebc8b2693d585d4a', 'decision': 'gold_patch_environment_smoke_admitted', 'future_harness_execution_authority_granted': False, 'git_authority_granted': False, 'gold_patch_available_to_solver': False, 'harness_commit_sha': 'f7bbbb2ccdf479001d6467c9e34af59e44a840f9', 'harness_repository': 'swe-bench/SWE-bench', 'instance_id': 'sympy__sympy-20590', 'maximum_workers': 1, 'predecessor_manifest_digest': '561be27194532088736124afa7c11542bc72dd00f724f3a422be429892c08f2a', 'predictions_path': 'gold', 'profile_version': 'CodeAI Gold-Patch Environment Smoke Validation v0.1', 'receipt_digest': 'f9e1756bbd2e05a494088ff68732764647099d901e28da14553d0e13edec0223', 'repository_mutation_authority_granted': False, 'resolved': True, 'smoke_pack_digest': 'ebe734d57d827eb1602d1b5d489c650d2dc355d617ff5cac9c0f08363509c0b1', 'timeout_seconds': 1800}

def h(label: str) -> str:
    return canonical_digest({"label": label})

def build_fixture() -> dict[str, Any]:
    predecessor_manifest_digest = canonical_digest(PREDECESSOR_MANIFEST)
    execution_contract_digest = h("bounded-official-harness-execution-contract-v0.1")
    source_digest = canonical_digest({"model_patch": MODEL_PATCH})
    prediction = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "instance_id": INSTANCE_ID,
            "base_commit_sha": BASE_COMMIT,
            "model_name_or_path": "kuuos-codeai/bounded-smoke-v0.1",
            "model_patch": MODEL_PATCH,
            "changed_paths": ["sympy/core/_print_helpers.py"],
            "source_kind": "kuuos-deterministic-engineering-smoke",
            "source_locator": "scripts/build_codeai_bounded_official_harness_execution_fixture_v0_1.py",
            "source_digest": source_digest,
            "gold_derived": False,
            "gold_accessed": False,
            "candidate_receipt_digest": h("bounded-smoke-candidate-receipt"),
            "prediction_created_epoch": EPOCH - 20,
            "claims_resolved": False,
            "claims_correctness": False,
        },
        PREDICTION_DIGEST_FIELD,
    )
    prediction_file_digest = canonical_digest(official_prediction(prediction))
    binding = {
        "controller_repository": "itakura-hidetoshi/KuuOS",
        "controller_source_commit_sha": CONTROLLER_SHA,
        "predecessor_manifest_digest": predecessor_manifest_digest,
        "predecessor_smoke_pack_digest": PREDECESSOR_MANIFEST["smoke_pack_digest"],
        "predecessor_smoke_receipt_digest": PREDECESSOR_MANIFEST["receipt_digest"],
        "predecessor_external_artifact_digest": PREDECESSOR_EXTERNAL_ARTIFACT_DIGEST,
        "dataset_name": PREDECESSOR_MANIFEST["dataset_name"],
        "dataset_revision": PREDECESSOR_MANIFEST["dataset_revision"],
        "dataset_split": "test",
        "dataset_artifact_sha256": DATASET_SHA256,
        "harness_repository": PREDECESSOR_MANIFEST["harness_repository"],
        "harness_commit_sha": HARNESS_SHA,
        "instance_id": INSTANCE_ID,
        "base_commit_sha": BASE_COMMIT,
        "prediction_digest": prediction[PREDICTION_DIGEST_FIELD],
        "execution_contract_digest": execution_contract_digest,
    }
    request = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "request_id": "bounded-official-harness-request-001",
            "request_revision": "bounded-official-harness-rev-001",
            **binding,
            "request_created_epoch": EPOCH - 10,
            "claims_gold_access": False,
            "claims_kernel_harness_execution": False,
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
            "maximum_request_age": 100,
            "maximum_observation_age": 100,
            "required_sample_count": 1,
            "maximum_workers": 1,
            "timeout_seconds": 1800,
            "require_exact_binding": True,
            "require_predecessor_smoke_admitted": True,
            "require_frozen_sample": True,
            "require_frozen_prediction": True,
            "require_official_prediction_shape": True,
            "require_non_gold_prediction": True,
            "require_patch_applied": True,
            "require_evaluation_completed": True,
            "require_report_observed": True,
            "require_logs_observed": True,
            "allow_resolved_or_unresolved": True,
            "allow_kernel_harness_execution": False,
            "allow_gold_access": False,
            "allow_repository_mutation": False,
            "allow_git_authority": False,
            "allow_correctness_claim": False,
        },
        POLICY_DIGEST_FIELD,
    )
    execution_plan = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            **binding,
            "run_id": "kuuos-bounded-official-harness-001",
            "prediction_file_name": "codeai-bounded-official-predictions-v0-1.jsonl",
            "prediction_file_digest": prediction_file_digest,
            "sample_count": 1,
            "maximum_workers": 1,
            "timeout_seconds": 1800,
            "cache_level": "none",
            "clean_images": True,
            "sample_frozen": True,
            "prediction_frozen": True,
            "official_prediction_shape": True,
            "non_gold_prediction": True,
            "gold_available_to_solver": False,
            "plan_created_epoch": EPOCH - 9,
        },
        PLAN_DIGEST_FIELD,
    )
    observation = seal(
        {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            **binding,
            "observer_id": "reference-bounded-harness-observer-001",
            "run_id": execution_plan["run_id"],
            "observation_created_epoch": EPOCH - 1,
            "external_harness_execution_observed": True,
            "harness_execution_performed_by_kernel": False,
            "network_used_by_external_harness": True,
            "docker_used": True,
            "image_available": True,
            "container_started": True,
            "patch_applied": True,
            "evaluation_completed": True,
            "resolved": False,
            "report_observed": True,
            "logs_observed": True,
            "report_digest": h("bounded-report"),
            "test_output_digest": h("bounded-test-output"),
            "instance_log_digest": h("bounded-instance-log"),
            "gold_exposed_to_solver": False,
            "gold_used_for_candidate_generation": False,
            "gold_used_for_repair_memory": False,
            "repository_mutated": False,
            "git_authority": False,
            "correctness_claimed": False,
        },
        OBSERVATION_DIGEST_FIELD,
    )
    result = build_codeai_bounded_official_harness_execution(
        request=request,
        policy=policy,
        predecessor_manifest=PREDECESSOR_MANIFEST,
        execution_plan=execution_plan,
        prediction=prediction,
        observation=observation,
    )
    assert result.status == STATUS_ADMITTED
    assert result.execution_pack is not None and result.receipt is not None
    return {
        "request": request,
        "policy": policy,
        "predecessor_manifest": deepcopy(PREDECESSOR_MANIFEST),
        "execution_plan": execution_plan,
        "prediction": prediction,
        "observation": observation,
        "execution_pack": result.execution_pack,
        "receipt": result.receipt,
    }

def clone_fixture() -> dict[str, Any]:
    return deepcopy(build_fixture())

if __name__ == "__main__":
    import json
    print(json.dumps(build_fixture(), indent=2, sort_keys=True))
