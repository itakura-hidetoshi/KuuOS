#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_github_mcp_server_bridge_v0_1 import MockGitHubMCPTransport
from runtime.kuuos_github_mcp_server_bridge_v0_2 import build_github_mcp_write_bridge
from runtime.kuuos_github_ci_completion_reentry_v1_1 import (
    compile_completion_event,
    verify_fresh_reobservation,
)
from runtime.kuuos_runtime_expected_head_merge_closure_v7_31 import (
    LINEAGE_CLOSED,
    MERGE_AUTHORITY_BINDING_OBSTRUCTION,
    MERGE_AUTHORITY_REQUIRED,
    MERGE_NOT_APPLIED,
    MERGE_RECEIPT_OBSTRUCTION,
    MERGE_RECEIPT_REQUIRED,
    OBSTRUCTED,
    PARTIAL,
    POST_MERGE_CI_BINDING_OBSTRUCTION,
    POST_MERGE_CI_NON_SUCCESS,
    POST_MERGE_CI_REOBSERVATION,
    POST_MERGE_MAIN_ADVANCED,
    POST_MERGE_REOBSERVATION,
    PRE_MERGE_RECONCILIATION,
    READY,
    build_expected_head_merge_closure,
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


HEAD = "c" * 40
BASE = "a" * 40
MERGE = "d" * 40


def source() -> dict:
    return {
        "version": "kuuos_runtime_remote_ci_merge_candidacy_v7_30",
        "status": "KUUOS_REMOTE_CI_MERGE_CANDIDACY_READY",
        "packet_id": "merge-candidate",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "candidate_branch": "automation/repair-example",
        "candidate_head_sha": HEAD,
        "base_branch": "main",
        "base_head_sha": BASE,
        "candidacy_state": "merge_candidate_ready_explicit_merge_authority_required",
        "candidate_retained": True,
        "pull_request_bound": True,
        "required_ci_complete": True,
        "required_ci_success": True,
        "merge_candidate": True,
        "merge_authority_granted": False,
        "next_route": "acquire_explicit_merge_authority_then_expected_head_merge",
        "evidence": {
            "source_materialization_packet_digest": "1" * 64,
            "source_remote_commit_sha": HEAD,
            "source_remote_base_sha": BASE,
            "candidate_branch_head_sha": HEAD,
            "candidate_branch_observation_digest": "2" * 64,
            "base_branch_head_sha": BASE,
            "base_branch_observation_digest": "3" * 64,
            "pull_request_number": 2001,
            "pull_request_observation_digest": "4" * 64,
            "required_workflow_names_digest": "5" * 64,
            "ci_verification_packets_digest": "6" * 64,
            "candidate_head_exact": True,
            "base_head_exact": True,
            "pull_request_bound": True,
            "required_ci_complete": True,
            "required_ci_success": True,
            "merge_authority_derived_from_ci": False,
            "write_authority_derived_from_ci": False,
            "merge_candidate_executes_merge": False,
            "ci_event_alone_is_success_evidence": False,
            "fresh_mcp_ci_reobservation_required": True,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def authority(src: dict, **overrides) -> dict:
    value = {
        "version": "kuuos_expected_head_merge_authority_v7_31",
        "status": "KUUOS_EXPECTED_HEAD_MERGE_AUTHORITY_READY",
        "merge_authority_granted": True,
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "pull_request_number": 2001,
        "expected_head_sha": HEAD,
        "expected_base_sha": BASE,
        "merge_method": "merge",
        "authority_scope_digest": "f" * 64,
        "source_merge_candidate_packet_digest": h(src),
    }
    value.update(overrides)
    return value


def _tool(name: str, read_only: bool) -> dict:
    return {
        "name": name,
        "description": name,
        "inputSchema": {"type": "object"},
        "annotations": {"readOnlyHint": read_only},
    }


def bridge_result() -> tuple[object, dict]:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        plan = {
            "version": "kuuos_github_mcp_server_bridge_plan_v0_2",
            "mode": "mock",
            "repository_full_name": "itakura-hidetoshi/KuuOS",
            "base_branch": "main",
            "base_sha": BASE,
            "write_capable": True,
            "read_only": False,
            "lockdown_mode": True,
            "execute_external_actions": True,
            "server": {
                "kind": "official_github_mcp_server",
                "launcher": "docker",
                "image": "ghcr.io/github/github-mcp-server",
                "token_env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                "toolsets": ["context", "repos", "pull_requests"],
                "tools": ["issue_read"],
            },
            "operations": [
                {
                    "kind": "exact_git_action",
                    "approved": True,
                    "expected_base_sha": BASE,
                    "action": {
                        "kind": "merge_pr",
                        "repository_full_name": "itakura-hidetoshi/KuuOS",
                        "base_branch": "main",
                        "pr_number": 2001,
                        "merge_method": "merge",
                        "expected_base_sha": BASE,
                        "expected_head_sha": HEAD,
                    },
                }
            ],
        }
        write_authority = {
            "authority_status": "KUUOS_GITHUB_MCP_WRITE_AUTHORITY_READY",
            "plan_read_allowed": True,
            "tool_discovery_allowed": True,
            "receipt_write_allowed": True,
            "audit_append_allowed": True,
            "external_action_allowed": True,
            "mcp_write_tool_call_allowed": True,
            "exact_git_delegation_allowed": True,
        }
        (root / "github_mcp_server_bridge_plan_v0_2.json").write_text(
            json.dumps(plan), encoding="utf-8"
        )

        def qi_transport(repository, action, token):
            assert repository == "itakura-hidetoshi/KuuOS"
            assert action["kind"] == "merge_pr"
            assert action["pr_number"] == 2001
            assert action["expected_head_sha"] == HEAD
            assert action["expected_base_sha"] == BASE
            return {
                "merged": True,
                "sha": MERGE,
                "message": "mock expected-head merge",
            }

        result = build_github_mcp_write_bridge(
            runtime_context={
                "runtime_root": str(root),
                "github_mcp_server_bridge_enabled": True,
                "apply_github_mcp_server_bridge": True,
                "execute_external_actions": True,
            },
            authority_packet=write_authority,
            transport=MockGitHubMCPTransport([_tool("issue_read", True)]),
            qi_transport=qi_transport,
        )
        receipt = json.loads(
            (root / "github_mcp_server_bridge_receipt_v0_2.json").read_text(
                encoding="utf-8"
            )
        )
        return result, receipt


def verified_ci(
    workflow: str,
    *,
    head: str = MERGE,
    conclusion: str = "success",
) -> dict:
    event = {
        "action": "completed",
        "repository": {"full_name": "itakura-hidetoshi/KuuOS"},
        "workflow_run": {
            "id": 3000 + sum(ord(ch) for ch in workflow),
            "name": workflow,
            "head_sha": head,
            "head_branch": "main",
            "status": "completed",
            "conclusion": conclusion,
            "event": "push",
        },
    }
    compiled = compile_completion_event(
        event,
        event_name="workflow_run",
        repository_allowlist=["itakura-hidetoshi/KuuOS"],
        workflow_allowlist=[workflow],
    )
    result = verify_fresh_reobservation(
        compiled["event_packet"],
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
                        "name": "check",
                        "status": "completed",
                        "conclusion": conclusion,
                    }
                ],
            }
        ],
    )
    assert result["status"] == "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"
    return result


