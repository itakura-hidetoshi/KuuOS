from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from runtime.qi_process_tensor_v0_1 import evaluate_qi_process_tensor
from runtime.kuuos_adaptive_agent_reference_types_v1_0 import (
    event_digest,
    state_digest,
)
from runtime.kuuos_adaptive_agent_runtime_megamodel_v1_0 import (
    MODEL_KINDS,
    build_runtime_megamodel,
    validate_runtime_megamodel,
)
from runtime.kuuos_adaptive_agent_transition_kernel_v1_0 import (
    apply_adaptive_event,
    build_adaptive_event,
    build_initial_adaptive_state,
    validate_adaptive_event,
    validate_adaptive_state,
)
from runtime.kuuos_belief_os_types_v0_1 import sha
from runtime.kuuos_qi_world_os_interface_bridge_v1_0 import (
    build_qi_world_os_interface_receipt,
    validate_qi_world_os_interface_receipt,
)
from runtime.kuuos_qi_world_os_interface_types_v1_0 import (
    OS_INTERFACE_SPECS,
    OS_KINDS,
)

VERSION = "kuuos_qi_world_adaptive_trace_adapter_v1_1"
RECEIPT_VERSION = "kuuos_qi_world_adaptive_trace_adapter_receipt_v1_1"

TRACE_EVENT_KINDS = (
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
)

TRACE_STAGE_SEQUENCE = (
    "BELIEF",
    "DECISION",
    "PLAN",
    "PLAN",
    "PLAN",
    "PLAN",
    "ACT",
    "OBSERVE",
    "VERIFY",
    "LEARN",
    "PLAN",
)

ADAPTER_NON_AUTHORITY = {
    "adapter_grants_execution": False,
    "adapter_grants_truth": False,
    "adapter_issues_authority": False,
    "adapter_changes_governance_decision": False,
    "adapter_updates_exact_world": False,
    "adapter_overwrites_history": False,
}


def _digest_without(value: Mapping[str, Any], field: str) -> str:
    packet = deepcopy(dict(value))
    packet.pop(field, None)
    return sha(packet)


def adaptive_trace_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "adaptive_trace_digest")


def adapter_receipt_digest(value: Mapping[str, Any]) -> str:
    return _digest_without(value, "adapter_receipt_digest")


