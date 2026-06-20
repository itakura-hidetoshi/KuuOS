from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.kuuos_act_os_fixture_v0_1 import apply as apply_act
from runtime.kuuos_act_os_fixture_v0_1 import event as build_fixture_event
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs
from runtime.kuuos_act_os_kernel_v0_1 import (
    build_authorized_invoke_event,
    build_initial_act_state,
    build_step_authorization,
    validate_act_state,
)
from runtime.kuuos_act_os_store_v0_1 import ActStore
from runtime.kuuos_act_os_types_v0_1 import copy_non_authority as act_non_authority
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_plan_os_kernel_v0_1 import (
    build_plan_phase_activation_receipt,
    validate_plan_state,
)
from runtime.kuuos_qi_world_cross_cycle_reentry_v1_4 import (
    _build_next_decision,
    _build_next_plan_from_learning,
)
from runtime import kuuos_qi_world_cross_cycle_reentry_v1_4_new as _reentry
from runtime.kuuos_qi_world_licensed_blocker_discharge_v1_7 import (
    RELEASE_SCOPE,
    authority_packet_digest,
)
from runtime.kuuos_qi_world_licensed_cycle_receipt_public_v1_9 import (
    build_licensed_cycle_receipt,
    build_successor_authority_intake,
    build_successor_authority_requirement,
    validate_licensed_cycle_receipt,
    validate_successor_authority_intake,
    validate_successor_authority_requirement,
)
from runtime.kuuos_qi_world_licensed_effect_evidence_closure_v1_8 import (
    build_post_effect_blocker_certificate,
    validate_post_effect_blocker_certificate,
)
from runtime.kuuos_qi_world_native_full_cycle_v1_3 import _build_downstream
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.v017_host_adapter_fixtures import registry

VERSION = "kuuos_qi_world_successor_licensed_cycle_materialization_v2_0"
HANDOFF_VERSION = "kuuos_qi_world_successor_licensed_act_handoff_receipt_v2_0"
CLOSURE_VERSION = "kuuos_qi_world_successor_evidence_closure_receipt_v2_0"
CYCLE_RECEIPT_VERSION = "kuuos_qi_world_closed_licensed_cycle_receipt_v2_0"
CHAIN_VERSION = "kuuos_qi_world_digest_linked_multi_cycle_chain_v2_0"
CYCLE_ID = "qi-world-successor-licensed-cycle-materialization-v20"

MATERIALIZATION_NON_AUTHORITY = {
    "materialization_grants_truth": False,
    "materialization_grants_world_identity": False,
    "materialization_grants_memory_overwrite": False,
    "materialization_issues_further_authority": False,
    "materialization_replays_predecessor_receipt": False,
    "materialization_inherits_predecessor_authority": False,
}
CLOSURE_NON_AUTHORITY = {
    "closure_grants_execution": False,
    "closure_grants_truth": False,
    "closure_issues_authority": False,
    "closure_starts_next_act": False,
    "closure_updates_exact_world": False,
    "closure_overwrites_history": False,
}
CYCLE_NON_AUTHORITY = {
    "receipt_grants_execution": False,
    "receipt_grants_truth": False,
    "receipt_grants_world_identity": False,
    "receipt_grants_memory_overwrite": False,
    "receipt_issues_successor_authority": False,
    "receipt_renews_consumed_authority": False,
}
CHAIN_NON_AUTHORITY = {
    "chain_is_execution_capability": False,
    "chain_issues_authority": False,
    "chain_replays_closed_receipts": False,
    "chain_overwrites_history": False,
    "chain_collapses_worlds": False,
    "chain_promotes_truth": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def successor_handoff_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_licensed_act_handoff_receipt_digest")


def successor_closure_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "successor_evidence_closure_receipt_digest")


def second_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "licensed_cycle_receipt_digest")


def multi_cycle_chain_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "multi_cycle_chain_digest")


