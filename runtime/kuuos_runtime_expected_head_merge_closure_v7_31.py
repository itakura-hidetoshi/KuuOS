#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_expected_head_merge_closure_v7_31"
SOURCE_VERSION = "kuuos_runtime_remote_ci_merge_candidacy_v7_30"
OBSERVATION_VERSION = "kuuos_expected_head_merge_closure_observation_v7_31"
CI_VERSION = "kuuos_github_ci_completion_reentry_v1_1"
CI_VERIFIED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"
BRIDGE_APPLIED = "KUUOS_GITHUB_MCP_WRITE_BRIDGE_APPLIED"

READY = "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_READY"
PARTIAL = "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_PARTIAL"
OBSTRUCTED = "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_NOT_APPLICABLE"

MERGE_AUTHORITY_REQUIRED = "merge_authority_required"
PRE_MERGE_RECONCILIATION = "pre_merge_revision_reconciliation_required"
MERGE_RECEIPT_REQUIRED = "expected_head_merge_receipt_required"
MERGE_NOT_APPLIED = "expected_head_merge_not_applied_reobservation_required"
MERGE_RECEIPT_OBSTRUCTION = "expected_head_merge_receipt_obstruction"
POST_MERGE_REOBSERVATION = "post_merge_main_pr_reobservation_required"
POST_MERGE_MAIN_ADVANCED = "post_merge_main_advanced_reconciliation_required"
POST_MERGE_CI_REOBSERVATION = "post_merge_ci_reobservation_required"
POST_MERGE_CI_NON_SUCCESS = "post_merge_ci_non_success_followup_required"
POST_MERGE_CI_BINDING_OBSTRUCTION = "post_merge_ci_binding_obstruction"
LINEAGE_CLOSED = "development_lineage_closed"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class ExpectedHeadMergeClosureResult:
    version: str
    status: str
    packet_id: str
    repository_full_name: str
    pull_request_number: int
    expected_head_sha: str
    expected_base_sha: str
    closure_state: str
    candidate_retained: bool
    merge_applied: bool
    merge_commit_sha: str
    post_merge_main_exact: bool
    post_merge_pr_exact: bool
    post_merge_ci_complete: bool
    post_merge_ci_success: bool
    development_lineage_closed: bool
    next_route: str
    evidence: dict[str, Any]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def _digest(value: Any, name: str, blockers: list[str], *, optional: bool = False) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _commit(value: Any, name: str, blockers: list[str], *, optional: bool = False) -> str:
    text = str(value or "").strip().lower()
    if optional and not text:
        return ""
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _bool(value: Any, name: str, blockers: list[str]) -> bool:
    if not isinstance(value, bool):
        blockers.append(name + "_must_be_bool")
        return False
    return value


def _positive_int(value: Any, name: str, blockers: list[str], *, optional: bool = False) -> int:
    if optional and value in (None, "", 0):
        return 0
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        blockers.append(name + "_invalid")
        return 0
    return value


