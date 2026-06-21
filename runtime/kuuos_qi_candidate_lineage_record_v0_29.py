from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_qi_candidate_lineage_types_v0_29 import (
    BOUND_REPORT_VERSION,
    copy_boundary,
    copy_non_authority,
    require_nonnegative_int,
    require_string,
)


def make_lineage_record(
    *,
    binding_id: str,
    state: Mapping[str, Any],
    packet: Mapping[str, Any],
    snapshot: Mapping[str, Any],
    route: str,
    reasons: list[str],
    bound_at_ms: int,
) -> dict[str, Any]:
    summary = snapshot["summary"]
    result = {
        "version": BOUND_REPORT_VERSION,
        "binding_id": require_string(binding_id, "binding_id"),
        "mission_id": state["mission_id"],
        "lineage_id": state["lineage_id"],
        "cycle_index": int(state["cycle_index"]),
        "source_mode": state["mode"],
        "source_v027_state_digest": snapshot["state_digest"],
        "source_v027_checkpoint_digest": state["latest_checkpoint_digest"],
        "source_v028_packet_id": packet["packet_id"],
        "source_v028_packet_digest": snapshot["packet_digest"],
        "source_v028_report_digest": snapshot["report_digest"],
        "candidate_set": deepcopy(summary["plural_hypotheses"]),
        "leading_candidate_id": summary.get("leading_hypothesis_id", ""),
        "leading_candidate_is_truth": False,
        "single_winner_forced": False,
        "counterevidence_preserved": True,
        "uncertainty_preserved": True,
        "potential_snapshot": deepcopy(snapshot["potential"]),
        "review_route": route,
        "route_reasons": list(reasons),
        "route_is_instruction": False,
        "route_activates_plan": False,
        "route_invokes_actos": False,
        "action_route_generated": False,
        "source_packet_substituted": False,
        "exact_checkpoint_binding": True,
        "multiple_reports_same_checkpoint_allowed": True,
        "memory_root_overwrite": False,
        "bound_at_ms": require_nonnegative_int(bound_at_ms, "bound_at_ms"),
        "non_authority": copy_non_authority(),
        "boundary": copy_boundary(),
        "qi_candidate_lineage_bound_report_digest": "",
    }
    return result


__all__ = ["make_lineage_record"]
