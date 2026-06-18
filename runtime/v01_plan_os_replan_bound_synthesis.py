from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_initial_plan_state,
    build_plan_event,
    build_plan_phase_activation_receipt,
)
from runtime.kuuos_plan_os_store_v0_1 import PlanStore, PlanStoreError
from runtime.kuuos_plan_os_types_v0_1 import copy_non_authority
from runtime.v02_decision_os_plural_harmony_appeal import _appeal
from runtime.v03_decision_os_wa_relational_harmony import (
    _complete_wa_cycle,
    _initial_wa,
    _plural_source,
    _profile,
    _standard_profiles,
)


def _make_wa_source(
    root: Path,
    name: str,
    *,
    plural_route: str,
    wa_route: str,
    appeals: Sequence[Mapping[str, Any]] = (),
    handover_required: bool = False,
    weak_dialogue: bool = False,
) -> dict[str, Any]:
    plural_state = _plural_source(
        root,
        name + "-plural",
        requested_route=plural_route,
        appeals=appeals,
        handover_required=handover_required,
    )
    store = WaDecisionStore(root / (name + "-wa"))
    state = store.initialize(_initial_wa(plural_state, name + "-wa-state"))
    profiles = _standard_profiles(plural_state)
    if weak_dialogue:
        profiles[0] = _profile(
            plural_state,
            "option-a",
            positive_lower=0.82,
            positive_upper=0.92,
            weak_dimension="dialogue",
            weak_interval=(0.20, 0.30),
        )
    state, _ = _complete_wa_cycle(
        store,
        state,
        profiles=profiles,
        requested_route=wa_route,
        tick_base=20,
    )
    return state


def _wa_activation(state: Mapping[str, Any], suffix: str) -> dict[str, Any]:
    return build_replan_wa_activation_receipt(
        state=state,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=sha("mission-cycle-" + suffix),
        replan_receipt_digest=sha("replan-receipt-" + suffix),
        next_plan_basis_digest=sha("next-plan-basis-" + suffix),
        now_ms=50_000,
    )


def _step(
    step_id: str,
    step_class: str,
    rank: int,
    *,
    depends_on: Sequence[str] = (),
    cost: float = 0.10,
    risk: float = 0.10,
    rollback_step_id: str = "",
    effectful: bool = False,
    external: bool = False,
    human: bool = False,
    source_option_id: str = "option-a",
    stop_conditions: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "step_id": step_id,
        "step_class": step_class,
        "rank": rank,
        "depends_on": list(depends_on),
        "precondition_digests": [sha("precondition-" + step_id)],
        "expected_observation_digest": sha("observation-" + step_id),
        "verification_criterion_digest": sha("verification-" + step_id),
        "estimated_cost": cost,
        "estimated_risk": risk,
        "reversibility": 0.90,
        "rollback_step_id": rollback_step_id,
        "stop_condition_digests": list(stop_conditions),
        "requires_external_license": external,
        "requires_human_review": human,
        "effectful": effectful,
        "source_option_id": source_option_id,
        "stakeholder_scope_digests": [sha("stakeholder-" + step_id)],
    }


def _candidate_steps(*, cost: float = 0.10) -> list[dict[str, Any]]:
    return [
        _step("prepare", "prepare", 0, cost=cost),
        _step(
            "act-candidate",
            "act_candidate",
            1,
            depends_on=["prepare"],
            cost=cost,
            rollback_step_id="rollback",
            effectful=True,
            external=True,
            human=True,
            stop_conditions=[sha("stop-risk"), sha("stop-dissent")],
        ),
        _step(
            "rollback", "repair", 2, depends_on=["act-candidate"], cost=cost
        ),
        _step("observe", "observe", 2, depends_on=["act-candidate"], cost=cost),
        _step("verify", "verify", 3, depends_on=["observe"], cost=cost),
    ]


