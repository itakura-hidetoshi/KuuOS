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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_memory_kernel_consistency_gate_v11_4 import build_physical_quantum_qi_memory_kernel_consistency_gate

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "process_tensor_candidate_set_receipt_only": True,
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
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-4",
    "memory_kernel_digest": "memory-kernel-digest-v11-4",
    "history_window_digest": "history-window-digest-v11-4",
    "instrument_trace_digest": "instrument-trace-digest-v11-4",
    "non_markov_context_digest": "non-markov-context-digest-v11-4",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_memory_kernel_consistency_gate_enabled": True,
        "apply_physical_quantum_qi_memory_kernel_consistency_gate": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_LICENSE_READY",
        "candidate_set_receipt_ledger_read_allowed": True,
        "memory_kernel_consistency_gate_packet_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def candidate(kind: str, idx: int, *, mismatch_key: str | None = None) -> dict[str, Any]:
    decision = {"admitted_candidates": "admit_candidate", "probe_candidates": "hold_candidate", "blocked_candidates": "block_candidate"}[kind]
    status = {"admitted_candidates": "weighted_candidate", "probe_candidates": "probe_only_candidate", "blocked_candidates": "blocked_candidate"}[kind]
    weighting = {
        "admitted_candidates": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe_candidates": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked_candidates": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[kind]
    item_pt = dict(PT)
    if mismatch_key is not None:
        item_pt[mismatch_key] = "mismatch"
    return {
        "candidate_id": f"candidate-{kind}-{idx}",
        "gate_receipt_digest": f"gate-receipt-{kind}-{idx}",
        "cycle_gate_decision": decision,
        "source_candidate_status": status,
        "candidate_weighting": weighting,
        "process_tensor_context": item_pt,
    }


def receipt(*, admitted: int = 1, probe: int = 1, blocked: int = 1) -> dict[str, Any]:
    return {
        "version": "physical_quantum_qi_process_tensor_candidate_set_receipt_record_v11_3",
        "record_type": "physical_quantum_qi_process_tensor_candidate_set_receipt",
        "counts": {"admitted": admitted, "probe": probe, "blocked": blocked},
        "admitted_candidates": [candidate("admitted_candidates", i) for i in range(admitted)],
        "probe_candidates": [candidate("probe_candidates", i) for i in range(probe)],
        "blocked_candidates": [candidate("blocked_candidates", i) for i in range(blocked)],
        "process_tensor_context": dict(PT),
        "source_candidate_set_digest": "candidate-set-digest-v11-4",
        "prev_record_digest": "GENESIS",
        "record_digest": "candidate-set-receipt-digest-v11-4",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_process_tensor_candidate_set_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_memory_kernel_consistency_gate(
        runtime_context=ctx(runtime),
        memory_kernel_consistency_gate_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_memory_kernel_consistency_gate_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_READY", label
    assert out["gate_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["memory_kernel_consistency_gate_only"] is True, label
    assert packet["boundary"]["history_bearing_process_tensor"] is True, label
    assert packet["boundary"]["non_markov_context_required"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["does_not_select_final_path"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "mixed", receipt(admitted=1, probe=1, blocked=1), lic())
        assert_ready("mixed", out, packet)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_admit"
        assert out["admitted_consistent_count"] == 1
        assert packet["process_tensor_context"]["memory_kernel_digest"] == "memory-kernel-digest-v11-4"

        out, packet = run(root, "probe_only", receipt(admitted=0, probe=2, blocked=0), lic())
        assert_ready("probe_only", out, packet)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_hold"
        assert out["probe_consistent_count"] == 2

        out, packet = run(root, "blocked_only", receipt(admitted=0, probe=0, blocked=1), lic())
        assert_ready("blocked_only", out, packet)
        assert out["consistency_gate_decision"] == "memory_kernel_consistency_block"
        assert out["blocked_consistent_count"] == 1

        mismatch = receipt(admitted=1, probe=0, blocked=0)
        mismatch["admitted_candidates"][0] = candidate("admitted_candidates", 0, mismatch_key="memory_kernel_digest")
        out, packet = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
        assert "admitted_candidates_0_memory_kernel_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt(admitted=1, probe=0, blocked=0)
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
        assert "candidate_set_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        bad_count = receipt(admitted=1, probe=0, blocked=0)
        bad_count["counts"]["admitted"] = 2
        out, packet = run(root, "bad_count", bad_count, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
        assert "admitted_count_mismatch" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
        assert "process_tensor_candidate_set_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt(admitted=1, probe=0, blocked=0), lic(memory_kernel_consistency_gate_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_MEMORY_KERNEL_CONSISTENCY_GATE_BLOCKED"
        assert "memory_kernel_consistency_gate_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_memory_kernel_consistency_gate_v11_4 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
