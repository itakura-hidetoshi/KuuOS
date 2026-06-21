from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_qi_candidate_lineage_kernel_v0_29"
BOUND_REPORT_VERSION = "kuuos_qi_candidate_lineage_bound_report_v0_29"
LEDGER_VERSION = "kuuos_qi_candidate_lineage_ledger_v0_29"

REVIEW_ROUTES = frozenset({"HOLD", "REOBSERVE", "REVIEW", "TERMINATE", "HANDOVER"})

NON_AUTHORITY_FLAGS = {
    "extends_source_authority": False,
    "creates_truth_status": False,
    "creates_plan_activation": False,
    "creates_effect_permission": False,
    "creates_host_access": False,
    "creates_memory_overwrite": False,
    "creates_successor_cycle_authority": False,
}

REQUIRED_BOUNDARY = {
    "v028_report_exactly_bound_to_v027_state": True,
    "v027_mission_and_lineage_preserved": True,
    "v027_checkpoint_preserved": True,
    "v028_packet_and_report_digests_preserved": True,
    "source_packet_substitution_forbidden": True,
    "multiple_distinct_reports_per_checkpoint_allowed": True,
    "plural_candidates_preserved": True,
    "counterevidence_and_uncertainty_preserved": True,
    "review_route_is_nonexecuting": True,
    "review_route_does_not_activate_plan": True,
    "review_route_does_not_invoke_actos": True,
    "terminate_and_handover_follow_source_state": True,
    "ledger_is_append_only": True,
    "duplicate_bound_report_is_idempotent": True,
    "memory_root_overwrite_forbidden": True,
}


def without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def bound_report_digest(value: Mapping[str, Any]) -> str:
    return sha(without(value, "qi_candidate_lineage_bound_report_digest"))


def require_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name}_required")
    return value


def require_nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name}_nonnegative_int_required")
    return value


def copy_non_authority() -> dict[str, bool]:
    return deepcopy(NON_AUTHORITY_FLAGS)


def copy_boundary() -> dict[str, bool]:
    return deepcopy(REQUIRED_BOUNDARY)


__all__ = [
    "BOUND_REPORT_VERSION",
    "LEDGER_VERSION",
    "NON_AUTHORITY_FLAGS",
    "REQUIRED_BOUNDARY",
    "REVIEW_ROUTES",
    "VERSION",
    "bound_report_digest",
    "copy_boundary",
    "copy_non_authority",
    "require_nonnegative_int",
    "require_string",
    "without",
]
