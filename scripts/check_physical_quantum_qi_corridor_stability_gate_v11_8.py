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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_corridor_stability_gate_v11_8 import build_physical_quantum_qi_corridor_stability_gate

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "history_aware_candidate_corridor_receipt_only": True,
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
    "receipt_does_not_mutate_corridor_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-8",
    "memory_kernel_digest": "memory-kernel-digest-v11-8",
    "history_window_digest": "history-window-digest-v11-8",
    "instrument_trace_digest": "instrument-trace-digest-v11-8",
    "non_markov_context_digest": "non-markov-context-digest-v11-8",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_corridor_stability_gate_enabled": True,
        "apply_physical_quantum_qi_corridor_stability_gate": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_LICENSE_READY",
        "history_aware_candidate_corridor_receipt_ledger_read_allowed": True,
        "corridor_stability_gate_packet_write_allowed": True,
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
        item_pt["history_window_digest"] = "mismatch"
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


def receipt(status: str) -> dict[str, Any]:
    admit = 1 if status == "history_aware_admissible_corridor" else 0
    probe = 2 if status == "history_aware_probe_corridor" else 0
    blocked = 1 if status == "history_aware_blocked_corridor" else 0
    segments = [segment("admit_lane", i) for i in range(admit)]
    segments += [segment("probe_lane", i) for i in range(probe)]
    segments += [segment("blocked_lane", i) for i in range(blocked)]
    return {
        "version": "physical_quantum_qi_history_aware_candidate_corridor_receipt_record_v11_7",
        "record_type": "physical_quantum_qi_history_aware_candidate_corridor_receipt",
        "corridor_status": status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_history_aware_candidate_corridor_digest": "corridor-digest-v11-8",
        "source_memory_kernel_consistency_gate_receipt_digest": "mk-receipt-digest-v11-8",
        "source_memory_kernel_consistency_gate_digest": "mk-gate-digest-v11-8",
        "source_process_tensor_candidate_set_receipt_digest": "candidate-set-receipt-digest-v11-8",
        "source_process_tensor_admissible_candidate_set_digest": "candidate-set-digest-v11-8",
        "prev_record_digest": "GENESIS",
        "record_digest": f"corridor-receipt-{status}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_corridor_stability_gate(
        runtime_context=ctx(runtime),
        corridor_stability_gate_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_corridor_stability_gate_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_READY", label
    assert out["gate_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["corridor_stability_gate_only"] is True, label
    assert packet["boundary"]["stability_gate_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["does_not_select_final_path"] is True, label
    assert packet["boundary"]["corridor_stability_not_execution_authority"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "admit", receipt("history_aware_admissible_corridor"), lic())
        assert_ready("admit", out, packet)
        assert out["corridor_stability_gate_decision"] == "corridor_stability_admit"
        assert out["admitted_count"] == 1
        assert packet["corridor_segments"][0]["corridor_lane"] == "admit_lane"

        out, packet = run(root, "probe", receipt("history_aware_probe_corridor"), lic())
        assert_ready("probe", out, packet)
        assert out["corridor_stability_gate_decision"] == "corridor_stability_hold"
        assert out["probe_count"] == 2

        out, packet = run(root, "blocked", receipt("history_aware_blocked_corridor"), lic())
        assert_ready("blocked", out, packet)
        assert out["corridor_stability_gate_decision"] == "corridor_stability_block"
        assert out["blocked_count"] == 1

        mismatch = receipt("history_aware_admissible_corridor")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, packet = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "admit_lane_segment_0_history_window_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_rank = receipt("history_aware_admissible_corridor")
        bad_rank["corridor_segments"][0] = segment("admit_lane", 0, bad_rank=True)
        out, packet = run(root, "bad_rank", bad_rank, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "admit_lane_segment_0_rank_mismatch" in out["blockers"]
        assert packet == {}

        bad_lane = receipt("history_aware_probe_corridor")
        bad_lane["corridor_segments"].insert(0, segment("admit_lane", 0))
        bad_lane["counts"]["admitted"] = 1
        bad_lane["lane_counts"]["admit_lane"] = 1
        out, packet = run(root, "bad_lane", bad_lane, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "probe_corridor_requires_probe_lane_only" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("history_aware_admissible_corridor")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "history_aware_corridor_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "history_aware_candidate_corridor_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("history_aware_admissible_corridor"), lic(corridor_stability_gate_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CORRIDOR_STABILITY_GATE_BLOCKED"
        assert "corridor_stability_gate_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_corridor_stability_gate_v11_8 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
