#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import pathlib
from typing import Any, Mapping


@dataclass(frozen=True)
class QiAppendOnlyRhythmReceiptLedgerResult:
    ledger_version: str
    ledger_status: str
    ledger_path: str
    append_requested: bool
    ledger_append_performed: bool
    appended_entry_count: int
    prior_entry_count: int
    final_entry_count: int
    prev_entry_digest: str | None
    entry_digest: str | None
    ledger_root_digest: str | None
    receipt_id: str | None
    source_rhythm_layer_status: str | None
    rhythm_bias: str | None
    rhythm_mode: str | None
    cadence_mode: str | None
    process_tensor_pressure_score: float | None
    rhythm_stability_score: float | None
    recommended_window_ticks: int | None
    delegated_completed_tick_count: int | None
    delegated_stop_reason: str | None
    append_only_enforced: bool
    destructive_rewrite_performed: bool
    rhythm_receipt_ledger_only: bool
    memory_write_performed: bool
    memory_append_performed: bool
    memory_overwrite_performed: bool
    world_update_performed: bool
    control_packet_mutation_performed: bool
    probe_execution_performed: bool
    grants_probe_execution_authority: bool
    grants_world_update_authority: bool
    grants_memory_overwrite_authority: bool
    ledger_entry: dict[str, Any]
    ledger_blockers: list[str]
    ledger_warnings: list[str]
    authority: str = "append_only_rhythm_receipt_ledger_only"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _truthy(value: Any) -> bool:
    return value is True or str(value).strip().lower() in {"true", "yes", "1"}


