#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_candidate_patch_envelope_v0_1 as m

EXAMPLE_PATH = "examples/codeai_candidate_patch_envelope_v0_1.json"


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def reseal_source(value: dict) -> dict:
    return m.seal(value, m.SOURCE_RECEIPT_DIGEST_FIELD)


def reseal_candidate(value: dict) -> dict:
    return m.seal(value, m.CANDIDATE_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def changed(value: dict, field: str, replacement) -> dict:
    result = deepcopy(value)
    result[field] = replacement
    return result


def candidate_for_artifact(candidate: dict, artifact: str) -> dict:
    result = deepcopy(candidate)
    result["patch_artifact_digest"] = m.patch_artifact_digest(artifact)
    result["patch_size_bytes"] = len(artifact.encode("utf-8"))
    return reseal_candidate(result)


def route(source: dict, candidate: dict, artifact: str, policy: dict) -> dict:
    result = m.build_codeai_candidate_patch_envelope(
        source_observation_receipt=source,
        patch_candidate=candidate,
        patch_artifact=artifact,
        candidate_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    assert receipt["source_commit_sha"] == receipt["resulting_commit_sha"]
    assert receipt["patch_candidate_only"] is True
    assert receipt["candidate_generated_by_kernel"] is False
    assert receipt["candidate_selected"] is False
    assert receipt["verification_lease_issued"] is False
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
    assert receipt["source_receipt_treated_as_successor_authority"] is False
    assert receipt["candidate_treated_as_correct"] is False
    assert receipt["validation_treated_as_correctness_proof"] is False
    return receipt


def main() -> None:
    example = load_example()
    base_source = example["source_observation_receipt"]
    base_candidate = example["patch_candidate"]
    base_artifact = example["patch_artifact"]
    base_policy = example["candidate_policy"]

    supported = route(base_source, base_candidate, base_artifact, base_policy)
    assert supported["codeai_disposition"] == m.DISPOSITION_SUPPORTED
    assert supported["operating_mode"] == m.MODE_PROPOSAL_ONLY
    assert supported["candidate_patch_ready"] is True
    assert supported["candidate_patch_artifact_parsed"] is True

    cases: list[tuple[str, str, dict, dict, str, dict]] = []

    source = reseal_source(changed(base_source, "codeai_profile_ready", False))
    cases.append(
        (
            m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
            m.MODE_REJECTED,
            source,
            base_candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(
        changed(base_candidate, "candidate_provenance_confirmed", False)
    )
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_PROVENANCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(
        changed(base_candidate, "repository_full_name", "unowned/other")
    )
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_CORRESPONDENCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    cases.append(
        (
            m.DISPOSITION_PATCH_ARTIFACT_REPAIR,
            m.MODE_REJECTED,
            base_source,
            base_candidate,
            base_artifact + "tampered\n",
            base_policy,
        )
    )

    candidate = reseal_candidate(changed(base_candidate, "candidate_created_epoch", 0))
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_WINDOW_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(
        changed(
            base_candidate,
            "prior_producer_session_ids",
            [base_candidate["producer_session_id"]],
        )
    )
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(
        changed(base_candidate, "patch_applied_by_kernel", True)
    )
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(
        changed(base_candidate, "execution_authority_claimed", True)
    )
    cases.append(
        (
            m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(changed(base_candidate, "patch_format", "context_diff"))
    cases.append(
        (
            m.DISPOSITION_UNSUPPORTED_PATCH_FORMAT_ABSTAINED,
            m.MODE_ABSTAIN,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    invalid_artifact = "diff --git malformed\nnot-a-supported-section\n"
    candidate = candidate_for_artifact(base_candidate, invalid_artifact)
    cases.append(
        (
            m.DISPOSITION_PATCH_SYNTAX_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            invalid_artifact,
            base_policy,
        )
    )

    candidate = deepcopy(base_candidate)
    candidate["changed_paths"] = [
        "docs/CodeAI/CANDIDATE_EXAMPLE.md",
        "docs/CodeAI/UNDECLARED.md",
    ]
    candidate["declared_change_count"] = 2
    candidate = reseal_candidate(candidate)
    cases.append(
        (
            m.DISPOSITION_PATH_ACCOUNTING_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    policy = reseal_policy(
        changed(base_policy, "allowed_path_prefixes", ["runtime"])
    )
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_SCOPE_REJECTED,
            m.MODE_REJECTED,
            base_source,
            base_candidate,
            base_artifact,
            policy,
        )
    )

    policy = reseal_policy(changed(base_policy, "maximum_patch_bytes", 1))
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_BUDGET_REJECTED,
            m.MODE_REJECTED,
            base_source,
            base_candidate,
            base_artifact,
            policy,
        )
    )

    candidate = reseal_candidate(
        changed(
            base_candidate,
            "unresolved_candidate_questions",
            ["which owner may approve this candidate?"],
        )
    )
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_CLARIFICATION_HOLD,
            m.MODE_HOLD,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(changed(base_candidate, "risk_labels", ["security"]))
    cases.append(
        (
            m.DISPOSITION_RISK_OWNERSHIP_HANDOVER,
            m.MODE_HANDOVER,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    candidate = reseal_candidate(changed(base_candidate, "test_plan_ids", []))
    policy = reseal_policy(
        changed(base_policy, "allow_evidence_degradation", False)
    )
    cases.append(
        (
            m.DISPOSITION_CANDIDATE_EVIDENCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            candidate,
            base_artifact,
            policy,
        )
    )

    cases.append(
        (
            m.DISPOSITION_CANDIDATE_EVIDENCE_DEGRADED,
            m.MODE_DEGRADED_PROPOSAL,
            base_source,
            candidate,
            base_artifact,
            base_policy,
        )
    )

    observed = {m.DISPOSITION_SUPPORTED}
    for expected_disposition, expected_mode, source, candidate, artifact, policy in cases:
        receipt = route(source, candidate, artifact, policy)
        assert receipt["codeai_disposition"] == expected_disposition, receipt
        assert receipt["operating_mode"] == expected_mode, receipt
        assert receipt["candidate_patch_ready"] is False, receipt
        observed.add(expected_disposition)

    expected = {
        m.DISPOSITION_SUPPORTED,
        m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
        m.DISPOSITION_CANDIDATE_PROVENANCE_REPAIR,
        m.DISPOSITION_REPOSITORY_CORRESPONDENCE_REPAIR,
        m.DISPOSITION_PATCH_ARTIFACT_REPAIR,
        m.DISPOSITION_CANDIDATE_WINDOW_REPAIR,
        m.DISPOSITION_REPLAY_REJECTED,
        m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
        m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        m.DISPOSITION_UNSUPPORTED_PATCH_FORMAT_ABSTAINED,
        m.DISPOSITION_PATCH_SYNTAX_REPAIR,
        m.DISPOSITION_PATH_ACCOUNTING_REPAIR,
        m.DISPOSITION_CANDIDATE_SCOPE_REJECTED,
        m.DISPOSITION_CANDIDATE_BUDGET_REJECTED,
        m.DISPOSITION_CANDIDATE_CLARIFICATION_HOLD,
        m.DISPOSITION_RISK_OWNERSHIP_HANDOVER,
        m.DISPOSITION_CANDIDATE_EVIDENCE_REPAIR,
        m.DISPOSITION_CANDIDATE_EVIDENCE_DEGRADED,
    }
    assert observed == expected

    tampered = deepcopy(base_candidate)
    tampered["risk_labels"] = ["unsealed-risk"]
    blocked = m.build_codeai_candidate_patch_envelope(
        source_observation_receipt=base_source,
        patch_candidate=tampered,
        patch_artifact=base_artifact,
        candidate_policy=base_policy,
    )
    assert blocked.status == m.STATUS_BLOCKED
    assert blocked.receipt is None
    assert "patch_candidate_digest_mismatch" in blocked.issues

    print("CodeAI Candidate Patch v0.1 checks: PASS (18 routes)")


if __name__ == "__main__":
    main()
