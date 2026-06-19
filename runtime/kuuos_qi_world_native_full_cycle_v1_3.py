from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_act_os_fixture_v0_1 import host_inputs, prepared_project_state
from runtime.kuuos_act_os_kernel_v0_1 import validate_act_state
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_learn_os_fixture_v0_1 import prepared_gated_state
from runtime.kuuos_learn_os_kernel_v0_1 import validate_learn_state
from runtime.kuuos_observe_os_fixture_v0_1 import prepared_assessed_state
from runtime.kuuos_observe_os_kernel_v0_1 import validate_observe_state
from runtime.kuuos_qi_world_native_upstream_cycle_v1_3 import (
    LINEAGE_ID,
    MISSION_CONTRACT_DIGEST,
    build_native_upstream_cycle,
    validate_native_upstream_cycle,
)
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
from runtime.v01_act_os_authority_bound_invocation import _finish as finish_act
from runtime.v01_learn_os_future_only_evidence_learning import _finish as finish_learn
from runtime.v01_observe_os_effect_grounded_observation import _finish as finish_observe
from runtime.v01_verify_os_evidence_bound_verification import _finish as finish_verify

VERSION = "kuuos_qi_world_native_full_cycle_v1_3"
RECEIPT_VERSION = "kuuos_qi_world_native_full_cycle_receipt_v1_3"
CYCLE_ID = "qi-world-native-full-cycle-v13"

FULL_CYCLE_NON_AUTHORITY = {
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


def full_cycle_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "full_cycle_receipt_digest")


