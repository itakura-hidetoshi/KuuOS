from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_external_corpus_acquisition_freeze_receipt_schema_v0_1 import (
    BINDING_FIELDS,
    PREDECESSOR_PROFILE_VERSION,
    canonical_digest,
)


def binding_mismatches(source: Mapping[str, Any], target: Mapping[str, Any]) -> list[str]:
    return [field for field in BINDING_FIELDS if source.get(field) != target.get(field)]


def validate_predecessor_manifest(manifest: Mapping[str, Any]) -> list[str]:
    required = {
        "adapter_decision", "adapter_pack_digest", "benchmark_id", "benchmark_result_ingested",
        "controller_source_commit_sha", "correctness_claimed", "dataset_name", "evaluation_mode",
        "expected_instance_count", "git_authority_granted", "harness_commit_sha",
        "harness_execution_performed", "harness_repository", "hold_reasons",
        "network_access_performed", "official_prediction_fields", "official_predictions_digest",
        "prediction_count", "profile_version", "protocol_projection_only", "receipt_digest",
        "repository_mutation_performed", "sample_count", "secret_access_performed", "split",
    }
    issues: list[str] = []
    missing = required.difference(manifest)
    extra = set(manifest).difference(required)
    if missing:
        issues.append("predecessor_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("predecessor_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if manifest["profile_version"] != PREDECESSOR_PROFILE_VERSION:
        issues.append("predecessor_profile_invalid")
    if manifest["adapter_decision"] != "external_benchmark_protocol_admitted":
        issues.append("predecessor_not_admitted")
    if manifest["benchmark_id"] != "swe-bench-verified":
        issues.append("predecessor_benchmark_invalid")
    if manifest["dataset_name"] != "princeton-nlp/SWE-bench_Verified" or manifest["split"] != "test":
        issues.append("predecessor_dataset_invalid")
    if manifest["expected_instance_count"] != 500:
        issues.append("predecessor_instance_count_invalid")
    if manifest["protocol_projection_only"] is not True:
        issues.append("predecessor_projection_boundary_missing")
    if manifest["hold_reasons"]:
        issues.append("predecessor_hold_reasons_present")
    for field in (
        "benchmark_result_ingested", "harness_execution_performed", "network_access_performed",
        "repository_mutation_performed", "secret_access_performed", "git_authority_granted",
        "correctness_claimed",
    ):
        if manifest[field] is not False:
            issues.append("predecessor_forbidden_effect:" + field)
    return sorted(set(issues))


def predecessor_digest(manifest: Mapping[str, Any]) -> str:
    return canonical_digest(manifest)


__all__ = ["binding_mismatches", "predecessor_digest", "validate_predecessor_manifest"]
