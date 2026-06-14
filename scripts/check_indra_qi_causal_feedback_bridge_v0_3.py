#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_causal_world_model_core_v14_0 import command_digest, valid_digest as valid_v14_digest
from runtime.kuuos_causal_world_model_os_v14_0 import build_kuuos_causal_world_model_os_v14_0
from runtime.kuuos_indra_qi_feedback_core_v0_3 import sha, valid_digest, without
from runtime.kuuos_runtime_daemon_indra_qi_causal_feedback_bridge_v0_3 import (
    build_indra_qi_causal_feedback_bridge_v0_3,
)
from runtime.kuuos_runtime_daemon_indra_qi_causal_projection_bridge_v0_2 import (
    build_indra_qi_causal_projection_bridge_v0_2,
)
from runtime.kuuos_runtime_daemon_indra_qi_world_model_v0_1 import (
    compute_indra_qi_world_state_digest,
)
from scripts.check_indra_qi_causal_projection_bridge_v0_2 import (
    bridge_license as projection_bridge_license,
    build_source,
    context as projection_context,
    latest,
    plan as projection_plan,
    read_json,
    records,
    write_json,
)

FEEDBACK_EXAMPLE = ROOT / "examples" / "indra_qi_causal_feedback_plan_v0_3.json"


def initialize_projection(root: pathlib.Path, suffix: str) -> tuple[dict[str, Any], dict[str, Any]]:
    source = build_source(root)
    plan = projection_plan(source, suffix)
    result = build_indra_qi_causal_projection_bridge_v0_2(
        runtime_context=projection_context(root),
        projection_plan=plan,
        projection_license=projection_bridge_license(list(plan["variables"])),
    ).to_dict()
    assert result["status"] == "INDRA_QI_CAUSAL_PROJECTION_BRIDGE_V0_2_READY", result
    return source, plan


def process_context(suffix: str) -> dict[str, str]:
    return {
        "process_tensor_digest": f"feedback-process-{suffix}",
        "memory_kernel_digest": f"feedback-memory-{suffix}",
        "history_window_digest": f"feedback-history-{suffix}",
        "instrument_trace_digest": f"feedback-instrument-{suffix}",
        "non_markov_context_digest": f"feedback-non-markov-{suffix}",
    }


def v14_license(kind: str, variables: list[str], command_hash: str) -> dict[str, Any]:
    value: dict[str, Any] = {
        "license_status": "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_LICENSE_READY",
        "bound_command_digest": command_hash,
        "state_read_allowed": True,
        "event_ledger_append_allowed": True,
        "result_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_command_kinds": [kind],
        "allowed_variables": variables,
        "protected_variables": [],
    }
    if kind == "observe":
        value.update(
            {
                "observation_update_allowed": True,
                "state_write_allowed": True,
                "snapshot_write_allowed": True,
                "direct_world_model_mutation_allowed": True,
            }
        )
    elif kind == "intervene":
        value.update(
            {
                "intervention_allowed": True,
                "state_write_allowed": True,
                "snapshot_write_allowed": True,
                "direct_world_model_mutation_allowed": True,
            }
        )
    elif kind == "counterfactual":
        value["counterfactual_allowed"] = True
    elif kind == "undo":
        value.update(
            {
                "undo_allowed": True,
                "state_write_allowed": True,
                "snapshot_read_allowed": True,
                "snapshot_write_allowed": True,
                "direct_world_model_mutation_allowed": True,
            }
        )
    return value


def run_v14(
    root: pathlib.Path,
    projection: dict[str, Any],
    *,
    kind: str,
    transaction_id: str,
) -> dict[str, Any]:
    if kind == "observe":
        payload = {
            "values": {"relational_load": 0.5, "qi_flow_signal": 0.7},
            "uncertainties": {"relational_load": 0.05, "qi_flow_signal": 0.1},
            "release_interventions": [],
        }
    elif kind == "counterfactual":
        payload = {
            "do": {"qi_flow_signal": 0.2},
            "uncertainties": {"qi_flow_signal": 0.08},
            "release": [],
        }
    else:
        raise AssertionError(kind)
    command: dict[str, Any] = {
        "kind": kind,
        "transaction_id": transaction_id,
        "world_id": projection["causal_world_id"],
        "payload": payload,
        "process_tensor_context": process_context(transaction_id),
    }
    command["command_digest"] = command_digest(command)
    result = build_kuuos_causal_world_model_os_v14_0(
        runtime_context={
            "runtime_root": str(root),
            "kuuos_causal_world_model_os_v14_0_enabled": True,
            "apply_kuuos_causal_world_model_os_v14_0": True,
        },
        command=command,
        license_packet=v14_license(kind, list(projection["variables"]), command["command_digest"]),
    ).to_dict()
    assert result["status"] == "KUUOS_CAUSAL_WORLD_MODEL_OS_V14_0_READY", result
    return result


