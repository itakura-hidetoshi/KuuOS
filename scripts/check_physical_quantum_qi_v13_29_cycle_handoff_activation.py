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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_29_cycle_handoff_activation import build_physical_quantum_qi_v13_29_cycle_handoff_activation

PT = {
    "process_tensor_digest": "pt-v13-29",
    "memory_kernel_digest": "memory-v13-29",
    "history_window_digest": "history-v13-29",
    "instrument_trace_digest": "instrument-v13-29",
    "non_markov_context_digest": "non-markov-v13-29",
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


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def latest_jsonl(path: pathlib.Path) -> dict[str, Any]:
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(lines[-1])


def parts(kind: str) -> tuple[str, str, str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return (
            "closed_loop_reentry_reinforced",
            "reinforce_path_weight",
            "candidate_weighting_cycle_handoff_reinforce",
            "reweight_candidate",
            "reinforce_admissible_candidate_seed",
            {"path_weight_delta": 2, "probe_potential_required": False, "barrier_potential_required": False, "barrier_blocks_ready_weight": False, "memory_feedback_weight": 1, "external_backaction_weight": 1, "next_cycle_amplitude_delta": 1},
        )
    if kind == "probe":
        return (
            "closed_loop_reentry_probe_opened",
            "open_probe_potential",
            "candidate_weighting_cycle_handoff_probe",
            "hold_candidate",
            "probe_candidate_seed",
            {"path_weight_delta": 0, "probe_potential_required": True, "barrier_potential_required": False, "barrier_blocks_ready_weight": False, "memory_feedback_weight": 0, "external_backaction_weight": 0, "next_cycle_amplitude_delta": 0},
        )
    return (
        "closed_loop_reentry_barrier_added",
        "add_barrier_potential",
        "candidate_weighting_cycle_handoff_barrier",
        "block_candidate",
        "barrier_candidate_seed",
        {"path_weight_delta": 0, "probe_potential_required": False, "barrier_potential_required": True, "barrier_blocks_ready_weight": True, "memory_feedback_weight": 0, "external_backaction_weight": 0, "next_cycle_amplitude_delta": 0},
    )


def prepare(root: pathlib.Path, kind: str, *, bad_digest: bool = False, bad_weighting: bool = False) -> None:
    closed_status, action, _, _, _, weighting = parts(kind)
    weighting = dict(weighting)
    if bad_weighting and kind == "reinforce":
        weighting["path_weight_delta"] = 0
    receipt_digest = f"v13-1-receipt-{kind}"
    receipt_record = {
        "version": "physical_quantum_qi_closed_loop_reentry_receipt_record_v13_1",
        "record_type": "physical_quantum_qi_closed_loop_reentry_receipt",
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": dict(PT),
        "source_closed_loop_path_integral_reentry_digest": f"v13-0-closed-loop-{kind}",
        "source_reentry_weighting_state_digest": f"v12-9-state-{kind}",
        "source_feedback_to_reentry_weighting_bridge_digest": f"v12-9-bridge-{kind}",
        "prev_record_digest": "GENESIS",
        "boundary": dict(RECEIPT_BOUNDARY),
        "epoch": 1,
        "record_digest": receipt_digest,
    }
    activation = {
        "version": "physical_quantum_qi_v13_28_reentry_receipt_activation_record",
        "activation_status": "reentry_receipt_activation_completed",
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "source_v13_27_activation_record_digest": f"v13-27-{kind}",
        "source_v13_0_closed_loop_packet_digest": f"v13-0-closed-loop-{kind}",
        "source_v13_0_candidate_cycle_state_digest": f"v13-0-cycle-{kind}",
        "source_v13_13_receipt_ready_state_digest": f"v13-13-ready-{kind}",
        "source_v13_1_receipt_record_digest": "wrong-receipt-digest" if bad_digest else receipt_digest,
        "boundary": {"two_stage_reentry_receipt_activation": True, "uses_process_tensor_feedback": True, "non_markov_feedback_preserved": True, "candidate_weighting_not_truth": True, "not_direct_execution_authority": True, "license_gated_receipt_activation": True, "fail_closed_on_boundary_loss": True},
        "reentry_receipt_activation_record_digest": f"v13-28-record-{kind}",
        "epoch": 1,
    }
    append_jsonl(root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl", receipt_record)
    write_json(root / "physical_quantum_qi_v13_28_reentry_receipt_activation_record.json", activation)


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_1_TO_V13_2_CYCLE_HANDOFF_BRIDGE_LICENSE_READY",
        "v13_1_closed_loop_reentry_receipt_ledger_read_allowed": True,
        "v13_2_handoff_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def handoff_license() -> dict[str, Any]:
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


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_29_CYCLE_HANDOFF_ACTIVATION_LICENSE_READY",
        "v13_28_activation_record_read_allowed": True,
        "v13_1_receipt_ledger_read_allowed": True,
        "v13_14_bridge_invoke_allowed": True,
        "v13_2_handoff_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_14_bridge_license": bridge_license(),
        "v13_2_handoff_license": handoff_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_29_cycle_handoff_activation_enabled": True,
        "apply_physical_quantum_qi_v13_29_cycle_handoff_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_29_cycle_handoff_activation(
        runtime_context=context(root),
        v13_29_cycle_handoff_activation_license=license_packet,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare(root, kind)
            result = run(root, activation_license())
            closed_status, action, handoff_status, decision, seed_mode, _ = parts(kind)
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_29_CYCLE_HANDOFF_ACTIVATION_READY", (kind, result)
            assert result["activation_status"] == "cycle_handoff_activation_completed"
            assert result["closed_loop_reentry_status"] == closed_status
            assert result["reentry_weighting_action"] == action
            assert result["handoff_status"] == handoff_status
            assert result["cycle_gate_decision"] == decision
            assert result["admissible_candidate_seed_mode"] == seed_mode
            assert result["v13_14_bridge_invoked"] is True
            assert result["v13_2_handoff_invoked"] is True
            assert result["handoff_ready_state_written"] is True
            assert result["handoff_packet_written"] is True
            assert result["cycle_gate_input_written"] is True
            assert result["admissible_candidate_set_seed_written"] is True
            assert result["handoff_ledger_appended"] is True
            record = json.loads((root / "physical_quantum_qi_v13_29_cycle_handoff_activation_record.json").read_text(encoding="utf-8"))
            handoff_record = latest_jsonl(root / "physical_quantum_qi_candidate_weighting_cycle_handoff_ledger.jsonl")
            assert record["source_v13_14_handoff_ready_state_digest"]
            assert record["source_v13_2_handoff_packet_digest"]
            assert record["source_v13_2_handoff_record_digest"] == handoff_record["record_digest"]

        root = base / "digest_mismatch"
        prepare(root, "reinforce", bad_digest=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_14_bridge_invoked"] is False
        assert "v13_28_receipt_record_digest_mismatch" in result["blockers"]

        root = base / "bad_weighting"
        prepare(root, "reinforce", bad_weighting=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_14_bridge_invoked"] is True
        assert result["v13_2_handoff_invoked"] is False
        assert "v13_14_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare(root, "reinforce")
        result = run(root, activation_license(v13_2_handoff_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_14_bridge_invoked"] is False
        assert result["v13_2_handoff_invoked"] is False
        assert "v13_2_handoff_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_29_cycle_handoff_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
