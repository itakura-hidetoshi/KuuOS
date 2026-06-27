from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_capabilityos_types_v0_60 import (
    VERSION, CANDIDATE_VERSION, PATH_VERSION, STATUS_OK, GUARD_ORDER,
    IMPEDIMENT_ORDER, READY, DISPOSITIONS, NON_AUTHORITY, BOUNDARY,
    _sha, _digest, _text, _nat, _names, _flags,
    build_capability_definition, validate_capability_definition,
)


def _evaluate_worlds(
    definition: Mapping[str, Any], context: Mapping[str, Any]
) -> list[dict[str, Any]]:
    required = set(definition.get("world_preconditions", []))
    raw = context.get("world_candidates", [])
    if not isinstance(raw, list):
        raise ValueError("world_candidates_invalid")
    result = []
    for index, item in enumerate(raw):
        if not isinstance(item, Mapping):
            raise ValueError("world_candidate_invalid")
        supported = set(
            _names(item.get("supported_predicates", []), "supported_predicates")
        )
        contradicted = set(
            _names(item.get("contradicted_predicates", []), "contradicted_predicates")
        )
        missing = sorted(required - supported)
        conflict = sorted(required & contradicted)
        result.append(
            {
                "world_candidate_id": _text(
                    item.get("world_candidate_id", f"world-{index}"),
                    "world_candidate_id",
                ),
                "world_fragment_digest": _text(
                    item.get(
                        "world_fragment_digest",
                        context.get("sourced_world_fragment_digest"),
                    ),
                    "world_fragment_digest",
                ),
                "applicability": (
                    not missing
                    and not conflict
                    and item.get("admissible", True) is True
                ),
                "missing_preconditions": missing,
                "contradicted_preconditions": conflict,
                "predicted_outcome_digest": _text(
                    item.get("predicted_outcome_digest", f"unresolved-{index}"),
                    "predicted_outcome_digest",
                ),
                "expected_observations": _names(
                    item.get("expected_observations", []), "expected_observations"
                ),
                "uncertainty_milli": min(
                    1000,
                    _nat(
                        item.get(
                            "uncertainty_milli",
                            int(float(item.get("uncertainty", 1.0)) * 1000),
                        ),
                        "uncertainty_milli",
                    ),
                ),
                "truth_claim": False,
                "commit_authority": False,
                "mutates_sourced_world": False,
            }
        )
    return result


