from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_plan_os_closed_loop_replan_intake_adapter_v0_4"
INTAKE_RECEIPT_VERSION = "kuuos_plan_os_closed_loop_replan_intake_receipt_v0_4"
BIND_RECEIPT_VERSION = "kuuos_plan_os_closed_loop_replan_bind_receipt_v0_4"
STORE_STATE_VERSION = "kuuos_plan_os_closed_loop_intake_store_state_v0_4"
STORE_COMMIT_VERSION = "kuuos_plan_os_closed_loop_intake_store_commit_v0_4"

STAGE_INTAKE = "INTAKE_COMMITTED"
STAGE_BIND = "REPLAN_BOUND"
STAGES = frozenset({STAGE_INTAKE, STAGE_BIND})

NON_AUTHORITY_FLAGS = {
    "truth_authority_granted": False,
    "causal_authority_granted": False,
    "execution_authority_granted": False,
    "final_commitment_authority_granted": False,
    "memory_overwrite_authority_granted": False,
    "self_modification_authority_granted": False,
    "clinical_authority_granted": False,
    "legal_authority_granted": False,
    "institutional_authority_granted": False,
    "theorem_authority_granted": False,
    "replan_activation_granted": False,
    "plan_activation_granted": False,
    "host_license_granted": False,
}

REQUIRED_BOUNDARY = {
    "committed_current_plan_required": True,
    "canonical_compiler_receipt_required": True,
    "committed_learn_state_required": True,
    "canonical_learn_lineage_required": True,
    "current_plan_identity_preserved": True,
    "learning_delta_identity_preserved": True,
    "verification_lineage_preserved": True,
    "qi_lineage_preserved": True,
    "decision_lineage_preserved": True,
    "exact_cycle_required": True,
    "future_only_required": True,
    "single_use_intake": True,
    "planos_v02_bind_only": True,
    "history_phase_required_after_bind": True,
    "current_cycle_mutation_forbidden": True,
    "past_plan_mutation_forbidden": True,
    "memory_overwrite_forbidden": True,
    "execution_owned_by_act_os": True,
    "selection_owned_by_decision_os": True,
    "replan_owned_by_plan_os": True,
    "append_only_history_required": True,
}


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = dict(value)
    packet.pop(field, None)
    return sha(packet)


def intake_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "closed_loop_intake_receipt_digest")


def bind_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "closed_loop_bind_receipt_digest")


def store_state_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "closed_loop_intake_store_state_digest")


def store_commit_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "closed_loop_intake_store_commit_digest")


def intake_single_use_key(value: Mapping[str, Any]) -> str:
    return sha(
        {
            "learn_completion": value.get(
                "learn_lineage_completion_receipt_digest"
            ),
            "current_plan": value.get("current_plan_state_digest"),
            "cycle": value.get("current_cycle_index"),
        }
    )


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def finite_number(
    value: Any,
    name: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name}_number_required")
    result = float(value)
    if result != result or result in (float("inf"), float("-inf")):
        raise ValueError(f"{name}_finite_required")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name}_below_minimum")
    if maximum is not None and result > maximum:
        raise ValueError(f"{name}_above_maximum")
    return result


def unit_number(value: Any, name: str) -> float:
    return finite_number(value, name, minimum=0.0, maximum=1.0)


def nonnegative_number(value: Any, name: str) -> float:
    return finite_number(value, name, minimum=0.0)