def _int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _sha_obj(value: Mapping[str, Any]) -> str:
    payload = json.dumps(dict(value), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_jsonl(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            out.append(value)
    return out


def _last_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    last = entries[-1]
    digest = last.get("entry_digest")
    if isinstance(digest, str) and digest:
        return digest
    return _sha_obj(last)


def _ledger_root_digest(entries: list[dict[str, Any]]) -> str | None:
    if not entries:
        return None
    material = {"entry_digests": [entry.get("entry_digest") or _sha_obj(entry) for entry in entries]}
    return _sha_obj(material)


def _entry_candidate(rhythm_layer_packet: Mapping[str, Any]) -> dict[str, Any]:
    candidate = rhythm_layer_packet.get("rhythm_entry_candidate")
    if isinstance(candidate, Mapping):
        return dict(candidate)
    return {
        "entry_kind": "rhythm_cadence_history_candidate",
        "projection_only": True,
        "rhythm_mode": rhythm_layer_packet.get("rhythm_mode"),
        "rhythm_bias": rhythm_layer_packet.get("rhythm_bias"),
        "process_tensor_pressure_score": rhythm_layer_packet.get("recent_pressure_mean"),
        "recommended_window_ticks": rhythm_layer_packet.get("delegated_recommended_window_ticks"),
        "delegated_completed_tick_count": rhythm_layer_packet.get("delegated_completed_tick_count"),
        "delegated_stop_reason": rhythm_layer_packet.get("delegated_stop_reason"),
        "cadence_mode": rhythm_layer_packet.get("delegated_cadence_mode"),
        "memory_write_performed": False,
        "memory_append_performed": False,
        "world_update_performed": False,
    }


def append_qi_rhythm_receipt_to_ledger(
    *,
    rhythm_layer_packet: Mapping[str, Any],
    ledger_path: str | pathlib.Path,
    ledger_context: Mapping[str, Any] | None = None,
) -> QiAppendOnlyRhythmReceiptLedgerResult:
    packet = _mapping(rhythm_layer_packet)
    ctx = _mapping(ledger_context)
    blockers: list[str] = []
    warnings: list[str] = []

    if ctx.get("append_only_rhythm_ledger_enabled") is not True:
        blockers.append("append_only_rhythm_ledger_enabled_not_true")
    if ctx.get("jsonl_backend_required") is not True:
        blockers.append("jsonl_backend_required_not_true")
    if ctx.get("append_only_required") is not True:
        blockers.append("append_only_required_not_true")
    if ctx.get("destructive_rewrite_requested") is True:
        blockers.append("destructive_rewrite_requested")
    if ctx.get("request_memory_write") is True or ctx.get("request_memory_append") is True:
        blockers.append("memory_write_or_append_requested")
    if ctx.get("request_world_update") is True:
        blockers.append("world_update_requested")
    if ctx.get("request_probe_execution") is True:
        blockers.append("probe_execution_requested")
    if packet.get("rhythm_layer_status") != "QI_RHYTHM_MEMORY_CADENCE_HISTORY_LAYER_COMPLETED":
        blockers.append("source_rhythm_layer_not_completed")
    if packet.get("rhythm_history_projection_only") is not True:
        blockers.append("source_rhythm_history_not_projection_only")
    if packet.get("rhythm_layer_grants_no_new_authority") is not True:
        blockers.append("source_rhythm_layer_authority_boundary_missing")

    candidate = _entry_candidate(packet)
    for key in ["memory_write_performed", "memory_append_performed", "world_update_performed", "probe_execution_performed"]:
        if key in candidate and candidate.get(key) is not False:
            blockers.append(f"candidate_{key}_not_false")

    path = pathlib.Path(ledger_path)
    entries: list[dict[str, Any]] = []
    parse_ok = True
    try:
        entries = _read_jsonl(path)
    except Exception as exc:  # pragma: no cover - defensive for corrupt ledger files
        parse_ok = False
        blockers.append("ledger_jsonl_parse_failed")
        warnings.append(str(exc))
    prior_count = len(entries) if parse_ok else 0
    prev_digest = _last_digest(entries) if parse_ok else None

    receipt_material = {
        "entry_kind": "qi_rhythm_receipt_ledger_entry_v0_1",
        "source_candidate": candidate,
        "source_rhythm_layer_status": packet.get("rhythm_layer_status"),
        "rhythm_layer_version": packet.get("rhythm_layer_version"),
        "prev_entry_digest": prev_digest,
        "prior_entry_count": prior_count,
        "append_only": True,
        "projection_source_only": True,
        "memory_write_performed": False,
        "memory_append_performed": False,
        "memory_overwrite_performed": False,
        "world_update_performed": False,
        "control_packet_mutation_performed": False,
        "probe_execution_performed": False,
    }
    entry_digest = _sha_obj(receipt_material)
    receipt_id = "qi-rhythm-ledger-" + entry_digest[:16]
    ledger_entry = dict(receipt_material)
    ledger_entry.update({
        "receipt_id": receipt_id,
        "entry_digest": entry_digest,
        "ledger_version": "kuuos_runtime_daemon_qi_append_only_rhythm_receipt_ledger_v0_1",
    })

    append_requested = ctx.get("append_receipt") is not False
    append_performed = False
    if not blockers and append_requested:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(ledger_entry, ensure_ascii=False, sort_keys=True) + "\n")
        append_performed = True

    final_entries = _read_jsonl(path) if path.is_file() and parse_ok else entries
    final_count = len(final_entries)
    root_digest = _ledger_root_digest(final_entries)
    ready = not blockers

    return QiAppendOnlyRhythmReceiptLedgerResult(
        ledger_version="kuuos_runtime_daemon_qi_append_only_rhythm_receipt_ledger_v0_1",
        ledger_status="QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_APPENDED" if ready and append_performed else ("QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_READY" if ready else "QI_APPEND_ONLY_RHYTHM_RECEIPT_LEDGER_BLOCKED"),
        ledger_path=str(path),
        append_requested=append_requested,
        ledger_append_performed=append_performed,
        appended_entry_count=1 if append_performed else 0,
        prior_entry_count=prior_count,
        final_entry_count=final_count,
        prev_entry_digest=prev_digest,
        entry_digest=entry_digest if ready else None,
        ledger_root_digest=root_digest,
        receipt_id=receipt_id if ready else None,
        source_rhythm_layer_status=str(packet.get("rhythm_layer_status")) if packet.get("rhythm_layer_status") else None,
        rhythm_bias=str(candidate.get("rhythm_bias")) if candidate.get("rhythm_bias") else None,
        rhythm_mode=str(candidate.get("rhythm_mode")) if candidate.get("rhythm_mode") else None,
        cadence_mode=str(candidate.get("cadence_mode")) if candidate.get("cadence_mode") else None,
        process_tensor_pressure_score=_float_or_none(candidate.get("process_tensor_pressure_score")),
        rhythm_stability_score=_float_or_none(packet.get("rhythm_stability_score")),
        recommended_window_ticks=_int(candidate.get("recommended_window_ticks"), 0) if candidate.get("recommended_window_ticks") is not None else None,
        delegated_completed_tick_count=_int(candidate.get("delegated_completed_tick_count"), 0) if candidate.get("delegated_completed_tick_count") is not None else None,
        delegated_stop_reason=str(candidate.get("delegated_stop_reason")) if candidate.get("delegated_stop_reason") else None,
        append_only_enforced=True,
        destructive_rewrite_performed=False,
        rhythm_receipt_ledger_only=True,
        memory_write_performed=False,
        memory_append_performed=False,
        memory_overwrite_performed=False,
        world_update_performed=False,
        control_packet_mutation_performed=False,
        probe_execution_performed=False,
        grants_probe_execution_authority=False,
        grants_world_update_authority=False,
        grants_memory_overwrite_authority=False,
        ledger_entry=ledger_entry if ready else {},
        ledger_blockers=blockers,
        ledger_warnings=warnings,
    )
