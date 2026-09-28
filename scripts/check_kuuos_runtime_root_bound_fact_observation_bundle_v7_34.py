#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_root_bound_fact_observation_bundle_v7_34 import (
    BINDING_OBSTRUCTION,
    BUNDLE_COMPLETE,
    MISSING_OBSERVATIONS,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    ROOT_REOBSERVATION,
    SEMANTIC_REOBSERVATION,
    build_root_bound_fact_observation_bundle,
)

ROOT_MAIN = "a" * 40
NEW_MAIN = "b" * 40
TARGET = "formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean"
FS = "1" * 64
LEAN_RESULT = "2" * 64


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def intake(*, applicable: bool = True, degraded: bool = False) -> dict:
    state = (
        "root_bound_task_intake_route_degraded"
        if degraded
        else "root_bound_task_intake_ready_future_mutation_authority_required"
    )
    return {
        "version": "kuuos_runtime_root_bound_development_intake_v7_33",
        "status": (
            "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_PARTIAL"
            if degraded
            else (
                "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_READY"
                if applicable
                else "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_OBSTRUCTED"
            )
        ),
        "packet_id": "intake-001",
        "intake_state": state if applicable else "task_binding_obstruction",
        "task_id": "task-001",
        "task_kind": "lean_ci_repair",
        "lineage_root_id": "kuuos-development-lineage-root-1234567890abcdef12345678",
        "lineage_root_main_sha": ROOT_MAIN,
        "target_paths": [TARGET],
        "mutation_requested": True,
        "write_authority_granted": False,
        "merge_authority_granted": False,
        "route_status": (
            "KUUOS_DEVELOPMENT_MCP_ROUTING_BLOCKED"
            if degraded
            else "KUUOS_DEVELOPMENT_MCP_ROUTING_READY"
        ),
        "required_fact_planes": [
            "lean_semantics",
            "local_diff",
            "remote_ci",
            "working_bytes",
        ],
        "local_reconciliation_required": False,
        "root_reobservation_required": False,
        "next_route": "observe_required_fact_planes_then_acquire_fresh_mutation_authority",
        "evidence": {
            "source_lineage_root_packet_digest": "3" * 64,
            "lineage_root_id": "kuuos-development-lineage-root-1234567890abcdef12345678",
            "lineage_root_main_sha": ROOT_MAIN,
            "fresh_current_main_head_sha": ROOT_MAIN,
            "fresh_current_main_observation_digest": "4" * 64,
            "root_stale_against_fresh_main": False,
            "intent_digest": "5" * 64,
            "scope_digest": "6" * 64,
            "task_binding_digest": "7" * 64,
            "routing_packet_digest": "8" * 64,
            "routing_required_route_count": 4,
            "routing_unavailable_required_count": 1 if degraded else 0,
            "mutation_requested": True,
            "intake_executes_mutation": False,
            "intake_grants_write_authority": False,
            "intake_grants_merge_authority": False,
            "predecessor_authority_reused": False,
            "root_receipt_is_write_authority": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def observation(
    plane: str,
    provider: str,
    *,
    target: str = "",
    fresh: bool = True,
    observed_head: str = ROOT_MAIN,
    content_digest: str = "",
    semantic_source_digest: str = "",
    semantic_result_digest: str = "",
) -> dict:
    return {
        "fact_plane": plane,
        "provider_id": provider,
        "target_path": target,
        "bound_root_main_sha": ROOT_MAIN,
        "observed_head_sha": observed_head,
        "fresh": fresh,
        "observation_digest": h(
            {
                "plane": plane,
                "provider": provider,
                "target": target,
                "fresh": fresh,
                "head": observed_head,
                "content": content_digest,
                "semantic_source": semantic_source_digest,
            }
        ),
        "freshness_binding_digest": h(
            {
                "root": ROOT_MAIN,
                "plane": plane,
                "target": target,
                "fresh": fresh,
            }
        ),
        "content_digest": content_digest,
        "semantic_source_content_digest": semantic_source_digest,
        "semantic_result_digest": semantic_result_digest,
        "raw_payload_persisted": False,
        "source_authority_transferred": False,
    }


def full_observations(*, lean_source: str = FS) -> list[dict]:
    return [
        observation(
            "remote_ci",
            "github_official",
            observed_head=ROOT_MAIN,
        ),
        observation(
            "working_bytes",
            "filesystem_reference",
            target=TARGET,
            observed_head=ROOT_MAIN,
            content_digest=FS,
        ),
        observation(
            "lean_semantics",
            "lean_lsp",
            target=TARGET,
            observed_head=ROOT_MAIN,
            semantic_source_digest=lean_source,
            semantic_result_digest=LEAN_RESULT,
        ),
        observation(
            "local_diff",
            "git_reference",
            target=TARGET,
            observed_head=ROOT_MAIN,
        ),
    ]


def packet(src: dict, observations: list[dict], *, fresh_main: str = ROOT_MAIN) -> dict:
    return {
        "version": "kuuos_root_bound_fact_observations_v7_34",
        "source_intake_packet_digest": h(src),
        "task_id": src["task_id"],
        "lineage_root_id": src["lineage_root_id"],
        "lineage_root_main_sha": src["lineage_root_main_sha"],
        "task_binding_digest": src["evidence"]["task_binding_digest"],
        "scope_digest": src["evidence"]["scope_digest"],
        "fresh_current_main_head_sha": fresh_main,
        "fresh_current_main_observation_digest": "9" * 64,
        "observations": observations,
    }


def test_complete_bundle_is_ready_and_non_authoritative() -> None:
    src = intake()
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, full_observations()),
    )
    assert result.status == READY, result.to_dict()
    assert result.bundle_state == BUNDLE_COMPLETE
    assert result.missing_fact_planes == []
    assert result.stale_fact_planes == []
    assert result.lean_filesystem_coherent is True
    assert result.task_candidate_retained is True
    assert result.mutation_executed is False
    assert result.write_authority_granted is False
    assert result.evidence["observation_bundle_grants_merge_authority"] is False


