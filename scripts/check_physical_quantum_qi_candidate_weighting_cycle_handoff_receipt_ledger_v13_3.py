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

PT = {
    "process_tensor_digest": "pt-digest-v13-3",
    "memory_kernel_digest": "memory-kernel-digest-v13-3",
    "history_window_digest": "history-window-digest-v13-3",
    "instrument_trace_digest": "instrument-trace-digest-v13-3",
    "non_markov_context_digest": "non-markov-context-digest-v13-3",
}
PACKET_BOUNDARY = {
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


def dump(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def ctx(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_LICENSE_READY",
        "handoff_packet_read_allowed": True,
        "cycle_gate_input_read_allowed": True,
        "admissible_candidate_set_seed_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def case(status: str) -> tuple[str, str, str, dict[str, Any]]:
    if status == "candidate_weighting_cycle_handoff_reinforce":
        return "reweight_candidate", "reinforce_admissible_candidate_seed", "closed_loop_reentry_reinforced", {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if status == "candidate_weighting_cycle_handoff_probe":
        return "hold_candidate", "probe_candidate_seed", "closed_loop_reentry_probe_opened", {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "block_candidate", "barrier_candidate_seed", "closed_loop_reentry_barrier_added", {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def packet(status: str, *, bad_boundary: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    gate, seed, closed, weight = case(status)
    if bad_weight:
        weight = dict(weight)
        if status.endswith("reinforce"):
            weight["path_weight_delta"] = 0
        elif status.endswith("probe"):
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    boundary = dict(PACKET_BOUNDARY)
    if bad_boundary:
        boundary["hands_off_to_cycle_gate"] = False
    context = dict(PT)
    if missing_context:
        context["history_window_digest"] = ""
    pkt = {
        "version": "physical_quantum_qi_candidate_weighting_cycle_handoff_packet_v13_2",
        "candidate_weighting_cycle_handoff_considered": True,
        "handoff_status": status,
        "closed_loop_reentry_status": closed,
        "reentry_weighting_action": "reinforce_path_weight" if status.endswith("reinforce") else ("open_probe_potential" if status.endswith("probe") else "add_barrier_potential"),
        "cycle_gate_decision": gate,
        "admissible_candidate_seed_mode": seed,
        "candidate_weighting": weight,
        "process_tensor_context": context,
        "source_digests": {
            "closed_loop_reentry_receipt": "closed-loop-reentry-receipt-digest-v13-3",
            "closed_loop_path_integral_reentry": "closed-loop-reentry-digest-v13-3",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    pkt["candidate_weighting_cycle_handoff_digest"] = f"handoff-digest-{status}"
    return pkt


def gate_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    weight = dict(pkt["candidate_weighting"])
    if mismatch:
        weight["path_weight_delta"] = int(weight.get("path_weight_delta", 0)) + 1
    boundary = dict(GATE_BOUNDARY)
    if bad_boundary:
        boundary["from_closed_loop_reentry_handoff"] = False
    payload = {
        "version": "physical_quantum_qi_next_cycle_gate_input_v13_2",
        "cycle_gate_input_ready": True,
        "cycle_gate_decision": pkt["cycle_gate_decision"],
        "candidate_weighting": weight,
        "source_candidate_weighting_cycle_handoff_digest": pkt["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["cycle_gate_input_digest"] = f"cycle-gate-input-digest-{pkt['handoff_status']}"
    return payload


def seed_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    weight = dict(pkt["candidate_weighting"])
    if mismatch:
        weight["probe_potential_required"] = not bool(weight.get("probe_potential_required"))
    boundary = dict(SEED_BOUNDARY)
    if bad_boundary:
        boundary["from_closed_loop_reentry_handoff"] = False
    payload = {
        "version": "physical_quantum_qi_admissible_candidate_set_seed_v13_2",
        "admissible_candidate_set_seed_ready": True,
        "admissible_candidate_seed_mode": pkt["admissible_candidate_seed_mode"],
        "candidate_weighting": weight,
        "source_candidate_weighting_cycle_handoff_digest": pkt["candidate_weighting_cycle_handoff_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["admissible_candidate_set_seed_digest"] = f"seed-digest-{pkt['handoff_status']}"
    return payload


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, gate: dict[str, Any] | None, seed: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_packet.json", pkt)
    if gate is not None:
        dump(runtime / "physical_quantum_qi_next_cycle_gate_input.json", gate)
    if seed is not None:
        dump(runtime / "physical_quantum_qi_admissible_candidate_set_seed.json", seed)
    result = build_physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger(
        runtime_context=ctx(runtime),
        candidate_weighting_cycle_handoff_receipt_ledger_license=license_packet,
    )
    ledger = load_jsonl(runtime / "physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["candidate_weighting_cycle_handoff_receipt_only"] is True, label
    assert latest["boundary"]["cycle_gate_input_traceable"] is True, label
    assert latest["boundary"]["admissible_candidate_set_seed_traceable"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        statuses = [
            "candidate_weighting_cycle_handoff_reinforce",
            "candidate_weighting_cycle_handoff_probe",
            "candidate_weighting_cycle_handoff_barrier",
        ]
        for status in statuses:
            pkt = packet(status)
            out, ledger = run(root, status, pkt, gate_for(pkt), seed_for(pkt), lic())
            assert_ready(status, out, ledger)

        pkt = packet("candidate_weighting_cycle_handoff_reinforce")
        out, ledger = run(root, "chain", pkt, gate_for(pkt), seed_for(pkt), lic())
        assert_ready("chain_1", out, ledger)
        pkt2 = packet("candidate_weighting_cycle_handoff_probe")
        out, ledger = run(root, "chain", pkt2, gate_for(pkt2), seed_for(pkt2), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = packet("candidate_weighting_cycle_handoff_reinforce", bad_boundary=True)
        out, ledger = run(root, "bad_boundary", pkt, gate_for(pkt), seed_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "candidate_weighting_cycle_handoff_boundary_hands_off_to_cycle_gate_missing" in out["blockers"]
        assert ledger == []

        pkt = packet("candidate_weighting_cycle_handoff_reinforce", bad_weight=True)
        out, ledger = run(root, "bad_weight", pkt, gate_for(pkt), seed_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "handoff_receipt_reinforce_weighting_invalid" in out["blockers"]
        assert ledger == []

        pkt = packet("candidate_weighting_cycle_handoff_probe")
        out, ledger = run(root, "gate_mismatch", pkt, gate_for(pkt, mismatch=True), seed_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "next_cycle_gate_input_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("candidate_weighting_cycle_handoff_barrier")
        out, ledger = run(root, "seed_mismatch", pkt, gate_for(pkt), seed_for(pkt, mismatch=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "admissible_candidate_set_seed_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("candidate_weighting_cycle_handoff_probe", missing_context=True)
        out, ledger = run(root, "missing_context", pkt, gate_for(pkt), seed_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_context_history_window_digest_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, None, None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "candidate_weighting_cycle_handoff_packet_missing_or_invalid" in out["blockers"]
        assert "next_cycle_gate_input_missing_or_invalid" in out["blockers"]
        assert "admissible_candidate_set_seed_missing_or_invalid" in out["blockers"]
        assert ledger == []

        pkt = packet("candidate_weighting_cycle_handoff_barrier")
        out, ledger = run(root, "license", pkt, gate_for(pkt), seed_for(pkt), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CANDIDATE_WEIGHTING_CYCLE_HANDOFF_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_candidate_weighting_cycle_handoff_receipt_ledger_v13_3 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
