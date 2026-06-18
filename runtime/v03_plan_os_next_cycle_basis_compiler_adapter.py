from __future__ import annotations

import json
import tempfile
from copy import deepcopy
from pathlib import Path

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_plan_os_next_cycle_kernel_v0_3 import (
    build_legacy_compat_activation_receipt,
    build_materialization_packet,
    build_next_cycle_compiler_receipt,
    build_next_cycle_initial_plan_state,
    build_next_plan_activation_receipt,
    project_replan_route,
)
from runtime.kuuos_plan_os_next_cycle_store_v0_3 import (
    NextCycleAdapterStore,
    NextCycleAdapterStoreError,
    build_initial_adapter_store_state,
)
from runtime.kuuos_plan_os_replan_fixture_v0_2 import (
    candidate,
    prepared_constrained_state,
    source_learn_state,
)
from runtime.kuuos_plan_os_replan_kernel_v0_2 import build_replan_phase_receipt
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.v01_plan_os_replan_bound_synthesis import (
    _candidate_steps,
    _complete_plan,
    _make_wa_source,
    _new_plan_state,
    _wa_activation,
)
from runtime.v02_plan_os_qi_conditioned_nonmarkov_replan import _finish


def _current_plan(root: Path) -> tuple[dict, dict]:
    wa_state = _make_wa_source(
        root,
        "v03-current-source",
        plural_route="CONSENSUS_CANDIDATE",
        wa_route="ENDORSE",
    )
    activation = _wa_activation(wa_state, "v03-current")
    store = PlanStore(root / "current-plan")
    state = store.initialize(
        _new_plan_state(
            plan_id="v03-current-plan",
            wa_state=wa_state,
            activation=activation,
        )
    )
    state, _ = _complete_plan(store, state, _candidate_steps(), 10)
    return state, wa_state


def _committed_replan(
    root: Path, current_plan: dict, learn_state: dict
) -> tuple[dict, dict]:
    raw_candidate = candidate(
        "strengthen-next-cycle",
        "strengthen",
        target_scope="belief_candidate",
        cost=0.50,
        risk=0.25,
        transition_distance=0.30,
        switch_benefit=0.75,
    )
    raw_candidate["step_template_digests"] = [
        sha("v03-template-prepare"),
        sha("v03-template-act"),
        sha("v03-template-rollback"),
        sha("v03-template-observe"),
        sha("v03-template-verify"),
    ]
    hold = candidate(
        "hold-alternative",
        "hold",
        target_scope="no_change",
        cost=0.0,
        risk=0.0,
        transition_distance=0.0,
        switch_benefit=0.0,
    )
    store, state = prepared_constrained_state(
        root=root / "replan",
        replan_id="v03-replan",
        current_plan=current_plan,
        learn_state=learn_state,
        candidates=[raw_candidate, hold],
        hysteresis=0.05,
        recovery=0.25,
        transition_readiness=0.80,
        oscillation_count=0,
    )
    state, _ = _finish(
        store=store,
        state=state,
        selected_candidate_id="strengthen-next-cycle",
        tick=20,
    )
    receipt = build_replan_phase_receipt(
        state=state,
        mission_cycle_state_digest=sha("v03-replan-mission-state"),
        replan_phase_event_digest=sha("v03-replan-phase-event"),
        now_ms=320_000,
    )
    return state, receipt


def _materialized_steps(replan_state: dict) -> list[dict]:
    selected = next(
        item
        for item in replan_state["candidates"]
        if item["candidate_id"] == replan_state["selected_candidate_id"]
    )
    templates = replan_state["synthesis_packet"]["next_plan_step_template_digests"]
    steps = _candidate_steps()
    for step, template in zip(steps, templates, strict=True):
        step["template_digest"] = template
        step["source_replan_candidate_id"] = replan_state["selected_candidate_id"]
        step["rollback_point_digest"] = ""
    observe = next(step for step in steps if step["step_class"] == "observe")
    verify = next(step for step in steps if step["step_class"] == "verify")
    effect = next(step for step in steps if step["step_class"] == "act_candidate")
    rollback = next(step for step in steps if step["step_class"] == "repair")
    observe["expected_observation_digest"] = selected["expected_observation_digest"]
    verify["verification_criterion_digest"] = selected[
        "verification_criterion_digest"
    ]
    effect["stop_condition_digests"] = list(selected["stop_condition_digests"])
    rollback["rollback_point_digest"] = selected["rollback_point_digest"]
    return steps


