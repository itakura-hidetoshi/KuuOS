from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_schema_v0_1 import (
    OBSERVATION_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    PROFILE_VERSION,
    REQUEST_DIGEST_FIELD,
    RESTRICTED_EVALUATOR_FIELDS,
    SCHEMA_COLUMNS,
    SCHEMA_VERSION,
    SOLVER_VISIBLE_FIELDS,
    canonical_digest,
    seal,
)
from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_v0_1 import (
    build_codeai_external_corpus_acquisition_freeze_receipt,
)

CONTROLLER_REPOSITORY = "itakura-hidetoshi/KuuOS"
CONTROLLER_SOURCE_COMMIT_SHA = "e07e32b76bebd3e260dbe1847080e29b3ffe6346"
PREDECESSOR_MANIFEST_DIGEST = "a5310fcfdb5d6c8ee99d66eb56d4d0f3cdd76152582c620f3b8dd6aa597b688d"
PREDECESSOR_PACK_DIGEST = "134475fc54fc23d0bcb48973b9fcfd158da51fa6a95ea4eff083a500f7936107"
PREDECESSOR_RECEIPT_DIGEST = "55233619cdc23640818f305564ee08652e5f9817cb0260128256c4d3ddfd7b73"
DATASET_NAME = "princeton-nlp/SWE-bench_Verified"
DATASET_REVISION = "c104f840cc67f8b6eec6f759ebc8b2693d585d4a"
DATASET_SPLIT = "test"
ARTIFACT_PATH = "data/test-00000-of-00001.parquet"
ARTIFACT_SHA256 = "a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd"
ARTIFACT_SIZE_BYTES = 2_096_679
EXPECTED_ROW_COUNT = 500
SOURCE_URI = (
    "https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified/resolve/"
    + DATASET_REVISION
    + "/"
    + ARTIFACT_PATH
)
SCHEMA_DIGEST = canonical_digest([{"name": name, "dtype": "string"} for name in SCHEMA_COLUMNS])
SOLVER_FIELDS_DIGEST = canonical_digest(list(SOLVER_VISIBLE_FIELDS))
RESTRICTED_FIELDS_DIGEST = canonical_digest(list(RESTRICTED_EVALUATOR_FIELDS))
ACQUISITION_CONTRACT_DIGEST = canonical_digest({
    "source_uri": SOURCE_URI,
    "fetch_method": "https-content-addressed",
    "expected_sha256": ARTIFACT_SHA256,
    "expected_size_bytes": ARTIFACT_SIZE_BYTES,
    "expected_row_count": EXPECTED_ROW_COUNT,
    "schema_digest": SCHEMA_DIGEST,
    "observer_independent": True,
})
FREEZE_POLICY_DIGEST = canonical_digest({
    "immutable": True,
    "content_addressed": True,
    "solver_visible_fields": list(SOLVER_VISIBLE_FIELDS),
    "restricted_evaluator_fields": list(RESTRICTED_EVALUATOR_FIELDS),
    "gold_patch_hidden": True,
    "test_patch_hidden": True,
    "evaluation_labels_hidden": True,
})
EVALUATION_EPOCH = 1_780_000_000


def binding() -> dict[str, Any]:
    return {
        "controller_repository": CONTROLLER_REPOSITORY,
        "controller_source_commit_sha": CONTROLLER_SOURCE_COMMIT_SHA,
        "predecessor_manifest_digest": PREDECESSOR_MANIFEST_DIGEST,
        "predecessor_adapter_pack_digest": PREDECESSOR_PACK_DIGEST,
        "predecessor_adapter_receipt_digest": PREDECESSOR_RECEIPT_DIGEST,
        "benchmark_id": "swe-bench-verified",
        "dataset_name": DATASET_NAME,
        "dataset_revision": DATASET_REVISION,
        "dataset_split": DATASET_SPLIT,
        "artifact_path": ARTIFACT_PATH,
        "artifact_sha256": ARTIFACT_SHA256,
        "artifact_size_bytes": ARTIFACT_SIZE_BYTES,
        "expected_row_count": EXPECTED_ROW_COUNT,
        "schema_digest": SCHEMA_DIGEST,
        "solver_visible_fields_digest": SOLVER_FIELDS_DIGEST,
        "restricted_evaluator_fields_digest": RESTRICTED_FIELDS_DIGEST,
        "acquisition_contract_digest": ACQUISITION_CONTRACT_DIGEST,
        "freeze_policy_digest": FREEZE_POLICY_DIGEST,
    }


