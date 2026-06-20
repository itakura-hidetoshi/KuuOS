from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_mission_contract_types_v0_20 import sha
from runtime.kuuos_os_qi_cognitive_integration_v0_23 import (
    NON_AUTHORITY,
    build_cognitive_memory_packet,
    build_os_qi_cognitive_cycle,
    receipt_digest,
    validate_os_qi_cognitive_cycle,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_verification_receipt,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _observation,
    _ready_belief_state,
)


def _os_packet(
    *,
    owner: str,
    mission_id: str,
    chart_id: str,
    digest_field: str,
    body: dict[str, Any],
) -> dict[str, Any]:
    packet = {
        "owner": owner,
        "mission_id": mission_id,
        "chart_id": chart_id,
        **deepcopy(body),
        "non_authority": deepcopy(NON_AUTHORITY),
    }
    packet[digest_field] = sha({k: v for k, v in packet.items() if k != digest_field})
    return packet


def _verified_fixture() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    contract, mission_state, goal, portfolio = _fixture()
    belief = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, belief, goal, portfolio)
    observations = [
        _observation(
            contract,
            mission_state,
            "verify-v023-output",
            "v023-output-confirmed",
            "Expected observations are present",
            "supports",
            "verifyos-independent-observer-1",
            31,
        ),
        _observation(
            contract,
            mission_state,
            "verify-v023-goal",
            "v023-goal-confirmed",
            "The bounded goal is independently confirmed",
            "supports",
            "verifyos-independent-observer-2",
            32,
        ),
    ]
    verification = build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=belief,
        goal=goal,
        goal_portfolio=portfolio,
        plan=plan,
        verifier_id="VerifyOS-v023",
        independent_observations=observations,
        criterion_assessments=[
            {
                "criterion": contract["success_criteria"][0],
                "status": "satisfied",
                "confidence": 0.95,
                "evidence_observation_digests": [observations[0]["observation_digest"]],
                "notes": "VerifyOS independently observed expected output",
            },
            {
                "criterion": contract["success_criteria"][1],
                "status": "satisfied",
                "confidence": 0.94,
                "evidence_observation_digests": [observations[1]["observation_digest"]],
                "notes": "VerifyOS independently confirmed the goal",
            },
        ],
        execution_receipt_digests=[],
        observed_at_ms=33,
    )
    return contract, mission_state, goal, portfolio, plan, verification