def _event(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_plan_event(
        state=state,
        target_phase=target_phase,
        artifact_digest=sha(
            {"target_phase": target_phase, "payload": dict(payload), "tick": tick}
        ),
        payload=payload,
        now_ms=60_000 + tick,
    )


def _apply(
    store: PlanStore,
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_event(state, target_phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _complete_plan(
    store: PlanStore,
    state: Mapping[str, Any],
    steps: Sequence[Mapping[str, Any]],
    tick_base: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    phases = (
        ("decompose", {"steps": list(steps)}),
        ("order", {"dependency_receipt_digest": sha("dependency-receipt")}),
        ("resource", {"resource_receipt_digest": sha("resource-receipt")}),
        ("guard", {"guard_receipt_digest": sha("guard-receipt")}),
        ("checkpoint", {"checkpoint_receipt_digest": sha("checkpoint-receipt")}),
        ("verify", {"verification_receipt_digest": sha("verification-receipt")}),
    )
    for offset, (phase, payload) in enumerate(phases, start=1):
        state = _apply(store, state, phase, payload, tick_base + offset)
    commit_event = _event(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "plan_not_execution": True,
            "plan_not_host_license": True,
            "source_identity_preserved": True,
            "activation_boundary": "mission_plan_phase_only",
            "non_authority": copy_non_authority(),
        },
        tick_base + 7,
    )
    result = store.apply(commit_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"], commit_event


def _new_plan_state(
    *,
    plan_id: str,
    wa_state: Mapping[str, Any],
    activation: Mapping[str, Any],
    budget: float = 2.0,
) -> dict[str, Any]:
    return build_initial_plan_state(
        plan_id=plan_id,
        source_wa_state=wa_state,
        replan_activation_receipt=activation,
        plan_budget=budget,
        maximum_step_risk=0.40,
        now_ms=60_000,
    )


def _validate_candidate_plan(
    root: Path,
) -> tuple[dict[str, Any], PlanStore, dict[str, Any]]:
    wa_state = _make_wa_source(
        root,
        "endorse-source",
        plural_route="CONSENSUS_CANDIDATE",
        wa_route="ENDORSE",
    )
    activation = _wa_activation(wa_state, "endorse")
    initial_state = _new_plan_state(
        plan_id="plan-candidate-001",
        wa_state=wa_state,
        activation=activation,
    )
    store = PlanStore(root / "candidate")
    state = store.initialize(initial_state)
    skipped = store.apply(
        _event(state, "order", {"dependency_receipt_digest": sha("skip")}, 1)
    )
    assert skipped["status"] == "REJECTED"
    assert "plan_event_phase_order_invalid" in skipped["errors"]
    state, commit_event = _complete_plan(store, state, _candidate_steps(), 10)
    assert state["route"] == "PLAN_CANDIDATE"
    assert state["topological_order"] == [
        "prepare",
        "act-candidate",
        "observe",
        "rollback",
        "verify",
    ]
    assert state["guard_summary"]["source_identity_preserved"] is True
    assert state["checkpoint_summary"]["all_effects_have_checkpoint"] is True
    assert state["verification_summary"]["plan_verified"] is True
    before_replay = store.ledger_commit_count()
    assert store.apply(commit_event)["status"] == "REPLAYED"
    assert store.ledger_commit_count() == before_replay
    return state, store, initial_state


def _validate_negative_cases(root: Path, initial_state: Mapping[str, Any]) -> None:
    cycle_store = PlanStore(root / "cycle-invalid")
    cycle_state = cycle_store.initialize(initial_state)
    cycle_state = _apply(
        cycle_store,
        cycle_state,
        "decompose",
        {
            "steps": [
                _step("a", "prepare", 1, depends_on=["b"]),
                _step("b", "verify", 1, depends_on=["a"]),
            ]
        },
        100,
    )
    cycle_result = cycle_store.apply(
        _event(
            cycle_state,
            "order",
            {"dependency_receipt_digest": sha("cycle")},
            101,
        )
    )
    assert cycle_result["status"] == "REJECTED"
    assert "plan_dependency_rank_not_lower" in cycle_result["errors"][0]

    budget_store = PlanStore(root / "budget-invalid")
    budget_state = budget_store.initialize(initial_state)
    budget_state = _apply(
        budget_store,
        budget_state,
        "decompose",
        {"steps": _candidate_steps(cost=0.50)},
        110,
    )
    budget_state = _apply(
        budget_store,
        budget_state,
        "order",
        {"dependency_receipt_digest": sha("budget-order")},
        111,
    )
    budget_result = budget_store.apply(
        _event(
            budget_state,
            "resource",
            {"resource_receipt_digest": sha("budget-resource")},
            112,
        )
    )
    assert budget_result["status"] == "REJECTED"
    assert budget_result["errors"] == ["plan_budget_exceeded"]

    guard_store = PlanStore(root / "guard-invalid")
    guard_state = guard_store.initialize(initial_state)
    unguarded = _candidate_steps()
    unguarded[1]["rollback_step_id"] = ""
    unguarded[1]["requires_external_license"] = False
    unguarded[1]["requires_human_review"] = False
    guard_state = _apply(
        guard_store, guard_state, "decompose", {"steps": unguarded}, 120
    )
    guard_state = _apply(
        guard_store,
        guard_state,
        "order",
        {"dependency_receipt_digest": sha("guard-order")},
        121,
    )
    guard_state = _apply(
        guard_store,
        guard_state,
        "resource",
        {"resource_receipt_digest": sha("guard-resource")},
        122,
    )
    guard_result = guard_store.apply(
        _event(
            guard_state,
            "guard",
            {"guard_receipt_digest": sha("guard-invalid")},
            123,
        )
    )
    assert guard_result["status"] == "REJECTED"
    assert guard_result["errors"] == ["plan_effect_guard_invalid"]


def _validate_routed_plan(
    root: Path,
    *,
    name: str,
    plural_route: str,
    wa_route: str,
    expected_plan_route: str,
    steps: Sequence[Mapping[str, Any]],
    appeals: Sequence[Mapping[str, Any]] = (),
    handover_required: bool = False,
    weak_dialogue: bool = False,
    tick_base: int,
) -> dict[str, Any]:
    wa_state = _make_wa_source(
        root,
        name,
        plural_route=plural_route,
        wa_route=wa_route,
        appeals=appeals,
        handover_required=handover_required,
        weak_dialogue=weak_dialogue,
    )
    activation = _wa_activation(wa_state, name)
    store = PlanStore(root / (name + "-plan"))
    state = store.initialize(
        _new_plan_state(
            plan_id=name + "-plan-state",
            wa_state=wa_state,
            activation=activation,
        )
    )
    state, _ = _complete_plan(store, state, steps, tick_base)
    assert state["route"] == expected_plan_route
    return state


def run_kernel() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v01-") as temporary:
        root = Path(temporary)
        candidate, candidate_store, initial_plan_state = _validate_candidate_plan(root)
        _validate_negative_cases(root, initial_plan_state)

        try:
            build_plan_phase_activation_receipt(
                state=candidate,
                mission_cycle_phase="replan",
                mission_cycle_state_digest=sha("mission-plan-state"),
                plan_phase_receipt_digest=sha("plan-phase-receipt"),
                now_ms=70_000,
            )
        except ValueError as exc:
            assert str(exc) == "mission_plan_phase_required"
        else:
            raise AssertionError("plan_activation_outside_plan_phase_was_accepted")

        plan_activation = build_plan_phase_activation_receipt(
            state=candidate,
            mission_cycle_phase="plan",
            mission_cycle_state_digest=sha("mission-plan-state"),
            plan_phase_receipt_digest=sha("plan-phase-receipt"),
            now_ms=70_001,
        )
        assert plan_activation["plan_not_execution"] is True
        assert plan_activation["host_license_granted"] is False
        assert plan_activation["memory_overwrite"] is False

        snapshot_path = root / "candidate" / "plan-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            candidate_store.recover(require_snapshot_match=True)
        except PlanStoreError as exc:
            assert str(exc) == "plan_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_plan_snapshot_was_accepted")
        repaired = candidate_store.repair_snapshot()
        recovered = candidate_store.recover(require_snapshot_match=True)
        assert repaired["plan_state_digest"] == recovered["plan_state_digest"]

        observation = _validate_routed_plan(
            root,
            name="observation",
            plural_route="APPEAL",
            wa_route="REOBSERVE",
            expected_plan_route="OBSERVATION_PLAN",
            appeals=[
                _appeal(
                    appeal_id="plan-observation-appeal",
                    stakeholder_id="patient",
                    target_option_id="option-a",
                    materiality=0.80,
                    protected=True,
                )
            ],
            steps=[
                _step("collect", "observe", 0),
                _step("verify-observation", "verify", 1, depends_on=["collect"]),
            ],
            tick_base=200,
        )
        repair = _validate_routed_plan(
            root,
            name="repair",
            plural_route="CONSENSUS_CANDIDATE",
            wa_route="REPAIR",
            expected_plan_route="REPAIR_PLAN",
            weak_dialogue=True,
            steps=[
                _step("repair-dialogue", "repair", 0),
                _step("observe-repair", "observe", 1, depends_on=["repair-dialogue"]),
            ],
            tick_base=300,
        )
        handover = _validate_routed_plan(
            root,
            name="handover",
            plural_route="HANDOVER",
            wa_route="ESCALATE",
            expected_plan_route="HANDOVER_PLAN",
            handover_required=True,
            steps=[
                _step("prepare-handover", "prepare", 0),
                _step("handover", "handover", 1, depends_on=["prepare-handover"]),
            ],
            tick_base=400,
        )
        assert not any(step["effectful"] for step in handover["steps"])

        return {
            "status": "PLAN_OS_REPLAN_BOUND_SYNTHESIS_V0_1_OK",
            "candidate_route": candidate["route"],
            "candidate_topological_order": candidate["topological_order"],
            "candidate_plan_digest": candidate["latest_committed_plan_digest"],
            "plan_activation_receipt_digest": plan_activation[
                "plan_activation_receipt_digest"
            ],
            "observation_route": observation["route"],
            "repair_route": repair["route"],
            "handover_route": handover["route"],
            "ledger_commits": candidate_store.ledger_commit_count(),
            "recovered_plan_state_digest": recovered["plan_state_digest"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
