from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_cooperative_execution_supervisor_handoff_v0_16 import build_pause_handoff
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import reseal_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import SLICE_VERSION, slice_digest


def finish_slice(*, slice_id: str, source_digest: str, mode: str, job: Mapping[str, Any], completed_in_slice: list[str], new_receipts: list[dict[str, Any]], spent_cost: float, handoff: Mapping[str, Any] | None = None, yield_receipt: Mapping[str, Any] | None = None) -> dict[str, Any]:
    raw_ticket = (handoff or {}).get("background_ticket", {})
    ticket = dict(raw_ticket) if isinstance(raw_ticket, Mapping) else {}
    packet = {
        "version": SLICE_VERSION,
        "slice_id": str(slice_id),
        "job_id": str(job.get("job_id", "")),
        "source_job_state_digest": str(source_digest),
        "result_job_state_digest": str(job.get("job_state_digest", "")),
        "manifest_digest": str(job.get("manifest_digest", "")),
        "execution_mode": str(mode),
        "completed_step_ids_in_slice": [str(item) for item in completed_in_slice],
        "new_step_receipts": [dict(item) for item in new_receipts],
        "spent_cost_units": round(max(0.0, float(spent_cost)), 6),
        "supervisor_state": str(job.get("supervisor_state", "")),
        "handoff": dict(handoff or {}),
        "yield_receipt": dict(yield_receipt or {}),
        "background_ticket": ticket,
        "result_job": deepcopy(dict(job)),
        "lower_authority_preserved": True,
        "slice_digest": "",
    }
    packet["slice_digest"] = slice_digest(packet)
    return packet


def apply_handoff(job: Mapping[str, Any], handoff: Mapping[str, Any]) -> dict[str, Any]:
    packet = deepcopy(dict(job))
    packet["supervisor_state"] = str(handoff.get("execution_state", "blocked_bug"))
    packet["latest_checkpoint_digest"] = str(handoff.get("checkpoint_digest", ""))
    packet["latest_feedback_digest"] = str(handoff.get("feedback_digest", ""))
    raw_ticket = handoff.get("background_ticket", {})
    packet["active_continuation_ticket"] = dict(raw_ticket) if isinstance(raw_ticket, Mapping) else {}
    return reseal_job(packet)


def pause_slice(*, work: Mapping[str, Any], slice_id: str, source_digest: str, mode: str, policy: Mapping[str, Any], step: Mapping[str, Any] | None, result: Mapping[str, Any] | None, completed_in_slice: list[str], new_receipts: list[dict[str, Any]], spent_cost: float, phase: str) -> dict[str, Any]:
    sealed = reseal_job(work)
    handoff = build_pause_handoff(
        job=sealed,
        attempt_id=f"{slice_id}:{phase}",
        phase=phase,
        next_step=step,
        policy=policy,
        mode=mode,
        result=result,
    )
    final_job = apply_handoff(sealed, handoff)
    return finish_slice(
        slice_id=slice_id,
        source_digest=source_digest,
        mode=mode,
        job=final_job,
        completed_in_slice=completed_in_slice,
        new_receipts=new_receipts,
        spent_cost=spent_cost,
        handoff=handoff,
    )
