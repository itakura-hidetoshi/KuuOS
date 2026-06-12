#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib
import sys
import tempfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9 import (
    build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_9_to_v12_6_executor_activation_v13_23 import (
    build_physical_quantum_qi_v13_9_to_v12_6_executor_activation,
)

PT = {
    "process_tensor_digest": "pt-v13-23",
    "memory_kernel_digest": "memory-v13-23",
    "history_window_digest": "history-v13-23",
    "instrument_trace_digest": "instrument-v13-23",
    "non_markov_context_digest": "non-markov-v13-23",
}
RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "guarded_execution_intent_receipt_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
    "receipt_does_not_mutate_intent_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
INTENT_BOUNDARY = {
    "guarded_execution_intent_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def weight(kind: str) -> dict[str, Any]:
    if kind == "ready":
        return {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "hold":
        return {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def receipt(kind: str) -> dict[str, Any]:
    status = {
        "ready": "guarded_execution_intent_ready",
        "hold": "guarded_execution_intent_hold",
        "block": "guarded_execution_intent_block",
    }[kind]
    intents: list[dict[str, Any]] = []
    if kind == "ready":
        intents = [{
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "intent_index": 0,
            "candidate_id": "candidate-v13-23",
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": weight(kind),
            "process_tensor_context": dict(PT),
            "source_transition_candidate_envelope_digest": "envelope-v13-23",
            "guarded_execution_intent_digest": "intent-v13-23",
            "boundary": dict(INTENT_BOUNDARY),
        }]
    return {
        "version": "physical_quantum_qi_guarded_execution_intent_receipt_record_v12_5",
        "record_type": "physical_quantum_qi_guarded_execution_intent_receipt",
        "execution_intent_status": status,
        "envelope_status": {
            "ready": "transition_candidate_envelope_ready",
            "hold": "transition_candidate_envelope_hold",
            "block": "transition_candidate_envelope_block",
        }[kind],
        "transition_precheck_decision": {
            "ready": "transition_precheck_admit_candidate",
            "hold": "transition_precheck_hold_candidate",
            "block": "transition_precheck_block_candidate",
        }[kind],
        "intent_count": len(intents),
        "envelope_count": len(intents),
        "guarded_execution_intents": intents,
        "process_tensor_context": dict(PT),
        "source_guarded_execution_intent_packet_digest": "packet-v13-23",
        "source_transition_candidate_envelope_receipt_digest": "envelope-receipt-v13-23",
        "source_transition_candidate_envelope_packet_digest": "envelope-packet-v13-23",
        "prev_record_digest": "GENESIS",
        "record_digest": f"receipt-v13-23-{kind}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def bridge_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge": True,
        "runtime_root": str(root),
    }


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_LICENSE_READY",
        "v12_5_guarded_execution_intent_receipt_ledger_read_allowed": True,
        "v12_6_transition_executor_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def executor_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_LICENSE_READY",
        "guarded_execution_intent_receipt_ledger_read_allowed": True,
        "internal_transition_record_write_allowed": True,
        "next_cycle_state_write_allowed": True,
        "memory_consumption_append_allowed": True,
        "external_state_mutation_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_9_to_v12_6_executor_activation_enabled": True,
        "apply_physical_quantum_qi_v13_9_to_v12_6_executor_activation": True,
        "runtime_root": str(root),
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_9_TO_V12_6_EXECUTOR_ACTIVATION_LICENSE_READY",
        "v13_9_ready_state_read_allowed": True,
        "v12_5_receipt_ledger_read_allowed": True,
        "v12_6_executor_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "executor_license": executor_license(),
    }
    value.update(overrides)
    return value


def run_case(root: pathlib.Path, kind: str) -> dict[str, Any]:
    runtime = root / kind
    append_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl", receipt(kind))
    bridge = build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
        runtime_context=bridge_context(runtime),
        v12_5_to_v12_6_transition_executor_bridge_license=bridge_license(),
    ).to_dict()
    assert bridge["status"] == "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_READY", bridge
    result = build_physical_quantum_qi_v13_9_to_v12_6_executor_activation(
        runtime_context=activation_context(runtime),
        v13_9_to_v12_6_executor_activation_license=activation_license(),
    ).to_dict()
    return result


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        expected = {
            "ready": ("guarded_transition_executed", True, True, True),
            "hold": ("guarded_transition_hold", False, False, False),
            "block": ("guarded_transition_block", False, False, False),
        }
        for kind, values in expected.items():
            result = run_case(root, kind)
            execution_status, next_cycle, memory, external = values
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_9_TO_V12_6_EXECUTOR_ACTIVATION_READY", (kind, result)
            assert result["observed_execution_status"] == execution_status
            assert result["execution_invoked"] is True
            assert result["execution_record_written"] is True
            assert result["next_cycle_state_updated"] is next_cycle
            assert result["memory_consumption_appended"] is memory
            assert result["external_state_mutation_appended"] is external

        runtime = root / "digest_mismatch"
        append_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl", receipt("ready"))
        build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
            runtime_context=bridge_context(runtime),
            v12_5_to_v12_6_transition_executor_bridge_license=bridge_license(),
        )
        state_path = runtime / "physical_quantum_qi_v12_6_guarded_transition_executor_ready_state.json"
        state = load_json(state_path)
        state["source_v12_5_guarded_execution_intent_receipt_digest"] = "wrong-digest"
        write_json(state_path, state)
        blocked = build_physical_quantum_qi_v13_9_to_v12_6_executor_activation(
            runtime_context=activation_context(runtime),
            v13_9_to_v12_6_executor_activation_license=activation_license(),
        ).to_dict()
        assert blocked["status"].endswith("BLOCKED")
        assert blocked["execution_invoked"] is False
        assert "v13_9_ready_state_receipt_digest_mismatch" in blocked["blockers"]

        runtime = root / "license_block"
        append_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl", receipt("ready"))
        build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
            runtime_context=bridge_context(runtime),
            v12_5_to_v12_6_transition_executor_bridge_license=bridge_license(),
        )
        blocked = build_physical_quantum_qi_v13_9_to_v12_6_executor_activation(
            runtime_context=activation_context(runtime),
            v13_9_to_v12_6_executor_activation_license=activation_license(v12_6_executor_invoke_allowed=False),
        ).to_dict()
        assert blocked["status"].endswith("BLOCKED")
        assert blocked["execution_invoked"] is False
        assert "v12_6_executor_invoke_not_allowed" in blocked["blockers"]

    print("physical_quantum_qi_v13_23_executor_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
