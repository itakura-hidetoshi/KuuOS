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

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v13_27_closed_loop_reentry_activation import (
    build_physical_quantum_qi_v13_27_closed_loop_reentry_activation,
)

PT = {
    "process_tensor_digest": "pt-v13-27",
    "memory_kernel_digest": "memory-v13-27",
    "history_window_digest": "history-v13-27",
    "instrument_trace_digest": "instrument-v13-27",
    "non_markov_context_digest": "non-markov-v13-27",
}
PACKET_BOUNDARY = {
    "feedback_to_reentry_weighting_bridge_only": True,
    "process_tensor_feedback_required": True,
    "feeds_next_path_integral_reentry": True,
    "non_markov_feedback_preserved": True,
    "history_window_feedback_preserved": True,
    "memory_kernel_feedback_preserved": True,
    "external_backaction_visible": True,
    "candidate_weighting_not_truth": True,
    "bridge_not_unbounded_execution": True,
    "license_gated_bridge": True,
    "fail_closed_on_boundary_loss": True,
}
STATE_BOUNDARY = {
    "reentry_weighting_state_only": True,
    "can_feed_next_path_integral_reentry": True,
    "non_markov_feedback_preserved": True,
    "candidate_weighting_not_truth": True,
    "not_direct_execution_authority": True,
}


