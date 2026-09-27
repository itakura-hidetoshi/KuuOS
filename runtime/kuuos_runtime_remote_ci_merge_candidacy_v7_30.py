#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_remote_ci_merge_candidacy_v7_30"
SOURCE_VERSION = "kuuos_runtime_github_remote_candidate_materialization_v7_29"
OBSERVATION_VERSION = "kuuos_remote_ci_merge_candidacy_observation_v7_30"
CI_VERSION = "kuuos_github_ci_completion_reentry_v1_1"
CI_VERIFIED = "KUUOS_GITHUB_CI_COMPLETION_REENTRY_VERIFIED"

READY = "KUUOS_REMOTE_CI_MERGE_CANDIDACY_READY"
PARTIAL = "KUUOS_REMOTE_CI_MERGE_CANDIDACY_PARTIAL"
OBSTRUCTED = "KUUOS_REMOTE_CI_MERGE_CANDIDACY_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_REMOTE_CI_MERGE_CANDIDACY_NOT_APPLICABLE"

HEAD_REOBSERVATION_REQUIRED = "remote_candidate_head_reobservation_required"
HEAD_RECONCILIATION_REQUIRED = "remote_candidate_head_reconciliation_required"
BASE_RECONCILIATION_REQUIRED = "remote_base_reconciliation_required"
PULL_REQUEST_REQUIRED = "pull_request_required"
PULL_REQUEST_REBIND_REQUIRED = "pull_request_binding_reconciliation_required"
PULL_REQUEST_REVIEW_STATE_REQUIRED = "pull_request_review_state_required"
CI_REOBSERVATION_REQUIRED = "candidate_ci_reobservation_required"
CI_NON_SUCCESS_REPAIR_REENTRY = "candidate_ci_non_success_repair_reentry"
CI_BINDING_OBSTRUCTION = "candidate_ci_binding_obstruction"
MERGE_CANDIDATE_READY = "merge_candidate_ready_explicit_merge_authority_required"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")
BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")


@dataclass(frozen=True)
class RemoteCIMergeCandidacyResult:
    version: str
    status: str
    packet_id: str
    repository_full_name: str
    candidate_branch: str
    candidate_head_sha: str
    base_branch: str
    base_head_sha: str
    candidacy_state: str
    candidate_retained: bool
    pull_request_bound: bool
    required_ci_complete: bool
    required_ci_success: bool
    merge_candidate: bool
    merge_authority_granted: bool
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


def _branch(value: Any, name: str, blockers: list[str]) -> str:
    text = str(value or "").strip()
    if (
        not text
        or BRANCH.fullmatch(text) is None
        or ".." in text
        or "@{" in text
        or "//" in text
        or text.endswith(("/", "."))
        or text.startswith(".")
        or text.endswith(".lock")
    ):
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
        blockers.append("required_workflow_names_missing")
        return []
    result = [str(item).strip() for item in value if str(item).strip()]
    if len(result) != len(value) or len(set(result)) != len(result):
        blockers.append("required_workflow_names_invalid")
    return result


