from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_decision_os_kernel_v0_1 import (
    build_initial_decision_state,
    validate_decision_state,
)
from runtime.kuuos_decision_os_plural_kernel_v0_2 import validate_plural_state
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_wa_kernel_v0_3 import validate_wa_state
from runtime.kuuos_plan_os_replan_fixture_v0_2 import candidate, standard_checks
from runtime.kuuos_plan_os_replan_kernel_v0_2 import (
    build_decision_receipt,
    build_history_packet,
    build_initial_replan_state,
    build_qi_condition_packet,
    build_replan_event,
    build_synthesis_packet,
    validate_replan_state,
)
from runtime.kuuos_plan_os_replan_store_v0_2 import ReplanStore
from runtime.kuuos_plan_os_replan_types_v0_2 import copy_non_authority
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    _build_plural,
    _build_wa,
    build_native_full_cycle_receipt,
    validate_native_full_cycle_receipt,
)
from runtime.v01_decision_os_relational_deliberation import (
    THRESHOLDS,
    WEIGHTS,
    _challenge,
    _complete_cycle,
    _middle,
    _option,
)

VERSION = "kuuos_qi_world_native_generational_replan_v1_4"
RECEIPT_VERSION = "kuuos_qi_world_native_generational_replan_receipt_v1_4"
CYCLE_ID = "qi-world-native-generational-replan-v14"

NON_AUTHORITY = {
    "adapter_grants_execution": False,
    "adapter_grants_truth": False,
    "adapter_issues_authority": False,
    "adapter_activates_next_plan": False,
    "adapter_updates_exact_world": False,
    "adapter_overwrites_history": False,
    "qi_grants_execution": False,
    "world_projection_grants_truth": False,
}


