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
    result = run_supervisor_slice(job=job, slice_id="budget-slice", mode="foreground", policy=supervisor_policy(auto_background_on_budget_pause=False), registry=registry())
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
    result = run_supervisor_slice(job=job, slice_id="bug-slice", mode="foreground", policy=supervisor_policy(), registry=registry())
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
    result = run_supervisor_slice(job=job, slice_id="timeout-slice", mode="foreground", policy=supervisor_policy(auto_background_on_transient_error=False), registry=registry())
    assert result["supervisor_state"] == "retry_backoff"
    assert result["handoff"]["reason_code"] == "timeout"
    assert result["handoff"]["retry_after_ms"] == 2000


def _permission_case():
    policy = supervisor_policy()
    job = create_supervised_job(
        job_id="permission-job",
        source_parent_digest="parent",
        steps=[_step("write", "success", permission="repo-write")],
        initial_budget_units=5.0,
    )
    bundle = register_job(empty_supervisor_bundle("agent"), job)
    blocked = run_supervisor_slice(job=job, slice_id="permission-block", mode="foreground", policy=policy, registry=registry())
    assert blocked["supervisor_state"] == "permission_blocked"
    bundle, replayed = commit_slice(bundle, blocked)
    assert replayed is False
    current = find_job(bundle, "permission-job")
    command = build_supervisor_command(
        job_id="permission-job",
        command_id="grant-write",
        action="grant_permission",
        payload={"permission": "repo-write"},
        source_job_state_digest=current["job_state_digest"],
    )
    bundle, replayed = store_command(bundle, command, policy)
    assert replayed is False
    resumed = run_supervisor_slice(job=find_job(bundle, "permission-job"), slice_id="permission-resume", mode="foreground", policy=policy, registry=registry())
    assert resumed["supervisor_state"] == "completed"


def _revision_case():
    policy = supervisor_policy()
    steps = [_step("a", "success"), _step("b", "success"), _step("c", "success")]
    job = create_supervised_job(job_id="revision-job", source_parent_digest="parent", steps=steps, initial_budget_units=10.0)
    bundle = register_job(empty_supervisor_bundle("agent"), job)
    first = run_supervisor_slice(job=job, slice_id="revision-first", mode="foreground", policy=policy, registry=registry())
    bundle, _ = commit_slice(bundle, first)
    current = find_job(bundle, "revision-job")
    revise = build_supervisor_command(
        job_id="revision-job",
        command_id="revise-b",
        action="revise_input",
        payload={"step_id": "b", "operation_input": {"value": 99}},
        source_job_state_digest=current["job_state_digest"],
    )
    bundle, _ = store_command(bundle, revise, policy)
    revised = find_job(bundle, "revision-job")
    assert revised["manifest_revision"] == 2
    assert revised["completed_step_ids"] == ["a"]
    assert revised["steps"][1]["operation_input"]["value"] == 99
    reduce = build_supervisor_command(
        job_id="revision-job",
        command_id="drop-c",
        action="reduce_scope",
        payload={"drop_step_ids": ["c"]},
        source_job_state_digest=revised["job_state_digest"],
    )
    bundle, _ = store_command(bundle, reduce, policy)
    reduced = find_job(bundle, "revision-job")
    assert reduced["manifest_revision"] == 3
    assert [step["step_id"] for step in reduced["steps"]] == ["a", "b"]
    final = run_supervisor_slice(job=reduced, slice_id="revision-final", mode="foreground", policy=policy, registry=registry())
    assert final["supervisor_state"] == "completed"


def _lease_reclaim_case():
    policy = supervisor_policy()
    job = create_supervised_job(job_id="lease-job", source_parent_digest="parent", steps=[_step("lease", "success")], initial_budget_units=5.0)
    bundle = register_job(empty_supervisor_bundle("agent"), job)
    command = build_supervisor_command(
        job_id="lease-job",
        command_id="queue-lease",
        action="queue_background",
        payload={},
        source_job_state_digest=job["job_state_digest"],
    )
    bundle, _ = store_command(bundle, command, policy)
    bundle, claimed = claim_background_job(bundle, job_id="lease-job", worker_id="worker-a", now_ms=1000, lease_duration_ms=100)
    assert claimed is True
    bundle, reclaimed = claim_background_job(bundle, job_id="lease-job", worker_id="worker-b", now_ms=1200, lease_duration_ms=100)
    assert reclaimed is True
    assert find_job(bundle, "lease-job")["active_continuation_ticket"]["lease_owner"] == "worker-b"


def run_edge_cases():
    _budget_case()
    _bug_case()
    _transient_case()
    _permission_case()
    _revision_case()
    _lease_reclaim_case()
    return True
