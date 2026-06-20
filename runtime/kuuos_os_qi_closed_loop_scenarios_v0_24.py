from __future__ import annotations

from copy import deepcopy
from typing import Any

from runtime.kuuos_cognitive_memory_credit_kernel_v0_23 import (
    build_cognitive_memory_consolidation,
)
from runtime.kuuos_cognitive_memory_credit_scenarios_v0_23 import (
    _observe_envelope,
    _qi_state,
    _verification,
    _verify_envelope,
)
from runtime.kuuos_os_qi_closed_loop_integration_v0_24 import (
    build_os_qi_closed_loop,
    closed_loop_digest,
    validate_os_qi_closed_loop,
)
from runtime.kuuos_semantic_planner_verifier_scenarios_v0_22 import (
    _build_plan,
    _fixture,
    _ready_belief_state,
)


def _build_case(status: str, cycle_id: str) -> dict[str, Any]:
    contract, mission_state, goal, portfolio = _fixture()
    belief = _ready_belief_state(contract, mission_state)
    plan = _build_plan(contract, mission_state, belief, goal, portfolio)
    verification, observations = _verification(
        contract=contract,
        mission_state=mission_state,
        belief=belief,
        goal=goal,
        portfolio=portfolio,
        plan=plan,
        status=status,
        observed_at_ms=80 if status == "verified_success" else 90,
    )
    observe = _observe_envelope(
        plan=plan,
        observation_digest=observations[-1]["observation_digest"],
        suffix=cycle_id,
    )
    verify = _verify_envelope(
        observe_envelope=observe,
        verification=verification,
        verdict="PASSED" if status == "verified_success" else "FAILED",
        suffix=cycle_id,
    )
    memory = build_cognitive_memory_consolidation(
        contract=contract,
        mission_state=mission_state,
        belief_state=belief,
        semantic_plan=plan,
        verification_receipt=verification,
        observe_envelope=observe,
        verify_envelope=verify,
        qi_state=_qi_state(cycle_id),
        memory_entries=[],
        consolidator_id="MemoryOS-v024",
        episode_id=f"episode-{cycle_id}",
        consolidated_at_ms=100,
        belief_coherence_receipt_digests=[f"belief-coherence-{cycle_id}"],
    )
    return {
        "plan": plan,
        "verification": verification,
        "observe": observe,
        "verify": verify,
        "memory": memory,
        "qi": _qi_state(cycle_id),
    }


def run_os_qi_closed_loop_scenarios() -> dict[str, Any]:
    success = _build_case("verified_success", "v024-success")
    ready = build_os_qi_closed_loop(
        cycle_id="v024-success",
        semantic_plan=success["plan"],
        verification_receipt=success["verification"],
        cognitive_memory_receipt=success["memory"],
        observe_envelope=success["observe"],
        verify_envelope=success["verify"],
        qi_state=success["qi"],
    )
    assert ready["status"] == "decision_candidate_ready"
    assert ready["decision_candidate_set"]["candidate_selected"] is False
    assert ready["planos_request"]["plan_activated"] is False
    assert ready["next_cycle_context"]["future_only"] is True
    assert ready["next_cycle_context"]["nonmarkov_memory_visible"] is True

    failure = _build_case("contradicted", "v024-contradicted")
    contradicted = build_os_qi_closed_loop(
        cycle_id="v024-contradicted",
        semantic_plan=failure["plan"],
        verification_receipt=failure["verification"],
        cognitive_memory_receipt=failure["memory"],
        observe_envelope=failure["observe"],
        verify_envelope=failure["verify"],
        qi_state=failure["qi"],
        previous_cycle_digest=ready["os_qi_closed_loop_digest"],
    )
    assert contradicted["status"] == "contradiction_preserved"
    assert contradicted["contradiction_preserved"] is True
    assert contradicted["planos_request"]["route"] == "repair"

    blocked_qi = deepcopy(success["qi"])
    blocked_qi["two_truths_gap"] = False
    blocked = build_os_qi_closed_loop(
        cycle_id="v024-blocked",
        semantic_plan=success["plan"],
        verification_receipt=success["verification"],
        cognitive_memory_receipt=success["memory"],
        observe_envelope=success["observe"],
        verify_envelope=success["verify"],
        qi_state=blocked_qi,
        previous_cycle_digest=contradicted["os_qi_closed_loop_digest"],
    )
    assert blocked["status"] == "blocked"
    assert "qi_process_tensor_not_visible" in blocked["blockers"]

    tampered = deepcopy(ready)
    tampered["decision_candidate_set"]["candidate_selected"] = True
    tampered["os_qi_closed_loop_digest"] = closed_loop_digest(tampered)
    assert "candidate_selection_bypass" in validate_os_qi_closed_loop(tampered)

    return {
        "status": "KUUOS_OS_QI_CLOSED_LOOP_V0_24_OK",
        "ready_status": ready["status"],
        "contradiction_status": contradicted["status"],
        "blocked_status": blocked["status"],
        "nonmarkov_memory_visible": ready["next_cycle_context"][
            "nonmarkov_memory_visible"
        ],
        "candidate_selected": False,
        "plan_activated": False,
        "execution_permission": False,
        "memory_overwrite": False,
    }


__all__ = ["_build_case", "run_os_qi_closed_loop_scenarios"]
