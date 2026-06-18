from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import (
    READY,
    REPLAYED,
    projection_digest,
    receipt_digest,
    tick_digest,
)
from runtime.kuuos_cooperative_host_adapter_v0_17 import (
    build_host_license,
    project_host_work,
    run_host_tick,
)
from runtime.v017_host_adapter_fixtures import queued_bundle, registry, steps, supervisor_policy


def main() -> bool:
    policy = supervisor_policy()
    executors = registry()
    bundle = queued_bundle(job_id="host-job", job_steps=steps(2), policy=policy)
    original = deepcopy(bundle)
    license_packet = build_host_license(
        license_id="host-license-main",
        issued_at_ms=1000,
        expires_at_ms=100000,
        operation_allowlist=["fixture.success"],
        max_steps_per_slice=1,
        max_cost_per_slice=1.0,
        lease_duration_ms=1000,
    )

    first_projection = project_host_work(
        supervisor_bundle=bundle,
        now_ms=2000,
        operation_allowlist=license_packet["operation_allowlist"],
    )
    assert bundle == original
    assert first_projection["adapter_state"] == "work_ready"
    assert first_projection["selected_job_id"] == "host-job"
    assert first_projection["selected_step_id"] == "step-1"
    assert first_projection["projection_digest"] == projection_digest(first_projection)

    first_tick = run_host_tick(
        supervisor_bundle=bundle,
        projection=first_projection,
        host_license=license_packet,
        worker_id="worker-main",
        invocation_id="invocation-1",
        now_ms=2000,
        supervisor_policy=policy,
        registry=executors,
    )
    assert first_tick["status"] == READY
    assert first_tick["adapter_state"] == "slice_committed"
    assert first_tick["host_tick_digest"] == tick_digest(first_tick)
    assert first_tick["receipt"]["host_receipt_digest"] == receipt_digest(first_tick["receipt"])
    assert first_tick["slice_packet"]["completed_step_ids_in_slice"] == ["step-1"]
    first_result = first_tick["result_supervisor_bundle"]
    assert first_result["supervisor_bundle_digest"] == bundle_digest(first_result)
    first_job = find_job(first_result, "host-job")
    assert first_job["supervisor_state"] == "background_queued"
    assert first_job["completed_step_ids"] == ["step-1"]
    assert first_job["active_continuation_ticket"]["queue_status"] == "queued"

    replay = run_host_tick(
        supervisor_bundle=first_result,
        projection=first_projection,
        host_license=license_packet,
        worker_id="worker-main",
        invocation_id="invocation-1",
        now_ms=2100,
        supervisor_policy=policy,
        registry=executors,
    )
    assert replay["status"] == REPLAYED
    assert replay["result_supervisor_bundle"] == first_result
    assert replay["slice_packet"] == {}

    second_projection = project_host_work(
        supervisor_bundle=first_result,
        now_ms=2200,
        operation_allowlist=license_packet["operation_allowlist"],
    )
    assert second_projection["selected_step_id"] == "step-2"
    second_tick = run_host_tick(
        supervisor_bundle=first_result,
        projection=second_projection,
        host_license=license_packet,
        worker_id="worker-main",
        invocation_id="invocation-2",
        now_ms=2200,
        supervisor_policy=policy,
        registry=executors,
    )
    assert second_tick["status"] == READY
    assert second_tick["adapter_state"] == "completed"
    completed_bundle = second_tick["result_supervisor_bundle"]
    completed_job = find_job(completed_bundle, "host-job")
    assert completed_job["supervisor_state"] == "completed"
    assert completed_job["completed_step_ids"] == ["step-1", "step-2"]
    assert len(completed_job["step_receipts"]) == 2
    assert len(completed_bundle["processed_host_invocation_digests"]) == 2
    assert completed_bundle["supervisor_bundle_digest"] == bundle_digest(completed_bundle)
    print("PASS: cooperative host adapter v0.17 main flow")
    return True


if __name__ == "__main__":
    main()
