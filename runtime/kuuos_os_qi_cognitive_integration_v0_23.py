from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_mission_contract_types_v0_20 import sha
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    validate_semantic_plan_static,
    validate_verification_receipt_static,
)
from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor

VERSION = "kuuos_os_qi_cognitive_integration_v0_23"
RECEIPT_VERSION = "kuuos_os_qi_cognitive_cycle_receipt_v0_23"
MEMORY_VERSION = "kuuos_cognitive_process_memory_packet_v0_23"

CYCLE_STATUSES = frozenset(
    {
        "blocked_observe",
        "blocked_belief",
        "blocked_memory",
        "blocked_qi",
        "replan_required",
        "verification_required",
        "verified_ready",
        "contradiction_visible",
    }
)

NON_AUTHORITY = {
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_truth_authority": False,
    "grants_final_commitment_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_mission_transition_authority": False,
    "grants_self_modification_authority": False,
}

OWNERSHIP = {
    "observation_owner": "ObserveOS",
    "belief_owner": "BeliefOS",
    "memory_owner": "MemoryOS",
    "planning_owner": "PlanOS",
    "verification_owner": "VerifyOS",
    "process_continuity_evaluator": "QiProcessTensor",
}

BOUNDARY = {
    "observation_is_not_truth": True,
    "belief_is_context_local": True,
    "contradiction_is_preserved": True,
    "memory_is_append_only": True,
    "memory_consolidation_is_proposal_only": True,
    "process_tensor_is_non_authoritative": True,
    "process_tensor_is_not_truth_probability": True,
    "process_history_is_non_markov": True,
    "learning_is_future_only": True,
    "plan_is_not_execution_license": True,
    "verification_is_independent": True,
    "execution_success_is_not_mission_success": True,
    "lower_execution_authority_preserved": True,
    "graph_semantics_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def receipt_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "os_qi_cognitive_cycle_digest"))


def memory_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_memory_digest"))


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _unique_strings(values: Sequence[Any], name: str, *, allow_empty: bool = False) -> list[str]:
    result = [_text(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def build_cognitive_memory_packet(
    *,
    mission_id: str,
    chart_id: str,
    memory_id: str,
    prior_memory_digest: str,
    process_history: Sequence[Mapping[str, Any]],
    episodic_refs: Sequence[str],
    semantic_claim_refs: Sequence[str],
    strategy_refs: Sequence[str],
    consolidation_candidates: Sequence[Mapping[str, Any]],
    created_at_ms: int,
) -> dict[str, Any]:
    history = [deepcopy(dict(item)) for item in process_history]
    if not history:
        raise ValueError("process_history_missing")
    candidates = [deepcopy(dict(item)) for item in consolidation_candidates]
    for candidate in candidates:
        if not str(candidate.get("candidate_id", "")).strip():
            raise ValueError("consolidation_candidate_id_missing")
        candidate["proposal_only"] = True
        candidate["overwrites_prior_memory"] = False
        candidate["grants_truth_authority"] = False
    packet = {
        "version": MEMORY_VERSION,
        "mission_id": _text(mission_id, "mission_id"),
        "chart_id": _text(chart_id, "chart_id"),
        "memory_id": _text(memory_id, "memory_id"),
        "prior_memory_digest": str(prior_memory_digest),
        "process_history": history,
        "episodic_refs": _unique_strings(episodic_refs, "episodic_refs", allow_empty=True),
        "semantic_claim_refs": _unique_strings(
            semantic_claim_refs, "semantic_claim_refs", allow_empty=True
        ),
        "strategy_refs": _unique_strings(strategy_refs, "strategy_refs", allow_empty=True),
        "consolidation_candidates": candidates,
        "append_only": True,
        "consolidation_is_proposal_only": True,
        "memory_overwrite_allowed": False,
        "created_at_ms": int(created_at_ms),
        "non_authority": deepcopy(NON_AUTHORITY),
        "cognitive_memory_digest": "",
    }
    if packet["created_at_ms"] < 0:
        raise ValueError("created_at_ms_negative")
    packet["cognitive_memory_digest"] = memory_digest(packet)
    errors = validate_cognitive_memory_packet(packet)
    if errors:
        raise ValueError(";".join(errors))
    return packet


def validate_cognitive_memory_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("version") != MEMORY_VERSION:
        errors.append("memory_version_invalid")
    for field in ("mission_id", "chart_id", "memory_id"):
        if not str(packet.get(field, "")).strip():
            errors.append(f"memory_{field}_missing")
    history = packet.get("process_history")
    if not isinstance(history, list) or not history:
        errors.append("memory_process_history_invalid")
    for field in ("episodic_refs", "semantic_claim_refs", "strategy_refs"):
        values = packet.get(field)
        if not isinstance(values, list):
            errors.append(f"memory_{field}_invalid")
        elif len(values) != len(set(str(item) for item in values)):
            errors.append(f"memory_{field}_duplicate")
    candidates = packet.get("consolidation_candidates")
    if not isinstance(candidates, list):
        errors.append("memory_consolidation_candidates_invalid")
    else:
        for candidate in candidates:
            if candidate.get("proposal_only") is not True:
                errors.append("memory_consolidation_not_proposal")
            if candidate.get("overwrites_prior_memory") is not False:
                errors.append("memory_consolidation_overwrite_forbidden")
            if candidate.get("grants_truth_authority") is not False:
                errors.append("memory_consolidation_truth_authority_forbidden")
    if packet.get("append_only") is not True:
        errors.append("memory_append_only_required")
    if packet.get("consolidation_is_proposal_only") is not True:
        errors.append("memory_consolidation_proposal_only_required")
    if packet.get("memory_overwrite_allowed") is not False:
        errors.append("memory_overwrite_forbidden")
    if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("memory_non_authority_invalid")
    try:
        if int(packet.get("created_at_ms", -1)) < 0:
            errors.append("memory_created_at_invalid")
    except (TypeError, ValueError):
        errors.append("memory_created_at_invalid")
    if packet.get("cognitive_memory_digest") != memory_digest(packet):
        errors.append("cognitive_memory_digest_invalid")
    return errors


def _validate_os_packet(
    packet: Mapping[str, Any],
    *,
    owner: str,
    mission_id: str,
    chart_id: str,
    required_digest_field: str,
) -> list[str]:
    errors: list[str] = []
    if packet.get("owner") != owner:
        errors.append(f"{owner}_owner_invalid")
    if packet.get("mission_id") != mission_id:
        errors.append(f"{owner}_mission_mismatch")
    if packet.get("chart_id") != chart_id:
        errors.append(f"{owner}_chart_mismatch")
    if not str(packet.get(required_digest_field, "")).strip():
        errors.append(f"{owner}_digest_missing")
    if dict(packet.get("non_authority", {})) != NON_AUTHORITY:
        errors.append(f"{owner}_non_authority_invalid")
    return errors


def _qi_input(
    *,
    cycle_id: str,
    memory_packet: Mapping[str, Any],
    extra_boundary: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    packet = {
        "cycle_id": cycle_id,
        "process_history": deepcopy(memory_packet["process_history"]),
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
    }
    if extra_boundary:
        packet.update(dict(extra_boundary))
    return packet


def _cycle_status(
    *,
    observe_ready: bool,
    belief_ready: bool,
    contradiction_visible: bool,
    memory_ready: bool,
    qi_ready: bool,
    plan_status: str,
    verification_status: str,
) -> str:
    if not observe_ready:
        return "blocked_observe"
    if contradiction_visible:
        return "contradiction_visible"
    if not belief_ready:
        return "blocked_belief"
    if not memory_ready:
        return "blocked_memory"
    if not qi_ready:
        return "blocked_qi"
    if plan_status != "ready":
        return "replan_required"
    if verification_status != "verified_success":
        return "verification_required"
    return "verified_ready"


def build_os_qi_cognitive_cycle(
    *,
    cycle_id: str,
    mission_id: str,
    chart_id: str,
    observe_packet: Mapping[str, Any],
    belief_packet: Mapping[str, Any],
    memory_packet: Mapping[str, Any],
    semantic_plan: Mapping[str, Any],
    plan_os_packet: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    verify_os_packet: Mapping[str, Any],
    previous_cycle_digest: str = "",
    qi_boundary_overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    cycle = _text(cycle_id, "cycle_id")
    mission = _text(mission_id, "mission_id")
    chart = _text(chart_id, "chart_id")

    errors: list[str] = []
    errors.extend(
        _validate_os_packet(
            observe_packet,
            owner="ObserveOS",
            mission_id=mission,
            chart_id=chart,
            required_digest_field="observation_receipt_digest",
        )
    )
    errors.extend(
        _validate_os_packet(
            belief_packet,
            owner="BeliefOS",
            mission_id=mission,
            chart_id=chart,
            required_digest_field="belief_receipt_digest",
        )
    )
    memory_errors = validate_cognitive_memory_packet(memory_packet)
    errors.extend("MemoryOS:" + item for item in memory_errors)
    if memory_packet.get("mission_id") != mission:
        errors.append("MemoryOS_mission_mismatch")
    if memory_packet.get("chart_id") != chart:
        errors.append("MemoryOS_chart_mismatch")
    errors.extend("PlanOS:plan:" + item for item in validate_semantic_plan_static(semantic_plan))
    errors.extend(
        _validate_os_packet(
            plan_os_packet,
            owner="PlanOS",
            mission_id=mission,
            chart_id=chart,
            required_digest_field="plan_activation_receipt_digest",
        )
    )
    if plan_os_packet.get("semantic_plan_digest") != semantic_plan.get("semantic_plan_digest"):
        errors.append("PlanOS_semantic_plan_mismatch")
    errors.extend(
        "VerifyOS:verification:" + item
        for item in validate_verification_receipt_static(verification_receipt)
    )
    errors.extend(
        _validate_os_packet(
            verify_os_packet,
            owner="VerifyOS",
            mission_id=mission,
            chart_id=chart,
            required_digest_field="verification_binding_receipt_digest",
        )
    )
    if verify_os_packet.get("verification_receipt_digest") != verification_receipt.get(
        "verification_receipt_digest"
    ):
        errors.append("VerifyOS_verification_receipt_mismatch")
    if verification_receipt.get("planner_id") == verification_receipt.get("verifier_id"):
        errors.append("VerifyOS_independence_violation")
    if errors:
        raise ValueError(";".join(errors))

    qi_receipt = evaluate_qi_process_tensor(
        _qi_input(
            cycle_id=cycle,
            memory_packet=memory_packet,
            extra_boundary=qi_boundary_overrides,
        )
    ).to_dict()
    observe_ready = bool(observe_packet.get("observation_grounded", False))
    contradiction_visible = bool(belief_packet.get("contradiction_visible", False))
    belief_ready = bool(belief_packet.get("belief_basis_ready", False))
    memory_ready = bool(
        memory_packet.get("append_only")
        and memory_packet.get("consolidation_is_proposal_only")
        and not memory_packet.get("memory_overwrite_allowed")
    )
    qi_ready = bool(
        qi_receipt["process_tensor_visible"]
        and qi_receipt["transition_continuity_visible"]
        and qi_receipt["memory_continuity_visible"]
    )
    plan_status = str(semantic_plan.get("status", ""))
    verification_status = str(verification_receipt.get("status", ""))
    status = _cycle_status(
        observe_ready=observe_ready,
        belief_ready=belief_ready,
        contradiction_visible=contradiction_visible,
        memory_ready=memory_ready,
        qi_ready=qi_ready,
        plan_status=plan_status,
        verification_status=verification_status,
    )

    future_only_delta = {
        "source_cycle_id": cycle,
        "source_memory_digest": memory_packet["cognitive_memory_digest"],
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "qi_process_tensor_reason": qi_receipt["process_tensor_reason"],
        "eligible_for_next_cycle_only": True,
        "mutates_past_cycle": False,
        "overwrites_memory": False,
        "grants_execution_authority": False,
    }
    next_cycle_basis = {
        "observation_receipt_digest": observe_packet["observation_receipt_digest"],
        "belief_receipt_digest": belief_packet["belief_receipt_digest"],
        "memory_digest": memory_packet["cognitive_memory_digest"],
        "semantic_plan_digest": semantic_plan["semantic_plan_digest"],
        "verification_receipt_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "qi_process_tensor_visible": qi_receipt["process_tensor_visible"],
        "nonmarkov_memory_visible": qi_receipt["nonmarkov_memory_visible"],
        "future_only_delta_digest": sha(future_only_delta),
        "activation_owner": "PlanOS",
        "execution_owner": "ActOS",
        "effect_authority_granted": False,
    }

    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": cycle,
        "mission_id": mission,
        "chart_id": chart,
        "previous_cycle_digest": str(previous_cycle_digest),
        "status": status,
        "ownership": deepcopy(OWNERSHIP),
        "observe_packet_digest": observe_packet["observation_receipt_digest"],
        "belief_packet_digest": belief_packet["belief_receipt_digest"],
        "memory_packet_digest": memory_packet["cognitive_memory_digest"],
        "semantic_plan_digest": semantic_plan["semantic_plan_digest"],
        "plan_os_packet_digest": plan_os_packet["plan_activation_receipt_digest"],
        "verification_receipt_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "verify_os_packet_digest": verify_os_packet[
            "verification_binding_receipt_digest"
        ],
        "qi_process_tensor_receipt": qi_receipt,
        "future_only_learning_delta": future_only_delta,
        "next_cycle_basis": next_cycle_basis,
        "contradiction_visible": contradiction_visible,
        "nonmarkov_feedback_preserved": qi_receipt["nonmarkov_memory_visible"],
        "execution_success_is_mission_success": False,
        "effect_authority_granted": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(BOUNDARY),
        "os_qi_cognitive_cycle_digest": "",
    }
    receipt["os_qi_cognitive_cycle_digest"] = receipt_digest(receipt)
    receipt_errors = validate_os_qi_cognitive_cycle(receipt)
    if receipt_errors:
        raise ValueError(";".join(receipt_errors))
    return receipt


def validate_os_qi_cognitive_cycle(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != RECEIPT_VERSION:
        errors.append("cycle_version_invalid")
    if receipt.get("status") not in CYCLE_STATUSES:
        errors.append("cycle_status_invalid")
    for field in ("cycle_id", "mission_id", "chart_id"):
        if not str(receipt.get(field, "")).strip():
            errors.append(f"cycle_{field}_missing")
    if dict(receipt.get("ownership", {})) != OWNERSHIP:
        errors.append("cycle_ownership_invalid")
    qi = receipt.get("qi_process_tensor_receipt")
    if not isinstance(qi, Mapping):
        errors.append("cycle_qi_receipt_invalid")
    else:
        for field in (
            "grants_execution_authority",
            "grants_truth_authority",
            "grants_memory_overwrite_authority",
        ):
            if qi.get(field) is not False:
                errors.append(f"cycle_qi_{field}_forbidden")
    delta = receipt.get("future_only_learning_delta")
    if not isinstance(delta, Mapping):
        errors.append("cycle_future_delta_invalid")
    else:
        if delta.get("eligible_for_next_cycle_only") is not True:
            errors.append("cycle_future_delta_not_future_only")
        if delta.get("mutates_past_cycle") is not False:
            errors.append("cycle_past_mutation_forbidden")
        if delta.get("overwrites_memory") is not False:
            errors.append("cycle_memory_overwrite_forbidden")
    basis = receipt.get("next_cycle_basis")
    if not isinstance(basis, Mapping):
        errors.append("cycle_next_basis_invalid")
    else:
        if basis.get("activation_owner") != "PlanOS":
            errors.append("cycle_activation_owner_invalid")
        if basis.get("execution_owner") != "ActOS":
            errors.append("cycle_execution_owner_invalid")
        if basis.get("effect_authority_granted") is not False:
            errors.append("cycle_basis_effect_authority_forbidden")
    if receipt.get("execution_success_is_mission_success") is not False:
        errors.append("cycle_execution_mission_success_collapse")
    if receipt.get("effect_authority_granted") is not False:
        errors.append("cycle_effect_authority_forbidden")
    if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("cycle_non_authority_invalid")
    if dict(receipt.get("boundary", {})) != BOUNDARY:
        errors.append("cycle_boundary_invalid")
    if receipt.get("os_qi_cognitive_cycle_digest") != receipt_digest(receipt):
        errors.append("cycle_digest_invalid")
    return errors


__all__ = [
    "BOUNDARY",
    "CYCLE_STATUSES",
    "MEMORY_VERSION",
    "NON_AUTHORITY",
    "OWNERSHIP",
    "RECEIPT_VERSION",
    "VERSION",
    "build_cognitive_memory_packet",
    "build_os_qi_cognitive_cycle",
    "memory_digest",
    "receipt_digest",
    "validate_cognitive_memory_packet",
    "validate_os_qi_cognitive_cycle",
]
