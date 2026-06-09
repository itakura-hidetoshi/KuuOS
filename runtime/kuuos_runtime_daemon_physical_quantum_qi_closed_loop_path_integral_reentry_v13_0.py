#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


REENTRY_ACTIONS = {
    "reinforce_path_weight": "closed_loop_reentry_reinforced",
    "open_probe_potential": "closed_loop_reentry_probe_opened",
    "add_barrier_potential": "closed_loop_reentry_barrier_added",
}
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
class PhysicalQuantumQiClosedLoopPathIntegralReentryResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    candidate_weighting_cycle_updated: bool
    closed_loop_ledger_appended: bool
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    closed_loop_packet_path: str
    candidate_weighting_cycle_state_path: str
    closed_loop_ledger_path: str
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
    return str(value.get("closed_loop_reentry_record_digest", _sha(value)))


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


def _validate_weighting(action: str, weighting: Mapping[str, Any], blockers: list[str]) -> dict[str, Any]:
    path_delta = _int(weighting.get("path_weight_delta"))
    probe = weighting.get("probe_potential_required") is True
    barrier = weighting.get("barrier_potential_required") is True
    barrier_blocks = weighting.get("barrier_blocks_ready_weight") is True
    memory_weight = _int(weighting.get("memory_feedback_weight"))
    external_weight = _int(weighting.get("external_backaction_weight"))
    amplitude_delta = _int(weighting.get("next_cycle_amplitude_delta"))
    if action == "reinforce_path_weight":
        if path_delta <= 0:
            blockers.append("closed_loop_reentry_reinforce_without_positive_path_weight_delta")
        if probe or barrier or barrier_blocks:
            blockers.append("closed_loop_reentry_reinforce_with_probe_or_barrier")
        if memory_weight <= 0:
            blockers.append("closed_loop_reentry_reinforce_without_memory_feedback_weight")
        if external_weight <= 0:
            blockers.append("closed_loop_reentry_reinforce_without_external_backaction_weight")
        if amplitude_delta <= 0:
            blockers.append("closed_loop_reentry_reinforce_without_next_cycle_amplitude_delta")
    elif action == "open_probe_potential":
        if path_delta != 0:
            blockers.append("closed_loop_reentry_probe_with_path_weight_delta")
        if not probe:
            blockers.append("closed_loop_reentry_probe_without_probe_potential")
        if barrier or barrier_blocks:
            blockers.append("closed_loop_reentry_probe_with_barrier")
        if memory_weight != 0 or external_weight != 0 or amplitude_delta != 0:
            blockers.append("closed_loop_reentry_probe_with_effect_weight")
    elif action == "add_barrier_potential":
        if path_delta != 0:
            blockers.append("closed_loop_reentry_barrier_with_path_weight_delta")
        if probe:
            blockers.append("closed_loop_reentry_barrier_with_probe")
        if not barrier or not barrier_blocks:
            blockers.append("closed_loop_reentry_barrier_without_blocking_barrier")
        if memory_weight != 0 or external_weight != 0 or amplitude_delta != 0:
            blockers.append("closed_loop_reentry_barrier_with_effect_weight")
    else:
        blockers.append("closed_loop_reentry_action_invalid")
    return {
        "path_weight_delta": path_delta,
        "probe_potential_required": probe,
        "barrier_potential_required": barrier,
        "barrier_blocks_ready_weight": barrier_blocks,
        "memory_feedback_weight": memory_weight,
        "external_backaction_weight": external_weight,
        "next_cycle_amplitude_delta": amplitude_delta,
    }


