from __future__ import annotations

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import (
    READY,
    REPLAYED,
    cycle_digest,
    orchestrator_state_digest,
    plan_digest,
    receipt_digest,
)
from runtime.kuuos_durable_host_orchestrator_v0_18 import (
    build_orchestrator_plan,
    run_orchestrator_cycle,
)
from runtime.v018_orchestrator_fixtures import (
    fixture_state,
    healthy_workers,
    host_license,
    orchestrator_policy,
    queued_jobs_bundle,
    registry,
    supervisor_policy,
)


def main() -> bool:
    runtime_policy = supervisor_policy()
    orchestration_policy = orchestrator_policy()
    license_packet = host_license()
    workers = healthy_workers()
    executors = registry()
    bundle = queued_jobs_bundle(
        [
            ("job-a", 2, "fixture.success"),
            ("job-b", 2, "fixture.success"),
            ("job-c", 2, "fixture.success"),
        ],
        policy=runtime_policy,
    )
    state = fixture_state()

    plan1 = build_orchestrator_plan(
        cycle_id="cycle-1",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=workers,
        host_license=license_packet,
        policy=orchestration_policy,
        registry=executors,
        now_ms=2000,
    )
    assert plan1["status"] == READY
    assert plan1["orchestrator_plan_digest"] == plan_digest(plan1)
    assert plan1["eligible_job_count"] == 3
    assert plan1["healthy_worker_count"] == 2
    assert plan1["dispatch_capacity"] == 2
    assert plan1["deferred_eligible_count"] == 1
    assert plan1["backpressure_class"] == "saturated"

    cycle1 = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state,
        plan=plan1,
        worker_reports=workers,
        host_license=license_packet,
        policy=orchestration_policy,
        supervisor_policy=runtime_policy,
        registry=executors,
        now_ms=2000,
    )
    assert cycle1["status"] == READY
    assert cycle1["orchestrator_cycle_digest"] == cycle_digest(cycle1)
    assert cycle1["receipt"]["orchestrator_receipt_digest"] == receipt_digest(cycle1["receipt"])
    assert [item["job_id"] for item in cycle1["assignments"]] == ["job-a", "job-b"]
    assert len({item["job_id"] for item in cycle1["assignments"]}) == 2
    assert len({item["worker_id"] for item in cycle1["assignments"]}) == 2

    bundle1 = cycle1["result_supervisor_bundle"]
    state1 = cycle1["result_orchestrator_state"]
    assert bundle1["supervisor_bundle_digest"] == bundle_digest(bundle1)
    assert state1["orchestrator_state_digest"] == orchestrator_state_digest(state1)
    assert state1["job_service_counts"] == {"job-a": 1, "job-b": 1}
    assert state1["worker_service_counts"] == {"worker-a": 1, "worker-b": 1}
    assert find_job(bundle1, "job-a")["completed_step_ids"] == ["job-a-step-1"]
    assert find_job(bundle1, "job-b")["completed_step_ids"] == ["job-b-step-1"]
    assert find_job(bundle1, "job-c")["completed_step_ids"] == []

    replay = run_orchestrator_cycle(
        supervisor_bundle=bundle1,
        orchestrator_state=state1,
        plan=plan1,
        worker_reports=workers,
        host_license=license_packet,
        policy=orchestration_policy,
        supervisor_policy=runtime_policy,
        registry=executors,
        now_ms=2050,
    )
    assert replay["status"] == REPLAYED
    assert replay["assignments"] == []
    assert replay["result_supervisor_bundle"] == bundle1
    assert replay["result_orchestrator_state"] == state1

    plan2 = build_orchestrator_plan(
        cycle_id="cycle-2",
        supervisor_bundle=bundle1,
        orchestrator_state=state1,
        worker_reports=workers,
        host_license=license_packet,
        policy=orchestration_policy,
        registry=executors,
        now_ms=2100,
    )
    cycle2 = run_orchestrator_cycle(
        supervisor_bundle=bundle1,
        orchestrator_state=state1,
        plan=plan2,
        worker_reports=workers,
        host_license=license_packet,
        policy=orchestration_policy,
        supervisor_policy=runtime_policy,
        registry=executors,
        now_ms=2100,
    )
    assert cycle2["status"] == READY
    assert [item["job_id"] for item in cycle2["assignments"]] == ["job-c", "job-a"]
    bundle2 = cycle2["result_supervisor_bundle"]
    state2 = cycle2["result_orchestrator_state"]
    assert find_job(bundle2, "job-a")["supervisor_state"] == "completed"
    assert find_job(bundle2, "job-b")["completed_step_ids"] == ["job-b-step-1"]
    assert find_job(bundle2, "job-c")["completed_step_ids"] == ["job-c-step-1"]
    assert state2["job_service_counts"] == {"job-a": 2, "job-b": 1, "job-c": 1}
    assert state2["worker_service_counts"] == {"worker-a": 2, "worker-b": 2}
    assert state2["cycle_index"] == 2
    assert len(state2["processed_plan_digests"]) == 2
    print("PASS: durable host orchestrator v0.18 fairness and replay")
    return True


if __name__ == "__main__":
    main()
