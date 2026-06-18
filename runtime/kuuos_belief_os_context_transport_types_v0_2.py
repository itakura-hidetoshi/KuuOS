from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import (
    canonical_json,
    require_bool,
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    require_unique_strings,
    sha,
)

VERSION = "kuuos_belief_os_context_gauge_credal_transport_v0_2"
PACKET_VERSION = "kuuos_belief_os_context_transport_packet_v0_2"
RECEIPT_VERSION = "kuuos_belief_os_context_transport_receipt_v0_2"
STATE_VERSION = "kuuos_belief_os_context_transport_state_v0_2"
STORE_COMMIT_VERSION = "kuuos_belief_os_context_transport_store_commit_v0_2"
APPLY_RESULT_VERSION = "kuuos_belief_os_context_transport_apply_result_v0_2"
ACTIVATION_RECEIPT_VERSION = "kuuos_belief_os_context_transport_activation_receipt_v0_2"

ROUTES = frozenset({"CANDIDATE", "OBSERVE", "HOLD", "REPAIR", "REJECT", "QUARANTINE"})

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "global_context_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "graph_route_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "source_belief_os_v0_1_is_canonical": True,
    "contexts_are_local_charts": True,
    "declared_paths_only": True,
    "path_search_forbidden": True,
    "global_chart_ranking_forbidden": True,
    "universal_winner_forbidden": True,
    "transport_is_conservative": True,
    "plurality_hull_required": True,
    "counterevidence_preserved": True,
    "curvature_is_not_veto": True,
    "cocycle_defect_is_not_prohibition": True,
    "holonomy_is_not_authority": True,
    "qi_history_is_context_only": True,
    "two_truths_separated": True,
    "activation_requires_replan": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def packet_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_packet_digest"))


def transition_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "atlas_transition_digest"))


def receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_receipt_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_state_digest"))


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_store_commit_digest"))


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_apply_result_digest"))


def activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_transport_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def clamp01(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0, maximum=1.0)


def normalize_declared_path(
    value: Sequence[Any], *, source_context_id: str, target_context_id: str
) -> list[str]:
    path = require_unique_strings(value, "declared_path", allow_empty=False)
    if len(path) < 2:
        raise ValueError("declared_path_too_short")
    if path[0] != source_context_id:
        raise ValueError("declared_path_source_mismatch")
    if path[-1] != target_context_id:
        raise ValueError("declared_path_target_mismatch")
    return path


def validate_thresholds(value: Mapping[str, Any]) -> dict[str, float]:
    candidate_width = clamp01(value.get("candidate_max_width"), "candidate_max_width")
    observe_width = clamp01(value.get("observe_max_width"), "observe_max_width")
    conflict = clamp01(value.get("candidate_max_conflict"), "candidate_max_conflict")
    if candidate_width > observe_width:
        raise ValueError("transport_width_threshold_order_invalid")
    return {
        "candidate_max_width": candidate_width,
        "observe_max_width": observe_width,
        "candidate_max_conflict": conflict,
    }


def validate_packet_shell(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if packet.get("version") != PACKET_VERSION:
            errors.append("packet_version_invalid")
        require_nonempty_string(packet.get("packet_id"), "packet_id")
        require_nonempty_string(packet.get("lineage_id"), "lineage_id")
        require_nonempty_string(packet.get("target_context_id"), "target_context_id")
        require_nonempty_string(
            packet.get("target_context_signature_digest"),
            "target_context_signature_digest",
        )
        require_nonempty_string(packet.get("atlas_bundle_digest"), "atlas_bundle_digest")
        require_nonnegative_int(packet.get("created_at_ms"), "created_at_ms")
        if packet.get("path_search_used") is not False:
            errors.append("path_search_forbidden")
        if packet.get("global_chart_ranking_used") is not False:
            errors.append("global_chart_ranking_forbidden")
        if packet.get("universal_winner_selected") is not False:
            errors.append("universal_winner_forbidden")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("packet_authority_escalation")
        validate_thresholds(require_mapping(packet.get("thresholds"), "thresholds"))
        source_states = packet.get("source_belief_states")
        if not isinstance(source_states, list) or not source_states:
            errors.append("source_belief_states_missing")
        transitions = packet.get("transitions")
        if not isinstance(transitions, list) or not transitions:
            errors.append("transitions_missing")
        if packet.get("belief_transport_packet_digest") != packet_digest(packet):
            errors.append("packet_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
