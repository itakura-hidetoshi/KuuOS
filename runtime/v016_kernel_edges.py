from __future__ import annotations

from runtime.kuuos_supervisor_v016 import (
    build_supervisor_command,
    claim_background_job,
    commit_slice,
    create_supervised_job,
    empty_supervisor_bundle,
    find_job,
    register_job,
    run_supervisor_slice,
    store_command,
)
from runtime.v016_kernel_fixtures import registry, supervisor_policy


def _step(step_id, operation_id, estimate=1.0, permission=""):
    return {
        "step_id": step_id,
        "operation_id": operation_id,
        "operation_input": {"value": step_id},
        "estimated_cost_units": estimate,
        "max_attempts": 3,
        "required_permission": permission,
    }


def _budget_case():
    job = create_supervised_job(
        job_id="budget-job",
        source_parent_digest="parent",
        steps=[_step("budget", "success", estimate=2.0)],
        initial_budget_units=0.5,
    )
    result = run_supervisor_slice(
        job=job,
        slice_id="budget-slice",
        mode="foreground",
        policy=supervisor_policy(auto_background_on_budget_pause=False),
        registry=registry(),
    )
    assert result["supervisor_state"] == "budget_paused"
    assert result["handoff"]["reason_code"] == "cost_budget_exhausted"
    assert result["handoff"]["feedback"]["foreground_prompt_released"] is True
    assert result["completed_step_ids_in_slice"] == []


def _bug_case():
    job = create_supervised_job(
        job_id="bug-job",
        source_parent_digest="parent",
        steps=[_step("bug", "missing-operation")],
        initial_budget_units=5.0,
    )
    result = run_supervisor_slice(
        job=job,
        slice_id="bug-slice",
        mode="foreground",
        policy=supervisor_policy(),
        registry=registry(),
    )
    assert result["supervisor_state"] == "blocked_bug"
    assert result["handoff"]["reason_code"] == "deterministic_bug"
    assert result["handoff"]["background_ticket"] == {}
    assert "inspect_bug" in result["handoff"]["feedback"]["user_actions"]


def _transient_case():
    job = create_supervised_job(
        job_id="timeout-job",
        source_parent_digest="parent",
        steps=[_step("timeout", "timeout")],
        initial_budget_units=5.0,
    )
    result = run_supervisor_slice(
        job=job,
        slice_id="timeout-slice",
        mode="foreground",
        policy=supervisor_policy(auto_background_on_transient_error=False),
        registry=registry(),
    )
    assert result["supervisor_state"] == "retry_backoff"
    assert result["handoff"]["reason_code"] == "timeout"
    assert result["handoff"]["retry_after_ms"] == 2000


def run_edge_cases():
    _budget_case()
    _bug_case()
    _transient_case()
    return True