def _process_history() -> list[dict[str, Any]]:
    return [
        {
            "cycle_index": 0,
            "os_owner": "ObserveOS",
            "process_observation": "repository basis observed",
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": False,
        },
        {
            "cycle_index": 1,
            "os_owner": "BeliefOS",
            "process_observation": "context-local belief updated",
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "cycle_index": 2,
            "os_owner": "PlanOS",
            "process_action": "bounded plan proposed",
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "cycle_index": 3,
            "os_owner": "VerifyOS",
            "process_observation": "independent verification completed",
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
    ]


def run_os_qi_cognitive_integration_scenarios() -> dict[str, Any]:
    contract, mission_state, _, _, plan, verification = _verified_fixture()
    mission_id = contract["mission_id"]
    chart_id = "github-main"

    observe = _os_packet(
        owner="ObserveOS",
        mission_id=mission_id,
        chart_id=chart_id,
        digest_field="observation_receipt_digest",
        body={
            "observation_grounded": True,
            "effect_grounded": True,
            "observation_is_truth": False,
        },
    )
    belief = _os_packet(
        owner="BeliefOS",
        mission_id=mission_id,
        chart_id=chart_id,
        digest_field="belief_receipt_digest",
        body={
            "belief_basis_ready": True,
            "contradiction_visible": False,
            "context_local": True,
            "credal_transport_preserved": True,
        },
    )
    memory = build_cognitive_memory_packet(
        mission_id=mission_id,
        chart_id=chart_id,
        memory_id="memory-v023-cycle-1",
        prior_memory_digest="",
        process_history=_process_history(),
        episodic_refs=[observe["observation_receipt_digest"]],
        semantic_claim_refs=[belief["belief_receipt_digest"]],
        strategy_refs=[plan["semantic_plan_digest"]],
        consolidation_candidates=[
            {
                "candidate_id": "candidate-preserve-independent-verification",
                "summary": "Prefer plans with independent VerifyOS evidence",
            }
        ],
        created_at_ms=34,
    )
    plan_os = _os_packet(
        owner="PlanOS",
        mission_id=mission_id,
        chart_id=chart_id,
        digest_field="plan_activation_receipt_digest",
        body={
            "semantic_plan_digest": plan["semantic_plan_digest"],
            "activation_state": "proposal_ready",
            "replan_owner": "PlanOS",
            "execution_owner": "ActOS",
        },
    )
    verify_os = _os_packet(
        owner="VerifyOS",
        mission_id=mission_id,
        chart_id=chart_id,
        digest_field="verification_binding_receipt_digest",
        body={
            "verification_receipt_digest": verification["verification_receipt_digest"],
            "independent": True,
            "execution_success_is_mission_success": False,
        },
    )

    ready = build_os_qi_cognitive_cycle(
        cycle_id="os-qi-cycle-1",
        mission_id=mission_id,
        chart_id=chart_id,
        observe_packet=observe,
        belief_packet=belief,
        memory_packet=memory,
        semantic_plan=plan,
        plan_os_packet=plan_os,
        verification_receipt=verification,
        verify_os_packet=verify_os,
    )
    assert ready["status"] == "verified_ready"
    assert ready["nonmarkov_feedback_preserved"] is True
    assert ready["future_only_learning_delta"]["eligible_for_next_cycle_only"] is True
    assert ready["next_cycle_basis"]["activation_owner"] == "PlanOS"
    assert ready["next_cycle_basis"]["execution_owner"] == "ActOS"

    contradicted_belief = deepcopy(belief)
    contradicted_belief["contradiction_visible"] = True
    contradicted_belief["belief_receipt_digest"] = sha(
        {k: v for k, v in contradicted_belief.items() if k != "belief_receipt_digest"}
    )
    contradicted = build_os_qi_cognitive_cycle(
        cycle_id="os-qi-cycle-2",
        mission_id=mission_id,
        chart_id=chart_id,
        observe_packet=observe,
        belief_packet=contradicted_belief,
        memory_packet=memory,
        semantic_plan=plan,
        plan_os_packet=plan_os,
        verification_receipt=verification,
        verify_os_packet=verify_os,
        previous_cycle_digest=ready["os_qi_cognitive_cycle_digest"],
    )
    assert contradicted["status"] == "contradiction_visible"

    short_memory = build_cognitive_memory_packet(
        mission_id=mission_id,
        chart_id=chart_id,
        memory_id="memory-v023-short",
        prior_memory_digest=memory["cognitive_memory_digest"],
        process_history=[_process_history()[0]],
        episodic_refs=[],
        semantic_claim_refs=[],
        strategy_refs=[],
        consolidation_candidates=[],
        created_at_ms=35,
    )
    blocked_qi = build_os_qi_cognitive_cycle(
        cycle_id="os-qi-cycle-3",
        mission_id=mission_id,
        chart_id=chart_id,
        observe_packet=observe,
        belief_packet=belief,
        memory_packet=short_memory,
        semantic_plan=plan,
        plan_os_packet=plan_os,
        verification_receipt=verification,
        verify_os_packet=verify_os,
        previous_cycle_digest=contradicted["os_qi_cognitive_cycle_digest"],
    )
    assert blocked_qi["status"] == "blocked_qi"

    tampered = deepcopy(ready)
    tampered["effect_authority_granted"] = True
    tampered["os_qi_cognitive_cycle_digest"] = receipt_digest(tampered)
    assert "cycle_effect_authority_forbidden" in validate_os_qi_cognitive_cycle(tampered)

    return {
        "status": "KUUOS_OS_QI_COGNITIVE_INTEGRATION_V0_23_OK",
        "ready_status": ready["status"],
        "contradiction_status": contradicted["status"],
        "short_history_status": blocked_qi["status"],
        "nonmarkov_feedback_preserved": ready["nonmarkov_feedback_preserved"],
        "future_only_learning": ready["future_only_learning_delta"][
            "eligible_for_next_cycle_only"
        ],
        "memory_overwrite_allowed": False,
        "effect_authority_granted": False,
    }


__all__ = [
    "_os_packet",
    "_process_history",
    "_verified_fixture",
    "run_os_qi_cognitive_integration_scenarios",
]