def feedback_plan(
    root: pathlib.Path,
    source: dict[str, Any],
    projection: dict[str, Any],
    transaction_id: str,
    suffix: str,
) -> dict[str, Any]:
    value = json.loads(FEEDBACK_EXAMPLE.read_text(encoding="utf-8"))
    event = next(
        record
        for record in reversed(records(root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl"))
        if record["transaction_id"] == transaction_id
    )
    value.update(
        {
            "feedback_id": f"indra-qi-feedback-{suffix}",
            "source_projection_id": projection["projection_id"],
            "source_world_model_id": source["world_model_id"],
            "source_indra_qi_world_state_digest": source["indra_qi_world_state_digest"],
            "causal_world_id": projection["causal_world_id"],
            "source_transaction_id": transaction_id,
            "source_causal_event_digest": event["record_digest"],
            "source_causal_world_model_digest": event["after_world_model_digest"],
        }
    )
    return value


def feedback_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_LICENSE_READY",
        "source_indra_state_read_allowed": True,
        "source_projection_read_allowed": True,
        "source_causal_state_read_allowed": True,
        "source_causal_event_read_allowed": True,
        "source_causal_result_read_allowed": True,
        "feedback_plan_validate_allowed": True,
        "feedback_packet_write_allowed": True,
        "approval_handoff_write_allowed": True,
        "feedback_ledger_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "allowed_feedback_kinds": [
            "local_patch_observation_candidate",
            "qi_flow_observable_candidate",
        ],
    }
    value.update(overrides)
    return value


def feedback_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "runtime_root": str(root),
        "indra_qi_causal_feedback_bridge_v0_3_enabled": True,
        "apply_indra_qi_causal_feedback_bridge_v0_3": True,
    }


def run_feedback(root: pathlib.Path, plan: dict[str, Any], license_value: dict[str, Any] | None = None) -> dict[str, Any]:
    return build_indra_qi_causal_feedback_bridge_v0_3(
        runtime_context=feedback_context(root),
        feedback_plan=plan,
        feedback_license=license_value or feedback_license(),
    ).to_dict()