def _build_downstream_states(
    root: Path,
    plan_state: Mapping[str, Any],
    plan_activation: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    job_id = "native-full-cycle-job-v13"
    policy, bundle, license_packet, projection = host_inputs(job_id=job_id)
    act_store, act_pending = prepared_project_state(
        root=root / "act",
        act_id="native-full-cycle-act-v13",
        plan_state=plan_state,
        plan_activation=plan_activation,
        job_id=job_id,
        host_license=license_packet,
        projection=projection,
    )
    act_state, _ = finish_act(
        store=act_store,
        state=act_pending,
        bundle=bundle,
        policy=policy,
        invoke_ms=90_004,
    )

    observe_store, observe_pending = prepared_assessed_state(
        root=root / "observe",
        observe_id="native-full-cycle-observe-v13",
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
        verify_id="native-full-cycle-verify-v13",
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
        learn_id="native-full-cycle-learn-v13",
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


def _ordered_native_digests(artifacts: Mapping[str, Mapping[str, Any]]) -> list[str]:
    return [
        str(artifacts["BeliefOS"]["belief_gerbe_receipt_digest"]),
        str(artifacts["DecisionOS"]["decision_state_digest"]),
        str(artifacts["DecisionOSPlural"]["plural_state_digest"]),
        str(artifacts["DecisionOSWa"]["wa_state_digest"]),
        str(artifacts["PlanOS"]["plan_state_digest"]),
        str(artifacts["ActOS"]["act_state_digest"]),
        str(artifacts["ObserveOS"]["observe_state_digest"]),
        str(artifacts["VerifyOS"]["verify_state_digest"]),
        str(artifacts["LearnOS"]["learn_state_digest"]),
    ]


def _process_lineage_digest(artifacts: Mapping[str, Mapping[str, Any]]) -> str:
    return sha(
        {
            "cycle_id": CYCLE_ID,
            "lineage_id": LINEAGE_ID,
            "mission_contract_digest": MISSION_CONTRACT_DIGEST,
            "ordered_native_digests": _ordered_native_digests(artifacts),
        }
    )


def _world_projection(artifacts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = {
        "cycle_id": CYCLE_ID,
        "projection_kind": "native_full_os_cycle_projection",
        "lineage_id": LINEAGE_ID,
        "mission_contract_digest": MISSION_CONTRACT_DIGEST,
        "belief_receipt_digest": artifacts["BeliefOS"][
            "belief_gerbe_receipt_digest"
        ],
        "decision_state_digest": artifacts["DecisionOS"]["decision_state_digest"],
        "plural_state_digest": artifacts["DecisionOSPlural"]["plural_state_digest"],
        "wa_state_digest": artifacts["DecisionOSWa"]["wa_state_digest"],
        "plan_state_digest": artifacts["PlanOS"]["plan_state_digest"],
        "act_state_digest": artifacts["ActOS"]["act_state_digest"],
        "observe_state_digest": artifacts["ObserveOS"]["observe_state_digest"],
        "evidence_packet_digest": artifacts["ObserveOS"]["evidence_packet_digest"],
        "verify_state_digest": artifacts["VerifyOS"]["verify_state_digest"],
        "verification_evidence_digest": artifacts["VerifyOS"][
            "verification_evidence_digest"
        ],
        "learn_state_digest": artifacts["LearnOS"]["learn_state_digest"],
        "learning_delta_digest": artifacts["LearnOS"]["learning_delta_digest"],
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


def _qi_receipt(artifacts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    names = (
        "BeliefOS",
        "DecisionOS",
        "DecisionOSPlural",
        "DecisionOSWa",
        "PlanOS",
        "ActOS",
        "ObserveOS",
        "VerifyOS",
        "LearnOS",
    )
    digests = _ordered_native_digests(artifacts)
    observations = {"ObserveOS", "VerifyOS"}
    history: list[dict[str, Any]] = []
    for index, (name, digest) in enumerate(zip(names, digests, strict=True)):
        item: dict[str, Any] = {
            "native_kind": name,
            "native_state_digest": digest,
            "transition_visible": True,
            "memory_link_visible": index > 0,
            "nonmarkov_link_visible": index >= 2,
        }
        if name in observations:
            item["process_observation"] = name
        else:
            item["process_action"] = name
        history.append(item)
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
    receipt = evaluate_qi_process_tensor(raw).to_dict()
    if receipt.get("process_tensor_visible") is not True:
        raise ValueError("native_full_cycle_qi_process_not_visible")
    if receipt.get("nonmarkov_memory_visible") is not True:
        raise ValueError("native_full_cycle_nonmarkov_memory_not_visible")
    return receipt


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
        "cycle_id": CYCLE_ID,
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


def _interface_receipt(
    artifacts: Mapping[str, Mapping[str, Any]],
    world: Mapping[str, Any],
    qi_receipt: Mapping[str, Any],
    lineage_digest: str,
) -> dict[str, Any]:
    belief = artifacts["BeliefOS"]
    decision = artifacts["DecisionOS"]
    plural = artifacts["DecisionOSPlural"]
    wa = artifacts["DecisionOSWa"]
    plan = artifacts["PlanOS"]
    act = artifacts["ActOS"]
    observe = artifacts["ObserveOS"]
    verify = artifacts["VerifyOS"]
    learn = artifacts["LearnOS"]
    world_digest = str(world["world_projection_digest"])

    packets = {
        "BeliefOS": _base_packet(
            name="BeliefOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=world_digest,
            output_digest=belief["belief_gerbe_receipt_digest"],
        ),
        "DecisionOS": _base_packet(
            name="DecisionOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=belief["belief_gerbe_receipt_digest"],
            output_digest=wa["wa_state_digest"],
        ),
        "PlanOS": _base_packet(
            name="PlanOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=wa["wa_state_digest"],
            output_digest=plan["plan_state_digest"],
        ),
        "Governance": _base_packet(
            name="Governance",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=plan["plan_state_digest"],
            output_digest=act["step_authorization_digest"],
        ),
        "ActOS": _base_packet(
            name="ActOS",
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=act["step_authorization_digest"],
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
            "native_artifact": True,
            "native_receipt_digest": belief["belief_gerbe_receipt_digest"],
            "route": belief["route"],
        }
    )
    packets["DecisionOS"].update(
        {
            "native_artifact": True,
            "native_decision_state_digest": decision["decision_state_digest"],
            "native_plural_state_digest": plural["plural_state_digest"],
            "native_wa_state_digest": wa["wa_state_digest"],
            "source_belief_receipt_digest": decision[
                "source_belief_receipt_digest"
            ],
        }
    )
    packets["PlanOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": plan["plan_state_digest"],
            "source_wa_state_digest": plan["source_wa_state_digest"],
        }
    )
    packets["Governance"].update(
        {
            "cross_cutting": True,
            "single_stage": False,
            "act_admitted": True,
            "step_authorization_digest": act["step_authorization_digest"],
            "host_license_digest": act["host_license_digest"],
        }
    )
    packets["ActOS"].update(
        {
            "native_artifact": True,
            "native_state_digest": act["act_state_digest"],
            "governance_decision_digest": act["step_authorization_digest"],
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
            "source_observe_state_digest": verify[
                "source_observe_state_digest"
            ],
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
        raise ValueError("native_full_cycle_os_packet_inventory_invalid")
    return build_qi_world_os_interface_receipt(
        world_projection=world,
        qi_process_receipt=qi_receipt,
        os_packets=packets,
    )


def build_native_full_cycle_receipt(root: Path) -> dict[str, Any]:
    upstream = build_native_upstream_cycle(root / "upstream")
    downstream = _build_downstream_states(
        root / "downstream",
        upstream["PlanOS"],
        upstream["PlanActivation"],
    )
    artifacts = {
        "BeliefOS": upstream["BeliefOS"],
        "DecisionOS": upstream["DecisionOS"],
        "DecisionOSPlural": upstream["DecisionOSPlural"],
        "DecisionOSWa": upstream["DecisionOSWa"],
        "PlanOS": upstream["PlanOS"],
        **downstream,
    }
    lineage_digest = _process_lineage_digest(artifacts)
    world = _world_projection(artifacts)
    qi_receipt = _qi_receipt(artifacts)
    interface = _interface_receipt(
        artifacts,
        world,
        qi_receipt,
        lineage_digest,
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": CYCLE_ID,
        "lineage_id": LINEAGE_ID,
        "mission_contract_digest": MISSION_CONTRACT_DIGEST,
        "native_artifacts": deepcopy(artifacts),
        "process_lineage_digest": lineage_digest,
        "world_projection_digest": world["world_projection_digest"],
        "qi_world_os_interface_receipt": interface,
        "full_cycle_non_authority": deepcopy(FULL_CYCLE_NON_AUTHORITY),
        "full_cycle_receipt_digest": "",
    }
    receipt["full_cycle_receipt_digest"] = full_cycle_receipt_digest(receipt)
    errors = validate_native_full_cycle_receipt(receipt)
    if errors:
        raise ValueError("native_full_cycle_invalid:" + ";".join(errors))
    return receipt


def validate_native_full_cycle_receipt(receipt: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("native_full_cycle_version_invalid")
        if receipt.get("full_cycle_receipt_digest") != full_cycle_receipt_digest(
            receipt
        ):
            errors.append("native_full_cycle_digest_invalid")
        if receipt.get("lineage_id") != LINEAGE_ID:
            errors.append("native_full_cycle_lineage_id_invalid")
        if receipt.get("mission_contract_digest") != MISSION_CONTRACT_DIGEST:
            errors.append("native_full_cycle_mission_invalid")
        artifacts = dict(receipt.get("native_artifacts", {}))
        expected = {
            "BeliefOS",
            "DecisionOS",
            "DecisionOSPlural",
            "DecisionOSWa",
            "PlanOS",
            "ActOS",
            "ObserveOS",
            "VerifyOS",
            "LearnOS",
        }
        if set(artifacts) != expected:
            errors.append("native_full_cycle_artifact_inventory_invalid")
            return errors
        upstream = {
            "version": "kuuos_qi_world_native_upstream_cycle_v1_3",
            "lineage_id": LINEAGE_ID,
            "mission_contract_digest": MISSION_CONTRACT_DIGEST,
            "BeliefOS": artifacts["BeliefOS"],
            "DecisionOS": artifacts["DecisionOS"],
            "DecisionOSPlural": artifacts["DecisionOSPlural"],
            "DecisionOSWa": artifacts["DecisionOSWa"],
            "PlanOS": artifacts["PlanOS"],
        }
        errors.extend(
            f"upstream:{error}" for error in validate_native_upstream_cycle(upstream)
        )
        act = dict(artifacts["ActOS"])
        observe = dict(artifacts["ObserveOS"])
        verify = dict(artifacts["VerifyOS"])
        learn = dict(artifacts["LearnOS"])
        errors.extend(f"ActOS:{error}" for error in validate_act_state(act))
        errors.extend(f"ObserveOS:{error}" for error in validate_observe_state(observe))
        errors.extend(f"VerifyOS:{error}" for error in validate_verify_state(verify))
        errors.extend(f"LearnOS:{error}" for error in validate_learn_state(learn))

        for name in (
            "DecisionOS",
            "DecisionOSPlural",
            "DecisionOSWa",
            "PlanOS",
            "ActOS",
            "ObserveOS",
            "VerifyOS",
            "LearnOS",
        ):
            state = dict(artifacts[name])
            if state.get("lineage_id") != LINEAGE_ID:
                errors.append(f"native_full_cycle_{name}_lineage_mismatch")
            if state.get("mission_contract_digest") != MISSION_CONTRACT_DIGEST:
                errors.append(f"native_full_cycle_{name}_mission_mismatch")

        if act.get("source_plan_state_digest") != artifacts["PlanOS"].get(
            "plan_state_digest"
        ):
            errors.append("native_full_cycle_act_source_plan_mismatch")
        if observe.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_full_cycle_observe_source_act_mismatch")
        if verify.get("source_observe_state_digest") != observe.get(
            "observe_state_digest"
        ):
            errors.append("native_full_cycle_verify_source_observe_mismatch")
        if verify.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_full_cycle_verify_source_act_mismatch")
        if learn.get("source_verify_state_digest") != verify.get(
            "verify_state_digest"
        ):
            errors.append("native_full_cycle_learn_source_verify_mismatch")
        if learn.get("source_observe_state_digest") != observe.get(
            "observe_state_digest"
        ):
            errors.append("native_full_cycle_learn_source_observe_mismatch")
        if learn.get("source_act_state_digest") != act.get("act_state_digest"):
            errors.append("native_full_cycle_learn_source_act_mismatch")
        if learn.get("past_records_unchanged") is not True:
            errors.append("native_full_cycle_past_mutation")
        if learn.get("active_now") is not False:
            errors.append("native_full_cycle_learning_active_now")

        expected_lineage = _process_lineage_digest(artifacts)
        if receipt.get("process_lineage_digest") != expected_lineage:
            errors.append("native_full_cycle_process_lineage_digest_mismatch")
        interface = dict(receipt.get("qi_world_os_interface_receipt", {}))
        errors.extend(
            f"interface:{error}"
            for error in validate_qi_world_os_interface_receipt(interface)
        )
        if interface.get("process_lineage_digest") != expected_lineage:
            errors.append("native_full_cycle_interface_lineage_mismatch")
        if interface.get("world_projection_digest") != receipt.get(
            "world_projection_digest"
        ):
            errors.append("native_full_cycle_world_projection_mismatch")
        packets = dict(interface.get("os_packets", {}))
        if packets.get("BeliefOS", {}).get("output_digest") != artifacts[
            "BeliefOS"
        ].get("belief_gerbe_receipt_digest"):
            errors.append("native_full_cycle_belief_packet_mismatch")
        if packets.get("DecisionOS", {}).get("output_digest") != artifacts[
            "DecisionOSWa"
        ].get("wa_state_digest"):
            errors.append("native_full_cycle_decision_packet_mismatch")
        if packets.get("PlanOS", {}).get("output_digest") != artifacts[
            "PlanOS"
        ].get("plan_state_digest"):
            errors.append("native_full_cycle_plan_packet_mismatch")
        if packets.get("ActOS", {}).get("output_digest") != act.get(
            "act_state_digest"
        ):
            errors.append("native_full_cycle_act_packet_mismatch")
        if packets.get("ObserveOS", {}).get("output_digest") != observe.get(
            "evidence_packet_digest"
        ):
            errors.append("native_full_cycle_observe_packet_mismatch")
        if packets.get("VerifyOS", {}).get("output_digest") != verify.get(
            "verification_evidence_digest"
        ):
            errors.append("native_full_cycle_verify_packet_mismatch")
        if packets.get("LearnOS", {}).get("output_digest") != learn.get(
            "learning_delta_digest"
        ):
            errors.append("native_full_cycle_learn_packet_mismatch")
        if dict(receipt.get("full_cycle_non_authority", {})) != FULL_CYCLE_NON_AUTHORITY:
            errors.append("native_full_cycle_non_authority_invalid")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
