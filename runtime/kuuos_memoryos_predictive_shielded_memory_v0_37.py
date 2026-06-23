from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime import kuuos_memoryos_qi_world_blocker_integration_v0_35 as v035

VERSION = "kuuos_memoryos_predictive_shielded_memory_v0_37"
CAPSULE_VERSION = "memoryos_predictive_shielded_capsule_v0_37"
RETRIEVAL_VERSION = "memoryos_predictive_shielded_retrieval_v0_37"

MEMORY_TYPES = ("working", "episodic", "semantic", "procedural")
RECORD_STATUS_BY_TYPE = {
    "working": "WORKING_CONTEXT",
    "episodic": "EPISODIC_SOURCE",
    "semantic": "SEMANTIC_CONSOLIDATION_CANDIDATE",
    "procedural": "PROCEDURAL_REUSE_CANDIDATE",
}
RETENTION_ROUTE_BY_TYPE = {
    "working": "PIN_WORKING_CONTEXT",
    "episodic": "APPEND_EPISODIC_SOURCE",
    "semantic": "PROPOSE_SEMANTIC_CONSOLIDATION",
    "procedural": "PROPOSE_PROCEDURAL_REUSE",
}
RESIDUE_STATUSES = {"OPEN", "REOBSERVE", "REVIEW"}
CAPSULE_ROUTES = {
    "QUARANTINE_SOURCE_BLOCKER_EVIDENCE",
    "REOBSERVE_PREDICTIVE_STATE",
    "REVIEW_CONTRADICTION_RESIDUE",
    "PRESERVE_RESIDUE_WITH_CONTEXT",
    "READY_FOR_SHIELDED_RETRIEVAL",
}
RETRIEVAL_ROUTES = {
    "QUARANTINE_RETRIEVAL",
    "RETURN_CONTEXT_WITH_ACTIVE_SHIELD",
    "REOBSERVE_BEFORE_RETRIEVAL",
    "REVIEW_BEFORE_RETRIEVAL",
    "RETURN_CONTEXT_WITH_RESIDUE",
    "RETURN_PREDICTIVE_CONTEXT_CANDIDATE",
}

NON_AUTHORITY = {
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_execution_authority": False,
    "grants_plan_activation": False,
    "grants_actos_invocation": False,
    "grants_blocker_discharge_authority": False,
    "grants_world_commit_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_semantic_truth_promotion": False,
    "grants_procedural_execution_promotion": False,
}

