#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_github_ci_completion_reentry_v1_1 import (
    compile_completion_event,
    verify_fresh_reobservation,
)
from runtime.kuuos_runtime_remote_ci_merge_candidacy_v7_30 import (
    BASE_RECONCILIATION_REQUIRED,
    CI_BINDING_OBSTRUCTION,
    CI_NON_SUCCESS_REPAIR_REENTRY,
    CI_REOBSERVATION_REQUIRED,
    HEAD_RECONCILIATION_REQUIRED,
    MERGE_CANDIDATE_READY,
    OBSTRUCTED,
    PARTIAL,
    PULL_REQUEST_REBIND_REQUIRED,
    PULL_REQUEST_REQUIRED,
    PULL_REQUEST_REVIEW_STATE_REQUIRED,
    READY,
    build_remote_ci_merge_candidacy,
)


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


REMOTE_COMMIT = "c" * 40
BASE_HEAD = "a" * 40
CANDIDATE_BRANCH = "automation/repair-example"


def source() -> dict:
    return {
        "version": "kuuos_runtime_github_remote_candidate_materialization_v7_29",
        "status": "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_READY",
        "packet_id": "remote-materialization",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "base_branch": "main",
        "candidate_branch": CANDIDATE_BRANCH,
        "materialization_state": "remote_candidate_published_ci_reobservation_required",
        "candidate_retained": True,
        "remote_objects_equivalent": True,
        "git_commit_identity_equal": False,
        "remote_candidate_published": True,
        "remote_base_aligned": True,
        "ci_reobservation_required": True,
        "merge_candidate": False,
        "next_route": "fresh_remote_exact_head_and_ci_reobservation",
        "evidence": {
            "source_post_commit_packet_digest": "1" * 64,
            "source_git_admission_receipt_digest": "2" * 64,
            "local_commit_sha": "b" * 40,
            "local_commit_parent_sha": BASE_HEAD,
            "local_commit_tree_digest": "3" * 64,
            "remote_base_before_sha": BASE_HEAD,
            "remote_base_tree_sha": "d" * 40,
            "remote_base_observation_digest": "4" * 64,
            "remote_object_materialization_receipt_digest": "5" * 64,
            "materialized_entries_digest": "6" * 64,
            "remote_tree_sha": "e" * 40,
            "remote_tree_content_digest": "3" * 64,
            "local_commit_message_digest": "7" * 64,
            "remote_commit_message_digest": "7" * 64,
            "remote_commit_sha": REMOTE_COMMIT,
            "remote_commit_parent_sha": BASE_HEAD,
            "remote_object_observation_digest": "8" * 64,
            "candidate_branch_absent_before": True,
            "candidate_branch_preexisting_head_sha": "",
            "candidate_branch_created": True,
            "post_publish_candidate_branch_head_sha": REMOTE_COMMIT,
            "post_publish_remote_observation_digest": "9" * 64,
            "remote_base_after_sha": BASE_HEAD,
            "commit_presentation_relation": "content_parent_message_equivalent_distinct_git_commit_identity",
            "git_commit_identity_equal": False,
            "remote_objects_equivalent": True,
            "partial_remote_objects_may_exist": False,
            "remote_branch_creation_is_base_branch_mutation": False,
            "remote_publish_receipt_is_merge_authority": False,
            "remote_publish_receipt_is_ci_success": False,
            "raw_source_bytes_persisted": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def verified_ci(
    workflow: str,
    *,
    head: str = REMOTE_COMMIT,
    conclusion: str = "success",
) -> dict:
    event = {
        "action": "completed",
        "repository": {"full_name": "itakura-hidetoshi/KuuOS"},
        "workflow_run": {
            "id": 1000 + sum(ord(ch) for ch in workflow),
            "name": workflow,
            "head_sha": head,
            "head_branch": CANDIDATE_BRANCH,
            "status": "completed",
            "conclusion": conclusion,
            "event": "pull_request",
        },
    }
    compiled = compile_completion_event(
        event,
        event_name="workflow_run",
        repository_allowlist=["itakura-hidetoshi/KuuOS"],
        workflow_allowlist=[workflow],
    )
    packet = compiled["event_packet"]
    verification = verify_fresh_reobservation(
        packet,
        observed_run={
            "repository": "itakura-hidetoshi/KuuOS",
            "id": event["workflow_run"]["id"],
            "name": workflow,
            "head_sha": head,
            "status": "completed",
            "conclusion": conclusion,
        },
        observed_jobs=[
            {
                "name": "validate",
                "status": "completed",
                "conclusion": conclusion,
                "steps": [
                    {
                        "name": "Run selected check",
                        "status": "completed",
                        "conclusion": conclusion,
                    }
                ],
            }
        ],
    )
    assert verification["status"] == "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"
    return verification


def observation(
    src: dict,
    *,
    candidate_head: str = REMOTE_COMMIT,
    base_head: str = BASE_HEAD,
    pr_exists: bool = True,
    pr_draft: bool = False,
    pr_head: str | None = None,
    pr_base: str | None = None,
    required: list[str] | None = None,
    ci: list[dict] | None = None,
) -> dict:
    if pr_head is None:
        pr_head = candidate_head
    if pr_base is None:
        pr_base = base_head
    if required is None:
        required = ["Runtime", "Governance"]
    if ci is None:
        ci = [verified_ci(name, head=candidate_head) for name in required]
    return {
        "version": "kuuos_remote_ci_merge_candidacy_observation_v7_30",
        "source_materialization_packet_digest": h(src),
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "candidate_branch": CANDIDATE_BRANCH,
        "base_branch": "main",
        "candidate_branch_head_sha": candidate_head,
        "candidate_branch_observation_digest": "a" * 64,
        "base_branch_head_sha": base_head,
        "base_branch_observation_digest": "b" * 64,
        "pull_request_exists": pr_exists,
        "pull_request_number": 2001 if pr_exists else 0,
        "pull_request_state": "open" if pr_exists else "",
        "pull_request_draft": pr_draft if pr_exists else False,
        "pull_request_head_branch": CANDIDATE_BRANCH if pr_exists else "",
        "pull_request_head_sha": pr_head if pr_exists else "",
        "pull_request_base_branch": "main" if pr_exists else "",
        "pull_request_base_sha": pr_base if pr_exists else "",
        "pull_request_observation_digest": "c" * 64 if pr_exists else "",
        "required_workflow_names": required,
        "ci_verifications": ci,
    }


def test_exact_pr_and_fresh_successful_ci_form_merge_candidate_without_authority() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src),
    )
    assert result.status == READY, result.to_dict()
    assert result.candidacy_state == MERGE_CANDIDATE_READY
    assert result.pull_request_bound is True
    assert result.required_ci_complete is True
    assert result.required_ci_success is True
    assert result.merge_candidate is True
    assert result.merge_authority_granted is False
    assert result.next_route == (
        "acquire_explicit_merge_authority_then_expected_head_merge"
    )
    assert result.evidence["merge_authority_derived_from_ci"] is False
    assert result.evidence["ci_event_alone_is_success_evidence"] is False


