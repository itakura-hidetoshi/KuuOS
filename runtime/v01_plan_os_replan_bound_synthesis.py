from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_replan_wa_activation_receipt,
)
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_initial_plan_state,
    build_plan_event,
    build_plan_phase_activation_receipt,
)
from runtime.kuuos_plan_os_store_v0_1 import PlanStore, PlanStoreError
from runtime.kuuos_plan_os_types_v0_1 import copy_non_authority
from runtime.v03_decision_os_wa_relational_harmony import (
    _complete_wa_cycle,
    _initial_wa,
    _plural_source,
    _profile,
    _standard_profiles,
)


def _wa_source(
    root: Path,
    name: str,
    *,
    source_plural_route: str,
    wa_route: str,
    weak_dialogue: bool = False,
    handover_required: bool = False,
) -> dict[str, Any]:
    plural = _plural_source(
        root,
        name + "-plural",
        requested_route=source_plural_route,
        handover_required=handover_required,
    )
    store_root = root / (name + "-wa")
    from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore

    store = WaDecisionStore(store_root)
    state = store.initialize(_initial_wa(plural, name + "-wa-state"))
    profiles = _standard_profiles(plural)
    if weak_dialogue:
        profiles[0] = _profile(
            plural,
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
    *,
    step_id: str,
    step_class: str,
    rank: int,
    depends_on: Sequence[str] = (),
    cost: float = 0.10,
    risk: float = 0.10,
    reversibility: float = 0.90,
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
        "verification_criterion_digest": sha("verify-" + step_id),
        "estimated_cost": cost,
        "estimated_risk": risk,
        "reversibility": reversibility,
        "rollback_step_id": rollback_step_id,
        "stop_condition_digests": list(stop_conditions),
        "requires_external_license": external,
        "requires_human_review": human,
        "effectful": effectful,
        "source_option_id": source_option_id,
        "stakeholder_scope_digests": [sha("stakeholder-scope-" + step_id)],
    }


def _candidate_steps() -> list[dict[str, Any]]:
    return [
        _step(step_id="prepare", step_class="prepare", rank=0),
        _step(
            step_id="act-candidate",
            step_class="act_candidate",
            rank=1,
            depends_on=["prepare"],
            rollback_step_id="rollback",
            effectful=True,
            external=True,
            human=True,
            stop_conditions=[sha("stop-risk"), sha("stop-dissent")],
        ),
        _step(
            step_id="rollback",
            step_class="repair",
            rank=2,
            depends_on=["act-candidate"],
            source_option_id="option-a",
        ),
        _step(
            step_id="observe",
            step_class="observe",
            rank=2,
            depends_on=["act-candidate"],
        ),
        _step(
            step_id="verify",
            step_class="verify",
            rank=3,
            depends_on=["observe"],
        ),
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
    *,
    steps: Sequence[Mapping[str, Any]],
    tick_base: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = _apply(store, state, "decompose", {"steps": list(steps)}, tick_base + 1)
    state = _apply(
        store,
        state,
        "order",
        {"dependency_receipt_digest": sha("dependency-receipt")},
        tick_base + 2,
    )
    state = _apply(
        store,
        state,
        "resource",
        {"resource_receipt_digest": sha("resource-receipt")},
        tick_base + 3,
    )
    state = _apply(
        store,
        state,
        "guard",
        {"guard_receipt_digest": sha("guard-receipt")},
        tick_base + 4,
    )
    state = _apply(
        store,
        state,
        "checkpoint",
        {"checkpoint_receipt_digest": sha("checkpoint-receipt")},
        tick_base + 5,
    )
    state = _apply(
        store,
        state,
        "verify",
        {"verification_receipt_digest": sha("verification-receipt")},
        tick_base + 6,
    )
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


def _initial_plan(
    *,
    plan_id: str,
    wa_state: Mapping[str, Any],
    activation: Mapping[str, Any],
    budget: float = 2.0,
    max_risk: float = 0.40,
) -> dict[str, Any]:
    return build_initial_plan_state(
        plan_id=plan_id,
        source_wa_state=wa_state,
        replan_activation_receipt=activation,
        plan_budget=budget,
        maximum_step_risk=max_risk,
        now_ms=60_000,
    )


def run_kernel() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kuuos-plan-os-v01-") as temporary:
        root = Path(temporary)
        endorse_wa = _wa_source(
            root,
            "endorse-source",
            source_plural_route="CONSENSUS_CANDIDATE",
            wa_route="ENDORSE",
        )
        endorse_activation = _wa_activation(endorse_wa, "endorse")
        store = PlanStore(root / "candidate")
        state = store.initialize(
            _initial_plan(
                plan_id="plan-candidate-001",
                wa_state=endorse_wa,
                activation=endorse_activation,
            )
        )
        assert state["route"] == "PLAN_CANDIDATE"

        skipped = store.apply(
            _event(
                state,
                "order",
                {"dependency_receipt_digest": sha("skip")},
                1,
            )
        )
        assert skipped["status"] == "REJECTED"
        assert "plan_event_phase_order_invalid" in skipped["errors"]
        assert store.ledger_commit_count() == 0

        state, commit_event = _complete_plan(
            store,
            state,
            steps=_candidate_steps(),
            tick_base=10,
        )
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
        assert state["pending_plan_phase_activation"] is True

        before_replay = store.ledger_commit_count()
        replay = store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == before_replay

        try:
            build_plan_phase_activation_receipt(
                state=state,
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
            state=state,
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
            store.recover(require_snapshot_match=True)
        except PlanStoreError as exc:
            assert str(exc) == "plan_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_plan_snapshot_was_accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["plan_state_digest"] == recovered["plan_state_digest"]

        cycle_store = PlanStore(root / "cycle-invalid")
        cycle_state = cycle_store.initialize(
            _initial_plan(
                plan_id="plan-cycle-invalid",
                wa_state=endorse_wa,
                activation=endorse_activation,
            )
        )
        cycle_steps = [
            _step(
                step_id="a",
                step_class="prepare",
                rank=1,
                depends_on=["b"],
            ),
            _step(
                step_id="b",
                step_class="verify",
                rank=1,
                depends_on=["a"],
            ),
        ]
        cycle_state = _apply(
            cycle_store,
            cycle_state,
            "decompose",
            {"steps": cycle_steps},
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
        budget_state = budget_store.initialize(
            _initial_plan(
                plan_id="plan-budget-invalid",
                wa_state=endorse_wa,
                activation=endorse_activation,
                budget=0.20,
            )
        )
        budget_state = _apply(
            budget_store,
            budget_state,
            "decompose",
            {"steps": _candidate_steps()},
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
        guard_state = guard_store.initialize(
            _initial_plan(
                plan_id="plan-guard-invalid",
                wa_state=endorse_wa,
                activation=endorse_activation,
            )
        )
        unguarded = _candidate_steps()
        unguarded[1]["rollback_step_id"] = ""
        unguarded[1]["requires_external_license"] = False
        unguarded[1]["requires_human_review"] = False
        guard_state = _apply(
            guard_store,
            guard_state,
            "decompose",
            {"steps": unguarded},
            120,
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

        observe_wa = _wa_source(
            root,
            "observe-source",
            source_plural_route="APPEAL",
            wa_route="REOBSERVE",
        )
        observe_activation = _wa_activation(observe_wa, "observe")
        observe_store = PlanStore(root / "observe")
        observe_state = observe_store.initialize(
            _initial_plan(
                plan_id="plan-observe-001",
                wa_state=observe_wa,
                activation=observe_activation,
            )
        )
        observe_steps = [
            _step(
                step_id="collect",
                step_class="observe",
                rank=0,
                source_option_id="option-a",
            ),
            _step(
                step_id="verify-observation",
                step_class="verify",
                rank=1,
                depends_on=["collect"],
                source_option_id="option-a",
            ),
        ]
        observe_state, _ = _complete_plan(
            observe_store,
            observe_state,
            steps=observe_steps,
            tick_base=200,
        )
        assert observe_state["route"] == "OBSERVATION_PLAN"

        repair_wa = _wa_source(
            root,
            "repair-source",
            source_plural_route="CONSENSUS_CANDIDATE",
            wa_route="REPAIR",
            weak_dialogue=True,
        )
        repair_activation = _wa_activation(repair_wa, "repair")
        repair_store = PlanStore(root / "repair")
        repair_state = repair_store.initialize(
            _initial_plan(
                plan_id="plan-repair-001",
                wa_state=repair_wa,
                activation=repair_activation,
            )
        )
        repair_steps = [
            _step(step_id="repair-dialogue", step_class="repair", rank=0),
            _step(
                step_id="observe-repair",
                step_class="observe",
                rank=1,
                depends_on=["repair-dialogue"],
            ),
        ]
        repair_state, _ = _complete_plan(
            repair_store,
            repair_state,
            steps=repair_steps,
            tick_base=300,
        )
        assert repair_state["route"] == "REPAIR_PLAN"

        handover_wa = _wa_source(
            root,
            "handover-source",
            source_plural_route="HANDOVER",
            wa_route="ESCALATE",
            handover_required=True,
        )
        handover_activation = _wa_activation(handover_wa, "handover")
        handover_store = PlanStore(root / "handover")
        handover_state = handover_store.initialize(
            _initial_plan(
                plan_id="plan-handover-001",
                wa_state=handover_wa,
                activation=handover_activation,
            )
        )
        handover_steps = [
            _step(step_id="prepare-handover", step_class="prepare", rank=0),
            _step(
                step_id="handover",
                step_class="handover",
                rank=1,
                depends_on=["prepare-handover"],
            ),
        ]
        handover_state, _ = _complete_plan(
            handover_store,
            handover_state,
            steps=handover_steps,
            tick_base=400,
        )
        assert handover_state["route"] == "HANDOVER_PLAN"
        assert not any(step["effectful"] for step in handover_state["steps"])

        return {
            "status": "PLAN_OS_REPLAN_BOUND_SYNTHESIS_V0_1_OK",
            "candidate_route": state["route"],
            "candidate_topological_order": state["topological_order"],
            "candidate_plan_digest": state["latest_committed_plan_digest"],
            "plan_activation_receipt_digest": plan_activation[
                "plan_activation_receipt_digest"
            ],
            "observation_route": observe_state["route"],
            "repair_route": repair_state["route"],
            "handover_route": handover_state["route"],
            "ledger_commits": store.ledger_commit_count(),
            "recovered_plan_state_digest": recovered["plan_state_digest"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
