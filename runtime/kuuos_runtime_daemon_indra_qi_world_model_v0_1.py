#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

SPEC_VERSION = "indra_qi_world_model_v0_1"
FLOW_KIND = "gauge_covariant_relational_effective_flow"
REQUIRED_OPERATOR_ROLES = {
    "observation",
    "projection",
    "parallel_transport",
    "bounded_mutation",
    "rollback_repair",
    "history_feedback",
    "emptiness_non_reification",
}
REQUIRED_PROCESS_CONTEXT = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)
REQUIRED_BOUNDARIES = {
    "indra_net_is_gauge_structured": True,
    "qi_is_indra_net_relational_flow": True,
    "qi_substance_claim": False,
    "noncommutative_operator_order_preserved": True,
    "holonomy_preserved": True,
    "transport_residue_visible": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "emptiness_non_reification_preserved": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
    "not_world_update_authority": True,
    "structural_bridge_not_physical_theorem_authority": True,
    "fail_closed_on_boundary_loss": True,
}


@dataclass(frozen=True)
class IndraQiWorldModelV0_1Result:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    world_model_id: str
    build_status: str
    local_patch_count: int
    connection_count: int
    qi_flow_count: int
    holonomy_cycle_count: int
    string_correspondence_count: int
    m_brane_surface_count: int
    state_digest: str
    state_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _items(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    payload = dict(value)
    payload.pop(field, None)
    return payload


def compute_indra_qi_world_state_digest(value: Mapping[str, Any]) -> str:
    return _sha(_without(value, "indra_qi_world_state_digest"))


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unique_identifiers(items: list[Any], field: str, prefix: str, blockers: list[str]) -> set[str]:
    values: list[str] = []
    for index, raw in enumerate(items):
        identifier = str(_m(raw).get(field, ""))
        if not identifier:
            blockers.append(f"{prefix}_{index}_{field}_missing")
        values.append(identifier)
    if len(set(values)) != len(values):
        blockers.append(f"{prefix}_{field}_duplicate")
    return {value for value in values if value}


def _validate_patches(patches: list[Any], blockers: list[str]) -> set[str]:
    if len(patches) < 2:
        blockers.append("local_world_patches_requires_at_least_two")
    patch_ids = _unique_identifiers(patches, "patch_id", "local_patch", blockers)
    for index, raw in enumerate(patches):
        patch = _m(raw)
        for field in (
            "representation_space",
            "state_functional_digest",
            "change_generator_digest",
            "gauge_chart_id",
        ):
            if not _text(patch.get(field)):
                blockers.append(f"local_patch_{index}_{field}_missing")
        algebra = _m(patch.get("operator_algebra"))
        roles = {str(value) for value in _items(algebra.get("operator_roles"))}
        missing = sorted(REQUIRED_OPERATOR_ROLES - roles)
        if missing:
            blockers.append(f"local_patch_{index}_operator_roles_missing:{','.join(missing)}")
        if algebra.get("noncommutative_ordering_required") is not True:
            blockers.append(f"local_patch_{index}_noncommutative_ordering_not_required")
        witnesses = _items(algebra.get("commutator_witnesses"))
        if not witnesses:
            blockers.append(f"local_patch_{index}_commutator_witnesses_missing")
        for witness_index, raw_witness in enumerate(witnesses):
            witness = _m(raw_witness)
            if not _text(witness.get("left_operator")) or not _text(witness.get("right_operator")):
                blockers.append(f"local_patch_{index}_commutator_{witness_index}_operators_missing")
            if witness.get("order_sensitive") is not True:
                blockers.append(f"local_patch_{index}_commutator_{witness_index}_not_order_sensitive")
    return patch_ids


def _validate_connections(
    connections: list[Any], patch_ids: set[str], blockers: list[str]
) -> tuple[set[str], dict[str, tuple[str, str]]]:
    if not connections:
        blockers.append("indra_connections_missing")
    connection_ids = _unique_identifiers(connections, "connection_id", "indra_connection", blockers)
    endpoints: dict[str, tuple[str, str]] = {}
    for index, raw in enumerate(connections):
        connection = _m(raw)
        connection_id = str(connection.get("connection_id", ""))
        source = str(connection.get("source_patch", ""))
        target = str(connection.get("target_patch", ""))
        if source not in patch_ids:
            blockers.append(f"indra_connection_{index}_source_patch_unknown")
        if target not in patch_ids:
            blockers.append(f"indra_connection_{index}_target_patch_unknown")
        if source and source == target:
            blockers.append(f"indra_connection_{index}_self_transport_not_declared")
        for field in ("connection_form_digest", "parallel_transport_digest"):
            if not _text(connection.get(field)):
                blockers.append(f"indra_connection_{index}_{field}_missing")
        if connection.get("gauge_equivalence_preserved") is not True:
            blockers.append(f"indra_connection_{index}_gauge_equivalence_not_preserved")
        if connection.get("transport_residue_visible") is not True:
            blockers.append(f"indra_connection_{index}_transport_residue_not_visible")
        if connection_id:
            endpoints[connection_id] = (source, target)
    return connection_ids, endpoints


def _validate_flows(
    flows: list[Any], connection_ids: set[str], endpoints: Mapping[str, tuple[str, str]], blockers: list[str]
) -> None:
    if not flows:
        blockers.append("qi_flow_channels_missing")
    _unique_identifiers(flows, "flow_id", "qi_flow", blockers)
    for index, raw in enumerate(flows):
        flow = _m(raw)
        connection_id = str(flow.get("connection_id", ""))
        endpoints_value = (str(flow.get("source_patch", "")), str(flow.get("target_patch", "")))
        if connection_id not in connection_ids:
            blockers.append(f"qi_flow_{index}_connection_unknown")
        elif endpoints.get(connection_id) != endpoints_value:
            blockers.append(f"qi_flow_{index}_connection_endpoint_mismatch")
        if flow.get("flow_kind") != FLOW_KIND:
            blockers.append(f"qi_flow_{index}_flow_kind_invalid")
        if flow.get("substance_claim") is not False:
            blockers.append(f"qi_flow_{index}_substance_claim_not_false")
        if not _text(flow.get("flow_observable_digest")):
            blockers.append(f"qi_flow_{index}_flow_observable_digest_missing")
        process_context = _m(flow.get("process_tensor_context"))
        for field in REQUIRED_PROCESS_CONTEXT:
            if not _text(process_context.get(field)):
                blockers.append(f"qi_flow_{index}_{field}_missing")


def _validate_holonomy(cycles: list[Any], connection_ids: set[str], blockers: list[str]) -> None:
    if not cycles:
        blockers.append("holonomy_cycles_missing")
    _unique_identifiers(cycles, "cycle_id", "holonomy_cycle", blockers)
    for index, raw in enumerate(cycles):
        cycle = _m(raw)
        path = [str(value) for value in _items(cycle.get("connection_ids"))]
        if len(path) < 2:
            blockers.append(f"holonomy_cycle_{index}_path_too_short")
        if any(connection_id not in connection_ids for connection_id in path):
            blockers.append(f"holonomy_cycle_{index}_connection_unknown")
        if cycle.get("holonomy_preserved") is not True:
            blockers.append(f"holonomy_cycle_{index}_not_preserved")
        if not _text(cycle.get("holonomy_digest")):
            blockers.append(f"holonomy_cycle_{index}_digest_missing")
        if not _text(cycle.get("transport_residue_digest")):
            blockers.append(f"holonomy_cycle_{index}_transport_residue_digest_missing")


def _validate_strings(strings: list[Any], patch_ids: set[str], blockers: list[str]) -> None:
    if not strings:
        blockers.append("ku_string_correspondences_missing")
    _unique_identifiers(strings, "string_id", "ku_string", blockers)
    for index, raw in enumerate(strings):
        relation = _m(raw)
        if str(relation.get("source_patch", "")) not in patch_ids:
            blockers.append(f"ku_string_{index}_source_patch_unknown")
        if str(relation.get("target_patch", "")) not in patch_ids:
            blockers.append(f"ku_string_{index}_target_patch_unknown")
        if relation.get("correspondence_kind") not in {
            "open_relational_correspondence",
            "closed_collective_correspondence",
        }:
            blockers.append(f"ku_string_{index}_correspondence_kind_invalid")
        if relation.get("relation_substance_claim") is not False:
            blockers.append(f"ku_string_{index}_relation_substance_claim_not_false")
        if not _text(relation.get("correspondence_digest")):
            blockers.append(f"ku_string_{index}_correspondence_digest_missing")


def _validate_branes(branes: list[Any], patch_ids: set[str], blockers: list[str]) -> None:
    if not branes:
        blockers.append("extended_m_brane_surfaces_missing")
    _unique_identifiers(branes, "surface_id", "m_brane_surface", blockers)
    kinds: set[str] = set()
    for index, raw in enumerate(branes):
        brane = _m(raw)
        kind = str(brane.get("brane_kind", ""))
        kinds.add(kind)
        if kind not in {"m2_interaction_surface", "m5_history_surface"}:
            blockers.append(f"m_brane_surface_{index}_kind_invalid")
        included = {str(value) for value in _items(brane.get("included_patch_ids"))}
        if not included or not included.issubset(patch_ids):
            blockers.append(f"m_brane_surface_{index}_included_patches_invalid")
        if not _text(brane.get("surface_digest")):
            blockers.append(f"m_brane_surface_{index}_surface_digest_missing")
        if brane.get("semantic_dimension_not_physical_spacetime_claim") is not True:
            blockers.append(f"m_brane_surface_{index}_semantic_dimension_boundary_missing")
    if "m2_interaction_surface" not in kinds:
        blockers.append("m2_interaction_surface_missing")
    if "m5_history_surface" not in kinds:
        blockers.append("m5_history_surface_missing")


def _validate_boundaries(model: Mapping[str, Any], patch_ids: set[str], blockers: list[str]) -> None:
    mandala = _m(model.get("mandala_inclusion"))
    if {str(value) for value in _items(mandala.get("included_patch_ids"))} != patch_ids:
        blockers.append("mandala_inclusion_patch_set_mismatch")
    if mandala.get("multi_world_noncollapse") is not True:
        blockers.append("mandala_multi_world_noncollapse_not_true")
    if mandala.get("single_ontology_forced") is not False:
        blockers.append("mandala_single_ontology_forced_not_false")
    if mandala.get("contradiction_visibility_preserved") is not True:
        blockers.append("mandala_contradiction_visibility_not_preserved")

    two_truths = _m(model.get("two_truths_boundary"))
    for field in (
        "two_truths_gap_preserved",
        "emptiness_non_reification_preserved",
        "model_prediction_not_fact",
        "validator_pass_not_truth",
        "receipt_not_theorem",
    ):
        if two_truths.get(field) is not True:
            blockers.append(f"two_truths_{field}_not_true")

    governance = _m(model.get("governance_boundary"))
    for field, expected in REQUIRED_BOUNDARIES.items():
        if governance.get(field) is not expected:
            blockers.append(f"governance_boundary_{field}_mismatch")
    if governance.get("direct_world_update_authority") is not False:
        blockers.append("direct_world_update_authority_not_false")
    if governance.get("operator_algebra_update_authority") is not False:
        blockers.append("operator_algebra_update_authority_not_false")


def build_indra_qi_world_model_v0_1(
    *,
    world_model: Mapping[str, Any],
    runtime_context: Mapping[str, Any],
    world_model_license: Mapping[str, Any],
) -> IndraQiWorldModelV0_1Result:
    model = dict(_m(world_model))
    context = _m(runtime_context)
    license_value = _m(world_model_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = context.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    state_path = root / "ku_indra_qi_noncommutative_mandala_world_state.json"
    receipt_path = root / "ku_indra_qi_noncommutative_mandala_world_receipt.json"
    audit_path = root / "ku_indra_qi_noncommutative_mandala_world_audit.jsonl"

    if context.get("indra_qi_world_model_enabled") is not True:
        blockers.append("indra_qi_world_model_enabled_not_true")
    if context.get("build_indra_qi_world_model") is not True:
        blockers.append("build_indra_qi_world_model_not_true")
    if license_value.get("license_status") != "INDRA_QI_WORLD_MODEL_LICENSE_READY":
        blockers.append("indra_qi_world_model_license_not_ready")
    for flag in (
        "world_model_validate_allowed",
        "world_state_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if license_value.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    if model.get("version") != SPEC_VERSION:
        blockers.append("world_model_version_invalid")
    world_model_id = str(model.get("world_model_id", ""))
    if not world_model_id:
        blockers.append("world_model_id_missing")

    patches = _items(model.get("local_world_patches"))
    connections = _items(model.get("indra_connections"))
    flows = _items(model.get("qi_flow_channels"))
    cycles = _items(model.get("holonomy_cycles"))
    strings = _items(model.get("ku_string_correspondences"))
    branes = _items(model.get("extended_m_brane_surfaces"))

    patch_ids = _validate_patches(patches, blockers)
    connection_ids, endpoints = _validate_connections(connections, patch_ids, blockers)
    _validate_flows(flows, connection_ids, endpoints, blockers)
    _validate_holonomy(cycles, connection_ids, blockers)
    _validate_strings(strings, patch_ids, blockers)
    _validate_branes(branes, patch_ids, blockers)
    _validate_boundaries(model, patch_ids, blockers)

    build_status = "indra_qi_world_model_blocked"
    state_digest = ""
    if not blockers:
        state = {
            "version": SPEC_VERSION,
            "world_model_id": world_model_id,
            "build_status": "indra_qi_world_model_ready",
            "core_statement": {
                "indra_net": "gauge_structured_relational_substrate",
                "qi": FLOW_KIND,
                "qi_substance_claim": False,
            },
            "causal_world_model_bridge": {
                "target": "kuuos_causal_world_model_os_v14_0",
                "relation": "local_conventional_projection_layer",
                "causal_dag_not_complete_world_ontology": True,
                "causal_edge_not_gauge_connection": True,
                "variable_value_not_qi_itself": True,
                "internal_causal_mutation_not_external_actuation": True,
            },
            "local_world_patches": patches,
            "indra_connections": connections,
            "qi_flow_channels": flows,
            "holonomy_cycles": cycles,
            "ku_string_correspondences": strings,
            "extended_m_brane_surfaces": branes,
            "mandala_inclusion": dict(_m(model.get("mandala_inclusion"))),
            "two_truths_boundary": dict(_m(model.get("two_truths_boundary"))),
            "governance_boundary": dict(_m(model.get("governance_boundary"))),
            "counts": {
                "local_patches": len(patches),
                "connections": len(connections),
                "qi_flows": len(flows),
                "holonomy_cycles": len(cycles),
                "string_correspondences": len(strings),
                "m_brane_surfaces": len(branes),
            },
            "epoch": int(time.time()),
        }
        state["indra_qi_world_state_digest"] = compute_indra_qi_world_state_digest(state)
        state_digest = state["indra_qi_world_state_digest"]
        _write_json(state_path, state)
        build_status = "indra_qi_world_model_ready"

    status = "INDRA_QI_WORLD_MODEL_READY" if not blockers else "INDRA_QI_WORLD_MODEL_BLOCKED"
    receipt = {
        "version": "kuuos_runtime_daemon_indra_qi_world_model_v0_1",
        "status": status,
        "packet_id": "indra-qi-world-model-"
        + _sha({"world_model_id": world_model_id, "state_digest": state_digest, "blockers": blockers})[:16],
        "world_model_id": world_model_id,
        "build_status": build_status,
        "local_patch_count": len(patches),
        "connection_count": len(connections),
        "qi_flow_count": len(flows),
        "holonomy_cycle_count": len(cycles),
        "string_correspondence_count": len(strings),
        "m_brane_surface_count": len(branes),
        "state_digest": state_digest,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if license_value.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if license_value.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return IndraQiWorldModelV0_1Result(
        receipt["version"],
        status,
        receipt["packet_id"],
        str(root),
        world_model_id,
        build_status,
        len(patches),
        len(connections),
        len(flows),
        len(cycles),
        len(strings),
        len(branes),
        state_digest,
        str(state_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