def _names(value: Any, blockers: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        blockers.append("post_merge_required_workflow_names_missing")
        return []
    names = [str(item).strip() for item in value if str(item).strip()]
    if len(names) != len(value) or len(names) != len(set(names)):
        blockers.append("post_merge_required_workflow_names_invalid")
    return names


def _post_merge_ci(
    value: Any,
    *,
    repository: str,
    merge_commit_sha: str,
    required_names: list[str],
) -> tuple[dict[str, dict[str, Any]], list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    if not isinstance(value, list):
        return {}, ["post_merge_ci_verifications_not_list"], warnings

    packets: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(value):
        if not isinstance(raw, Mapping):
            blockers.append(f"post_merge_ci_{index}_not_object")
            continue
        packet = dict(raw)
        workflow = str(packet.get("workflow_name", "")).strip()
        if not workflow:
            blockers.append(f"post_merge_ci_{index}_workflow_missing")
            continue
        if workflow in packets:
            blockers.append("duplicate_post_merge_ci_workflow:" + workflow)
            continue
        packets[workflow] = packet

        if packet.get("version") != CI_VERSION:
            blockers.append("post_merge_ci_version_invalid:" + workflow)
        if packet.get("status") != CI_VERIFIED:
            blockers.append("post_merge_ci_not_verified:" + workflow)
        if str(packet.get("repository", "")) != repository:
            blockers.append("post_merge_ci_repository_mismatch:" + workflow)
        if str(packet.get("head_sha", "")).lower() != merge_commit_sha:
            blockers.append("post_merge_ci_head_mismatch:" + workflow)
        if packet.get("fresh_mcp_reobservation") is not True:
            blockers.append("post_merge_ci_fresh_observation_missing:" + workflow)
        if packet.get("merge_authority_granted") is not False:
            blockers.append("post_merge_ci_must_not_grant_merge_authority:" + workflow)
        if packet.get("write_authority_granted") is not False:
            blockers.append("post_merge_ci_must_not_grant_write_authority:" + workflow)
        _digest(
            packet.get("evidence_digest"),
            f"post_merge_ci_{index}_evidence_digest",
            blockers,
        )
        route = str(packet.get("route", ""))
        if route not in {"verified_success", "verified_non_success"}:
            blockers.append("post_merge_ci_route_invalid:" + workflow)
        elif route == "verified_non_success":
            warnings.append("post_merge_ci_verified_non_success:" + workflow)

    missing = [name for name in required_names if name not in packets]
    if missing:
        warnings.append("post_merge_required_ci_missing:" + ",".join(missing))
    extras = [name for name in packets if name not in required_names]
    if extras:
        warnings.append("post_merge_extra_ci_ignored:" + ",".join(sorted(extras)))
    return packets, blockers, warnings


def build_expected_head_merge_closure(
    *,
    merge_candidate_packet: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> ExpectedHeadMergeClosureResult:
    source = _m(merge_candidate_packet)
    obs = _m(observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if source.get("version") != SOURCE_VERSION:
        blockers.append("merge_candidate_packet_version_invalid")
    if obs.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")

    source_digest = _sha(source)
    if _digest(
        obs.get("source_merge_candidate_packet_digest"),
        "source_merge_candidate_packet_digest",
        blockers,
    ) != source_digest:
        blockers.append("source_merge_candidate_packet_digest_mismatch")

    repository = str(obs.get("repository_full_name", "")).strip()
    if repository != "itakura-hidetoshi/KuuOS":
        blockers.append("repository_full_name_invalid")

    source_ready = bool(
        source.get("status") == "KUUOS_REMOTE_CI_MERGE_CANDIDACY_READY"
        and source.get("candidacy_state")
        == "merge_candidate_ready_explicit_merge_authority_required"
        and source.get("merge_candidate") is True
        and source.get("merge_authority_granted") is False
    )

    expected_head = _commit(
        source.get("candidate_head_sha"),
        "source_expected_head_sha",
        blockers,
        optional=not source_ready,
    )
    expected_base = _commit(
        source.get("base_head_sha"),
        "source_expected_base_sha",
        blockers,
        optional=not source_ready,
    )
    source_evidence = _m(source.get("evidence"))
    pr_number = _positive_int(
        source_evidence.get("pull_request_number"),
        "source_pull_request_number",
        blockers,
        optional=not source_ready,
    )

    if not source_ready:
        packet_id = "kuuos-expected-head-merge-closure-" + _sha(
            {
                "source_digest": source_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return ExpectedHeadMergeClosureResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            repository,
            pr_number,
            expected_head,
            expected_base,
            "merge_candidate_packet_not_ready",
            True,
            False,
            "",
            False,
            False,
            False,
            False,
            False,
            "return_to_v7_30_remote_ci_merge_candidacy",
            {
                "source_merge_candidate_packet_digest": source_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    merge_authority_ready = _bool(
        obs.get("merge_authority_ready"),
        "merge_authority_ready",
        blockers,
    )
    pre_merge_head = _commit(
        obs.get("pre_merge_pr_head_sha"),
        "pre_merge_pr_head_sha",
        blockers,
    )
    pre_merge_base = _commit(
        obs.get("pre_merge_base_head_sha"),
        "pre_merge_base_head_sha",
        blockers,
    )
    pre_merge_observation_digest = _digest(
        obs.get("pre_merge_observation_digest"),
        "pre_merge_observation_digest",
        blockers,
    )

    merge_attempted = _bool(
        obs.get("merge_attempted"),
        "merge_attempted",
        blockers,
    )
    bridge_status = str(obs.get("github_mcp_bridge_status", "")).strip()
    bridge_receipt_digest = _digest(
        obs.get("github_mcp_bridge_receipt_digest"),
        "github_mcp_bridge_receipt_digest",
        blockers,
        optional=not merge_attempted,
    )
    bridge_applied_count = obs.get("github_mcp_bridge_delegated_applied_count", 0)
    if (
        isinstance(bridge_applied_count, bool)
        or not isinstance(bridge_applied_count, int)
        or bridge_applied_count < 0
    ):
        blockers.append("github_mcp_bridge_delegated_applied_count_invalid")
        bridge_applied_count = 0

    merge_action_kind = str(obs.get("merge_action_kind", "")).strip()
    merge_pr_number = _positive_int(
        obs.get("merge_pr_number"),
        "merge_pr_number",
        blockers,
        optional=not merge_attempted,
    )
    merge_expected_head = _commit(
        obs.get("merge_expected_head_sha"),
        "merge_expected_head_sha",
        blockers,
        optional=not merge_attempted,
    )
    merge_expected_base = _commit(
        obs.get("merge_expected_base_sha"),
        "merge_expected_base_sha",
        blockers,
        optional=not merge_attempted,
    )
    merge_method = str(obs.get("merge_method", "")).strip()
    if merge_attempted and merge_method not in {"merge", "squash", "rebase"}:
        blockers.append("merge_method_invalid")

    merge_result_merged = _bool(
        obs.get("merge_result_merged"),
        "merge_result_merged",
        blockers,
    )
    merge_commit_sha = _commit(
        obs.get("merge_result_sha"),
        "merge_result_sha",
        blockers,
        optional=not merge_result_merged,
    )
    merge_result_message_digest = _digest(
        obs.get("merge_result_message_digest"),
        "merge_result_message_digest",
        blockers,
        optional=not merge_attempted,
    )

    if merge_attempted:
        if merge_action_kind != "merge_pr":
            blockers.append("merge_action_kind_invalid")
        if merge_pr_number != pr_number:
            blockers.append("merge_pr_number_source_mismatch")
        if merge_expected_head != expected_head:
            blockers.append("merge_expected_head_source_mismatch")
        if merge_expected_base != expected_base:
            blockers.append("merge_expected_base_source_mismatch")

    merge_applied = bool(
        merge_attempted
        and bridge_status == BRIDGE_APPLIED
        and bridge_applied_count == 1
        and merge_result_merged
        and merge_commit_sha
        and bridge_receipt_digest
        and not blockers
    )

    post_main_head = _commit(
        obs.get("post_merge_main_head_sha"),
        "post_merge_main_head_sha",
        blockers,
        optional=not merge_applied,
    )
    post_main_observation_digest = _digest(
        obs.get("post_merge_main_observation_digest"),
        "post_merge_main_observation_digest",
        blockers,
        optional=not merge_applied,
    )
    post_pr_merged = _bool(
        obs.get("post_merge_pr_merged"),
        "post_merge_pr_merged",
        blockers,
    )
    post_pr_merge_sha = _commit(
        obs.get("post_merge_pr_merge_commit_sha"),
        "post_merge_pr_merge_commit_sha",
        blockers,
        optional=not post_pr_merged,
    )
    post_pr_observation_digest = _digest(
        obs.get("post_merge_pr_observation_digest"),
        "post_merge_pr_observation_digest",
        blockers,
        optional=not merge_applied,
    )

    post_main_exact = bool(
        merge_applied
        and post_main_head == merge_commit_sha
        and post_main_observation_digest
    )
    post_pr_exact = bool(
        merge_applied
        and post_pr_merged
        and post_pr_merge_sha == merge_commit_sha
        and post_pr_observation_digest
    )

    required_names = _names(
        obs.get("post_merge_required_workflow_names"),
        blockers,
    )
    ci_packets, ci_blockers, ci_warnings = _post_merge_ci(
        obs.get("post_merge_ci_verifications"),
        repository=repository,
        merge_commit_sha=merge_commit_sha,
        required_names=required_names,
    )
    blockers.extend(ci_blockers)
    warnings.extend(ci_warnings)

    post_ci_complete = bool(
        merge_commit_sha
        and required_names
        and all(name in ci_packets for name in required_names)
    )
    post_ci_success = bool(
        post_ci_complete
        and all(
            ci_packets[name].get("status") == CI_VERIFIED
            and ci_packets[name].get("route") == "verified_success"
            and str(ci_packets[name].get("head_sha", "")).lower()
            == merge_commit_sha
            for name in required_names
        )
    )
    post_ci_non_success = bool(
        post_ci_complete
        and any(
            ci_packets[name].get("route") == "verified_non_success"
            for name in required_names
        )
    )
    ci_binding_blockers = [
        item for item in blockers if item.startswith("post_merge_ci_")
    ]

    if not merge_authority_ready:
        state = MERGE_AUTHORITY_REQUIRED
        status = PARTIAL
        next_route = "retain_merge_candidate_and_acquire_explicit_merge_authority"
    elif pre_merge_head != expected_head or pre_merge_base != expected_base:
        state = PRE_MERGE_RECONCILIATION
        status = PARTIAL
        next_route = "freshly_revalidate_v7_30_candidacy_before_merge"
    elif not merge_attempted:
        state = MERGE_RECEIPT_REQUIRED
        status = PARTIAL
        next_route = "perform_expected_head_merge_through_existing_github_mcp_bridge"
    elif blockers:
        state = (
            POST_MERGE_CI_BINDING_OBSTRUCTION
            if ci_binding_blockers and merge_applied
            else MERGE_RECEIPT_OBSTRUCTION
        )
        status = OBSTRUCTED
        next_route = (
            "discard_stale_post_merge_ci_binding_and_reobserve_merge_commit"
            if ci_binding_blockers and merge_applied
            else "repair_expected_head_merge_receipt_binding"
        )
    elif not merge_applied:
        state = MERGE_NOT_APPLIED
        status = PARTIAL
        next_route = "reobserve_pr_head_base_and_merge_bridge_result_before_retry"
    elif not post_pr_exact:
        state = POST_MERGE_REOBSERVATION
        status = PARTIAL
        next_route = "freshly_reobserve_merged_pr_and_main"
    elif not post_main_exact:
        state = POST_MERGE_MAIN_ADVANCED
        status = PARTIAL
        next_route = "retain_successful_merge_and_reconcile_current_main_head"
    elif not post_ci_complete:
        state = POST_MERGE_CI_REOBSERVATION
        status = PARTIAL
        next_route = "freshly_reobserve_required_post_merge_ci"
    elif post_ci_non_success:
        state = POST_MERGE_CI_NON_SUCCESS
        status = PARTIAL
        next_route = "retain_merge_fact_and_route_post_merge_failure_to_followup_repair"
    elif not post_ci_success:
        state = POST_MERGE_CI_REOBSERVATION
        status = PARTIAL
        next_route = "freshly_reobserve_required_post_merge_ci"
    else:
        state = LINEAGE_CLOSED
        status = READY
        next_route = "development_lineage_closed"

    # Malformed source/receipt evidence always overrides partial live-state routes.
    if blockers and state not in {
        POST_MERGE_CI_BINDING_OBSTRUCTION,
        MERGE_RECEIPT_OBSTRUCTION,
    }:
        state = MERGE_RECEIPT_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "repair_expected_head_merge_receipt_binding"

    closed = state == LINEAGE_CLOSED

    evidence = {
        "source_merge_candidate_packet_digest": source_digest,
        "pull_request_number": pr_number,
        "expected_head_sha": expected_head,
        "expected_base_sha": expected_base,
        "pre_merge_pr_head_sha": pre_merge_head,
        "pre_merge_base_head_sha": pre_merge_base,
        "pre_merge_observation_digest": pre_merge_observation_digest,
        "github_mcp_bridge_status": bridge_status,
        "github_mcp_bridge_receipt_digest": bridge_receipt_digest,
        "github_mcp_bridge_delegated_applied_count": bridge_applied_count,
        "merge_action_kind": merge_action_kind,
        "merge_method": merge_method,
        "merge_result_merged": merge_result_merged,
        "merge_result_sha": merge_commit_sha,
        "merge_result_message_digest": merge_result_message_digest,
        "post_merge_main_head_sha": post_main_head,
        "post_merge_main_observation_digest": post_main_observation_digest,
        "post_merge_pr_merge_commit_sha": post_pr_merge_sha,
        "post_merge_pr_observation_digest": post_pr_observation_digest,
        "post_merge_required_workflows_digest": _sha(required_names),
        "post_merge_ci_verifications_digest": _sha(
            {name: ci_packets[name] for name in sorted(ci_packets)}
        ),
        "expected_head_merge_used": merge_attempted,
        "merge_candidate_was_merge_authority": False,
        "ci_success_was_merge_authority": False,
        "merge_success_implied_post_merge_ci_success": False,
        "post_merge_ci_failure_implies_automatic_rollback": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-expected-head-merge-closure-" + _sha(
        {
            "source_digest": source_digest,
            "state": state,
            "merge_commit_sha": merge_commit_sha,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return ExpectedHeadMergeClosureResult(
        VERSION,
        status,
        packet_id,
        repository,
        pr_number,
        expected_head,
        expected_base,
        state,
        True,
        merge_applied,
        merge_commit_sha,
        post_main_exact,
        post_pr_exact,
        post_ci_complete,
        post_ci_success,
        closed,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
