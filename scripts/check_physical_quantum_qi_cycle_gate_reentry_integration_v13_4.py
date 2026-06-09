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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_v13_4 import build_physical_quantum_qi_cycle_gate_reentry_integration

PT = {
    "process_tensor_digest": "pt-digest-v13-4",
    "memory_kernel_digest": "memory-kernel-digest-v13-4",
    "history_window_digest": "history-window-digest-v13-4",
    "instrument_trace_digest": "instrument-trace-digest-v13-4",
    "non_markov_context_digest": "non-markov-context-digest-v13-4",
}
BOUNDARY = {
    "receipt_ledger_only": True,
    "candidate_weighting_cycle_handoff_receipt_only": True,
    "cycle_gate_input_traceable": True,
    "admissible_candidate_set_seed_traceable": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "handoff_not_direct_execution": True,
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
        "physical_quantum_qi_cycle_gate_reentry_integration_enabled": True,
        "apply_physical_quantum_qi_cycle_gate_reentry_integration": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_LICENSE_READY",
        "candidate_weighting_cycle_handoff_receipt_ledger_read_allowed": True,
        "integration_packet_write_allowed": True,
        "integrated_cycle_gate_state_write_allowed": True,
        "integrated_admissible_candidate_set_write_allowed": True,
        "integration_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(status: str, *, bad_boundary: bool = False, bad_gate: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    if status == "candidate_weighting_cycle_handoff_reinforce":
        gate = "reweight_candidate"
        seed = "reinforce_admissible_candidate_seed"
        weighting = {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
        if bad_weight:
            weighting["path_weight_delta"] = 0
    elif status == "candidate_weighting_cycle_handoff_probe":
        gate = "hold_candidate"
        seed = "probe_candidate_seed"
        weighting = {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        if bad_weight:
            weighting["barrier_potential_required"] = True
    else:
        gate = "block_candidate"
        seed = "barrier_candidate_seed"
        weighting = {
            "path_weight_delta": 0,
            "probe_potential_required": False,
            "barrier_potential_required": True,
            "barrier_blocks_ready_weight": True,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
        if bad_weight:
            weighting["barrier_blocks_ready_weight"] = False
    if bad_gate:
        gate = "invalid_gate"
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["cycle_gate_input_traceable"] = False
    context = dict(PT)
    if missing_context:
        context["instrument_trace_digest"] = ""
    return {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_record_v13_3",
        "record_type": "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt",
        "handoff_status": status,
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_candidate_weighting_cycle_handoff_digest": "handoff-digest-v13-4",
        "source_closed_loop_reentry_receipt_digest": "closed-loop-reentry-receipt-digest-v13-4",
        "source_closed_loop_path_integral_reentry_digest": "closed-loop-reentry-digest-v13-4",
        "prev_record_digest": "GENESIS",
        "record_digest": f"handoff-receipt-{status}",
        "boundary": boundary,
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_cycle_gate_reentry_integration(
        runtime_context=ctx(runtime),
        cycle_gate_reentry_integration_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json")
    cycle = load_json(runtime / "physical_quantum_qi_integrated_cycle_gate_state.json")
    candidate_set = load_json(runtime / "physical_quantum_qi_integrated_admissible_candidate_set.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_ledger.jsonl")
    return result.to_dict(), packet, cycle, candidate_set, ledger


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any], cycle: dict[str, Any], candidate_set: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_READY", label
    assert out["integration_packet_written"] is True, label
    assert out["integrated_cycle_gate_state_written"] is True, label
    assert out["integrated_admissible_candidate_set_written"] is True, label
    assert out["integration_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["cycle_gate_reentry_integration_only"] is True, label
    assert packet["boundary"]["integrates_cycle_gate"] is True, label
    assert packet["boundary"]["integrates_admissible_candidate_set"] is True, label
    assert cycle["boundary"]["from_candidate_weighting_cycle_handoff_receipt"] is True, label
    assert candidate_set["boundary"]["from_candidate_weighting_cycle_handoff_receipt"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("candidate_weighting_cycle_handoff_reinforce", "cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1),
            ("candidate_weighting_cycle_handoff_probe", "cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1),
            ("candidate_weighting_cycle_handoff_barrier", "cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0),
        ]
        for status, integration, gate, aset, count in cases:
            out, packet, cycle, candidate_set, ledger = run(root, status, receipt(status), lic())
            assert_ready(status, out, packet, cycle, candidate_set, ledger)
            assert out["integration_status"] == integration
            assert out["integrated_cycle_gate_status"] == gate
            assert out["integrated_admissible_candidate_set_status"] == aset
            assert candidate_set["admissible_candidate_count"] == count

        out, packet, cycle, candidate_set, ledger = run(root, "chain", receipt("candidate_weighting_cycle_handoff_reinforce"), lic())
        assert_ready("chain_1", out, packet, cycle, candidate_set, ledger)
        out, packet, cycle, candidate_set, ledger = run(root, "chain", receipt("candidate_weighting_cycle_handoff_probe"), lic())
        assert_ready("chain_2", out, packet, cycle, candidate_set, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, packet, cycle, candidate_set, ledger = run(root, "bad_boundary", receipt("candidate_weighting_cycle_handoff_reinforce", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_boundary_cycle_gate_input_traceable_missing" in out["blockers"]
        assert packet == {}
        assert cycle == {}
        assert candidate_set == {}
        assert ledger == []

        out, packet, cycle, candidate_set, ledger = run(root, "bad_gate", receipt("candidate_weighting_cycle_handoff_probe", bad_gate=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_gate_decision_mismatch" in out["blockers"]
        assert packet == {}

        out, packet, cycle, candidate_set, ledger = run(root, "bad_weight", receipt("candidate_weighting_cycle_handoff_barrier", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "integration_barrier_without_blocking_barrier" in out["blockers"]
        assert packet == {}

        out, packet, cycle, candidate_set, ledger = run(root, "missing_context", receipt("candidate_weighting_cycle_handoff_reinforce", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "process_tensor_context_instrument_trace_digest_missing" in out["blockers"]
        assert packet == {}

        out, packet, cycle, candidate_set, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "candidate_weighting_cycle_handoff_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet, cycle, candidate_set, ledger = run(root, "license", receipt("candidate_weighting_cycle_handoff_probe"), lic(integrated_admissible_candidate_set_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_BLOCKED"
        assert "integrated_admissible_candidate_set_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_cycle_gate_reentry_integration_v13_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
