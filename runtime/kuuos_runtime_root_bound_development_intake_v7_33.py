#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
from typing import Any, Mapping

from runtime.kuuos_runtime_development_mcp_capability_routing_v7_24 import (
    BLOCKED as ROUTING_BLOCKED,
    PARTIAL as ROUTING_PARTIAL,
    READY as ROUTING_READY,
    TASK_KINDS,
    route_development_mcp_task,
)

VERSION = "kuuos_runtime_root_bound_development_intake_v7_33"
SOURCE_VERSION = "kuuos_runtime_development_lineage_reroot_v7_32"
REQUEST_VERSION = "kuuos_root_bound_development_intake_request_v7_33"

READY = "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_READY"
PARTIAL = "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_PARTIAL"
OBSTRUCTED = "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_OBSTRUCTED"
NOT_APPLICABLE = "KUUOS_ROOT_BOUND_DEVELOPMENT_INTAKE_NOT_APPLICABLE"

INTAKE_READY = "root_bound_task_intake_ready"
INTAKE_READY_LOCAL_RECONCILIATION = (
    "root_bound_task_intake_ready_local_reconciliation_required"
)
INTAKE_READY_AUTHORITY_REQUIRED = (
    "root_bound_task_intake_ready_future_mutation_authority_required"
)
ROUTE_DEGRADED = "root_bound_task_intake_route_degraded"
ROOT_REOBSERVATION = "root_main_reobservation_required"
ROOT_BINDING_OBSTRUCTION = "root_binding_obstruction"
TASK_BINDING_OBSTRUCTION = "task_binding_obstruction"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")

ROOT_READY_STATES = {
    "new_lineage_root_ready_exact_closed_merge",
    "new_lineage_root_ready_descendant_main",
    "new_lineage_root_ready_local_revision_reconciliation_required",
}


@dataclass(frozen=True)
class RootBoundDevelopmentIntakeResult:
    version: str
    status: str
    packet_id: str
    intake_state: str
    task_id: str
    task_kind: str
    lineage_root_id: str
    lineage_root_main_sha: str
    target_paths: list[str]
    mutation_requested: bool
    write_authority_granted: bool
    merge_authority_granted: bool
    route_status: str
    required_fact_planes: list[str]
    local_reconciliation_required: bool
    root_reobservation_required: bool
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
) -> str:
    text = str(value or "").strip()
    if SHA64.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _commit(
    value: Any,
    name: str,
    blockers: list[str],
) -> str:
    text = str(value or "").strip().lower()
    if SHA40.fullmatch(text) is None:
        blockers.append(name + "_invalid")
    return text


def _paths(value: Any, blockers: list[str]) -> list[str]:
    if not isinstance(value, list):
        blockers.append("target_paths_not_list")
        return []
    paths: list[str] = []
    for raw in value:
        path = str(raw).strip()
        if not path:
            blockers.append("target_path_empty")
            continue
        if path.startswith("/") or path.startswith("../") or "/../" in path:
            blockers.append("target_path_outside_repository:" + path)
            continue
        paths.append(path)
    if len(paths) != len(set(paths)):
        blockers.append("target_paths_duplicate")
    return sorted(set(paths))


