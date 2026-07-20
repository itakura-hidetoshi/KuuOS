#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_independent_test_strengthening_v0_1 import (
    build_codeai_independent_test_strengthening,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    OBLIGATION_DIGEST_FIELD,
    PLAN_DIGEST_FIELD as STRENGTHENING_PLAN_DIGEST_FIELD,
    RECEIPT_DIGEST_FIELD as STRENGTHENING_RECEIPT_DIGEST_FIELD,
)
from runtime.kuuos_codeai_evidence_weighted_selection_abstention_schema_v0_1 import (
    EVIDENCE_PACKET_DIGEST_FIELD,
    EVIDENCE_RECORD_DIGEST_FIELD,
    OUTCOME_PASSED,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    canonical_digest,
    seal,
)
from scripts.build_codeai_independent_test_strengthening_fixture_v0_1 import (
    build_fixture as build_strengthening_fixture,
)


def build_fixture(
    selection_spec: dict[str, Any],
    strengthening_spec: dict[str, Any],
    classification_spec: dict[str, Any],
    portfolio_spec: dict[str, Any],
    baseline_spec: dict[str, Any],
) -> dict[str, Any]:
    strengthening_inputs = build_strengthening_fixture(
        strengthening_spec,
        classification_spec,
        portfolio_spec,
        baseline_spec,
    )
    strengthening_result = build_codeai_independent_test_strengthening(
        source_classification=strengthening_inputs["source_classification"],
        source_classification_receipt=strengthening_inputs[
            "source_classification_receipt"
        ],
        capability_catalog=strengthening_inputs["capability_catalog"],
        strengthening_request=strengthening_inputs["strengthening_request"],
        strengthening_policy=strengthening_inputs["strengthening_policy"],
    )
    if strengthening_result.plan is None or strengthening_result.receipt is None:
        raise ValueError("strengthening fixture blocked: " + ",".join(strengthening_result.issues))

    plan = strengthening_result.plan
    receipt = strengthening_result.receipt
    producer_id = selection_spec["candidate_producer_id"]
    runner_id = selection_spec["independent_runner_id"]
    reviewer_id = selection_spec["independent_reviewer_id"]

    candidate_results: list[dict[str, Any]] = []
    evidence_record_count = 0
    for candidate in plan["candidate_plans"]:
        records: list[dict[str, Any]] = []
        for obligation in candidate["obligations"]:
            artifact_digest = canonical_digest(
                {
                    "candidate_id": candidate["candidate_id"],
                    "obligation_digest": obligation[OBLIGATION_DIGEST_FIELD],
                    "outcome": OUTCOME_PASSED,
                    "runner_id": runner_id,
                    "reviewer_id": reviewer_id,
                }
            )
            record = seal(
                {
                    "candidate_id": candidate["candidate_id"],
                    "candidate_sequence": candidate["candidate_sequence"],
                    "obligation_id": obligation["obligation_id"],
                    "obligation_digest": obligation[OBLIGATION_DIGEST_FIELD],
                    "category": obligation["category"],
                    "check_kind": obligation["check_kind"],
                    "outcome": OUTCOME_PASSED,
                    "evidence_artifact_digest": artifact_digest,
                    "runner_id": runner_id,
                    "reviewer_id": reviewer_id,
                    "completed": True,
                    "external_execution": True,
                    "independent_runner": True,
                    "independent_reviewer": True,
                    "isolated_execution": True,
                    "source_correspondence": True,
                    "candidate_producer_involved": False,
                    "repository_mutation_performed": False,
                    "git_effect_performed": False,
                },
                EVIDENCE_RECORD_DIGEST_FIELD,
            )
            records.append(record)
        evidence_record_count += len(records)
        candidate_results.append(
            {
                "candidate_id": candidate["candidate_id"],
                "candidate_sequence": candidate["candidate_sequence"],
                "obligation_results": records,
                "obligation_result_count": len(records),
            }
        )

    packet = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Evidence-Weighted Selection and Abstention v0.1",
            "evidence_packet_id": selection_spec["evidence_packet_id"],
            "evidence_packet_revision": selection_spec["evidence_packet_revision"],
            "repository_full_name": plan["repository_full_name"],
            "source_commit_sha": plan["source_commit_sha"],
            "strengthening_plan_digest": plan[STRENGTHENING_PLAN_DIGEST_FIELD],
            "strengthening_receipt_digest": receipt[
                STRENGTHENING_RECEIPT_DIGEST_FIELD
            ],
            "evidence_created_epoch": selection_spec["evidence_created_epoch"],
            "candidate_producer_id": producer_id,
            "independent_runner_id": runner_id,
            "independent_reviewer_id": reviewer_id,
            "candidate_results": candidate_results,
            "candidate_count": len(candidate_results),
            "evidence_record_count": evidence_record_count,
            "external_test_execution_reported": True,
            "independent_runner_verified": True,
            "independent_reviewer_verified": True,
            "isolated_execution_verified": True,
            "source_correspondence_verified": True,
            "candidate_producer_involved_in_evidence": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
        },
        EVIDENCE_PACKET_DIGEST_FIELD,
    )
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Evidence-Weighted Selection and Abstention v0.1",
            "selection_id": selection_spec["selection_id"],
            "selection_revision": selection_spec["selection_revision"],
            "repository_full_name": plan["repository_full_name"],
            "source_commit_sha": plan["source_commit_sha"],
            "strengthening_plan_digest": plan[STRENGTHENING_PLAN_DIGEST_FIELD],
            "strengthening_receipt_digest": receipt[
                STRENGTHENING_RECEIPT_DIGEST_FIELD
            ],
            "evidence_packet_digest": packet[EVIDENCE_PACKET_DIGEST_FIELD],
            "request_created_epoch": selection_spec["request_created_epoch"],
            "unresolved_selection_questions": [],
            "claims_execution_authority": False,
            "claims_git_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Evidence-Weighted Selection and Abstention v0.1",
            "expected_repository_full_name": plan["repository_full_name"],
            "expected_source_commit_sha": plan["source_commit_sha"],
            "expected_strengthening_plan_digest": plan[
                STRENGTHENING_PLAN_DIGEST_FIELD
            ],
            "expected_strengthening_receipt_digest": receipt[
                STRENGTHENING_RECEIPT_DIGEST_FIELD
            ],
            "expected_evidence_packet_digest": packet[
                EVIDENCE_PACKET_DIGEST_FIELD
            ],
            "evaluation_epoch": selection_spec["evaluation_epoch"],
            "maximum_request_age": selection_spec["maximum_request_age"],
            "maximum_evidence_age": selection_spec["maximum_evidence_age"],
            "maximum_candidates": selection_spec["maximum_candidates"],
            "maximum_evidence_records": selection_spec[
                "maximum_evidence_records"
            ],
            "minimum_evidence_score": selection_spec["minimum_evidence_score"],
            "minimum_score_margin": selection_spec["minimum_score_margin"],
            "category_weights": selection_spec["category_weights"],
            "require_exact_lineage": True,
            "require_complete_obligation_coverage": True,
            "require_independent_runner": True,
            "require_independent_reviewer": True,
            "require_isolated_execution": True,
            "require_source_correspondence": True,
            "require_admissible_source_classification": True,
            "require_all_obligations_passed": True,
            "allow_selection_decision": True,
            "allow_test_execution": False,
            "allow_repair_execution": False,
            "allow_repository_mutation": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )
    return {
        "strengthening_plan": plan,
        "strengthening_receipt": receipt,
        "evidence_packet": packet,
        "selection_request": request,
        "selection_policy": policy,
    }


__all__ = ["build_fixture"]
