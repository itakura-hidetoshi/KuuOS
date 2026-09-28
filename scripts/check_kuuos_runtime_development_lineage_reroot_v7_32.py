#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_development_lineage_reroot_v7_32 import (
    ANCESTRY_OBSTRUCTION,
    ANCESTRY_REOBSERVATION_REQUIRED,
    AUTHORITY_CARRYOVER_OBSTRUCTION,
    MAIN_REOBSERVATION_REQUIRED,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    ROOT_READY_DESCENDANT,
    ROOT_READY_EXACT,
    ROOT_READY_LOCAL_RECONCILIATION,
    build_development_lineage_reroot,
)

MERGE = "d" * 40
ADVANCED = "e" * 40
LOCAL_OLD = "c" * 40


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def source(*, closed: bool = True) -> dict:
    return {
        "version": "kuuos_runtime_expected_head_merge_closure_v7_31",
        "status": (
            "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_READY"
            if closed
            else "KUUOS_EXPECTED_HEAD_MERGE_CLOSURE_PARTIAL"
        ),
        "packet_id": "closed-lineage",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "pull_request_number": 2001,
        "expected_head_sha": "b" * 40,
        "expected_base_sha": "a" * 40,
        "closure_state": (
            "development_lineage_closed"
            if closed
            else "post_merge_ci_reobservation_required"
        ),
        "candidate_retained": True,
        "merge_applied": closed,
        "merge_commit_sha": MERGE if closed else "",
        "post_merge_main_exact": closed,
        "post_merge_pr_exact": closed,
        "post_merge_ci_complete": closed,
        "post_merge_ci_success": closed,
        "development_lineage_closed": closed,
        "next_route": (
            "development_lineage_closed"
            if closed
            else "freshly_reobserve_required_post_merge_ci"
        ),
        "evidence": {
            "source_merge_candidate_packet_digest": "1" * 64,
            "merge_authority_packet_digest": "2" * 64,
            "merge_authority_scope_digest": "3" * 64,
            "merge_authority_independently_supplied": True,
            "merge_authority_derived_from_ci": False,
            "merge_authority_derived_from_candidacy": False,
            "merge_result_sha": MERGE if closed else "",
            "merge_candidate_was_merge_authority": False,
            "ci_success_was_merge_authority": False,
            "merge_success_implied_post_merge_ci_success": False,
            "post_merge_ci_failure_implies_automatic_rollback": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def observation(
    src: dict,
    *,
    main: str = MERGE,
    main_observed: bool = True,
    comparison_available: bool = False,
    comparison_status: str = "identical",
    ahead_by: int = 0,
    behind_by: int = 0,
    local_observed: bool = True,
    local_head: str | None = None,
    prior_merge_authority_reused: bool = False,
    prior_write_authority_reused: bool = False,
    prior_receipt_used_as_successor_authority: bool = False,
    successor_authority_granted_by_reroot: bool = False,
) -> dict:
    if local_head is None:
        local_head = main
    comparison = {
        "available": comparison_available,
        "base_sha": MERGE if comparison_available else "",
        "head_sha": main if comparison_available else "",
        "status": comparison_status if comparison_available else "",
        "ahead_by": ahead_by if comparison_available else 0,
        "behind_by": behind_by if comparison_available else 0,
        "observation_digest": "4" * 64 if comparison_available else "",
    }
    return {
        "version": "kuuos_development_lineage_reroot_observation_v7_32",
        "source_closed_lineage_packet_digest": h(src),
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "current_main_head_sha": main if main_observed else "",
        "current_main_observation_digest": "5" * 64 if main_observed else "",
        "ancestry_comparison": comparison,
        "local_git_observed": local_observed,
        "local_git_head_sha": local_head if local_observed else "",
        "local_git_observation_digest": "6" * 64 if local_observed else "",
        "prior_merge_authority_reused": prior_merge_authority_reused,
        "prior_write_authority_reused": prior_write_authority_reused,
        "prior_receipt_used_as_successor_authority": (
            prior_receipt_used_as_successor_authority
        ),
        "successor_authority_granted_by_reroot": (
            successor_authority_granted_by_reroot
        ),
    }


def test_exact_closed_merge_becomes_new_root_without_authority_carryover() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(src),
    )
    assert result.status == READY, result.to_dict()
    assert result.reroot_state == ROOT_READY_EXACT
    assert result.current_main_is_descendant_or_equal is True
    assert result.local_head_aligned is True
    assert result.local_reconciliation_required is False
    assert result.next_lineage_root_id
    assert result.successor_write_authority_granted is False
    assert result.successor_merge_authority_granted is False
    assert result.evidence["previous_merge_authority_reused"] is False


def test_advanced_main_can_be_new_root_when_closed_merge_is_verified_ancestor() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main=ADVANCED,
            comparison_available=True,
            comparison_status="ahead",
            ahead_by=3,
            behind_by=0,
        ),
    )
    assert result.status == READY, result.to_dict()
    assert result.reroot_state == ROOT_READY_DESCENDANT
    assert result.current_main_head_sha == ADVANCED
    assert result.current_main_is_descendant_or_equal is True
    assert result.next_lineage_root_id
    assert result.evidence["prior_closure_ci_certifies_advanced_main"] is False


