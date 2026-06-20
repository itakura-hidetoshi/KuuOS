from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from runtime.kuuos_belief_os_context_transport_types_v0_2 import (
    NON_AUTHORITY_FLAGS as BELIEF_TRANSPORT_NON_AUTHORITY,
    RECEIPT_VERSION as BELIEF_TRANSPORT_RECEIPT_VERSION,
    receipt_digest as belief_transport_receipt_digest,
)
from runtime.kuuos_belief_os_kernel_v0_1 import build_belief_event, validate_belief_state
from runtime.kuuos_goal_portfolio_v0_20 import (
    validate_goal_portfolio,
    validate_goal_proposal,
)
from runtime.kuuos_mission_contract_types_v0_20 import sha, validate_mission_contract
from runtime.kuuos_mission_state_v0_20 import validate_mission_state
from runtime.kuuos_observation_belief_state_kernel_v0_21 import (
    build_observation,
    validate_belief_state as validate_epistemic_belief_state,
    validate_observation,
)
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_semantic_planner_verifier_kernel_v0_22 import (
    build_verification_receipt,
    validate_semantic_plan,
    validate_semantic_plan_static,
    validate_verification_receipt_static,
)

VERSION = "kuuos_belief_observe_grounded_cognition_bridge_v0_22_1"
BELIEF_BASIS_VERSION = "kuuos_belief_os_planning_basis_receipt_v0_22_1"
PLAN_BUNDLE_VERSION = "kuuos_belief_grounded_semantic_plan_bundle_v0_22_1"
OBSERVE_ADAPTER_VERSION = "kuuos_observe_os_epistemic_adapter_receipt_v0_22_1"
VERIFICATION_BUNDLE_VERSION = "kuuos_observe_grounded_verification_bundle_v0_22_1"
TRACE_PROPOSAL_VERSION = "kuuos_observe_to_belief_trace_proposal_v0_22_1"

OBSERVE_ROUTE_TO_RELATION = {
    "OBSERVATION_MATCHED": "supports",
    "OBSERVATION_DIVERGENT": "opposes",
    "OBSERVATION_INCONCLUSIVE": "unknown",
    "OBSERVATION_CONFLICTED": "unknown",
}
OBSERVE_ROUTE_TO_CRITERION_STATUS = {
    "OBSERVATION_MATCHED": "satisfied",
    "OBSERVATION_DIVERGENT": "contradicted",
    "OBSERVATION_INCONCLUSIVE": "unknown",
    "OBSERVATION_CONFLICTED": "unknown",
}

NON_AUTHORITY = {
    "grants_truth_authority": False,
    "grants_execution_authority": False,
    "grants_tool_authority": False,
    "grants_network_authority": False,
    "grants_shell_authority": False,
    "grants_verification_authority": False,
    "grants_mission_transition_authority": False,
    "grants_memory_overwrite_authority": False,
    "grants_self_modification_authority": False,
}

REQUIRED_BOUNDARY = {
    "belief_os_is_conditional_planning_support": True,
    "belief_os_is_not_truth_authority": True,
    "credal_interval_and_counterevidence_are_preserved": True,
    "context_transport_is_local_and_declared_path_only": True,
    "observe_os_requires_effect_grounding": True,
    "observe_os_comparison_is_not_verification": True,
    "observe_os_does_not_update_belief_automatically": True,
    "observe_os_does_not_complete_plan_automatically": True,
    "planner_and_observer_independence_is_required": True,
    "verification_remains_verify_os_owned": True,
    "belief_activation_remains_replan_only": True,
    "memory_overwrite_is_forbidden": True,
}


def _without(value: Mapping[str, Any], field: str) -> dict[str, Any]:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return packet


def belief_basis_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "belief_planning_basis_receipt_digest"))


def plan_bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "belief_grounded_plan_bundle_digest"))


def observe_adapter_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observe_adapter_receipt_digest"))


def verification_bundle_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observe_grounded_verification_bundle_digest"))


def trace_proposal_digest(value: Mapping[str, Any]) -> str:
    return sha(_without(value, "observe_to_belief_trace_proposal_digest"))


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


