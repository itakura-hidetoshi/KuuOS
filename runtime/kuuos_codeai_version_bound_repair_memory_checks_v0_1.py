from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD as SOURCE_CLASSIFICATION_DIGEST_FIELD,
    DISPOSITION_COMPLETED as SOURCE_DISPOSITION_COMPLETED,
    MODE_CLASSIFICATION_ONLY,
    RECEIPT_DIGEST_FIELD as SOURCE_CLASSIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import *


def validate_source_pair(
    classification: Mapping[str, Any], receipt: Mapping[str, Any]
) -> list[str]:
    issues: list[str] = []
    if not digest_ok(classification, SOURCE_CLASSIFICATION_DIGEST_FIELD):
        issues.append("source_classification_digest_mismatch")
    if not digest_ok(receipt, SOURCE_CLASSIFICATION_RECEIPT_DIGEST_FIELD):
        issues.append("source_classification_receipt_digest_mismatch")
    if issues:
        return issues
    if classification.get("codeai_disposition") != SOURCE_DISPOSITION_COMPLETED:
        issues.append("source_classification_disposition_invalid")
    if classification.get("operating_mode") != MODE_CLASSIFICATION_ONLY:
        issues.append("source_classification_mode_invalid")
    pairs = (
        (
            receipt.get("typed_error_classification_digest"),
            classification.get(SOURCE_CLASSIFICATION_DIGEST_FIELD),
            "source_classification_receipt_correspondence_mismatch",
        ),
        (
            receipt.get("repository_full_name"),
            classification.get("repository_full_name"),
            "source_classification_receipt_repository_mismatch",
        ),
        (
            receipt.get("source_commit_sha"),
            classification.get("source_commit_sha"),
            "source_classification_receipt_commit_mismatch",
        ),
        (
            receipt.get("candidate_count"),
            classification.get("candidate_count"),
            "source_classification_receipt_candidate_count_mismatch",
        ),
        (
            receipt.get("typed_error_count"),
            classification.get("typed_error_count"),
            "source_classification_receipt_error_count_mismatch",
        ),
    )
    issues.extend(code for left, right, code in pairs if left != right)
    for field in (
        "exact_lineage_verified",
        "source_finding_evidence_preserved",
        "taxonomy_complete_for_observed_findings",
        "historical_baseline_used_as_reference_only",
    ):
        if classification.get(field) is not True or receipt.get(field) is not True:
            issues.append("source_classification_required_true:" + field)
    for field in (
        "provider_invoked",
        "ranking_performed",
        "candidate_selected",
        "verification_runner_invoked",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "typed_error_treated_as_cause_proof",
        "historical_frequency_treated_as_probability",
        "zero_static_error_treated_as_correctness_proof",
    ):
        if classification.get(field) is not False or receipt.get(field) is not False:
            issues.append("source_classification_forbidden_true:" + field)

    candidates = classification.get("typed_candidates")
    if not isinstance(candidates, list) or not candidates:
        issues.append("source_classification_candidates_invalid")
        return sorted(set(issues))
    ids = [candidate.get("candidate_id") for candidate in candidates if isinstance(candidate, Mapping)]
    if ids != classification.get("candidate_ids") or len(ids) != len(set(ids)):
        issues.append("source_classification_candidate_ids_invalid")
    error_count = 0
    for candidate_index, candidate in enumerate(candidates):
        if not isinstance(candidate, Mapping):
            issues.append(f"source_classification_candidate_not_mapping:{candidate_index}")
            continue
        errors = candidate.get("typed_errors")
        if not isinstance(errors, list):
            issues.append(f"source_classification_errors_invalid:{candidate_index}")
            continue
        if candidate.get("typed_error_count") != len(errors):
            issues.append(f"source_classification_error_count_invalid:{candidate_index}")
        error_count += len(errors)
        for error_index, error in enumerate(errors):
            if not isinstance(error, Mapping):
                issues.append(
                    f"source_classification_error_not_mapping:{candidate_index}:{error_index}"
                )
                continue
            if not digest_ok(error, "typed_error_digest"):
                issues.append(
                    f"source_classification_error_digest_mismatch:{candidate_index}:{error_index}"
                )
            if error.get("candidate_id") != candidate.get("candidate_id"):
                issues.append(
                    f"source_classification_error_candidate_mismatch:{candidate_index}:{error_index}"
                )
            for field in (
                "cause_proven",
                "correctness_implication_claimed",
                "repair_authority_granted",
                "selection_authority_granted",
            ):
                if error.get(field) is not False:
                    issues.append(
                        f"source_classification_error_forbidden_true:{candidate_index}:{error_index}:{field}"
                    )
    if classification.get("typed_error_count") != error_count:
        issues.append("source_classification_error_accounting_invalid")
    return sorted(set(issues))


def typed_error_index(classification: Mapping[str, Any]) -> dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]]:
    index: dict[str, tuple[Mapping[str, Any], Mapping[str, Any]]] = {}
    for candidate in classification["typed_candidates"]:
        for error in candidate["typed_errors"]:
            index[str(error["typed_error_digest"])] = (candidate, error)
    return index


