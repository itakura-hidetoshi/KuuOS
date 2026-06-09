#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import os
import pathlib
import time
from typing import Any, Mapping


FEEDBACK_STATUSES = {
    "process_tensor_feedback_reinforce_next_cycle",
    "process_tensor_feedback_hold_context",
    "process_tensor_feedback_block_context",
}
EXPECTED_EXECUTION = {
    "process_tensor_feedback_reinforce_next_cycle": "guarded_transition_executed",
    "process_tensor_feedback_hold_context": "guarded_transition_hold",
    "process_tensor_feedback_block_context": "guarded_transition_block",
}
REQUIRED_PACKET_BOUNDARY_FLAGS = (
    "process_tensor_execution_feedback_only",
    "uses_execution_effects_as_non_markov_feedback",
    "feeds_path_integral_weighting",
    "history_window_feedback_required",
    "memory_kernel_feedback_required",
    "external_backaction_visible",
    "feedback_not_direct_truth",
    "feedback_not_unbounded_execution",
    "runtime_local_feedback_only",
    "fail_closed_on_boundary_loss",
)
REQUIRED_STATE_BOUNDARY_FLAGS = (
    "path_integral_feedback_state_only",
    "non_markov_feedback_preserved",
    "feedback_not_direct_authority",
)
REQUIRED_KERNEL_FLAGS = (
    "non_markov_feedback_required",
    "history_window_feedback_required",
    "instrument_trace_feedback_required",
    "process_tensor_feedback_not_truth",
)
REQUIRED_CONTEXT_KEYS = (
    "process_tensor_digest",
    "memory_kernel_digest",
    "history_window_digest",
    "instrument_trace_digest",
    "non_markov_context_digest",
)


@dataclass(frozen=True)
class PhysicalQuantumQiProcessTensorFeedbackReceiptLedgerResult:
    version: str
    status: str
    packet_id: str
    runtime_root: str
    feedback_status: str
    execution_status: str
    path_weight_delta: int
    memory_feedback_weight: int
    external_backaction_weight: int
    next_cycle_amplitude_delta: int
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


def _validate_packet(packet: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> tuple[dict[str, Any], str, str]:
    if not packet:
        blockers.append("process_tensor_execution_feedback_packet_missing_or_invalid")
        return {}, "process_tensor_feedback_block_context", "guarded_transition_block"
    boundary = _m(packet.get("boundary"))
    for name in REQUIRED_PACKET_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"process_tensor_execution_feedback_boundary_{name}_missing")
    status = str(packet.get("feedback_status", "process_tensor_feedback_block_context"))
    if status not in FEEDBACK_STATUSES:
        blockers.append("process_tensor_feedback_status_invalid")
        status = "process_tensor_feedback_block_context"
    execution_status = str(packet.get("execution_status", "guarded_transition_block"))
    if execution_status != EXPECTED_EXECUTION[status]:
        blockers.append("process_tensor_feedback_execution_status_mismatch")
    kernel = dict(_m(packet.get("process_tensor_feedback_kernel")))
    for name in REQUIRED_KERNEL_FLAGS:
        if kernel.get(name) is not True:
            blockers.append(f"process_tensor_feedback_kernel_{name}_missing")
    context = _validate_context(_m(packet.get("process_tensor_context")), blockers)
    observed = dict(_m(packet.get("observed_effects")))
    if status == "process_tensor_feedback_reinforce_next_cycle":
        if _int(kernel.get("path_weight_delta")) <= 0:
            blockers.append("reinforce_feedback_without_positive_path_weight_delta")
        if _int(kernel.get("memory_feedback_weight")) <= 0:
            blockers.append("reinforce_feedback_without_memory_feedback_weight")
        if _int(kernel.get("external_backaction_weight")) <= 0:
            blockers.append("reinforce_feedback_without_external_backaction_weight")
        if _int(kernel.get("next_cycle_amplitude_delta")) <= 0:
            blockers.append("reinforce_feedback_without_next_cycle_amplitude_delta")
        for key in ("next_cycle_observed", "memory_feedback_observed", "external_backaction_observed"):
            if observed.get(key) is not True:
                blockers.append(f"reinforce_feedback_{key}_not_true")
    else:
        if _int(kernel.get("memory_feedback_weight")) != 0 or _int(kernel.get("external_backaction_weight")) != 0 or _int(kernel.get("next_cycle_amplitude_delta")) != 0:
            blockers.append("hold_or_block_feedback_has_runtime_effect_weight")
    if not packet.get("process_tensor_execution_feedback_digest"):
        warnings.append("process_tensor_execution_feedback_digest_missing")
    payload = {
        "feedback_status": status,
        "execution_status": execution_status,
        "process_tensor_feedback_kernel": kernel,
        "observed_effects": observed,
        "process_tensor_context": context,
        "source_process_tensor_execution_feedback_digest": str(packet.get("process_tensor_execution_feedback_digest", _sha(dict(packet)))),
        "source_execution_record_digest": str(_m(packet.get("source_digests")).get("execution_record", "")),
        "source_next_cycle_state_digest": str(_m(packet.get("source_digests")).get("next_cycle_state", "")),
        "source_memory_consumption_digest": str(_m(packet.get("source_digests")).get("memory_consumption", "")),
        "source_external_state_mutation_digest": str(_m(packet.get("source_digests")).get("external_state_mutation", "")),
    }
    return payload, status, execution_status