def observation(
    src: dict,
    *,
    pre_head: str = HEAD,
    pre_base: str = BASE,
    attempted: bool = True,
    bridge_status: str = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED",
    applied_count: int = 1,
    expected_head: str = HEAD,
    expected_base: str = BASE,
    merged: bool = True,
    merge_sha: str = MERGE,
    post_main: str | None = MERGE,
    post_pr_merged: bool = True,
    post_pr_merge_sha: str | None = MERGE,
    include_post_observation: bool = True,
    required: list[str] | None = None,
    ci: list[dict] | None = None,
) -> dict:
    if required is None:
        required = ["PostMerge Runtime"]
    if ci is None:
        ci = [verified_ci(name, head=merge_sha) for name in required] if merged else []
    return {
        "version": "kuuos_expected_head_merge_closure_observation_v7_31",
        "source_merge_candidate_packet_digest": h(src),
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "pre_merge_pr_head_sha": pre_head,
        "pre_merge_base_head_sha": pre_base,
        "pre_merge_observation_digest": "7" * 64,
        "merge_attempted": attempted,
        "github_mcp_bridge_status": bridge_status if attempted else "",
        "github_mcp_bridge_receipt_digest": "8" * 64 if attempted else "",
        "github_mcp_bridge_delegated_applied_count": applied_count if attempted else 0,
        "merge_action_kind": "merge_pr" if attempted else "",
        "merge_pr_number": 2001 if attempted else 0,
        "merge_expected_head_sha": expected_head if attempted else "",
        "merge_expected_base_sha": expected_base if attempted else "",
        "merge_method": "merge" if attempted else "",
        "merge_result_merged": merged if attempted else False,
        "merge_result_sha": merge_sha if attempted and merged else "",
        "merge_result_message_digest": "9" * 64 if attempted else "",
        "post_merge_main_head_sha": (
            post_main if merged and include_post_observation and post_main else ""
        ),
        "post_merge_main_observation_digest": (
            "a" * 64 if merged and include_post_observation and post_main else ""
        ),
        "post_merge_pr_merged": (
            post_pr_merged if merged and include_post_observation else False
        ),
        "post_merge_pr_merge_commit_sha": (
            post_pr_merge_sha
            if merged and include_post_observation and post_pr_merge_sha
            else ""
        ),
        "post_merge_pr_observation_digest": (
            "b" * 64 if merged and include_post_observation else ""
        ),
        "post_merge_required_workflow_names": required if merged else [],
        "post_merge_ci_verifications": ci if merged else [],
    }


