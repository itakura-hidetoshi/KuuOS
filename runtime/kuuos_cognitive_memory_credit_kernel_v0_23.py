from __future__ import annotations

import math
from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_mission_contract_types_v0_20 import (
    sha,
    validate_mission_contract,
)
from runtime.kuuos_mission_state_v0_20 import validate_mission_state
from runtime.kuuos_observation_belief_state_kernel_v0_21 import validate_belief_state
from runtime.kuuos_runtime_daemon_qi_memoryos_process_tensor_retrieval_replay_v0_1 import (
    build_qi_memoryos_process_tensor_retrieval_replay,
)
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    validate_semantic_plan_static,
    validate_verification_receipt_static,
)
from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor

VERSION = "kuuos_cognitive_memory_credit_kernel_v0_23"
RECEIPT_VERSION = "kuuos_cognitive_memory_consolidation_receipt_v0_23"
CREDIT_VERSION = "kuuos_bounded_credit_assignment_v0_23"
BELIEF_CANDIDATE_VERSION = "kuuos_belief_release_candidate_v0_23"
PLAN_CANDIDATE_VERSION = "kuuos_plan_strategy_candidate_v0_23"
MEMORY_CANDIDATE_VERSION = "kuuos_memoryos_consolidation_append_candidate_v0_23"

CONSOLIDATION_STATUSES = frozenset(
    {
        "consolidated",
        "contradiction_preserved",
        "reobserve_required",
        "human_review_required",
        "blocked",
    }
)
PLAN_ROUTES = frozenset(
    {"continue", "strengthen", "repair", "reobserve", "reroute", "hold"}
)
BELIEF_ROUTES = frozenset({"candidate", "observe", "repair", "hold"})

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
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "observe_is_not_verify": True,
    "verify_is_not_absolute_truth": True,
    "belief_is_local_and_plural": True,
    "memory_is_not_belief_authority": True,
    "qi_conditions_history_but_is_not_authority": True,
    "credit_is_correlational_not_causal": True,
    "learning_is_future_only": True,
    "learning_delta_is_not_replan_activation": True,
    "replan_belongs_to_planos": True,
    "candidate_selection_belongs_to_decisionos": True,
    "execution_belongs_to_actos": True,
    "memory_append_is_not_memory_overwrite": True,
    "counterevidence_is_preserved": True,
    "contradiction_is_not_silently_resolved": True,
    "root_overwrite_is_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    result = deepcopy(dict(value))
    result.pop(field, None)
    return result


def consolidation_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "cognitive_memory_consolidation_digest"))


def credit_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "credit_assignment_digest"))


def belief_candidate_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "belief_release_candidate_digest"))


def plan_candidate_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "plan_strategy_candidate_digest"))


def memory_candidate_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "memory_append_candidate_digest"))


def _text(value: Any, name: str) -> str:
    result = str(value).strip()
    if not result:
        raise ValueError(f"{name}_missing")
    return result


def _nonnegative_int(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name}_invalid")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if result < 0:
        raise ValueError(f"{name}_negative")
    return result


def _finite(value: Any, name: str, *, minimum: float | None = None) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}_invalid") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name}_not_finite")
    if minimum is not None and result < minimum:
        raise ValueError(f"{name}_below_minimum")
    return result


def _bounded(value: Any, name: str, *, lower: float, upper: float) -> float:
    result = _finite(value, name)
    if result < lower or result > upper:
        raise ValueError(f"{name}_out_of_bounds")
    return result