def test_missing_observation_is_partial_and_task_retained() -> None:
    src = intake()
    observations = [
        item for item in full_observations()
        if item["fact_plane"] != "remote_ci"
    ]
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, observations),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.bundle_state == MISSING_OBSERVATIONS
    assert result.missing_fact_planes == ["remote_ci"]
    assert result.task_candidate_retained is True


def test_stale_provider_observation_is_partial_when_explicitly_marked_stale() -> None:
    src = intake()
    observations = full_observations()
    for item in observations:
        if item["fact_plane"] == "remote_ci":
            item["fresh"] = False
            item["observed_head_sha"] = NEW_MAIN
            item["observation_digest"] = h(item)
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, observations),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.bundle_state == MISSING_OBSERVATIONS
    assert "remote_ci" in result.stale_fact_planes
    assert "remote_ci" in result.missing_fact_planes


def test_claimed_fresh_observation_from_wrong_head_is_obstruction() -> None:
    src = intake()
    observations = full_observations()
    for item in observations:
        if item["fact_plane"] == "remote_ci":
            item["observed_head_sha"] = NEW_MAIN
            item["observation_digest"] = h(item)
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, observations),
    )
    assert result.status == OBSTRUCTED, result.to_dict()
    assert result.bundle_state == BINDING_OBSTRUCTION
    assert any("fresh_head_mismatch" in item for item in result.blockers)


def test_lean_filesystem_digest_mismatch_requests_semantic_reobservation() -> None:
    src = intake()
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(
            src,
            full_observations(lean_source="f" * 64),
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.bundle_state == SEMANTIC_REOBSERVATION
    assert result.lean_filesystem_coherent is False
    assert any(
        item == "lean_semantic_source_stale:" + TARGET
        for item in result.warnings
    )


def test_current_main_move_returns_to_reroot_without_discarding_task() -> None:
    src = intake()
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(
            src,
            full_observations(),
            fresh_main=NEW_MAIN,
        ),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.bundle_state == ROOT_REOBSERVATION
    assert result.task_candidate_retained is True
    assert result.write_authority_granted is False


def test_wrong_task_binding_is_obstruction() -> None:
    src = intake()
    p = packet(src, full_observations())
    p["task_binding_digest"] = "0" * 64
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=p,
    )
    assert result.status == OBSTRUCTED
    assert result.bundle_state == BINDING_OBSTRUCTION
    assert "task_binding_digest_mismatch" in result.blockers


def test_observation_for_unselected_plane_is_obstruction() -> None:
    src = intake()
    observations = full_observations()
    observations.append(
        observation("external_docs", "context7", observed_head="")
    )
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, observations),
    )
    assert result.status == OBSTRUCTED
    assert result.bundle_state == BINDING_OBSTRUCTION
    assert any("unselected_fact_plane:external_docs" in item for item in result.blockers)


def test_raw_provider_payload_boundary_is_enforced() -> None:
    src = intake()
    observations = full_observations()
    observations[0]["raw_payload_persisted"] = True
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, observations),
    )
    assert result.status == OBSTRUCTED
    assert result.bundle_state == BINDING_OBSTRUCTION
    assert any("raw_payload_boundary_invalid" in item for item in result.blockers)


def test_route_degraded_intake_can_be_completed_after_provider_recovers() -> None:
    src = intake(degraded=True)
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, full_observations()),
    )
    assert result.status == READY, result.to_dict()
    assert result.bundle_state == BUNDLE_COMPLETE
    assert result.task_candidate_retained is True


def test_nonapplicable_intake_remains_nonapplicable() -> None:
    src = intake(applicable=False)
    result = build_root_bound_fact_observation_bundle(
        intake_packet=src,
        observations_packet=packet(src, []),
    )
    assert result.status == NOT_APPLICABLE, result.to_dict()
    assert result.task_candidate_retained is True


def main() -> int:
    test_complete_bundle_is_ready_and_non_authoritative()
    test_missing_observation_is_partial_and_task_retained()
    test_stale_provider_observation_is_partial_when_explicitly_marked_stale()
    test_claimed_fresh_observation_from_wrong_head_is_obstruction()
    test_lean_filesystem_digest_mismatch_requests_semantic_reobservation()
    test_current_main_move_returns_to_reroot_without_discarding_task()
    test_wrong_task_binding_is_obstruction()
    test_observation_for_unselected_plane_is_obstruction()
    test_raw_provider_payload_boundary_is_enforced()
    test_route_degraded_intake_can_be_completed_after_provider_recovers()
    test_nonapplicable_intake_remains_nonapplicable()
    print("PASS: KuuOS Root-Bound Fact Observation Bundle v7.34")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