def _unique_strings(
    values: Sequence[Any], name: str, *, allow_empty: bool = False
) -> list[str]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name}_invalid")
    result = [_text(item, name) for item in values]
    if not allow_empty and not result:
        raise ValueError(f"{name}_missing")
    if len(result) != len(set(result)):
        raise ValueError(f"{name}_duplicate")
    return result


def _source_errors(
    contract: Mapping[str, Any], mission_state: Mapping[str, Any]
) -> list[str]:
    errors = ["contract:" + item for item in validate_mission_contract(contract)]
    errors.extend(
        "mission_state:" + item
        for item in validate_mission_state(mission_state, contract)
    )
    if mission_state.get("lifecycle_state") != "active":
        errors.append("mission_not_active")
    return errors


def validate_belief_transport_receipt(
    receipt: Mapping[str, Any], *, expected_lineage_id: str, expected_chart_id: str
) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != BELIEF_TRANSPORT_RECEIPT_VERSION:
        errors.append("belief_transport_receipt_version_invalid")
    if receipt.get("belief_transport_receipt_digest") != belief_transport_receipt_digest(
        receipt
    ):
        errors.append("belief_transport_receipt_digest_invalid")
    if receipt.get("lineage_id") != expected_lineage_id:
        errors.append("belief_transport_lineage_mismatch")
    if receipt.get("target_context_id") != expected_chart_id:
        errors.append("belief_transport_chart_mismatch")
    if receipt.get("route") != "CANDIDATE":
        errors.append("belief_transport_candidate_required")
    if receipt.get("planning_support_license") is not True:
        errors.append("belief_transport_planning_support_missing")
    if receipt.get("pending_replan_activation") is not True:
        errors.append("belief_transport_replan_activation_missing")
    for field in (
        "locality_preserved",
        "plurality_preserved",
        "paramartha_non_reified",
        "two_truths_separated",
        "curvature_is_not_veto",
        "cocycle_defect_is_not_prohibition",
        "holonomy_is_not_authority",
        "future_only",
    ):
        if receipt.get(field) is not True:
            errors.append(f"belief_transport_{field}_missing")
    for field in (
        "path_search_used",
        "global_chart_ranking_used",
        "universal_winner_selected",
        "memory_overwrite",
    ):
        if receipt.get(field) is not False:
            errors.append(f"belief_transport_{field}_forbidden")
    if dict(receipt.get("non_authority", {})) != BELIEF_TRANSPORT_NON_AUTHORITY:
        errors.append("belief_transport_authority_escalation")
    interval = receipt.get("aggregate_interval")
    if not isinstance(interval, Mapping):
        errors.append("belief_transport_interval_missing")
    else:
        try:
            lower = float(interval.get("lower_probability"))
            upper = float(interval.get("upper_probability"))
            width = float(interval.get("ignorance_width"))
            if not 0.0 <= lower <= upper <= 1.0:
                errors.append("belief_transport_interval_invalid")
            if abs(width - (upper - lower)) > 1e-12:
                errors.append("belief_transport_interval_width_mismatch")
        except (TypeError, ValueError):
            errors.append("belief_transport_interval_invalid")
    if not isinstance(receipt.get("counterevidence_digests"), list):
        errors.append("belief_transport_counterevidence_missing")
    return errors


