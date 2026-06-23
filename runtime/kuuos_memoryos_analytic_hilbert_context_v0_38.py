from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime import kuuos_memoryos_predictive_shielded_memory_v0_37 as v037

VERSION = "kuuos_memoryos_analytic_hilbert_context_v0_38"
ANALYTIC_PACKET_VERSION = "world_kuu_vacuum_os_hilbert_analytic_packet_v0_49"
CAPSULE_VERSION = "memoryos_analytic_hilbert_context_capsule_v0_38"
RETRIEVAL_VERSION = "memoryos_analytic_hilbert_context_retrieval_v0_38"
WORLD_BRIDGE_ID = "KUOS.WORLD.KuuVacuumOSHilbertCompletionBridgeV0_49"

ANALYTIC_SURFACES = (
    "os_reflection_form",
    "os_hilbert_vacuum",
    "vacuum_state",
    "gauge_invariance",
    "modular_time",
    "physical_time",
    "hamiltonian_vacuum",
)

CAPSULE_ROUTES = {
    "QUARANTINE_MEMORY_SOURCE",
    "REOBSERVE_ANALYTIC_EVIDENCE",
    "PRESERVE_RESIDUE_WITH_ANALYTIC_CONTEXT",
    "READY_FOR_READ_ONLY_ANALYTIC_RETRIEVAL",
}

RETRIEVAL_ROUTES = {
    "QUARANTINE_ANALYTIC_RETRIEVAL",
    "RETURN_ANALYTIC_CONTEXT_WITH_ACTIVE_SHIELD",
    "REOBSERVE_ANALYTIC_EVIDENCE",
    "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE",
    "RETURN_READ_ONLY_HILBERT_CONTEXT",
}

NON_AUTHORITY = {
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_execution_authority": False,
    "grants_plan_activation": False,
    "grants_actos_invocation": False,
    "grants_blocker_discharge_authority": False,
    "grants_world_commit_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_unique_vacuum_declaration": False,
    "grants_metaphysical_kuu_identification": False,
    "grants_world_vacuum_identification": False,
}

BOUNDARY = {
    "source_v037_capsule_preserved": True,
    "source_world_fragment_exactly_bound": True,
    "analytic_packet_candidate_only": True,
    "reflection_positivity_is_supplied_evidence": True,
    "os_completion_not_constructed_by_runtime": True,
    "vacuum_state_not_truth_authority": True,
    "analytic_vacuum_not_unique_vacuum_claim": True,
    "analytic_vacuum_not_metaphysical_kuu": True,
    "analytic_vacuum_not_exact_world": True,
    "modular_time_distinct_from_physical_time": True,
    "physical_time_not_executed_by_memoryos": True,
    "hamiltonian_not_executed_by_memoryos": True,
    "contradiction_residue_preserved": True,
    "blocker_shield_precedes_analytic_return": True,
    "append_only_analytic_lineage": True,
    "multiworld_noncollapse_preserved": True,
}

_REQUIRED_ANALYTIC_FLAGS = (
    "os_reflection_positive",
    "os_null_characterization_available",
    "os_quotient_completion_supplied",
    "vacuum_state_normalized",
    "vacuum_state_positive",
    "gauge_invariant",
    "modular_vacuum_invariant",
    "physical_vacuum_invariant",
    "physical_hamiltonian_vacuum",
    "physical_hamiltonian_self_adjoint_supplied",
    "physical_time_stone_supplied",
    "modular_time_distinct_from_physical_time",
)

_FORBIDDEN_PACKET_FLAGS = (
    "runtime_constructed_os_completion",
    "runtime_executed_physical_hamiltonian",
    "runtime_executed_physical_time",
    "unique_vacuum_claim",
    "kuu_zero_vector_identification",
    "metaphysical_kuu_identification",
    "world_vacuum_identification",
    "world_truth_claim",
    "world_update_authority",
    "execution_authority",
)


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def digest(value: Mapping[str, Any]) -> str:
    return v037.v035.world_v034.digest(value)


def analytic_packet_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "analytic_packet_digest"))


def analytic_capsule_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "analytic_capsule_digest"))


