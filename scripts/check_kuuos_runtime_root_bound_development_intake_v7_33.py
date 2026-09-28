#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_root_bound_development_intake_v7_33 import (
    INTAKE_READY,
    INTAKE_READY_AUTHORITY_REQUIRED,
    INTAKE_READY_LOCAL_RECONCILIATION,
    NOT_APPLICABLE,
    OBSTRUCTED,
    PARTIAL,
    READY,
    ROOT_REOBSERVATION,
    ROUTE_DEGRADED,
    TASK_BINDING_OBSTRUCTION,
    build_root_bound_development_intake,
)

REGISTRY_PATH = (
    ROOT / "manifests" / "kuuos_development_mcp_capability_registry_v7_16.json"
)
ROOT_MAIN = "a" * 40
FRESHER_MAIN = "b" * 40


def h(value) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()


def registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def environment(*, unavailable: list[str] | None = None) -> dict:
    return {
        "unavailable_server_ids": unavailable or [],
        "github_write_authority_ready": False,
        "workspace_write_authority_ready": False,
        "browser_effect_authority_ready": False,
        "mcp_orchestration_authority_ready": False,
        "vercel_write_authority_ready": False,
        "supabase_write_authority_ready": False,
        "neon_write_authority_ready": False,
        "sentry_project_configured": False,
    }


def root_packet(
    *,
    ready: bool = True,
    local_reconciliation: bool = False,
) -> dict:
    return {
        "version": "kuuos_runtime_development_lineage_reroot_v7_32",
        "status": (
            "KUUOS_DEVELOPMENT_LINEAGE_REROOT_READY"
            if ready
            else "KUUOS_DEVELOPMENT_LINEAGE_REROOT_PARTIAL"
        ),
        "packet_id": "reroot-packet",
        "repository_full_name": "itakura-hidetoshi/KuuOS",
        "predecessor_closure_packet_digest": "1" * 64,
        "predecessor_merge_commit_sha": "c" * 40,
        "current_main_head_sha": ROOT_MAIN,
        "reroot_state": (
            "new_lineage_root_ready_local_revision_reconciliation_required"
            if local_reconciliation
            else (
                "new_lineage_root_ready_exact_closed_merge"
                if ready
                else "fresh_main_reobservation_required"
            )
        ),
        "current_main_is_descendant_or_equal": ready,
        "local_head_aligned": (
            False if local_reconciliation else (True if ready else None)
        ),
        "local_reconciliation_required": local_reconciliation,
        "local_observation_required": False,
        "next_lineage_root_id": (
            "kuuos-development-lineage-root-1234567890abcdef12345678"
            if ready
            else ""
        ),
        "successor_write_authority_granted": False,
        "successor_merge_authority_granted": False,
        "next_route": (
            "use_remote_root_and_reconcile_local_git_before_remote_bound_work"
            if local_reconciliation
            else "begin_new_development_lineage_from_fresh_main_root"
        ),
        "evidence": {
            "source_closed_lineage_packet_digest": "2" * 64,
            "predecessor_merge_commit_sha": "c" * 40,
            "current_main_head_sha": ROOT_MAIN,
            "current_main_observation_digest": "3" * 64,
            "current_main_is_descendant_or_equal": ready,
            "previous_closure_receipt_reused_as_authority": False,
            "previous_merge_authority_reused": False,
            "previous_write_authority_reused": False,
            "successor_write_authority_granted": False,
            "successor_merge_authority_granted": False,
            "source_authority_transferred": False,
        },
        "blockers": [],
        "warnings": [],
    }


def request(
    src: dict,
    *,
    task_id: str = "task-001",
    task_kind: str = "lean_ci_repair",
    target_paths: list[str] | None = None,
    mutation_requested: bool = True,
    fresh_main: str = ROOT_MAIN,
    prior_authority_reused: bool = False,
) -> dict:
    if target_paths is None:
        target_paths = [
            "formal/KUOS/DependentOriginationFunctorialTransportV0_1.lean"
        ]
    return {
        "version": "kuuos_root_bound_development_intake_request_v7_33",
        "source_lineage_root_packet_digest": h(src),
        "lineage_root_id": src.get("next_lineage_root_id", ""),
        "lineage_root_main_sha": src.get("current_main_head_sha", ROOT_MAIN),
        "task_id": task_id,
        "task_kind": task_kind,
        "intent_digest": "4" * 64,
        "scope_digest": "5" * 64,
        "target_paths": target_paths,
        "mutation_requested": mutation_requested,
        "provider": "",
        "needs_external_docs": False,
        "needs_mcp_spec": False,
        "needs_browser_diagnostics": False,
        "fresh_current_main_head_sha": fresh_main,
        "fresh_current_main_observation_digest": "6" * 64,
        "prior_authority_reused": prior_authority_reused,
        "intake_grants_write_authority": False,
    }