def build_capability_candidate(
    *,
    definition: Mapping[str, Any],
    mission_id: str,
    lineage_id: str,
    cycle_id: str,
    chart_id: str,
    qi_receipt: Mapping[str, Any],
    yin_yang_receipt: Mapping[str, Any],
    world_context: Mapping[str, Any],
    memory_context: Mapping[str, Any] | None,
    available_tools: Sequence[str],
    available_verifiers: Sequence[str],
    requested_cost: int,
    requested_steps: int,
    requested_duration_ms: int,
    explicit_impediments: Mapping[str, Any] | None = None,
    validity_not_before_ms: int = 0,
    validity_expires_at_ms: int = 1,
) -> dict[str, Any]:
    errors = validate_capability_definition(definition)
    if errors:
        raise ValueError("definition_invalid:" + ";".join(errors))
    not_before = _nat(validity_not_before_ms, "validity_not_before_ms")
    expires = _nat(
        validity_expires_at_ms, "validity_expires_at_ms", positive=True
    )
    if expires <= not_before:
        raise ValueError("validity_interval_invalid")

    process = all(
        qi_receipt.get(key) is True
        for key in (
            "process_tensor_visible",
            "transition_continuity_visible",
            "memory_continuity_visible",
        )
    )
    yin = yin_yang_receipt.get("yin_surface", {})
    yang = yin_yang_receipt.get("yang_surface", {})
    if not isinstance(yin, Mapping) or not isinstance(yang, Mapping):
        raise ValueError("yin_yang_surface_invalid")
    guards = _flags(yin.get("blocker_vector"), GUARD_ORDER)
    guard_ok = (
        yin.get("boundary_visible") is True
        and yin.get("all_required_blockers_active") is True
        and all(guards.values())
    )
    intensity = _nat(yang.get("qi_intensity", 0), "qi_intensity")
    capacity = _nat(yang.get("qi_capacity", 0), "qi_capacity")
    saturation = intensity > capacity

    request = {
        "cost": _nat(requested_cost, "requested_cost"),
        "steps": _nat(requested_steps, "requested_steps"),
        "duration_ms": _nat(requested_duration_ms, "requested_duration_ms"),
    }
    envelope = definition["resource_envelope"]
    resource_ok = (
        request["cost"] <= envelope["max_cost"]
        and request["steps"] <= envelope["max_steps"]
        and request["duration_ms"] <= envelope["max_duration_ms"]
    )
    missing_tools = sorted(
        set(definition["required_tools"])
        - set(_names(available_tools, "available_tools"))
    )
    verifier_ok = definition["verifier_capability"] in set(
        _names(available_verifiers, "available_verifiers")
    )
    memory = dict(memory_context or {})
    review = str(memory.get("contradiction_status", "NONE")).upper() in {
        "REVIEW",
        "OPEN_REVIEW",
        "HUMAN_REVIEW",
    }

    worlds = _evaluate_worlds(definition, world_context)
    applicable = [item for item in worlds if item["applicability"]]
    plurality = len(applicable) > 1
    disagreement = (
        len({item["predicted_outcome_digest"] for item in applicable}) > 1
    )

    impediments = _flags(explicit_impediments, IMPEDIMENT_ORDER)
    impediments.update(
        {
            "missing_input": impediments["missing_input"] or not worlds,
            "stale_world_state": impediments["stale_world_state"]
            or world_context.get("stale") is True,
            "tool_unavailable": impediments["tool_unavailable"]
            or bool(missing_tools),
            "resource_insufficient": impediments["resource_insufficient"]
            or not resource_ok,
            "verifier_unavailable": impediments["verifier_unavailable"]
            or not verifier_ok,
            "unresolved_contradiction": impediments["unresolved_contradiction"]
            or review,
            "capability_saturation": impediments["capability_saturation"]
            or saturation,
        }
    )

    if not guard_ok:
        disposition = "QUARANTINE_GUARD_EVIDENCE"
    elif not process:
        disposition = "REOBSERVE_PROCESS"
    elif review:
        disposition = "REVIEW_CONTRADICTION"
    elif not verifier_ok:
        disposition = "HOLD_NO_VERIFIER"
    elif saturation:
        disposition = "CONTAIN_YANG_SATURATION"
    elif not resource_ok:
        disposition = "DECOMPOSE_CAPABILITY"
    elif missing_tools:
        disposition = "SUBSTITUTE_CAPABILITY"
    elif not worlds:
        disposition = "REOBSERVE_WORLD_PRECONDITION"
    elif not applicable:
        disposition = (
            "REOBSERVE_WORLD_PRECONDITION"
            if any(item["missing_preconditions"] for item in worlds)
            else "UNAVAILABLE_IN_CURRENT_WORLD"
        )
    elif any(
        impediments[key]
        for key in (
            "stale_world_state",
            "representation_mismatch",
            "distribution_shift",
            "unsafe_side_effect",
            "causal_model_insufficient",
        )
    ):
        disposition = "UNAVAILABLE_IN_CURRENT_WORLD"
    elif plurality and disagreement:
        disposition = "READY_WITH_WORLD_PLURALITY"
    else:
        disposition = "READY_FOR_PLANOS"

    ready = disposition in READY
    packet = {
        "version": VERSION,
        "candidate_version": CANDIDATE_VERSION,
        "capability_definition_digest": definition[
            "capability_definition_digest"
        ],
        "capability_id": definition["capability_id"],
        "capability_revision": definition["revision"],
        "provider_id": definition["provider_id"],
        "skill_digest": definition["skill_digest"],
        "mission_id": _text(mission_id, "mission_id"),
        "lineage_id": _text(lineage_id, "lineage_id"),
        "cycle_id": _text(cycle_id, "cycle_id"),
        "chart_id": _text(chart_id, "chart_id"),
        "task_type": definition["task_type"],
        "source_qi_digest": qi_receipt.get("qi_process_tensor_receipt_digest")
        or _sha(qi_receipt),
        "source_yin_yang_digest": yin_yang_receipt.get(
            "yin_yang_receipt_digest"
        )
        or _sha(yin_yang_receipt),
        "source_memory_digest": memory.get("memory_capsule_digest")
        or (_sha(memory) if memory else ""),
        "world_context": {
            "world_store_id": _text(
                world_context.get("world_store_id"), "world_store_id"
            ),
            "root_lineage_digest": _text(
                world_context.get("root_lineage_digest"),
                "root_lineage_digest",
            ),
            "world_generation": _nat(
                world_context.get("world_generation", 0), "world_generation"
            ),
            "sourced_world_fragment_digest": _text(
                world_context.get("sourced_world_fragment_digest"),
                "sourced_world_fragment_digest",
            ),
            "world_evaluations": worlds,
            "applicable_world_count": len(applicable),
            "world_plurality_visible": plurality,
            "world_disagreement_visible": disagreement,
            "world_imagination_only": True,
            "mutates_sourced_world": False,
        },
        "qi_surface": {
            "process_ready": process,
            "nonmarkov_memory_visible": qi_receipt.get(
                "nonmarkov_memory_visible"
            )
            is True,
            "qi_intensity": intensity,
            "qi_capacity": capacity,
            "saturation_detected": saturation,
            "effective_capability_support": intensity if ready else 0,
            "qi_support_is_not_truth": True,
        },
        "yin_surface": {
            "guard_vector": guards,
            "guard_meet": all(guards.values()),
            "guard_evidence_complete": guard_ok,
            "guard_occupancy_idempotent": True,
            "protective_guard_is_not_impediment": True,
        },
        "impediment_surface": {
            "impediment_vector": impediments,
            "active_impediments": [
                key for key in IMPEDIMENT_ORDER if impediments[key]
            ],
            "missing_tools": missing_tools,
            "impediment_is_not_protective_guard": True,
        },
        "resource_surface": {
            "requested": request,
            "envelope": deepcopy(envelope),
            "resource_satisfied": resource_ok,
        },
        "verification_surface": {
            "required_verifier_capability": definition["verifier_capability"],
            "verifier_available": verifier_ok,
            "independent_verification_required": True,
            "execution_success_is_not_mission_success": True,
        },
        "memory_surface": {
            "contradiction_status": str(
                memory.get("contradiction_status", "NONE")
            ).upper(),
            "contradiction_review_required": review,
            "retrieval_is_read_only": True,
            "procedural_reuse_is_not_execution": True,
        },
        "disposition": disposition,
        "ready_for_planos_candidate": ready,
        "validity_interval": {
            "not_before_ms": not_before,
            "expires_at_ms": expires,
        },
        "candidate_only": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "capability_candidate_digest": "",
    }
    packet["capability_candidate_digest"] = _digest(
        packet, "capability_candidate_digest"
    )
    return packet


