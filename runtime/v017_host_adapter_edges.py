from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_cooperative_execution_supervisor_bundle_v0_16 import find_job
from runtime.kuuos_cooperative_execution_supervisor_job_v0_16 import job_state_digest
from runtime.kuuos_cooperative_execution_supervisor_types_v0_16 import bundle_digest
from runtime.kuuos_cooperative_execution_supervisor_worker_v0_16 import claim_background_job
from runtime.kuuos_cooperative_host_adapter_types_v0_17 import BLOCKED, READY
from runtime.kuuos_cooperative_host_adapter_v0_17 import build_host_license, project_host_work, run_host_tick
from runtime.kuuos_resumable_execution_handoff_types_v0_15 import ticket_digest
from runtime.v017_host_adapter_fixtures import queued_bundle, registry, steps, supervisor_policy


def _license(**updates):
    packet = build_host_license(
        license_id="edge-license",
        issued_at_ms=1000,
        expires_at_ms=100000,
        operation_allowlist=["fixture.success"],
        max_steps_per_slice=1,
        max_cost_per_slice=1.0,
        lease_duration_ms=100,
    )
    packet.update(updates)
    if updates:
        from runtime.kuuos_cooperative_host_adapter_types_v0_17 import license_digest
        packet["host_license_digest"] = ""
        packet["host_license_digest"] = license_digest(packet)
    return packet


def _permission_block_case():
    policy = supervisor_policy()
    bundle = queued_bundle(job_id="permission-block", job_steps=steps(1), policy=policy)
    license_packet = build_host_license(
        license_id="permission-block-license",
        issued_at_ms=1000,
        expires_at_ms=100000,
        operation_allowlist=["fixture.success"],
        permissions={"ticket_claim_allowed": False},
    )
    projection = project_host_work(supervisor_bundle=bundle, now_ms=2000, operation_allowlist=["fixture.success"])
    result = run_host_tick(
        supervisor_bundle=bundle,
        projection=projection,
        host_license=license_packet,
        worker_id="worker-edge",
        invocation_id="permission-block-invocation",
        now_ms=2000,
        supervisor_policy=policy,
        registry=registry(),
    )
    assert result["status"] == BLOCKED
    assert result["adapter_state"] == "blocked_before_claim"
    assert "ticket_claim_allowed_not_true" in result["blockers"]
    assert result["result_supervisor_bundle"] == bundle
    assert find_job(bundle, "permission-block")["supervisor_state"] == "background_queued"


def _operation_block_case():
    bundle = queued_bundle(job_id="operation-block", job_steps=steps(1), policy=supervisor_policy())
    projection = project_host_work(supervisor_bundle=bundle, now_ms=2000, operation_allowlist=["other.operation"])
    assert projection["adapter_state"] == "idle"
    assert projection["selected_job_id"] == ""
    assert projection["candidates"][0]["eligible"] is False
    assert "operation_not_allowlisted_by_host" in projection["candidates"][0]["blockers"]


def _checkpoint_block_case():
    bundle = queued_bundle(job_id="checkpoint-block", job_steps=steps(1), policy=supervisor_policy())
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
    projection = project_host_work(supervisor_bundle=damaged, now_ms=2000, operation_allowlist=["fixture.success"])
    assert projection["adapter_state"] == "idle"
    assert "background_ticket_checkpoint_mismatch" in projection["candidates"][0]["blockers"]


def _expired_lease_case():
    policy = supervisor_policy()
    bundle = queued_bundle(job_id="expired-lease", job_steps=steps(1), policy=policy)
    leased, claimed = claim_background_job(
        bundle,
        job_id="expired-lease",
        worker_id="worker-old",
        now_ms=1000,
        lease_duration_ms=10,
    )
    assert claimed is True
    projection = project_host_work(supervisor_bundle=leased, now_ms=1020, operation_allowlist=["fixture.success"])
    assert projection["adapter_state"] == "work_ready"
    assert projection["selection_reason"] == "expired_lease"
    result = run_host_tick(
        supervisor_bundle=leased,
        projection=projection,
        host_license=_license(),
        worker_id="worker-new",
        invocation_id="expired-reclaim",
        now_ms=1020,
        supervisor_policy=policy,
        registry=registry(),
    )
    assert result["status"] == READY
    assert result["adapter_state"] == "completed"
    assert find_job(result["result_supervisor_bundle"], "expired-lease")["supervisor_state"] == "completed"


def _expired_license_case():
    policy = supervisor_policy()
    bundle = queued_bundle(job_id="expired-license", job_steps=steps(1), policy=policy)
    license_packet = build_host_license(
        license_id="expired-license",
        issued_at_ms=1000,
        expires_at_ms=1500,
        operation_allowlist=["fixture.success"],
    )
    projection = project_host_work(supervisor_bundle=bundle, now_ms=2000, operation_allowlist=["fixture.success"])
    result = run_host_tick(
        supervisor_bundle=bundle,
        projection=projection,
        host_license=license_packet,
        worker_id="worker-edge",
        invocation_id="expired-license-invocation",
        now_ms=2000,
        supervisor_policy=policy,
        registry=registry(),
    )
    assert result["status"] == BLOCKED
    assert "host_license_expired" in result["blockers"]
    assert result["result_supervisor_bundle"] == bundle


def run_edge_cases() -> bool:
    _permission_block_case()
    _operation_block_case()
    _checkpoint_block_case()
    _expired_lease_case()
    _expired_license_case()
    print("PASS: cooperative host adapter v0.17 edge cases")
    return True
