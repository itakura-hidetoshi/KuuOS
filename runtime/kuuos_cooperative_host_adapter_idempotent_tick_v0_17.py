from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_context_gauge_atlas_types_v0_13 import as_list
from runtime.kuuos_cooperative_execution_supervisor_registry_v0_16 import Executor
from runtime.kuuos_cooperative_host_adapter_tick_v0_17 import run_host_tick as _run_host_tick
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    NON_AUTHORITY_FLAGS,
    RECEIPT_VERSION,
    REPLAYED,
    REQUIRED_BOUNDARY,
    TICK_VERSION,
    invocation_digest,
    receipt_digest,
    tick_digest,
)


def run_host_tick(
    *,
    supervisor_bundle: Mapping[str, Any],
    projection: Mapping[str, Any],
    host_license: Mapping[str, Any],
    worker_id: str,
    invocation_id: str,
    now_ms: int,
    supervisor_policy: Mapping[str, Any],
    registry: Mapping[str, Executor],
) -> dict[str, Any]:
    projection_source = str(projection.get("source_supervisor_bundle_digest", ""))
    projection_key = str(projection.get("projection_digest", ""))
    invocation = invocation_digest(
        invocation_id=str(invocation_id),
        source_bundle_digest=projection_source,
        projection=projection_key,
        worker_id=str(worker_id),
    )
    processed = {str(item) for item in as_list(supervisor_bundle.get("processed_host_invocation_digests"))}
    if invocation not in processed:
        return _run_host_tick(
            supervisor_bundle=supervisor_bundle,
            projection=projection,
            host_license=host_license,
            worker_id=worker_id,
            invocation_id=invocation_id,
            now_ms=now_ms,
            supervisor_policy=supervisor_policy,
            registry=registry,
        )

    current_digest = str(supervisor_bundle.get("supervisor_bundle_digest", ""))
    receipt = {
        "version": RECEIPT_VERSION,
        "status": REPLAYED,
        "invocation_digest": invocation,
        "worker_id": str(worker_id),
        "projection_digest": projection_key,
        "job_id": str(projection.get("selected_job_id", "")),
        "source_supervisor_bundle_digest": projection_source,
        "result_supervisor_bundle_digest": current_digest,
        "slice_digest": "",
        "supervisor_state": "",
        "completed_step_ids_in_slice": [],
        "replayed": True,
        "blockers": [],
        "one_job_claimed_at_most": True,
        "one_bounded_slice_run_at_most": True,
        **NON_AUTHORITY_FLAGS,
        "host_receipt_digest": "",
    }
    receipt["host_receipt_digest"] = receipt_digest(receipt)
    packet = {
        "version": TICK_VERSION,
        "status": REPLAYED,
        "adapter_state": "replayed",
        "invocation_digest": invocation,
        "effective_policy": {},
        "result_supervisor_bundle": deepcopy(dict(supervisor_bundle)),
        "slice_packet": {},
        "receipt": receipt,
        "blockers": [],
        "boundary": dict(REQUIRED_BOUNDARY),
        **NON_AUTHORITY_FLAGS,
        "host_tick_digest": "",
    }
    packet["host_tick_digest"] = tick_digest(packet)
    return packet
