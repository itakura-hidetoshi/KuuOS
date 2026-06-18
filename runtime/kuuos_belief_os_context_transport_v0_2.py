from __future__ import annotations

from copy import deepcopy
from itertools import combinations
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_context_transport_types_v0_2 import (
    ACTIVATION_RECEIPT_VERSION,
    PACKET_VERSION,
    RECEIPT_VERSION,
    activation_receipt_digest,
    clamp01,
    copy_non_authority,
    normalize_declared_path,
    packet_digest,
    receipt_digest,
    require_bool,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
    transition_digest,
    validate_packet_shell,
    validate_thresholds,
)
from runtime.kuuos_belief_os_state_v0_1 import validate_belief_state


def append_unique(existing: list[str], incoming: Sequence[str]) -> list[str]:
    result = list(existing)
    seen = set(result)
    for item in incoming:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def build_atlas_transition(
    *,
    source_context_id: str,
    target_context_id: str,
    declared_path: Sequence[str],
    overlap: float,
    curvature: float,
    cocycle_defect: float,
    holonomy_residual: float,
    qi_history_compatibility: float,
    atlas_receipt_digest: str,
) -> dict[str, Any]:
    source = require_nonempty_string(source_context_id, "source_context_id")
    target = require_nonempty_string(target_context_id, "target_context_id")
    transition = {
        "source_context_id": source,
        "target_context_id": target,
        "declared_path": normalize_declared_path(
            declared_path,
            source_context_id=source,
            target_context_id=target,
        ),
        "overlap": clamp01(overlap, "overlap"),
        "curvature": clamp01(curvature, "curvature"),
        "cocycle_defect": clamp01(cocycle_defect, "cocycle_defect"),
        "holonomy_residual": clamp01(holonomy_residual, "holonomy_residual"),
        "qi_history_compatibility": clamp01(
            qi_history_compatibility, "qi_history_compatibility"
        ),
        "atlas_receipt_digest": require_nonempty_string(
            atlas_receipt_digest, "atlas_receipt_digest"
        ),
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "atlas_transition_digest": "",
    }
    transition["atlas_transition_digest"] = transition_digest(transition)
    return transition


def build_transport_packet(
    *,
    packet_id: str,
    lineage_id: str,
    target_context_id: str,
    target_context_signature_digest: str,
    atlas_bundle_digest: str,
    source_belief_states: Sequence[Mapping[str, Any]],
    transitions: Sequence[Mapping[str, Any]],
    candidate_max_width: float,
    observe_max_width: float,
    candidate_max_conflict: float,
    created_at_ms: int,
) -> dict[str, Any]:
    packet = {
        "version": PACKET_VERSION,
        "packet_id": require_nonempty_string(packet_id, "packet_id"),
        "lineage_id": require_nonempty_string(lineage_id, "lineage_id"),
        "target_context_id": require_nonempty_string(
            target_context_id, "target_context_id"
        ),
        "target_context_signature_digest": require_nonempty_string(
            target_context_signature_digest, "target_context_signature_digest"
        ),
        "atlas_bundle_digest": require_nonempty_string(
            atlas_bundle_digest, "atlas_bundle_digest"
        ),
        "source_belief_states": [deepcopy(dict(item)) for item in source_belief_states],
        "transitions": [deepcopy(dict(item)) for item in transitions],
        "thresholds": {
            "candidate_max_width": clamp01(
                candidate_max_width, "candidate_max_width"
            ),
            "observe_max_width": clamp01(observe_max_width, "observe_max_width"),
            "candidate_max_conflict": clamp01(
                candidate_max_conflict, "candidate_max_conflict"
            ),
        },
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "created_at_ms": require_nonnegative_int(created_at_ms, "created_at_ms"),
        "non_authority": copy_non_authority(),
        "belief_transport_packet_digest": "",
    }
    validate_thresholds(packet["thresholds"])
    packet["belief_transport_packet_digest"] = packet_digest(packet)
    return packet


