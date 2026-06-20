from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_plan_os_kernel_v0_1 import validate_plan_state
from runtime.kuuos_qi_world_cross_cycle_blocker_v1_5 import (
    BLOCKER_ORDER,
    blocker_identity,
    meet_blocker_vectors,
)
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    _build_next_decision,
    _build_next_plan_from_learning,
)
from runtime import kuuos_qi_world_cross_cycle_reentry_v1_4_new as _reentry
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    build_licensed_act_handoff_receipt,
    validate_licensed_act_handoff_receipt,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import _build_downstream
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state

VERSION = "kuuos_qi_world_licensed_effect_evidence_closure_v1_8"
RECEIPT_VERSION = "kuuos_qi_world_licensed_effect_evidence_closure_receipt_v1_8"
BLOCKER_VERSION = "kuuos_qi_world_post_effect_blocker_certificate_v1_8"
CYCLE_ID = "qi-world-licensed-effect-evidence-closure-v18"

CLOSURE_NON_AUTHORITY = {
    "closure_grants_execution": False,
    "closure_grants_truth": False,
    "closure_issues_authority": False,
    "closure_starts_next_act": False,
    "closure_updates_exact_world": False,
    "closure_overwrites_history": False,
    "closure_renews_external_authority": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def closure_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_effect_evidence_closure_receipt_digest")


def blocker_certificate_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "post_effect_blocker_certificate_digest")


def _native_validation_errors(states: Mapping[str, Mapping[str, Any]]) -> list[str]:
    validators = {
        "ObserveOS": validate_observe_state,
        "VerifyOS": validate_verify_state,
        "LearnOS": validate_learn_state,
    }
    errors: list[str] = []
    for name, validator in validators.items():
        state = states.get(name)
        if not isinstance(state, Mapping):
            errors.append(f"{name}_native_state_missing")
            continue
        errors.extend(f"{name}:{error}" for error in validator(state))
    return errors


def _evidence_lineage_digest(
    source: Mapping[str, Any], states: Mapping[str, Mapping[str, Any]]
) -> str:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    return sha(
        {
            "source_licensed_handoff_receipt_digest": source[
                "licensed_act_handoff_receipt_digest"
            ],
            "act_state_digest": act["act_state_digest"],
            "observe_state_digest": observe["observe_state_digest"],
            "verify_state_digest": verify["verify_state_digest"],
            "learn_state_digest": learn["learn_state_digest"],
        }
    )


