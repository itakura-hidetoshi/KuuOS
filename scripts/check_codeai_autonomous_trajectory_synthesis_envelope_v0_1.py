#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_autonomous_trajectory_synthesis_envelope_v0_1 as m

EXAMPLE_PATH = "examples/codeai_autonomous_trajectory_synthesis_envelope_v0_1.json"


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def reseal_source(value: dict) -> dict:
    return m.seal(value, m.SOURCE_RECEIPT_DIGEST_FIELD)


def reseal_request(value: dict) -> dict:
    return m.seal(value, m.REQUEST_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def changed(value: dict, field: str, replacement) -> dict:
    result = deepcopy(value)
    result[field] = replacement
    return result


def failed_source(base: dict) -> dict:
    source = deepcopy(base)
    source["codeai_disposition"] = "independent_verification_failed"
    source["operating_mode"] = "verified_fail"
    source["verification_outcome"] = m.OUTCOME_FAILED
    source["candidate_verification_passed"] = False
    source["candidate_verification_failed"] = True
    source["passed_check_count"] = 2
    source["failed_check_count"] = 1
    return reseal_source(source)


def inconclusive_source(base: dict) -> dict:
    source = deepcopy(base)
    source["codeai_disposition"] = "verification_inconclusive_degraded"
    source["operating_mode"] = "degraded_verification"
    source["verification_outcome"] = m.OUTCOME_INCONCLUSIVE
    source["verification_debt_open"] = True
    source["reverification_required"] = True
    source["candidate_verification_passed"] = False
    source["evidence_degraded"] = True
    return reseal_source(source)


def bind_to_source(request: dict, policy: dict, source: dict) -> tuple[dict, dict]:
    bound_request = deepcopy(request)
    bound_policy = deepcopy(policy)
    bindings = {
        "source_verification_receipt_digest": source[m.SOURCE_RECEIPT_DIGEST_FIELD],
        "source_candidate_receipt_digest": source["source_candidate_receipt_digest"],
        "candidate_patch_digest": source["candidate_patch_digest"],
        "patch_artifact_digest": source["patch_artifact_digest"],
        "repository_full_name": source["repository_full_name"],
        "source_commit_sha": source["source_commit_sha"],
    }
    bound_request.update(bindings)
    bound_policy.update(
        {
            "expected_source_verification_receipt_digest": bindings[
                "source_verification_receipt_digest"
            ],
            "expected_source_candidate_receipt_digest": bindings[
                "source_candidate_receipt_digest"
            ],
            "expected_candidate_patch_digest": bindings["candidate_patch_digest"],
            "expected_repository_full_name": bindings["repository_full_name"],
            "expected_source_commit_sha": bindings["source_commit_sha"],
        }
    )
    return reseal_request(bound_request), reseal_policy(bound_policy)


def route(source: dict, request: dict, policy: dict) -> dict:
    result = m.build_codeai_autonomous_trajectory_synthesis_envelope(
        source_verification_receipt=source,
        trajectory_request=request,
        trajectory_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    assert receipt["source_commit_sha"] == receipt["resulting_commit_sha"]
    assert receipt["trajectory_read_only"] is True
    assert receipt["full_intent_lineage_reconstructed"] is False
    assert receipt["human_handover_performed"] is False
    assert receipt["external_authority_handover_performed"] is False
    for field in (
        "candidate_selected",
        "patch_generated",
        "patch_applied",
        "execution_lease_issued",
        "repository_mutation_performed",
        "git_ref_changed",
        "branch_created",
        "commit_created",
        "push_performed",
        "pull_request_created",
        "merge_performed",
        "deployment_performed",
        "secret_access_performed",
        "selection_authority_granted",
        "verification_authority_granted",
        "execution_authority_granted",
        "merge_authority_granted",
        "deployment_authority_granted",
        "secret_access_authority_granted",
        "source_receipt_treated_as_successor_authority",
        "trajectory_treated_as_truth",
        "autonomous_candidate_treated_as_authority",
    ):
        assert receipt[field] is False, field
    return receipt


def main() -> None:
    example = load_example()
    base_source = example["source_verification_receipt"]
    base_request = example["trajectory_request"]
    base_policy = example["trajectory_policy"]

    passed = route(base_source, base_request, base_policy)
    assert passed["codeai_disposition"] == m.DISPOSITION_DELIBERATION
    assert passed["operating_mode"] == m.MODE_AUTONOMOUS_READ_ONLY
    assert passed["trajectory_step_count"] == 2
    assert passed["trajectory_synthesized_by_kernel"] is True
    assert passed["trajectory_complete_for_available_receipts"] is True
    assert passed["autonomous_deliberation_candidate_generated"] is True

    cases: list[tuple[str, str, dict, dict, dict]] = []

    source = reseal_source(changed(base_source, "candidate_selected", True))
    request, policy = bind_to_source(base_request, base_policy, source)
    cases.append(
        (
            m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
            m.MODE_REJECTED,
            source,
            request,
            policy,
        )
    )

    request = reseal_request(
        changed(base_request, "provenance_integrity_confirmed", False)
    )
    cases.append(
        (
            m.DISPOSITION_PROVENANCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(
        changed(base_request, "repository_full_name", "unowned/other")
    )
    cases.append(
        (
            m.DISPOSITION_CORRESPONDENCE_REPAIR,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "request_created_epoch", 4800))
    cases.append(
        (
            m.DISPOSITION_WINDOW_REPAIR,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(
        changed(
            base_request,
            "prior_synthesis_session_ids",
            [base_request["synthesis_session_id"]],
        )
    )
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "patch_generation_requested", True))
    cases.append(
        (
            m.DISPOSITION_EFFECT_REQUEST_REJECTED,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "execution_authority_claimed", True))
    cases.append(
        (
            m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "external_handover_requested", True))
    cases.append(
        (
            m.DISPOSITION_HANDOVER_DEFERRED,
            m.MODE_HOLD,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "trajectory_format", "unsupported"))
    cases.append(
        (
            m.DISPOSITION_UNSUPPORTED_FORMAT_ABSTAINED,
            m.MODE_ABSTAIN,
            base_source,
            request,
            base_policy,
        )
    )

    request = reseal_request(changed(base_request, "requested_step_count", 3))
    cases.append(
        (
            m.DISPOSITION_BUDGET_REJECTED,
            m.MODE_REJECTED,
            base_source,
            request,
            base_policy,
        )
    )

    policy = reseal_policy(
        changed(base_policy, "require_passed_for_deliberation", False)
    )
    cases.append(
        (
            m.DISPOSITION_OUTCOME_POLICY_REPAIR,
            m.MODE_REJECTED,
            base_source,
            base_request,
            policy,
        )
    )

    failed = failed_source(base_source)
    request, policy = bind_to_source(base_request, base_policy, failed)
    cases.append(
        (
            m.DISPOSITION_REPAIR,
            m.MODE_AUTONOMOUS_REPAIR,
            failed,
            request,
            policy,
        )
    )

    inconclusive = inconclusive_source(base_source)
    request, policy = bind_to_source(base_request, base_policy, inconclusive)
    cases.append(
        (
            m.DISPOSITION_REVERIFICATION,
            m.MODE_DEGRADED_AUTONOMY,
            inconclusive,
            request,
            policy,
        )
    )

    observed = {m.DISPOSITION_DELIBERATION}
    for expected_disposition, expected_mode, source, request, policy in cases:
        receipt = route(source, request, policy)
        assert receipt["codeai_disposition"] == expected_disposition, receipt
        assert receipt["operating_mode"] == expected_mode, receipt
        observed.add(expected_disposition)

    expected = {
        m.DISPOSITION_DELIBERATION,
        m.DISPOSITION_REPAIR,
        m.DISPOSITION_REVERIFICATION,
        m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
        m.DISPOSITION_PROVENANCE_REPAIR,
        m.DISPOSITION_CORRESPONDENCE_REPAIR,
        m.DISPOSITION_WINDOW_REPAIR,
        m.DISPOSITION_REPLAY_REJECTED,
        m.DISPOSITION_EFFECT_REQUEST_REJECTED,
        m.DISPOSITION_AUTHORITY_ESCALATION_REJECTED,
        m.DISPOSITION_HANDOVER_DEFERRED,
        m.DISPOSITION_UNSUPPORTED_FORMAT_ABSTAINED,
        m.DISPOSITION_BUDGET_REJECTED,
        m.DISPOSITION_OUTCOME_POLICY_REPAIR,
    }
    assert observed == expected

    failed_request, failed_policy = bind_to_source(base_request, base_policy, failed)
    failed_receipt = route(failed, failed_request, failed_policy)
    assert failed_receipt["next_internal_step_kind"] == m.NEXT_REPAIR
    assert failed_receipt["autonomous_repair_candidate_generated"] is True
    assert failed_receipt["patch_generated"] is False

    inconclusive_request, inconclusive_policy = bind_to_source(
        base_request, base_policy, inconclusive
    )
    inconclusive_receipt = route(
        inconclusive, inconclusive_request, inconclusive_policy
    )
    assert inconclusive_receipt["next_internal_step_kind"] == m.NEXT_REVERIFICATION
    assert inconclusive_receipt["autonomous_reverification_candidate_generated"] is True
    assert inconclusive_receipt["evidence_degraded"] is True

    handover_request = reseal_request(
        changed(base_request, "external_handover_requested", True)
    )
    deferred = route(base_source, handover_request, base_policy)
    assert deferred["external_handover_deferred"] is True
    assert deferred["trajectory_synthesized_by_kernel"] is False
    assert deferred["human_handover_performed"] is False
    assert deferred["external_authority_handover_performed"] is False

    tampered = deepcopy(base_request)
    tampered["trajectory_revision"] = "unsealed-revision"
    blocked = m.build_codeai_autonomous_trajectory_synthesis_envelope(
        source_verification_receipt=base_source,
        trajectory_request=tampered,
        trajectory_policy=base_policy,
    )
    assert blocked.status == m.STATUS_BLOCKED
    assert blocked.receipt is None
    assert "trajectory_request_digest_mismatch" in blocked.issues

    print("CodeAI Autonomous Trajectory Synthesis v0.1 checks: PASS (14 routes)")


if __name__ == "__main__":
    main()
