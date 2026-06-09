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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6 import build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-6",
    "memory_kernel_digest": "memory-kernel-digest-v13-6",
    "history_window_digest": "history-window-digest-v13-6",
    "instrument_trace_digest": "instrument-trace-digest-v13-6",
    "non_markov_context_digest": "non-markov-context-digest-v13-6",
}
BOUNDARY = {
    "receipt_ledger_only": True,
    "cycle_gate_reentry_integration_receipt_only": True,
    "integrated_cycle_gate_state_traceable": True,
    "integrated_admissible_candidate_set_traceable": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "integration_not_direct_execution": True,
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
        "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_enabled": True,
        "apply_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_LICENSE_READY",
        "cycle_gate_reentry_integration_receipt_ledger_read_allowed": True,
        "bridge_packet_write_allowed": True,
        "guarded_execution_intent_packet_write_allowed": True,
        "bridge_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(status: str, *, bad_boundary: bool = False, bad_gate: bool = False, bad_weight: bool = False, missing_context: bool = False, bad_count: bool = False) -> dict[str, Any]:
    if status == "cycle_gate_reentry_integration_admit":
        gate = "integrated_cycle_gate_admit"
        aset = "integrated_admissible_candidate_set_admit"
        count = 1
        weight = {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
        candidates = [{"candidate_id": "closed_loop_reentry_reinforced_candidate", "candidate_mode": "admit_candidate", "candidate_weighting": weight, "process_tensor_context": dict(PT), "admissibility_status": "admissible_candidate_ready", "candidate_digest": "admit-candidate-digest-v13-6"}]
        if bad_weight:
            weight["path_weight_delta"] = 0
    elif status == "cycle_gate_reentry_integration_hold":
        gate = "integrated_cycle_gate_hold"
        aset = "integrated_admissible_candidate_set_probe"
        count = 1
        weight = {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        candidates = [{"candidate_id": "closed_loop_reentry_probe_candidate", "candidate_mode": "probe_candidate", "candidate_weighting": weight, "process_tensor_context": dict(PT), "admissibility_status": "admissible_candidate_probe_required", "candidate_digest": "probe-candidate-digest-v13-6"}]
        if bad_weight:
            weight["barrier_potential_required"] = True
    else:
        gate = "integrated_cycle_gate_block"
        aset = "integrated_admissible_candidate_set_block"
        count = 0
        weight = {
            "path_weight_delta": 0,
            "probe_potential_required": False,
            "barrier_potential_required": True,
            "barrier_blocks_ready_weight": True,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        candidates = []
        if bad_weight:
            weight["barrier_blocks_ready_weight"] = False
    if bad_gate:
        gate = "invalid_gate"
    if bad_count:
        count = 0 if status != "cycle_gate_reentry_integration_block" else 1
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["integrated_admissible_candidate_set_traceable"] = False
    context = dict(PT)
    if missing_context:
        context["process_tensor_digest"] = ""
    return {
        "version": "physical_quantum_qi_cycle_gate_reentry_integration_receipt_record_v13_5",
        "record_type": "physical_quantum_qi_cycle_gate_reentry_integration_receipt",
        "integration_status": status,
        "integrated_cycle_gate_status": gate,
        "integrated_admissible_candidate_set_status": aset,
        "admissible_candidate_count": count,
        "candidate_weighting": weight,
        "integrated_candidates": candidates,
        "process_tensor_context": context,
        "source_cycle_gate_reentry_integration_digest": "cycle-gate-reentry-integration-digest-v13-6",
        "source_candidate_weighting_cycle_handoff_receipt_digest": "handoff-receipt-digest-v13-6",
        "source_candidate_weighting_cycle_handoff_digest": "handoff-digest-v13-6",
        "prev_record_digest": "GENESIS",
        "record_digest": f"integration-receipt-{status}",
        "boundary": boundary,
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge(
        runtime_context=ctx(runtime),
        integrated_candidate_to_guarded_intent_bridge_license=license_packet,
    )
    bridge = load_json(runtime / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json")
    intent = load_json(runtime / "physical_quantum_qi_guarded_execution_intent_packet.json")
    state = load_json(runtime / "physical_quantum_qi_guarded_execution_intent_bridge_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_ledger.jsonl")
    return result.to_dict(), bridge, intent, state, ledger


def assert_ready(label: str, out: dict[str, Any], bridge: dict[str, Any], intent: dict[str, Any], state: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_READY", label
    assert out["bridge_packet_written"] is True, label
    assert out["guarded_execution_intent_packet_written"] is True, label
    assert out["bridge_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert bridge["boundary"]["emits_guarded_execution_intent_packet"] is True, label
    assert bridge["boundary"]["bridge_not_direct_execution"] is True, label
    assert intent["boundary"]["guarded_execution_intent_packet_only"] is True, label
    assert state["boundary"]["can_feed_guarded_execution_intent_receipt_layer"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("cycle_gate_reentry_integration_admit", "integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", 1),
            ("cycle_gate_reentry_integration_hold", "integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", 0),
            ("cycle_gate_reentry_integration_block", "integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", 0),
        ]
        for status, bridge_status, guarded_status, count in cases:
            out, bridge, intent, state, ledger = run(root, status, receipt(status), lic())
            assert_ready(status, out, bridge, intent, state, ledger)
            assert out["bridge_status"] == bridge_status
            assert out["guarded_execution_intent_status"] == guarded_status
            assert out["guarded_execution_intent_count"] == count
            assert intent["guarded_execution_intent_count"] == count

        out, bridge, intent, state, ledger = run(root, "chain", receipt("cycle_gate_reentry_integration_admit"), lic())
        assert_ready("chain_1", out, bridge, intent, state, ledger)
        out, bridge, intent, state, ledger = run(root, "chain", receipt("cycle_gate_reentry_integration_hold"), lic())
        assert_ready("chain_2", out, bridge, intent, state, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, bridge, intent, state, ledger = run(root, "bad_boundary", receipt("cycle_gate_reentry_integration_admit", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_receipt_boundary_integrated_admissible_candidate_set_traceable_missing" in out["blockers"]
        assert bridge == {}
        assert intent == {}
        assert state == {}
        assert ledger == []

        out, bridge, intent, state, ledger = run(root, "bad_gate", receipt("cycle_gate_reentry_integration_hold", bad_gate=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_receipt_gate_status_mismatch" in out["blockers"]
        assert bridge == {}

        out, bridge, intent, state, ledger = run(root, "bad_weight", receipt("cycle_gate_reentry_integration_block", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "guarded_intent_block_without_blocking_barrier" in out["blockers"]
        assert bridge == {}

        out, bridge, intent, state, ledger = run(root, "bad_count", receipt("cycle_gate_reentry_integration_admit", bad_count=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "guarded_intent_bridge_requires_candidate_for_admit_or_hold" in out["blockers"]
        assert bridge == {}

        out, bridge, intent, state, ledger = run(root, "missing_context", receipt("cycle_gate_reentry_integration_admit", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "process_tensor_context_process_tensor_digest_missing" in out["blockers"]
        assert bridge == {}

        out, bridge, intent, state, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "cycle_gate_reentry_integration_receipt_ledger_missing" in out["blockers"]
        assert bridge == {}

        out, bridge, intent, state, ledger = run(root, "license", receipt("cycle_gate_reentry_integration_hold"), lic(guarded_execution_intent_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_INTEGRATED_CANDIDATE_TO_GUARDED_INTENT_BRIDGE_BLOCKED"
        assert "guarded_execution_intent_packet_write_not_allowed" in out["blockers"]
        assert bridge == {}

    print("physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_v13_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