def _world_projection(
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    indra = dict(source["source_indra_transport_request_receipt"])
    request = dict(indra["transport_request"])
    packet = {
        "projection_kind": "licensed_effect_evidence_closure_projection",
        "source_world_projection_digest": request[
            "target_world_projection_digest"
        ],
        "source_indra_transport_request_digest": request[
            "transport_request_digest"
        ],
        "act_state_digest": states["ActOS"]["act_state_digest"],
        "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
        "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
        "learn_state_digest": states["LearnOS"]["learn_state_digest"],
        "next_plan_state_digest": next_artifacts["PlanOS"]["plan_state_digest"],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "indra_transport_still_unrealized": True,
        "world_projection_digest": "",
    }
    packet["world_projection_digest"] = _digest_without(
        packet, "world_projection_digest"
    )
    return packet


def _qi_receipt(
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    plan = next_artifacts["PlanOS"]
    history = [
        {
            "process_action": "LICENSED_EFFECT_RECORDED",
            "native_state_digest": act["act_state_digest"],
            "source_state_digest": act["source_plan_state_digest"],
            "target_state_digest": act["act_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_observation": "OBSERVATION_DEBT_DISCHARGED",
            "native_state_digest": observe["observe_state_digest"],
            "source_state_digest": observe["source_act_state_digest"],
            "target_state_digest": observe["observe_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_observation": "VERIFICATION_DEBT_DISCHARGED",
            "native_state_digest": verify["verify_state_digest"],
            "source_state_digest": verify["source_observe_state_digest"],
            "target_state_digest": verify["verify_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_action": "FUTURE_ONLY_LEARNING_RECORDED",
            "native_state_digest": learn["learn_state_digest"],
            "source_state_digest": learn["source_verify_state_digest"],
            "target_state_digest": learn["learn_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_action": "NEXT_PLAN_COMMITTED_WITHOUT_ACT",
            "native_state_digest": plan["plan_state_digest"],
            "source_state_digest": learn["learn_state_digest"],
            "target_state_digest": plan["plan_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
    ]
    raw = {
        "cycle_id": CYCLE_ID,
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "process_history": history,
    }
    return evaluate_qi_process_tensor(raw).to_dict()


def _synthetic_previous_receipt(
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    lineage_digest: str,
) -> dict[str, Any]:
    indra = dict(source["source_indra_transport_request_receipt"])
    request = dict(indra["transport_request"])
    packet = {
        "native_artifacts": {
            "ActOS": deepcopy(dict(states["ActOS"])),
            "ObserveOS": deepcopy(dict(states["ObserveOS"])),
            "VerifyOS": deepcopy(dict(states["VerifyOS"])),
            "LearnOS": deepcopy(dict(states["LearnOS"])),
        },
        "world_projection_digest": request["target_world_projection_digest"],
        "process_lineage_digest": lineage_digest,
        "native_full_cycle_receipt_digest": "",
    }
    packet["native_full_cycle_receipt_digest"] = sha(packet)
    return packet


def _build_next_cycle(
    root: Path,
    *,
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    lineage_digest: str,
) -> dict[str, dict[str, Any]]:
    learn = states["LearnOS"]
    previous = _synthetic_previous_receipt(source, states, lineage_digest)
    lineage_id = str(learn["lineage_id"])
    mission_contract_digest = str(learn["mission_contract_digest"])

    belief, activation = _reentry._build_next_belief(
        root / "belief",
        lineage_id=lineage_id,
        previous_receipt=previous,
    )
    decision = _build_next_decision(
        root / "decision",
        lineage_id=lineage_id,
        mission_contract_digest=mission_contract_digest,
        previous_learn_state_digest=str(learn["learn_state_digest"]),
        belief_activation=activation,
    )
    plural = _reentry._build_next_plural(
        root / "plural",
        lineage_id=lineage_id,
        decision=decision,
    )
    wa = _reentry._build_next_wa(root / "wa", plural)
    plan = _build_next_plan_from_learning(
        root / "plan",
        wa,
        str(learn["learning_delta_digest"]),
    )
    artifacts = {
        "BeliefOS": belief,
        "BeliefActivation": activation,
        "DecisionOS": decision,
        "DecisionOSPlural": plural,
        "DecisionOSWa": wa,
        "PlanOS": plan,
    }
    errors = _reentry._validate_next_artifacts(artifacts)
    if errors:
        raise ValueError("next_cycle_invalid:" + ";".join(errors))
    return artifacts


def _component_vector(**updates: bool) -> dict[str, bool]:
    vector = blocker_identity()
    for name, value in updates.items():
        if name not in vector:
            raise KeyError(f"unknown_blocker:{name}")
        vector[name] = bool(value)
    return vector


def build_post_effect_blocker_certificate(
    *,
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
) -> dict[str, Any]:
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    plan = next_artifacts["PlanOS"]

    evidence_vector = _component_vector(
        present_activation_blocker=plan.get("current_phase") == "commit",
        execution_authority_blocker=True,
        memory_overwrite_blocker=(
            learn.get("memory_overwrite") is False
            and learn.get("past_records_unchanged") is True
        ),
        truth_authority_blocker=(
            observe.get("automatic_truth_promotion") is False
            and verify.get("automatic_truth_promotion") is False
            and learn.get("automatic_truth_promotion") is False
        ),
        same_cycle_self_loop_blocker=(
            learn.get("active_now") is False
            and learn.get("current_cycle_unchanged") is True
        ),
    )
    world_vector = _component_vector(
        world_identity_blocker=(
            world.get("projection_read_only") is True
            and world.get("runtime_updates_world") is False
            and world.get("exact_world_identified") is False
        ),
        truth_authority_blocker=(
            world.get("candidate_only") is True
            and world.get("nonfinal_marker") is True
            and world.get("two_truths_gap") is True
        ),
        multi_world_collapse_blocker=(
            world.get("multi_world_noncollapse") is True
            and world.get("indra_transport_still_unrealized") is True
        ),
    )
    authority_vector = _component_vector(
        present_activation_blocker=True,
        execution_authority_blocker=(
            source.get("release_consumption_count") == 1
            and source.get("release_consumed") is True
        ),
        memory_overwrite_blocker=True,
        world_identity_blocker=True,
        truth_authority_blocker=True,
        same_cycle_self_loop_blocker=True,
        multi_world_collapse_blocker=True,
    )
    debt_vector = _component_vector(
        present_activation_blocker=(
            observe.get("observation_debt_discharged") is True
            and verify.get("verification_debt_discharged") is True
            and learn.get("activation_requires_replan") is True
        ),
        execution_authority_blocker=True,
    )
    components = {
        "native_evidence_surface": evidence_vector,
        "world_projection_surface": world_vector,
        "consumed_authority_surface": authority_vector,
        "debt_closure_surface": debt_vector,
    }
    composed = meet_blocker_vectors(list(components.values()))
    active = [name for name in BLOCKER_ORDER if composed[name]]
    missing = [name for name in BLOCKER_ORDER if not composed[name]]
    certificate = {
        "version": BLOCKER_VERSION,
        "cycle_id": CYCLE_ID,
        "source_licensed_handoff_receipt_digest": source[
            "licensed_act_handoff_receipt_digest"
        ],
        "source_act_state_digest": states["ActOS"]["act_state_digest"],
        "observe_state_digest": observe["observe_state_digest"],
        "verify_state_digest": verify["verify_state_digest"],
        "learn_state_digest": learn["learn_state_digest"],
        "next_plan_state_digest": plan["plan_state_digest"],
        "component_vectors": components,
        "composed_blocker_vector": composed,
        "active_blockers": active,
        "missing_blockers": missing,
        "all_required_blockers_active": not missing,
        "next_act_not_started": True,
        "disposition": (
            "BLOCKED_PENDING_NEXT_EXTERNAL_AUTHORITY"
            if not missing
            else "QUARANTINE_EVIDENCE_CLOSURE_INCOMPLETE"
        ),
        "non_authority": deepcopy(CLOSURE_NON_AUTHORITY),
        "post_effect_blocker_certificate_digest": "",
    }
    certificate["post_effect_blocker_certificate_digest"] = (
        blocker_certificate_digest(certificate)
    )
    return certificate


def validate_post_effect_blocker_certificate(
    certificate: Mapping[str, Any],
    *,
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        expected = build_post_effect_blocker_certificate(
            source=source,
            states=states,
            next_artifacts=next_artifacts,
            world=world,
        )
        require(certificate.get("version") == BLOCKER_VERSION, "closure_blocker_version_invalid")
        require(
            certificate.get("post_effect_blocker_certificate_digest")
            == blocker_certificate_digest(certificate),
            "closure_blocker_digest_invalid",
        )
        for field in (
            "source_licensed_handoff_receipt_digest",
            "source_act_state_digest",
            "observe_state_digest",
            "verify_state_digest",
            "learn_state_digest",
            "next_plan_state_digest",
            "component_vectors",
            "composed_blocker_vector",
            "active_blockers",
            "missing_blockers",
            "all_required_blockers_active",
            "next_act_not_started",
            "disposition",
            "non_authority",
        ):
            require(certificate.get(field) == expected.get(field), f"closure_blocker_{field}_invalid")
        require(certificate.get("all_required_blockers_active") is True, "closure_blocker_not_all_active")
        require(certificate.get("missing_blockers") == [], "closure_blocker_missing_inventory")
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_licensed_effect_evidence_closure_receipt(root: Path) -> dict[str, Any]:
    source = build_licensed_act_handoff_receipt(root / "source-v17")
    source_errors = validate_licensed_act_handoff_receipt(source)
    if source_errors:
        raise ValueError("source_v17_invalid:" + ";".join(source_errors))

    act = deepcopy(dict(source["target_act_state"]))
    observe, verify, learn = _build_downstream(root / "evidence", act)
    states = {
        "ActOS": act,
        "ObserveOS": observe,
        "VerifyOS": verify,
        "LearnOS": learn,
    }
    native_errors = _native_validation_errors(states)
    if native_errors:
        raise ValueError("native_evidence_invalid:" + ";".join(native_errors))

    lineage_digest = _evidence_lineage_digest(source, states)
    next_artifacts = _build_next_cycle(
        root / "next-cycle",
        source=source,
        states=states,
        lineage_digest=lineage_digest,
    )
    world = _world_projection(source, states, next_artifacts)
    qi = _qi_receipt(states, next_artifacts)
    blocker = build_post_effect_blocker_certificate(
        source=source,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )

    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "source_licensed_handoff_receipt": deepcopy(source),
        "source_licensed_handoff_receipt_digest": source[
            "licensed_act_handoff_receipt_digest"
        ],
        "native_evidence_states": deepcopy(states),
        "native_evidence_lineage_digest": lineage_digest,
        "next_cycle_artifacts": deepcopy(next_artifacts),
        "post_effect_qi_receipt": qi,
        "post_effect_world_projection": world,
        "post_effect_world_projection_digest": world["world_projection_digest"],
        "post_effect_blocker_certificate": blocker,
        "post_effect_blocker_certificate_digest": blocker[
            "post_effect_blocker_certificate_digest"
        ],
        "source_effect_immutable": True,
        "source_authority_consumed_once": True,
        "observation_debt_discharged": True,
        "verification_debt_discharged": True,
        "learning_recorded": True,
        "replan_debt_discharged": True,
        "next_act_not_started": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CLOSURE_NON_AUTHORITY),
        "licensed_effect_evidence_closure_receipt_digest": "",
    }
    receipt["licensed_effect_evidence_closure_receipt_digest"] = (
        closure_receipt_digest(receipt)
    )
    errors = validate_licensed_effect_evidence_closure_receipt(receipt)
    if errors:
        raise ValueError("evidence_closure_invalid:" + ";".join(errors))
    return receipt


def validate_licensed_effect_evidence_closure_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    try:
        require(receipt.get("version") == RECEIPT_VERSION, "closure_version_invalid")
        require(
            receipt.get("licensed_effect_evidence_closure_receipt_digest")
            == closure_receipt_digest(receipt),
            "closure_receipt_digest_invalid",
        )
        source = dict(receipt.get("source_licensed_handoff_receipt", {}))
        errors.extend(
            "closure_source_" + error
            for error in validate_licensed_act_handoff_receipt(source)
        )
        require(
            receipt.get("source_licensed_handoff_receipt_digest")
            == source.get("licensed_act_handoff_receipt_digest"),
            "closure_source_receipt_digest_mismatch",
        )
        require(source.get("release_consumption_count") == 1, "closure_source_release_not_single_use")
        require(source.get("release_consumed") is True, "closure_source_release_not_consumed")

        states = dict(receipt.get("native_evidence_states", {}))
        errors.extend("closure_" + error for error in _native_validation_errors(states))
        act = dict(states.get("ActOS", {}))
        observe = dict(states.get("ObserveOS", {}))
        verify = dict(states.get("VerifyOS", {}))
        learn = dict(states.get("LearnOS", {}))
        require(act == dict(source.get("target_act_state", {})), "closure_source_act_state_substitution")
        require(
            observe.get("source_act_state_digest") == act.get("act_state_digest"),
            "closure_observe_source_act_mismatch",
        )
        require(
            verify.get("source_observe_state_digest") == observe.get("observe_state_digest"),
            "closure_verify_source_observe_mismatch",
        )
        require(
            learn.get("source_verify_state_digest") == verify.get("verify_state_digest"),
            "closure_learn_source_verify_mismatch",
        )
        require(observe.get("observation_debt_discharged") is True, "closure_observation_debt_open")
        require(verify.get("verification_debt_discharged") is True, "closure_verification_debt_open")
        require(learn.get("future_only") is True, "closure_learning_not_future_only")
        require(learn.get("memory_overwrite") is False, "closure_learning_memory_overwrite")
        require(learn.get("past_records_unchanged") is True, "closure_learning_past_changed")
        require(
            receipt.get("native_evidence_lineage_digest")
            == _evidence_lineage_digest(source, states),
            "closure_evidence_lineage_digest_mismatch",
        )

        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        next_errors = _reentry._validate_next_artifacts(next_artifacts)
        errors.extend("closure_next_" + error for error in next_errors)
        plan = dict(next_artifacts.get("PlanOS", {}))
        require(
            plan.get("next_plan_basis_digest") == learn.get("learning_delta_digest"),
            "closure_next_plan_learning_basis_mismatch",
        )
        require(plan.get("current_phase") == "commit", "closure_next_plan_not_committed")

        world = dict(receipt.get("post_effect_world_projection", {}))
        require(
            receipt.get("post_effect_world_projection_digest")
            == world.get("world_projection_digest"),
            "closure_world_projection_digest_mismatch",
        )
        require(
            world.get("world_projection_digest")
            == _digest_without(world, "world_projection_digest"),
            "closure_world_projection_digest_invalid",
        )
        require(world.get("projection_read_only") is True, "closure_world_not_read_only")
        require(world.get("runtime_updates_world") is False, "closure_world_update_claim")
        require(world.get("exact_world_identified") is False, "closure_exact_world_identity_claim")
        require(world.get("indra_transport_still_unrealized") is True, "closure_indra_transport_realized")

        blocker = dict(receipt.get("post_effect_blocker_certificate", {}))
        errors.extend(
            validate_post_effect_blocker_certificate(
                blocker,
                source=source,
                states=states,
                next_artifacts=next_artifacts,
                world=world,
            )
        )
        require(
            receipt.get("post_effect_blocker_certificate_digest")
            == blocker.get("post_effect_blocker_certificate_digest"),
            "closure_blocker_digest_mismatch",
        )

        for field, expected in {
            "source_effect_immutable": True,
            "source_authority_consumed_once": True,
            "observation_debt_discharged": True,
            "verification_debt_discharged": True,
            "learning_recorded": True,
            "replan_debt_discharged": True,
            "next_act_not_started": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }.items():
            require(receipt.get(field) == expected, f"closure_{field}_invalid")
        require(
            dict(receipt.get("non_authority", {})) == CLOSURE_NON_AUTHORITY,
            "closure_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
