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
from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 import build_physical_quantum_qi_closed_loop_reentry_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14 import build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-14",
    "memory_kernel_digest": "memory-kernel-digest-v13-14",
    "history_window_digest": "history-window-digest-v13-14",
    "instrument_trace_digest": "instrument-trace-digest-v13-14",
    "non_markov_context_digest": "non-markov-context-digest-v13-14",
}
RECEIPT_BOUNDARY = {
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
PACKET_BOUNDARY = {
    "closed_loop_path_integral_reentry_only": True,
    "feeds_candidate_weighting_cycle": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "closed_loop_reentry_not_unbounded_execution": True,
    "license_gated_closed_loop": True,
    "fail_closed_on_boundary_loss": True,
}
CYCLE_BOUNDARY = {
    "candidate_weighting_cycle_state_only": True,
    "closed_loop_reentry_applied": True,
    "can_feed_next_candidate_weighting_cycle": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_enabled": True,
        "apply_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_LICENSE_READY",
        "v13_1_closed_loop_reentry_receipt_ledger_read_allowed": True,
        "v13_2_handoff_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v13_1_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v13_1_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY",
        "closed_loop_reentry_packet_read_allowed": True,
        "candidate_weighting_cycle_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def v13_2_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_candidate_weighting_cycle_handoff_enabled": True,
        "apply_physical_quantum_qi_candidate_weighting_cycle_handoff": True,
        "runtime_root": str(root),
    }


def v13_2_lic() -> dict[str, Any]:
    return {
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


def parts(kind: str) -> tuple[str, str, str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return "closed_loop_reentry_reinforced", "reinforce_path_weight", "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "probe":
        return "closed_loop_reentry_probe_opened", "open_probe_potential", "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "closed_loop_reentry_barrier_added", "add_barrier_potential", "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def receipt(kind: str, *, bad_boundary: bool = False, bad_action: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    status, action, _, _, _, weight = parts(kind)
    if bad_weight:
        if kind == "reinforce":
            weight["path_weight_delta"] = 0
        elif kind == "probe":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["instrument_trace_digest"] = ""
    boundary = dict(RECEIPT_BOUNDARY)
    if bad_boundary:
        boundary["candidate_weighting_cycle_traceable"] = False
    return {
        "version": "physical_quantum_qi_closed_loop_reentry_receipt_record_v13_1",
        "record_type": "physical_quantum_qi_closed_loop_reentry_receipt",
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": "wrong_action" if bad_action else action,
        "candidate_weighting": dict(weight),
        "process_tensor_context": context,
        "source_closed_loop_path_integral_reentry_digest": f"closed-loop-reentry-digest-{kind}",
        "source_reentry_weighting_state_digest": "reentry-state-digest-v13-14",
        "source_feedback_to_reentry_weighting_bridge_digest": "feedback-to-reentry-digest-v13-14",
        "prev_record_digest": "GENESIS",
        "record_digest": f"closed-loop-reentry-receipt-digest-{kind}",
        "boundary": boundary,
        "epoch": 1,
    }


def packet_cycle(kind: str) -> tuple[dict[str, Any], dict[str, Any]]:
    status, action, _, _, _, weight = parts(kind)
    packet = {
        "version": "physical_quantum_qi_closed_loop_path_integral_reentry_packet_v13_0",
        "closed_loop_path_integral_reentry_considered": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weight),
        "process_tensor_context": dict(PT),
        "source_digests": {
            "reentry_weighting_state": "reentry-state-digest-v13-14",
            "feedback_to_reentry_weighting_bridge": "feedback-to-reentry-digest-v13-14",
        },
        "boundary": dict(PACKET_BOUNDARY),
        "closed_loop_path_integral_reentry_digest": f"closed-loop-reentry-digest-{kind}",
        "epoch": 1,
    }
    cycle = {
        "version": "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state_v13_0",
        "candidate_weighting_cycle_ready": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weight),
        "process_tensor_context": dict(PT),
        "source_closed_loop_path_integral_reentry_digest": packet["closed_loop_path_integral_reentry_digest"],
        "boundary": dict(CYCLE_BOUNDARY),
        "candidate_weighting_cycle_state_digest": f"candidate-cycle-digest-{kind}",
        "epoch": 1,
    }
    return packet, cycle


def run_bridge(root: pathlib.Path, name: str, rec: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if rec is not None:
        append_jsonl(runtime / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl", rec)
    out = build_physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge(
        runtime_context=bridge_ctx(runtime),
        v13_1_to_v13_2_cycle_handoff_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_2_candidate_weighting_cycle_handoff_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_READY", (label, out)
    assert out["handoff_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_2_candidate_weighting_cycle_handoff"] is True, label
    assert ready["boundary"]["does_not_run_handoff_runtime"] is True, label
    assert ledger[-1]["boundary"]["v13_2_cycle_handoff_ready_state_traceable"] is True, label


def assert_v13_2_accepts(runtime: pathlib.Path, label: str, expected_handoff: str, expected_decision: str, expected_seed: str) -> None:
    out = build_physical_quantum_qi_candidate_weighting_cycle_handoff(
        runtime_context=v13_2_ctx(runtime),
        candidate_weighting_cycle_handoff_license=v13_2_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY", (label, out)
    assert out["handoff_status"] == expected_handoff, (label, out)
    assert out["cycle_gate_decision"] == expected_decision, (label, out)
    assert out["admissible_candidate_seed_mode"] == expected_seed, (label, out)
    assert out["handoff_packet_written"] is True, label
    assert out["cycle_gate_input_written"] is True, label
    assert out["admissible_candidate_set_seed_written"] is True, label
    assert out["handoff_ledger_appended"] is True, label


def run_full_v13_1_to_v13_2(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    pkt, cyc = packet_cycle(kind)
    dump(runtime / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json", pkt)
    dump(runtime / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json", cyc)
    v13_1 = build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
        runtime_context=v13_1_ctx(runtime),
        closed_loop_reentry_receipt_ledger_license=v13_1_lic(),
    ).to_dict()
    assert v13_1["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY", v13_1
    out, ready, ledger = run_bridge(root, f"full_{kind}", None, bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    _, _, expected_handoff, expected_decision, expected_seed, _ = parts(kind)
    assert_v13_2_accepts(runtime, f"full_{kind}", expected_handoff, expected_decision, expected_seed)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforce", "probe", "barrier"]:
            rec = receipt(kind)
            out, ready, ledger = run_bridge(root, kind, rec, bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            _, _, expected_handoff, expected_decision, expected_seed, _ = parts(kind)
            assert out["expected_v13_2_handoff_status"] == expected_handoff
            assert out["expected_v13_2_cycle_gate_decision"] == expected_decision
            assert out["expected_v13_2_admissible_candidate_seed_mode"] == expected_seed
            assert_v13_2_accepts(root / kind, kind, expected_handoff, expected_decision, expected_seed)

        for kind in ["reinforce", "probe", "barrier"]:
            run_full_v13_1_to_v13_2(root, kind)

        out, ready, ledger = run_bridge(root, "chain", receipt("reinforce"), bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        out, ready, ledger = run_bridge(root, "chain", receipt("probe"), bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, ready, ledger = run_bridge(root, "bad_boundary", receipt("reinforce", bad_boundary=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "closed_loop_reentry_receipt_boundary_candidate_weighting_cycle_traceable_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        out, ready, ledger = run_bridge(root, "bad_action", receipt("reinforce", bad_action=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "closed_loop_reentry_action_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_weight", receipt("barrier", bad_weight=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "v13_2_bridge_barrier_weighting_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing_context", receipt("reinforce", missing_context=True), bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "process_tensor_context_instrument_trace_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "closed_loop_reentry_receipt_ledger_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "license", receipt("reinforce"), bridge_lic(v13_2_handoff_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_BLOCKED"
        assert "v13_2_handoff_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v13_1_to_v13_2_cycle_handoff_bridge_v13_14 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