def build_root_bound_development_intake(
    *,
    lineage_root_packet: Mapping[str, Any],
    request: Mapping[str, Any],
    registry: Mapping[str, Any],
    environment: Mapping[str, Any],
) -> RootBoundDevelopmentIntakeResult:
    source = _m(lineage_root_packet)
    req = _m(request)
    blockers: list[str] = []
    warnings: list[str] = []

    source_digest = _sha(source)
    if source.get("version") != SOURCE_VERSION:
        blockers.append("lineage_root_packet_version_invalid")

    source_ready = bool(
        source.get("status") == "KUUOS_DEVELOPMENT_LINEAGE_REROOT_READY"
        and source.get("reroot_state") in ROOT_READY_STATES
        and str(source.get("next_lineage_root_id", "")).strip()
        and source.get("successor_write_authority_granted") is False
        and source.get("successor_merge_authority_granted") is False
    )

    root_id = str(source.get("next_lineage_root_id", "")).strip()
    root_main = str(source.get("current_main_head_sha", "")).strip().lower()

    if not source_ready:
        packet_id = "kuuos-root-bound-intake-" + _sha(
            {
                "source_digest": source_digest,
                "state": "not_applicable",
                "blockers": sorted(set(blockers)),
            }
        )[:16]
        return RootBoundDevelopmentIntakeResult(
            VERSION,
            OBSTRUCTED if blockers else NOT_APPLICABLE,
            packet_id,
            "lineage_root_not_ready",
            "",
            "",
            root_id,
            root_main,
            [],
            False,
            False,
            False,
            "",
            [],
            False,
            False,
            "return_to_v7_32_development_lineage_reroot",
            {
                "source_lineage_root_packet_digest": source_digest,
                "source_authority_transferred": False,
            },
            sorted(set(blockers)),
            warnings,
        )

    if req.get("version") != REQUEST_VERSION:
        blockers.append("request_version_invalid")

    observed_root_digest = _digest(
        req.get("source_lineage_root_packet_digest"),
        "source_lineage_root_packet_digest",
        blockers,
    )
    if observed_root_digest != source_digest:
        blockers.append("source_lineage_root_packet_digest_mismatch")

    requested_root_id = str(req.get("lineage_root_id", "")).strip()
    if requested_root_id != root_id:
        blockers.append("lineage_root_id_mismatch")

    requested_root_main = _commit(
        req.get("lineage_root_main_sha"),
        "lineage_root_main_sha",
        blockers,
    )
    if requested_root_main != root_main:
        blockers.append("lineage_root_main_sha_mismatch")

    task_id = str(req.get("task_id", "")).strip()
    task_kind = str(req.get("task_kind", "")).strip()
    if not task_id:
        blockers.append("task_id_missing")
    if task_kind not in TASK_KINDS:
        blockers.append("task_kind_invalid")

    intent_digest = _digest(
        req.get("intent_digest"),
        "intent_digest",
        blockers,
    )
    scope_digest = _digest(
        req.get("scope_digest"),
        "scope_digest",
        blockers,
    )
    target_paths = _paths(req.get("target_paths", []), blockers)

    if task_kind in {"lean_ci_repair", "local_worktree_review"} and not target_paths:
        blockers.append("target_paths_required_for_local_task")
    if task_kind == "lean_ci_repair" and target_paths:
        if not any(path.endswith(".lean") for path in target_paths):
            blockers.append("lean_ci_repair_requires_lean_target")

    mutation_requested = req.get("mutation_requested")
    if not isinstance(mutation_requested, bool):
        blockers.append("mutation_requested_must_be_bool")
        mutation_requested = False

    prior_authority_reused = req.get("prior_authority_reused")
    if prior_authority_reused is not False:
        blockers.append("prior_authority_reuse_not_allowed")
    intake_grants_authority = req.get("intake_grants_write_authority")
    if intake_grants_authority is not False:
        blockers.append("intake_may_not_grant_write_authority")

    fresh_main = _commit(
        req.get("fresh_current_main_head_sha"),
        "fresh_current_main_head_sha",
        blockers,
    )
    fresh_main_observation_digest = _digest(
        req.get("fresh_current_main_observation_digest"),
        "fresh_current_main_observation_digest",
        blockers,
    )
    root_stale = bool(fresh_main and root_main and fresh_main != root_main)

    route_request = {
        "task_id": task_id,
        "task_kind": task_kind,
        "target_path": target_paths[0] if target_paths else "",
        "provider": str(req.get("provider", "")).strip(),
        "needs_external_docs": req.get("needs_external_docs") is True,
        "needs_mcp_spec": req.get("needs_mcp_spec") is True,
        "needs_browser_diagnostics": req.get("needs_browser_diagnostics") is True,
        # Intake is route discovery only. It never asks v7.24 to grant write mode.
        "request_write": False,
    }

    routing = None
    if not blockers:
        routing = route_development_mcp_task(
            registry=registry,
            request=route_request,
            environment=environment,
        )
        if routing.status == ROUTING_BLOCKED:
            blockers.extend("routing:" + item for item in routing.blockers)

    local_reconciliation_required = bool(
        source.get("local_reconciliation_required") is True
    )

    if blockers:
        state = TASK_BINDING_OBSTRUCTION
        status = OBSTRUCTED
        next_route = "repair_task_or_root_binding"
        required_fact_planes: list[str] = []
        route_status = ROUTING_BLOCKED if routing is None else routing.status
    elif root_stale:
        state = ROOT_REOBSERVATION
        status = PARTIAL
        next_route = "reroot_again_from_fresh_current_main_before_root_bound_work"
        required_fact_planes = sorted(
            {
                str(route.get("fact_plane"))
                for route in routing.routes
                if route.get("fact_plane")
            }
        )
        route_status = routing.status
    elif routing.status == ROUTING_PARTIAL:
        state = ROUTE_DEGRADED
        status = PARTIAL
        next_route = "retain_task_intake_and_restore_required_mcp_planes"
        required_fact_planes = sorted(
            {
                str(route.get("fact_plane"))
                for route in routing.routes
                if route.get("fact_plane")
            }
        )
        route_status = routing.status
    elif local_reconciliation_required and any(
        route.get("server_id") in {"git_reference", "filesystem_reference", "lean_lsp"}
        and route.get("required") is True
        for route in routing.routes
    ):
        state = INTAKE_READY_LOCAL_RECONCILIATION
        status = READY
        next_route = "reconcile_local_git_to_root_then_observe_required_local_planes"
        required_fact_planes = sorted(
            {
                str(route.get("fact_plane"))
                for route in routing.routes
                if route.get("fact_plane")
            }
        )
        route_status = routing.status
    elif mutation_requested:
        state = INTAKE_READY_AUTHORITY_REQUIRED
        status = READY
        next_route = "observe_required_fact_planes_then_acquire_fresh_mutation_authority"
        required_fact_planes = sorted(
            {
                str(route.get("fact_plane"))
                for route in routing.routes
                if route.get("fact_plane")
            }
        )
        route_status = routing.status
    else:
        state = INTAKE_READY
        status = READY
        next_route = "observe_required_fact_planes_for_new_lineage_task"
        required_fact_planes = sorted(
            {
                str(route.get("fact_plane"))
                for route in routing.routes
                if route.get("fact_plane")
            }
        )
        route_status = routing.status

    if routing is not None:
        warnings.extend(routing.warnings)

    task_binding_digest = _sha(
        {
            "lineage_root_id": root_id,
            "lineage_root_main_sha": root_main,
            "task_id": task_id,
            "task_kind": task_kind,
            "intent_digest": intent_digest,
            "scope_digest": scope_digest,
            "target_paths": target_paths,
            "mutation_requested": mutation_requested,
            "required_fact_planes": required_fact_planes,
        }
    )

    evidence = {
        "source_lineage_root_packet_digest": source_digest,
        "lineage_root_id": root_id,
        "lineage_root_main_sha": root_main,
        "fresh_current_main_head_sha": fresh_main,
        "fresh_current_main_observation_digest": fresh_main_observation_digest,
        "root_stale_against_fresh_main": root_stale,
        "intent_digest": intent_digest,
        "scope_digest": scope_digest,
        "task_binding_digest": task_binding_digest,
        "routing_packet_digest": _sha(routing.to_dict()) if routing is not None else "",
        "routing_required_route_count": (
            routing.required_route_count if routing is not None else 0
        ),
        "routing_unavailable_required_count": (
            routing.unavailable_required_count if routing is not None else 0
        ),
        "mutation_requested": mutation_requested,
        "intake_executes_mutation": False,
        "intake_grants_write_authority": False,
        "intake_grants_merge_authority": False,
        "predecessor_authority_reused": False,
        "root_receipt_is_write_authority": False,
        "source_authority_transferred": False,
    }

    packet_id = "kuuos-root-bound-intake-" + _sha(
        {
            "source_digest": source_digest,
            "task_binding_digest": task_binding_digest,
            "state": state,
            "blockers": sorted(set(blockers)),
            "warnings": sorted(set(warnings)),
        }
    )[:16]

    return RootBoundDevelopmentIntakeResult(
        VERSION,
        status,
        packet_id,
        state,
        task_id,
        task_kind,
        root_id,
        root_main,
        target_paths,
        mutation_requested,
        False,
        False,
        route_status,
        required_fact_planes,
        local_reconciliation_required,
        root_stale,
        next_route,
        evidence,
        sorted(set(blockers)),
        sorted(set(warnings)),
    )
