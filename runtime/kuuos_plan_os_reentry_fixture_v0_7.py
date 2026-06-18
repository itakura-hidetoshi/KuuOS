from __future__ import annotations

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_multigeneration_fixture_v0_6 import fresh_state, report
from runtime.kuuos_plan_os_multigeneration_kernel_v0_6 import (
    apply_multi_generation_event,
    build_generation_supervision_decision,
    build_multi_generation_event,
)
from runtime.kuuos_plan_os_reentry_kernel_v0_7 import (
    build_external_reentry_receipt,
    build_reentry_controller_state,
)
from runtime.kuuos_plan_os_reentry_types_v0_7 import (
    ACCEPT_HANDOVER,
    RESUME_HOLD,
)


def terminal_state(kind: str) -> dict:
    state = fresh_state(maximum_generations=5, cycle=30)
    kwargs = {
        "tag": f"terminal-{kind.lower()}",
        "plan_change": 0.4,
        "residual": 0.5,
        "now_ms": 1_000,
    }
    if kind == "HOLD":
        kwargs["debt"] = 0.9
    elif kind == "HANDOVER":
        kwargs["human_handover"] = True
    elif kind == "STOPPED":
        kwargs["mission_complete"] = True
    else:
        raise ValueError("terminal_fixture_kind_invalid")
    item = report(state, **kwargs)
    decision = build_generation_supervision_decision(
        state=state, report=item, now_ms=1_001
    )
    event = build_multi_generation_event(
        state=state, report=item, decision=decision, now_ms=1_002
    )
    result = apply_multi_generation_event(state, event)
    assert result["status"] == "APPLIED"
    return result["state"]


def controller_for(kind: str, *, owner: str = "owner-alpha") -> dict:
    return build_reentry_controller_state(
        source_terminal_state=terminal_state(kind),
        current_owner_id=owner,
        now_ms=2_000,
    )


def valid_receipt(controller: dict, *, now_ms: int = 3_000) -> dict:
    if controller["source_terminal_status"] == "HOLD":
        kind = RESUME_HOLD
        proposed = controller["current_owner_id"]
        delegated = controller["current_owner_id"]
        accepted = controller["current_owner_id"]
    else:
        kind = ACCEPT_HANDOVER
        proposed = "owner-beta"
        delegated = controller["current_owner_id"]
        accepted = proposed
    return build_external_reentry_receipt(
        controller_state=controller,
        kind=kind,
        proposed_owner_id=proposed,
        delegated_by_owner_id=delegated,
        accepted_by_owner_id=accepted,
        authority_scope_digest=sha({"scope": kind}),
        evidence_digest=sha({"evidence": kind}),
        issued_at_ms=now_ms,
        expires_at_ms=now_ms + 1_000,
    )