def test_advanced_main_without_ancestry_evidence_is_partial_not_rejected() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main=ADVANCED,
            comparison_available=False,
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.reroot_state == ANCESTRY_REOBSERVATION_REQUIRED
    assert result.next_lineage_root_id == ""
    assert result.successor_write_authority_granted is False


def test_diverged_main_is_true_history_obstruction() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main=ADVANCED,
            comparison_available=True,
            comparison_status="diverged",
            ahead_by=2,
            behind_by=1,
        ),
    )
    assert result.status == OBSTRUCTED, result.to_dict()
    assert result.reroot_state == ANCESTRY_OBSTRUCTION
    assert result.next_lineage_root_id == ""


def test_stale_local_git_does_not_block_remote_root() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main=ADVANCED,
            comparison_available=True,
            comparison_status="ahead",
            ahead_by=2,
            behind_by=0,
            local_head=LOCAL_OLD,
        ),
    )
    assert result.status == READY, result.to_dict()
    assert result.reroot_state == ROOT_READY_LOCAL_RECONCILIATION
    assert result.current_main_is_descendant_or_equal is True
    assert result.local_head_aligned is False
    assert result.local_reconciliation_required is True
    assert result.next_lineage_root_id


def test_missing_local_observation_does_not_block_remote_root() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            local_observed=False,
        ),
    )
    assert result.status == READY, result.to_dict()
    assert result.reroot_state == ROOT_READY_EXACT
    assert result.local_observation_required is True
    assert result.local_head_aligned is None
    assert "local_git_observation_not_required_for_remote_reroot" in result.warnings


def test_predecessor_authority_cannot_be_reused() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            prior_merge_authority_reused=True,
        ),
    )
    assert result.status == OBSTRUCTED, result.to_dict()
    assert result.reroot_state == AUTHORITY_CARRYOVER_OBSTRUCTION
    assert result.successor_write_authority_granted is False
    assert result.successor_merge_authority_granted is False


def test_closed_receipt_cannot_issue_successor_authority() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            prior_receipt_used_as_successor_authority=True,
        ),
    )
    assert result.status == OBSTRUCTED
    assert result.reroot_state == AUTHORITY_CARRYOVER_OBSTRUCTION


def test_missing_main_observation_requests_reobservation() -> None:
    src = source()
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main_observed=False,
            local_observed=False,
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.reroot_state == MAIN_REOBSERVATION_REQUIRED


def test_nonclosed_source_is_not_applicable() -> None:
    src = source(closed=False)
    result = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(src),
    )
    assert result.status == NOT_APPLICABLE, result.to_dict()
    assert result.next_lineage_root_id == ""


def test_root_identity_changes_with_fresh_main() -> None:
    src = source()
    exact = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(src),
    )
    advanced = build_development_lineage_reroot(
        closed_lineage_packet=src,
        observation=observation(
            src,
            main=ADVANCED,
            comparison_available=True,
            comparison_status="ahead",
            ahead_by=1,
            behind_by=0,
        ),
    )
    assert exact.status == READY
    assert advanced.status == READY
    assert exact.next_lineage_root_id != advanced.next_lineage_root_id


def main() -> int:
    test_exact_closed_merge_becomes_new_root_without_authority_carryover()
    test_advanced_main_can_be_new_root_when_closed_merge_is_verified_ancestor()
    test_advanced_main_without_ancestry_evidence_is_partial_not_rejected()
    test_diverged_main_is_true_history_obstruction()
    test_stale_local_git_does_not_block_remote_root()
    test_missing_local_observation_does_not_block_remote_root()
    test_predecessor_authority_cannot_be_reused()
    test_closed_receipt_cannot_issue_successor_authority()
    test_missing_main_observation_requests_reobservation()
    test_nonclosed_source_is_not_applicable()
    test_root_identity_changes_with_fresh_main()
    print("PASS: KuuOS Development Lineage Re-rooting v7.32")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