def test_successful_expected_head_merge_and_post_merge_ci_closes_lineage() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(src),
    )
    assert result.status == READY, result.to_dict()
    assert result.closure_state == LINEAGE_CLOSED
    assert result.merge_applied is True
    assert result.post_merge_main_exact is True
    assert result.post_merge_pr_exact is True
    assert result.post_merge_ci_complete is True
    assert result.post_merge_ci_success is True
    assert result.development_lineage_closed is True
    assert result.next_route == "development_lineage_closed"
    assert result.evidence["merge_candidate_was_merge_authority"] is False
    assert result.evidence["ci_success_was_merge_authority"] is False


def test_missing_merge_authority_retains_candidate() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        observation=observation(
            src,
            attempted=False,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == MERGE_AUTHORITY_REQUIRED
    assert result.candidate_retained is True
    assert result.merge_applied is False


def test_pre_merge_head_move_requires_reconciliation() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            pre_head="e" * 40,
            attempted=False,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == PRE_MERGE_RECONCILIATION
    assert result.candidate_retained is True


def test_authorized_candidate_without_merge_requests_receipt() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            attempted=False,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == MERGE_RECEIPT_REQUIRED


def test_bridge_non_applied_merge_is_partial_not_false_success() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            bridge_status="KUUOS_GITHUB_MCP_WRITE_BRIDGE_PARTIAL",
            applied_count=0,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == MERGE_NOT_APPLIED
    assert result.merge_applied is False
    assert result.development_lineage_closed is False


def test_wrong_expected_head_in_merge_receipt_is_obstruction() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            expected_head="e" * 40,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == OBSTRUCTED
    assert result.closure_state == MERGE_RECEIPT_OBSTRUCTION
    assert "merge_expected_head_source_mismatch" in result.blockers


def test_successful_merge_without_post_observation_requests_reobservation() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.closure_state == POST_MERGE_REOBSERVATION
    assert result.merge_applied is True
    assert result.development_lineage_closed is False


def test_main_advancing_after_successful_merge_does_not_erase_merge_fact() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(src, post_main="e" * 40),
    )
    assert result.status == PARTIAL
    assert result.closure_state == POST_MERGE_MAIN_ADVANCED
    assert result.merge_applied is True
    assert result.candidate_retained is True