def assert_no_feedback_outputs(root: pathlib.Path) -> None:
    assert not (root / "indra_qi_causal_feedback_candidate_packet_v0_3.json").is_file()
    assert not (root / "indra_qi_causal_feedback_approval_handoff_v0_3.json").is_file()
    assert not (root / "indra_qi_causal_feedback_ledger_v0_3.jsonl").is_file()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)

        root = base / "observe-success"
        source, projection = initialize_projection(root, "feedback-observe")
        observe = run_v14(root, projection, kind="observe", transaction_id="feedback-observe-event")
        plan = feedback_plan(root, source, projection, "feedback-observe-event", "observe")
        result = run_feedback(root, plan)
        assert result["status"] == "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_READY", result
        assert result["source_event_kind"] == "observe"
        assert result["candidate_count"] == 3
        assert result["local_patch_candidate_count"] == 2
        assert result["qi_flow_candidate_count"] == 1
        assert result["source_indra_state_unchanged"] is True
        packet = read_json(root / "indra_qi_causal_feedback_candidate_packet_v0_3.json")
        handoff = read_json(root / "indra_qi_causal_feedback_approval_handoff_v0_3.json")
        ledger = latest(root / "indra_qi_causal_feedback_ledger_v0_3.jsonl")
        source_after = read_json(root / "ku_indra_qi_noncommutative_mandala_world_state.json")
        assert valid_digest(packet, "feedback_packet_digest")
        assert valid_digest(handoff, "approval_handoff_digest")
        assert valid_digest(ledger, "record_digest")
        assert packet["source_causal_event_digest"] == observe["event_record_digest"]
        assert packet["boundary"]["connection_update_not_inferred_from_causal_edges"] is True
        assert handoff["handoff_status"] == "approval_required"
        assert handoff["direct_application_allowed"] is False
        assert handoff["gauge_connection_mutation_allowed"] is False
        assert source_after["indra_qi_world_state_digest"] == source["indra_qi_world_state_digest"]
        assert compute_indra_qi_world_state_digest(source_after) == source["indra_qi_world_state_digest"]
        flow_candidates = [item for item in packet["feedback_candidates"] if item["feedback_kind"] == "qi_flow_observable_candidate"]
        assert len(flow_candidates) == 1
        assert flow_candidates[0]["target"]["qi_itself"] is False
        assert flow_candidates[0]["boundary"]["not_gauge_connection_mutation"] is True
        assert all(0.1 <= item["candidate_weight"] <= 0.95 for item in packet["feedback_candidates"])

        ledger_count = len(records(root / "indra_qi_causal_feedback_ledger_v0_3.jsonl"))
        replay = run_feedback(root, plan)
        assert replay["status"].endswith("BLOCKED")
        assert "feedback_id_replay" in replay["blockers"]
        assert "source_causal_transaction_feedback_replay" in replay["blockers"]
        assert len(records(root / "indra_qi_causal_feedback_ledger_v0_3.jsonl")) == ledger_count

        root = base / "counterfactual-success"
        source, projection = initialize_projection(root, "feedback-counterfactual")
        state_before = read_json(root / "kuuos_causal_world_model_state_v14_0.json")
        counterfactual = run_v14(
            root,
            projection,
            kind="counterfactual",
            transaction_id="feedback-counterfactual-event",
        )
        state_after = read_json(root / "kuuos_causal_world_model_state_v14_0.json")
        assert state_before["world_model_digest"] == state_after["world_model_digest"]
        plan = feedback_plan(root, source, projection, "feedback-counterfactual-event", "counterfactual")
        result = run_feedback(root, plan)
        assert result["status"] == "INDRA_QI_CAUSAL_FEEDBACK_BRIDGE_V0_3_READY", result
        assert result["source_event_kind"] == "counterfactual"
        packet = read_json(root / "indra_qi_causal_feedback_candidate_packet_v0_3.json")
        assert packet["source_causal_event_digest"] == counterfactual["event_record_digest"]
        assert max(item["candidate_weight"] for item in packet["feedback_candidates"]) < 0.9

        root = base / "direct-apply"
        source, projection = initialize_projection(root, "feedback-direct")
        run_v14(root, projection, kind="observe", transaction_id="feedback-direct-event")
        plan = feedback_plan(root, source, projection, "feedback-direct-event", "direct")
        plan["apply_feedback_directly"] = True
        result = run_feedback(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "feedback_plan_direct_apply_not_false" in result["blockers"]
        assert_no_feedback_outputs(root)

        root = base / "gauge-inference"
        source, projection = initialize_projection(root, "feedback-gauge")
        run_v14(root, projection, kind="observe", transaction_id="feedback-gauge-event")
        plan = feedback_plan(root, source, projection, "feedback-gauge-event", "gauge")
        plan["infer_gauge_connection_update_from_causal_edges"] = True
        result = run_feedback(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "feedback_plan_gauge_connection_inference_not_false" in result["blockers"]
        assert_no_feedback_outputs(root)

        root = base / "qi-identity"
        source, projection = initialize_projection(root, "feedback-qi-identity")
        packet_path = root / "indra_qi_causal_projection_packet_v0_2.json"
        activation_path = root / "indra_qi_causal_projection_activation_record_v0_2.json"
        projection_packet = read_json(packet_path)
        projection_packet["variable_bindings"]["qi_flow_signal"]["qi_itself"] = True
        projection_packet["projection_packet_digest"] = sha(without(projection_packet, "projection_packet_digest"))
        write_json(packet_path, projection_packet)
        activation = read_json(activation_path)
        activation["source_projection_packet_digest"] = projection_packet["projection_packet_digest"]
        activation["activation_record_digest"] = sha(without(activation, "activation_record_digest"))
        write_json(activation_path, activation)
        run_v14(root, projection, kind="observe", transaction_id="feedback-qi-identity-event")
        plan = feedback_plan(root, source, projection, "feedback-qi-identity-event", "qi-identity")
        result = run_feedback(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "feedback_variable_qi_flow_signal_qi_itself_not_false" in result["blockers"]
        assert_no_feedback_outputs(root)

        root = base / "event-digest"
        source, projection = initialize_projection(root, "feedback-event-digest")
        run_v14(root, projection, kind="observe", transaction_id="feedback-event-digest-event")
        plan = feedback_plan(root, source, projection, "feedback-event-digest-event", "event-digest")
        plan["source_causal_event_digest"] = "mismatch"
        result = run_feedback(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "feedback_source_causal_event_digest_mismatch" in result["blockers"]
        assert_no_feedback_outputs(root)

        root = base / "license-kind"
        source, projection = initialize_projection(root, "feedback-license")
        run_v14(root, projection, kind="observe", transaction_id="feedback-license-event")
        plan = feedback_plan(root, source, projection, "feedback-license-event", "license")
        result = run_feedback(
            root,
            plan,
            feedback_license(allowed_feedback_kinds=["local_patch_observation_candidate"]),
        )
        assert result["status"].endswith("BLOCKED")
        assert "feedback_license_allowed_feedback_kinds_not_exact" in result["blockers"]
        assert "feedback_candidate_kind_not_licensed" in result["blockers"]
        assert_no_feedback_outputs(root)

        root = base / "initialize-ineligible"
        source, projection = initialize_projection(root, "feedback-initialize")
        initialization_event = latest(root / "kuuos_causal_world_model_event_ledger_v14_0.jsonl")
        plan = json.loads(FEEDBACK_EXAMPLE.read_text(encoding="utf-8"))
        plan.update(
            {
                "feedback_id": "indra-qi-feedback-initialize",
                "source_projection_id": projection["projection_id"],
                "source_world_model_id": source["world_model_id"],
                "source_indra_qi_world_state_digest": source["indra_qi_world_state_digest"],
                "causal_world_id": projection["causal_world_id"],
                "source_transaction_id": projection["transaction_id"],
                "source_causal_event_digest": initialization_event["record_digest"],
                "source_causal_world_model_digest": initialization_event["after_world_model_digest"],
            }
        )
        result = run_feedback(root, plan)
        assert result["status"].endswith("BLOCKED")
        assert "source_causal_event_kind_not_feedback_eligible" in result["blockers"]
        assert_no_feedback_outputs(root)

    print("indra_qi_causal_feedback_bridge_v0_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
