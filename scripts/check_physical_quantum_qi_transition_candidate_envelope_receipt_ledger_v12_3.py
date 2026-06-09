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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_transition_candidate_envelope_receipt_ledger_v12_3 import build_physical_quantum_qi_transition_candidate_envelope_receipt_ledger

PACKET_BOUNDARY = {
    "transition_candidate_envelope_only": True,
    "envelope_build_only": True,
    "stable_corridor_transition_precheck_required": True,
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
    "envelope_not_transition_start": True,
    "fail_closed_on_boundary_loss": True,
}
PT = {
    "process_tensor_digest": "pt-digest-v12-3",
    "memory_kernel_digest": "memory-kernel-digest-v12-3",
    "history_window_digest": "history-window-digest-v12-3",
    "instrument_trace_digest": "instrument-trace-digest-v12-3",
    "non_markov_context_digest": "non-markov-context-digest-v12-3",
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
        "physical_quantum_qi_transition_candidate_envelope_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_transition_candidate_envelope_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_LICENSE_READY",
        "transition_candidate_envelope_packet_read_allowed": True,
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


def envelope_for(seg: dict[str, Any], *, bad_boundary: bool = False) -> dict[str, Any]:
    boundary = {
        "transition_candidate_envelope_only": True,
        "envelope_build_only": True,
        "does_not_start_next_cycle": True,
        "does_not_authorize_execution": True,
        "does_not_select_final_path": True,
        "does_not_execute_path": True,
    }
    if bad_boundary:
        boundary["does_not_authorize_execution"] = False
    env = {
        "envelope_type": "physical_quantum_qi_transition_candidate_envelope",
        "candidate_id": seg["candidate_id"],
        "corridor_lane": seg["corridor_lane"],
        "corridor_rank": seg["corridor_rank"],
        "transition_precheck_decision": "transition_precheck_admit_candidate",
        "corridor_stability_gate_decision": "corridor_stability_admit",
        "candidate_weighting": seg["candidate_weighting"],
        "process_tensor_context": seg["process_tensor_context"],
        "boundary": boundary,
    }
    env["transition_candidate_envelope_digest"] = f"envelope-digest-{seg['candidate_id']}"
    return env


def packet(status: str) -> dict[str, Any]:
    precheck = {
        "transition_candidate_envelope_ready": "transition_precheck_admit_candidate",
        "transition_candidate_envelope_hold": "transition_precheck_hold_candidate",
        "transition_candidate_envelope_block": "transition_precheck_block_candidate",
    }[status]
    stability = {
        "transition_candidate_envelope_ready": "corridor_stability_admit",
        "transition_candidate_envelope_hold": "corridor_stability_hold",
        "transition_candidate_envelope_block": "corridor_stability_block",
    }[status]
    corridor_status = {
        "transition_candidate_envelope_ready": "history_aware_admissible_corridor",
        "transition_candidate_envelope_hold": "history_aware_probe_corridor",
        "transition_candidate_envelope_block": "history_aware_blocked_corridor",
    }[status]
    admit = 1 if status == "transition_candidate_envelope_ready" else 0
    probe = 2 if status == "transition_candidate_envelope_hold" else 0
    blocked = 1 if status == "transition_candidate_envelope_block" else 0
    segments = [segment("admit_lane", i) for i in range(admit)]
    segments += [segment("probe_lane", i) for i in range(probe)]
    segments += [segment("blocked_lane", i) for i in range(blocked)]
    envelopes = [envelope_for(seg) for seg in segments if seg["corridor_lane"] == "admit_lane"]
    pkt = {
        "version": "physical_quantum_qi_transition_candidate_envelope_packet_v12_2",
        "physical_quantum_qi_transition_candidate_envelope_considered": True,
        "envelope_status": status,
        "transition_precheck_decision": precheck,
        "corridor_stability_gate_decision": stability,
        "corridor_status": corridor_status,
        "counts": {"admitted": admit, "probe": probe, "blocked": blocked},
        "lane_counts": {"admit_lane": admit, "probe_lane": probe, "blocked_lane": blocked},
        "transition_candidate_envelopes": envelopes,
        "corridor_segments": segments,
        "process_tensor_context": dict(PT),
        "source_digests": {
            "stable_corridor_transition_precheck_receipt": "transition-precheck-receipt-digest-v12-3",
            "stable_corridor_transition_precheck": "transition-precheck-digest-v12-3",
            "corridor_stability_gate_receipt": "corridor-stability-receipt-digest-v12-3",
            "corridor_stability_gate": "corridor-stability-gate-digest-v12-3",
            "history_aware_candidate_corridor_receipt": "corridor-receipt-digest-v12-3",
            "history_aware_candidate_corridor": "corridor-digest-v12-3",
        },
        "boundary": dict(PACKET_BOUNDARY),
        "epoch": 1,
    }
    pkt["transition_candidate_envelope_packet_digest"] = f"transition-candidate-envelope-packet-digest-{status}"
    return pkt


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_transition_candidate_envelope_packet.json", pkt)
    result = build_physical_quantum_qi_transition_candidate_envelope_receipt_ledger(
        runtime_context=ctx(runtime),
        transition_candidate_envelope_receipt_ledger_license=license_packet,
    )
    ledger = read_jsonl(runtime / "physical_quantum_qi_transition_candidate_envelope_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["receipt_ledger_only"] is True, label
    assert latest["boundary"]["transition_candidate_envelope_receipt_only"] is True, label
    assert latest["boundary"]["envelope_receipt_only"] is True, label
    assert latest["boundary"]["does_not_start_next_cycle"] is True, label
    assert latest["boundary"]["does_not_authorize_execution"] is True, label
    assert latest["boundary"]["does_not_select_final_path"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, ledger = run(root, "ready", packet("transition_candidate_envelope_ready"), lic())
        assert_ready("ready", out, ledger)
        assert out["envelope_status"] == "transition_candidate_envelope_ready"
        assert out["envelope_count"] == 1
        assert ledger[-1]["transition_candidate_envelopes"][0]["corridor_lane"] == "admit_lane"

        out, ledger = run(root, "hold", packet("transition_candidate_envelope_hold"), lic())
        assert_ready("hold", out, ledger)
        assert out["envelope_status"] == "transition_candidate_envelope_hold"
        assert out["envelope_count"] == 0

        out, ledger = run(root, "block", packet("transition_candidate_envelope_block"), lic())
        assert_ready("block", out, ledger)
        assert out["envelope_status"] == "transition_candidate_envelope_block"
        assert out["envelope_count"] == 0

        out, ledger = run(root, "chain", packet("transition_candidate_envelope_ready"), lic())
        assert_ready("chain_1", out, ledger)
        out, ledger = run(root, "chain", packet("transition_candidate_envelope_hold"), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        bad_hold = packet("transition_candidate_envelope_hold")
        bad_hold["transition_candidate_envelopes"] = [envelope_for(segment("admit_lane", 0))]
        out, ledger = run(root, "bad_hold", bad_hold, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "hold_or_block_envelope_must_be_empty" in out["blockers"]
        assert ledger == []

        bad_boundary = packet("transition_candidate_envelope_ready")
        bad_boundary["transition_candidate_envelopes"][0] = envelope_for(bad_boundary["corridor_segments"][0], bad_boundary=True)
        out, ledger = run(root, "bad_envelope_boundary", bad_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "transition_candidate_envelope_0_boundary_does_not_authorize_execution_missing" in out["blockers"]
        assert ledger == []

        mismatch = packet("transition_candidate_envelope_ready")
        mismatch["corridor_segments"][0] = segment("admit_lane", 0, mismatch=True)
        out, ledger = run(root, "mismatch", mismatch, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "admit_lane_segment_0_history_window_digest_mismatch" in out["blockers"]
        assert ledger == []

        bad_packet_boundary = packet("transition_candidate_envelope_ready")
        bad_packet_boundary["boundary"]["does_not_start_next_cycle"] = False
        out, ledger = run(root, "bad_packet_boundary", bad_packet_boundary, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "transition_candidate_envelope_boundary_does_not_start_next_cycle_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "transition_candidate_envelope_packet_missing_or_invalid" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "license_block", packet("transition_candidate_envelope_ready"), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_TRANSITION_CANDIDATE_ENVELOPE_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_transition_candidate_envelope_receipt_ledger_v12_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
