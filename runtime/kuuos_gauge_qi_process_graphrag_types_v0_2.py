from __future__ import annotations

from copy import deepcopy
from math import isfinite
from typing import Any, Mapping

from runtime.kuuos_gauge_qi_process_graphrag_v0_1 import ROUTES, digest_payload

STATE_VERSION = "kuuos_gauge_qi_process_graphrag_state_v0_2"
PERSISTENT_RECEIPT_VERSION = "kuuos_gauge_qi_process_graphrag_persistent_receipt_v0_2"
APPLY_RESULT_VERSION = "kuuos_gauge_qi_process_graphrag_apply_result_v0_2"
STORE_COMMIT_VERSION = "kuuos_gauge_qi_process_graphrag_store_commit_v0_2"
BELIEF_EVIDENCE_PACKET_VERSION = "kuuos_gauge_qi_process_graphrag_belief_evidence_packet_v0_2"
REPLAN_ADOPTION_VERSION = "kuuos_gauge_qi_process_graphrag_replan_adoption_v0_2"

REQUIRED_BOUNDARY = {
    "query_specific_evidence_lineage": True,
    "persistent_global_context_graph": False,
    "evidence_ledger_is_belief_authority": False,
    "direct_belief_commit": False,
    "direct_mission_activation": False,
    "belief_os_commit_required": True,
    "replan_required": True,
    "decision_commit_granted": False,
    "execution_authority_granted": False,
    "clinical_authority_granted": False,
    "theorem_authority_granted": False,
}

NON_AUTHORITY = {
    "persistent_evidence_is_truth": False,
    "evidence_chain_is_belief_authority": False,
    "holonomy_chain_is_veto_authority": False,
    "observation_debt_is_punishment": False,
    "belief_packet_is_belief_commit": False,
    "replan_adoption_is_decision_commit": False,
    "replan_adoption_is_execution_license": False,
}


def require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_must_be_nonempty_string")
    return value


def require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_must_be_nonnegative_int")
    return value


def require_finite_number(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_must_be_number")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name}_must_be_finite")
    return result


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def _digest_with_blank(value: Mapping[str, Any], field: str) -> str:
    payload = deepcopy(dict(value))
    payload[field] = ""
    return digest_payload(payload)


def state_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "graph_rag_state_digest")


def persistent_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "persistent_receipt_digest")


def apply_result_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "graph_rag_apply_result_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "graph_rag_store_commit_digest")


def belief_evidence_packet_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "belief_evidence_packet_digest")


def replan_adoption_digest(value: Mapping[str, Any]) -> str:
    return _digest_with_blank(value, "replan_adoption_receipt_digest")


def validate_fixed_boundary(value: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if dict(value.get("boundary", {})) != copy_boundary():
        errors.append("graph_rag_boundary_invalid")
    if dict(value.get("non_authority", {})) != copy_non_authority():
        errors.append("graph_rag_authority_escalation")
    return errors


def validate_route(value: Any, name: str = "route") -> str:
    route = require_nonempty_string(value, name)
    if route not in ROUTES:
        raise ValueError(f"{name}_invalid")
    return route
