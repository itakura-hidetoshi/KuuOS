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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_transition_candidate_envelope_v12_2 import build_physical_quantum_qi_transition_candidate_envelope

RECEIPT_BOUNDARY = {
    "receipt_ledger_only": True,
    "stable_corridor_transition_precheck_receipt_only": True,
    "transition_precheck_receipt_only": True,
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
    "transition_precheck_not_execution_authority": True,
    "receipt_does_not_mutate_transition_precheck_packet": True,
    "replayable_receipt": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-2",
    "memory_kernel_digest": "memory-kernel-digest-v12-2",
    "history_window_digest": "history-window-digest-v12-2",
    "instrument_trace_digest": "instrument-trace-digest-v12-2",
    "non_markov_context_digest": "non-markov-context-digest-v12-2",
}


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_transition_candidate_envelope_enabled": True,
        "apply_physical_quantum_qi_transition_candidate_envelope": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_LICENSE_READY",
        "stable_corridor_transition_precheck_receipt_ledger_read_allowed": True,
        "transition_candidate_envelope_packet_write_allowed": True,
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
        item_pt["non_markov_context_digest"] = "mismatch"
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
    stability = {
        "transition_precheck_admit_candidate": "corridor_stability_admit",
        "transition_precheck_hold_candidate": "corridor_stability_hold",
        "transition_precheck_block_candidate": "corridor_stability_block",
    }[decision]
    status = {
        "transition_precheck_admit_candidate": "history_aware_admissible_corridor",
        "transition_precheck_hold_candidate": "history_aware_probe_corridor",
        "transition_precheck_block_candidate": "history_aware_blocked_corridor",
    }[decision]
    admit = 1 if decision == "transition_precheck_admit_candidate" else 0
    probe = 2 if decision == "transition_precheck_hold_candidate" else 0
    blocked = 1 if decision == "transition_precheck_block_candidate" else 0
    segments = [segment("admit_lane", i) for i in range(admit)]
    segments += [segment("probe_lane", i) for i in range(probe)]
    segments += [segment("blocked_lane", i) for i in range(blocked)]
    return {
        "version": "physical_quantum_qi_stable_corridor_transition_precheck_receipt_record_v12_1",
        "record_type": "physical_quantum_qi_stable_corridor_transition_precheck_receipt",
        "transition_precheck_decision": decision,
        "corridor_stability_gate_decision": stability,
        "corridor_status": status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_stable_corridor_transition_precheck_digest": "transition-precheck-digest-v12-2",
        "source_corridor_stability_gate_receipt_digest": "corridor-stability-receipt-digest-v12-2",
        "source_corridor_stability_gate_digest": "corridor-stability-gate-digest-v12-2",
        "source_history_aware_candidate_corridor_receipt_digest": "corridor-receipt-digest-v12-2",
        "source_history_aware_candidate_corridor_digest": "corridor-digest-v12-2",
        "prev_record_digest": "GENESIS",
        "record_digest": f"transition-precheck-receipt-{decision}",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, record: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime = root / name
    if record is not None:
        append_jsonl(runtime / "physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger.jsonl", record)
    result = build_physical_quantum_qi_transition_candidate_envelope(
        runtime_context=ctx(runtime),
        transition_candidate_envelope_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_transition_candidate_envelope_packet.json")
    return result.to_dict(), packet


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_READY", label
    assert out["envelope_packet_written"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["transition_candidate_envelope_only"] is True, label
    assert packet["boundary"]["envelope_build_only"] is True, label
    assert packet["boundary"]["does_not_start_next_cycle"] is True, label
    assert packet["boundary"]["does_not_authorize_execution"] is True, label
    assert packet["boundary"]["does_not_select_final_path"] is True, label
    assert packet["boundary"]["envelope_not_transition_start"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet = run(root, "admit", receipt("transition_precheck_admit_candidate"), lic())
        assert_ready("admit", out, packet)
        assert out["envelope_status"] == "transition_candidate_envelope_ready"
        assert out["envelope_count"] == 1
        assert packet["transition_candidate_envelopes"][0]["boundary"]["envelope_build_only"] is True

        out, packet = run(root, "hold", receipt("transition_precheck_hold_candidate"), lic())
        assert_ready("hold", out, packet)
        assert out["envelope_status"] == "transition_candidate_envelope_hold"
        assert out["envelope_count"] == 0
        assert packet["transition_candidate_envelopes"] == []

        out, packet = run(root, "block", receipt("transition_precheck_block_candidate"), lic())
        assert_ready("block", out, packet)
        assert out["envelope_status"] == "transition_candidate_envelope_block"
        assert out["envelope_count"] == 0

        bad_stability = receipt("transition_precheck_hold_candidate")
        bad_stability["corridor_stability_gate_decision"] = "corridor_stability_admit"
        out, packet = run(root, "bad_stability", bad_stability, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "transition_precheck_stability_decision_mismatch" in out["blockers"]
        assert packet == {}

        mismatch = receipt("transition_precheck_admit_candidate")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, packet = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "admit_lane_segment_0_non_markov_context_digest_mismatch" in out["blockers"]
        assert packet == {}

        bad_rank = receipt("transition_precheck_admit_candidate")
        bad_rank["corridor_segments"][0] = segment("admit_lane", 0, bad_rank=True)
        out, packet = run(root, "bad_rank", bad_rank, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "admit_lane_segment_0_rank_mismatch" in out["blockers"]
        assert packet == {}

        bad_boundary = receipt("transition_precheck_admit_candidate")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, packet = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "stable_corridor_transition_precheck_receipt_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "stable_corridor_transition_precheck_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet = run(root, "license_block", receipt("transition_precheck_admit_candidate"), lic(transition_candidate_envelope_packet_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_BLOCKED"
        assert "transition_candidate_envelope_packet_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_transition_candidate_envelope_v12_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
