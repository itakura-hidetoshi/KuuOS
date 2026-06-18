from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_cooperative_host_adapter_v0_17 import (
    build_host_license,
    project_host_work,
)
from runtime.kuuos_plan_os_kernel_v0_1 import build_plan_phase_activation_receipt
from runtime.kuuos_act_os_kernel_v0_1 import (
    build_act_event,
    build_initial_act_state,
    build_step_authorization,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.v017_host_adapter_fixtures import queued_bundle, steps, supervisor_policy
from runtime.v01_plan_os_replan_bound_synthesis import _validate_candidate_plan


def source_plan(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    plan_state, _, _ = _validate_candidate_plan(root / "plan-source")
    activation = build_plan_phase_activation_receipt(
        state=plan_state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("act-fixture-mission-plan"),
        plan_phase_receipt_digest=sha("act-fixture-plan-phase"),
        now_ms=80_000,
    )
    return plan_state, activation


def host_inputs(
    *, job_id: str, expires_at_ms: int = 200_000
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = supervisor_policy()
    bundle = queued_bundle(job_id=job_id, job_steps=steps(1), policy=policy)
    license_packet = build_host_license(
        license_id=job_id + "-license",
        issued_at_ms=80_000,
        expires_at_ms=expires_at_ms,
        operation_allowlist=["fixture.success"],
        max_steps_per_slice=1,
        max_cost_per_slice=1.0,
        lease_duration_ms=60_000,
    )
    projection = project_host_work(
        supervisor_bundle=bundle,
        now_ms=90_000,
        operation_allowlist=["fixture.success"],
    )
    if projection.get("adapter_state") != "work_ready":
        raise AssertionError(projection)
    return policy, bundle, license_packet, projection


def event(
    state: Mapping[str, Any], phase: str, payload: Mapping[str, Any], tick: int
) -> dict[str, Any]:
    return build_act_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=90_000 + tick,
    )


def apply(
    store: ActStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(event(state, phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def prepared_project_state(
    *,
    root: Path,
    act_id: str,
    plan_state: Mapping[str, Any],
    plan_activation: Mapping[str, Any],
    job_id: str,
    host_license: Mapping[str, Any],
    projection: Mapping[str, Any],
) -> tuple[ActStore, dict[str, Any]]:
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id=act_id,
            plan_state=plan_state,
            plan_activation_receipt=plan_activation,
            now_ms=90_000,
        )
    )
    operation_input_digest = sha({"value": 1})
    state = apply(
        store,
        state,
        "select",
        {
            "plan_state": dict(plan_state),
            "selected_step_id": "act-candidate",
            "operation_id": "fixture.success",
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id=act_id + "-authorization",
        operation_id="fixture.success",
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=sha(act_id + "-act-phase"),
        invocation_id=act_id + "-invocation",
        source_supervisor_bundle_digest=projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id=job_id,
        host_step_id="step-1",
        host_license=host_license,
        human_approval_receipt_digest=sha(act_id + "-human-approval"),
        human_approver_id="human-operator",
        issued_at_ms=90_000,
        expires_at_ms=180_000,
    )
    state = apply(
        store,
        state,
        "authorize",
        {"step_authorization": authorization, "host_license": dict(host_license)},
        2,
    )
    state = apply(
        store,
        state,
        "project",
        {"host_projection": dict(projection)},
        3,
    )
    return store, state