def _emit(
    state: Mapping[str, Any],
    kind: str,
    *,
    payload: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event = build_adaptive_event(
        kind=kind,
        event_index=int(state["sequence"]) + 1,
        payload=payload,
    )
    next_state = apply_adaptive_event(state, event)
    return event, next_state


def build_nominal_adaptive_trace(*, label: str = "qi-world-concrete") -> dict[str, Any]:
    cycle_id = f"adaptive-cycle-{label}"
    megamodel = build_runtime_megamodel(
        model_digests={kind: sha({"model": kind, "label": label}) for kind in MODEL_KINDS}
    )
    if validate_runtime_megamodel(megamodel):
        raise ValueError("adaptive_trace_megamodel_invalid")

    initial = build_initial_adaptive_state(
        owner_id="owner-alpha",
        lineage_id=f"lineage-{label}-0",
        runtime_megamodel_digest=megamodel["runtime_megamodel_digest"],
    )
    states: list[dict[str, Any]] = [initial]
    events: list[dict[str, Any]] = []

    payloads: tuple[Mapping[str, Any] | None, ...] = (
        None,
        {"plan_digest": sha(f"{label}:plan")},
        {"authority_receipt_digest": sha(f"{label}:authority")},
        None,
        {"session_digest": sha(f"{label}:session")},
        None,
        None,
        {"evidence_digest": sha(f"{label}:evidence")},
        {"verification_digest": sha(f"{label}:verification")},
        {"next_plan_digest": sha(f"{label}:next-plan")},
    )

    current = initial
    for kind, payload in zip(TRACE_EVENT_KINDS, payloads, strict=True):
        event, current = _emit(current, kind, payload=payload)
        events.append(event)
        states.append(current)

    trace = {
        "version": VERSION,
        "cycle_id": cycle_id,
        "label": label,
        "runtime_megamodel": megamodel,
        "initial_state": deepcopy(initial),
        "events": deepcopy(events),
        "states": deepcopy(states),
        "adaptive_trace_digest": "",
    }
    trace["adaptive_trace_digest"] = adaptive_trace_digest(trace)
    errors = validate_adaptive_trace(trace)
    if errors:
        raise ValueError("adaptive_trace_invalid:" + ";".join(errors))
    return trace


def validate_adaptive_trace(trace: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        if trace.get("version") != VERSION:
            errors.append("adaptive_trace_version_invalid")
        if trace.get("adaptive_trace_digest") != adaptive_trace_digest(trace):
            errors.append("adaptive_trace_digest_invalid")
        megamodel = dict(trace.get("runtime_megamodel", {}))
        errors.extend(
            f"megamodel:{error}" for error in validate_runtime_megamodel(megamodel)
        )
        events = list(trace.get("events", []))
        states = list(trace.get("states", []))
        if len(events) != len(TRACE_EVENT_KINDS):
            errors.append("adaptive_trace_event_count_invalid")
        if len(states) != len(events) + 1:
            errors.append("adaptive_trace_state_count_invalid")
        if tuple(event.get("kind") for event in events) != TRACE_EVENT_KINDS:
            errors.append("adaptive_trace_event_order_invalid")
        if tuple(state.get("task_stage") for state in states) != TRACE_STAGE_SEQUENCE:
            errors.append("adaptive_trace_stage_sequence_invalid")
        if states and dict(trace.get("initial_state", {})) != dict(states[0]):
            errors.append("adaptive_trace_initial_state_mismatch")

        if not states:
            return errors + ["adaptive_trace_states_missing"]
        replay = dict(states[0])
        errors.extend(
            f"initial:{error}" for error in validate_adaptive_state(replay)
        )
        lineage_id = replay.get("lineage_id")
        for index, event in enumerate(events):
            errors.extend(
                f"event_{index}:{error}"
                for error in validate_adaptive_event(event)
            )
            if event.get("adaptive_event_digest") != event_digest(event):
                errors.append(f"event_{index}_digest_invalid")
            try:
                replay = apply_adaptive_event(replay, event)
            except ValueError as exc:
                errors.append(f"event_{index}_replay_failed:{exc}")
                break
            expected = dict(states[index + 1])
            if replay.get("adaptive_control_state_digest") != expected.get(
                "adaptive_control_state_digest"
            ):
                errors.append(f"state_{index + 1}_replay_digest_mismatch")
            if expected.get("adaptive_control_state_digest") != state_digest(expected):
                errors.append(f"state_{index + 1}_digest_invalid")
            if expected.get("lineage_id") != lineage_id:
                errors.append(f"state_{index + 1}_lineage_changed")
        if states[-1].get("task_stage") != "PLAN":
            errors.append("adaptive_trace_final_stage_invalid")
        if states[6].get("execution_allowed") is not True:
            errors.append("adaptive_trace_act_not_authorized")
        if states[7].get("execution_allowed") is not False:
            errors.append("adaptive_trace_effect_not_closed")
        if states[8].get("observation_committed") is not True:
            errors.append("adaptive_trace_observation_missing")
        if states[9].get("verification_committed") is not True:
            errors.append("adaptive_trace_verification_missing")
    except (IndexError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def _build_world_projection(trace: Mapping[str, Any]) -> dict[str, Any]:
    states = list(trace["states"])
    observation_event = dict(trace["events"][7])
    payload = {
        "cycle_id": trace["cycle_id"],
        "projection_kind": "adaptive_trace_world_projection_bundle",
        "source_state_digest": states[0]["adaptive_control_state_digest"],
        "post_effect_state_digest": states[7]["adaptive_control_state_digest"],
        "observation_state_digest": states[8]["adaptive_control_state_digest"],
        "evidence_digest": observation_event["payload"]["evidence_digest"],
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


def _build_qi_receipt(trace: Mapping[str, Any]) -> dict[str, Any]:
    states = list(trace["states"])
    history = []
    for index, event in enumerate(trace["events"]):
        kind = str(event["kind"])
        item: dict[str, Any] = {
            "event_kind": kind,
            "event_digest": event["adaptive_event_digest"],
            "source_state_digest": states[index]["adaptive_control_state_digest"],
            "target_state_digest": states[index + 1]["adaptive_control_state_digest"],
            "transition_visible": True,
            "memory_link_visible": index > 0,
            "nonmarkov_link_visible": index >= 2,
        }
        if kind == "OBSERVATION_COMMITTED":
            item["process_observation"] = kind
        else:
            item["process_action"] = kind
        history.append(item)
    raw = {
        "cycle_id": trace["cycle_id"],
        "candidate_only": True,
        "nonfinal_marker": True,
        "two_truths_gap": True,
        "noncollapse_guard": True,
        "memory_overwrite_blocker": True,
        "world_identity_blocker": True,
        "process_history": history,
    }
    receipt = evaluate_qi_process_tensor(raw).to_dict()
    if receipt["process_tensor_visible"] is not True:
        raise ValueError("adaptive_trace_qi_process_not_visible")
    if receipt["nonmarkov_memory_visible"] is not True:
        raise ValueError("adaptive_trace_nonmarkov_memory_not_visible")
    return receipt


def _process_lineage_digest(trace: Mapping[str, Any]) -> str:
    return sha(
        {
            "cycle_id": trace["cycle_id"],
            "adaptive_lineage_id": trace["initial_state"]["lineage_id"],
            "source_state_digest": trace["states"][0][
                "adaptive_control_state_digest"
            ],
            "ordered_event_digests": [
                event["adaptive_event_digest"] for event in trace["events"]
            ],
            "target_state_digest": trace["states"][-1][
                "adaptive_control_state_digest"
            ],
        }
    )


def _base_os_packet(
    *,
    name: str,
    cycle_id: str,
    lineage_digest: str,
    world_digest: str,
    input_digest: str,
    output_digest: str,
) -> dict[str, Any]:
    spec = OS_INTERFACE_SPECS[name]
    return {
        "os_kind": name,
        "cycle_id": cycle_id,
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


def _build_os_packets(
    trace: Mapping[str, Any],
    *,
    world_digest: str,
    lineage_digest: str,
) -> dict[str, dict[str, Any]]:
    states = list(trace["states"])
    events = list(trace["events"])
    cycle_id = str(trace["cycle_id"])
    belief_output = states[0]["adaptive_control_state_digest"]
    decision_output = states[1]["adaptive_control_state_digest"]
    plan_output = states[2]["plan_digest"]
    governance_output = states[5]["adaptive_control_state_digest"]
    act_output = states[7]["adaptive_control_state_digest"]
    observation_output = events[7]["payload"]["evidence_digest"]
    verification_output = events[8]["payload"]["verification_digest"]
    learning_output = events[9]["payload"]["next_plan_digest"]

    packets = {
        "BeliefOS": _base_os_packet(
            name="BeliefOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=world_digest,
            output_digest=belief_output,
        ),
        "DecisionOS": _base_os_packet(
            name="DecisionOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=belief_output,
            output_digest=decision_output,
        ),
        "PlanOS": _base_os_packet(
            name="PlanOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=decision_output,
            output_digest=plan_output,
        ),
        "Governance": _base_os_packet(
            name="Governance",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=plan_output,
            output_digest=governance_output,
        ),
        "ActOS": _base_os_packet(
            name="ActOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=governance_output,
            output_digest=act_output,
        ),
        "ObserveOS": _base_os_packet(
            name="ObserveOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=act_output,
            output_digest=observation_output,
        ),
        "VerifyOS": _base_os_packet(
            name="VerifyOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=observation_output,
            output_digest=verification_output,
        ),
        "LearnOS": _base_os_packet(
            name="LearnOS",
            cycle_id=cycle_id,
            lineage_digest=lineage_digest,
            world_digest=world_digest,
            input_digest=verification_output,
            output_digest=learning_output,
        ),
    }

    packets["BeliefOS"].update(
        {
            "source_state_digest": states[0]["adaptive_control_state_digest"],
            "concrete_source": "INITIAL_ADAPTIVE_BELIEF_STAGE",
        }
    )
    packets["DecisionOS"].update(
        {
            "event_digest": events[0]["adaptive_event_digest"],
            "target_state_digest": states[1]["adaptive_control_state_digest"],
        }
    )
    packets["PlanOS"].update(
        {
            "event_digest": events[1]["adaptive_event_digest"],
            "target_state_digest": states[2]["adaptive_control_state_digest"],
        }
    )
    packets["Governance"].update(
        {
            "cross_cutting": True,
            "single_stage": False,
            "act_admitted": True,
            "authority_event_digest": events[2]["adaptive_event_digest"],
            "lease_event_digest": events[3]["adaptive_event_digest"],
            "session_event_digest": events[4]["adaptive_event_digest"],
        }
    )
    packets["ActOS"].update(
        {
            "governance_decision_digest": governance_output,
            "external_authority_receipt_digest": states[5][
                "authority_receipt_digest"
            ],
            "authorization_event_digest": events[5]["adaptive_event_digest"],
            "effect_event_digest": events[6]["adaptive_event_digest"],
            "actual_intervention_appended": True,
        }
    )
    packets["ObserveOS"].update(
        {
            "event_digest": events[7]["adaptive_event_digest"],
            "observation_only": True,
            "verification_complete": False,
        }
    )
    packets["VerifyOS"].update(
        {
            "event_digest": events[8]["adaptive_event_digest"],
            "observation_digest": observation_output,
            "verification_complete": True,
            "truth_claim": False,
        }
    )
    packets["LearnOS"].update(
        {
            "event_digest": events[9]["adaptive_event_digest"],
            "verification_digest": verification_output,
            "future_only": True,
            "past_overwrite": False,
        }
    )
    if set(packets) != set(OS_KINDS):
        raise ValueError("adaptive_trace_os_packet_inventory_invalid")
    return packets


def build_adaptive_trace_adapter_receipt(
    *, label: str = "qi-world-concrete"
) -> dict[str, Any]:
    trace = build_nominal_adaptive_trace(label=label)
    world = _build_world_projection(trace)
    qi_receipt = _build_qi_receipt(trace)
    lineage_digest = _process_lineage_digest(trace)
    packets = _build_os_packets(
        trace,
        world_digest=world["world_projection_digest"],
        lineage_digest=lineage_digest,
    )
    interface_receipt = build_qi_world_os_interface_receipt(
        world_projection=world,
        qi_process_receipt=qi_receipt,
        os_packets=packets,
    )
    receipt = {
        "version": RECEIPT_VERSION,
        "cycle_id": trace["cycle_id"],
        "adaptive_trace": trace,
        "adaptive_trace_digest": trace["adaptive_trace_digest"],
        "process_lineage_digest": lineage_digest,
        "world_projection_digest": world["world_projection_digest"],
        "ordered_event_digests": [
            event["adaptive_event_digest"] for event in trace["events"]
        ],
        "qi_world_os_interface_receipt": interface_receipt,
        "adapter_non_authority": deepcopy(ADAPTER_NON_AUTHORITY),
        "adapter_receipt_digest": "",
    }
    receipt["adapter_receipt_digest"] = adapter_receipt_digest(receipt)
    errors = validate_adaptive_trace_adapter_receipt(receipt)
    if errors:
        raise ValueError("adaptive_trace_adapter_invalid:" + ";".join(errors))
    return receipt


def validate_adaptive_trace_adapter_receipt(
    receipt: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    try:
        if receipt.get("version") != RECEIPT_VERSION:
            errors.append("adaptive_adapter_version_invalid")
        if receipt.get("adapter_receipt_digest") != adapter_receipt_digest(receipt):
            errors.append("adaptive_adapter_digest_invalid")
        trace = dict(receipt.get("adaptive_trace", {}))
        errors.extend(
            f"trace:{error}" for error in validate_adaptive_trace(trace)
        )
        if receipt.get("adaptive_trace_digest") != trace.get(
            "adaptive_trace_digest"
        ):
            errors.append("adaptive_adapter_trace_digest_mismatch")
        expected_events = [
            event["adaptive_event_digest"] for event in trace.get("events", [])
        ]
        if list(receipt.get("ordered_event_digests", [])) != expected_events:
            errors.append("adaptive_adapter_event_order_mismatch")
        expected_lineage = _process_lineage_digest(trace)
        if receipt.get("process_lineage_digest") != expected_lineage:
            errors.append("adaptive_adapter_lineage_digest_mismatch")

        interface = dict(receipt.get("qi_world_os_interface_receipt", {}))
        errors.extend(
            f"interface:{error}"
            for error in validate_qi_world_os_interface_receipt(interface)
        )
        if interface.get("process_lineage_digest") != expected_lineage:
            errors.append("adaptive_adapter_interface_lineage_mismatch")
        if interface.get("world_projection_digest") != receipt.get(
            "world_projection_digest"
        ):
            errors.append("adaptive_adapter_world_projection_mismatch")
        if interface.get("cycle_id") != trace.get("cycle_id"):
            errors.append("adaptive_adapter_cycle_mismatch")

        packets = dict(interface.get("os_packets", {}))
        states = list(trace.get("states", []))
        events = list(trace.get("events", []))
        if states and packets.get("BeliefOS", {}).get("output_digest") != states[0].get(
            "adaptive_control_state_digest"
        ):
            errors.append("adaptive_adapter_belief_binding_invalid")
        if len(states) > 1 and packets.get("DecisionOS", {}).get(
            "output_digest"
        ) != states[1].get("adaptive_control_state_digest"):
            errors.append("adaptive_adapter_decision_binding_invalid")
        if len(states) > 2 and packets.get("PlanOS", {}).get("output_digest") != states[
            2
        ].get("plan_digest"):
            errors.append("adaptive_adapter_plan_binding_invalid")
        if len(states) > 5 and packets.get("Governance", {}).get(
            "output_digest"
        ) != states[5].get("adaptive_control_state_digest"):
            errors.append("adaptive_adapter_governance_binding_invalid")
        if len(states) > 7 and packets.get("ActOS", {}).get("output_digest") != states[
            7
        ].get("adaptive_control_state_digest"):
            errors.append("adaptive_adapter_act_binding_invalid")
        if len(events) > 7 and packets.get("ObserveOS", {}).get(
            "output_digest"
        ) != events[7].get("payload", {}).get("evidence_digest"):
            errors.append("adaptive_adapter_observe_binding_invalid")
        if len(events) > 8 and packets.get("VerifyOS", {}).get(
            "output_digest"
        ) != events[8].get("payload", {}).get("verification_digest"):
            errors.append("adaptive_adapter_verify_binding_invalid")
        if len(events) > 9 and packets.get("LearnOS", {}).get(
            "output_digest"
        ) != events[9].get("payload", {}).get("next_plan_digest"):
            errors.append("adaptive_adapter_learn_binding_invalid")
        if dict(receipt.get("adapter_non_authority", {})) != ADAPTER_NON_AUTHORITY:
            errors.append("adaptive_adapter_non_authority_invalid")
    except (IndexError, KeyError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors
