from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest, job_state_digest
from runtime.kuuos_durable_host_orchestrator_state_v0_18 import active_dead_letter_keys
from runtime.kuuos_durable_host_orchestrator_types_v0_18 import IDLE, READY
from runtime.kuuos_durable_host_orchestrator_v0_18 import (
    apply_dead_letter_release,
    build_dead_letter_release,
    build_orchestrator_plan,
    build_worker_report,
    run_orchestrator_cycle,
)
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import ticket_digest
from runtime.v018_orchestrator_fixtures import (
    fixture_state,
    host_license,
    orchestrator_policy,
    queued_jobs_bundle,
    registry,
    supervisor_policy,
)


def _worker_health_cases() -> None:
    runtime_policy = supervisor_policy()
    bundle = queued_jobs_bundle([("health-job", 1, "fixture.success")], policy=runtime_policy)
    state = fixture_state()
    license_packet = host_license()
    policy = orchestrator_policy(worker_heartbeat_ttl_ms=100, max_worker_failure_streak=3)
    reports = [
        build_worker_report(
            worker_id="healthy",
            observed_at_ms=2000,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success"],
        ),
        build_worker_report(
            worker_id="stale",
            observed_at_ms=1000,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success"],
        ),
        build_worker_report(
            worker_id="draining",
            observed_at_ms=2000,
            sequence=1,
            status="draining",
            operation_allowlist=["fixture.success"],
        ),
        build_worker_report(
            worker_id="degraded",
            observed_at_ms=2000,
            sequence=1,
            status="degraded",
            operation_allowlist=["fixture.success"],
        ),
        build_worker_report(
            worker_id="failed",
            observed_at_ms=2000,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success"],
            failure_streak=3,
        ),
    ]
    plan = build_orchestrator_plan(
        cycle_id="health-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=reports,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    assert plan["status"] == READY
    assert plan["healthy_worker_count"] == 1
    assert plan["ordered_worker_ids"] == ["healthy"]
    blockers = {item["worker_id"]: set(item["blockers"]) for item in plan["worker_health"]}
    assert "worker_report_stale" in blockers["stale"]
    assert "worker_status_draining" in blockers["draining"]
    assert "degraded_worker_not_allowed" in blockers["degraded"]
    assert "worker_failure_streak_exceeded" in blockers["failed"]

    no_healthy = build_orchestrator_plan(
        cycle_id="no-worker-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=state,
        worker_reports=reports[1:],
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    assert no_healthy["healthy_worker_count"] == 0
    assert no_healthy["dispatch_capacity"] == 0
    assert no_healthy["backpressure_class"] == "no_healthy_workers"


def _capability_gap_case() -> None:
    bundle = queued_jobs_bundle([("capability-job", 1, "fixture.success")])
    report = build_worker_report(
        worker_id="other-only",
        observed_at_ms=2000,
        sequence=1,
        status="healthy",
        operation_allowlist=["fixture.other"],
    )
    plan = build_orchestrator_plan(
        cycle_id="capability-cycle",
        supervisor_bundle=bundle,
        orchestrator_state=fixture_state(),
        worker_reports=[report],
        host_license=host_license(),
        policy=orchestrator_policy(),
        registry=registry(),
        now_ms=2000,
    )
    assert plan["healthy_worker_count"] == 1
    assert plan["eligible_job_count"] == 0
    assert plan["dispatch_capacity"] == 0
    assert plan["backpressure_class"] == "capability_gap_or_blocked"


def _damaged_checkpoint_bundle():
    bundle = queued_jobs_bundle([("dead-job", 1, "fixture.success")])
    damaged = deepcopy(bundle)
    job = damaged["jobs"][0]
    ticket = dict(job["active_continuation_ticket"])
    ticket["checkpoint_digest"] = "wrong-checkpoint"
    ticket["background_ticket_digest"] = ""
    ticket["background_ticket_digest"] = ticket_digest(ticket)
    job["active_continuation_ticket"] = ticket
    job["job_state_digest"] = ""
    job["job_state_digest"] = job_state_digest(job)
    damaged["supervisor_bundle_digest"] = ""
    damaged["supervisor_bundle_digest"] = bundle_digest(damaged)
    return damaged


def _dead_letter_case() -> None:
    bundle = _damaged_checkpoint_bundle()
    state0 = fixture_state()
    workers = [
        build_worker_report(
            worker_id="dead-worker",
            observed_at_ms=2000,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success"],
        )
    ]
    policy = orchestrator_policy(dead_letter_observation_threshold=2)
    runtime_policy = supervisor_policy()
    license_packet = host_license()

    plan1 = build_orchestrator_plan(
        cycle_id="dead-cycle-1",
        supervisor_bundle=bundle,
        orchestrator_state=state0,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2000,
    )
    assert plan1["eligible_job_count"] == 0
    cycle1 = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state0,
        plan=plan1,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=runtime_policy,
        registry=registry(),
        now_ms=2000,
    )
    assert cycle1["status"] == IDLE
    state1 = cycle1["result_orchestrator_state"]
    assert state1["dead_letters"] == []
    observation = next(iter(state1["candidate_observations"].values()))
    assert observation["observation_count"] == 1

    plan2 = build_orchestrator_plan(
        cycle_id="dead-cycle-2",
        supervisor_bundle=bundle,
        orchestrator_state=state1,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        registry=registry(),
        now_ms=2100,
    )
    cycle2 = run_orchestrator_cycle(
        supervisor_bundle=bundle,
        orchestrator_state=state1,
        plan=plan2,
        worker_reports=workers,
        host_license=license_packet,
        policy=policy,
        supervisor_policy=runtime_policy,
        registry=registry(),
        now_ms=2100,
    )
    state2 = cycle2["result_orchestrator_state"]
    assert len(state2["dead_letters"]) == 1
    assert len(cycle2["dead_letters_added"]) == 1
    dead_letter = state2["dead_letters"][0]
    assert dead_letter["observation_count"] == 2
    assert "background_ticket_checkpoint_mismatch" in dead_letter["reasons"]
    assert dead_letter["candidate_key"] in active_dead_letter_keys(state2)

    release = build_dead_letter_release(
        dead_letter=dead_letter,
        operator_command_digest="operator-release-command-digest",
        reason="checkpoint repaired outside this fixture",
        released_at_ms=2200,
    )
    state3, replayed = apply_dead_letter_release(state2, release)
    assert replayed is False
    assert active_dead_letter_keys(state3) == set()
    replay_state, replayed = apply_dead_letter_release(state3, release)
    assert replayed is True and replay_state == state3


def run_edge_cases() -> bool:
    _worker_health_cases()
    _capability_gap_case()
    _dead_letter_case()
    print("PASS: durable host orchestrator v0.18 edge cases")
    return True
