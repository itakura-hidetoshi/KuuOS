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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_v11_5 import build_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger

GATE_BOUNDARY = {
    "memory_kernel_consistency_gate_only": True,
    "history_bearing_process_tensor": True,
    "non_markov_context_required": True,
    "multi_time_window_required": True,
    "finite_horizon_only": True,
    "memory_kernel_visible": True,
    "does_not_execute_path": True,
    "does_not_run_runner": True,
    "does_not_start_next_cycle": True,
    "does_not_commit_plan": True,
    "does_not_consume_memory": True,
    "does_not_authorize_execution": True,
    "does_not_select_final_path": True,
    "does_not_promote_truth": True,
    "candidate_weighting_not_truth": True,
    "admissible_set_not_execution_set": True,
    "gate_does_not_mutate_candidate_set_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-5",
    "memory_kernel_digest": "memory-kernel-digest-v11-5",
    "history_window_digest": "history-window-digest-v11-5",
    "instrument_trace_digest": "instrument-trace-digest-v11-5",
    "non_markov_context_digest": "non-markov-context-digest-v11-5",
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_LICENSE_READY",
        "memory_kernel_consistency_gate_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def candidate(kind: str, idx: int, *, mismatch: bool = False) -> dict[str, Any]:
    decision = {"admitted_candidates": "admit_candidate", "probe_candidates": "hold_candidate", "blocked_candidates": "block_candidate"}[kind]
    consistency = {"admitted_candidates": "memory_consistent_admit", "probe_candidates": "memory_consistent_probe", "blocked_candidates": "memory_consistent_block"}[kind]
    weighting = {
        "admitted_candidates": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe_candidates": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked_candidates": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[kind]
    item_pt = dict(PT)
    if mismatch:
        item_pt["history_window_digest"] = "mismatch"
    return {
        "candidate_id": f"candidate-{kind}-{idx}",
        "gate_receipt_digest": f"gate-receipt-{kind}-{idx}",
        "cycle_gate_decision": decision,
        "memory_kernel_consistency_decision": consistency,
        "candidate_weighting": weighting,
        "process_tensor_context": item_pt,
    }


def gate_packet(decision: str) -> dict[str, Any]:
    admitted = 1 if decision == "memory_kernel_consistency_admit" else 0
    probe = 2 if decision == "memory_kernel_consistency_hold" else 0
    blocked = 1 if decision == "memory_kernel_consistency_block" else 0
    packet = {
        "version": "physical_quantum_qi_memory_kernel_consistency_gate_packet_v11_4",
        "physical_quantum_qi_memory_kernel_consistency_gate_considered": True,
        "memory_kernel_consistency_gate_decision": decision,
        "counts": {"admitted": admitted, "probe": probe, "blocked": blocked},
        "process_tensor_context": dict(PT),
        "admitted_candidates": [candidate("admitted_candidates", i) for i in range(admitted)],
        "probe_candidates": [candidate("probe_candidates", i) for i in range(probe)],
        "blocked_candidates": [candidate("blocked_candidates", i) for i in range(blocked)],
        "source_digests": {
            "process_tensor_candidate_set_receipt": "candidate-set-receipt-digest-v11-5",
            "process_tensor_admissible_candidate_set": "candidate-set-digest-v11-5",
        },
        "boundary": dict(GATE_BOUNDARY),
        "epoch": 1,
    }
    packet["memory_kernel_consistency_gate_digest"] = f"memory-kernel-consistency-gate-digest-{decision}"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_memory_kernel_consistency_gate_packet.json", packet)
    result = build_physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger(
        runtime_context=ctx(runtime),
        memory_kernel_consistency_gate_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["memory_kernel_consistency_gate_receipt_only"] is True, label
    assert latest["boundary"]["history_bearing_process_tensor"] is True, label
    assert latest["boundary"]["non_markov_context_required"] is True, label
    assert latest["boundary"]["does_not_start_next_cycle"] is True, label
    assert latest["boundary"]["does_not_authorize_execution"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "admit", gate_packet("memory_kernel_consistency_admit"), lic())
        assert_ready("admit", out, ledger)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_admit"
        assert out["admitted_count"] == 1
        assert ledger[-1]["process_tensor_context"]["memory_kernel_digest"] == "memory-kernel-digest-v11-5"

        out, ledger = run(root, "hold", gate_packet("memory_kernel_consistency_hold"), lic())
        assert_ready("hold", out, ledger)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_hold"
        assert out["probe_count"] == 2

        out, ledger = run(root, "block", gate_packet("memory_kernel_consistency_block"), lic())
        assert_ready("block", out, ledger)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_block"
        assert out["blocked_count"] == 1

        out, ledger = run(root, "chain", gate_packet("memory_kernel_consistency_admit"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", gate_packet("memory_kernel_consistency_hold"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_decision = gate_packet("memory_kernel_consistency_hold")
        bad_decision["admitted_candidates"] = [candidate("admitted_candidates", 0)]
        bad_decision["counts"]["admitted"] = 1
        out, ledger = run(root, "bad_decision", bad_decision, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "hold_decision_with_admitted_candidates" in out["blockers"]
        assert ledger == []

        mismatch = gate_packet("memory_kernel_consistency_admit")
        mismatch["admitted_candidates"][0] = candidate("admitted_candidates", 0, mismatch=True)
        out, ledger = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "admitted_candidates_0_history_window_digest_mismatch" in out["blockers"]
        assert ledger == []

        bad_boundary = gate_packet("memory_kernel_consistency_admit")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "memory_kernel_consistency_gate_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "memory_kernel_consistency_gate_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", gate_packet("memory_kernel_consistency_admit"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger_v11_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