def validate_capability_candidate(
    *, definition: Mapping[str, Any], candidate: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if validate_capability_definition(definition):
            errors.append("source_definition_invalid")
        if (
            candidate.get("version") != VERSION
            or candidate.get("candidate_version") != CANDIDATE_VERSION
        ):
            errors.append("candidate_version_invalid")
        if candidate.get("capability_definition_digest") != definition.get(
            "capability_definition_digest"
        ):
            errors.append("candidate_definition_mismatch")
        if candidate.get("disposition") not in DISPOSITIONS:
            errors.append("candidate_disposition_invalid")
        ready = candidate.get("disposition") in READY
        if candidate.get("ready_for_planos_candidate") is not ready:
            errors.append("candidate_ready_flag_invalid")
        qi = candidate.get("qi_surface", {})
        if not isinstance(qi, Mapping):
            errors.append("candidate_qi_surface_invalid")
        elif _nat(
            qi.get("effective_capability_support", 0), "effective_support"
        ) != (
            _nat(qi.get("qi_intensity", 0), "qi_intensity") if ready else 0
        ):
            errors.append("candidate_effective_support_invalid")
        world = candidate.get("world_context", {})
        if (
            not isinstance(world, Mapping)
            or world.get("mutates_sourced_world") is not False
            or world.get("world_imagination_only") is not True
        ):
            errors.append("candidate_world_boundary_invalid")
        if candidate.get("candidate_only") is not True:
            errors.append("candidate_only_required")
        if dict(candidate.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("candidate_authority_expansion")
        if dict(candidate.get("boundary", {})) != BOUNDARY:
            errors.append("candidate_boundary_invalid")
        if candidate.get("capability_candidate_digest") != _digest(
            candidate, "capability_candidate_digest"
        ):
            errors.append("candidate_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_capability_path_candidate(
    *, path_id: str, candidates: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    if not candidates:
        raise ValueError("path_candidates_missing")
    guards = {name: True for name in GUARD_ORDER}
    impediments = {name: False for name in IMPEDIMENT_ORDER}
    ids: list[str] = []
    digests: list[str] = []
    supports: list[int] = []
    all_ready = True
    for item in candidates:
        ids.append(_text(item.get("capability_id"), "capability_id"))
        digests.append(
            _text(item.get("capability_candidate_digest"), "candidate_digest")
        )
        qi = item.get("qi_surface", {})
        yin = item.get("yin_surface", {})
        impediment = item.get("impediment_surface", {})
        if (
            not isinstance(qi, Mapping)
            or not isinstance(yin, Mapping)
            or not isinstance(impediment, Mapping)
        ):
            raise ValueError("path_surface_invalid")
        supports.append(
            _nat(qi.get("effective_capability_support", 0), "support")
        )
        all_ready = (
            all_ready and item.get("ready_for_planos_candidate") is True
        )
        guard_vector = _flags(yin.get("guard_vector"), GUARD_ORDER)
        impediment_vector = _flags(
            impediment.get("impediment_vector"), IMPEDIMENT_ORDER
        )
        for key in GUARD_ORDER:
            guards[key] = guards[key] and guard_vector[key]
        for key in IMPEDIMENT_ORDER:
            impediments[key] = impediments[key] or impediment_vector[key]
    ready = (
        all_ready and all(guards.values()) and not any(impediments.values())
    )
    packet = {
        "version": VERSION,
        "path_version": PATH_VERSION,
        "path_id": _text(path_id, "path_id"),
        "capability_ids": ids,
        "candidate_digests": digests,
        "component_count": len(ids),
        "guard_meet": guards,
        "impediment_join": impediments,
        "effective_path_support": min(supports) if ready else 0,
        "path_ready_for_planos_candidate": ready,
        "strong_component_cannot_repair_missing_guard": True,
        "strong_component_cannot_repair_active_impediment": True,
        "candidate_only": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "capability_path_digest": "",
    }
    packet["capability_path_digest"] = _digest(
        packet, "capability_path_digest"
    )
    return packet


def validate_capability_path_candidate(
    packet: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    try:
        if (
            packet.get("version") != VERSION
            or packet.get("path_version") != PATH_VERSION
        ):
            errors.append("path_version_invalid")
        ids = packet.get("capability_ids")
        digests = packet.get("candidate_digests")
        if (
            not isinstance(ids, list)
            or not ids
            or not isinstance(digests, list)
            or len(ids) != len(digests)
            or packet.get("component_count") != len(ids)
        ):
            errors.append("path_components_invalid")
        ready = packet.get("path_ready_for_planos_candidate") is True
        if not ready and packet.get("effective_path_support") != 0:
            errors.append("path_nonready_support_not_zero")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("path_authority_expansion")
        if dict(packet.get("boundary", {})) != BOUNDARY:
            errors.append("path_boundary_invalid")
        if packet.get("capability_path_digest") != _digest(
            packet, "capability_path_digest"
        ):
            errors.append("path_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