def _strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = False
) -> list[str]:
    result = [_text(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _first_digest(packet: Mapping[str, Any], names: Sequence[str]) -> str:
    for name in names:
        value = str(packet.get(name, "")).strip()
        if value:
            return value
    return ""


def _false_or_missing(packet: Mapping[str, Any], field: str) -> bool:
    return packet.get(field, False) is False


def _validate_observe_envelope(
    packet: Mapping[str, Any], plan: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if packet.get("observation_recorded") is not True:
        errors.append("observe_observation_not_recorded")
    if packet.get("observation_not_verification") is not True:
        errors.append("observe_verification_separation_missing")
    if packet.get("verification_required") is not True:
        errors.append("observe_verification_required_missing")
    if packet.get("mission_id") not in {None, plan.get("mission_id")}:
        errors.append("observe_mission_mismatch")
    if packet.get("chart_id") not in {None, plan.get("chart_id")}:
        errors.append("observe_chart_mismatch")
    source_plan = _first_digest(
        packet,
        (
            "source_plan_digest",
            "semantic_plan_digest",
            "structured_plan_digest",
            "next_plan_basis_digest",
        ),
    )
    if source_plan and source_plan != plan.get("semantic_plan_digest"):
        errors.append("observe_plan_mismatch")
    if not _first_digest(
        packet,
        (
            "observe_completion_receipt_digest",
            "observation_completion_digest",
            "observation_digest",
        ),
    ):
        errors.append("observe_completion_digest_missing")
    for field in (
        "grants_truth_authority",
        "grants_verification_authority",
        "grants_execution_authority",
        "grants_memory_overwrite_authority",
        "memory_overwrite_performed",
    ):
        if not _false_or_missing(packet, field):
            errors.append(f"observe_{field}_not_false")
    return errors


def _validate_verify_envelope(
    packet: Mapping[str, Any],
    observe_packet: Mapping[str, Any],
    verification: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    verdict = str(packet.get("verdict", packet.get("status", ""))).upper()
    if verdict not in {
        "PASSED",
        "FAILED",
        "INDETERMINATE",
        "VERIFIED_SUCCESS",
        "PARTIAL_SUCCESS",
        "INCONCLUSIVE",
        "CONTRADICTED",
        "REGRESSION_DETECTED",
        "VERIFICATION_REQUIRES_HUMAN",
    }:
        errors.append("verify_verdict_invalid")
    if packet.get("learning_required") is not True:
        errors.append("verify_learning_required_missing")
    if packet.get("learning_must_be_future_only") is not True:
        errors.append("verify_future_only_missing")
    if packet.get("automatic_learning") is not False:
        errors.append("verify_automatic_learning_not_false")
    source_observation = _first_digest(
        packet,
        (
            "source_observation_digest",
            "observation_digest",
            "observe_completion_receipt_digest",
        ),
    )
    observe_digest = _first_digest(
        observe_packet,
        (
            "observation_digest",
            "observation_completion_digest",
            "observe_completion_receipt_digest",
        ),
    )
    if source_observation and observe_digest and source_observation != observe_digest:
        errors.append("verify_observation_mismatch")
    source_verification = _first_digest(
        packet,
        (
            "source_verification_receipt_digest",
            "verification_receipt_digest",
        ),
    )
    if source_verification and source_verification != verification.get(
        "verification_receipt_digest"
    ):
        errors.append("verify_receipt_mismatch")
    if not _first_digest(
        packet,
        (
            "verify_completion_receipt_digest",
            "verification_completion_digest",
            "verification_receipt_digest",
        ),
    ):
        errors.append("verify_completion_digest_missing")
    for field in (
        "grants_truth_authority",
        "grants_causal_authority",
        "grants_execution_authority",
        "grants_memory_overwrite_authority",
        "grants_automatic_learning_authority",
    ):
        if not _false_or_missing(packet, field):
            errors.append(f"verify_{field}_not_false")
    return errors


def _outcome_score(status: str) -> float:
    return {
        "verified_success": 1.0,
        "partial_success": 0.4,
        "inconclusive": 0.0,
        "contradicted": -0.7,
        "regression_detected": -1.0,
        "verification_requires_human": 0.0,
    }[status]


def _criterion_coverage(verification: Mapping[str, Any]) -> float:
    assessments = verification.get("criterion_assessments", [])
    if not assessments:
        return 0.0
    values = {
        "satisfied": 1.0,
        "unsatisfied": 0.0,
        "unknown": 0.25,
        "contradicted": 0.0,
        "regressed": 0.0,
    }
    return sum(values.get(str(item.get("status")), 0.0) for item in assessments) / len(
        assessments
    )


def _qi_scalar(qi_state: Mapping[str, Any], field: str, default: float) -> float:
    try:
        value = float(qi_state.get(field, default))
    except (TypeError, ValueError):
        return default
    if not math.isfinite(value):
        return default
    return min(1.0, max(0.0, value))


def _build_credit_assignments(
    *,
    plan: Mapping[str, Any],
    verification: Mapping[str, Any],
    qi_state: Mapping[str, Any],
) -> list[dict[str, Any]]:
    steps = list(plan.get("steps", []))
    count = len(steps)
    if count == 0:
        raise ValueError("credit_plan_steps_missing")
    outcome = _outcome_score(str(verification["status"]))
    coverage = _criterion_coverage(verification)
    confidence = float(verification.get("aggregate_confidence", 0.0))
    hysteresis = _qi_scalar(qi_state, "hysteresis", 0.25)
    memory_horizon = _qi_scalar(qi_state, "memory_horizon", 0.5)
    observation_debt = _qi_scalar(qi_state, "observation_debt", 0.0)
    assignments: list[dict[str, Any]] = []
    for index, step in enumerate(steps):
        distance = count - index - 1
        temporal_weight = 1.0 / (1.0 + hysteresis * distance)
        history_floor = 0.5 + 0.5 * memory_horizon
        temporal_weight = min(1.0, temporal_weight * history_floor)
        evidence_weight = coverage * (1.0 - 0.5 * observation_debt)
        signed_credit = max(
            -1.0,
            min(1.0, outcome * temporal_weight * evidence_weight * confidence),
        )
        if verification["status"] in {
            "inconclusive",
            "verification_requires_human",
        }:
            attribution = "uncertain"
        elif signed_credit > 0.05:
            attribution = "supporting"
        elif signed_credit < -0.05:
            attribution = "adverse"
        else:
            attribution = "neutral"
        packet = {
            "version": CREDIT_VERSION,
            "step_id": step["step_id"],
            "plan_step_digest": step["plan_step_digest"],
            "source_plan_digest": plan["semantic_plan_digest"],
            "source_verification_digest": verification[
                "verification_receipt_digest"
            ],
            "temporal_weight": temporal_weight,
            "criterion_coverage": coverage,
            "verification_confidence": confidence,
            "signed_credit": signed_credit,
            "attribution_class": attribution,
            "causal_claim": False,
            "future_only": True,
            "active_now": False,
            "credit_assignment_digest": "",
        }
        packet["credit_assignment_digest"] = credit_digest(packet)
        assignments.append(packet)
    return assignments


def _routes(
    verification_status: str,
    qi_state: Mapping[str, Any],
) -> tuple[str, str, str]:
    observation_debt = _qi_scalar(qi_state, "observation_debt", 0.0)
    transition_readiness = _qi_scalar(qi_state, "transition_readiness", 0.5)
    if verification_status == "verified_success":
        plan_route = (
            "strengthen"
            if transition_readiness >= 0.8 and observation_debt <= 0.2
            else "continue"
        )
        return "consolidated", "candidate", plan_route
    if verification_status == "partial_success":
        return "reobserve_required", "observe", "reobserve"
    if verification_status == "inconclusive":
        return "reobserve_required", "observe", "reobserve"
    if verification_status == "contradicted":
        return "contradiction_preserved", "repair", "repair"
    if verification_status == "regression_detected":
        return "contradiction_preserved", "repair", "hold"
    return "human_review_required", "hold", "hold"


def _counterevidence(verification: Mapping[str, Any]) -> list[str]:
    result: set[str] = set()
    for assessment in verification.get("criterion_assessments", []):
        if assessment.get("status") in {
            "unsatisfied",
            "contradicted",
            "regressed",
            "unknown",
        }:
            result.update(
                str(item)
                for item in assessment.get("evidence_observation_digests", [])
            )
    return sorted(result)


def _belief_claim_summary(belief_state: Mapping[str, Any]) -> dict[str, Any]:
    claims = belief_state.get("claims", {})
    statuses: dict[str, int] = {}
    support: set[str] = set()
    oppose: set[str] = set()
    unknown: set[str] = set()
    for claim in claims.values():
        status = str(claim.get("status", "unknown"))
        statuses[status] = statuses.get(status, 0) + 1
        support.update(str(item) for item in claim.get("support_evidence_digests", []))
        oppose.update(str(item) for item in claim.get("oppose_evidence_digests", []))
        unknown.update(str(item) for item in claim.get("unknown_evidence_digests", []))
    return {
        "claim_count": len(claims),
        "status_counts": statuses,
        "support_evidence_digests": sorted(support),
        "oppose_evidence_digests": sorted(oppose),
        "unknown_evidence_digests": sorted(unknown),
    }


def build_cognitive_memory_consolidation(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    belief_state: Mapping[str, Any],
    semantic_plan: Mapping[str, Any],
    verification_receipt: Mapping[str, Any],
    observe_envelope: Mapping[str, Any],
    verify_envelope: Mapping[str, Any],
    qi_state: Mapping[str, Any],
    memory_entries: Sequence[Mapping[str, Any]],
    consolidator_id: str,
    episode_id: str,
    consolidated_at_ms: int,
    belief_coherence_receipt_digests: Sequence[str] = (),
) -> dict[str, Any]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    errors.extend(
        "belief_state:" + item
        for item in validate_belief_state(belief_state, contract, mission_state)
    )
    errors.extend(
        "plan:" + item for item in validate_semantic_plan_static(semantic_plan)
    )
    errors.extend(
        "verification:" + item
        for item in validate_verification_receipt_static(verification_receipt)
    )
    errors.extend(_validate_observe_envelope(observe_envelope, semantic_plan))
    errors.extend(
        _validate_verify_envelope(
            verify_envelope, observe_envelope, verification_receipt
        )
    )
    if semantic_plan.get("mission_id") != contract.get("mission_id"):
        errors.append("plan_mission_mismatch")
    if semantic_plan.get("contract_digest") != contract.get(
        "mission_contract_digest"
    ):
        errors.append("plan_contract_mismatch")
    if semantic_plan.get("source_belief_state_digest") != belief_state.get(
        "observation_belief_state_digest"
    ):
        errors.append("plan_belief_mismatch")
    if verification_receipt.get("source_plan_digest") != semantic_plan.get(
        "semantic_plan_digest"
    ):
        errors.append("verification_plan_mismatch")
    if verification_receipt.get("source_belief_state_digest") != belief_state.get(
        "observation_belief_state_digest"
    ):
        errors.append("verification_belief_mismatch")
    if verification_receipt.get("chart_id") != belief_state.get("chart_id"):
        errors.append("verification_chart_mismatch")
    if errors:
        raise ValueError(";".join(errors))

    qi_receipt = evaluate_qi_process_tensor(qi_state).to_dict()
    blockers: list[str] = []
    warnings: list[str] = []
    if not qi_receipt["process_tensor_visible"]:
        blockers.append("qi_process_tensor_not_visible")
    if not qi_receipt["memory_continuity_visible"]:
        blockers.append("qi_memory_continuity_not_visible")
    if not qi_receipt["transition_continuity_visible"]:
        blockers.append("qi_transition_continuity_not_visible")

    replay = build_qi_memoryos_process_tensor_retrieval_replay(
        memory_entries=memory_entries,
        replay_context={
            "request_memory_write": False,
            "request_memory_overwrite": False,
            "request_world_update": False,
            "request_scheduler_mutation": False,
            "request_probe_execution": False,
        },
    ).to_dict()
    memory_genesis = len(list(memory_entries)) == 0
    if memory_genesis:
        warnings.append("memoryos_genesis_episode")
    elif replay["replay_status"] != "QI_MEMORYOS_PROCESS_TENSOR_RETRIEVAL_REPLAY_READY":
        blockers.append("memoryos_replay_not_ready")

    status, belief_route, plan_route = _routes(
        str(verification_receipt["status"]), qi_state
    )
    if blockers:
        status = "blocked"
        belief_route = "hold"
        plan_route = "hold"

    assignments = _build_credit_assignments(
        plan=semantic_plan,
        verification=verification_receipt,
        qi_state=qi_state,
    )
    counterevidence = sorted(
        set(_counterevidence(verification_receipt))
        | set(str(item) for item in belief_state.get("contradiction_residues", []))
    )
    coherence_digests = _strings(
        belief_coherence_receipt_digests,
        "belief_coherence_receipt_digests",
        allow_empty=True,
    )

    belief_candidate = {
        "version": BELIEF_CANDIDATE_VERSION,
        "source_belief_state_digest": belief_state[
            "observation_belief_state_digest"
        ],
        "chart_id": belief_state["chart_id"],
        "route": belief_route,
        "claim_summary": _belief_claim_summary(belief_state),
        "belief_coherence_receipt_digests": coherence_digests,
        "counterevidence_digests": counterevidence,
        "plurality_preserved": True,
        "locality_preserved": True,
        "global_trivialization_used": False,
        "belief_release_required": True,
        "belief_released": False,
        "future_only": True,
        "memory_overwrite": False,
        "belief_release_candidate_digest": "",
    }
    belief_candidate["belief_release_candidate_digest"] = belief_candidate_digest(
        belief_candidate
    )

    plan_candidate = {
        "version": PLAN_CANDIDATE_VERSION,
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "route": plan_route,
        "credit_assignment_digests": [
            item["credit_assignment_digest"] for item in assignments
        ],
        "qi_process_tensor_reason": qi_receipt["process_tensor_reason"],
        "memory_replay_status": replay["replay_status"],
        "planos_synthesis_required": True,
        "decisionos_selection_required": True,
        "active_now": False,
        "future_only": True,
        "execution_permission": False,
        "host_license_granted": False,
        "plan_strategy_candidate_digest": "",
    }
    plan_candidate["plan_strategy_candidate_digest"] = plan_candidate_digest(
        plan_candidate
    )

    memory_candidate = {
        "version": MEMORY_CANDIDATE_VERSION,
        "episode_id": _text(episode_id, "episode_id"),
        "mission_id": contract["mission_id"],
        "chart_id": belief_state["chart_id"],
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_belief_state_digest": belief_state[
            "observation_belief_state_digest"
        ],
        "source_observe_digest": _first_digest(
            observe_envelope,
            (
                "observe_completion_receipt_digest",
                "observation_completion_digest",
                "observation_digest",
            ),
        ),
        "source_verify_digest": _first_digest(
            verify_envelope,
            (
                "verify_completion_receipt_digest",
                "verification_completion_digest",
                "verification_receipt_digest",
            ),
        ),
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "qi_process_tensor_receipt_digest": sha(qi_receipt),
        "prior_memory_replay_digest": sha(replay),
        "credit_assignment_digests": [
            item["credit_assignment_digest"] for item in assignments
        ],
        "counterevidence_digests": counterevidence,
        "process_tensor_trace_preserved": qi_receipt[
            "process_tensor_visible"
        ],
        "nonmarkov_trace_preserved": qi_receipt["nonmarkov_memory_visible"],
        "observation_debt_trace_preserved": "observation_debt" in qi_state,
        "recoverability_trace_preserved": "recovery" in qi_state
        or "recoverability" in qi_state,
        "safe_reentry_trace_preserved": True,
        "lineage_preserved": True,
        "append_only": True,
        "memory_append_requested": status != "blocked",
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "memory_delete_performed": False,
        "world_update_performed": False,
        "memory_append_candidate_digest": "",
    }
    memory_candidate["memory_append_candidate_digest"] = memory_candidate_digest(
        memory_candidate
    )

    receipt = {
        "version": RECEIPT_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_belief_state_digest": belief_state[
            "observation_belief_state_digest"
        ],
        "source_plan_digest": semantic_plan["semantic_plan_digest"],
        "source_verification_digest": verification_receipt[
            "verification_receipt_digest"
        ],
        "chart_id": belief_state["chart_id"],
        "episode_id": memory_candidate["episode_id"],
        "consolidator_id": _text(consolidator_id, "consolidator_id"),
        "status": status,
        "observe_envelope_digest": sha(observe_envelope),
        "verify_envelope_digest": sha(verify_envelope),
        "qi_process_tensor_receipt": qi_receipt,
        "memoryos_retrieval_replay": replay,
        "memory_genesis": memory_genesis,
        "credit_assignments": assignments,
        "belief_release_candidate": belief_candidate,
        "plan_strategy_candidate": plan_candidate,
        "memory_append_candidate": memory_candidate,
        "counterevidence_digests": counterevidence,
        "blockers": blockers,
        "warnings": warnings,
        "automatic_learning": False,
        "belief_released": False,
        "plan_activated": False,
        "execution_performed": False,
        "memory_overwrite_performed": False,
        "consolidated_at_ms": _nonnegative_int(
            consolidated_at_ms, "consolidated_at_ms"
        ),
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "cognitive_memory_consolidation_digest": "",
    }
    receipt["cognitive_memory_consolidation_digest"] = consolidation_digest(receipt)
    receipt_errors = validate_cognitive_memory_consolidation_static(receipt)
    if receipt_errors:
        raise ValueError(";".join(receipt_errors))
    return receipt


def validate_credit_assignment_static(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if packet.get("version") != CREDIT_VERSION:
        errors.append("credit_version_invalid")
    for field in (
        "step_id",
        "plan_step_digest",
        "source_plan_digest",
        "source_verification_digest",
        "attribution_class",
    ):
        if not str(packet.get(field, "")).strip():
            errors.append(f"credit_{field}_missing")
    try:
        _bounded(packet.get("temporal_weight"), "temporal_weight", lower=0.0, upper=1.0)
        _bounded(packet.get("criterion_coverage"), "criterion_coverage", lower=0.0, upper=1.0)
        _bounded(
            packet.get("verification_confidence"),
            "verification_confidence",
            lower=0.0,
            upper=1.0,
        )
        _bounded(packet.get("signed_credit"), "signed_credit", lower=-1.0, upper=1.0)
    except ValueError as exc:
        errors.append(str(exc))
    if packet.get("causal_claim") is not False:
        errors.append("credit_causal_claim_forbidden")
    if packet.get("future_only") is not True:
        errors.append("credit_future_only_missing")
    if packet.get("active_now") is not False:
        errors.append("credit_active_now_forbidden")
    if packet.get("credit_assignment_digest") != credit_digest(packet):
        errors.append("credit_digest_invalid")
    return errors


def validate_cognitive_memory_consolidation_static(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != RECEIPT_VERSION:
        errors.append("consolidation_version_invalid")
    if receipt.get("status") not in CONSOLIDATION_STATUSES:
        errors.append("consolidation_status_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "contract_digest",
        "source_mission_state_digest",
        "source_belief_state_digest",
        "source_plan_digest",
        "source_verification_digest",
        "chart_id",
        "episode_id",
        "consolidator_id",
        "observe_envelope_digest",
        "verify_envelope_digest",
    ):
        if not str(receipt.get(field, "")).strip():
            errors.append(f"consolidation_{field}_missing")
    assignments = receipt.get("credit_assignments")
    if not isinstance(assignments, list) or not assignments:
        errors.append("consolidation_credit_assignments_missing")
    else:
        for assignment in assignments:
            errors.extend(
                "credit:" + item
                for item in validate_credit_assignment_static(assignment)
            )
    belief_candidate = receipt.get("belief_release_candidate")
    if not isinstance(belief_candidate, Mapping):
        errors.append("belief_candidate_missing")
    else:
        if belief_candidate.get("route") not in BELIEF_ROUTES:
            errors.append("belief_candidate_route_invalid")
        if belief_candidate.get("belief_released") is not False:
            errors.append("belief_candidate_release_forbidden")
        if belief_candidate.get("memory_overwrite") is not False:
            errors.append("belief_candidate_memory_overwrite_forbidden")
        if belief_candidate.get("belief_release_candidate_digest") != belief_candidate_digest(
            belief_candidate
        ):
            errors.append("belief_candidate_digest_invalid")
    plan_candidate = receipt.get("plan_strategy_candidate")
    if not isinstance(plan_candidate, Mapping):
        errors.append("plan_candidate_missing")
    else:
        if plan_candidate.get("route") not in PLAN_ROUTES:
            errors.append("plan_candidate_route_invalid")
        if plan_candidate.get("planos_synthesis_required") is not True:
            errors.append("planos_synthesis_requirement_missing")
        if plan_candidate.get("decisionos_selection_required") is not True:
            errors.append("decisionos_selection_requirement_missing")
        if plan_candidate.get("active_now") is not False:
            errors.append("plan_candidate_active_now_forbidden")
        if plan_candidate.get("execution_permission") is not False:
            errors.append("plan_candidate_execution_permission_forbidden")
        if plan_candidate.get("plan_strategy_candidate_digest") != plan_candidate_digest(
            plan_candidate
        ):
            errors.append("plan_candidate_digest_invalid")
    memory_candidate = receipt.get("memory_append_candidate")
    if not isinstance(memory_candidate, Mapping):
        errors.append("memory_candidate_missing")
    else:
        if memory_candidate.get("append_only") is not True:
            errors.append("memory_candidate_append_only_missing")
        if memory_candidate.get("memory_append_performed") is not False:
            errors.append("memory_candidate_precommit_append_forbidden")
        if memory_candidate.get("memory_overwrite_performed") is not False:
            errors.append("memory_candidate_overwrite_forbidden")
        if memory_candidate.get("memory_append_candidate_digest") != memory_candidate_digest(
            memory_candidate
        ):
            errors.append("memory_candidate_digest_invalid")
    if receipt.get("automatic_learning") is not False:
        errors.append("automatic_learning_forbidden")
    if receipt.get("belief_released") is not False:
        errors.append("consolidation_belief_release_forbidden")
    if receipt.get("plan_activated") is not False:
        errors.append("consolidation_plan_activation_forbidden")
    if receipt.get("execution_performed") is not False:
        errors.append("consolidation_execution_forbidden")
    if receipt.get("memory_overwrite_performed") is not False:
        errors.append("consolidation_memory_overwrite_forbidden")
    try:
        _nonnegative_int(receipt.get("consolidated_at_ms"), "consolidated_at_ms")
    except ValueError as exc:
        errors.append(str(exc))
    if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("consolidation_non_authority_invalid")
    if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("consolidation_boundary_invalid")
    if receipt.get("cognitive_memory_consolidation_digest") != consolidation_digest(
        receipt
    ):
        errors.append("consolidation_digest_invalid")
    return errors


__all__ = [
    "BELIEF_CANDIDATE_VERSION",
    "BELIEF_ROUTES",
    "CONSOLIDATION_STATUSES",
    "CREDIT_VERSION",
    "MEMORY_CANDIDATE_VERSION",
    "NON_AUTHORITY",
    "PLAN_CANDIDATE_VERSION",
    "PLAN_ROUTES",
    "RECEIPT_VERSION",
    "REQUIRED_BOUNDARY",
    "VERSION",
    "belief_candidate_digest",
    "build_cognitive_memory_consolidation",
    "consolidation_digest",
    "credit_digest",
    "memory_candidate_digest",
    "plan_candidate_digest",
    "validate_cognitive_memory_consolidation_static",
    "validate_credit_assignment_static",
]
