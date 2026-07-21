from __future__ import annotations

from runtime.kuuos_codeai_independent_verifier_ensemble_checks_v0_2 import canonical_digest, seal
from runtime.kuuos_codeai_independent_verifier_ensemble_schema_v0_2 import (
    EVIDENCE_DIGEST_FIELD,
    POLICY_DIGEST_FIELD,
    REQUEST_DIGEST_FIELD,
)

SOURCE_COMMIT = "7566e188174d8e36880b6cfbc77fe164d0637f9c"
REPOSITORY = "itakura-hidetoshi/KuuOS"
CANDIDATE_DIGEST = canonical_digest({"candidate": "order-total-tax-flow-v2"})
CONTEXT_PACK_DIGEST = canonical_digest({"context": "intent-aligned-dataflow-pack-v0.2"})
FAMILIES = [
    "adversarial_and_falsification",
    "behavioral_and_regression",
    "maintainability_and_static",
    "type_and_formal",
]


def build_request() -> dict:
    return seal(
        {
            "request_id": "independent-verifier-ensemble-001",
            "request_revision": "1",
            "repository_full_name": REPOSITORY,
            "source_commit_sha": SOURCE_COMMIT,
            "candidate_digest": CANDIDATE_DIGEST,
            "context_pack_digest": CONTEXT_PACK_DIGEST,
            "required_check_families": FAMILIES,
            "request_created_epoch": 200,
        },
        REQUEST_DIGEST_FIELD,
    )


def build_policy() -> dict:
    return seal(
        {
            "expected_repository_full_name": REPOSITORY,
            "expected_source_commit_sha": SOURCE_COMMIT,
            "expected_candidate_digest": CANDIDATE_DIGEST,
            "expected_context_pack_digest": CONTEXT_PACK_DIGEST,
            "allowed_verifier_ids": ["adversarial-verifier", "behavior-verifier", "formal-verifier", "static-verifier"],
            "allowed_reviewer_ids": ["reviewer-a", "reviewer-b", "reviewer-c", "reviewer-d"],
            "allowed_runner_ids": ["runner-a", "runner-b", "runner-c", "runner-d"],
            "required_check_families": FAMILIES,
            "minimum_verifier_count": 4,
            "minimum_organization_count": 4,
            "minimum_method_count": 4,
            "minimum_pass_quorum": 3,
            "minimum_fail_quorum": 2,
            "maximum_skipped_checks": 0,
            "maximum_evidence_age": 50,
            "maximum_verification_duration": 20,
            "evaluation_epoch": 220,
            "require_distinct_verifiers": True,
            "require_distinct_sessions": True,
            "require_distinct_organizations": True,
            "require_producer_independence": True,
            "require_peer_independence": True,
            "require_prompt_independence": True,
            "require_memory_independence": True,
            "require_test_generation_independence": True,
            "critical_failure_overrides_quorum": True,
            "conflict_requires_hold": True,
            "allow_repository_mutation": False,
            "allow_network_access": False,
            "allow_secret_access": False,
            "allow_candidate_selection_authority": False,
            "allow_execution_authority": False,
            "allow_git_authority": False,
        },
        POLICY_DIGEST_FIELD,
    )


def _packet(index: int, verifier: str, reviewer: str, runner: str, organization: str, family: str, checks: list[str]) -> dict:
    sorted_checks = sorted(checks)
    return seal(
        {
            "evidence_id": f"evidence-{index}",
            "verifier_id": verifier,
            "reviewer_id": reviewer,
            "runner_id": runner,
            "organization_id": organization,
            "verification_session_id": f"session-{index}",
            "nonce": f"nonce-{index}",
            "repository_full_name": REPOSITORY,
            "source_commit_sha": SOURCE_COMMIT,
            "candidate_digest": CANDIDATE_DIGEST,
            "context_pack_digest": CONTEXT_PACK_DIGEST,
            "check_family": family,
            "verification_method_digest": canonical_digest({"method": family, "index": index}),
            "environment_digest": canonical_digest({"environment": organization}),
            "toolchain_digest": canonical_digest({"toolchain": verifier}),
            "protocol_digest": canonical_digest({"protocol": family, "version": 2}),
            "check_ids": sorted_checks,
            "passed_check_ids": sorted_checks,
            "failed_check_ids": [],
            "skipped_check_ids": [],
            "finding_labels": [],
            "highest_severity": "none",
            "declared_outcome": "passed",
            "falsification_executed": family == "adversarial_and_falsification",
            "falsification_passed": True,
            "acceptance_criteria_satisfied": True,
            "independent_from_candidate_producer": True,
            "independent_from_other_verifiers": True,
            "prompt_lineage_independent": True,
            "repair_memory_independent": True,
            "test_generation_independent": True,
            "isolated_execution_reported": True,
            "evidence_artifact_digest": canonical_digest({"artifact": index, "checks": sorted_checks}),
            "verification_started_epoch": 205 + index,
            "verification_completed_epoch": 208 + index,
            "kernel_executed_verification": False,
            "repository_mutation_performed": False,
            "candidate_selection_performed": False,
            "execution_authority_granted": False,
            "git_authority_granted": False,
            "correctness_proof_claimed": False,
        },
        EVIDENCE_DIGEST_FIELD,
    )


def build_evidence_packets() -> list[dict]:
    return [
        _packet(1, "formal-verifier", "reviewer-a", "runner-a", "org-formal", "type_and_formal", ["lean-strict", "python-typecheck"]),
        _packet(2, "behavior-verifier", "reviewer-b", "runner-b", "org-behavior", "behavioral_and_regression", ["unit-regression", "property-regression"]),
        _packet(3, "adversarial-verifier", "reviewer-c", "runner-c", "org-adversarial", "adversarial_and_falsification", ["boundary-falsification", "tamper-falsification"]),
        _packet(4, "static-verifier", "reviewer-d", "runner-d", "org-static", "maintainability_and_static", ["complexity-check", "dead-code-check"]),
    ]


def build_fixture() -> dict:
    return {"request": build_request(), "policy": build_policy(), "evidence_packets": build_evidence_packets()}
