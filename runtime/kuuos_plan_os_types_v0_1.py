from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import (
    canonical_json,
    require_finite_number,
    require_mapping,
    require_nonempty_string,
    require_nonnegative_int,
    require_unique_strings,
    sha,
)

VERSION = "kuuos_plan_os_replan_bound_synthesis_v0_1"
EVENT_VERSION = "kuuos_plan_os_event_v0_1"
STATE_VERSION = "kuuos_plan_os_state_v0_1"
STORE_COMMIT_VERSION = "kuuos_plan_os_store_commit_v0_1"
APPLY_RESULT_VERSION = "kuuos_plan_os_apply_result_v0_1"
ACTIVATION_RECEIPT_VERSION = "kuuos_plan_os_activation_receipt_v0_1"

PHASES = (
    "bind",
    "decompose",
    "order",
    "resource",
    "guard",
    "checkpoint",
    "verify",
    "commit",
)
PHASE_INDEX = {phase: index for index, phase in enumerate(PHASES)}

ROUTES = frozenset(
    {
        "PLAN_CANDIDATE",
        "OBSERVATION_PLAN",
        "REPAIR_PLAN",
        "HANDOVER_PLAN",
        "HOLD",
        "REJECT",
        "QUARANTINE",
    }
)

SOURCE_ROUTE_MAP = {
    "ENDORSE": "PLAN_CANDIDATE",
    "REOBSERVE": "OBSERVATION_PLAN",
    "REPAIR": "REPAIR_PLAN",
    "ESCALATE": "HANDOVER_PLAN",
    "HOLD": "HOLD",
    "REJECT": "REJECT",
    "QUARANTINE": "QUARANTINE",
}

STEP_CLASSES = frozenset(
    {"observe", "prepare", "act_candidate", "verify", "repair", "handover", "hold"}
)

ACTIVE_ROUTES = frozenset(
    {"PLAN_CANDIDATE", "OBSERVATION_PLAN", "REPAIR_PLAN", "HANDOVER_PLAN"}
)

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "execution_authority_granted": False,
    "proof_authority_granted": False,
    "clinical_authority_granted": False,
    "institutional_authority_granted": False,
    "legal_authority_granted": False,
    "host_license_granted": False,
    "memory_overwrite_authority_granted": False,
    "tool_authority_granted": False,
    "network_authority_granted": False,
    "shell_authority_granted": False,
}

REQUIRED_BOUNDARY = {
    "plan_is_structured_proposal": True,
    "plan_is_not_decision": True,
    "plan_is_not_execution": True,
    "plan_is_not_host_license": True,
    "source_wa_state_is_read_only": True,
    "source_option_identity_preserved": True,
    "stakeholder_veto_appeal_history_preserved": True,
    "dependency_dag_required": True,
    "resource_bounds_required": True,
    "rollback_or_escalation_required": True,
    "observation_checkpoint_required": True,
    "activation_requires_plan_phase": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = dict(value)
    result.pop(field, None)
    return result


def plan_event_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plan_event_digest"))


def plan_state_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plan_state_digest"))


def plan_store_commit_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plan_store_commit_digest"))


def plan_apply_result_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plan_apply_result_digest"))


def plan_activation_receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "plan_activation_receipt_digest"))


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def normalize_string_list(
    value: Sequence[Any], name: str, *, allow_empty: bool = True
) -> list[str]:
    return require_unique_strings(value, name, allow_empty=allow_empty)


def nonnegative_number(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0)


def unit_number(value: Any, name: str) -> float:
    return require_finite_number(value, name, minimum=0.0, maximum=1.0)


def next_phase(current: str) -> str | None:
    index = PHASE_INDEX.get(current)
    if index is None or index + 1 >= len(PHASES):
        return None
    return PHASES[index + 1]
