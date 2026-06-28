#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from typing import Any

from runtime.kuuos_gauge_field_self_organization_types_v0_60 import canonical_digest
from runtime.kuuos_self_organization_cycle_v0_78 import run_self_organization_cycle
from runtime.kuuos_self_organization_types_v0_78 import (
    NO_CHANGE,
    ROLLED_BACK,
    ObservationContext,
    SelfOrganizationCycleReceipt,
    SelfOrganizationPolicy,
    StructureState,
)

STOP_NO_CHANGE = "STOP_NO_CHANGE"
STOP_REOBSERVATION_ROLLBACK = "STOP_REOBSERVATION_ROLLBACK"
STOP_MAX_CYCLES = "STOP_MAX_CYCLES"


@dataclass(frozen=True)
class BoundedSelfOrganizationReceipt:
    supervisor_id: str
    initial_state_digest: str
    final_state_digest: str
    initial_revision: int
    final_revision: int
    cycle_receipt_digests: tuple[str, ...]
    cycle_count: int
    max_cycles: int
    stop_reason: str
    external_approval_required: bool
    unbounded_execution_allowed: bool
    host_state_write_performed: bool
    receipt_digest: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["cycle_receipt_digests"] = list(self.cycle_receipt_digests)
        return payload


def bounded_supervisor_receipt_digest(
    receipt: BoundedSelfOrganizationReceipt,
) -> str:
    payload = receipt.to_dict()
    payload.pop("receipt_digest", None)
    return canonical_digest(payload)


def run_bounded_self_organization(
    supervisor_id: str,
    initial_state: StructureState,
    observation_context: ObservationContext,
    shadow_contexts: tuple[ObservationContext, ...],
    reobservation_context: ObservationContext,
    policy: SelfOrganizationPolicy,
    max_cycles: int,
) -> tuple[
    StructureState,
    tuple[SelfOrganizationCycleReceipt, ...],
    BoundedSelfOrganizationReceipt,
]:
    if not supervisor_id:
        raise ValueError("supervisor_id_missing")
    if max_cycles <= 0:
        raise ValueError("max_cycles_invalid")

    state = initial_state
    receipts: list[SelfOrganizationCycleReceipt] = []
    stop_reason = STOP_MAX_CYCLES

    for cycle_index in range(max_cycles):
        state, cycle_receipt = run_self_organization_cycle(
            f"{supervisor_id}/cycle-{cycle_index:04d}",
            state,
            observation_context,
            shadow_contexts,
            reobservation_context,
            policy,
        )
        receipts.append(cycle_receipt)
        if cycle_receipt.status == NO_CHANGE:
            stop_reason = STOP_NO_CHANGE
            break
        if cycle_receipt.status == ROLLED_BACK:
            stop_reason = STOP_REOBSERVATION_ROLLBACK
            break

    receipt = BoundedSelfOrganizationReceipt(
        supervisor_id,
        initial_state.digest,
        state.digest,
        initial_state.revision,
        state.revision,
        tuple(item.receipt_digest for item in receipts),
        len(receipts),
        max_cycles,
        stop_reason,
        False,
        False,
        False,
        "",
    )
    return state, tuple(receipts), replace(
        receipt,
        receipt_digest=bounded_supervisor_receipt_digest(receipt),
    )
