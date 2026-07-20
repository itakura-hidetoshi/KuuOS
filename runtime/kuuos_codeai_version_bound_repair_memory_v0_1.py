from __future__ import annotations

from collections import Counter
from typing import Any

from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD as SOURCE_CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as SOURCE_CLASSIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_checks_v0_1 import (
    binding_matches,
    binding_mismatches,
    typed_error_index,
    validate_repair_packet,
    validate_source_pair,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import *


def _blocked(*issues: str) -> CodeAIVersionBoundRepairMemoryResult:
    return CodeAIVersionBoundRepairMemoryResult(
        STATUS_BLOCKED,
        tuple(sorted(set(issues))),
        None,
        None,
    )


def _receipt(snapshot: dict[str, Any]) -> dict[str, Any]:
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "version_bound_repair_memory_snapshot_digest": snapshot[
            MEMORY_SNAPSHOT_DIGEST_FIELD
        ],
        "memory_request_digest": snapshot["memory_request_digest"],
        "memory_policy_digest": snapshot["memory_policy_digest"],
        "source_classification_digest": snapshot["source_classification_digest"],
        "source_classification_receipt_digest": snapshot[
            "source_classification_receipt_digest"
        ],
        "repair_evidence_packet_digest": snapshot["repair_evidence_packet_digest"],
        "repository_full_name": snapshot["repository_full_name"],
        "source_commit_sha": snapshot["source_commit_sha"],
        "memory_entry_count": snapshot["memory_entry_count"],
        "matched_entry_count": snapshot["matched_entry_count"],
        "excluded_entry_count": snapshot["excluded_entry_count"],
        "recommendation": snapshot["recommendation"],
        "exact_version_binding_verified": True,
        "typed_error_correspondence_verified": True,
        "independent_verification_verified": True,
        "isolated_candidate_repair_verified": True,
        "live_repository_unchanged": True,
        "history_read_only": True,
        "memory_hint_emitted": snapshot["matched_entry_count"] > 0,
        "repair_executed_by_memory": False,
        "repository_mutation_performed_by_memory": False,
        "git_effect_performed_by_memory": False,
        "repair_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "historical_outcome_treated_as_probability": False,
        "historical_success_treated_as_future_success_proof": False,
        "memory_hint_treated_as_correctness_proof": False,
        "version_mismatch_treated_as_transferable": False,
        "future_only": True,
        "active_now": False,
    }
    return seal(receipt, RECEIPT_DIGEST_FIELD)


