#!/usr/bin/env python3

from copy import deepcopy

from runtime.kuuos_resumable_execution_handoff_types_v0_15 import (
    PAUSED_OR_BLOCKED_STATES,
    bundle_digest,
    checkpoint_digest,
    decision_digest,
    feedback_digest,
    ticket_digest,
)
from runtime.kuuos_resumable_execution_handoff_v0_15 import (
    build_execution_handoff,
    claim_next_background_ticket,
    commit_execution_handoff,
    empty_handoff_bundle,
    finish_ticket_in_bundle,
    heartbeat_ticket_in_bundle,
)


def observation(attempt_id: str, **updates):
    packet = {
        "job_id": "job-1",
        "attempt_id": attempt_id,
        "source_parent_digest": "parent-digest",
        "phase": "integration",
        "completed_work_units": 4,
        "total_work_units": 10,
        "last_successful_operation": "validated previous checkpoint",
        "checkpoint_payload": {"completed_files": ["a.py", "b.py"]},
        "remaining_cost_units": 10.0,
        "estimated_next_cost_units": 1.0,
        "wait_elapsed_ms": 0,
        "external_dependency_ready": True,
        "background_capable": True,
        "background_requested": False,
        "retry_count": 0,
        "error_kind": "",
        "blocker_summary": "",
        "user_input_required": False,
        "completed": False,
        "cancelled": False,
    }
    packet.update(updates)
    return packet


