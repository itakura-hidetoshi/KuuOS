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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2 import build_physical_quantum_qi_candidate_weighting_cycle_handoff

PT = {
    "process_tensor_digest": "pt-digest-v13-2",
    "memory_kernel_digest": "memory-kernel-digest-v13-2",
    "history_window_digest": "history-window-digest-v13-2",
    "instrument_trace_digest": "instrument-trace-digest-v13-2",
    "non_markov_context_digest": "non-markov-context-digest-v13-2",
}
BOUNDARY = {
    "receipt_ledger_only": True,
    "closed_loop_reentry_receipt_only": True,
    "candidate_weighting_cycle_traceable": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
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
        "physical_quantum_qi_candidate_weighting_cycle_handoff_enabled": True,
        "apply_physical_quantum_qi_candidate_weighting_cycle_handoff": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_LICENSE_READY",
        "closed_loop_reentry_receipt_ledger_read_allowed": True,
        "handoff_packet_write_allowed": True,
        "cycle_gate_input_write_allowed": True,
        "admissible_candidate_set_seed_write_allowed": True,
        "handoff_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def receipt(status: str, *, bad_boundary: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    if status == "closed_loop_reentry_reinforced":
        action = "reinforce_path_weight"
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
    elif status == "closed_loop_reentry_probe_opened":
        action = "open_probe_potential"
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
        action = "add_barrier_potential"
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
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["candidate_weighting_cycle_traceable"] = False
    context = dict(PT)
    if missing_context:
        context["process_tensor_digest"] = ""
    return {
        "version": "physical_quantum_qi_closed_loop_reentry_receipt_record_v13_1",
        "record_type": "physical_quantum_qi_closed_loop_reentry_receipt",
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_closed_loop_path_integral_reentry_digest": "closed-loop-reentry-digest-v13-2",
        "source_reentry_weighting_state_digest": "reentry-weighting-state-digest-v13-2",
        "source_feedback_to_reentry_weighting_bridge_digest": "feedback-to-reentry-bridge-digest-v13-2",
        "prev_record_digest": "GENESIS",
        "record_digest": f"closed-loop-reentry-receipt-{status}",
        "boundary": boundary,
        "epoch": 1,
    }


def run(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl", rec)
    result = build_physical_quantum_qi_candidate_weighting_cycle_handoff(
        runtime_context=ctx(runtime),
        candidate_weighting_cycle_handoff_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json")
    gate = load_json(runtime / "physical_quantum_qi_next_cycle_gate_input.json")
    seed = load_json(runtime / "physical_quantum_qi_admissible_candidate_set_seed.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")
    return result.to_dict(), packet, gate, seed, ledger


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any], gate: dict[str, Any], seed: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY", label
    assert out["handoff_packet_written"] is True, label
    assert out["cycle_gate_input_written"] is True, label
    assert out["admissible_candidate_set_seed_written"] is True, label
    assert out["handoff_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["hands_off_to_cycle_gate"] is True, label
    assert packet["boundary"]["hands_off_to_admissible_candidate_set"] is True, label
    assert gate["boundary"]["from_closed_loop_reentry_handoff"] is True, label
    assert seed["boundary"]["from_closed_loop_reentry_handoff"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        cases = [
            ("closed_loop_reentry_reinforced", "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed"),
            ("closed_loop_reentry_probe_opened", "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed"),
            ("closed_loop_reentry_barrier_added", "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed"),
        ]
        for status, handoff_status, cycle_decision, seed_mode in cases:
            out, packet, gate, seed, ledger = run(root, status, receipt(status), lic())
            assert_ready(status, out, packet, gate, seed, ledger)
            assert out["handoff_status"] == handoff_status
            assert out["cycle_gate_decision"] == cycle_decision
            assert out["admissible_candidate_seed_mode"] == seed_mode

        out, packet, gate, seed, ledger = run(root, "chain", receipt("closed_loop_reentry_reinforced"), lic())
        assert_ready("chain_1", out, packet, gate, seed, ledger)
        out, packet, gate, seed, ledger = run(root, "chain", receipt("closed_loop_reentry_probe_opened"), lic())
        assert_ready("chain_2", out, packet, gate, seed, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, packet, gate, seed, ledger = run(root, "bad_boundary", receipt("closed_loop_reentry_reinforced", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
        assert "closed_loop_reentry_receipt_boundary_candidate_weighting_cycle_traceable_missing" in out["blockers"]
        assert packet == {}
        assert gate == {}
        assert seed == {}
        assert ledger == []

        out, packet, gate, seed, ledger = run(root, "bad_weight", receipt("closed_loop_reentry_reinforced", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
        assert "handoff_reinforce_without_positive_path_weight_delta" in out["blockers"]
        assert packet == {}

        out, packet, gate, seed, ledger = run(root, "missing_context", receipt("closed_loop_reentry_probe_opened", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
        assert "process_tensor_context_process_tensor_digest_missing" in out["blockers"]
        assert packet == {}

        out, packet, gate, seed, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
        assert "closed_loop_reentry_receipt_ledger_missing" in out["blockers"]
        assert packet == {}

        out, packet, gate, seed, ledger = run(root, "license", receipt("closed_loop_reentry_barrier_added"), lic(cycle_gate_input_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_BLOCKED"
        assert "cycle_gate_input_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
