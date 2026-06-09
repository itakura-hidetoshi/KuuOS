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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_guarded_intent_bridge_receipt_ledger_v13_7 import build_physical_quantum_qi_guarded_intent_bridge_receipt_ledger

PT = {
    "process_tensor_digest": "pt-digest-v13-7",
    "memory_kernel_digest": "memory-kernel-digest-v13-7",
    "history_window_digest": "history-window-digest-v13-7",
    "instrument_trace_digest": "instrument-trace-digest-v13-7",
    "non_markov_context_digest": "non-markov-context-digest-v13-7",
}
BRIDGE_BOUNDARY = {
    "integrated_candidate_to_guarded_intent_bridge_only": True,
    "cycle_gate_reentry_integration_receipt_required": True,
    "emits_guarded_execution_intent_packet": True,
    "uses_process_tensor_feedback": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "bridge_not_direct_execution": True,
    "does_not_run_runner": True,
    "does_not_mutate_external_state": True,
    "does_not_start_next_cycle": True,
    "license_gated_bridge": True,
    "fail_closed_on_boundary_loss": True,
}
INTENT_PACKET_BOUNDARY = {
    "guarded_execution_intent_packet_only": True,
    "from_integrated_candidate_bridge": True,
    "requires_guarded_execution_license": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
    "does_not_run_runner": True,
    "does_not_mutate_external_state": True,
}
INTENT_BOUNDARY = {
    "guarded_execution_intent_only": True,
    "execution_layer_entrypoint": True,
    "no_dry_run_required": True,
    "requires_guarded_execution_license": True,
    "intent_not_world_mutation": True,
    "does_not_start_next_cycle": True,
    "does_not_mutate_external_state": True,
    "does_not_consume_memory": True,
    "does_not_promote_truth": True,
}
STATE_BOUNDARY = {
    "guarded_execution_intent_bridge_state_only": True,
    "from_integrated_candidate_bridge": True,
    "can_feed_guarded_execution_intent_receipt_layer": True,
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
        "physical_quantum_qi_guarded_intent_bridge_receipt_ledger_enabled": True,
        "apply_physical_quantum_qi_guarded_intent_bridge_receipt_ledger": True,
        "runtime_root": str(root),
    }