BOUNDARY = {
    "memory_hierarchy_separated": True,
    "episodic_source_immutable": True,
    "semantic_consolidation_candidate_only": True,
    "procedural_memory_not_execution": True,
    "observable_predictive_state_candidate_only": True,
    "contradiction_residue_preserved": True,
    "blocker_shield_precedes_capability_return": True,
    "safe_read_only_fallback_available": True,
    "world_imagination_candidate_not_truth": True,
    "world_imagination_cannot_commit": True,
    "append_only_capsule_lineage": True,
    "source_v035_boundary_preserved": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def capsule_digest(value: Mapping[str, Any]) -> str:
    return v035.world_v034.digest(_without(value, "memory_capsule_digest"))


def retrieval_digest(value: Mapping[str, Any]) -> str:
    return v035.world_v034.digest(_without(value, "retrieval_digest"))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _milli(value: Any, field: str) -> int:
    result = _nat(value, field)
    if result > 1000:
        raise ValueError(f"{field}_invalid")
    return result


def _strings(values: Any, field: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{field}_invalid")
    result = [_text(value, field) for value in values]
    if not allow_empty and not result:
        raise ValueError(f"{field}_empty")
    if len(result) != len(set(result)):
        raise ValueError(f"{field}_duplicate")
    return result


def _normalize_record(record: Mapping[str, Any]) -> dict[str, Any]:
    memory_type = _text(record.get("memory_type"), "memory_type")
    if memory_type not in MEMORY_TYPES:
        raise ValueError("memory_type_unsupported")
    source_digests = _strings(
        record.get("source_digests", []), "record_source_digest", allow_empty=False
    )
    status = _text(record.get("status"), "record_status")
    if status != RECORD_STATUS_BY_TYPE[memory_type]:
        raise ValueError("record_status_memory_type_mismatch")
    truth_claim = record.get("truth_claim")
    if truth_claim is not False:
        raise ValueError("record_truth_claim_forbidden")
    action_authority = record.get("action_authority")
    if action_authority is not False:
        raise ValueError("record_action_authority_forbidden")
    overwrite_performed = record.get("overwrite_performed")
    if overwrite_performed is not False:
        raise ValueError("record_overwrite_forbidden")
    return {
        "record_id": _text(record.get("record_id"), "record_id"),
        "memory_type": memory_type,
        "content_digest": _text(record.get("content_digest"), "content_digest"),
        "source_digests": source_digests,
        "confidence_milli": _milli(
            record.get("confidence_milli"), "confidence_milli"
        ),
        "uncertainty_milli": _milli(
            record.get("uncertainty_milli"), "uncertainty_milli"
        ),
        "status": status,
        "retention_route": RETENTION_ROUTE_BY_TYPE[memory_type],
        "consolidation_candidate": memory_type in {"semantic", "procedural"},
        "retrieval_candidate_only": True,
        "truth_claim": False,
        "action_authority": False,
        "overwrite_performed": False,
    }


def _normalize_predictive_state(value: Mapping[str, Any]) -> dict[str, Any]:
    if value.get("representation_kind") != "OBSERVABLE_PREDICTIVE_STATE_CANDIDATE":
        raise ValueError("predictive_representation_kind_invalid")
    if value.get("latent_state_truth_claim") is not False:
        raise ValueError("predictive_latent_truth_claim_forbidden")
    if value.get("action_authority") is not False:
        raise ValueError("predictive_action_authority_forbidden")
    if not isinstance(value.get("history_sufficient"), bool):
        raise ValueError("predictive_history_sufficient_invalid")
    return {
        "representation_kind": "OBSERVABLE_PREDICTIVE_STATE_CANDIDATE",
        "observable_history_digest": _text(
            value.get("observable_history_digest"), "observable_history_digest"
        ),
        "prediction_target": _text(
            value.get("prediction_target"), "prediction_target"
        ),
        "prediction_digest": _text(
            value.get("prediction_digest"), "prediction_digest"
        ),
        "uncertainty_milli": _milli(
            value.get("uncertainty_milli"), "predictive_uncertainty_milli"
        ),
        "history_sufficient": value["history_sufficient"],
        "latent_state_truth_claim": False,
        "action_authority": False,
    }


def _normalize_world_candidate(
    value: Mapping[str, Any], source_world_fragment_digest: str
) -> dict[str, Any]:
    source_digest = _text(
        value.get("source_world_fragment_digest"),
        "source_world_fragment_digest",
    )
    if source_digest != source_world_fragment_digest:
        raise ValueError("world_candidate_source_fragment_mismatch")
    for field in (
        "truth_claim",
        "commit_authority",
        "execution_authority",
        "replaces_sourced_world",
    ):
        if value.get(field) is not False:
            raise ValueError(f"world_candidate_{field}_forbidden")
    return {
        "candidate_id": _text(value.get("candidate_id"), "world_candidate_id"),
        "source_world_fragment_digest": source_digest,
        "counterfactual_digest": _text(
            value.get("counterfactual_digest"), "counterfactual_digest"
        ),
        "uncertainty_milli": _milli(
            value.get("uncertainty_milli"), "world_candidate_uncertainty_milli"
        ),
        "truth_claim": False,
        "commit_authority": False,
        "execution_authority": False,
        "replaces_sourced_world": False,
    }


def _normalize_residue(value: Mapping[str, Any]) -> dict[str, Any]:
    status = _text(value.get("status"), "residue_status")
    if status not in RESIDUE_STATUSES:
        raise ValueError("residue_status_invalid")
    if value.get("resolved_by_consolidation") is not False:
        raise ValueError("residue_consolidation_resolution_forbidden")
    if value.get("silent_collapse") is not False:
        raise ValueError("residue_silent_collapse_forbidden")
    return {
        "residue_id": _text(value.get("residue_id"), "residue_id"),
        "left_digest": _text(value.get("left_digest"), "residue_left_digest"),
        "right_digest": _text(value.get("right_digest"), "residue_right_digest"),
        "status": status,
        "resolved_by_consolidation": False,
        "silent_collapse": False,
    }


def _normalize_unique(
    values: Any,
    normalizer: Any,
    id_field: str,
    field: str,
) -> list[dict[str, Any]]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        raise ValueError(f"{field}_invalid")
    result = [normalizer(value) for value in values]
    ids = [item[id_field] for item in result]
    if len(ids) != len(set(ids)):
        raise ValueError(f"{field}_id_duplicate")
    return result


def _expected_route(
    source_memory_route: str,
    predictive_state: Mapping[str, Any],
    residues: Sequence[Mapping[str, Any]],
) -> str:
    if source_memory_route == "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE":
        return "QUARANTINE_SOURCE_BLOCKER_EVIDENCE"
    if predictive_state.get("history_sufficient") is not True:
        return "REOBSERVE_PREDICTIVE_STATE"
    statuses = {str(value.get("status")) for value in residues}
    if "REVIEW" in statuses:
        return "REVIEW_CONTRADICTION_RESIDUE"
    if statuses:
        return "PRESERVE_RESIDUE_WITH_CONTEXT"
    return "READY_FOR_SHIELDED_RETRIEVAL"


def _validate_prior_capsule(
    prior_capsule: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if prior_capsule is None:
        return None
    errors = validate_predictive_shielded_memory_capsule(prior_capsule)
    if errors:
        raise ValueError("prior_capsule_invalid:" + ";".join(errors))
    return deepcopy(dict(prior_capsule))


def build_predictive_shielded_memory_capsule(
    *,
    source_snapshot: Mapping[str, Any],
    memory_records: Sequence[Mapping[str, Any]],
    predictive_state_candidate: Mapping[str, Any],
    world_imagination_candidates: Sequence[Mapping[str, Any]],
    contradiction_residue: Sequence[Mapping[str, Any]],
    created_at_ms: int,
    prior_capsule: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    source_errors = v035.validate_memoryos_qi_world_blocker_snapshot(source_snapshot)
    if source_errors:
        raise ValueError("source_snapshot_invalid:" + ";".join(source_errors))
    prior = _validate_prior_capsule(prior_capsule)
    records = _normalize_unique(
        memory_records, _normalize_record, "record_id", "memory_records"
    )
    predictive = _normalize_predictive_state(predictive_state_candidate)
    source_world_fragment = _text(
        source_snapshot["world_context"]["current_world_fragment_digest"],
        "source_world_fragment_digest",
    )
    world_candidates = _normalize_unique(
        world_imagination_candidates,
        lambda value: _normalize_world_candidate(value, source_world_fragment),
        "candidate_id",
        "world_imagination_candidates",
    )
    residues = _normalize_unique(
        contradiction_residue,
        _normalize_residue,
        "residue_id",
        "contradiction_residue",
    )

    if prior is None:
        sequence_index = 0
        previous_digest = v035.world_v034.ZERO_DIGEST
        previous_predictive_digest = v035.world_v034.ZERO_DIGEST
    else:
        if source_snapshot["mission_id"] != prior["mission_id"]:
            raise ValueError("capsule_mission_changed")
        if source_snapshot["lineage_id"] != prior["lineage_id"]:
            raise ValueError("capsule_lineage_changed")
        previous_source_sequence = prior["source_snapshot_sequence_index"]
        current_source_sequence = source_snapshot["sequence_index"]
        if current_source_sequence < previous_source_sequence:
            raise ValueError("source_snapshot_sequence_regressed")
        if (
            current_source_sequence == previous_source_sequence
            and source_snapshot["memory_snapshot_digest"]
            != prior["source_memory_snapshot_digest"]
        ):
            raise ValueError("source_snapshot_changed_without_sequence")
        for field, new_values in (
            ("memory_records", records),
            ("world_imagination_candidates", world_candidates),
            ("contradiction_residue", residues),
        ):
            old_values = prior[field]
            if new_values[: len(old_values)] != old_values:
                raise ValueError(f"{field}_append_only_violation")
        sequence_index = prior["sequence_index"] + 1
        previous_digest = prior["memory_capsule_digest"]
        previous_predictive_digest = prior["predictive_state_digest"]

    inventory = {
        memory_type: sum(
            1 for record in records if record["memory_type"] == memory_type
        )
        for memory_type in MEMORY_TYPES
    }
    consolidation_ids = [
        record["record_id"]
        for record in records
        if record["consolidation_candidate"] is True
    ]
    route = _expected_route(
        source_snapshot["memory_route"], predictive, residues
    )
    predictive_state_digest = v035.world_v034.digest(predictive)
    capsule = {
        "version": CAPSULE_VERSION,
        "sequence_index": sequence_index,
        "previous_memory_capsule_digest": previous_digest,
        "source_memory_snapshot_digest": source_snapshot["memory_snapshot_digest"],
        "source_snapshot_sequence_index": source_snapshot["sequence_index"],
        "source_qi_process_tensor_trace_digest": source_snapshot["qi_context"][
            "process_tensor_trace_digest"
        ],
        "source_world_fragment_digest": source_world_fragment,
        "mission_id": source_snapshot["mission_id"],
        "lineage_id": source_snapshot["lineage_id"],
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "capsule_route": route,
        "memory_records": records,
        "memory_inventory": inventory,
        "consolidation_candidate_record_ids": consolidation_ids,
        "automatic_consolidation_performed": False,
        "predictive_state_candidate": predictive,
        "predictive_state_digest": predictive_state_digest,
        "previous_predictive_state_digest": previous_predictive_digest,
        "world_imagination_candidates": world_candidates,
        "contradiction_residue": residues,
        "blocker_projection": {
            "source_memory_route": source_snapshot["memory_route"],
            "active_blockers": deepcopy(
                source_snapshot["blocker_context"]["active_blockers"]
            ),
            "missing_blockers": deepcopy(
                source_snapshot["blocker_context"]["missing_blockers"]
            ),
            "blocked_capabilities": deepcopy(
                source_snapshot["blocker_context"]["blocked_capabilities"]
            ),
            "all_required_blockers_active": source_snapshot["blocker_context"][
                "all_required_blockers_active"
            ],
            "shield_gate_required": True,
            "memory_may_discharge_blocker": False,
            "safe_fallback_route": "READ_ONLY_CONTEXT_OR_REOBSERVE",
        },
        "append_candidate": {
            "target_stream": "memoryos/predictive_shielded_memory/append_only",
            "append_only_required": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
        },
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "memory_capsule_digest": "",
    }
    capsule["memory_capsule_digest"] = capsule_digest(capsule)
    errors = validate_predictive_shielded_memory_capsule(capsule)
    if errors:
        raise ValueError(";".join(errors))
    return capsule


def validate_predictive_shielded_memory_capsule(
    capsule: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if capsule.get("version") != CAPSULE_VERSION:
        errors.append("capsule_version_invalid")
    for field in ("sequence_index", "source_snapshot_sequence_index", "created_at_ms"):
        try:
            _nat(capsule.get(field), field)
        except ValueError as exc:
            errors.append(str(exc))
    for field in (
        "previous_memory_capsule_digest",
        "source_memory_snapshot_digest",
        "source_qi_process_tensor_trace_digest",
        "source_world_fragment_digest",
        "mission_id",
        "lineage_id",
        "predictive_state_digest",
        "previous_predictive_state_digest",
    ):
        if not isinstance(capsule.get(field), str) or not capsule.get(field):
            errors.append(f"capsule_{field}_missing")
    if capsule.get("capsule_route") not in CAPSULE_ROUTES:
        errors.append("capsule_route_invalid")

    records = capsule.get("memory_records")
    normalized_records: list[dict[str, Any]] = []
    if not isinstance(records, list):
        errors.append("capsule_memory_records_invalid")
    else:
        try:
            normalized_records = _normalize_unique(
                records, _normalize_record, "record_id", "memory_records"
            )
            if records != normalized_records:
                errors.append("capsule_memory_records_not_normalized")
        except ValueError as exc:
            errors.append(str(exc))
    expected_inventory = {
        memory_type: sum(
            1 for record in normalized_records if record["memory_type"] == memory_type
        )
        for memory_type in MEMORY_TYPES
    }
    if capsule.get("memory_inventory") != expected_inventory:
        errors.append("capsule_memory_inventory_invalid")
    expected_consolidation = [
        record["record_id"]
        for record in normalized_records
        if record["consolidation_candidate"] is True
    ]
    if capsule.get("consolidation_candidate_record_ids") != expected_consolidation:
        errors.append("capsule_consolidation_inventory_invalid")
    if capsule.get("automatic_consolidation_performed") is not False:
        errors.append("capsule_automatic_consolidation_forbidden")

    predictive = capsule.get("predictive_state_candidate")
    normalized_predictive: dict[str, Any] = {}
    if not isinstance(predictive, Mapping):
        errors.append("capsule_predictive_state_invalid")
    else:
        try:
            normalized_predictive = _normalize_predictive_state(predictive)
            if dict(predictive) != normalized_predictive:
                errors.append("capsule_predictive_state_not_normalized")
            if capsule.get("predictive_state_digest") != v035.world_v034.digest(
                normalized_predictive
            ):
                errors.append("capsule_predictive_state_digest_invalid")
        except ValueError as exc:
            errors.append(str(exc))

    source_world = capsule.get("source_world_fragment_digest")
    world_candidates = capsule.get("world_imagination_candidates")
    if not isinstance(world_candidates, list) or not isinstance(source_world, str):
        errors.append("capsule_world_candidates_invalid")
    else:
        try:
            normalized_world = _normalize_unique(
                world_candidates,
                lambda value: _normalize_world_candidate(value, source_world),
                "candidate_id",
                "world_imagination_candidates",
            )
            if world_candidates != normalized_world:
                errors.append("capsule_world_candidates_not_normalized")
        except ValueError as exc:
            errors.append(str(exc))

    residues = capsule.get("contradiction_residue")
    normalized_residues: list[dict[str, Any]] = []
    if not isinstance(residues, list):
        errors.append("capsule_contradiction_residue_invalid")
    else:
        try:
            normalized_residues = _normalize_unique(
                residues, _normalize_residue, "residue_id", "contradiction_residue"
            )
            if residues != normalized_residues:
                errors.append("capsule_contradiction_residue_not_normalized")
        except ValueError as exc:
            errors.append(str(exc))

    blocker = capsule.get("blocker_projection")
    source_route = ""
    if not isinstance(blocker, Mapping):
        errors.append("capsule_blocker_projection_invalid")
    else:
        source_route = str(blocker.get("source_memory_route", ""))
        for field in ("active_blockers", "missing_blockers", "blocked_capabilities"):
            if not isinstance(blocker.get(field), list):
                errors.append(f"capsule_blocker_{field}_invalid")
        for field, expected in (
            ("shield_gate_required", True),
            ("memory_may_discharge_blocker", False),
        ):
            if blocker.get(field) is not expected:
                errors.append(f"capsule_blocker_{field}_invalid")
        if blocker.get("safe_fallback_route") != "READ_ONLY_CONTEXT_OR_REOBSERVE":
            errors.append("capsule_blocker_safe_fallback_route_invalid")
    if normalized_predictive:
        expected_route = _expected_route(
            source_route, normalized_predictive, normalized_residues
        )
        if capsule.get("capsule_route") != expected_route:
            errors.append("capsule_route_state_mismatch")

    append_candidate = capsule.get("append_candidate")
    if not isinstance(append_candidate, Mapping):
        errors.append("capsule_append_candidate_invalid")
    else:
        for field, expected in (
            ("append_only_required", True),
            ("durable_persistence_performed_by_this_kernel", False),
            ("memory_overwrite_performed", False),
            ("world_update_performed", False),
        ):
            if append_candidate.get(field) is not expected:
                errors.append(f"capsule_append_{field}_invalid")
    if dict(capsule.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("capsule_non_authority_invalid")
    if dict(capsule.get("boundary", {})) != BOUNDARY:
        errors.append("capsule_boundary_invalid")
    if capsule.get("memory_capsule_digest") != capsule_digest(capsule):
        errors.append("capsule_digest_invalid")
    return errors


def build_theory_grounded_memory_retrieval(
    *,
    capsule: Mapping[str, Any],
    query_id: str,
    requested_memory_types: Sequence[str],
    requested_capabilities: Sequence[str],
    created_at_ms: int,
) -> dict[str, Any]:
    errors = validate_predictive_shielded_memory_capsule(capsule)
    if errors:
        raise ValueError("capsule_invalid:" + ";".join(errors))
    memory_types = _strings(
        requested_memory_types, "requested_memory_type", allow_empty=False
    )
    unsupported = sorted(set(memory_types) - set(MEMORY_TYPES))
    if unsupported:
        raise ValueError("requested_memory_type_unsupported:" + ",".join(unsupported))
    capabilities = _strings(requested_capabilities, "requested_capability")
    active_blockers = set(capsule["blocker_projection"]["active_blockers"])
    capability_blockers = {
        capability: v035.BLOCKED_CAPABILITY_TO_BLOCKER[capability]
        for capability in capabilities
        if capability in v035.BLOCKED_CAPABILITY_TO_BLOCKER
        and v035.BLOCKED_CAPABILITY_TO_BLOCKER[capability] in active_blockers
    }
    blocked_capabilities = sorted(capability_blockers)
    capsule_route = capsule["capsule_route"]
    if capsule_route == "QUARANTINE_SOURCE_BLOCKER_EVIDENCE":
        route = "QUARANTINE_RETRIEVAL"
    elif blocked_capabilities:
        route = "RETURN_CONTEXT_WITH_ACTIVE_SHIELD"
    elif capsule_route == "REOBSERVE_PREDICTIVE_STATE":
        route = "REOBSERVE_BEFORE_RETRIEVAL"
    elif capsule_route == "REVIEW_CONTRADICTION_RESIDUE":
        route = "REVIEW_BEFORE_RETRIEVAL"
    elif capsule_route == "PRESERVE_RESIDUE_WITH_CONTEXT":
        route = "RETURN_CONTEXT_WITH_RESIDUE"
    else:
        route = "RETURN_PREDICTIVE_CONTEXT_CANDIDATE"
    selected_records = [
        {
            "record_id": record["record_id"],
            "memory_type": record["memory_type"],
            "content_digest": record["content_digest"],
            "status": record["status"],
        }
        for record in capsule["memory_records"]
        if record["memory_type"] in memory_types
    ]
    retrieval = {
        "version": RETRIEVAL_VERSION,
        "query_id": _text(query_id, "query_id"),
        "source_memory_capsule_digest": capsule["memory_capsule_digest"],
        "requested_memory_types": memory_types,
        "requested_capabilities": capabilities,
        "selected_record_candidates": selected_records,
        "blocked_requested_capabilities": blocked_capabilities,
        "capability_blockers": capability_blockers,
        "world_imagination_candidate_ids": [
            value["candidate_id"]
            for value in capsule["world_imagination_candidates"]
        ],
        "contradiction_residue_ids": [
            value["residue_id"] for value in capsule["contradiction_residue"]
        ],
        "predictive_state_digest": capsule["predictive_state_digest"],
        "route": route,
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "candidate_context_only": True,
        "safe_fallback_available": True,
        "automatic_consolidation": False,
        "automatic_blocker_discharge": False,
        "automatic_world_commit": False,
        "automatic_plan_activation": False,
        "automatic_execution": False,
        "truth_claim": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "retrieval_digest": "",
    }
    retrieval["retrieval_digest"] = retrieval_digest(retrieval)
    retrieval_errors = validate_theory_grounded_memory_retrieval(retrieval)
    if retrieval_errors:
        raise ValueError(";".join(retrieval_errors))
    return retrieval


def validate_theory_grounded_memory_retrieval(
    retrieval: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if retrieval.get("version") != RETRIEVAL_VERSION:
        errors.append("retrieval_version_invalid")
    if retrieval.get("route") not in RETRIEVAL_ROUTES:
        errors.append("retrieval_route_invalid")
    for field in (
        "query_id",
        "source_memory_capsule_digest",
        "predictive_state_digest",
    ):
        if not isinstance(retrieval.get(field), str) or not retrieval.get(field):
            errors.append(f"retrieval_{field}_missing")
    for field in (
        "requested_memory_types",
        "requested_capabilities",
        "selected_record_candidates",
        "blocked_requested_capabilities",
        "world_imagination_candidate_ids",
        "contradiction_residue_ids",
    ):
        if not isinstance(retrieval.get(field), list):
            errors.append(f"retrieval_{field}_invalid")
    if not isinstance(retrieval.get("capability_blockers"), Mapping):
        errors.append("retrieval_capability_blockers_invalid")
    for field, expected in (
        ("candidate_context_only", True),
        ("safe_fallback_available", True),
        ("automatic_consolidation", False),
        ("automatic_blocker_discharge", False),
        ("automatic_world_commit", False),
        ("automatic_plan_activation", False),
        ("automatic_execution", False),
        ("truth_claim", False),
    ):
        if retrieval.get(field) is not expected:
            errors.append(f"retrieval_{field}_invalid")
    if dict(retrieval.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("retrieval_non_authority_invalid")
    if retrieval.get("retrieval_digest") != retrieval_digest(retrieval):
        errors.append("retrieval_digest_invalid")
    return errors
