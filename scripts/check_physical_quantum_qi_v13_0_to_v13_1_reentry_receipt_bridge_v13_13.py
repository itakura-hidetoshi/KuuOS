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
from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1 import build_physical_quantum_qi_closed_loop_reentry_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_v13_13 import build_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-13",
    "memory_kernel_digest": "memory-kernel-digest-v13-13",
    "history_window_digest": "history-window-digest-v13-13",
    "instrument_trace_digest": "instrument-trace-digest-v13-13",
    "non_markov_context_digest": "non-markov-context-digest-v13-13",
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
REENTRY_STATE_BOUNDARY = {
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


def bridge_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_enabled": True,
        "apply_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_0_closed_loop_reentry_packet_read_allowed": True,
        "v13_0_candidate_weighting_cycle_state_read_allowed": True,
        "v13_1_reentry_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def v13_0_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_closed_loop_path_integral_reentry_enabled": True,
        "apply_physical_quantum_qi_closed_loop_path_integral_reentry": True,
        "runtime_root": str(root),
    }


def v13_0_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY",
        "reentry_weighting_state_read_allowed": True,
        "closed_loop_reentry_packet_write_allowed": True,
        "candidate_weighting_cycle_state_write_allowed": True,
        "closed_loop_reentry_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


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


def parts(kind: str) -> tuple[str, str, dict[str, Any]]:
    if kind == "reinforced":
        return "closed_loop_reentry_reinforced", "reinforce_path_weight", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "probe":
        return "closed_loop_reentry_probe_opened", "open_probe_potential", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "closed_loop_reentry_barrier_added", "add_barrier_potential", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def packet_cycle(kind: str, *, bad_packet_boundary: bool = False, bad_cycle_boundary: bool = False, bad_weight: bool = False, bad_action: bool = False, digest_mismatch: bool = False, missing_context: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
    status, action, weight = parts(kind)
    if bad_weight:
        if kind == "reinforced":
            weight["path_weight_delta"] = 0
        elif kind == "probe":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["history_window_digest"] = ""
    pb = dict(PACKET_BOUNDARY)
    if bad_packet_boundary:
        pb["feeds_candidate_weighting_cycle"] = False
    packet = {
        "version": "physical_quantum_qi_closed_loop_path_integral_reentry_packet_v13_0",
        "closed_loop_path_integral_reentry_considered": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": "wrong_action" if bad_action else action,
        "candidate_weighting": dict(weight),
        "process_tensor_context": context,
        "source_digests": {
            "reentry_weighting_state": "reentry-state-digest-v13-13",
            "feedback_to_reentry_weighting_bridge": "feedback-to-reentry-digest-v13-13",
        },
        "boundary": pb,
        "epoch": 1,
    }
    packet["closed_loop_path_integral_reentry_digest"] = f"closed-loop-reentry-digest-{kind}"
    cb = dict(CYCLE_BOUNDARY)
    if bad_cycle_boundary:
        cb["can_feed_next_candidate_weighting_cycle"] = False
    cycle = {
        "version": "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state_v13_0",
        "candidate_weighting_cycle_ready": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weight),
        "process_tensor_context": context,
        "source_closed_loop_path_integral_reentry_digest": "mismatch" if digest_mismatch else packet["closed_loop_path_integral_reentry_digest"],
        "boundary": cb,
        "epoch": 1,
    }
    cycle["candidate_weighting_cycle_state_digest"] = f"candidate-cycle-state-digest-{kind}"
    return packet, cycle


def reentry_state(kind: str) -> dict[str, Any]:
    status, action, weight = parts(kind)
    status_map = {
        "closed_loop_reentry_reinforced": "reentry_weighting_reinforce",
        "closed_loop_reentry_probe_opened": "reentry_weighting_hold",
        "closed_loop_reentry_barrier_added": "reentry_weighting_block",
    }
    return {
        "version": "physical_quantum_qi_reentry_weighting_state_v12_9",
        "reentry_weighting_state_ready": True,
        "feedback_status": "feedback-for-v13-13",
        "reentry_weighting_status": status_map[status],
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weight),
        "can_feed_next_path_integral_reentry": True,
        "source_feedback_to_reentry_weighting_bridge_digest": "feedback-to-reentry-digest-v13-13",
        "process_tensor_context": dict(PT),
        "boundary": dict(REENTRY_STATE_BOUNDARY),
        "reentry_weighting_state_digest": "reentry-state-digest-v13-13",
        "epoch": 1,
    }


