from __future__ import annotations


def supervisor_policy(**updates):
    packet = {
        "max_steps_per_slice": 1,
        "max_cost_per_slice": 2.0,
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


def success_executor(operation_input, context):
    return {
        "outcome": "success",
        "summary": "step completed",
        "output": {"value": operation_input.get("value"), "step_id": context.get("step_id")},
        "cost_units": 1.0,
        "checkpoint_payload": {"execution_key": context.get("execution_key")},
    }


def timeout_executor(operation_input, context):
    return {
        "outcome": "transient_error",
        "error_kind": "timeout",
        "summary": "temporary timeout",
        "output": {},
        "cost_units": 0.0,
        "checkpoint_payload": {},
    }


def bug_executor(operation_input, context):
    return {
        "outcome": "deterministic_bug",
        "error_kind": "deterministic_bug",
        "summary": "reproducible fixture bug",
        "output": {},
        "cost_units": 0.0,
        "checkpoint_payload": {},
    }


def three_steps():
    return [
        {"step_id": "a", "operation_id": "success", "operation_input": {"value": 1}, "estimated_cost_units": 1.0, "max_attempts": 2},
        {"step_id": "b", "operation_id": "success", "operation_input": {"value": 2}, "estimated_cost_units": 1.0, "max_attempts": 2},
        {"step_id": "c", "operation_id": "success", "operation_input": {"value": 3}, "estimated_cost_units": 1.0, "max_attempts": 2},
    ]


def registry():
    return {
        "success": success_executor,
        "timeout": timeout_executor,
        "bug": bug_executor,
    }
