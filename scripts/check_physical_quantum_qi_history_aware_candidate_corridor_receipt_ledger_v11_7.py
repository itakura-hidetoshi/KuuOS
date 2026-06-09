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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger_v11_7 import build_physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger

CORRIDOR_BOUNDARY = {
    "history_aware_candidate_corridor_only": True,
    "corridor_build_only": True,
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
    "admissible_set_not_execution_set": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v11-7",
    "memory_kernel_digest": "memory-kernel-digest-v11-7",
    "history_window_digest": "history-window-digest-v11-7",
    "instrument_trace_digest": "instrument-trace-digest-v11-7",
    "non_markov_context_digest": "non-markov-context-digest-v11-7",
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
        "physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_LICENSE_READY",
        "history_aware_candidate_corridor_read_allowed": True,
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


def corridor(status: str) -> dict[str, Any]:
    admit = 1 if status == "history_aware_admissible_corridor" else 0
    probe = 2 if status == "history_aware_probe_corridor" else 0
    blocked = 1 if status == "history_aware_blocked_corridor" else 0
    segments = [segment("admit_lane", i) for i in range(admit)]
    segments += [segment("probe_lane", i) for i in range(probe)]
    segments += [segment("blocked_lane", i) for i in range(blocked)]
    packet = {
        "version": "physical_quantum_qi_history_aware_candidate_corridor_packet_v11_6",
        "physical_quantum_qi_history_aware_candidate_corridor_considered": True,
        "corridor_status": status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_digests": {
            "memory_kernel_consistency_gate_receipt": "mk-gate-receipt-digest-v11-7",
            "memory_kernel_consistency_gate": "mk-gate-digest-v11-7",
            "process_tensor_candidate_set_receipt": "candidate-set-receipt-digest-v11-7",
            "process_tensor_admissible_candidate_set": "candidate-set-digest-v11-7",
        },
        "boundary": dict(CORRIDOR_BOUNDARY),
        "epoch": 1,
    }
    packet["history_aware_candidate_corridor_digest"] = f"corridor-digest-{status}"
    return packet


def run(root: pathlib.Path, name: str, packet: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if packet is not None:
        dump(runtime / "physical_quantum_qi_history_aware_candidate_corridor.json", packet)
    result = build_physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger(
        runtime_context=ctx(runtime),
        history_aware_candidate_corridor_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["history_aware_candidate_corridor_receipt_only"] is True, label
    assert latest["boundary"]["history_bearing_process_tensor"] is True, label
    assert latest["boundary"]["non_markov_context_required"] is True, label
    assert latest["boundary"]["does_not_start_next_cycle"] is True, label
    assert latest["boundary"]["does_not_authorize_execution"] is True, label
    assert latest["boundary"]["corridor_not_execution_path"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "admit", corridor("history_aware_admissible_corridor"), lic())
        assert_ready("admit", out, ledger)
        assert out["corridor_status"] == "history_aware_admissible_corridor"
        assert out["admitted_count"] == 1
        assert ledger[-1]["corridor_segments"][0]["corridor_lane"] == "admit_lane"

        out, ledger = run(root, "probe", corridor("history_aware_probe_corridor"), lic())
        assert_ready("probe", out, ledger)
        assert out["corridor_status"] == "history_aware_probe_corridor"
        assert out["probe_count"] == 2

        out, ledger = run(root, "blocked", corridor("history_aware_blocked_corridor"), lic())
        assert_ready("blocked", out, ledger)
        assert out["corridor_status"] == "history_aware_blocked_corridor"
        assert out["blocked_count"] == 1

        out, ledger = run(root, "chain", corridor("history_aware_admissible_corridor"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", corridor("history_aware_probe_corridor"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        mismatch = corridor("history_aware_admissible_corridor")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, ledger = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "admit_lane_segment_0_non_markov_context_digest_mismatch" in out["blockers"]
        assert ledger == []

        bad_rank = corridor("history_aware_admissible_corridor")
        bad_rank["corridor_segments"][0] = segment("admit_lane", 0, bad_rank=True)
        out, ledger = run(root, "bad_rank", bad_rank, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "admit_lane_segment_0_rank_mismatch" in out["blockers"]
        assert ledger == []

        bad_lane = corridor("history_aware_probe_corridor")
        bad_lane["corridor_segments"].insert(0, segment("admit_lane", 0))
        bad_lane["counts"]["admitted"] = 1
        bad_lane["lane_counts"]["admit_lane"] = 1
        out, ledger = run(root, "bad_lane", bad_lane, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "probe_corridor_requires_probe_lane_only" in out["blockers"]
        assert ledger == []

        bad_boundary = corridor("history_aware_admissible_corridor")
        bad_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "history_aware_candidate_corridor_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "history_aware_candidate_corridor_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", corridor("history_aware_admissible_corridor"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_HISTORY_AWARE_CANDIDATE_CORRIDOR_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_history_aware_candidate_corridor_receipt_ledger_v11_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