def write_json(path: pathlib.Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def parts(kind: str) -> tuple[str, str, str, str, dict[str, Any]]:
    if kind == "reinforce":
        return (
            "process_tensor_feedback_reinforce_next_cycle",
            "reentry_weighting_reinforce",
            "reinforce_path_weight",
            "closed_loop_reentry_reinforced",
            {
                "path_weight_delta": 2,
                "probe_potential_required": False,
                "barrier_potential_required": False,
                "barrier_blocks_ready_weight": False,
                "memory_feedback_weight": 1,
                "external_backaction_weight": 1,
                "next_cycle_amplitude_delta": 1,
            },
        )
    if kind == "probe":
        return (
            "process_tensor_feedback_hold_context",
            "reentry_weighting_hold",
            "open_probe_potential",
            "closed_loop_reentry_probe_opened",
            {
                "path_weight_delta": 0,
                "probe_potential_required": True,
                "barrier_potential_required": False,
                "barrier_blocks_ready_weight": False,
                "memory_feedback_weight": 0,
                "external_backaction_weight": 0,
                "next_cycle_amplitude_delta": 0,
            },
        )
    return (
        "process_tensor_feedback_block_context",
        "reentry_weighting_block",
        "add_barrier_potential",
        "closed_loop_reentry_barrier_added",
        {
            "path_weight_delta": 0,
            "probe_potential_required": False,
            "barrier_potential_required": True,
            "barrier_blocks_ready_weight": True,
            "memory_feedback_weight": 0,
            "external_backaction_weight": 0,
            "next_cycle_amplitude_delta": 0,
        },
    )


def prepare(root: pathlib.Path, kind: str, *, bad_state_digest: bool = False, bad_weighting: bool = False) -> None:
    feedback, weighting_status, action, closed_status, weighting = parts(kind)
    weighting = dict(weighting)
    if bad_weighting and kind == "reinforce":
        weighting["path_weight_delta"] = 0
    bridge_digest = f"v12-9-bridge-{kind}"
    state_digest = f"v12-9-state-{kind}"
    packet = {
        "version": "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet_v12_9",
        "feedback_to_reentry_weighting_bridge_considered": True,
        "feedback_status": feedback,
        "reentry_weighting_status": weighting_status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": dict(PT),
        "source_digests": {
            "process_tensor_feedback_receipt": "feedback-receipt-v13-27",
            "process_tensor_execution_feedback": "feedback-packet-v13-27",
            "execution_record": "execution-v13-27",
        },
        "boundary": dict(PACKET_BOUNDARY),
        "feedback_to_reentry_weighting_bridge_digest": bridge_digest,
        "epoch": 1,
    }
    state = {
        "version": "physical_quantum_qi_reentry_weighting_state_v12_9",
        "reentry_weighting_state_ready": True,
        "feedback_status": feedback,
        "reentry_weighting_status": weighting_status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "can_feed_next_path_integral_reentry": True,
        "source_feedback_to_reentry_weighting_bridge_digest": bridge_digest,
        "process_tensor_context": dict(PT),
        "boundary": dict(STATE_BOUNDARY),
        "reentry_weighting_state_digest": state_digest,
        "epoch": 1,
    }
    activation = {
        "version": "physical_quantum_qi_v13_26_reentry_weighting_activation_record",
        "activation_status": "reentry_weighting_activation_completed",
        "feedback_status": feedback,
        "expected_reentry_weighting_status": weighting_status,
        "observed_reentry_weighting_status": weighting_status,
        "observed_reentry_weighting_action": action,
        "source_v13_25_activation_record_digest": "v13-25-record-v13-27",
        "source_v12_8_feedback_receipt_ready_state_digest": "v12-8-ready-v13-27",
        "source_v12_8_feedback_receipt_record_digest": "v12-8-record-v13-27",
        "source_v12_9_reentry_weighting_state_digest": "wrong-state" if bad_state_digest else state_digest,
        "boundary": {
            "two_stage_reentry_weighting_activation": True,
            "non_markov_feedback_preserved": True,
            "candidate_weighting_not_truth": True,
            "license_gated_reentry_activation": True,
            "not_direct_execution_authority": True,
            "fail_closed_on_boundary_loss": True,
        },
        "reentry_weighting_activation_record_digest": f"v13-26-record-{kind}",
        "epoch": 1,
    }
    write_json(root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json", packet)
    write_json(root / "physical_quantum_qi_reentry_weighting_state.json", state)
    write_json(root / "physical_quantum_qi_v13_26_reentry_weighting_activation_record.json", activation)


def bridge_license() -> dict[str, Any]:
    return {
        "license_status": "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_LICENSE_READY",
        "v12_9_feedback_to_reentry_weighting_packet_read_allowed": True,
        "v12_9_reentry_weighting_state_read_allowed": True,
        "v13_0_closed_loop_reentry_ready_state_write_allowed": True,
        "bridge_ledger_append_allowed": True,
        "summary_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
    }


def closed_loop_license() -> dict[str, Any]:
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


def activation_license(**overrides: Any) -> dict[str, Any]:
    value = {
        "license_status": "PHYSICAL_QUANTUM_QI_V13_27_CLOSED_LOOP_REENTRY_ACTIVATION_LICENSE_READY",
        "v13_26_activation_record_read_allowed": True,
        "v12_9_weighting_packet_read_allowed": True,
        "v12_9_weighting_state_read_allowed": True,
        "v13_12_reentry_bridge_invoke_allowed": True,
        "v13_0_closed_loop_invoke_allowed": True,
        "activation_record_write_allowed": True,
        "receipt_write_allowed": True,
        "audit_append_allowed": True,
        "v13_12_reentry_bridge_license": bridge_license(),
        "v13_0_closed_loop_license": closed_loop_license(),
    }
    value.update(overrides)
    return value


def context(root: pathlib.Path) -> dict[str, Any]:
    return {
        "physical_quantum_qi_v13_27_closed_loop_reentry_activation_enabled": True,
        "apply_physical_quantum_qi_v13_27_closed_loop_reentry_activation": True,
        "runtime_root": str(root),
    }


def run(root: pathlib.Path, license_packet: dict[str, Any]) -> dict[str, Any]:
    return build_physical_quantum_qi_v13_27_closed_loop_reentry_activation(
        runtime_context=context(root),
        v13_27_closed_loop_reentry_activation_license=license_packet,
    ).to_dict()


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = pathlib.Path(directory)
        for kind in ("reinforce", "probe", "barrier"):
            root = base / kind
            prepare(root, kind)
            result = run(root, activation_license())
            _, weighting_status, action, closed_status, _ = parts(kind)
            assert result["status"] == "PHYSICAL_QUANTUM_QI_V13_27_CLOSED_LOOP_REENTRY_ACTIVATION_READY", (kind, result)
            assert result["reentry_weighting_status"] == weighting_status
            assert result["reentry_weighting_action"] == action
            assert result["expected_closed_loop_reentry_status"] == closed_status
            assert result["observed_closed_loop_reentry_status"] == closed_status
            assert result["v13_12_reentry_bridge_invoked"] is True
            assert result["v13_0_closed_loop_invoked"] is True
            assert result["reentry_ready_state_written"] is True
            assert result["candidate_weighting_cycle_updated"] is True
            assert result["closed_loop_ledger_appended"] is True
            cycle = json.loads(
                (root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json").read_text(encoding="utf-8")
            )
            assert cycle["closed_loop_reentry_status"] == closed_status
            assert cycle["reentry_weighting_action"] == action

        root = base / "digest_mismatch"
        prepare(root, "reinforce", bad_state_digest=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_12_reentry_bridge_invoked"] is False
        assert "v13_26_reentry_weighting_state_digest_mismatch" in result["blockers"]

        root = base / "bad_weighting"
        prepare(root, "reinforce", bad_weighting=True)
        result = run(root, activation_license())
        assert result["status"].endswith("BLOCKED")
        assert result["v13_12_reentry_bridge_invoked"] is True
        assert result["v13_0_closed_loop_invoked"] is False
        assert "v13_12_reentry_bridge_not_ready" in result["blockers"]

        root = base / "license_block"
        prepare(root, "reinforce")
        result = run(root, activation_license(v13_0_closed_loop_invoke_allowed=False))
        assert result["status"].endswith("BLOCKED")
        assert result["v13_12_reentry_bridge_invoked"] is False
        assert result["v13_0_closed_loop_invoked"] is False
        assert "v13_0_closed_loop_invoke_not_allowed" in result["blockers"]

    print("physical_quantum_qi_v13_27_closed_loop_reentry_activation checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
