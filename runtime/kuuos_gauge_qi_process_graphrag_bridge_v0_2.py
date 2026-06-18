from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_gauge_qi_process_graphrag_store_v0_2 import (
    validate_graph_rag_state,
)
from runtime.kuuos_gauge_qi_process_graphrag_types_v0_2 import (
    BELIEF_EVIDENCE_PACKET_VERSION,
    REPLAN_ADOPTION_VERSION,
    belief_evidence_packet_digest,
    copy_boundary,
    copy_non_authority,
    replan_adoption_digest,
    require_nonempty_string,
    require_nonnegative_int,
    validate_route,
)


def _latest_history(state: Mapping[str, Any]) -> Mapping[str, Any]:
    errors = validate_graph_rag_state(state)
    if errors:
        raise ValueError("invalid_graph_rag_state:" + ";".join(errors))
    history = list(state.get("receipt_history", []))
    if not history:
        raise ValueError("graph_rag_receipt_history_empty")
    latest = history[-1]
    if not isinstance(latest, Mapping):
        raise ValueError("graph_rag_latest_history_invalid")
    return latest


def build_belief_evidence_packet(
    *, state: Mapping[str, Any], now_ms: int
) -> dict[str, Any]:
    latest = _latest_history(state)
    route = validate_route(state.get("latest_route"), "latest_route")
    packet = {
        "version": BELIEF_EVIDENCE_PACKET_VERSION,
        "lineage_id": state["lineage_id"],
        "query_id": state["query_id"],
        "graph_rag_state_digest": state["graph_rag_state_digest"],
        "persistent_receipt_digest": state[
            "latest_persistent_receipt_digest"
        ],
        "v01_receipt_digest": state["latest_v01_receipt_digest"],
        "route": route,
        "evidence_chain_digest": state["evidence_chain_digest"],
        "holonomy_chain_digest": state["holonomy_chain_digest"],
        "observation_debt_chain_digest": state[
            "observation_debt_chain_digest"
        ],
        "next_observation_target": require_nonempty_string(
            latest.get("next_observation_target"), "next_observation_target"
        ),
        "candidate_for_belief_weighing": route == "CANDIDATE",
        "belief_authority_granted": False,
        "truth_authority_granted": False,
        "future_only": True,
        "memory_overwrite": False,
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "boundary": copy_boundary(),
        "non_authority": copy_non_authority(),
        "belief_evidence_packet_digest": "",
    }
    packet["belief_evidence_packet_digest"] = belief_evidence_packet_digest(
        packet
    )
    return packet


def build_replan_adoption_receipt(
    *,
    state: Mapping[str, Any],
    belief_state_digest: str,
    belief_commit_receipt_digest: str,
    belief_route: str,
    mission_cycle_phase: str,
    mission_cycle_state_digest: str,
    replan_receipt_digest: str,
    next_plan_basis_digest: str,
    now_ms: int,
) -> dict[str, Any]:
    _latest_history(state)
    graph_route = validate_route(state.get("latest_route"), "latest_route")
    belief_candidate_route = validate_route(belief_route, "belief_route")
    if graph_route != "CANDIDATE":
        raise ValueError("graph_rag_candidate_required")
    if belief_candidate_route != "CANDIDATE":
        raise ValueError("belief_os_candidate_required")
    if mission_cycle_phase != "replan":
        raise ValueError("mission_replan_required")

    receipt = {
        "version": REPLAN_ADOPTION_VERSION,
        "lineage_id": state["lineage_id"],
        "query_id": state["query_id"],
        "graph_rag_state_digest": state["graph_rag_state_digest"],
        "persistent_receipt_digest": state[
            "latest_persistent_receipt_digest"
        ],
        "graph_rag_route": "CANDIDATE",
        "belief_state_digest": require_nonempty_string(
            belief_state_digest, "belief_state_digest"
        ),
        "belief_commit_receipt_digest": require_nonempty_string(
            belief_commit_receipt_digest, "belief_commit_receipt_digest"
        ),
        "belief_route": "CANDIDATE",
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
        "evidence_chain_digest": state["evidence_chain_digest"],
        "holonomy_chain_digest": state["holonomy_chain_digest"],
        "observation_debt_chain_digest": state[
            "observation_debt_chain_digest"
        ],
        "belief_os_commit_required": True,
        "replan_required": True,
        "future_only": True,
        "memory_overwrite": False,
        "decision_commit_granted": False,
        "execution_authority_granted": False,
        "clinical_authority_granted": False,
        "theorem_authority_granted": False,
        "created_at_ms": require_nonnegative_int(now_ms, "now_ms"),
        "boundary": copy_boundary(),
        "non_authority": copy_non_authority(),
        "replan_adoption_receipt_digest": "",
    }
    receipt["replan_adoption_receipt_digest"] = replan_adoption_digest(
        receipt
    )
    return deepcopy(receipt)
