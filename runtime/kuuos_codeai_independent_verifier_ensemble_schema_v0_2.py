from __future__ import annotations

VERSION = "kuuos_codeai_independent_verifier_ensemble_v0_2"
SCHEMA_VERSION = "v0.2"
PROFILE_VERSION = "CodeAI Independent Verifier Ensemble v0.2"

STATUS_READY = "ready"
STATUS_BLOCKED = "blocked"
MODE_CONSENSUS_PASS = "consensus_pass"
MODE_CONSENSUS_FAIL = "consensus_fail"
MODE_DISAGREEMENT_HOLD = "disagreement_hold"
MODE_INCONCLUSIVE_HOLD = "inconclusive_hold"

DISPOSITION_ACCEPTED = "independent_verifier_ensemble_consensus_passed"
DISPOSITION_FAILED = "independent_verifier_ensemble_consensus_failed"
DISPOSITION_DISAGREEMENT = "independent_verifier_ensemble_disagreement_held"
DISPOSITION_INCONCLUSIVE = "independent_verifier_ensemble_inconclusive_held"

REQUEST_DIGEST_FIELD = "codeai_independent_verifier_ensemble_request_digest"
POLICY_DIGEST_FIELD = "codeai_independent_verifier_ensemble_policy_digest"
EVIDENCE_DIGEST_FIELD = "codeai_independent_verifier_evidence_digest"
ENSEMBLE_DIGEST_FIELD = "codeai_independent_verifier_ensemble_digest"
RECEIPT_DIGEST_FIELD = "codeai_independent_verifier_ensemble_receipt_digest"

ALLOWED_OUTCOMES = {"passed", "failed", "inconclusive"}
ALLOWED_FAMILIES = {
    "type_and_formal",
    "behavioral_and_regression",
    "adversarial_and_falsification",
    "maintainability_and_static",
}
ALLOWED_SEVERITIES = {"none", "low", "medium", "high", "critical"}

REQUEST_FIELDS = {
    "request_id",
    "request_revision",
    "repository_full_name",
    "source_commit_sha",
    "candidate_digest",
    "context_pack_digest",
    "required_check_families",
    "request_created_epoch",
    REQUEST_DIGEST_FIELD,
}

POLICY_FIELDS = {
    "expected_repository_full_name",
    "expected_source_commit_sha",
    "expected_candidate_digest",
    "expected_context_pack_digest",
    "allowed_verifier_ids",
    "allowed_reviewer_ids",
    "allowed_runner_ids",
    "required_check_families",
    "minimum_verifier_count",
    "minimum_organization_count",
    "minimum_method_count",
    "minimum_pass_quorum",
    "minimum_fail_quorum",
    "maximum_skipped_checks",
    "maximum_evidence_age",
    "maximum_verification_duration",
    "evaluation_epoch",
    "require_distinct_verifiers",
    "require_distinct_sessions",
    "require_distinct_organizations",
    "require_producer_independence",
    "require_peer_independence",
    "require_prompt_independence",
    "require_memory_independence",
    "require_test_generation_independence",
    "critical_failure_overrides_quorum",
    "conflict_requires_hold",
    "allow_repository_mutation",
    "allow_network_access",
    "allow_secret_access",
    "allow_candidate_selection_authority",
    "allow_execution_authority",
    "allow_git_authority",
    POLICY_DIGEST_FIELD,
}

EVIDENCE_FIELDS = {
    "evidence_id",
    "verifier_id",
    "reviewer_id",
    "runner_id",
    "organization_id",
    "verification_session_id",
    "nonce",
    "repository_full_name",
    "source_commit_sha",
    "candidate_digest",
    "context_pack_digest",
    "check_family",
    "verification_method_digest",
    "environment_digest",
    "toolchain_digest",
    "protocol_digest",
    "check_ids",
    "passed_check_ids",
    "failed_check_ids",
    "skipped_check_ids",
    "finding_labels",
    "highest_severity",
    "declared_outcome",
    "falsification_executed",
    "falsification_passed",
    "acceptance_criteria_satisfied",
    "independent_from_candidate_producer",
    "independent_from_other_verifiers",
    "prompt_lineage_independent",
    "repair_memory_independent",
    "test_generation_independent",
    "isolated_execution_reported",
    "evidence_artifact_digest",
    "verification_started_epoch",
    "verification_completed_epoch",
    "kernel_executed_verification",
    "repository_mutation_performed",
    "candidate_selection_performed",
    "execution_authority_granted",
    "git_authority_granted",
    "correctness_proof_claimed",
    EVIDENCE_DIGEST_FIELD,
}
