from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from runtime.kuuos_nonmarkov_cognitive_loop_kernel_v0_23 import (
    build_nonmarkov_cognitive_episode,
    episode_digest,
    validate_nonmarkov_cognitive_episode,
)
from runtime.kuuos_nonmarkov_cognitive_loop_store_v0_23 import (
    initialize_store,
    persist_episode,
    recover_store,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_verification_receipt,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _assessment,
    _build_plan,
    _fixture,
    _observation,
    _ready_belief_state,
)


def _process_packet() -> dict[str, Any]:
    path = Path("examples/physical_quantum_qi_process_tensor_packet_v0_2F.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _success_receipt(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    belief: dict[str, Any],
    goal: dict[str, Any],
    portfolio: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    observations = [
        _observation(
            contract,
            mission_state,
            "v023-observe-output",
            "v023-plan-output-confirmed",
            "Expected observation artifacts were independently inspected",
            "supports",
            "v023-independent-observer-1",
            31,
        ),
        _observation(
            contract,
            mission_state,
            "v023-observe-goal",
            "v023-goal-confirmed",
            "The bounded cognitive goal was independently confirmed",
            "supports",
            "v023-independent-observer-2",
            32,
        ),
    ]
    return build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verifier_id="v023-independent-verifier",
        independent_observations=observations,
        criterion_assessments=[
            _assessment(
                contract["success_criteria"][0],
                "satisfied",
                observations[0],
                0.95,
            ),
            _assessment(
                contract["success_criteria"][1],
                "satisfied",
                observations[1],
                0.94,
            ),
        ],
        execution_receipt_digests=[],
        observed_at_ms=33,
    )


def _failed_receipt(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    belief: dict[str, Any],
    goal: dict[str, Any],
    portfolio: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    observation = _observation(
        contract,
        mission_state,
        "v023-observe-counterevidence",
        "v023-goal-counterevidence",
        "Independent checking found counterevidence",
        "supports",
        "v023-falsification-observer",
        41,
    )
    return build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verifier_id="v023-falsification-verifier",
        independent_observations=[observation],
        criterion_assessments=[
            _assessment(
                contract["success_criteria"][0],
                "satisfied",
                observation,
                0.90,
            ),
            _assessment(
                contract["success_criteria"][1],
                "contradicted",
                observation,
                0.92,
            ),
        ],
        execution_receipt_digests=[],
        observed_at_ms=42,
    )


def _indeterminate_receipt(
    contract: dict[str, Any],
    mission_state: dict[str, Any],
    belief: dict[str, Any],
    goal: dict[str, Any],
    portfolio: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    return build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verifier_id="v023-indeterminate-verifier",
        independent_observations=[],
        criterion_assessments=[
            _assessment(item, "unknown", None, 0.0)
            for item in contract["success_criteria"]
        ],
        execution_receipt_digests=[],
        observed_at_ms=51,
    )


def _all_expected_labels(plan: dict[str, Any]) -> list[str]:
    return sorted(
        {
            str(label)
            for step in plan["steps"]
            for label in step["expected_observations"]
        }
    )


