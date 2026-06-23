from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime import kuuos_authorized_atomic_world_commit_v0_34 as world_v034
from runtime import kuuos_nonmarkov_cognitive_loop_kernel_v0_23 as memory_v023
from runtime import kuuos_qi_world_cross_cycle_blocker_v1_5 as blocker_v15

VERSION = "kuuos_memoryos_qi_world_blocker_integration_v0_35"
SNAPSHOT_VERSION = "memoryos_qi_world_blocker_snapshot_v0_35"
RETRIEVAL_VERSION = "memoryos_qi_world_blocker_retrieval_v0_35"

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_truth_authority": False,
    "grants_verification_authority": False,
    "grants_blocker_discharge_authority": False,
    "grants_world_commit_authority": False,
    "grants_world_rewrite_authority": False,
    "grants_constitutional_root_rewrite": False,
    "grants_memory_overwrite_authority": False,
    "grants_plan_activation": False,
    "grants_actos_invocation": False,
}

BOUNDARY = {
    "qi_history_preserved": True,
    "snapshot_does_not_replace_process_history": True,
    "blocker_certificate_preserved_as_context": True,
    "memory_cannot_discharge_blocker": True,
    "missing_blocker_evidence_fails_closed": True,
    "world_store_is_exact_source_not_truth": True,
    "world_generation_history_is_append_only": True,
    "memory_projection_is_read_only": True,
    "memory_append_candidate_not_durable_claim": True,
    "candidate_world_not_collapsed_to_fact": True,
    "same_root_required": True,
    "future_retrieval_is_conditioned_not_authoritative": True,
}

BLOCKED_CAPABILITY_TO_BLOCKER = {
    capability: blocker
    for blocker, capability in blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER.items()
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def snapshot_digest(value: Mapping[str, Any]) -> str:
    return world_v034.digest(_without(value, "memory_snapshot_digest"))


def retrieval_digest(value: Mapping[str, Any]) -> str:
    return world_v034.digest(_without(value, "retrieval_context_digest"))


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field}_invalid")
    return value.strip()