def _activation(
    *,
    current_plan: dict,
    wa_state: dict,
    replan_state: dict,
    replan_receipt: dict,
    cycle: int,
) -> dict:
    return build_next_plan_activation_receipt(
        current_plan_state=current_plan,
        source_wa_state=wa_state,
        replan_state=replan_state,
        replan_phase_receipt=replan_receipt,
        mission_cycle_phase="plan",
        mission_cycle_cycle_index=cycle,
        mission_cycle_state_digest=sha("v03-next-plan-mission-state"),
        mission_plan_phase_event_digest=sha("v03-next-plan-phase-event"),
        now_ms=330_000 + cycle,
    )


def _negative_cycle_cases(
    *,
    current_plan: dict,
    wa_state: dict,
    replan_state: dict,
    replan_receipt: dict,
) -> None:
    expected = replan_state["active_from_cycle"]
    for cycle, expected_error in (
        (expected - 1, "next_cycle_activation_too_early"),
        (expected + 1, "next_cycle_activation_window_missed"),
    ):
        try:
            _activation(
                current_plan=current_plan,
                wa_state=wa_state,
                replan_state=replan_state,
                replan_receipt=replan_receipt,
                cycle=cycle,
            )
        except ValueError as exc:
            assert str(exc) == expected_error
        else:
            raise AssertionError("invalid next-cycle activation accepted")
    try:
        build_next_plan_activation_receipt(
            current_plan_state=current_plan,
            source_wa_state=wa_state,
            replan_state=replan_state,
            replan_phase_receipt=replan_receipt,
            mission_cycle_phase="replan",
            mission_cycle_cycle_index=expected,
            mission_cycle_state_digest=sha("bad-phase"),
            mission_plan_phase_event_digest=sha("bad-event"),
            now_ms=330_100,
        )
    except ValueError as exc:
        assert str(exc) == "next_cycle_plan_phase_required"
    else:
        raise AssertionError("activation outside Plan phase accepted")


def _materialization_negative_cases(
    *,
    current_plan: dict,
    replan_state: dict,
    activation: dict,
    steps: list[dict],
) -> None:
    reordered = deepcopy(steps)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    try:
        build_materialization_packet(
            current_plan_state=current_plan,
            replan_state=replan_state,
            next_plan_activation_receipt=activation,
            steps=reordered,
        )
    except ValueError as exc:
        assert str(exc) == "materialization_template_digest_mismatch"
    else:
        raise AssertionError("reordered templates accepted")

    substituted = deepcopy(steps)
    substituted[0]["source_replan_candidate_id"] = "substituted-candidate"
    try:
        build_materialization_packet(
            current_plan_state=current_plan,
            replan_state=replan_state,
            next_plan_activation_receipt=activation,
            steps=substituted,
        )
    except ValueError as exc:
        assert str(exc) == "materialization_selected_candidate_mismatch"
    else:
        raise AssertionError("substituted candidate accepted")


def _hold_materialization(current_plan: dict, activation: dict, replan_state: dict) -> None:
    hold_state = deepcopy(replan_state)
    hold_state["route"] = "HOLD"
    hold_state["selected_candidate_id"] = "hold-only"
    hold_state["selected_candidate_digest"] = sha("hold-only")
    hold_state["replan_state_digest"] = activation["replan_state_digest"]
    hold_activation = deepcopy(activation)
    hold_activation["replan_route"] = "HOLD"
    hold_activation["projected_plan_route"] = "HOLD"
    hold_activation["selected_candidate_id"] = "hold-only"
    hold_activation["selected_candidate_digest"] = sha("hold-only")
    from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
        next_plan_activation_receipt_digest,
    )

    hold_activation["next_plan_activation_receipt_digest"] = ""
    hold_activation["next_plan_activation_receipt_digest"] = next_plan_activation_receipt_digest(
        hold_activation
    )
    packet = build_materialization_packet(
        current_plan_state=current_plan,
        replan_state=hold_state,
        next_plan_activation_receipt=hold_activation,
        steps=[],
        withheld_template_digests=hold_state["synthesis_packet"][
            "next_plan_step_template_digests"
        ],
    )
    assert packet["v01_steps"] == []
    assert packet["projected_plan_route"] == "HOLD"


