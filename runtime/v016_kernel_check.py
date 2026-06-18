from __future__ import annotations

from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest, job_state_digest, slice_digest
from runtime.kuuos_supervisor_v016 import (
    build_supervisor_command,
    claim_background_job,
    commit_background_slice,
    commit_slice,
    create_supervised_job,
    empty_supervisor_bundle,
    find_job,
    heartbeat_background_job,
    register_job,
    run_supervisor_slice,
    store_command,
)
from runtime.v016_kernel_fixtures import registry, supervisor_policy, three_steps


def main():
    policy = supervisor_policy()
    executors = registry()
    job = create_supervised_job(
        job_id="cooperative-job",
        source_parent_digest="parent-v015",
        steps=three_steps(),
        initial_budget_units=10.0,
    )
    assert job["job_state_digest"] == job_state_digest(job)
    bundle = register_job(empty_supervisor_bundle("agent"), job)
    assert bundle["supervisor_bundle_digest"] == bundle_digest(bundle)

    first = run_supervisor_slice(
        job=find_job(bundle, "cooperative-job"),
        slice_id="slice-1",
        mode="foreground",
        policy=policy,
        registry=executors,
    )
    assert first["slice_digest"] == slice_digest(first)
    assert first["completed_step_ids_in_slice"] == ["a"]
    assert first["supervisor_state"] == "foreground_yielded"
    assert first["yield_receipt"]["foreground_prompt_released"] is True
    assert first["yield_receipt"]["next_step_id"] == "b"
    bundle, replayed = commit_slice(bundle, first)
    assert replayed is False
    replay_bundle, replayed = commit_slice(bundle, first)
    assert replayed is True and replay_bundle == bundle

    current = find_job(bundle, "cooperative-job")
    command = build_supervisor_command(
        job_id="cooperative-job",
        command_id="continue-1",
        action="continue_foreground",
        payload={},
        source_job_state_digest=current["job_state_digest"],
    )
    bundle, replayed = store_command(bundle, command, policy)
    assert replayed is False
    command_replay, replayed = store_command(bundle, command, policy)
    assert replayed is True and command_replay == bundle

    second = run_supervisor_slice(
        job=find_job(bundle, "cooperative-job"),
        slice_id="slice-2",
        mode="foreground",
        policy=policy,
        registry=executors,
    )
    assert second["completed_step_ids_in_slice"] == ["b"]
    assert second["yield_receipt"]["next_step_id"] == "c"
    bundle, replayed = commit_slice(bundle, second)
    assert replayed is False

    current = find_job(bundle, "cooperative-job")
    queue = build_supervisor_command(
        job_id="cooperative-job",
        command_id="queue-1",
        action="queue_background",
        payload={},
        source_job_state_digest=current["job_state_digest"],
    )
    bundle, replayed = store_command(bundle, queue, policy)
    assert replayed is False
    queued = find_job(bundle, "cooperative-job")
    assert queued["supervisor_state"] == "background_queued"
    assert queued["active_continuation_ticket"]["queue_status"] == "queued"

    bundle, claimed = claim_background_job(
        bundle,
        job_id="cooperative-job",
        worker_id="worker-a",
        now_ms=1000,
        lease_duration_ms=100,
    )
    assert claimed is True
    leased = find_job(bundle, "cooperative-job")
    assert leased["supervisor_state"] == "background_leased"
    assert leased["active_continuation_ticket"]["lease_owner"] == "worker-a"
    bundle, heartbeated = heartbeat_background_job(
        bundle,
        job_id="cooperative-job",
        worker_id="worker-a",
        now_ms=1050,
        lease_duration_ms=100,
    )
    assert heartbeated is True

    background = run_supervisor_slice(
        job=find_job(bundle, "cooperative-job"),
        slice_id="slice-3",
        mode="background",
        policy=policy,
        registry=executors,
    )
    assert background["completed_step_ids_in_slice"] == ["c"]
    assert background["supervisor_state"] == "completed"
    bundle, replayed = commit_background_slice(bundle, background, worker_id="worker-a")
    assert replayed is False
    completed = find_job(bundle, "cooperative-job")
    assert completed["supervisor_state"] == "completed"
    assert completed["completed_step_ids"] == ["a", "b", "c"]
    assert len(completed["step_receipts"]) == 3
    assert bundle["supervisor_bundle_digest"] == bundle_digest(bundle)
    print("PASS: cooperative execution supervisor v0.16 main flow")
    return True


if __name__ == "__main__":
    main()