def test_missing_post_merge_ci_requests_reobservation() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            required=["PostMerge Runtime", "PostMerge Governance"],
            ci=[verified_ci("PostMerge Runtime")],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == POST_MERGE_CI_REOBSERVATION
    assert result.merge_applied is True
    assert result.post_merge_ci_complete is False


def test_post_merge_ci_failure_requires_followup_without_automatic_rollback() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            ci=[verified_ci("PostMerge Runtime", conclusion="failure")],
        ),
    )
    assert result.status == PARTIAL
    assert result.closure_state == POST_MERGE_CI_NON_SUCCESS
    assert result.merge_applied is True
    assert result.post_merge_ci_success is False
    assert result.evidence["post_merge_ci_failure_implies_automatic_rollback"] is False


def test_stale_post_merge_ci_head_is_binding_obstruction() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=observation(
            src,
            ci=[verified_ci("PostMerge Runtime", head="e" * 40)],
        ),
    )
    assert result.status == OBSTRUCTED
    assert result.closure_state == POST_MERGE_CI_BINDING_OBSTRUCTION
    assert "post_merge_ci_head_mismatch:PostMerge Runtime" in result.blockers


def test_mismatched_explicit_merge_authority_is_true_binding_obstruction() -> None:
    src = source()
    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(
            src,
            expected_head_sha="e" * 40,
        ),
        observation=observation(
            src,
            attempted=False,
            merged=False,
            include_post_observation=False,
            required=[],
            ci=[],
        ),
    )
    assert result.status == OBSTRUCTED
    assert result.closure_state == MERGE_AUTHORITY_BINDING_OBSTRUCTION
    assert "merge_authority_expected_head_mismatch" in result.blockers
    assert result.candidate_retained is True


def test_existing_github_mcp_bridge_exact_merge_receipt_closes_with_post_merge_evidence() -> None:
    src = source()
    bridge, receipt = bridge_result()
    assert bridge.status == "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED"
    assert bridge.delegated_applied_count == 1
    assert bridge.blocked_count == 0
    assert bridge.records[0]["execution_path"] == "exact_sha_rest_delegate"
    assert bridge.records[0]["result"]["merged"] is True
    assert bridge.records[0]["result"]["sha"] == MERGE

    obs = observation(src)
    obs["github_mcp_bridge_status"] = bridge.status
    obs["github_mcp_bridge_receipt_digest"] = h(receipt)
    obs["github_mcp_bridge_delegated_applied_count"] = bridge.delegated_applied_count
    obs["merge_result_merged"] = bridge.records[0]["result"]["merged"]
    obs["merge_result_sha"] = bridge.records[0]["result"]["sha"]

    result = build_expected_head_merge_closure(
        merge_candidate_packet=src,
        merge_authority_packet=authority(src),
        observation=obs,
    )
    assert result.status == READY, result.to_dict()
    assert result.closure_state == LINEAGE_CLOSED
    assert result.merge_applied is True
    assert result.development_lineage_closed is True
    assert result.evidence["merge_authority_independently_supplied"] is True
    assert result.evidence["merge_authority_derived_from_ci"] is False
    assert result.evidence["merge_authority_derived_from_candidacy"] is False


def main() -> int:
    test_successful_expected_head_merge_and_post_merge_ci_closes_lineage()
    test_missing_merge_authority_retains_candidate()
    test_pre_merge_head_move_requires_reconciliation()
    test_authorized_candidate_without_merge_requests_receipt()
    test_bridge_non_applied_merge_is_partial_not_false_success()
    test_wrong_expected_head_in_merge_receipt_is_obstruction()
    test_successful_merge_without_post_observation_requests_reobservation()
    test_main_advancing_after_successful_merge_does_not_erase_merge_fact()
    test_missing_post_merge_ci_requests_reobservation()
    test_post_merge_ci_failure_requires_followup_without_automatic_rollback()
    test_stale_post_merge_ci_head_is_binding_obstruction()
    test_mismatched_explicit_merge_authority_is_true_binding_obstruction()
    test_existing_github_mcp_bridge_exact_merge_receipt_closes_with_post_merge_evidence()
    print("PASS: KuuOS Expected-Head Merge Closure v7.31")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
