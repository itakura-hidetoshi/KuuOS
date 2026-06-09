#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


CLOSED_LOOP_STATUSES = {
    "closed_loop_reentry_reinforced",
    "closed_loop_reentry_probe_opened",
    "closed_loop_reentry_barrier_added",
}
EXPECTED_ACTION = {
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
class PhysicalQuantumQiClosedLoopReentryReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    closed_loop_reentry_status: str
    reentry_weighting_action: str
    path_weight_delta: int
    probe_potential_required: bool
    barrier_potential_required: bool
    ledger_path: str
    summary_path: str
    receipt_path: str
    audit_path: str
    ledger_appended: bool
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
            blockers.append("closed_loop_receipt_reinforce_without_positive_path_weight_delta")
        if norm["probe_potential_required"] or norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("closed_loop_receipt_reinforce_with_probe_or_barrier")
        if norm["memory_feedback_weight"] <= 0:
            blockers.append("closed_loop_receipt_reinforce_without_memory_feedback_weight")
        if norm["external_backaction_weight"] <= 0:
            blockers.append("closed_loop_receipt_reinforce_without_external_backaction_weight")
        if norm["next_cycle_amplitude_delta"] <= 0:
            blockers.append("closed_loop_receipt_reinforce_without_next_cycle_amplitude_delta")
    elif status == "closed_loop_reentry_probe_opened":
        if norm["path_weight_delta"] != 0:
            blockers.append("closed_loop_receipt_probe_with_path_weight_delta")
        if not norm["probe_potential_required"]:
            blockers.append("closed_loop_receipt_probe_without_probe_potential")
        if norm["barrier_potential_required"] or norm["barrier_blocks_ready_weight"]:
            blockers.append("closed_loop_receipt_probe_with_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("closed_loop_receipt_probe_with_effect_weight")
    elif status == "closed_loop_reentry_barrier_added":
        if norm["path_weight_delta"] != 0:
            blockers.append("closed_loop_receipt_barrier_with_path_weight_delta")
        if norm["probe_potential_required"]:
            blockers.append("closed_loop_receipt_barrier_with_probe")
        if not norm["barrier_potential_required"] or not norm["barrier_blocks_ready_weight"]:
            blockers.append("closed_loop_receipt_barrier_without_blocking_barrier")
        if norm["memory_feedback_weight"] != 0 or norm["external_backaction_weight"] != 0 or norm["next_cycle_amplitude_delta"] != 0:
            blockers.append("closed_loop_receipt_barrier_with_effect_weight")
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
    if status not in CLOSED_LOOP_STATUSES:
        blockers.append("closed_loop_reentry_status_invalid")
        status = "closed_loop_reentry_barrier_added"
    action = str(packet.get("reentry_weighting_action", "add_barrier_potential"))
    if action != EXPECTED_ACTION[status]:
        blockers.append("closed_loop_reentry_action_mismatch")
        action = EXPECTED_ACTION[status]
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    weighting = _validate_weighting(status, _m(packet.get("candidate_weighting")), blockers)
    if not packet.get("closed_loop_path_integral_reentry_digest"):
        warnings.append("closed_loop_path_integral_reentry_digest_missing")
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


def _record(payload: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    rec = {
        "version": "physical_quantum_qi_closed_loop_reentry_receipt_record_v13_1",
        "record_type": "physical_quantum_qi_closed_loop_reentry_receipt",
        "closed_loop_reentry_status": str(payload.get("closed_loop_reentry_status", "")),
        "reentry_weighting_action": str(payload.get("reentry_weighting_action", "")),
        "candidate_weighting": dict(_m(payload.get("candidate_weighting"))),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_closed_loop_path_integral_reentry_digest": str(payload.get("source_closed_loop_path_integral_reentry_digest", "")),
        "source_reentry_weighting_state_digest": str(payload.get("source_reentry_weighting_state_digest", "")),
        "source_feedback_to_reentry_weighting_bridge_digest": str(payload.get("source_feedback_to_reentry_weighting_bridge_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
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
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_closed_loop_reentry_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    closed_loop_reentry_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiClosedLoopReentryReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(closed_loop_reentry_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_closed_loop_path_integral_reentry_packet.json"
    cycle_state_path = root / "physical_quantum_qi_next_path_integral_candidate_weighting_cycle_state.json"
    ledger_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_closed_loop_reentry_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_closed_loop_reentry_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_closed_loop_reentry_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_closed_loop_reentry_receipt_ledger_license_not_ready")
    for name in [
        "closed_loop_reentry_packet_read_allowed",
        "candidate_weighting_cycle_state_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, status_value, action = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_cycle(_read_json(cycle_state_path), payload, blockers)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        weighting = dict(record["candidate_weighting"])
        summary = {
            "version": "physical_quantum_qi_closed_loop_reentry_receipt_summary_v13_1",
            "closed_loop_reentry_status": status_value,
            "reentry_weighting_action": action,
            "candidate_weighting": weighting,
            "latest_record_digest": record["record_digest"],
            "source_closed_loop_path_integral_reentry_digest": record["source_closed_loop_path_integral_reentry_digest"],
            "boundary": {
                "summary_only": True,
                "closed_loop_reentry_receipt_only": True,
                "candidate_weighting_cycle_traceable": True,
                "candidate_weighting_not_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    final_status = "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_CLOSED_LOOP_REENTRY_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-closed-loop-reentry-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1",
        "status": final_status,
        "packet_id": packet_id,
        "closed_loop_reentry_status": status_value,
        "reentry_weighting_action": action,
        "ledger_appended": appended,
        "record_digest": str(record.get("record_digest", "")),
        "summary_digest": _sha(summary),
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
    if lic.get("receipt_write_allowed") is True:
        _write_json(receipt_path, receipt)
    if lic.get("audit_append_allowed") is True:
        _append_jsonl(audit_path, {**receipt, "audit_record_digest": _sha(receipt)})
    weighting = _m(record.get("candidate_weighting")) if record else {}
    return PhysicalQuantumQiClosedLoopReentryReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_closed_loop_reentry_receipt_ledger_v13_1",
        final_status,
        packet_id,
        str(root),
        status_value,
        action,
        _int(weighting.get("path_weight_delta")),
        weighting.get("probe_potential_required") is True,
        weighting.get("barrier_potential_required") is True,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
