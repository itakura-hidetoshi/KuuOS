#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import runtime.kuuos_codeai_autonomous_git_lifecycle_envelope_v0_1 as m

EXAMPLE_PATH = "examples/codeai_autonomous_git_lifecycle_envelope_v0_1.json"
COMMIT_SHA = "a" * 40
MERGE_SHA = "b" * 40


def load_example() -> dict:
    root = Path(__file__).resolve().parents[1]
    return json.loads((root / EXAMPLE_PATH).read_text(encoding="utf-8"))


def changed(value: dict, field: str, replacement) -> dict:
    result = deepcopy(value)
    result[field] = replacement
    return result


def reseal_source(value: dict) -> dict:
    return m.seal(value, m.SOURCE_RECEIPT_DIGEST_FIELD)


def reseal_request(value: dict) -> dict:
    return m.seal(value, m.REQUEST_DIGEST_FIELD)


def reseal_state(value: dict) -> dict:
    return m.seal(value, m.STATE_DIGEST_FIELD)


def reseal_policy(value: dict) -> dict:
    return m.seal(value, m.POLICY_DIGEST_FIELD)


def committed_state(base: dict, commit_sha: str = COMMIT_SHA) -> dict:
    state = deepcopy(base)
    state["local_commit_created"] = True
    state["local_commit_sha"] = commit_sha
    state["local_commit_parent_sha"] = state["source_commit_sha"]
    return reseal_state(state)


def pushed_state(base: dict) -> dict:
    state = deepcopy(committed_state(base))
    state["branch_pushed"] = True
    state["pushed_head_sha"] = state["local_commit_sha"]
    return reseal_state(state)


def pull_request_state(base: dict, *, draft: bool = True) -> dict:
    state = deepcopy(pushed_state(base))
    state["pull_request_created"] = True
    state["pull_request_number"] = 1288
    state["pull_request_url_digest"] = "9" * 64
    state["pull_request_draft"] = draft
    state["pr_head_sha"] = state["local_commit_sha"]
    state["pr_base_branch"] = state["base_branch"]
    return reseal_state(state)


def checks_state(
    base: dict,
    policy: dict,
    *,
    successful: list[str],
    pending: list[str],
    failed: list[str],
    mergeable: bool = True,
    blockers: int = 0,
) -> dict:
    state = deepcopy(pull_request_state(base, draft=False))
    state["checks_observed"] = True
    state["required_check_names"] = sorted(policy["required_check_names"])
    state["successful_check_names"] = sorted(successful)
    state["pending_check_names"] = sorted(pending)
    state["failed_check_names"] = sorted(failed)
    state["mergeable"] = mergeable
    state["unresolved_blocker_count"] = blockers
    return reseal_state(state)


def merge_ready_state(base: dict, policy: dict) -> dict:
    return checks_state(
        base,
        policy,
        successful=list(policy["required_check_names"]),
        pending=[],
        failed=[],
        mergeable=True,
    )


def merged_state(base: dict, policy: dict) -> dict:
    state = deepcopy(merge_ready_state(base, policy))
    state["merge_performed"] = True
    state["merged_head_sha"] = state["local_commit_sha"]
    state["merge_commit_sha"] = MERGE_SHA
    return reseal_state(state)


def bind_source(
    source: dict, request: dict, state: dict, policy: dict
) -> tuple[dict, dict, dict]:
    request = deepcopy(request)
    state = deepcopy(state)
    policy = deepcopy(policy)
    source_digest = source[m.SOURCE_RECEIPT_DIGEST_FIELD]
    for value in (request, state):
        value["source_trajectory_receipt_digest"] = source_digest
        value["repository_full_name"] = source["repository_full_name"]
        value["source_commit_sha"] = source["source_commit_sha"]
    policy["expected_source_trajectory_receipt_digest"] = source_digest
    policy["expected_repository_full_name"] = source["repository_full_name"]
    policy["expected_source_commit_sha"] = source["source_commit_sha"]
    return reseal_request(request), reseal_state(state), reseal_policy(policy)