def validate_transition(
    transition: Mapping[str, Any], *, target_context_id: str
) -> list[str]:
    errors: list[str] = []
    try:
        source = require_nonempty_string(
            transition.get("source_context_id"), "source_context_id"
        )
        target = require_nonempty_string(
            transition.get("target_context_id"), "target_context_id"
        )
        if target != target_context_id:
            errors.append("transition_target_context_mismatch")
        normalize_declared_path(
            transition.get("declared_path", []),
            source_context_id=source,
            target_context_id=target,
        )
        for field in (
            "overlap",
            "curvature",
            "cocycle_defect",
            "holonomy_residual",
            "qi_history_compatibility",
        ):
            clamp01(transition.get(field), field)
        require_nonempty_string(
            transition.get("atlas_receipt_digest"), "atlas_receipt_digest"
        )
        if transition.get("path_search_used") is not False:
            errors.append("transition_path_search_forbidden")
        if transition.get("global_chart_ranking_used") is not False:
            errors.append("transition_global_ranking_forbidden")
        if transition.get("universal_winner_selected") is not False:
            errors.append("transition_universal_winner_forbidden")
        if transition.get("atlas_transition_digest") != transition_digest(transition):
            errors.append("transition_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def validate_source_belief_state(
    state: Mapping[str, Any], *, lineage_id: str
) -> list[str]:
    errors = validate_belief_state(state)
    try:
        if state.get("lineage_id") != lineage_id:
            errors.append("source_lineage_mismatch")
        if state.get("current_phase") != "commit":
            errors.append("source_belief_not_committed")
        require_nonempty_string(
            state.get("latest_committed_belief_digest"),
            "latest_committed_belief_digest",
        )
        context = require_mapping(state.get("context"), "context")
        require_nonempty_string(context.get("context_id"), "context_id")
        credal = require_mapping(state.get("credal_state"), "credal_state")
        lower = clamp01(credal.get("lower_probability"), "lower_probability")
        upper = clamp01(credal.get("upper_probability"), "upper_probability")
        if lower > upper:
            errors.append("source_credal_interval_inverted")
        two_truths = require_mapping(state.get("two_truths"), "two_truths")
        if two_truths.get("paramartha_non_reified") is not True:
            errors.append("source_paramartha_reification")
        if two_truths.get("two_truths_separated") is not True:
            errors.append("source_two_truths_collapsed")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def transport_reliability(transition: Mapping[str, Any]) -> float:
    overlap = clamp01(transition.get("overlap"), "overlap")
    curvature = clamp01(transition.get("curvature"), "curvature")
    cocycle = clamp01(transition.get("cocycle_defect"), "cocycle_defect")
    holonomy = clamp01(transition.get("holonomy_residual"), "holonomy_residual")
    qi_compatibility = clamp01(
        transition.get("qi_history_compatibility"), "qi_history_compatibility"
    )
    result = (
        overlap
        * (1.0 - curvature)
        * (1.0 - cocycle)
        * (1.0 - holonomy)
        * qi_compatibility
    )
    return min(1.0, max(0.0, result))


def conservative_transport_interval(
    lower: float, upper: float, reliability: float
) -> dict[str, float]:
    lower_value = clamp01(lower, "source_lower")
    upper_value = clamp01(upper, "source_upper")
    if lower_value > upper_value:
        raise ValueError("source_interval_inverted")
    r = clamp01(reliability, "transport_reliability")
    transported_lower = r * lower_value
    transported_upper = r * upper_value + (1.0 - r)
    transported_lower = min(1.0, max(0.0, transported_lower))
    transported_upper = min(1.0, max(0.0, transported_upper))
    if transported_lower > lower_value + 1e-12:
        raise ValueError("transport_lower_not_conservative")
    if transported_upper + 1e-12 < upper_value:
        raise ValueError("transport_upper_not_conservative")
    if transported_lower > transported_upper + 1e-12:
        raise ValueError("transported_interval_inverted")
    return {
        "lower_probability": transported_lower,
        "upper_probability": transported_upper,
        "ignorance_width": transported_upper - transported_lower,
    }


def pairwise_conflict(intervals: Sequence[Mapping[str, float]]) -> float:
    result = 0.0
    for left, right in combinations(intervals, 2):
        left_lower = float(left["lower_probability"])
        left_upper = float(left["upper_probability"])
        right_lower = float(right["lower_probability"])
        right_upper = float(right["upper_probability"])
        gap = max(0.0, max(left_lower, right_lower) - min(left_upper, right_upper))
        result = max(result, gap)
    return min(1.0, max(0.0, result))