def test_lean_mutation_intake_is_ready_but_requires_future_authority() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == READY, result.to_dict()
    assert result.intake_state == INTAKE_READY_AUTHORITY_REQUIRED
    assert result.mutation_requested is True
    assert result.write_authority_granted is False
    assert result.merge_authority_granted is False
    assert {
        "remote_ci",
        "working_bytes",
        "lean_semantics",
        "local_diff",
    }.issubset(set(result.required_fact_planes))
    assert result.evidence["intake_executes_mutation"] is False
    assert result.evidence["intake_grants_write_authority"] is False


def test_read_only_remote_observation_intake_is_ready() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(
            src,
            task_kind="remote_repository_observation",
            target_paths=[],
            mutation_requested=False,
        ),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == READY, result.to_dict()
    assert result.intake_state == INTAKE_READY
    assert result.required_fact_planes == ["remote_repository"]
    assert result.write_authority_granted is False


def test_stale_root_against_fresh_main_requests_reroot() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, fresh_main=FRESHER_MAIN),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.intake_state == ROOT_REOBSERVATION
    assert result.root_reobservation_required is True
    assert result.write_authority_granted is False


def test_local_reconciliation_root_keeps_local_task_intake_alive() -> None:
    src = root_packet(local_reconciliation=True)
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, mutation_requested=False),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == READY, result.to_dict()
    assert result.intake_state == INTAKE_READY_LOCAL_RECONCILIATION
    assert result.local_reconciliation_required is True
    assert result.next_route.startswith("reconcile_local_git_to_root")


def test_local_reconciliation_does_not_pollute_remote_only_task() -> None:
    src = root_packet(local_reconciliation=True)
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(
            src,
            task_kind="remote_repository_observation",
            target_paths=[],
            mutation_requested=False,
        ),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == READY
    assert result.intake_state == INTAKE_READY
    assert result.local_reconciliation_required is True
    assert result.required_fact_planes == ["remote_repository"]


def test_missing_required_mcp_plane_degrades_without_losing_intake() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, mutation_requested=False),
        registry=registry(),
        environment=environment(unavailable=["lean_lsp"]),
    )
    assert result.status == PARTIAL, result.to_dict()
    assert result.intake_state == ROUTE_DEGRADED
    assert result.task_id == "task-001"
    assert result.lineage_root_id == src["next_lineage_root_id"]
    assert result.write_authority_granted is False


def test_wrong_root_binding_is_obstruction() -> None:
    src = root_packet()
    req = request(src)
    req["lineage_root_id"] = "wrong-root"
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=req,
        registry=registry(),
        environment=environment(),
    )
    assert result.status == OBSTRUCTED
    assert result.intake_state == TASK_BINDING_OBSTRUCTION
    assert "lineage_root_id_mismatch" in result.blockers


def test_prior_authority_cannot_enter_new_task_intake() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, prior_authority_reused=True),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == OBSTRUCTED
    assert result.intake_state == TASK_BINDING_OBSTRUCTION
    assert "prior_authority_reuse_not_allowed" in result.blockers


def test_path_escape_is_obstructed() -> None:
    src = root_packet()
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, target_paths=["../outside.lean"]),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == OBSTRUCTED
    assert result.intake_state == TASK_BINDING_OBSTRUCTION
    assert any(item.startswith("target_path_outside_repository:") for item in result.blockers)


def test_nonready_root_is_not_applicable() -> None:
    src = root_packet(ready=False)
    result = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src),
        registry=registry(),
        environment=environment(),
    )
    assert result.status == NOT_APPLICABLE, result.to_dict()
    assert result.write_authority_granted is False


def test_task_binding_digest_changes_with_task_identity() -> None:
    src = root_packet()
    first = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, task_id="task-A"),
        registry=registry(),
        environment=environment(),
    )
    second = build_root_bound_development_intake(
        lineage_root_packet=src,
        request=request(src, task_id="task-B"),
        registry=registry(),
        environment=environment(),
    )
    assert first.status == READY
    assert second.status == READY
    assert first.evidence["task_binding_digest"] != second.evidence["task_binding_digest"]


def main() -> int:
    test_lean_mutation_intake_is_ready_but_requires_future_authority()
    test_read_only_remote_observation_intake_is_ready()
    test_stale_root_against_fresh_main_requests_reroot()
    test_local_reconciliation_root_keeps_local_task_intake_alive()
    test_local_reconciliation_does_not_pollute_remote_only_task()
    test_missing_required_mcp_plane_degrades_without_losing_intake()
    test_wrong_root_binding_is_obstruction()
    test_prior_authority_cannot_enter_new_task_intake()
    test_path_escape_is_obstructed()
    test_nonready_root_is_not_applicable()
    test_task_binding_digest_changes_with_task_identity()
    print("PASS: KuuOS Root-Bound Development Intake v7.33")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
