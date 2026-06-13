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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation import (
    build_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation,
)

PT = {
    "process_tensor_digest": "pt-v13-28",
    "memory_kernel_digest": "memory-v13-28",
    "history_window_digest": "history-v13-28",
    "instrument_trace_digest": "instrument-v13-28",
    "non_markov_context_digest": "non-markov-v13-28",
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


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parts(kind: str) -> tuple[str, str, dict[str, Any]]:
    if kind == "reinforce":
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


def prepare(root: pathlib.Path, kind: str, *, bad_cycle_digest: bool = False, bad_weighting: bool = False) -> None:
    status, action, weighting = parts(kind)
    weighting = dict(weighting)
    if bad_weighting and kind == "reinforce":
        weighting["path_weight_delta"] = 0
    packet_digest = f"closed-loop-packet-{kind}"
    cycle_digest = f"candidate-cycle-{kind}"
    packet = {
        "version": "physical_quantum_qi_closed_loop_path_integral_reentry_packet_v13_0",
        "closed_loop_path_integral_reentry_considered": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": dict(PT),
        "source_digests": {
            "reentry_weighting_state": f"reentry-state-{kind}",
            "feedback_to_reentry_weighting_bridge": f"feedback-to-reentry-{kind}",
        },
        "boundary": dict(PACKET_BOUNDARY),
        "closed_loop_path_integral_reentry_digest": packet_digest,
        "epoch": 1,
    }
    cycle = {
        "version": "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state_v13_0",
        "candidate_weighting_cycle_ready": True,
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": dict(PT),
        "source_closed_loop_path_integral_reentry_digest": packet_digest,
        "boundary": dict(CYCLE_BOUNDARY),
        "candidate_weighting_cycle_state_digest": cycle_digest,
        "epoch": 1,
    }
    activation = {
        "version": "physical_quantum_qi_v13_27_closed_loop_reentry_activation_record",
        "activation_status": "closed_loop_reentry_activation_completed",
        "reentry_weighting_status": {
            "reinforce": "reentry_weighting_reinforce",
            "probe": "reentry_weighting_hold",
            "barrier": "reentry_weighting_block",
        }[kind],
        "reentry_weighting_action": action,
        "expected_closed_loop_reentry_status": status,
        "observed_closed_loop_reentry_status": status,
        "source_v13_26_activation_record_digest": f"v13-26-{kind}",
        "source_v12_9_reentry_weighting_state_digest": f"v12-9-{kind}",
        "source_v13_12_reentry_ready_state_digest": f"v13-12-{kind}",
        "source_v13_0_candidate_weighting_cycle_state_digest": "wrong-cycle" if bad_cycle_digest else cycle_digest,
        "boundary": {
            "two_stage_closed_loop_reentry_activation": True,
            "uses_process_tensor_feedback": True,
            "non_markov_feedback_preserved": True,
            "candidate_weighting_not_truth": True,
            "not_direct_execution_authority": True,
            "license_gated_closed_loop": True,
            "fail_closed_on_boundary_loss": True,
        },
        "closed_loop_reentry_activation_record_digest": f"v13-27-record-{kind}",
        "epoch": 1,
    }
    write_json(root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json", packet)
    write_json(root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json", cycle)
    write_json(root / "physical_quantum_qi_v13_27_closed_loop_reentry_activation_record.json", activation)


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_LICENSE_READY",
        "v13_0_closed_loop_reentry_packet_read_allowed": True,
        "v13_0_candidate_weighting_cycle_state_read_allowed": True,
        "v13_1_reentry_receipt_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def ledger_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY",
        "closed_loop_reentry_packet_read_allowed": True,
        "candidate_weighting_cycle_state_read_allowed": True,
        "receipt_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_28_CLOSED_LOOP_REENTRY_RECEIPT_ACTIVATION_LICENSE_READY",
        "v13_27_activation_record_read_allowed": True,
        "v13_0_closed_loop_packet_read_allowed": True,
        "v13_0_candidate_weighting_cycle_state_read_allowed": True,
        "v13_13_receipt_bridge_invoke_allowed": True,
        "v13_1_receipt_ledger_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_13_receipt_bridge_license": bridge_license(),
        "v13_1_receipt_ledger_license": ledger_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_enabled": True,
        "apply_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation(
        runtime_context=context(root),
        v13_28_closed_loop_reentry_receipt_activation_license=license_packet,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare(root, kind)
            result = run(root, activation_license())
            status, action, _ = parts(kind)
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_28_CLOSED_LOOP_REENTRY_RECEIPT_ACTIVATION_READY", (kind, result)
            assert result["activation_status"] == "closed_loop_reentry_receipt_activation_completed"
            assert result["closed_loop_reentry_status"] == status
            assert result["reentry_weighting_action"] == action
            assert result["v13_13_receipt_bridge_invoked"] is True
            assert result["v13_1_receipt_ledger_invoked"] is True
            assert result["receipt_ready_state_written"] is True
            assert result["bridge_ledger_appended"] is True
            assert result["receipt_ledger_appended"] is True
            record = json.loads(
                (root / "physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation_record.json").read_text(encoding="utf-8")
            )
            assert record["activation_status"] == "closed_loop_reentry_receipt_activation_completed"
            assert record["source_v13_13_reentry_receipt_ready_state_digest"]
            assert record["source_v13_1_reentry_receipt_record_digest"]
            assert (root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl").is_file()

        root = base / "digest_mismatch"
        prepare(root, "reinforce", bad_cycle_digest=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_13_receipt_bridge_invoked"] is False
        assert "v13_27_candidate_weighting_cycle_state_digest_mismatch" in result["blockers"]

        root = base / "bad_weighting"
        prepare(root, "reinforce", bad_weighting=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_13_receipt_bridge_invoked"] is True
        assert result["v13_1_receipt_ledger_invoked"] is False
        assert "v13_13_reentry_receipt_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare(root, "reinforce")
        result = run(root, activation_license(v13_1_receipt_ledger_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_13_receipt_bridge_invoked"] is False
        assert result["v13_1_receipt_ledger_invoked"] is False
        assert "v13_1_receipt_ledger_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_28_closed_loop_reentry_receipt_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