def run_nonmarkov_cognitive_loop_scenarios() -> dict[str, Any]:
    contract, mission_state, goal, portfolio = _fixture()
    belief = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, belief, goal, portfolio)
    process_packet = _process_packet()

    success = _success_receipt(
        contract, mission_state, belief, goal, portfolio, plan
    )
    episode_one = build_nonmarkov_cognitive_episode(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verification_receipt=success,
        qi_process_tensor_packet=process_packet,
        prior_memory_entries=[],
        actual_observation_labels=_all_expected_labels(plan),
        step_outcomes=[
            {
                "step_id": step["step_id"],
                "outcome": "succeeded",
                "evidence_refs": [success["verification_receipt_digest"]],
            }
            for step in plan["steps"]
        ],
        coherence_defect=0.1,
        cycle_index=1,
        created_at_ms=60,
    )
    assert episode_one["verification_route"] == "passed"
    assert episode_one["observation_route"] == "matched"
    assert episode_one["plan_route"] == "complete_candidate"
    assert episode_one["memory_mode"] == "cold_start_or_history_gap"
    assert episode_one["handoff"]["strategy_learning"]["future_only"] is True

    memory_entry = episode_one["handoff"]["memoryos"]["append_writeback_receipt"]
    failed = _failed_receipt(
        contract, mission_state, belief, goal, portfolio, plan
    )
    episode_two = build_nonmarkov_cognitive_episode(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verification_receipt=failed,
        qi_process_tensor_packet=process_packet,
        prior_memory_entries=[memory_entry],
        actual_observation_labels=["bounded_basis_report"],
        step_outcomes=[
            {
                "step_id": plan["steps"][0]["step_id"],
                "outcome": "succeeded",
                "evidence_refs": [failed["verification_receipt_digest"]],
            },
            {
                "step_id": plan["steps"][1]["step_id"],
                "outcome": "failed",
                "evidence_refs": [failed["verification_receipt_digest"]],
            },
        ],
        coherence_defect=0.25,
        cycle_index=2,
        created_at_ms=70,
    )
    assert episode_two["verification_route"] == "failed"
    assert episode_two["observation_route"] == "conflicted"
    assert episode_two["plan_route"] == "replan"
    assert episode_two["memory_mode"] == "history_replay_ready"
    assert (
        episode_two["handoff"]["strategy_learning"]["aggregate_bounded_credit"]
        < 0.5
    )

    indeterminate = _indeterminate_receipt(
        contract, mission_state, belief, goal, portfolio, plan
    )
    episode_three = build_nonmarkov_cognitive_episode(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verification_receipt=indeterminate,
        qi_process_tensor_packet=process_packet,
        prior_memory_entries=[memory_entry],
        actual_observation_labels=[],
        step_outcomes=[
            {
                "step_id": step["step_id"],
                "outcome": "not_observed",
                "evidence_refs": [],
            }
            for step in plan["steps"]
        ],
        coherence_defect=0.4,
        cycle_index=3,
        created_at_ms=80,
    )
    assert episode_three["verification_route"] == "indeterminate"
    assert episode_three["plan_route"] == "reobserve"
    assert episode_three["missing_expected_observation_labels"]

    rerotation = build_nonmarkov_cognitive_episode(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verification_receipt=indeterminate,
        qi_process_tensor_packet=process_packet,
        prior_memory_entries=[memory_entry],
        actual_observation_labels=[],
        step_outcomes=[],
        coherence_defect=0.4,
        cycle_index=4,
        created_at_ms=90,
        suspension_context={
            "suspended": True,
            "recovery_route": "rerotate_required",
        },
    )
    assert rerotation["plan_route"] == "rerotate_required"
    assert rerotation["handoff"]["planos"]["old_session_closed"] is True
    assert rerotation["handoff"]["planos"]["new_lineage_required"] is True
    assert rerotation["handoff"]["planos"]["execution_granted"] is False

    with TemporaryDirectory(prefix="kuuos-nonmarkov-v023-") as directory:
        initialize_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            chart_id=belief["chart_id"],
            now_ms=59,
        )
        first = persist_episode(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            episode=episode_one,
        )
        replay = persist_episode(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            episode=episode_one,
        )
        second = persist_episode(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
            episode=episode_two,
        )
        assert first["status"] == "APPLIED"
        assert replay["status"] == "REPLAYED"
        assert second["status"] == "APPLIED"
        recovered = recover_store(
            store_dir=directory,
            contract=contract,
            mission_state=mission_state,
        )
        assert recovered["revision"] == 2
        assert recovered["append_only"] is True
        assert recovered["memory_overwrite"] is False

    tampered = deepcopy(episode_one)
    tampered["non_authority"]["grants_execution_authority"] = True
    tampered["cognitive_episode_digest"] = episode_digest(tampered)
    assert "episode_non_authority_invalid" in validate_nonmarkov_cognitive_episode(
        tampered
    )

    return {
        "status": "KUUOS_NONMARKOV_COGNITIVE_LOOP_V0_23_OK",
        "passed_route": episode_one["plan_route"],
        "failed_route": episode_two["plan_route"],
        "indeterminate_route": episode_three["plan_route"],
        "rerotation_route": rerotation["plan_route"],
        "history_replay_ready": episode_two["memory_mode"]
        == "history_replay_ready",
        "belief_plurality_preserved": episode_one["handoff"]["beliefos"][
            "plurality_preserved"
        ],
        "observation_not_verification": episode_one["handoff"]["observeos"][
            "observation_not_verification"
        ],
        "verification_not_truth": episode_one["handoff"]["verifyos"][
            "verification_not_truth"
        ],
        "learning_future_only": episode_one["handoff"]["strategy_learning"][
            "future_only"
        ],
        "memory_append_only": episode_one["handoff"]["memoryos"]["append_only"],
        "execution_authority_granted": False,
    }


__all__ = [
    "_all_expected_labels",
    "_failed_receipt",
    "_indeterminate_receipt",
    "_process_packet",
    "_success_receipt",
    "run_nonmarkov_cognitive_loop_scenarios",
]