def build_codeai_version_bound_repair_memory(
    *,
    source_classification: Any,
    source_classification_receipt: Any,
    repair_evidence_packet: Any,
    memory_request: Any,
    memory_policy: Any,
) -> CodeAIVersionBoundRepairMemoryResult:
    classification = mapping(source_classification)
    classification_receipt = mapping(source_classification_receipt)
    packet = mapping(repair_evidence_packet)
    request = mapping(memory_request)
    policy = mapping(memory_policy)
    if any(value is None for value in (classification, classification_receipt, packet, request, policy)):
        return _blocked("memory_input_not_mapping")

    assert classification is not None
    assert classification_receipt is not None
    assert packet is not None
    assert request is not None
    assert policy is not None

    issues = (
        validate_request(request)
        + validate_policy(policy)
        + validate_source_pair(classification, classification_receipt)
        + validate_repair_packet(packet)
    )
    if issues:
        return _blocked(*issues)

    required_policy = (
        "require_exact_version_binding",
        "require_complete_typed_error_correspondence",
        "require_independent_verification",
        "require_isolated_candidate_repair",
        "require_live_repository_unchanged",
        "allow_memory_hint",
    )
    disabled = [field for field in required_policy if policy[field] is not True]
    if disabled:
        return _blocked("memory_policy_required_guarantee_disabled:" + ",".join(disabled))
    forbidden_policy = (
        "allow_repair_execution",
        "allow_repository_mutation",
        "allow_execution_authority",
        "allow_git_authority",
    )
    if any(policy[field] for field in forbidden_policy):
        return _blocked("memory_policy_effect_or_authority_enabled")
    if any(
        request[field]
        for field in (
            "claims_repair_authority",
            "claims_execution_authority",
            "claims_git_authority",
        )
    ):
        return _blocked("memory_request_claims_authority")
    if request["unresolved_memory_questions"]:
        return _blocked("memory_unresolved_questions_present")

    classification_digest = str(classification[SOURCE_CLASSIFICATION_DIGEST_FIELD])
    classification_receipt_digest = str(
        classification_receipt[SOURCE_CLASSIFICATION_RECEIPT_DIGEST_FIELD]
    )
    packet_digest = str(packet[REPAIR_PACKET_DIGEST_FIELD])
    exact_pairs = (
        (
            request["source_classification_digest"],
            classification_digest,
            "request_classification_digest_mismatch",
        ),
        (
            request["source_classification_receipt_digest"],
            classification_receipt_digest,
            "request_classification_receipt_digest_mismatch",
        ),
        (
            request["repair_evidence_packet_digest"],
            packet_digest,
            "request_repair_packet_digest_mismatch",
        ),
        (
            policy["expected_source_classification_digest"],
            classification_digest,
            "policy_classification_digest_mismatch",
        ),
        (
            policy["expected_source_classification_receipt_digest"],
            classification_receipt_digest,
            "policy_classification_receipt_digest_mismatch",
        ),
        (
            policy["expected_repair_evidence_packet_digest"],
            packet_digest,
            "policy_repair_packet_digest_mismatch",
        ),
        (
            packet["repository_full_name"],
            classification["repository_full_name"],
            "repair_packet_repository_mismatch",
        ),
        (
            packet["source_classification_digest"],
            classification_digest,
            "repair_packet_classification_digest_mismatch",
        ),
        (
            packet["source_classification_receipt_digest"],
            classification_receipt_digest,
            "repair_packet_classification_receipt_digest_mismatch",
        ),
    )
    correspondence_issues = [code for left, right, code in exact_pairs if left != right]
    for field in VERSION_BINDING_FIELDS:
        if request[field] != policy["expected_" + field]:
            correspondence_issues.append("request_policy_binding_mismatch:" + field)
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    evaluation_epoch = int(policy["evaluation_epoch"])
    request_epoch = int(request["request_created_epoch"])
    evidence_epoch = int(packet["evidence_created_epoch"])
    if not evaluation_epoch - int(policy["maximum_request_age"]) <= request_epoch <= evaluation_epoch:
        return _blocked("memory_request_window_invalid")
    if not evaluation_epoch - int(policy["maximum_evidence_age"]) <= evidence_epoch <= evaluation_epoch:
        return _blocked("memory_evidence_window_invalid")

    role_ids = {
        str(packet["repair_producer_id"]),
        str(packet["independent_verifier_id"]),
        str(packet["memory_curator_id"]),
    }
    if len(role_ids) != 3:
        return _blocked("memory_roles_not_separated")
    for field in (
        "external_repair_execution_reported",
        "independent_verification_verified",
        "isolated_candidate_repair_verified",
        "live_repository_unchanged",
    ):
        if packet[field] is not True:
            return _blocked("repair_packet_required_true:" + field)
    if packet["git_effect_performed"] is not False:
        return _blocked("repair_packet_git_effect_present")

    records = packet["records"]
    if len(records) > int(policy["maximum_memory_entries"]):
        return _blocked("memory_entry_budget_exceeded")
    errors = typed_error_index(classification)
    correspondence_issues = []
    entries: list[dict[str, Any]] = []
    for record_index, record in enumerate(records):
        digest = str(record["typed_error_digest"])
        source = errors.get(digest)
        if source is None:
            correspondence_issues.append(
                f"repair_record_typed_error_unknown:{record_index}"
            )
            continue
        candidate, error = source
        pairs = (
            (record["candidate_id"], candidate["candidate_id"]),
            (record["candidate_sequence"], candidate["candidate_sequence"]),
            (record["source_candidate_digest"], candidate["source_candidate_digest"]),
            (record["error_fingerprint"], error["error_fingerprint"]),
            (record["error_family"], error["error_family"]),
            (record["error_stage"], error["error_stage"]),
            (record["repair_route"], error["repair_route"]),
            (record["repair_producer_id"], packet["repair_producer_id"]),
            (record["verifier_id"], packet["independent_verifier_id"]),
        )
        if any(left != right for left, right in pairs):
            correspondence_issues.append(
                f"repair_record_typed_error_correspondence_mismatch:{record_index}"
            )
        for field in (
            "completed",
            "external_repair_execution",
            "independent_verification",
            "isolated_candidate_repair",
        ):
            if record[field] is not True:
                correspondence_issues.append(
                    f"repair_record_required_true:{record_index}:{field}"
                )
        for field in ("live_repository_mutation", "git_effect"):
            if record[field] is not False:
                correspondence_issues.append(
                    f"repair_record_forbidden_true:{record_index}:{field}"
                )
        entry = {
            "schema_version": SCHEMA_VERSION,
            "profile_version": PROFILE_VERSION,
            "memory_entry_id": "memory:" + str(record["repair_record_id"]),
            "repository_full_name": classification["repository_full_name"],
            "source_commit_sha": classification["source_commit_sha"],
            "source_repository_snapshot_digest": classification[
                "source_repository_snapshot_digest"
            ],
            "source_candidate_digest": record["source_candidate_digest"],
            "typed_error_digest": record["typed_error_digest"],
            "error_fingerprint": record["error_fingerprint"],
            "classification_schema_version": classification["profile_version"],
            "toolchain_digest": record["toolchain_digest"],
            "dependency_manifest_digest": record["dependency_manifest_digest"],
            "repair_policy_digest": record["repair_policy_digest"],
            "candidate_id": record["candidate_id"],
            "candidate_sequence": record["candidate_sequence"],
            "error_family": record["error_family"],
            "error_stage": record["error_stage"],
            "repair_route": record["repair_route"],
            "repair_action_digest": record["repair_action_digest"],
            "repair_outcome": record["repair_outcome"],
            "verification_evidence_digest": record["verification_evidence_digest"],
            "repair_record_digest": record[REPAIR_RECORD_DIGEST_FIELD],
            "repair_evidence_created_epoch": evidence_epoch,
            "exact_version_binding": True,
            "historical_repair_hint_only": True,
            "future_success_proven": False,
            "probability_claimed": False,
            "correctness_proven": False,
            "repair_authority_granted": False,
            "execution_authority_granted": False,
            "git_authority_granted": False,
        }
        entries.append(seal(entry, MEMORY_ENTRY_DIGEST_FIELD))
    if correspondence_issues:
        return _blocked(*correspondence_issues)

    allowed_outcomes = set(policy["allowed_repair_outcomes"])
    matched_entries: list[dict[str, Any]] = []
    excluded_entries: list[dict[str, Any]] = []
    exclusion_counts: Counter[str] = Counter()
    for entry in entries:
        reasons: list[str] = []
        mismatches = binding_mismatches(entry, request)
        if mismatches:
            reasons.extend("version_binding_mismatch:" + field for field in mismatches)
        if entry["repair_outcome"] not in allowed_outcomes:
            reasons.append("repair_outcome_not_allowed")
        if reasons:
            exclusion_counts.update(reasons)
            excluded_entries.append(
                {
                    "memory_entry_digest": entry[MEMORY_ENTRY_DIGEST_FIELD],
                    "reasons": reasons,
                }
            )
        else:
            if not binding_matches(entry, request):
                return _blocked("memory_internal_binding_inconsistency")
            matched_entries.append(entry)
    if len(matched_entries) > int(policy["maximum_matched_entries"]):
        return _blocked("memory_match_budget_exceeded")

    recommendation = (
        RECOMMENDATION_HINT_AVAILABLE if matched_entries else RECOMMENDATION_NO_HINT
    )
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "profile_version": PROFILE_VERSION,
        "memory_request_id": request["memory_request_id"],
        "memory_request_revision": request["memory_request_revision"],
        "memory_request_digest": request[REQUEST_DIGEST_FIELD],
        "memory_policy_digest": policy[POLICY_DIGEST_FIELD],
        "source_classification_digest": classification_digest,
        "source_classification_receipt_digest": classification_receipt_digest,
        "repair_evidence_packet_digest": packet_digest,
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_repository_snapshot_digest": classification[
            "source_repository_snapshot_digest"
        ],
        "query_version_binding": {
            field: request[field] for field in VERSION_BINDING_FIELDS
        },
        "memory_entries": entries,
        "memory_entry_count": len(entries),
        "matched_entries": matched_entries,
        "matched_entry_count": len(matched_entries),
        "excluded_entries": excluded_entries,
        "excluded_entry_count": len(excluded_entries),
        "exclusion_counts": dict(sorted(exclusion_counts.items())),
        "allowed_repair_outcomes": list(policy["allowed_repair_outcomes"]),
        "recommendation": recommendation,
        "codeai_disposition": DISPOSITION_COMPLETED,
        "operating_mode": MODE_MEMORY_ONLY,
        "exact_version_binding_verified": True,
        "typed_error_correspondence_verified": True,
        "independent_verification_verified": True,
        "isolated_candidate_repair_verified": True,
        "live_repository_unchanged": True,
        "history_read_only": True,
        "memory_hint_emitted": bool(matched_entries),
        "repair_executed_by_memory": False,
        "repository_mutation_performed_by_memory": False,
        "git_effect_performed_by_memory": False,
        "repair_authority_granted": False,
        "verification_authority_granted": False,
        "execution_authority_granted": False,
        "git_authority_granted": False,
        "historical_outcome_treated_as_probability": False,
        "historical_success_treated_as_future_success_proof": False,
        "memory_hint_treated_as_correctness_proof": False,
        "version_mismatch_treated_as_transferable": False,
        "future_only": True,
        "active_now": False,
    }
    snapshot = seal(snapshot, MEMORY_SNAPSHOT_DIGEST_FIELD)
    return CodeAIVersionBoundRepairMemoryResult(
        STATUS_READY,
        (),
        snapshot,
        _receipt(snapshot),
    )


__all__ = [name for name in globals() if name.isupper()] + [
    "CodeAIVersionBoundRepairMemoryResult",
    "build_codeai_version_bound_repair_memory",
    "canonical_digest",
    "canonical_json",
    "digest_without",
    "seal",
]