def _digest(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest(value, "native_generational_replan_receipt_digest")


def _apply(
    store: ReplanStore,
    state: Mapping[str, Any],
    phase: str,
    payload: Mapping[str, Any],
    tick: int,
) -> dict[str, Any]:
    event = build_replan_event(
        state=state,
        target_phase=phase,
        artifact_digest=sha({"phase": phase, "payload": dict(payload), "tick": tick}),
        payload=payload,
        now_ms=410_000 + tick,
    )
    result = store.apply(event)
    if result.get("status") != "APPLIED":
        raise ValueError("v14_replan_apply_failed:" + ";".join(result.get("errors", [])))
    return dict(result["state"])


def _source_surfaces(source: Mapping[str, Any]) -> tuple[dict, dict, list[dict]]:
    interface = dict(source["qi_world_os_interface_receipt"])
    world = deepcopy(dict(interface["world_projection"]))
    qi = deepcopy(dict(interface["qi_process_receipt"]))
    raw = dict(qi.get("enriched_state", {})).get("process_history", [])
    history = [deepcopy(dict(item)) for item in raw if isinstance(item, Mapping)]
    if not history:
        raise ValueError("v14_source_qi_history_missing")
    return world, qi, history


def _candidates() -> list[dict[str, Any]]:
    return [
        candidate(
            "strengthen-evidence",
            "strengthen",
            target_scope="belief_candidate",
            cost=0.20,
            risk=0.12,
            transition_distance=0.18,
            switch_benefit=0.78,
        ),
        candidate(
            "continue-current",
            "continue",
            target_scope="belief_candidate",
            cost=0.08,
            risk=0.10,
            transition_distance=0.05,
            switch_benefit=0.50,
        ),
        candidate(
            "hold-safe",
            "hold",
            target_scope="no_change",
            cost=0.00,
            risk=0.00,
            transition_distance=0.00,
            switch_benefit=0.00,
        ),
    ]


def _decision(
    root: Path,
    source: Mapping[str, Any],
    replan: Mapping[str, Any],
    world: Mapping[str, Any],
    qi: Mapping[str, Any],
) -> dict[str, Any]:
    native = dict(source["native_artifacts"])
    plan = dict(native["PlanOS"])
    belief = dict(native["BeliefOSReceipt"])
    store = DecisionStore(root)
    state = store.initialize(
        build_initial_decision_state(
            decision_id="native-generational-replan-decision",
            lineage_id=str(plan["lineage_id"]),
            mission_contract_digest=str(plan["mission_contract_digest"]),
            mission_state_digest=sha(
                {
                    "source_replan_state_digest": replan["replan_state_digest"],
                    "source_learning_delta_digest": replan[
                        "source_learning_delta_digest"
                    ],
                }
            ),
            source_belief_receipt_digest=str(
                belief["belief_gerbe_receipt_digest"]
            ),
            decision_context_digest=sha(
                {
                    "replan": replan["replan_state_digest"],
                    "qi": sha(qi),
                    "world": world["world_projection_digest"],
                    "candidates": replan["candidate_field_digest"],
                    "constraints": replan["constraint_field_digest"],
                }
            ),
            decision_budget=1.0,
            weights=WEIGHTS,
            thresholds=THRESHOLDS,
            now_ms=1_000,
        )
    )
    evidence = str(replan["source_learning_delta_digest"])
    options = [
        _option(
            option_id="strengthen-evidence",
            action_class="exploit",
            positive=(0.86, 0.94),
            negative=(0.04, 0.10),
            information_gain=(0.30, 0.45),
            estimated_cost=0.20,
            estimated_risk=0.12,
            recoverability=0.90,
            reversibility=0.85,
            required_evidence=[evidence],
            available_evidence=[evidence],
        ),
        _option(
            option_id="continue-current",
            action_class="exploit",
            positive=(0.62, 0.72),
            negative=(0.12, 0.20),
            information_gain=(0.20, 0.30),
            estimated_cost=0.08,
            estimated_risk=0.10,
            recoverability=0.88,
            reversibility=0.85,
            required_evidence=[evidence],
            available_evidence=[evidence],
        ),
        _option(
            option_id="hold-safe",
            action_class="hold",
            positive=(0.42, 0.55),
            negative=(0.02, 0.06),
            information_gain=(0.10, 0.18),
            estimated_cost=0.0,
            estimated_risk=0.0,
            recoverability=0.95,
            reversibility=0.95,
        ),
    ]
    committed, _ = _complete_cycle(
        store,
        state,
        options=options,
        challenge=_challenge(),
        middle_way=_middle(),
        tick_base=10,
        requested_route="SELECT_CANDIDATE",
    )
    if committed.get("selected_option_id") != "strengthen-evidence":
        raise ValueError("v14_unexpected_decision_selection")
    return committed


def _native_replan(
    root: Path,
    source: Mapping[str, Any],
    world: Mapping[str, Any],
    qi: Mapping[str, Any],
    history: list[dict],
) -> tuple[dict, dict, dict, dict]:
    native = dict(source["native_artifacts"])
    plan = dict(native["PlanOS"])
    learn = dict(native["LearnOS"])
    store = ReplanStore(root / "plan-replan")
    state = store.initialize(
        build_initial_replan_state(
            replan_id="native-generational-replan",
            current_plan_state=plan,
            learn_state=learn,
            current_cycle_index=1,
            plan_budget=2.0,
            maximum_candidate_risk=0.50,
            base_switch_threshold=0.10,
            now_ms=400_000,
        )
    )
    packet = build_history_packet(
        state=state,
        previous_plan_change_digests=[],
        successful_transition_digests=[native["VerifyOS"]["verify_state_digest"]],
        failed_transition_digests=[],
        oscillation_history_digests=[],
        recovery_history_digests=[learn["middle_way_report_digest"]],
        stagnation_history_digests=[],
        action_history_digest=native["ActOS"]["act_state_digest"],
        observation_history_digest=native["ObserveOS"]["observe_state_digest"],
        verification_history_digest=native["VerifyOS"]["verify_state_digest"],
        learning_history_digest=learn["learn_state_digest"],
        history_window=len(history),
        path_dependence_digest=sha(history),
    )
    state = _apply(store, state, "history", {"history_packet": packet}, 1)
    qi_packet = build_qi_condition_packet(
        state=state,
        process_tensor_digest=sha(qi),
        process_history_digest=sha(history),
        activation=0.55,
        stagnation=0.15,
        tension=0.20,
        recovery=0.80,
        coherence=0.82,
        coupling=0.72,
        transition_readiness=0.84,
        local_global_balance=0.75,
        observation_debt=0.00,
        hysteresis=0.10,
        memory_horizon=len(history),
        intervention_history_digest=sha(
            [
                native["ActOS"]["act_state_digest"],
                native["ObserveOS"]["observe_state_digest"],
                native["VerifyOS"]["verify_state_digest"],
                learn["learn_state_digest"],
            ]
        ),
    )
    state = _apply(store, state, "qi_condition", {"qi_condition_packet": qi_packet}, 2)
    candidates = _candidates()
    state = _apply(store, state, "generate", {"candidates": candidates}, 3)
    state = _apply(
        store,
        state,
        "constrain",
        {
            "candidate_checks": standard_checks(
                [item["candidate_id"] for item in candidates]
            ),
            "mission_invariant_receipt_digest": sha(
                {
                    "mission": plan["mission_contract_digest"],
                    "world": world["world_projection_digest"],
                }
            ),
            "authority_boundary_receipt_digest": sha("v14-authority-boundary"),
            "resource_envelope_digest": sha("v14-resource-envelope"),
            "scope_compatibility_digest": sha(
                {
                    "target": learn["learning_delta"]["target_scope"],
                    "candidates": [item["candidate_id"] for item in candidates],
                }
            ),
        },
        4,
    )
    decision = _decision(root / "decision", source, state, world, qi)
    plural = _build_plural(root / "plural", str(plan["lineage_id"]), decision)
    wa = _build_wa(root / "wa", plural)
    decision_receipt = build_decision_receipt(
        state=state,
        decision_os_state_digest=decision["decision_state_digest"],
        decision_basis_digest=decision["decision_basis_digest"],
        wa_relational_harmony_digest=wa["wa_state_digest"],
        selected_candidate_id=decision["selected_option_id"],
        retained_candidate_ids=list(decision["retained_alternative_ids"]),
        dissent_evidence_digests=[],
        minority_stakeholder_digests=[],
        decided_at_ms=430_000,
    )
    state = _apply(store, state, "deliberate", {"decision_receipt": decision_receipt}, 5)
    selected = next(
        item
        for item in state["candidates"]
        if item["candidate_id"] == state["selected_candidate_id"]
    )
    synthesis = build_synthesis_packet(
        state=state,
        next_plan_goal_digest=selected["goal_digest"],
        next_plan_step_template_digests=selected["step_template_digests"],
        next_observation_point_digests=[selected["expected_observation_digest"]],
        next_verification_criterion_digests=[
            selected["verification_criterion_digest"]
        ],
        next_stop_condition_digests=selected["stop_condition_digests"],
        next_rollback_point_digests=[selected["rollback_point_digest"]],
        resource_envelope_digest=sha("v14-next-resource-envelope"),
        authority_boundary_digest=sha("v14-next-authority-boundary"),
    )
    state = _apply(store, state, "synthesize", {"synthesis_packet": synthesis}, 6)
    state = _apply(
        store,
        state,
        "commit_next",
        {
            "next_plan_basis_committed": True,
            "next_plan_phase_required": True,
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_plan_unchanged": True,
            "memory_overwrite": False,
            "plan_not_execution": True,
            "decision_not_execution": True,
            "qi_context_only": True,
            "host_license_granted": False,
            "non_authority": copy_non_authority(),
        },
        7,
    )
    return state, decision, plural, wa


def _extended_qi(
    source_qi: Mapping[str, Any],
    source_history: list[dict],
    replan: Mapping[str, Any],
    decision: Mapping[str, Any],
    wa: Mapping[str, Any],
) -> dict[str, Any]:
    history = deepcopy(source_history)
    history.append(
        {
            "stage": "GENERATIONAL_REPLAN_BASIS_COMMITTED",
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
            "process_observation": True,
            "process_action": False,
            "source_state_digest": replan["source_learn_state_digest"],
            "target_state_digest": replan["replan_state_digest"],
            "native_decision_state_digest": decision["decision_state_digest"],
            "native_wa_state_digest": wa["wa_state_digest"],
            "next_plan_basis_digest": replan["next_plan_basis_digest"],
            "source_generation": replan["current_cycle_index"],
            "target_generation": replan["active_from_cycle"],
            "future_only": True,
            "active_now": False,
        }
    )
    raw = {
        "cycle_id": CYCLE_ID,
        "process_history": history,
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "source_qi_process_receipt_digest": sha(source_qi),
        "source_process_history_digest": sha(source_history),
    }
    return evaluate_qi_process_tensor(raw).to_dict()


def _next_world(
    source_world: Mapping[str, Any],
    source_qi: Mapping[str, Any],
    qi: Mapping[str, Any],
    replan: Mapping[str, Any],
    decision: Mapping[str, Any],
    plural: Mapping[str, Any],
    wa: Mapping[str, Any],
) -> dict[str, Any]:
    projection = {
        "version": "kuuos_qi_world_native_generational_projection_v1_4",
        "source_world_projection_digest": source_world["world_projection_digest"],
        "source_qi_process_receipt_digest": sha(source_qi),
        "extended_qi_process_receipt_digest": sha(qi),
        "source_generation": replan["current_cycle_index"],
        "target_generation": replan["active_from_cycle"],
        "source_learn_state_digest": replan["source_learn_state_digest"],
        "source_learning_delta_digest": replan["source_learning_delta_digest"],
        "native_decision_state_digest": decision["decision_state_digest"],
        "native_plural_state_digest": plural["plural_state_digest"],
        "native_wa_state_digest": wa["wa_state_digest"],
        "native_replan_state_digest": replan["replan_state_digest"],
        "next_plan_basis_digest": replan["next_plan_basis_digest"],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "future_model_candidate_only": True,
        "world_projection_digest": "",
    }
    projection["world_projection_digest"] = _digest(
        projection, "world_projection_digest"
    )
    return projection


def build_native_generational_replan_receipt(root: Path) -> dict[str, Any]:
    source = build_native_full_cycle_receipt(root / "source-v13")
    if validate_native_full_cycle_receipt(source):
        raise ValueError("v14_source_full_cycle_invalid")
    world, source_qi, history = _source_surfaces(source)
    replan, decision, plural, wa = _native_replan(
        root / "next-generation", source, world, source_qi, history
    )
    qi = _extended_qi(source_qi, history, replan, decision, wa)
    next_world = _next_world(
        world, source_qi, qi, replan, decision, plural, wa
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "source_native_full_cycle_receipt": source,
        "source_native_full_cycle_receipt_digest": source[
            "native_full_cycle_receipt_digest"
        ],
        "source_world_projection_digest": world["world_projection_digest"],
        "source_qi_process_receipt_digest": sha(source_qi),
        "source_process_history_digest": sha(history),
        "native_replan_artifacts": {
            "DecisionOS": decision,
            "DecisionOSPlural": plural,
            "DecisionOSWa": wa,
            "PlanOSReplan": replan,
        },
        "extended_qi_process_receipt": qi,
        "extended_qi_process_receipt_digest": sha(qi),
        "next_world_projection": next_world,
        "next_world_projection_digest": next_world["world_projection_digest"],
        "source_generation": replan["current_cycle_index"],
        "target_generation": replan["active_from_cycle"],
        "future_only": True,
        "active_now": False,
        "current_cycle_unchanged": True,
        "past_history_unchanged": True,
        "next_plan_not_execution": True,
        "external_authority_required_for_future_act": True,
        "world_projection_read_only": True,
        "exact_world_updated": False,
        "qi_context_only": True,
        "non_authority": deepcopy(NON_AUTHORITY),
        "native_generational_replan_receipt_digest": "",
    }
    receipt["native_generational_replan_receipt_digest"] = receipt_digest(receipt)
    errors = validate_native_generational_replan_receipt(receipt)
    if errors:
        raise ValueError("v14_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_native_generational_replan_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == RECEIPT_VERSION, "v14_version_invalid")
        require(
            receipt.get("native_generational_replan_receipt_digest")
            == receipt_digest(receipt),
            "v14_digest_invalid",
        )
        source = dict(receipt.get("source_native_full_cycle_receipt", {}))
        errors.extend("v14_source_" + e for e in validate_native_full_cycle_receipt(source))
        require(
            receipt.get("source_native_full_cycle_receipt_digest")
            == source.get("native_full_cycle_receipt_digest"),
            "v14_source_digest_mismatch",
        )
        source_native = dict(source.get("native_artifacts", {}))
        interface = dict(source.get("qi_world_os_interface_receipt", {}))
        source_world = dict(interface.get("world_projection", {}))
        source_qi = dict(interface.get("qi_process_receipt", {}))
        source_history = list(
            dict(source_qi.get("enriched_state", {})).get("process_history", [])
        )
        require(
            receipt.get("source_world_projection_digest")
            == source_world.get("world_projection_digest"),
            "v14_source_world_mismatch",
        )
        require(
            receipt.get("source_qi_process_receipt_digest") == sha(source_qi),
            "v14_source_qi_mismatch",
        )
        require(
            receipt.get("source_process_history_digest") == sha(source_history),
            "v14_source_history_mismatch",
        )

        native = dict(receipt.get("native_replan_artifacts", {}))
        decision = dict(native.get("DecisionOS", {}))
        plural = dict(native.get("DecisionOSPlural", {}))
        wa = dict(native.get("DecisionOSWa", {}))
        replan = dict(native.get("PlanOSReplan", {}))
        errors.extend("v14_decision_" + e for e in validate_decision_state(decision))
        errors.extend("v14_plural_" + e for e in validate_plural_state(plural))
        errors.extend("v14_wa_" + e for e in validate_wa_state(wa))
        errors.extend("v14_replan_" + e for e in validate_replan_state(replan))
        require(
            replan.get("source_plan_state_digest")
            == dict(source_native.get("PlanOS", {})).get("plan_state_digest"),
            "v14_source_plan_mismatch",
        )
        require(
            replan.get("source_learn_state_digest")
            == dict(source_native.get("LearnOS", {})).get("learn_state_digest"),
            "v14_source_learn_mismatch",
        )
        require(
            replan.get("source_learning_delta_digest")
            == dict(source_native.get("LearnOS", {})).get("learning_delta_digest"),
            "v14_learning_delta_mismatch",
        )
        require(
            decision.get("source_belief_receipt_digest")
            == dict(source_native.get("BeliefOSReceipt", {})).get(
                "belief_gerbe_receipt_digest"
            ),
            "v14_decision_belief_mismatch",
        )
        require(
            plural.get("source_decision_state_digest")
            == decision.get("decision_state_digest"),
            "v14_plural_decision_mismatch",
        )
        require(
            wa.get("source_plural_state_digest") == plural.get("plural_state_digest"),
            "v14_wa_plural_mismatch",
        )
        decision_receipt = dict(replan.get("decision_receipt", {}))
        require(
            decision_receipt.get("decision_os_state_digest")
            == decision.get("decision_state_digest"),
            "v14_replan_decision_mismatch",
        )
        require(
            decision_receipt.get("wa_relational_harmony_digest")
            == wa.get("wa_state_digest"),
            "v14_replan_wa_mismatch",
        )
        require(
            replan.get("selected_candidate_id") == decision.get("selected_option_id"),
            "v14_selected_identity_mismatch",
        )
        require(replan.get("next_plan_basis_committed") is True, "v14_basis_missing")
        require(replan.get("next_plan_phase_required") is True, "v14_plan_debt_missing")
        require(replan.get("active_now") is False, "v14_present_activation_forbidden")
        require(replan.get("host_license_granted") is False, "v14_host_license_forbidden")
        require(
            receipt.get("target_generation") == receipt.get("source_generation") + 1,
            "v14_generation_order_invalid",
        )

        qi = dict(receipt.get("extended_qi_process_receipt", {}))
        require(
            receipt.get("extended_qi_process_receipt_digest") == sha(qi),
            "v14_extended_qi_digest_mismatch",
        )
        for field in (
            "process_tensor_visible",
            "transition_continuity_visible",
            "memory_continuity_visible",
            "nonmarkov_memory_visible",
        ):
            require(qi.get(field) is True, "v14_qi_" + field + "_missing")
        extended_history = list(
            dict(qi.get("enriched_state", {})).get("process_history", [])
        )
        require(
            len(extended_history) == len(source_history) + 1,
            "v14_qi_history_length_invalid",
        )
        if len(extended_history) == len(source_history) + 1:
            require(
                extended_history[:-1] == source_history,
                "v14_qi_history_prefix_mutated",
            )
            appended = dict(extended_history[-1])
            require(
                appended.get("next_plan_basis_digest")
                == replan.get("next_plan_basis_digest"),
                "v14_qi_basis_mismatch",
            )
            require(appended.get("future_only") is True, "v14_qi_future_only_missing")
            require(appended.get("active_now") is False, "v14_qi_activation_forbidden")

        world = dict(receipt.get("next_world_projection", {}))
        require(
            receipt.get("next_world_projection_digest")
            == world.get("world_projection_digest"),
            "v14_next_world_digest_mismatch",
        )
        require(
            world.get("world_projection_digest")
            == _digest(world, "world_projection_digest"),
            "v14_next_world_projection_invalid",
        )
        require(
            world.get("source_world_projection_digest")
            == source_world.get("world_projection_digest"),
            "v14_next_world_source_mismatch",
        )
        require(
            world.get("next_plan_basis_digest") == replan.get("next_plan_basis_digest"),
            "v14_next_world_basis_mismatch",
        )
        for key, expected in {
            "projection_read_only": True,
            "candidate_only": True,
            "nonfinal_marker": True,
            "exact_world_identified": False,
            "runtime_updates_world": False,
            "multi_world_noncollapse": True,
            "two_truths_gap": True,
            "future_model_candidate_only": True,
        }.items():
            require(world.get(key) is expected, "v14_world_" + key + "_invalid")
        for key, expected in {
            "future_only": True,
            "active_now": False,
            "current_cycle_unchanged": True,
            "past_history_unchanged": True,
            "next_plan_not_execution": True,
            "external_authority_required_for_future_act": True,
            "world_projection_read_only": True,
            "exact_world_updated": False,
            "qi_context_only": True,
        }.items():
            require(receipt.get(key) is expected, "v14_" + key + "_invalid")
        require(dict(receipt.get("non_authority", {})) == NON_AUTHORITY, "v14_authority_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
