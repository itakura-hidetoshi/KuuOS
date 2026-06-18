from __future__ import annotations

from typing import Any, Mapping, Sequence

from runtime.kuuos_cooperative_execution_supervisor_v0_16 import (
    build_supervisor_command,
    create_supervised_job,
    empty_supervisor_bundle,
    register_job,
    store_command,
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
        "summary": "host adapter fixture step completed",
        "output": {
            "value": operation_input.get("value"),
            "step_id": context.get("step_id"),
            "execution_key": context.get("execution_key"),
        },
        "cost_units": 1.0,
        "checkpoint_payload": {"execution_key": context.get("execution_key")},
    }


def registry() -> dict[str, Any]:
    return {"fixture.success": success_executor}


def steps(count: int = 2) -> list[dict[str, Any]]:
    return [
        {
            "step_id": f"step-{index + 1}",
            "operation_id": "fixture.success",
            "operation_input": {"value": index + 1},
            "estimated_cost_units": 1.0,
            "max_attempts": 2,
        }
        for index in range(max(1, int(count)))
    ]


def queued_bundle(*, job_id: str, job_steps: Sequence[Mapping[str, Any]], policy: Mapping[str, Any] | None = None) -> dict[str, Any]:
    runtime_policy = supervisor_policy() if policy is None else dict(policy)
    job = create_supervised_job(
        job_id=job_id,
        source_parent_digest="host-adapter-parent-v016",
        steps=job_steps,
        initial_budget_units=20.0,
    )
    bundle = register_job(empty_supervisor_bundle("host-adapter-agent"), job)
    command = build_supervisor_command(
        job_id=job_id,
        command_id=f"queue-{job_id}",
        action="queue_background",
        payload={},
        source_job_state_digest=job["job_state_digest"],
    )
    bundle, replayed = store_command(bundle, command, runtime_policy)
    if replayed:
        raise ValueError("fixture_queue_command_replayed")
    return bundle
