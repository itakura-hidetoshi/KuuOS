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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_v13_8 import build_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_execution_intent_receipt_ledger_v12_5 import build_physical_quantum_qi_guarded_execution_intent_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_transition_executor_v12_6 import build_physical_quantum_qi_guarded_transition_executor
from runtime.kuuos_runtime_daemon_physical_quantum_qi_process_tensor_execution_feedback_v12_7 import build_physical_quantum_qi_process_tensor_execution_feedback
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9 import build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_v13_10 import build_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-10",
    "memory_kernel_digest": "memory-kernel-digest-v13-10",
    "history_window_digest": "history-window-digest-v13-10",
    "instrument_trace_digest": "instrument-trace-digest-v13-10",
    "non_markov_context_digest": "non-markov-context-digest-v13-10",
}
V13_7_BOUNDARY = {
    "receipt_ledger_only": True,
    "guarded_intent_bridge_receipt_only": True,
    "guarded_execution_intent_packet_traceable": True,
    "guarded_execution_intent_bridge_state_traceable": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "bridge_not_direct_execution": True,
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
EXEC_BOUNDARY = {
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


def bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_LICENSE_READY",
        "v12_6_execution_record_read_allowed": True,
        "v12_6_next_cycle_state_read_allowed": True,
        "v12_6_memory_consumption_ledger_read_allowed": True,
        "v12_6_external_state_mutation_ledger_read_allowed": True,
        "v12_7_feedback_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v13_8_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_enabled": True,
        "apply_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge": True,
        "runtime_root": str(root),
    }


def v13_8_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_LICENSE_READY",
        "guarded_intent_bridge_receipt_ledger_read_allowed": True,
        "v12_5_guarded_execution_intent_packet_write_allowed": True,
        "compatibility_bridge_state_write_allowed": True,
        "compatibility_bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v12_5_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v12_5_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_LICENSE_READY",
        "guarded_execution_intent_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v13_9_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge": True,
        "runtime_root": str(root),
    }


def v13_9_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_LICENSE_READY",
        "v12_5_guarded_execution_intent_receipt_ledger_read_allowed": True,
        "v12_6_transition_executor_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v12_6_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_transition_executor_enabled": True,
        "apply_physical_quantum_qi_guarded_transition_executor": True,
        "runtime_root": str(root),
    }


def v12_6_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_LICENSE_READY",
        "guarded_execution_intent_receipt_ledger_read_allowed": True,
        "internal_transition_record_write_allowed": True,
        "next_cycle_state_write_allowed": True,
        "memory_consumption_append_allowed": True,
        "external_state_mutation_append_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v12_7_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_process_tensor_execution_feedback_enabled": True,
        "apply_physical_quantum_qi_process_tensor_execution_feedback": True,
        "runtime_root": str(root),
    }


