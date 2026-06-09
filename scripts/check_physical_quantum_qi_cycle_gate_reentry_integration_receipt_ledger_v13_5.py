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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 import build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger

PT = {
    "process_tensor_digest": "pt-digest-v13-5",
    "memory_kernel_digest": "memory-kernel-digest-v13-5",
    "history_window_digest": "history-window-digest-v13-5",
    "instrument_trace_digest": "instrument-trace-digest-v13-5",
    "non_markov_context_digest": "non-markov-context-digest-v13-5",
}
PACKET_BOUNDARY = {
    "cycle_gate_reentry_integration_only": True,
    "candidate_weighting_cycle_handoff_receipt_required": True,
    "integrates_cycle_gate": True,
    "integrates_admissible_candidate_set": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "integration_not_direct_execution": True,
    "license_gated_integration": True,
    "fail_closed_on_boundary_loss": True,
}
GATE_BOUNDARY = {
    "integrated_cycle_gate_state_only": True,
    "from_candidate_weighting_cycle_handoff_receipt": True,
    "uses_process_tensor_feedback": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}
SET_BOUNDARY = {
    "integrated_admissible_candidate_set_only": True,
    "from_candidate_weighting_cycle_handoff_receipt": True,
    "uses_process_tensor_feedback": True,
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
        "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_LICENSE_READY",
        "integration_packet_read_allowed": True,
        "integrated_cycle_gate_state_read_allowed": True,
        "integrated_admissible_candidate_set_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def case(status: str) -> tuple[str, str, int, dict[str, Any]]:
    if status == "cycle_gate_reentry_integration_admit":
        return "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1, {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if status == "cycle_gate_reentry_integration_hold":
        return "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1, {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0, {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def candidates_for(status: str, weight: dict[str, Any]) -> list[dict[str, Any]]:
    if status == "cycle_gate_reentry_integration_admit":
        return [{"candidate_id": "closed_loop_reentry_reinforced_candidate", "candidate_mode": "admit_candidate", "candidate_weighting": weight, "process_tensor_context": dict(PT), "admissibility_status": "admissible_candidate_ready", "candidate_digest": "candidate-admit-digest-v13-5"}]
    if status == "cycle_gate_reentry_integration_hold":
        return [{"candidate_id": "closed_loop_reentry_probe_candidate", "candidate_mode": "probe_candidate", "candidate_weighting": weight, "process_tensor_context": dict(PT), "admissibility_status": "admissible_candidate_probe_required", "candidate_digest": "candidate-probe-digest-v13-5"}]
    return []


def packet(status: str, *, bad_boundary: bool = False, bad_status: bool = False, bad_weight: bool = False, missing_context: bool = False) -> dict[str, Any]:
    gate, aset, count, weight = case(status)
    if bad_weight:
        weight = dict(weight)
        if status.endswith("admit"):
            weight["path_weight_delta"] = 0
        elif status.endswith("hold"):
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    boundary = dict(PACKET_BOUNDARY)
    if bad_boundary:
        boundary["integrates_cycle_gate"] = False
    context = dict(PT)
    if missing_context:
        context["non_markov_context_digest"] = ""
    pkt = {
        "version": "physical_quantum_qi_cycle_gate_reentry_integration_packet_v13_4",
        "cycle_gate_reentry_integration_considered": True,
        "integration_status": status,
        "integrated_cycle_gate_status": "wrong_gate" if bad_status else gate,
        "integrated_admissible_candidate_set_status": aset,
        "handoff_status": "candidate_weighting_cycle_handoff_reinforce" if status.endswith("admit") else ("candidate_weighting_cycle_handoff_probe" if status.endswith("hold") else "candidate_weighting_cycle_handoff_barrier"),
        "cycle_gate_decision": "reweight_candidate" if status.endswith("admit") else ("hold_candidate" if status.endswith("hold") else "block_candidate"),
        "admissible_candidate_seed_mode": "reinforce_admissible_candidate_seed" if status.endswith("admit") else ("probe_candidate_seed" if status.endswith("hold") else "barrier_candidate_seed"),
        "candidate_weighting": weight,
        "integrated_candidates": candidates_for(status, weight),
        "process_tensor_context": context,
        "source_digests": {
            "candidate_weighting_cycle_handoff_receipt": "handoff-receipt-digest-v13-5",
            "candidate_weighting_cycle_handoff": "handoff-digest-v13-5",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    pkt["cycle_gate_reentry_integration_digest"] = f"integration-digest-{status}"
    return pkt


def gate_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    weight = dict(pkt["candidate_weighting"])
    if mismatch:
        weight["path_weight_delta"] = int(weight.get("path_weight_delta", 0)) + 1
    boundary = dict(GATE_BOUNDARY)
    if bad_boundary:
        boundary["from_candidate_weighting_cycle_handoff_receipt"] = False
    payload = {
        "version": "physical_quantum_qi_integrated_cycle_gate_state_v13_4",
        "integrated_cycle_gate_ready": True,
        "integrated_cycle_gate_status": pkt["integrated_cycle_gate_status"],
        "cycle_gate_decision": pkt["cycle_gate_decision"],
        "candidate_weighting": weight,
        "source_cycle_gate_reentry_integration_digest": pkt["cycle_gate_reentry_integration_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["integrated_cycle_gate_state_digest"] = f"gate-digest-{pkt['integration_status']}"
    return payload


def candidate_set_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    weight = dict(pkt["candidate_weighting"])
    if mismatch:
        weight["probe_potential_required"] = not bool(weight.get("probe_potential_required"))
    boundary = dict(SET_BOUNDARY)
    if bad_boundary:
        boundary["from_candidate_weighting_cycle_handoff_receipt"] = False
    payload = {
        "version": "physical_quantum_qi_integrated_admissible_candidate_set_v13_4",
        "integrated_admissible_candidate_set_ready": True,
        "integrated_admissible_candidate_set_status": pkt["integrated_admissible_candidate_set_status"],
        "admissible_candidate_count": len(pkt["integrated_candidates"]),
        "integrated_candidates": list(pkt["integrated_candidates"]),
        "candidate_weighting": weight,
        "source_cycle_gate_reentry_integration_digest": pkt["cycle_gate_reentry_integration_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["integrated_admissible_candidate_set_digest"] = f"set-digest-{pkt['integration_status']}"
    return payload


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, gate: dict[str, Any] | None, candidate_set: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_packet.json", pkt)
    if gate is not None:
        dump(runtime / "physical_quantum_qi_integrated_cycle_gate_state.json", gate)
    if candidate_set is not None:
        dump(runtime / "physical_quantum_qi_integrated_admissible_candidate_set.json", candidate_set)
    result = build_physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger(
        runtime_context=ctx(runtime),
        cycle_gate_reentry_integration_receipt_ledger_license=license_packet,
    )
    ledger = load_jsonl(runtime / "physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["cycle_gate_reentry_integration_receipt_only"] is True, label
    assert latest["boundary"]["integrated_cycle_gate_state_traceable"] is True, label
    assert latest["boundary"]["integrated_admissible_candidate_set_traceable"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        cases = [
            ("cycle_gate_reentry_integration_admit", "integrated_cycle_gate_admit", "integrated_admissible_candidate_set_admit", 1),
            ("cycle_gate_reentry_integration_hold", "integrated_cycle_gate_hold", "integrated_admissible_candidate_set_probe", 1),
            ("cycle_gate_reentry_integration_block", "integrated_cycle_gate_block", "integrated_admissible_candidate_set_block", 0),
        ]
        for status, gate_status, set_status, count in cases:
            pkt = packet(status)
            out, ledger = run(root, status, pkt, gate_for(pkt), candidate_set_for(pkt), lic())
            assert_ready(status, out, ledger)
            assert out["integration_status"] == status
            assert out["integrated_cycle_gate_status"] == gate_status
            assert out["integrated_admissible_candidate_set_status"] == set_status
            assert out["admissible_candidate_count"] == count

        pkt = packet("cycle_gate_reentry_integration_admit")
        out, ledger = run(root, "chain", pkt, gate_for(pkt), candidate_set_for(pkt), lic())
        assert_ready("chain_1", out, ledger)
        pkt2 = packet("cycle_gate_reentry_integration_hold")
        out, ledger = run(root, "chain", pkt2, gate_for(pkt2), candidate_set_for(pkt2), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = packet("cycle_gate_reentry_integration_admit", bad_boundary=True)
        out, ledger = run(root, "bad_boundary", pkt, gate_for(pkt), candidate_set_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "cycle_gate_reentry_integration_boundary_integrates_cycle_gate_missing" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_admit", bad_status=True)
        out, ledger = run(root, "bad_status", pkt, gate_for(pkt), candidate_set_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "cycle_gate_reentry_integration_gate_status_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_block", bad_weight=True)
        out, ledger = run(root, "bad_weight", pkt, gate_for(pkt), candidate_set_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "integration_receipt_block_without_blocking_barrier" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_hold")
        out, ledger = run(root, "gate_mismatch", pkt, gate_for(pkt, mismatch=True), candidate_set_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "integrated_cycle_gate_state_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_hold")
        out, ledger = run(root, "set_mismatch", pkt, gate_for(pkt), candidate_set_for(pkt, mismatch=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "integrated_admissible_candidate_set_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_admit", missing_context=True)
        out, ledger = run(root, "missing_context", pkt, gate_for(pkt), candidate_set_for(pkt), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_context_non_markov_context_digest_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, None, None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "cycle_gate_reentry_integration_packet_missing_or_invalid" in out["blockers"]
        assert "integrated_cycle_gate_state_missing_or_invalid" in out["blockers"]
        assert "integrated_admissible_candidate_set_missing_or_invalid" in out["blockers"]
        assert ledger == []

        pkt = packet("cycle_gate_reentry_integration_block")
        out, ledger = run(root, "license", pkt, gate_for(pkt), candidate_set_for(pkt), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_CYCLE_GATE_REENTRY_INTEGRATION_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_cycle_gate_reentry_integration_receipt_ledger_v13_5 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
