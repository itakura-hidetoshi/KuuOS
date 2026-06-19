from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_fixture_v0_1 import prepared_gated_state
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state, source_act_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_qi_world_os_interface_bridge_v1_0 import (
    build_qi_world_os_interface_receipt,
    validate_qi_world_os_interface_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    OS_INTERFACE_SPECS,
    OS_KINDS,
)
from runtime.kuuos_verify_os_fixture_v0_1 import prepared_corroborated_state
from runtime.kuuos_verify_os_kernel_v0_1 import validate_verify_state
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify

VERSION = "kuuos_qi_world_native_evidence_loop_v1_2"
RECEIPT_VERSION = "kuuos_qi_world_native_evidence_loop_receipt_v1_2"

NATIVE_NON_AUTHORITY = {
    "adapter_grants_execution": False,
    "adapter_grants_truth": False,
    "adapter_issues_authority": False,
    "adapter_changes_native_state": False,
    "adapter_updates_exact_world": False,
    "adapter_overwrites_history": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def native_loop_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "native_loop_receipt_digest")


def _build_native_states(root: Path) -> dict[str, dict[str, Any]]:
    act_state = source_act_state(root / "act")

    observe_store, observe_pending = prepared_assessed_state(
        root=root / "observe",
        observe_id="qi-world-native-observe",
        act_state=act_state,
    )
    observe_state, _ = finish_observe(
        store=observe_store,
        state=observe_pending,
        verdict="MATCHED",
        tick=5,
    )

    verify_store, verify_pending = prepared_corroborated_state(
        root=root / "verify",
        verify_id="qi-world-native-verify",
        observe_state=observe_state,
        admissible=True,
    )
    verify_state, _ = finish_verify(
        store=verify_store,
        state=verify_pending,
        verdict="PASSED",
        criterion_satisfied=True,
        tick=4,
    )

    learn_store, learn_pending = prepared_gated_state(
        root=root / "learn",
        learn_id="qi-world-native-learn",
        verify_state=verify_state,
        learning_kind="reinforcement",
        target_scope="belief_candidate",
    )
    learn_state, _ = finish_learn(
        store=learn_store,
        state=learn_pending,
        tick=5,
    )

    return {
        "ActOS": act_state,
        "ObserveOS": observe_state,
        "VerifyOS": verify_state,
        "LearnOS": learn_state,
    }


