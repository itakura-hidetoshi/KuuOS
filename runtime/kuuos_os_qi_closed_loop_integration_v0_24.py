from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.kuuos_cognitive_memory_credit_kernel_v0_23 import (
    validate_cognitive_memory_consolidation_static,
)
from runtime.kuuos_mission_contract_types_v0_20 import sha
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    validate_semantic_plan_static,
    validate_verification_receipt_static,
)
from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor

VERSION = "kuuos_os_qi_closed_loop_integration_v0_24"
RECEIPT_VERSION = "kuuos_os_qi_closed_loop_receipt_v0_24"

STATUSES = frozenset(
    {
        "decision_candidate_ready",
        "reobserve_required",
        "contradiction_preserved",
        "human_review_required",
        "blocked",
    }
)

OWNERSHIP = {
    "observation": "ObserveOS",
    "belief_release": "BeliefOS",
    "memory_append": "MemoryOS",
    "candidate_selection": "DecisionOS",
    "plan_synthesis": "PlanOS",
    "verification": "VerifyOS",
    "execution": "ActOS",
    "process_context": "QiProcessTensor",
}

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_causal_authority": False,
    "grants_belief_release_authority": False,
    "grants_plan_activation_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_automatic_learning_authority": False,
    "grants_final_commitment_authority": False,
}

BOUNDARY = {
    "observe_is_not_verify": True,
    "verify_is_not_truth": True,
    "belief_is_local_plural": True,
    "memory_append_is_not_overwrite": True,
    "qi_process_tensor_is_context_not_authority": True,
    "nonmarkov_history_is_preserved": True,
    "credit_is_correlational_not_causal": True,
    "learning_is_future_only": True,
    "learning_delta_is_not_replan_activation": True,
    "replan_owner_is_planos": True,
    "selection_owner_is_decisionos": True,
    "execution_owner_is_actos": True,
    "verification_is_independent": True,
    "execution_success_is_not_mission_success": True,
    "graph_semantics_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def closed_loop_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "os_qi_closed_loop_digest"))


def _status(consolidation_status: str) -> str:
    return {
        "consolidated": "decision_candidate_ready",
        "reobserve_required": "reobserve_required",
        "contradiction_preserved": "contradiction_preserved",
        "human_review_required": "human_review_required",
        "blocked": "blocked",
    }[consolidation_status]


def build_os_qi_closed_loop(
    *,
    cycle_id: str,
    semantic_plan: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    cognitive_memory_receipt: Mapping[str, Any],
    observe_envelope: Mapping[str, Any],
    verify_envelope: Mapping[str, Any],
    qi_state: Mapping[str, Any],
    previous_cycle_digest: str = "",
) -> dict[str, Any]:
    errors = ["plan:" + item for item in validate_semantic_plan_static(semantic_plan)]
    errors.extend(
        "verification:" + item
        for item in validate_verification_receipt_static(verification_receipt)
    )
    errors.extend(
        "memory:" + item
        for item in validate_cognitive_memory_consolidation_static(
            cognitive_memory_receipt
        )
    )
    if cognitive_memory_receipt.get("source_plan_digest") != semantic_plan.get(
        "semantic_plan_digest"
    ):
        errors.append("memory_plan_mismatch")
    if cognitive_memory_receipt.get(
        "source_verification_digest"
    ) != verification_receipt.get("verification_receipt_digest"):
        errors.append("memory_verification_mismatch")
    if cognitive_memory_receipt.get("observe_envelope_digest") != sha(observe_envelope):
        errors.append("observe_envelope_mismatch")
    if cognitive_memory_receipt.get("verify_envelope_digest") != sha(verify_envelope):
        errors.append("verify_envelope_mismatch")
    if errors:
        raise ValueError(";".join(errors))

    qi_receipt = evaluate_qi_process_tensor(qi_state).to_dict()
    blockers = list(cognitive_memory_receipt.get("blockers", []))
    if not qi_receipt["process_tensor_visible"]:
        blockers.append("qi_process_tensor_not_visible")
    if not qi_receipt["transition_continuity_visible"]:
        blockers.append("qi_transition_continuity_not_visible")
    if not qi_receipt["memory_continuity_visible"]:
        blockers.append("qi_memory_continuity_not_visible")

    consolidation_status = str(cognitive_memory_receipt["status"])
    status = "blocked" if blockers else _status(consolidation_status)
    belief_candidate = deepcopy(
        cognitive_memory_receipt["belief_release_candidate"]
    )
    plan_candidate = deepcopy(cognitive_memory_receipt["plan_strategy_candidate"])
    memory_candidate = deepcopy(cognitive_memory_receipt["memory_append_candidate"])

    decision_candidate_set = {
        "belief_candidate_digest": belief_candidate[
            "belief_release_candidate_digest"
        ],
        "plan_candidate_digest": plan_candidate[
            "plan_strategy_candidate_digest"
        ],
        "memory_candidate_digest": memory_candidate[
            "memory_append_candidate_digest"
        ],
        "candidate_selection_required": True,
        "candidate_selected": False,
        "selection_owner": "DecisionOS",
        "qi_conditioning_used": qi_receipt["process_tensor_visible"],
        "qi_is_truth_probability": False,
        "grants_execution_authority": False,
    }
    planos_request = {
        "route": plan_candidate["route"],
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "credit_assignment_digests": list(
            plan_candidate["credit_assignment_digests"]
        ),
        "nonmarkov_context_digest": sha(qi_receipt),
        "planos_synthesis_required": True,
        "plan_activated": False,
        "execution_permission": False,
    }
    next_cycle_context = {
        "source_cycle_id": str(cycle_id),
        "source_memory_digest": cognitive_memory_receipt[
            "cognitive_memory_consolidation_digest"
        ],
        "belief_route": belief_candidate["route"],
        "plan_route": plan_candidate["route"],
        "counterevidence_digests": list(
            cognitive_memory_receipt.get("counterevidence_digests", [])
        ),
        "process_tensor_visible": qi_receipt["process_tensor_visible"],
        "nonmarkov_memory_visible": qi_receipt["nonmarkov_memory_visible"],
        "future_only": True,
        "mutates_past_cycle": False,
        "memory_overwrite": False,
        "automatic_replan_activation": False,
        "automatic_execution": False,
    }

    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": str(cycle_id),
        "mission_id": semantic_plan["mission_id"],
        "chart_id": semantic_plan["chart_id"],
        "previous_cycle_digest": str(previous_cycle_digest),
        "status": status,
        "ownership": deepcopy(OWNERSHIP),
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "source_memory_digest": cognitive_memory_receipt[
            "cognitive_memory_consolidation_digest"
        ],
        "observe_envelope_digest": sha(observe_envelope),
        "verify_envelope_digest": sha(verify_envelope),
        "qi_process_tensor_receipt": qi_receipt,
        "decision_candidate_set": decision_candidate_set,
        "planos_request": planos_request,
        "memoryos_append_candidate": memory_candidate,
        "next_cycle_context": next_cycle_context,
        "blockers": sorted(set(blockers)),
        "contradiction_preserved": consolidation_status
        == "contradiction_preserved",
        "execution_success_is_mission_success": False,
        "effect_authority_granted": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "os_qi_closed_loop_digest": "",
    }
    receipt["os_qi_closed_loop_digest"] = closed_loop_digest(receipt)
    receipt_errors = validate_os_qi_closed_loop(receipt)
    if receipt_errors:
        raise ValueError(";".join(receipt_errors))
    return receipt


