from __future__ import annotations

from copy import deepcopy

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_os_interface_bridge_v1_0 import (
    build_qi_world_os_interface_receipt,
    validate_qi_world_os_interface_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    OS_INTERFACE_SPECS,
    OS_KINDS,
    interface_receipt_digest,
)


def _qi_raw(cycle_id: str) -> dict:
    return {
        "cycle_id": cycle_id,
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "process_history": [
            {
                "process_action": "belief_context_read",
                "transition_visible": True,
                "memory_link_visible": True,
            },
            {
                "process_action": "authorized_intervention",
                "transition_visible": True,
                "nonmarkov_link_visible": True,
            },
            {
                "process_observation": "post_intervention_evidence",
                "memory_link_visible": True,
            },
        ],
    }


def _world_projection(cycle_id: str) -> dict:
    payload = {
        "cycle_id": cycle_id,
        "projection_kind": "candidate_world_projection",
        "projection_read_only": True,
        "candidate_only": True,
        "nonfinal_marker": True,
        "exact_world_identified": False,
        "runtime_updates_world": False,
        "multi_world_noncollapse": True,
        "two_truths_gap": True,
    }
    payload["world_projection_digest"] = sha(payload)
    return payload


def _packet(
    *,
    name: str,
    cycle_id: str,
    lineage: str,
    world_digest: str,
    input_label: str,
    output_label: str,
) -> dict:
    spec = OS_INTERFACE_SPECS[name]
    return {
        "os_kind": name,
        "cycle_id": cycle_id,
        "process_lineage_digest": lineage,
        "world_projection_digest": world_digest,
        "world_relation": spec["world_relation"],
        "qi_relation": spec["qi_relation"],
        "output_kind": spec["output_kind"],
        "input_digest": sha(input_label),
        "output_digest": sha(output_label),
        "candidate_only": True,
        "nonfinal_marker": True,
    }


def _os_packets(cycle_id: str, lineage: str, world_digest: str) -> dict[str, dict]:
    packets = {
        name: _packet(
            name=name,
            cycle_id=cycle_id,
            lineage=lineage,
            world_digest=world_digest,
            input_label=f"{cycle_id}:{name}:input",
            output_label=f"{cycle_id}:{name}:output",
        )
        for name in OS_KINDS
    }
    governance_digest = packets["Governance"]["output_digest"]
    packets["Governance"].update(
        {
            "cross_cutting": True,
            "single_stage": False,
            "act_admitted": True,
        }
    )
    packets["ActOS"].update(
        {
            "governance_decision_digest": governance_digest,
            "external_authority_receipt_digest": sha(
                f"{cycle_id}:external-authority"
            ),
            "actual_intervention_appended": True,
        }
    )
    packets["ObserveOS"].update(
        {
            "observation_only": True,
            "verification_complete": False,
        }
    )
    packets["VerifyOS"].update(
        {
            "observation_digest": packets["ObserveOS"]["output_digest"],
            "verification_complete": True,
            "truth_claim": False,
        }
    )
    packets["LearnOS"].update(
        {
            "verification_digest": packets["VerifyOS"]["output_digest"],
            "future_only": True,
            "past_overwrite": False,
        }
    )
    return packets


def _retag(receipt: dict) -> dict:
    receipt["qi_world_os_interface_receipt_digest"] = ""
    receipt["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(
        receipt
    )
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_qi_world_os_interface_receipt(_retag(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_qi_world_os_interface_bridge() -> dict:
    cycle_id = "qi-world-os-cycle-1"
    world = _world_projection(cycle_id)
    qi = evaluate_qi_process_tensor(_qi_raw(cycle_id))
    assert qi.process_tensor_visible is True
    assert qi.nonmarkov_memory_visible is True
    lineage = sha(
        {
            "cycle_id": cycle_id,
            "world_projection_digest": world["world_projection_digest"],
            "process_history_length": qi.process_history_length,
        }
    )
    packets = _os_packets(
        cycle_id,
        lineage,
        world["world_projection_digest"],
    )
    receipt = build_qi_world_os_interface_receipt(
        world_projection=world,
        qi_process_receipt=qi,
        os_packets=packets,
    )
    assert validate_qi_world_os_interface_receipt(receipt) == []

    wrong_lineage = deepcopy(receipt)
    wrong_lineage["os_packets"]["DecisionOS"][
        "process_lineage_digest"
    ] = sha("wrong-lineage")
    _require_error(wrong_lineage, "DecisionOS_lineage_mismatch")

    mutable_world = deepcopy(receipt)
    mutable_world["world_projection"]["runtime_updates_world"] = True
    _require_error(mutable_world, "world_projection_runtime_updates_world_invalid")

    ungoverned_act = deepcopy(receipt)
    ungoverned_act["os_packets"]["ActOS"][
        "governance_decision_digest"
    ] = sha("substituted-governance")
    _require_error(ungoverned_act, "act_governance_binding_invalid")

    observation_claims_verification = deepcopy(receipt)
    observation_claims_verification["os_packets"]["ObserveOS"][
        "verification_complete"
    ] = True
    _require_error(
        observation_claims_verification,
        "observe_verification_boundary_invalid",
    )

    past_rewrite = deepcopy(receipt)
    past_rewrite["os_packets"]["LearnOS"]["past_overwrite"] = True
    _require_error(past_rewrite, "learn_past_overwrite_invalid")

    qi_without_nonmarkov = deepcopy(receipt)
    qi_without_nonmarkov["qi_process_receipt"][
        "nonmarkov_memory_visible"
    ] = False
    _require_error(qi_without_nonmarkov, "qi_nonmarkov_memory_missing")

    return receipt