def validate_repair_packet(packet: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "evidence_packet_id",
        "evidence_packet_revision",
        "repository_full_name",
        "source_classification_digest",
        "source_classification_receipt_digest",
        "evidence_created_epoch",
        "repair_producer_id",
        "independent_verifier_id",
        "memory_curator_id",
        "records",
        "record_count",
        "external_repair_execution_reported",
        "independent_verification_verified",
        "isolated_candidate_repair_verified",
        "live_repository_unchanged",
        "git_effect_performed",
        REPAIR_PACKET_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(packet)
    extra = set(packet).difference(required)
    if missing:
        issues.append("repair_packet_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("repair_packet_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if packet["schema_version"] != SCHEMA_VERSION or packet["profile_version"] != PROFILE_VERSION:
        issues.append("repair_packet_profile_invalid")
    for field in (
        "evidence_packet_id",
        "evidence_packet_revision",
        "repository_full_name",
        "repair_producer_id",
        "independent_verifier_id",
        "memory_curator_id",
    ):
        if not isinstance(packet[field], str) or not packet[field]:
            issues.append("repair_packet_string_invalid:" + field)
    for field in ("source_classification_digest", "source_classification_receipt_digest"):
        if not isinstance(packet[field], str) or SHA256.fullmatch(packet[field]) is None:
            issues.append("repair_packet_digest_invalid:" + field)
    for field in ("evidence_created_epoch", "record_count"):
        if not nonnegative_int(packet[field]):
            issues.append("repair_packet_integer_invalid:" + field)
    for field in (
        "external_repair_execution_reported",
        "independent_verification_verified",
        "isolated_candidate_repair_verified",
        "live_repository_unchanged",
        "git_effect_performed",
    ):
        if not isinstance(packet[field], bool):
            issues.append("repair_packet_boolean_invalid:" + field)
    if not digest_ok(packet, REPAIR_PACKET_DIGEST_FIELD):
        issues.append("repair_packet_digest_mismatch")

    records = packet["records"]
    if not isinstance(records, list) or not records:
        issues.append("repair_packet_records_invalid")
        return sorted(set(issues))
    if packet["record_count"] != len(records):
        issues.append("repair_packet_record_count_mismatch")
    record_ids: list[str] = []
    required_record = {
        "repair_record_id",
        "candidate_id",
        "candidate_sequence",
        "source_candidate_digest",
        "typed_error_digest",
        "error_fingerprint",
        "error_family",
        "error_stage",
        "repair_route",
        "repair_action_digest",
        "repair_outcome",
        "verification_evidence_digest",
        "toolchain_digest",
        "dependency_manifest_digest",
        "repair_policy_digest",
        "repair_producer_id",
        "verifier_id",
        "completed",
        "external_repair_execution",
        "independent_verification",
        "isolated_candidate_repair",
        "live_repository_mutation",
        "git_effect",
        REPAIR_RECORD_DIGEST_FIELD,
    }
    for record_index, record in enumerate(records):
        if not isinstance(record, Mapping):
            issues.append(f"repair_record_not_mapping:{record_index}")
            continue
        if set(record) != required_record:
            issues.append(f"repair_record_fields_invalid:{record_index}")
            continue
        record_ids.append(str(record["repair_record_id"]))
        for field in (
            "repair_record_id",
            "candidate_id",
            "error_fingerprint",
            "error_family",
            "error_stage",
            "repair_route",
            "repair_producer_id",
            "verifier_id",
        ):
            if not isinstance(record[field], str) or not record[field]:
                issues.append(f"repair_record_string_invalid:{record_index}:{field}")
        if not positive_int(record["candidate_sequence"]):
            issues.append(f"repair_record_candidate_sequence_invalid:{record_index}")
        for field in (
            "source_candidate_digest",
            "typed_error_digest",
            "repair_action_digest",
            "verification_evidence_digest",
            "toolchain_digest",
            "dependency_manifest_digest",
            "repair_policy_digest",
        ):
            if not isinstance(record[field], str) or SHA256.fullmatch(record[field]) is None:
                issues.append(f"repair_record_digest_invalid:{record_index}:{field}")
        if record["repair_outcome"] not in REPAIR_OUTCOMES:
            issues.append(f"repair_record_outcome_invalid:{record_index}")
        for field in (
            "completed",
            "external_repair_execution",
            "independent_verification",
            "isolated_candidate_repair",
            "live_repository_mutation",
            "git_effect",
        ):
            if not isinstance(record[field], bool):
                issues.append(f"repair_record_boolean_invalid:{record_index}:{field}")
        if not digest_ok(record, REPAIR_RECORD_DIGEST_FIELD):
            issues.append(f"repair_record_digest_mismatch:{record_index}")
    if len(record_ids) != len(set(record_ids)):
        issues.append("repair_packet_record_ids_duplicate")
    return sorted(set(issues))


def binding_matches(entry: Mapping[str, Any], request: Mapping[str, Any]) -> bool:
    return all(entry[field] == request[field] for field in VERSION_BINDING_FIELDS)


def binding_mismatches(entry: Mapping[str, Any], request: Mapping[str, Any]) -> list[str]:
    return [field for field in VERSION_BINDING_FIELDS if entry[field] != request[field]]


__all__ = [
    "binding_matches",
    "binding_mismatches",
    "typed_error_index",
    "validate_repair_packet",
    "validate_source_pair",
]
