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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3 import build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger
from runtime.kuuos_runtime_daemon_physical_quantum_qi_candidate_weighting_cycle_handoff_v13_2 import build_physical_quantum_qi_candidate_weighting_cycle_handoff
from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15 import build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge

PT = {
    "process_tensor_digest": "pt-digest-v13-15",
    "memory_kernel_digest": "memory-kernel-digest-v13-15",
    "history_window_digest": "history-window-digest-v13-15",
    "instrument_trace_digest": "instrument-trace-digest-v13-15",
    "non_markov_context_digest": "non-markov-context-digest-v13-15",
}
HANDOFF_BOUNDARY = {
    "candidate_weighting_cycle_handoff_only": True,
    "closed_loop_reentry_receipt_required": True,
    "hands_off_to_cycle_gate": True,
    "hands_off_to_admissible_candidate_set": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "handoff_not_direct_execution": True,
    "license_gated_handoff": True,
    "fail_closed_on_boundary_loss": True,
}
GATE_BOUNDARY = {
    "cycle_gate_input_only": True,
    "from_closed_loop_reentry_handoff": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
SEED_BOUNDARY = {
    "admissible_candidate_set_seed_only": True,
    "from_closed_loop_reentry_handoff": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
REENTRY_RECEIPT_BOUNDARY = {
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
        "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_enabled": True,
        "apply_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge": True,
        "runtime_root": str(root),
    }


def bridge_lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_2_handoff_packet_read_allowed": True,
        "v13_2_cycle_gate_input_read_allowed": True,
        "v13_2_admissible_candidate_set_seed_read_allowed": True,
        "v13_3_handoff_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


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


def v13_3_ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger": True,
        "runtime_root": str(root),
    }


def v13_3_lic() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "cycle_gate_input_read_allowed": True,
        "admissible_candidate_set_seed_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def parts(kind: str) -> tuple[str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return "candidate_weighting_cycle_handoff_reinforce", "reweight_candidate", "reinforce_admissible_candidate_seed", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if kind == "probe":
        return "candidate_weighting_cycle_handoff_probe", "hold_candidate", "probe_candidate_seed", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "candidate_weighting_cycle_handoff_barrier", "block_candidate", "barrier_candidate_seed", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def write_inputs(runtime: pathlib.Path, kind: str, *, bad_packet_boundary: bool = False, bad_gate: bool = False, bad_seed: bool = False, bad_weight: bool = False, missing_context: bool = False) -> None:
    handoff, gate, seed, weighting = parts(kind)
    if bad_weight:
        if kind == "reinforce":
            weighting["path_weight_delta"] = 0
        elif kind == "probe":
            weighting["barrier_potential_required"] = True
        else:
            weighting["barrier_blocks_ready_weight"] = False
    context = dict(PT)
    if missing_context:
        context["non_markov_context_digest"] = ""
    boundary = dict(HANDOFF_BOUNDARY)
    if bad_packet_boundary:
        boundary["hands_off_to_cycle_gate"] = False
    packet = {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_packet_v13_2",
        "candidate_weighting_cycle_handoff_considered": True,
        "handoff_status": handoff,
        "closed_loop_reentry_status": "closed-loop-status-v13-15",
        "reentry_weighting_action": "action-v13-15",
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": dict(weighting),
        "process_tensor_context": context,
        "source_digests": {
            "closed_loop_reentry_receipt": "closed-loop-reentry-receipt-digest-v13-15",
            "closed_loop_path_integral_reentry": "closed-loop-reentry-digest-v13-15",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    packet["candidate_weighting_cycle_handoff_digest"] = f"handoff-digest-{kind}"
    gate_payload = {
        "version": "physical_quantum_qi_next_cycle_gate_input_v13_2",
        "cycle_gate_input_ready": True,
        "cycle_gate_decision": "wrong_gate" if bad_gate else gate,
        "candidate_weighting": dict(weighting),
        "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": context,
        "boundary": dict(GATE_BOUNDARY),
        "epoch": 1,
    }
    gate_payload["cycle_gate_input_digest"] = f"gate-digest-{kind}"
    seed_payload = {
        "version": "physical_quantum_qi_admissible_candidate_set_seed_v13_2",
        "admissible_candidate_set_seed_ready": True,
        "admissible_candidate_seed_mode": "wrong_seed" if bad_seed else seed,
        "candidate_weighting": dict(weighting),
        "source_candidate_weighting_cycle_handoff_digest": packet["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": context,
        "boundary": dict(SEED_BOUNDARY),
        "epoch": 1,
    }
    seed_payload["admissible_candidate_set_seed_digest"] = f"seed-digest-{kind}"
    dump(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json", packet)
    dump(runtime / "physical_quantum_qi_next_cycle_gate_input.json", gate_payload)
    dump(runtime / "physical_quantum_qi_admissible_candidate_set_seed.json", seed_payload)


def reentry_receipt(kind: str) -> dict[str, Any]:
    handoff, gate, seed, weighting = parts(kind)
    closed = {
        "reinforce": "closed_loop_reentry_reinforced",
        "probe": "closed_loop_reentry_probe_opened",
        "barrier": "closed_loop_reentry_barrier_added",
    }[kind]
    action = {
        "reinforce": "reinforce_path_weight",
        "probe": "open_probe_potential",
        "barrier": "add_barrier_potential",
    }[kind]
    return {
        "version": "physical_quantum_qi_closed_loop_reentry_receipt_record_v13_1",
        "record_type": "physical_quantum_qi_closed_loop_reentry_receipt",
        "closed_loop_reentry_status": closed,
        "reentry_weighting_action": action,
        "candidate_weighting": dict(weighting),
        "process_tensor_context": dict(PT),
        "source_closed_loop_path_integral_reentry_digest": "closed-loop-reentry-digest-v13-15",
        "source_reentry_weighting_state_digest": "reentry-state-digest-v13-15",
        "source_feedback_to_reentry_weighting_bridge_digest": "feedback-to-reentry-digest-v13-15",
        "prev_record_digest": "GENESIS",
        "record_digest": "closed-loop-reentry-receipt-digest-v13-15",
        "boundary": dict(REENTRY_RECEIPT_BOUNDARY),
        "epoch": 1,
    }


def run_bridge(root: pathlib.Path, name: str, *, kind: str | None, license_packet: dict[str, Any], **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if kind is not None:
        write_inputs(runtime, kind, **kwargs)
    out = build_physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge(
        runtime_context=bridge_ctx(runtime),
        v13_2_to_v13_3_handoff_receipt_bridge_license=license_packet,
    ).to_dict()
    ready = load_json(runtime / "physical_quantum_qi_v13_3_candidate_weighting_cycle_handoff_receipt_ready_state.json")
    ledger = load_jsonl(runtime / "physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_ledger.jsonl")
    return out, ready, ledger


def assert_bridge_ready(label: str, out: dict[str, Any], ready: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_READY", (label, out)
    assert out["receipt_ready_state_written"] is True, label
    assert out["bridge_ledger_appended"] is True, label
    assert not out["blockers"], label
    assert ready["boundary"]["can_feed_v13_3_candidate_weighting_cycle_handoff_receipt_ledger"] is True, label
    assert ready["boundary"]["does_not_run_receipt_ledger"] is True, label
    assert ledger[-1]["boundary"]["v13_3_handoff_receipt_ready_state_traceable"] is True, label


def assert_v13_3_accepts(runtime: pathlib.Path, label: str, expected_handoff: str, expected_gate: str, expected_seed: str) -> None:
    out = build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
        runtime_context=v13_3_ctx(runtime),
        candidate_weighting_cycle_handoff_receipt_ledger_license=v13_3_lic(),
    ).to_dict()
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY", (label, out)
    assert out["handoff_status"] == expected_handoff, (label, out)
    assert out["cycle_gate_decision"] == expected_gate, (label, out)
    assert out["admissible_candidate_seed_mode"] == expected_seed, (label, out)
    assert out["ledger_appended"] is True, label


def run_full_v13_2_to_v13_3(root: pathlib.Path, kind: str) -> None:
    runtime = root / f"full_{kind}"
    append_jsonl(runtime / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl", reentry_receipt(kind))
    v13_2 = build_physical_quantum_qi_candidate_weighting_cycle_handoff(
        runtime_context=v13_2_ctx(runtime),
        candidate_weighting_cycle_handoff_license=v13_2_lic(),
    ).to_dict()
    assert v13_2["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_READY", v13_2
    out, ready, ledger = run_bridge(root, f"full_{kind}", kind=None, license_packet=bridge_lic())
    assert_bridge_ready(f"full_{kind}", out, ready, ledger)
    handoff, gate, seed, _ = parts(kind)
    assert_v13_3_accepts(runtime, f"full_{kind}", handoff, gate, seed)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for kind in ["reinforce", "probe", "barrier"]:
            out, ready, ledger = run_bridge(root, kind, kind=kind, license_packet=bridge_lic())
            assert_bridge_ready(kind, out, ready, ledger)
            handoff, gate, seed, _ = parts(kind)
            assert out["handoff_status"] == handoff
            assert out["cycle_gate_decision"] == gate
            assert out["admissible_candidate_seed_mode"] == seed
            assert_v13_3_accepts(root / kind, kind, handoff, gate, seed)

        for kind in ["reinforce", "probe", "barrier"]:
            run_full_v13_2_to_v13_3(root, kind)

        out, ready, ledger = run_bridge(root, "chain", kind="reinforce", license_packet=bridge_lic())
        assert_bridge_ready("chain_1", out, ready, ledger)
        out, ready, ledger = run_bridge(root, "chain", kind="probe", license_packet=bridge_lic())
        assert_bridge_ready("chain_2", out, ready, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        out, ready, ledger = run_bridge(root, "bad_packet_boundary", kind="reinforce", license_packet=bridge_lic(), bad_packet_boundary=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_boundary_hands_off_to_cycle_gate_missing" in out["blockers"]
        assert ready == {}
        assert ledger == []

        out, ready, ledger = run_bridge(root, "bad_gate", kind="probe", license_packet=bridge_lic(), bad_gate=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "next_cycle_gate_input_decision_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_seed", kind="barrier", license_packet=bridge_lic(), bad_seed=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "admissible_candidate_set_seed_mode_mismatch" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "bad_weight", kind="barrier", license_packet=bridge_lic(), bad_weight=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_3_bridge_barrier_weighting_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing_context", kind="reinforce", license_packet=bridge_lic(), missing_context=True)
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "process_tensor_context_non_markov_context_digest_missing" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "missing", kind=None, license_packet=bridge_lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "candidate_weighting_cycle_handoff_packet_missing_or_invalid" in out["blockers"]
        assert "next_cycle_gate_input_missing_or_invalid" in out["blockers"]
        assert "admissible_candidate_set_seed_missing_or_invalid" in out["blockers"]
        assert ready == {}

        out, ready, ledger = run_bridge(root, "license", kind="reinforce", license_packet=bridge_lic(v13_3_handoff_receipt_ready_state_write_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_V13_2_TO_V13_3_HANDOFF_RECEIPT_BRIDGE_BLOCKED"
        assert "v13_3_handoff_receipt_ready_state_write_not_allowed" in out["blockers"]
        assert ready == {}

    print("physical_quantum_qi_v13_2_to_v13_3_handoff_receipt_bridge_v13_15 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