def _nat(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{field}_invalid")
    return value


def _strings(values: Sequence[Any], field: str) -> list[str]:
    result = [_text(value, field) for value in values]
    if len(result) != len(set(result)):
        raise ValueError(f"{field}_duplicate")
    return result


def _validate_prior_snapshot(
    prior_snapshot: Mapping[str, Any] | None,
) -> dict[str, Any] | None:
    if prior_snapshot is None:
        return None
    errors = validate_memoryos_qi_world_blocker_snapshot(prior_snapshot)
    if errors:
        raise ValueError("prior_snapshot_invalid:" + ";".join(errors))
    return dict(prior_snapshot)


def _validate_sources(
    *,
    cognitive_episode: Mapping[str, Any],
    source_cross_cycle_receipt: Mapping[str, Any],
    blocker_certificate: Mapping[str, Any],
    world_store: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    episode_errors = memory_v023.validate_nonmarkov_cognitive_episode(cognitive_episode)
    if episode_errors:
        raise ValueError("cognitive_episode_invalid:" + ";".join(episode_errors))

    blocker_errors = blocker_v15.validate_cross_cycle_blocker_certificate(
        source_cross_cycle_receipt, blocker_certificate
    )
    inactive_errors = {
        f"blocker_{name}_inactive" for name in blocker_v15.BLOCKER_ORDER
    }
    structural_errors = [
        error for error in blocker_errors if error not in inactive_errors
    ]
    if structural_errors:
        raise ValueError(
            "blocker_certificate_invalid:" + ";".join(structural_errors)
        )
    if blocker_errors and blocker_certificate.get("disposition") != (
        "QUARANTINE_BLOCKER_EVIDENCE_INCOMPLETE"
    ):
        raise ValueError("inactive_blocker_without_quarantine")

    world_body = world_v034.validate_world_store(world_store)
    if blocker_certificate.get("source_cross_cycle_receipt_digest") != (
        source_cross_cycle_receipt.get("cross_cycle_receipt_digest")
    ):
        raise ValueError("blocker_source_receipt_digest_mismatch")

    return dict(cognitive_episode), dict(world_body)


def build_memoryos_qi_world_blocker_snapshot(
    *,
    cognitive_episode: Mapping[str, Any],
    source_cross_cycle_receipt: Mapping[str, Any],
    blocker_certificate: Mapping[str, Any],
    world_store: Mapping[str, Any],
    created_at_ms: int,
    prior_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    episode, world_body = _validate_sources(
        cognitive_episode=cognitive_episode,
        source_cross_cycle_receipt=source_cross_cycle_receipt,
        blocker_certificate=blocker_certificate,
        world_store=world_store,
    )
    prior = _validate_prior_snapshot(prior_snapshot)
    created = _nat(created_at_ms, "created_at_ms")

    active_blockers = _strings(
        blocker_certificate.get("active_blockers", []), "active_blocker"
    )
    missing_blockers = _strings(
        blocker_certificate.get("missing_blockers", []), "missing_blocker"
    )
    blocked_capabilities = _strings(
        blocker_certificate.get("blocked_capabilities", []), "blocked_capability"
    )
    all_active = blocker_certificate.get("all_required_blockers_active") is True

    vector = blocker_certificate.get("composed_blocker_vector", {})
    if not isinstance(vector, Mapping):
        raise ValueError("blocker_vector_invalid")
    expected_active = [
        name for name in blocker_v15.BLOCKER_ORDER if vector.get(name) is True
    ]
    expected_missing = [
        name for name in blocker_v15.BLOCKER_ORDER if vector.get(name) is not True
    ]
    expected_blocked_capabilities = [
        blocker_v15.BLOCKED_CAPABILITY_BY_BLOCKER[name]
        for name in expected_active
    ]
    if active_blockers != expected_active or missing_blockers != expected_missing:
        raise ValueError("blocker_inventory_mismatch")
    if blocked_capabilities != expected_blocked_capabilities:
        raise ValueError("blocked_capability_inventory_mismatch")
    if all_active != (not missing_blockers):
        raise ValueError("blocker_all_active_flag_mismatch")

    if prior is None:
        sequence_index = 0
        previous_snapshot_digest = world_v034.ZERO_DIGEST
        previous_world_generation = None
        previous_world_fragment_digest = None
        world_transition = "GENESIS_MEMORY_PROJECTION"
    else:
        sequence_index = int(prior["sequence_index"]) + 1
        previous_snapshot_digest = prior["memory_snapshot_digest"]
        previous_world_generation = prior["world_context"]["generation"]
        previous_world_fragment_digest = prior["world_context"][
            "current_world_fragment_digest"
        ]
        if world_body["world_store_id"] != prior["world_context"]["world_store_id"]:
            raise ValueError("world_store_identity_changed")
        if world_body["root_lineage_digest"] != prior["world_context"][
            "root_lineage_digest"
        ]:
            raise ValueError("world_root_lineage_changed")
        if world_body["generation"] < previous_world_generation:
            raise ValueError("world_generation_regressed")
        if world_body["generation"] == previous_world_generation:
            if (
                world_body["current_world_fragment_digest"]
                != previous_world_fragment_digest
            ):
                raise ValueError("world_fragment_changed_without_generation")
            world_transition = "WORLD_GENERATION_UNCHANGED"
        else:
            world_transition = "WORLD_GENERATION_ADVANCED"

    disposition = str(blocker_certificate.get("disposition", ""))
    memory_route = (
        "PRESERVE_BLOCKED_CONTEXT"
        if all_active
        else "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE"
    )

    handoff = episode.get("handoff", {})
    if not isinstance(handoff, Mapping):
        handoff = {}
    qi_handoff = handoff.get("qi_process_tensor", {})
    if not isinstance(qi_handoff, Mapping):
        qi_handoff = {}

    snapshot = {
        "version": SNAPSHOT_VERSION,
        "sequence_index": sequence_index,
        "previous_memory_snapshot_digest": previous_snapshot_digest,
        "source_cognitive_episode_digest": episode["cognitive_episode_digest"],
        "source_cross_cycle_receipt_digest": source_cross_cycle_receipt[
            "cross_cycle_receipt_digest"
        ],
        "source_blocker_certificate_digest": blocker_certificate[
            "blocker_certificate_digest"
        ],
        "source_world_store_digest": world_store["body_digest"],
        "mission_id": episode["mission_id"],
        "lineage_id": episode["lineage_id"],
        "created_at_ms": created,
        "memory_route": memory_route,
        "qi_context": {
            "process_tensor_trace_digest": episode["process_tensor_trace_digest"],
            "memory_mode": episode["memory_mode"],
            "verification_route": episode["verification_route"],
            "observation_route": episode["observation_route"],
            "plan_route": episode["plan_route"],
            "recoverability_projection": deepcopy(
                qi_handoff.get("recoverability_projection", {})
            ),
            "process_summary": deepcopy(qi_handoff.get("process_summary", {})),
            "process_history_preserved": True,
            "snapshot_replacement_used": False,
            "qi_grants_authority": False,
        },
        "blocker_context": {
            "disposition": disposition,
            "active_blockers": active_blockers,
            "missing_blockers": missing_blockers,
            "blocked_capabilities": blocked_capabilities,
            "all_required_blockers_active": all_active,
            "contextual_not_root_sovereignty": blocker_certificate.get(
                "contextual_not_root_sovereignty"
            )
            is True,
            "repairable_by_new_evidence": blocker_certificate.get(
                "repairable_by_new_evidence"
            )
            is True,
            "memory_may_discharge_blocker": False,
            "memory_may_silently_repair_missing_evidence": False,
        },
        "world_context": {
            "world_store_id": world_body["world_store_id"],
            "root_lineage_digest": world_body["root_lineage_digest"],
            "generation": world_body["generation"],
            "current_world_fragment_digest": world_body[
                "current_world_fragment_digest"
            ],
            "last_commit_digest": world_body["last_commit_digest"],
            "commit_history_length": len(world_body["commits"]),
            "previous_projection_generation": previous_world_generation,
            "previous_projection_fragment_digest": previous_world_fragment_digest,
            "transition": world_transition,
            "projection_only": True,
            "world_store_is_truth": False,
            "memory_may_commit_world": False,
            "memory_may_rewrite_world": False,
            "constitutional_root_rewritten": False,
        },
        "append_candidate": {
            "target_stream": "memoryos/qi_world_blocker/append_only",
            "append_only_required": True,
            "durable_persistence_performed_by_this_kernel": False,
            "memory_overwrite_performed": False,
            "world_update_performed": False,
        },
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "memory_snapshot_digest": "",
    }
    snapshot["memory_snapshot_digest"] = snapshot_digest(snapshot)
    errors = validate_memoryos_qi_world_blocker_snapshot(snapshot)
    if errors:
        raise ValueError(";".join(errors))
    return snapshot


def validate_memoryos_qi_world_blocker_snapshot(
    snapshot: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if snapshot.get("version") != SNAPSHOT_VERSION:
        errors.append("snapshot_version_invalid")
    try:
        _nat(snapshot.get("sequence_index"), "sequence_index")
        _nat(snapshot.get("created_at_ms"), "created_at_ms")
    except ValueError as exc:
        errors.append(str(exc))

    for field in (
        "previous_memory_snapshot_digest",
        "source_cognitive_episode_digest",
        "source_cross_cycle_receipt_digest",
        "source_blocker_certificate_digest",
        "source_world_store_digest",
        "mission_id",
        "lineage_id",
    ):
        if not isinstance(snapshot.get(field), str) or not snapshot.get(field):
            errors.append(f"snapshot_{field}_missing")

    if snapshot.get("memory_route") not in {
        "PRESERVE_BLOCKED_CONTEXT",
        "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE",
    }:
        errors.append("snapshot_memory_route_invalid")

    qi = snapshot.get("qi_context")
    if not isinstance(qi, Mapping):
        errors.append("snapshot_qi_context_invalid")
    else:
        for field, expected in (
            ("process_history_preserved", True),
            ("snapshot_replacement_used", False),
            ("qi_grants_authority", False),
        ):
            if qi.get(field) is not expected:
                errors.append(f"snapshot_qi_{field}_invalid")

    blocker = snapshot.get("blocker_context")
    if not isinstance(blocker, Mapping):
        errors.append("snapshot_blocker_context_invalid")
    else:
        active = blocker.get("active_blockers")
        missing = blocker.get("missing_blockers")
        blocked = blocker.get("blocked_capabilities")
        if not isinstance(active, list) or not isinstance(missing, list):
            errors.append("snapshot_blocker_inventory_invalid")
        if not isinstance(blocked, list):
            errors.append("snapshot_blocked_capabilities_invalid")
        for field, expected in (
            ("memory_may_discharge_blocker", False),
            ("memory_may_silently_repair_missing_evidence", False),
        ):
            if blocker.get(field) is not expected:
                errors.append(f"snapshot_blocker_{field}_invalid")
        all_active = blocker.get("all_required_blockers_active") is True
        if all_active and snapshot.get("memory_route") != "PRESERVE_BLOCKED_CONTEXT":
            errors.append("snapshot_active_blocker_route_invalid")
        if not all_active and snapshot.get("memory_route") != (
            "QUARANTINE_INCOMPLETE_BLOCKER_EVIDENCE"
        ):
            errors.append("snapshot_incomplete_blocker_route_invalid")

    world = snapshot.get("world_context")
    if not isinstance(world, Mapping):
        errors.append("snapshot_world_context_invalid")
    else:
        for field, expected in (
            ("projection_only", True),
            ("world_store_is_truth", False),
            ("memory_may_commit_world", False),
            ("memory_may_rewrite_world", False),
            ("constitutional_root_rewritten", False),
        ):
            if world.get(field) is not expected:
                errors.append(f"snapshot_world_{field}_invalid")
        try:
            generation = _nat(world.get("generation"), "world_generation")
            history_length = _nat(
                world.get("commit_history_length"), "world_commit_history_length"
            )
            if generation != history_length:
                errors.append("snapshot_world_history_length_mismatch")
        except ValueError as exc:
            errors.append(str(exc))

    append_candidate = snapshot.get("append_candidate")
    if not isinstance(append_candidate, Mapping):
        errors.append("snapshot_append_candidate_invalid")
    else:
        for field, expected in (
            ("append_only_required", True),
            ("durable_persistence_performed_by_this_kernel", False),
            ("memory_overwrite_performed", False),
            ("world_update_performed", False),
        ):
            if append_candidate.get(field) is not expected:
                errors.append(f"snapshot_append_{field}_invalid")

    if dict(snapshot.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("snapshot_non_authority_invalid")
    if dict(snapshot.get("boundary", {})) != BOUNDARY:
        errors.append("snapshot_boundary_invalid")
    if snapshot.get("memory_snapshot_digest") != snapshot_digest(snapshot):
        errors.append("snapshot_digest_invalid")
    return errors


def build_memoryos_conditioned_retrieval(
    *,
    snapshot: Mapping[str, Any],
    requested_capabilities: Sequence[str],
    query_id: str,
    created_at_ms: int,
) -> dict[str, Any]:
    errors = validate_memoryos_qi_world_blocker_snapshot(snapshot)
    if errors:
        raise ValueError("snapshot_invalid:" + ";".join(errors))

    requested = _strings(requested_capabilities, "requested_capability")
    active_blockers = set(snapshot["blocker_context"]["active_blockers"])
    capability_blockers = {
        capability: BLOCKED_CAPABILITY_TO_BLOCKER[capability]
        for capability in requested
        if capability in BLOCKED_CAPABILITY_TO_BLOCKER
        and BLOCKED_CAPABILITY_TO_BLOCKER[capability] in active_blockers
    }
    blocked_requested = sorted(capability_blockers)
    if snapshot["blocker_context"]["all_required_blockers_active"] is not True:
        route = "QUARANTINE_RETRIEVAL"
    elif blocked_requested:
        route = "RETURN_CONTEXT_WITH_ACTIVE_BLOCKER"
    else:
        route = "RETURN_CONDITIONED_CONTEXT_CANDIDATE"

    retrieval = {
        "version": RETRIEVAL_VERSION,
        "query_id": _text(query_id, "query_id"),
        "source_memory_snapshot_digest": snapshot["memory_snapshot_digest"],
        "requested_capabilities": requested,
        "blocked_requested_capabilities": blocked_requested,
        "capability_blockers": capability_blockers,
        "route": route,
        "qi_process_tensor_trace_digest": snapshot["qi_context"][
            "process_tensor_trace_digest"
        ],
        "world_store_id": snapshot["world_context"]["world_store_id"],
        "world_generation": snapshot["world_context"]["generation"],
        "world_fragment_digest": snapshot["world_context"][
            "current_world_fragment_digest"
        ],
        "created_at_ms": _nat(created_at_ms, "created_at_ms"),
        "candidate_context_only": True,
        "automatic_plan_mutation": False,
        "automatic_blocker_discharge": False,
        "automatic_world_commit": False,
        "automatic_execution": False,
        "truth_claim": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "retrieval_context_digest": "",
    }
    retrieval["retrieval_context_digest"] = retrieval_digest(retrieval)
    retrieval_errors = validate_memoryos_conditioned_retrieval(retrieval)
    if retrieval_errors:
        raise ValueError(";".join(retrieval_errors))
    return retrieval


def validate_memoryos_conditioned_retrieval(
    retrieval: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if retrieval.get("version") != RETRIEVAL_VERSION:
        errors.append("retrieval_version_invalid")
    if retrieval.get("route") not in {
        "QUARANTINE_RETRIEVAL",
        "RETURN_CONTEXT_WITH_ACTIVE_BLOCKER",
        "RETURN_CONDITIONED_CONTEXT_CANDIDATE",
    }:
        errors.append("retrieval_route_invalid")
    for field in (
        "query_id",
        "source_memory_snapshot_digest",
        "qi_process_tensor_trace_digest",
        "world_store_id",
        "world_fragment_digest",
    ):
        if not isinstance(retrieval.get(field), str) or not retrieval.get(field):
            errors.append(f"retrieval_{field}_missing")
    for field in (
        "requested_capabilities",
        "blocked_requested_capabilities",
    ):
        if not isinstance(retrieval.get(field), list):
            errors.append(f"retrieval_{field}_invalid")
    if not isinstance(retrieval.get("capability_blockers"), Mapping):
        errors.append("retrieval_capability_blockers_invalid")
    for field, expected in (
        ("candidate_context_only", True),
        ("automatic_plan_mutation", False),
        ("automatic_blocker_discharge", False),
        ("automatic_world_commit", False),
        ("automatic_execution", False),
        ("truth_claim", False),
    ):
        if retrieval.get(field) is not expected:
            errors.append(f"retrieval_{field}_invalid")
    if dict(retrieval.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("retrieval_non_authority_invalid")
    if retrieval.get("retrieval_context_digest") != retrieval_digest(retrieval):
        errors.append("retrieval_digest_invalid")
    return errors


__all__ = [
    "BLOCKED_CAPABILITY_TO_BLOCKER",
    "BOUNDARY",
    "NON_AUTHORITY",
    "RETRIEVAL_VERSION",
    "SNAPSHOT_VERSION",
    "VERSION",
    "build_memoryos_conditioned_retrieval",
    "build_memoryos_qi_world_blocker_snapshot",
    "retrieval_digest",
    "snapshot_digest",
    "validate_memoryos_conditioned_retrieval",
    "validate_memoryos_qi_world_blocker_snapshot",
]
