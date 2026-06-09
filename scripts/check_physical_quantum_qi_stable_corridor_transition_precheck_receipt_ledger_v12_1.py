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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger_v12_1 import build_physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger

PRECHECK_BOUNDARY = {
    "stable_corridor_transition_precheck_only": True,
    "transition_precheck_only": True,
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
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-1",
    "memory_kernel_digest": "memory-kernel-digest-v12-1",
    "history_window_digest": "history-window-digest-v12-1",
    "instrument_trace_digest": "instrument-trace-digest-v12-1",
    "non_markov_context_digest": "non-markov-context-digest-v12-1",
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
        "physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_LICENSE_READY",
        "stable_corridor_transition_precheck_packet_read_allowed": True,
        "receipt_ledger_append_allowed": True,
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
        item_pt["process_tensor_digest"] = "mismatch"
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


def precheck_packet(decision: str) -> dict[str, Any]:
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
    packet = {
        "version": "physical_quantum_qi_stable_corridor_transition_precheck_packet_v12_0",
        "physical_quantum_qi_stable_corridor_transition_precheck_considered": True,
        "transition_precheck_decision": decision,
        "corridor_stability_gate_decision": stability,
        "corridor_status": status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_digests": {
            "corridor_stability_gate_receipt": "corridor-stability-receipt-digest-v12-1",
            "corridor_stability_gate": "corridor-stability-gate-digest-v12-1",
            "history_aware_candidate_corridor_receipt": "corridor-receipt-digest-v12-1",
            "history_aware_candidate_corridor": "corridor-digest-v12-1",
        },
        "boundary": dict(PRECHECK_BOUNDARY),
        "epoch": 1,
    }
    packet["stable_corridor_transition_precheck_digest"] = f"stable-corridor-transition-precheck-digest-{decision}"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_stable_corridor_transition_precheck_packet.json", packet)
    result = build_physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger(
        runtime_context=ctx(runtime),
        stable_corridor_transition_precheck_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["stable_corridor_transition_precheck_receipt_only"] is True, label
    assert latest["boundary"]["transition_precheck_receipt_only"] is True, label
    assert latest["boundary"]["does_not_start_next_cycle"] is True, label
    assert latest["boundary"]["does_not_authorize_execution"] is True, label
    assert latest["boundary"]["does_not_select_final_path"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "admit", precheck_packet("transition_precheck_admit_candidate"), lic())
        assert_ready("admit", out, ledger)
        assert out["transition_precheck_decision"] == "transition_precheck_admit_candidate"
        assert out["admitted_count"] == 1

        out, ledger = run(root, "hold", precheck_packet("transition_precheck_hold_candidate"), lic())
        assert_ready("hold", out, ledger)
        assert out["transition_precheck_decision"] == "transition_precheck_hold_candidate"
        assert out["probe_count"] == 2

        out, ledger = run(root, "block", precheck_packet("transition_precheck_block_candidate"), lic())
        assert_ready("block", out, ledger)
        assert out["transition_precheck_decision"] == "transition_precheck_block_candidate"
        assert out["blocked_count"] == 1

        out, ledger = run(root, "chain", precheck_packet("transition_precheck_admit_candidate"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", precheck_packet("transition_precheck_hold_candidate"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_stability = precheck_packet("transition_precheck_hold_candidate")
        bad_stability["corridor_stability_gate_decision"] = "corridor_stability_admit"
        out, ledger = run(root, "bad_stability", bad_stability, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "transition_precheck_stability_decision_mismatch" in out["blockers"]
        assert ledger == []

        mismatch = precheck_packet("transition_precheck_admit_candidate")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, ledger = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "admit_lane_segment_0_process_tensor_digest_mismatch" in out["blockers"]
        assert ledger == []

        bad_rank = precheck_packet("transition_precheck_admit_candidate")
        bad_rank["corridor_segments"][0] = segment("admit_lane", 0, bad_rank=True)
        out, ledger = run(root, "bad_rank", bad_rank, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "admit_lane_segment_0_rank_mismatch" in out["blockers"]
        assert ledger == []

        bad_boundary = precheck_packet("transition_precheck_admit_candidate")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "stable_corridor_transition_precheck_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "stable_corridor_transition_precheck_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", precheck_packet("transition_precheck_admit_candidate"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_STABLE_CORRIDOR_TRANSITION_PRECHECK_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_stable_corridor_transition_precheck_receipt_ledger_v12_1 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