def transport_belief_sections(packet: Mapping[str, Any]) -> dict[str, Any]:
    errors = validate_packet_shell(packet)
    if errors:
        raise ValueError("invalid_packet:" + ";".join(errors))

    lineage_id = str(packet["lineage_id"])
    target_context_id = str(packet["target_context_id"])
    source_states = [dict(require_mapping(item, "source_belief_state")) for item in packet["source_belief_states"]]
    transitions = [dict(require_mapping(item, "transition")) for item in packet["transitions"]]

    contexts: list[str] = []
    transition_by_source: dict[str, dict[str, Any]] = {}
    transition_errors: list[str] = []
    for transition in transitions:
        transition_errors.extend(
            validate_transition(transition, target_context_id=target_context_id)
        )
        source_context = str(transition.get("source_context_id", ""))
        if source_context in transition_by_source:
            transition_errors.append("transition_source_duplicate")
        transition_by_source[source_context] = transition
    if transition_errors:
        raise ValueError("invalid_transition:" + ";".join(transition_errors))

    transported_sections: list[dict[str, Any]] = []
    transported_intervals: list[dict[str, float]] = []
    evidence_digests: list[str] = []
    counterevidence_digests: list[str] = []
    source_routes: list[str] = []

    for source_state in source_states:
        source_errors = validate_source_belief_state(
            source_state, lineage_id=lineage_id
        )
        if source_errors:
            raise ValueError("invalid_source_state:" + ";".join(source_errors))
        context = dict(source_state["context"])
        source_context_id = str(context["context_id"])
        if source_context_id in contexts:
            raise ValueError("source_context_duplicate")
        contexts.append(source_context_id)
        transition = transition_by_source.get(source_context_id)
        if transition is None:
            raise ValueError("source_transition_missing")
        reliability = transport_reliability(transition)
        source_credal = dict(source_state["credal_state"])
        transported = conservative_transport_interval(
            float(source_credal["lower_probability"]),
            float(source_credal["upper_probability"]),
            reliability,
        )
        transported_intervals.append(transported)
        evidence_digests = append_unique(
            evidence_digests, list(source_state.get("evidence_digests", []))
        )
        counterevidence_digests = append_unique(
            counterevidence_digests,
            list(source_state.get("counterevidence_digests", [])),
        )
        source_routes.append(str(source_state.get("route", "")))
        transported_sections.append(
            {
                "source_belief_id": source_state["belief_id"],
                "source_context_id": source_context_id,
                "source_belief_state_digest": source_state["belief_state_digest"],
                "source_committed_belief_digest": source_state[
                    "latest_committed_belief_digest"
                ],
                "source_route": source_state["route"],
                "source_interval": {
                    "lower_probability": source_credal["lower_probability"],
                    "upper_probability": source_credal["upper_probability"],
                },
                "transport_reliability": reliability,
                "transported_interval": transported,
                "declared_path": list(transition["declared_path"]),
                "overlap": transition["overlap"],
                "curvature": transition["curvature"],
                "cocycle_defect": transition["cocycle_defect"],
                "holonomy_residual": transition["holonomy_residual"],
                "qi_history_compatibility": transition[
                    "qi_history_compatibility"
                ],
                "atlas_transition_digest": transition["atlas_transition_digest"],
                "atlas_receipt_digest": transition["atlas_receipt_digest"],
                "evidence_digests": list(source_state.get("evidence_digests", [])),
                "counterevidence_digests": list(
                    source_state.get("counterevidence_digests", [])
                ),
            }
        )

    unused_transitions = set(transition_by_source) - set(contexts)
    if unused_transitions:
        raise ValueError("unused_transition_source")

    lower = min(item["lower_probability"] for item in transported_intervals)
    upper = max(item["upper_probability"] for item in transported_intervals)
    width = upper - lower
    conflict = pairwise_conflict(transported_intervals)
    thresholds = validate_thresholds(dict(packet["thresholds"]))

    if "QUARANTINE" in source_routes:
        route = "QUARANTINE"
    elif all(route in {"REJECT", "RETIRED"} for route in source_routes):
        route = "REJECT"
    elif conflict > thresholds["candidate_max_conflict"]:
        route = "HOLD"
    elif width > thresholds["observe_max_width"]:
        route = "REPAIR"
    elif width > thresholds["candidate_max_width"]:
        route = "OBSERVE"
    else:
        route = "CANDIDATE"

    aggregate_curvature = max(float(item["curvature"]) for item in transitions)
    aggregate_cocycle = max(float(item["cocycle_defect"]) for item in transitions)
    aggregate_holonomy = max(float(item["holonomy_residual"]) for item in transitions)
    qi_history_residual = max(
        1.0 - float(item["qi_history_compatibility"]) for item in transitions
    )

    basis = {
        "lineage_id": lineage_id,
        "target_context_id": target_context_id,
        "source_belief_state_digests": [
            item["source_belief_state_digest"] for item in transported_sections
        ],
        "aggregate_interval": {
            "lower_probability": lower,
            "upper_probability": upper,
            "ignorance_width": width,
        },
        "conflict_index": conflict,
        "route": route,
        "evidence_digests": evidence_digests,
        "counterevidence_digests": counterevidence_digests,
    }
    next_revision_basis_digest = sha(basis)

    receipt = {
        "version": RECEIPT_VERSION,
        "packet_id": packet["packet_id"],
        "lineage_id": lineage_id,
        "belief_transport_packet_digest": packet[
            "belief_transport_packet_digest"
        ],
        "target_context_id": target_context_id,
        "target_context_signature_digest": packet[
            "target_context_signature_digest"
        ],
        "atlas_bundle_digest": packet["atlas_bundle_digest"],
        "transported_sections": transported_sections,
        "plurality_count": len(transported_sections),
        "aggregate_interval": basis["aggregate_interval"],
        "conflict_index": conflict,
        "aggregate_curvature": aggregate_curvature,
        "aggregate_cocycle_defect": aggregate_cocycle,
        "aggregate_holonomy_residual": aggregate_holonomy,
        "qi_history_residual": qi_history_residual,
        "evidence_digests": evidence_digests,
        "counterevidence_digests": counterevidence_digests,
        "route": route,
        "reasoning_license": route in {"CANDIDATE", "OBSERVE"},
        "planning_support_license": route == "CANDIDATE",
        "next_revision_basis_digest": next_revision_basis_digest,
        "pending_replan_activation": route == "CANDIDATE",
        "locality_preserved": True,
        "plurality_preserved": True,
        "paramartha_non_reified": True,
        "two_truths_separated": True,
        "curvature_is_not_veto": True,
        "cocycle_defect_is_not_prohibition": True,
        "holonomy_is_not_authority": True,
        "path_search_used": False,
        "global_chart_ranking_used": False,
        "universal_winner_selected": False,
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": packet["created_at_ms"],
        "belief_transport_receipt_digest": "",
    }
    receipt["belief_transport_receipt_digest"] = receipt_digest(receipt)
    return receipt


