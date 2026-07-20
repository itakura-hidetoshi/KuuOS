#!/usr/bin/env python3
from __future__ import annotations

from typing import Any

from runtime.kuuos_codeai_typed_error_classification_v0_1 import (
    build_codeai_typed_error_classification,
)
from runtime.kuuos_codeai_independent_test_strengthening_schema_v0_1 import (
    CAPABILITY_CATALOG_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
    seal,
)
from scripts.build_codeai_typed_error_classification_fixture_v0_1 import (
    build_fixture as build_classification_fixture,
)


def build_fixture(
    strengthening_spec: dict[str, Any],
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
        raise ValueError("classification fixture blocked: " + ",".join(classification_result.issues))

    classification = classification_result.classification
    classification_receipt = classification_result.receipt
    catalog = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Independent Test Strengthening v0.1",
            "catalog_id": strengthening_spec["catalog_id"],
            "catalog_revision": strengthening_spec["catalog_revision"],
            "supported_check_kinds": sorted(
                capability["check_kind"]
                for capability in strengthening_spec["check_capabilities"]
            ),
            "capability_count": len(strengthening_spec["check_capabilities"]),
            "check_capabilities": strengthening_spec["check_capabilities"],
            "test_generation_performed": False,
            "test_execution_performed": False,
            "verification_authority_granted": False,
            "repository_mutation_performed": False,
            "git_effect_performed": False,
        },
        CAPABILITY_CATALOG_DIGEST_FIELD,
    )
    request = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Independent Test Strengthening v0.1",
            "strengthening_id": strengthening_spec["strengthening_id"],
            "strengthening_revision": strengthening_spec["strengthening_revision"],
            "repository_full_name": classification["repository_full_name"],
            "source_commit_sha": classification["source_commit_sha"],
            "source_classification_digest": classification[
                "codeai_typed_error_classification_digest"
            ],
            "source_classification_receipt_digest": classification_receipt[
                "codeai_typed_error_classification_receipt_digest"
            ],
            "capability_catalog_digest": catalog[
                "codeai_independent_test_capability_catalog_digest"
            ],
            "request_created_epoch": strengthening_spec["request_created_epoch"],
            "unresolved_strengthening_questions": [],
            "claims_authority": False,
        },
        REQUEST_DIGEST_FIELD,
    )
    policy = seal(
        {
            "schema_version": "v0.1",
            "profile_version": "CodeAI Independent Test Strengthening v0.1",
            "expected_repository_full_name": classification["repository_full_name"],
            "expected_source_commit_sha": classification["source_commit_sha"],
            "expected_source_classification_digest": classification[
                "codeai_typed_error_classification_digest"
            ],
            "expected_source_classification_receipt_digest": classification_receipt[
                "codeai_typed_error_classification_receipt_digest"
            ],
            "expected_capability_catalog_digest": catalog[
                "codeai_independent_test_capability_catalog_digest"
            ],
            "evaluation_epoch": strengthening_spec["evaluation_epoch"],
            "maximum_request_age": strengthening_spec["maximum_request_age"],
            "maximum_candidates": strengthening_spec["maximum_candidates"],
            "maximum_obligations": strengthening_spec["maximum_obligations"],
            "require_exact_lineage": True,
            "require_baseline_obligations": True,
            "require_independent_runner": True,
            "require_isolated_execution": True,
            "require_falsification_for_novel_errors": True,
            "require_error_free_mutation_probe": True,
            "require_route_specific_obligations": True,
            "allow_test_generation": False,
            "allow_test_execution": False,
            "allow_candidate_selection": False,
            "allow_verification_authority": False,
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
        "capability_catalog": catalog,
        "strengthening_request": request,
        "strengthening_policy": policy,
    }


__all__ = ["build_fixture"]
