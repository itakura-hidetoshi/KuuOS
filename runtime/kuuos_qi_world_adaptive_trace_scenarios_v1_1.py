from __future__ import annotations

from copy import deepcopy

from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_adaptive_trace_adapter_v1_1 import (
    adapter_receipt_digest,
    adaptive_trace_digest,
    build_adaptive_trace_adapter_receipt,
    validate_adaptive_trace,
    validate_adaptive_trace_adapter_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    interface_receipt_digest,
)


def _retag_trace(trace: dict) -> dict:
    trace["adaptive_trace_digest"] = ""
    trace["adaptive_trace_digest"] = adaptive_trace_digest(trace)
    return trace


def _retag_interface(interface: dict) -> dict:
    interface["qi_world_os_interface_receipt_digest"] = ""
    interface["qi_world_os_interface_receipt_digest"] = interface_receipt_digest(
        interface
    )
    return interface


def _retag_adapter(receipt: dict) -> dict:
    receipt["adapter_receipt_digest"] = ""
    receipt["adapter_receipt_digest"] = adapter_receipt_digest(receipt)
    return receipt


def _require_error(receipt: dict, expected: str) -> None:
    errors = validate_adaptive_trace_adapter_receipt(_retag_adapter(receipt))
    if expected not in errors:
        raise AssertionError({"expected": expected, "errors": errors})


def run_adaptive_trace_adapter_scenarios() -> dict:
    receipt = build_adaptive_trace_adapter_receipt(label="scenario")
    assert validate_adaptive_trace_adapter_receipt(receipt) == []
    trace = receipt["adaptive_trace"]
    interface = receipt["qi_world_os_interface_receipt"]

    assert [event["kind"] for event in trace["events"]] == [
        "DECISION_COMMITTED",
        "PLAN_BOUND",
        "AUTHORITY_BOUND",
        "LEASE_ACTIVATED",
        "SESSION_BOOTSTRAPPED",
        "ACT_AUTHORIZED",
        "EFFECT_RECORDED",
        "OBSERVATION_COMMITTED",
        "VERIFICATION_PASSED",
        "LEARNING_COMMITTED",
    ]
    assert interface["os_packets"]["ActOS"][
        "external_authority_receipt_digest"
    ] == trace["states"][5]["authority_receipt_digest"]
    assert interface["os_packets"]["ObserveOS"]["output_digest"] == trace[
        "events"
    ][7]["payload"]["evidence_digest"]
    assert interface["os_packets"]["VerifyOS"]["output_digest"] == trace[
        "events"
    ][8]["payload"]["verification_digest"]
    assert interface["os_packets"]["LearnOS"]["output_digest"] == trace[
        "events"
    ][9]["payload"]["next_plan_digest"]

    event_reordered = deepcopy(receipt)
    event_reordered["adaptive_trace"]["events"][7], event_reordered[
        "adaptive_trace"
    ]["events"][8] = (
        event_reordered["adaptive_trace"]["events"][8],
        event_reordered["adaptive_trace"]["events"][7],
    )
    _retag_trace(event_reordered["adaptive_trace"])
    event_reordered["adaptive_trace_digest"] = event_reordered[
        "adaptive_trace"
    ]["adaptive_trace_digest"]
    event_reordered["ordered_event_digests"] = [
        event["adaptive_event_digest"]
        for event in event_reordered["adaptive_trace"]["events"]
    ]
    _require_error(
        event_reordered,
        "trace:adaptive_trace_event_order_invalid",
    )

    state_substitution = deepcopy(receipt)
    state_substitution["adaptive_trace"]["states"][7][
        "adaptive_control_state_digest"
    ] = sha("substituted-state")
    _retag_trace(state_substitution["adaptive_trace"])
    state_substitution["adaptive_trace_digest"] = state_substitution[
        "adaptive_trace"
    ]["adaptive_trace_digest"]
    _require_error(
        state_substitution,
        "trace:state_7_replay_digest_mismatch",
    )

    wrong_lineage = deepcopy(receipt)
    wrong_lineage["qi_world_os_interface_receipt"]["os_packets"]["PlanOS"][
        "process_lineage_digest"
    ] = sha("wrong-lineage")
    _retag_interface(wrong_lineage["qi_world_os_interface_receipt"])
    _require_error(
        wrong_lineage,
        "interface:PlanOS_lineage_mismatch",
    )

    missing_authority = deepcopy(receipt)
    missing_authority["qi_world_os_interface_receipt"]["os_packets"]["ActOS"][
        "external_authority_receipt_digest"
    ] = ""
    _retag_interface(missing_authority["qi_world_os_interface_receipt"])
    errors = validate_adaptive_trace_adapter_receipt(
        _retag_adapter(missing_authority)
    )
    if not any("act_external_authority_receipt_digest_required" in error for error in errors):
        raise AssertionError(errors)

    observation_substitution = deepcopy(receipt)
    observation_substitution["qi_world_os_interface_receipt"]["os_packets"][
        "ObserveOS"
    ]["output_digest"] = sha("substituted-observation")
    observation_substitution["qi_world_os_interface_receipt"]["os_packets"][
        "VerifyOS"
    ]["observation_digest"] = sha("substituted-observation")
    _retag_interface(observation_substitution["qi_world_os_interface_receipt"])
    _require_error(
        observation_substitution,
        "adaptive_adapter_observe_binding_invalid",
    )

    past_overwrite = deepcopy(receipt)
    past_overwrite["qi_world_os_interface_receipt"]["os_packets"]["LearnOS"][
        "past_overwrite"
    ] = True
    _retag_interface(past_overwrite["qi_world_os_interface_receipt"])
    _require_error(
        past_overwrite,
        "interface:learn_past_overwrite_invalid",
    )

    trace_errors = validate_adaptive_trace(trace)
    assert trace_errors == []

    return {
        "status": "KUUOS_QI_WORLD_ADAPTIVE_TRACE_ADAPTER_V1_1_OK",
        "cycle_id": receipt["cycle_id"],
        "event_count": len(trace["events"]),
        "state_count": len(trace["states"]),
        "os_packet_count": len(interface["os_packets"]),
        "adaptive_trace_digest": receipt["adaptive_trace_digest"],
        "process_lineage_digest": receipt["process_lineage_digest"],
        "world_projection_digest": receipt["world_projection_digest"],
        "adapter_non_authority": receipt["adapter_non_authority"],
    }
