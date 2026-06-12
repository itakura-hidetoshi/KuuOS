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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_v13_22 import build_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_v13_9 import build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-22",
    "memory_kernel_digest": "memory-kernel-digest-v13-22",
    "history_window_digest": "history-window-digest-v13-22",
    "instrument_trace_digest": "instrument-trace-digest-v13-22",
    "non_markov_context_digest": "non-markov-context-digest-v13-22",
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


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def bridge_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge": True,
        "runtime_root": str(root),
    }


def bridge_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_5_RECEIPT_TO_V12_6_EXECUTOR_READINESS_BRIDGE_LICENSE_READY",
        "v12_5_receipt_ledger_read_allowed": True,
        "v13_9_bridge_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v13_9_context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge_enabled": True,
        "apply_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge": True,
        "runtime_root": str(root),
    }


def v13_9_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_LICENSE_READY",
        "v12_5_guarded_execution_intent_receipt_ledger_read_allowed": True,
        "v12_6_transition_executor_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def parts(kind: str) -> tuple[str, str, int, dict[str, Any]]:
    if kind == "ready":
        return "guarded_execution_intent_ready", "guarded_transition_executed", 1, {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "hold":
        return "guarded_execution_intent_hold", "guarded_transition_hold", 0, {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "guarded_execution_intent_block", "guarded_transition_block", 0, {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def receipt(kind: str, *, bad_boundary: bool = False, bad_count: bool = False, missing_context: bool = False, bad_weight: bool = False) -> dict[str, Any]:
    status, _, count, weighting = parts(kind)
    weighting = dict(weighting)
    if bad_weight and kind == "ready":
        weighting["path_weight_delta"] = 0
    context = dict(PT)
    if missing_context:
        context["process_tensor_digest"] = ""
    boundary = dict(RECEIPT_BOUNDARY)
    if bad_boundary:
        boundary["receipt_does_not_mutate_intent_packet"] = False
    intents: list[dict[str, Any]] = []
    if count:
        intents = [{
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "intent_index": 0,
            "candidate_id": "candidate-v13-22",
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": weighting,
            "process_tensor_context": context,
            "source_transition_candidate_envelope_digest": "envelope-digest-v13-22",
            "guarded_execution_intent_digest": "intent-digest-v13-22",
            "boundary": dict(INTENT_BOUNDARY),
        }]
    if bad_count:
        intents = [] if count else [{"intent_type": "physical_quantum_qi_guarded_execution_intent"}]
    return {
        "version": "physical_quantum_qi_guarded_execution_intent_receipt_record_v12_5",
        "record_type": "physical_quantum_qi_guarded_execution_intent_receipt",
        "execution_intent_status": status,
        "envelope_status": {
            "guarded_execution_intent_ready": "transition_candidate_envelope_ready",
            "guarded_execution_intent_hold": "transition_candidate_envelope_hold",
            "guarded_execution_intent_block": "transition_candidate_envelope_block",
        }[status],
        "transition_precheck_decision": {
            "guarded_execution_intent_ready": "transition_precheck_admit_candidate",
            "guarded_execution_intent_hold": "transition_precheck_hold_candidate",
            "guarded_execution_intent_block": "transition_precheck_block_candidate",
        }[status],
        "intent_count": len(intents) if bad_count else count,
        "envelope_count": count,
        "guarded_execution_intents": intents,
        "process_tensor_context": context,
        "source_guarded_execution_intent_packet_digest": "packet-digest-v13-22",
        "prev_record_digest": "GENESIS",
        "record_digest": f"receipt-digest-{kind}",
        "boundary": boundary,
        "epoch": 1,
    }


def run_bridge(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]):
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_guarded_execution_intent_receipt_ledger.jsonl", record)
    out = build_physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge(
        runtime_context=bridge_context(runtime),
        v12_5_receipt_to_v12_6_executor_readiness_bridge_license=license_packet,
    ).to_dict()
    state = load_json(runtime / "physical_quantum_qi_v13_9_transition_executor_bridge_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v12_5_receipt_to_v12_6_executor_readiness_bridge_ledger.jsonl")
    return runtime, out, state, ledger


def assert_ready(label: str, out: dict[str, Any], state: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_5_RECEIPT_TO_V12_6_EXECUTOR_READINESS_BRIDGE_READY", (label, out)
    assert out["readiness_state_written"] is True
    assert out["bridge_ledger_appended"] is True
    assert not out["blockers"]
    assert state["boundary"]["can_feed_v13_9_v12_5_to_v12_6_transition_executor_bridge"] is True
    assert state["boundary"]["does_not_run_v12_6_executor"] is True
    assert ledger[-1]["boundary"]["v13_9_transition_executor_bridge_ready_state_traceable"] is True


def assert_v13_9_accepts(runtime: pathlib.Path, label: str, expected: str) -> None:
    out = build_physical_quantum_qi_v12_5_to_v12_6_transition_executor_bridge(
        runtime_context=v13_9_context(runtime),
        v12_5_to_v12_6_transition_executor_bridge_license=v13_9_license(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V12_5_TO_V12_6_TRANSITION_EXECUTOR_BRIDGE_READY", (label, out)
    assert out["expected_v12_6_execution_status"] == expected
    assert out["executor_ready_state_written"] is True
    assert out["bridge_ledger_appended"] is True


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        for kind in ("ready", "hold", "block"):
            runtime, out, state, ledger = run_bridge(root, kind, receipt(kind), bridge_license())
            assert_ready(kind, out, state, ledger)
            _, expected, _, _ = parts(kind)
            assert_v13_9_accepts(runtime, kind, expected)

        runtime, out, state, ledger = run_bridge(root, "chain", receipt("ready"), bridge_license())
        assert_ready("chain1", out, state, ledger)
        runtime, out, state, ledger = run_bridge(root, "chain", receipt("hold"), bridge_license())
        assert_ready("chain2", out, state, ledger)
        assert len(ledger) == 2
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        cases = (
            ("bad_boundary", receipt("ready", bad_boundary=True), "v12_5_guarded_execution_intent_receipt_boundary_receipt_does_not_mutate_intent_packet_missing"),
            ("bad_count", receipt("ready", bad_count=True), "v13_22_ready_without_intents"),
            ("missing_context", receipt("ready", missing_context=True), "process_tensor_context_process_tensor_digest_missing"),
            ("bad_weight", receipt("ready", bad_weight=True), "v13_22_intent_0_weighting_not_executable"),
        )
        for name, record, error in cases:
            _, out, state, ledger = run_bridge(root, name, record, bridge_license())
            assert out["status"].endswith("BLOCKED")
            assert error in out["blockers"]
            assert state == {}
            assert ledger == []

        _, out, state, ledger = run_bridge(root, "missing", None, bridge_license())
        assert "v12_5_guarded_execution_intent_receipt_ledger_missing" in out["blockers"]
        assert state == {}
        assert ledger == []

        _, out, state, ledger = run_bridge(root, "license", receipt("ready"), bridge_license(v13_9_bridge_ready_state_write_allowed=False))
        assert "v13_9_bridge_ready_state_write_not_allowed" in out["blockers"]
        assert state == {}
        assert ledger == []

    print("physical_quantum_qi_v13_22_readiness_bridge checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
