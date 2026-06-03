#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiRhythmReceiptLedgerResult:
    ledger_version: str
    ledger_status: str
    receipt_id: str | None
    ledger_path: str
    previous_line_count: int
    appended_line_count: int
    total_line_count: int
    append_only_enforced: bool
    rhythm_entry_candidate_bound: bool
    rhythm_receipt_kind: str
    rhythm_mode: str | None
    rhythm_bias: str | None
    cadence_mode: str | None
    process_tensor_pressure_score: float | None
    rhythm_stability_score: float | None
    recommended_window_ticks: int | None
    delegated_completed_tick_count: int | None
    delegated_stop_reason: str | None
    receipt_packet: dict[str, Any]
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    ledger_blockers: list[str]
    ledger_warnings: list[str]
    authority: str = "append_only_rhythm_receipt_ledger_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _int(value: Any, default: int | None = None) -> int | None:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _float(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _sha(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(dict(payload), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            value = {"_invalid_jsonl_line": line}
        if isinstance(value, dict):
            out.append(value)
    return out


def build_rhythm_receipt(entry_candidate: Mapping[str, Any], context: Mapping[str, Any]) -> dict[str, Any]:
    candidate = dict(entry_candidate)
    material = {
        "entry": candidate,
        "root_id": context.get("root_id"),
        "ledger_scope": context.get("ledger_scope", "qi_rhythm_receipt_ledger"),
    }
    digest = _sha(material)
    return {
        "receipt_version": "qi_rhythm_receipt_ledger_v0_1",
        "receipt_kind": "rhythm_cadence_history_receipt",
        "receipt_id": "qi-rhythm-receipt-" + digest[:16],
        "receipt_digest": digest,
        "root_id": context.get("root_id"),
        "ledger_scope": context.get("ledger_scope", "qi_rhythm_receipt_ledger"),
        "append_only": True,
        "projection_source": "rhythm_entry_candidate",
        "rhythm_mode": candidate.get("rhythm_mode"),
        "rhythm_bias": candidate.get("rhythm_bias"),
        "cadence_mode": candidate.get("cadence_mode"),
        "process_tensor_pressure_score": candidate.get("process_tensor_pressure_score"),
        "rhythm_stability_score": candidate.get("rhythm_stability_score"),
        "recommended_window_ticks": candidate.get("recommended_window_ticks"),
        "delegated_completed_tick_count": candidate.get("delegated_completed_tick_count"),
        "delegated_stop_reason": candidate.get("delegated_stop_reason"),
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
        "grants_probe_execution_authority": False,
        "grants_world_update_authority": False,
        "grants_memory_overwrite_authority": False,
        "source_entry_candidate": candidate,
    }


def append_qi_rhythm_receipt_ledger(
    *,
    rhythm_entry_candidate: Mapping[str, Any],
    ledger_path: str | pathlib.Path,
    ledger_context: Mapping[str, Any] | None = None,
) -> QiRhythmReceiptLedgerResult:
    ctx = _mapping(ledger_context)
    candidate = _mapping(rhythm_entry_candidate)
    path = pathlib.Path(ledger_path)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("rhythm_receipt_ledger_enabled") is not True:
        blockers.append("rhythm_receipt_ledger_enabled_not_true")
    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("request_memory_write") is True:
        blockers.append("request_memory_write")
    if ctx.get("request_memory_overwrite") is True:
        blockers.append("request_memory_overwrite")
    if ctx.get("request_world_update") is True:
        blockers.append("request_world_update")
    if ctx.get("request_probe_execution") is True:
        blockers.append("request_probe_execution")
    if candidate.get("entry_kind") != "rhythm_cadence_history_candidate":
        blockers.append("entry_kind_not_rhythm_cadence_history_candidate")
    if candidate.get("projection_only") is not True:
        blockers.append("candidate_projection_only_not_true")
    for key in ["memory_write_performed", "memory_append_performed", "world_update_performed"]:
        if candidate.get(key) is not False:
            blockers.append(f"candidate_{key}_not_false")

    before = _read_jsonl(path)
    receipt: dict[str, Any] = {}
    appended = 0
    if not blockers:
        receipt = build_rhythm_receipt(candidate, ctx)
        if ctx.get("deduplicate_receipt_id") is True:
            existing = {str(item.get("receipt_id")) for item in before}
            if receipt["receipt_id"] in existing:
                warnings.append("duplicate_receipt_id_skipped")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("a", encoding="utf-8") as handle:
                    handle.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")
                appended = 1
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(receipt, ensure_ascii=False, sort_keys=True) + "\n")
            appended = 1
    after = _read_jsonl(path)
    if len(after) < len(before):
        blockers.append("ledger_line_count_decreased")
    if appended and len(after) != len(before) + appended:
        blockers.append("append_line_count_mismatch")
    ready = not blockers

    return QiRhythmReceiptLedgerResult(
        ledger_version="kuuos_runtime_daemon_qi_rhythm_receipt_ledger_v0_1",
        ledger_status="QI_RHYTHM_RECEIPT_LEDGER_APPENDED" if ready else "QI_RHYTHM_RECEIPT_LEDGER_BLOCKED",
        receipt_id=str(receipt.get("receipt_id")) if receipt.get("receipt_id") else None,
        ledger_path=str(path),
        previous_line_count=len(before),
        appended_line_count=appended if ready else 0,
        total_line_count=len(after),
        append_only_enforced=True,
        rhythm_entry_candidate_bound=bool(candidate),
        rhythm_receipt_kind=str(receipt.get("receipt_kind", "")) if receipt else "",
        rhythm_mode=str(receipt.get("rhythm_mode")) if receipt.get("rhythm_mode") else None,
        rhythm_bias=str(receipt.get("rhythm_bias")) if receipt.get("rhythm_bias") else None,
        cadence_mode=str(receipt.get("cadence_mode")) if receipt.get("cadence_mode") else None,
        process_tensor_pressure_score=_float(receipt.get("process_tensor_pressure_score")) if receipt else None,
        rhythm_stability_score=_float(receipt.get("rhythm_stability_score")) if receipt else None,
        recommended_window_ticks=_int(receipt.get("recommended_window_ticks")) if receipt else None,
        delegated_completed_tick_count=_int(receipt.get("delegated_completed_tick_count")) if receipt else None,
        delegated_stop_reason=str(receipt.get("delegated_stop_reason")) if receipt.get("delegated_stop_reason") else None,
        receipt_packet=receipt,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        ledger_blockers=blockers,
        ledger_warnings=warnings,
    )