def retrieval_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "retrieval_digest"))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _strings(values: Any, field: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{field}_invalid")
    result = [_text(value, field) for value in values]
    if not allow_empty and not result:
        raise ValueError(f"{field}_empty")
    if len(result) != len(set(result)):
        raise ValueError(f"{field}_duplicate")
    return result


def normalize_analytic_packet(
    packet: Mapping[str, Any],
    *,
    source_world_fragment_digest: str,
) -> dict[str, Any]:
    if packet.get("version") != ANALYTIC_PACKET_VERSION:
        raise ValueError("analytic_packet_version_invalid")
    if packet.get("world_bridge_id") != WORLD_BRIDGE_ID:
        raise ValueError("analytic_packet_world_bridge_invalid")
    packet_source = _text(
        packet.get("source_world_fragment_digest"),
        "analytic_source_world_fragment_digest",
    )
    if packet_source != source_world_fragment_digest:
        raise ValueError("analytic_source_world_fragment_mismatch")
    for field in _FORBIDDEN_PACKET_FLAGS:
        if packet.get(field) is not False:
            raise ValueError(f"analytic_packet_{field}_forbidden")
    normalized = {
        "version": ANALYTIC_PACKET_VERSION,
        "packet_id": _text(packet.get("packet_id"), "analytic_packet_id"),
        "world_bridge_id": WORLD_BRIDGE_ID,
        "source_world_fragment_digest": packet_source,
        "positive_time_observable_surface_digest": _text(
            packet.get("positive_time_observable_surface_digest"),
            "positive_time_observable_surface_digest",
        ),
        "os_reflection_form_digest": _text(
            packet.get("os_reflection_form_digest"),
            "os_reflection_form_digest",
        ),
        "os_hilbert_carrier_digest": _text(
            packet.get("os_hilbert_carrier_digest"),
            "os_hilbert_carrier_digest",
        ),
        "analytic_vacuum_digest": _text(
            packet.get("analytic_vacuum_digest"),
            "analytic_vacuum_digest",
        ),
        "vacuum_state_digest": _text(
            packet.get("vacuum_state_digest"),
            "vacuum_state_digest",
        ),
        "physical_hamiltonian_digest": _text(
            packet.get("physical_hamiltonian_digest"),
            "physical_hamiltonian_digest",
        ),
        "physical_time_flow_digest": _text(
            packet.get("physical_time_flow_digest"),
            "physical_time_flow_digest",
        ),
        "modular_time_flow_digest": _text(
            packet.get("modular_time_flow_digest"),
            "modular_time_flow_digest",
        ),
        "os_vacuum_norm_milli": _nat(
            packet.get("os_vacuum_norm_milli"),
            "os_vacuum_norm_milli",
        ),
        **{field: packet.get(field) is True for field in _REQUIRED_ANALYTIC_FLAGS},
        **{field: False for field in _FORBIDDEN_PACKET_FLAGS},
        "analytic_packet_digest": "",
    }
    if normalized["os_vacuum_norm_milli"] != 1000:
        raise ValueError("analytic_packet_os_vacuum_not_normalized")
    supplied = all(normalized[field] is True for field in _REQUIRED_ANALYTIC_FLAGS)
    normalized["analytic_evidence_complete"] = supplied
    normalized["analytic_packet_digest"] = analytic_packet_digest(normalized)
    provided_digest = packet.get("analytic_packet_digest")
    if provided_digest not in (None, "") and provided_digest != normalized[
        "analytic_packet_digest"
    ]:
        raise ValueError("analytic_packet_digest_invalid")
    return normalized


def validate_analytic_packet(
    packet: Mapping[str, Any],
    *,
    source_world_fragment_digest: str,
) -> list[str]:
    try:
        normalized = normalize_analytic_packet(
            packet,
            source_world_fragment_digest=source_world_fragment_digest,
        )
    except ValueError as exc:
        return [str(exc)]
    if dict(packet) != normalized:
        return ["analytic_packet_not_normalized"]
    return []


def _expected_capsule_route(
    memory_capsule: Mapping[str, Any],
    analytic_packet: Mapping[str, Any],
) -> str:
    if memory_capsule.get("capsule_route") == "QUARANTINE_SOURCE_BLOCKER_EVIDENCE":
        return "QUARANTINE_MEMORY_SOURCE"
    if analytic_packet.get("analytic_evidence_complete") is not True:
        return "REOBSERVE_ANALYTIC_EVIDENCE"
    if memory_capsule.get("contradiction_residue"):
        return "PRESERVE_RESIDUE_WITH_ANALYTIC_CONTEXT"
    return "READY_FOR_READ_ONLY_ANALYTIC_RETRIEVAL"


def _validate_prior_capsule(
    prior_capsule: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if prior_capsule is None:
        return None
    errors = validate_memoryos_analytic_hilbert_context_capsule(prior_capsule)
    if errors:
        raise ValueError("prior_analytic_capsule_invalid:" + ";".join(errors))
    return deepcopy(dict(prior_capsule))


def build_memoryos_analytic_hilbert_context_capsule(
    *,
    memory_capsule: Mapping[str, Any],
    analytic_packet: Mapping[str, Any],
    created_at_ms: int,
    prior_capsule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    memory_errors = v037.validate_predictive_shielded_memory_capsule(memory_capsule)
    if memory_errors:
        raise ValueError("memory_capsule_invalid:" + ";".join(memory_errors))
    prior = _validate_prior_capsule(prior_capsule)
    normalized_packet = normalize_analytic_packet(
        analytic_packet,
        source_world_fragment_digest=memory_capsule["source_world_fragment_digest"],
    )
    if prior is None:
        sequence_index = 0
        previous_digest = v037.v035.world_v034.ZERO_DIGEST
    else:
        if memory_capsule["mission_id"] != prior["mission_id"]:
            raise ValueError("analytic_capsule_mission_changed")
        if memory_capsule["lineage_id"] != prior["lineage_id"]:
            raise ValueError("analytic_capsule_lineage_changed")
        if memory_capsule["sequence_index"] < prior["source_memory_sequence_index"]:
            raise ValueError("analytic_source_memory_sequence_regressed")
        if (
            memory_capsule["sequence_index"] == prior["source_memory_sequence_index"]
            and memory_capsule["memory_capsule_digest"]
            != prior["source_memory_capsule_digest"]
        ):
            raise ValueError("analytic_source_memory_changed_without_sequence")
        if normalized_packet["source_world_fragment_digest"] != prior[
            "source_world_fragment_digest"
        ]:
            raise ValueError("analytic_world_fragment_changed")
        sequence_index = prior["sequence_index"] + 1
        previous_digest = prior["analytic_capsule_digest"]

    route = _expected_capsule_route(memory_capsule, normalized_packet)
    capsule = {
        "version": CAPSULE_VERSION,
        "sequence_index": sequence_index,
        "previous_analytic_capsule_digest": previous_digest,
        "source_memory_capsule_digest": memory_capsule["memory_capsule_digest"],
        "source_memory_sequence_index": memory_capsule["sequence_index"],
        "source_predictive_state_digest": memory_capsule["predictive_state_digest"],
        "source_qi_process_tensor_trace_digest": memory_capsule[
            "source_qi_process_tensor_trace_digest"
        ],
        "source_world_fragment_digest": memory_capsule[
            "source_world_fragment_digest"
        ],
        "source_analytic_packet_digest": normalized_packet[
            "analytic_packet_digest"
        ],
        "mission_id": memory_capsule["mission_id"],
        "lineage_id": memory_capsule["lineage_id"],
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "capsule_route": route,
        "memory_projection": {
            "memory_inventory": deepcopy(memory_capsule["memory_inventory"]),
            "memory_record_ids": [
                record["record_id"] for record in memory_capsule["memory_records"]
            ],
            "consolidation_candidate_record_ids": deepcopy(
                memory_capsule["consolidation_candidate_record_ids"]
            ),
            "contradiction_residue_ids": [
                residue["residue_id"]
                for residue in memory_capsule["contradiction_residue"]
            ],
            "automatic_consolidation_performed": False,
            "memory_overwrite_performed": False,
        },
        "analytic_projection": {
            "packet_id": normalized_packet["packet_id"],
            "world_bridge_id": normalized_packet["world_bridge_id"],
            "positive_time_observable_surface_digest": normalized_packet[
                "positive_time_observable_surface_digest"
            ],
            "os_reflection_form_digest": normalized_packet[
                "os_reflection_form_digest"
            ],
            "os_hilbert_carrier_digest": normalized_packet[
                "os_hilbert_carrier_digest"
            ],
            "analytic_vacuum_digest": normalized_packet[
                "analytic_vacuum_digest"
            ],
            "vacuum_state_digest": normalized_packet["vacuum_state_digest"],
            "physical_hamiltonian_digest": normalized_packet[
                "physical_hamiltonian_digest"
            ],
            "physical_time_flow_digest": normalized_packet[
                "physical_time_flow_digest"
            ],
            "modular_time_flow_digest": normalized_packet[
                "modular_time_flow_digest"
            ],
            "analytic_evidence_complete": normalized_packet[
                "analytic_evidence_complete"
            ],
            "os_reflection_positive": normalized_packet[
                "os_reflection_positive"
            ],
            "vacuum_state_normalized": normalized_packet[
                "vacuum_state_normalized"
            ],
            "vacuum_state_positive": normalized_packet[
                "vacuum_state_positive"
            ],
            "gauge_invariant": normalized_packet["gauge_invariant"],
            "modular_vacuum_invariant": normalized_packet[
                "modular_vacuum_invariant"
            ],
            "physical_vacuum_invariant": normalized_packet[
                "physical_vacuum_invariant"
            ],
            "physical_hamiltonian_vacuum": normalized_packet[
                "physical_hamiltonian_vacuum"
            ],
            "modular_time_distinct_from_physical_time": True,
            "candidate_context_only": True,
            "truth_claim": False,
            "unique_vacuum_claim": False,
            "metaphysical_kuu_identification": False,
            "world_vacuum_identification": False,
            "world_update_performed": False,
            "physical_time_execution_performed": False,
            "hamiltonian_execution_performed": False,
        },
        "blocker_projection": deepcopy(memory_capsule["blocker_projection"]),
        "append_candidate": {
            "target_stream": "memoryos/analytic_hilbert_context/append_only",
            "append_only_required": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
        },
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "analytic_capsule_digest": "",
    }
    capsule["analytic_capsule_digest"] = analytic_capsule_digest(capsule)
    errors = validate_memoryos_analytic_hilbert_context_capsule(capsule)
    if errors:
        raise ValueError(";".join(errors))
    return capsule


def validate_memoryos_analytic_hilbert_context_capsule(
    capsule: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if capsule.get("version") != CAPSULE_VERSION:
        errors.append("analytic_capsule_version_invalid")
    for field in ("sequence_index", "source_memory_sequence_index", "created_at_ms"):
        try:
            _nat(capsule.get(field), field)
        except ValueError as exc:
            errors.append(str(exc))
    for field in (
        "previous_analytic_capsule_digest",
        "source_memory_capsule_digest",
        "source_predictive_state_digest",
        "source_qi_process_tensor_trace_digest",
        "source_world_fragment_digest",
        "source_analytic_packet_digest",
        "mission_id",
        "lineage_id",
    ):
        if not isinstance(capsule.get(field), str) or not capsule.get(field):
            errors.append(f"analytic_capsule_{field}_missing")
    if capsule.get("capsule_route") not in CAPSULE_ROUTES:
        errors.append("analytic_capsule_route_invalid")

    memory = capsule.get("memory_projection")
    if not isinstance(memory, Mapping):
        errors.append("analytic_capsule_memory_projection_invalid")
    else:
        for field in (
            "memory_record_ids",
            "consolidation_candidate_record_ids",
            "contradiction_residue_ids",
        ):
            if not isinstance(memory.get(field), list):
                errors.append(f"analytic_capsule_memory_{field}_invalid")
        if not isinstance(memory.get("memory_inventory"), Mapping):
            errors.append("analytic_capsule_memory_inventory_invalid")
        for field in (
            "automatic_consolidation_performed",
            "memory_overwrite_performed",
        ):
            if memory.get(field) is not False:
                errors.append(f"analytic_capsule_memory_{field}_forbidden")

    analytic = capsule.get("analytic_projection")
    if not isinstance(analytic, Mapping):
        errors.append("analytic_capsule_projection_invalid")
    else:
        for field in (
            "packet_id",
            "world_bridge_id",
            "positive_time_observable_surface_digest",
            "os_reflection_form_digest",
            "os_hilbert_carrier_digest",
            "analytic_vacuum_digest",
            "vacuum_state_digest",
            "physical_hamiltonian_digest",
            "physical_time_flow_digest",
            "modular_time_flow_digest",
        ):
            if not isinstance(analytic.get(field), str) or not analytic.get(field):
                errors.append(f"analytic_capsule_projection_{field}_missing")
        for field, expected in (
            ("candidate_context_only", True),
            ("truth_claim", False),
            ("unique_vacuum_claim", False),
            ("metaphysical_kuu_identification", False),
            ("world_vacuum_identification", False),
            ("world_update_performed", False),
            ("physical_time_execution_performed", False),
            ("hamiltonian_execution_performed", False),
            ("modular_time_distinct_from_physical_time", True),
        ):
            if analytic.get(field) is not expected:
                errors.append(f"analytic_capsule_projection_{field}_invalid")
        complete = analytic.get("analytic_evidence_complete") is True
        if complete:
            for field in (
                "os_reflection_positive",
                "vacuum_state_normalized",
                "vacuum_state_positive",
                "gauge_invariant",
                "modular_vacuum_invariant",
                "physical_vacuum_invariant",
                "physical_hamiltonian_vacuum",
            ):
                if analytic.get(field) is not True:
                    errors.append(f"analytic_capsule_projection_{field}_invalid")

    blocker = capsule.get("blocker_projection")
    if not isinstance(blocker, Mapping):
        errors.append("analytic_capsule_blocker_projection_invalid")
    else:
        if blocker.get("shield_gate_required") is not True:
            errors.append("analytic_capsule_blocker_shield_missing")
        if blocker.get("memory_may_discharge_blocker") is not False:
            errors.append("analytic_capsule_blocker_discharge_forbidden")

    append_candidate = capsule.get("append_candidate")
    if not isinstance(append_candidate, Mapping):
        errors.append("analytic_capsule_append_candidate_invalid")
    else:
        for field, expected in (
            ("append_only_required", True),
            ("durable_persistence_performed_by_this_kernel", False),
            ("memory_overwrite_performed", False),
            ("world_update_performed", False),
        ):
            if append_candidate.get(field) is not expected:
                errors.append(f"analytic_capsule_append_{field}_invalid")
    if dict(capsule.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("analytic_capsule_non_authority_invalid")
    if dict(capsule.get("boundary", {})) != BOUNDARY:
        errors.append("analytic_capsule_boundary_invalid")
    if capsule.get("analytic_capsule_digest") != analytic_capsule_digest(capsule):
        errors.append("analytic_capsule_digest_invalid")
    return errors


def build_memoryos_analytic_hilbert_retrieval(
    *,
    capsule: Mapping[str, Any],
    query_id: str,
    requested_surfaces: Sequence[str],
    requested_capabilities: Sequence[str],
    created_at_ms: int,
) -> dict[str, Any]:
    errors = validate_memoryos_analytic_hilbert_context_capsule(capsule)
    if errors:
        raise ValueError("analytic_capsule_invalid:" + ";".join(errors))
    surfaces = _strings(requested_surfaces, "requested_analytic_surface", allow_empty=False)
    unsupported = sorted(set(surfaces) - set(ANALYTIC_SURFACES))
    if unsupported:
        raise ValueError("requested_analytic_surface_unsupported:" + ",".join(unsupported))
    capabilities = _strings(requested_capabilities, "requested_capability")
    active_blockers = set(capsule["blocker_projection"]["active_blockers"])
    capability_blockers = {
        capability: v037.v035.BLOCKED_CAPABILITY_TO_BLOCKER[capability]
        for capability in capabilities
        if capability in v037.v035.BLOCKED_CAPABILITY_TO_BLOCKER
        and v037.v035.BLOCKED_CAPABILITY_TO_BLOCKER[capability] in active_blockers
    }
    blocked = sorted(capability_blockers)
    capsule_route = capsule["capsule_route"]
    if capsule_route == "QUARANTINE_MEMORY_SOURCE":
        route = "QUARANTINE_ANALYTIC_RETRIEVAL"
    elif blocked:
        route = "RETURN_ANALYTIC_CONTEXT_WITH_ACTIVE_SHIELD"
    elif capsule_route == "REOBSERVE_ANALYTIC_EVIDENCE":
        route = "REOBSERVE_ANALYTIC_EVIDENCE"
    elif capsule_route == "PRESERVE_RESIDUE_WITH_ANALYTIC_CONTEXT":
        route = "RETURN_ANALYTIC_CONTEXT_WITH_RESIDUE"
    else:
        route = "RETURN_READ_ONLY_HILBERT_CONTEXT"

    analytic = capsule["analytic_projection"]
    surface_values = {
        "os_reflection_form": analytic["os_reflection_form_digest"],
        "os_hilbert_vacuum": analytic["analytic_vacuum_digest"],
        "vacuum_state": analytic["vacuum_state_digest"],
        "gauge_invariance": str(analytic["gauge_invariant"]).lower(),
        "modular_time": analytic["modular_time_flow_digest"],
        "physical_time": analytic["physical_time_flow_digest"],
        "hamiltonian_vacuum": analytic["physical_hamiltonian_digest"],
    }
    retrieval = {
        "version": RETRIEVAL_VERSION,
        "query_id": _text(query_id, "query_id"),
        "source_analytic_capsule_digest": capsule["analytic_capsule_digest"],
        "requested_surfaces": surfaces,
        "requested_capabilities": capabilities,
        "selected_analytic_candidates": {
            surface: surface_values[surface] for surface in surfaces
        },
        "blocked_requested_capabilities": blocked,
        "capability_blockers": capability_blockers,
        "contradiction_residue_ids": deepcopy(
            capsule["memory_projection"]["contradiction_residue_ids"]
        ),
        "route": route,
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "read_only_context": True,
        "candidate_context_only": True,
        "automatic_blocker_discharge": False,
        "automatic_world_commit": False,
        "automatic_world_update": False,
        "automatic_plan_activation": False,
        "automatic_execution": False,
        "truth_claim": False,
        "unique_vacuum_claim": False,
        "metaphysical_kuu_identification": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "retrieval_digest": "",
    }
    retrieval["retrieval_digest"] = retrieval_digest(retrieval)
    retrieval_errors = validate_memoryos_analytic_hilbert_retrieval(retrieval)
    if retrieval_errors:
        raise ValueError(";".join(retrieval_errors))
    return retrieval


def validate_memoryos_analytic_hilbert_retrieval(
    retrieval: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if retrieval.get("version") != RETRIEVAL_VERSION:
        errors.append("analytic_retrieval_version_invalid")
    if retrieval.get("route") not in RETRIEVAL_ROUTES:
        errors.append("analytic_retrieval_route_invalid")
    for field in ("query_id", "source_analytic_capsule_digest"):
        if not isinstance(retrieval.get(field), str) or not retrieval.get(field):
            errors.append(f"analytic_retrieval_{field}_missing")
    for field in (
        "requested_surfaces",
        "requested_capabilities",
        "blocked_requested_capabilities",
        "contradiction_residue_ids",
    ):
        if not isinstance(retrieval.get(field), list):
            errors.append(f"analytic_retrieval_{field}_invalid")
    if not isinstance(retrieval.get("selected_analytic_candidates"), Mapping):
        errors.append("analytic_retrieval_candidates_invalid")
    if not isinstance(retrieval.get("capability_blockers"), Mapping):
        errors.append("analytic_retrieval_capability_blockers_invalid")
    for field, expected in (
        ("read_only_context", True),
        ("candidate_context_only", True),
        ("automatic_blocker_discharge", False),
        ("automatic_world_commit", False),
        ("automatic_world_update", False),
        ("automatic_plan_activation", False),
        ("automatic_execution", False),
        ("truth_claim", False),
        ("unique_vacuum_claim", False),
        ("metaphysical_kuu_identification", False),
    ):
        if retrieval.get(field) is not expected:
            errors.append(f"analytic_retrieval_{field}_invalid")
    if dict(retrieval.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("analytic_retrieval_non_authority_invalid")
    if retrieval.get("retrieval_digest") != retrieval_digest(retrieval):
        errors.append("analytic_retrieval_digest_invalid")
    return errors