def lic(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_LICENSE_READY",
        "bridge_packet_read_allowed": True,
        "guarded_execution_intent_packet_read_allowed": True,
        "bridge_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }
    value.update(overrides)
    return value


def case(status: str) -> tuple[str, str, str, int, dict[str, Any]]:
    if status == "ready":
        return "integrated_candidate_to_guarded_intent_ready", "guarded_execution_intent_ready", "emit_guarded_ready_intent", 1, {
            "path_weight_delta": 2,
            "probe_potential_required": False,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 1,
            "external_backaction_weight": 1,
            "next_cycle_amplitude_delta": 1,
        }
    if status == "hold":
        return "integrated_candidate_to_guarded_intent_hold", "guarded_execution_intent_hold", "emit_guarded_hold_intent", 0, {
            "path_weight_delta": 0,
            "probe_potential_required": True,
            "barrier_potential_required": False,
            "barrier_blocks_ready_weight": False,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        }
    return "integrated_candidate_to_guarded_intent_block", "guarded_execution_intent_block", "emit_guarded_block_intent", 0, {
        "path_weight_delta": 0,
        "probe_potential_required": False,
        "barrier_potential_required": True,
        "barrier_blocks_ready_weight": True,
        "memory_feedback_weight": 0,
        "external_backaction_weight": 0,
        "next_cycle_amplitude_delta": 0,
    }


def intents(count: int, weight: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx in range(count):
        item = {
            "intent_index": idx,
            "intent_type": "physical_quantum_qi_guarded_execution_intent",
            "candidate_id": f"candidate-{idx}",
            "transition_precheck_decision": "transition_precheck_admit_candidate",
            "corridor_stability_gate_decision": "corridor_stability_admit",
            "candidate_weighting": weight,
            "process_tensor_context": dict(PT),
            "source_integrated_candidate_digest": f"candidate-digest-{idx}",
            "source_cycle_gate_reentry_integration_receipt_digest": "integration-receipt-digest-v13-7",
            "boundary": dict(INTENT_BOUNDARY),
        }
        item["guarded_execution_intent_digest"] = f"guarded-intent-digest-{idx}"
        out.append(item)
    return out


def bridge_packet(status: str, *, bad_boundary: bool = False, bad_status: bool = False, bad_weight: bool = False, bad_count: bool = False, missing_context: bool = False) -> dict[str, Any]:
    bridge, guarded, emit, count, weight = case(status)
    if bad_weight:
        if status == "ready":
            weight["path_weight_delta"] = 0
        elif status == "hold":
            weight["barrier_potential_required"] = True
        else:
            weight["barrier_blocks_ready_weight"] = False
    if bad_count:
        count = 0 if status == "ready" else 1
    context = dict(PT)
    if missing_context:
        context["memory_kernel_digest"] = ""
    boundary = dict(BRIDGE_BOUNDARY)
    if bad_boundary:
        boundary["emits_guarded_execution_intent_packet"] = False
    pkt = {
        "version": "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet_v13_6",
        "integrated_candidate_to_guarded_intent_bridge_considered": True,
        "bridge_status": bridge,
        "integration_status": "cycle_gate_reentry_integration_admit" if status == "ready" else ("cycle_gate_reentry_integration_hold" if status == "hold" else "cycle_gate_reentry_integration_block"),
        "guarded_execution_intent_status": "wrong_status" if bad_status else guarded,
        "guarded_intent_emit_action": emit,
        "guarded_execution_intent_count": count,
        "candidate_weighting": weight,
        "guarded_execution_intents": intents(count, weight),
        "process_tensor_context": context,
        "source_digests": {
            "cycle_gate_reentry_integration_receipt": "integration-receipt-digest-v13-7",
            "cycle_gate_reentry_integration": "integration-digest-v13-7",
        },
        "boundary": boundary,
        "epoch": 1,
    }
    pkt["integrated_candidate_to_guarded_intent_bridge_digest"] = f"bridge-digest-{status}"
    return pkt


def intent_packet_for(pkt: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    weight = dict(pkt["candidate_weighting"])
    if mismatch:
        weight["path_weight_delta"] = int(weight.get("path_weight_delta", 0)) + 1
    boundary = dict(INTENT_PACKET_BOUNDARY)
    if bad_boundary:
        boundary["from_integrated_candidate_bridge"] = False
    payload = {
        "version": "physical_quantum_qi_guarded_execution_intent_packet_v13_6",
        "guarded_execution_intent_packet_ready": True,
        "guarded_execution_intent_status": pkt["guarded_execution_intent_status"],
        "guarded_execution_intent_count": pkt["guarded_execution_intent_count"],
        "guarded_execution_intents": list(pkt["guarded_execution_intents"]),
        "candidate_weighting": weight,
        "process_tensor_context": dict(PT),
        "source_integrated_candidate_to_guarded_intent_bridge_digest": pkt["integrated_candidate_to_guarded_intent_bridge_digest"],
        "boundary": boundary,
        "epoch": 1,
    }
    payload["guarded_execution_intent_packet_digest"] = f"intent-packet-digest-{pkt['bridge_status']}"
    return payload


def state_for(pkt: dict[str, Any], intent_packet: dict[str, Any], *, mismatch: bool = False, bad_boundary: bool = False) -> dict[str, Any]:
    boundary = dict(STATE_BOUNDARY)
    if bad_boundary:
        boundary["can_feed_guarded_execution_intent_receipt_layer"] = False
    payload = {
        "version": "physical_quantum_qi_guarded_execution_intent_bridge_state_v13_6",
        "guarded_execution_intent_bridge_state_ready": True,
        "bridge_status": pkt["bridge_status"],
        "guarded_execution_intent_status": pkt["guarded_execution_intent_status"],
        "guarded_execution_intent_packet_digest": "mismatch" if mismatch else intent_packet["guarded_execution_intent_packet_digest"],
        "source_integrated_candidate_to_guarded_intent_bridge_digest": pkt["integrated_candidate_to_guarded_intent_bridge_digest"],
        "process_tensor_context": dict(PT),
        "boundary": boundary,
        "epoch": 1,
    }
    payload["guarded_execution_intent_bridge_state_digest"] = f"bridge-state-digest-{pkt['bridge_status']}"
    return payload


def run(root: pathlib.Path, name: str, pkt: dict[str, Any] | None, intent_packet: dict[str, Any] | None, state: dict[str, Any] | None, license_packet: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runtime = root / name
    if pkt is not None:
        dump(runtime / "physical_quantum_qi_integrated_candidate_to_guarded_intent_bridge_packet.json", pkt)
    if intent_packet is not None:
        dump(runtime / "physical_quantum_qi_guarded_execution_intent_packet.json", intent_packet)
    if state is not None:
        dump(runtime / "physical_quantum_qi_guarded_execution_intent_bridge_state.json", state)
    result = build_physical_quantum_qi_guarded_intent_bridge_receipt_ledger(
        runtime_context=ctx(runtime),
        guarded_intent_bridge_receipt_ledger_license=license_packet,
    )
    ledger = load_jsonl(runtime / "physical_quantum_qi_guarded_intent_bridge_receipt_ledger.jsonl")
    return result.to_dict(), ledger


def assert_ready(label: str, out: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_READY", label
    assert out["ledger_appended"] is True, label
    assert not out["blockers"], label
    latest = ledger[-1]
    assert latest["boundary"]["guarded_intent_bridge_receipt_only"] is True, label
    assert latest["boundary"]["guarded_execution_intent_packet_traceable"] is True, label
    assert latest["boundary"]["guarded_execution_intent_bridge_state_traceable"] is True, label
    assert latest["boundary"]["replayable_receipt"] is True, label


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for status, guarded_status, count in [
            ("ready", "guarded_execution_intent_ready", 1),
            ("hold", "guarded_execution_intent_hold", 0),
            ("block", "guarded_execution_intent_block", 0),
        ]:
            pkt = bridge_packet(status)
            ip = intent_packet_for(pkt)
            out, ledger = run(root, status, pkt, ip, state_for(pkt, ip), lic())
            assert_ready(status, out, ledger)
            assert out["guarded_execution_intent_status"] == guarded_status
            assert out["guarded_execution_intent_count"] == count

        pkt = bridge_packet("ready")
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "chain", pkt, ip, state_for(pkt, ip), lic())
        assert_ready("chain_1", out, ledger)
        pkt2 = bridge_packet("hold")
        ip2 = intent_packet_for(pkt2)
        out, ledger = run(root, "chain", pkt2, ip2, state_for(pkt2, ip2), lic())
        assert_ready("chain_2", out, ledger)
        assert len(ledger) == 2
        assert ledger[0]["prev_record_digest"] == "GENESIS"
        assert ledger[1]["prev_record_digest"] == ledger[0]["record_digest"]

        pkt = bridge_packet("ready", bad_boundary=True)
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "bad_boundary", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "integrated_candidate_to_guarded_intent_bridge_boundary_emits_guarded_execution_intent_packet_missing" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("ready", bad_status=True)
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "bad_status", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_status_mismatch" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("block", bad_weight=True)
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "bad_weight", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_intent_receipt_block_without_blocking_barrier" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("ready", bad_count=True)
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "bad_count", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_intent_receipt_ready_requires_intent" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("hold")
        ip = intent_packet_for(pkt, mismatch=True)
        out, ledger = run(root, "intent_mismatch", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_packet_weighting_mismatch" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("hold")
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "state_mismatch", pkt, ip, state_for(pkt, ip, mismatch=True), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "guarded_execution_intent_bridge_state_intent_packet_digest_mismatch" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("ready", missing_context=True)
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "missing_context", pkt, ip, state_for(pkt, ip), lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "process_tensor_context_memory_kernel_digest_missing" in out["blockers"]
        assert ledger == []

        out, ledger = run(root, "missing", None, None, None, lic())
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "integrated_candidate_to_guarded_intent_bridge_packet_missing_or_invalid" in out["blockers"]
        assert "guarded_execution_intent_packet_missing_or_invalid" in out["blockers"]
        assert "guarded_execution_intent_bridge_state_missing_or_invalid" in out["blockers"]
        assert ledger == []

        pkt = bridge_packet("block")
        ip = intent_packet_for(pkt)
        out, ledger = run(root, "license", pkt, ip, state_for(pkt, ip), lic(receipt_ledger_append_allowed=False))
        assert out["status"] == "PHYSICAL_QUANTUM_QI_GUARDED_INTENT_BRIDGE_RECEIPT_LEDGER_BLOCKED"
        assert "receipt_ledger_append_not_allowed" in out["blockers"]
        assert ledger == []

    print("physical_quantum_qi_guarded_intent_bridge_receipt_ledger_v13_7 checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