def build_belief_planning_basis_receipt(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    epistemic_belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    belief_transport_receipt: Mapping[str, Any],
    created_at_ms: int,
) -> dict[str, Any]:
    errors = _source_errors(contract, mission_state)
    errors.extend(
        "epistemic_belief_state:" + item
        for item in validate_epistemic_belief_state(
            epistemic_belief_state, contract, mission_state
        )
    )
    errors.extend("goal:" + item for item in validate_goal_proposal(goal, contract))
    errors.extend(
        "goal_portfolio:" + item
        for item in validate_goal_portfolio(goal_portfolio, contract)
    )
    errors.extend(
        "belief_transport:" + item
        for item in validate_belief_transport_receipt(
            belief_transport_receipt,
            expected_lineage_id=str(contract.get("lineage_id")),
            expected_chart_id=str(epistemic_belief_state.get("chart_id")),
        )
    )
    if goal.get("goal_id") not in goal_portfolio.get("active_goal_ids", []):
        errors.append("belief_basis_goal_not_active")
    if errors:
        raise ValueError(";".join(errors))

    receipt = {
        "version": BELIEF_BASIS_VERSION,
        "mission_id": contract["mission_id"],
        "lineage_id": contract["lineage_id"],
        "contract_digest": contract["mission_contract_digest"],
        "source_mission_state_digest": mission_state["mission_state_digest"],
        "source_epistemic_belief_state_digest": epistemic_belief_state[
            "observation_belief_state_digest"
        ],
        "chart_id": epistemic_belief_state["chart_id"],
        "goal_id": goal["goal_id"],
        "goal_digest": goal["goal_digest"],
        "goal_portfolio_digest": goal_portfolio["goal_portfolio_digest"],
        "belief_transport_receipt_digest": belief_transport_receipt[
            "belief_transport_receipt_digest"
        ],
        "belief_transport_next_revision_basis_digest": belief_transport_receipt[
            "next_revision_basis_digest"
        ],
        "source_belief_state_digests": [
            str(item["source_belief_state_digest"])
            for item in belief_transport_receipt["transported_sections"]
        ],
        "aggregate_interval": deepcopy(
            dict(belief_transport_receipt["aggregate_interval"])
        ),
        "conflict_index": float(belief_transport_receipt["conflict_index"]),
        "aggregate_curvature": float(
            belief_transport_receipt["aggregate_curvature"]
        ),
        "aggregate_cocycle_defect": float(
            belief_transport_receipt["aggregate_cocycle_defect"]
        ),
        "aggregate_holonomy_residual": float(
            belief_transport_receipt["aggregate_holonomy_residual"]
        ),
        "qi_history_residual": float(
            belief_transport_receipt["qi_history_residual"]
        ),
        "evidence_digests": _unique_strings(
            belief_transport_receipt.get("evidence_digests", []),
            "belief_evidence_digests",
            allow_empty=True,
        ),
        "counterevidence_digests": _unique_strings(
            belief_transport_receipt.get("counterevidence_digests", []),
            "belief_counterevidence_digests",
            allow_empty=True,
        ),
        "route": "CANDIDATE",
        "planning_support_only": True,
        "truth_authority_granted": False,
        "execution_authority_granted": False,
        "activation_boundary": "mission_replan_only",
        "created_at_ms": _nonnegative_int(created_at_ms, "created_at_ms"),
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "belief_planning_basis_receipt_digest": "",
    }
    receipt["belief_planning_basis_receipt_digest"] = belief_basis_digest(receipt)
    return receipt


def validate_belief_planning_basis_receipt_static(
    receipt: Mapping[str, Any]
) -> list[str]:
    errors: list[str] = []
    if receipt.get("version") != BELIEF_BASIS_VERSION:
        errors.append("belief_basis_version_invalid")
    for field in (
        "mission_id",
        "lineage_id",
        "contract_digest",
        "source_mission_state_digest",
        "source_epistemic_belief_state_digest",
        "chart_id",
        "goal_id",
        "goal_digest",
        "goal_portfolio_digest",
        "belief_transport_receipt_digest",
        "belief_transport_next_revision_basis_digest",
    ):
        if not str(receipt.get(field, "")).strip():
            errors.append(f"belief_basis_{field}_missing")
    if receipt.get("route") != "CANDIDATE":
        errors.append("belief_basis_candidate_required")
    if receipt.get("planning_support_only") is not True:
        errors.append("belief_basis_support_boundary_missing")
    if receipt.get("truth_authority_granted") is not False:
        errors.append("belief_basis_truth_authority_forbidden")
    if receipt.get("execution_authority_granted") is not False:
        errors.append("belief_basis_execution_authority_forbidden")
    if receipt.get("activation_boundary") != "mission_replan_only":
        errors.append("belief_basis_activation_boundary_invalid")
    if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
        errors.append("belief_basis_non_authority_invalid")
    if dict(receipt.get("boundary", {})) != REQUIRED_BOUNDARY:
        errors.append("belief_basis_boundary_invalid")
    if receipt.get("belief_planning_basis_receipt_digest") != belief_basis_digest(
        receipt
    ):
        errors.append("belief_basis_digest_invalid")
    return errors


