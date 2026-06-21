from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_multi_loop_operational_circulation_types_v0_28 import (
    APPLY_RESULT_VERSION,
    ASSESSMENT_VERSION,
    CONTRACT_VERSION,
    CONTROL_COMMANDS,
    CONTROL_VERSION,
    EDGE_KINDS,
    EDGE_VERSION,
    EVENT_KINDS,
    EVENT_VERSION,
    INTERFERENCE_CLASSES,
    LOOP_MODES,
    LOOP_VERSION,
    NETWORK_MODES,
    NON_AUTHORITY_FLAGS,
    REPAIR_ROUTES,
    REPAIR_VERSION,
    REQUIRED_BOUNDARY,
    SEVERITIES,
    STATE_VERSION,
    apply_result_digest,
    assessment_digest,
    contract_digest,
    control_digest,
    copy_boundary,
    copy_non_authority,
    edge_digest,
    event_digest,
    loop_digest,
    nonnegative_int_map,
    positive_int_map,
    repair_digest,
    require_bool,
    require_nonnegative_int,
    require_positive_int,
    require_string,
    state_digest,
    unique_strings,
)


def build_network_contract(
    *,
    contract_id: str,
    lineage_id: str,
    v027_schema_digest: str,
    resource_capacities: Mapping[str, int],
    max_loops: int,
    max_edges: int,
    max_assessments_per_epoch: int,
    max_repair_candidates: int,
    max_circulation_rounds: int,
    epoch_duration_ms: int,
    external_control_policy_digest: str,
    audit_policy_digest: str,
    created_at_ms: int,
) -> dict[str, Any]:
    packet = {
        "version": CONTRACT_VERSION,
        "contract_id": require_string(contract_id, "contract_id"),
        "lineage_id": require_string(lineage_id, "lineage_id"),
        "v027_schema_digest": require_string(v027_schema_digest, "v027_schema_digest"),
        "resource_capacities": positive_int_map(
            resource_capacities, "resource_capacities"
        ),
        "max_loops": require_positive_int(max_loops, "max_loops"),
        "max_edges": require_positive_int(max_edges, "max_edges"),
        "max_assessments_per_epoch": require_positive_int(
            max_assessments_per_epoch, "max_assessments_per_epoch"
        ),
        "max_repair_candidates": require_positive_int(
            max_repair_candidates, "max_repair_candidates"
        ),
        "max_circulation_rounds": require_positive_int(
            max_circulation_rounds, "max_circulation_rounds"
        ),
        "epoch_duration_ms": require_positive_int(
            epoch_duration_ms, "epoch_duration_ms"
        ),
        "external_control_policy_digest": require_string(
            external_control_policy_digest, "external_control_policy_digest"
        ),
        "audit_policy_digest": require_string(
            audit_policy_digest, "audit_policy_digest"
        ),
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "finite_network_contract": True,
        "external_arbitration_required": True,
        "automatic_loop_dispatch": False,
        "automatic_license_transfer": False,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "multi_loop_contract_digest": "",
    }
    packet["multi_loop_contract_digest"] = contract_digest(packet)
    errors = validate_network_contract(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_network_contract(contract: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if contract.get("version") != CONTRACT_VERSION:
            errors.append("multi_loop_contract_version_invalid")
        for field in (
            "contract_id",
            "lineage_id",
            "v027_schema_digest",
            "external_control_policy_digest",
            "audit_policy_digest",
        ):
            require_string(contract.get(field), field)
        positive_int_map(contract.get("resource_capacities"), "resource_capacities")
        for field in (
            "max_loops",
            "max_edges",
            "max_assessments_per_epoch",
            "max_repair_candidates",
            "max_circulation_rounds",
            "epoch_duration_ms",
        ):
            require_positive_int(contract.get(field), field)
        require_nonnegative_int(contract.get("created_at_ms"), "created_at_ms")
        if contract.get("finite_network_contract") is not True:
            errors.append("multi_loop_finite_network_required")
        if contract.get("external_arbitration_required") is not True:
            errors.append("multi_loop_external_arbitration_required")
        if contract.get("automatic_loop_dispatch") is not False:
            errors.append("multi_loop_automatic_dispatch_forbidden")
        if contract.get("automatic_license_transfer") is not False:
            errors.append("multi_loop_automatic_license_transfer_forbidden")
        if dict(contract.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("multi_loop_contract_authority_expansion")
        if dict(contract.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("multi_loop_contract_boundary_invalid")
        if contract.get("multi_loop_contract_digest") != contract_digest(contract):
            errors.append("multi_loop_contract_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_loop_binding(
    *,
    network_contract: Mapping[str, Any],
    loop_id: str,
    mission_id: str,
    v027_contract_digest: str,
    v027_state_digest: str,
    mode: str,
    completed_cycles: int,
    lease_sequence: int,
    lease_cycles_remaining: int,
    resource_claims: Mapping[str, int],
    effect_scopes: list[str],
    evidence_produces: list[str],
    evidence_consumes: list[str],
    control_priority: int,
    observed_at_ms: int,
) -> dict[str, Any]:
    contract_errors = validate_network_contract(network_contract)
    if contract_errors:
        raise ValueError("network_contract_invalid:" + ";".join(contract_errors))
    normalized_mode = require_string(mode, "mode")
    if normalized_mode not in LOOP_MODES:
        raise ValueError("multi_loop_mode_invalid")
    claims = nonnegative_int_map(resource_claims, "resource_claims", allow_empty=True)
    capacities = network_contract["resource_capacities"]
    unknown_resources = sorted(set(claims) - set(capacities))
    if unknown_resources:
        raise ValueError("multi_loop_unknown_resource:" + ",".join(unknown_resources))
    packet = {
        "version": LOOP_VERSION,
        "network_contract_digest": network_contract["multi_loop_contract_digest"],
        "loop_id": require_string(loop_id, "loop_id"),
        "mission_id": require_string(mission_id, "mission_id"),
        "v027_contract_digest": require_string(
            v027_contract_digest, "v027_contract_digest"
        ),
        "v027_state_digest": require_string(v027_state_digest, "v027_state_digest"),
        "mode": normalized_mode,
        "completed_cycles": require_nonnegative_int(
            completed_cycles, "completed_cycles"
        ),
        "lease_sequence": require_nonnegative_int(lease_sequence, "lease_sequence"),
        "lease_cycles_remaining": require_nonnegative_int(
            lease_cycles_remaining, "lease_cycles_remaining"
        ),
        "resource_claims": claims,
        "effect_scopes": sorted(
            unique_strings(effect_scopes, "effect_scopes", allow_empty=True)
        ),
        "evidence_produces": sorted(
            unique_strings(
                evidence_produces, "evidence_produces", allow_empty=True
            )
        ),
        "evidence_consumes": sorted(
            unique_strings(
                evidence_consumes, "evidence_consumes", allow_empty=True
            )
        ),
        "control_priority": require_nonnegative_int(
            control_priority, "control_priority"
        ),
        "observed_at_ms": require_nonnegative_int(observed_at_ms, "observed_at_ms"),
        "v027_state_preserved": True,
        "network_mutates_loop": False,
        "license_transfer_performed": False,
        "non_authority": copy_non_authority(),
        "multi_loop_binding_digest": "",
    }
    packet["multi_loop_binding_digest"] = loop_digest(packet)
    errors = validate_loop_binding(packet, network_contract)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_loop_binding(
    binding: Mapping[str, Any], network_contract: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if binding.get("version") != LOOP_VERSION:
            errors.append("multi_loop_binding_version_invalid")
        if binding.get("network_contract_digest") != network_contract.get(
            "multi_loop_contract_digest"
        ):
            errors.append("multi_loop_binding_contract_mismatch")
        for field in (
            "loop_id",
            "mission_id",
            "v027_contract_digest",
            "v027_state_digest",
        ):
            require_string(binding.get(field), field)
        if binding.get("mode") not in LOOP_MODES:
            errors.append("multi_loop_binding_mode_invalid")
        for field in (
            "completed_cycles",
            "lease_sequence",
            "lease_cycles_remaining",
            "control_priority",
            "observed_at_ms",
        ):
            require_nonnegative_int(binding.get(field), field)
        claims = nonnegative_int_map(
            binding.get("resource_claims"), "resource_claims", allow_empty=True
        )
        if set(claims) - set(network_contract.get("resource_capacities", {})):
            errors.append("multi_loop_binding_unknown_resource")
        for field in ("effect_scopes", "evidence_produces", "evidence_consumes"):
            unique_strings(binding.get(field), field, allow_empty=True)
        if binding.get("v027_state_preserved") is not True:
            errors.append("multi_loop_v027_state_preservation_required")
        if binding.get("network_mutates_loop") is not False:
            errors.append("multi_loop_direct_loop_mutation_forbidden")
        if binding.get("license_transfer_performed") is not False:
            errors.append("multi_loop_license_transfer_forbidden")
        if dict(binding.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("multi_loop_binding_authority_expansion")
        if binding.get("multi_loop_binding_digest") != loop_digest(binding):
            errors.append("multi_loop_binding_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_edge(
    *,
    state: Mapping[str, Any],
    edge_id: str,
    source_loop_id: str,
    target_loop_id: str,
    kind: str,
    subject: str,
    directed: bool,
    evidence_digest: str,
    expires_at_ms: int,
    created_at_ms: int,
) -> dict[str, Any]:
    normalized_kind = require_string(kind, "kind")
    if normalized_kind not in EDGE_KINDS:
        raise ValueError("multi_loop_edge_kind_invalid")
    source = require_string(source_loop_id, "source_loop_id")
    target = require_string(target_loop_id, "target_loop_id")
    if source == target:
        raise ValueError("multi_loop_self_edge_forbidden")
    if source not in state.get("loops", {}) or target not in state.get("loops", {}):
        raise ValueError("multi_loop_edge_endpoint_missing")
    created = require_nonnegative_int(created_at_ms, "created_at_ms")
    expiry = require_positive_int(expires_at_ms, "expires_at_ms")
    if expiry <= created:
        raise ValueError("multi_loop_edge_expiry_invalid")
    packet = {
        "version": EDGE_VERSION,
        "network_contract_digest": state["contract_digest"],
        "source_state_digest": state["multi_loop_state_digest"],
        "edge_id": require_string(edge_id, "edge_id"),
        "source_loop_id": source,
        "target_loop_id": target,
        "kind": normalized_kind,
        "subject": require_string(subject, "subject"),
        "directed": require_bool(directed, "directed"),
        "evidence_digest": require_string(evidence_digest, "evidence_digest"),
        "expires_at_ms": expiry,
        "created_at_ms": created,
        "grants_cross_loop_authority": False,
        "transfers_license": False,
        "multi_loop_edge_digest": "",
    }
    packet["multi_loop_edge_digest"] = edge_digest(packet)
    return packet


def validate_edge(edge: Mapping[str, Any], state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if edge.get("version") != EDGE_VERSION:
            errors.append("multi_loop_edge_version_invalid")
        if edge.get("network_contract_digest") != state.get("contract_digest"):
            errors.append("multi_loop_edge_contract_mismatch")
        if edge.get("source_state_digest") != state.get("multi_loop_state_digest"):
            errors.append("multi_loop_edge_state_stale")
        for field in (
            "edge_id",
            "source_loop_id",
            "target_loop_id",
            "subject",
            "evidence_digest",
        ):
            require_string(edge.get(field), field)
        if edge.get("source_loop_id") == edge.get("target_loop_id"):
            errors.append("multi_loop_self_edge_forbidden")
        if edge.get("source_loop_id") not in state.get("loops", {}):
            errors.append("multi_loop_edge_source_missing")
        if edge.get("target_loop_id") not in state.get("loops", {}):
            errors.append("multi_loop_edge_target_missing")
        if edge.get("kind") not in EDGE_KINDS:
            errors.append("multi_loop_edge_kind_invalid")
        require_bool(edge.get("directed"), "directed")
        created = require_nonnegative_int(edge.get("created_at_ms"), "created_at_ms")
        expiry = require_positive_int(edge.get("expires_at_ms"), "expires_at_ms")
        if expiry <= created:
            errors.append("multi_loop_edge_expiry_invalid")
        if edge.get("grants_cross_loop_authority") is not False:
            errors.append("multi_loop_edge_authority_forbidden")
        if edge.get("transfers_license") is not False:
            errors.append("multi_loop_edge_license_transfer_forbidden")
        if edge.get("multi_loop_edge_digest") != edge_digest(edge):
            errors.append("multi_loop_edge_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_initial_state(
    *, network_contract: Mapping[str, Any], initialized_at_ms: int
) -> dict[str, Any]:
    errors = validate_network_contract(network_contract)
    if errors:
        raise ValueError("network_contract_invalid:" + ";".join(errors))
    now = require_nonnegative_int(initialized_at_ms, "initialized_at_ms")
    state = {
        "version": STATE_VERSION,
        "contract": deepcopy(dict(network_contract)),
        "contract_digest": network_contract["multi_loop_contract_digest"],
        "lineage_id": network_contract["lineage_id"],
        "mode": "ACTIVE",
        "epoch": 0,
        "epoch_started_at_ms": now,
        "loops": {},
        "edges": {},
        "assessment_summaries": [],
        "repair_summaries": [],
        "latest_assessment_digest": "",
        "latest_assessment_class": "NONE",
        "latest_repair_digest": "",
        "processed_event_digests": [],
        "event_history": [],
        "event_index": 0,
        "updated_at_ms": now,
        "foreground_control_available": True,
        "automatic_loop_dispatch_performed": False,
        "automatic_license_transfer_performed": False,
        "direct_loop_mutation_performed": False,
        "history_append_only": True,
        "audit_preserved": True,
        "provenance_preserved": True,
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "multi_loop_state_digest": "",
    }
    state["multi_loop_state_digest"] = state_digest(state)
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("initial_state_invalid:" + ";".join(state_errors))
    return state


def validate_state(state: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if state.get("version") != STATE_VERSION:
            errors.append("multi_loop_state_version_invalid")
        contract = state.get("contract")
        if not isinstance(contract, Mapping):
            errors.append("multi_loop_state_contract_missing")
        else:
            errors.extend("contract:" + item for item in validate_network_contract(contract))
            if state.get("contract_digest") != contract.get("multi_loop_contract_digest"):
                errors.append("multi_loop_state_contract_digest_mismatch")
        if state.get("mode") not in NETWORK_MODES:
            errors.append("multi_loop_state_mode_invalid")
        for field in ("epoch", "epoch_started_at_ms", "event_index", "updated_at_ms"):
            require_nonnegative_int(state.get(field), field)
        loops = state.get("loops")
        edges = state.get("edges")
        if not isinstance(loops, Mapping):
            errors.append("multi_loop_state_loops_invalid")
            loops = {}
        if not isinstance(edges, Mapping):
            errors.append("multi_loop_state_edges_invalid")
            edges = {}
        if isinstance(contract, Mapping):
            if len(loops) > int(contract.get("max_loops", 0)):
                errors.append("multi_loop_state_loop_cap_exceeded")
            if len(edges) > int(contract.get("max_edges", 0)):
                errors.append("multi_loop_state_edge_cap_exceeded")
            for loop_id, binding in loops.items():
                if loop_id != binding.get("loop_id"):
                    errors.append("multi_loop_state_loop_key_mismatch")
                errors.extend(
                    f"loop:{loop_id}:{item}"
                    for item in validate_loop_binding(binding, contract)
                )
        for edge_id, edge in edges.items():
            if edge_id != edge.get("edge_id"):
                errors.append("multi_loop_state_edge_key_mismatch")
            if edge.get("source_loop_id") not in loops or edge.get("target_loop_id") not in loops:
                errors.append("multi_loop_state_edge_endpoint_missing")
            if edge.get("multi_loop_edge_digest") != edge_digest(edge):
                errors.append("multi_loop_state_edge_digest_invalid")
        for field in (
            "assessment_summaries",
            "repair_summaries",
            "processed_event_digests",
            "event_history",
        ):
            if not isinstance(state.get(field), list):
                errors.append(f"multi_loop_state_{field}_invalid")
        processed = list(state.get("processed_event_digests", []))
        if len(processed) != len(set(processed)):
            errors.append("multi_loop_state_processed_event_duplicate")
        if len(list(state.get("event_history", []))) != int(state.get("event_index", -1)):
            errors.append("multi_loop_state_event_count_mismatch")
        for field in (
            "foreground_control_available",
            "automatic_loop_dispatch_performed",
            "automatic_license_transfer_performed",
            "direct_loop_mutation_performed",
            "history_append_only",
            "audit_preserved",
            "provenance_preserved",
        ):
            require_bool(state.get(field), field)
        if state.get("foreground_control_available") is not True:
            errors.append("multi_loop_foreground_control_required")
        if state.get("automatic_loop_dispatch_performed") is not False:
            errors.append("multi_loop_automatic_dispatch_forbidden")
        if state.get("automatic_license_transfer_performed") is not False:
            errors.append("multi_loop_license_transfer_forbidden")
        if state.get("direct_loop_mutation_performed") is not False:
            errors.append("multi_loop_direct_loop_mutation_forbidden")
        if state.get("history_append_only") is not True:
            errors.append("multi_loop_history_append_only_required")
        if state.get("audit_preserved") is not True:
            errors.append("multi_loop_audit_preservation_required")
        if state.get("provenance_preserved") is not True:
            errors.append("multi_loop_provenance_preservation_required")
        if dict(state.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("multi_loop_state_authority_expansion")
        if dict(state.get("boundary", {})) != REQUIRED_BOUNDARY:
            errors.append("multi_loop_state_boundary_invalid")
        if state.get("latest_assessment_class") not in INTERFERENCE_CLASSES:
            errors.append("multi_loop_latest_assessment_class_invalid")
        if state.get("multi_loop_state_digest") != state_digest(state):
            errors.append("multi_loop_state_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _active_loop_ids(state: Mapping[str, Any]) -> list[str]:
    return sorted(
        loop_id
        for loop_id, binding in state.get("loops", {}).items()
        if binding.get("mode") == "ACTIVE"
    )


def _live_edges(state: Mapping[str, Any], now_ms: int) -> list[Mapping[str, Any]]:
    return sorted(
        (
            edge
            for edge in state.get("edges", {}).values()
            if int(edge.get("expires_at_ms", 0)) > now_ms
        ),
        key=lambda edge: str(edge.get("edge_id", "")),
    )


def _wait_cycle_nodes(
    active: set[str], dependency_edges: list[Mapping[str, Any]]
) -> list[str]:
    adjacency: dict[str, list[str]] = {loop_id: [] for loop_id in active}
    for edge in dependency_edges:
        source = str(edge["source_loop_id"])
        target = str(edge["target_loop_id"])
        if source in active and target in active:
            adjacency[source].append(target)
            if edge.get("directed") is False:
                adjacency[target].append(source)
    for source in adjacency:
        adjacency[source] = sorted(set(adjacency[source]))

    def reaches_start(start: str, current: str, visited: set[str]) -> bool:
        if current in visited:
            return False
        visited.add(current)
        for target in adjacency.get(current, []):
            if target == start:
                return True
            if reaches_start(start, target, visited):
                return True
        return False

    return sorted(
        loop_id
        for loop_id in active
        if any(
            target == loop_id or reaches_start(loop_id, target, {loop_id})
            for target in adjacency.get(loop_id, [])
        )
    )


def _diagnose(state: Mapping[str, Any], now_ms: int) -> dict[str, Any]:
    active_ids = _active_loop_ids(state)
    active = set(active_ids)
    contract = state["contract"]
    capacities = contract["resource_capacities"]
    resource_contentions: list[dict[str, Any]] = []
    for resource in sorted(capacities):
        claims = {
            loop_id: int(state["loops"][loop_id].get("resource_claims", {}).get(resource, 0))
            for loop_id in active_ids
        }
        used = sum(claims.values())
        capacity = int(capacities[resource])
        if used > capacity:
            resource_contentions.append(
                {
                    "resource": resource,
                    "used": used,
                    "capacity": capacity,
                    "loop_ids": sorted(loop_id for loop_id, units in claims.items() if units > 0),
                }
            )

    live_edges = _live_edges(state, now_ms)
    effect_collisions = sorted(
        str(edge["edge_id"])
        for edge in live_edges
        if edge.get("kind") == "EFFECT_CONFLICT"
        and edge.get("source_loop_id") in active
        and edge.get("target_loop_id") in active
    )
    control_collisions = sorted(
        str(edge["edge_id"])
        for edge in live_edges
        if edge.get("kind") == "CONTROL_COLLISION"
        and edge.get("source_loop_id") in active
        and edge.get("target_loop_id") in active
    )
    dependency_edges = [
        edge
        for edge in live_edges
        if edge.get("kind") in {"EVIDENCE_DEPENDENCY", "CHECKPOINT_DEPENDENCY"}
    ]
    dependency_blocks = sorted(
        str(edge["edge_id"])
        for edge in dependency_edges
        if edge.get("source_loop_id") in active
        and edge.get("target_loop_id") not in active
    )
    wait_cycle_nodes = _wait_cycle_nodes(active, dependency_edges)

    issue_types: list[str] = []
    if resource_contentions:
        issue_types.append("RESOURCE_CONTENTION")
    if effect_collisions:
        issue_types.append("EFFECT_COLLISION")
    if dependency_blocks:
        issue_types.append("DEPENDENCY_BLOCK")
    if wait_cycle_nodes:
        issue_types.append("WAIT_CYCLE")
    if control_collisions:
        issue_types.append("CONTROL_COLLISION")

    if not issue_types:
        classification = "NONE"
    elif len(issue_types) > 1:
        classification = "MIXED"
    else:
        classification = issue_types[0]

    if classification == "NONE":
        severity = "INFO"
    elif classification == "MIXED":
        severity = (
            "CRITICAL"
            if "WAIT_CYCLE" in issue_types or "EFFECT_COLLISION" in issue_types
            else "HIGH"
        )
    elif classification in {"WAIT_CYCLE", "EFFECT_COLLISION"}:
        severity = "HIGH"
    elif classification in {"RESOURCE_CONTENTION", "CONTROL_COLLISION"}:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    route_map = {
        "NONE": ["NO_ACTION"],
        "RESOURCE_CONTENTION": ["SPLIT_RESOURCE", "SERIALIZE", "HOLD"],
        "EFFECT_COLLISION": ["SERIALIZE", "REQUEST_ARBITRATION", "HANDOVER"],
        "DEPENDENCY_BLOCK": ["HOLD", "REQUEST_ARBITRATION"],
        "WAIT_CYCLE": ["REQUEST_ARBITRATION", "HANDOVER"],
        "CONTROL_COLLISION": ["REQUEST_ARBITRATION", "HOLD"],
        "MIXED": ["REQUEST_ARBITRATION", "SERIALIZE", "HANDOVER"],
    }

    affected: set[str] = set(wait_cycle_nodes)
    for item in resource_contentions:
        affected.update(item["loop_ids"])
    edge_ids = set(effect_collisions + control_collisions + dependency_blocks)
    for edge in live_edges:
        if edge.get("edge_id") in edge_ids:
            affected.add(str(edge["source_loop_id"]))
            affected.add(str(edge["target_loop_id"]))

    return {
        "classification": classification,
        "severity": severity,
        "issue_types": sorted(issue_types),
        "affected_loop_ids": sorted(affected),
        "resource_contentions": resource_contentions,
        "effect_collision_edge_ids": effect_collisions,
        "dependency_block_edge_ids": dependency_blocks,
        "wait_cycle_loop_ids": wait_cycle_nodes,
        "control_collision_edge_ids": control_collisions,
        "recommended_routes": route_map[classification],
    }


def build_assessment(
    *, state: Mapping[str, Any], assessment_id: str, assessed_at_ms: int
) -> dict[str, Any]:
    errors = validate_state(state)
    if errors:
        raise ValueError("state_invalid:" + ";".join(errors))
    now = require_nonnegative_int(assessed_at_ms, "assessed_at_ms")
    if now < int(state["updated_at_ms"]):
        raise ValueError("multi_loop_assessment_time_regression")
    diagnosis = _diagnose(state, now)
    packet = {
        "version": ASSESSMENT_VERSION,
        "assessment_id": require_string(assessment_id, "assessment_id"),
        "network_contract_digest": state["contract_digest"],
        "source_state_digest": state["multi_loop_state_digest"],
        **diagnosis,
        "assessed_at_ms": now,
        "advisory_only": True,
        "direct_loop_mutation": False,
        "direct_dispatch": False,
        "license_transfer": False,
        "non_authority": copy_non_authority(),
        "multi_loop_assessment_digest": "",
    }
    packet["multi_loop_assessment_digest"] = assessment_digest(packet)
    return packet


def validate_assessment(
    assessment: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if assessment.get("version") != ASSESSMENT_VERSION:
            errors.append("multi_loop_assessment_version_invalid")
        if assessment.get("network_contract_digest") != state.get("contract_digest"):
            errors.append("multi_loop_assessment_contract_mismatch")
        if assessment.get("source_state_digest") != state.get("multi_loop_state_digest"):
            errors.append("multi_loop_assessment_state_stale")
        require_string(assessment.get("assessment_id"), "assessment_id")
        now = require_nonnegative_int(assessment.get("assessed_at_ms"), "assessed_at_ms")
        expected = _diagnose(state, now)
        for field, value in expected.items():
            if assessment.get(field) != value:
                errors.append(f"multi_loop_assessment_{field}_mismatch")
        if assessment.get("classification") not in INTERFERENCE_CLASSES:
            errors.append("multi_loop_assessment_class_invalid")
        if assessment.get("severity") not in SEVERITIES:
            errors.append("multi_loop_assessment_severity_invalid")
        if assessment.get("advisory_only") is not True:
            errors.append("multi_loop_assessment_advisory_required")
        for field in ("direct_loop_mutation", "direct_dispatch", "license_transfer"):
            if assessment.get(field) is not False:
                errors.append(f"multi_loop_assessment_{field}_forbidden")
        if dict(assessment.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("multi_loop_assessment_authority_expansion")
        if assessment.get("multi_loop_assessment_digest") != assessment_digest(
            assessment
        ):
            errors.append("multi_loop_assessment_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _normalize_allocations(
    allocations: Mapping[str, Mapping[str, int]], state: Mapping[str, Any]
) -> dict[str, dict[str, int]]:
    if not isinstance(allocations, Mapping):
        raise ValueError("resource_allocations_mapping_required")
    result: dict[str, dict[str, int]] = {}
    capacities = state["contract"]["resource_capacities"]
    for resource, per_loop in allocations.items():
        resource_name = require_string(resource, "resource_allocations_key")
        if resource_name not in capacities:
            raise ValueError("resource_allocation_unknown_resource")
        normalized = nonnegative_int_map(
            per_loop, f"resource_allocations_{resource_name}", allow_empty=True
        )
        if set(normalized) - set(state["loops"]):
            raise ValueError("resource_allocation_unknown_loop")
        if sum(normalized.values()) > int(capacities[resource_name]):
            raise ValueError("resource_allocation_above_capacity")
        result[resource_name] = normalized
    return dict(sorted(result.items()))


def build_repair_proposal(
    *,
    state: Mapping[str, Any],
    assessment: Mapping[str, Any],
    proposal_id: str,
    route: str,
    target_loop_ids: list[str],
    circulation_order: list[str],
    resource_allocations: Mapping[str, Mapping[str, int]],
    max_rounds: int,
    rationale_digest: str,
    proposed_at_ms: int,
) -> dict[str, Any]:
    assessment_errors = validate_assessment(assessment, state)
    if assessment_errors:
        raise ValueError("assessment_invalid:" + ";".join(assessment_errors))
    normalized_route = require_string(route, "route")
    if normalized_route not in REPAIR_ROUTES:
        raise ValueError("multi_loop_repair_route_invalid")
    if normalized_route not in assessment["recommended_routes"]:
        raise ValueError("multi_loop_repair_route_not_recommended")
    targets = sorted(unique_strings(target_loop_ids, "target_loop_ids", allow_empty=True))
    if set(targets) - set(state["loops"]):
        raise ValueError("multi_loop_repair_unknown_target")
    affected = set(assessment["affected_loop_ids"])
    if normalized_route != "NO_ACTION" and not targets:
        raise ValueError("multi_loop_repair_target_required")
    if set(targets) - affected:
        raise ValueError("multi_loop_repair_target_not_affected")
    order = unique_strings(circulation_order, "circulation_order", allow_empty=True)
    if set(order) - set(state["loops"]):
        raise ValueError("multi_loop_repair_unknown_order_loop")
    rounds = require_nonnegative_int(max_rounds, "max_rounds")
    if normalized_route == "NO_ACTION":
        if rounds != 0 or targets or order or resource_allocations:
            raise ValueError("multi_loop_no_action_payload_invalid")
    else:
        if rounds < 1:
            raise ValueError("multi_loop_repair_round_required")
        if rounds > int(state["contract"]["max_circulation_rounds"]):
            raise ValueError("multi_loop_repair_round_cap_exceeded")
    allocations = _normalize_allocations(resource_allocations, state)
    packet = {
        "version": REPAIR_VERSION,
        "proposal_id": require_string(proposal_id, "proposal_id"),
        "network_contract_digest": state["contract_digest"],
        "source_state_digest": state["multi_loop_state_digest"],
        "assessment_digest": assessment["multi_loop_assessment_digest"],
        "assessment_class": assessment["classification"],
        "route": normalized_route,
        "target_loop_ids": targets,
        "circulation_order": order,
        "resource_allocations": allocations,
        "max_rounds": rounds,
        "rationale_digest": require_string(rationale_digest, "rationale_digest"),
        "proposed_at_ms": require_nonnegative_int(proposed_at_ms, "proposed_at_ms"),
        "requires_external_authorization": normalized_route != "NO_ACTION",
        "proposal_only": True,
        "direct_dispatch": False,
        "direct_loop_state_change": False,
        "license_transfer": False,
        "non_authority": copy_non_authority(),
        "multi_loop_repair_digest": "",
    }
    packet["multi_loop_repair_digest"] = repair_digest(packet)
    return packet


def validate_repair_proposal(
    proposal: Mapping[str, Any], state: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if proposal.get("version") != REPAIR_VERSION:
            errors.append("multi_loop_repair_version_invalid")
        if proposal.get("network_contract_digest") != state.get("contract_digest"):
            errors.append("multi_loop_repair_contract_mismatch")
        if proposal.get("source_state_digest") != state.get("multi_loop_state_digest"):
            errors.append("multi_loop_repair_state_stale")
        if proposal.get("assessment_digest") != state.get("latest_assessment_digest"):
            errors.append("multi_loop_repair_assessment_not_latest")
        for field in ("proposal_id", "assessment_digest", "rationale_digest"):
            require_string(proposal.get(field), field)
        route = proposal.get("route")
        if route not in REPAIR_ROUTES:
            errors.append("multi_loop_repair_route_invalid")
        targets = unique_strings(
            proposal.get("target_loop_ids"), "target_loop_ids", allow_empty=True
        )
        order = unique_strings(
            proposal.get("circulation_order"), "circulation_order", allow_empty=True
        )
        if set(targets + order) - set(state.get("loops", {})):
            errors.append("multi_loop_repair_unknown_loop")
        rounds = require_nonnegative_int(proposal.get("max_rounds"), "max_rounds")
        if rounds > int(state["contract"]["max_circulation_rounds"]):
            errors.append("multi_loop_repair_round_cap_exceeded")
        _normalize_allocations(proposal.get("resource_allocations", {}), state)
        if route == "NO_ACTION":
            if proposal.get("requires_external_authorization") is not False:
                errors.append("multi_loop_no_action_external_authority_invalid")
        elif proposal.get("requires_external_authorization") is not True:
            errors.append("multi_loop_external_authorization_required")
        if proposal.get("proposal_only") is not True:
            errors.append("multi_loop_repair_proposal_only_required")
        for field in ("direct_dispatch", "direct_loop_state_change", "license_transfer"):
            if proposal.get(field) is not False:
                errors.append(f"multi_loop_repair_{field}_forbidden")
        if dict(proposal.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("multi_loop_repair_authority_expansion")
        if proposal.get("multi_loop_repair_digest") != repair_digest(proposal):
            errors.append("multi_loop_repair_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_control_event(
    *,
    state: Mapping[str, Any],
    command: str,
    command_id: str,
    external_authority_digest: str,
    reason_digest: str,
    issued_at_ms: int,
) -> dict[str, Any]:
    normalized = require_string(command, "command")
    if normalized not in CONTROL_COMMANDS:
        raise ValueError("multi_loop_control_command_invalid")
    packet = {
        "version": CONTROL_VERSION,
        "command": normalized,
        "command_id": require_string(command_id, "command_id"),
        "network_contract_digest": state["contract_digest"],
        "source_state_digest": state["multi_loop_state_digest"],
        "external_authority_digest": require_string(
            external_authority_digest, "external_authority_digest"
        ),
        "reason_digest": require_string(reason_digest, "reason_digest"),
        "issued_at_ms": require_nonnegative_int(issued_at_ms, "issued_at_ms"),
        "mutates_loop": False,
        "dispatches_loop": False,
        "transfers_license": False,
        "multi_loop_control_digest": "",
    }
    packet["multi_loop_control_digest"] = control_digest(packet)
    return packet


def build_event(
    *,
    state: Mapping[str, Any],
    event_kind: str,
    payload: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    kind = require_string(event_kind, "event_kind")
    if kind not in EVENT_KINDS:
        raise ValueError("multi_loop_event_kind_invalid")
    packet = {
        "version": EVENT_VERSION,
        "network_contract_digest": state["contract_digest"],
        "expected_state_digest": state["multi_loop_state_digest"],
        "event_index": int(state["event_index"]) + 1,
        "event_kind": kind,
        "payload": deepcopy(dict(payload)),
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "multi_loop_event_digest": "",
    }
    packet["multi_loop_event_digest"] = event_digest(packet)
    return packet


def _apply_loop_binding(state: dict[str, Any], binding: Mapping[str, Any]) -> None:
    errors = validate_loop_binding(binding, state["contract"])
    if errors:
        raise ValueError("loop_binding_invalid:" + ";".join(errors))
    loop_id = str(binding["loop_id"])
    current = state["loops"].get(loop_id)
    if current is None:
        if len(state["loops"]) >= int(state["contract"]["max_loops"]):
            raise ValueError("multi_loop_loop_cap_exceeded")
    else:
        if binding.get("mission_id") != current.get("mission_id"):
            raise ValueError("multi_loop_mission_rebinding_forbidden")
        if binding.get("v027_contract_digest") != current.get("v027_contract_digest"):
            raise ValueError("multi_loop_v027_contract_rebinding_forbidden")
        if int(binding["completed_cycles"]) < int(current["completed_cycles"]):
            raise ValueError("multi_loop_completed_cycle_regression")
        if int(binding["lease_sequence"]) < int(current["lease_sequence"]):
            raise ValueError("multi_loop_lease_sequence_regression")
        if int(binding["observed_at_ms"]) <= int(current["observed_at_ms"]):
            raise ValueError("multi_loop_binding_time_not_newer")
    state["loops"] = dict(state["loops"])
    state["loops"][loop_id] = deepcopy(dict(binding))


def _apply_edge_binding(state: dict[str, Any], edge: Mapping[str, Any]) -> None:
    errors = validate_edge(edge, state)
    if errors:
        raise ValueError("edge_invalid:" + ";".join(errors))
    edge_id = str(edge["edge_id"])
    if edge_id in state["edges"]:
        raise ValueError("multi_loop_edge_id_already_bound")
    if len(state["edges"]) >= int(state["contract"]["max_edges"]):
        raise ValueError("multi_loop_edge_cap_exceeded")
    state["edges"] = dict(state["edges"])
    state["edges"][edge_id] = deepcopy(dict(edge))


def _apply_assessment(state: dict[str, Any], assessment: Mapping[str, Any]) -> None:
    errors = validate_assessment(assessment, state)
    if errors:
        raise ValueError("assessment_invalid:" + ";".join(errors))
    if len(state["assessment_summaries"]) >= int(
        state["contract"]["max_assessments_per_epoch"]
    ):
        raise ValueError("multi_loop_assessment_epoch_cap_exceeded")
    summary = {
        "assessment_id": assessment["assessment_id"],
        "classification": assessment["classification"],
        "severity": assessment["severity"],
        "affected_loop_ids": assessment["affected_loop_ids"],
        "multi_loop_assessment_digest": assessment["multi_loop_assessment_digest"],
    }
    state["assessment_summaries"] = list(state["assessment_summaries"]) + [summary]
    state["latest_assessment_digest"] = assessment["multi_loop_assessment_digest"]
    state["latest_assessment_class"] = assessment["classification"]
    if state["mode"] not in {"PAUSED", "ARBITRATION_REQUIRED", "TERMINATED"}:
        state["mode"] = (
            "ACTIVE" if assessment["classification"] == "NONE" else "DEGRADED"
        )


def _apply_repair_proposal(state: dict[str, Any], proposal: Mapping[str, Any]) -> None:
    errors = validate_repair_proposal(proposal, state)
    if errors:
        raise ValueError("repair_invalid:" + ";".join(errors))
    if len(state["repair_summaries"]) >= int(
        state["contract"]["max_repair_candidates"]
    ):
        raise ValueError("multi_loop_repair_candidate_cap_exceeded")
    summary = {
        "proposal_id": proposal["proposal_id"],
        "route": proposal["route"],
        "target_loop_ids": proposal["target_loop_ids"],
        "max_rounds": proposal["max_rounds"],
        "multi_loop_repair_digest": proposal["multi_loop_repair_digest"],
    }
    state["repair_summaries"] = list(state["repair_summaries"]) + [summary]
    state["latest_repair_digest"] = proposal["multi_loop_repair_digest"]
    if proposal["route"] in {"REQUEST_ARBITRATION", "HANDOVER", "TERMINATE_ONE"}:
        state["mode"] = "ARBITRATION_REQUIRED"


def _apply_control(state: dict[str, Any], control: Mapping[str, Any]) -> None:
    if control.get("version") != CONTROL_VERSION:
        raise ValueError("multi_loop_control_version_invalid")
    if control.get("network_contract_digest") != state.get("contract_digest"):
        raise ValueError("multi_loop_control_contract_mismatch")
    if control.get("source_state_digest") != state.get("multi_loop_state_digest"):
        raise ValueError("multi_loop_control_state_stale")
    if control.get("multi_loop_control_digest") != control_digest(control):
        raise ValueError("multi_loop_control_digest_invalid")
    for field in ("command_id", "external_authority_digest", "reason_digest"):
        require_string(control.get(field), field)
    for field in ("mutates_loop", "dispatches_loop", "transfers_license"):
        if control.get(field) is not False:
            raise ValueError(f"multi_loop_control_{field}_forbidden")
    command = control.get("command")
    if command not in CONTROL_COMMANDS:
        raise ValueError("multi_loop_control_command_invalid")
    if state["mode"] == "TERMINATED":
        raise ValueError("multi_loop_terminal_state_rejects_control")
    if command == "pause_network":
        state["mode"] = "PAUSED"
    elif command == "resume_network":
        if state["mode"] != "PAUSED":
            raise ValueError("multi_loop_resume_requires_paused")
        state["mode"] = (
            "ACTIVE" if state["latest_assessment_class"] == "NONE" else "DEGRADED"
        )
    elif command == "request_arbitration":
        state["mode"] = "ARBITRATION_REQUIRED"
    elif command == "release_arbitration":
        if state["mode"] != "ARBITRATION_REQUIRED":
            raise ValueError("multi_loop_release_requires_arbitration")
        if state["latest_assessment_class"] != "NONE":
            raise ValueError("multi_loop_release_requires_clear_assessment")
        state["mode"] = "ACTIVE"
    elif command == "terminate_network":
        state["mode"] = "TERMINATED"


def _result(
    *,
    status: str,
    state: Mapping[str, Any],
    event_id: str,
    predecessor: str,
    errors: list[str],
) -> dict[str, Any]:
    packet = {
        "version": APPLY_RESULT_VERSION,
        "status": status,
        "multi_loop_event_digest": event_id,
        "predecessor_state_digest": predecessor,
        "result_state_digest": state["multi_loop_state_digest"],
        "state": deepcopy(dict(state)),
        "errors": list(errors),
        "multi_loop_apply_result_digest": "",
    }
    packet["multi_loop_apply_result_digest"] = apply_result_digest(packet)
    return packet


def apply_event(state: Mapping[str, Any], event: Mapping[str, Any]) -> dict[str, Any]:
    state_errors = validate_state(state)
    if state_errors:
        raise ValueError("state_invalid:" + ";".join(state_errors))
    predecessor = state["multi_loop_state_digest"]
    event_id = str(event.get("multi_loop_event_digest", ""))
    if event_id in set(state["processed_event_digests"]):
        return _result(
            status="REPLAYED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[],
        )
    errors: list[str] = []
    if event.get("version") != EVENT_VERSION:
        errors.append("multi_loop_event_version_invalid")
    if event.get("network_contract_digest") != state.get("contract_digest"):
        errors.append("multi_loop_event_contract_mismatch")
    if event.get("expected_state_digest") != predecessor:
        errors.append("multi_loop_event_state_stale")
    if event.get("event_index") != int(state["event_index"]) + 1:
        errors.append("multi_loop_event_index_invalid")
    if event.get("event_kind") not in EVENT_KINDS:
        errors.append("multi_loop_event_kind_invalid")
    if int(event.get("created_at_ms", -1)) < int(state["updated_at_ms"]):
        errors.append("multi_loop_event_time_regression")
    if event.get("multi_loop_event_digest") != event_digest(event):
        errors.append("multi_loop_event_digest_invalid")
    if errors:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=errors,
        )
    payload = event.get("payload")
    if not isinstance(payload, Mapping):
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=["multi_loop_event_payload_invalid"],
        )
    next_state = deepcopy(dict(state))
    try:
        kind = event["event_kind"]
        if kind == "loop_binding":
            _apply_loop_binding(next_state, payload)
        elif kind == "edge_binding":
            _apply_edge_binding(next_state, payload)
        elif kind == "assessment":
            _apply_assessment(next_state, payload)
        elif kind == "repair_proposal":
            _apply_repair_proposal(next_state, payload)
        else:
            _apply_control(next_state, payload)
    except (TypeError, ValueError) as exc:
        return _result(
            status="REJECTED",
            state=state,
            event_id=event_id,
            predecessor=predecessor,
            errors=[str(exc)],
        )
    next_state["processed_event_digests"] = list(
        next_state["processed_event_digests"]
    ) + [event_id]
    next_state["event_index"] += 1
    next_state["updated_at_ms"] = int(event["created_at_ms"])
    next_state["event_history"] = list(next_state["event_history"]) + [
        {
            "event_index": next_state["event_index"],
            "event_kind": event["event_kind"],
            "event_digest": event_id,
            "created_at_ms": event["created_at_ms"],
            "mode": next_state["mode"],
            "loop_count": len(next_state["loops"]),
            "edge_count": len(next_state["edges"]),
        }
    ]
    next_state["multi_loop_state_digest"] = ""
    next_state["multi_loop_state_digest"] = state_digest(next_state)
    next_errors = validate_state(next_state)
    if next_errors:
        raise ValueError("next_state_invalid:" + ";".join(next_errors))
    return _result(
        status="APPLIED",
        state=next_state,
        event_id=event_id,
        predecessor=predecessor,
        errors=[],
    )


__all__ = [
    "apply_event",
    "build_assessment",
    "build_control_event",
    "build_edge",
    "build_event",
    "build_initial_state",
    "build_loop_binding",
    "build_network_contract",
    "build_repair_proposal",
    "validate_assessment",
    "validate_edge",
    "validate_loop_binding",
    "validate_network_contract",
    "validate_repair_proposal",
    "validate_state",
]
