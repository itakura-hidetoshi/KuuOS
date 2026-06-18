from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_kernel_v0_1 import (
    build_decision_event,
    build_initial_decision_state,
    build_replan_decision_activation_receipt,
)
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore, DecisionStoreError
from runtime.kuuos_decision_os_types_v0_1 import copy_non_authority


WEIGHTS = {
    "mission_alignment": 0.15,
    "expected_benefit": 0.20,
    "information_gain": 0.10,
    "recoverability": 0.10,
    "reversibility": 0.10,
    "stakeholder_fit": 0.10,
    "qi_process_compatibility": 0.05,
    "expected_harm": 0.08,
    "cost_burden": 0.05,
    "delay_risk": 0.04,
    "uncertainty_burden": 0.03,
}

THRESHOLDS = {
    "maximum_risk": 0.50,
    "minimum_recoverability": 0.50,
    "minimum_reversibility": 0.40,
    "dominance_margin": 0.05,
    "observe_width": 0.45,
    "experiment_information_gain": 0.70,
    "experiment_maximum_risk": 0.35,
    "experiment_minimum_recoverability": 0.70,
    "middle_way_maximum_risk": 0.40,
}


def _interval(lower: float, upper: float) -> dict[str, float]:
    return {"lower": lower, "upper": upper}


def _option(
    *,
    option_id: str,
    action_class: str,
    positive: tuple[float, float],
    negative: tuple[float, float],
    information_gain: tuple[float, float] | None = None,
    mission_allowed: bool = True,
    prohibited: bool = False,
    authority_claimed: bool = False,
    estimated_cost: float = 0.20,
    estimated_risk: float = 0.20,
    recoverability: float = 0.85,
    reversibility: float = 0.85,
    requires_human_review: bool = False,
    required_evidence: Sequence[str] = (),
    available_evidence: Sequence[str] = (),
) -> dict[str, Any]:
    info = information_gain or positive
    dimensions = {
        "mission_alignment": _interval(*positive),
        "expected_benefit": _interval(*positive),
        "information_gain": _interval(*info),
        "recoverability": _interval(recoverability, min(1.0, recoverability + 0.05)),
        "reversibility": _interval(reversibility, min(1.0, reversibility + 0.05)),
        "stakeholder_fit": _interval(*positive),
        "qi_process_compatibility": _interval(*positive),
        "expected_harm": _interval(*negative),
        "cost_burden": _interval(*negative),
        "delay_risk": _interval(*negative),
        "uncertainty_burden": _interval(*negative),
    }
    return {
        "option_id": option_id,
        "description_digest": sha({"option_id": option_id, "description": "fixture"}),
        "action_class": action_class,
        "requires_external_license": action_class in {"experiment", "exploit", "local_action"},
        "requires_human_review": requires_human_review,
        "mission_allowed": mission_allowed,
        "prohibited": prohibited,
        "authority_claimed": authority_claimed,
        "estimated_cost": estimated_cost,
        "estimated_risk": estimated_risk,
        "recoverability": recoverability,
        "reversibility": reversibility,
        "required_evidence_digests": list(required_evidence),
        "available_evidence_digests": list(available_evidence),
        "supporting_evidence_digests": [sha("support-" + option_id)],
        "opposing_evidence_digests": [sha("oppose-" + option_id)],
        "stakeholder_digests": [sha("stakeholder-" + option_id)],
        "dimensions": dimensions,
    }


def _event(
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    return build_decision_event(
        state=state,
        target_phase=target_phase,
        artifact_digest=sha(
            {"target_phase": target_phase, "payload": dict(payload), "tick": tick}
        ),
        payload=payload,
        now_ms=1_000 + tick,
    )


def _apply(
    store: DecisionStore,
    state: Mapping[str, Any],
    target_phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    result = store.apply(_event(state, target_phase, payload, tick))
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    return result["state"]


def _initial(decision_id: str, now_ms: int = 1_000) -> dict[str, Any]:
    return build_initial_decision_state(
        decision_id=decision_id,
        lineage_id="decision-lineage-001",
        mission_contract_digest=sha("mission-contract-v020"),
        mission_state_digest=sha("mission-state-v020"),
        source_belief_receipt_digest=sha("belief-gerbe-receipt-v03"),
        decision_context_digest=sha({"context": "local-deliberation"}),
        decision_budget=1.0,
        weights=WEIGHTS,
        thresholds=THRESHOLDS,
        now_ms=now_ms,
    )


def _complete_cycle(
    store: DecisionStore,
    state: Mapping[str, Any],
    *,
    options: Sequence[Mapping[str, Any]],
    challenge: Mapping[str, Any],
    middle_way: Mapping[str, Any],
    tick_base: int,
    requested_route: str | None = None,
    test_forbidden_qi: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = _apply(
        store,
        state,
        "generate",
        {
            "options": list(options),
            "advisory_receipt_digests": [
                sha("policy-v09"),
                sha("regret-v010"),
                sha("horizon-v012"),
            ],
        },
        tick_base + 1,
    )
    state = _apply(
        store,
        state,
        "constrain",
        {"constraint_receipt_digest": sha("constraint-receipt")},
        tick_base + 2,
    )
    state = _apply(
        store,
        state,
        "evaluate",
        {"evaluation_receipt_digest": sha("evaluation-receipt")},
        tick_base + 3,
    )
    state = _apply(store, state, "challenge", challenge, tick_base + 4)

    if test_forbidden_qi:
        forbidden = store.apply(
            _event(
                state,
                "qi_condition",
                {
                    "process_tensor_digest": sha("qi-process"),
                    "history_window_digest": sha("qi-history"),
                    "roles": ["execution_license"],
                    "flow_phase": "decision-transition",
                    "authority_source": False,
                },
                tick_base + 5,
            )
        )
        assert forbidden["status"] == "REJECTED"
        assert "decision_qi_forbidden_role" in forbidden["errors"]

    state = _apply(
        store,
        state,
        "qi_condition",
        {
            "process_tensor_digest": sha("qi-process"),
            "history_window_digest": sha("qi-history"),
            "roles": [
                "temporal_transition_context",
                "reversibility_context",
                "uncertainty_context",
            ],
            "flow_phase": "decision-transition",
            "authority_source": False,
        },
        tick_base + 6,
    )
    state = _apply(
        store,
        state,
        "two_truths_check",
        {
            "two_truths": {
                "samvrti_decision_usable": True,
                "paramartha_non_reified": True,
                "selected_option_not_absolute": True,
                "two_truths_separated": True,
            }
        },
        tick_base + 7,
    )
    state = _apply(
        store,
        state,
        "middle_way_gate",
        {"middle_way": dict(middle_way)},
        tick_base + 8,
    )
    decide_payload: dict[str, Any] = {
        "decision_rule_digest": sha("robust-interval-partial-order")
    }
    if requested_route is not None:
        decide_payload["requested_route"] = requested_route
    state = _apply(store, state, "decide", decide_payload, tick_base + 9)
    commit_event = _event(
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "decision_not_execution": True,
            "activation_boundary": "mission_replan_only",
            "non_authority": copy_non_authority(),
        },
        tick_base + 10,
    )
    commit_result = store.apply(commit_event)
    if commit_result.get("status") != "APPLIED":
        raise AssertionError(commit_result)
    return commit_result["state"], commit_event


def _challenge(
    *,
    missing: Sequence[str] = (),
    catastrophic: bool = False,
    normative: bool = False,
) -> dict[str, Any]:
    return {
        "counterargument_digests": [sha("counterargument")],
        "missing_evidence_digests": list(missing),
        "stakeholder_objection_digests": [sha("stakeholder-objection")],
        "alternative_option_ids": [],
        "counterfactual_receipt_digests": [sha("counterfactual-v010")],
        "catastrophic_risk_detected": catastrophic,
        "unresolved_normative_conflict": normative,
    }


def _middle(
    *,
    reification: float = 0.10,
    nihilism: float = 0.10,
    closure: float = 0.10,
    abandonment: float = 0.10,
    exclusion: float = 0.10,
    irreversibility: float = 0.10,
    repairability: float = 0.90,
) -> dict[str, float]:
    return {
        "reification_risk": reification,
        "nihilistic_erasure_risk": nihilism,
        "premature_closure_risk": closure,
        "responsibility_abandonment_risk": abandonment,
        "stakeholder_exclusion_risk": exclusion,
        "irreversibility_risk": irreversibility,
        "repairability": repairability,
    }


def run_kernel() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="kuuos-decision-v01-") as tmp:
        store = DecisionStore(Path(tmp) / "select")
        state = store.initialize(_initial("decision-select-001"))

        skipped = store.apply(
            _event(
                state,
                "evaluate",
                {"evaluation_receipt_digest": sha("invalid-skip")},
                1,
            )
        )
        assert skipped["status"] == "REJECTED"
        assert "decision_event_phase_order_invalid" in skipped["errors"]
        assert store.ledger_commit_count() == 0

        evidence = sha("required-evidence")
        select_options = [
            _option(
                option_id="option-a",
                action_class="exploit",
                positive=(0.86, 0.94),
                negative=(0.04, 0.10),
                information_gain=(0.30, 0.45),
                required_evidence=[evidence],
                available_evidence=[evidence],
            ),
            _option(
                option_id="option-b",
                action_class="observe",
                positive=(0.38, 0.52),
                negative=(0.28, 0.38),
                information_gain=(0.45, 0.58),
            ),
            _option(
                option_id="option-c",
                action_class="local_action",
                positive=(0.90, 0.96),
                negative=(0.02, 0.06),
                prohibited=True,
            ),
        ]
        state, commit_event = _complete_cycle(
            store,
            state,
            options=select_options,
            challenge=_challenge(),
            middle_way=_middle(),
            tick_base=10,
            requested_route="SELECT_CANDIDATE",
            test_forbidden_qi=True,
        )
        assert state["route"] == "SELECT_CANDIDATE"
        assert state["selected_option_id"] == "option-a"
        assert state["admissible_option_ids"] == ["option-a", "option-b"]
        assert state["retained_alternative_ids"] == ["option-b"]
        assert state["excluded_options"][0]["option_id"] == "option-c"
        assert state["pending_replan_activation"] is True
        assert state["decision_version"] == 1
        assert state["latest_committed_decision_digest"]

        commits_before_replay = store.ledger_commit_count()
        replay = store.apply(commit_event)
        assert replay["status"] == "REPLAYED"
        assert store.ledger_commit_count() == commits_before_replay

        try:
            build_replan_decision_activation_receipt(
                state=state,
                mission_cycle_phase="learn",
                mission_cycle_state_digest=sha("mission-cycle-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=3_000,
            )
        except ValueError as exc:
            assert str(exc) == "mission_replan_required"
        else:
            raise AssertionError("decision_activation_without_replan_was_accepted")

        activation = build_replan_decision_activation_receipt(
            state=state,
            mission_cycle_phase="replan",
            mission_cycle_state_digest=sha("mission-cycle-state"),
            replan_receipt_digest=sha("replan-receipt"),
            next_plan_basis_digest=sha("next-plan-basis"),
            now_ms=3_001,
        )
        assert activation["decision_not_execution"] is True
        assert activation["host_license_granted"] is False
        assert activation["memory_overwrite"] is False

        snapshot_path = Path(tmp) / "select" / "decision-snapshot.json"
        snapshot_path.write_text(json.dumps({"corrupt": True}), encoding="utf-8")
        try:
            store.recover(require_snapshot_match=True)
        except DecisionStoreError as exc:
            assert str(exc) == "decision_snapshot_ledger_mismatch"
        else:
            raise AssertionError("corrupt_decision_snapshot_was_accepted")
        repaired = store.repair_snapshot()
        recovered = store.recover(require_snapshot_match=True)
        assert repaired["decision_state_digest"] == recovered[
            "decision_state_digest"
        ]

        experiment_store = DecisionStore(Path(tmp) / "experiment")
        experiment_state = experiment_store.initialize(
            _initial("decision-experiment-001")
        )
        experiment_options = [
            _option(
                option_id="experiment-a",
                action_class="experiment",
                positive=(0.60, 0.70),
                negative=(0.18, 0.25),
                information_gain=(0.82, 0.92),
                estimated_risk=0.25,
                recoverability=0.88,
                reversibility=0.90,
            ),
            _option(
                option_id="exploit-b",
                action_class="exploit",
                positive=(0.58, 0.69),
                negative=(0.17, 0.24),
                information_gain=(0.20, 0.35),
            ),
        ]
        experiment_state, _ = _complete_cycle(
            experiment_store,
            experiment_state,
            options=experiment_options,
            challenge=_challenge(),
            middle_way=_middle(),
            tick_base=100,
            requested_route="EXPERIMENT_RECOMMENDED",
        )
        assert experiment_state["route"] == "EXPERIMENT_RECOMMENDED"
        assert experiment_state["selected_option_id"] == ""
        assert experiment_state["recommended_option_ids"] == ["experiment-a"]

        observe_store = DecisionStore(Path(tmp) / "observe")
        observe_state = observe_store.initialize(_initial("decision-observe-001"))
        observe_state, _ = _complete_cycle(
            observe_store,
            observe_state,
            options=experiment_options,
            challenge=_challenge(missing=[sha("missing-evidence")]),
            middle_way=_middle(),
            tick_base=200,
            requested_route="OBSERVE",
        )
        assert observe_state["route"] == "OBSERVE"

        escalate_store = DecisionStore(Path(tmp) / "escalate")
        escalate_state = escalate_store.initialize(
            _initial("decision-escalate-001")
        )
        escalate_state, _ = _complete_cycle(
            escalate_store,
            escalate_state,
            options=experiment_options,
            challenge=_challenge(catastrophic=True),
            middle_way=_middle(),
            tick_base=300,
            requested_route="ESCALATE",
        )
        assert escalate_state["route"] == "ESCALATE"

        reject_store = DecisionStore(Path(tmp) / "reject")
        reject_state = reject_store.initialize(_initial("decision-reject-001"))
        reject_options = [
            _option(
                option_id="forbidden-option",
                action_class="local_action",
                positive=(0.80, 0.90),
                negative=(0.05, 0.10),
                prohibited=True,
            ),
            _option(
                option_id="authority-option",
                action_class="local_action",
                positive=(0.80, 0.90),
                negative=(0.05, 0.10),
                authority_claimed=True,
            ),
        ]
        reject_state, _ = _complete_cycle(
            reject_store,
            reject_state,
            options=reject_options,
            challenge=_challenge(),
            middle_way=_middle(),
            tick_base=400,
            requested_route="REJECT",
        )
        assert reject_state["route"] == "REJECT"
        assert reject_state["pending_replan_activation"] is False
        try:
            build_replan_decision_activation_receipt(
                state=reject_state,
                mission_cycle_phase="replan",
                mission_cycle_state_digest=sha("mission-cycle-state"),
                replan_receipt_digest=sha("replan-receipt"),
                next_plan_basis_digest=sha("next-plan-basis"),
                now_ms=5_000,
            )
        except ValueError as exc:
            assert str(exc) == "decision_not_pending_activation"
        else:
            raise AssertionError("rejected_decision_was_activated")

        return {
            "status": "DECISION_OS_RELATIONAL_DELIBERATION_V0_1_OK",
            "selected_route": state["route"],
            "selected_option_id": state["selected_option_id"],
            "retained_alternative_ids": state["retained_alternative_ids"],
            "decision_state_digest": recovered["decision_state_digest"],
            "committed_decision_digest": recovered[
                "latest_committed_decision_digest"
            ],
            "activation_receipt_digest": activation[
                "decision_activation_receipt_digest"
            ],
            "ledger_commits": store.ledger_commit_count(),
            "experiment_route": experiment_state["route"],
            "observe_route": observe_state["route"],
            "escalate_route": escalate_state["route"],
            "reject_route": reject_state["route"],
        }


if __name__ == "__main__":
    print(json.dumps(run_kernel(), ensure_ascii=False, sort_keys=True))