def _ci_packets(
    value: Any,
    *,
    repository: str,
    candidate_head: str,
    required_names: list[str],
) -> tuple[dict[str, dict[str, Any]], list[str], list[str]]:
    blockers: list[str] = []
    warnings: list[str] = []
    if not isinstance(value, list):
        return {}, ["ci_verifications_not_list"], warnings

    packets: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(value):
        if not isinstance(raw, Mapping):
            blockers.append(f"ci_verification_{index}_not_object")
            continue
        packet = dict(raw)
        workflow = str(packet.get("workflow_name", "")).strip()
        if not workflow:
            blockers.append(f"ci_verification_{index}_workflow_name_missing")
            continue
        if workflow in packets:
            blockers.append("duplicate_ci_workflow_verification:" + workflow)
            continue
        packets[workflow] = packet

        if packet.get("version") != CI_VERSION:
            blockers.append("ci_verification_version_invalid:" + workflow)
        if packet.get("status") != CI_VERIFIED:
            blockers.append("ci_verification_not_verified:" + workflow)
        if str(packet.get("repository", "")) != repository:
            blockers.append("ci_repository_mismatch:" + workflow)
        if str(packet.get("head_sha", "")).lower() != candidate_head:
            blockers.append("ci_head_sha_mismatch:" + workflow)
        if packet.get("fresh_mcp_reobservation") is not True:
            blockers.append("ci_fresh_reobservation_missing:" + workflow)
        if packet.get("merge_authority_granted") is not False:
            blockers.append("ci_must_not_grant_merge_authority:" + workflow)
        if packet.get("write_authority_granted") is not False:
            blockers.append("ci_must_not_grant_write_authority:" + workflow)
        _digest(
            packet.get("evidence_digest"),
            "ci_evidence_digest_" + str(index),
            blockers,
        )
        route = str(packet.get("route", ""))
        if route not in {"verified_success", "verified_non_success"}:
            blockers.append("ci_route_invalid:" + workflow)
        if route == "verified_non_success":
            warnings.append("ci_verified_non_success:" + workflow)

    missing = [name for name in required_names if name not in packets]
    if missing:
        warnings.append("required_ci_verification_missing:" + ",".join(missing))
    extras = [name for name in packets if name not in required_names]
    if extras:
        warnings.append("extra_ci_verification_ignored:" + ",".join(sorted(extras)))
    return packets, blockers, warnings


