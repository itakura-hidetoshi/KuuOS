from __future__ import annotations

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_adaptive_agent_runtime_megamodel_v1_0 import (
    MODEL_KINDS,
    build_runtime_megamodel,
    validate_runtime_megamodel,
)
from runtime.kuuos_adaptive_agent_transition_kernel_v1_0 import (
    apply_adaptive_event,
    build_adaptive_event,
    build_initial_adaptive_state,
    validate_adaptive_state,
)


def _emit(state: dict, kind: str, **payload: object) -> dict:
    event = build_adaptive_event(
        kind=kind,
        event_index=state["sequence"] + 1,
        payload=payload,
    )
    return apply_adaptive_event(state, event)


def _build_megamodel() -> dict:
    value = build_runtime_megamodel(
        model_digests={kind: sha({"model": kind}) for kind in MODEL_KINDS}
    )
    assert validate_runtime_megamodel(value) == []
    return value


def _active_plan_session(megamodel: dict, label: str) -> tuple[dict, str]:
    state = build_initial_adaptive_state(
        owner_id="owner-alpha",
        lineage_id=f"lineage-{label}-0",
        runtime_megamodel_digest=megamodel["runtime_megamodel_digest"],
    )
    state = _emit(state, "DECISION_COMMITTED")
    state = _emit(state, "PLAN_BOUND", plan_digest=sha(f"plan-{label}"))
    state = _emit(
        state,
        "AUTHORITY_BOUND",
        authority_receipt_digest=sha(f"authority-{label}"),
    )
    state = _emit(state, "LEASE_ACTIVATED")
    session_digest = sha(f"session-{label}-0")
    state = _emit(
        state,
        "SESSION_BOOTSTRAPPED",
        session_digest=session_digest,
    )
    return state, session_digest


def run_nominal_cycle(megamodel: dict) -> dict:
    state, _ = _active_plan_session(megamodel, "nominal")
    state = _emit(state, "ACT_AUTHORIZED")
    assert state["execution_allowed"] is True
    state = _emit(state, "EFFECT_RECORDED")
    assert state["execution_allowed"] is False
    state = _emit(
        state,
        "OBSERVATION_COMMITTED",
        evidence_digest=sha("nominal-evidence"),
    )
    assert state["observation_committed"] is True
    assert state["verification_committed"] is False
    state = _emit(
        state,
        "VERIFICATION_PASSED",
        verification_digest=sha("nominal-verification"),
    )
    assert state["task_stage"] == "LEARN"
    state = _emit(
        state,
        "LEARNING_COMMITTED",
        next_plan_digest=sha("nominal-next-plan"),
    )
    assert state["task_stage"] == "PLAN"
    assert validate_adaptive_state(state) == []
    return state


def run_order_violation(megamodel: dict) -> None:
    state, _ = _active_plan_session(megamodel, "order")
    state = _emit(state, "ACT_AUTHORIZED")
    state = _emit(state, "EFFECT_RECORDED")
    event = build_adaptive_event(
        kind="VERIFICATION_PASSED",
        event_index=state["sequence"] + 1,
        payload={"verification_digest": sha("premature-verification")},
    )
    try:
        apply_adaptive_event(state, event)
    except ValueError as exc:
        assert str(exc) == "verification_transition_invalid"
    else:
        raise AssertionError("verification accepted before observation")


def run_rerotation_recovery(megamodel: dict) -> dict:
    state, old_session = _active_plan_session(megamodel, "rerotation")
    state = _emit(
        state,
        "LEASE_ANOMALY",
        recovery_decision="REROTATE",
    )
    assert state["control_mode"] == "SUSPENDED"
    assert old_session in state["terminal_session_digests"]
    assert state["active_session_digest"] == ""
    assert state["execution_allowed"] is False

    invalid_act = build_adaptive_event(
        kind="ACT_AUTHORIZED",
        event_index=state["sequence"] + 1,
    )
    try:
        apply_adaptive_event(state, invalid_act)
    except ValueError as exc:
        assert str(exc) == "act_transition_invalid"
    else:
        raise AssertionError("suspended session permitted execution")

    state = _emit(
        state,
        "RECOVERY_ROUTED",
        recovery_decision="REROTATE",
        authority_receipt_digest=sha("rerotation-authority"),
    )
    old_lineage = state["lineage_id"]
    state = _emit(
        state,
        "RECOVERY_COMPLETED",
        new_lineage_id="lineage-rerotation-1",
        new_epoch_index=1,
    )
    assert state["lineage_id"] != old_lineage
    assert state["epoch_index"] == 1
    assert state["requires_new_activation"] is True
    assert state["requires_new_session"] is True
    assert state["active_session_digest"] == ""

    state = _emit(state, "LEASE_ACTIVATED")
    reuse_event = build_adaptive_event(
        kind="SESSION_BOOTSTRAPPED",
        event_index=state["sequence"] + 1,
        payload={"session_digest": old_session},
    )
    try:
        apply_adaptive_event(state, reuse_event)
    except ValueError as exc:
        assert str(exc) == "terminal_session_reactivation_forbidden"
    else:
        raise AssertionError("terminal session was reactivated")

    state = _emit(
        state,
        "SESSION_BOOTSTRAPPED",
        session_digest=sha("session-rerotation-1"),
    )
    assert state["active_session_digest"] not in state[
        "terminal_session_digests"
    ]
    assert validate_adaptive_state(state) == []
    return state


def run_abort(megamodel: dict) -> dict:
    state, old_session = _active_plan_session(megamodel, "abort")
    state = _emit(
        state,
        "LEASE_ANOMALY",
        recovery_decision="ABORT",
    )
    state = _emit(
        state,
        "RECOVERY_ROUTED",
        recovery_decision="ABORT",
        authority_receipt_digest=sha("abort-authority"),
    )
    assert state["task_stage"] == "TERMINAL"
    assert state["control_mode"] == "TERMINATED"
    assert state["execution_allowed"] is False
    assert old_session in state["terminal_session_digests"]
    assert validate_adaptive_state(state) == []
    return state


def run_reference_architecture() -> dict:
    megamodel = _build_megamodel()
    nominal = run_nominal_cycle(megamodel)
    run_order_violation(megamodel)
    rerotation = run_rerotation_recovery(megamodel)
    aborted = run_abort(megamodel)
    return {
        "status": "KUUOS_ADAPTIVE_AGENT_REFERENCE_ARCHITECTURE_V1_0_OK",
        "megamodel_digest": megamodel["runtime_megamodel_digest"],
        "model_count": megamodel["model_count"],
        "relation_count": megamodel["relation_count"],
        "planos_mapping_count": sum(
            1
            for key in megamodel["implementation_refinement_map"]
            if key.startswith("PlanOS_v0_")
        ),
        "nominal_stage": nominal["task_stage"],
        "rerotation_epoch": rerotation["epoch_index"],
        "terminal_session_count": len(
            rerotation["terminal_session_digests"]
        ),
        "abort_mode": aborted["control_mode"],
        "execution_allowed": rerotation["execution_allowed"],
    }