def write_inputs(runtime: pathlib.Path, packet: dict[str, Any] | None, cycle: dict[str, Any] | None) -> None:
    if packet is not None:
        dump(runtime / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json", packet)
    if cycle is not None:
        dump(runtime / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json", cycle)


def run_bridge(root: pathlib.Path, name: str, packet: dict[str, Any] | None, cycle: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    write_inputs(runtime, packet, cycle)
    out = build_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge(
        runtime_context=bridge_ctx(runtime),
        v13_0_to_v13_1_reentry_receipt_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_1_closed_loop_reentry_receipt_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_READY", (label, out)
    assert out["receipt_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_1_closed_loop_reentry_receipt_ledger"] is True, label
    assert ready["boundary"]["does_not_run_receipt_ledger"] is True, label
    assert ledger[-1]["boundary"]["v13_1_reentry_receipt_ready_state_traceable"] is True, label


def assert_v13_1_accepts(runtime: pathlib.Path, label: str, expected: str) -> None:
    out = build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
        runtime_context=v13_1_ctx(runtime),
        closed_loop_reentry_receipt_ledger_license=v13_1_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY", (label, out)
    assert out["closed_loop_reentry_status"] == expected, (label, out)
    assert out["ledger_appended"] is True, label


def run_full_v13_0_to_v13_1(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    dump(runtime / "physical_quantum_qi_reentry_weighting_state.json", reentry_state(kind))
    v13_0 = build_physical_quantum_qi_closed_loop_path_integral_reentry(
        runtime_context=v13_0_ctx(runtime),
        closed_loop_path_integral_reentry_license=v13_0_lic(),
    ).to_dict()
    assert v13_0["status"] == "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY", v13_0
    out, ready, ledger = run_bridge(root, f"full_{kind}", None, None, bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    status, _, _ = parts(kind)
    assert out["closed_loop_reentry_status"] == status
    assert_v13_1_accepts(runtime, f"full_{kind}", status)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforced", "probe", "barrier"]:
            pkt, cyc = packet_cycle(kind)
            out, ready, ledger = run_bridge(root, kind, pkt, cyc, bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            status, _, _ = parts(kind)
            assert out["closed_loop_reentry_status"] == status
            assert_v13_1_accepts(root / kind, kind, status)

        for kind in ["reinforced", "probe", "barrier"]:
            run_full_v13_0_to_v13_1(root, kind)

        pkt, cyc = packet_cycle("reinforced")
        out, ready, ledger = run_bridge(root, "chain", pkt, cyc, bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        pkt2, cyc2 = packet_cycle("probe")
        out, ready, ledger = run_bridge(root, "chain", pkt2, cyc2, bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt, cyc = packet_cycle("reinforced", bad_packet_boundary=True)
        out, ready, ledger = run_bridge(root, "bad_packet_boundary", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "closed_loop_path_integral_reentry_boundary_feeds_candidate_weighting_cycle_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        pkt, cyc = packet_cycle("probe", bad_cycle_boundary=True)
        out, ready, ledger = run_bridge(root, "bad_cycle_boundary", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_state_boundary_can_feed_next_candidate_weighting_cycle_missing" in out["blockers"]
        assert ready == {}

        pkt, cyc = packet_cycle("barrier", bad_weight=True)
        out, ready, ledger = run_bridge(root, "bad_weight", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_1_bridge_barrier_weighting_invalid" in out["blockers"]
        assert ready == {}

        pkt, cyc = packet_cycle("reinforced", bad_action=True)
        out, ready, ledger = run_bridge(root, "bad_action", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "closed_loop_reentry_action_mismatch" in out["blockers"]
        assert ready == {}

        pkt, cyc = packet_cycle("reinforced", digest_mismatch=True)
        out, ready, ledger = run_bridge(root, "digest_mismatch", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_state_source_digest_mismatch" in out["blockers"]
        assert ready == {}

        pkt, cyc = packet_cycle("reinforced", missing_context=True)
        out, ready, ledger = run_bridge(root, "missing_context", pkt, cyc, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "process_tensor_context_history_window_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", None, None, bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "closed_loop_path_integral_reentry_packet_missing_or_invalid" in out["blockers"]
        assert "candidate_weighting_cycle_state_missing_or_invalid" in out["blockers"]
        assert ready == {}

        pkt, cyc = packet_cycle("reinforced")
        out, ready, ledger = run_bridge(root, "license", pkt, cyc, bridge_lic(v13_1_reentry_receipt_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_1_reentry_receipt_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_v13_13 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
