#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import sys

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from runtime.kuuos_runtime_root_bound_analysis_repair_readiness_v7_35 import (
    ANALYSIS_READY,
    BINDING_OBSTRUCTION,
    EFFECT_READY_AUTHORITY_PENDING,
    FACT_REOBSERVATION_REQUIRED,
    OBSTRUCTED,
    PARTIAL,
    READY,
    REPAIR_READY_AUTHORITY_PENDING,
    TASK_RECLASSIFICATION_REQUIRED,
    build_root_bound_analysis_repair_readiness,
)

ROOT_MAIN = "a" * 40
TASK_BINDING = "b" * 64
SCOPE = "c" * 64
OBS = "d" * 64


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()


def intake(
    *,
    task_kind: str = "lean_ci_repair",
    mutation_requested: bool = True,
    target_paths: list[str] | None = None,
    planes: list[str] | None = None,
) -> dict:
    if target_paths is None:
        target_paths = ["formal/KUOS/Test.lean"]
    if planes is None:
        planes = ["local_diff", "lean_semantics", "remote_ci", "working_bytes"]
    return {
        "version": "kuuos_runtime_root_bound_development_intake_v7_33",
        "status": "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_READY",
        "packet_id": "intake-packet",
        "intake_state": (
            "root_bound_task_intake_ready_future_mutation_authority_required"
            if mutation_requested
            else "root_bound_task_intake_ready"
        ),
        "task_id": "task-001",
        "task_kind": task_kind,
        "lineage_root_id": "root-001",
        "lineage_root_main_sha": ROOT_MAIN,
        "target_paths": target_paths,
        "mutation_requested": mutation_requested,
        "write_authority_granted": False,
        "merge_authority_granted": False,
        "route_status": "KUUOS_DEVELOPMENT_MCP_ROUTING_READY",
        "required_fact_planes": sorted(planes),
        "local_reconciliation_required": False,
        "root_reobservation_required": False,
        "next_route": "observe_required_fact_planes_for_new_lineage_task",
        "evidence": {
            "task_binding_digest": TASK_BINDING,
            "scope_digest": SCOPE,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def bundle(
    source: dict,
    *,
    complete: bool = True,
    coherent: bool = True,
) -> dict:
    selected = list(source["required_fact_planes"])
    fresh = list(selected) if complete else selected[:-1]
    missing = [] if complete else [selected[-1]]
    return {
        "version": "kuuos_runtime_root_bound_fact_observation_bundle_v7_34",
        "status": (
            "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_READY"
            if complete
            else "KUUOS_ROOT_BOUND_FACT_OBSERVATION_BUNDLE_PARTIAL"
        ),
        "packet_id": "bundle-packet",
        "bundle_state": (
            "root_bound_fact_bundle_complete"
            if complete
            else "root_bound_fact_bundle_missing_observations"
        ),
        "task_id": source["task_id"],
        "task_kind": source["task_kind"],
        "lineage_root_id": source["lineage_root_id"],
        "lineage_root_main_sha": source["lineage_root_main_sha"],
        "selected_fact_planes": selected,
        "fresh_fact_planes": fresh,
        "missing_fact_planes": missing,
        "stale_fact_planes": [],
        "target_paths": list(source["target_paths"]),
        "lean_filesystem_coherent": (
            coherent
            if {"working_bytes", "lean_semantics"}.issubset(set(selected))
            else None
        ),
        "task_candidate_retained": True,
        "mutation_executed": False,
        "write_authority_granted": False,
        "next_route": (
            "derive_task_specific_readiness_from_complete_fact_bundle"
            if complete
            else "collect_missing_root_bound_fact_observations"
        ),
        "evidence": {
            "source_intake_packet_digest": h(source),
            "task_binding_digest": source["evidence"]["task_binding_digest"],
            "scope_digest": source["evidence"]["scope_digest"],
            "normalized_observations_digest": OBS,
            "selected_fact_planes": selected,
            "fresh_fact_planes": fresh,
            "missing_fact_planes": missing,
            "stale_fact_planes": [],
            "lean_filesystem_coherent": coherent,
            "observation_bundle_executes_mutation": False,
            "observation_bundle_grants_write_authority": False,
            "observation_bundle_grants_merge_authority": False,
            "task_candidate_retained": True,
            "raw_provider_payloads_persisted": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def test_lean_repair_requests_only_fresh_workspace_authority() -> None:
    i = intake(mutation_requested=True)
    b = bundle(i)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == READY, result.to_dict()
    assert result.readiness_state == REPAIR_READY_AUTHORITY_PENDING
    assert result.analysis_ready is True
    assert result.repair_planning_ready is True
    assert result.effect_requested is True
    assert result.effect_required is True
    assert result.effect_class == "workspace_source_edit"
    assert result.fresh_authority_required is True
    assert result.requested_authority_class == "workspace_write_authority"
    assert result.mutation_executed is False
    assert result.write_authority_granted is False
    assert result.merge_authority_granted is False


def test_lean_analysis_only_needs_no_authority() -> None:
    i = intake(mutation_requested=False)
    b = bundle(i)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == READY, result.to_dict()
    assert result.readiness_state == ANALYSIS_READY
    assert result.analysis_ready is True
    assert result.repair_planning_ready is True
    assert result.effect_requested is False
    assert result.effect_required is False
    assert result.fresh_authority_required is False
    assert result.requested_authority_class == ""
    assert result.next_route == "derive_bounded_local_repair_plan_without_mutation"


def test_analysis_only_task_with_mutation_intent_reclassifies_without_authority() -> None:
    i = intake(
        task_kind="external_library_docs",
        mutation_requested=True,
        target_paths=[],
        planes=["external_docs"],
    )
    b = bundle(i)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.readiness_state == TASK_RECLASSIFICATION_REQUIRED
    assert result.analysis_ready is True
    assert result.effect_requested is True
    assert result.effect_required is False
    assert result.fresh_authority_required is False
    assert result.requested_authority_class == ""
    assert "mutation_intent_present_on_analysis_only_task_kind" in result.warnings


def test_remote_repository_effect_uses_github_authority_class() -> None:
    i = intake(
        task_kind="remote_repository_observation",
        mutation_requested=True,
        target_paths=[],
        planes=["remote_repository"],
    )
    b = bundle(i)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == READY, result.to_dict()
    assert result.readiness_state == EFFECT_READY_AUTHORITY_PENDING
    assert result.effect_class == "github_remote_mutation"
    assert result.requested_authority_class == "github_write_authority"
    assert result.fresh_authority_required is True
    assert result.evidence["authority_requested_only_if_effect_required"] is True


def test_incomplete_fact_bundle_remains_partial_without_authority_request() -> None:
    i = intake(mutation_requested=True)
    b = bundle(i, complete=False)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.readiness_state == FACT_REOBSERVATION_REQUIRED
    assert result.analysis_ready is False
    assert result.effect_required is False
    assert result.fresh_authority_required is False
    assert result.task_candidate_retained is True
    assert result.next_route == "collect_missing_root_bound_fact_observations"


def test_lean_filesystem_semantic_mismatch_returns_to_reobservation() -> None:
    i = intake(mutation_requested=True)
    b = bundle(i, complete=True, coherent=False)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.readiness_state == FACT_REOBSERVATION_REQUIRED
    assert result.fresh_authority_required is False
    assert "lean_filesystem_semantics_require_reobservation" in result.warnings


def test_wrong_intake_digest_is_binding_obstruction() -> None:
    i = intake()
    b = bundle(i)
    b["evidence"]["source_intake_packet_digest"] = "e" * 64
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == OBSTRUCTED, result.to_dict()
    assert result.readiness_state == BINDING_OBSTRUCTION
    assert "fact_bundle_source_intake_digest_mismatch" in result.blockers
    assert result.fresh_authority_required is False


def test_bundle_cannot_smuggle_write_or_merge_authority() -> None:
    i = intake()
    b = bundle(i)
    b["write_authority_granted"] = True
    b["evidence"]["observation_bundle_grants_merge_authority"] = True
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == OBSTRUCTED
    assert "fact_bundle_write_authority_boundary_invalid" in result.blockers
    assert "fact_bundle_merge_authority_boundary_invalid" in result.blockers
    assert result.mutation_executed is False
    assert result.write_authority_granted is False
    assert result.merge_authority_granted is False


def test_database_effect_requests_provider_specific_authority_class() -> None:
    i = intake(
        task_kind="database_debugging",
        mutation_requested=True,
        target_paths=[],
        planes=["database"],
    )
    b = bundle(i)
    result = build_root_bound_analysis_repair_readiness(
        intake_packet=i,
        fact_bundle_packet=b,
    )
    assert result.status == READY
    assert result.readiness_state == EFFECT_READY_AUTHORITY_PENDING
    assert result.effect_class == "database_provider_effect"
    assert result.requested_authority_class == "database_provider_write_authority"


def main() -> int:
    test_lean_repair_requests_only_fresh_workspace_authority()
    test_lean_analysis_only_needs_no_authority()
    test_analysis_only_task_with_mutation_intent_reclassifies_without_authority()
    test_remote_repository_effect_uses_github_authority_class()
    test_incomplete_fact_bundle_remains_partial_without_authority_request()
    test_lean_filesystem_semantic_mismatch_returns_to_reobservation()
    test_wrong_intake_digest_is_binding_obstruction()
    test_bundle_cannot_smuggle_write_or_merge_authority()
    test_database_effect_requests_provider_specific_authority_class()
    print("PASS: KuuOS Root-Bound Analysis/Repair Readiness v7.35")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