def build_remote_ci_merge_candidacy(
    *,
    materialization_packet: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> RemoteCIMergeCandidacyResult:
    source = _m(materialization_packet)
    obs = _m(observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if source.get("version") != SOURCE_VERSION:
        blockers.append("materialization_packet_version_invalid")
    if obs.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")

    source_digest = _sha(source)
    if _digest(
        obs.get("source_materialization_packet_digest"),
        "source_materialization_packet_digest",
        blockers,
    ) != source_digest:
        blockers.append("source_materialization_packet_digest_mismatch")

    repository = str(obs.get("repository_full_name", "")).strip()
    if repository != "itakura-hidetoshi/KuuOS":
        blockers.append("repository_full_name_invalid")

    source_ready = bool(
        source.get("status") == "KUUOS_GITHUB_REMOTE_CANDIDATE_MATERIALIZATION_READY"
        and source.get("remote_candidate_published") is True
        and source.get("remote_base_aligned") is True
        and source.get("ci_reobservation_required") is True
        and source.get("materialization_state")
        in {
            "remote_candidate_published_ci_reobservation_required",
            "remote_candidate_already_published_ci_reobservation_required",
        }
    )

    source_candidate_branch = str(source.get("candidate_branch", "")).strip()
    source_base_branch = str(source.get("base_branch", "")).strip()
    source_evidence = _m(source.get("evidence"))
    source_candidate_head = _commit(
        source_evidence.get("remote_commit_sha"),
        "source_remote_commit_sha",
        blockers,
        optional=not source_ready,
    )
    source_base_head = _commit(
        source_evidence.get("remote_base_after_sha"),
        "source_remote_base_after_sha",
        blockers,
        optional=not source_ready,
    )

    candidate_branch = _branch(
        obs.get("candidate_branch"),
        "candidate_branch",
        blockers,
    )
    base_branch = _branch(
        obs.get("base_branch"),
        "base_branch",
        blockers,
    )
    if candidate_branch != source_candidate_branch:
        blockers.append("candidate_branch_source_binding_mismatch")
    if base_branch != source_base_branch:
        blockers.append("base_branch_source_binding_mismatch")

    if not source_ready:
        packet_id = "kuuos-remote-ci-merge-candidacy-" + _sha(
            {
                "source_digest": source_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return RemoteCIMergeCandidacyResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            repository,
            candidate_branch,
            "",
            base_branch,
            "",
            "materialization_packet_not_ci_reobservation_ready",
            bool(source.get("candidate_retained", True)),
            False,
            False,
            False,
            False,
            False,
            "return_to_v7_29_remote_materialization",
            {
                "source_materialization_packet_digest": source_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    candidate_head = _commit(
        obs.get("candidate_branch_head_sha"),
        "candidate_branch_head_sha",
        blockers,
    )
    base_head = _commit(
        obs.get("base_branch_head_sha"),
        "base_branch_head_sha",
        blockers,
    )
    candidate_observation_digest = _digest(
        obs.get("candidate_branch_observation_digest"),
        "candidate_branch_observation_digest",
        blockers,
    )
    base_observation_digest = _digest(
        obs.get("base_branch_observation_digest"),
        "base_branch_observation_digest",
        blockers,
    )

    pr_exists = _bool(obs.get("pull_request_exists"), "pull_request_exists", blockers)
    pr_number = _positive_int(
        obs.get("pull_request_number"),
        "pull_request_number",
        blockers,
        optional=not pr_exists,
    )
    pr_state = str(obs.get("pull_request_state", "")).strip()
    pr_draft = obs.get("pull_request_draft")
    if pr_exists and not isinstance(pr_draft, bool):
        blockers.append("pull_request_draft_must_be_bool")
        pr_draft = False

    pr_head_branch = str(obs.get("pull_request_head_branch", "")).strip()
    pr_head_sha = _commit(
        obs.get("pull_request_head_sha"),
        "pull_request_head_sha",
        blockers,
        optional=not pr_exists,
    )
    pr_base_branch = str(obs.get("pull_request_base_branch", "")).strip()
    pr_base_sha = _commit(
        obs.get("pull_request_base_sha"),
        "pull_request_base_sha",
        blockers,
        optional=not pr_exists,
    )
    pr_observation_digest = _digest(
        obs.get("pull_request_observation_digest"),
        "pull_request_observation_digest",
        blockers,
        optional=not pr_exists,
    )

    required_names = _names(obs.get("required_workflow_names"), blockers)
    ci_packets, ci_blockers, ci_warnings = _ci_packets(
        obs.get("ci_verifications"),
        repository=repository,
        candidate_head=candidate_head,
        required_names=required_names,
    )
    blockers.extend(ci_blockers)
    warnings.extend(ci_warnings)

    head_exact = candidate_head == source_candidate_head
    base_exact = base_head == source_base_head

    pull_request_bound = bool(
        pr_exists
        and pr_number > 0
        and pr_state == "open"
        and pr_head_branch == candidate_branch
        and pr_head_sha == candidate_head
        and pr_base_branch == base_branch
        and pr_base_sha == base_head
        and pr_observation_digest
    )

    required_ci_complete = bool(
        required_names
        and all(name in ci_packets for name in required_names)
    )
    required_ci_success = bool(
        required_ci_complete
        and all(
            ci_packets[name].get("status") == CI_VERIFIED
            and ci_packets[name].get("route") == "verified_success"
            and str(ci_packets[name].get("head_sha", "")).lower() == candidate_head
            and ci_packets[name].get("fresh_mcp_reobservation") is True
            for name in required_names
        )
    )
    required_ci_non_success = bool(
        required_ci_complete
        and any(
            ci_packets[name].get("route") == "verified_non_success"
            for name in required_names
        )
    )

    # Evidence-binding errors for supplied CI packets are true obstructions.
    ci_binding_errors = [
        item
        for item in blockers
        if item.startswith("ci_")
        and not item.startswith("ci_evidence_digest_")
    ]

    if blockers and any(
        item
        for item in blockers
        if item
        not in {
            # these are handled as reconciliation states below
        }
    ):
        # Do not short-circuit yet; state classification below gives more specific
        # non-rejecting routes for head/base/PR/CI incompleteness.
        pass

    if candidate_head != source_candidate_head:
        state = HEAD_RECONCILIATION_REQUIRED
        status = PARTIAL
        next_route = "retain_published_candidate_and_reconcile_candidate_branch_head"
    elif base_head != source_base_head:
        state = BASE_RECONCILIATION_REQUIRED
        status = PARTIAL
        next_route = "retain_published_candidate_and_reconcile_current_base"
    elif not candidate_observation_digest or not base_observation_digest:
        state = HEAD_REOBSERVATION_REQUIRED
        status = PARTIAL
        next_route = "freshly_reobserve_candidate_and_base_heads"
    elif not pr_exists:
        state = PULL_REQUEST_REQUIRED
        status = PARTIAL
        next_route = "create_or_bind_pull_request_without_deriving_merge_authority"
    elif not pull_request_bound:
        state = PULL_REQUEST_REBIND_REQUIRED
        status = PARTIAL
        next_route = "reobserve_or_retarget_pull_request_to_exact_candidate_and_base"
    elif pr_draft is True:
        state = PULL_REQUEST_REVIEW_STATE_REQUIRED
        status = PARTIAL
        next_route = "retain_candidate_until_pull_request_review_state_is_explicitly_changed"
    elif ci_binding_errors:
        state = CI_BINDING_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "discard_stale_ci_binding_and_freshly_reobserve_exact_candidate_head"
    elif not required_ci_complete:
        state = CI_REOBSERVATION_REQUIRED
        status = PARTIAL
        next_route = "freshly_reobserve_all_required_ci_workflows"
    elif required_ci_non_success:
        state = CI_NON_SUCCESS_REPAIR_REENTRY
        status = PARTIAL
        next_route = "retain_remote_candidate_and_reenter_ci_repair_routing"
    elif not required_ci_success:
        state = CI_REOBSERVATION_REQUIRED
        status = PARTIAL
        next_route = "freshly_reobserve_all_required_ci_workflows"
    else:
        state = MERGE_CANDIDATE_READY
        status = READY
        next_route = "acquire_explicit_merge_authority_then_expected_head_merge"

    merge_candidate = state == MERGE_CANDIDATE_READY
    merge_authority_granted = False

    # Binding/path errors unrelated to live reconciliation remain hard evidence obstructions.
    structural_blockers = [
        item
        for item in blockers
        if item
        in {
            "materialization_packet_version_invalid",
            "observation_version_invalid",
            "source_materialization_packet_digest_invalid",
            "source_materialization_packet_digest_mismatch",
            "repository_full_name_invalid",
            "candidate_branch_source_binding_mismatch",
            "base_branch_source_binding_mismatch",
            "candidate_branch_invalid",
            "base_branch_invalid",
        }
    ]
    if structural_blockers:
        state = CI_BINDING_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "repair_remote_ci_candidacy_source_binding"
        merge_candidate = False

    evidence = {
        "source_materialization_packet_digest": source_digest,
        "source_remote_commit_sha": source_candidate_head,
        "source_remote_base_sha": source_base_head,
        "candidate_branch_head_sha": candidate_head,
        "candidate_branch_observation_digest": candidate_observation_digest,
        "base_branch_head_sha": base_head,
        "base_branch_observation_digest": base_observation_digest,
        "pull_request_number": pr_number,
        "pull_request_observation_digest": pr_observation_digest,
        "required_workflow_names_digest": _sha(required_names),
        "ci_verification_packets_digest": _sha(
            {name: ci_packets[name] for name in sorted(ci_packets)}
        ),
        "candidate_head_exact": head_exact,
        "base_head_exact": base_exact,
        "pull_request_bound": pull_request_bound,
        "required_ci_complete": required_ci_complete,
        "required_ci_success": required_ci_success,
        "merge_authority_derived_from_ci": False,
        "write_authority_derived_from_ci": False,
        "merge_candidate_executes_merge": False,
        "ci_event_alone_is_success_evidence": False,
        "fresh_mcp_ci_reobservation_required": True,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-remote-ci-merge-candidacy-" + _sha(
        {
            "source_digest": source_digest,
            "state": state,
            "repository": repository,
            "candidate_branch": candidate_branch,
            "candidate_head": candidate_head,
            "base_branch": base_branch,
            "base_head": base_head,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return RemoteCIMergeCandidacyResult(
        VERSION,
        status,
        packet_id,
        repository,
        candidate_branch,
        candidate_head,
        base_branch,
        base_head,
        state,
        True,
        pull_request_bound,
        required_ci_complete,
        required_ci_success,
        merge_candidate,
        merge_authority_granted,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
