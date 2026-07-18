#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_independent_verification_envelope_v0_1 as m

EXAMPLE_PATH = "examples/codeai_independent_verification_envelope_v0_1.json"


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def reseal_source(value: dict) -> dict:
    return m.seal(value, m.SOURCE_RECEIPT_DIGEST_FIELD)


def reseal_evidence(value: dict) -> dict:
    return m.seal(value, m.EVIDENCE_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def changed(value: dict, field: str, replacement) -> dict:
    result = deepcopy(value)
    result[field] = replacement
    return result


def route(source: dict, evidence: dict, policy: dict) -> dict:
    result = m.build_codeai_independent_verification_envelope(
        source_candidate_receipt=source,
        verification_evidence=evidence,
        verification_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    assert receipt["source_commit_sha"] == receipt["resulting_commit_sha"]
    assert receipt["verification_execution_performed_by_kernel"] is False
    assert receipt["candidate_selected"] is False
    assert receipt["candidate_applied"] is False
    assert receipt["execution_lease_issued"] is False
    assert receipt["repository_mutation_performed"] is False
    assert receipt["git_ref_changed"] is False
    assert receipt["branch_created"] is False
    assert receipt["commit_created"] is False
    assert receipt["push_performed"] is False
    assert receipt["pull_request_created"] is False
    assert receipt["merge_performed"] is False
    assert receipt["deployment_performed"] is False
    assert receipt["secret_access_performed"] is False
    assert receipt["selection_authority_granted"] is False
    assert receipt["verification_authority_granted"] is False
    assert receipt["execution_authority_granted"] is False
    assert receipt["merge_authority_granted"] is False
    assert receipt["deployment_authority_granted"] is False
    assert receipt["secret_access_authority_granted"] is False
    assert receipt["source_receipt_treated_as_verification_authority"] is False
    assert receipt["verification_treated_as_truth"] is False
    assert receipt["passed_treated_as_correctness_proof"] is False
    assert receipt["failed_treated_as_rejection_authority"] is False
    return receipt


def failed_evidence(base: dict) -> dict:
    evidence = deepcopy(base)
    failing = "check:json"
    evidence["passed_check_ids"] = [
        item for item in evidence["passed_check_ids"] if item != failing
    ]
    evidence["failed_check_ids"] = [failing]
    evidence["acceptance_criteria_satisfied"] = False
    evidence["declared_verification_outcome"] = m.OUTCOME_FAILED
    evidence["outcome_reason_ids"] = ["required-check-failed"]
    return reseal_evidence(evidence)


def inconclusive_evidence(base: dict) -> dict:
    evidence = deepcopy(base)
    evidence["evidence_conclusive"] = False
    evidence["declared_verification_outcome"] = m.OUTCOME_INCONCLUSIVE
    evidence["outcome_reason_ids"] = ["bounded-evidence-inconclusive"]
    return reseal_evidence(evidence)


def main() -> None:
    example = load_example()
    base_source = example["source_candidate_receipt"]
    base_evidence = example["verification_evidence"]
    base_policy = example["verification_policy"]

    passed = route(base_source, base_evidence, base_policy)
    assert passed["codeai_disposition"] == m.DISPOSITION_PASSED
    assert passed["operating_mode"] == m.MODE_VERIFIED_PASS
    assert passed["verification_outcome"] == m.OUTCOME_PASSED
    assert passed["verification_completed"] is True
    assert passed["verification_debt_open"] is False
    assert passed["candidate_verification_passed"] is True

    cases: list[tuple[str, str, dict, dict, dict]] = []

    source = reseal_source(changed(base_source, "candidate_patch_ready", False))
    cases.append(
        (
            m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
            m.MODE_REJECTED,
            source,
            base_evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "provenance_integrity_confirmed", False)
    )
    cases.append(
        (
            m.DISPOSITION_PROVENANCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "verifier_id", base_source["producer_id"])
    )
    cases.append(
        (
            m.DISPOSITION_INDEPENDENCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "repository_full_name", "unowned/other")
    )
    cases.append(
        (
            m.DISPOSITION_CORRESPONDENCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "evidence_integrity_confirmed", False)
    )
    cases.append(
        (
            m.DISPOSITION_EVIDENCE_INTEGRITY_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(changed(base_evidence, "declared_check_count", 4))
    cases.append(
        (
            m.DISPOSITION_CHECK_ACCOUNTING_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = deepcopy(base_evidence)
    evidence["verification_started_epoch"] = 0
    evidence["verification_completed_epoch"] = 60
    evidence = reseal_evidence(evidence)
    cases.append(
        (
            m.DISPOSITION_WINDOW_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(
            base_evidence,
            "prior_verification_session_ids",
            [base_evidence["verification_session_id"]],
        )
    )
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "live_repository_mutated_by_verifier", True)
    )
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "execution_authority_claimed", True)
    )
    cases.append(
        (
            m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "toolchain_digest", "unsupported-toolchain")
    )
    cases.append(
        (
            m.DISPOSITION_UNSUPPORTED_PROFILE_ABSTAINED,
            m.MODE_ABSTAIN,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = deepcopy(base_evidence)
    evidence["check_ids"] = ["check:lean", "check:python"]
    evidence["passed_check_ids"] = ["check:lean", "check:python"]
    evidence["declared_check_count"] = 2
    evidence = reseal_evidence(evidence)
    cases.append(
        (
            m.DISPOSITION_MANDATORY_EVIDENCE_HOLD,
            m.MODE_HOLD,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = deepcopy(base_evidence)
    evidence["planned_reproduction_attempts"] = 1
    evidence["completed_reproduction_attempts"] = 1
    evidence["successful_reproduction_attempts"] = 1
    evidence = reseal_evidence(evidence)
    cases.append(
        (
            m.DISPOSITION_PROTOCOL_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = deepcopy(base_evidence)
    evidence["declared_verification_outcome"] = m.OUTCOME_FAILED
    evidence["outcome_reason_ids"] = ["inconsistent-failure-verdict"]
    evidence = reseal_evidence(evidence)
    cases.append(
        (
            m.DISPOSITION_OUTCOME_REPAIR,
            m.MODE_REJECTED,
            base_source,
            evidence,
            base_policy,
        )
    )

    evidence = reseal_evidence(
        changed(base_evidence, "finding_labels", ["security"])
    )
    cases.append(
        (
            m.DISPOSITION_FINDING_HANDOVER,
            m.MODE_HANDOVER,
            base_source,
            evidence,
            base_policy,
        )
    )

    inconclusive = inconclusive_evidence(base_evidence)
    policy = reseal_policy(
        changed(base_policy, "allow_inconclusive_degradation", False)
    )
    cases.append(
        (
            m.DISPOSITION_INCONCLUSIVE_HOLD,
            m.MODE_HOLD,
            base_source,
            inconclusive,
            policy,
        )
    )
    cases.append(
        (
            m.DISPOSITION_INCONCLUSIVE_DEGRADED,
            m.MODE_DEGRADED_VERIFICATION,
            base_source,
            inconclusive,
            base_policy,
        )
    )

    failed = failed_evidence(base_evidence)
    cases.append(
        (
            m.DISPOSITION_FAILED,
            m.MODE_VERIFIED_FAIL,
            base_source,
            failed,
            base_policy,
        )
    )

    observed = {m.DISPOSITION_PASSED}
    for expected_disposition, expected_mode, source, evidence, policy in cases:
        receipt = route(source, evidence, policy)
        assert receipt["codeai_disposition"] == expected_disposition, receipt
        assert receipt["operating_mode"] == expected_mode, receipt
        observed.add(expected_disposition)

    expected = {
        m.DISPOSITION_PASSED,
        m.DISPOSITION_FAILED,
        m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
        m.DISPOSITION_PROVENANCE_REPAIR,
        m.DISPOSITION_INDEPENDENCE_REPAIR,
        m.DISPOSITION_CORRESPONDENCE_REPAIR,
        m.DISPOSITION_EVIDENCE_INTEGRITY_REPAIR,
        m.DISPOSITION_CHECK_ACCOUNTING_REPAIR,
        m.DISPOSITION_WINDOW_REPAIR,
        m.DISPOSITION_REPLAY_REJECTED,
        m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
        m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        m.DISPOSITION_UNSUPPORTED_PROFILE_ABSTAINED,
        m.DISPOSITION_MANDATORY_EVIDENCE_HOLD,
        m.DISPOSITION_PROTOCOL_REPAIR,
        m.DISPOSITION_OUTCOME_REPAIR,
        m.DISPOSITION_FINDING_HANDOVER,
        m.DISPOSITION_INCONCLUSIVE_HOLD,
        m.DISPOSITION_INCONCLUSIVE_DEGRADED,
    }
    assert observed == expected

    failed_receipt = route(base_source, failed, base_policy)
    assert failed_receipt["verification_outcome"] == m.OUTCOME_FAILED
    assert failed_receipt["verification_completed"] is True
    assert failed_receipt["verification_debt_open"] is False
    assert failed_receipt["candidate_verification_failed"] is True
    assert failed_receipt["failed_treated_as_rejection_authority"] is False

    degraded_receipt = route(base_source, inconclusive, base_policy)
    assert degraded_receipt["verification_outcome"] == m.OUTCOME_INCONCLUSIVE
    assert degraded_receipt["verification_debt_open"] is True
    assert degraded_receipt["reverification_required"] is True

    tampered = deepcopy(base_evidence)
    tampered["finding_labels"] = ["unsealed-finding"]
    blocked = m.build_codeai_independent_verification_envelope(
        source_candidate_receipt=base_source,
        verification_evidence=tampered,
        verification_policy=base_policy,
    )
    assert blocked.status == m.STATUS_BLOCKED
    assert blocked.receipt is None
    assert "verification_evidence_digest_mismatch" in blocked.issues

    print("CodeAI Independent Verification v0.1 checks: PASS (19 routes)")


if __name__ == "__main__":
    main()
