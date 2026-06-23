from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime import kuuos_memoryos_analytic_hilbert_context_v0_38 as v038

VERSION = "kuuos_memoryos_world_observe_intake_v0_39"
WORLD_CANDIDATE_VERSION = "world_vacuum_expectation_observation_candidate_packet_v0_50"
CAPSULE_VERSION = "memoryos_world_observe_intake_capsule_v0_39"
INTAKE_VERSION = "memoryos_world_observe_intake_envelope_v0_39"

CAPSULE_ROUTES = {
    "QUARANTINE_ANALYTIC_SOURCE",
    "REOBSERVE_ANALYTIC_SOURCE",
    "HOLD_INCOMPLETE_WORLD_CANDIDATE",
    "PRESERVE_RESIDUE_FOR_OBSERVE_OWNER",
    "READY_FOR_OBSERVE_OWNER_REVIEW",
}

INTAKE_ROUTES = {
    "QUARANTINE_OBSERVE_INTAKE",
    "REOBSERVE_BEFORE_OBSERVE_INTAKE",
    "HOLD_WORLD_CANDIDATE_INCOMPLETE",
    "RETURN_CANDIDATE_WITH_ACTIVE_SHIELD",
    "RETURN_CANDIDATE_WITH_RESIDUE_TO_OBSERVE_OWNER",
    "RETURN_READ_ONLY_CANDIDATE_TO_OBSERVE_OWNER",
}

_REQUIRED_TRUE_FLAGS = (
    "candidate_source_immutable",
    "value_eq_vacuum_expectation",
    "admissibility_supplied",
    "vacuum_expectation_not_fact",
    "vacuum_expectation_not_truth_authority",
    "candidate_not_belief_promotion",
    "candidate_not_plan_activation",
    "candidate_not_act_authority",
    "runtime_read_only",
)

_FORBIDDEN_PACKET_FLAGS = (
    "raw_empirical_evidence",
    "observation_record_claim",
    "verification_result_claim",
    "observe_activation_authority",
    "automatic_observe_commit",
    "plan_activation_authority",
    "actos_authority",
    "world_update_authority",
    "memory_overwrite_authority",
)

NON_AUTHORITY = {
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_observation_commit_authority": False,
    "grants_observe_activation": False,
    "grants_plan_activation": False,
    "grants_actos_authority": False,
    "grants_blocker_discharge_authority": False,
    "grants_world_update_authority": False,
    "grants_memory_overwrite_authority": False,
}

BOUNDARY = {
    "source_v038_capsule_preserved": True,
    "source_world_fragment_exactly_bound": True,
    "world_v050_candidate_exactly_bound": True,
    "world_candidate_not_empirical_evidence": True,
    "world_candidate_not_observation_record": True,
    "world_candidate_not_verification_result": True,
    "actos_effect_observation_route_not_impersonated": True,
    "observeos_owns_scope_collect_trace_assess_compare_commit": True,
    "raw_evidence_still_required": True,
    "observation_not_verification": True,
    "verification_debt_preserved": True,
    "blocker_shield_precedes_observe_intake": True,
    "contradiction_residue_preserved": True,
    "append_only_intake_lineage": True,
    "runtime_read_only": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def digest(value: Mapping[str, Any]) -> str:
    return v038.v037.v035.world_v034.digest(value)


def candidate_packet_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "candidate_packet_digest"))


def intake_capsule_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "intake_capsule_digest"))


def intake_envelope_digest(value: Mapping[str, Any]) -> str:
    return digest(_without(value, "intake_envelope_digest"))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _strings(values: Any, field: str) -> list[str]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{field}_invalid")
    result = [_text(value, field) for value in values]
    if len(result) != len(set(result)):
        raise ValueError(f"{field}_duplicate")
    return result