def _validate_state(state: Mapping[str, Any], payload: Mapping[str, Any], blockers: list[str]) -> None:
    if not state:
        blockers.append("path_integral_feedback_state_missing_or_invalid")
        return
    if state.get("path_integral_feedback_ready") is not True:
        blockers.append("path_integral_feedback_state_not_ready")
    if str(state.get("feedback_status", "")) != payload.get("feedback_status"):
        blockers.append("path_integral_feedback_state_status_mismatch")
    kernel = _m(payload.get("process_tensor_feedback_kernel"))
    for key in ("path_weight_delta", "memory_feedback_weight", "external_backaction_weight", "next_cycle_amplitude_delta"):
        if _int(state.get(key)) != _int(kernel.get(key)):
            blockers.append(f"path_integral_feedback_state_{key}_mismatch")
    if str(state.get("source_process_tensor_execution_feedback_digest", "")) != str(payload.get("source_process_tensor_execution_feedback_digest", "")):
        blockers.append("path_integral_feedback_state_source_digest_mismatch")
    boundary = _m(state.get("boundary"))
    for name in REQUIRED_STATE_BOUNDARY_FLAGS:
        if boundary.get(name) is not True:
            blockers.append(f"path_integral_feedback_state_boundary_{name}_missing")
    if payload.get("feedback_status") == "process_tensor_feedback_reinforce_next_cycle":
        if boundary.get("can_feed_next_path_integral_cycle") is not True:
            blockers.append("reinforce_feedback_state_cannot_feed_next_path_integral_cycle")
    elif boundary.get("can_feed_next_path_integral_cycle") is True:
        blockers.append("hold_or_block_feedback_state_can_feed_next_path_integral_cycle")


def _record(payload: Mapping[str, Any], prev_digest: str) -> dict[str, Any]:
    kernel = _m(payload.get("process_tensor_feedback_kernel"))
    rec = {
        "version": "physical_quantum_qi_process_tensor_feedback_receipt_record_v12_8",
        "record_type": "physical_quantum_qi_process_tensor_feedback_receipt",
        "feedback_status": str(payload.get("feedback_status", "")),
        "execution_status": str(payload.get("execution_status", "")),
        "path_weight_delta": _int(kernel.get("path_weight_delta")),
        "memory_feedback_weight": _int(kernel.get("memory_feedback_weight")),
        "external_backaction_weight": _int(kernel.get("external_backaction_weight")),
        "next_cycle_amplitude_delta": _int(kernel.get("next_cycle_amplitude_delta")),
        "observed_effects": dict(_m(payload.get("observed_effects"))),
        "process_tensor_context": dict(_m(payload.get("process_tensor_context"))),
        "source_process_tensor_execution_feedback_digest": str(payload.get("source_process_tensor_execution_feedback_digest", "")),
        "source_execution_record_digest": str(payload.get("source_execution_record_digest", "")),
        "source_next_cycle_state_digest": str(payload.get("source_next_cycle_state_digest", "")),
        "source_memory_consumption_digest": str(payload.get("source_memory_consumption_digest", "")),
        "source_external_state_mutation_digest": str(payload.get("source_external_state_mutation_digest", "")),
        "prev_record_digest": prev_digest,
        "boundary": {
            "receipt_ledger_only": True,
            "process_tensor_feedback_receipt_only": True,
            "non_markov_feedback_preserved": True,
            "history_window_feedback_preserved": True,
            "memory_kernel_feedback_preserved": True,
            "external_backaction_visible": True,
            "path_integral_feedback_traceable": True,
            "feedback_not_direct_truth": True,
            "feedback_not_unbounded_execution": True,
            "replayable_receipt": True,
            "fail_closed_on_boundary_loss": True,
        },
        "epoch": int(time.time()),
    }
    rec["record_digest"] = _sha(rec)
    return rec


