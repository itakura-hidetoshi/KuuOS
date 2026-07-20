#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_typed_error_classification_v0_1 import (
    build_codeai_typed_error_classification,
)
from runtime.kuuos_codeai_typed_error_classification_schema_v0_1 import (
    CLASSIFICATION_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as CLASSIFICATION_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_version_bound_repair_memory_schema_v0_1 import (
    OUTCOME_INCONCLUSIVE,
    OUTCOME_VERIFIED_EFFECTIVE,
    OUTCOME_VERIFIED_INEFFECTIVE,
    POLICY_DIGEST_FIELD,
    REPAIR_PACKET_DIGEST_FIELD,
    REPAIR_RECORD_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from scripts.build_codeai_typed_error_classification_fixture_v0_1 import (
    build_fixture as build_classification_fixture,
)


def build_fixture(
    memory_spec: dict[str, Any],
    classification_spec: dict[str, Any],
    portfolio_spec: dict[str, Any],
    baseline_spec: dict[str, Any],
) -> dict[str, Any]:
    classification_inputs = build_classification_fixture(
        classification_spec,
        portfolio_spec,
        baseline_spec,
    )
    classification_result = build_codeai_typed_error_classification(
        source_portfolio=classification_inputs["source_portfolio"],
        source_portfolio_receipt=classification_inputs["source_portfolio_receipt"],
        baseline_evidence=classification_inputs["baseline_evidence"],
        baseline_receipt=classification_inputs["baseline_receipt"],
        classification_request=classification_inputs["classification_request"],
        classification_policy=classification_inputs["classification_policy"],
    )
    if classification_result.classification is None or classification_result.receipt is None:
        raise ValueError(
            "classification fixture blocked: " + ",".join(classification_result.issues)
        )

    classification = classification_result.classification
    classification_receipt = classification_result.receipt
    typed: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for candidate in classification["typed_candidates"]:
        for error in candidate["typed_errors"]:
            typed.append((candidate, error))
    if len(typed) < 3:
        raise ValueError("version-bound repair memory fixture requires three typed errors")

    current_toolchain = canonical_digest(
        {"toolchain": memory_spec["current_toolchain_label"]}
    )
    legacy_toolchain = canonical_digest(
        {"toolchain": memory_spec["legacy_toolchain_label"]}
    )
    dependency_manifest = canonical_digest(
        {"dependency_manifest": memory_spec["dependency_manifest_label"]}
    )
    repair_policy = canonical_digest(
        {"repair_policy": memory_spec["repair_policy_label"]}
    )

    producer = memory_spec["repair_producer_id"]
    verifier = memory_spec["independent_verifier_id"]
    outcomes = (
        OUTCOME_VERIFIED_EFFECTIVE,
        OUTCOME_VERIFIED_EFFECTIVE,
        OUTCOME_VERIFIED_INEFFECTIVE,
    )
    records: list[dict[str, Any]] = []
    for index, ((candidate, error), outcome) in enumerate(zip(typed[:3], outcomes), start=1):
        record = {
            "repair_record_id": f"repair-record-{index:03d}",
            "candidate_id": candidate["candidate_id"],
            "candidate_sequence": candidate["candidate_sequence"],
            "source_candidate_digest": candidate["source_candidate_digest"],
            "typed_error_digest": error["typed_error_digest"],
            "error_fingerprint": error["error_fingerprint"],
            "error_family": error["error_family"],
            "error_stage": error["error_stage"],
            "repair_route": error["repair_route"],
            "repair_action_digest": canonical_digest(
                {
                    "typed_error_digest": error["typed_error_digest"],
                    "repair_action": f"repair-action-{index:03d}",
                }
            ),
            "repair_outcome": outcome,
            "verification_evidence_digest": canonical_digest(
                {
                    "typed_error_digest": error["typed_error_digest"],
                    "verification": f"verification-{index:03d}",
                    "outcome": outcome,
                }
            ),
            "toolchain_digest": current_toolchain,
            "dependency_manifest_digest": dependency_manifest,
            "repair_policy_digest": repair_policy,
            "repair_producer_id": producer,
            "verifier_id": verifier,
            "completed": True,
            "external_repair_execution": True,
            "independent_verification": True,
            "isolated_candidate_repair": True,
            "live_repository_mutation": False,
            "git_effect": False,
        }
        records.append(seal(record, REPAIR_RECORD_DIGEST_FIELD))

    first_candidate, first_error = typed[0]
    legacy_record = {
        "repair_record_id": "repair-record-legacy-001",
        "candidate_id": first_candidate["candidate_id"],
        "candidate_sequence": first_candidate["candidate_sequence"],
        "source_candidate_digest": first_candidate["source_candidate_digest"],
        "typed_error_digest": first_error["typed_error_digest"],
        "error_fingerprint": first_error["error_fingerprint"],
        "error_family": first_error["error_family"],
        "error_stage": first_error["error_stage"],
        "repair_route": first_error["repair_route"],
        "repair_action_digest": canonical_digest(
            {
                "typed_error_digest": first_error["typed_error_digest"],
                "repair_action": "legacy-repair-action-001",
            }
        ),
        "repair_outcome": OUTCOME_VERIFIED_EFFECTIVE,
        "verification_evidence_digest": canonical_digest(
            {
                "typed_error_digest": first_error["typed_error_digest"],
                "verification": "legacy-verification-001",
                "outcome": OUTCOME_VERIFIED_EFFECTIVE,
            }
        ),
        "toolchain_digest": legacy_toolchain,
        "dependency_manifest_digest": dependency_manifest,
        "repair_policy_digest": repair_policy,
        "repair_producer_id": producer,
        "verifier_id": verifier,
        "completed": True,
        "external_repair_execution": True,
        "independent_verification": True,
        "isolated_candidate_repair": True,
        "live_repository_mutation": False,
        "git_effect": False,
    }
    records.append(seal(legacy_record, REPAIR_RECORD_DIGEST_FIELD))

    packet = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Version-Bound Repair Memory v0.1",
            "evidence_packet_id": memory_spec["evidence_packet_id"],
            "evidence_packet_revision": memory_spec["evidence_packet_revision"],
            "repository_full_name": classification["repository_full_name"],
            "source_classification_digest": classification[
                CLASSIFICATION_DIGEST_FIELD
            ],
            "source_classification_receipt_digest": classification_receipt[
                CLASSIFICATION_RECEIPT_DIGEST_FIELD
            ],
            "evidence_created_epoch": memory_spec["evidence_created_epoch"],
            "repair_producer_id": producer,
            "independent_verifier_id": verifier,
            "memory_curator_id": memory_spec["memory_curator_id"],
            "records": records,
            "record_count": len(records),
            "external_repair_execution_reported": True,
            "independent_verification_verified": True,
            "isolated_candidate_repair_verified": True,
            "live_repository_unchanged": True,
            "git_effect_performed": False,
        },
        REPAIR_PACKET_DIGEST_FIELD,
    )

    binding = {
        "repository_full_name": classification["repository_full_name"],
        "source_commit_sha": classification["source_commit_sha"],
        "source_repository_snapshot_digest": classification[
            "source_repository_snapshot_digest"
        ],
        "source_candidate_digest": first_candidate["source_candidate_digest"],
        "typed_error_digest": first_error["typed_error_digest"],
        "error_fingerprint": first_error["error_fingerprint"],
        "classification_schema_version": classification["profile_version"],
        "toolchain_digest": current_toolchain,
        "dependency_manifest_digest": dependency_manifest,
        "repair_policy_digest": repair_policy,
    }
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Version-Bound Repair Memory v0.1",
            "memory_request_id": memory_spec["memory_request_id"],
            "memory_request_revision": memory_spec["memory_request_revision"],
            "source_classification_digest": classification[
                CLASSIFICATION_DIGEST_FIELD
            ],
            "source_classification_receipt_digest": classification_receipt[
                CLASSIFICATION_RECEIPT_DIGEST_FIELD
            ],
            "repair_evidence_packet_digest": packet[REPAIR_PACKET_DIGEST_FIELD],
            **binding,
            "request_created_epoch": memory_spec["request_created_epoch"],
            "unresolved_memory_questions": [],
            "claims_repair_authority": False,
            "claims_execution_authority": False,
            "claims_git_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Version-Bound Repair Memory v0.1",
            "expected_source_classification_digest": classification[
                CLASSIFICATION_DIGEST_FIELD
            ],
            "expected_source_classification_receipt_digest": classification_receipt[
                CLASSIFICATION_RECEIPT_DIGEST_FIELD
            ],
            "expected_repair_evidence_packet_digest": packet[
                REPAIR_PACKET_DIGEST_FIELD
            ],
            **{"expected_" + key: value for key, value in binding.items()},
            "evaluation_epoch": memory_spec["evaluation_epoch"],
            "maximum_request_age": memory_spec["maximum_request_age"],
            "maximum_evidence_age": memory_spec["maximum_evidence_age"],
            "maximum_memory_entries": memory_spec["maximum_memory_entries"],
            "maximum_matched_entries": memory_spec["maximum_matched_entries"],
            "allowed_repair_outcomes": [OUTCOME_VERIFIED_EFFECTIVE],
            "require_exact_version_binding": True,
            "require_complete_typed_error_correspondence": True,
            "require_independent_verification": True,
            "require_isolated_candidate_repair": True,
            "require_live_repository_unchanged": True,
            "allow_memory_hint": True,
            "allow_repair_execution": False,
            "allow_repository_mutation": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return {
        "source_classification": classification,
        "source_classification_receipt": classification_receipt,
        "repair_evidence_packet": packet,
        "memory_request": request,
        "memory_policy": policy,
    }


__all__ = ["build_fixture"]