def main():
    plan = {
        "background_handoff_enabled": True,
        "auto_background_on_budget_pause": True,
        "auto_background_on_external_wait": True,
        "auto_background_on_transient_error": True,
        "cost_reserve_units": 0.5,
        "foreground_wait_threshold_ms": 10000,
        "external_recheck_after_ms": 5000,
        "retry_backoff_base_ms": 1000,
        "max_retry_backoff_ms": 60000,
        "max_retries": 3,
    }

    cases = {
        "cost_background": observation(
            "attempt-cost-background",
            remaining_cost_units=0.2,
            estimated_next_cost_units=1.0,
        ),
        "cost_foreground_release": observation(
            "attempt-cost-no-worker",
            remaining_cost_units=0.2,
            estimated_next_cost_units=1.0,
            background_capable=False,
        ),
        "external_wait": observation(
            "attempt-wait",
            wait_elapsed_ms=20000,
            external_dependency_ready=False,
            blocker_summary="Waiting for an external build runner.",
        ),
        "transient": observation(
            "attempt-timeout",
            error_kind="timeout",
            retry_count=1,
            blocker_summary="The remote operation timed out.",
        ),
        "bug": observation(
            "attempt-bug",
            error_kind="deterministic_bug",
            blocker_summary="The same parser branch fails for the checkpointed input.",
        ),
        "permission": observation(
            "attempt-permission",
            error_kind="permission_denied",
            blocker_summary="The write action lacks repository permission.",
        ),
        "user_input": observation(
            "attempt-input",
            user_input_required=True,
            blocker_summary="A target scope must be selected.",
        ),
        "retry_exhausted": observation(
            "attempt-retry-limit",
            error_kind="transient_error",
            retry_count=3,
        ),
        "running": observation("attempt-running"),
        "completed": observation("attempt-completed", completed=True),
        "cancelled": observation("attempt-cancelled", cancelled=True),
    }
    decisions = {
        name: build_execution_handoff(observation=value, plan=plan)
        for name, value in cases.items()
    }

    assert decisions["cost_background"]["execution_state"] == "background_queued"
    assert decisions["cost_background"]["reason_code"] == "cost_budget_exhausted"
    assert decisions["cost_background"]["background_ticket"]
    assert decisions["cost_foreground_release"]["execution_state"] == "budget_paused"
    assert decisions["cost_foreground_release"]["background_disposition"] == "unsupported"
    assert decisions["external_wait"]["execution_state"] == "background_queued"
    assert decisions["external_wait"]["reason_code"] == "external_latency"
    assert decisions["transient"]["execution_state"] == "background_queued"
    assert decisions["transient"]["retry_after_ms"] == 2000
    assert decisions["bug"]["execution_state"] == "blocked_bug"
    assert not decisions["bug"]["background_ticket"]
    assert "inspect_bug" in decisions["bug"]["feedback"]["user_actions"]
    assert decisions["permission"]["execution_state"] == "permission_blocked"
    assert decisions["user_input"]["execution_state"] == "needs_user_input"
    assert decisions["retry_exhausted"]["execution_state"] == "retry_exhausted"
    assert decisions["running"]["execution_state"] == "running"
    assert decisions["running"]["foreground_prompt_released"] is False
    assert decisions["completed"]["execution_state"] == "completed"
    assert decisions["cancelled"]["execution_state"] == "cancelled"

    for decision in decisions.values():
        assert decision["handoff_decision_digest"] == decision_digest(decision)
        assert decision["checkpoint"]["checkpoint_digest"] == checkpoint_digest(
            decision["checkpoint"]
        )
        assert decision["feedback"]["feedback_digest"] == feedback_digest(
            decision["feedback"]
        )
        assert decision["feedback_receipt_present"] is True
        assert decision["feedback"]["no_silent_stop"] is True
        if decision["execution_state"] != "running":
            assert decision["foreground_prompt_released"] is True
            assert decision["feedback"]["foreground_prompt_released"] is True
        if decision["execution_state"] in PAUSED_OR_BLOCKED_STATES:
            assert decision["feedback"]["resume_condition"]
        if decision["background_ticket"]:
            assert decision["background_ticket"]["background_ticket_digest"] == ticket_digest(
                decision["background_ticket"]
            )
            assert decision["background_ticket"]["checkpoint_digest"] == decision[
                "checkpoint_digest"
            ]

    bundle = empty_handoff_bundle("agent")
    committed, replayed = commit_execution_handoff(
        previous=bundle,
        decision=decisions["cost_background"],
    )
    assert replayed is False
    assert committed["generation"] == 1
    assert len(committed["feedback_history"]) == 1
    assert len(committed["checkpoint_history"]) == 1
    assert len(committed["background_queue"]) == 1
    assert committed["handoff_bundle_digest"] == bundle_digest(committed)

    replay, replayed = commit_execution_handoff(
        previous=committed,
        decision=decisions["cost_background"],
    )
    assert replayed is True and replay == committed

    leased_bundle, ticket, claimed = claim_next_background_ticket(
        committed,
        worker_id="worker-a",
        now_ms=1000,
        lease_duration_ms=100,
    )
    assert claimed is True
    assert ticket["queue_status"] == "leased"
    assert ticket["lease_owner"] == "worker-a"
    assert leased_bundle["handoff_bundle_digest"] == bundle_digest(leased_bundle)

    heartbeat_bundle, changed = heartbeat_ticket_in_bundle(
        leased_bundle,
        ticket_id=ticket["ticket_id"],
        worker_id="worker-a",
        now_ms=1050,
        lease_duration_ms=100,
    )
    assert changed is True
    heartbeated_ticket = heartbeat_bundle["background_queue"][0]
    assert heartbeated_ticket["lease_expires_at_ms"] == 1150

    reclaimed_bundle, reclaimed_ticket, reclaimed = claim_next_background_ticket(
        heartbeat_bundle,
        worker_id="worker-b",
        now_ms=1200,
        lease_duration_ms=100,
    )
    assert reclaimed is True
    assert reclaimed_ticket["lease_owner"] == "worker-b"

    finished_bundle, finished = finish_ticket_in_bundle(
        reclaimed_bundle,
        ticket_id=reclaimed_ticket["ticket_id"],
        worker_id="worker-b",
        final_status="completed",
        summary="Continuation completed from the persisted checkpoint.",
    )
    assert finished is True
    assert finished_bundle["background_queue"][0]["queue_status"] == "completed"
    assert finished_bundle["handoff_bundle_digest"] == bundle_digest(finished_bundle)

    tampered = deepcopy(decisions["bug"])
    tampered["reason_code"] = "execution_active"
    try:
        commit_execution_handoff(previous=bundle, decision=tampered)
        raise AssertionError("tampered handoff decision was accepted")
    except ValueError as error:
        assert str(error) == "handoff_decision_digest_invalid"

    text = repr({"decisions": decisions, "bundle": finished_bundle}).lower()
    for token in ("'nodes'", "'edges'", "'graph'", "'dependencies'"):
        assert token not in text

    print("PASS: resumable execution handoff v0.15 kernel")


if __name__ == "__main__":
    main()
