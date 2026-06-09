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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_stable_corridor_transition_precheck_v12_0 import build_physical_quantum_qi_stable_corridor_transition_precheck

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "corridor_stability_gate_receipt_only": True,
    "stability_gate_receipt_only": True,
    "history_aware_candidate_corridor_only": True,
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
    "corridor_not_execution_path": True,
    "corridor_stability_not_execution_authority": True,
    "receipt_does_not_mutate_stability_gate_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-0",
    "memory_kernel_digest": "memory-kernel-digest-v12-0",
    "history_window_digest": "history-window-digest-v12-0",
    "instrument_trace_digest": "instrument-trace-digest-v12-0",
    "non_markov_context_digest": "non-markov-context-digest-v12-0",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_stable_corridor_transition_precheck_enabled": True,
        "apply_physical_quantum_qi_stable_corridor_transition_precheck": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_LICENSE_READY",
        "corridor_stability_gate_receipt_ledger_read_allowed": True,
        "stable_corridor_transition_precheck_packet_write_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def segment(lane: str, rank: int, *, mismatch: bool = False, bad_rank: bool = False) -> dict[str, Any]:
    consistency = {"admit_lane": "memory_consistent_admit", "probe_lane": "memory_consistent_probe", "blocked_lane": "memory_consistent_block"}[lane]
    cycle = {"admit_lane": "admit_candidate", "probe_lane": "hold_candidate", "blocked_lane": "block_candidate"}[lane]
    weighting = {
        "admit_lane": {"path_weight_delta": 3, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "probe_lane": {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False},
        "blocked_lane": {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True},
    }[lane]
    item_pt = dict(PT)
    if mismatch:
        item_pt["memory_kernel_digest"] = "mismatch"
    return {
        "corridor_lane": lane,
        "corridor_rank": rank + (1 if bad_rank else 0),
        "candidate_id": f"candidate-{lane}-{rank}",
        "gate_receipt_digest": f"gate-receipt-{lane}-{rank}",
        "cycle_gate_decision": cycle,
        "memory_kernel_consistency_decision": consistency,
        "candidate_weighting": weighting,
        "process_tensor_context": item_pt,
    }


def receipt(decision: str) -> dict[str, Any]:
    status = {
        "corridor_stability_admit": "history_aware_admissible_corridor",
        "corridor_stability_hold": "history_aware_probe_corridor",
        "corridor_stability_block": "history_aware_blocked_corridor",
    }[decision]
    admit = 1 if decision == "corridor_stability_admit" else 0
    probe = 2 if decision == "corridor_stability_hold" else 0
    blocked = 1 if decision == "corridor_stability_block" else 0
    segments = [segment("admit_lane", i) for i in range(admit)]
    segments += [segment("probe_lane", i) for i in range(probe)]
    segments += [segment("blocked_lane", i) for i in range(blocked)]
    return {
        "version": "physical_quantum_qi_corridor_stability_gate_receipt_record_v11_9",
        "record_type": "physical_quantum_qi_corridor_stability_gate_receipt",
        "corridor_stability_gate_decision": decision,
        "corridor_status": status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_corridor_stability_gate_digest": "corridor-stability-gate-digest-v12-0",
        "source_history_aware_candidate_corridor_receipt_digest": "corridor-receipt-digest-v12-0",
        "source_history_aware_candidate_corridor_digest": "corridor-digest-v12-0",
        "prev_record_digest": "GENESIS",
        "record_digest": f"corridor-stability-receipt-{decision}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_corridor_stability_gate_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_stable_corridor_transition_precheck(
        runtime_context=ctx(runtime),
        stable_corridor_transition_precheck_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_stable_corridor_transition_precheck_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_READY", label
    assert out["precheck_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["stable_corridor_transition_precheck_only"] is True, label
    assert packet["boundary"]["transition_precheck_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["does_not_select_final_path"] is True, label
    assert packet["boundary"]["transition_precheck_not_execution_authority"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "admit", receipt("corridor_stability_admit"), lic())
        assert_ready("admit", out, packet)
        assert out["transition_precheck_decision"] == "transition_precheck_admit_candidate"
        assert out["admitted_count"] == 1

        out, packet = run(root, "hold", receipt("corridor_stability_hold"), lic())
        assert_ready("hold", out, packet)
        assert out["transition_precheck_decision"] == "transition_precheck_hold_candidate"
        assert out["probe_count"] == 2

        out, packet = run(root, "block", receipt("corridor_stability_block"), lic())
        assert_ready("block", out, packet)
        assert out["transition_precheck_decision"] == "transition_precheck_block_candidate"
        assert out["blocked_count"] == 1

        bad_status = receipt("corridor_stability_hold")
        bad_status["corridor_status"] = "history_aware_admissible_corridor"
        out, packet = run(root, "bad_status", bad_status, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "corridor_status_stability_decision_mismatch" in out["blockers"]
        assert packet == {}

        mismatch = receipt("corridor_stability_admit")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, packet = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "admit_lane_segment_0_memory_kernel_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_rank = receipt("corridor_stability_admit")
        bad_rank["corridor_segments"][0] = segment("admit_lane", 0, bad_rank=True)
        out, packet = run(root, "bad_rank", bad_rank, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "admit_lane_segment_0_rank_mismatch" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("corridor_stability_admit")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "corridor_stability_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "corridor_stability_gate_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("corridor_stability_admit"), lic(stable_corridor_transition_precheck_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_BLOCKED"
        assert "stable_corridor_transition_precheck_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_stable_corridor_transition_precheck_v12_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