def _native_validation_errors(states: Mapping[str, Mapping[str, Any]]) -> list[str]:
    validators = {
        "ActOS": validate_act_state,
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


def _process_lineage_digest(states: Mapping[str, Mapping[str, Any]]) -> str:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    return sha(
        {
            "lineage_id": act["lineage_id"],
            "source_plan_state_digest": act["source_plan_state_digest"],
            "act_state_digest": act["act_state_digest"],
            "observe_state_digest": observe["observe_state_digest"],
            "verify_state_digest": verify["verify_state_digest"],
            "learn_state_digest": learn["learn_state_digest"],
        }
    )


def _build_world_projection(states: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    packet = {
        "projection_kind": "native_evidence_loop_projection",
        "lineage_id": act["lineage_id"],
        "source_plan_state_digest": act["source_plan_state_digest"],
        "source_committed_plan_digest": act["source_committed_plan_digest"],
        "act_state_digest": act["act_state_digest"],
        "observe_state_digest": observe["observe_state_digest"],
        "evidence_packet_digest": observe["evidence_packet_digest"],
        "verify_state_digest": verify["verify_state_digest"],
        "verification_evidence_digest": verify["verification_evidence_digest"],
        "learn_state_digest": learn["learn_state_digest"],
        "learning_delta_digest": learn["learning_delta_digest"],
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
        "world_projection_digest": "",
    }
    packet["world_projection_digest"] = _digest_without(
        packet, "world_projection_digest"
    )
    return packet


def _build_qi_receipt(states: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    history = [
        {
            "process_action": "ACT_EFFECT_RECORDED",
            "native_state_digest": act["act_state_digest"],
            "source_state_digest": act["source_plan_state_digest"],
            "target_state_digest": act["act_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_observation": "OBSERVATION_RECORDED",
            "native_state_digest": observe["observe_state_digest"],
            "source_state_digest": observe["source_act_state_digest"],
            "target_state_digest": observe["observe_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_observation": "VERIFICATION_RECORDED",
            "native_state_digest": verify["verify_state_digest"],
            "source_state_digest": verify["source_observe_state_digest"],
            "target_state_digest": verify["verify_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
        {
            "process_action": "FUTURE_LEARNING_RECORDED",
            "native_state_digest": learn["learn_state_digest"],
            "source_state_digest": learn["source_verify_state_digest"],
            "target_state_digest": learn["learn_state_digest"],
            "transition_visible": True,
            "memory_link_visible": True,
            "nonmarkov_link_visible": True,
        },
    ]
    raw = {
        "cycle_id": "qi-world-native-evidence-loop",
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "process_history": history,
    }
    return evaluate_qi_process_tensor(raw).to_dict()


def _base_packet(
    *,
    name: str,
    lineage_digest: str,
    world_digest: str,
    input_digest: str,
    output_digest: str,
) -> dict[str, Any]:
    spec = OS_INTERFACE_SPECS[name]
    return {
        "os_kind": name,
        "cycle_id": "qi-world-native-evidence-loop",
        "process_lineage_digest": lineage_digest,
        "world_projection_digest": world_digest,
        "world_relation": spec["world_relation"],
        "qi_relation": spec["qi_relation"],
        "output_kind": spec["output_kind"],
        "input_digest": input_digest,
        "output_digest": output_digest,
        "candidate_only": True,
        "nonfinal_marker": True,
    }


def _build_interface_receipt(
    states: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
    qi_receipt: Mapping[str, Any],
    lineage_digest: str,
) -> dict[str, Any]:
    act = states["ActOS"]
    observe = states["ObserveOS"]
    verify = states["VerifyOS"]
    learn = states["LearnOS"]
    world_digest = str(world["world_projection_digest"])
    belief_projection = sha(
        {
            "lineage_id": act["lineage_id"],
            "mission_contract_digest": act["mission_contract_digest"],
            "projection_only": True,
        }
    )
    decision_projection = act["source_wa_basis_digest"]
    plan_projection = act["source_plan_state_digest"]
    governance_digest = act["step_authorization_digest"]

    packets = {
        "BeliefOS": _base_packet(
            name="BeliefOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=world_digest,
            output_digest=belief_projection,
        ),
        "DecisionOS": _base_packet(
            name="DecisionOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=belief_projection,
            output_digest=decision_projection,
        ),
        "PlanOS": _base_packet(
            name="PlanOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=decision_projection,
            output_digest=plan_projection,
        ),
        "Governance": _base_packet(
            name="Governance",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=plan_projection,
            output_digest=governance_digest,
        ),
        "ActOS": _base_packet(
            name="ActOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=governance_digest,
            output_digest=act["act_state_digest"],
        ),
        "ObserveOS": _base_packet(
            name="ObserveOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=act["act_state_digest"],
            output_digest=observe["evidence_packet_digest"],
        ),
        "VerifyOS": _base_packet(
            name="VerifyOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=observe["evidence_packet_digest"],
            output_digest=verify["verification_evidence_digest"],
        ),
        "LearnOS": _base_packet(
            name="LearnOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=verify["verification_evidence_digest"],
            output_digest=learn["learning_delta_digest"],
        ),
    }
    packets["BeliefOS"].update(
        {
            "native_artifact": False,
            "projection_only": True,
            "upstream_identity_preserved_by_act": True,
        }
    )
    packets["DecisionOS"].update(
        {
            "native_artifact": False,
            "projection_only": True,
            "upstream_identity_preserved_by_act": True,
        }
    )
    packets["PlanOS"].update(
        {
            "native_artifact": False,
            "projection_only": True,
            "source_plan_state_digest": act["source_plan_state_digest"],
        }
    )
    packets["Governance"].update(
        {
            "cross_cutting": True,
            "single_stage": False,
            "act_admitted": True,
            "step_authorization_digest": governance_digest,
            "host_license_digest": act["host_license_digest"],
        }
    )
    packets["ActOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": act["act_state_digest"],
            "governance_decision_digest": governance_digest,
            "external_authority_receipt_digest": act["host_license_digest"],
            "actual_intervention_appended": True,
        }
    )
    packets["ObserveOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": observe["observe_state_digest"],
            "source_act_state_digest": observe["source_act_state_digest"],
            "observation_only": True,
            "verification_complete": False,
        }
    )
    packets["VerifyOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": verify["verify_state_digest"],
            "source_observe_state_digest": verify["source_observe_state_digest"],
            "observation_digest": observe["evidence_packet_digest"],
            "verification_complete": True,
            "truth_claim": False,
        }
    )
    packets["LearnOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": learn["learn_state_digest"],
            "source_verify_state_digest": learn["source_verify_state_digest"],
            "verification_digest": verify["verification_evidence_digest"],
            "future_only": True,
            "past_overwrite": False,
        }
    )
    if set(packets) != set(OS_KINDS):
        raise ValueError("native_loop_os_packet_inventory_invalid")
    return build_qi_world_os_interface_receipt(
        world_projection=world,
        qi_process_receipt=qi_receipt,
        os_packets=packets,
    )


def build_native_evidence_loop_receipt(root: Path) -> dict[str, Any]:
    states = _build_native_states(root)
    errors = _native_validation_errors(states)
    if errors:
        raise ValueError("native_loop_source_invalid:" + ";".join(errors))
    lineage_digest = _process_lineage_digest(states)
    world = _build_world_projection(states)
    qi_receipt = _build_qi_receipt(states)
    interface = _build_interface_receipt(
        states, world, qi_receipt, lineage_digest
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": "qi-world-native-evidence-loop",
        "native_states": deepcopy(states),
        "process_lineage_digest": lineage_digest,
        "world_projection_digest": world["world_projection_digest"],
        "qi_world_os_interface_receipt": interface,
        "native_non_authority": deepcopy(NATIVE_NON_AUTHORITY),
        "native_loop_receipt_digest": "",
    }
    receipt["native_loop_receipt_digest"] = native_loop_receipt_digest(receipt)
    validation = validate_native_evidence_loop_receipt(receipt)
    if validation:
        raise ValueError("native_loop_receipt_invalid:" + ";".join(validation))
    return receipt


def validate_native_evidence_loop_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("native_loop_version_invalid")
        if receipt.get("native_loop_receipt_digest") != native_loop_receipt_digest(
            receipt
        ):
            errors.append("native_loop_digest_invalid")
        states = dict(receipt.get("native_states", {}))
        errors.extend(_native_validation_errors(states))
        if set(states) != {"ActOS", "ObserveOS", "VerifyOS", "LearnOS"}:
            errors.append("native_loop_state_inventory_invalid")
            return errors
        act = dict(states["ActOS"])
        observe = dict(states["ObserveOS"])
        verify = dict(states["VerifyOS"])
        learn = dict(states["LearnOS"])

        lineage_ids = {
            act.get("lineage_id"),
            observe.get("lineage_id"),
            verify.get("lineage_id"),
            learn.get("lineage_id"),
        }
        if len(lineage_ids) != 1:
            errors.append("native_loop_lineage_mismatch")
        mission_ids = {
            act.get("mission_contract_digest"),
            observe.get("mission_contract_digest"),
            verify.get("mission_contract_digest"),
            learn.get("mission_contract_digest"),
        }
        if len(mission_ids) != 1:
            errors.append("native_loop_mission_binding_mismatch")

        if observe.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_loop_observe_source_act_mismatch")
        if verify.get("source_observe_state_digest") != observe.get(
            "observe_state_digest"
        ):
            errors.append("native_loop_verify_source_observe_mismatch")
        if verify.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_loop_verify_source_act_mismatch")
        if learn.get("source_verify_state_digest") != verify.get(
            "verify_state_digest"
        ):
            errors.append("native_loop_learn_source_verify_mismatch")
        if learn.get("source_observe_state_digest") != observe.get(
            "observe_state_digest"
        ):
            errors.append("native_loop_learn_source_observe_mismatch")
        if learn.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_loop_learn_source_act_mismatch")

        if act.get("current_phase") != "commit" or act.get("route") != "EFFECT_RECORDED":
            errors.append("native_loop_act_not_committed_effect")
        if act.get("effect_recorded") is not True:
            errors.append("native_loop_act_effect_missing")
        if observe.get("current_phase") != "commit" or observe.get(
            "observation_recorded"
        ) is not True:
            errors.append("native_loop_observe_not_committed")
        if observe.get("verification_required") is not True:
            errors.append("native_loop_observe_verification_debt_missing")
        if verify.get("current_phase") != "commit" or verify.get(
            "verification_recorded"
        ) is not True:
            errors.append("native_loop_verify_not_committed")
        if verify.get("learning_required") is not True:
            errors.append("native_loop_verify_learning_debt_missing")
        if learn.get("current_phase") != "commit" or learn.get(
            "learning_recorded"
        ) is not True:
            errors.append("native_loop_learn_not_committed")
        if learn.get("replan_required") is not True:
            errors.append("native_loop_learn_replan_debt_missing")
        if learn.get("active_now") is not False:
            errors.append("native_loop_learn_present_activation_invalid")
        if learn.get("past_records_unchanged") is not True:
            errors.append("native_loop_learn_past_mutation")

        expected_lineage = _process_lineage_digest(states)
        if receipt.get("process_lineage_digest") != expected_lineage:
            errors.append("native_loop_process_lineage_digest_mismatch")
        interface = dict(receipt.get("qi_world_os_interface_receipt", {}))
        errors.extend(
            f"interface:{error}"
            for error in validate_qi_world_os_interface_receipt(interface)
        )
        if interface.get("process_lineage_digest") != expected_lineage:
            errors.append("native_loop_interface_lineage_mismatch")
        if interface.get("world_projection_digest") != receipt.get(
            "world_projection_digest"
        ):
            errors.append("native_loop_world_projection_mismatch")
        packets = dict(interface.get("os_packets", {}))
        if packets.get("ActOS", {}).get("native_state_digest") != act.get(
            "act_state_digest"
        ):
            errors.append("native_loop_act_packet_mismatch")
        if packets.get("ObserveOS", {}).get("native_state_digest") != observe.get(
            "observe_state_digest"
        ):
            errors.append("native_loop_observe_packet_mismatch")
        if packets.get("VerifyOS", {}).get("native_state_digest") != verify.get(
            "verify_state_digest"
        ):
            errors.append("native_loop_verify_packet_mismatch")
        if packets.get("LearnOS", {}).get("native_state_digest") != learn.get(
            "learn_state_digest"
        ):
            errors.append("native_loop_learn_packet_mismatch")
        if dict(receipt.get("native_non_authority", {})) != NATIVE_NON_AUTHORITY:
            errors.append("native_loop_non_authority_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
