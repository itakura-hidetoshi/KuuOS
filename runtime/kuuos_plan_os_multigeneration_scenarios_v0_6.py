from __future__ import annotations

import json
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_multigeneration_fixture_v0_6 import (
    decision_for,
    fresh_state,
    report,
)
from runtime.kuuos_plan_os_multigeneration_kernel_v0_6 import (
    build_generation_supervision_decision,
    build_multi_generation_event,
)
from runtime.kuuos_plan_os_multigeneration_store_v0_6 import (
    MultiGenerationStoreError,
    MultiGenerationSupervisorStore,
)
from runtime.kuuos_plan_os_multigeneration_types_v0_6 import (
    ACTIVE,
    CONTINUE,
    HANDOVER_AUTHORITY,
    HANDOVER_HUMAN,
    HOLD_OBSERVATION_DEBT,
    HOLD_RECOVERY,
    STOP_CONVERGED,
    STOP_MAX_GENERATIONS,
    STOP_MISSION_COMPLETE,
    STOP_OSCILLATION,
    STOP_STAGNATION,
    report_digest,
)


def run_primary_store_scenario(root: Path) -> tuple[dict, MultiGenerationSupervisorStore]:
    state = fresh_state(maximum_generations=3, cycle=10)
    store = MultiGenerationSupervisorStore(root / "supervisor-store")
    state = store.initialize(state)

    first_report = report(
        state,
        tag="generation-one",
        plan_change=0.35,
        residual=0.60,
        now_ms=1_000,
    )
    first_decision = build_generation_supervision_decision(
        state=state, report=first_report, now_ms=1_001
    )
    assert first_decision["decision"] == CONTINUE
    first_event = build_multi_generation_event(
        state=state,
        report=first_report,
        decision=first_decision,
        now_ms=1_002,
    )
    result = store.apply(first_event)
    assert result["status"] == "APPLIED"
    state = result["state"]
    assert state["status"] == ACTIVE
    assert state["completed_generations"] == 1
    assert state["current_cycle_index"] == 11
    assert store.apply(first_event)["status"] == "REPLAYED"
    assert store.ledger_commit_count() == 1

    broken = report(
        state,
        tag="broken-chain",
        plan_change=0.30,
        residual=0.50,
        now_ms=1_100,
    )
    broken["previous_generation_report_digest"] = sha("wrong-previous")
    broken["supervised_generation_report_digest"] = ""
    broken["supervised_generation_report_digest"] = report_digest(broken)
    try:
        build_generation_supervision_decision(
            state=state, report=broken, now_ms=1_101
        )
    except ValueError as exc:
        assert str(exc) == "multi_generation_report_chain_broken"
    else:
        raise AssertionError("broken generation chain accepted")

    second_report = report(
        state,
        tag="generation-two",
        plan_change=0.02,
        residual=0.03,
        now_ms=2_000,
    )
    second_decision = build_generation_supervision_decision(
        state=state, report=second_report, now_ms=2_001
    )
    assert second_decision["decision"] == STOP_CONVERGED
    second_event = build_multi_generation_event(
        state=state,
        report=second_report,
        decision=second_decision,
        now_ms=2_002,
    )
    result = store.apply(second_event)
    assert result["status"] == "APPLIED"
    state = result["state"]
    assert state["completed_generations"] == 2
    assert state["current_cycle_index"] == 12
    assert state["status"] == "STOPPED"
    assert state["next_generation_authorized"] is False
    try:
        report(state, tag="forbidden-third", now_ms=3_000)
    except ValueError as exc:
        assert str(exc) == "multi_generation_supervisor_not_active"
    else:
        raise AssertionError("terminal supervisor allowed another generation")

    snapshot = root / "supervisor-store" / "multi-generation-snapshot.json"
    snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
    try:
        store.recover(require_snapshot_match=True)
    except MultiGenerationStoreError as exc:
        assert str(exc) == "multi_generation_snapshot_ledger_mismatch"
    else:
        raise AssertionError("corrupt multi-generation snapshot accepted")
    store.repair_snapshot()
    return store.recover(require_snapshot_match=True), store


def verify_decision_matrix() -> list[str]:
    checks = [
        (decision_for(fresh_state(), tag="human", human_handover=True), HANDOVER_HUMAN),
        (
            decision_for(
                fresh_state(), tag="authority", authority_boundary=True
            ),
            HANDOVER_AUTHORITY,
        ),
        (
            decision_for(fresh_state(), tag="mission", mission_complete=True),
            STOP_MISSION_COMPLETE,
        ),
        (
            decision_for(fresh_state(maximum_generations=1), tag="maximum"),
            STOP_MAX_GENERATIONS,
        ),
        (
            decision_for(fresh_state(), tag="stagnation", stagnation=2),
            STOP_STAGNATION,
        ),
        (
            decision_for(fresh_state(), tag="oscillation", oscillation=2),
            STOP_OSCILLATION,
        ),
        (
            decision_for(fresh_state(), tag="debt", debt=0.90),
            HOLD_OBSERVATION_DEBT,
        ),
        (
            decision_for(fresh_state(), tag="recovery", recovery=0.90),
            HOLD_RECOVERY,
        ),
    ]
    for actual, expected in checks:
        assert actual == expected
    return [expected for _, expected in checks] + [STOP_CONVERGED, CONTINUE]