def test_candidate_head_move_retains_candidate_for_reconciliation() -> None:
    src = source()
    moved = "d" * 40
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(
            src,
            candidate_head=moved,
            ci=[
                verified_ci("Runtime", head=moved),
                verified_ci("Governance", head=moved),
            ],
        ),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == HEAD_RECONCILIATION_REQUIRED
    assert result.candidate_retained is True
    assert result.merge_candidate is False


def test_base_move_retains_candidate_for_reconciliation() -> None:
    src = source()
    moved = "d" * 40
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src, base_head=moved, pr_base=moved),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == BASE_RECONCILIATION_REQUIRED
    assert result.candidate_retained is True


def test_missing_pull_request_keeps_published_candidate() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src, pr_exists=False),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == PULL_REQUEST_REQUIRED
    assert result.candidate_retained is True


def test_pr_head_mismatch_routes_to_pr_rebinding() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src, pr_head="d" * 40),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == PULL_REQUEST_REBIND_REQUIRED
    assert result.merge_candidate is False


def test_draft_pr_is_not_merge_candidate_but_is_not_rejected() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src, pr_draft=True),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == PULL_REQUEST_REVIEW_STATE_REQUIRED
    assert result.candidate_retained is True
    assert result.merge_candidate is False


def test_missing_required_ci_requests_reobservation() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(
            src,
            required=["Runtime", "Governance"],
            ci=[verified_ci("Runtime")],
        ),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == CI_REOBSERVATION_REQUIRED
    assert result.required_ci_complete is False
    assert result.merge_candidate is False
    assert any(
        warning.startswith("required_ci_verification_missing:")
        for warning in result.warnings
    )


def test_verified_non_success_reenters_repair_without_discarding_remote_candidate() -> None:
    src = source()
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(
            src,
            ci=[
                verified_ci("Runtime", conclusion="failure"),
                verified_ci("Governance"),
            ],
        ),
    )
    assert result.status == PARTIAL
    assert result.candidacy_state == CI_NON_SUCCESS_REPAIR_REENTRY
    assert result.candidate_retained is True
    assert result.required_ci_complete is True
    assert result.required_ci_success is False
    assert result.merge_candidate is False


def test_stale_ci_head_is_true_evidence_binding_obstruction() -> None:
    src = source()
    stale = verified_ci("Runtime", head="d" * 40)
    good = verified_ci("Governance")
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(src, ci=[stale, good]),
    )
    assert result.status == OBSTRUCTED, result.to_dict()
    assert result.candidacy_state == CI_BINDING_OBSTRUCTION
    assert "ci_head_sha_mismatch:Runtime" in result.blockers
    assert result.merge_candidate is False


def test_ci_packet_cannot_grant_merge_authority() -> None:
    src = source()
    forged = verified_ci("Runtime")
    forged["merge_authority_granted"] = True
    result = build_remote_ci_merge_candidacy(
        materialization_packet=src,
        observation=observation(
            src,
            required=["Runtime"],
            ci=[forged],
        ),
    )
    assert result.status == OBSTRUCTED
    assert result.candidacy_state == CI_BINDING_OBSTRUCTION
    assert "ci_must_not_grant_merge_authority:Runtime" in result.blockers
    assert result.merge_authority_granted is False


def main() -> int:
    test_exact_pr_and_fresh_successful_ci_form_merge_candidate_without_authority()
    test_candidate_head_move_retains_candidate_for_reconciliation()
    test_base_move_retains_candidate_for_reconciliation()
    test_missing_pull_request_keeps_published_candidate()
    test_pr_head_mismatch_routes_to_pr_rebinding()
    test_draft_pr_is_not_merge_candidate_but_is_not_rejected()
    test_missing_required_ci_requests_reobservation()
    test_verified_non_success_reenters_repair_without_discarding_remote_candidate()
    test_stale_ci_head_is_true_evidence_binding_obstruction()
    test_ci_packet_cannot_grant_merge_authority()
    print("PASS: KuuOS Remote CI Merge Candidacy v7.30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