def predecessor_manifest() -> dict[str, Any]:
    return {
        "adapter_decision": "external_benchmark_protocol_admitted",
        "adapter_pack_digest": PREDECESSOR_PACK_DIGEST,
        "benchmark_id": "swe-bench-verified",
        "benchmark_result_ingested": False,
        "controller_source_commit_sha": "f5bf17314041e0cdfefb5862990e6c1abea320d6",
        "correctness_claimed": False,
        "dataset_name": DATASET_NAME,
        "evaluation_mode": "smoke",
        "expected_instance_count": EXPECTED_ROW_COUNT,
        "git_authority_granted": False,
        "harness_commit_sha": "f7bbbb2ccdf479001d6467c9e34af59e44a840f9",
        "harness_execution_performed": False,
        "harness_repository": "swe-bench/SWE-bench",
        "hold_reasons": [],
        "network_access_performed": False,
        "official_prediction_fields": ["instance_id", "model_name_or_path", "model_patch"],
        "official_predictions_digest": "6c120860918f9ff0cd8bf0bbf2f22210fbe66a6426551514be024a4159e2485e",
        "prediction_count": 3,
        "profile_version": "CodeAI External General Benchmark Protocol and SWE-bench Verified Adapter v0.1",
        "protocol_projection_only": True,
        "receipt_digest": PREDECESSOR_RECEIPT_DIGEST,
        "repository_mutation_performed": False,
        "sample_count": 3,
        "secret_access_performed": False,
        "split": DATASET_SPLIT,
    }


def request() -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "request_id": "external-corpus-freeze-001",
        "request_revision": "r1",
        **binding(),
        "request_created_epoch": EVALUATION_EPOCH - 30,
        "unresolved_questions": [],
        "claims_solver_label_access": False,
        "claims_gold_patch_access": False,
        "claims_harness_execution_authority": False,
        "claims_repository_mutation_authority": False,
        "claims_git_authority": False,
        "claims_correctness": False,
    }
    return seal(value, REQUEST_DIGEST_FIELD)


def policy() -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **{"expected_" + key: item for key, item in binding().items()},
        "evaluation_epoch": EVALUATION_EPOCH,
        "maximum_request_age": 600,
        "maximum_observation_age": 600,
        "require_exact_binding": True,
        "require_predecessor_admitted": True,
        "require_pinned_revision": True,
        "require_artifact_sha256": True,
        "require_artifact_size": True,
        "require_row_count": True,
        "require_schema": True,
        "require_independent_observation": True,
        "require_content_addressed_storage": True,
        "require_immutable_freeze": True,
        "require_solver_field_partition": True,
        "allow_external_fetch_evidence": True,
        "allow_solver_label_access": False,
        "allow_gold_patch_access": False,
        "allow_harness_execution": False,
        "allow_repository_mutation": False,
        "allow_git_authority": False,
        "allow_correctness_claim": False,
    }
    return seal(value, POLICY_DIGEST_FIELD)


def acquisition_observation() -> dict[str, Any]:
    value = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        **binding(),
        "observation_id": "hf-artifact-observation-001",
        "observer_id": "external-fetcher-hf-001",
        "observation_created_epoch": EVALUATION_EPOCH - 10,
        "source_uri": SOURCE_URI,
        "fetch_completed": True,
        "fetch_performed_by_kernel": False,
        "network_access_performed_by_fetcher": True,
        "artifact_observed": True,
        "artifact_sha256_verified": True,
        "artifact_size_verified": True,
        "row_count_verified": True,
        "schema_verified": True,
        "solver_field_partition_verified": True,
        "content_addressed_storage": True,
        "immutable_freeze": True,
        "artifact_copy_committed_to_repository": False,
        "gold_patch_exposed_to_solver": False,
        "test_patch_exposed_to_solver": False,
        "evaluation_labels_exposed_to_solver": False,
        "harness_execution_performed": False,
        "repository_mutation_performed": False,
        "git_authority_granted": False,
        "correctness_claimed": False,
        "observed_row_count": EXPECTED_ROW_COUNT,
        "observed_schema_columns": list(SCHEMA_COLUMNS),
        "solver_visible_fields": list(SOLVER_VISIBLE_FIELDS),
        "restricted_evaluator_fields": list(RESTRICTED_EVALUATOR_FIELDS),
    }
    return seal(value, OBSERVATION_DIGEST_FIELD)


def build_fixture() -> dict[str, Any]:
    pred = predecessor_manifest()
    req = request()
    pol = policy()
    obs = acquisition_observation()
    result = build_codeai_external_corpus_acquisition_freeze_receipt(
        request=req, policy=pol, predecessor_manifest=pred, acquisition_observation=obs
    )
    assert result.status == "ready", result.issues
    assert result.freeze_pack is not None and result.receipt is not None
    return {
        "predecessor_manifest": pred,
        "request": req,
        "policy": pol,
        "acquisition_observation": obs,
        "freeze_pack": result.freeze_pack,
        "receipt": result.receipt,
    }


def held_variant(field: str, value: Any) -> dict[str, Any]:
    fixture = build_fixture()
    obs = deepcopy(fixture["acquisition_observation"])
    obs[field] = value
    obs = seal(obs, OBSERVATION_DIGEST_FIELD)
    result = build_codeai_external_corpus_acquisition_freeze_receipt(
        request=fixture["request"], policy=fixture["policy"],
        predecessor_manifest=fixture["predecessor_manifest"], acquisition_observation=obs
    )
    assert result.status == "ready"
    assert result.freeze_pack is not None and result.receipt is not None
    return {"observation": obs, "freeze_pack": result.freeze_pack, "receipt": result.receipt}


if __name__ == "__main__":
    import json
    print(json.dumps(build_fixture(), indent=2, sort_keys=True))
