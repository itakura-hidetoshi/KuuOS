from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_qi_world_os_interface_bridge_v1_0"
RECEIPT_VERSION = "kuuos_qi_world_os_interface_receipt_v1_0"

OS_KINDS = (
    "BeliefOS",
    "DecisionOS",
    "PlanOS",
    "ActOS",
    "ObserveOS",
    "VerifyOS",
    "LearnOS",
    "Governance",
)

OS_INTERFACE_SPECS = {
    "BeliefOS": {
        "world_relation": "WEIGHTS_WORLD_PROJECTIONS",
        "qi_relation": "CONDITIONS_ON_PROCESS_HISTORY",
        "output_kind": "BELIEF_STATE",
    },
    "DecisionOS": {
        "world_relation": "COMPARES_POSSIBLE_WORLD_OUTCOMES",
        "qi_relation": "COMPARES_INTERVENTION_HISTORIES",
        "output_kind": "DECISION_CANDIDATE",
    },
    "PlanOS": {
        "world_relation": "COMPILES_PATH_THROUGH_WORLD_PROJECTIONS",
        "qi_relation": "ORDERS_HISTORY_DEPENDENT_INTERVENTIONS",
        "output_kind": "INTERVENTION_SCHEDULE",
    },
    "ActOS": {
        "world_relation": "APPLIES_AUTHORIZED_INTERVENTION",
        "qi_relation": "APPENDS_ACTUAL_PROCESS_OPERATION",
        "output_kind": "ACTION_RECEIPT",
    },
    "ObserveOS": {
        "world_relation": "SAMPLES_POST_INTERVENTION_PROJECTION",
        "qi_relation": "APPENDS_CONDITIONED_OBSERVATION",
        "output_kind": "OBSERVATION_EVIDENCE",
    },
    "VerifyOS": {
        "world_relation": "CHECKS_EVIDENCE_AGAINST_CRITERIA",
        "qi_relation": "COMPARES_EXPECTED_AND_OBSERVED_HISTORY",
        "output_kind": "VERIFICATION_RESULT",
    },
    "LearnOS": {
        "world_relation": "UPDATES_FUTURE_WORLD_MODEL_ONLY",
        "qi_relation": "UPDATES_FUTURE_PROCESS_MODEL_ONLY",
        "output_kind": "FUTURE_UPDATE",
    },
    "Governance": {
        "world_relation": "CONSTRAINS_WORLD_CLAIMS_AND_COMMITMENTS",
        "qi_relation": "CONSTRAINS_PERMITTED_PROCESS_OPERATIONS",
        "output_kind": "BOUNDARY_DECISION",
    },
}

CROSS_OS_RELATIONS = (
    ("WORLD", "PROJECTS_TO", "BeliefOS"),
    ("BeliefOS", "SUPPORTS", "DecisionOS"),
    ("DecisionOS", "SELECTS_FOR", "PlanOS"),
    ("PlanOS", "REQUESTS", "Governance"),
    ("Governance", "ADMITS_OR_BLOCKS", "ActOS"),
    ("ActOS", "INTERVENES_THROUGH", "QI_PROCESS_TENSOR"),
    ("QI_PROCESS_TENSOR", "CONDITIONS", "WORLD"),
    ("WORLD", "PROJECTS_TO", "ObserveOS"),
    ("ObserveOS", "SUPPLIES_EVIDENCE_TO", "VerifyOS"),
    ("VerifyOS", "SUPPLIES_RESULT_TO", "LearnOS"),
    ("LearnOS", "UPDATES_FUTURE_MODEL_OF", "WORLD"),
    ("LearnOS", "UPDATES_FUTURE_MODEL_OF", "QI_PROCESS_TENSOR"),
    ("Governance", "ENVELOPES", "BeliefOS"),
    ("Governance", "ENVELOPES", "DecisionOS"),
    ("Governance", "ENVELOPES", "PlanOS"),
    ("Governance", "ENVELOPES", "ObserveOS"),
    ("Governance", "ENVELOPES", "VerifyOS"),
    ("Governance", "ENVELOPES", "LearnOS"),
)

WORLD_BOUNDARY = {
    "projection_read_only": True,
    "candidate_only": True,
    "nonfinal_marker": True,
    "exact_world_identified": False,
    "runtime_updates_world": False,
    "multi_world_noncollapse": True,
    "two_truths_gap": True,
}

NON_AUTHORITY = {
    "belief_grants_truth": False,
    "decision_grants_action": False,
    "plan_grants_execution": False,
    "qi_process_grants_execution": False,
    "observation_grants_verification": False,
    "verification_grants_truth": False,
    "learning_overwrites_past": False,
    "governance_generates_substantive_action": False,
    "bridge_updates_exact_world": False,
}


def copy_world_boundary() -> dict[str, bool]:
    return deepcopy(WORLD_BOUNDARY)


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY)


def digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def interface_receipt_digest(value: Mapping[str, Any]) -> str:
    return digest_without(value, "qi_world_os_interface_receipt_digest")


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str, *, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name}_int_minimum_{minimum}_required")
    return value
