from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_cooperative_host_adapter_v0_17 import build_host_license
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import BLOCKED, READY, plan_digest
from runtime.kuuos_durable_host_orchestrator_v0_18 import (
    build_orchestrator_plan,
    build_worker_report,
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


def _tampered_replay_case() -> None:
    bundle = queued_jobs_bundle([("replay-job", 1, "fixture.success")])
    state = fixture_state()
    workers = healthy_workers()[:1]
    policy = orchestrator_policy(max_assignments_per_cycle=1)
    license_packet = host_license()
    plan = build_orchestrator_plan(
        cycle_id="replay-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    completed = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state,
        plan=plan,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=supervisor_policy(),
        registry=registry(),
        now_ms=2000,
    )
    tampered = deepcopy(plan)
    tampered["cycle_id"] = "tampered-replay-cycle"
    replay = run_orchestrator_cycle(
        supervisor_bundle=completed["result_supervisor_bundle"],
        orchestrator_state=completed["result_orchestrator_state"],
        plan=tampered,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=supervisor_policy(),
        registry=registry(),
        now_ms=2100,
    )
    assert replay["status"] == BLOCKED
    assert "orchestrator_plan_digest_invalid" in replay["blockers"]
    assert replay["assignments"] == []


def _capacity_and_worker_distinctness_case() -> None:
    bundle = queued_jobs_bundle(
        [
            ("capacity-a", 1, "fixture.success"),
            ("capacity-b", 1, "fixture.success"),
        ]
    )
    state = fixture_state()
    workers = healthy_workers()[:1]
    policy = orchestrator_policy(max_assignments_per_cycle=1)
    license_packet = host_license()
    plan = build_orchestrator_plan(
        cycle_id="capacity-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    crafted = deepcopy(plan)
    crafted["dispatch_capacity"] = 99
    crafted["ordered_worker_ids"] = ["worker-a", "worker-a", "worker-a"]
    crafted["orchestrator_plan_digest"] = ""
    crafted["orchestrator_plan_digest"] = plan_digest(crafted)
    result = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state,
        plan=crafted,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=supervisor_policy(),
        registry=registry(),
        now_ms=2000,
    )
    assert result["status"] == READY
    assert result["effective_dispatch_capacity"] == 1
    assert len(result["assignments"]) == 1
    assert len({item["worker_id"] for item in result["assignments"]}) == 1


def _duplicate_worker_report_case() -> None:
    bundle = queued_jobs_bundle([("duplicate-worker-job", 1, "fixture.success")])
    state = fixture_state()
    policy = orchestrator_policy()
    license_packet = host_license()
    duplicate_reports = [
        build_worker_report(
            worker_id="same-worker",
            observed_at_ms=2000,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success"],
        ),
        build_worker_report(
            worker_id="same-worker",
            observed_at_ms=2000,
            sequence=2,
            status="healthy",
            operation_allowlist=["fixture.success"],
        ),
    ]
    plan = build_orchestrator_plan(
        cycle_id="duplicate-worker-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=duplicate_reports,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    assert plan["status"] == BLOCKED
    assert "duplicate_worker_id" in plan["blockers"]
    result = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state,
        plan=plan,
        worker_reports=duplicate_reports,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=supervisor_policy(),
        registry=registry(),
        now_ms=2000,
    )
    assert result["status"] == BLOCKED
    assert result["assignments"] == []


def _license_expiry_between_plan_and_cycle_case() -> None:
    bundle = queued_jobs_bundle([("expiry-job", 1, "fixture.success")])
    state = fixture_state()
    workers = healthy_workers()[:1]
    policy = orchestrator_policy(max_assignments_per_cycle=1)
    expiring_license = build_host_license(
        license_id="expiring-license",
        issued_at_ms=1000,
        expires_at_ms=2500,
        operation_allowlist=["fixture.success"],
        max_steps_per_slice=1,
        max_cost_per_slice=1.0,
        lease_duration_ms=1000,
    )
    plan = build_orchestrator_plan(
        cycle_id="expiry-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=workers,
        host_license=expiring_license,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    assert plan["status"] == READY
    result = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state,
        plan=plan,
        worker_reports=workers,
        host_license=expiring_license,
        policy=policy,
        supervisor_policy=supervisor_policy(),
        registry=registry(),
        now_ms=3000,
    )
    assert result["status"] == BLOCKED
    assert "host_license_expired" in result["blockers"]
    assert result["assignments"] == []


def run_hardening_cases() -> bool:
    _tampered_replay_case()
    _capacity_and_worker_distinctness_case()
    _duplicate_worker_report_case()
    _license_expiry_between_plan_and_cycle_case()
    print("PASS: durable host orchestrator v0.18 hardening cases")
    return True