def validate_os_qi_closed_loop(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != RECEIPT_VERSION:
        errors.append("version_invalid")
    if receipt.get("status") not in STATUSES:
        errors.append("status_invalid")
    if dict(receipt.get("ownership", {})) != OWNERSHIP:
        errors.append("ownership_invalid")
    candidates = receipt.get("decision_candidate_set", {})
    if candidates.get("candidate_selected") is not False:
        errors.append("candidate_selection_bypass")
    if candidates.get("selection_owner") != "DecisionOS":
        errors.append("selection_owner_invalid")
    if candidates.get("qi_is_truth_probability") is not False:
        errors.append("qi_truth_probability_forbidden")
    plan_request = receipt.get("planos_request", {})
    if plan_request.get("planos_synthesis_required") is not True:
        errors.append("planos_synthesis_missing")
    if plan_request.get("plan_activated") is not False:
        errors.append("plan_activation_bypass")
    if plan_request.get("execution_permission") is not False:
        errors.append("execution_permission_forbidden")
    context = receipt.get("next_cycle_context", {})
    if context.get("future_only") is not True:
        errors.append("future_only_missing")
    if context.get("mutates_past_cycle") is not False:
        errors.append("past_mutation_forbidden")
    if context.get("memory_overwrite") is not False:
        errors.append("memory_overwrite_forbidden")
    if context.get("automatic_replan_activation") is not False:
        errors.append("automatic_replan_activation_forbidden")
    if context.get("automatic_execution") is not False:
        errors.append("automatic_execution_forbidden")
    if receipt.get("execution_success_is_mission_success") is not False:
        errors.append("execution_mission_success_collapse")
    if receipt.get("effect_authority_granted") is not False:
        errors.append("effect_authority_forbidden")
    if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("non_authority_invalid")
    if dict(receipt.get("boundary", {})) != BOUNDARY:
        errors.append("boundary_invalid")
    if receipt.get("os_qi_closed_loop_digest") != closed_loop_digest(receipt):
        errors.append("digest_invalid")
    return errors


__all__ = [
    "BOUNDARY",
    "NON_AUTHORITY",
    "OWNERSHIP",
    "RECEIPT_VERSION",
    "STATUSES",
    "VERSION",
    "build_os_qi_closed_loop",
    "closed_loop_digest",
    "validate_os_qi_closed_loop",
]
