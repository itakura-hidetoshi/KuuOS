#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


STATUS_TO_ACTION = {
    "closed_loop_reentry_reinforced": "reinforce_path_weight",
    "closed_loop_reentry_probe_opened": "open_probe_potential",
    "closed_loop_reentry_barrier_added": "add_barrier_potential",
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "closed_loop_path_integral_reentry_only",
    "feeds_candidate_weighting_cycle",
    "uses_process_tensor_feedback",
    "non_markov_feedback_preserved",
    "history_window_feedback_preserved",
    "memory_kernel_feedback_preserved",
    "external_backaction_visible",
    "candidate_weighting_not_truth",
    "closed_loop_reentry_not_unbounded_execution",
    "license_gated_closed_loop",
    "fail_closed_on_boundary_loss",
)
REQUIRED_CYCLE_BOUNDARY_FLAGS = (
    "candidate_weighting_cycle_state_only",
    "closed_loop_reentry_applied",
    "can_feed_next_candidate_weighting_cycle",
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
class PhysicalQuantumQiV13_0ToV13_1ReentryReceiptBridgeResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    bridge_status: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    receipt_ready_state_written: bool
    bridge_ledger_appended: bool
    receipt_ready_state_path: str
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


def _validate_weighting(status: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    norm = _normalize_weighting(weighting)
    if status == "closed_loop_reentry_reinforced":
        if norm["path_weight_delta"] <= 0:
            blockers.append("v13_1_bridge_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_1_bridge_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0 or norm["external_backaction_weight"] <= 0 or norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("v13_1_bridge_reinforce_missing_effect_feedback_weight")
    elif status == "closed_loop_reentry_probe_opened":
        if norm["path_weight_delta"] != 0 or not norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_1_bridge_probe_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_1_bridge_probe_with_effect_feedback_weight")
    elif status == "closed_loop_reentry_barrier_added":
        if norm["path_weight_delta"] != 0 or norm["probe_potential_required"] or not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("v13_1_bridge_barrier_weighting_invalid")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("v13_1_bridge_barrier_with_effect_feedback_weight")
    else:
        blockers.append("closed_loop_reentry_status_invalid")
    return norm


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str]:
    if not packet:
        blockers.append("closed_loop_path_integral_reentry_packet_missing_or_invalid")
        return {}, "closed_loop_reentry_barrier_added", "add_barrier_potential"
    if packet.get("closed_loop_path_integral_reentry_considered") is not True:
        blockers.append("closed_loop_path_integral_reentry_considered_not_true")
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"closed_loop_path_integral_reentry_boundary_{name}_missing")
    status = str(packet.get("closed_loop_reentry_status", "closed_loop_reentry_barrier_added"))
    if status not in STATUS_TO_ACTION:
        blockers.append("closed_loop_reentry_status_invalid")
        status = "closed_loop_reentry_barrier_added"
    action = str(packet.get("reentry_weighting_action", "add_barrier_potential"))
    if action != STATUS_TO_ACTION[status]:
        blockers.append("closed_loop_reentry_action_mismatch")
        action = STATUS_TO_ACTION[status]
    if not packet.get("closed_loop_path_integral_reentry_digest"):
        warnings.append("closed_loop_path_integral_reentry_digest_missing")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(status, _m(packet.get("candidate_weighting")), blockers)
    payload = {
        "closed_loop_reentry_status": status,
        "reentry_weighting_action": action,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_closed_loop_path_integral_reentry_digest": str(packet.get("closed_loop_path_integral_reentry_digest", _sha(dict(packet)))),
        "source_reentry_weighting_state_digest": str(_m(packet.get("source_digests")).get("reentry_weighting_state", "")),
        "source_feedback_to_reentry_weighting_bridge_digest": str(_m(packet.get("source_digests")).get("feedback_to_reentry_weighting_bridge", "")),
    }
    return payload, status, action


def _validate_cycle(cycle: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not cycle:
        blockers.append("candidate_weighting_cycle_state_missing_or_invalid")
        return
    if cycle.get("candidate_weighting_cycle_ready") is not True:
        blockers.append("candidate_weighting_cycle_state_not_ready")
    if str(cycle.get("closed_loop_reentry_status", "")) != payload.get("closed_loop_reentry_status"):
        blockers.append("candidate_weighting_cycle_state_status_mismatch")
    if str(cycle.get("reentry_weighting_action", "")) != payload.get("reentry_weighting_action"):
        blockers.append("candidate_weighting_cycle_state_action_mismatch")
    if _normalize_weighting(_m(cycle.get("candidate_weighting"))) != payload.get("candidate_weighting"):
        blockers.append("candidate_weighting_cycle_state_weighting_mismatch")
    if str(cycle.get("source_closed_loop_path_integral_reentry_digest", "")) != str(payload.get("source_closed_loop_path_integral_reentry_digest", "")):
        blockers.append("candidate_weighting_cycle_state_source_digest_mismatch")
    boundary = _m(cycle.get("boundary"))
    for name in REQUIRED_CYCLE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"candidate_weighting_cycle_state_boundary_{name}_missing")


def build_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge(
    *,
    runtime_context: Mapping[str, Any],
    v13_0_to_v13_1_reentry_receipt_bridge_license: Mapping[str, Any],
) -> PhysicalQuantumQiV13_0ToV13_1ReentryReceiptBridgeResult:
    ctx = _m(runtime_context)
    lic = _m(v13_0_to_v13_1_reentry_receipt_bridge_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json"
    cycle_state_path = root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json"
    ready_state_path = root / "physical_quantum_qi_v13_1_closed_loop_reentry_receipt_ready_state.json"
    bridge_ledger_path = root / "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_summary.json"
    receipt_path = root / "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_receipt.json"
    audit_path = root / "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_audit.jsonl"

    if ctx.get("physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_enabled") is not True:
        blockers.append("physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge") is not True:
        blockers.append("apply_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_LICENSE_READY":
        blockers.append("physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_license_not_ready")
    for name in [
        "v13_0_closed_loop_reentry_packet_read_allowed",
        "v13_0_candidate_weighting_cycle_state_read_allowed",
        "v13_1_reentry_receipt_ready_state_write_allowed",
        "bridge_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, status_value, action = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_cycle(_read_json(cycle_state_path), payload, blockers)
    ready_written = ledger_appended = False
    bridge_status = "v13_0_to_v13_1_reentry_receipt_bridge_block"
    weighting: dict[str, Any] = dict(_m(payload.get("candidate_weighting"))) if payload else {}
    if not blockers:
        epoch = int(time.time())
        bridge_status = "v13_0_to_v13_1_reentry_receipt_bridge_" + status_value.rsplit("_", 1)[-1]
        ready_state = {
            "version": "physical_quantum_qi_v13_1_closed_loop_reentry_receipt_ready_state_v13_13",
            "closed_loop_reentry_receipt_ready_state": True,
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": status_value,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "source_closed_loop_path_integral_reentry_digest": payload["source_closed_loop_path_integral_reentry_digest"],
            "source_reentry_weighting_state_digest": payload["source_reentry_weighting_state_digest"],
            "source_feedback_to_reentry_weighting_bridge_digest": payload["source_feedback_to_reentry_weighting_bridge_digest"],
            "process_tensor_context": dict(payload["process_tensor_context"]),
            "boundary": {
                "v13_1_reentry_receipt_ready_state_only": True,
                "v13_0_closed_loop_packet_required": True,
                "candidate_weighting_cycle_state_required": True,
                "can_feed_v13_1_closed_loop_reentry_receipt_ledger": True,
                "candidate_weighting_cycle_traceable": True,
                "uses_process_tensor_feedback": True,
                "non_markov_feedback_preserved": True,
                "history_window_feedback_preserved": True,
                "memory_kernel_feedback_preserved": True,
                "external_backaction_visible": True,
                "candidate_weighting_not_truth": True,
                "bridge_not_direct_receipt_append": True,
                "does_not_run_receipt_ledger": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ready_state["closed_loop_reentry_receipt_ready_state_digest"] = _sha(ready_state)
        _write_json(ready_state_path, ready_state)
        ready_written = True
        record = {
            "version": "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_record_v13_13",
            "record_type": "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge",
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": status_value,
            "reentry_weighting_action": action,
            "source_closed_loop_reentry_receipt_ready_state_digest": ready_state["closed_loop_reentry_receipt_ready_state_digest"],
            "source_closed_loop_path_integral_reentry_digest": payload["source_closed_loop_path_integral_reentry_digest"],
            "prev_record_digest": _last_digest(bridge_ledger_path),
            "boundary": {
                "bridge_receipt_only": True,
                "v13_1_reentry_receipt_ready_state_traceable": True,
                "candidate_weighting_cycle_traceable": True,
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
            "version": "physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_summary_v13_13",
            "bridge_status": bridge_status,
            "closed_loop_reentry_status": status_value,
            "reentry_weighting_action": action,
            "closed_loop_reentry_receipt_ready_state_digest": ready_state["closed_loop_reentry_receipt_ready_state_digest"],
            "boundary": {
                "summary_only": True,
                "can_feed_v13_1_closed_loop_reentry_receipt_ledger": True,
                "candidate_weighting_cycle_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    final_status = "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_READY" if not blockers else "PHYSICAL_QUANTUM_QI_V13_0_TO_V13_1_REENTRY_RECEIPT_BRIDGE_BLOCKED"
    packet_id = "physical-quantum-qi-v13-0-to-v13-1-reentry-receipt-bridge-" + _sha({"payload": payload, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_v13_13",
        "status": final_status,
        "packet_id": packet_id,
        "bridge_status": bridge_status,
        "closed_loop_reentry_status": status_value,
        "reentry_weighting_action": action,
        "receipt_ready_state_written": ready_written,
        "bridge_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    return PhysicalQuantumQiV13_0ToV13_1ReentryReceiptBridgeResult(
        "kuuos_runtime_daemon_physical_quantum_qi_v13_0_to_v13_1_reentry_receipt_bridge_v13_13",
        final_status,
        packet_id,
        str(root),
        bridge_status,
        status_value,
        action,
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
