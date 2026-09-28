#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

VERSION = "kuuos_runtime_development_lineage_reroot_v7_32"
SOURCE_VERSION = "kuuos_runtime_expected_head_merge_closure_v7_31"
OBSERVATION_VERSION = "kuuos_development_lineage_reroot_observation_v7_32"

READY = "KUUOS_DEVELOPMENT_LINEAGE_REROOT_READY"
PARTIAL = "KUUOS_DEVELOPMENT_LINEAGE_REROOT_PARTIAL"
OBSTRUCTED = "KUUOS_DEVELOPMENT_LINEAGE_REROOT_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_DEVELOPMENT_LINEAGE_REROOT_NOT_APPLICABLE"

ROOT_READY_EXACT = "new_lineage_root_ready_exact_closed_merge"
ROOT_READY_DESCENDANT = "new_lineage_root_ready_descendant_main"
ROOT_READY_LOCAL_RECONCILIATION = (
    "new_lineage_root_ready_local_revision_reconciliation_required"
)
MAIN_REOBSERVATION_REQUIRED = "fresh_main_reobservation_required"
ANCESTRY_REOBSERVATION_REQUIRED = "closed_merge_ancestry_reobservation_required"
ANCESTRY_OBSTRUCTION = "closed_merge_not_ancestor_of_current_main_obstruction"
AUTHORITY_CARRYOVER_OBSTRUCTION = "predecessor_authority_carryover_obstruction"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class DevelopmentLineageRerootResult:
    version: str
    status: str
    packet_id: str
    repository_full_name: str
    predecessor_closure_packet_digest: str
    predecessor_merge_commit_sha: str
    current_main_head_sha: str
    reroot_state: str
    current_main_is_descendant_or_equal: bool
    local_head_aligned: bool | None
    local_reconciliation_required: bool
    local_observation_required: bool
    next_lineage_root_id: str
    successor_write_authority_granted: bool
    successor_merge_authority_granted: bool
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


