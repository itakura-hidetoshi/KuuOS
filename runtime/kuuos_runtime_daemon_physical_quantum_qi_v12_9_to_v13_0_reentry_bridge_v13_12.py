#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


ACTION_TO_CLOSED = {
    "reinforce_path_weight": ("reentry_weighting_reinforce", "closed_loop_reentry_reinforced"),
    "open_probe_potential": ("reentry_weighting_hold", "closed_loop_reentry_probe_opened"),
    "add_barrier_potential": ("reentry_weighting_block", "closed_loop_reentry_barrier_added"),
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "feedback_to_reentry_weighting_bridge_only",
    "process_tensor_feedback_required",
    "feeds_next_path_integral_reentry",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "bridge_not_unbounded_execution",
    "license_gated_bridge",
    "fail_closed_on_boundary_loss",
)
REQUIRED_STATE_BOUNDARY_FLAGS = (
    "reentry_weighting_state_only",
    "can_feed_next_path_integral_reentry",
    "non_markov_feedback_preserved",
    "candidate_weighting_not_truth",
    "not_direct_execution_authority",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiV12_9ToV13_0ReentryBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    reentry_weighting_status: str
    reentry_weighting_action: str
    expected_v13_0_closed_loop_reentry_status: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    reentry_ready_state_written: bool
    bridge_ledger_appended: bool
    reentry_ready_state_path: str
    bridge_ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _m(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _root(value: Any, blockers: list[str]) -> pathlib.Path:
    if not value:
        blockers.append("runtime_root_missing")
        return pathlib.Path(".").resolve()
    root = pathlib.Path(str(value)).expanduser().resolve()
    if root == pathlib.Path("/").resolve():
        blockers.append("runtime_root_forbidden")
    return root


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


def _last_digest(path: pathlib.Path) -> str:
    if not path.is_file():
        return "GENESIS"
    latest = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            latest = line
    if not latest:
        return "GENESIS"
    try:
        value = json.loads(latest)
    except json.JSONDecodeError:
        return "CORRUPT_PREVIOUS_LEDGER_LINE"
    return str(value.get("record_digest", _sha(value)))


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _validate_context(ctx: Mapping[str, Any], blockers: list[str]) -> dict[str, str]:
    out = {key: str(ctx.get(key, "")) for key in REQUIRED_CONTEXT_KEYS}
    for key, value in out.items():
        if not value:
            blockers.append(f"process_tensor_context_{key}_missing")
    return out


def _normalize_weighting(weighting: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "path_weight_delta": _int(weighting.get("path_weight_delta")),
        "probe_potential_required": weighting.get("probe_potential_required") is True,
        "barrier_potential_required": weighting.get("barrier_potential_required") is True,
        "barrier_blocks_ready_weight": weighting.get("barrier_blocks_ready_weight") is True,
        "memory_feedback_weight": _int(weighting.get("memory_feedback_weight")),
        "external_backaction_weight": _int(weighting.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _int(weighting.get("next_cycle_amplitude_delta")),
    }


def _validate_weighting(action: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if action == "reinforce_path_weight":
        if norm["path_weight_delta"] <= 0:
            blockers.append("v13_0_reentry_bridge_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_0_reentry_bridge_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("v13_0_reentry_bridge_reinforce_missing_feedback_effect_weight")
    elif action == "open_probe_potential":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_0_reentry_bridge_probe_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_0_reentry_bridge_probe_with_effect_weight")
    elif action == "add_barrier_potential":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_0_reentry_bridge_barrier_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_0_reentry_bridge_barrier_with_effect_weight")
    else:
        blockers.append("v13_0_reentry_bridge_action_invalid")
    return norm


def _validate_packet(packet: Mapping[str, Any], blockers: list[str]) -> None:
    if not packet:
        blockers.append("feedback_to_reentry_weighting_bridge_packet_missing_or_invalid")
        return
    if packet.get("feedback_to_reentry_weighting_bridge_considered") is not True:
        blockers.append("feedback_to_reentry_weighting_bridge_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"feedback_to_reentry_weighting_bridge_boundary_{name}_missing")


def _validate_state(state: Mapping[str, Any], packet: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str, str]:
    if not state:
        blockers.append("reentry_weighting_state_missing_or_invalid")
        return {}, "reentry_weighting_block", "add_barrier_potential", "closed_loop_reentry_barrier_added"
    if state.get("reentry_weighting_state_ready") is not True:
        blockers.append("reentry_weighting_state_not_ready")
    if state.get("can_feed_next_path_integral_reentry") is not True:
        blockers.append("reentry_weighting_state_cannot_feed_next_path_integral_reentry")
    boundary = _m(state.get("boundary"))
    for name in REQUIRED_STATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"reentry_weighting_state_boundary_{name}_missing")
    action = str(state.get("reentry_weighting_action", "add_barrier_potential"))
    if action not in ACTION_TO_CLOSED:
        blockers.append("reentry_weighting_action_invalid")
        action = "add_barrier_potential"
    expected_status, closed_status = ACTION_TO_CLOSED[action]
    status = str(state.get("reentry_weighting_status", ""))
    if status != expected_status:
        blockers.append("reentry_weighting_status_mismatch")
    if packet:
        if str(packet.get("reentry_weighting_action", "")) != action:
            blockers.append("reentry_weighting_packet_action_mismatch")
        if str(packet.get("reentry_weighting_status", "")) != status:
            blockers.append("reentry_weighting_packet_status_mismatch")
        if _normalize_weighting(_m(packet.get("candidate_weighting"))) != _normalize_weighting(_m(state.get("candidate_weighting"))):
            blockers.append("reentry_weighting_packet_state_weighting_mismatch")
        if str(state.get("source_feedback_to_reentry_weighting_bridge_digest", "")) != str(packet.get("feedback_to_reentry_weighting_bridge_digest", "")):
            blockers.append("reentry_weighting_state_source_bridge_digest_mismatch")
    context = _validate_context(_m(state.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(action, _m(state.get("candidate_weighting")), blockers)
    payload = {
        "feedback_status": str(state.get("feedback_status", "")),
        "reentry_weighting_status": status,
        "reentry_weighting_action": action,
        "expected_v13_0_closed_loop_reentry_status": closed_status,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_reentry_weighting_state_digest": str(state.get("reentry_weighting_state_digest", _sha(dict(state)))),
        "source_feedback_to_reentry_weighting_bridge_digest": str(state.get("source_feedback_to_reentry_weighting_bridge_digest", "")),
    }
    return payload, status, action, closed_status


def build_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v12_9_to_v13_0_reentry_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV12_9ToV13_0ReentryBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v12_9_to_v13_0_reentry_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_feedback_to_reentry_weighting_bridge_packet.json"
    state_path = root / "physical_quantum_qi_reentry_weighting_state.json"
    ready_state_path = root / "physical_quantum_qi_v13_0_closed_loop_reentry_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_license_not_ready")
    for name in [
        "v12_9_feedback_to_reentry_weighting_packet_read_allowed",
        "v12_9_reentry_weighting_state_read_allowed",
        "v13_0_closed_loop_reentry_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    packet = _read_json(packet_path)
    _validate_packet(packet, blockers)
    payload, reentry_status, action, closed_status = _validate_state(_read_json(state_path), packet, blockers)
    ready_written = ledger_appended = False
    bridge_status = "v12_9_to_v13_0_reentry_bridge_block"
    weighting: dict[str, Any] = dict(_m(payload.get("candidate_weighting"))) if payload else {}
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v12_9_to_v13_0_reentry_bridge_" + closed_status.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v13_0_closed_loop_reentry_ready_state_v13_12",
            "closed_loop_reentry_ready_state": True,
            "bridge_status": bridge_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "expected_v13_0_closed_loop_reentry_status": closed_status,
            "candidate_weighting": weighting,
            "source_reentry_weighting_state_digest": payload["source_reentry_weighting_state_digest"],
            "source_feedback_to_reentry_weighting_bridge_digest": payload["source_feedback_to_reentry_weighting_bridge_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v13_0_closed_loop_reentry_ready_state_only": True,
                "v12_9_reentry_weighting_state_required": True,
                "can_feed_v13_0_closed_loop_path_integral_reentry": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_reentry_execution": True,
                "does_not_run_closed_loop_reentry": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["closed_loop_reentry_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        ready_written = True
        record = {
            "version": "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_record_v13_12",
            "record_type": "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge",
            "bridge_status": bridge_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "expected_v13_0_closed_loop_reentry_status": closed_status,
            "source_closed_loop_reentry_ready_state_digest": ready_state["closed_loop_reentry_ready_state_digest"],
            "source_reentry_weighting_state_digest": payload["source_reentry_weighting_state_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_0_closed_loop_reentry_ready_state_traceable": True,
                "same_semantic_root": True,
                "uses_process_tensor_feedback": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_execution": True,
                "replayable_receipt": True,
            },
            "epoch": epoch,
        }
        record["record_digest"] = _sha(record)
        _append_jsonl(bridge_ledger_path, record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_summary_v13_12",
            "bridge_status": bridge_status,
            "reentry_weighting_status": reentry_status,
            "reentry_weighting_action": action,
            "expected_v13_0_closed_loop_reentry_status": closed_status,
            "closed_loop_reentry_ready_state_digest": ready_state["closed_loop_reentry_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_0_closed_loop_path_integral_reentry": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V12_9_TO_V13_0_REENTRY_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v12-9-to-v13-0-reentry-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_v13_12",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "reentry_weighting_status": reentry_status,
        "reentry_weighting_action": action,
        "expected_v13_0_closed_loop_reentry_status": closed_status,
        "reentry_ready_state_written": ready_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV12_9ToV13_0ReentryBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v12_9_to_v13_0_reentry_bridge_v13_12",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        reentry_status,
        action,
        closed_status,
        _int(weighting.get("path_weight_delta")),
        weighting.get("probe_potential_required") is True,
        weighting.get("barrier_potential_required") is True,
        ready_written,
        ledger_appended,
        str(ready_state_path),
        str(bridge_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
