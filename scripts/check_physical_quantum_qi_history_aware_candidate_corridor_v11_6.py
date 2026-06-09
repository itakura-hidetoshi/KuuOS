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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_history_aware_candidate_corridor_v11_6 import build_physical_quantum_qi_history_aware_candidate_corridor

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "memory_kernel_consistency_gate_receipt_only": True,
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
    "receipt_does_not_mutate_gate_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-6",
    "memory_kernel_digest": "memory-kernel-digest-v11-6",
    "history_window_digest": "history-window-digest-v11-6",
    "instrument_trace_digest": "instrument-trace-digest-v11-6",
    "non_markov_context_digest": "non-markov-context-digest-v11-6",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_history_aware_candidate_corridor_enabled": True,
        "apply_physical_quantum_qi_history_aware_candidate_corridor": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_LICENSE_READY",
        "memory_kernel_consistency_gate_receipt_ledger_read_allowed": True,
        "history_aware_candidate_corridor_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def candidate(kind: str, idx: int, *, mismatch: bool = False) -> dict[str, Any]:
    consistency = {"admitted_candidates": "memory_consistent_admit", "probe_candidates": "memory_consistent_probe", "blocked_candidates": "memory_consistent_block"}[kind]
    cycle = {"admitted_candidates": "admit_candidate", "probe_candidates": "hold_candidate", "blocked_candidates": "block_candidate"}[kind]
    weighting = {
        "admitted_candidates": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe_candidates": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked_candidates": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[kind]
    item_pt = dict(PT)
    if mismatch:
        item_pt["instrument_trace_digest"] = "mismatch"
    return {
        "candidate_id": f"candidate-{kind}-{idx}",
        "gate_receipt_digest": f"gate-receipt-{kind}-{idx}",
        "cycle_gate_decision": cycle,
        "memory_kernel_consistency_decision": consistency,
        "candidate_weighting": weighting,
        "process_tensor_context": item_pt,
    }


def receipt(decision: str) -> dict[str, Any]:
    admitted = 1 if decision == "memory_kernel_consistency_admit" else 0
    probe = 2 if decision == "memory_kernel_consistency_hold" else 0
    blocked = 1 if decision == "memory_kernel_consistency_block" else 0
    return {
        "version": "physical_quantum_qi_memory_kernel_consistency_gate_receipt_record_v11_5",
        "record_type": "physical_quantum_qi_memory_kernel_consistency_gate_receipt",
        "memory_kernel_consistency_gate_decision": decision,
        "counts": {"admitted": admitted, "probe": probe, "blocked": blocked},
        "admitted_candidates": [candidate("admitted_candidates", i) for i in range(admitted)],
        "probe_candidates": [candidate("probe_candidates", i) for i in range(probe)],
        "blocked_candidates": [candidate("blocked_candidates", i) for i in range(blocked)],
        "process_tensor_context": dict(PT),
        "source_memory_kernel_consistency_gate_digest": "mk-gate-digest-v11-6",
        "source_process_tensor_candidate_set_receipt_digest": "candidate-set-receipt-digest-v11-6",
        "source_process_tensor_admissible_candidate_set_digest": "candidate-set-digest-v11-6",
        "prev_record_digest": "GENESIS",
        "record_digest": f"mk-gate-receipt-{decision}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_memory_kernel_consistency_gate_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_history_aware_candidate_corridor(
        runtime_context=ctx(runtime),
        history_aware_candidate_corridor_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_history_aware_candidate_corridor.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_READY", label
    assert out["corridor_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["history_aware_candidate_corridor_only"] is True, label
    assert packet["boundary"]["corridor_build_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["does_not_select_final_path"] is True, label
    assert packet["boundary"]["corridor_not_execution_path"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "admit", receipt("memory_kernel_consistency_admit"), lic())
        assert_ready("admit", out, packet)
        assert out["corridor_status"] == "history_aware_admissible_corridor"
        assert out["admitted_count"] == 1
        assert packet["corridor_segments"][0]["corridor_lane"] == "admit_lane"

        out, packet = run(root, "hold", receipt("memory_kernel_consistency_hold"), lic())
        assert_ready("hold", out, packet)
        assert out["corridor_status"] == "history_aware_probe_corridor"
        assert out["probe_count"] == 2
        assert packet["corridor_segments"][0]["corridor_lane"] == "probe_lane"

        out, packet = run(root, "block", receipt("memory_kernel_consistency_block"), lic())
        assert_ready("block", out, packet)
        assert out["corridor_status"] == "history_aware_blocked_corridor"
        assert out["blocked_count"] == 1

        mismatch = receipt("memory_kernel_consistency_admit")
        mismatch["admitted_candidates"][0] = candidate("admitted_candidates", 0, mismatch=True)
        out, packet = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
        assert "admitted_candidates_0_instrument_trace_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_hold = receipt("memory_kernel_consistency_hold")
        bad_hold["admitted_candidates"] = [candidate("admitted_candidates", 0)]
        bad_hold["counts"]["admitted"] = 1
        out, packet = run(root, "bad_hold", bad_hold, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
        assert "hold_corridor_requires_probe_only_candidates" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("memory_kernel_consistency_admit")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
        assert "memory_kernel_consistency_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
        assert "memory_kernel_consistency_gate_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("memory_kernel_consistency_admit"), lic(history_aware_candidate_corridor_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_BLOCKED"
        assert "history_aware_candidate_corridor_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_history_aware_candidate_corridor_v11_6 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
