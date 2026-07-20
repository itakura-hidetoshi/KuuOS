from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    DECISION_ABSTAINED,
    DECISION_SELECTED,
    DECISION_DIGEST_FIELD as SOURCE_SELECTION_DECISION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_SELECTION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    DISPOSITION_COMPLETED as MEMORY_DISPOSITION_COMPLETED,
    MEMORY_SNAPSHOT_DIGEST_FIELD as SOURCE_MEMORY_SNAPSHOT_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_MEMORY_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_maintainability_trajectory_gate_schema_v0_1 import (
    EVIDENCE_PACKET_DIGEST_FIELD,
    EVIDENCE_RECORD_DIGEST_FIELD,
    MAINTAINABILITY_AXES,
    PROFILE_VERSION,
    SCHEMA_VERSION,
    SHA256,
    digest_ok,
    mapping,
    nonnegative_int,
    positive_int,
    unique_strings,
)


def _digest_string(value: Any) -> bool:
    return isinstance(value, str) and SHA256.fullmatch(value) is not None


def validate_selection_pair(
    decision: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    if not digest_ok(decision, SOURCE_SELECTION_DECISION_DIGEST_FIELD):
        issues.append("source_selection_decision_digest_mismatch")
    if not digest_ok(receipt, SOURCE_SELECTION_RECEIPT_DIGEST_FIELD):
        issues.append("source_selection_receipt_digest_mismatch")
    if issues:
        return sorted(set(issues))

    decision_digest = decision[SOURCE_SELECTION_DECISION_DIGEST_FIELD]
    if receipt.get("decision_digest") != decision_digest:
        issues.append("source_selection_receipt_decision_digest_mismatch")
    for field in (
        "repository_full_name",
        "source_commit_sha",
        "decision",
        "decision_reason",
        "selected_candidate_id",
        "candidate_count",
        "eligible_candidate_count",
        "evidence_record_count",
    ):
        if receipt.get(field) != decision.get(field):
            issues.append("source_selection_receipt_field_mismatch:" + field)
    if decision.get("decision") not in (DECISION_SELECTED, DECISION_ABSTAINED):
        issues.append("source_selection_decision_value_invalid")
    if not _digest_string(decision.get("source_repository_snapshot_digest")):
        issues.append("source_selection_snapshot_digest_invalid")
    if decision.get("decision") == DECISION_SELECTED:
        if not isinstance(decision.get("selected_candidate_id"), str) or not decision["selected_candidate_id"]:
            issues.append("source_selection_selected_candidate_id_invalid")
        if not _digest_string(decision.get("selected_candidate_digest")):
            issues.append("source_selection_selected_candidate_digest_invalid")
        if decision.get("candidate_selected") is not True:
            issues.append("source_selection_candidate_selected_false")
        if receipt.get("candidate_selected") is not True:
            issues.append("source_selection_receipt_candidate_selected_false")
    if decision.get("selection_authority_bounded_to_decision") is not True:
        issues.append("source_selection_authority_not_bounded")
    for field in (
        "test_execution_performed_by_kernel",
        "repair_executed",
        "repository_mutation_performed",
        "git_effect_performed",
        "verification_authority_granted",
        "repair_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "score_treated_as_probability",
        "score_treated_as_correctness_proof",
        "selection_treated_as_correctness_proof",
    ):
        if decision.get(field) is not False:
            issues.append("source_selection_boundary_invalid:" + field)
    return sorted(set(issues))


def validate_memory_pair(
    snapshot: Mapping[str, Any],
    receipt: Mapping[str, Any],
) -> list[str]:
    issues: list[str] = []
    if not digest_ok(snapshot, SOURCE_MEMORY_SNAPSHOT_DIGEST_FIELD):
        issues.append("source_memory_snapshot_digest_mismatch")
    if not digest_ok(receipt, SOURCE_MEMORY_RECEIPT_DIGEST_FIELD):
        issues.append("source_memory_receipt_digest_mismatch")
    if issues:
        return sorted(set(issues))

    snapshot_digest = snapshot[SOURCE_MEMORY_SNAPSHOT_DIGEST_FIELD]
    if receipt.get("version_bound_repair_memory_snapshot_digest") != snapshot_digest:
        issues.append("source_memory_receipt_snapshot_digest_mismatch")
    for field in (
        "repository_full_name",
        "source_commit_sha",
        "memory_entry_count",
        "matched_entry_count",
        "excluded_entry_count",
        "recommendation",
    ):
        if receipt.get(field) != snapshot.get(field):
            issues.append("source_memory_receipt_field_mismatch:" + field)
    if snapshot.get("codeai_disposition") != MEMORY_DISPOSITION_COMPLETED:
        issues.append("source_memory_disposition_invalid")
    if snapshot.get("exact_version_binding_verified") is not True:
        issues.append("source_memory_exact_binding_not_verified")
    if snapshot.get("history_read_only") is not True:
        issues.append("source_memory_not_read_only")
    query = mapping(snapshot.get("query_version_binding"))
    if query is None:
        issues.append("source_memory_query_binding_invalid")
    for field in (
        "repair_executed_by_memory",
        "repository_mutation_performed_by_memory",
        "git_effect_performed_by_memory",
        "repair_authority_granted",
        "verification_authority_granted",
        "execution_authority_granted",
        "git_authority_granted",
        "historical_outcome_treated_as_probability",
        "historical_success_treated_as_future_success_proof",
        "memory_hint_treated_as_correctness_proof",
        "version_mismatch_treated_as_transferable",
    ):
        if snapshot.get(field) is not False:
            issues.append("source_memory_boundary_invalid:" + field)
    return sorted(set(issues))


def validate_trajectory_evidence_packet(packet: Mapping[str, Any]) -> list[str]:
    required = {
        "schema_version",
        "profile_version",
        "evidence_packet_id",
        "evidence_packet_revision",
        "selection_decision_digest",
        "selection_receipt_digest",
        "memory_snapshot_digest",
        "memory_receipt_digest",
        "repository_full_name",
        "source_commit_sha",
        "source_repository_snapshot_digest",
        "selected_candidate_id",
        "selected_candidate_digest",
        "evidence_created_epoch",
        "candidate_producer_id",
        "independent_assessor_id",
        "independent_reviewer_id",
        "records",
        "record_count",
        "external_measurement_reported",
        "independent_assessor_verified",
        "independent_reviewer_verified",
        "isolated_candidate_evaluation_verified",
        "source_correspondence_verified",
        "live_repository_unchanged",
        "candidate_producer_involved_in_measurement",
        "repository_mutation_performed",
        "git_effect_performed",
        EVIDENCE_PACKET_DIGEST_FIELD,
    }
    issues: list[str] = []
    missing = required.difference(packet)
    extra = set(packet).difference(required)
    if missing:
        issues.append("trajectory_packet_missing_fields:" + ",".join(sorted(missing)))
    if extra:
        issues.append("trajectory_packet_extra_fields:" + ",".join(sorted(extra)))
    if issues:
        return issues
    if packet["schema_version"] != SCHEMA_VERSION or packet["profile_version"] != PROFILE_VERSION:
        issues.append("trajectory_packet_profile_invalid")
    for field in (
        "evidence_packet_id",
        "evidence_packet_revision",
        "repository_full_name",
        "selected_candidate_id",
        "candidate_producer_id",
        "independent_assessor_id",
        "independent_reviewer_id",
    ):
        if not isinstance(packet[field], str) or not packet[field]:
            issues.append("trajectory_packet_string_invalid:" + field)
    for field in (
        "selection_decision_digest",
        "selection_receipt_digest",
        "memory_snapshot_digest",
        "memory_receipt_digest",
        "source_repository_snapshot_digest",
        "selected_candidate_digest",
    ):
        if not _digest_string(packet[field]):
            issues.append("trajectory_packet_digest_invalid:" + field)
    if not isinstance(packet["source_commit_sha"], str) or len(packet["source_commit_sha"]) != 40:
        issues.append("trajectory_packet_source_commit_invalid")
    if not nonnegative_int(packet["evidence_created_epoch"]):
        issues.append("trajectory_packet_epoch_invalid")
    records = packet["records"]
    if not isinstance(records, list):
        issues.append("trajectory_packet_records_invalid")
        records = []
    if not nonnegative_int(packet["record_count"]) or packet["record_count"] != len(records):
        issues.append("trajectory_packet_record_count_mismatch")
    for field in (
        "external_measurement_reported",
        "independent_assessor_verified",
        "independent_reviewer_verified",
        "isolated_candidate_evaluation_verified",
        "source_correspondence_verified",
        "live_repository_unchanged",
        "candidate_producer_involved_in_measurement",
        "repository_mutation_performed",
        "git_effect_performed",
    ):
        if not isinstance(packet[field], bool):
            issues.append("trajectory_packet_boolean_invalid:" + field)
    record_ids: list[str] = []
    axes: list[str] = []
    for index, raw_record in enumerate(records):
        record = mapping(raw_record)
        if record is None:
            issues.append(f"trajectory_record_not_mapping:{index}")
            continue
        required_record = {
            "measurement_record_id",
            "axis",
            "baseline_value",
            "candidate_value",
            "observed_delta",
            "measurement_artifact_digest",
            "assessor_id",
            "reviewer_id",
            "completed",
            "external_measurement",
            "independent_assessor",
            "independent_reviewer",
            "isolated_candidate_evaluation",
            "source_correspondence",
            "candidate_producer_involved",
            "repository_mutation_performed",
            "git_effect_performed",
            EVIDENCE_RECORD_DIGEST_FIELD,
        }
        missing_record = required_record.difference(record)
        extra_record = set(record).difference(required_record)
        if missing_record:
            issues.append(
                f"trajectory_record_missing_fields:{index}:"
                + ",".join(sorted(missing_record))
            )
        if extra_record:
            issues.append(
                f"trajectory_record_extra_fields:{index}:"
                + ",".join(sorted(extra_record))
            )
        if missing_record or extra_record:
            continue
        if not isinstance(record["measurement_record_id"], str) or not record["measurement_record_id"]:
            issues.append(f"trajectory_record_id_invalid:{index}")
        else:
            record_ids.append(record["measurement_record_id"])
        if record["axis"] not in MAINTAINABILITY_AXES:
            issues.append(f"trajectory_record_axis_invalid:{index}")
        else:
            axes.append(record["axis"])
        for field in ("baseline_value", "candidate_value"):
            if not nonnegative_int(record[field]):
                issues.append(f"trajectory_record_value_invalid:{index}:{field}")
        if not isinstance(record["observed_delta"], int) or isinstance(record["observed_delta"], bool):
            issues.append(f"trajectory_record_delta_invalid:{index}")
        if not _digest_string(record["measurement_artifact_digest"]):
            issues.append(f"trajectory_record_artifact_digest_invalid:{index}")
        for field in ("assessor_id", "reviewer_id"):
            if not isinstance(record[field], str) or not record[field]:
                issues.append(f"trajectory_record_identity_invalid:{index}:{field}")
        for field in (
            "completed",
            "external_measurement",
            "independent_assessor",
            "independent_reviewer",
            "isolated_candidate_evaluation",
            "source_correspondence",
            "candidate_producer_involved",
            "repository_mutation_performed",
            "git_effect_performed",
        ):
            if not isinstance(record[field], bool):
                issues.append(f"trajectory_record_boolean_invalid:{index}:{field}")
        if not digest_ok(record, EVIDENCE_RECORD_DIGEST_FIELD):
            issues.append(f"trajectory_record_digest_mismatch:{index}")
    if len(record_ids) != len(set(record_ids)):
        issues.append("trajectory_record_ids_not_unique")
    if len(axes) != len(set(axes)):
        issues.append("trajectory_record_axes_not_unique")
    if not digest_ok(packet, EVIDENCE_PACKET_DIGEST_FIELD):
        issues.append("trajectory_packet_digest_mismatch")
    return sorted(set(issues))


def regression_amount(record: Mapping[str, Any]) -> int:
    return max(int(record["candidate_value"]) - int(record["baseline_value"]), 0)


def is_improved(record: Mapping[str, Any]) -> bool:
    return int(record["candidate_value"]) < int(record["baseline_value"])


def build_axis_assessment(
    record: Mapping[str, Any],
    maximum_allowed_increase: int,
) -> dict[str, Any]:
    regression = regression_amount(record)
    return {
        "axis": record["axis"],
        "baseline_value": record["baseline_value"],
        "candidate_value": record["candidate_value"],
        "observed_delta": record["observed_delta"],
        "regression_amount": regression,
        "maximum_allowed_increase": maximum_allowed_increase,
        "within_axis_limit": regression <= maximum_allowed_increase,
        "improved": is_improved(record),
        "measurement_artifact_digest": record["measurement_artifact_digest"],
        "measurement_record_digest": record[EVIDENCE_RECORD_DIGEST_FIELD],
    }


__all__ = [
    "build_axis_assessment",
    "is_improved",
    "regression_amount",
    "validate_memory_pair",
    "validate_selection_pair",
    "validate_trajectory_evidence_packet",
]