def normalize_world_observation_candidate_packet(
    packet: Mapping[str, Any],
    *,
    source_analytic_capsule_digest: str,
    source_world_fragment_digest: str,
) -> dict[str, Any]:
    if packet.get("version") != WORLD_CANDIDATE_VERSION:
        raise ValueError("world_candidate_packet_version_invalid")
    if (
        _text(
            packet.get("source_analytic_capsule_digest"),
            "source_analytic_capsule_digest",
        )
        != source_analytic_capsule_digest
    ):
        raise ValueError("world_candidate_analytic_capsule_mismatch")
    if (
        _text(
            packet.get("source_world_fragment_digest"),
            "source_world_fragment_digest",
        )
        != source_world_fragment_digest
    ):
        raise ValueError("world_candidate_source_world_mismatch")
    for field in _FORBIDDEN_PACKET_FLAGS:
        if packet.get(field) is not False:
            raise ValueError(f"world_candidate_{field}_forbidden")
    normalized = {
        "version": WORLD_CANDIDATE_VERSION,
        "candidate_id": _text(packet.get("candidate_id"), "candidate_id"),
        "source_analytic_capsule_digest": source_analytic_capsule_digest,
        "source_world_fragment_digest": source_world_fragment_digest,
        "observation_id_digest": _text(
            packet.get("observation_id_digest"), "observation_id_digest"
        ),
        "observation_context_digest": _text(
            packet.get("observation_context_digest"), "observation_context_digest"
        ),
        "evidence_receipt_digest": _text(
            packet.get("evidence_receipt_digest"), "evidence_receipt_digest"
        ),
        "observable_digest": _text(
            packet.get("observable_digest"), "observable_digest"
        ),
        "admissibility_receipt_digest": _text(
            packet.get("admissibility_receipt_digest"),
            "admissibility_receipt_digest",
        ),
        "candidate_value_digest": _text(
            packet.get("candidate_value_digest"), "candidate_value_digest"
        ),
        **{field: packet.get(field) is True for field in _REQUIRED_TRUE_FLAGS},
        **{field: False for field in _FORBIDDEN_PACKET_FLAGS},
        "candidate_packet_digest": "",
    }
    normalized["candidate_complete"] = all(
        normalized[field] is True for field in _REQUIRED_TRUE_FLAGS
    )
    normalized["candidate_packet_digest"] = candidate_packet_digest(normalized)
    supplied_digest = packet.get("candidate_packet_digest")
    if supplied_digest not in (None, "") and supplied_digest != normalized[
        "candidate_packet_digest"
    ]:
        raise ValueError("world_candidate_packet_digest_invalid")
    return normalized


def validate_world_observation_candidate_packet(
    packet: Mapping[str, Any],
    *,
    source_analytic_capsule_digest: str,
    source_world_fragment_digest: str,
) -> list[str]:
    try:
        normalized = normalize_world_observation_candidate_packet(
            packet,
            source_analytic_capsule_digest=source_analytic_capsule_digest,
            source_world_fragment_digest=source_world_fragment_digest,
        )
    except ValueError as exc:
        return [str(exc)]
    if dict(packet) != normalized:
        return ["world_candidate_packet_not_normalized"]
    return []


def _expected_capsule_route(
    analytic_capsule: Mapping[str, Any],
    packet: Mapping[str, Any],
) -> str:
    source_route = analytic_capsule.get("capsule_route")
    if source_route == "QUARANTINE_MEMORY_SOURCE":
        return "QUARANTINE_ANALYTIC_SOURCE"
    if source_route == "REOBSERVE_ANALYTIC_EVIDENCE":
        return "REOBSERVE_ANALYTIC_SOURCE"
    if packet.get("candidate_complete") is not True:
        return "HOLD_INCOMPLETE_WORLD_CANDIDATE"
    residue_ids = analytic_capsule.get("memory_projection", {}).get(
        "contradiction_residue_ids", []
    )
    if residue_ids:
        return "PRESERVE_RESIDUE_FOR_OBSERVE_OWNER"
    return "READY_FOR_OBSERVE_OWNER_REVIEW"