def _digest(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
    text = str(value or "").strip()
    if optional and not text:
        return ""
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _commit(
    value: Any,
    name: str,
    blockers: list[str],
    *,
    optional: bool = False,
) -> str:
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


def _nonnegative_int(
    value: Any,
    name: str,
    blockers: list[str],
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        blockers.append(name + "_invalid")
        return 0
    return value


def build_development_lineage_reroot(
    *,
    closed_lineage_packet: Mapping[str, Any],
    observation: Mapping[str, Any],
) -> DevelopmentLineageRerootResult:
    source = _m(closed_lineage_packet)
    obs = _m(observation)
    blockers: list[str] = []
    warnings: list[str] = []

    if source.get("version") != SOURCE_VERSION:
        blockers.append("closed_lineage_packet_version_invalid")
    if obs.get("version") != OBSERVATION_VERSION:
        blockers.append("observation_version_invalid")

    source_digest = _sha(source)
    observed_source_digest = _digest(
        obs.get("source_closed_lineage_packet_digest"),
        "source_closed_lineage_packet_digest",
        blockers,
    )
    if observed_source_digest != source_digest:
        blockers.append("source_closed_lineage_packet_digest_mismatch")

    repository = str(obs.get("repository_full_name", "")).strip()
    if repository != "itakura-hidetoshi/KuuOS":
        blockers.append("repository_full_name_invalid")

    source_closed = bool(
        source.get("status") == "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_READY"
        and source.get("closure_state") == "development_lineage_closed"
        and source.get("development_lineage_closed") is True
        and source.get("merge_applied") is True
        and source.get("post_merge_main_exact") is True
        and source.get("post_merge_pr_exact") is True
        and source.get("post_merge_ci_complete") is True
        and source.get("post_merge_ci_success") is True
    )

    predecessor_merge = _commit(
        source.get("merge_commit_sha"),
        "predecessor_merge_commit_sha",
        blockers,
        optional=not source_closed,
    )

    if not source_closed:
        packet_id = "kuuos-development-lineage-reroot-" + _sha(
            {
                "source_digest": source_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return DevelopmentLineageRerootResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            repository,
            source_digest,
            predecessor_merge,
            "",
            "closed_lineage_packet_not_closed",
            False,
            None,
            False,
            True,
            "",
            False,
            False,
            "return_to_v7_31_expected_head_merge_closure",
            {
                "source_closed_lineage_packet_digest": source_digest,
                "predecessor_authority_reused": False,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    prior_merge_authority_reused = _bool(
        obs.get("prior_merge_authority_reused"),
        "prior_merge_authority_reused",
        blockers,
    )
    prior_write_authority_reused = _bool(
        obs.get("prior_write_authority_reused"),
        "prior_write_authority_reused",
        blockers,
    )
    prior_receipt_as_authority = _bool(
        obs.get("prior_receipt_used_as_successor_authority"),
        "prior_receipt_used_as_successor_authority",
        blockers,
    )
    successor_authority_claimed = _bool(
        obs.get("successor_authority_granted_by_reroot"),
        "successor_authority_granted_by_reroot",
        blockers,
    )

    authority_carryover = bool(
        prior_merge_authority_reused
        or prior_write_authority_reused
        or prior_receipt_as_authority
        or successor_authority_claimed
    )

    raw_main = str(obs.get("current_main_head_sha", "") or "").strip().lower()
    raw_main_digest = str(
        obs.get("current_main_observation_digest", "") or ""
    ).strip()

    main_observed = bool(raw_main and raw_main_digest)
    if raw_main and SHA40.fullmatch(raw_main) is None:
        blockers.append("current_main_head_sha_invalid")
    if raw_main_digest and SHA64.fullmatch(raw_main_digest) is None:
        blockers.append("current_main_observation_digest_invalid")

    current_main = raw_main if SHA40.fullmatch(raw_main or "") else ""
    main_observation_digest = (
        raw_main_digest if SHA64.fullmatch(raw_main_digest or "") else ""
    )

    comparison = _m(obs.get("ancestry_comparison"))
    comparison_available = comparison.get("available") is True
    comparison_digest = ""
    comparison_status = ""
    comparison_ahead_by = 0
    comparison_behind_by = 0
    ancestry_verified = False
    ancestry_obstructed = False

    if main_observed and current_main == predecessor_merge:
        ancestry_verified = True
        if comparison_available:
            cmp_base = _commit(
                comparison.get("base_sha"),
                "ancestry_base_sha",
                blockers,
            )
            cmp_head = _commit(
                comparison.get("head_sha"),
                "ancestry_head_sha",
                blockers,
            )
            comparison_status = str(comparison.get("status", "")).strip()
            comparison_ahead_by = _nonnegative_int(
                comparison.get("ahead_by"),
                "ancestry_ahead_by",
                blockers,
            )
            comparison_behind_by = _nonnegative_int(
                comparison.get("behind_by"),
                "ancestry_behind_by",
                blockers,
            )
            comparison_digest = _digest(
                comparison.get("observation_digest"),
                "ancestry_observation_digest",
                blockers,
            )
            if (
                cmp_base != predecessor_merge
                or cmp_head != current_main
                or comparison_status not in {"identical", "ahead"}
                or comparison_behind_by != 0
            ):
                blockers.append("exact_main_ancestry_comparison_inconsistent")
    elif main_observed:
        if comparison_available:
            cmp_base = _commit(
                comparison.get("base_sha"),
                "ancestry_base_sha",
                blockers,
            )
            cmp_head = _commit(
                comparison.get("head_sha"),
                "ancestry_head_sha",
                blockers,
            )
            comparison_status = str(comparison.get("status", "")).strip()
            comparison_ahead_by = _nonnegative_int(
                comparison.get("ahead_by"),
                "ancestry_ahead_by",
                blockers,
            )
            comparison_behind_by = _nonnegative_int(
                comparison.get("behind_by"),
                "ancestry_behind_by",
                blockers,
            )
            comparison_digest = _digest(
                comparison.get("observation_digest"),
                "ancestry_observation_digest",
                blockers,
            )
            if cmp_base != predecessor_merge:
                blockers.append("ancestry_base_sha_mismatch")
            if cmp_head != current_main:
                blockers.append("ancestry_head_sha_mismatch")

            if (
                comparison_status == "ahead"
                and comparison_ahead_by > 0
                and comparison_behind_by == 0
                and not blockers
            ):
                ancestry_verified = True
            elif comparison_status in {"diverged", "behind"} or (
                comparison_behind_by > 0
            ):
                ancestry_obstructed = True
            elif comparison_status == "identical":
                blockers.append("ancestry_identical_but_main_sha_differs")
            elif comparison_status not in {"ahead", "diverged", "behind", "identical"}:
                blockers.append("ancestry_status_invalid")

    local_observed = obs.get("local_git_observed")
    if not isinstance(local_observed, bool):
        blockers.append("local_git_observed_must_be_bool")
        local_observed = False

    local_head = ""
    local_observation_digest = ""
    local_head_aligned: bool | None = None
    if local_observed:
        local_head = _commit(
            obs.get("local_git_head_sha"),
            "local_git_head_sha",
            blockers,
        )
        local_observation_digest = _digest(
            obs.get("local_git_observation_digest"),
            "local_git_observation_digest",
            blockers,
        )
        if current_main:
            local_head_aligned = local_head == current_main
    else:
        warnings.append("local_git_observation_not_required_for_remote_reroot")

    local_observation_required = not local_observed
    local_reconciliation_required = bool(
        local_observed
        and current_main
        and local_head
        and local_head != current_main
    )

    if authority_carryover:
        state = AUTHORITY_CARRYOVER_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "discard_predecessor_authority_and_issue_no_successor_authority"
    elif blockers:
        state = ANCESTRY_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "repair_reroot_evidence_binding"
    elif not main_observed:
        state = MAIN_REOBSERVATION_REQUIRED
        status = PARTIAL
        next_route = "freshly_reobserve_current_main"
    elif current_main != predecessor_merge and not comparison_available:
        state = ANCESTRY_REOBSERVATION_REQUIRED
        status = PARTIAL
        next_route = "freshly_compare_closed_merge_to_current_main"
    elif ancestry_obstructed or not ancestry_verified:
        state = ANCESTRY_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "reconcile_repository_history_before_new_lineage_root"
    elif local_reconciliation_required:
        state = ROOT_READY_LOCAL_RECONCILIATION
        status = READY
        next_route = "use_remote_root_and_reconcile_local_git_before_remote_bound_work"
    elif current_main == predecessor_merge:
        state = ROOT_READY_EXACT
        status = READY
        next_route = "begin_new_development_lineage_from_fresh_main_root"
    else:
        state = ROOT_READY_DESCENDANT
        status = READY
        next_route = "begin_new_development_lineage_from_fresh_descendant_main_root"

    root_ready = status == READY
    next_root_id = (
        "kuuos-development-lineage-root-"
        + _sha(
            {
                "repository_full_name": repository,
                "predecessor_closure_packet_digest": source_digest,
                "predecessor_merge_commit_sha": predecessor_merge,
                "current_main_head_sha": current_main,
                "current_main_observation_digest": main_observation_digest,
            }
        )[:24]
        if root_ready
        else ""
    )

    evidence = {
        "source_closed_lineage_packet_digest": source_digest,
        "predecessor_merge_commit_sha": predecessor_merge,
        "current_main_head_sha": current_main,
        "current_main_observation_digest": main_observation_digest,
        "ancestry_comparison_available": comparison_available,
        "ancestry_comparison_status": comparison_status,
        "ancestry_ahead_by": comparison_ahead_by,
        "ancestry_behind_by": comparison_behind_by,
        "ancestry_observation_digest": comparison_digest,
        "current_main_is_descendant_or_equal": ancestry_verified,
        "local_git_observed": local_observed,
        "local_git_head_sha": local_head,
        "local_git_observation_digest": local_observation_digest,
        "local_head_aligned": local_head_aligned,
        "previous_closure_receipt_reused_as_authority": False,
        "previous_merge_authority_reused": False,
        "previous_write_authority_reused": False,
        "successor_write_authority_granted": False,
        "successor_merge_authority_granted": False,
        "prior_closure_ci_certifies_advanced_main": False,
        "closed_lineage_history_overwritten": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-development-lineage-reroot-" + _sha(
        {
            "source_digest": source_digest,
            "state": state,
            "current_main": current_main,
            "next_root_id": next_root_id,
            "evidence": evidence,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return DevelopmentLineageRerootResult(
        VERSION,
        status,
        packet_id,
        repository,
        source_digest,
        predecessor_merge,
        current_main,
        state,
        ancestry_verified,
        local_head_aligned,
        local_reconciliation_required,
        local_observation_required,
        next_root_id,
        False,
        False,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