def v12_7_lic() -> dict[str, Any]:
    return {
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


def v13_7_receipt(kind: str) -> dict[str, Any]:
    bridge = {
        "ready": "integrated_candidate_to_guarded_intent_ready",
        "hold": "integrated_candidate_to_guarded_intent_hold",
        "block": "integrated_candidate_to_guarded_intent_block",
    }[kind]
    status = {
        "ready": "guarded_execution_intent_ready",
        "hold": "guarded_execution_intent_hold",
        "block": "guarded_execution_intent_block",
    }[kind]
    emit = {
        "ready": "emit_guarded_ready_intent",
        "hold": "emit_guarded_hold_intent",
        "block": "emit_guarded_block_intent",
    }[kind]
    w = weight(kind)
    intents = []
    if kind == "ready":
        intents = [{
            "intent_index": 0,
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "candidate_id": "v13-10-compat-candidate",
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": dict(w),
            "process_tensor_context": dict(PT),
            "source_integrated_candidate_digest": "v13-10-candidate-digest",
            "boundary": dict(INTENT_BOUNDARY),
            "guarded_execution_intent_digest": "v13-10-guarded-intent-digest",
        }]
    return {
        "version": "physical_quantum_qi_guarded_intent_bridge_receipt_record_v13_7",
        "record_type": "physical_quantum_qi_guarded_intent_bridge_receipt",
        "bridge_status": bridge,
        "guarded_execution_intent_status": status,
        "guarded_intent_emit_action": emit,
        "guarded_execution_intent_count": len(intents),
        "guarded_execution_intents": intents,
        "candidate_weighting": w,
        "process_tensor_context": dict(PT),
        "source_integrated_candidate_to_guarded_intent_bridge_digest": "v13-10-bridge-digest",
        "source_guarded_execution_intent_packet_digest": "v13-10-intent-packet-digest",
        "source_cycle_gate_reentry_integration_receipt_digest": "v13-10-integration-receipt-digest",
        "source_cycle_gate_reentry_integration_digest": "v13-10-integration-digest",
        "prev_record_digest": "GENESIS",
        "record_digest": f"v13-7-receipt-{kind}",
        "boundary": dict(V13_7_BOUNDARY),
        "epoch": 1,
    }


def execution_record(kind: str, *, bad_boundary: bool = False, bad_effect: bool = False, missing_context: bool = False) -> dict[str, Any]:
    status = {
        "ready": "guarded_transition_executed",
        "hold": "guarded_transition_hold",
        "block": "guarded_transition_block",
    }[kind]
    executed = kind == "ready"
    effects = {
        "internal_transition_record": True,
        "next_cycle_state_update": executed,
        "memory_consumption": executed,
        "external_state_mutation": executed,
    }
    if bad_effect:
        effects["next_cycle_state_update"] = not effects["next_cycle_state_update"]
    context = dict(PT)
    if missing_context:
        context["non_markov_context_digest"] = ""
    boundary = dict(EXEC_BOUNDARY)
    boundary["can_update_next_cycle_state"] = executed
    boundary["can_consume_memory"] = executed
    boundary["can_mutate_runtime_external_state"] = executed
    if bad_boundary:
        boundary["guarded_transition_executor"] = False
    rec = {
        "version": "physical_quantum_qi_guarded_transition_execution_record_v12_6",
        "execution_status": status,
        "execution_layer_entrypoint": True,
        "no_dry_run_required": True,
        "effects": effects,
        "intent_count": 1 if executed else 0,
        "guarded_execution_intents": [],
        "process_tensor_context": context,
        "source_guarded_execution_intent_receipt_digest": "v12-5-receipt-digest-v13-10",
        "source_guarded_execution_intent_packet_digest": "v12-5-packet-digest-v13-10",
        "boundary": boundary,
        "epoch": 1,
    }
    rec["execution_record_digest"] = f"execution-record-digest-{kind}"
    return rec


def effect_files(runtime: pathlib.Path, rec: dict[str, Any], *, missing_next: bool = False, unexpected_effect: bool = False) -> None:
    if rec["execution_status"] == "guarded_transition_executed" and not missing_next:
        dump(runtime / "physical_quantum_qi_next_cycle_state.json", {
            "version": "physical_quantum_qi_next_cycle_state_v12_6",
            "next_cycle_started": True,
            "source_execution_record_digest": rec["execution_record_digest"],
            "process_tensor_context": dict(rec["process_tensor_context"]),
            "next_cycle_state_digest": "next-cycle-state-digest-v13-10",
            "epoch": 1,
        })
        append_jsonl(runtime / "physical_quantum_qi_memory_consumption_ledger.jsonl", {
            "version": "physical_quantum_qi_memory_consumption_receipt_v12_6",
            "memory_consumed": True,
            "consumption_scope": "runtime_local_memory_ledger",
            "source_execution_record_digest": rec["execution_record_digest"],
            "intent_count": rec["intent_count"],
            "memory_consumption_digest": "memory-consumption-digest-v13-10",
            "epoch": 1,
        })
        append_jsonl(runtime / "physical_quantum_qi_external_state_mutation_ledger.jsonl", {
            "version": "physical_quantum_qi_external_state_mutation_receipt_v12_6",
            "external_state_mutated": True,
            "mutation_scope": "runtime_local_external_state_store",
            "source_execution_record_digest": rec["execution_record_digest"],
            "intent_count": rec["intent_count"],
            "external_state_mutation_digest": "external-state-mutation-digest-v13-10",
            "epoch": 1,
        })
    elif unexpected_effect:
        dump(runtime / "physical_quantum_qi_next_cycle_state.json", {
            "next_cycle_started": True,
            "source_execution_record_digest": rec["execution_record_digest"],
            "next_cycle_state_digest": "unexpected-next-cycle-state-digest",
        })


def run_bridge(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any], *, missing_next: bool = False, unexpected_effect: bool = False) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        dump(runtime / "physical_quantum_qi_guarded_transition_execution_record.json", rec)
        effect_files(runtime, rec, missing_next=missing_next, unexpected_effect=unexpected_effect)
    result = build_physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge(
        runtime_context=bridge_ctx(runtime),
        v12_6_to_v12_7_process_tensor_feedback_bridge_license=license_packet,
    ).to_dict()
    state = load_json(runtime / "physical_quantum_qi_v12_7_process_tensor_feedback_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_ledger.jsonl")
    return result, state, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], state: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_READY", (label, out)
    assert out["feedback_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert state["boundary"]["can_feed_v12_7_process_tensor_execution_feedback"] is True, label
    assert state["boundary"]["does_not_run_feedback_runtime"] is True, label
    assert ledger[-1]["boundary"]["v12_7_feedback_ready_state_traceable"] is True, label


def assert_v12_7_accepts(label: str, runtime: pathlib.Path, expected: str) -> None:
    out = build_physical_quantum_qi_process_tensor_execution_feedback(
        runtime_context=v12_7_ctx(runtime),
        process_tensor_execution_feedback_license=v12_7_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_EXECUTION_FEEDBACK_READY", (label, out)
    assert out["feedback_status"] == expected, (label, out)
    if expected == "process_tensor_feedback_reinforce_next_cycle":
        assert out["next_cycle_observed"] is True, label
        assert out["memory_feedback_observed"] is True, label
        assert out["external_backaction_observed"] is True, label
    else:
        assert out["next_cycle_observed"] is False, label
        assert out["memory_feedback_observed"] is False, label
        assert out["external_backaction_observed"] is False, label


def run_full_v13_7_to_v12_7(root: pathlib.Path, kind: str) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / f"full_{kind}"
    append_jsonl(runtime / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl", v13_7_receipt(kind))
    compat = build_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge(
        runtime_context=v13_8_ctx(runtime),
        guarded_intent_receipt_ledger_compatibility_bridge_license=v13_8_lic(),
    ).to_dict()
    assert compat["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_READY", compat
    v12_5 = build_physical_quantum_qi_guarded_execution_intent_receipt_ledger(
        runtime_context=v12_5_ctx(runtime),
        guarded_execution_intent_receipt_ledger_license=v12_5_lic(),
    ).to_dict()
    assert v12_5["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_READY", v12_5
    v13_9 = build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
        runtime_context=v13_9_ctx(runtime),
        v12_5_to_v12_6_transition_executor_bridge_license=v13_9_lic(),
    ).to_dict()
    assert v13_9["status"] == "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_READY", v13_9
    v12_6 = build_physical_quantum_qi_guarded_transition_executor(
        runtime_context=v12_6_ctx(runtime),
        guarded_transition_executor_license=v12_6_lic(),
    ).to_dict()
    assert v12_6["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_TRANSITION_EXECUTOR_READY", v12_6
    out, state, ledger = run_bridge(root, f"full_{kind}", None, bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, state, ledger)
    expected = {
        "ready": "process_tensor_feedback_reinforce_next_cycle",
        "hold": "process_tensor_feedback_hold_context",
        "block": "process_tensor_feedback_block_context",
    }[kind]
    assert out["expected_v12_7_feedback_status"] == expected
    assert_v12_7_accepts(f"full_{kind}", runtime, expected)
    return out, state, ledger


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind, expected in [
            ("ready", "process_tensor_feedback_reinforce_next_cycle"),
            ("hold", "process_tensor_feedback_hold_context"),
            ("block", "process_tensor_feedback_block_context"),
        ]:
            out, state, ledger = run_bridge(root, kind, execution_record(kind), bridge_lic())
            assert_bridge_ready(kind, out, state, ledger)
            assert out["expected_v12_7_feedback_status"] == expected
            assert_v12_7_accepts(kind, root / kind, expected)

        for kind in ["ready", "hold", "block"]:
            run_full_v13_7_to_v12_7(root, kind)

        out, state, ledger = run_bridge(root, "chain", execution_record("ready"), bridge_lic())
        assert_bridge_ready("chain_1", out, state, ledger)
        out, state, ledger = run_bridge(root, "chain", execution_record("hold"), bridge_lic())
        assert_bridge_ready("chain_2", out, state, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, state, ledger = run_bridge(root, "bad_boundary", execution_record("ready", bad_boundary=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_6_guarded_transition_execution_boundary_guarded_transition_executor_missing" in out["blockers"]
        assert state == {}
        assert ledger == []

        out, state, ledger = run_bridge(root, "bad_effect", execution_record("ready", bad_effect=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_6_guarded_transition_guarded_transition_executed_next_cycle_state_update_effect_mismatch" in out["blockers"]
        assert state == {}

        out, state, ledger = run_bridge(root, "missing_next", execution_record("ready"), bridge_lic(), missing_next=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_7_bridge_executed_transition_next_cycle_state_not_observed" in out["blockers"]
        assert state == {}

        out, state, ledger = run_bridge(root, "unexpected_effect", execution_record("hold"), bridge_lic(), unexpected_effect=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_7_bridge_hold_or_block_with_unexpected_runtime_effect_observed" in out["blockers"]
        assert state == {}

        out, state, ledger = run_bridge(root, "missing_context", execution_record("ready", missing_context=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "process_tensor_context_non_markov_context_digest_missing" in out["blockers"]
        assert state == {}

        out, state, ledger = run_bridge(root, "missing", None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_6_guarded_transition_execution_record_missing_or_invalid" in out["blockers"]
        assert state == {}

        out, state, ledger = run_bridge(root, "license", execution_record("ready"), bridge_lic(v12_7_feedback_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_6_TO_V12_7_PROCESS_TENSOR_FEEDBACK_BRIDGE_BLOCKED"
        assert "v12_7_feedback_ready_state_write_not_allowed" in out["blockers"]
        assert state == {}

    print("physical_quantum_qi_v12_6_to_v12_7_process_tensor_feedback_bridge_v13_10 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