def _validate_prior_capsule(
    prior_capsule: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if prior_capsule is None:
        return None
    errors = validate_memoryos_world_observe_intake_capsule(prior_capsule)
    if errors:
        raise ValueError("prior_intake_capsule_invalid:" + ";".join(errors))
    return deepcopy(dict(prior_capsule))


def build_memoryos_world_observe_intake_capsule(
    *,
    analytic_capsule: Mapping[str, Any],
    world_candidate_packet: Mapping[str, Any],
    created_at_ms: int,
    prior_capsule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    source_errors = v038.validate_memoryos_analytic_hilbert_context_capsule(
        analytic_capsule
    )
    if source_errors:
        raise ValueError("analytic_capsule_invalid:" + ";".join(source_errors))
    prior = _validate_prior_capsule(prior_capsule)
    normalized_packet = normalize_world_observation_candidate_packet(
        world_candidate_packet,
        source_analytic_capsule_digest=analytic_capsule["analytic_capsule_digest"],
        source_world_fragment_digest=analytic_capsule[
            "source_world_fragment_digest"
        ],
    )
    if prior is None:
        sequence_index = 0
        previous_digest = v038.v037.v035.world_v034.ZERO_DIGEST
    else:
        if analytic_capsule["mission_id"] != prior["mission_id"]:
            raise ValueError("intake_capsule_mission_changed")
        if analytic_capsule["lineage_id"] != prior["lineage_id"]:
            raise ValueError("intake_capsule_lineage_changed")
        source_sequence = analytic_capsule["sequence_index"]
        if source_sequence < prior["source_analytic_sequence_index"]:
            raise ValueError("intake_source_analytic_sequence_regressed")
        if (
            source_sequence == prior["source_analytic_sequence_index"]
            and analytic_capsule["analytic_capsule_digest"]
            != prior["source_analytic_capsule_digest"]
        ):
            raise ValueError("intake_source_analytic_changed_without_sequence")
        if (
            normalized_packet["source_world_fragment_digest"]
            != prior["source_world_fragment_digest"]
        ):
            raise ValueError("intake_source_world_changed")
        if (
            normalized_packet["candidate_id"]
            == prior["world_candidate_projection"]["candidate_id"]
            and normalized_packet["candidate_packet_digest"]
            != prior["source_world_candidate_packet_digest"]
        ):
            raise ValueError("intake_candidate_identity_substituted")
        sequence_index = prior["sequence_index"] + 1
        previous_digest = prior["intake_capsule_digest"]

    residue_ids = deepcopy(
        analytic_capsule["memory_projection"]["contradiction_residue_ids"]
    )
    route = _expected_capsule_route(analytic_capsule, normalized_packet)
    capsule = {
        "version": CAPSULE_VERSION,
        "sequence_index": sequence_index,
        "previous_intake_capsule_digest": previous_digest,
        "source_analytic_capsule_digest": analytic_capsule[
            "analytic_capsule_digest"
        ],
        "source_analytic_sequence_index": analytic_capsule["sequence_index"],
        "source_memory_capsule_digest": analytic_capsule[
            "source_memory_capsule_digest"
        ],
        "source_world_fragment_digest": analytic_capsule[
            "source_world_fragment_digest"
        ],
        "source_world_candidate_packet_digest": normalized_packet[
            "candidate_packet_digest"
        ],
        "mission_id": analytic_capsule["mission_id"],
        "lineage_id": analytic_capsule["lineage_id"],
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "capsule_route": route,
        "world_candidate_projection": {
            "candidate_id": normalized_packet["candidate_id"],
            "observation_id_digest": normalized_packet["observation_id_digest"],
            "observation_context_digest": normalized_packet[
                "observation_context_digest"
            ],
            "evidence_receipt_digest": normalized_packet[
                "evidence_receipt_digest"
            ],
            "observable_digest": normalized_packet["observable_digest"],
            "admissibility_receipt_digest": normalized_packet[
                "admissibility_receipt_digest"
            ],
            "candidate_value_digest": normalized_packet[
                "candidate_value_digest"
            ],
            "candidate_complete": normalized_packet["candidate_complete"],
            "world_candidate_only": True,
            "raw_empirical_evidence": False,
            "observation_record_claim": False,
            "verification_result_claim": False,
        },
        "observe_intake_projection": {
            "target_owner": "ObserveOS",
            "route_kind": "READ_ONLY_OWNER_REVIEW_INTAKE",
            "act_effect_lineage_present": False,
            "act_effect_observation_route_impersonated": False,
            "raw_evidence_required": True,
            "raw_evidence_supplied": False,
            "observe_scope_required": True,
            "observe_collect_required": True,
            "observe_trace_required": True,
            "observe_assess_required": True,
            "observe_compare_required": True,
            "observe_commit_performed": False,
            "automatic_observe_activation": False,
            "observation_not_verification": True,
            "verification_required": True,
        },
        "contradiction_residue_ids": residue_ids,
        "blocker_projection": deepcopy(analytic_capsule["blocker_projection"]),
        "append_candidate": {
            "target_stream": "memoryos/world_observe_intake/append_only",
            "append_only_required": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
        },
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "intake_capsule_digest": "",
    }
    capsule["intake_capsule_digest"] = intake_capsule_digest(capsule)
    errors = validate_memoryos_world_observe_intake_capsule(capsule)
    if errors:
        raise ValueError(";".join(errors))
    return capsule


def validate_memoryos_world_observe_intake_capsule(
    capsule: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if capsule.get("version") != CAPSULE_VERSION:
        errors.append("intake_capsule_version_invalid")
    for field in (
        "sequence_index",
        "source_analytic_sequence_index",
        "created_at_ms",
    ):
        try:
            _nat(capsule.get(field), field)
        except ValueError as exc:
            errors.append(str(exc))
    for field in (
        "previous_intake_capsule_digest",
        "source_analytic_capsule_digest",
        "source_memory_capsule_digest",
        "source_world_fragment_digest",
        "source_world_candidate_packet_digest",
        "mission_id",
        "lineage_id",
    ):
        if not isinstance(capsule.get(field), str) or not capsule.get(field):
            errors.append(f"intake_capsule_{field}_missing")
    if capsule.get("capsule_route") not in CAPSULE_ROUTES:
        errors.append("intake_capsule_route_invalid")

    candidate = capsule.get("world_candidate_projection")
    if not isinstance(candidate, Mapping):
        errors.append("intake_capsule_candidate_projection_invalid")
    else:
        for field in (
            "candidate_id",
            "observation_id_digest",
            "observation_context_digest",
            "evidence_receipt_digest",
            "observable_digest",
            "admissibility_receipt_digest",
            "candidate_value_digest",
        ):
            if not isinstance(candidate.get(field), str) or not candidate.get(field):
                errors.append(f"intake_capsule_candidate_{field}_missing")
        for field, expected in (
            ("world_candidate_only", True),
            ("raw_empirical_evidence", False),
            ("observation_record_claim", False),
            ("verification_result_claim", False),
        ):
            if candidate.get(field) is not expected:
                errors.append(f"intake_capsule_candidate_{field}_invalid")
        if not isinstance(candidate.get("candidate_complete"), bool):
            errors.append("intake_capsule_candidate_complete_invalid")

    observe = capsule.get("observe_intake_projection")
    if not isinstance(observe, Mapping):
        errors.append("intake_capsule_observe_projection_invalid")
    else:
        if observe.get("target_owner") != "ObserveOS":
            errors.append("intake_capsule_observe_owner_invalid")
        if observe.get("route_kind") != "READ_ONLY_OWNER_REVIEW_INTAKE":
            errors.append("intake_capsule_observe_route_kind_invalid")
        for field, expected in (
            ("act_effect_lineage_present", False),
            ("act_effect_observation_route_impersonated", False),
            ("raw_evidence_required", True),
            ("raw_evidence_supplied", False),
            ("observe_scope_required", True),
            ("observe_collect_required", True),
            ("observe_trace_required", True),
            ("observe_assess_required", True),
            ("observe_compare_required", True),
            ("observe_commit_performed", False),
            ("automatic_observe_activation", False),
            ("observation_not_verification", True),
            ("verification_required", True),
        ):
            if observe.get(field) is not expected:
                errors.append(f"intake_capsule_observe_{field}_invalid")

    if not isinstance(capsule.get("contradiction_residue_ids"), list):
        errors.append("intake_capsule_residue_ids_invalid")
    blocker = capsule.get("blocker_projection")
    if not isinstance(blocker, Mapping):
        errors.append("intake_capsule_blocker_projection_invalid")
    else:
        if blocker.get("shield_gate_required") is not True:
            errors.append("intake_capsule_blocker_shield_missing")
        if blocker.get("memory_may_discharge_blocker") is not False:
            errors.append("intake_capsule_blocker_discharge_forbidden")
    append_candidate = capsule.get("append_candidate")
    if not isinstance(append_candidate, Mapping):
        errors.append("intake_capsule_append_candidate_invalid")
    else:
        for field, expected in (
            ("append_only_required", True),
            ("durable_persistence_performed_by_this_kernel", False),
            ("memory_overwrite_performed", False),
            ("world_update_performed", False),
        ):
            if append_candidate.get(field) is not expected:
                errors.append(f"intake_capsule_append_{field}_invalid")
    if dict(capsule.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("intake_capsule_non_authority_invalid")
    if dict(capsule.get("boundary", {})) != BOUNDARY:
        errors.append("intake_capsule_boundary_invalid")
    if capsule.get("intake_capsule_digest") != intake_capsule_digest(capsule):
        errors.append("intake_capsule_digest_invalid")
    return errors


def build_memoryos_world_observe_intake_envelope(
    *,
    capsule: Mapping[str, Any],
    query_id: str,
    requested_capabilities: Sequence[str],
    created_at_ms: int,
) -> dict[str, Any]:
    errors = validate_memoryos_world_observe_intake_capsule(capsule)
    if errors:
        raise ValueError("intake_capsule_invalid:" + ";".join(errors))
    capabilities = _strings(requested_capabilities, "requested_capability")
    active_blockers = set(capsule["blocker_projection"]["active_blockers"])
    mapping = v038.v037.v035.BLOCKED_CAPABILITY_TO_BLOCKER
    capability_blockers = {
        capability: mapping[capability]
        for capability in capabilities
        if capability in mapping and mapping[capability] in active_blockers
    }
    blocked = sorted(capability_blockers)
    capsule_route = capsule["capsule_route"]
    if capsule_route == "QUARANTINE_ANALYTIC_SOURCE":
        route = "QUARANTINE_OBSERVE_INTAKE"
    elif capsule_route == "REOBSERVE_ANALYTIC_SOURCE":
        route = "REOBSERVE_BEFORE_OBSERVE_INTAKE"
    elif capsule_route == "HOLD_INCOMPLETE_WORLD_CANDIDATE":
        route = "HOLD_WORLD_CANDIDATE_INCOMPLETE"
    elif blocked:
        route = "RETURN_CANDIDATE_WITH_ACTIVE_SHIELD"
    elif capsule_route == "PRESERVE_RESIDUE_FOR_OBSERVE_OWNER":
        route = "RETURN_CANDIDATE_WITH_RESIDUE_TO_OBSERVE_OWNER"
    else:
        route = "RETURN_READ_ONLY_CANDIDATE_TO_OBSERVE_OWNER"

    envelope = {
        "version": INTAKE_VERSION,
        "query_id": _text(query_id, "query_id"),
        "source_intake_capsule_digest": capsule["intake_capsule_digest"],
        "source_world_candidate_packet_digest": capsule[
            "source_world_candidate_packet_digest"
        ],
        "candidate_id": capsule["world_candidate_projection"]["candidate_id"],
        "observation_id_digest": capsule["world_candidate_projection"][
            "observation_id_digest"
        ],
        "requested_capabilities": capabilities,
        "blocked_requested_capabilities": blocked,
        "capability_blockers": capability_blockers,
        "contradiction_residue_ids": deepcopy(
            capsule["contradiction_residue_ids"]
        ),
        "route": route,
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "target_owner": "ObserveOS",
        "world_candidate_only": True,
        "raw_empirical_evidence": False,
        "observation_record_created": False,
        "verification_result_created": False,
        "act_effect_lineage_present": False,
        "observe_owner_review_required": True,
        "observe_scope_required": True,
        "observe_collection_required": True,
        "observe_commit_performed": False,
        "automatic_observe_activation": False,
        "observation_not_verification": True,
        "verification_required": True,
        "automatic_blocker_discharge": False,
        "automatic_plan_activation": False,
        "automatic_execution": False,
        "automatic_world_update": False,
        "memory_overwrite": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "intake_envelope_digest": "",
    }
    envelope["intake_envelope_digest"] = intake_envelope_digest(envelope)
    envelope_errors = validate_memoryos_world_observe_intake_envelope(envelope)
    if envelope_errors:
        raise ValueError(";".join(envelope_errors))
    return envelope


def validate_memoryos_world_observe_intake_envelope(
    envelope: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if envelope.get("version") != INTAKE_VERSION:
        errors.append("observe_intake_version_invalid")
    if envelope.get("route") not in INTAKE_ROUTES:
        errors.append("observe_intake_route_invalid")
    for field in (
        "query_id",
        "source_intake_capsule_digest",
        "source_world_candidate_packet_digest",
        "candidate_id",
        "observation_id_digest",
    ):
        if not isinstance(envelope.get(field), str) or not envelope.get(field):
            errors.append(f"observe_intake_{field}_missing")
    for field in (
        "requested_capabilities",
        "blocked_requested_capabilities",
        "contradiction_residue_ids",
    ):
        if not isinstance(envelope.get(field), list):
            errors.append(f"observe_intake_{field}_invalid")
    if not isinstance(envelope.get("capability_blockers"), Mapping):
        errors.append("observe_intake_capability_blockers_invalid")
    for field, expected in (
        ("target_owner", "ObserveOS"),
        ("world_candidate_only", True),
        ("raw_empirical_evidence", False),
        ("observation_record_created", False),
        ("verification_result_created", False),
        ("act_effect_lineage_present", False),
        ("observe_owner_review_required", True),
        ("observe_scope_required", True),
        ("observe_collection_required", True),
        ("observe_commit_performed", False),
        ("automatic_observe_activation", False),
        ("observation_not_verification", True),
        ("verification_required", True),
        ("automatic_blocker_discharge", False),
        ("automatic_plan_activation", False),
        ("automatic_execution", False),
        ("automatic_world_update", False),
        ("memory_overwrite", False),
    ):
        if envelope.get(field) != expected:
            errors.append(f"observe_intake_{field}_invalid")
    if dict(envelope.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("observe_intake_non_authority_invalid")
    if envelope.get("intake_envelope_digest") != intake_envelope_digest(envelope):
        errors.append("observe_intake_digest_invalid")
    return errors