def run_kernel() -> dict:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v03-") as temporary:
        root = Path(temporary)
        current_plan, wa_state = _current_plan(root / "source")
        learn_state = source_learn_state(root / "learn", verdict="PASSED")
        assert current_plan["mission_contract_digest"] == learn_state[
            "mission_contract_digest"
        ]
        replan_state, replan_receipt = _committed_replan(
            root, current_plan, learn_state
        )
        _negative_cycle_cases(
            current_plan=current_plan,
            wa_state=wa_state,
            replan_state=replan_state,
            replan_receipt=replan_receipt,
        )
        activation = _activation(
            current_plan=current_plan,
            wa_state=wa_state,
            replan_state=replan_state,
            replan_receipt=replan_receipt,
            cycle=replan_state["active_from_cycle"],
        )
        steps = _materialized_steps(replan_state)
        _materialization_negative_cases(
            current_plan=current_plan,
            replan_state=replan_state,
            activation=activation,
            steps=steps,
        )
        materialization = build_materialization_packet(
            current_plan_state=current_plan,
            replan_state=replan_state,
            next_plan_activation_receipt=activation,
            steps=steps,
        )
        legacy = build_legacy_compat_activation_receipt(
            source_wa_state=wa_state,
            replan_phase_receipt=replan_receipt,
            next_plan_activation_receipt=activation,
            now_ms=340_000,
        )
        next_plan_store = PlanStore(root / "compiled-next-plan")
        next_plan = next_plan_store.initialize(
            build_next_cycle_initial_plan_state(
                plan_id="v03-compiled-next-plan",
                source_wa_state=wa_state,
                legacy_compat_activation_receipt=legacy,
                replan_state=replan_state,
                next_plan_activation_receipt=activation,
                plan_budget=2.0,
                maximum_step_risk=0.40,
                now_ms=350_000,
            )
        )
        next_plan, _ = _complete_plan(
            next_plan_store, next_plan, materialization["v01_steps"], 100
        )
        receipt = build_next_cycle_compiler_receipt(
            previous_plan_state=current_plan,
            replan_state=replan_state,
            next_plan_activation_receipt=activation,
            materialization_packet=materialization,
            compiled_plan_state=next_plan,
            now_ms=360_000,
        )
        adapter_store = NextCycleAdapterStore(root / "adapter-store")
        adapter_store.initialize(
            build_initial_adapter_store_state(
                adapter_id="v03-adapter", now_ms=300_000
            )
        )
        committed = adapter_store.commit(receipt)
        assert committed["status"] == "COMMITTED"
        before_replay = adapter_store.ledger_commit_count()
        replay = adapter_store.commit(receipt)
        assert replay["status"] == "REPLAYED"
        assert adapter_store.ledger_commit_count() == before_replay

        conflict = deepcopy(receipt)
        conflict["compiled_plan_state_digest"] = sha("conflicting-plan")
        from runtime.kuuos_plan_os_next_cycle_types_v0_3 import (
            next_cycle_compiler_receipt_digest,
        )

        conflict["next_cycle_compiler_receipt_digest"] = ""
        conflict["next_cycle_compiler_receipt_digest"] = next_cycle_compiler_receipt_digest(
            conflict
        )
        try:
            adapter_store.commit(conflict)
        except NextCycleAdapterStoreError as exc:
            assert str(exc) == "adapter_replan_receipt_already_consumed"
        else:
            raise AssertionError("conflicting single-use activation accepted")

        snapshot = root / "adapter-store" / "next-cycle-adapter-snapshot.json"
        snapshot.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            adapter_store.recover(require_snapshot_match=True)
        except NextCycleAdapterStoreError as exc:
            assert str(exc) == "adapter_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt adapter snapshot accepted")
        adapter_store.repair_snapshot()
        recovered = adapter_store.recover(require_snapshot_match=True)
        assert recovered["committed_records"] == 1

        _hold_materialization(current_plan, activation, replan_state)
        assert project_replan_route("NEXT_PLAN_CANDIDATE") == "PLAN_CANDIDATE"
        assert project_replan_route("REPAIR_PLAN_CANDIDATE") == "REPAIR_PLAN"
        assert project_replan_route("REOBSERVATION_PLAN_CANDIDATE") == "OBSERVATION_PLAN"
        assert project_replan_route("REROUTE_PLAN_CANDIDATE") == "HANDOVER_PLAN"
        assert project_replan_route("TERMINATION_PLAN_CANDIDATE") == "HANDOVER_PLAN"
        assert project_replan_route("HOLD") == "HOLD"

        return {
            "status": "PLAN_OS_NEXT_CYCLE_BASIS_COMPILER_ADAPTER_V0_3_OK",
            "replan_route": replan_state["route"],
            "projected_plan_route": activation["projected_plan_route"],
            "active_from_cycle": replan_state["active_from_cycle"],
            "compiled_plan_id": next_plan["plan_id"],
            "compiled_plan_state_digest": next_plan["plan_state_digest"],
            "compiled_plan_basis_digest": next_plan["plan_basis_digest"],
            "next_plan_basis_digest": replan_state["next_plan_basis_digest"],
            "compiler_receipt_digest": receipt[
                "next_cycle_compiler_receipt_digest"
            ],
            "adapter_ledger_commits": adapter_store.ledger_commit_count(),
            "previous_plan_unchanged": receipt["previous_plan_unchanged"],
            "plan_not_execution": receipt["plan_not_execution"],
            "host_license_granted": receipt["host_license_granted"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
