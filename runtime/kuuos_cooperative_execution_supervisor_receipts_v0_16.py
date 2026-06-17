from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import sha
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import STEP_RECEIPT_VERSION, step_receipt_digest


def build_step_receipt(*, job: Mapping[str, Any], step: Mapping[str, Any], attempt: int, execution_key: str, result: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": STEP_RECEIPT_VERSION,
        "job_id": str(job.get("job_id", "")),
        "manifest_digest": str(job.get("manifest_digest", "")),
        "step_id": str(step.get("step_id", "")),
        "operation_id": str(step.get("operation_id", "")),
        "operation_input_digest": str(step.get("operation_input_digest", "")),
        "attempt": int(attempt),
        "execution_key": str(execution_key),
        "outcome": str(result.get("outcome", "")),
        "summary": str(result.get("summary", "")),
        "cost_units": max(0.0, float(result.get("cost_units", 0.0) or 0.0)),
        "output_digest": sha(result.get("output", {})),
        "checkpoint_payload_digest": sha(result.get("checkpoint_payload", {})),
        "step_receipt_digest": "",
    }
    packet["step_receipt_digest"] = step_receipt_digest(packet)
    return packet