def build_physical_quantum_qi_process_tensor_feedback_receipt_ledger(
    *,
    runtime_context: Mapping[str, Any],
    process_tensor_feedback_receipt_ledger_license: Mapping[str, Any],
) -> PhysicalQuantumQiProcessTensorFeedbackReceiptLedgerResult:
    ctx = _m(runtime_context)
    lic = _m(process_tensor_feedback_receipt_ledger_license)
    blockers: list[str] = []
    warnings: list[str] = []
    root = _root(ctx.get("runtime_root"), blockers)
    packet_path = root / "physical_quantum_qi_process_tensor_execution_feedback_packet.json"
    state_path = root / "physical_quantum_qi_path_integral_feedback_state.json"
    ledger_path = root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger.jsonl"
    summary_path = root / "physical_quantum_qi_process_tensor_feedback_receipt_summary.json"
    receipt_path = root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger_receipt.json"
    audit_path = root / "physical_quantum_qi_process_tensor_feedback_receipt_ledger_audit.jsonl"

    if ctx.get("physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled") is not True:
        blockers.append("physical_quantum_qi_process_tensor_feedback_receipt_ledger_enabled_not_true")
    if ctx.get("apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger") is not True:
        blockers.append("apply_physical_quantum_qi_process_tensor_feedback_receipt_ledger_not_true")
    if lic.get("license_status") != "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_LICENSE_READY":
        blockers.append("physical_quantum_qi_process_tensor_feedback_receipt_ledger_license_not_ready")
    for name in [
        "process_tensor_execution_feedback_packet_read_allowed",
        "path_integral_feedback_state_read_allowed",
        "receipt_ledger_append_allowed",
        "summary_write_allowed",
        "receipt_write_allowed",
        "audit_append_allowed",
    ]:
        if lic.get(name) is not True:
            blockers.append(name.replace("allowed", "not_allowed"))

    payload, feedback_status, execution_status = _validate_packet(_read_json(packet_path), blockers, warnings)
    _validate_state(_read_json(state_path), payload, blockers)
    record: dict[str, Any] = {}
    summary: dict[str, Any] = {}
    appended = False
    if not blockers:
        record = _record(payload, _last_digest(ledger_path))
        _append_jsonl(ledger_path, record)
        summary = {
            "version": "physical_quantum_qi_process_tensor_feedback_receipt_summary_v12_8",
            "feedback_status": feedback_status,
            "execution_status": execution_status,
            "path_weight_delta": record["path_weight_delta"],
            "memory_feedback_weight": record["memory_feedback_weight"],
            "external_backaction_weight": record["external_backaction_weight"],
            "next_cycle_amplitude_delta": record["next_cycle_amplitude_delta"],
            "latest_record_digest": record["record_digest"],
            "source_process_tensor_execution_feedback_digest": record["source_process_tensor_execution_feedback_digest"],
            "boundary": {
                "summary_only": True,
                "process_tensor_feedback_receipt_only": True,
                "path_integral_feedback_traceable": True,
                "feedback_not_direct_truth": True,
            },
            "epoch": int(time.time()),
        }
        summary["summary_digest"] = _sha(summary)
        _write_json(summary_path, summary)
        appended = True

    status = "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_READY" if not blockers else "PHYSICAL_QUANTUM_QI_PROCESS_TENSOR_FEEDBACK_RECEIPT_LEDGER_BLOCKED"
    packet_id = "physical-quantum-qi-process-tensor-feedback-receipt-" + _sha({"record": record, "blockers": blockers})[:16]
    receipt = {
        "version": "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8",
        "status": status,
        "packet_id": packet_id,
        "feedback_status": feedback_status,
        "execution_status": execution_status,
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
    return PhysicalQuantumQiProcessTensorFeedbackReceiptLedgerResult(
        "kuuos_runtime_daemon_physical_quantum_qi_process_tensor_feedback_receipt_ledger_v12_8",
        status,
        packet_id,
        str(root),
        feedback_status,
        execution_status,
        _int(record.get("path_weight_delta")) if record else 0,
        _int(record.get("memory_feedback_weight")) if record else 0,
        _int(record.get("external_backaction_weight")) if record else 0,
        _int(record.get("next_cycle_amplitude_delta")) if record else 0,
        str(ledger_path),
        str(summary_path),
        str(receipt_path),
        str(audit_path),
        appended,
        blockers,
        warnings,
    )
