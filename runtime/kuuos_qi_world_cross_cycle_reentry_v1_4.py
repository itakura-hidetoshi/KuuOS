from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_belief_os_kernel_v0_1 import (
    build_initial_belief_state,
    build_replan_activation_receipt,
    validate_belief_state,
)
from runtime.kuuos_belief_os_store_v0_1 import BeliefStore
from runtime.kuuos_belief_os_types_v0_1 import (
    ACTIVATION_RECEIPT_VERSION as BELIEF_ACTIVATION_VERSION,
    activation_receipt_digest as belief_activation_digest,
    sha,
)
from runtime.kuuos_decision_os_kernel_v0_1 import (
    build_initial_decision_state,
    validate_decision_state,
)
from runtime.kuuos_decision_os_plural_kernel_v0_2 import (
    build_initial_plural_state,
    validate_plural_state,
)
from runtime.kuuos_decision_os_plural_store_v0_2 import PluralDecisionStore
from runtime.kuuos_decision_os_store_v0_1 import DecisionStore
from runtime.kuuos_decision_os_wa_kernel_v0_3 import (
    build_initial_wa_state,
    build_replan_wa_activation_receipt,
    validate_wa_state,
)
from runtime.kuuos_decision_os_wa_store_v0_3 import WaDecisionStore
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_initial_plan_state,
    build_plan_phase_activation_receipt,
    validate_plan_state,
)
from runtime.kuuos_plan_os_store_v0_1 import PlanStore
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import (
    build_native_full_cycle_receipt,
    validate_native_full_cycle_receipt,
)
from runtime.v01_belief_os_relational_conditional_kernel import _apply as apply_belief
from runtime.v01_decision_os_relational_deliberation import (
    THRESHOLDS as DECISION_THRESHOLDS,
    WEIGHTS as DECISION_WEIGHTS,
    _challenge,
    _complete_cycle,
    _middle,
    _option,
)
from runtime.v01_plan_os_replan_bound_synthesis import (
    _candidate_steps,
    _complete_plan,
)
from runtime.v02_decision_os_plural_harmony_appeal import (
    PLURAL_THRESHOLDS,
    _complete_plural_cycle,
    _stakeholders,
)
from runtime.v03_decision_os_wa_relational_harmony import (
    WA_THRESHOLDS,
    WA_WEIGHTS,
    _complete_wa_cycle,
    _standard_profiles,
)

VERSION = "kuuos_qi_world_cross_cycle_reentry_v1_4"
RECEIPT_VERSION = "kuuos_qi_world_cross_cycle_reentry_receipt_v1_4"
CYCLE_ID = "qi-world-cross-cycle-v14"

CROSS_CYCLE_NON_AUTHORITY = {
    "bridge_grants_execution": False,
    "bridge_grants_truth": False,
    "bridge_issues_authority": False,
    "bridge_activates_plan": False,
    "bridge_updates_exact_world": False,
    "bridge_overwrites_previous_cycle": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def cross_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "cross_cycle_receipt_digest")


