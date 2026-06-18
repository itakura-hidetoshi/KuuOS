from __future__ import annotations

from pathlib import Path

from runtime.kuuos_act_os_fixture_v0_1 import apply as apply_act
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs
from runtime.kuuos_act_os_kernel_v0_1 import build_initial_act_state, build_step_authorization
from runtime.kuuos_act_os_lineage_kernel_v0_2 import (
    build_act_lineage_completion_receipt,
    build_authorization_envelope,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_fixture_v0_1 import prepared_gated_state
from runtime.kuuos_learn_os_kernel_v0_1 import build_learn_phase_receipt
from runtime.kuuos_learn_os_lineage_kernel_v0_2 import (
    build_learn_lineage_completion_receipt,
    build_learn_lineage_handoff_receipt,
)
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state
from runtime.kuuos_observe_os_kernel_v0_1 import build_observe_phase_receipt
from runtime.kuuos_observe_os_lineage_kernel_v0_2 import (
    build_observe_lineage_completion_receipt,
    build_observe_lineage_handoff_receipt,
)
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_verify_os_kernel_v0_1 import build_verify_phase_receipt
from runtime.kuuos_verify_os_lineage_kernel_v0_2 import (
    build_verify_lineage_completion_receipt,
    build_verify_lineage_handoff_receipt,
)
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify
from runtime.v02_act_os_replan_lineage_authority_envelope import (
    _compiled_next_plan,
    _handoff as build_act_handoff,
)


def closed_loop_learning_source(root: Path) -> tuple[dict, dict, dict, dict, dict]:
    plan, activation, compiler, _ = _compiled_next_plan(root / "compiled")
    cycle = compiler["mission_cycle_cycle_index"]
    act_handoff = build_act_handoff(
        plan=plan,
        plan_activation=activation,
        compiler_receipt=compiler,
        cycle=cycle,
    )
    policy, bundle, license_packet, projection = host_inputs(
        job_id="plan-v04-closed-loop-job"
    )
    act_store = ActStore(root / "act")
    act_state = act_store.initialize(
        build_initial_act_state(
            act_id="plan-v04-act",
            plan_state=plan,
            plan_activation_receipt=activation,
            now_ms=500_000,
        )
    )
    input_digest = act_handoff["operation_input_digest"]
    act_state = apply_act(
        act_store,
        act_state,
        "select",
        {
            "plan_state": plan,
            "selected_step_id": act_handoff["selected_step_id"],
            "operation_id": act_handoff["operation_id"],
            "operation_input_digest": input_digest,
        },
        410_001,
    )
    authorization = build_step_authorization(
        state=act_state,
        authorization_id="plan-v04-authorization",
        operation_id=act_handoff["operation_id"],
        operation_input_digest=input_digest,
        act_phase_receipt_digest=act_handoff["act_phase_receipt_digest"],
        invocation_id="plan-v04-invocation",
        source_supervisor_bundle_digest=projection["source_supervisor_bundle_digest"],
        host_job_id="plan-v04-closed-loop-job",
        host_step_id="step-1",
        host_license=license_packet,
        human_approval_receipt_digest=sha("plan-v04-human-approval"),
        human_approver_id="human-operator",
        issued_at_ms=500_000,
        expires_at_ms=580_000,
    )
    envelope = build_authorization_envelope(
        handoff_receipt=act_handoff,
        act_state=act_state,
        step_authorization=authorization,
        host_license=license_packet,
        now_ms=500_001,
    )
    act_state = apply_act(
        act_store,
        act_state,
        "authorize",
        {"step_authorization": authorization, "host_license": license_packet},
        410_002,
    )
    act_state = apply_act(
        act_store,
        act_state,
        "project",
        {"host_projection": projection},
        410_003,
    )
    committed_act, _ = finish_act(
        store=act_store,
        state=act_state,
        bundle=bundle,
        policy=policy,
        invoke_ms=500_004,
    )
    act_completion = build_act_lineage_completion_receipt(
        handoff_receipt=act_handoff,
        authorization_envelope=envelope,
        committed_act_state=committed_act,
        now_ms=500_010,
    )

    observe_handoff = build_observe_lineage_handoff_receipt(
        committed_act_state=committed_act,
        act_lineage_handoff_receipt=act_handoff,
        act_lineage_completion_receipt=act_completion,
        mission_cycle_phase="observe",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("plan-v04-observe-cycle-state"),
        observe_phase_event_digest=sha("plan-v04-observe-cycle-event"),
        now_ms=510_000,
    )
    observe_store, assessed = prepared_assessed_state(
        root=root / "observe",
        observe_id="plan-v04-observe",
        act_state=committed_act,
    )
    committed_observe, _ = finish_observe(
        store=observe_store,
        state=assessed,
        verdict="MATCHED",
        tick=5,
    )
    observe_phase = build_observe_phase_receipt(
        state=committed_observe,
        mission_cycle_state_digest=sha("plan-v04-observe-phase-state"),
        observe_phase_event_digest=sha("plan-v04-observe-phase-event"),
        now_ms=520_100,
    )
    observe_completion = build_observe_lineage_completion_receipt(
        handoff_receipt=observe_handoff,
        committed_observe_state=committed_observe,
        observe_phase_receipt=observe_phase,
        now_ms=520_200,
    )

    verify_handoff = build_verify_lineage_handoff_receipt(
        committed_observe_state=committed_observe,
        observe_lineage_handoff_receipt=observe_handoff,
        observe_lineage_completion_receipt=observe_completion,
        mission_cycle_phase="verify",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("plan-v04-verify-cycle-state"),
        verify_phase_event_digest=sha("plan-v04-verify-cycle-event"),
        now_ms=521_000,
    )
    verify_store, corroborated = prepared_corroborated_state(
        root=root / "verify",
        verify_id="plan-v04-verify",
        observe_state=committed_observe,
    )
    committed_verify, _ = finish_verify(
        store=verify_store,
        state=corroborated,
        verdict="PASSED",
        criterion_satisfied=True,
        tick=4,
    )
    verify_phase = build_verify_phase_receipt(
        state=committed_verify,
        mission_cycle_state_digest=sha("plan-v04-verify-phase-state"),
        verify_phase_event_digest=sha("plan-v04-verify-phase-event"),
        now_ms=530_100,
    )
    verify_completion = build_verify_lineage_completion_receipt(
        handoff_receipt=verify_handoff,
        committed_verify_state=committed_verify,
        verify_phase_receipt=verify_phase,
        now_ms=530_200,
    )

    learn_handoff = build_learn_lineage_handoff_receipt(
        committed_verify_state=committed_verify,
        verify_lineage_handoff_receipt=verify_handoff,
        verify_lineage_completion_receipt=verify_completion,
        mission_cycle_phase="learn",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("plan-v04-learn-cycle-state"),
        learn_phase_event_digest=sha("plan-v04-learn-cycle-event"),
        now_ms=531_000,
    )
    learn_store, gated = prepared_gated_state(
        root=root / "learn",
        learn_id="plan-v04-learn",
        verify_state=committed_verify,
        learning_kind="reinforcement",
        target_scope="belief_candidate",
    )
    committed_learn, _ = finish_learn(store=learn_store, state=gated, tick=5)
    learn_phase = build_learn_phase_receipt(
        state=committed_learn,
        mission_cycle_state_digest=sha("plan-v04-learn-phase-state"),
        learn_phase_event_digest=sha("plan-v04-learn-phase-event"),
        now_ms=540_100,
    )
    learn_completion = build_learn_lineage_completion_receipt(
        handoff_receipt=learn_handoff,
        committed_learn_state=committed_learn,
        learn_phase_receipt=learn_phase,
        now_ms=540_200,
    )
    return plan, compiler, committed_learn, learn_handoff, learn_completion
