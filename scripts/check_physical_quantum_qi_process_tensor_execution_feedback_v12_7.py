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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7 import build_physical_quantum_qi_process_tensor_execution_feedback

PT = {
    "process_tensor_digest": "pt-digest-v12-7",
    "memory_kernel_digest": "memory-kernel-digest-v12-7",
    "history_window_digest": "history-window-digest-v12-7",
    "instrument_trace_digest": "instrument-trace-digest-v12-7",
    "non_markov_context_digest": "non-markov-context-digest-v12-7",
}
BOUNDARY = {
    "guarded_transition_executor": True,
    "can_update_next_cycle_state": True,
    "can_consume_memory": True,
    "can_mutate_runtime_external_state": True,
    "runtime_local_external_state_only": True,
    "license_gated_execution": True,
    "no_dry_run_required": True,
    "fail_closed_on_boundary_loss": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_process_tensor_execution_feedback_enabled": True,
        "apply_physical_quantum_qi_process_tensor_execution_feedback": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_LICENSE_READY",
        "guarded_transition_execution_record_read_allowed": True,
        "next_cycle_state_read_allowed": True,
        "memory_consumption_ledger_read_allowed": True,
        "external_state_mutation_ledger_read_allowed": True,
        "process_tensor_feedback_append_allowed": True,
        "path_integral_feedback_state_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def execution_record(status: str, *, bad_boundary: bool = False, mismatch: bool = False) -> dict[str, Any]:
    executed = status == "guarded_transition_executed"
    boundary = dict(BOUNDARY)
    if not executed:
        boundary["can_update_next_cycle_state"] = False
        boundary["can_consume_memory"] = False
        boundary["can_mutate_runtime_external_state"] = False
    if bad_boundary:
        boundary["runtime_local_external_state_only"] = False
    context = dict(PT)
    if mismatch:
        context["process_tensor_digest"] = ""
    rec = {
        "version": "physical_quantum_qi_guarded_transition_execution_record_v12_6",
        "execution_status": status,
        "execution_layer_entrypoint": True,
        "no_dry_run_required": True,
        "effects": {
            "internal_transition_record": True,
            "next_cycle_state_update": executed,
            "memory_consumption": executed,
            "external_state_mutation": executed,
        },
        "intent_count": 1 if executed else 0,
        "guarded_execution_intents": [],
        "process_tensor_context": context,
        "source_guarded_execution_intent_receipt_digest": "intent-receipt-digest-v12-7",
        "source_guarded_execution_intent_packet_digest": "intent-packet-digest-v12-7",
        "boundary": boundary,
        "epoch": 1,
    }
    rec["execution_record_digest"] = f"execution-record-digest-{status}"
    return rec


def write_effects(root: pathlib.Path) -> None:
    dump(root / "physical_quantum_qi_next_cycle_state.json", {
        "version": "physical_quantum_qi_next_cycle_state_v12_6",
        "next_cycle_started": True,
        "next_cycle_state_digest": "next-cycle-state-digest-v12-7",
        "process_tensor_context": dict(PT),
    })
    append_jsonl(root / "physical_quantum_qi_memory_consumption_ledger.jsonl", {
        "version": "physical_quantum_qi_memory_consumption_receipt_v12_6",
        "memory_consumed": True,
        "memory_consumption_digest": "memory-consumption-digest-v12-7",
    })
    append_jsonl(root / "physical_quantum_qi_external_state_mutation_ledger.jsonl", {
        "version": "physical_quantum_qi_external_state_mutation_receipt_v12_6",
        "external_state_mutated": True,
        "external_state_mutation_digest": "external-state-mutation-digest-v12-7",
    })


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any], *, effects: bool = False) -> tuple[dict[str, Any], pathlib.Path]:
    runtime = root / name
    if record is not None:
        dump(runtime / "physical_quantum_qi_guarded_transition_execution_record.json", record)
    if effects:
        write_effects(runtime)
    result = build_physical_quantum_qi_process_tensor_execution_feedback(
        runtime_context=ctx(runtime),
        process_tensor_execution_feedback_license=license_packet,
    )
    return result.to_dict(), runtime


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, runtime = run(root, "executed", execution_record("guarded_transition_executed"), lic(), effects=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY"
        assert out["feedback_status"] == "process_tensor_feedback_reinforce_next_cycle"
        assert out["memory_feedback_observed"] is True
        assert out["external_backaction_observed"] is True
        assert out["next_cycle_observed"] is True
        packet = load_json(runtime / "physical_quantum_qi_process_tensor_execution_feedback_packet.json")
        assert packet["process_tensor_feedback_kernel"]["path_weight_delta"] == 1
        state = load_json(runtime / "physical_quantum_qi_path_integral_feedback_state.json")
        assert state["boundary"]["can_feed_next_path_integral_cycle"] is True
        assert load_jsonl(runtime / "physical_quantum_qi_process_tensor_execution_feedback_ledger.jsonl")[-1]["feedback_status"] == "process_tensor_feedback_reinforce_next_cycle"

        out, runtime = run(root, "hold", execution_record("guarded_transition_hold"), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY"
        assert out["feedback_status"] == "process_tensor_feedback_hold_context"
        assert load_json(runtime / "physical_quantum_qi_path_integral_feedback_state.json")["path_weight_delta"] == 0

        out, runtime = run(root, "block", execution_record("guarded_transition_block"), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY"
        assert out["feedback_status"] == "process_tensor_feedback_block_context"
        assert load_json(runtime / "physical_quantum_qi_path_integral_feedback_state.json")["path_weight_delta"] == -1

        out, _ = run(root, "missing_effects", execution_record("guarded_transition_executed"), lic(), effects=False)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "executed_transition_next_cycle_state_not_observed" in out["blockers"]
        assert "executed_transition_memory_consumption_not_observed" in out["blockers"]
        assert "executed_transition_external_state_mutation_not_observed" in out["blockers"]

        out, _ = run(root, "unexpected_effect", execution_record("guarded_transition_hold"), lic(), effects=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "hold_or_block_transition_with_unexpected_runtime_effect_observed" in out["blockers"]

        out, _ = run(root, "bad_boundary", execution_record("guarded_transition_executed", bad_boundary=True), lic(), effects=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "guarded_transition_execution_boundary_runtime_local_external_state_only_missing" in out["blockers"]

        out, _ = run(root, "bad_context", execution_record("guarded_transition_executed", mismatch=True), lic(), effects=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "process_tensor_context_process_tensor_digest_missing" in out["blockers"]

        out, _ = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "guarded_transition_execution_record_missing_or_invalid" in out["blockers"]

        out, _ = run(root, "license", execution_record("guarded_transition_executed"), lic(path_integral_feedback_state_write_allowed=False), effects=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_BLOCKED"
        assert "path_integral_feedback_state_write_not_allowed" in out["blockers"]

    print("physical_quantum_qi_process_tensor_execution_feedback_v12_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
