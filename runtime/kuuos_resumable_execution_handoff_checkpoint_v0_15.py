from __future__ import annotations

from typing import Any, Mapping

from runtime.kuuos_resumable_execution_handoff_model_v0_15 import (
    bounded_progress,
    integer,
)
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    CHECKPOINT_VERSION,
    checkpoint_digest,
)


def build_checkpoint(observation: Mapping[str, Any]) -> dict[str, Any]:
    completed_units = max(0, integer(observation.get("completed_work_units"), 0))
    total_units = max(0, integer(observation.get("total_work_units"), 0))
    packet = {
        "version": CHECKPOINT_VERSION,
        "job_id": str(observation.get("job_id", "")),
        "attempt_id": str(observation.get("attempt_id", "")),
        "source_parent_digest": str(observation.get("source_parent_digest", "")),
        "phase": str(observation.get("phase", "")),
        "completed_work_units": completed_units,
        "total_work_units": total_units,
        "progress_fraction": bounded_progress(completed_units, total_units),
        "last_successful_operation": str(
            observation.get("last_successful_operation", "")
        ),
        "checkpoint_payload": dict(
            observation.get("checkpoint_payload", {})
            if isinstance(observation.get("checkpoint_payload", {}), Mapping)
            else {}
        ),
        "checkpoint_digest": "",
    }
    packet["checkpoint_digest"] = checkpoint_digest(packet)
    return packet