def build_belief_grounded_plan_bundle(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    epistemic_belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    semantic_plan: Mapping[str, Any],
    belief_basis_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    errors = validate_semantic_plan(
        semantic_plan,
        contract,
        mission_state,
        epistemic_belief_state,
        goal,
        goal_portfolio,
    )
    errors.extend(
        "belief_basis:" + item
        for item in validate_belief_planning_basis_receipt_static(
            belief_basis_receipt
        )
    )
    expected = {
        "mission_id": semantic_plan.get("mission_id"),
        "lineage_id": semantic_plan.get("lineage_id"),
        "contract_digest": semantic_plan.get("contract_digest"),
        "source_mission_state_digest": semantic_plan.get(
            "source_mission_state_digest"
        ),
        "source_epistemic_belief_state_digest": semantic_plan.get(
            "source_belief_state_digest"
        ),
        "chart_id": semantic_plan.get("chart_id"),
        "goal_id": semantic_plan.get("goal_id"),
        "goal_digest": semantic_plan.get("goal_digest"),
        "goal_portfolio_digest": semantic_plan.get("goal_portfolio_digest"),
    }
    for field, value in expected.items():
        if belief_basis_receipt.get(field) != value:
            errors.append(f"belief_grounded_plan_{field}_mismatch")
    if semantic_plan.get("status") != "ready":
        errors.append("belief_grounded_plan_not_ready")
    if errors:
        raise ValueError(";".join(errors))
    bundle = {
        "version": PLAN_BUNDLE_VERSION,
        "mission_id": semantic_plan["mission_id"],
        "contract_digest": semantic_plan["contract_digest"],
        "chart_id": semantic_plan["chart_id"],
        "goal_id": semantic_plan["goal_id"],
        "semantic_plan_digest": semantic_plan["semantic_plan_digest"],
        "belief_planning_basis_receipt_digest": belief_basis_receipt[
            "belief_planning_basis_receipt_digest"
        ],
        "belief_transport_receipt_digest": belief_basis_receipt[
            "belief_transport_receipt_digest"
        ],
        "route": "BELIEF_GROUNDED_PLAN_CANDIDATE",
        "effect_authority_granted": False,
        "verification_required_after_effect": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "belief_grounded_plan_bundle_digest": "",
    }
    bundle["belief_grounded_plan_bundle_digest"] = plan_bundle_digest(bundle)
    return bundle


def _observe_confidence(state: Mapping[str, Any]) -> float:
    quality = state.get("quality_report")
    if not isinstance(quality, Mapping):
        raise ValueError("observe_quality_report_missing")
    values = [
        float(quality.get("coverage")),
        float(quality.get("freshness")),
        float(quality.get("provenance")),
        float(quality.get("calibration")),
        float(quality.get("completeness")),
        1.0 - float(quality.get("conflict")),
    ]
    return max(0.0, min(1.0, min(values)))


def adapt_observe_state_to_epistemic_observation(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    observe_state: Mapping[str, Any],
    chart_id: str,
    claim_id: str,
    proposition: str,
    planner_id: str,
    valid_until_ms: int,
) -> dict[str, Any]:
    errors = _source_errors(contract, mission_state)
    errors.extend("observe_state:" + item for item in validate_observe_state(observe_state))
    if observe_state.get("current_phase") != "commit":
        errors.append("observe_state_not_committed")
    if observe_state.get("observation_recorded") is not True:
        errors.append("observe_state_not_recorded")
    route = str(observe_state.get("route", ""))
    if route not in OBSERVE_ROUTE_TO_RELATION:
        errors.append("observe_route_not_adaptable")
    if observe_state.get("mission_contract_digest") != contract.get(
        "mission_contract_digest"
    ):
        errors.append("observe_contract_mismatch")
    if observe_state.get("lineage_id") != contract.get("lineage_id"):
        errors.append("observe_lineage_mismatch")
    if observe_state.get("automatic_belief_update") is not False:
        errors.append("observe_automatic_belief_update_forbidden")
    if observe_state.get("automatic_plan_completion") is not False:
        errors.append("observe_automatic_plan_completion_forbidden")
    if observe_state.get("verification_required") is not True:
        errors.append("observe_verification_debt_lost")
    evidence_items = observe_state.get("evidence_items")
    if not isinstance(evidence_items, list) or not evidence_items:
        errors.append("observe_evidence_items_missing")
    planner = _text(planner_id, "planner_id")
    independent_sources: list[str] = []
    collectors: list[str] = []
    evidence_digests: list[str] = []
    observed_at = 0
    if isinstance(evidence_items, list):
        for item in evidence_items:
            if not isinstance(item, Mapping):
                errors.append("observe_evidence_item_invalid")
                continue
            independent_sources.append(str(item.get("independent_source_id", "")))
            collectors.append(str(item.get("collector_id", "")))
            evidence_digests.append(str(item.get("evidence_digest", "")))
            observed_at = max(observed_at, int(item.get("collected_at_ms", 0)))
    if planner in set(independent_sources) or planner in set(collectors):
        errors.append("planner_observer_independence_violated")
    if not all(independent_sources) or not all(collectors) or not all(evidence_digests):
        errors.append("observe_independent_provenance_incomplete")
    if len(set(independent_sources)) < 1:
        errors.append("observe_independent_source_missing")
    if errors:
        raise ValueError(";".join(errors))

    provenance = []
    for digest_value in evidence_digests + [
        str(observe_state["source_act_state_digest"]),
        str(observe_state["host_receipt_digest"]),
        str(observe_state["comparison_receipt_digest"]),
        str(observe_state["observe_state_digest"]),
    ]:
        if digest_value and digest_value not in provenance:
            provenance.append(digest_value)
    source_identity = "observeos:" + sha(
        {
            "observe_id": observe_state["observe_id"],
            "independent_sources": sorted(set(independent_sources)),
            "collectors": sorted(set(collectors)),
        }
    )
    observation = build_observation(
        contract=contract,
        mission_state=mission_state,
        observation_id="observeos-" + str(observe_state["observe_id"]),
        chart_id=_text(chart_id, "chart_id"),
        claim_id=_text(claim_id, "claim_id"),
        proposition=_text(proposition, "proposition"),
        relation=OBSERVE_ROUTE_TO_RELATION[route],
        source_id=source_identity,
        source_kind="system",
        raw_artifact_digest=str(observe_state["evidence_packet_digest"]),
        provenance_digests=provenance,
        observed_at_ms=observed_at,
        valid_until_ms=_nonnegative_int(valid_until_ms, "valid_until_ms"),
        confidence=_observe_confidence(observe_state),
        inference_rule_digest=sha(
            {
                "bridge_version": VERSION,
                "observe_route": route,
                "relation": OBSERVE_ROUTE_TO_RELATION[route],
                "comparison_is_not_verification": True,
            }
        ),
    )
    observation_errors = validate_observation(observation, contract, mission_state)
    if observation_errors:
        raise ValueError("adapted_observation:" + ";".join(observation_errors))
    return observation


def build_observe_adapter_receipt(
    *,
    observe_state: Mapping[str, Any],
    adapted_observation: Mapping[str, Any],
    planner_id: str,
) -> dict[str, Any]:
    errors = validate_observe_state(observe_state)
    if errors:
        raise ValueError("observe_state:" + ";".join(errors))
    if adapted_observation.get("raw_artifact_digest") != observe_state.get(
        "evidence_packet_digest"
    ):
        raise ValueError("observe_adapter_artifact_binding_mismatch")
    if adapted_observation.get("chart_id") == "":
        raise ValueError("observe_adapter_chart_missing")
    if adapted_observation.get("source_id") == planner_id:
        raise ValueError("observe_adapter_planner_source_forbidden")
    receipt = {
        "version": OBSERVE_ADAPTER_VERSION,
        "observe_id": observe_state["observe_id"],
        "observe_state_digest": observe_state["observe_state_digest"],
        "source_act_state_digest": observe_state["source_act_state_digest"],
        "host_receipt_digest": observe_state["host_receipt_digest"],
        "evidence_packet_digest": observe_state["evidence_packet_digest"],
        "comparison_receipt_digest": observe_state["comparison_receipt_digest"],
        "observe_route": observe_state["route"],
        "adapted_observation_digest": adapted_observation["observation_digest"],
        "adapted_relation": adapted_observation["relation"],
        "adapted_confidence": adapted_observation["confidence"],
        "planner_id": _text(planner_id, "planner_id"),
        "observer_source_id": adapted_observation["source_id"],
        "effect_grounded": True,
        "comparison_is_not_verification": True,
        "automatic_belief_update": False,
        "automatic_plan_completion": False,
        "verification_required": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "observe_adapter_receipt_digest": "",
    }
    receipt["observe_adapter_receipt_digest"] = observe_adapter_digest(receipt)
    return receipt


def build_observe_grounded_verification_bundle(
    *,
    contract: Mapping[str, Any],
    mission_state: Mapping[str, Any],
    source_epistemic_belief_state: Mapping[str, Any],
    goal: Mapping[str, Any],
    goal_portfolio: Mapping[str, Any],
    semantic_plan: Mapping[str, Any],
    verifier_id: str,
    criterion_bindings: Sequence[Mapping[str, Any]],
    execution_receipt_digests: Sequence[str],
    observed_at_ms: int,
    valid_until_ms: int,
) -> dict[str, Any]:
    plan_errors = validate_semantic_plan(
        semantic_plan,
        contract,
        mission_state,
        source_epistemic_belief_state,
        goal,
        goal_portfolio,
    )
    if plan_errors:
        raise ValueError("semantic_plan:" + ";".join(plan_errors))
    observations: list[dict[str, Any]] = []
    assessments: list[dict[str, Any]] = []
    adapter_receipts: list[dict[str, Any]] = []
    for binding in criterion_bindings:
        criterion = _text(binding.get("criterion"), "criterion")
        observe_state = binding.get("observe_state")
        if not isinstance(observe_state, Mapping):
            raise ValueError("criterion_observe_state_missing")
        observation = adapt_observe_state_to_epistemic_observation(
            contract=contract,
            mission_state=mission_state,
            observe_state=observe_state,
            chart_id=str(semantic_plan["chart_id"]),
            claim_id=_text(binding.get("claim_id"), "claim_id"),
            proposition=_text(binding.get("proposition"), "proposition"),
            planner_id=str(semantic_plan["planner_id"]),
            valid_until_ms=valid_until_ms,
        )
        observations.append(observation)
        adapter_receipts.append(
            build_observe_adapter_receipt(
                observe_state=observe_state,
                adapted_observation=observation,
                planner_id=str(semantic_plan["planner_id"]),
            )
        )
        route = str(observe_state["route"])
        status = OBSERVE_ROUTE_TO_CRITERION_STATUS[route]
        assessments.append(
            {
                "criterion": criterion,
                "status": status,
                "confidence": observation["confidence"],
                "evidence_observation_digests": [observation["observation_digest"]],
                "notes": "ObserveOS effect-grounded comparison adapted for independent verifier assessment",
            }
        )
    receipt = build_verification_receipt(
        contract=contract,
        mission_state=mission_state,
        source_belief_state=source_epistemic_belief_state,
        goal=goal,
        goal_portfolio=goal_portfolio,
        plan=semantic_plan,
        verifier_id=_text(verifier_id, "verifier_id"),
        independent_observations=observations,
        criterion_assessments=assessments,
        execution_receipt_digests=execution_receipt_digests,
        observed_at_ms=_nonnegative_int(observed_at_ms, "observed_at_ms"),
    )
    receipt_errors = validate_verification_receipt_static(receipt)
    if receipt_errors:
        raise ValueError("verification_receipt:" + ";".join(receipt_errors))
    bundle = {
        "version": VERIFICATION_BUNDLE_VERSION,
        "mission_id": contract["mission_id"],
        "contract_digest": contract["mission_contract_digest"],
        "semantic_plan_digest": semantic_plan["semantic_plan_digest"],
        "verification_receipt_digest": receipt["verification_receipt_digest"],
        "observe_adapter_receipt_digests": [
            item["observe_adapter_receipt_digest"] for item in adapter_receipts
        ],
        "adapted_observation_digests": [
            item["observation_digest"] for item in observations
        ],
        "verification_status": receipt["status"],
        "effect_grounded": True,
        "comparison_is_not_verification": True,
        "verify_os_decision_required": True,
        "mission_transition_authority_granted": False,
        "verification_receipt": receipt,
        "adapted_observations": observations,
        "adapter_receipts": adapter_receipts,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "observe_grounded_verification_bundle_digest": "",
    }
    bundle["observe_grounded_verification_bundle_digest"] = (
        verification_bundle_digest(bundle)
    )
    return bundle


def build_observe_to_belief_trace_proposal(
    *,
    belief_state: Mapping[str, Any],
    adapted_observation: Mapping[str, Any],
    observe_adapter_receipt: Mapping[str, Any],
    now_ms: int,
) -> dict[str, Any]:
    belief_errors = validate_belief_state(belief_state)
    if belief_errors:
        raise ValueError("belief_state:" + ";".join(belief_errors))
    if belief_state.get("current_phase") != "contextualize":
        raise ValueError("belief_trace_requires_contextualized_state")
    if belief_state.get("lineage_id") != adapted_observation.get("lineage_id"):
        raise ValueError("belief_observation_lineage_mismatch")
    if observe_adapter_receipt.get("adapted_observation_digest") != adapted_observation.get(
        "observation_digest"
    ):
        raise ValueError("belief_trace_adapter_binding_mismatch")
    event = build_belief_event(
        state=belief_state,
        target_phase="trace",
        artifact_digest=str(observe_adapter_receipt["observe_adapter_receipt_digest"]),
        payload={
            "evidence_digests": list(adapted_observation["provenance_digests"]),
            "observation_digests": [adapted_observation["observation_digest"]],
            "verification_receipt_digests": [],
            "causal_support_digests": [],
        },
        now_ms=_nonnegative_int(now_ms, "now_ms"),
    )
    proposal = {
        "version": TRACE_PROPOSAL_VERSION,
        "belief_id": belief_state["belief_id"],
        "belief_state_digest": belief_state["belief_state_digest"],
        "adapted_observation_digest": adapted_observation["observation_digest"],
        "observe_adapter_receipt_digest": observe_adapter_receipt[
            "observe_adapter_receipt_digest"
        ],
        "belief_event": event,
        "automatic_apply": False,
        "future_only": True,
        "memory_overwrite": False,
        "non_authority": deepcopy(NON_AUTHORITY),
        "boundary": deepcopy(REQUIRED_BOUNDARY),
        "observe_to_belief_trace_proposal_digest": "",
    }
    proposal["observe_to_belief_trace_proposal_digest"] = trace_proposal_digest(
        proposal
    )
    return proposal


__all__ = [
    "BELIEF_BASIS_VERSION",
    "OBSERVE_ADAPTER_VERSION",
    "PLAN_BUNDLE_VERSION",
    "REQUIRED_BOUNDARY",
    "TRACE_PROPOSAL_VERSION",
    "VERIFICATION_BUNDLE_VERSION",
    "VERSION",
    "adapt_observe_state_to_epistemic_observation",
    "belief_basis_digest",
    "build_belief_grounded_plan_bundle",
    "build_belief_planning_basis_receipt",
    "build_observe_adapter_receipt",
    "build_observe_grounded_verification_bundle",
    "build_observe_to_belief_trace_proposal",
    "observe_adapter_digest",
    "plan_bundle_digest",
    "trace_proposal_digest",
    "validate_belief_planning_basis_receipt_static",
    "validate_belief_transport_receipt",
    "verification_bundle_digest",
]
