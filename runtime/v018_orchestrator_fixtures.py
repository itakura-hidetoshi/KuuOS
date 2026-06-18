from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_cooperative_execution_supervisor_v0_16 import (
    build_supervisor_command,
    create_supervised_job,
    empty_supervisor_bundle,
    find_job,
    register_job,
    store_command,
)
from runtime.kuuos_cooperative_host_adapter_v0_17 import build_host_license
from runtime.kuuos_durable_host_orchestrator_v0_18 import (
    build_orchestrator_policy,
    build_worker_report,
    empty_orchestrator_state,
)


def supervisor_policy(**updates: Any) -> dict[str, Any]:
    packet = {
        "max_steps_per_slice": 1,
        "max_cost_per_slice": 1.0,
        "background_worker_available": True,
        "background_handoff_enabled": True,
        "auto_background_on_budget_pause": False,
        "auto_background_on_external_wait": False,
        "auto_background_on_transient_error": False,
        "cost_reserve_units": 0.0,
        "foreground_wait_threshold_ms": 100,
        "external_recheck_after_ms": 10,
        "retry_backoff_base_ms": 1000,
        "max_retry_backoff_ms": 60000,
        "max_retries": 3,
    }
    packet.update(updates)
    return packet


def success_executor(operation_input: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "outcome": "success",
        "summary": "orchestrator fixture step completed",
        "output": {
            "value": operation_input.get("value"),
            "job_id": context.get("job_id"),
            "step_id": context.get("step_id"),
        },
        "cost_units": 1.0,
        "checkpoint_payload": {"execution_key": context.get("execution_key")},
    }


def other_executor(operation_input: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "outcome": "success",
        "summary": "other fixture operation completed",
        "output": {"value": operation_input.get("value")},
        "cost_units": 1.0,
        "checkpoint_payload": {},
    }


def registry() -> dict[str, Any]:
    return {
        "fixture.success": success_executor,
        "fixture.other": other_executor,
    }


def job_steps(job_id: str, count: int = 2, operation_id: str = "fixture.success") -> list[dict[str, Any]]:
    return [
        {
            "step_id": f"{job_id}-step-{index + 1}",
            "operation_id": operation_id,
            "operation_input": {"value": index + 1},
            "estimated_cost_units": 1.0,
            "max_attempts": 2,
        }
        for index in range(max(1, int(count)))
    ]


def queued_jobs_bundle(
    job_specs: Sequence[tuple[str, int, str]],
    *,
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    runtime_policy = supervisor_policy() if policy is None else dict(policy)
    bundle = empty_supervisor_bundle("orchestrator-fixture-agent")
    for job_id, count, operation_id in job_specs:
        job = create_supervised_job(
            job_id=job_id,
            source_parent_digest="orchestrator-parent-v017",
            steps=job_steps(job_id, count, operation_id),
            initial_budget_units=20.0,
        )
        bundle = register_job(bundle, job)
        current = find_job(bundle, job_id)
        command = build_supervisor_command(
            job_id=job_id,
            command_id=f"queue-{job_id}",
            action="queue_background",
            payload={},
            source_job_state_digest=current["job_state_digest"],
        )
        bundle, replayed = store_command(bundle, command, runtime_policy)
        if replayed:
            raise ValueError("fixture_queue_command_replayed")
    return bundle


def host_license(now_ms: int = 1000) -> dict[str, Any]:
    return build_host_license(
        license_id="orchestrator-host-license",
        issued_at_ms=now_ms,
        expires_at_ms=now_ms + 1_000_000,
        operation_allowlist=["fixture.success", "fixture.other"],
        max_steps_per_slice=1,
        max_cost_per_slice=1.0,
        lease_duration_ms=1000,
    )


def orchestrator_policy(**updates: Any) -> dict[str, Any]:
    args = {
        "policy_id": "orchestrator-policy",
        "max_assignments_per_cycle": 2,
        "worker_heartbeat_ttl_ms": 1000,
        "max_worker_failure_streak": 3,
        "allow_degraded_workers": False,
        "queue_high_watermark": 2,
        "dead_letter_observation_threshold": 2,
        "max_history": 128,
    }
    args.update(updates)
    return build_orchestrator_policy(**args)


def healthy_workers(now_ms: int = 2000) -> list[dict[str, Any]]:
    return [
        build_worker_report(
            worker_id="worker-a",
            observed_at_ms=now_ms,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success", "fixture.other"],
            capacity_slots=1,
        ),
        build_worker_report(
            worker_id="worker-b",
            observed_at_ms=now_ms,
            sequence=1,
            status="healthy",
            operation_allowlist=["fixture.success", "fixture.other"],
            capacity_slots=1,
        ),
    ]


def fixture_state() -> dict[str, Any]:
    return empty_orchestrator_state("orchestrator-fixture")