def build_replan_transport_activation_receipt(
    *,
    transport_receipt: Mapping[str, Any],
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    if transport_receipt.get("version") != RECEIPT_VERSION:
        raise ValueError("transport_receipt_version_invalid")
    if transport_receipt.get("belief_transport_receipt_digest") != receipt_digest(
        transport_receipt
    ):
        raise ValueError("transport_receipt_digest_invalid")
    if transport_receipt.get("route") != "CANDIDATE":
        raise ValueError("transport_candidate_route_required")
    if transport_receipt.get("pending_replan_activation") is not True:
        raise ValueError("transport_not_pending_replan_activation")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")
    if transport_receipt.get("future_only") is not True:
        raise ValueError("transport_not_future_only")
    if transport_receipt.get("memory_overwrite") is not False:
        raise ValueError("transport_memory_overwrite_forbidden")

    activation = {
        "version": ACTIVATION_RECEIPT_VERSION,
        "lineage_id": transport_receipt["lineage_id"],
        "belief_transport_receipt_digest": transport_receipt[
            "belief_transport_receipt_digest"
        ],
        "transport_next_revision_basis_digest": transport_receipt[
            "next_revision_basis_digest"
        ],
        "mission_cycle_phase": "replan",
        "mission_cycle_state_digest": require_nonempty_string(
            mission_cycle_state_digest, "mission_cycle_state_digest"
        ),
        "replan_receipt_digest": require_nonempty_string(
            replan_receipt_digest, "replan_receipt_digest"
        ),
        "next_plan_basis_digest": require_nonempty_string(
            next_plan_basis_digest, "next_plan_basis_digest"
        ),
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": copy_non_authority(),
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "belief_transport_activation_receipt_digest": "",
    }
    activation["belief_transport_activation_receipt_digest"] = (
        activation_receipt_digest(activation)
    )
    return activation