def route(source: dict, request: dict, state: dict, policy: dict) -> dict:
    result = m.build_codeai_autonomous_git_lifecycle_envelope(
        source_trajectory_receipt=source,
        lifecycle_request=request,
        lifecycle_state=state,
        lifecycle_policy=policy,
    )
    assert result.status == m.STATUS_READY, result
    assert result.issues == (), result
    assert result.receipt is not None, result
    receipt = result.receipt
    assert receipt[m.RECEIPT_DIGEST_FIELD] == m.digest_without(
        receipt, m.RECEIPT_DIGEST_FIELD
    )
    grants = (
        receipt["local_commit_authority_granted"],
        receipt["push_authority_granted"],
        receipt["pull_request_authority_granted"],
        receipt["pull_request_readiness_authority_granted"],
        receipt["merge_authority_granted"],
    )
    assert sum(grants) <= 1
    assert receipt["execution_lease_issued"] is (sum(grants) == 1)
    assert receipt["active_now"] is receipt["execution_lease_issued"]
    assert receipt["effect_execution_performed_by_kernel"] is False
    assert receipt["force_push_performed"] is False
    assert receipt["remote_branch_deleted"] is False
    assert receipt["admin_merge_bypass_used"] is False
    assert receipt["human_handover_performed"] is False
    assert receipt["external_authority_handover_performed"] is False
    assert receipt["deployment_authority_granted"] is False
    assert receipt["deployment_performed"] is False
    assert receipt["secret_access_authority_granted"] is False
    assert receipt["secret_access_performed"] is False
    assert receipt["source_receipt_treated_as_git_authority"] is False
    assert receipt["checks_treated_as_correctness_proof"] is False
    assert receipt["merge_treated_as_truth"] is False
    return receipt