def _validate_state(state: Mapping[str, Any], blockers: list[str]) -> tuple[dict[str, Any], str, str]:
    if not state:
        blockers.append("reentry_weighting_state_missing_or_invalid")
        return {}, "add_barrier_potential", "closed_loop_reentry_barrier_added"
    if state.get("reentry_weighting_state_ready") is not True:
        blockers.append("reentry_weighting_state_not_ready")
    if state.get("can_feed_next_path_integral_reentry") is not True:
        blockers.append("reentry_weighting_state_cannot_feed_next_path_integral_reentry")
    boundary = _m(state.get("boundary"))
    for name in REQUIRED_STATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"reentry_weighting_state_boundary_{name}_missing")
    action = str(state.get("reentry_weighting_action", "add_barrier_potential"))
    if action not in REENTRY_ACTIONS:
        blockers.append("reentry_weighting_action_invalid")
        action = "add_barrier_potential"
    closed_status = REENTRY_ACTIONS[action]
    context = _validate_context(_m(state.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(action, _m(state.get("candidate_weighting")), blockers)
    payload = {
        "feedback_status": str(state.get("feedback_status", "")),
        "reentry_weighting_status": str(state.get("reentry_weighting_status", "")),
        "reentry_weighting_action": action,
        "closed_loop_reentry_status": closed_status,
        "candidate_weighting": weighting,
        "process_tensor_context": context,
        "source_reentry_weighting_state_digest": str(state.get("reentry_weighting_state_digest", _sha(dict(state)))),
        "source_feedback_to_reentry_weighting_bridge_digest": str(state.get("source_feedback_to_reentry_weighting_bridge_digest", "")),
    }
    return payload, action, closed_status


def build_physical_quantum_qi_closed_loop_path_integral_reentry(
    *,
    runtime_context: Mapping[str, Any],
    closed_loop_path_integral_reentry_license: Mapping[str, Any],
) -> PhysicalQuantumQiClosedLoopPathIntegralReentryResult:
    ctx = _m(runtime_context)
    lic = _m(closed_loop_path_integral_reentry_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    reentry_state_path = root / "physical_quantum_qi_reentry_weighting_state.json"
    closed_loop_packet_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json"
    cycle_state_path = root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json"
    closed_loop_ledger_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_summary.json"
    receipt_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_receipt.json"
    audit_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_audit.jsonl"

    if ctx.get("physical_quantum_qi_closed_loop_path_integral_reentry_enabled") is not True:
        blockers.append("physical_quantum_qi_closed_loop_path_integral_reentry_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_closed_loop_path_integral_reentry") is not True:
        blockers.append("apply_physical_quantum_qi_closed_loop_path_integral_reentry_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_LICENSE_READY":
        blockers.append("physical_quantum_qi_closed_loop_path_integral_reentry_license_not_ready")
    for name in [
        "reentry_weighting_state_read_allowed",
        "closed_loop_reentry_packet_write_allowed",
        "candidate_weighting_cycle_state_write_allowed",
        "closed_loop_reentry_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, action, closed_status = _validate_state(_read_json(reentry_state_path), blockers)
    packet: dict[str, Any] = {}
    cycle_state: dict[str, Any] = {}
    packet_written = cycle_updated = ledger_appended = False
    if not blockers:
        epoch = int(time.time())
        weighting = dict(_m(payload.get("candidate_weighting")))
        packet = {
            "version": "physical_quantum_qi_closed_loop_path_integral_reentry_packet_v13_0",
            "closed_loop_path_integral_reentry_considered": True,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
            "source_digests": {
                "reentry_weighting_state": str(payload.get("source_reentry_weighting_state_digest", "")),
                "feedback_to_reentry_weighting_bridge": str(payload.get("source_feedback_to_reentry_weighting_bridge_digest", "")),
            },
            "boundary": {
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
            },
            "epoch": epoch,
        }
        packet["closed_loop_path_integral_reentry_digest"] = _sha(packet)
        _write_json(closed_loop_packet_path, packet)
        packet_written = True
        cycle_state = {
            "version": "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state_v13_0",
            "candidate_weighting_cycle_ready": True,
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "process_tensor_context": dict(packet["process_tensor_context"]),
            "source_closed_loop_path_integral_reentry_digest": packet["closed_loop_path_integral_reentry_digest"],
            "boundary": {
                "candidate_weighting_cycle_state_only": True,
                "closed_loop_reentry_applied": True,
                "can_feed_next_candidate_weighting_cycle": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "not_direct_execution_authority": True,
            },
            "epoch": epoch,
        }
        cycle_state["candidate_weighting_cycle_state_digest"] = _sha(cycle_state)
        _write_json(cycle_state_path, cycle_state)
        cycle_updated = True
        ledger_record = {
            "version": "physical_quantum_qi_closed_loop_path_integral_reentry_record_v13_0",
            "record_type": "physical_quantum_qi_closed_loop_path_integral_reentry",
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "source_closed_loop_path_integral_reentry_digest": packet["closed_loop_path_integral_reentry_digest"],
            "source_reentry_weighting_state_digest": payload["source_reentry_weighting_state_digest"],
            "prev_record_digest": _last_digest(closed_loop_ledger_path),
            "boundary": {
                "closed_loop_reentry_receipt_only": True,
                "feeds_candidate_weighting_cycle": True,
                "non_markov_feedback_preserved": True,
                "candidate_weighting_not_truth": True,
                "replayable_receipt": True,
                "fail_closed_on_boundary_loss": True,
            },
            "epoch": epoch,
        }
        ledger_record["closed_loop_reentry_record_digest"] = _sha(ledger_record)
        _append_jsonl(closed_loop_ledger_path, ledger_record)
        ledger_appended = True
        summary = {
            "version": "physical_quantum_qi_closed_loop_path_integral_reentry_summary_v13_0",
            "closed_loop_reentry_status": closed_status,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "closed_loop_path_integral_reentry_digest": packet["closed_loop_path_integral_reentry_digest"],
            "candidate_weighting_cycle_state_digest": cycle_state["candidate_weighting_cycle_state_digest"],
            "boundary": {
                "summary_only": True,
                "closed_loop_path_integral_reentry_only": True,
                "feeds_candidate_weighting_cycle": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": epoch,
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)

    status = "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_PATH_INTEGRAL_REENTRY_BLOCKED"
    packet_id = "physical-quantum-qi-closed-loop-path-integral-reentry-" + _sha({"packet": packet, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0",
        "status": status,
        "packet_id": packet_id,
        "closed_loop_reentry_status": closed_status,
        "reentry_weighting_action": action,
        "candidate_weighting_cycle_updated": cycle_updated,
        "closed_loop_ledger_appended": ledger_appended,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    weighting = _m(packet.get("candidate_weighting")) if packet else {}
    return PhysicalQuantumQiClosedLoopPathIntegralReentryResult(
        "kuuos_runtime_daemon_physical_quantum_qi_closed_loop_path_integral_reentry_v13_0",
        status,
        packet_id,
        str(root),
        closed_status,
        action,
        cycle_updated,
        ledger_appended,
        _int(weighting.get("path_weight_delta")),
        weighting.get("probe_potential_required") is True,
        weighting.get("barrier_potential_required") is True,
        str(closed_loop_packet_path),
        str(cycle_state_path),
        str(closed_loop_ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        blockers,
        warnings,
    )
