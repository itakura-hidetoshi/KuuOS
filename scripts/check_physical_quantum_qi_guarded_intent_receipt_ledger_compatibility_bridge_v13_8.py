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

PT = {
    "process_tensor_digest": "pt-digest-v13-8",
    "memory_kernel_digest": "memory-kernel-digest-v13-8",
    "history_window_digest": "history-window-digest-v13-8",
    "instrument_trace_digest": "instrument-trace-digest-v13-8",
    "non_markov_context_digest": "non-markov-context-digest-v13-8",
}
BOUNDARY = {
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
        "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_enabled": True,
        "apply_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_LICENSE_READY",
        "guarded_intent_bridge_receipt_ledger_read_allowed": True,
        "v12_5_guarded_execution_intent_packet_write_allowed": True,
        "compatibility_bridge_state_write_allowed": True,
        "compatibility_bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v12_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_guarded_execution_intent_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_guarded_execution_intent_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v12_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_LICENSE_READY",
        "guarded_execution_intent_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def status_parts(kind: str) -> tuple[str, str, str, int, dict[str, Any]]:
    if kind == "ready":
        return "integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", "emit_guarded_ready_intent", 1, {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "hold":
        return "integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", "emit_guarded_hold_intent", 0, {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0, {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def intent_items(count: int, weight: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx in range(count):
        out.append({
            "intent_index": idx,
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "candidate_id": f"compat-candidate-{idx}",
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": dict(weight),
            "process_tensor_context": dict(PT),
            "source_integrated_candidate_digest": f"candidate-digest-{idx}",
            "source_cycle_gate_reentry_integration_receipt_digest": "integration-receipt-digest-v13-8",
            "boundary": {
                "guarded_execution_intent_only": True,
                "execution_layer_entrypoint": True,
                "no_dry_run_required": True,
                "requires_guarded_execution_license": True,
                "intent_not_world_mutation": True,
                "does_not_start_next_cycle": True,
                "does_not_mutate_external_state": True,
                "does_not_consume_memory": True,
                "does_not_promote_truth": True,
            },
            "guarded_execution_intent_digest": f"guarded-intent-digest-{idx}",
        })
    return out


def receipt(kind: str, *, bad_boundary: bool = False, bad_bridge: bool = False, bad_weight: bool = False, bad_count: bool = False, missing_context: bool = False) -> dict[str, Any]:
    bridge, guarded, emit, count, weight = status_parts(kind)
    if bad_weight:
        if kind == "ready":
            weight["path_weight_delta"] = 0
        elif kind == "hold":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    if bad_count:
        count = 0 if kind == "ready" else 1
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["guarded_execution_intent_packet_traceable"] = False
    context = dict(PT)
    if missing_context:
        context["history_window_digest"] = ""
    return {
        "version": "physical_quantum_qi_guarded_intent_bridge_receipt_record_v13_7",
        "record_type": "physical_quantum_qi_guarded_intent_bridge_receipt",
        "bridge_status": "wrong_bridge" if bad_bridge else bridge,
        "guarded_execution_intent_status": guarded,
        "guarded_intent_emit_action": emit,
        "guarded_execution_intent_count": count,
        "guarded_execution_intents": intent_items(count, weight),
        "candidate_weighting": weight,
        "process_tensor_context": context,
        "source_integrated_candidate_to_guarded_intent_bridge_digest": "bridge-digest-v13-8",
        "source_guarded_execution_intent_packet_digest": "guarded-intent-packet-digest-v13-8",
        "source_cycle_gate_reentry_integration_receipt_digest": "integration-receipt-digest-v13-8",
        "source_cycle_gate_reentry_integration_digest": "integration-digest-v13-8",
        "prev_record_digest": "GENESIS",
        "record_digest": f"guarded-intent-bridge-receipt-{kind}",
        "boundary": boundary,
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge(
        runtime_context=ctx(runtime),
        guarded_intent_receipt_ledger_compatibility_bridge_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_guarded_execution_intent_packet.json")
    state = load_json(runtime / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_ledger.jsonl")
    return result.to_dict(), packet, state, ledger


def assert_ready_and_v12(label: str, runtime: pathlib.Path, out: dict[str, Any], packet: dict[str, Any], state: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_READY", label
    assert out["v12_5_packet_written"] is True, label
    assert out["compatibility_state_written"] is True, label
    assert out["compatibility_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert packet["physical_quantum_qi_guarded_execution_intent_considered"] is True, label
    assert packet["boundary"]["transition_candidate_envelope_required"] is True, label
    assert state["boundary"]["can_feed_v12_5_guarded_execution_intent_receipt_ledger"] is True, label
    assert ledger[-1]["boundary"]["target_v12_5_packet_traceable"] is True, label
    v12 = build_physical_quantum_qi_guarded_execution_intent_receipt_ledger(
        runtime_context=v12_ctx(runtime),
        guarded_execution_intent_receipt_ledger_license=v12_lic(),
    ).to_dict()
    assert v12["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_EXECUTION_INTENT_RECEIPT_LEDGER_READY", (label, v12)
    assert v12["ledger_appended"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind, expected, count in [
            ("ready", "guarded_execution_intent_ready", 1),
            ("hold", "guarded_execution_intent_hold", 0),
            ("block", "guarded_execution_intent_block", 0),
        ]:
            runtime = root / kind
            out, packet, state, ledger = run(root, kind, receipt(kind), lic())
            assert_ready_and_v12(kind, runtime, out, packet, state, ledger)
            assert out["execution_intent_status"] == expected
            assert out["intent_count"] == count

        out, packet, state, ledger = run(root, "chain", receipt("ready"), lic())
        assert_ready_and_v12("chain_1", root / "chain", out, packet, state, ledger)
        out, packet, state, ledger = run(root, "chain", receipt("hold"), lic())
        assert_ready_and_v12("chain_2", root / "chain", out, packet, state, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, packet, state, ledger = run(root, "bad_boundary", receipt("ready", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "guarded_intent_bridge_receipt_boundary_guarded_execution_intent_packet_traceable_missing" in out["blockers"]
        assert packet == {}
        assert ledger == []

        out, packet, state, ledger = run(root, "bad_bridge", receipt("hold", bad_bridge=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "guarded_intent_bridge_status_mismatch" in out["blockers"]
        assert packet == {}

        out, packet, state, ledger = run(root, "bad_weight", receipt("block", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "v12_5_compat_block_weighting_invalid" in out["blockers"]
        assert packet == {}

        out, packet, state, ledger = run(root, "bad_count", receipt("ready", bad_count=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "v12_5_compat_ready_requires_intent" in out["blockers"]
        assert packet == {}

        out, packet, state, ledger = run(root, "missing_context", receipt("ready", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "process_tensor_context_history_window_digest_missing" in out["blockers"]
        assert packet == {}

        out, packet, state, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "guarded_intent_bridge_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet, state, ledger = run(root, "license", receipt("ready"), lic(v12_5_guarded_execution_intent_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_RECEIPT_LEDGER_COMPATIBILITY_BRIDGE_BLOCKED"
        assert "v12_5_guarded_execution_intent_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_guarded_intent_receipt_ledger_compatibility_bridge_v13_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
