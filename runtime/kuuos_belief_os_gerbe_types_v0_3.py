from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import (
    canonical_json,
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    sha,
)

VERSION = "kuuos_belief_os_context_gerbe_coherence_v0_3"
PACKET_VERSION = "kuuos_belief_os_gerbe_packet_v0_3"
RECEIPT_VERSION = "kuuos_belief_os_gerbe_receipt_v0_3"
STATE_VERSION = "kuuos_belief_os_gerbe_state_v0_3"
STORE_COMMIT_VERSION = "kuuos_belief_os_gerbe_store_commit_v0_3"
APPLY_RESULT_VERSION = "kuuos_belief_os_gerbe_apply_result_v0_3"
ACTIVATION_RECEIPT_VERSION = "kuuos_belief_os_gerbe_activation_receipt_v0_3"

ROUTES = frozenset(
    {"CANDIDATE", "OBSERVE", "HOLD", "REPAIR", "REJECT", "QUARANTINE"}
)

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "global_context_authority_granted": False,
    "global_trivialization_authority_granted": False,
    "coherence_veto_authority_granted": False,
    "surface_holonomy_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "graph_route_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "v0_2_transport_receipts_are_canonical": True,
    "v0_14_gerbe_decision_is_observation_source": True,
    "declared_paths_only": True,
    "path_search_forbidden": True,
    "global_chart_ranking_forbidden": True,
    "universal_winner_forbidden": True,
    "global_trivialization_forbidden": True,
    "two_cell_residue_is_not_veto": True,
    "higher_defect_is_not_prohibition": True,
    "coherence_widening_is_conservative": True,
    "counterevidence_preserved": True,
    "surface_holonomy_append_only": True,
    "qi_history_is_context_only": True,
    "two_truths_separated": True,
    "activation_requires_replan": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def packet_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_packet_digest"))


def receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_receipt_digest"))


def state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_state_digest"))


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_store_commit_digest"))


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_apply_result_digest"))


def activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "belief_gerbe_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def clamp01(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0, maximum=1.0)


def validate_thresholds(value: Mapping[str, Any]) -> dict[str, float]:
    candidate_width = clamp01(value.get("candidate_max_width"), "candidate_max_width")
    observe_width = clamp01(value.get("observe_max_width"), "observe_max_width")
    candidate_two_cell = clamp01(
        value.get("candidate_max_two_cell_residue"),
        "candidate_max_two_cell_residue",
    )
    candidate_higher = clamp01(
        value.get("candidate_max_higher_defect"),
        "candidate_max_higher_defect",
    )
    hold_min_defect = clamp01(value.get("hold_min_defect"), "hold_min_defect")
    triple_overlap = clamp01(
        value.get("minimum_triple_overlap"), "minimum_triple_overlap"
    )
    quadruple_overlap = clamp01(
        value.get("minimum_quadruple_overlap"), "minimum_quadruple_overlap"
    )
    if candidate_width > observe_width:
        raise ValueError("gerbe_width_threshold_order_invalid")
    if candidate_two_cell > hold_min_defect:
        raise ValueError("gerbe_two_cell_threshold_order_invalid")
    if candidate_higher > hold_min_defect:
        raise ValueError("gerbe_higher_threshold_order_invalid")
    return {
        "candidate_max_width": candidate_width,
        "observe_max_width": observe_width,
        "candidate_max_two_cell_residue": candidate_two_cell,
        "candidate_max_higher_defect": candidate_higher,
        "hold_min_defect": hold_min_defect,
        "minimum_triple_overlap": triple_overlap,
        "minimum_quadruple_overlap": quadruple_overlap,
    }


def validate_packet_shell(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if packet.get("version") != PACKET_VERSION:
            errors.append("gerbe_packet_version_invalid")
        require_nonempty_string(packet.get("packet_id"), "packet_id")
        require_nonempty_string(packet.get("lineage_id"), "lineage_id")
        require_nonempty_string(packet.get("target_context_id"), "target_context_id")
        require_nonnegative_int(packet.get("created_at_ms"), "created_at_ms")
        receipts = packet.get("source_transport_receipts")
        if not isinstance(receipts, list) or not receipts:
            errors.append("source_transport_receipts_missing")
        gerbe_decision = packet.get("source_gerbe_decision")
        if not isinstance(gerbe_decision, Mapping):
            errors.append("source_gerbe_decision_missing")
        validate_thresholds(require_mapping(packet.get("thresholds"), "thresholds"))
        if packet.get("path_search_used") is not False:
            errors.append("gerbe_path_search_forbidden")
        if packet.get("global_chart_ranking_used") is not False:
            errors.append("gerbe_global_chart_ranking_forbidden")
        if packet.get("universal_winner_selected") is not False:
            errors.append("gerbe_universal_winner_forbidden")
        if packet.get("global_trivialization_used") is not False:
            errors.append("gerbe_global_trivialization_forbidden")
        if dict(packet.get("non_authority", {})) != NON_AUTHORITY_FLAGS:
            errors.append("gerbe_packet_authority_escalation")
        if packet.get("belief_gerbe_packet_digest") != packet_digest(packet):
            errors.append("gerbe_packet_digest_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