def _basis_bridge(plan: Mapping[str, Any]) -> dict[str, Any]:
    bridge = {
        "next_plan_basis_digest": plan["next_plan_basis_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "plan_state_digest": plan["plan_state_digest"],
        "committed_plan_digest": plan["latest_committed_plan_digest"],
        "bridge_read_only": True,
        "bridge_grants_execution": False,
        "basis_bridge_digest": "",
    }
    bridge["basis_bridge_digest"] = _digest_without(bridge, "basis_bridge_digest")
    return bridge


def _fresh_authority(
    predecessor: Mapping[str, Any],
    plan: Mapping[str, Any],
    host_license: Mapping[str, Any],
) -> dict[str, Any]:
    packet = deepcopy(
        dict(predecessor["source_v17_handoff_receipt"]["external_authority_packet"])
    )
    bridge = _basis_bridge(plan)
    packet.update(
        {
            "authority_id": "qi-world-v20-successor-external-authority",
            "source_blocker_receipt_digest": predecessor["successor_basis_digest"],
            "source_blocker_certificate_digest": predecessor["successor_basis"][
                "post_effect_blocker_certificate_digest"
            ],
            "source_plan_state_digest": plan["plan_state_digest"],
            "source_plan_basis_digest": plan["next_plan_basis_digest"],
            "source_committed_plan_digest": plan["latest_committed_plan_digest"],
            "materialized_plan_basis_digest": plan["plan_basis_digest"],
            "basis_bridge_digest": bridge["basis_bridge_digest"],
            "predecessor_cycle_receipt_digest": predecessor[
                "licensed_cycle_receipt_digest"
            ],
            "predecessor_cycle_ordinal": 1,
            "target_cycle_ordinal": 2,
            "host_license_digest": host_license["host_license_digest"],
            "human_approval_receipt_digest": sha(
                "qi-world-v20-fresh-human-approval"
            ),
            "human_approver_id": "external-human-operator-v20",
            "issued_at_ms": 290_000,
            "expires_at_ms": 380_000,
            "external_authority_packet_digest": "",
        }
    )
    packet["external_authority_packet_digest"] = authority_packet_digest(packet)
    return packet


def _materialize_act(
    root: Path,
    predecessor: Mapping[str, Any],
    requirement: Mapping[str, Any],
    plan: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy, bundle, host_license, projection = host_inputs(
        job_id="qi-world-v20-job",
        expires_at_ms=380_000,
    )
    candidate = _fresh_authority(predecessor, plan, host_license)
    intake = build_successor_authority_intake(
        requirement=requirement,
        closed_cycle_receipt=predecessor,
        candidate_external_authority_packet=candidate,
    )
    intake_errors = validate_successor_authority_intake(
        intake,
        requirement=requirement,
        closed_cycle_receipt=predecessor,
        candidate_external_authority_packet=candidate,
    )
    if intake_errors:
        raise ValueError("successor_intake_invalid:" + ";".join(intake_errors))

    activation = build_plan_phase_activation_receipt(
        state=plan,
        mission_cycle_phase="plan",
        mission_cycle_state_digest=requirement[
            "successor_authority_requirement_digest"
        ],
        plan_phase_receipt_digest=sha("qi-world-v20-plan-phase"),
        now_ms=290_000,
    )
    store = ActStore(root)
    state = store.initialize(
        build_initial_act_state(
            act_id="qi-world-v20-act",
            plan_state=plan,
            plan_activation_receipt=activation,
            now_ms=290_000,
        )
    )
    operation_input_digest = sha({"value": 2})
    state = apply_act(
        store,
        state,
        "select",
        {
            "plan_state": deepcopy(dict(plan)),
            "selected_step_id": RELEASE_SCOPE["selected_step_id"],
            "operation_id": RELEASE_SCOPE["operation_id"],
            "operation_input_digest": operation_input_digest,
        },
        1,
    )
    authorization = build_step_authorization(
        state=state,
        authorization_id="qi-world-v20-step-authorization",
        operation_id=RELEASE_SCOPE["operation_id"],
        operation_input_digest=operation_input_digest,
        act_phase_receipt_digest=candidate["external_authority_packet_digest"],
        invocation_id="qi-world-v20-single-invocation",
        source_supervisor_bundle_digest=projection[
            "source_supervisor_bundle_digest"
        ],
        host_job_id="qi-world-v20-job",
        host_step_id="step-1",
        host_license=host_license,
        human_approval_receipt_digest=candidate[
            "human_approval_receipt_digest"
        ],
        human_approver_id=candidate["human_approver_id"],
        issued_at_ms=290_000,
        expires_at_ms=380_000,
    )
    state = apply_act(
        store,
        state,
        "authorize",
        {"step_authorization": authorization, "host_license": deepcopy(host_license)},
        2,
    )
    state = apply_act(
        store,
        state,
        "project",
        {"host_projection": deepcopy(projection)},
        3,
    )
    invoke_event, host_tick = build_authorized_invoke_event(
        state=state,
        supervisor_bundle=bundle,
        worker_id="qi-world-v20-worker",
        now_ms=290_004,
        supervisor_policy=policy,
        registry=registry(),
    )
    result = store.apply(invoke_event)
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    state = result["state"]
    state = apply_act(
        store,
        state,
        "verify",
        {"verification_receipt_digest": sha("qi-world-v20-act-verification")},
        5,
    )
    result = store.apply(
        build_fixture_event(
            state,
            "commit",
            {
                "memory_overwrite": False,
                "automatic_truth_promotion": False,
                "automatic_plan_completion": False,
                "automatic_rollback": False,
                "lower_host_receipt_canonical": True,
                "source_lineage_preserved": True,
                "non_authority": act_non_authority(),
            },
            6,
        )
    )
    if result.get("status") != "APPLIED":
        raise AssertionError(result)
    state = result["state"]
    errors = validate_act_state(state)
    if errors:
        raise ValueError("successor_act_invalid:" + ";".join(errors))
    return state, activation, candidate, intake, host_tick


def build_successor_licensed_act_handoff_receipt(root: Path) -> dict[str, Any]:
    predecessor = build_licensed_cycle_receipt(root / "predecessor-v19")
    errors = validate_licensed_cycle_receipt(predecessor)
    if errors:
        raise ValueError("predecessor_invalid:" + ";".join(errors))
    requirement = build_successor_authority_requirement(predecessor)
    errors = validate_successor_authority_requirement(
        requirement, closed_cycle_receipt=predecessor
    )
    if errors:
        raise ValueError("requirement_invalid:" + ";".join(errors))
    plan = deepcopy(
        dict(
            predecessor["source_v18_closure_receipt"]["next_cycle_artifacts"][
                "PlanOS"
            ]
        )
    )
    errors = validate_plan_state(plan)
    if errors:
        raise ValueError("successor_plan_invalid:" + ";".join(errors))
    act, activation, candidate, intake, host_tick = _materialize_act(
        root / "act", predecessor, requirement, plan
    )
    bridge = _basis_bridge(plan)
    discharge = {
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "external_authority_packet_digest": candidate[
            "external_authority_packet_digest"
        ],
        "basis_bridge_digest": bridge["basis_bridge_digest"],
        "single_use_release": True,
        "release_consumption_count": 1,
        "released_act_state_digest": act["act_state_digest"],
        "predecessor_receipt_consumed": False,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "blocker_discharge_certificate_digest": "",
    }
    discharge["blocker_discharge_certificate_digest"] = _digest_without(
        discharge, "blocker_discharge_certificate_digest"
    )
    receipt = {
        "version": HANDOFF_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_closed_cycle_receipt": deepcopy(predecessor),
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "successor_authority_requirement": deepcopy(requirement),
        "successor_authority_requirement_digest": requirement[
            "successor_authority_requirement_digest"
        ],
        "successor_authority_intake": deepcopy(intake),
        "successor_authority_intake_digest": intake[
            "successor_authority_intake_digest"
        ],
        "basis_bridge": bridge,
        "basis_bridge_digest": bridge["basis_bridge_digest"],
        "source_plan_state": deepcopy(plan),
        "source_plan_state_digest": plan["plan_state_digest"],
        "source_plan_basis_digest": plan["next_plan_basis_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "source_committed_plan_digest": plan["latest_committed_plan_digest"],
        "plan_activation_receipt": deepcopy(activation),
        "external_authority_packet": deepcopy(candidate),
        "blocker_discharge_certificate": discharge,
        "target_act_state": deepcopy(act),
        "host_tick_digest": host_tick["host_tick_digest"],
        "source_cycle_immutable": True,
        "source_receipt_read_only": True,
        "source_receipt_consumed": False,
        "predecessor_authority_inherited": False,
        "predecessor_authority_renewed": False,
        "target_cycle_strictly_later": True,
        "release_consumed": True,
        "release_consumption_count": 1,
        "target_act_started": True,
        "effect_recorded": True,
        "observation_required": True,
        "verification_required": True,
        "memory_overwritten": False,
        "exact_world_updated": False,
        "truth_promoted": False,
        "same_cycle_recursive_invocation": False,
        "multi_world_collapsed": False,
        "non_authority": deepcopy(MATERIALIZATION_NON_AUTHORITY),
        "successor_licensed_act_handoff_receipt_digest": "",
    }
    receipt["successor_licensed_act_handoff_receipt_digest"] = successor_handoff_digest(
        receipt
    )
    errors = validate_successor_licensed_act_handoff_receipt(receipt)
    if errors:
        raise ValueError("successor_handoff_invalid:" + ";".join(errors))
    return receipt


def validate_successor_licensed_act_handoff_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(receipt.get("version") == HANDOFF_VERSION, "handoff_version_invalid")
        req(
            receipt.get("successor_licensed_act_handoff_receipt_digest")
            == successor_handoff_digest(receipt),
            "handoff_digest_invalid",
        )
        req(receipt.get("cycle_ordinal") == 2, "handoff_cycle_ordinal_invalid")
        predecessor = dict(receipt.get("predecessor_closed_cycle_receipt", {}))
        errors += [
            "handoff_predecessor_" + e
            for e in validate_licensed_cycle_receipt(predecessor)
        ]
        req(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "handoff_predecessor_digest_mismatch",
        )
        requirement = dict(receipt.get("successor_authority_requirement", {}))
        errors += [
            "handoff_requirement_" + e
            for e in validate_successor_authority_requirement(
                requirement, closed_cycle_receipt=predecessor
            )
        ]
        candidate = dict(receipt.get("external_authority_packet", {}))
        intake = dict(receipt.get("successor_authority_intake", {}))
        errors += [
            "handoff_intake_" + e
            for e in validate_successor_authority_intake(
                intake,
                requirement=requirement,
                closed_cycle_receipt=predecessor,
                candidate_external_authority_packet=candidate,
            )
        ]
        req(
            candidate.get("external_authority_packet_digest")
            == authority_packet_digest(candidate),
            "handoff_authority_digest_invalid",
        )
        req(
            candidate.get("external_authority_packet_digest")
            != predecessor.get("consumed_external_authority_packet_digest"),
            "handoff_predecessor_authority_reuse",
        )
        req(
            candidate.get("human_approval_receipt_digest")
            != predecessor.get("consumed_human_approval_receipt_digest"),
            "handoff_predecessor_approval_reuse",
        )
        req(
            candidate.get("host_license_digest")
            != predecessor.get("consumed_host_license_digest"),
            "handoff_predecessor_host_license_reuse",
        )
        plan = dict(receipt.get("source_plan_state", {}))
        errors += ["handoff_plan_" + e for e in validate_plan_state(plan)]
        bridge = dict(receipt.get("basis_bridge", {}))
        req(bridge == _basis_bridge(plan), "handoff_basis_bridge_substitution")
        req(
            candidate.get("source_plan_basis_digest")
            == plan.get("next_plan_basis_digest"),
            "handoff_authority_next_plan_basis_mismatch",
        )
        req(
            candidate.get("materialized_plan_basis_digest")
            == plan.get("plan_basis_digest"),
            "handoff_authority_materialized_basis_mismatch",
        )
        req(
            candidate.get("basis_bridge_digest") == bridge.get("basis_bridge_digest"),
            "handoff_authority_basis_bridge_mismatch",
        )
        act = dict(receipt.get("target_act_state", {}))
        errors += ["handoff_act_" + e for e in validate_act_state(act)]
        req(act.get("current_phase") == "commit", "handoff_act_not_committed")
        req(act.get("route") == "EFFECT_RECORDED", "handoff_act_route_invalid")
        req(
            act.get("source_plan_basis_digest") == plan.get("plan_basis_digest"),
            "handoff_act_materialized_basis_mismatch",
        )
        authorization = dict(act.get("step_authorization", {}))
        req(
            authorization.get("act_phase_receipt_digest")
            == candidate.get("external_authority_packet_digest"),
            "handoff_authorization_authority_mismatch",
        )
        req(
            authorization.get("host_license_digest")
            == candidate.get("host_license_digest"),
            "handoff_authorization_host_license_mismatch",
        )
        req(
            authorization.get("human_approval_receipt_digest")
            == candidate.get("human_approval_receipt_digest"),
            "handoff_authorization_approval_mismatch",
        )
        discharge = dict(receipt.get("blocker_discharge_certificate", {}))
        req(
            discharge.get("blocker_discharge_certificate_digest")
            == _digest_without(discharge, "blocker_discharge_certificate_digest"),
            "handoff_discharge_digest_invalid",
        )
        req(
            discharge.get("release_consumption_count") == 1
            and discharge.get("single_use_release") is True,
            "handoff_discharge_not_single_use",
        )
        expected = {
            "source_cycle_immutable": True,
            "source_receipt_read_only": True,
            "source_receipt_consumed": False,
            "predecessor_authority_inherited": False,
            "predecessor_authority_renewed": False,
            "target_cycle_strictly_later": True,
            "release_consumed": True,
            "release_consumption_count": 1,
            "target_act_started": True,
            "effect_recorded": True,
            "observation_required": True,
            "verification_required": True,
            "memory_overwritten": False,
            "exact_world_updated": False,
            "truth_promoted": False,
            "same_cycle_recursive_invocation": False,
            "multi_world_collapsed": False,
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"handoff_{field}_invalid")
        req(
            dict(receipt.get("non_authority", {}))
            == MATERIALIZATION_NON_AUTHORITY,
            "handoff_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _native_errors(states: Mapping[str, Mapping[str, Any]]) -> list[str]:
    validators = {
        "ObserveOS": validate_observe_state,
        "VerifyOS": validate_verify_state,
        "LearnOS": validate_learn_state,
    }
    errors: list[str] = []
    for name, validator in validators.items():
        state = states.get(name)
        if not isinstance(state, Mapping):
            errors.append(f"{name}_missing")
        else:
            errors += [f"{name}:{e}" for e in validator(state)]
    return errors


def _evidence_lineage(source: Mapping[str, Any], states: Mapping[str, Mapping[str, Any]]) -> str:
    return sha(
        {
            "predecessor_cycle_receipt_digest": source[
                "predecessor_cycle_receipt_digest"
            ],
            "successor_handoff_receipt_digest": source[
                "successor_licensed_act_handoff_receipt_digest"
            ],
            "act_state_digest": states["ActOS"]["act_state_digest"],
            "observe_state_digest": states["ObserveOS"]["observe_state_digest"],
            "verify_state_digest": states["VerifyOS"]["verify_state_digest"],
            "learn_state_digest": states["LearnOS"]["learn_state_digest"],
        }
    )


def _next_cycle(
    root: Path,
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    lineage: str,
) -> dict[str, dict[str, Any]]:
    learn = states["LearnOS"]
    predecessor = source["predecessor_closed_cycle_receipt"]
    previous = {
        "native_artifacts": deepcopy(dict(states)),
        "world_projection_digest": predecessor["source_v18_closure_receipt"][
            "post_effect_world_projection_digest"
        ],
        "process_lineage_digest": lineage,
        "native_full_cycle_receipt_digest": "",
    }
    previous["native_full_cycle_receipt_digest"] = sha(previous)
    lineage_id = str(learn["lineage_id"])
    belief, activation = _reentry._build_next_belief(
        root / "belief", lineage_id=lineage_id, previous_receipt=previous
    )
    decision = _build_next_decision(
        root / "decision",
        lineage_id=lineage_id,
        mission_contract_digest=str(learn["mission_contract_digest"]),
        previous_learn_state_digest=str(learn["learn_state_digest"]),
        belief_activation=activation,
    )
    plural = _reentry._build_next_plural(
        root / "plural", lineage_id=lineage_id, decision=decision
    )
    wa = _reentry._build_next_wa(root / "wa", plural)
    plan = _build_next_plan_from_learning(
        root / "plan", wa, str(learn["learning_delta_digest"])
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


def _world_projection(
    source: Mapping[str, Any],
    states: Mapping[str, Mapping[str, Any]],
    next_artifacts: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    predecessor = source["predecessor_closed_cycle_receipt"]
    packet = {
        "projection_kind": "successor_licensed_cycle_projection_v2_0",
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_world_projection_digest": predecessor[
            "source_v18_closure_receipt"
        ]["post_effect_world_projection_digest"],
        "successor_handoff_receipt_digest": source[
            "successor_licensed_act_handoff_receipt_digest"
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


def build_successor_evidence_closure_receipt(root: Path) -> dict[str, Any]:
    source = build_successor_licensed_act_handoff_receipt(root / "handoff")
    act = deepcopy(dict(source["target_act_state"]))
    observe, verify, learn = _build_downstream(root / "evidence", act)
    states = {"ActOS": act, "ObserveOS": observe, "VerifyOS": verify, "LearnOS": learn}
    errors = _native_errors(states)
    if errors:
        raise ValueError("native_evidence_invalid:" + ";".join(errors))
    lineage = _evidence_lineage(source, states)
    next_artifacts = _next_cycle(root / "next-cycle", source, states, lineage)
    world = _world_projection(source, states, next_artifacts)
    blocker = build_post_effect_blocker_certificate(
        source=source,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    errors = validate_post_effect_blocker_certificate(
        blocker,
        source=source,
        states=states,
        next_artifacts=next_artifacts,
        world=world,
    )
    if errors:
        raise ValueError("blocker_invalid:" + ";".join(errors))
    receipt = {
        "version": CLOSURE_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "source_successor_handoff_receipt": deepcopy(source),
        "source_successor_handoff_receipt_digest": source[
            "successor_licensed_act_handoff_receipt_digest"
        ],
        "predecessor_cycle_receipt_digest": source[
            "predecessor_cycle_receipt_digest"
        ],
        "native_evidence_states": deepcopy(states),
        "native_evidence_lineage_digest": lineage,
        "next_cycle_artifacts": deepcopy(next_artifacts),
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
        "all_post_effect_blockers_active": True,
        "indra_transport_still_unrealized": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CLOSURE_NON_AUTHORITY),
        "successor_evidence_closure_receipt_digest": "",
    }
    receipt["successor_evidence_closure_receipt_digest"] = successor_closure_digest(
        receipt
    )
    errors = validate_successor_evidence_closure_receipt(receipt)
    if errors:
        raise ValueError("closure_invalid:" + ";".join(errors))
    return receipt


def validate_successor_evidence_closure_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(receipt.get("version") == CLOSURE_VERSION, "closure_version_invalid")
        req(
            receipt.get("successor_evidence_closure_receipt_digest")
            == successor_closure_digest(receipt),
            "closure_digest_invalid",
        )
        source = dict(receipt.get("source_successor_handoff_receipt", {}))
        errors += [
            "closure_source_" + e
            for e in validate_successor_licensed_act_handoff_receipt(source)
        ]
        states = dict(receipt.get("native_evidence_states", {}))
        errors += ["closure_" + e for e in _native_errors(states)]
        act = dict(states.get("ActOS", {}))
        observe = dict(states.get("ObserveOS", {}))
        verify = dict(states.get("VerifyOS", {}))
        learn = dict(states.get("LearnOS", {}))
        req(
            act == dict(source.get("target_act_state", {})),
            "closure_source_act_state_substitution",
        )
        req(
            observe.get("source_act_state_digest") == act.get("act_state_digest"),
            "closure_observe_source_act_mismatch",
        )
        req(
            verify.get("source_observe_state_digest")
            == observe.get("observe_state_digest"),
            "closure_verify_source_observe_mismatch",
        )
        req(
            learn.get("source_verify_state_digest") == verify.get("verify_state_digest"),
            "closure_learn_source_verify_mismatch",
        )
        req(
            receipt.get("native_evidence_lineage_digest")
            == _evidence_lineage(source, states),
            "closure_evidence_lineage_digest_mismatch",
        )
        next_artifacts = dict(receipt.get("next_cycle_artifacts", {}))
        errors += [
            "closure_next_" + e
            for e in _reentry._validate_next_artifacts(next_artifacts)
        ]
        req(
            next_artifacts.get("PlanOS", {}).get("next_plan_basis_digest")
            == learn.get("learning_delta_digest"),
            "closure_next_plan_learning_basis_mismatch",
        )
        world = dict(receipt.get("post_effect_world_projection", {}))
        req(
            world.get("world_projection_digest")
            == _digest_without(world, "world_projection_digest"),
            "closure_world_digest_invalid",
        )
        req(
            world.get("projection_read_only") is True
            and world.get("runtime_updates_world") is False
            and world.get("exact_world_identified") is False,
            "closure_world_boundary_invalid",
        )
        blocker = dict(receipt.get("post_effect_blocker_certificate", {}))
        errors += validate_post_effect_blocker_certificate(
            blocker,
            source=source,
            states=states,
            next_artifacts=next_artifacts,
            world=world,
        )
        req(
            blocker.get("all_required_blockers_active") is True
            and blocker.get("missing_blockers") == []
            and blocker.get("next_act_not_started") is True,
            "closure_blockers_not_restored",
        )
        expected = {
            "source_effect_immutable": True,
            "source_authority_consumed_once": True,
            "observation_debt_discharged": True,
            "verification_debt_discharged": True,
            "learning_recorded": True,
            "replan_debt_discharged": True,
            "next_act_not_started": True,
            "all_post_effect_blockers_active": True,
            "indra_transport_still_unrealized": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"closure_{field}_invalid")
        req(
            dict(receipt.get("non_authority", {})) == CLOSURE_NON_AUTHORITY,
            "closure_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _terminal_digest(closure: Mapping[str, Any]) -> str:
    states = closure["native_evidence_states"]
    plan = closure["next_cycle_artifacts"]["PlanOS"]
    return sha(
        {
            "act": states["ActOS"]["act_state_digest"],
            "observe": states["ObserveOS"]["observe_state_digest"],
            "verify": states["VerifyOS"]["verify_state_digest"],
            "learn": states["LearnOS"]["learn_state_digest"],
            "next_plan": plan["plan_state_digest"],
            "blockers": closure["post_effect_blocker_certificate_digest"],
            "world": closure["post_effect_world_projection_digest"],
        }
    )


def _successor_basis(closure: Mapping[str, Any]) -> dict[str, Any]:
    plan = closure["next_cycle_artifacts"]["PlanOS"]
    blocker = closure["post_effect_blocker_certificate"]
    return {
        "next_plan_state_digest": plan["plan_state_digest"],
        "next_plan_basis_digest": plan["next_plan_basis_digest"],
        "next_committed_plan_digest": plan["latest_committed_plan_digest"],
        "materialized_plan_basis_digest": plan["plan_basis_digest"],
        "post_effect_blocker_certificate_digest": closure[
            "post_effect_blocker_certificate_digest"
        ],
        "post_effect_world_projection_digest": closure[
            "post_effect_world_projection_digest"
        ],
        "all_required_blockers_active": blocker["all_required_blockers_active"],
        "next_act_not_started": blocker["next_act_not_started"],
    }


def build_second_closed_cycle_receipt(root: Path) -> dict[str, Any]:
    closure = build_successor_evidence_closure_receipt(root / "closure")
    handoff = closure["source_successor_handoff_receipt"]
    predecessor = handoff["predecessor_closed_cycle_receipt"]
    authority = handoff["external_authority_packet"]
    basis = _successor_basis(closure)
    receipt = {
        "version": CYCLE_RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_ordinal": 2,
        "predecessor_cycle_receipt_digest": predecessor[
            "licensed_cycle_receipt_digest"
        ],
        "source_successor_handoff_receipt": deepcopy(handoff),
        "source_successor_closure_receipt": deepcopy(closure),
        "consumed_external_authority_packet_digest": authority[
            "external_authority_packet_digest"
        ],
        "consumed_human_approval_receipt_digest": authority[
            "human_approval_receipt_digest"
        ],
        "consumed_host_license_digest": authority["host_license_digest"],
        "terminal_state_digest": _terminal_digest(closure),
        "successor_basis": basis,
        "successor_basis_digest": sha(basis),
        "cycle_started": True,
        "effect_recorded": True,
        "observation_closed": True,
        "verification_closed": True,
        "learning_closed": True,
        "replan_closed": True,
        "cycle_closed": True,
        "closed_cycle_immutable": True,
        "closed_cycle_append_only": True,
        "receipt_replay_forbidden": True,
        "receipt_consumption_count": 0,
        "consumed_authority_single_use": True,
        "consumed_authority_renewable": False,
        "consumed_authority_inheritable": False,
        "next_act_started": False,
        "all_post_effect_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CYCLE_NON_AUTHORITY),
        "licensed_cycle_receipt_digest": "",
    }
    receipt["licensed_cycle_receipt_digest"] = second_cycle_receipt_digest(receipt)
    errors = validate_second_closed_cycle_receipt(receipt)
    if errors:
        raise ValueError("second_cycle_invalid:" + ";".join(errors))
    return receipt


def validate_second_closed_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(
            receipt.get("version") == CYCLE_RECEIPT_VERSION,
            "cycle_receipt_version_invalid",
        )
        req(
            receipt.get("licensed_cycle_receipt_digest")
            == second_cycle_receipt_digest(receipt),
            "cycle_receipt_digest_invalid",
        )
        handoff = dict(receipt.get("source_successor_handoff_receipt", {}))
        closure = dict(receipt.get("source_successor_closure_receipt", {}))
        errors += [
            "cycle_receipt_handoff_" + e
            for e in validate_successor_licensed_act_handoff_receipt(handoff)
        ]
        errors += [
            "cycle_receipt_closure_" + e
            for e in validate_successor_evidence_closure_receipt(closure)
        ]
        req(
            closure.get("source_successor_handoff_receipt") == handoff,
            "cycle_receipt_handoff_closure_substitution",
        )
        predecessor = handoff["predecessor_closed_cycle_receipt"]
        req(
            receipt.get("predecessor_cycle_receipt_digest")
            == predecessor.get("licensed_cycle_receipt_digest"),
            "cycle_receipt_predecessor_link_mismatch",
        )
        authority = handoff["external_authority_packet"]
        req(
            receipt.get("consumed_external_authority_packet_digest")
            == authority.get("external_authority_packet_digest"),
            "cycle_receipt_authority_digest_mismatch",
        )
        req(
            receipt.get("consumed_human_approval_receipt_digest")
            == authority.get("human_approval_receipt_digest"),
            "cycle_receipt_human_approval_digest_mismatch",
        )
        req(
            receipt.get("consumed_host_license_digest")
            == authority.get("host_license_digest"),
            "cycle_receipt_host_license_digest_mismatch",
        )
        req(
            dict(receipt.get("non_authority", {})) == CYCLE_NON_AUTHORITY,
            "cycle_receipt_non_authority_invalid",
        )
        req(
            receipt.get("terminal_state_digest") == _terminal_digest(closure),
            "cycle_receipt_terminal_state_digest_mismatch",
        )
        basis = dict(receipt.get("successor_basis", {}))
        req(
            basis == _successor_basis(closure),
            "cycle_receipt_successor_basis_substitution",
        )
        req(
            receipt.get("successor_basis_digest") == sha(basis),
            "cycle_receipt_successor_basis_digest_invalid",
        )
        expected = {
            "cycle_started": True,
            "effect_recorded": True,
            "observation_closed": True,
            "verification_closed": True,
            "learning_closed": True,
            "replan_closed": True,
            "cycle_closed": True,
            "closed_cycle_immutable": True,
            "closed_cycle_append_only": True,
            "receipt_replay_forbidden": True,
            "consumed_authority_single_use": True,
            "consumed_authority_renewable": False,
            "consumed_authority_inheritable": False,
            "next_act_started": False,
            "all_post_effect_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(receipt.get(field) == value, f"cycle_receipt_{field}_invalid")
        req(
            receipt.get("receipt_consumption_count") == 0,
            "cycle_receipt_consumption_forbidden",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def build_digest_linked_multi_cycle_chain(root: Path) -> dict[str, Any]:
    second = build_second_closed_cycle_receipt(root / "second-cycle")
    first = second["source_successor_handoff_receipt"][
        "predecessor_closed_cycle_receipt"
    ]
    chain = {
        "version": CHAIN_VERSION,
        "cycle_id": CYCLE_ID,
        "cycle_count": 2,
        "cycle_ordinals": [1, 2],
        "first_cycle_receipt": deepcopy(first),
        "first_cycle_receipt_digest": first["licensed_cycle_receipt_digest"],
        "second_cycle_receipt": deepcopy(second),
        "second_cycle_receipt_digest": second["licensed_cycle_receipt_digest"],
        "authority_packet_digests": [
            first["consumed_external_authority_packet_digest"],
            second["consumed_external_authority_packet_digest"],
        ],
        "human_approval_receipt_digests": [
            first["consumed_human_approval_receipt_digest"],
            second["consumed_human_approval_receipt_digest"],
        ],
        "host_license_digests": [
            first["consumed_host_license_digest"],
            second["consumed_host_license_digest"],
        ],
        "authority_packets_distinct": True,
        "human_approvals_distinct": True,
        "host_licenses_distinct": True,
        "all_cycles_closed": True,
        "all_receipts_immutable": True,
        "all_receipts_append_only": True,
        "all_receipts_non_consumable": True,
        "all_authorities_single_use": True,
        "no_authority_inheritance": True,
        "no_authority_renewal": True,
        "next_act_started": False,
        "all_blockers_active": True,
        "exact_world_updated": False,
        "history_overwritten": False,
        "truth_promoted": False,
        "non_authority": deepcopy(CHAIN_NON_AUTHORITY),
        "multi_cycle_chain_digest": "",
    }
    chain["multi_cycle_chain_digest"] = multi_cycle_chain_digest(chain)
    errors = validate_digest_linked_multi_cycle_chain(chain)
    if errors:
        raise ValueError("chain_invalid:" + ";".join(errors))
    return chain


def validate_digest_linked_multi_cycle_chain(chain: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []

    def req(ok: bool, code: str) -> None:
        if not ok:
            errors.append(code)

    try:
        req(chain.get("version") == CHAIN_VERSION, "chain_version_invalid")
        req(
            chain.get("multi_cycle_chain_digest")
            == multi_cycle_chain_digest(chain),
            "chain_digest_invalid",
        )
        first = dict(chain.get("first_cycle_receipt", {}))
        second = dict(chain.get("second_cycle_receipt", {}))
        errors += ["chain_first_" + e for e in validate_licensed_cycle_receipt(first)]
        errors += [
            "chain_second_" + e for e in validate_second_closed_cycle_receipt(second)
        ]
        req(
            chain.get("cycle_count") == 2
            and chain.get("cycle_ordinals") == [1, 2],
            "chain_cycle_sequence_invalid",
        )
        req(
            second.get("predecessor_cycle_receipt_digest")
            == first.get("licensed_cycle_receipt_digest"),
            "chain_predecessor_link_mismatch",
        )
        authorities = list(chain.get("authority_packet_digests", []))
        approvals = list(chain.get("human_approval_receipt_digests", []))
        licenses = list(chain.get("host_license_digests", []))
        req(
            chain.get("first_cycle_receipt_digest")
            == first.get("licensed_cycle_receipt_digest")
            and chain.get("second_cycle_receipt_digest")
            == second.get("licensed_cycle_receipt_digest"),
            "chain_receipt_digest_inventory_invalid",
        )
        req(
            authorities
            == [
                first.get("consumed_external_authority_packet_digest"),
                second.get("consumed_external_authority_packet_digest"),
            ],
            "chain_authority_inventory_invalid",
        )
        req(
            approvals
            == [
                first.get("consumed_human_approval_receipt_digest"),
                second.get("consumed_human_approval_receipt_digest"),
            ],
            "chain_approval_inventory_invalid",
        )
        req(
            licenses
            == [
                first.get("consumed_host_license_digest"),
                second.get("consumed_host_license_digest"),
            ],
            "chain_host_license_inventory_invalid",
        )
        req(
            len(authorities) == 2 and len(set(authorities)) == 2,
            "chain_authority_distinctness_invalid",
        )
        req(
            len(approvals) == 2 and len(set(approvals)) == 2,
            "chain_approval_distinctness_invalid",
        )
        req(
            len(licenses) == 2 and len(set(licenses)) == 2,
            "chain_host_license_distinctness_invalid",
        )
        expected = {
            "authority_packets_distinct": True,
            "human_approvals_distinct": True,
            "host_licenses_distinct": True,
            "all_cycles_closed": True,
            "all_receipts_immutable": True,
            "all_receipts_append_only": True,
            "all_receipts_non_consumable": True,
            "all_authorities_single_use": True,
            "no_authority_inheritance": True,
            "no_authority_renewal": True,
            "next_act_started": False,
            "all_blockers_active": True,
            "exact_world_updated": False,
            "history_overwritten": False,
            "truth_promoted": False,
        }
        for field, value in expected.items():
            req(chain.get(field) == value, f"chain_{field}_invalid")
        req(
            dict(chain.get("non_authority", {})) == CHAIN_NON_AUTHORITY,
            "chain_non_authority_invalid",
        )
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
