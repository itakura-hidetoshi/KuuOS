from __future__ import annotations

from dataclasses import asdict, dataclass
from math import exp, isfinite
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha

VERSION = "kuuos_planos_zero_temperature_minimal_action_limit_kernel_v0_1"
STATUS_READY = "PLANOS_ZERO_TEMPERATURE_MINIMAL_ACTION_LIMIT_KERNEL_READY"

BOUNDARY = {
    "source_kl_update_preserved": True,
    "admissible_support_preserved": True,
    "minimal_action_support_identified": True,
    "authority_invariance_preserved": True,
    "history_read_only": True,
    "future_only": True,
    "active_now": False,
    "execution_permission": False,
}

@dataclass(frozen=True)
class ZeroTemperatureMinimalActionLimitKernel:
    version: str
    status: str
    source_update_digest: str
    candidate_actions: dict[str, float]
    minimal_action: float | None
    minimal_action_candidate_ids: list[str]
    positive_temperature_distribution: dict[str, float]
    zero_temperature_limit_distribution: dict[str, float]
    selected_candidate_id: str
    blockers: list[str]
    boundary: dict[str, bool]
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_zero_temperature_minimal_action_limit(
    source_update: Mapping[str, Any],
    *,
    candidate_actions: Mapping[str, float],
    temperature: float = 0.05,
    selected_candidate_id: str | None = None,
) -> ZeroTemperatureMinimalActionLimitKernel:
    blockers: list[str] = []
    if not source_update or not source_update.get("receipt_digest"):
        blockers.append("source_update_missing")
    source_boundary = source_update.get("boundary") if isinstance(source_update.get("boundary"), Mapping) else {}
    if source_boundary.get("future_only") is not True:
        blockers.append("source_future_only_missing")
    if source_boundary.get("execution_permission") is not False:
        blockers.append("source_execution_boundary_invalid")
    if not isfinite(float(temperature)) or float(temperature) <= 0.0:
        blockers.append("temperature_not_positive")

    actions: dict[str, float] = {}
    for cid, raw in candidate_actions.items():
        value = float(raw)
        if not cid or not isfinite(value) or value < 0.0:
            blockers.append("candidate_action_invalid")
            continue
        actions[str(cid)] = value
    if not actions:
        blockers.append("candidate_actions_empty")

    minimal_action: float | None = min(actions.values()) if actions else None
    minimizers = sorted([cid for cid, value in actions.items() if value == minimal_action]) if minimal_action is not None else []
    if not minimizers:
        blockers.append("minimal_action_support_empty")

    selected = selected_candidate_id or (minimizers[0] if minimizers else "")
    if selected and selected not in minimizers:
        blockers.append("selected_candidate_not_minimal_action")

    positive: dict[str, float] = {}
    limit: dict[str, float] = {}
    if not blockers:
        shifted = {cid: exp(-(value - minimal_action) / float(temperature)) for cid, value in actions.items()}
        z = sum(shifted.values())
        if not isfinite(z) or z <= 0.0:
            blockers.append("partition_function_invalid")
        else:
            positive = {cid: weight / z for cid, weight in shifted.items()}
            share = 1.0 / len(minimizers)
            limit = {cid: (share if cid in minimizers else 0.0) for cid in actions}

    outer = {
        "version": VERSION,
        "status": STATUS_READY if not blockers else "PLANOS_ZERO_TEMPERATURE_MINIMAL_ACTION_LIMIT_KERNEL_BLOCKED",
        "source_update_digest": str(source_update.get("receipt_digest", "")),
        "candidate_actions": actions,
        "minimal_action": minimal_action,
        "minimal_action_candidate_ids": minimizers,
        "positive_temperature_distribution": positive,
        "zero_temperature_limit_distribution": limit,
        "selected_candidate_id": selected,
        "blockers": blockers,
        "boundary": dict(BOUNDARY),
    }
    return ZeroTemperatureMinimalActionLimitKernel(**outer, receipt_digest=sha(outer))
