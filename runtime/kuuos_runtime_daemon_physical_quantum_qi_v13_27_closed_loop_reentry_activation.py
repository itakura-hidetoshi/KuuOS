#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping

from runtime.kuuos_runtime_daemon_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_v13_12 import (
    build_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge,
)
from runtime.kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0 import (
    build_physical_quantum_qi_closed_loop_path_integral_reentry,
)

CLOSED_BY_ACTION = {
    "reinforce_path_weight": "closed_loop_reentry_reinforced",
    "open_probe_potential": "closed_loop_reentry_probe_opened",
    "add_barrier_potential": "closed_loop_reentry_barrier_added",
}


@dataclass(frozen=True)
class PhysicalQuantumQiV13_27ClosedLoopReentryActivationResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    activation_status: str
    reentry_weighting_status: str
    reentry_weighting_action: str
    expected_closed_loop_reentry_status: str
    observed_closed_loop_reentry_status: str
    v13_12_reentry_bridge_invoked: bool
    v13_0_closed_loop_invoked: bool
    reentry_ready_state_written: bool
    candidate_weighting_cycle_updated: bool
    closed_loop_ledger_appended: bool
    activation_record_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def _append_jsonl(path: pathlib.Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")


def build_physical_quantum_qi_v13_27_closed_loop_reentry_activation(
    *,
    runtime_context: Mapping[str, Any],
    v13_27_closed_loop_reentry_activation_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_27ClosedLoopReentryActivationResult:
    ctx = _m(runtime_context)
    lic = _m(v13_27_closed_loop_reentry_activation_license)
    blockers: list[str] = []
    warnings: list[str] = []

    root_value = ctx.get("runtime_root")
    root = pathlib.Path(str(root_value)).expanduser().resolve() if root_value else pathlib.Path(".").resolve()
    if not root_value:
        blockers.append("runtime_root_missing")
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")

    source_activation_path = root / "physical_quantum_qi_v13_26_reentry_weighting_activation_record.json"
    weighting_packet_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json"
    weighting_state_path = root / "physical_quantum_qi_reentry_weighting_state.json"
    activation_record_path = root / "physical_quantum_qi_v13_27_closed_loop_reentry_activation_record.json"
    receipt_path = root / "physical_quantum_qi_v13_27_closed_loop_reentry_activation_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_27_closed_loop_reentry_activation_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_27_closed_loop_reentry_activation_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_27_closed_loop_reentry_activation_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_27_closed_loop_reentry_activation") is not True:
        blockers.append("apply_physical_quantum_qi_v13_27_closed_loop_reentry_activation_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_27_CLOSED_LOOP_REENTRY_ACTIVATION_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_27_closed_loop_reentry_activation_license_not_ready")
    for flag in (
        "v13_26_activation_record_read_allowed",
        "v12_9_weighting_packet_read_allowed",
        "v12_9_weighting_state_read_allowed",
        "v13_12_reentry_bridge_invoke_allowed",
        "v13_0_closed_loop_invoke_allowed",
        "activation_record_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ):
        if lic.get(flag) is not True:
            blockers.append(flag.replace("allowed", "not_allowed"))

    source_activation = _read_json(source_activation_path)
    packet = _read_json(weighting_packet_path)
    state = _read_json(weighting_state_path)
    if not source_activation:
        blockers.append("v13_26_reentry_weighting_activation_record_missing_or_invalid")
    if not packet:
        blockers.append("v12_9_reentry_weighting_packet_missing_or_invalid")
    if not state:
        blockers.append("v12_9_reentry_weighting_state_missing_or_invalid")

    action = str(state.get("reentry_weighting_action", "add_barrier_potential"))
    if action not in CLOSED_BY_ACTION:
        blockers.append("v12_9_reentry_weighting_action_invalid")
        action = "add_barrier_potential"
    expected_closed = CLOSED_BY_ACTION[action]
    weighting_status = str(state.get("reentry_weighting_status", "reentry_weighting_block"))

    if source_activation:
        if source_activation.get("activation_status") != "reentry_weighting_activation_completed":
            blockers.append("v13_26_reentry_weighting_activation_not_completed")
        if str(source_activation.get("observed_reentry_weighting_status", "")) != weighting_status:
            blockers.append("v13_26_reentry_weighting_status_mismatch")
        if str(source_activation.get("observed_reentry_weighting_action", "")) != action:
            blockers.append("v13_26_reentry_weighting_action_mismatch")
        source_state_digest = str(source_activation.get("source_v12_9_reentry_weighting_state_digest", ""))
        actual_state_digest = str(state.get("reentry_weighting_state_digest", ""))
        if not source_state_digest or source_state_digest != actual_state_digest:
            blockers.append("v13_26_reentry_weighting_state_digest_mismatch")

    if state:
        if state.get("reentry_weighting_state_ready") is not True:
            blockers.append("v12_9_reentry_weighting_state_not_ready")
        if state.get("can_feed_next_path_integral_reentry") is not True:
            blockers.append("v12_9_reentry_weighting_state_cannot_feed_reentry")
        if str(packet.get("reentry_weighting_action", "")) != action:
            blockers.append("v12_9_packet_state_action_mismatch")
        if str(packet.get("reentry_weighting_status", "")) != weighting_status:
            blockers.append("v12_9_packet_state_status_mismatch")
        source_bridge_digest = str(state.get("source_feedback_to_reentry_weighting_bridge_digest", ""))
        actual_bridge_digest = str(packet.get("feedback_to_reentry_weighting_bridge_digest", ""))
        if not source_bridge_digest or source_bridge_digest != actual_bridge_digest:
            blockers.append("v12_9_packet_state_digest_mismatch")

    v13_12_invoked = False
    v13_0_invoked = False
    bridge_result: dict[str, Any] = {}
    loop_result: dict[str, Any] = {}

    if not blockers:
        bridge_result = build_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge(
            runtime_context={
                "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_enabled": True,
                "apply_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge": True,
                "runtime_root": str(root),
            },
            v12_9_to_v13_0_reentry_bridge_license=dict(_m(lic.get("v13_12_reentry_bridge_license"))),
        ).to_dict()
        v13_12_invoked = True
        if bridge_result.get("status") != "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_READY":
            blockers.append("v13_12_reentry_bridge_not_ready")
        if str(bridge_result.get("expected_v13_0_closed_loop_reentry_status", "")) != expected_closed:
            blockers.append("v13_12_expected_closed_loop_status_mismatch")

    if v13_12_invoked and not blockers:
        loop_result = build_physical_quantum_qi_closed_loop_path_integral_reentry(
            runtime_context={
                "physical_quantum_qi_closed_loop_path_integral_reentry_enabled": True,
                "apply_physical_quantum_qi_closed_loop_path_integral_reentry": True,
                "runtime_root": str(root),
            },
            closed_loop_path_integral_reentry_license=dict(_m(lic.get("v13_0_closed_loop_license"))),
        ).to_dict()
        v13_0_invoked = True
        if loop_result.get("status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY":
            blockers.append("v13_0_closed_loop_reentry_not_ready")
        if str(loop_result.get("closed_loop_reentry_status", "")) != expected_closed:
            blockers.append("v13_0_closed_loop_reentry_status_mismatch")
        if str(loop_result.get("reentry_weighting_action", "")) != action:
            blockers.append("v13_0_reentry_weighting_action_mismatch")

    observed_closed = str(loop_result.get("closed_loop_reentry_status", "closed_loop_reentry_barrier_added"))
    activation_status = (
        "closed_loop_reentry_activation_completed"
        if v13_12_invoked and v13_0_invoked and not blockers
        else "closed_loop_reentry_activation_blocked"
    )

    if v13_12_invoked or v13_0_invoked:
        record = {
            "version": "physical_quantum_qi_v13_27_closed_loop_reentry_activation_record",
            "activation_status": activation_status,
            "reentry_weighting_status": weighting_status,
            "reentry_weighting_action": action,
            "expected_closed_loop_reentry_status": expected_closed,
            "observed_closed_loop_reentry_status": observed_closed,
            "source_v13_26_activation_record_digest": str(
                source_activation.get("reentry_weighting_activation_record_digest", "")
            ),
            "source_v12_9_reentry_weighting_state_digest": str(state.get("reentry_weighting_state_digest", "")),
            "source_v13_12_reentry_ready_state_digest": str(
                _read_json(root / "physical_quantum_qi_v13_0_closed_loop_reentry_ready_state.json").get(
                    "closed_loop_reentry_ready_state_digest", ""
                )
            ),
            "source_v13_0_candidate_weighting_cycle_state_digest": str(
                _read_json(root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json").get(
                    "candidate_weighting_cycle_state_digest", ""
                )
            ),
            "boundary": {
                "two_stage_closed_loop_reentry_activation": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
                "license_gated_closed_loop": True,
                "fail_closed_on_boundary_loss": True,
            },
            "blockers": blockers,
            "epoch": int(time.time()),
        }
        record["closed_loop_reentry_activation_record_digest"] = _sha(record)
        if lic.get("activation_record_write_allowed") is True:
            _write_json(activation_record_path, record)

    status = (
        "PHYSICAL_QUANTUM_QI_V13_27_CLOSED_LOOP_REENTRY_ACTIVATION_READY"
        if v13_12_invoked and v13_0_invoked and not blockers
        else "PHYSICAL_QUANTUM_QI_V13_27_CLOSED_LOOP_REENTRY_ACTIVATION_BLOCKED"
    )
    packet_id = "physical-quantum-qi-v13-27-closed-loop-reentry-activation-" + _sha(
        {"action": action, "observed": observed_closed, "blockers": blockers}
    )[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_27_closed_loop_reentry_activation",
        "status": status,
        "packet_id": packet_id,
        "activation_status": activation_status,
        "reentry_weighting_status": weighting_status,
        "reentry_weighting_action": action,
        "expected_closed_loop_reentry_status": expected_closed,
        "observed_closed_loop_reentry_status": observed_closed,
        "v13_12_reentry_bridge_invoked": v13_12_invoked,
        "v13_0_closed_loop_invoked": v13_0_invoked,
        "reentry_ready_state_written": bridge_result.get("reentry_ready_state_written") is True,
        "candidate_weighting_cycle_updated": loop_result.get("candidate_weighting_cycle_updated") is True,
        "closed_loop_ledger_appended": loop_result.get("closed_loop_ledger_appended") is True,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})

    return PhysicalQuantumQiV13_27ClosedLoopReentryActivationResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_27_closed_loop_reentry_activation",
        status,
        packet_id,
        str(root),
        activation_status,
        weighting_status,
        action,
        expected_closed,
        observed_closed,
        v13_12_invoked,
        v13_0_invoked,
        bridge_result.get("reentry_ready_state_written") is True,
        loop_result.get("candidate_weighting_cycle_updated") is True,
        loop_result.get("closed_loop_ledger_appended") is True,
        str(activation_record_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