def _build_next_belief(
    root: Path,
    *,
    lineage_id: str,
    previous_receipt: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    artifacts = previous_receipt["native_artifacts"]
    observe = artifacts["ObserveOS"]
    verify = artifacts["VerifyOS"]
    learn = artifacts["LearnOS"]
    store = BeliefStore(root)
    state = store.initialize(
        build_initial_belief_state(
            belief_id="cross-cycle-belief-v14",
            lineage_id=lineage_id,
            claim="Verified prior-cycle evidence supports a future belief candidate.",
            claim_digest=sha(
                {
                    "previous_learning_delta_digest": learn["learning_delta_digest"],
                    "future_only": True,
                }
            ),
            hypothesis_space_digest=sha(
                ["continue", "reobserve", "replan", "hold"]
            ),
            source_memory_digest=learn["learn_state_digest"],
            now_ms=1_000,
        )
    )
    state = apply_belief(
        store,
        state,
        "contextualize",
        {
            "context": {
                "context_id": "cross-cycle-reentry-context",
                "observer_id": "cross-cycle-reviewer",
                "observer_role": "responsible-reviewer",
                "temporal_scope": "next-cycle",
                "scale": "lineage-local",
                "task_scope": "future-belief-reentry",
                "world_model_id": previous_receipt["world_projection_digest"],
            }
        },
        1,
    )
    state = apply_belief(
        store,
        state,
        "trace",
        {
            "evidence_digests": [
                observe["evidence_packet_digest"],
                verify["verification_evidence_digest"],
                learn["learning_delta_digest"],
            ],
            "observation_digests": [observe["observe_state_digest"]],
            "verification_receipt_digests": [verify["verify_state_digest"]],
            "causal_support_digests": [],
        },
        2,
    )
    state = apply_belief(
        store,
        state,
        "weigh",
        {
            "credal_state": {
                "lower_probability": 0.57,
                "upper_probability": 0.81,
                "central_estimate": 0.69,
                "conflict_index": 0.12,
            },
            "uncertainty": {
                "epistemic": 0.25,
                "aleatory": 0.18,
                "contextual": 0.20,
                "temporal": 0.22,
                "model": 0.28,
                "observer": 0.18,
                "process_history": 0.16,
            },
        },
        3,
    )
    state = apply_belief(
        store,
        state,
        "challenge",
        {
            "counterevidence_digests": observe.get(
                "counterevidence_digests", []
            ),
            "contradiction_digests": [],
            "alternative_hypothesis_digests": [sha("cross-cycle-hold")],
            "unresolved_residual_digests": [
                sha("cross-cycle-context-residual")
            ],
        },
        4,
    )
    state = apply_belief(
        store,
        state,
        "qi_condition",
        {
            "process_tensor_digest": previous_receipt[
                "process_lineage_digest"
            ],
            "history_window_digest": sha(
                {
                    "previous_cycle_receipt_digest": previous_receipt[
                        "native_full_cycle_receipt_digest"
                    ],
                    "learn_state_digest": learn["learn_state_digest"],
                }
            ),
            "roles": [
                "likelihood_context_modifier",
                "recovery_trajectory_signal",
            ],
            "flow_phase": "cross-cycle-reentry",
            "authority_source": False,
        },
        5,
    )
    state = apply_belief(
        store,
        state,
        "two_truths_check",
        {
            "two_truths": {
                "samvrti_operationally_usable": True,
                "paramartha_non_reified": True,
                "two_truths_separated": True,
            }
        },
        6,
    )
    state = apply_belief(
        store,
        state,
        "middle_way_gate",
        {
            "middle_way": {
                "reification_risk": 0.14,
                "nihilistic_erasure_risk": 0.10,
                "premature_closure_risk": 0.18,
                "responsibility_abandonment_risk": 0.08,
                "repairability": 0.94,
            },
            "route": "CANDIDATE",
            "reasoning_license": True,
            "planning_support_license": True,
        },
        7,
    )
    state = apply_belief(
        store,
        state,
        "commit",
        {
            "future_only": True,
            "memory_overwrite": False,
            "activation_boundary": "mission_replan_only",
            "non_authority": state["non_authority"],
        },
        8,
    )
    activation = build_replan_activation_receipt(
        state=state,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=learn["learn_state_digest"],
        replan_receipt_digest=previous_receipt[
            "native_full_cycle_receipt_digest"
        ],
        next_plan_basis_digest=learn["learning_delta_digest"],
        now_ms=2_000,
    )
    return state, activation


def _build_next_decision(
    root: Path,
    *,
    lineage_id: str,
    mission_contract_digest: str,
    previous_learn_state_digest: str,
    belief_activation: Mapping[str, Any],
) -> dict[str, Any]:
    store = DecisionStore(root)
    state = store.initialize(
        build_initial_decision_state(
            decision_id="cross-cycle-decision-v14",
            lineage_id=lineage_id,
            mission_contract_digest=mission_contract_digest,
            mission_state_digest=previous_learn_state_digest,
            source_belief_receipt_digest=belief_activation[
                "belief_activation_receipt_digest"
            ],
            decision_context_digest=sha("cross-cycle-decision-context"),
            decision_budget=1.0,
            weights=DECISION_WEIGHTS,
            thresholds=DECISION_THRESHOLDS,
            now_ms=3_000,
        )
    )
    evidence = sha("cross-cycle-required-evidence")
    options = [
        _option(
            option_id="option-a",
            action_class="exploit",
            positive=(0.84, 0.93),
            negative=(0.05, 0.11),
            information_gain=(0.34, 0.48),
            required_evidence=[evidence],
            available_evidence=[evidence],
        ),
        _option(
            option_id="option-b",
            action_class="observe",
            positive=(0.42, 0.58),
            negative=(0.22, 0.34),
            information_gain=(0.54, 0.70),
        ),
        _option(
            option_id="option-c",
            action_class="local_action",
            positive=(0.88, 0.95),
            negative=(0.03, 0.08),
            prohibited=True,
        ),
    ]
    state, _ = _complete_cycle(
        store,
        state,
        options=options,
        challenge=_challenge(),
        middle_way=_middle(),
        tick_base=10,
        requested_route="SELECT_CANDIDATE",
    )
    return state


def _build_next_plural(
    root: Path,
    *,
    lineage_id: str,
    decision: Mapping[str, Any],
) -> dict[str, Any]:
    store = PluralDecisionStore(root)
    state = store.initialize(
        build_initial_plural_state(
            source_decision_state=decision,
            plural_id="cross-cycle-plural-v14",
            lineage_id=lineage_id,
            thresholds=PLURAL_THRESHOLDS,
            now_ms=10_000,
        )
    )
    state, _ = _complete_plural_cycle(
        store=store,
        state=state,
        stakeholders=_stakeholders(),
        requested_route="CONSENSUS_CANDIDATE",
        tick_base=10,
    )
    return state


def _build_next_wa(
    root: Path,
    plural: Mapping[str, Any],
) -> dict[str, Any]:
    store = WaDecisionStore(root)
    state = store.initialize(
        build_initial_wa_state(
            wa_id="cross-cycle-wa-v14",
            source_plural_state=plural,
            weights=WA_WEIGHTS,
            thresholds=WA_THRESHOLDS,
            now_ms=30_000,
        )
    )
    state, _ = _complete_wa_cycle(
        store,
        state,
        profiles=_standard_profiles(plural),
        requested_route="ENDORSE",
        tick_base=20,
    )
    return state


def _build_next_plan(
    root: Path,
    wa: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    wa_activation = build_replan_wa_activation_receipt(
        state=wa,
        mission_cycle_phase="replan",
        mission_cycle_state_digest=sha("cross-cycle-wa-replan-state"),
        replan_receipt_digest=sha("cross-cycle-wa-replan-receipt"),
        next_plan_basis_digest=sha("cross-cycle-wa-next-plan-basis"),
        now_ms=50_000,
    )
    store = PlanStore(root)
    state = store.initialize(
        build_initial_plan_state(
            plan_id="cross-cycle-plan-v14",
            source_wa_state=wa,
            replan_activation_receipt=wa_activation,
            plan_budget=2.0,
            maximum_step_risk=0.40,
            now_ms=60_000,
        )
    )
    state, _ = _complete_plan(store, state, _candidate_steps(), 10)
    activation = build_plan_phase_activation_receipt(
        state=state,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=sha("cross-cycle-plan-phase-state"),
        plan_phase_receipt_digest=sha("cross-cycle-plan-phase-receipt"),
        now_ms=80_000,
    )
    return state, activation


def _validate_next_artifacts(
    artifacts: Mapping[str, Mapping[str, Any]],
) -> list[str]:
    validators = {
        "BeliefOS": validate_belief_state,
        "DecisionOS": validate_decision_state,
        "DecisionOSPlural": validate_plural_state,
        "DecisionOSWa": validate_wa_state,
        "PlanOS": validate_plan_state,
    }
    errors: list[str] = []
    for name, validator in validators.items():
        artifact = artifacts.get(name)
        if not isinstance(artifact, Mapping):
            errors.append(f"{name}_missing")
        else:
            errors.extend(f"{name}:{error}" for error in validator(artifact))
    activation = artifacts.get("BeliefActivation")
    if not isinstance(activation, Mapping):
        errors.append("BeliefActivation_missing")
    else:
        if activation.get("version") != BELIEF_ACTIVATION_VERSION:
            errors.append("BeliefActivation_version_invalid")
        if activation.get("belief_activation_receipt_digest") != belief_activation_digest(
            activation
        ):
            errors.append("BeliefActivation_digest_invalid")
    return errors


def _build_cross_cycle_qi_receipt(
    previous: Mapping[str, Any],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    learn = previous["native_artifacts"]["LearnOS"]
    stages = [
        ("process_action", "PREVIOUS_CYCLE_LEARNING", learn["learn_state_digest"]),
        ("process_observation", "NEXT_BELIEF_COMMITTED", next_artifacts["BeliefOS"]["belief_state_digest"]),
        ("process_action", "NEXT_DECISION_COMMITTED", next_artifacts["DecisionOS"]["decision_state_digest"]),
        ("process_action", "NEXT_WA_COMMITTED", next_artifacts["DecisionOSWa"]["wa_state_digest"]),
        ("process_action", "NEXT_PLAN_COMMITTED", next_artifacts["PlanOS"]["plan_state_digest"]),
    ]
    history = []
    previous_digest = previous["native_full_cycle_receipt_digest"]
    for index, (field, kind, digest) in enumerate(stages):
        history.append(
            {
                field: kind,
                "native_artifact_digest": digest,
                "source_state_digest": previous_digest,
                "target_state_digest": digest,
                "transition_visible": True,
                "memory_link_visible": True,
                "nonmarkov_link_visible": index >= 1,
            }
        )
        previous_digest = digest
    return evaluate_qi_process_tensor(
        {
            "cycle_id": CYCLE_ID,
            "candidate_only": True,
            "nonfinal_marker": True,
            "two_truths_gap": True,
            "noncollapse_guard": True,
            "memory_overwrite_blocker": True,
            "world_identity_blocker": True,
            "process_history": history,
        }
    ).to_dict()


def _build_cross_cycle_world_projection(
    previous: Mapping[str, Any],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    learn = previous["native_artifacts"]["LearnOS"]
    packet = {
        "projection_kind": "cross_cycle_reentry_projection",
        "previous_cycle_receipt_digest": previous[
            "native_full_cycle_receipt_digest"
        ],
        "previous_world_projection_digest": previous[
            "world_projection_digest"
        ],
        "previous_learn_state_digest": learn["learn_state_digest"],
        "previous_learning_delta_digest": learn["learning_delta_digest"],
        "next_belief_state_digest": next_artifacts["BeliefOS"][
            "belief_state_digest"
        ],
        "next_decision_state_digest": next_artifacts["DecisionOS"][
            "decision_state_digest"
        ],
        "next_plural_state_digest": next_artifacts["DecisionOSPlural"][
            "plural_state_digest"
        ],
        "next_wa_state_digest": next_artifacts["DecisionOSWa"][
            "wa_state_digest"
        ],
        "next_plan_state_digest": next_artifacts["PlanOS"][
            "plan_state_digest"
        ],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "previous_cycle_immutable": True,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "world_projection_digest": "",
    }
    packet["world_projection_digest"] = _digest_without(
        packet, "world_projection_digest"
    )
    return packet


def build_cross_cycle_reentry_receipt(root: Path) -> dict[str, Any]:
    previous = build_native_full_cycle_receipt(root / "previous-cycle")
    prior_errors = validate_native_full_cycle_receipt(previous)
    if prior_errors:
        raise ValueError("previous_cycle_invalid:" + ";".join(prior_errors))
    prior_artifacts = previous["native_artifacts"]
    learn = prior_artifacts["LearnOS"]
    lineage_id = str(learn["lineage_id"])
    mission_contract_digest = str(learn["mission_contract_digest"])

    belief, belief_activation = _build_next_belief(
        root / "next-belief",
        lineage_id=lineage_id,
        previous_receipt=previous,
    )
    decision = _build_next_decision(
        root / "next-decision",
        lineage_id=lineage_id,
        mission_contract_digest=mission_contract_digest,
        previous_learn_state_digest=learn["learn_state_digest"],
        belief_activation=belief_activation,
    )
    plural = _build_next_plural(
        root / "next-plural",
        lineage_id=lineage_id,
        decision=decision,
    )
    wa = _build_next_wa(root / "next-wa", plural)
    plan, plan_activation = _build_next_plan(root / "next-plan", wa)
    next_artifacts = {
        "BeliefOS": belief,
        "BeliefActivation": belief_activation,
        "DecisionOS": decision,
        "DecisionOSPlural": plural,
        "DecisionOSWa": wa,
        "PlanOS": plan,
        "PlanActivation": plan_activation,
    }
    next_errors = _validate_next_artifacts(next_artifacts)
    if next_errors:
        raise ValueError("next_cycle_invalid:" + ";".join(next_errors))

    qi_receipt = _build_cross_cycle_qi_receipt(previous, next_artifacts)
    world = _build_cross_cycle_world_projection(previous, next_artifacts)
    process_lineage_digest = sha(
        {
            "previous_process_lineage_digest": previous[
                "process_lineage_digest"
            ],
            "previous_learn_state_digest": learn["learn_state_digest"],
            "previous_learning_delta_digest": learn["learning_delta_digest"],
            "next_belief_state_digest": belief["belief_state_digest"],
            "next_decision_state_digest": decision["decision_state_digest"],
            "next_wa_state_digest": wa["wa_state_digest"],
            "next_plan_state_digest": plan["plan_state_digest"],
        }
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "previous_cycle_receipt": deepcopy(previous),
        "previous_cycle_receipt_digest": previous[
            "native_full_cycle_receipt_digest"
        ],
        "next_cycle_artifacts": deepcopy(next_artifacts),
        "cross_cycle_process_lineage_digest": process_lineage_digest,
        "cross_cycle_qi_receipt": qi_receipt,
        "cross_cycle_world_projection": world,
        "cross_cycle_world_projection_digest": world[
            "world_projection_digest"
        ],
        "previous_cycle_immutable": True,
        "next_plan_not_activated": True,
        "cross_cycle_non_authority": deepcopy(CROSS_CYCLE_NON_AUTHORITY),
        "cross_cycle_receipt_digest": "",
    }
    receipt["cross_cycle_receipt_digest"] = cross_cycle_receipt_digest(receipt)
    errors = validate_cross_cycle_reentry_receipt(receipt)
    if errors:
        raise ValueError("cross_cycle_receipt_invalid:" + ";".join(errors))
    return receipt


def validate_cross_cycle_reentry_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("cross_cycle_version_invalid")
        if receipt.get("cross_cycle_receipt_digest") != cross_cycle_receipt_digest(
            receipt
        ):
            errors.append("cross_cycle_digest_invalid")
        previous = dict(receipt.get("previous_cycle_receipt", {}))
        errors.extend(
            f"previous:{error}"
            for error in validate_native_full_cycle_receipt(previous)
        )
        if receipt.get("previous_cycle_receipt_digest") != previous.get(
            "native_full_cycle_receipt_digest"
        ):
            errors.append("cross_cycle_previous_receipt_digest_mismatch")
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        errors.extend(_validate_next_artifacts(next_artifacts))
        expected_inventory = {
            "BeliefOS",
            "BeliefActivation",
            "DecisionOS",
            "DecisionOSPlural",
            "DecisionOSWa",
            "PlanOS",
            "PlanActivation",
        }
        if set(next_artifacts) != expected_inventory:
            errors.append("cross_cycle_next_artifact_inventory_invalid")
            return errors
        prior_artifacts = previous["native_artifacts"]
        observe = prior_artifacts["ObserveOS"]
        verify = prior_artifacts["VerifyOS"]
        learn = prior_artifacts["LearnOS"]
        belief = next_artifacts["BeliefOS"]
        belief_activation = next_artifacts["BeliefActivation"]
        decision = next_artifacts["DecisionOS"]
        plural = next_artifacts["DecisionOSPlural"]
        wa = next_artifacts["DecisionOSWa"]
        plan = next_artifacts["PlanOS"]

        if learn.get("replan_required") is not True:
            errors.append("cross_cycle_previous_learning_replan_missing")
        if learn.get("active_now") is not False:
            errors.append("cross_cycle_previous_learning_active_now")
        if learn.get("past_records_unchanged") is not True:
            errors.append("cross_cycle_previous_learning_mutated_past")
        if belief.get("source_memory_digest") != learn.get("learn_state_digest"):
            errors.append("cross_cycle_belief_memory_binding_mismatch")
        required_evidence = {
            observe.get("evidence_packet_digest"),
            verify.get("verification_evidence_digest"),
            learn.get("learning_delta_digest"),
        }
        if not required_evidence.issubset(set(belief.get("evidence_digests", []))):
            errors.append("cross_cycle_belief_evidence_binding_mismatch")
        if belief_activation.get("belief_state_digest") != belief.get(
            "belief_state_digest"
        ):
            errors.append("cross_cycle_belief_activation_state_mismatch")
        if belief_activation.get("next_plan_basis_digest") != learn.get(
            "learning_delta_digest"
        ):
            errors.append("cross_cycle_learning_delta_basis_mismatch")
        if decision.get("source_belief_receipt_digest") != belief_activation.get(
            "belief_activation_receipt_digest"
        ):
            errors.append("cross_cycle_decision_belief_mismatch")
        if plural.get("source_decision_state_digest") != decision.get(
            "decision_state_digest"
        ):
            errors.append("cross_cycle_plural_decision_mismatch")
        if wa.get("source_plural_state_digest") != plural.get(
            "plural_state_digest"
        ):
            errors.append("cross_cycle_wa_plural_mismatch")
        if plan.get("source_wa_state_digest") != wa.get("wa_state_digest"):
            errors.append("cross_cycle_plan_wa_mismatch")
        lineage_ids = {
            learn.get("lineage_id"),
            belief.get("lineage_id"),
            decision.get("lineage_id"),
            plural.get("lineage_id"),
            wa.get("lineage_id"),
            plan.get("lineage_id"),
        }
        if len(lineage_ids) != 1:
            errors.append("cross_cycle_lineage_mismatch")
        mission_contracts = {
            learn.get("mission_contract_digest"),
            decision.get("mission_contract_digest"),
            plural.get("mission_contract_digest"),
            wa.get("mission_contract_digest"),
            plan.get("mission_contract_digest"),
        }
        if len(mission_contracts) != 1:
            errors.append("cross_cycle_mission_contract_mismatch")
        qi_receipt = dict(receipt.get("cross_cycle_qi_receipt", {}))
        if qi_receipt.get("process_tensor_visible") is not True:
            errors.append("cross_cycle_qi_process_not_visible")
        if qi_receipt.get("memory_continuity_visible") is not True:
            errors.append("cross_cycle_qi_memory_not_visible")
        if qi_receipt.get("nonmarkov_memory_visible") is not True:
            errors.append("cross_cycle_qi_nonmarkov_not_visible")
        world = dict(receipt.get("cross_cycle_world_projection", {}))
        if receipt.get("cross_cycle_world_projection_digest") != world.get(
            "world_projection_digest"
        ):
            errors.append("cross_cycle_world_projection_digest_mismatch")
        for field, expected in {
            "projection_read_only": True,
            "candidate_only": True,
            "nonfinal_marker": True,
            "exact_world_identified": False,
            "runtime_updates_world": False,
            "previous_cycle_immutable": True,
            "multi_world_noncollapse": True,
            "two_truths_gap": True,
        }.items():
            if world.get(field) != expected:
                errors.append(f"cross_cycle_world_{field}_invalid")
        if receipt.get("previous_cycle_immutable") is not True:
            errors.append("cross_cycle_previous_cycle_not_immutable")
        if receipt.get("next_plan_not_activated") is not True:
            errors.append("cross_cycle_next_plan_activation_boundary_invalid")
        if dict(receipt.get("cross_cycle_non_authority", {})) != CROSS_CYCLE_NON_AUTHORITY:
            errors.append("cross_cycle_non_authority_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
