#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_intent_repository_observation_envelope_v0_1 as m

EXAMPLE_PATH = "examples/codeai_intent_repository_observation_envelope_v0_1.json"


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def reseal_intent(value: dict) -> dict:
    return m.seal(value, m.INTENT_DIGEST_FIELD)


def reseal_repository(value: dict) -> dict:
    return m.seal(value, m.REPOSITORY_OBSERVATION_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def route(intent: dict, repository: dict, policy: dict) -> dict:
    result = m.build_codeai_intent_repository_observation_envelope(
        intent_packet=intent,
        repository_observation=repository,
        observation_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    assert receipt["source_commit_sha"] == receipt["resulting_commit_sha"]
    assert receipt["repository_observation_read_only"] is True
    assert receipt["code_change_candidate_created"] is False
    assert receipt["execution_lease_issued"] is False
    assert receipt["repository_mutation_performed"] is False
    assert receipt["selection_authority_granted"] is False
    assert receipt["execution_authority_granted"] is False
    assert receipt["merge_authority_granted"] is False
    assert receipt["deployment_authority_granted"] is False
    assert receipt["secret_access_authority_granted"] is False
    assert receipt["intent_treated_as_truth"] is False
    assert receipt["repository_observation_treated_as_repository_truth"] is False
    assert receipt["validation_treated_as_correctness_proof"] is False
    return receipt


def mutate_and_seal(value: dict, field: str, replacement) -> dict:
    changed = deepcopy(value)
    changed[field] = replacement
    return changed


def main() -> None:
    example = load_example()
    base_intent = example["intent_packet"]
    base_repository = example["repository_observation"]
    base_policy = example["observation_policy"]

    supported = route(base_intent, base_repository, base_policy)
    assert supported["codeai_disposition"] == m.DISPOSITION_SUPPORTED
    assert supported["operating_mode"] == m.MODE_READ_ONLY
    assert supported["codeai_profile_ready"] is True
    assert supported["route_receipt_recorded"] is True

    cases: list[tuple[str, str, dict, dict, dict]] = []

    intent = mutate_and_seal(base_intent, "intent_provenance_confirmed", False)
    cases.append(
        (
            m.DISPOSITION_INTENT_PROVENANCE_REPAIR,
            m.MODE_REJECTED,
            reseal_intent(intent),
            base_repository,
            base_policy,
        )
    )

    repository = mutate_and_seal(base_repository, "source_commit_sha", "0" * 40)
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_IDENTITY_REPAIR,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(base_repository, "tree_digest", "")
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_SNAPSHOT_REPAIR,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(base_repository, "declared_path_count", 9)
    cases.append(
        (
            m.DISPOSITION_PATH_ACCOUNTING_REPAIR,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(base_repository, "baseline_checks_complete", False)
    cases.append(
        (
            m.DISPOSITION_BASELINE_EVIDENCE_REPAIR,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(
        base_repository,
        "observation_completed_epoch",
        base_repository["observation_started_epoch"]
        + base_policy["maximum_observation_duration"]
        + 1,
    )
    cases.append(
        (
            m.DISPOSITION_OBSERVATION_WINDOW_REPAIR,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(
        base_repository, "prior_session_ids", [base_repository["session_id"]]
    )
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(
        base_repository, "repository_files_changed_by_kernel", True
    )
    cases.append(
        (
            m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(
        base_repository, "execution_authority_claimed", True
    )
    cases.append(
        (
            m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
            m.MODE_REJECTED,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    intent = mutate_and_seal(
        base_intent,
        "unresolved_questions",
        ["which authority owns deployment policy?"],
    )
    cases.append(
        (
            m.DISPOSITION_INTENT_CLARIFICATION_HOLD,
            m.MODE_HOLD,
            reseal_intent(intent),
            base_repository,
            base_policy,
        )
    )

    repository = mutate_and_seal(base_repository, "toolchain_supported", False)
    cases.append(
        (
            m.DISPOSITION_UNSUPPORTED_TOOLCHAIN_ABSTAINED,
            m.MODE_ABSTAIN,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = mutate_and_seal(
        base_repository, "crosses_unowned_boundary", True
    )
    cases.append(
        (
            m.DISPOSITION_OWNERSHIP_HANDOVER,
            m.MODE_HANDOVER,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    repository = deepcopy(base_repository)
    repository["unavailable_paths"] = ["private/owned_elsewhere.py"]
    repository["declared_path_count"] += 1
    cases.append(
        (
            m.DISPOSITION_PARTIAL_OBSERVATION_DEGRADED,
            m.MODE_DEGRADED_READ_ONLY,
            base_intent,
            reseal_repository(repository),
            base_policy,
        )
    )

    observed: set[str] = {m.DISPOSITION_SUPPORTED}
    for expected_disposition, expected_mode, intent, repository, policy in cases:
        receipt = route(intent, repository, policy)
        assert receipt["codeai_disposition"] == expected_disposition, receipt
        assert receipt["operating_mode"] == expected_mode, receipt
        assert receipt["codeai_profile_ready"] is False, receipt
        observed.add(expected_disposition)

    expected = {
        m.DISPOSITION_SUPPORTED,
        m.DISPOSITION_INTENT_PROVENANCE_REPAIR,
        m.DISPOSITION_REPOSITORY_IDENTITY_REPAIR,
        m.DISPOSITION_REPOSITORY_SNAPSHOT_REPAIR,
        m.DISPOSITION_PATH_ACCOUNTING_REPAIR,
        m.DISPOSITION_BASELINE_EVIDENCE_REPAIR,
        m.DISPOSITION_OBSERVATION_WINDOW_REPAIR,
        m.DISPOSITION_REPLAY_REJECTED,
        m.DISPOSITION_REPOSITORY_MUTATION_REJECTED,
        m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        m.DISPOSITION_INTENT_CLARIFICATION_HOLD,
        m.DISPOSITION_UNSUPPORTED_TOOLCHAIN_ABSTAINED,
        m.DISPOSITION_OWNERSHIP_HANDOVER,
        m.DISPOSITION_PARTIAL_OBSERVATION_DEGRADED,
    }
    assert observed == expected

    tampered = deepcopy(base_intent)
    tampered["requirements"] = ["tampered without resealing"]
    blocked = m.build_codeai_intent_repository_observation_envelope(
        intent_packet=tampered,
        repository_observation=base_repository,
        observation_policy=base_policy,
    )
    assert blocked.status == m.STATUS_BLOCKED
    assert blocked.receipt is None
    assert "intent_packet_digest_mismatch" in blocked.issues

    print("CodeAI v0.1 intent/repository observation checks: PASS (14 routes)")


if __name__ == "__main__":
    main()
