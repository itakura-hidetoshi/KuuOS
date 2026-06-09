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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0 import build_physical_quantum_qi_closed_loop_path_integral_reentry

PT = {
    "process_tensor_digest": "pt-digest-v13-0",
    "memory_kernel_digest": "memory-kernel-digest-v13-0",
    "history_window_digest": "history-window-digest-v13-0",
    "instrument_trace_digest": "instrument-trace-digest-v13-0",
    "non_markov_context_digest": "non-markov-context-digest-v13-0",
}
BOUNDARY = {
    "reentry_weighting_state_only": True,
    "can_feed_next_path_integral_reentry": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_closed_loop_path_integral_reentry_enabled": True,
        "apply_physical_quantum_qi_closed_loop_path_integral_reentry": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY",
        "reentry_weighting_state_read_allowed": True,
        "closed_loop_reentry_packet_write_allowed": True,
        "candidate_weighting_cycle_state_write_allowed": True,
        "closed_loop_reentry_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def state(action: str, *, bad_boundary: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    if action == "reinforce_path_weight":
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
        feedback_status = "process_tensor_feedback_reinforce_next_cycle"
        reentry_status = "reentry_weighting_reinforce"
    elif action == "open_probe_potential":
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
            weighting["path_weight_delta"] = 1
        feedback_status = "process_tensor_feedback_hold_context"
        reentry_status = "reentry_weighting_hold"
    else:
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
        feedback_status = "process_tensor_feedback_block_context"
        reentry_status = "reentry_weighting_block"
    boundary = dict(BOUNDARY)
    if bad_boundary:
        boundary["can_feed_next_path_integral_reentry"] = False
    context = dict(PT)
    if missing_context:
        context["history_window_digest"] = ""
    st = {
        "version": "physical_quantum_qi_reentry_weighting_state_v12_9",
        "reentry_weighting_state_ready": True,
        "feedback_status": feedback_status,
        "reentry_weighting_status": reentry_status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "can_feed_next_path_integral_reentry": True,
        "source_feedback_to_reentry_weighting_bridge_digest": "feedback-to-reentry-bridge-digest-v13-0",
        "process_tensor_context": context,
        "boundary": boundary,
        "epoch": 1,
    }
    st["reentry_weighting_state_digest"] = f"reentry-weighting-state-digest-{action}"
    return st


def run(root: pathlib.Path, name: str, st: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if st is not None:
        dump(runtime / "physical_quantum_qi_reentry_weighting_state.json", st)
    result = build_physical_quantum_qi_closed_loop_path_integral_reentry(
        runtime_context=ctx(runtime),
        closed_loop_path_integral_reentry_license=license_packet,
    )
    packet = load_json(runtime / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json")
    cycle = load_json(runtime / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_closed_loop_path_integral_reentry_ledger.jsonl")
    return result.to_dict(), packet, cycle, ledger


def assert_ready(label: str, out: dict[str, Any], packet: dict[str, Any], cycle: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY", label
    assert out["candidate_weighting_cycle_updated"] is True, label
    assert out["closed_loop_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert packet["boundary"]["closed_loop_path_integral_reentry_only"] is True, label
    assert packet["boundary"]["feeds_candidate_weighting_cycle"] is True, label
    assert cycle["candidate_weighting_cycle_ready"] is True, label
    assert cycle["boundary"]["closed_loop_reentry_applied"] is True, label
    assert ledger[-1]["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)

        out, packet, cycle, ledger = run(root, "reinforce", state("reinforce_path_weight"), lic())
        assert_ready("reinforce", out, packet, cycle, ledger)
        assert out["closed_loop_reentry_status"] == "closed_loop_reentry_reinforced"
        assert out["path_weight_delta"] == 2
        assert out["probe_potential_required"] is False
        assert out["barrier_potential_required"] is False
        assert cycle["candidate_weighting"]["memory_feedback_weight"] == 1

        out, packet, cycle, ledger = run(root, "probe", state("open_probe_potential"), lic())
        assert_ready("probe", out, packet, cycle, ledger)
        assert out["closed_loop_reentry_status"] == "closed_loop_reentry_probe_opened"
        assert out["path_weight_delta"] == 0
        assert out["probe_potential_required"] is True
        assert out["barrier_potential_required"] is False

        out, packet, cycle, ledger = run(root, "barrier", state("add_barrier_potential"), lic())
        assert_ready("barrier", out, packet, cycle, ledger)
        assert out["closed_loop_reentry_status"] == "closed_loop_reentry_barrier_added"
        assert out["path_weight_delta"] == 0
        assert out["probe_potential_required"] is False
        assert out["barrier_potential_required"] is True
        assert cycle["candidate_weighting"]["barrier_blocks_ready_weight"] is True

        out, packet, cycle, ledger = run(root, "chain", state("reinforce_path_weight"), lic())
        assert_ready("chain_1", out, packet, cycle, ledger)
        out, packet, cycle, ledger = run(root, "chain", state("open_probe_potential"), lic())
        assert_ready("chain_2", out, packet, cycle, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["closed_loop_reentry_record_digest"]

        out, packet, cycle, ledger = run(root, "bad_boundary", state("reinforce_path_weight", bad_boundary=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
        assert "reentry_weighting_state_boundary_can_feed_next_path_integral_reentry_missing" in out["blockers"]
        assert packet == {}
        assert cycle == {}
        assert ledger == []

        out, packet, cycle, ledger = run(root, "bad_weight", state("reinforce_path_weight", bad_weight=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
        assert "closed_loop_reentry_reinforce_without_positive_path_weight_delta" in out["blockers"]
        assert packet == {}

        out, packet, cycle, ledger = run(root, "missing_context", state("open_probe_potential", missing_context=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
        assert "process_tensor_context_history_window_digest_missing" in out["blockers"]
        assert packet == {}

        out, packet, cycle, ledger = run(root, "missing", None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
        assert "reentry_weighting_state_missing_or_invalid" in out["blockers"]
        assert packet == {}

        out, packet, cycle, ledger = run(root, "license", state("open_probe_potential"), lic(candidate_weighting_cycle_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
        assert "candidate_weighting_cycle_state_write_not_allowed" in out["blockers"]
        assert packet == {}

    print("physical_quantum_qi_closed_loop_path_integral_reentry_v13_0 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