def main() -> None:
    example = load_example()
    source = example["source_trajectory_receipt"]
    request = example["lifecycle_request"]
    state = example["lifecycle_state"]
    policy = example["lifecycle_policy"]

    local = route(source, request, state, policy)
    assert local["codeai_disposition"] == m.DISPOSITION_LOCAL_COMMIT_AUTHORIZED
    assert local["operating_mode"] == m.MODE_LOCAL_GIT_AUTHORIZED
    assert local["next_effect_phase"] == m.PHASE_LOCAL_COMMIT
    assert local["local_commit_authority_granted"] is True

    cases: list[tuple[str, str, str, dict, dict, dict, dict]] = []

    bad_source = reseal_source(changed(source, "trajectory_read_only", False))
    bound_request, bound_state, bound_policy = bind_source(
        bad_source, request, state, policy
    )
    cases.append(
        (
            m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            bad_source,
            bound_request,
            bound_state,
            bound_policy,
        )
    )

    bad_request = reseal_request(
        changed(request, "provenance_integrity_confirmed", False)
    )
    cases.append(
        (
            m.DISPOSITION_REQUEST_PROVENANCE_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            bad_request,
            state,
            policy,
        )
    )

    bad_state = reseal_state(changed(state, "provenance_integrity_confirmed", False))
    cases.append(
        (
            m.DISPOSITION_STATE_EVIDENCE_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            request,
            bad_state,
            policy,
        )
    )

    bad_state = reseal_state(changed(state, "repository_full_name", "other/repo"))
    cases.append(
        (
            m.DISPOSITION_CORRESPONDENCE_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            request,
            bad_state,
            policy,
        )
    )

    bad_state = reseal_state(changed(state, "observed_at_epoch", 5800))
    cases.append(
        (
            m.DISPOSITION_WINDOW_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            request,
            bad_state,
            policy,
        )
    )

    bad_request = reseal_request(
        changed(
            request,
            "prior_execution_session_ids",
            [request["execution_session_id"]],
        )
    )
    cases.append(
        (
            m.DISPOSITION_REPLAY_REJECTED,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            bad_request,
            state,
            policy,
        )
    )

    bad_request = reseal_request(changed(request, "base_branch", "release"))
    bad_state = reseal_state(changed(state, "base_branch", "release"))
    cases.append(
        (
            m.DISPOSITION_SCOPE_ABSTAINED,
            m.MODE_ABSTAIN,
            m.PHASE_NONE,
            source,
            bad_request,
            bad_state,
            policy,
        )
    )

    bad_request = reseal_request(changed(request, "force_push_requested", True))
    cases.append(
        (
            m.DISPOSITION_DESTRUCTIVE_REJECTED,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            bad_request,
            state,
            policy,
        )
    )

    bad_request = reseal_request(changed(request, "human_handover_requested", True))
    cases.append(
        (
            m.DISPOSITION_HANDOVER_DEFERRED,
            m.MODE_HOLD,
            m.PHASE_NONE,
            source,
            bad_request,
            state,
            policy,
        )
    )

    bad_state = reseal_state(changed(state, "branch_pushed", True))
    cases.append(
        (
            m.DISPOSITION_STATE_REPAIR,
            m.MODE_REJECTED,
            m.PHASE_NONE,
            source,
            request,
            bad_state,
            policy,
        )
    )

    committed = committed_state(state)
    cases.append(
        (
            m.DISPOSITION_PUSH_AUTHORIZED,
            m.MODE_REMOTE_GIT_AUTHORIZED,
            m.PHASE_PUSH,
            source,
            request,
            committed,
            policy,
        )
    )

    pushed = pushed_state(state)
    cases.append(
        (
            m.DISPOSITION_PR_AUTHORIZED,
            m.MODE_PR_AUTHORIZED,
            m.PHASE_CREATE_PR,
            source,
            request,
            pushed,
            policy,
        )
    )

    draft = pull_request_state(state, draft=True)
    cases.append(
        (
            m.DISPOSITION_PR_READY_AUTHORIZED,
            m.MODE_PR_AUTHORIZED,
            m.PHASE_MARK_PR_READY,
            source,
            request,
            draft,
            policy,
        )
    )

    ready = pull_request_state(state, draft=False)
    cases.append(
        (
            m.DISPOSITION_CHECKS_PENDING,
            m.MODE_AWAITING_CHECKS,
            m.PHASE_AWAIT_CHECKS,
            source,
            request,
            ready,
            policy,
        )
    )

    required = sorted(policy["required_check_names"])
    pending = checks_state(
        state,
        policy,
        successful=[required[0]],
        pending=[required[1]],
        failed=[],
    )
    cases.append(
        (
            m.DISPOSITION_CHECKS_PENDING,
            m.MODE_AWAITING_CHECKS,
            m.PHASE_AWAIT_CHECKS,
            source,
            request,
            pending,
            policy,
        )
    )

    failed = checks_state(
        state,
        policy,
        successful=[required[0]],
        pending=[],
        failed=[required[1]],
    )
    cases.append(
        (
            m.DISPOSITION_CHECKS_FAILED,
            m.MODE_DEGRADED_AUTONOMY,
            m.PHASE_AWAIT_CHECKS,
            source,
            request,
            failed,
            policy,
        )
    )

    blocked_gate = checks_state(
        state,
        policy,
        successful=required,
        pending=[],
        failed=[],
        mergeable=False,
    )
    cases.append(
        (
            m.DISPOSITION_MERGE_GATE_HOLD,
            m.MODE_HOLD,
            m.PHASE_AWAIT_CHECKS,
            source,
            request,
            blocked_gate,
            policy,
        )
    )

    merge_ready = merge_ready_state(state, policy)
    cases.append(
        (
            m.DISPOSITION_MERGE_AUTHORIZED,
            m.MODE_MERGE_AUTHORIZED,
            m.PHASE_MERGE,
            source,
            request,
            merge_ready,
            policy,
        )
    )

    merged = merged_state(state, policy)
    cases.append(
        (
            m.DISPOSITION_COMPLETED,
            m.MODE_COMPLETED,
            m.PHASE_COMPLETE,
            source,
            request,
            merged,
            policy,
        )
    )

    observed = {m.DISPOSITION_LOCAL_COMMIT_AUTHORIZED}
    for expected_disposition, expected_mode, expected_phase, s, r, st, p in cases:
        receipt = route(s, r, st, p)
        assert receipt["codeai_disposition"] == expected_disposition, receipt
        assert receipt["operating_mode"] == expected_mode, receipt
        assert receipt["next_effect_phase"] == expected_phase, receipt
        observed.add(expected_disposition)

    expected = {
        m.DISPOSITION_LOCAL_COMMIT_AUTHORIZED,
        m.DISPOSITION_PUSH_AUTHORIZED,
        m.DISPOSITION_PR_AUTHORIZED,
        m.DISPOSITION_PR_READY_AUTHORIZED,
        m.DISPOSITION_CHECKS_PENDING,
        m.DISPOSITION_CHECKS_FAILED,
        m.DISPOSITION_MERGE_GATE_HOLD,
        m.DISPOSITION_MERGE_AUTHORIZED,
        m.DISPOSITION_COMPLETED,
        m.DISPOSITION_SOURCE_RECEIPT_REPAIR,
        m.DISPOSITION_REQUEST_PROVENANCE_REPAIR,
        m.DISPOSITION_STATE_EVIDENCE_REPAIR,
        m.DISPOSITION_CORRESPONDENCE_REPAIR,
        m.DISPOSITION_WINDOW_REPAIR,
        m.DISPOSITION_REPLAY_REJECTED,
        m.DISPOSITION_SCOPE_ABSTAINED,
        m.DISPOSITION_DESTRUCTIVE_REJECTED,
        m.DISPOSITION_HANDOVER_DEFERRED,
        m.DISPOSITION_STATE_REPAIR,
    }
    assert observed == expected

    tampered = deepcopy(state)
    tampered["observed_at_epoch"] = 5996
    blocked = m.build_codeai_autonomous_git_lifecycle_envelope(
        source_trajectory_receipt=source,
        lifecycle_request=request,
        lifecycle_state=tampered,
        lifecycle_policy=policy,
    )
    assert blocked.status == m.STATUS_BLOCKED
    assert blocked.receipt is None
    assert "git_lifecycle_state_digest_mismatch" in blocked.issues

    print("CodeAI Autonomous Git Lifecycle v0.1 checks: PASS (19 routes)")


if __name__ == "__main__":
    main()
