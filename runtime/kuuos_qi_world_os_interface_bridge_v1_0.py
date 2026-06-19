from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import QiProcessTensorReceipt
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    CROSS_OS_RELATIONS,
    NON_AUTHORITY,
    OS_INTERFACE_SPECS,
    OS_KINDS,
    RECEIPT_VERSION,
    WORLD_BOUNDARY,
    copy_non_authority,
    copy_world_boundary,
    interface_receipt_digest,
    require_string,
)


def _qi_receipt_dict(value: QiProcessTensorReceipt | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(value, QiProcessTensorReceipt):
        return value.to_dict()
    return deepcopy(dict(value))


def build_qi_world_os_interface_receipt(
    *,
    world_projection: Mapping[str, Any],
    qi_process_receipt: QiProcessTensorReceipt | Mapping[str, Any],
    os_packets: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    world = deepcopy(dict(world_projection))
    qi = _qi_receipt_dict(qi_process_receipt)
    packets = {name: deepcopy(dict(packet)) for name, packet in os_packets.items()}
    if set(packets) != set(OS_KINDS):
        raise ValueError("qi_world_os_packet_inventory_incomplete")
    cycle_id = require_string(qi.get("cycle_id"), "cycle_id")
    lineage = require_string(
        packets["BeliefOS"].get("process_lineage_digest"),
        "process_lineage_digest",
    )
    world_digest = require_string(
        world.get("world_projection_digest"), "world_projection_digest"
    )
    governance_digest = require_string(
        packets["Governance"].get("output_digest"),
        "governance_output_digest",
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": cycle_id,
        "process_lineage_digest": lineage,
        "world_projection_digest": world_digest,
        "world_projection": world,
        "qi_process_receipt": qi,
        "os_packets": packets,
        "os_interface_specs": deepcopy(OS_INTERFACE_SPECS),
        "cross_os_relations": [
            {"source": source, "relation": relation, "target": target}
            for source, relation, target in CROSS_OS_RELATIONS
        ],
        "governance_decision_digest": governance_digest,
        "world_boundary": copy_world_boundary(),
        "non_authority": copy_non_authority(),
        "same_process_lineage": True,
        "world_projection_read_only": True,
        "qi_process_is_temporal_substrate": True,
        "governance_is_cross_cutting": True,
        "governance_is_single_stage": False,
        "exact_world_updated": False,
        "qi_world_os_interface_receipt_digest": "",
    }
    receipt["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(
        receipt
    )
    errors = validate_qi_world_os_interface_receipt(receipt)
    if errors:
        raise ValueError("qi_world_os_interface_invalid:" + ";".join(errors))
    return receipt


def validate_qi_world_os_interface_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("interface_version_invalid")
        if receipt.get("qi_world_os_interface_receipt_digest") != interface_receipt_digest(
            receipt
        ):
            errors.append("interface_digest_invalid")
        cycle_id = require_string(receipt.get("cycle_id"), "cycle_id")
        lineage = require_string(
            receipt.get("process_lineage_digest"), "process_lineage_digest"
        )
        world_digest = require_string(
            receipt.get("world_projection_digest"),
            "world_projection_digest",
        )
        world = dict(receipt.get("world_projection", {}))
        if world.get("world_projection_digest") != world_digest:
            errors.append("world_projection_digest_mismatch")
        for key, expected in WORLD_BOUNDARY.items():
            if world.get(key) != expected:
                errors.append(f"world_projection_{key}_invalid")
        if dict(receipt.get("world_boundary", {})) != WORLD_BOUNDARY:
            errors.append("world_boundary_invalid")

        qi = dict(receipt.get("qi_process_receipt", {}))
        if qi.get("cycle_id") != cycle_id:
            errors.append("qi_cycle_mismatch")
        if qi.get("process_tensor_visible") is not True:
            errors.append("qi_process_tensor_not_visible")
        if qi.get("transition_continuity_visible") is not True:
            errors.append("qi_transition_continuity_missing")
        if qi.get("memory_continuity_visible") is not True:
            errors.append("qi_memory_continuity_missing")
        if qi.get("nonmarkov_memory_visible") is not True:
            errors.append("qi_nonmarkov_memory_missing")
        for key in (
            "grants_execution_authority",
            "grants_truth_authority",
            "grants_final_commitment_authority",
            "grants_memory_overwrite_authority",
        ):
            if qi.get(key) is not False:
                errors.append(f"qi_{key}_invalid")

        packets = dict(receipt.get("os_packets", {}))
        if set(packets) != set(OS_KINDS):
            errors.append("os_packet_inventory_invalid")
        specs = dict(receipt.get("os_interface_specs", {}))
        if specs != OS_INTERFACE_SPECS:
            errors.append("os_interface_specs_invalid")
        for name in OS_KINDS:
            packet = dict(packets.get(name, {}))
            spec = OS_INTERFACE_SPECS[name]
            if packet.get("os_kind") != name:
                errors.append(f"{name}_kind_invalid")
            if packet.get("cycle_id") != cycle_id:
                errors.append(f"{name}_cycle_mismatch")
            if packet.get("process_lineage_digest") != lineage:
                errors.append(f"{name}_lineage_mismatch")
            if packet.get("world_projection_digest") != world_digest:
                errors.append(f"{name}_world_projection_mismatch")
            if packet.get("world_relation") != spec["world_relation"]:
                errors.append(f"{name}_world_relation_invalid")
            if packet.get("qi_relation") != spec["qi_relation"]:
                errors.append(f"{name}_qi_relation_invalid")
            if packet.get("output_kind") != spec["output_kind"]:
                errors.append(f"{name}_output_kind_invalid")
            require_string(packet.get("input_digest"), f"{name}_input_digest")
            require_string(packet.get("output_digest"), f"{name}_output_digest")
            if packet.get("candidate_only") is not True:
                errors.append(f"{name}_candidate_boundary_invalid")
            if packet.get("nonfinal_marker") is not True:
                errors.append(f"{name}_nonfinal_boundary_invalid")

        governance = dict(packets.get("Governance", {}))
        if governance.get("cross_cutting") is not True:
            errors.append("governance_cross_cutting_missing")
        if governance.get("single_stage") is not False:
            errors.append("governance_single_stage_invalid")
        if governance.get("output_digest") != receipt.get(
            "governance_decision_digest"
        ):
            errors.append("governance_decision_digest_mismatch")
        if governance.get("act_admitted") is not True:
            errors.append("governance_act_not_admitted")

        act = dict(packets.get("ActOS", {}))
        if act.get("governance_decision_digest") != governance.get(
            "output_digest"
        ):
            errors.append("act_governance_binding_invalid")
        require_string(
            act.get("external_authority_receipt_digest"),
            "act_external_authority_receipt_digest",
        )
        if act.get("actual_intervention_appended") is not True:
            errors.append("act_intervention_append_missing")

        observe = dict(packets.get("ObserveOS", {}))
        if observe.get("observation_only") is not True:
            errors.append("observe_observation_only_invalid")
        if observe.get("verification_complete") is not False:
            errors.append("observe_verification_boundary_invalid")

        verify = dict(packets.get("VerifyOS", {}))
        if verify.get("observation_digest") != observe.get("output_digest"):
            errors.append("verify_observation_binding_invalid")
        if verify.get("verification_complete") is not True:
            errors.append("verify_completion_missing")
        if verify.get("truth_claim") is not False:
            errors.append("verify_truth_claim_invalid")

        learn = dict(packets.get("LearnOS", {}))
        if learn.get("verification_digest") != verify.get("output_digest"):
            errors.append("learn_verification_binding_invalid")
        if learn.get("future_only") is not True:
            errors.append("learn_future_only_invalid")
        if learn.get("past_overwrite") is not False:
            errors.append("learn_past_overwrite_invalid")

        relations = list(receipt.get("cross_os_relations", []))
        relation_set = {
            (item.get("source"), item.get("relation"), item.get("target"))
            for item in relations
            if isinstance(item, dict)
        }
        if relation_set != set(CROSS_OS_RELATIONS):
            errors.append("cross_os_relations_invalid")

        if receipt.get("same_process_lineage") is not True:
            errors.append("same_process_lineage_invalid")
        if receipt.get("world_projection_read_only") is not True:
            errors.append("world_projection_read_only_invalid")
        if receipt.get("qi_process_is_temporal_substrate") is not True:
            errors.append("qi_temporal_substrate_invalid")
        if receipt.get("governance_is_cross_cutting") is not True:
            errors.append("governance_cross_cutting_invalid")
        if receipt.get("governance_is_single_stage") is not False:
            errors.append("governance_stage_boundary_invalid")
        if receipt.get("exact_world_updated") is not False:
            errors.append("exact_world_update_invalid")
        if dict(receipt.get("non_authority", {})) != NON_AUTHORITY:
            errors.append("non_authority_invalid")
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
